# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from pathlib import Path

import pytest

from tests.support.assets.path_resolver import resolve
from tests.support.assets.registry import AudioAsset


@pytest.fixture
def audio_asset():
    def _get_file(asset: AudioAsset) -> Path:
        return resolve(asset)

    return _get_file
