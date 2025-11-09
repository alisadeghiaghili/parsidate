"""
Date formatting functions for Jalali (Persian) and Gregorian dates.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from typing import Any, Literal
from parsidate.utils.helpers import (
    month_name,
    weekday_name,
    to_persian_digits,
    to_english_digits,
)

def format_jalali_date(
    date: Any,
    pattern: str,
    locale: Literal["fa", "en"] = "fa"
) -> str:
    """
    Flexible formatter for JalaliDate objects.
    Pattern codes:
        Y - 4-digit year (1399)
        y - 2-digit year (99)
        m - month with leading zero (01-12)
        n - month no leading zero (1-12)
        d - day with leading zero (01-31)
        j - day no leading zero (1-31)
        H - hour with leading zero (00-23)
        i - minute with leading zero (00-59)
        s - second with leading zero (00-59)
        E - full month name
        M - short month name (3 letters, e.g., Far/Mar)
        l - full weekday name
        w - weekday number (0=Saturday)
        q - quarter (1-4)
        L - is leap year (1/0)
    """
    values = {
        "Y": str(date.year()).zfill(4),
        "y": str(date.year() % 100).zfill(2),
        "m": f"{date.month():02d}",
        "n": str(date.month()),
        "d": f"{date.day():02d}",
        "j": str(date.day()),
        "H": f"{date.hour():02d}",
        "i": f"{date.minute():02d}",
        "s": f"{date.second():02d}",
        "E": month_name(date.month(), locale, "jalali"),
        "M": month_name(date.month(), locale, "jalali")[:3],
        "l": weekday_name(date.weekday(), locale, "jalali"),
        "w": str(date.weekday()),
        "q": str(date.quarter()),
        "L": "1" if date.is_leap_year() else "0",
    }
    result = ""
    esc = False
    for c in pattern:
        if esc:
            result += c
            esc = False
            continue
        if c == "\\":
            esc = True
            continue
        if c in values:
            val = values[c]
            if locale == "fa" and c in ("Y", "y", "m", "n", "d", "j", "H", "i", "s", "w", "q", "L"):
                val = to_persian_digits(val)
            result += val
        else:
            result += c
    return result

def format_gregorian_date(
    date: Any,
    pattern: str,
    locale: Literal["fa", "en"] = "en"
) -> str:
    """
    Flexible formatter for GregorianDate objects.
    Pattern codes same as for JalaliDate.
    """
    values = {
        "Y": str(date.year()).zfill(4),
        "y": str(date.year() % 100).zfill(2),
        "m": f"{date.month():02d}",
        "n": str(date.month()),
        "d": f"{date.day():02d}",
        "j": str(date.day()),
        "H": f"{date.hour():02d}",
        "i": f"{date.minute():02d}",
        "s": f"{date.second():02d}",
        "E": month_name(date.month(), locale, "gregorian"),
        "M": month_name(date.month(), locale, "gregorian")[:3],
        "l": weekday_name(date.weekday(), locale, "gregorian"),
        "w": str(date.weekday()),
        "q": str(date.quarter()),
        "L": "1" if date.is_leap_year() else "0",
    }
    result = ""
    esc = False
    for c in pattern:
        if esc:
            result += c
            esc = False
            continue
        if c == "\\":
            esc = True
            continue
        if c in values:
            val = values[c]
            if locale == "fa" and c in ("Y", "y", "m", "n", "d", "j", "H", "i", "s", "w", "q", "L"):
                val = to_persian_digits(val)
            result += val
        else:
            result += c
    return result
