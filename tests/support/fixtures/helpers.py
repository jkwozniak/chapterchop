# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from collections.abc import Callable
from typing import TypeVar

import pytest
from pytest import FixtureRequest

T = TypeVar("T")


# Helper for simple parametrized contract fixtures based solely
# on zero-argument factories.
# Components requiring additional pytest-managed resources
# (e.g. tmp_path, monkeypatch, environment setup)
# should define dedicated fixtures explicitly.
def simple_parametrized_fixture_factory(
    factories: list[Callable[[], T]],
):
    @pytest.fixture(params=factories)
    def _fixture(request: FixtureRequest) -> T:
        factory: Callable[[], T] = request.param
        return factory()

    return _fixture
