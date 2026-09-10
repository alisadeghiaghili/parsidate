"""
Rounding and truncation operations for JalaliDate and GregorianDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from typing import Literal


def _zero_time(date) -> object:
    """Create a copy of date with time zeroed."""
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def _set_day(date, day: int) -> object:
    """Create a copy of date with specific day."""
    return date.replace(day=day)


def _set_month(date, month: int) -> object:
    """Create a copy of date with specific month."""
    return date.replace(month=month)


def floor_to_day(date) -> object:
    """Return a copy of date with time zeroed (00:00:00.000000)."""
    return _zero_time(date)


def ceil_to_day(date) -> object:
    """Return a copy of date rounded up to start of next day (if time not zero)."""
    if date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0:
        return date.copy()
    return _zero_time(date.add(days=1))


def floor_to_week(date, week_start: int = 0) -> object:
    """Round date down to start of week.

    Args:
        date: Date object.
        week_start: 0 for Saturday, 1 for Sunday, etc.

    Returns:
        Date object.
    """
    delta = (date.weekday() - week_start) % 7
    return _zero_time(date.add(days=-delta))


def ceil_to_week(date, week_start: int = 0) -> object:
    """Round date up to start of next week (if not start of week).

    Args:
        date: Date object.
        week_start: 0 for Saturday, 1 for Sunday, etc.

    Returns:
        Date object.
    """
    if date.weekday() == week_start and date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0:
        return date.copy()
    return _zero_time(date.add(days=(7 - (date.weekday() - week_start) % 7)))


def floor_to_month(date) -> object:
    """Round date down to start of its month."""
    return _zero_time(_set_day(date, 1))


def ceil_to_month(date) -> object:
    """Round date up to start of next month (if not first of month at 00:00)."""
    if date.day() == 1 and date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0:
        return date.copy()
    return _zero_time(_set_day(date.add(months=1), 1))


def floor_to_quarter(date) -> object:
    """Round date down to start of its quarter."""
    q_start_month = 3 * ((date.month() - 1) // 3) + 1
    return _zero_time(_set_day(_set_month(date, q_start_month), 1))


def ceil_to_quarter(date) -> object:
    """Round date up to start of next quarter (if not at start already)."""
    q_start_month = 3 * ((date.month() - 1) // 3) + 1
    at_start = (date.month() == q_start_month and date.day() == 1 and date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0)
    if at_start:
        return date.copy()
    months_to_add = 3 - ((date.month() - q_start_month) % 3)
    next_month = q_start_month + 3
    if next_month > 12:
        next_month = (q_start_month + 3) % 12
    return _zero_time(_set_day(_set_month(date.add(months=months_to_add), next_month), 1))


def floor_to_year(date) -> object:
    """Round date down to start of year."""
    return _zero_time(_set_day(_set_month(date, 1), 1))


def ceil_to_year(date) -> object:
    """Round date up to start of next year (if not at start already)."""
    at_start = (date.month() == 1 and date.day() == 1 and date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0)
    if at_start:
        return date.copy()
    return _zero_time(_set_day(_set_month(date.add(years=1), 1), 1))


def floor_date(date, unit: Literal["day", "week", "month", "quarter", "year"]) -> object:
    """Round date down to nearest unit.

    Args:
        date: Date object (JalaliDate or GregorianDate)
        unit: Unit to round to ("day", "week", "month", "quarter", "year")

    Returns:
        Rounded date object

    Example:
        floor_date(jmd("1403/08/18"), "month")  # 1403/08/01
    """
    if unit == "day":
        return floor_to_day(date)
    elif unit == "week":
        return floor_to_week(date)
    elif unit == "month":
        return floor_to_month(date)
    elif unit == "quarter":
        return floor_to_quarter(date)
    elif unit == "year":
        return floor_to_year(date)
    else:
        raise ValueError(f"Invalid unit: {unit}. Must be one of: day, week, month, quarter, year")


def ceiling_date(date, unit: Literal["day", "week", "month", "quarter", "year"]) -> object:
    """Round date up to nearest unit.

    Args:
        date: Date object (JalaliDate or GregorianDate)
        unit: Unit to round to ("day", "week", "month", "quarter", "year")

    Returns:
        Rounded date object

    Example:
        ceiling_date(jmd("1403/08/18"), "month")  # 1403/09/01
    """
    if unit == "day":
        return ceil_to_day(date)
    elif unit == "week":
        return ceil_to_week(date)
    elif unit == "month":
        return ceil_to_month(date)
    elif unit == "quarter":
        return ceil_to_quarter(date)
    elif unit == "year":
        return ceil_to_year(date)
    else:
        raise ValueError(f"Invalid unit: {unit}. Must be one of: day, week, month, quarter, year")


def round_date(date, unit: Literal["day", "week", "month", "quarter", "year"]) -> object:
    """Round date to nearest unit (floor if before midpoint, ceiling if after).

    Args:
        date: Date object (JalaliDate or GregorianDate)
        unit: Unit to round to ("day", "week", "month", "quarter", "year")

    Returns:
        Rounded date object

    Example:
        round_date(jmd("1403/08/15"), "month")  # Rounds to nearest month boundary
    """
    floor_result = floor_date(date, unit)
    ceiling_result = ceiling_date(date, unit)

    if floor_result == date:
        return date

    from parsidate.intervals.duration import Duration
    diff_from_floor = date - floor_result
    diff_to_ceiling = ceiling_result - date

    floor_secs = diff_from_floor.total_seconds() if hasattr(diff_from_floor, 'total_seconds') else 0
    ceil_secs = diff_to_ceiling.total_seconds() if hasattr(diff_to_ceiling, 'total_seconds') else 0

    if floor_secs <= ceil_secs:
        return floor_result
    else:
        return ceiling_result
