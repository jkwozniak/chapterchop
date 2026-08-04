# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from chapterchop.audio_data import AudioData
from chapterchop.cutters import Cutter
from chapterchop.models import Chapter, Segment


class CutterStub(Cutter):
    def __init__(self, result: list[Segment]) -> None:
        self._result = result

    def cut(self, audio: AudioData, chapters: list[Chapter]) -> list[Segment]:
        return self._result
