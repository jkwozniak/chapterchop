# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from collections.abc import Callable

import pytest

from chapterchop.audio_data.protocols import AudioData
from chapterchop.audio_data.pydub import PydubAudioData
from tests.support.factories.audio_data import (
    make_pydub_audio_data,
)
from tests.support.fixtures.helpers import simple_parametrized_fixture_factory

AudioDataFactory = Callable[[], AudioData]

AUDIO_DATA_FACTORIES: list[AudioDataFactory] = [
    make_pydub_audio_data,
]

WRITABLE_AUDIO_DATA_FACTORIES: list[AudioDataFactory] = [
    make_pydub_audio_data,
]


audio_data = simple_parametrized_fixture_factory(
    AUDIO_DATA_FACTORIES,
)

writable_audio_data = simple_parametrized_fixture_factory(
    WRITABLE_AUDIO_DATA_FACTORIES,
)


@pytest.fixture
def pydub_audio_data() -> PydubAudioData:
    return make_pydub_audio_data()
