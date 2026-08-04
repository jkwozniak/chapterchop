# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from pathlib import Path

from chapterchop.writers import DirectoryWriter


def make_directory_writer(output_dir: Path, format: str) -> DirectoryWriter:
    return DirectoryWriter(
        output_dir=output_dir,
        format=format,
    )
