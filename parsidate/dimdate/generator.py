"""
Date generators for Jalali (Persian) and Gregorian calendars.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

def date_range(start, end, step_days: int = 1):
    """
    Generate sequence of dates from start to end (inclusive) with step in days.

    Args:
        start: Start date object (JalaliDate or GregorianDate).
        end: End date object (same type).
        step_days: Step in days (positive integer).

    Yields:
        Date objects, starting from start to end.
    """
    current = start.copy()
    while current <= end:
        yield current.copy()
        current.add(days=step_days)

def month_range(start, end):
    """
    Generate sequence of first days of months from start to end (inclusive).

    Args:
        start: Start date (date object).
        end: End date (date object).

    Yields:
        Date objects at first day of each month from start to end.
    """
    from parsidate.operations.arithmetic import add_months
    current = start.copy().day(1)
    while current <= end:
        yield current.copy()
        current = add_months(current, 1).day(1)

def year_range(start, end):
    """
    Generate sequence of first days of years from start to end (inclusive).

    Args:
        start: Start date (date object).
        end: End date (date object).

    Yields:
        Date objects at first day of each year from start to end.
    """
    from parsidate.operations.arithmetic import add_years
    current = start.copy().month(1).day(1)
    while current <= end:
        yield current.copy()
        current = add_years(current, 1).month(1).day(1)

def custom_range(start, end, days=0, months=0, years=0):
    """
    Generate custom sequence of dates with arbitrary step (days, months, years).

    Args:
        start: Start date (date object).
        end: End date (date object).
        days: Step in days.
        months: Step in months.
        years: Step in years.

    Yields:
        Date objects.
    """
    current = start.copy()
    while current <= end:
        yield current.copy()
        current = current.add(years=years, months=months, days=days)
