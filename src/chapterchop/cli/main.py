# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import argparse
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import cast

from ..analyzers.even_split import EvenSplitAnalyzer
from ..audio_data.pydub import PydubAudioData
from ..cutters.simple import SimpleCutter
from ..exceptions import ChapterChopError
from ..writers.directory import DirectoryWriter

try:
    __version__ = version("chapterchop")
except PackageNotFoundError:
    __version__ = "unknown"

# ============================================================
# COMMANDS
# ============================================================


def cmd_split(args: argparse.Namespace) -> int:
    if args.verbose:
        print(f"Splitting {args.input} into {args.parts} parts")
        print(f"Results will be written to the {args.output} directory")

    if args.verbose:
        print(f"Loading file: {args.input}")

    audio_data = PydubAudioData.from_file(path=args.input)

    if args.verbose:
        print("Analyzing chapters...")

    analyzer = EvenSplitAnalyzer(parts=args.parts)
    chapters = analyzer.analyze(audio=audio_data)

    if args.verbose:
        print("Cutting audio...")

    cutter = SimpleCutter()
    segments = cutter.cut(audio=audio_data, chapters=chapters)

    if args.verbose:
        print("Writing output files...")

    writer = DirectoryWriter(
        output_dir=args.output,
        format=args.format,
    )
    paths = writer.write(segments=segments)

    if args.verbose:
        for path in paths:
            print(f"Created: {path}")
        print(f"Created {len(paths)} files")

    return 0


# ============================================================
# PARSER
# ============================================================


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chapterchop",
        description="Offline audio chaptering and segmentation utility.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Example:\n  chapterchop split -i podcast.mp3 -o output -p 10"),
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="print version number and exit",
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
        required=True,
    )

    parser_split = subparsers.add_parser(
        "split",
        help="Split audio file into parts",
        description=(
            "Analyze an audio file, split it into chapters, "
            "and write the resulting segments to disk."
        ),
    )
    parser_split.add_argument(
        "-i",
        "--input",
        metavar="PATH",
        type=Path,
        required=True,
        help="Path to the input audio file",
    )
    parser_split.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        type=Path,
        required=True,
        help="Directory where output files will be written",
    )
    parser_split.add_argument(
        "-f",
        "--format",
        type=str,
        default="wav",
        metavar="FORMAT",
        help="Output audio format: 'wav' (default), 'mp3' or 'ogg'",
    )
    parser_split.add_argument(
        "-p",
        "--parts",
        type=int,
        default=4,
        metavar="N",
        help="Number of equally sized chapters to be created (default: 4)",
    )
    parser_split.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed processing information",
    )
    parser_split.set_defaults(func=cmd_split)

    return parser


# ============================================================
# MAIN
# ============================================================


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return cast(int, args.func(args))
    except ChapterChopError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
