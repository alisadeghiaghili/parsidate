"""
Utility helper functions for date operations and conversions.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from typing import Literal
from parsidate.formatting.locales import (
    PERSIAN_MONTH_NAMES_EN as PERSIAN_MONTH_NAMES,
    PERSIAN_MONTH_NAMES_FA as PERSIAN_MONTH_NAMES_PERSIAN,
    GREGORIAN_MONTH_NAMES_EN as GREGORIAN_MONTH_NAMES,
    PERSIAN_WEEKDAY_NAMES_EN as PERSIAN_WEEKDAY_NAMES,
    PERSIAN_WEEKDAY_NAMES_FA as PERSIAN_WEEKDAY_NAMES_PERSIAN,
    GREGORIAN_WEEKDAY_NAMES_EN as GREGORIAN_WEEKDAY_NAMES,
    PERSIAN_DIGITS,
    ENGLISH_DIGITS
)


def is_leap_year(
    year: int,
    calendar: Literal["jalali", "gregorian"] = "jalali"
) -> bool:
    if calendar == "jalali":
        breaks = [1, 5, 9, 13, 17, 22, 26, 30]
        cycle = year % 33
        return cycle in breaks
    else:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def days_in_month(
    year: int,
    month: int,
    calendar: Literal["jalali", "gregorian"] = "jalali"
) -> int:
    if calendar == "jalali":
        if month <= 6:
            return 31
        elif month <= 11:
            return 30
        else:
            return 30 if is_leap_year(year, "jalali") else 29
    else:
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 29 if is_leap_year(year, "gregorian") else 28


def month_name(
    month: int,
    locale: Literal["fa", "en"] = "en",
    calendar: Literal["jalali", "gregorian"] = "jalali"
) -> str:
    if not 1 <= month <= 12:
        raise ValueError(f"Month must be between 1 and 12, got {month}")
    if calendar == "jalali":
        return (
            PERSIAN_MONTH_NAMES_PERSIAN[month - 1]
            if locale == "fa"
            else PERSIAN_MONTH_NAMES[month - 1]
        )
    else:
        return GREGORIAN_MONTH_NAMES[month - 1]


def weekday_name(
    weekday: int,
    locale: Literal["fa", "en"] = "en",
    calendar: Literal["jalali", "gregorian"] = "jalali"
) -> str:
    if not 0 <= weekday <= 6:
        raise ValueError(f"Weekday must be between 0 and 6, got {weekday}")
    if calendar == "jalali":
        return (
            PERSIAN_WEEKDAY_NAMES_PERSIAN[weekday]
            if locale == "fa"
            else PERSIAN_WEEKDAY_NAMES[weekday]
        )
    else:
        return GREGORIAN_WEEKDAY_NAMES[weekday]


def to_persian_digits(text: str) -> str:
    return text.translate(str.maketrans(ENGLISH_DIGITS, PERSIAN_DIGITS))


def to_english_digits(text: str) -> str:
    return text.translate(str.maketrans(PERSIAN_DIGITS, ENGLISH_DIGITS))


def normalize_date_separator(date_str: str) -> str:
    return date_str.replace("-", "/").replace(".", "/").replace("_", "/")


def get_season(
    month: int,
    calendar: Literal["jalali", "gregorian"] = "jalali"
) -> str:
    if calendar == "jalali":
        if 1 <= month <= 3:
            return "Spring"
        elif 4 <= month <= 6:
            return "Summer"
        elif 7 <= month <= 9:
            return "Fall"
        else:
            return "Winter"
    else:
        if month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        elif month in [9, 10, 11]:
            return "Fall"
        else:
            return "Winter"
