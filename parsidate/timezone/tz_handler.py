"""
Timezone helper functions for ParsiDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

import pytz
from datetime import timezone as dt_timezone, timedelta

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
    """
    Get UTC offset in minutes for a timezone (relative to now).

    Args:
        tz_name: Timezone string.

    Returns:
        UTC offset in minutes (int).
    """
    tz = get_timezone(tz_name)
    offset = tz.utcoffset(None)
    if offset is None:
        # Use current time
        import datetime as _dt
        offset = tz.utcoffset(_dt.datetime.now(tz))
    return int(offset.total_seconds() // 60)

def is_dst(dt, tz_name: str) -> bool:
    """
    Returns True if given datetime is in daylight saving for that timezone.
    """
    tz = get_timezone(tz_name)
    return bool(tz.dst(dt))

def list_timezones():
    """
    List all timezone names available in pytz.
    """
    return pytz.all_timezones
