# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import pytest

from chapterchop.clf_parser import ClfParser
from chapterchop.models.chapter_entry import ChapterEntry
from chapterchop.models.chapter_list import ChapterList
from tests.support.factories.clf_texts import (
    make_valid_timestamp_only_text,
    make_valid_timestamp_with_titles_text,
)


@pytest.fixture
def parser() -> ClfParser:
    return ClfParser()


@pytest.mark.unit
def test_parse_text_returns_chapter_list_for_timestamp_only_text(
    parser: ClfParser,
) -> None:
    text = make_valid_timestamp_only_text()

    result = parser.parse_text(text)

    assert isinstance(result, ChapterList)
    assert result.entries == (
        ChapterEntry(start_ms=0, title=None),
        ChapterEntry(start_ms=5_000, title=None),
        ChapterEntry(start_ms=10_000, title=None),
    )


@pytest.mark.unit
def test_parse_text_returns_chapter_list_for_timestamp_with_titles(
    parser: ClfParser,
) -> None:
    text = make_valid_timestamp_with_titles_text()

    result = parser.parse_text(text)

    assert isinstance(result, ChapterList)
    assert result.entries == (
        ChapterEntry(start_ms=0, title="Intro"),
        ChapterEntry(start_ms=5_000, title="Prerequisites"),
        ChapterEntry(start_ms=10_000, title="Bonus Track"),
    )
