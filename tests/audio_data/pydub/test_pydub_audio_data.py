# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from pathlib import Path

import pytest
from pydub.exceptions import (
    CouldntDecodeError,
    CouldntEncodeError,
)

from chapterchop.audio_data.pydub import PydubAudioData
from chapterchop.exceptions import AudioBackendError
from tests.support.assets.path_resolver import resolve
from tests.support.assets.registry import AudioAsset
from tests.support.fakes.pydub_segments import (
    FailingExportSegment,
    FailingSliceSegment,
)

# ============================================================
# GENERAL CONTRACT COMPLIANCE
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    "asset",
    [
        AudioAsset.SILENCE_1S_MONO_WAV,
        AudioAsset.TONE_440HZ_1S_MONO_WAV,
        AudioAsset.TONE_440HZ_1S_MONO_MP3,
        AudioAsset.TONE_440HZ_1S_STEREO_WAV,
        AudioAsset.TONE_440HZ_1S_STEREO_MP3,
    ],
)
def test_from_file_creates_pydub_audio_data_instance(
    asset: AudioAsset,
) -> None:
    path = resolve(asset)
    audio_data = PydubAudioData.from_file(path)

    assert isinstance(audio_data, PydubAudioData)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("start_ms", "end_ms"),
    [
        (0, 100),
        (15, 50),
        (50, 51),
    ],
)
def test_slice_is_deterministic(
    pydub_audio_data: PydubAudioData,
    start_ms: int,
    end_ms: int,
) -> None:
    result1 = pydub_audio_data.slice(start_ms=start_ms, end_ms=end_ms)
    result2 = pydub_audio_data.slice(start_ms=start_ms, end_ms=end_ms)

    assert result1._audio_segment == result2._audio_segment


@pytest.mark.unit
@pytest.mark.parametrize(
    ("start_ms", "end_ms"),
    [
        (10, 10),
        (10, 5),
        (-2, 5),
    ],
)
def test_slice_rejects_invalid_ranges(
    pydub_audio_data: PydubAudioData,
    start_ms: int,
    end_ms: int,
) -> None:
    with pytest.raises(ValueError):
        pydub_audio_data.slice(start_ms=start_ms, end_ms=end_ms)


@pytest.mark.unit
def test_slice_rejects_out_of_bounds_ranges(
    pydub_audio_data: PydubAudioData,
) -> None:
    out_of_bounds_end_ms = pydub_audio_data.duration_ms + 1

    with pytest.raises(ValueError):
        pydub_audio_data.slice(start_ms=0, end_ms=out_of_bounds_end_ms)


@pytest.mark.unit
def test_export_rejects_empty_format(
    pydub_audio_data: PydubAudioData, tmp_path: Path
) -> None:
    with pytest.raises(ValueError):
        pydub_audio_data.export(output_path=tmp_path, format="")


# ============================================================
# IMMUTABILITY GUARANTEES
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    ("start_ms", "end_ms"),
    [
        (0, 100),
        (15, 50),
        (50, 51),
    ],
)
def test_slice_does_not_modify_original_audio_data_instance(
    pydub_audio_data: PydubAudioData,
    start_ms: int,
    end_ms: int,
) -> None:
    before = pydub_audio_data._audio_segment
    pydub_audio_data.slice(start_ms=start_ms, end_ms=end_ms)
    after = pydub_audio_data._audio_segment

    assert before == after


# ============================================================
# ERROR HANDLING
# ============================================================


@pytest.mark.unit
@pytest.mark.parametrize(
    "asset",
    [
        AudioAsset.CORRUPTED_WAV,
        AudioAsset.CORRUPTED_MP3,
    ],
)
def test_from_file_wraps_backend_errors(
    asset: AudioAsset,
) -> None:
    path = resolve(asset)

    with pytest.raises(AudioBackendError):
        PydubAudioData.from_file(path)


@pytest.mark.unit
@pytest.mark.parametrize(
    "asset",
    [
        AudioAsset.CORRUPTED_WAV,
        AudioAsset.CORRUPTED_MP3,
    ],
)
def test_from_file_preserves_backend_exception_context(
    asset: AudioAsset,
) -> None:
    path = resolve(asset)

    with pytest.raises(AudioBackendError) as exc_info:
        PydubAudioData.from_file(path)

    assert type(exc_info.value.__cause__) is CouldntDecodeError


@pytest.mark.unit
@pytest.mark.parametrize(
    ("start_ms", "end_ms"),
    [
        (0, 100),
        (15, 50),
        (50, 51),
    ],
)
def test_slice_wraps_backend_errors(
    start_ms: int,
    end_ms: int,
) -> None:
    fake_segment = FailingSliceSegment()
    pydub_audio_data = PydubAudioData(segment=fake_segment)  # type: ignore

    with pytest.raises(AudioBackendError):
        pydub_audio_data.slice(start_ms=start_ms, end_ms=end_ms)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("start_ms", "end_ms"),
    [
        (0, 100),
        (15, 50),
        (50, 51),
    ],
)
def test_slice_preserves_backend_exception_context(
    start_ms: int,
    end_ms: int,
) -> None:
    fake_segment = FailingSliceSegment()
    pydub_audio_data = PydubAudioData(segment=fake_segment)  # type: ignore

    with pytest.raises(AudioBackendError) as exc_info:
        pydub_audio_data.slice(start_ms=start_ms, end_ms=end_ms)

    assert str(exc_info.value.__cause__) == "Simulated backend slice failure"


@pytest.mark.unit
def test_export_wraps_backend_errors(
    tmp_path: Path,
) -> None:
    fake_segment = FailingExportSegment()
    pydub_audio_data = PydubAudioData(segment=fake_segment)  # type: ignore

    with pytest.raises(AudioBackendError):
        pydub_audio_data.export(output_path=tmp_path, format="wav")


@pytest.mark.unit
def test_export_preserves_backend_exception_context(
    tmp_path: Path,
) -> None:
    fake_segment = FailingExportSegment()
    pydub_audio_data = PydubAudioData(segment=fake_segment)  # type: ignore

    with pytest.raises(AudioBackendError) as exc_info:
        pydub_audio_data.export(output_path=tmp_path, format="wav")

    assert type(exc_info.value.__cause__) is CouldntEncodeError
    assert str(exc_info.value.__cause__) == "Simulated backend export failure"
