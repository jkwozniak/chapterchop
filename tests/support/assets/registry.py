# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from enum import StrEnum


class AudioAsset(StrEnum):
    SILENCE_1S_MONO_WAV = "audio/silence/silence_1s_mono.wav"
    SILENCE_1S_MONO_MP3 = "audio/silence/silence_1s_mono.mp3"

    TONE_440HZ_1S_MONO_WAV = "audio/tone/tone440_1s_mono.wav"
    TONE_440HZ_1S_MONO_MP3 = "audio/tone/tone440_1s_mono.mp3"
    TONE_440HZ_1S_STEREO_WAV = "audio/tone/tone440_1s_stereo.wav"
    TONE_440HZ_1S_STEREO_MP3 = "audio/tone/tone440_1s_stereo.mp3"
    TONE_440HZ_10S_MONO_WAV = "audio/tone/tone440_10s_mono.wav"
    TONE_440HZ_10S_MONO_MP3 = "audio/tone/tone440_10s_mono.mp3"

    CORRUPTED_WAV = "audio/corrupted/corrupted.wav"
    CORRUPTED_MP3 = "audio/corrupted/corrupted.mp3"
