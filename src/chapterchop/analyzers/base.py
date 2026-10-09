# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..audio_data.protocols import AudioData
from ..models import Chapter


@runtime_checkable
class Analyzer(Protocol):
    """
    A protocol defining an audio analysis component.

    An Analyzer inspects audio data and produces a list of Chapter
    objects describing time ranges of interest.

    Implementations may use arbitrary strategies (e.g. silence detection,
    fixed splits, external metadata) and may optionally attach additional
    chapter metadata such as titles or tags.

    Contract guarantees:
    - returned value is a list of Chapter objects
    - valid time boundaries for each Chapter:
        * start_ms >= 0
        * start_ms < end_ms
        * end_ms <= audio.duration_ms

    Non-guarantees (implementation-defined):
    - full coverage of the audio
    - absence of gaps between chapters
    - absence of overlaps between chapters
    - number of returned chapters

    An Analyzer does not perform audio cutting or persistence.
    """

    def analyze(self, audio: AudioData) -> list[Chapter]:
        """
        Analyze audio data and produce chapter definitions.

        Args:
          - audio (AudioData): Audio material to be analyzed.

        Returns:
          - list[Chapter]: A list of detected chapters.

        Raises:
          - AnalyzerError: If input is invalid or cannot be
            meaningfully analyzed.

        Semantic details:
          - operation must not mutate the provided audio object
          - the result should be deterministic for the same input
          - may return an empty list if no relevant segments are found
        """
        ...
