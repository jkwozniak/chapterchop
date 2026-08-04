# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from chapterchop.models import Chapter

# ---------------------------------------------------------------------------
# Multi-purpose chapter factories
# ---------------------------------------------------------------------------


def make_chapter(
    start_ms: int,
    end_ms: int,
    *,
    title: str | None = None,
    metadata: dict[str, object] | None = None,
) -> Chapter:
    return Chapter(
        start_ms=start_ms,
        end_ms=end_ms,
        title=title,
        metadata=metadata,
    )


def make_chapters(
    *ranges: tuple[int, int],
    title_prefix: str | None = None,
) -> list[Chapter]:
    """
    Creates multiple chapters. Usage:
    `make_chapters((0, 10), (10, 20), title_prefix="ch")`
    """
    chapters = []

    for i, (start, end) in enumerate(ranges, start=1):
        title = f"{title_prefix}_{i}" if title_prefix else None
        chapters.append(Chapter(start, end, title=title))

    return chapters


# ---------------------------------------------------------------------------
# Valid chapters
# ---------------------------------------------------------------------------


def make_full_coverage(duration: int) -> list[Chapter]:  # 2 chapters
    return [
        Chapter(0, duration // 2),
        Chapter(duration // 2, duration),
    ]


def make_full_coverage_multiple_chapters(  # N chapters
    duration: int, parts: int = 4
) -> list[Chapter]:
    step = duration // parts
    return make_chapters(
        *[
            (i * step, (i + 1) * step if i < parts - 1 else duration)
            for i in range(parts)
        ]
    )


def make_single(duration: int) -> list[Chapter]:
    return [Chapter(0, duration)]


# ---------------------------------------------------------------------------
# Invalid chapters
# ---------------------------------------------------------------------------


def make_invalid_range() -> list[Chapter]:
    return [Chapter(10, 5)]


def make_out_of_bounds(duration: int) -> list[Chapter]:
    return [Chapter(0, duration + 1)]


# ---------------------------------------------------------------------------
# Edge-cases
# ---------------------------------------------------------------------------


def make_duplicate_start(duration: int) -> list[Chapter]:
    return [
        Chapter(0, duration // 2),
        Chapter(0, duration),
    ]


def make_missing_start_zero(duration: int) -> list[Chapter]:
    return [Chapter(10, duration)]


def make_not_full_coverage(duration: int) -> list[Chapter]:
    return [Chapter(0, duration - 1)]


def make_with_gap(duration: int) -> list[Chapter]:
    mid = duration // 2

    return [
        Chapter(0, mid),
        Chapter(mid + 1, duration),
    ]


def make_with_overlap(duration: int) -> list[Chapter]:
    return [
        Chapter(0, duration // 2 + 10),
        Chapter(duration // 2, duration),
    ]
