# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from ..audio_data.protocols import AudioData
from ..exceptions import (
    AnalyzerError,
    ChapterListOutOfBoundsError,
)
from ..models import Chapter, ChapterList
from .base import Analyzer


class ChapterListAnalyzer(Analyzer):
    """
    An implementation of the Analyzer protocol that uses a provided
    ChapterList to determine chapter boundaries instead of analyzing
    the audio content.

    Specification:
      - analyzed audio must have a duration greater than 0 ms,
      - exactly one Chapter is created for each ChapterEntry,
      - returned chapters preserve the order of the ChapterList entries,
      - returned chapters are contiguous and non-overlapping,
      - each returned chapter has a duration of at least 1 ms.

    The first ChapterEntry does not have to start at 0 ms. Consequently,
    the returned chapters may not cover the section of the audio before
    the first ChapterEntry.

    This analyzer does not:
      - add a chapter for the section before the first entry,
      - add a chapter after the last entry,
      - combine entries,
      - skip entries,
      - add or modify titles,
      - require full audio coverage,
      - analyze the content of the audio signal.

    Runtime validation:
      - the last ChapterEntry must start before the end of the audio
        being analyzed
    """

    _chapter_list: ChapterList

    def __init__(self, chapter_list: ChapterList) -> None:
        self._chapter_list = chapter_list

    def __repr__(self) -> str:
        return f"{type(self).__name__}(chapter_list={self._chapter_list!r})"

    def analyze(self, audio: AudioData) -> list[Chapter]:
        """
        Determine chapter boundaries based on the provided ChapterList.

        Args:
          - audio (AudioData): Source audio data to analyze.

        Returns:
          - list[Chapter]: A sorted list of contiguous Chapter objects.

        Raises:
          - AnalyzerError: If the audio duration is not greater than 0 ms.
          - ChapterListOutOfBoundsError: If the last ChapterEntry starts
            at or after the end of the audio.

        Semantic details:
          - exactly one Chapter is created for each ChapterEntry
          - ChapterEntry.start_ms defines Chapter.start_ms
          - Chapter.end_ms is equal to the start_ms of the next
            ChapterEntry; for the last Chapter, it is equal to
            audio.duration_ms
          - ChapterEntry.title defines Chapter.title
          - if ChapterList is empty, an empty list is returned
          - the returned chapters do not cover any audio before the
            first ChapterEntry
          - the source AudioData is not modified
        """
        try:
            duration = audio.duration_ms
        except Exception as exc:
            raise AnalyzerError("Invalid input audio.") from exc

        if duration <= 0:
            raise AnalyzerError("Audio duration must be greater than 0.")

        if not self._chapter_list.entries:
            return []

        last_entry = self._chapter_list.entries[-1]
        if last_entry.start_ms >= duration:
            raise ChapterListOutOfBoundsError(
                "Chapter list contains an entry outside the audio duration."
            )

        chapters: list[Chapter] = []
        for index, entry in enumerate(self._chapter_list.entries):
            end_ms = (
                self._chapter_list.entries[index + 1].start_ms
                if index + 1 < len(self._chapter_list.entries)
                else duration
            )
            chapters.append(
                Chapter(
                    start_ms=entry.start_ms,
                    end_ms=end_ms,
                    title=entry.title,
                )
            )

        return chapters
