# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from __future__ import annotations

from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Self

from chapterchop.audio_data import AudioData, WritableAudioData
from chapterchop.exceptions import AudioBackendError


@dataclass(slots=True)
class AudioDataStub(AudioData):
    """
    Minimal stub implementation of AudioData protocol
    (without export capability).

    - operates only on duration (ms)
    - validates slice boundaries
    - returns new AudioDataStub instances on slice()
    """

    _duration_ms: int
    _channels: int | None = None
    _sample_rate: int | None = None

    @property
    def duration_ms(self) -> int:
        return self._duration_ms

    @property
    def channels(self) -> int | None:
        return self._channels

    @property
    def sample_rate(self) -> int | None:
        return self._sample_rate

    def slice(self, start_ms: int, end_ms: int) -> Self:
        if start_ms < 0:
            raise AudioBackendError(f"start_ms < 0: {start_ms}")

        if end_ms < start_ms:
            raise AudioBackendError(f"end_ms < start_ms: {end_ms} < {start_ms}")

        if end_ms > self._duration_ms:
            raise AudioBackendError(
                f"end_ms exceeds duration: {end_ms} > {self._duration_ms}"
            )

        return type(self)(
            _duration_ms=end_ms - start_ms,
            _channels=self._channels,
            _sample_rate=self._sample_rate,
        )


class FailingAudioDataStub(AudioDataStub):
    """
    Audio stub that always fails on 'duration_ms' access.
    Used for testing error handling.
    """

    @property
    def duration_ms(self) -> int:
        raise RuntimeError("Simulated backend failure")


class WritableAudioDataStub(AudioData, WritableAudioData):
    """
    Audio stub that supports export.

    - creates empty files
    """

    _duration_ms: int
    _channels: int | None = None
    _sample_rate: int | None = None

    def __init__(self, duration: int):
        self._duration_ms = duration
        self.export_calls: list[tuple[str, str]] = []

    @property
    def duration_ms(self) -> int:
        return self._duration_ms

    @property
    def channels(self) -> int | None:
        return self._channels

    @property
    def sample_rate(self) -> int | None:
        return self._sample_rate

    def slice(self, start_ms: int, end_ms: int) -> WritableAudioDataStub:
        return type(self)(end_ms - start_ms)

    def export(self, output_path: str | PathLike[str], format: str) -> None:
        Path(output_path).touch()


class FailingWritableAudioDataStub(WritableAudioDataStub):
    """
    Audio stub that fails during export.
    """

    def export(self, output_path: str | PathLike[str], format: str) -> None:
        raise RuntimeError("Simulated export failure")
