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
    return n.replace(hour=0, minute=0, second=0, microsecond=0)

def today_gregorian(tz: Optional[str] = None) -> GregorianDate:
    """Get today Gregorian date with zeroed time and optional timezone."""
    n = now_gregorian(tz)
    return n.replace(hour=0, minute=0, second=0, microsecond=0)

# === Standard strptime-style parsers ===

_STRPTIME_FIELD_PATTERN = {
    "%Y": r"(?P<year>\d{4})",
    "%y": r"(?P<year2>\d{2})",
    "%m": r"(?P<month>\d{1,2})",
    "%d": r"(?P<day>\d{1,2})",
    "%H": r"(?P<hour>\d{1,2})",
    "%M": r"(?P<minute>\d{1,2})",
    "%S": r"(?P<second>\d{1,2})",
}


def _compile_strptime_regex(fmt: str) -> re.Pattern:
    """Compile a strptime-style format into a named-group regex.

    Only the numeric directives used by ParsiDate are supported:
    ``%Y %y %m %d %H %M %S``. Literal characters are escaped.

    Args:
        fmt: Format string such as ``\"%Y/%m/%d\"``.

    Returns:
        Compiled regular expression with named groups.

    Example:
        >>> _compile_strptime_regex(\"%Y/%m/%d\").pattern
        '(?P<year>\\\\d{4})/(?P<month>\\\\d{1,2})/(?P<day>\\\\d{1,2})'
    """
    parts = []
    i = 0
    while i < len(fmt):
        if fmt[i] == "%" and i + 1 < len(fmt):
            token = fmt[i : i + 2]
            if token in _STRPTIME_FIELD_PATTERN:
                parts.append(_STRPTIME_FIELD_PATTERN[token])
                i += 2
                continue
            raise ValueError(f"Unsupported strptime directive: {token}")
        parts.append(re.escape(fmt[i]))
        i += 1
    return re.compile("".join(parts))


def strptime_jalali(
    date_str: str,
    fmt: str = "%Y/%m/%d",
    tz: Optional[str] = None,
) -> JalaliDate:
    """Parse a Jalali date using standard ``strptime`` format codes.

    Args:
        date_str: Input string (Persian or English digits).
        fmt: ``strptime`` format. Supported codes: ``%Y %y %m %d %H %M %S``.
        tz: Optional IANA timezone name.

    Returns:
        Parsed :class:`~parsidate.core.jalali.JalaliDate`.

    Raises:
        ValueError: If the string does not match ``fmt``.

    Example:
        >>> strptime_jalali(\"1403/08/18\", \"%Y/%m/%d\").day()
        18
        >>> strptime_jalali(\"18-08-1403\", \"%d-%m-%Y\").year()
        1403
    """
    s = to_english_digits(date_str).strip()
    match = _compile_strptime_regex(fmt).fullmatch(s)
    if not match:
        raise ValueError(f"Date string {date_str!r} does not match format {fmt!r}")
    fields = match.groupdict()
    year = int(fields["year"]) if fields.get("year") else 2000 + int(fields["year2"])
    month = int(fields.get("month") or 1)
    day = int(fields.get("day") or 1)
    hour = int(fields.get("hour") or 0)
    minute = int(fields.get("minute") or 0)
    second = int(fields.get("second") or 0)
    tzinfo = pytz.timezone(tz) if tz else None
    return JalaliDate(year, month, day, hour, minute, second, 0, tzinfo)


def strptime_gregorian(
    date_str: str,
    fmt: str = "%Y-%m-%d",
    tz: Optional[str] = None,
) -> GregorianDate:
    """Parse a Gregorian date using standard ``strptime`` format codes.

    Args:
        date_str: Input string (Persian or English digits).
        fmt: ``strptime`` format. Supported codes: ``%Y %y %m %d %H %M %S``.
        tz: Optional IANA timezone name.

    Returns:
        Parsed :class:`~parsidate.core.gregorian.GregorianDate`.

    Raises:
        ValueError: If the string does not match ``fmt``.

    Example:
        >>> strptime_gregorian(\"2024-11-08\", \"%Y-%m-%d\").month()
        11
    """
    s = to_english_digits(date_str).strip()
    match = _compile_strptime_regex(fmt).fullmatch(s)
    if not match:
        raise ValueError(f"Date string {date_str!r} does not match format {fmt!r}")
    fields = match.groupdict()
    year = int(fields["year"]) if fields.get("year") else 2000 + int(fields["year2"])
    month = int(fields.get("month") or 1)
    day = int(fields.get("day") or 1)
    hour = int(fields.get("hour") or 0)
    minute = int(fields.get("minute") or 0)
    second = int(fields.get("second") or 0)
    tzinfo = pytz.timezone(tz) if tz else None
    return GregorianDate(year, month, day, hour, minute, second, 0, tzinfo)


def parse_jalali(date_str: str, tz: Optional[str] = None) -> JalaliDate:
    """
    Smart parser for Jalali dates with flexible format support.

    Automatically detects format and parses:
    - Date only: "1403/08/18" or "1403-08-18"
    - Date with time: "1403/08/18 14:30:25"
    - Different separators: /, -, .

    Args:
        date_str: Date string to parse
        tz: Optional timezone name

    Returns:
        JalaliDate object

    Example:
        parse_jalali("1403/08/18 14:30:25")
        parse_jalali("1403-08-18")
    """
    s = to_english_digits(normalize_date_separator(date_str)).strip()

    # Check if has time component
    if ' ' in s:
        parts = s.split()
        date_part = parts[0]
        time_part = parts[1] if len(parts) > 1 else "00:00:00"

        # Parse date
        y, m, d = map(int, date_part.split("/"))

        # Parse time
        time_components = time_part.split(":")
        h = int(time_components[0]) if len(time_components) > 0 else 0
        mi = int(time_components[1]) if len(time_components) > 1 else 0
        se = int(time_components[2]) if len(time_components) > 2 else 0
    else:
        # Date only
        y, m, d = map(int, s.split("/"))
        h, mi, se = 0, 0, 0

    tzinfo = pytz.timezone(tz) if tz else None
    return JalaliDate(y, m, d, h, mi, se, 0, tzinfo)


def parse_gregorian(date_str: str, tz: Optional[str] = None) -> GregorianDate:
    """
    Smart parser for Gregorian dates with flexible format support.

    Automatically detects format and parses:
    - Date only: "2024-11-08" or "2024/11/08"
    - Date with time: "2024-11-08 14:30:25"
    - Different separators: /, -, .

    Args:
        date_str: Date string to parse
        tz: Optional timezone name

    Returns:
        GregorianDate object

    Example:
        parse_gregorian("2024-11-08 14:30:25")
        parse_gregorian("2024/11/08")
    """
    s = to_english_digits(normalize_date_separator(date_str)).strip()

    # Check if has time component
    if ' ' in s:
        parts = s.split()
        date_part = parts[0]
        time_part = parts[1] if len(parts) > 1 else "00:00:00"

        # Parse date
        y, m, d = map(int, date_part.split("/"))

        # Parse time
        time_components = time_part.split(":")
        h = int(time_components[0]) if len(time_components) > 0 else 0
        mi = int(time_components[1]) if len(time_components) > 1 else 0
        se = int(time_components[2]) if len(time_components) > 2 else 0
    else:
        # Date only
        y, m, d = map(int, s.split("/"))
        h, mi, se = 0, 0, 0

    tzinfo = pytz.timezone(tz) if tz else None
    return GregorianDate(y, m, d, h, mi, se, 0, tzinfo)
