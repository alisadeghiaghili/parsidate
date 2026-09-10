"""Optional bridges to third-party Jalali types.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from parsidate.core.gregorian import GregorianDate
from parsidate.core.jalali import JalaliDate

__all__ = [
    "from_jdatetime",
    "to_jdatetime",
    "from_datetime",
    "to_datetime_naive",
]


def from_datetime(dt: datetime) -> JalaliDate:
    """Convert a Gregorian ``datetime`` to JalaliDate.

    Args:
        dt: Gregorian datetime (naive or aware).

    Returns:
        Equivalent JalaliDate (tzinfo preserved when present).

    Example:
        >>> from datetime import datetime
        >>> from parsidate.interop import from_datetime
        >>> from_datetime(datetime(2024, 3, 20)).year()
        1403
    """
    from parsidate.core.converters import gregorian_to_jalali

    jy, jm, jd = gregorian_to_jalali(dt.year, dt.month, dt.day)
    return JalaliDate(
        jy,
        jm,
        jd,
        dt.hour,
        dt.minute,
        dt.second,
        dt.microsecond,
        dt.tzinfo,
    )


def to_datetime_naive(date: JalaliDate) -> datetime:
    """Convert JalaliDate to a naive Gregorian ``datetime``.

    Args:
        date: Jalali date (tzinfo ignored).

    Returns:
        Naive Gregorian datetime with the same wall clock.

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> from parsidate.interop import to_datetime_naive
        >>> to_datetime_naive(JalaliDate(1403, 1, 1)).year
        2024
    """
    gy, gm, gd = date.to_gregorian()
    return datetime(gy, gm, gd, date.hour(), date.minute(), date.second(), date.microsecond())


def to_jdatetime(date: JalaliDate) -> Any:
    """Convert JalaliDate to ``jdatetime.datetime`` / ``jdatetime.date``.

    Args:
        date: JalaliDate with optional time.

    Returns:
        ``jdatetime.datetime`` when time is non-zero, else ``jdatetime.date``.

    Raises:
        ImportError: If ``jdatetime`` is not installed.

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> from parsidate.interop import to_jdatetime
        >>> to_jdatetime(JalaliDate(1403, 8, 18)).day
        18
    """
    try:
        import jdatetime
    except ImportError as exc:  # pragma: no cover
        raise ImportError("jdatetime is required for this bridge: pip install jdatetime") from exc

    if date.hour() or date.minute() or date.second() or date.microsecond():
        return jdatetime.datetime(
            date.year(),
            date.month(),
            date.day(),
            date.hour(),
            date.minute(),
            date.second(),
            date.microsecond(),
            tzinfo=date.tzinfo(),
        )
    return jdatetime.date(date.year(), date.month(), date.day())


def from_jdatetime(obj: Any) -> JalaliDate:
    """Convert ``jdatetime.date`` / ``jdatetime.datetime`` to JalaliDate.

    Args:
        obj: jdatetime instance.

    Returns:
        Equivalent JalaliDate.

    Example:
        >>> import jdatetime
        >>> from parsidate.interop import from_jdatetime
        >>> from_jdatetime(jdatetime.date(1403, 8, 18)).day()
        18
    """
    hour = getattr(obj, "hour", 0) or 0
    minute = getattr(obj, "minute", 0) or 0
    second = getattr(obj, "second", 0) or 0
    micro = getattr(obj, "microsecond", 0) or 0
    tz = getattr(obj, "tzinfo", None)
    return JalaliDate(obj.year, obj.month, obj.day, hour, minute, second, micro, tz)
