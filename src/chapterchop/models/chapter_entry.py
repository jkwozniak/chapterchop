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
    - instances violating the above invariants are considered invalid
      and shouldand should raise InvalidChapterEntryError when detected.
    """

    start_ms: int
    title: str | None = None
