# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from collections.abc import Callable

from chapterchop.cutters import Cutter
from tests.support.factories.cutters import (
    make_simple_cutter,
)
from tests.support.fixtures.helpers import simple_parametrized_fixture_factory

CutterFactory = Callable[[], Cutter]

CUTTER_FACTORIES: list[CutterFactory] = [
    make_simple_cutter,
]

cutter = simple_parametrized_fixture_factory(
    CUTTER_FACTORIES,
)
