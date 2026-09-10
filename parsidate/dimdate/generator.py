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
    include_fiscal: bool = True,
    fiscal_year_start_month: int = 1,
    holidays=None,
    weekend_days: Optional[List[int]] = None,
    use_iran_holidays: bool = True,
    as_of=None,
) -> pd.DataFrame:
    """Generate a warehouse-grade date dimension table.

    Args:
        start: Start date string (``1403/01/01`` or ``2024-01-01``).
        end: End date string (inclusive).
        calendar: ``\"jalali\"`` or ``\"gregorian\"``.
        include_fiscal: Include fiscal_year/quarter/month columns.
        fiscal_year_start_month: Month when fiscal year starts (1-12).
        holidays: ``HolidaySet``, iterable of dates, or list of date strings.
        weekend_days: Weekend weekday indices. Jalali default ``[6]`` (Friday);
            Gregorian default ``[5, 6]`` (Sat/Sun in Python numbering).
        use_iran_holidays: Auto-load official Iranian holidays for Jalali
            years when ``holidays`` is not provided.
        as_of: Optional reference date for ``ytd_flag`` / ``mtd_flag``.

    Returns:
        ``pandas.DataFrame`` with one row per calendar day.

    Example:
        >>> from parsidate.dimdate import generate_dim_date
        >>> dim = generate_dim_date("1403/01/01", "1403/01/07")
        >>> bool(dim.loc[dim.date_key == 14030101, "is_holiday"].iloc[0])
        True
    """
    from parsidate.core.jalali import JalaliDate
    from parsidate.core.gregorian import GregorianDate
    from parsidate.core.converters import jalali_to_gregorian, gregorian_to_jalali
    from parsidate.holidays import HolidaySet, iran_holidays
    from parsidate.operations.business import is_business_day
    from parsidate.parsers import jmd, ymd
    from parsidate.utils.helpers import (
        month_name, weekday_name, is_leap_year,
        days_in_month, get_season,
    )

    if calendar == "jalali":
        start_date = jmd(start)
        end_date = jmd(end)
        if weekend_days is None:
            weekend_days = [6]
    else:
        start_date = ymd(start)
        end_date = ymd(end)
        if weekend_days is None:
            weekend_days = [5, 6]

    # Normalize holidays to HolidaySet + optional name map
    holiday_names = {}
    if holidays is None and use_iran_holidays and calendar == "jalali":
        years = range(start_date.year(), end_date.year() + 1)
        acc = HolidaySet()
        for y in years:
            acc = acc | iran_holidays(y)
        holiday_set = acc
        for d in holiday_set:
            holiday_names[(d.year(), d.month(), d.day())] = "official"
    elif isinstance(holidays, HolidaySet):
        holiday_set = holidays
    elif holidays:
        parsed = []
        for h in holidays:
            if isinstance(h, str):
                parsed.append(jmd(h) if calendar == "jalali" else ymd(h))
            else:
                parsed.append(h)
        holiday_set = HolidaySet(dates=parsed)
    else:
        holiday_set = HolidaySet()

    rows = []
    current = start_date.copy()

    while current <= end_date:
        year, month, day = current.year(), current.month(), current.day()
        date_key = year * 10000 + month * 100 + day
        weekday = current.weekday()
        is_weekend = weekday in weekend_days
        key3 = (year, month, day)
        is_holiday = current in holiday_set
        holiday_name = holiday_names.get(key3, "") if is_holiday else ""

        if calendar == "jalali":
            biz = is_business_day(
                current,
                weekend=weekend_days,
                holidays=holiday_set if holiday_set else None,
                use_iran_holidays=False,
            )
            gy, gm, gd = jalali_to_gregorian(year, month, day)
            gdt = datetime(gy, gm, gd)
            iso_y, iso_w, iso_d = gdt.isocalendar()
            month_end_day = days_in_month(year, month, "jalali")
        else:
            biz = not is_weekend
            gy, gm, gd = year, month, day
            gdt = current.to_datetime()
            iso_y, iso_w, iso_d = gdt.isocalendar()
            month_end_day = days_in_month(year, month, "gregorian")

        full_date = current.strftime(
            "%Y/%m/%d" if calendar == "jalali" else "%Y-%m-%d", "en"
        )
        month_start = f"{year:04d}/{month:02d}/01" if calendar == "jalali" else f"{year:04d}-{month:02d}-01"
        month_end = (
            f"{year:04d}/{month:02d}/{month_end_day:02d}"
            if calendar == "jalali"
            else f"{year:04d}-{month:02d}-{month_end_day:02d}"
        )

        ytd_flag = False
        mtd_flag = False
        if as_of is not None:
            ytd_flag = year == as_of.year() and (
                (month, day) <= (as_of.month(), as_of.day())
            )
            mtd_flag = (
                year == as_of.year()
                and month == as_of.month()
                and day <= as_of.day()
            )

        row = {
            "date_key": date_key,
            "full_date": full_date,
            "year": year,
            "quarter": current.quarter(),
            "month": month,
            "day": day,
            "month_name_en": month_name(month, "en", calendar),
            "month_short_en": month_name(month, "en", calendar)[:3],
            "weekday": weekday,
            "weekday_name_en": weekday_name(weekday, "en", calendar),
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
            "is_business_day": biz,
            "holiday_name": holiday_name,
            "iso_year": int(iso_y),
            "iso_week": int(iso_w),
            "iso_weekday": int(iso_d),
            "month_start": month_start,
            "month_end": month_end,
            "is_leap_year": is_leap_year(year, calendar),
            "day_of_year": current.day_of_year(),
            "week_of_year": (current.day_of_year() - 1) // 7 + 1,
            "days_in_month": month_end_day,
            "season": get_season(month, calendar),
            "ytd_flag": ytd_flag,
            "mtd_flag": mtd_flag,
        }

        if calendar == "jalali":
            row["month_name_fa"] = month_name(month, "fa", calendar)
            row["weekday_name_fa"] = weekday_name(weekday, "fa", calendar)

        if include_fiscal:
            if month >= fiscal_year_start_month:
                fiscal_year = year
            else:
                fiscal_year = year - 1
            fiscal_month = ((month - fiscal_year_start_month) % 12) + 1
            row["fiscal_year"] = fiscal_year
            row["fiscal_quarter"] = ((fiscal_month - 1) // 3) + 1
            row["fiscal_month"] = fiscal_month

        rows.append(row)
        current = current.add(days=1)

    df = pd.DataFrame(rows)

    cols = [
        "date_key", "full_date", "year", "quarter", "month", "day",
        "month_name_en",
    ]
    if calendar == "jalali":
        cols.append("month_name_fa")
    cols += [
        "month_short_en",
        "weekday", "weekday_name_en",
    ]
    if calendar == "jalali":
        cols.append("weekday_name_fa")
    cols += [
        "is_weekend", "is_holiday", "is_business_day", "holiday_name",
        "iso_year", "iso_week", "iso_weekday",
        "month_start", "month_end",
        "is_leap_year", "day_of_year", "week_of_year", "days_in_month",
        "season", "ytd_flag", "mtd_flag",
    ]
    if include_fiscal:
        cols += ["fiscal_year", "fiscal_quarter", "fiscal_month"]
    return df[cols]
