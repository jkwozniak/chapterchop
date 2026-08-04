# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import pytest

from chapterchop import ClfParser
from chapterchop.exceptions import ClfParserError
from tests.support.assets.registry import ClfAsset
from tests.support.factories.clf_texts import (
    make_invalid_leading_whitespace_text,
    make_invalid_line_carriage_return_text,
    make_invalid_separator_text,
    make_invalid_timestamp_format_text,
)


@pytest.fixture
def parser() -> ClfParser:
    return ClfParser()


@pytest.mark.unit
def test_parse_text_rejects_empty_input(
    parser: ClfParser,
    clf_asset,
) -> None:
    asset_path = clf_asset(ClfAsset.INVALID_EMPTY_FILE)
    text = asset_path.read_text(encoding="utf-8")

    with pytest.raises(ClfParserError):
        parser.parse_text(text)


@pytest.mark.unit
def test_parse_text_rejects_blank_line(
    parser: ClfParser,
    clf_asset,
) -> None:
    asset_path = clf_asset(ClfAsset.INVALID_EMPTY_LINE)
    text = asset_path.read_text(encoding="utf-8")

    with pytest.raises(ClfParserError):
        parser.parse_text(text)


@pytest.mark.unit
def test_parse_text_rejects_invalid_line(
    parser: ClfParser,
    clf_asset,
) -> None:
    asset_path = clf_asset(ClfAsset.INVALID_INCORRECT_LINE)
    text = asset_path.read_text(encoding="utf-8")

    with pytest.raises(ClfParserError):
        parser.parse_text(text)


@pytest.mark.unit
def test_parse_text_rejects_carriage_return(
    parser: ClfParser,
) -> None:
    text = make_invalid_line_carriage_return_text()

    with pytest.raises(ClfParserError):
        parser.parse_text(text)


@pytest.mark.unit
def test_parse_text_rejects_invalid_timestamp_format(
    parser: ClfParser,
) -> None:
    text = make_invalid_timestamp_format_text()

    with pytest.raises(ClfParserError):
        parser.parse_text(text)


@pytest.mark.unit
def test_parse_text_rejects_invalid_separator(
    parser: ClfParser,
) -> None:
    text = make_invalid_separator_text()

    with pytest.raises(ClfParserError):
        parser.parse_text(text)


@pytest.mark.unit
def test_parse_text_rejects_leading_whitespace(
    parser: ClfParser,
) -> None:
    text = make_invalid_leading_whitespace_text()

    with pytest.raises(ClfParserError):
        parser.parse_text(text)
