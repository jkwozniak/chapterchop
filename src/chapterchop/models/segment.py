# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from dataclasses import dataclass

from chapterchop.audio_data.protocols import AudioData

from .chapter import Chapter


@dataclass(frozen=True, slots=True)
class Segment:
    """
    An audio fragment extracted from the source material as a chapter.

    It contains raw audio data along with corresponding chapter identification data.
    It does not impose any audio data format, but enforces compliance with the
    AudioData protocol.
    """

    audio: AudioData
    chapter: Chapter
