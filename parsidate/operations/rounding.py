"""
Rounding and truncation operations for JalaliDate and GregorianDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

def floor_to_day(date) -> object:
    """Return a copy of date with time zeroed (00:00:00.000000)."""
    return date.copy().hour(0).minute(0).second(0).microsecond(0)

def ceil_to_day(date) -> object:
    """
    Return a copy of date rounded up to start of next day (if time not zero).
    """
    if date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0:
        return date.copy()
    # Add 1 day, then zero time
    return date.copy().add(days=1).hour(0).minute(0).second(0).microsecond(0)

def floor_to_week(date, week_start: int = 0) -> سobject:
    """
    Round date down to start of week.

    Args:
        date: Date object.
        week_start: 0 for Saturday, 1 for Sunday, etc.

    Returns:
        Date object.
    """
    delta = (date.weekday() - week_start) % 7
    return date.copy().add(days=-delta).hour(0).minute(0).second(0).microsecond(0)

def ceil_to_week(date, week_start: int = 0) -> object:
    """
    Round date up to start of next week (if not start of week).

    Args:
        date: Date object.
        week_start: 0 for Saturday, 1 for Sunday, etc.

    Returns:
        Date object.
    """
    if date.weekday() == week_start and date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0:
        return date.copy()
    return date.copy().add(days=(7 - (date.weekday() - week_start) % 7)).hour(0).minute(0).second(0).microsecond(0)

def floor_to_month(date) -> object:
    """Round date down to start of its month."""
    return date.copy().day(1).hour(0).minute(0).second(0).microsecond(0)

def ceil_to_month(date) -> object:
    """Round date up to start of next month (if not first of month at 00:00)."""
    if date.day() == 1 and date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0:
        return date.copy()
    # Add one month and floor
    return date.copy().add(months=1).day(1).hour(0).minute(0).second(0).microsecond(0)

def floor_to_quarter(date) -> object:
    """Round date down to start of its quarter."""
    q_start_month = 3 * ((date.month() - 1) // 3) + 1
    return date.copy().month(q_start_month).day(1).hour(0).minute(0).second(0).microsecond(0)

def ceil_to_quarter(date) -> object:
    """
    Round date up to start of next quarter (if not at start already).
    """
    q_start_month = 3 * ((date.month() - 1) // 3) + 1
    at_start = (date.month() == q_start_month and date.day() == 1 and date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0)
    if at_start:
        return date.copy()
    # Next quarter: add 3 - ((date.month() - q_start_month) % 3) months, floor to first day
    return date.copy().add(months=3 - ((date.month() - q_start_month) % 3)).month(q_start_month + 3 if q_start_month + 3 <= 12 else (q_start_month + 3) % 12).day(1).hour(0).minute(0).second(0).microsecond(0)

def floor_to_year(date) -> object:
    """Round date down to start of year."""
    return date.copy().month(1).day(1).hour(0).minute(0).second(0).microsecond(0)

def ceil_to_year(date) -> object:
    """Round date up to start of next year (if not at start already)."""
    at_start = (date.month() == 1 and date.day() == 1 and date.hour() == 0 and date.minute() == 0 and date.second() == 0 and date.microsecond() == 0)
    if at_start:
        return date.copy()
    return date.copy().add(years=1).month(1).day(1).hour(0).minute(0).second(0).microsecond(0)
