# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import pytest

from chapterchop import ClfParser
from chapterchop.exceptions import ClfParserError
from tests.support.assets.registry import ClfAsset


@pytest.fixture
def parser() -> ClfParser:
    return ClfParser()


@pytest.mark.unit
def test_parse_file_reads_valid_clf_asset(
    parser: ClfParser,
    clf_asset,
) -> None:
    asset_path = clf_asset(ClfAsset.VALID_TIMESTAMPS_ONLY)

    result = parser.parse_file(asset_path)

    assert len(result.entries) == 3


@pytest.mark.unit
def test_parse_file_rejects_invalid_utf8_asset(
    parser: ClfParser,
    clf_asset,
) -> None:
    asset_path = clf_asset(ClfAsset.INVALID_UTF8)

    with pytest.raises(ClfParserError):
        parser.parse_file(asset_path)


@pytest.mark.unit
def test_parse_file_rejects_bom_prefixed_clf_asset(
    parser: ClfParser,
    clf_asset,
) -> None:
    asset_path = clf_asset(ClfAsset.INVALID_UTF8_WITH_BOM)

    with pytest.raises(ClfParserError):
        parser.parse_file(asset_path)
