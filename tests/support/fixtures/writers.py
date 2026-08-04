# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from collections.abc import Callable
from pathlib import Path

import pytest
from pytest import FixtureRequest

from chapterchop.writers import DirectoryWriter, Writer
from tests.support.factories.writers import (
    make_directory_writer,
)

WriterFactory = Callable[..., Writer]

WRITER_FACTORIES: list[WriterFactory] = [
    lambda path, format: make_directory_writer(output_dir=path, format=format),
]

DEFAULT_EXPORT_FORMAT = "wav"


@pytest.fixture(params=WRITER_FACTORIES)
def writer(
    request: FixtureRequest,
    tmp_path: Path,
) -> Writer:
    factory: WriterFactory = request.param
    return factory(path=tmp_path, format=DEFAULT_EXPORT_FORMAT)


@pytest.fixture
def directory_writer_factory(
    tmp_path: Path,
) -> Callable[..., DirectoryWriter]:
    def factory(format: str = "wav", directory: str | None = None) -> DirectoryWriter:
        output_dir = tmp_path / directory if directory is not None else tmp_path
        return make_directory_writer(
            output_dir=output_dir,
            format=format,
        )

    return factory
