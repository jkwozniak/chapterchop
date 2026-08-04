# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import pytest

from chapterchop.cutters import SimpleCutter
from chapterchop.exceptions import (
    ChapterGapError,
    ChapterOutOfBoundsError,
    ChapterOverlapError,
    CutterError,
    InvalidChapterError,
    NonFullCoverageError,
)
from tests.support.factories.chapters import (
    make_duplicate_start,
    make_full_coverage,
    make_invalid_range,
    make_missing_start_zero,
    make_not_full_coverage,
    make_out_of_bounds,
    make_with_gap,
    make_with_overlap,
)
from tests.support.stubs.audio_data import (
    AudioDataStub,
    FailingAudioDataStub,
)


@pytest.fixture
def cutter() -> SimpleCutter:
    return SimpleCutter()


@pytest.mark.unit
@pytest.mark.parametrize("duration", [100])
def test_cut_rejects_chapters_with_gaps(
    cutter: SimpleCutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = make_with_gap(duration)

    with pytest.raises(ChapterGapError):
        cutter.cut(audio_data, chapters)


@pytest.mark.unit
@pytest.mark.parametrize("duration", [100])
def test_cut_rejects_overlapping_chapters(
    cutter: SimpleCutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = make_with_overlap(duration)

    with pytest.raises(ChapterOverlapError):
        cutter.cut(audio_data, chapters)


@pytest.mark.unit
def test_cut_requires_full_audio_coverage(
    cutter: SimpleCutter,
) -> None:
    audio_data = AudioDataStub(100)
    chapters = make_not_full_coverage(100)

    with pytest.raises(NonFullCoverageError):
        cutter.cut(audio_data, chapters)


@pytest.mark.unit
def test_cut_requires_chapters_starting_at_zero(
    cutter: SimpleCutter,
) -> None:
    audio_data = AudioDataStub(100)
    chapters = make_missing_start_zero(100)

    with pytest.raises(NonFullCoverageError):
        cutter.cut(audio_data, chapters)


@pytest.mark.unit
def test_cut_rejects_duplicate_chapter_starts(
    cutter: SimpleCutter,
) -> None:
    audio_data = AudioDataStub(100)
    chapters = make_duplicate_start(100)

    with pytest.raises(ChapterOverlapError):
        cutter.cut(audio_data, chapters)


@pytest.mark.unit
def test_cut_rejects_invalid_chapter_ranges(
    cutter: SimpleCutter,
) -> None:
    audio_data = AudioDataStub(100)
    chapters = make_invalid_range()

    with pytest.raises(InvalidChapterError):
        cutter.cut(audio_data, chapters)


@pytest.mark.unit
def test_cut_rejects_out_of_bounds_chapters(
    cutter: SimpleCutter,
) -> None:
    audio_data = AudioDataStub(100)
    chapters = make_out_of_bounds(100)

    with pytest.raises(ChapterOutOfBoundsError):
        cutter.cut(audio_data, chapters)


@pytest.mark.unit
def test_cut_preserves_backend_exception_context(
    cutter: SimpleCutter,
) -> None:
    audio_data = FailingAudioDataStub(100)
    chapters = make_full_coverage(100)

    with pytest.raises(CutterError) as exc_info:
        cutter.cut(audio_data, chapters)

    assert type(exc_info.value.__cause__) is RuntimeError
    assert str(exc_info.value.__cause__) == "Simulated backend failure"
