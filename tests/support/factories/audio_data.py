# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from pydub import AudioSegment

from chapterchop.audio_data.pydub import PydubAudioData


def make_pydub_audio_data() -> PydubAudioData:
    return PydubAudioData(segment=AudioSegment.silent(duration=100))
