# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from operator import attrgetter

from chapterchop.audio_data.protocols import AudioData
from chapterchop.cutters.base import Cutter
from chapterchop.exceptions import (
    ChapterGapError,
    ChapterOutOfBoundsError,
    ChapterOverlapError,
    CutterError,
    InvalidChapterError,
    NonFullCoverageError,
)
from chapterchop.models import Chapter, Segment


class SimpleCutter(Cutter):
    """
    Strict reference implementation of the Cutter protocol.

    - validates chapters
    - sorts by start_ms
    - performs direct AudioData slicing

    It enforces:
    - non-overlapping chapters
    - no gaps between chapters
    - full coverage of the audio

    SimpleCutter is intended as:
    - a correctness baseline
    - a reference for contract behavior

    It is NOT intended to handle more complex real-world input.
    """

    def cut(self, audio: AudioData, chapters: list[Chapter]) -> list[Segment]:
        """
        Cut audio into segments according to provided chapter bounds.

        Args:
          - audio (AudioData): Source audio to be cut.
          - chapters (list[Chapter]): List of chapters to be extracted
                from the source material.

        Returns:
          - list[Segment]: A list of audio segments produced from the source audio.

        Raises:
          - CutterError: If input audio is invalid or
                slicing audio fails.
          - ChapterOutOfBoundsError: If any of the chapters exceeds
                the audio duration.
          - ChapterOverlapError: If two or more chapters share the same
                part of source audio.
          - InvalidChapterError: If any of the chapters has invalid values
                of start_ms or end_ms.
        """

        if not chapters:
            return []

        try:
            duration = audio.duration_ms
        except Exception as exc:
            raise CutterError("Invalid input audio.") from exc

        chapters_sorted = self._validate_and_sort(chapters, duration)

        segments: list[Segment] = []
        for chapter in chapters_sorted:
            try:
                sliced_audio = audio.slice(
                    chapter.start_ms,
                    chapter.end_ms,
                )
            except Exception as exc:
                raise CutterError(
                    f"Failed to slice audio for chapter:"
                    f"[{chapter.start_ms}; {chapter.end_ms}]."
                ) from exc

            segments.append(
                Segment(
                    audio=sliced_audio,
                    chapter=chapter,
                )
            )
        return segments

    def _validate_and_sort(
        self,
        chapters: list[Chapter],
        duration_ms: int,
    ) -> list[Chapter]:
        self._validate_chapter_boundaries(chapters, duration_ms)
        chapters_sorted = sorted(chapters, key=attrgetter("start_ms"))
        self._validate_continuity(chapters_sorted, duration_ms)

        return chapters_sorted

    def _validate_chapter_boundaries(
        self,
        chapters: list[Chapter],
        duration_ms: int,
    ) -> None:
        """
        Validate individual chapter constraints:
        - non-negative start
        - end > start
        - end within audio duration
        - unique start_ms
        """

        seen_starts: set[int] = set()

        for chapter in chapters:
            if chapter.start_ms in seen_starts:
                raise ChapterOverlapError(
                    f"Duplicate chapter start_ms detected: {chapter.start_ms}."
                )
            seen_starts.add(chapter.start_ms)

            if chapter.start_ms < 0:
                raise InvalidChapterError(
                    f"Chapter start_ms must be >= 0 (got: {chapter.start_ms})."
                )

            if chapter.end_ms <= chapter.start_ms:
                raise InvalidChapterError(
                    f"Invalid chapter range:"
                    f"[start_ms={chapter.start_ms}; end_ms={chapter.end_ms}]"
                )

            if chapter.end_ms > duration_ms:
                raise ChapterOutOfBoundsError(
                    f"Chapter 'end_ms': ({chapter.end_ms}) exceeds"
                    f"audio duration: ({duration_ms})."
                )

    def _validate_continuity(
        self,
        chapters_sorted: list[Chapter],
        duration_ms: int,
    ) -> None:
        """
        Validate relationships between chapters:
        - full coverage (start at 0, end at audio duration)
        - no overlaps
        - no gaps
        """

        if chapters_sorted[0].start_ms != 0:
            raise NonFullCoverageError(
                f"First chapter must start at 0 (got: {chapters_sorted[0].start_ms})."
            )

        if chapters_sorted[-1].end_ms != duration_ms:
            raise NonFullCoverageError(
                f"Last chapter must end at audio duration"
                f"(got: {chapters_sorted[-1].end_ms}, expected: {duration_ms})."
            )

        for prev, curr in zip(chapters_sorted, chapters_sorted[1:], strict=False):
            if curr.start_ms < prev.end_ms:
                raise ChapterOverlapError(
                    f"Chapters overlap:"
                    f"[{prev.start_ms}; {prev.end_ms}]"
                    f"[{curr.start_ms}; {curr.end_ms}]"
                )

            if curr.start_ms > prev.end_ms:
                raise ChapterGapError(
                    f"Gap between chapters:"
                    f"[{prev.start_ms}; {prev.end_ms}]"
                    f"[{curr.start_ms}; {curr.end_ms}]"
                )
