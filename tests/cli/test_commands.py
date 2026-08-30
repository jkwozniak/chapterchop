# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import argparse
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from chapterchop.cli.main import cmd_split
from chapterchop.exceptions import (
    AnalyzerError,
    ClfParserError,
)
from chapterchop.models import (
    Chapter,
    ChapterList,
    Segment,
)


@pytest.fixture
def mock_audio_data() -> MagicMock:
    """Mock audio data object returned by PydubAudioData.from_file()."""
    return MagicMock()


@pytest.fixture
def mock_chapters() -> list[Chapter]:
    """Mock chapters returned by analyzer.analyze()."""
    return [
        Chapter(start_ms=0, end_ms=5000),
        Chapter(start_ms=5000, end_ms=10000),
    ]


@pytest.fixture
def mock_segments() -> list[Segment]:
    """Mock segments returned by SimpleCutter.cut()."""
    return [
        MagicMock(spec=Segment),
        MagicMock(spec=Segment),
    ]


@pytest.fixture
def mock_chapter_list() -> ChapterList:
    """Mock chapter list returned by ClfParser.parse_file()."""
    return MagicMock(spec=ChapterList)


@pytest.fixture
def standard_workflow_args() -> argparse.Namespace:
    """Arguments for standard workflow (no CLF)."""
    return argparse.Namespace(
        input=Path("input.mp3"),
        output=Path("output"),
        format="wav",
        parts=4,
        clf=None,
        verbose=False,
    )


@pytest.fixture
def clf_workflow_args() -> argparse.Namespace:
    """Arguments for CLF workflow."""
    return argparse.Namespace(
        input=Path("input.mp3"),
        output=Path("output"),
        format="mp3",
        clf=Path("chapters.clf"),
        verbose=False,
    )


# ============================================================
# Error Propagation
# ============================================================


@pytest.mark.unit
def test_propagates_error_from_pydub_audio_data(
    standard_workflow_args: argparse.Namespace,
) -> None:
    """
    When PydubAudioData.from_file() raises an error,
    cmd_split() should propagate it without catching.
    """
    with patch("chapterchop.cli.main.PydubAudioData") as mock_pydub_class:
        mock_pydub_class.from_file.side_effect = AnalyzerError("Cannot load audio file")

        with pytest.raises(AnalyzerError) as exc_info:
            cmd_split(standard_workflow_args)

        assert str(exc_info.value) == "Cannot load audio file"


@pytest.mark.unit
def test_propagates_error_from_analyzer(
    standard_workflow_args: argparse.Namespace,
    mock_audio_data: MagicMock,
) -> None:
    """
    When analyzer.analyze() raises an error,
    cmd_split() should propagate it without catching.
    """
    with (
        patch("chapterchop.cli.main.PydubAudioData") as mock_pydub_class,
        patch("chapterchop.cli.main.EvenSplitAnalyzer") as mock_analyzer_class,
    ):
        mock_pydub_class.from_file.return_value = mock_audio_data
        mock_analyzer = Mock()
        mock_analyzer.analyze.side_effect = AnalyzerError(
            "Audio too short for 4 chapters"
        )
        mock_analyzer_class.return_value = mock_analyzer

        with pytest.raises(AnalyzerError) as exc_info:
            cmd_split(standard_workflow_args)

        assert str(exc_info.value) == "Audio too short for 4 chapters"


@pytest.mark.unit
def test_propagates_error_from_clf_parser(
    clf_workflow_args: argparse.Namespace,
    mock_audio_data: MagicMock,
) -> None:
    """
    When ClfParser.parse_file() raises an error,
    cmd_split() should propagate it without catching.
    """

    with (
        patch("chapterchop.cli.main.PydubAudioData") as mock_pydub_class,
        patch("chapterchop.cli.main.ClfParser") as mock_parser_class,
    ):
        mock_pydub_class.from_file.return_value = mock_audio_data
        mock_parser = Mock()
        mock_parser.parse_file.side_effect = ClfParserError("Invalid CLF file format")
        mock_parser_class.return_value = mock_parser

        with pytest.raises(ClfParserError) as exc_info:
            cmd_split(clf_workflow_args)

        assert str(exc_info.value) == "Invalid CLF file format"


# ============================================================
# Standard Workflow
# ============================================================


