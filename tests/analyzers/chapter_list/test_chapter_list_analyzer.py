# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak

import pytest
from support.factories.chapter_lists import make_chapter_list
from support.stubs.audio_data import AudioDataStub

from chapterchop.analyzers.chapter_list import ChapterListAnalyzer
from chapterchop.exceptions import (
    AnalyzerError,
    ChapterListOutOfBoundsError,
    InvalidChapterEntryError,
    InvalidChapterListError,
)


@pytest.mark.unit
def test_init_accepts_valid_chapter_list() -> None:
    chapter_list = make_chapter_list((0, "Intro"), (100, "Main"))

    analyzer = ChapterListAnalyzer(chapter_list)

    assert isinstance(analyzer, ChapterListAnalyzer)


@pytest.mark.unit
def test_init_accepts_empty_chapter_list() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list())

    assert isinstance(analyzer, ChapterListAnalyzer)


@pytest.mark.unit
def test_init_accepts_chapter_list_whose_first_entry_does_not_start_at_zero() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list((100, "Chapter")))

    assert isinstance(analyzer, ChapterListAnalyzer)


@pytest.mark.unit
def test_init_rejects_chapter_entry_with_invalid_timestamp() -> None:
    with pytest.raises(InvalidChapterEntryError):
        ChapterListAnalyzer(make_chapter_list((-1, "Invalid")))


@pytest.mark.unit
def test_init_rejects_chapter_entry_with_invalid_title() -> None:
    with pytest.raises(InvalidChapterEntryError):
        ChapterListAnalyzer(make_chapter_list((0, 123)))  # pyright: ignore[reportArgumentType]


@pytest.mark.unit
def test_init_rejects_unsorted_chapter_list() -> None:
    with pytest.raises(InvalidChapterListError):
        ChapterListAnalyzer(make_chapter_list((100, "Second"), (0, "First")))


@pytest.mark.unit
def test_init_rejects_duplicate_start_times() -> None:
    with pytest.raises(InvalidChapterListError):
        ChapterListAnalyzer(make_chapter_list((0, "First"), (0, "Second")))


@pytest.mark.unit
def test_analyze_creates_one_chapter_per_entry() -> None:
    analyzer = ChapterListAnalyzer(
        make_chapter_list((0, "First"), (100, "Second"), (200, "Third"))
    )

    result = analyzer.analyze(AudioDataStub(300))

    assert len(result) == 3


@pytest.mark.unit
def test_analyze_preserves_chapter_entry_order() -> None:
    analyzer = ChapterListAnalyzer(
        make_chapter_list((0, "First"), (100, "Second"), (200, "Third"))
    )

    result = analyzer.analyze(AudioDataStub(300))

    assert [chapter.title for chapter in result] == ["First", "Second", "Third"]


@pytest.mark.unit
def test_analyze_uses_entry_start_as_chapter_start() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list((25, "Chapter")))

    result = analyzer.analyze(AudioDataStub(100))

    assert result[0].start_ms == 25


@pytest.mark.unit
def test_analyze_uses_next_entry_start_as_chapter_end() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list((0, "First"), (125, "Second")))

    result = analyzer.analyze(AudioDataStub(200))

    assert result[0].end_ms == 125


@pytest.mark.unit
def test_analyze_uses_audio_duration_as_last_chapter_end() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list((25, "Chapter")))

    result = analyzer.analyze(AudioDataStub(100))

    assert result[0].end_ms == 100


@pytest.mark.unit
def test_analyze_preserves_entry_titles() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list((0, "Intro"), (100, None)))

    result = analyzer.analyze(AudioDataStub(200))

    assert [chapter.title for chapter in result] == ["Intro", None]


@pytest.mark.unit
def test_analyze_omits_audio_before_first_entry() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list((25, "Chapter")))

    result = analyzer.analyze(AudioDataStub(100))

    assert result[0].start_ms == 25


@pytest.mark.unit
def test_analyze_returns_empty_list_for_empty_chapter_list() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list())

    result = analyzer.analyze(AudioDataStub(100))

    assert result == []


@pytest.mark.unit
def test_analyze_rejects_non_positive_audio_duration() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list((0, "Chapter")))

    with pytest.raises(AnalyzerError):
        analyzer.analyze(AudioDataStub(0))


@pytest.mark.unit
def test_analyze_rejects_entry_at_audio_end() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list((100, "Chapter")))

    with pytest.raises(ChapterListOutOfBoundsError):
        analyzer.analyze(AudioDataStub(100))


@pytest.mark.unit
def test_analyze_rejects_entry_beyond_audio_end() -> None:
    analyzer = ChapterListAnalyzer(make_chapter_list((101, "Chapter")))

    with pytest.raises(ChapterListOutOfBoundsError):
        analyzer.analyze(AudioDataStub(100))
