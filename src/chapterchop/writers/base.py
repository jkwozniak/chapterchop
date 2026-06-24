# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from chapterchop.models import Segment


@runtime_checkable
class Writer(Protocol):
    """
    A protocol defining a component responsible for exporting
    audio segments as files.

    A Writer receives already prepared audio segments and
    persists them to the local filesystem.

    It does not perform audio analysis or audio cutting.

    Implementations may define their own:
    - output format,
    - filename generation strategy,
    - directory layout,
    - export configuration.

    Contract guarantees:
    - One output file is created for each input Segment.
    - Returned paths correspond to created output files.

    Implementations may raise WriterError for invalid input
    or export failures.
    """

    def write(self, segments: list[Segment]) -> list[Path]:
        """
        Write audio segments to the configured output destination.

        Args:
          - segments (list[Segment]): Audio segments to be written.

        Returns:
          - list[Path]: Paths to the created audio files.

        Raises:
          - WriterError: If writing fails or the input data is invalid.

        Semantic details:
          - operations must not mutate provided Segment objects
          - for empty segments list should return []
        """
        ...
