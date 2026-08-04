# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import textwrap

import pytest

from chapterchop import ClfParser
from chapterchop.models import ChapterEntry
from tests.support.assets.registry import ClfAsset
from tests.support.factories.clf_texts import (
    make_invalid_trailing_whitespace_text,
    make_valid_timestamp_only_text,
    make_valid_timestamp_with_titles_text,
)


@pytest.fixture
def parser() -> ClfParser:
    return ClfParser()


@pytest.mark.unit
def test_parse_text_removes_trailing_whitespace_before_parsing(
    parser: ClfParser,
) -> None:
    text = make_invalid_trailing_whitespace_text()

    result = parser.parse_text(text)

    assert result.entries == (ChapterEntry(start_ms=0, title="Intro"),)


@pytest.mark.unit
def test_parse_text_sets_title_to_none_for_timestamp_only_line(
    parser: ClfParser,
) -> None:
    text = make_valid_timestamp_only_text()

    result = parser.parse_text(text)

    for entry in result.entries:
        assert entry.title is None


@pytest.mark.unit
def test_parse_text_preserves_title_for_timestamp_with_separator(
    parser: ClfParser,
) -> None:
    text = make_valid_timestamp_with_titles_text()

    result = parser.parse_text(text)

    assert result.entries == (
        ChapterEntry(start_ms=0, title="Intro"),
        ChapterEntry(start_ms=5_000, title="Prerequisites"),
        ChapterEntry(start_ms=10_000, title="Bonus Track"),
    )


@pytest.mark.unit
def test_parse_text_produces_same_chapter_lists_for_equivalent_clfs(
    parser: ClfParser,
) -> None:
    first_text = textwrap.dedent("""\
        0:00 Intro
        1:00 Chapter 1
        2:00 Chapter 2
        3:00 Summary
    """)
    second_text = textwrap.dedent("""\
        0:00 - Intro
        01:00 - Chapter 1
        02:00 - Chapter 2
        03:00 - Summary
    """)

    first_result = parser.parse_text(first_text)
    second_result = parser.parse_text(second_text)

    assert first_result == second_result


@pytest.mark.unit
def test_parse_text_preserves_unicode_titles(
    parser: ClfParser,
    clf_asset,
) -> None:
    asset_path = clf_asset(ClfAsset.VALID_UNICODE_CHARS_TITLE)
    text = asset_path.read_text(encoding="utf-8")

    result = parser.parse_text(text)

    assert result.entries == (ChapterEntry(start_ms=0, title="歪みねぇな"),)