@pytest.mark.unit
def test_standard_workflow_selects_correct_analyzer_and_creates_pipeline(
    standard_workflow_args: argparse.Namespace,
    mock_audio_data: MagicMock,
    mock_chapters: list[Chapter],
    mock_segments: list[Segment],
) -> None:
    """
    Standard workflow: when clf is None, the pipeline should be:
    PydubAudioData -> EvenSplitAnalyzer -> SimpleCutter -> DirectoryWriter

    Verifies:
    - PydubAudioData.from_file() is called with correct path
    - EvenSplitAnalyzer is initialized with correct parts count
    - EvenSplitAnalyzer.analyze() receives the audio data
    - SimpleCutter.cut() receives the audio data and chapters from analyzer
    - DirectoryWriter is initialized with correct output and format
    - DirectoryWriter.write() receives segments from cutter
    - ChapterListAnalyzer and ClfParser are NOT used
    - Command returns 0
    """
    with (
        patch("chapterchop.cli.main.PydubAudioData") as mock_pydub_class,
        patch("chapterchop.cli.main.EvenSplitAnalyzer") as mock_even_split_class,
        patch("chapterchop.cli.main.SimpleCutter") as mock_cutter_class,
        patch("chapterchop.cli.main.DirectoryWriter") as mock_writer_class,
        patch("chapterchop.cli.main.ClfParser") as mock_clf_parser_class,
        patch(
            "chapterchop.cli.main.ChapterListAnalyzer"
        ) as mock_chapter_list_analyzer_class,
    ):
        # Set up mock return values
        mock_pydub_class.from_file.return_value = mock_audio_data
        mock_analyzer = Mock()
        mock_analyzer.analyze.return_value = mock_chapters
        mock_even_split_class.return_value = mock_analyzer
        mock_cutter = Mock()
        mock_cutter.cut.return_value = mock_segments
        mock_cutter_class.return_value = mock_cutter
        mock_writer = Mock()
        mock_writer.write.return_value = [Path("output/file1.wav")]
        mock_writer_class.return_value = mock_writer

        # Execute
        result = cmd_split(standard_workflow_args)

        # Verify PydubAudioData
        mock_pydub_class.from_file.assert_called_once_with(
            path=standard_workflow_args.input
        )

        # Verify EvenSplitAnalyzer
        mock_even_split_class.assert_called_once_with(
            parts=standard_workflow_args.parts
        )
        mock_analyzer.analyze.assert_called_once_with(audio=mock_audio_data)

        # Verify SimpleCutter
        mock_cutter_class.assert_called_once_with()
        mock_cutter.cut.assert_called_once_with(
            audio=mock_audio_data, chapters=mock_chapters
        )

        # Verify DirectoryWriter
        mock_writer_class.assert_called_once_with(
            output_dir=standard_workflow_args.output,
            format=standard_workflow_args.format,
        )
        mock_writer.write.assert_called_once_with(segments=mock_segments)

        # Verify CLF-specific components are NOT used
        mock_clf_parser_class.assert_not_called()
        mock_chapter_list_analyzer_class.assert_not_called()

        # Verify return value
        assert result == 0


@pytest.mark.unit
def test_standard_workflow_non_verbose_produces_no_output(
    standard_workflow_args: argparse.Namespace,
    mock_audio_data: MagicMock,
    mock_chapters: list[Chapter],
    mock_segments: list[Segment],
    capsys,
) -> None:
    """
    When verbose=False, cmd_split() should not write to stdout.
    """
    with (
        patch("chapterchop.cli.main.PydubAudioData") as mock_pydub_class,
        patch("chapterchop.cli.main.EvenSplitAnalyzer") as mock_analyzer_class,
        patch("chapterchop.cli.main.SimpleCutter") as mock_cutter_class,
        patch("chapterchop.cli.main.DirectoryWriter") as mock_writer_class,
    ):
        mock_pydub_class.from_file.return_value = mock_audio_data
        mock_analyzer = Mock()
        mock_analyzer.analyze.return_value = mock_chapters
        mock_analyzer_class.return_value = mock_analyzer
        mock_cutter = Mock()
        mock_cutter.cut.return_value = mock_segments
        mock_cutter_class.return_value = mock_cutter
        mock_writer = Mock()
        mock_writer.write.return_value = [Path("output/file1.wav")]
        mock_writer_class.return_value = mock_writer

        cmd_split(standard_workflow_args)

        captured = capsys.readouterr()
        assert captured.out == ""


