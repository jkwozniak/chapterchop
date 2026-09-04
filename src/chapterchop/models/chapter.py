# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from dataclasses import dataclass

from frozendict import frozendict


@dataclass(frozen=True, slots=True)
class Chapter:
    """
    Logical representation of a chapter.

    Stores information about the start and end timestamps of the fragment
    in the source audio material and optional metadata.
    Does not contain the audio data itself.

    The value of 'start_ms' must be greater than or equal to 0
    and less than 'end_ms'.
    """

    start_ms: int
    end_ms: int
    title: str | None = None
    metadata: frozendict[str, str] = frozendict()

    def __post_init__(self) -> None:
        if self.start_ms < 0:
            raise ValueError("Chapter start_ms cannot be negative.")
        if self.end_ms <= self.start_ms:
            raise ValueError("Chapter end_ms must be greater than start_ms.")
