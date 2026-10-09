# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from collections.abc import Callable

from support.factories.cutters import (
    make_simple_cutter,
)
from support.fixtures.helpers import simple_parametrized_fixture_factory

from chapterchop.cutters import Cutter

CutterFactory = Callable[[], Cutter]

CUTTER_FACTORIES: list[CutterFactory] = [
    make_simple_cutter,
]

cutter = simple_parametrized_fixture_factory(
    CUTTER_FACTORIES,
)
