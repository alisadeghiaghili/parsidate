"""
Interval: Range class for intervals between two dates, precise or calendar-based.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from typing import Union

class Interval:
    """
    Represents an interval (range) between two date objects.

    Attributes:
        start: Start date/time (JalaliDate or GregorianDate)
        end: End date/time (JalaliDate or GregorianDate)

    Examples:
        Interval(JalaliDate(1402,4,15), JalaliDate(1403,4,15))
        Interval(GregorianDate(...), GregorianDate(...))
    """

    def __init__(self, start, end):
        """
        Initialize interval.

        Args:
            start: Start date/time object (JalaliDate or GregorianDate)
            end: End date/time object (same type as start)
        Raises:
            ValueError if types don't match or end < start
        """
        if type(start) != type(end):
            raise TypeError(f"Start and end must be of same type (got {type(start).__name__} and {type(end).__name__})")
        if end < start:
            raise ValueError("End date must be >= start date.")
        self.start = start
        self.end = end

    def duration(self):
        """
        Compute precise duration (in seconds) between start and end.

        Returns:
            Duration object (parsidate.intervals.duration.Duration)
        """
        from parsidate.intervals.duration import Duration
        diff = self.end - self.start
        if hasattr(diff, 'total_seconds'):
            return Duration(seconds=diff.total_seconds())
        elif hasattr(diff, 'days'):
            return Duration(days=diff.days())
        else:
            return diff

    def length(self, unit: str = "days") -> int:
        """
        Get length of interval in specified unit.

        Args:
            unit: "days", "hours", "minutes", or "seconds"

        Returns:
            Integer length
        """
        dur = self.duration()
        if unit == "days":
            return dur.days()
        elif unit == "hours":
            return int(dur.total_seconds() // 3600)
        elif unit == "minutes":
            return int(dur.total_seconds() // 60)
        elif unit == "seconds":
            return int(dur.total_seconds())
        else:
            raise ValueError(f"Invalid unit: {unit}")

    def __contains__(self, date) -> bool:
        """Check if date is within interval (inclusive)."""
        return self.start <= date <= self.end

    def __repr__(self) -> str:
        return f"Interval(start={self.start}, end={self.end})"

    def __str__(self) -> str:
        return f"[{self.start} to {self.end}]"


def interval(start, end) -> Interval:
    """
    Create an Interval object.

    Args:
        start: Start date (JalaliDate or GregorianDate)
        end: End date (same type as start)

    Returns:
        Interval object

    Example:
        interval(jmd("1403/01/01"), jmd("1403/12/29"))
    """
    return Interval(start, end)
