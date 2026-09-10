"""
Date and Dimension Date Table for Jalali (Persian) and Gregorian calendars.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from typing import Optional, List, Literal

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "parsidate.dimdate requires pandas. Install with: pip install parsidate[dimdate]"
    ) from exc

from datetime import datetime

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
        current = current.add(days=step_days)

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
    current = start.replace(day=1)
    while current <= end:
        yield current.copy()
        current = add_months(current, 1).replace(day=1)

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
    current = start.replace(month=1, day=1)
    while current <= end:
        yield current.copy()
        current = add_years(current, 1).replace(month=1, day=1)

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

def generate_dim_date(
    start: str,
    end: str,
    calendar: Literal["jalali", "gregorian"] = "jalali",
    include_fiscal: bool = False,
    fiscal_year_start_month: int = 1,
    holidays: Optional[List[str]] = None,
    weekend_days: Optional[List[int]] = None
) -> pd.DataFrame:
    """
    Generate a complete date dimension table for data warehousing.

    This function creates a comprehensive date dimension DataFrame suitable
    for use in data warehouses, business intelligence, and analytics.

    Args:
        start: Start date string (e.g., "1400/01/01" or "2021-01-01")
        end: End date string (e.g., "1400/12/29" or "2021-12-31")
        calendar: Calendar system ("jalali" or "gregorian")
        include_fiscal: Include fiscal year columns
        fiscal_year_start_month: Month when fiscal year starts (1-12)
        holidays: List of holiday date strings (optional)
        weekend_days: List of weekend day numbers (0=Sat for Jalali, 0=Mon for Greg)
                     Default: [6] (Friday) for Jalali, [5,6] (Sat/Sun) for Gregorian

    Returns:
        pandas.DataFrame with comprehensive date dimension columns

    Example:
        >>> from parsidate.dimdate import generate_dim_date
        >>> dim = generate_dim_date(
        ...     start="1400/01/01",
        ...     end="1400/01/10",
        ...     calendar="jalali",
        ...     include_fiscal=True
        ... )
        >>> print(dim.head())
        >>> dim.to_csv("dim_date.csv", index=False)

    Columns:
        - date_key: Integer key (YYYYMMDD format)
        - full_date: Full date string
        - year: Year number
        - quarter: Quarter (1-4)
        - month: Month number (1-12)
        - day: Day of month
        - month_name_en: Month name in English
        - month_name_fa: Month name in Persian (Jalali only)
        - month_short_en: Short month name (3 chars)
        - weekday: Day of week (0-6)
        - weekday_name_en: Weekday name in English
        - weekday_name_fa: Weekday name in Persian (Jalali only)
        - is_weekend: Boolean for weekend
        - is_holiday: Boolean for holiday (if holidays provided)
        - is_leap_year: Boolean for leap year
        - day_of_year: Day number in year (1-365/366)
        - week_of_year: Week number in year
        - days_in_month: Number of days in the month
        - season: Season name
        - fiscal_year: Fiscal year (if include_fiscal=True)
        - fiscal_quarter: Fiscal quarter (if include_fiscal=True)
        - fiscal_month: Fiscal month number (if include_fiscal=True)
    """
    from parsidate.parsers import jmd, ymd
    from parsidate.utils.helpers import (
        month_name, weekday_name, is_leap_year, 
        days_in_month, get_season
    )

    # Parse start and end dates
    if calendar == "jalali":
        start_date = jmd(start)
        end_date = jmd(end)
        if weekend_days is None:
            weekend_days = [6]  # Friday for Jalali
    else:
        start_date = ymd(start)
        end_date = ymd(end)
        if weekend_days is None:
            weekend_days = [5, 6]  # Saturday and Sunday for Gregorian

    # Parse holidays if provided
    holiday_set = set()
    if holidays:
        for h in holidays:
            if calendar == "jalali":
                h_date = jmd(h)
            else:
                h_date = ymd(h)
            # Create key: YYYYMMDD
            h_key = h_date.year() * 10000 + h_date.month() * 100 + h_date.day()
            holiday_set.add(h_key)

    # Generate date range
    dates_data = []
    current = start_date.copy()

    while current <= end_date:
        # Basic date components
        year = current.year()
        month = current.month()
        day = current.day()

        # Date key (YYYYMMDD format)
        date_key = year * 10000 + month * 100 + day

        # Standard strftime codes (Python strptime/strftime compatible)
        full_date = current.strftime(
            "%Y/%m/%d" if calendar == "jalali" else "%Y-%m-%d", "en"
        )

        # Quarter
        quarter = current.quarter()

        # Month names
        month_name_en = month_name(month, "en", calendar)
        month_short_en = month_name_en[:3]

        # Weekday
        weekday = current.weekday()
        weekday_name_en = weekday_name(weekday, "en", calendar)

        # Weekend check
        is_weekend = weekday in weekend_days

        # Holiday check
        is_holiday = date_key in holiday_set

        # Leap year
        is_leap = is_leap_year(year, calendar)

        # Day of year
        day_of_year = current.day_of_year()

        # Week of year (simple calculation)
        week_of_year = (day_of_year - 1) // 7 + 1

        # Days in month
        days_in_this_month = days_in_month(year, month, calendar)

        # Season
        season = get_season(month, calendar)

        # Build row dictionary
        row = {
            "date_key": date_key,
            "full_date": full_date,
            "year": year,
            "quarter": quarter,
            "month": month,
            "day": day,
            "month_name_en": month_name_en,
            "month_short_en": month_short_en,
            "weekday": weekday,
            "weekday_name_en": weekday_name_en,
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
            "is_leap_year": is_leap,
            "day_of_year": day_of_year,
            "week_of_year": week_of_year,
            "days_in_month": days_in_this_month,
            "season": season,
        }

        # Add Persian names for Jalali calendar
        if calendar == "jalali":
            row["month_name_fa"] = month_name(month, "fa", calendar)
            row["weekday_name_fa"] = weekday_name(weekday, "fa", calendar)

        # Fiscal year calculations
        if include_fiscal:
            # Calculate fiscal year
            if month >= fiscal_year_start_month:
                fiscal_year = year
            else:
                fiscal_year = year - 1

            # Calculate fiscal month (1-12 starting from fiscal_year_start_month)
            fiscal_month = ((month - fiscal_year_start_month) % 12) + 1

            # Calculate fiscal quarter
            fiscal_quarter = ((fiscal_month - 1) // 3) + 1

            row["fiscal_year"] = fiscal_year
            row["fiscal_quarter"] = fiscal_quarter
            row["fiscal_month"] = fiscal_month

        dates_data.append(row)

        # Move to next day
        current = current.add(days=1)

    # Create DataFrame
    df = pd.DataFrame(dates_data)

    # Reorder columns for better presentation
    base_columns = [
        "date_key", "full_date", "year", "quarter", "month", "day",
        "month_name_en"
    ]

    if calendar == "jalali":
        base_columns.append("month_name_fa")

    base_columns.extend([
        "month_short_en",
        "weekday", "weekday_name_en"
    ])

    if calendar == "jalali":
        base_columns.append("weekday_name_fa")

    base_columns.extend([
        "is_weekend", "is_holiday", "is_leap_year",
        "day_of_year", "week_of_year", "days_in_month", "season"
    ])

    if include_fiscal:
        base_columns.extend(["fiscal_year", "fiscal_quarter", "fiscal_month"])

    # Reorder DataFrame columns
    df = df[base_columns]

    return df
