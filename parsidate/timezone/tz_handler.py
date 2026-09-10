"""Timezone helpers for ParsiDate using the standard library ``zoneinfo``.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from datetime import datetime, timezone as dt_timezone
from typing import Any, List
from zoneinfo import ZoneInfo


def get_timezone(name: str) -> ZoneInfo:
    """Return a ``ZoneInfo`` timezone by IANA name.

    Args:
        name: IANA zone name, e.g. ``\"Asia/Tehran\"`` or ``\"UTC\"``.

    Returns:
        ``zoneinfo.ZoneInfo`` instance.

    Raises:
        ValueError: If the zone name is unknown.

    Example:
        >>> get_timezone(\"UTC\").key
        'UTC'
    """
    try:
        return ZoneInfo(name)
    except Exception as exc:
        raise ValueError(f"Invalid timezone: {name}") from exc


def localize_datetime(dt: datetime, tz_name: str) -> datetime:
    """Attach a timezone to a naive datetime.

    Args:
        dt: Naive ``datetime``.
        tz_name: IANA zone name.

    Returns:
        Aware datetime in ``tz_name``.

    Raises:
        ValueError: If ``dt`` already has tzinfo.

    Example:
        >>> localize_datetime(datetime(2024, 1, 1, 12, 0), \"UTC\").tzinfo.key
        'UTC'
    """
    if dt.tzinfo is not None:
        raise ValueError("datetime is already timezone-aware")
    return dt.replace(tzinfo=get_timezone(tz_name))


def convert_timezone(dt: datetime, to_tz: str) -> datetime:
    """Convert an aware datetime into another timezone.

    Args:
        dt: Aware ``datetime``.
        to_tz: Target IANA zone name.

    Returns:
        Datetime expressed in ``to_tz``.

    Raises:
        ValueError: If ``dt`` is naive.

    Example:
        >>> aware = datetime(2024, 1, 1, 12, 0, tzinfo=dt_timezone.utc)
        >>> convert_timezone(aware, \"UTC\").hour
        12
    """
    if dt.tzinfo is None:
        raise ValueError("Input datetime must have tzinfo.")
    return dt.astimezone(get_timezone(to_tz))


def remove_timezone(dt: datetime) -> datetime:
    """Return a naive datetime with the same wall-clock fields.

    Args:
        dt: Any ``datetime``.

    Returns:
        Naive datetime (tzinfo stripped, clock fields unchanged).

    Example:
        >>> remove_timezone(datetime(2024, 1, 1, tzinfo=dt_timezone.utc)).tzinfo is None
        True
    """
    return dt.replace(tzinfo=None)


def utc_offset_minutes(tz_name: str) -> int:
    """Return the UTC offset in minutes for a zone at the current instant.

    Args:
        tz_name: IANA zone name.

    Returns:
        Offset east of UTC in minutes (negative west).

    Example:
        >>> isinstance(utc_offset_minutes(\"UTC\"), int)
        True
    """
    tz = get_timezone(tz_name)
    now = datetime.now(tz)
    offset = now.utcoffset()
    if offset is None:
        return 0
    return int(offset.total_seconds() // 60)


def is_dst(dt: datetime, tz_name: str) -> bool:
    """Return whether a datetime falls in daylight saving time.

    Args:
        dt: Naive or aware ``datetime``.
        tz_name: IANA zone name.

    Returns:
        ``True`` if the datetime observes DST in that zone.

    Example:
        >>> is_dst(datetime(2024, 7, 1, 12, 0), \"UTC\")
        False
    """
    tz = get_timezone(tz_name)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    else:
        dt = dt.astimezone(tz)
    return bool(dt.dst())


def list_timezones() -> List[str]:
    """List available IANA timezone names from ``zoneinfo``.

    Returns:
        Sorted list of zone keys available on this system.

    Example:
        >>> \"UTC\" in list_timezones()
        True
    """
    try:
        from zoneinfo import available_timezones

        return sorted(available_timezones())
    except Exception:  # pragma: no cover - fallback
        return ["UTC"]


def _date_parts(date: Any):
    """Extract Y/M/D/h/m/s/us/tz from a date-like object."""
    year = date.year() if hasattr(date, "year") else date.year
    month = date.month() if hasattr(date, "month") else date.month
    day = date.day() if hasattr(date, "day") else date.day
    hour = date.hour() if hasattr(date, "hour") else 0
    minute = date.minute() if hasattr(date, "minute") else 0
    second = date.second() if hasattr(date, "second") else 0
    microsecond = date.microsecond() if hasattr(date, "microsecond") else 0
    tz = date.tzinfo() if hasattr(date, "tzinfo") else getattr(date, "tzinfo", None)
    return year, month, day, hour, minute, second, microsecond, tz


def with_tz(date: Any, tz: str) -> Any:
    """Convert a date object into another timezone (clock fields change).

    Args:
        date: ``JalaliDate`` or ``GregorianDate`` with optional tzinfo.
        tz: Target IANA zone name.

    Returns:
        New date object of the same type in the target zone.

    Example:
        >>> from parsidate.parsers import jmd_hms
        >>> d = jmd_hms(\"1403/08/18 14:30:00\", tz=\"Asia/Tehran\")
        >>> with_tz(d, \"UTC\").tzinfo() is not None
        True
    """
    y, mo, d, h, mi, s, us, current_tz = _date_parts(date)
    if current_tz is None:
        raise ValueError("Input date must have tzinfo to convert zones.")
    # Jalali wall-clock cannot be shifted via Gregorian fields alone;
    # convert via Gregorian datetime for GregorianDate, and via
    # to_gregorian for JalaliDate.
    from parsidate.core.jalali import JalaliDate

    if isinstance(date, JalaliDate):
        gy, gm, gd = date.to_gregorian()
        src = datetime(gy, gm, gd, h, mi, s, us, tzinfo=current_tz)
        shifted = convert_timezone(src, tz)
        from parsidate.core.converters import gregorian_to_jalali

        jy, jm, jd = gregorian_to_jalali(shifted.year, shifted.month, shifted.day)
        return JalaliDate(
            jy,
            jm,
            jd,
            shifted.hour,
            shifted.minute,
            shifted.second,
            shifted.microsecond,
            shifted.tzinfo,
        )

    src = datetime(y, mo, d, h, mi, s, us, tzinfo=current_tz)
    shifted = convert_timezone(src, tz)
    return date.replace(
        year=shifted.year,
        month=shifted.month,
        day=shifted.day,
        hour=shifted.hour,
        minute=shifted.minute,
        second=shifted.second,
        microsecond=shifted.microsecond,
        tzinfo=shifted.tzinfo,
    )


def force_tz(date: Any, tz: str) -> Any:
    """Attach a timezone without changing clock fields.

    Args:
        date: ``JalaliDate`` or ``GregorianDate``.
        tz: IANA zone name to assign.

    Returns:
        New date object with ``tz`` attached.

    Example:
        >>> from parsidate.parsers import jmd
        >>> force_tz(jmd(\"1403/08/18\"), \"Asia/Tehran\").tzinfo() is not None
        True
    """
    return date.replace(tzinfo=get_timezone(tz))
