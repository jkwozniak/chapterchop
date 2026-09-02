# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChapterEntry:
    """
    Logical representation of a single entry from an external chapter list.

    Specifies the starting position, expressed in milliseconds,
    of a logical chapter in the source audio material.
    End positions are intentionally omitted and are derived later
    by components that interpret the surrounding ChapterList.

    A ChapterEntry has no complete meaning on its own.
    It should always be interpreted as part of a ChapterList.

    Semantic details:
    - start_ms >= 0
    - title is None or non-empty string
    """

    start_ms: int
    title: str | None = None

    def __post_init__(self) -> None:
        if self.start_ms < 0:
            raise ValueError("Chapter start cannot be negative.")
        if self.title == "":
            raise ValueError("Chapter title cannot be an empty string.")
