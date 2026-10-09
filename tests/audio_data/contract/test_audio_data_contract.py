# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import pytest

from chapterchop.audio_data import AudioData

# ============================================================
# GENERAL CONTRACT COMPLIANCE
# ============================================================


@pytest.mark.contract
def test_duration_ms_is_non_negative(
    audio_data: AudioData,
) -> None:
    assert audio_data.duration_ms >= 0


@pytest.mark.contract
def test_channels_is_positive_when_present(
    audio_data: AudioData,
) -> None:
    if audio_data.channels is not None:
        assert audio_data.channels > 0


@pytest.mark.contract
def test_sample_rate_is_positive_when_present(
    audio_data: AudioData,
) -> None:
    if audio_data.sample_rate is not None:
        assert audio_data.sample_rate > 0


@pytest.mark.contract
@pytest.mark.parametrize(
    ("start_ms", "end_ms"),
    [
        (10, 10),
        (10, 5),
        (-2, 5),
    ],
)
def test_slice_rejects_invalid_ranges(
    audio_data: AudioData,
    start_ms: int,
    end_ms: int,
) -> None:
    with pytest.raises(ValueError):
        audio_data.slice(start_ms=start_ms, end_ms=end_ms)


@pytest.mark.contract
def test_slice_rejects_out_of_bounds_ranges(
    audio_data: AudioData,
) -> None:
    with pytest.raises(ValueError):
        audio_data.slice(0, audio_data.duration_ms + 1)


@pytest.mark.contract
def test_slice_supports_full_audio_range(
    audio_data: AudioData,
) -> None:
    result = audio_data.slice(0, audio_data.duration_ms)

    assert result is not None
    assert result is not audio_data
    assert type(result) is type(audio_data)
    assert result.duration_ms == audio_data.duration_ms


@pytest.mark.contract
@pytest.mark.parametrize(
    ("start_ms", "end_ms"),
    [
        (0, 50),
        (0, 100),
    ],
)
def test_slice_returns_same_type(
    audio_data: AudioData,
    start_ms: int,
    end_ms: int,
) -> None:
    result = audio_data.slice(start_ms, end_ms)

    assert type(result) is type(audio_data)


@pytest.mark.contract
@pytest.mark.parametrize(
    ("start_ms", "end_ms"),
    [
        (0, 50),
        (20, 80),
        (11, 34),
    ],
)
def test_slice_returns_expected_duration(
    audio_data: AudioData,
    start_ms: int,
    end_ms: int,
) -> None:
    result = audio_data.slice(start_ms, end_ms)

    assert result.duration_ms == (end_ms - start_ms)


# Contract-level determinism covers only protocol-visible state.
# Backend audio content handling is implementation-specific
# and should be tested on the implementation level.


@pytest.mark.contract
@pytest.mark.parametrize(
    ("start_ms", "end_ms"),
    [
        (0, 35),
        (0, 100),
        (17, 41),
    ],
)
def test_slice_is_deterministic(
    audio_data: AudioData,
    start_ms: int,
    end_ms: int,
) -> None:
    result1 = audio_data.slice(start_ms, end_ms)
    result2 = audio_data.slice(start_ms, end_ms)

    assert type(result1) is type(result2)

    assert result1.duration_ms == result2.duration_ms
    assert result1.channels == result2.channels
    assert result1.sample_rate == result2.sample_rate


# ============================================================
# IMMUTABILITY GUARANTEES
# ============================================================

# Contract-level immutability covers only protocol-visible state.
# Backend audio content handling is implementation-specific
# and should be tested on the implementation level.


@pytest.mark.contract
def test_slice_does_not_modify_original_audio_data_instance(
    audio_data: AudioData,
) -> None:
    before = (
        audio_data.duration_ms,
        audio_data.channels,
        audio_data.sample_rate,
    )

    audio_data.slice(0, 50)

    after = (
        audio_data.duration_ms,
        audio_data.channels,
        audio_data.sample_rate,
    )

    assert after == before


# ============================================================
# ERROR HANDLING
# ============================================================

# The AudioData protocol requires an AudioBackendError to be raised
# if the underlying audio backend fails during slicing.
# However, verifying this requirement depends on the backend implementation
# and cannot be done at the contract level without introducing artificial workarounds.
# Therefore, to avoid unnecessarily complicating the protocol structure,
# this condition should be verified in unit tests for each implementation.
