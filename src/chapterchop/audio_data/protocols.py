# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from __future__ import annotations

from os import PathLike
from typing import Protocol, Self, runtime_checkable


@runtime_checkable
class AudioData(Protocol):
    """
    Structural protocol representing audio content used by
    Analyzer, Cutter and Writer.

    AudioData implementations should behave as conceptually immutable objects.

    Backend implementations may provide convenience constructors
    for loading audio from files.
    When supported, to ensure consistency across implementations,
    the recommended API is::

        @classmethod
        def from_file(cls, path: str | PathLike[str]) -> Self:
            ...

    """

    @property
    def duration_ms(self) -> int:
        """
        Total duration of the audio in milliseconds.

        Must be greater than or equal to 0.
        """
        ...

    @property
    def channels(self) -> int | None:
        """
        Number of audio channels.

        Must be greater than 0 when provided.
        May be None if the implementation does not expose this information.
        """
        ...

    @property
    def sample_rate(self) -> int | None:
        """
        Sample rate of the audio in Hz.

        Must be greater than 0 when provided.
        May be None if the implementation does not expose this information.
        """
        ...

    def slice(self, start_ms: int, end_ms: int) -> Self:
        """
        Return a new AudioData instance representing the requested time range.

        Args:
          - start_ms: Start time of the slice in milliseconds.
          - end_ms: End time of the slice in milliseconds.

        Returns:
          - AudioData: A new instance containing only the requested subsegment.

        Raises:
          - ValueError: If the provided range is invalid.
          - AudioBackendError: If the underlying audio backend fails during slicing.

        Semantic details:
          - start_ms is inclusive
          - end_ms is exclusive
          - 0 <= start_ms < end_ms <= duration_ms
          - the original instance must not be modified
          - the returned object must preserve audio metadata
            exposed by the implementation where applicable
        """
        ...


@runtime_checkable
class WritableAudioData(Protocol):
    """
    Optional capability for AudioData implementations that support exporting.

    This protocol defines the ability to persist audio data to a file
    in a specified format.

    Implementations may rely on backend-specific mechanisms (e.g. ffmpeg).
    """

    def export(self, output_path: str | PathLike[str], format: str) -> None:
        """
        Export audio data to a file.

        Args:
          - path (str | PathLike[str]): Full destination path.
          - format (str): Audio export format requested from the underlying
            backend (for example: "mp3", "wav", "flac").

        Raises:
          - ValueError: If the output path is invalid or the requested
            export format is not supported by the underlying audio backend.
          - AudioBackendError: If export fails at backend level.

        Semantic details:
          - output_path must include both the filename and extension.
          - implementations must not modify the provided path
            or automatically append extensions
          - successful export must create or overwrite the file located
            at the provided output_path
          - the original audio object must not be modified
          - format validation is implementation-dependent and may rely
            on backend capabilities
            ...
        """
