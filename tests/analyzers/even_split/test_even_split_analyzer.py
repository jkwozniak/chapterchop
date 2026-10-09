# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import pytest
from support.stubs.audio_data import AudioDataStub, FailingAudioDataStub

from chapterchop.analyzers import EvenSplitAnalyzer
from chapterchop.exceptions import AnalyzerError


@pytest.fixture
def analyzer() -> EvenSplitAnalyzer:
    return EvenSplitAnalyzer(parts=4)


@pytest.mark.unit
@pytest.mark.parametrize("parts", [0, -10])
def test_init_raises_value_error_for_non_positive_parts(
    parts: int,
) -> None:
    with pytest.raises(ValueError):
        EvenSplitAnalyzer(parts=parts)


@pytest.mark.unit
def test_analyze_rejects_audio_shorter_than_number_of_parts(
    analyzer: EvenSplitAnalyzer,
) -> None:
    audio_data = AudioDataStub(2)

    with pytest.raises(AnalyzerError):
        analyzer.analyze(audio_data)


@pytest.mark.unit
@pytest.mark.parametrize("duration", [0, -10])
def test_analyze_rejects_audio_of_non_positive_length(
    analyzer: EvenSplitAnalyzer,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)

    with pytest.raises(AnalyzerError):
        analyzer.analyze(audio_data)


@pytest.mark.unit
@pytest.mark.parametrize("duration", [4, 10, 13])
def test_analyze_returns_requested_number_of_chapters(
    analyzer: EvenSplitAnalyzer,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    result = analyzer.analyze(audio_data)

    assert len(result) == 4


@pytest.mark.unit
@pytest.mark.parametrize(
    ("duration", "parts"),
    [
        (10, 4),
        (11, 4),
        (13, 5),
        (100, 6),
    ],
)
def test_analyze_distributes_remainder_deterministically(
    duration: int,
    parts: int,
) -> None:
    analyzer = EvenSplitAnalyzer(parts=parts)
    audio_data = AudioDataStub(duration)
    result = analyzer.analyze(audio_data)

    base_duration = duration // parts
    remainder = duration % parts

    durations = [chapter.end_ms - chapter.start_ms for chapter in result]

    assert durations[:-1] == [base_duration] * (parts - 1)
    assert durations[-1] == base_duration + remainder


@pytest.mark.unit
@pytest.mark.parametrize("duration", [10, 15])
def test_analyze_returns_contiguous_non_overlapping_full_coverage_chapters(
    analyzer: EvenSplitAnalyzer,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    result = analyzer.analyze(audio_data)

    previous_end = 0
    for chapter in result:
        assert chapter.start_ms == previous_end
        previous_end = chapter.end_ms

    assert result[-1].end_ms == duration


@pytest.mark.unit
@pytest.mark.parametrize("duration", [10, 15])
def test_analyze_returns_chapters_with_minimum_duration_of_1ms(
    analyzer: EvenSplitAnalyzer,
    duration: int,
) -> None:
    audio_data = AudioDataStub(duration)
    result = analyzer.analyze(audio_data)

    for chapter in result:
        assert (chapter.end_ms - chapter.start_ms) >= 1


@pytest.mark.unit
def test_analyze_preserves_backend_exception_context(
    analyzer: EvenSplitAnalyzer,
) -> None:
    audio_data = FailingAudioDataStub(100)

    with pytest.raises(AnalyzerError) as exc_info:
        analyzer.analyze(audio_data)

    assert type(exc_info.value.__cause__) is RuntimeError
    assert str(exc_info.value.__cause__) == "Simulated backend failure"
