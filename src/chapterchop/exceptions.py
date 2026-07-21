# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak


class ChapterChopError(Exception):
    """Base exception for all ChapterChop errors."""


# ---------------------------------------------------------------------------
# Domain model errors
#
# Raised when a domain model object breaks its own fundamental rules.
# These errors indicate globally invalid model state.
# ---------------------------------------------------------------------------


class InvalidChapterError(ChapterChopError):
    """
    Raised when a chapter has invalid time values
    (e.g. start_ms < 0 or start_ms >= end_ms).
    """


class InvalidChapterEntryError(ChapterChopError):
    """
    Raised when a chapter entry violates its invariants
    (e.g. start_ms < 0 or title is an empty string).
    """


class InvalidChapterListError(ChapterChopError):
    """
    Raised when a chapter list violates its invariants
    (e.g. entries are not sorted by start_ms 
    or contain duplicate start_ms values).
    """


# ---------------------------------------------------------------------------
# Processing constraint errors
#
# Raised when otherwise valid data violates semantic constraints
# required by a specific processing context or implementation.
# ---------------------------------------------------------------------------


class ChapterOutOfBoundsError(ChapterChopError):
    """Raised when a chapter exceeds the duration of the source audio."""


class ChapterOverlapError(ChapterChopError):
    """
    Raised when chapter ranges overlap in a context
    where overlapping chapters are not allowed.
    """


class ChapterGapError(ChapterChopError):
    """
    Raised when gaps exist between chapters in a context
    where continuous chapter coverage is required.
    """


class NonFullCoverageError(ChapterChopError):
    """
    Raised when chapters do not cover the entire audio duration
    in a context where full coverage is required.

    ChapterGapError should be preferred when uncovered regions
    exist between chapters rather than at the beginning or end
    of the audio.
    """


class ChapterListOutOfBoundsError(ChapterChopError):
    """
    Raised when a chapter list contains one or more chapter entries
    that start outside the source audio.
    """


# ---------------------------------------------------------------------------
# Operational component errors
#
# Raised when a processing component fails while performing its operation.
# ---------------------------------------------------------------------------


class AnalyzerError(ChapterChopError):
    """Raised when audio analysis fails."""


class CutterError(ChapterChopError):
    """Raised when audio cutting fails."""


class WriterError(ChapterChopError):
    """Raised when writing audio file fails."""


class AudioBackendError(ChapterChopError):
    """Raised when an audio backend returns invalid or inconsistent data."""