@pytest.mark.unit
def test_standard_workflow_verbose_produces_expected_output(
    mock_audio_data: MagicMock,
    mock_chapters: list[Chapter],
    mock_segments: list[Segment],
    capsys,
) -> None:
    """
    When verbose=True and no CLF, cmd_split() should print expected messages
    in the expected order.
    """
    args = argparse.Namespace(
        input=Path("podcast.mp3"),
        output=Path("chapters"),
        format="wav",
        parts=3,
        clf=None,
        verbose=True,
    )

    with (
        patch("chapterchop.cli.main.PydubAudioData") as mock_pydub_class,
        patch("chapterchop.cli.main.EvenSplitAnalyzer") as mock_analyzer_class,
        patch("chapterchop.cli.main.SimpleCutter") as mock_cutter_class,
        patch("chapterchop.cli.main.DirectoryWriter") as mock_writer_class,
    ):
        mock_pydub_class.from_file.return_value = mock_audio_data
        mock_analyzer = Mock()
        mock_analyzer.analyze.return_value = mock_chapters
        mock_analyzer_class.return_value = mock_analyzer
        mock_cutter = Mock()
        mock_cutter.cut.return_value = mock_segments
        mock_cutter_class.return_value = mock_cutter
        output_paths = [Path("chapters/part1.wav"), Path("chapters/part2.wav")]
        mock_writer = Mock()
        mock_writer.write.return_value = output_paths
        mock_writer_class.return_value = mock_writer

        cmd_split(args)

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")

        # Verify complete expected output in order
        assert lines[0] == "Splitting podcast.mp3 into 3 parts"
        assert lines[1] == "Results will be written to the chapters directory"
        assert lines[2] == "Loading file: podcast.mp3"
        assert lines[3] == "Analyzing chapters..."
        assert lines[4] == "Cutting audio..."
        assert lines[5] == "Writing output files..."
        assert lines[6] == "Created: chapters/part1.wav"
        assert lines[7] == "Created: chapters/part2.wav"
        assert lines[8] == "Created 2 files"


# ============================================================
# CLF Workflow
# ============================================================


@pytest.mark.unit
def test_clf_workflow_selects_correct_analyzer_and_creates_pipeline(
    clf_workflow_args: argparse.Namespace,
    mock_audio_data: MagicMock,
    mock_chapter_list: ChapterList,
    mock_chapters: list[Chapter],
    mock_segments: list[Segment],
) -> None:
    """
    CLF workflow: when clf is provided, the pipeline should be:
    PydubAudioData -> ClfParser -> ChapterListAnalyzer ->
    SimpleCutter -> DirectoryWriter

    Verifies:
    - PydubAudioData.from_file() is called with correct path
    - ClfParser is initialized and parse_file() is called with correct path
    - ChapterListAnalyzer is initialized with the parsed chapter list
    - ChapterListAnalyzer.analyze() receives the audio data
    - SimpleCutter.cut() receives the audio data and chapters from analyzer
    - DirectoryWriter is initialized with correct output and format
    - DirectoryWriter.write() receives segments from cutter
    - EvenSplitAnalyzer is NOT used
    - Command returns 0
    """
    with (
        patch("chapterchop.cli.main.PydubAudioData") as mock_pydub_class,
        patch("chapterchop.cli.main.ClfParser") as mock_clf_parser_class,
        patch(
            "chapterchop.cli.main.ChapterListAnalyzer"
        ) as mock_chapter_list_analyzer_class,
        patch("chapterchop.cli.main.SimpleCutter") as mock_cutter_class,
        patch("chapterchop.cli.main.DirectoryWriter") as mock_writer_class,
        patch("chapterchop.cli.main.EvenSplitAnalyzer") as mock_even_split_class,
    ):
        # Set up mock return values
        mock_pydub_class.from_file.return_value = mock_audio_data
        mock_parser = Mock()
        mock_parser.parse_file.return_value = mock_chapter_list
        mock_clf_parser_class.return_value = mock_parser
        mock_analyzer = Mock()
        mock_analyzer.analyze.return_value = mock_chapters
        mock_chapter_list_analyzer_class.return_value = mock_analyzer
        mock_cutter = Mock()
        mock_cutter.cut.return_value = mock_segments
        mock_cutter_class.return_value = mock_cutter
        mock_writer = Mock()
        mock_writer.write.return_value = [Path("output/file1.mp3")]
        mock_writer_class.return_value = mock_writer

        # Execute
        result = cmd_split(clf_workflow_args)

        # Verify PydubAudioData
        mock_pydub_class.from_file.assert_called_once_with(path=clf_workflow_args.input)

        # Verify ClfParser
        mock_clf_parser_class.assert_called_once_with()
        mock_parser.parse_file.assert_called_once_with(path=clf_workflow_args.clf)

        # Verify ChapterListAnalyzer
        mock_chapter_list_analyzer_class.assert_called_once_with(
            chapter_list=mock_chapter_list
        )
        mock_analyzer.analyze.assert_called_once_with(audio=mock_audio_data)

        # Verify SimpleCutter
        mock_cutter_class.assert_called_once_with()
        mock_cutter.cut.assert_called_once_with(
            audio=mock_audio_data, chapters=mock_chapters
        )

        # Verify DirectoryWriter
        mock_writer_class.assert_called_once_with(
            output_dir=clf_workflow_args.output,
            format=clf_workflow_args.format,
        )
        mock_writer.write.assert_called_once_with(segments=mock_segments)

        # Verify EvenSplitAnalyzer is NOT used
        mock_even_split_class.assert_not_called()

        # Verify return value
        assert result == 0


