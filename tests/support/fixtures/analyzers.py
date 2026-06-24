# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from collections.abc import Callable

from chapterchop.analyzers.base import Analyzer
from tests.support.factories.analyzers import (
    make_even_split_analyzer,
)
from tests.support.fixtures.helpers import simple_parametrized_fixture_factory

AnalyzerFactory = Callable[[], Analyzer]

ANALYZER_FACTORIES: list[AnalyzerFactory] = [
    make_even_split_analyzer,
]

analyzer = simple_parametrized_fixture_factory(
    ANALYZER_FACTORIES,
)
