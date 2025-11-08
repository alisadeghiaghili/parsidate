"""
parsidate.generator: Range and sequence generators for dates.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from .generator import (
    date_range,
    month_range,
    year_range,
    custom_range,
)

__all__ = [
    "date_range",
    "month_range",
    "year_range",
    "custom_range",
]
