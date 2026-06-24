# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

from os import PathLike

from pydub.exceptions import CouldntEncodeError


class FailingSliceSegment:
    def __getitem__(self, item):
        raise Exception("Simulated backend slice failure")

    def __len__(self):
        return 100


class FailingExportSegment:
    def export(self, out_f: str | PathLike[str], format: str):
        raise CouldntEncodeError("Simulated backend export failure")

    def __len__(self):
        return 100
