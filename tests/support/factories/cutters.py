# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from chapterchop.cutters.base import Cutter
from chapterchop.cutters.simple import SimpleCutter


def make_simple_cutter() -> Cutter:
    return SimpleCutter()
