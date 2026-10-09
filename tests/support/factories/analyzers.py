# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from support.factories.chapter_lists import make_chapter_list

from chapterchop.analyzers import (
    Analyzer,
    ChapterListAnalyzer,
    EvenSplitAnalyzer,
)


def make_chapter_list_analyzer() -> Analyzer:
    chapter_list = make_chapter_list((0, "First"), (30, "Second"), (60, "Third"))
    return ChapterListAnalyzer(chapter_list=chapter_list)


def make_even_split_analyzer() -> Analyzer:
    return EvenSplitAnalyzer(parts=4)
