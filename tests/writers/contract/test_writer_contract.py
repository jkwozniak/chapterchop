# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from copy import deepcopy
from pathlib import Path

import pytest
from support.stubs.audio_data import (
    FailingWritableAudioDataStub,
    WritableAudioDataStub,
)

from chapterchop.exceptions import WriterError
from chapterchop.writers.base import Writer
from tests.support.factories.segments import (
    make_segments,
)

# ============================================================
# GENERAL CONTRACT COMPLIANCE
# ============================================================


@pytest.mark.contract
def test_write_returns_output_paths(
    writer: Writer,
) -> None:
    segments = make_segments([50, 50, 100], audio_factory=WritableAudioDataStub)
    paths = writer.write(segments=segments)

    assert isinstance(paths, list)
    for path in paths:
        assert isinstance(path, Path)


@pytest.mark.contract
def test_write_returns_one_path_per_segment(
    writer: Writer,
) -> None:
    segments = make_segments([100, 200, 150, 100], audio_factory=WritableAudioDataStub)
    paths = writer.write(segments=segments)

    assert len(paths) == len(segments)


@pytest.mark.contract
def test_write_creates_output_files(
    writer: Writer,
) -> None:
    segments = make_segments([100, 300, 250, 120], audio_factory=WritableAudioDataStub)
    paths = writer.write(segments=segments)

    assert all(path.exists() for path in paths)


@pytest.mark.contract
def test_write_returns_empty_list_for_empty_segments(
    writer: Writer,
) -> None:
    segments = []
    paths = writer.write(segments=segments)

    assert paths == []


# ============================================================
# IMMUTABILITY GUARANTEES
# ============================================================

# Contract-level immutability covers only protocol-visible state.
# Backend audio content handling is implementation-specific
# and should be tested on the implementation level.


@pytest.mark.contract
def test_write_does_not_modify_segments(
    writer: Writer,
) -> None:
    segments = make_segments([50, 50, 100], audio_factory=WritableAudioDataStub)

    original = deepcopy(segments)

    writer.write(segments=segments)

    for before, after in zip(original, segments, strict=True):
        assert before.chapter == after.chapter
        assert before.audio.duration_ms == after.audio.duration_ms
        assert before.audio.channels == after.audio.channels
        assert before.audio.sample_rate == after.audio.sample_rate


# ============================================================
# ERROR HANDLING
# ============================================================


@pytest.mark.contract
def test_write_wraps_backend_errors(
    writer: Writer,
) -> None:
    segments = make_segments(
        [50, 50, 100],
        audio_factory=FailingWritableAudioDataStub,
    )

    with pytest.raises(WriterError):
        writer.write(segments)
