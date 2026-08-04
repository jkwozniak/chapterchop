# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from collections.abc import Callable
from pathlib import Path

import pytest
from support.stubs.audio_data import (
    AudioDataStub,
    FailingWritableAudioDataStub,
    WritableAudioDataStub,
)

from chapterchop.exceptions import WriterError
from chapterchop.writers import DirectoryWriter
from tests.support.factories.segments import (
    make_segments,
    make_segments_mixed_writability,
)


@pytest.mark.unit
def test_init_rejects_non_alphanumeric_format(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    with pytest.raises(ValueError):
        directory_writer_factory(".mp-3")


@pytest.mark.unit
def test_init_normalizes_format_to_lowercase(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    writer = directory_writer_factory(format="WAV")

    assert writer._format == "wav"


@pytest.mark.unit
def test_init_strips_format_whitespace(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    writer = directory_writer_factory(" wav  ")

    assert writer._format == "wav"


@pytest.mark.unit
def test_write_uses_sequential_numbering_for_filenames(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    writer = directory_writer_factory(format="wav")
    segments = make_segments([100, 150, 100], audio_factory=WritableAudioDataStub)
    result = writer.write(segments=segments)

    for i, path in enumerate(result, start=1):
        assert path.name.startswith(f"{i:02d}.")


@pytest.mark.unit
def test_write_omits_title_when_not_present(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    writer = directory_writer_factory(format="wav")
    segments = make_segments([100, 150, 100], audio_factory=WritableAudioDataStub)
    result = writer.write(segments=segments)

    for i, path in enumerate(result, start=1):
        assert path.name == f"{i:02d}.wav"


@pytest.mark.unit
def test_write_preserves_chapter_titles_if_present(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    writer = directory_writer_factory(format="wav")
    segments = make_segments(
        [100, 150, 100],
        audio_factory=WritableAudioDataStub,
        title_prefix="chapter",
    )
    result = writer.write(segments=segments)

    for i, path in enumerate(result, start=1):
        assert path.name == f"{i:02d}.chapter_{i}.wav"


@pytest.mark.unit
def test_write_sanitizes_invalid_filename_characters(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    writer = directory_writer_factory(format="wav")
    segments = make_segments(
        [100, 150, 100],
        audio_factory=WritableAudioDataStub,
        title_prefix="a#b_c -&d",
    )
    result = writer.write(segments=segments)

    for i, path in enumerate(result, start=1):
        assert path.name == f"{i:02d}.a_b_c -_d_{i}.wav"


@pytest.mark.unit
def test_write_creates_output_directory_if_missing(
    directory_writer_factory: Callable[..., DirectoryWriter], tmp_path: Path
) -> None:
    segments = make_segments([200, 100, 100], audio_factory=WritableAudioDataStub)
    directory = "exports"
    writer = directory_writer_factory(format="wav", directory=directory)
    output_dir = tmp_path / directory

    assert not output_dir.exists()

    writer.write(segments)

    assert output_dir.is_dir()


@pytest.mark.unit
def test_write_raises_writer_error_for_non_writable_audio_data(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    writer = directory_writer_factory(format="wav")
    segments = make_segments([120, 40, 100], audio_factory=AudioDataStub)

    with pytest.raises(WriterError):
        writer.write(segments)


@pytest.mark.unit
def test_write_raises_writer_error_for_partly_writable_audio_data(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    writer = directory_writer_factory(format="wav")
    segments = make_segments_mixed_writability()

    with pytest.raises(WriterError):
        writer.write(segments)


@pytest.mark.unit
def test_write_preserves_backend_exception_context(
    directory_writer_factory: Callable[..., DirectoryWriter],
) -> None:
    segments = make_segments([100, 50, 120], audio_factory=FailingWritableAudioDataStub)
    writer = directory_writer_factory(format="wav")

    with pytest.raises(WriterError) as exc_info:
        writer.write(segments)

    assert type(exc_info.value.__cause__) is RuntimeError
    assert str(exc_info.value.__cause__) == "Simulated export failure"
