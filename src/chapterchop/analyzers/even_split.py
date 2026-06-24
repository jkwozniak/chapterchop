# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from chapterchop.analyzers.base import Analyzer
from chapterchop.audio_data.protocols import AudioData
from chapterchop.exceptions import AnalyzerError
from chapterchop.models import Chapter


class EvenSplitAnalyzer(Analyzer):
    """
    A simple reference implementation of the Analyzer protocol.

    This analyzer divides the input audio into a configurable
    number of contiguous chapters of approximately equal duration.
    If the duration is not evenly divisible by the number of parts,
    the remaining milliseconds are added to the final chapter.

    The implementation is fully deterministic and intended primarily as:
    - a correctness baseline,
    - a reference implementation of the Analyzer contract,
    - a predictable component for testing and educational purposes.

    Guarantees:
    - returns a non-empty list of chapters
    - chapters are contiguous and non-overlapping
    - chapters fully cover the audio duration
    - returned chapters are sorted by start_ms
    - each chapter has a duration of at least 1 ms

    Runtime validation:
    - analyzed audio duration must be greater than 0

    Not intended for real-world audio analysis.
    """

    _parts: int

    def __init__(self, parts: int) -> None:
        """
        Initialize the analyzer.

        Args:
          - parts (int): Number of chapters to generate from the input audio.

        Configuration constraints:
          - parts must be greater than or equal to 1
          - parts must not exceed the analyzed audio duration
            to ensure that every chapter has a minimum duration
            of at least 1 ms

        Raises:
          - ValueError: If parts is less than 1.
        """

        self._parts = parts

        if parts < 1:
            raise ValueError("'parts' must be >= 1.")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(parts={self._parts!r})"

    def analyze(self, audio: AudioData) -> list[Chapter]:
        """
        Analyze audio data and divide it into evenly sized chapters.

        Args:
          - audio: Source audio data to analyze.

        Returns:
          - list[Chapter]: A list of contiguous Chapter objects covering
            the entire audio duration.

        Raises:
          - AnalyzerError: If analysis fails or the input audio is invalid.

        Semantic details:
          - returned chapters are sorted by start_ms
          - chapter boundaries are deterministic for identical input audio
            and analyzer configuration
        """

        try:
            duration = audio.duration_ms
        except Exception as exc:
            raise AnalyzerError("Invalid input audio.") from exc

        if duration <= 0:
            raise AnalyzerError("Audio duration must be greater than 0.")

        if self._parts > duration:
            raise AnalyzerError(
                "Number of parts cannot exceed audio duration in milliseconds."
            )

        step = duration // self._parts

        chapters: list[Chapter] = []
        for i in range(self._parts):
            start = i * step
            end = (i + 1) * step if i < self._parts - 1 else duration
            chapters.append(Chapter(start, end))

        return chapters
