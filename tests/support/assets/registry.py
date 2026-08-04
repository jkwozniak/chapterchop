# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from enum import StrEnum


class TestAsset(StrEnum):
    """
    Base class for all test asset identifiers.

    Each subclass of TestAsset must represent a set of test assets
    that actually exist in the project and contain their correct paths.
    The creator of a TestAsset subclass is responsible for ensuring
    that it works correctly with the path resolver.
    """


class AudioAsset(TestAsset):
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


class ClfAsset(TestAsset):
    VALID_TIMESTAMPS_ONLY = "clf/valid/timestamps_only.clf"
    VALID_TIMESTAMPS_WITH_TITLES = "clf/valid/timestamps_with_titles.clf"
    VALID_UNICODE_CHARS_TITLE = "clf/valid/unicode_chars_title.clf"

    INVALID_EMPTY_FILE = "clf/invalid/empty_file.clf"
    INVALID_EMPTY_LINE = "clf/invalid/empty_line.clf"
    INVALID_INCORRECT_LINE = "clf/invalid/incorrect_line.clf"
    INVALID_UTF8_WITH_BOM = "clf/invalid/utf8_with_bom.clf"
    INVALID_UTF8 = "clf/invalid/invalid_utf8.clf"
