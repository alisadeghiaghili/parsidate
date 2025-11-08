"""
Date parsing functions and shortcuts for Jalali (Persian) and Gregorian calendars.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

import pytz
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.utils.helpers import normalize_date_separator, to_english_digits
from typing import Optional, Union
from datetime import datetime
import re

# === Jalali Parsers ===

def jmd(date_str: str, tz: Optional[str] = None) -> JalaliDate:
    """Parse a Persian date string in Year/Month/Day format: '1403/08/18'."""
    s = to_english_digits(normalize_date_separator(date_str)).strip()
    y, m, d = map(int, s.split("/"))
    tzinfo = pytz.timezone(tz) if tz else None
    return JalaliDate(y, m, d, tzinfo=tzinfo)

def jdm(date_str: str, tz: Optional[str] = None) -> JalaliDate:
    """Parse Day/Month/Year: '18/08/1403'."""
    s = to_english_digits(normalize_date_separator(date_str)).strip()
    d, m, y = map(int, s.split("/"))
    tzinfo = pytz.timezone(tz) if tz else None
    return JalaliDate(y, m, d, tzinfo=tzinfo)

def jmdy(date_str: str, tz: Optional[str] = None) -> JalaliDate:
    """Parse Month/Day/Year: '08/18/1403'."""
    s = to_english_digits(normalize_date_separator(date_str)).strip()
    m, d, y = map(int, s.split("/"))
    tzinfo = pytz.timezone(tz) if tz else None
    return JalaliDate(y, m, d, tzinfo=tzinfo)

def jdmy(date_str: str, tz: Optional[str] = None) -> JalaliDate:
    """Parse Day/Month/Year: alias for jdm."""
    return jdm(date_str, tz=tz)

def jmd_hms(date_str: str, tz: Optional[str] = None) -> JalaliDate:
    """
    Parse Jalali date and time string: '1403/08/18 14:30:25'
    Args:
        date_str: Date with time.
        tz: Timezone name (e.g. 'Asia/Tehran'); optional.
    Returns:
        JalaliDate with correct tzinfo.
    """
    s = to_english_digits(normalize_date_separator(date_str)).strip()
    parts = s.split()
    y, m, d = map(int, parts[0].split("/"))
    if len(parts) > 1:
        h, mi, se = map(int, parts[1].split(":"))
    else:
        h, mi, se = 0, 0, 0
    tzinfo = pytz.timezone(tz) if tz else None
    return JalaliDate(y, m, d, h, mi, se, 0, tzinfo)

# === Gregorian Parsers ===

def ymd(date_str: str, tz: Optional[str] = None) -> GregorianDate:
    """Parse Year-Month-Day: '2024-11-08' or '2024/11/08'."""
    s = to_english_digits(normalize_date_separator(date_str)).strip()
    y, m, d = map(int, s.split("/"))
    tzinfo = pytz.timezone(tz) if tz else None
    return GregorianDate(y, m, d, tzinfo=tzinfo)

def dmy(date_str: str, tz: Optional[str] = None) -> GregorianDate:
    """Parse Day-Month-Year: '08-11-2024'."""
    s = to_english_digits(normalize_date_separator(date_str)).strip()
    d, m, y = map(int, s.split("/"))
    tzinfo = pytz.timezone(tz) if tz else None
    return GregorianDate(y, m, d, tzinfo=tzinfo)

def mdy(date_str: str, tz: Optional[str] = None) -> GregorianDate:
    """Parse Month-Day-Year: '11-08-2024'."""
    s = to_english_digits(normalize_date_separator(date_str)).strip()
    m, d, y = map(int, s.split("/"))
    tzinfo = pytz.timezone(tz) if tz else None
    return GregorianDate(y, m, d, tzinfo=tzinfo)

def ydm(date_str: str, tz: Optional[str] = None) -> GregorianDate:
    """Parse Year-Day-Month: '2024-08-11'."""
    s = to_english_digits(normalize_date_separator(date_str)).strip()
    y, d, m = map(int, s.split("/"))
    tzinfo = pytz.timezone(tz) if tz else None
    return GregorianDate(y, m, d, tzinfo=tzinfo)

def ymd_hms(date_str: str, tz: Optional[str] = None) -> GregorianDate:
    """
    Parse Gregorian date and time: '2024-11-08 14:30:25'
    Args:
        date_str: Date/time string.
        tz: Optional timezone.
    Returns:
        GregorianDate with tzinfo.
    """
    s = to_english_digits(normalize_date_separator(date_str)).strip()
    parts = s.split()
    y, m, d = map(int, parts[0].split("/"))
    if len(parts) > 1:
        h, mi, se = map(int, parts[1].split(":"))
    else:
        h, mi, se = 0, 0, 0
    tzinfo = pytz.timezone(tz) if tz else None
    return GregorianDate(y, m, d, h, mi, se, 0, tzinfo)


# === Smart Parser ===

def parse_date(date_str: str, calendar: Optional[str] = None, tz: Optional[str] = None) -> Union[JalaliDate, GregorianDate]:
    """
    Attempt to parse a date string and guess calendar and format.
    Args:
        date_str: Input date string.
        calendar: 'jalali', 'gregorian', or None for auto-detect.
        tz: Optional timezone.
    Returns:
        JalaliDate or GregorianDate.
    """
    try:
        if calendar == "jalali" or (calendar is None and re.match(r"1[34]\d\d/", date_str)):
            return jmd(date_str, tz=tz)
    except Exception:
        pass
    try:
        return ymd(date_str, tz=tz)
    except Exception:
        pass
    raise ValueError(f"Cannot parse date string: {date_str}")

# === Now/Today Functions ===

def now_jalali(tz: Optional[str] = None) -> JalaliDate:
    """Get current Jalali date/time with optional timezone."""
    dt = datetime.now(pytz.timezone(tz)) if tz else datetime.now()
    from parsidate.core.converters import gregorian_to_jalali
    jy, jm, jd = gregorian_to_jalali(dt.year, dt.month, dt.day)
    return JalaliDate(jy, jm, jd, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)

def now_gregorian(tz: Optional[str] = None) -> GregorianDate:
    """Get current Gregorian date/time with optional timezone."""
    dt = datetime.now(pytz.timezone(tz)) if tz else datetime.now()
    return GregorianDate(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)

def today_jalali(tz: Optional[str] = None) -> JalaliDate:
    """Get today Jalali date with zeroed time and optional timezone."""
    n = now_jalali(tz)
    return n.copy().hour(0).minute(0).second(0).microsecond(0)

def today_gregorian(tz: Optional[str] = None) -> GregorianDate:
    """Get today Gregorian date with zeroed time and optional timezone."""
    n = now_gregorian(tz)
    return n.copy().hour(0).minute(0).second(0).microsecond(0)
