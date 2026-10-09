# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from __future__ import annotations

from os import PathLike
from typing import Self, cast

from pydub import AudioSegment
from pydub.exceptions import CouldntEncodeError

from ..exceptions import AudioBackendError
from .protocols import AudioData


class PydubAudioData(AudioData):
    """
    Reference implementation of the AudioData and WritableAudioData
    protocols using the pydub/ffmpeg backend.

    PydubAudioData provides:
    - audio metadata access
    - immutable audio slicing
    - audio export support
    - loading audio from existing files via from_file()

    Backend capabilities such as supported audio formats depend
    on the underlying pydub and ffmpeg installation.

    The implementation wraps backend-specific failures as
    AudioBackendError while preserving the original exception context.
    """

    def __init__(self, segment: AudioSegment):
        self._audio_segment = segment

    @classmethod
    def from_file(cls, path: str | PathLike[str]) -> Self:
        """
        Create a PydubAudioData instance from an audio file.

        Backend behavior:
          - audio loading is delegated to the pydub/ffmpeg backend
          - supported input formats depend on backend capabilities

        Error handling:
          - backend loading failures are wrapped as AudioBackendError
          - original backend exception context is preserved
        """

        try:
            segment = AudioSegment.from_file(path)
        except Exception as exc:
            raise AudioBackendError(f"Failed to load audio file: '{path}'.") from exc

        return cls(segment=segment)

    @property
    def duration_ms(self) -> int:
        return len(self._audio_segment)

    @property
    def channels(self) -> int | None:
        if self._audio_segment.channels is None:
            return None
        channels = cast(int, self._audio_segment.channels)
        if channels <= 0:
            raise AudioBackendError(
                f"Invalid channel count returned by backend: {channels!r}."
            )
        return channels

    @property
    def sample_rate(self) -> int | None:
        if self._audio_segment.frame_rate is None:
            return None
        sample_rate = cast(int, self._audio_segment.frame_rate)
        if sample_rate <= 0:
            raise AudioBackendError(
                f"Invalid sample rate returned by backend: {sample_rate!r}."
            )
        return sample_rate

    def export(self, output_path: str | PathLike[str], format: str) -> None:
        """
        Export audio using pydub/ffmpeg backend integration.

        Validation policy:
          - format must not be empty

        Backend behavior:
          - supported export formats depend on ffmpeg capabilities
          - backend encoding and filesystem errors are wrapped
            as AudioBackendError
        """

        if not format.strip():
            raise ValueError("'format' must not be empty.")

        try:
            self._audio_segment.export(out_f=output_path, format=format)

        except FileNotFoundError as exc:
            raise AudioBackendError("'ffmpeg' executable could not be found.") from exc

        except CouldntEncodeError as exc:
            raise AudioBackendError(
                f"Failed to export audio using format '{format}'."
            ) from exc

        except OSError as exc:
            raise AudioBackendError(
                f"Failed to write exported audio to '{output_path}'."
            ) from exc

    def slice(self, start_ms: int, end_ms: int) -> PydubAudioData:
        """
        Return a new PydubAudioData instance representing
        the requested audio range.

        Validation policy:
          - start_ms and end_ms must be non-negative
          - start_ms must be smaller than end_ms
          - end_ms must not exceed audio duration

        Backend behavior:
          - slicing is delegated to pydub's AudioSegment backend
          - the original audio object is not modified
          - the returned object preserves backend audio properties
        """

        if start_ms < 0 or end_ms < 0:
            raise ValueError("'start_ms' and 'end_ms' must be non-negative.")
        if start_ms >= end_ms:
            raise ValueError("'start_ms' must be < 'end_ms'.")
        if end_ms > self.duration_ms:
            raise ValueError("'end_ms' exceeds audio duration.")

        try:
            # Simple slicing of pydub's AudioSegment (`audio_segment_object[a:b]`)
            # always returns an `AudioSegment` object,
            # hovewer `AudioSegment.__getitem__` may return `Generator[AudioSegment]`
            # if additional step parameter is provided
            # (see https://github.com/jiaaro/pydub/blob/v0.25.1/pydub/audio_segment.py#L300)
            # For this reason, cast(AudioSegment, ...) is used here
            # to satisfy the static type checkers (e.g. Pylance, mypy)
            segment = cast(AudioSegment, self._audio_segment[start_ms:end_ms])
            return PydubAudioData(segment)
        except Exception as exc:
            raise AudioBackendError("Failed to slice audio") from exc

    def __repr__(self) -> str:
        return f"PydubAudioData(duration_ms={self.duration_ms})"
