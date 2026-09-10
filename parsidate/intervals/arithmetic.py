"""Calendar arithmetic re-exported from :mod:`parsidate.operations.arithmetic`.

This module exists only for backward compatibility. Canonical implementations
live in ``parsidate.operations.arithmetic``.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from parsidate.operations.arithmetic import (
    add_days,
    add_months,
    add_weeks,
    add_years,
    date_range,
    diff_in_days,
    next_month,
    next_year,
    prev_month,
    prev_year,
)

__all__ = [
    "add_days",
    "add_months",
    "add_weeks",
    "add_years",
    "date_range",
    "diff_in_days",
    "next_month",
    "next_year",
    "prev_month",
    "prev_year",
]
