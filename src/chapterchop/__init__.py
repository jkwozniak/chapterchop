# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from .analyzers import Analyzer, ChapterListAnalyzer, EvenSplitAnalyzer
from .audio_data import AudioData, PydubAudioData, WritableAudioData
from .clf_parser import ClfParser
from .cutters import Cutter, SimpleCutter
from .exceptions import (
    AnalyzerError,
    AudioBackendError,
    ChapterChopError,
    ChapterGapError,
    ChapterOutOfBoundsError,
    ChapterOverlapError,
    ClfParserError,
    CutterError,
    NonFullCoverageError,
    WriterError,
)
from .models import Chapter, ChapterEntry, ChapterList, Segment
from .writers import DirectoryWriter, Writer

__all__ = [
    # --- domain models --- #
    "Chapter",
    "ChapterEntry",
    "ChapterList",
    "Segment",
    # --- protocols --- #
    "AudioData",
    "WritableAudioData",
    "Analyzer",
    "Cutter",
    "Writer",
    # --- audio backend --- #
    "PydubAudioData",
    # --- processing components --- #
    "ClfParser",
    "EvenSplitAnalyzer",
    "ChapterListAnalyzer",
    "SimpleCutter",
    "DirectoryWriter",
    # --- custom exceptions --- #
    "AnalyzerError",
    "AudioBackendError",
    "ChapterChopError",
    "ChapterGapError",
    "ChapterOutOfBoundsError",
    "ChapterOverlapError",
    "ClfParserError",
    "CutterError",
    "NonFullCoverageError",
    "WriterError",
]