@pytest.mark.unit
def test_clf_workflow_non_verbose_produces_no_output(
    clf_workflow_args: argparse.Namespace,
    mock_audio_data: MagicMock,
    mock_chapter_list: ChapterList,
    mock_chapters: list[Chapter],
    mock_segments: list[Segment],
    capsys,
) -> None:
    """
    When verbose=False with CLF, cmd_split() should not write to stdout.
    """
    with (
        patch("chapterchop.cli.main.PydubAudioData") as mock_pydub_class,
        patch("chapterchop.cli.main.ClfParser") as mock_clf_parser_class,
        patch("chapterchop.cli.main.ChapterListAnalyzer") as mock_analyzer_class,
        patch("chapterchop.cli.main.SimpleCutter") as mock_cutter_class,
        patch("chapterchop.cli.main.DirectoryWriter") as mock_writer_class,
    ):
        mock_pydub_class.from_file.return_value = mock_audio_data
        mock_parser = Mock()
        mock_parser.parse_file.return_value = mock_chapter_list
        mock_clf_parser_class.return_value = mock_parser
        mock_analyzer = Mock()
        mock_analyzer.analyze.return_value = mock_chapters
        mock_analyzer_class.return_value = mock_analyzer
        mock_cutter = Mock()
        mock_cutter.cut.return_value = mock_segments
        mock_cutter_class.return_value = mock_cutter
        mock_writer = Mock()
        mock_writer.write.return_value = [Path("output/file1.mp3")]
        mock_writer_class.return_value = mock_writer

        cmd_split(clf_workflow_args)

        captured = capsys.readouterr()
        assert captured.out == ""


@pytest.mark.unit
def test_clf_workflow_verbose_produces_expected_output(
    mock_audio_data: MagicMock,
    mock_chapter_list: ChapterList,
    mock_chapters: list[Chapter],
    mock_segments: list[Segment],
    capsys,
) -> None:
    """
    When verbose=True and CLF is provided, cmd_split() should print expected
    messages in the expected order.
    """
    args = argparse.Namespace(
        input=Path("podcast.mp3"),
        output=Path("chapters"),
        format="mp3",
        parts=4,
        clf=Path("chapters.clf"),
        verbose=True,
    )

    with (
        patch("chapterchop.cli.main.PydubAudioData") as mock_pydub_class,
        patch("chapterchop.cli.main.ClfParser") as mock_clf_parser_class,
        patch("chapterchop.cli.main.ChapterListAnalyzer") as mock_analyzer_class,
        patch("chapterchop.cli.main.SimpleCutter") as mock_cutter_class,
        patch("chapterchop.cli.main.DirectoryWriter") as mock_writer_class,
    ):
        mock_pydub_class.from_file.return_value = mock_audio_data
        mock_parser = Mock()
        mock_parser.parse_file.return_value = mock_chapter_list
        mock_clf_parser_class.return_value = mock_parser
        mock_analyzer = Mock()
        mock_analyzer.analyze.return_value = mock_chapters
        mock_analyzer_class.return_value = mock_analyzer
        mock_cutter = Mock()
        mock_cutter.cut.return_value = mock_segments
        mock_cutter_class.return_value = mock_cutter
        output_paths = [Path("chapters/intro.mp3"), Path("chapters/main.mp3")]
        mock_writer = Mock()
        mock_writer.write.return_value = output_paths
        mock_writer_class.return_value = mock_writer

        cmd_split(args)

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")

        # Verify complete expected output in order
        assert lines[0] == "Splitting podcast.mp3 using chapters from chapters.clf"
        assert lines[1] == "Results will be written to the chapters directory"
        assert lines[2] == "Loading file: podcast.mp3"
        assert lines[3] == "Analyzing chapters..."
        assert lines[4] == "Cutting audio..."
        assert lines[5] == "Writing output files..."
        assert lines[6] == "Created: chapters/intro.mp3"
        assert lines[7] == "Created: chapters/main.mp3"
        assert lines[8] == "Created 2 files"
