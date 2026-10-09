# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import pytest
from support.factories.clf_texts import (
    make_invalid_non_increasing_timestamp_text,
)

from chapterchop import ClfParser


@pytest.fixture
def parser() -> ClfParser:
    return ClfParser()


@pytest.mark.unit
def test_parse_text_rejects_non_increasing_timestamps(
    parser: ClfParser,
) -> None:
    text = make_invalid_non_increasing_timestamp_text()

    with pytest.raises(ValueError):
        parser.parse_text(text)
