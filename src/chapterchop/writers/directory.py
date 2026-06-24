# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from pathlib import Path

from chapterchop.audio_data.protocols import AudioData, WritableAudioData
from chapterchop.exceptions import WriterError
from chapterchop.models import Segment
from chapterchop.writers.base import Writer


class DirectoryWriter(Writer):
    """
    A reference implementation of the Writer protocol.

    DirectoryWriter writes each Segment as a separate audio file
    inside a configured local output directory.

    The writer uses deterministic sequential filenames and may
    optionally include sanitized chapter titles in generated
    filenames.

    Guarantees:
    - writes one output file per segment
    - returns paths to all created files
    - output paths are returned in write order
    - generated filenames are deterministic for identical input
      and configuration
    - operation does not mutate provided Segment objects

    Runtime validation:
    - all Segment.audio objects must implement WritableAudioData
    - writing failures are wrapped as WriterError

    Intended use:
    - correctness baseline
    - predictable local filesystem export
    - educational reference implementation

    Not intended for advanced media management workflows
    or high-performance batch exporting.
    """

    _output_dir: Path
    _format: str

    def __init__(
        self,
        output_dir: Path,
        *,
        format: str = "wav",
    ) -> None:
        """
        Initialize the writer.

        Args:
          - output_dir (pathlib.Path): Target directory where exported
            audio files will be written.
          - format (str): Audio export format passed to the underlying
            audio backend export implementation.

        Configuration semantics:
          - output_dir is stored as persistent writer configuration
          - output directories are created automatically during write()
            if they do not already exist
          - filename generation uses the configured export format

        Raises:
          - ValueError: If configuration values are invalid.
        """

        normalized_format = format.strip().lower()

        if not normalized_format.isalnum():
            raise ValueError("format must contain only alphanumeric characters")

        self._format = normalized_format
        self._output_dir = output_dir

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"output_dir={self._output_dir!r}, "
            f"format={self._format!r})"
        )

    def write(self, segments: list[Segment]) -> list[Path]:
        """
        Write audio segments to the configured output directory.

        Args:
          - segments (list[Segment]): Audio segments to export.

        Returns:
          - list[Path]: Paths to all created audio files.

        Raises:
          - WriterError: If writing fails, export is unsupported,
            or filesystem operations fail.

        Semantic details:
          - returns [] if provided list of segments is empty
          - exported files are written sequentially
          - output filenames are deterministic for identical input
            and writer configuration
        """

        output_paths: list[Path] = []

        try:
            self._output_dir.mkdir(parents=True, exist_ok=True)

            for index, segment in enumerate(segments, start=1):
                audio = self._is_writable(segment.audio)

                filename = self._build_filename(index, segment)
                path = self._output_dir / filename

                audio.export(path, self._format)
                output_paths.append(path)

        except WriterError:
            raise
        except Exception as exc:
            raise WriterError("Failed to write audio segments.") from exc

        return output_paths

    def _is_writable(self, audio: AudioData) -> WritableAudioData:
        """
        Validate WritableAudioData export capability.

        Args:
          - audio (AudioData): Audio object to validate.

        Returns:
         - WritableAudioData: Audio object supporting export operations.

        Raises:
          - WriterError: If audio does not implement WritableAudioData.
        """

        if not isinstance(audio, WritableAudioData):
            raise WriterError(
                "AudioData does not support export "
                "(missing WritableAudioData capability)."
            )

        return audio

    def _build_filename(self, index: int, segment: Segment) -> str:
        """
        Build a deterministic output filename for a segment.

        Args:
          - index (int): Sequential segment number.
          - segment (Segment): Segment for which the filename is generated.

        Returns:
          - str: Generated filename including export extension.
        """

        title = segment.chapter.title

        if title:
            safe_title = self._sanitize(title)
            return f"{index:02d}.{safe_title}.{self._format}"

        return f"{index:02d}.{self._format}"

    def _sanitize(self, filename: str) -> str:
        """
        Sanitize a string for filesystem-safe filename usage.

        Args:
          - filename (str): Raw filename fragment.

        Returns:
          - str: Sanitized filename fragment safe for local
            filesystem usage.
        """

        return "".strip().join(
            c if c.isalnum() or c in (" ", "_", "-") else "_" for c in filename
        )
