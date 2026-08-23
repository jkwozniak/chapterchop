# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from chapterchop.models import ChapterEntry, ChapterList


def make_chapter_entry(start_ms: int, title: str | None = None) -> ChapterEntry:
    return ChapterEntry(start_ms=start_ms, title=title)


def make_chapter_list(
    *entries: tuple[int, str | None],
) -> ChapterList:
    return ChapterList(
        entries=tuple(
            make_chapter_entry(start_ms, title) for start_ms, title in entries
        )
    )
