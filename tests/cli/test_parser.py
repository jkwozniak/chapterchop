# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import argparse
from pathlib import Path

import pytest

from chapterchop.cli.main import build_parser, cmd_split


@pytest.fixture
def parser() -> argparse.ArgumentParser:
    return build_parser()


@pytest.mark.unit
def test_build_parser_returns_argument_parser(
    parser: argparse.ArgumentParser,
) -> None:
    assert isinstance(parser, argparse.ArgumentParser)


@pytest.mark.unit
def test_split_command_selects_split_handler(
    parser: argparse.ArgumentParser,
) -> None:
    args = parser.parse_args(["split", "--input", "input.mp3", "--output", "output"])

    assert args.command == "split"
    assert args.func is cmd_split


@pytest.mark.unit
def test_split_requires_input(parser: argparse.ArgumentParser) -> None:
    with pytest.raises(SystemExit):
        parser.parse_args(["split", "--output", "output"])


@pytest.mark.unit
def test_split_requires_output(parser: argparse.ArgumentParser) -> None:
    with pytest.raises(SystemExit):
        parser.parse_args(["split", "--input", "input.mp3"])


@pytest.mark.unit
def test_split_accepts_required_arguments(
    parser: argparse.ArgumentParser,
) -> None:
    args = parser.parse_args(["split", "--input", "input.mp3", "--output", "output"])

    assert args.input == Path("input.mp3")
    assert args.output == Path("output")


@pytest.mark.unit
def test_split_uses_existing_option_defaults(
    parser: argparse.ArgumentParser,
) -> None:
    args = parser.parse_args(["split", "--input", "input.mp3", "--output", "output"])

    assert args.format == "wav"
    assert args.parts == 4
    assert args.verbose is False


@pytest.mark.unit
def test_split_preserves_user_provided_options(
    parser: argparse.ArgumentParser,
) -> None:
    args = parser.parse_args(
        [
            "split",
            "--input",
            "input.mp3",
            "--output",
            "output",
            "--format",
            "ogg",
            "--parts",
            "7",
            "--verbose",
        ]
    )

    assert args.format == "ogg"
    assert args.parts == 7
    assert args.verbose is True


@pytest.mark.unit
def test_split_accepts_clf_without_explicit_parts(
    parser: argparse.ArgumentParser,
) -> None:
    args = parser.parse_args(
        [
            "split",
            "--input",
            "input.mp3",
            "--output",
            "output",
            "--clf",
            "chapters.clf",
        ]
    )

    assert args.clf == Path("chapters.clf")


@pytest.mark.unit
def test_split_accepts_parts_without_clf(
    parser: argparse.ArgumentParser,
) -> None:
    args = parser.parse_args(
        [
            "split",
            "--input",
            "input.mp3",
            "--output",
            "output",
            "--parts",
            "3",
        ]
    )

    assert args.parts == 3
    assert args.clf is None


@pytest.mark.unit
def test_split_rejects_parts_and_clf_together(
    parser: argparse.ArgumentParser,
) -> None:
    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "split",
                "--input",
                "input.mp3",
                "--output",
                "output",
                "--parts",
                "3",
                "--clf",
                "chapters.clf",
            ]
        )
