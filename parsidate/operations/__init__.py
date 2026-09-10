"""
parsidate.operations: Arithmetic, comparison, and rounding operations for calendar dates.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
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
    min_date, max_date,
    is_before, is_after, is_between,
)
from .rounding import (
    floor_to_day, ceil_to_day,
    floor_to_week, ceil_to_week,
    floor_to_month, ceil_to_month,
    floor_to_quarter, ceil_to_quarter,
    floor_to_year, ceil_to_year,
    floor_date, ceiling_date, round_date,
)
from .business import (
    is_business_day,
    networkdays,
    add_business_days,
    next_business_day,
    prev_business_day,
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
    "is_before", "is_after", "is_between",
    "floor_to_day", "ceil_to_day",
    "floor_to_week", "ceil_to_week",
    "floor_to_month", "ceil_to_month",
    "floor_to_quarter", "ceil_to_quarter",
    "floor_to_year", "ceil_to_year",
    "floor_date", "ceiling_date", "round_date",
    "is_business_day", "networkdays", "add_business_days",
    "next_business_day", "prev_business_day",
]
