# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import pytest
from support.stubs.audio_data import AudioDataStub, FailingAudioDataStub

from chapterchop.analyzers import Analyzer
from chapterchop.exceptions import AnalyzerError
from chapterchop.models import Chapter

# ============================================================
# GENERAL CONTRACT COMPLIANCE
# ============================================================


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_analyze_returns_chapters(
    analyzer: Analyzer,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    result = analyzer.analyze(audio_data)

    assert isinstance(result, list)
    for chapter in result:
        assert isinstance(chapter, Chapter)


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_analyze_returns_chapters_with_valid_bounds(
    analyzer: Analyzer,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    result = analyzer.analyze(audio_data)

    for ch in result:
        assert ch.start_ms >= 0
        assert ch.start_ms < ch.end_ms


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_analyze_returns_chapters_within_audio_bounds(
    analyzer: Analyzer, duration: int
) -> None:
    audio_data = AudioDataStub(duration)
    result = analyzer.analyze(audio_data)

    for ch in result:
        assert ch.end_ms <= duration


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_analyze_is_deterministic(
    analyzer: Analyzer,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    result1 = analyzer.analyze(audio_data)
    result2 = analyzer.analyze(audio_data)

    assert result1 == result2


# ============================================================
# IMMUTABILITY GUARANTEES
# ============================================================

# Contract-level immutability covers only protocol-visible state.
# Backend audio content handling is implementation-specific
# and should be tested on the implementation level.


@pytest.mark.contract
@pytest.mark.parametrize("duration", [100, 1000])
def test_analyze_does_not_modify_audio_data(
    analyzer: Analyzer,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)

    before = (
        audio_data.duration_ms,
        audio_data.channels,
        audio_data.sample_rate,
    )

    analyzer.analyze(audio_data)

    after = (
        audio_data.duration_ms,
        audio_data.channels,
        audio_data.sample_rate,
    )

    assert after == before


# ============================================================
# ERROR HANDLING
# ============================================================


@pytest.mark.contract
def test_analyze_raises_analyzer_error_for_invalid_input(
    analyzer: Analyzer,
) -> None:
    audio_data = AudioDataStub(-1)

    with pytest.raises(AnalyzerError):
        analyzer.analyze(audio_data)


@pytest.mark.contract
def test_analyze_wraps_backend_errors(
    analyzer: Analyzer,
) -> None:
    audio_data = FailingAudioDataStub(100)

    with pytest.raises(AnalyzerError):
        analyzer.analyze(audio_data)
