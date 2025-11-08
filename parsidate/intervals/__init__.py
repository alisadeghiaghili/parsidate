"""
parsidate.intervals: Time interval classes (Duration, Period, Interval) for ParsiDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from .duration import Duration
from .period import Period, years, months, weeks, days
from .interval import Interval

__all__ = [
    "Duration",
    "Period", "years", "months", "weeks", "days",
    "Interval",
]
