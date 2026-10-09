# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..audio_data.protocols import AudioData
from ..models import Chapter, Segment


@runtime_checkable
class Cutter(Protocol):
    """
    A protocol defining an audio cutting component.

    A Cutter splits audio data into physical segments based on
    chapter boundaries provided as input.

    It may perform internal preprocessing or postprocessing
    required to complete the cutting operation, but it does not
    handle file I/O operations or data persistence.

    Contract guarantees:
    - Each input Chapter results in exactly one Segment in output.
    - Segment.audio corresponds to audio sliced between
      chapter.start_ms and chapter.end_ms.
    - Returned segments are sorted by chapter.start_ms.
    - The operation is independent of the input order of chapters;
      implementations must correctly handle unsorted chapter lists
      and produce the same logical result as if chapters were sorted
      by chapter.start_ms prior to processing.

    Non-guarantees (implementation-defined):
    - Handling of overlapping chapters
    - Handling of gaps between chapters
    - Requirement for full audio coverage
    - Validation strictness

    Implementations may raise CutterError for invalid input.
    """

    def cut(self, audio: AudioData, chapters: list[Chapter]) -> list[Segment]:
        """
        Cut audio data into segments according to provided chapter boundaries.

        Args:
          - audio (AudioData): Source audio data to be cut.
          - chapters (list[Chapter]): Chapter definitions specifying
            time boundaries for each segment.

        Returns:
          - list[Segment]: A list of audio segments produced from the source audio.

        Raises:
          - CutterError: If cutting fails or the input data is invalid.

        Semantic details:
          - operation must not mutate the provided audio object
            or the list of chapter definitions
          - the operation must not depend on the input order of chapters
          - the result is sorted by chapter.start_ms
          - should return [] if provided list of chapters is empty
        """
        ...
