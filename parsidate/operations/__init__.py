"""
parsidate.operations: Arithmetic, comparison, and rounding operations for calendar dates.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from .arithmetic import (
    add_months,
    add_years,
    diff_in_days,
    next_month,
    prev_month,
    next_year,
    prev_year,
    add_days,
    add_weeks,
    date_range,
)
from .comparison import (
    eq, ne, lt, le, gt, ge,
    between,
    min_date, max_date
)
from .rounding import (
    floor_to_day, ceil_to_day,
    floor_to_week, ceil_to_week,
    floor_to_month, ceil_to_month,
    floor_to_quarter, ceil_to_quarter,
    floor_to_year, ceil_to_year
)

__all__ = [
    "add_months", "add_years",
    "diff_in_days",
    "next_month", "prev_month",
    "next_year", "prev_year",
    "add_days", "add_weeks",
    "date_range",
    "eq", "ne", "lt", "le", "gt", "ge",
    "between",
    "min_date", "max_date",
    "floor_to_day", "ceil_to_day",
    "floor_to_week", "ceil_to_week",
    "floor_to_month", "ceil_to_month",
    "floor_to_quarter", "ceil_to_quarter",
    "floor_to_year", "ceil_to_year"
]
