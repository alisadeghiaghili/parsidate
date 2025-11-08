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
        # If classes implement __sub__ for two dates, returns
