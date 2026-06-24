# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak


from pathlib import Path

import pytest

from chapterchop.audio_data.protocols import WritableAudioData

# ============================================================
# GENERAL CONTRACT COMPLIANCE
# ============================================================


@pytest.mark.contract
def test_export_creates_output_file(
    writable_audio_data: WritableAudioData,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "test.wav"

    writable_audio_data.export(
        output_path=output_path,
        format="wav",
    )

    assert output_path.exists()


@pytest.mark.contract
def test_export_rejects_invalid_path(
    writable_audio_data: WritableAudioData,
    tmp_path: Path,
) -> None:
    invalid_output_path = tmp_path / "?/*\0."

    with pytest.raises(ValueError):
        writable_audio_data.export(
            output_path=invalid_output_path,
            format="wav",
        )


# ============================================================
# IMMUTABILITY GUARANTEES
# ============================================================

# The WritableAudioData contract guarantees that export operations
# must not mutate the original audio object.
# However, WritableAudioData itself does not define any observable
# state that could be verified in a backend-independent way.
# Therefore, immutability guarantees should be validated in the
# implementation-specific test suites.


# ============================================================
# ERROR HANDLING
# ============================================================

# The WritableAudioData contract requires an AudioBackendError to be raised
# if the underlying audio backend fails during export.
# However, verifying this requirement depends on the backend implementation
# and cannot be done at the contract level without introducing artificial workarounds.
# Therefore, to avoid unnecessarily complicating the protocol structure,
# this condition should be verified in unit tests for each implementation.
