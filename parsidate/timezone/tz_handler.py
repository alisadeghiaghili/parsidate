"""
Timezone helper functions for ParsiDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

import pytz
from datetime import timezone as dt_timezone, timedelta
from typing import Union

def get_timezone(name: str):
    """
    Get pytz timezone object from name (e.g. 'Asia/Tehran', 'UTC').
    """
    try:
        return pytz.timezone(name)
    except Exception as e:
        raise ValueError(f"Invalid timezone: {name}") from e

def localize_datetime(dt, tz_name: str):
    """
    Attach timezone info to naive datetime object (pytz style).

    Args:
        dt: datetime object (naive).
        tz_name: Timezone string.

    Returns:
        Aware datetime object.
    """
    tz = get_timezone(tz_name)
    return tz.localize(dt)

def convert_timezone(dt, to_tz: str):
    """
    Convert a datetime object with tzinfo to another timezone.

    Args:
        dt: datetime object (must have tzinfo).
        to_tz: Target timezone string.

    Returns:
        datetime in new timezone.
    """
    if dt.tzinfo is None:
        raise ValueError("Input datetime must have tzinfo.")
    tz = get_timezone(to_tz)
    return dt.astimezone(tz)

def remove_timezone(dt):
    """
    Return datetime object without timezone info (naive).
    """
    return dt.replace(tzinfo=None)

def utc_offset_minutes(tz_name: str) -> int:
    """Get UTC offset in minutes for a timezone (relative to now).

    Args:
        tz_name: Timezone string.

    Returns:
        UTC offset in minutes (int).
    """
    import datetime as _dt
    tz = get_timezone(tz_name)
    naive_now = _dt.datetime.now()
    offset = tz.utcoffset(naive_now)
    return int(offset.total_seconds() // 60)

def is_dst(dt, tz_name: str) -> bool:
    """Return whether a datetime falls in daylight saving time.

    Args:
        dt: Naive or aware ``datetime``.
        tz_name: IANA timezone name such as ``\"Asia/Tehran\"``.

    Returns:
        ``True`` if the datetime is in DST for that zone.

    Example:
        >>> from datetime import datetime
        >>> is_dst(datetime(2024, 7, 1, 12, 0), "UTC")
        False
    """
    tz = get_timezone(tz_name)
    if dt.tzinfo is None:
        dt = tz.localize(dt)
    return bool(dt.dst())

def list_timezones():
    """
    List all timezone names available in pytz.
    """
    return pytz.all_timezones

def with_tz(date, tz: str):
    """
    Convert a date to a different timezone (changes the time).

    This converts the date/time to a different timezone, adjusting the
    hour/minute/second values to match the new timezone.

    Args:
        date: JalaliDate or GregorianDate with tzinfo
        tz: Target timezone name (e.g., 'UTC', 'Asia/Tehran')

    Returns:
        New date object in the target timezone

    Example:
        date_tehran = jmd_hms("1403/08/18 14:30:00", tz="Asia/Tehran")
        date_utc = with_tz(date_tehran, "UTC")  # Converts to UTC time
    """
    from datetime import datetime

    # Create datetime from date object
    dt = datetime(
        date.year() if hasattr(date, 'year') else date.year,
        date.month() if hasattr(date, 'month') else date.month,
        date.day() if hasattr(date, 'day') else date.day,
        date.hour() if hasattr(date, 'hour') else 0,
        date.minute() if hasattr(date, 'minute') else 0,
        date.second() if hasattr(date, 'second') else 0,
        date.microsecond() if hasattr(date, 'microsecond') else 0,
        tzinfo=date.tzinfo() if hasattr(date, 'tzinfo') else None
    )

    # Convert timezone
    new_dt = convert_timezone(dt, tz)

    # Create new date object with same type
    new_date = date.copy()
    return new_date.replace(
        hour=new_dt.hour,
        minute=new_dt.minute,
        second=new_dt.second,
        microsecond=new_dt.microsecond,
        tzinfo=new_dt.tzinfo
    )


def force_tz(date, tz: str):
    """
    Force a timezone onto a date without converting the time.

    This sets the timezone but keeps the hour/minute/second values the same.
    Useful when you have a naive date and want to assign it a timezone.

    Args:
        date: JalaliDate or GregorianDate (can be naive or aware)
        tz: Timezone name to assign (e.g., 'UTC', 'Asia/Tehran')

    Returns:
        New date object with the specified timezone

    Example:
        date = jmd_hms("1403/08/18 14:30:00")  # Naive
        date_tehran = force_tz(date, "Asia/Tehran")  # Same time, but with TZ
    """
    tz_obj = get_timezone(tz)
    return date.replace(tzinfo=tz_obj)

