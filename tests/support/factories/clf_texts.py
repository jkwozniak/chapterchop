# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Jan Woźniak


# ---------------------------------------------------------------------------
# Valid CLF texts
# ---------------------------------------------------------------------------


def make_valid_timestamp_only_text() -> str:
    return "0:00\n0:05\n0:10\n"


def make_valid_timestamp_with_titles_text() -> str:
    return "0:00 - Intro\n0:05 - Prerequisites\n0:10 - Bonus Track\n"


# ---------------------------------------------------------------------------
# Inavlid CLF texts
# ---------------------------------------------------------------------------


def make_invalid_empty_line_text() -> str:
    return "0:00 - Intro\n\n0:10 - Track 2\n"


def make_invalid_leading_whitespace_text() -> str:
    return " 0:00 - Intro\n"


def make_invalid_line_carriage_return_text() -> str:
    return "00 Intro\r"


def make_invalid_non_increasing_timestamp_text() -> str:
    return "0:10\n0:05\n"


def make_invalid_separator_text() -> str:
    return "0:10>>Title\n"


def make_invalid_timestamp_format_text() -> str:
    return "00 Intro\n"


def make_invalid_trailing_whitespace_text() -> str:
    return "0:00 - Intro   \n"
