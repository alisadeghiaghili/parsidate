"""
parsidate.intervals: Time interval classes (Duration, Period, Interval) for ParsiDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from .duration import Duration, hours, minutes, seconds, duration
from .period import Period, years, months, weeks, days, period
from .interval import Interval, interval

__all__ = [
    "Duration", "hours", "minutes", "seconds", "duration",
    "Period", "years", "months", "weeks", "days", "period",
    "Interval", "interval",
]
