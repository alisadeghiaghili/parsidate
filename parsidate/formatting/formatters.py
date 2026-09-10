"""
Date formatting functions for Jalali (Persian) and Gregorian dates.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from typing import Any, Literal
from parsidate.formatting.locales import (
    get_month_name,
    get_weekday_name,
    PERSIAN_DIGITS,
    ENGLISH_DIGITS
)


def to_persian_digits(text: str) -> str:
    """Convert English digits to Persian."""
    trans = str.maketrans(ENGLISH_DIGITS, PERSIAN_DIGITS)
    return text.translate(trans)


def to_english_digits(text: str) -> str:
    """Convert Persian digits to English."""
    trans = str.maketrans(PERSIAN_DIGITS, ENGLISH_DIGITS)
    return text.translate(trans)


def format_jalali_date(
    date: Any,
    pattern: str,
    locale: Literal["fa", "en"] = "fa"
) -> str:
    """
    Format JalaliDate using strftime-style format codes.

    Format codes (compatible with Python's strftime):
        %Y - 4-digit year (1402)
        %y - 2-digit year (02)
        %m - month with leading zero (01-12)
        %d - day with leading zero (01-31)
        %H - hour with leading zero (00-23)
        %I - hour 12-hour format (01-12)
        %M - minute with leading zero (00-59)
        %S - second with leading zero (00-59)
        %f - microsecond (000000-999999)
        %p - AM/PM (for 12-hour format)
        %B - full month name (Farvardin, فروردین)
        %b - abbreviated month name (Far, فرو)
        %A - full weekday name (Shanbe, شنبه)
        %a - abbreviated weekday name (Sha, ش)
        %w - weekday as number (0=Saturday)
        %j - day of year (001-366)
        %U - week number (00-53)
        %% - literal %

        Non-standard extensions:
        %-m - month without leading zero (1-12)
        %-d - day without leading zero (1-31)
        %-H - hour without leading zero (0-23)
        %-I - hour 12-hour without leading zero (1-12)
        %-M - minute without leading zero (0-59)
        %-S - second without leading zero (0-59)

    Example:
        >>> jdate = JalaliDate(1402, 8, 18, 14, 45, 30)
        >>> jdate.strftime("%Y/%m/%d %H:%M:%S")
        '1402/08/18 14:45:30'
        >>> jdate.strftime("%A, %d %B %Y", locale="fa")
        'سه‌شنبه، ۱۸ آبان ۱۴۰۲'
    """

    # Helper for 12-hour format
    hour_12 = date.hour() % 12
    if hour_12 == 0:
        hour_12 = 12
    am_pm = "AM" if date.hour() < 12 else "PM"
    if locale == "fa":
        am_pm = "ق.ظ" if date.hour() < 12 else "ب.ظ"

    # Map format codes to values
    values = {
        '%Y': lambda: str(date.year()).zfill(4),
        '%y': lambda: str(date.year() % 100).zfill(2),
        '%m': lambda: f"{date.month():02d}",
        '%-m': lambda: str(date.month()),
        '%d': lambda: f"{date.day():02d}",
        '%-d': lambda: str(date.day()),
        '%H': lambda: f"{date.hour():02d}",
        '%-H': lambda: str(date.hour()),
        '%I': lambda: f"{hour_12:02d}",
        '%-I': lambda: str(hour_12),
        '%M': lambda: f"{date.minute():02d}",
        '%-M': lambda: str(date.minute()),
        '%S': lambda: f"{date.second():02d}",
        '%-S': lambda: str(date.second()),
        '%f': lambda: f"{date.microsecond():06d}",
        '%p': lambda: am_pm,
        '%B': lambda: get_month_name(date.month(), locale, "jalali", short=False),
        '%b': lambda: get_month_name(date.month(), locale, "jalali", short=True),
        '%A': lambda: get_weekday_name(date.weekday(), locale, "jalali", short=False),
        '%a': lambda: get_weekday_name(date.weekday(), locale, "jalali", short=True),
        '%w': lambda: str(date.weekday()),
        '%j': lambda: f"{date.day_of_year():03d}",
        '%U': lambda: f"{((date.day_of_year() - 1) // 7):02d}",
        '%%': lambda: '%',
    }

    # Replace format codes (process longer codes first: %-m before %m)
    result = pattern
    for code in sorted(values.keys(), key=len, reverse=True):
        if code in result:
            value = values[code]()
            # Convert to Persian digits if needed
            if locale == "fa" and code not in ('%B', '%b', '%A', '%a', '%%', '%p'):
                value = to_persian_digits(value)
            result = result.replace(code, value)

    return result


def format_gregorian_date(
    date: Any,
    pattern: str,
    locale: Literal["fa", "en"] = "en"
) -> str:
    """
    Format GregorianDate using strftime-style format codes.

    Same format codes as format_jalali_date.
    """

    # Helper for 12-hour format
    hour_12 = date.hour() % 12
    if hour_12 == 0:
        hour_12 = 12
    am_pm = "AM" if date.hour() < 12 else "PM"
    if locale == "fa":
        am_pm = "ق.ظ" if date.hour() < 12 else "ب.ظ"

    values = {
        '%Y': lambda: str(date.year()).zfill(4),
        '%y': lambda: str(date.year() % 100).zfill(2),
        '%m': lambda: f"{date.month():02d}",
        '%-m': lambda: str(date.month()),
        '%d': lambda: f"{date.day():02d}",
        '%-d': lambda: str(date.day()),
        '%H': lambda: f"{date.hour():02d}",
        '%-H': lambda: str(date.hour()),
        '%I': lambda: f"{hour_12:02d}",
        '%-I': lambda: str(hour_12),
        '%M': lambda: f"{date.minute():02d}",
        '%-M': lambda: str(date.minute()),
        '%S': lambda: f"{date.second():02d}",
        '%-S': lambda: str(date.second()),
        '%f': lambda: f"{date.microsecond():06d}",
        '%p': lambda: am_pm,
        '%B': lambda: get_month_name(date.month(), locale, "gregorian", short=False),
        '%b': lambda: get_month_name(date.month(), locale, "gregorian", short=True),
        '%A': lambda: get_weekday_name(date.weekday(), locale, "gregorian", short=False),
        '%a': lambda: get_weekday_name(date.weekday(), locale, "gregorian", short=True),
        '%w': lambda: str(date.weekday()),
        '%j': lambda: f"{date.day_of_year():03d}",
        '%U': lambda: f"{((date.day_of_year() - 1) // 7):02d}",
        '%%': lambda: '%',
    }

    result = pattern
    for code in sorted(values.keys(), key=len, reverse=True):
        if code in result:
            value = values[code]()
            if locale == "fa" and code not in ('%B', '%b', '%A', '%a', '%%', '%p'):
                value = to_persian_digits(value)
            result = result.replace(code, value)

    return result


# Backward compatibility - keep old format codes if needed
def format_date_custom(date: Any, pattern: str, locale: str = "fa") -> str:
    """
    Custom format function (alias for format_jalali_date or format_gregorian_date).

    Deprecated: Use strftime method on date objects instead.
    """
    from parsidate.core.jalali import JalaliDate
    if isinstance(date, JalaliDate):
        return format_jalali_date(date, pattern, locale)
    else:
        return format_gregorian_date(date, pattern, locale)
