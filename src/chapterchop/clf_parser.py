# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import re
from os import PathLike
from pathlib import Path

from chapterchop.exceptions import (
    ClfParserError,
    InvalidChapterEntryError,
    InvalidChapterListError,
)
from chapterchop.models.chapter_entry import ChapterEntry
from chapterchop.models.chapter_list import ChapterList


class ClfParser:
    """
    Parser for Chapter List File (CLF).

    The parser reads CLF text, validates it according to the CLF
    specification, normalizes it line by line, and returns an immutable
    ChapterList.
    """

    _CHAPTER_LINE_RE = re.compile(
        r"^(?P<timestamp>(?:\d{1,2}:\d{2}|\d{1,2}:\d{2}:\d{2}))"
        r"(?:(?P<separator> - | )(?P<title>.+))?$"
    )

    def parse_file(self, path: str | PathLike[str]) -> ChapterList:
        """
        Read a CLF file from disk and return a normalized ChapterList.

        Args:
          - path (str | PathLike[str]): Path to a UTF-8 encoded CLF file.

        Returns:
          - ChapterList: A normalized ChapterList parsed from the CLF file.

        Raises:
          - ClfParserError: When the file cannot be read or decoded as UTF-8
                or when the file content does not comply with the CLF specification.
        """

        file_path = Path(path)

        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise ClfParserError("CLF file must be encoded as UTF-8.") from exc
        except OSError as exc:
            raise ClfParserError(f"Unable to read CLF file: {file_path}") from exc

        return self.parse_text(text)

    def parse_text(self, text: str) -> ChapterList:
        """
        Parse CLF text and return a normalized ChapterList.

        The method performs the CLF-specific syntax validation and
        semantic normalization required to construct a ChapterList.

        Parameters:
          - text: CLF content represented as text.

        Returns:
          - ChapterList: A normalized ChapterList parsed from the CLF file.

        Raises:
          - ClfParserError: When the supplied text does not comply with the
                CLF specification.
        """

        lines = self._read_text(text)
        entries = self._parse_lines(lines)
        chapter_entries = self._validate_entries(entries)
        return self._build_chapter_list(chapter_entries)

    def _read_text(self, text: str) -> list[str]:
        """Read and normalize the raw CLF text into a line list."""

        if text.startswith("\ufeff"):
            raise ClfParserError("CLF files must not contain a UTF-8 BOM.")

        if "\r" in text.replace("\r\n", ""):
            raise ClfParserError("CLF files must use LF or CRLF line endings.")

        lines = text.splitlines()

        if not lines:
            raise ClfParserError("CLF file must contain at least one chapter.")

        return lines

    def _parse_lines(self, lines: list[str]) -> list[tuple[int, str | None]]:
        """Parse each line of the CLF text into a normalized chapter entry."""

        result: list[tuple[int, str | None]] = []

        for line_number, raw_line in enumerate(lines, start=1):
            normalized_line = raw_line.rstrip()

            if normalized_line == "":
                raise ClfParserError(
                    f"Blank lines are not permitted in CLF content "
                    f"at line {line_number}."
                )

            if normalized_line.startswith(" "):
                raise ClfParserError(
                    f"Leading whitespace is not permitted in CLF content "
                    f"at line {line_number}."
                )

            match = self._CHAPTER_LINE_RE.fullmatch(normalized_line)
            if match is None:
                raise ClfParserError(f"Invalid chapter line at line {line_number}.")

            title = match.group("title") or None
            timestamp = match.group("timestamp")
            start_ms = self._timestamp_to_ms(timestamp)

            result.append((start_ms, title))

        return result

    def _validate_entries(
        self,
        entries: list[tuple[int, str | None]],
    ) -> tuple[ChapterEntry, ...]:
        """Validate parsed entries before constructing the final ChapterList."""

        if not entries:
            raise InvalidChapterListError(
                "ChapterList must contain at least one entry."
            )

        chapter_entries: list[ChapterEntry] = []

        for line_number, (start_ms, title) in enumerate(entries, start=1):
            if start_ms < 0:
                raise InvalidChapterEntryError(
                    f"Chapter entry start time must be non-negative "
                    f"at line {line_number}."
                )

            chapter_entries.append(ChapterEntry(start_ms=start_ms, title=title))

        previous_start_ms = chapter_entries[0].start_ms
        for chapter_entry in chapter_entries[1:]:
            if chapter_entry.start_ms <= previous_start_ms:
                raise InvalidChapterListError(
                    "Chapter entries must be sorted by start_ms "
                    "and have unique timestamps."
                )
            previous_start_ms = chapter_entry.start_ms

        return tuple(chapter_entries)

    def _build_chapter_list(
        self,
        entries: tuple[ChapterEntry, ...],
    ) -> ChapterList:
        """Construct an immutable ChapterList from validated entries."""

        return ChapterList(entries=entries)

    def _timestamp_to_ms(self, timestamp: str) -> int:
        """Convert a CLF timestamp into a millisecond count."""

        parts = timestamp.split(":")

        if len(parts) == 2:
            minutes_text, seconds_text = parts
            if len(minutes_text) not in {1, 2} or len(seconds_text) != 2:
                raise ClfParserError("Invalid timestamp format.")
            if not minutes_text.isdigit() or not seconds_text.isdigit():
                raise ClfParserError("Invalid timestamp format.")

            minutes = int(minutes_text)
            seconds = int(seconds_text)
            if not (0 <= minutes <= 59 and 0 <= seconds <= 59):
                raise ClfParserError("Timestamp values must be within the range 0..59.")

            return minutes * 60_000 + seconds * 1_000

        if len(parts) == 3:
            hours_text, minutes_text, seconds_text = parts
            if (
                len(hours_text) not in {1, 2}
                or len(minutes_text) != 2
                or len(seconds_text) != 2
            ):
                raise ClfParserError("Invalid timestamp format.")
            if (
                not hours_text.isdigit()
                or not minutes_text.isdigit()
                or not seconds_text.isdigit()
            ):
                raise ClfParserError("Invalid timestamp format.")

            hours = int(hours_text)
            minutes = int(minutes_text)
            seconds = int(seconds_text)
            if not (0 <= hours <= 59 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                raise ClfParserError("Timestamp values must be within the range 0..59.")

            return hours * 3_600_000 + minutes * 60_000 + seconds * 1_000

        raise ClfParserError("Invalid timestamp format.")
