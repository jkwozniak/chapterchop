# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from collections.abc import Callable

from support.stubs.audio_data import AudioDataStub, WritableAudioDataStub

from chapterchop.audio_data.protocols import AudioData
from chapterchop.models import Chapter, Segment


def make_segment(
    start: int,
    end: int,
    *,
    audio: AudioData,
    title: str | None = None,
) -> Segment:
    return Segment(
        audio=audio,
        chapter=Chapter(start, end, title=title),
    )


def make_segments(
    durations: list[int],
    *,
    audio_factory: Callable[[int], AudioData],
    title_prefix: str | None = None,
) -> list[Segment]:
    """
    Creates multiple segments. Usage:
    `make_segments([50, 50], audio_factory=WritableAudioDataStub, title_prefix="s")`
    Notice: uses same `audio_factory` for all segments.
    """
    segments = []

    current_start = 0
    for i, duration in enumerate(durations, start=1):
        audio = audio_factory(duration)

        title = f"{title_prefix}_{i}" if title_prefix else None

        segments.append(
            Segment(
                audio=audio,
                chapter=Chapter(current_start, current_start + duration, title=title),
            )
        )

        current_start += duration

    return segments


def make_segments_mixed_writability() -> list[Segment]:
    return [
        make_segment(0, 10, audio=WritableAudioDataStub(10)),
        make_segment(10, 20, audio=AudioDataStub(10)),
    ]


def make_segments_empty_title() -> list[Segment]:
    return [
        make_segment(0, 10, audio=WritableAudioDataStub(10), title=""),
        make_segment(10, 20, audio=WritableAudioDataStub(10), title=""),
    ]
