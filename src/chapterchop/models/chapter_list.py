# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from dataclasses import dataclass

from .chapter_entry import ChapterEntry


@dataclass(frozen=True, slots=True)
class ChapterList:
    """
    Logical representation of the external list of chapters
    describing the content of an audio recording.

    Serves as an alternative to audio analysis as a basis
    for determining chapter boundaries.

    Stores an immutable, sorted collection of ChapterEntry objects.
    A ChapterList describes only the start positions of chapters.
    Chapter boundaries are derived later by components interpreting the list.

    Semantic details:
    - chapter entries are sorted in ascending order by start_ms
    - each chapter entry must have a unique start_ms value
    """

    entries: tuple[ChapterEntry, ...]

    def __post_init__(self) -> None:
        previous_start_ms: int | None = None
        for entry in self.entries:
            if previous_start_ms is not None and entry.start_ms <= previous_start_ms:
                raise ValueError(
                    "Chapter entries must be sorted by start_ms "
                    "and have unique timestamps."
                )
            previous_start_ms = entry.start_ms
