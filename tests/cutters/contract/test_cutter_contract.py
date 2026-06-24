# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from copy import deepcopy

import pytest
from support.stubs.audio_data import AudioDataStub, FailingAudioDataStub

from chapterchop.cutters.base import Cutter
from chapterchop.exceptions import CutterError
from tests.support.factories.chapters import (
    make_full_coverage,
    make_full_coverage_multiple_chapters,
    make_single,
)

# ============================================================
# GENERAL CONTRACT COMPLIANCE
# ============================================================


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_cut_returns_segments_matching_chapters(
    cutter: Cutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = make_full_coverage(duration)
    result = cutter.cut(audio_data, chapters)

    assert len(result) == len(chapters)


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_cut_returns_segments_with_expected_duration(
    cutter: Cutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = make_full_coverage(duration)
    result = cutter.cut(audio_data, chapters)

    for segment in result:
        expected = segment.chapter.end_ms - segment.chapter.start_ms
        assert segment.audio.duration_ms == expected


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_cut_single_chapter(
    cutter: Cutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = make_single(duration)
    result = cutter.cut(audio_data, chapters)

    assert len(result) == 1
    assert result[0].audio.duration_ms == duration


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_cut_preserves_chapter_data(
    cutter: Cutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = make_full_coverage(duration)
    result = cutter.cut(audio_data, chapters)

    for segment, chapter in zip(result, chapters, strict=True):
        assert segment.chapter == chapter


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_cut_returns_segments_sorted_by_start_ms(
    cutter: Cutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = list(reversed(make_full_coverage(duration)))
    result = cutter.cut(audio_data, chapters)
    starts = [s.chapter.start_ms for s in result]

    assert starts == sorted(starts)


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_cut_input_order_does_not_affect_output(
    cutter: Cutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = make_full_coverage_multiple_chapters(duration, 4)
    expected = cutter.cut(audio_data, chapters)
    reversed_chapters = list(reversed(chapters))
    result = cutter.cut(audio_data, reversed_chapters)

    assert result == expected


@pytest.mark.contract
def test_cut_returns_empty_list_for_empty_chapters(
    cutter: Cutter,
) -> None:
    audio_data = AudioDataStub(100)
    result = cutter.cut(audio_data, [])

    assert result == []


# ============================================================
# IMMUTABILITY GUARANTEES
# ============================================================

# Contract-level immutability covers only protocol-visible state.
# Backend audio content handling is implementation-specific
# and should be tested on the implementation level.


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_cut_does_not_modify_audio_data(
    cutter: Cutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = make_full_coverage(duration)

    before = (
        audio_data.duration_ms,
        audio_data.channels,
        audio_data.sample_rate,
    )

    cutter.cut(audio_data, chapters)

    after = (
        audio_data.duration_ms,
        audio_data.channels,
        audio_data.sample_rate,
    )

    assert after == before


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_cut_does_not_modify_chapters(
    cutter: Cutter,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    chapters = make_full_coverage(duration)
    before = deepcopy(chapters)
    cutter.cut(audio_data, chapters)

    assert chapters == before


# ============================================================
# ERROR HANDLING
# ============================================================


@pytest.mark.contract
def test_cut_wraps_backend_errors(
    cutter: Cutter,
) -> None:
    audio_data = FailingAudioDataStub(100)
    chapters = make_full_coverage(100)

    with pytest.raises(CutterError):
        cutter.cut(audio_data, chapters)
