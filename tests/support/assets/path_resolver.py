# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from pathlib import Path

from tests.support.assets.registry import TestAsset

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ASSETS_ROOT = PROJECT_ROOT / "tests" / "assets"


def resolve(asset: TestAsset) -> Path:
    return ASSETS_ROOT / asset.value
