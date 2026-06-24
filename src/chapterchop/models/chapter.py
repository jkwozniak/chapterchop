# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from dataclasses import dataclass


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
    metadata: dict[str, object] | None = None
