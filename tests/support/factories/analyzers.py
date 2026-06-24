# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from chapterchop.analyzers.base import Analyzer
from chapterchop.analyzers.even_split import EvenSplitAnalyzer


def make_even_split_analyzer() -> Analyzer:
    return EvenSplitAnalyzer(parts=4)
