"""
Calendar arithmetic operations for Jalali and Gregorian dates.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from typing import Union

def add_months(date, n: int) -> object:
    """
    Add n months to date (JalaliDate or GregorianDate).

    Args:
        date: Date object.
        n: Number of months to add.

    Returns:
        Date object (same type) after addition.
    """
    month = date.month() + n
    year = date.year() + (month - 1) // 12
    month = (month - 1) % 12 + 1
    day = date.day()
    # Adjust max day
    from parsidate.utils.helpers import days_in_month
    max_day = days_in_month(year, month, "jalali" if date.__class__.__name__ == "JalaliDate" else "gregorian")
    if day > max_day:
        day = max_day
    return date.copy().year(year).month(month).day(day)

def add_years(date, n: int) -> object:
    """
    Add n years to date (JalaliDate or GregorianDate).

    Args:
        date: Date object.
        n: Years to add.

    Returns:
        Date object (same type) after addition.
    """
    year = date.year() + n
    month = date.month()
    day = date.day()
    from parsidate.utils.helpers import days_in_month
    max_day = days_in_month(year, month, "jalali" if date.__class__.__name__ == "JalaliDate" else "gregorian")
    if day > max_day:
        day = max_day
    return date.copy().year(year).month(month).day(day)

def diff_in_days(date1, date2) -> int:
    """
    Return difference in days between two dates (date1 - date2).

    Args:
        date1: First date object.
        date2: Second date object.

    Returns:
        Integer number of days.
    """
    dur = date1 - date2  
    return dur.days() if hasattr(dur, "days") else int(dur)

def next_month(date) -> object:
    """Return next calendar month for date."""
    return add_months(date, 1)

def prev_month(date) -> object:
    """Return previous calendar month for date."""
    return add_months(date, -1)

def next_year(date) -> object:
    """Return next calendar year for date."""
    return add_years(date, 1)

def prev_year(date) -> object:
    """Return previous calendar year for date."""
    return add_years(date, -1)

def add_days(date, n: int) -> object:
    """
    Add n days to date.

    Args:
        date: Date object.
        n: Days to add.

    Returns:
        Date object after addition.
    """
    return date.copy().add(days=n)

def add_weeks(date, n: int) -> object:
    """
    Add n weeks to date.

    Args:
        date: Date object.
        n: Weeks to add.

    Returns:
        Date object after addition.
    """
    return date.copy().add(days=7*n)

def date_range(start, end, step_days: int = 1):
    """
    Generate dates from start to end (inclusive) with step in days.

    Args:
        start: Start date object.
        end: End date object.
        step_days: Step in days.

    Yields:
        Date objects.
    """
    current = start.copy()
    while current <= end:
        yield current.copy()
        current.add(days=step_days)
