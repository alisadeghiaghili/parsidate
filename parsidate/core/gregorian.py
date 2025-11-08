"""
GregorianDate: Gregorian calendar date/time class with extended functionality.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from datetime import datetime, timezone as dt_timezone, tzinfo
from typing import Optional, Union, Literal


class GregorianDate:
    """
    Gregorian calendar date/time class similar to JalaliDate.

    Attributes:
        year: Gregorian year.
        month: Gregorian month (1-12).
        day: Gregorian day (1-31).
        hour: Hour (0-23).
        minute: Minute (0-59).
        second: Second (0-59).
        microsecond: Microsecond (0-999999).
        tzinfo: Timezone (optional).
    """

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: Optional[tzinfo] = None
    ):
        """
        Initialize GregorianDate.

        Args:
            year: Year.
            month: Month (1-12).
            day: Day (1-31).
            hour: Hour (0-23). Default is 0.
            minute: Minute (0-59). Default is 0.
            second: Second (0-59). Default is 0.
            microsecond: Microsecond (0-999999). Default is 0.
            tzinfo: Timezone info. Default is None.

        Raises:
            ValueError: For invalid date or time.
        """
        self._dt = datetime(year, month, day, hour, minute, second, microsecond, tzinfo)

    def year(self, new_year: Optional[int] = None) -> Union[int, "GregorianDate"]:
        """
        Get or set year.

        Args:
            new_year: New year value or None.
        Returns:
            int if new_year is None, otherwise self for chaining.
        """
        if new_year is None:
            return self._dt.year
        self._dt = self._dt.replace(year=new_year)
        return self

    def month(self, new_month: Optional[int] = None) -> Union[int, "GregorianDate"]:
        """Get or set month."""
        if new_month is None:
            return self._dt.month
        self._dt = self._dt.replace(month=new_month)
        return self

    def day(self, new_day: Optional[int] = None) -> Union[int, "GregorianDate"]:
        """Get or set day."""
        if new_day is None:
            return self._dt.day
        self._dt = self._dt.replace(day=new_day)
        return self

    def hour(self, new_hour: Optional[int] = None) -> Union[int, "GregorianDate"]:
        """Get or set hour."""
        if new_hour is None:
            return self._dt.hour
        self._dt = self._dt.replace(hour=new_hour)
        return self

    def minute(self, new_minute: Optional[int] = None) -> Union[int, "GregorianDate"]:
        """Get or set minute."""
        if new_minute is None:
            return self._dt.minute
        self._dt = self._dt.replace(minute=new_minute)
        return self

    def second(self, new_second: Optional[int] = None) -> Union[int, "GregorianDate"]:
        """Get or set second."""
        if new_second is None:
            return self._dt.second
        self._dt = self._dt.replace(second=new_second)
        return self

    def microsecond(self, new_microsecond: Optional[int] = None) -> Union[int, "GregorianDate"]:
        """Get or set microsecond."""
        if new_microsecond is None:
            return self._dt.microsecond
        self._dt = self._dt.replace(microsecond=new_microsecond)
        return self

    def tzinfo(self, new_tzinfo: Optional[tzinfo] = None) -> Union[Optional[tzinfo], "GregorianDate"]:
        """Get or set timezone."""
        if new_tzinfo is None:
            return self._dt.tzinfo
        self._dt = self._dt.replace(tzinfo=new_tzinfo)
        return self

    def weekday(self) -> int:
        """
        Get weekday (0=Monday, 6=Sunday).
        """
        return self._dt.weekday()

    def format(self, pattern: str, locale: Literal["en"] = "en") -> str:
        """
        Format date using strftime pattern.

        Args:
            pattern: strftime compatible format string.
            locale: Ignored for now (reserved for future/localization).

        Returns:
            Formatted date string.
        """
        return self._dt.strftime(pattern)

    def is_leap_year(self) -> bool:
        """
        Check if the year is a leap year.

        Returns:
            True if leap year, False otherwise.
        """
        year = self._dt.year
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def copy(self) -> "GregorianDate":
        """
        Make a copy of this date object.
        """
        return GregorianDate(
            self._dt.year, self._dt.month, self._dt.day,
            self._dt.hour, self._dt.minute, self._dt.second,
            self._dt.microsecond, self._dt.tzinfo
        )

    def to_datetime(self) -> datetime:
        """
        Return underlying datetime object.
        """
        return self._dt

    def __str__(self) -> str:
        return self._dt.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self) -> str:
        return (f"GregorianDate({self.year()}, {self.month()}, {self.day()}, "
                f"{self.hour()}, {self.minute()}, {self.second()})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, GregorianDate):
            return False
        return self._dt == other._dt

    def __lt__(self, other) -> bool:
        return self._dt < other._dt

    def __le__(self, other) -> bool:
        return self._dt <= other._dt

    def __gt__(self, other) -> bool:
        return self._dt > other._dt

    def __ge__(self, other) -> bool:
        return self._dt >= other._dt
    
    def __add__(
    self,
    years: int = 0,
    months: int = 0,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0
    ) -> "GregorianDate":
    """Add time periods to date (calendar arithmetic).

    Args:
        years: Years to add.
        months: Months to add.
        days: Days to add.
        hours: Hours to add.
        minutes: Minutes to add.
        seconds: Seconds to add.
    Returns:
        Self for method chaining.
    """
    from parsidate.utils.helpers import days_in_month

    # Add years/months
    new_year = self.year() + years
    new_month = self.month() + months
    while new_month > 12:
        new_month -= 12
        new_year += 1
    while new_month < 1:
        new_month += 12
        new_year -= 1
    max_day = days_in_month(new_year, new_month, "gregorian")
    new_day = min(self.day(), max_day)

    # Start new date
    self._dt = self._dt.replace(year=new_year, month=new_month, day=new_day)

    # Add days/hours/minutes/seconds
    extra_time = (
        days * 86400 +
        hours * 3600 +
        minutes * 60 +
        seconds
    )
    if extra_time:
        from datetime import timedelta
        self._dt = self._dt + timedelta(seconds=extra_time)

    return self

    def __sub__(
    self,
    years: int = 0,
    months: int = 0,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0
    ) -> "GregorianDate":
    """
    Subtract time periods from date (calendar arithmetic).

    Args:
        years: Years to subtract.
        months: Months to subtract.
        days: Days to subtract.
        hours: Hours to subtract.
        minutes: Minutes to subtract.
        seconds: Seconds to subtract.
    Returns:
        Self for method chaining.
    """
    
    return self.add(
        years=-years,
        months=-months,
        days=-days,
        hours=-hours,
        minutes=-minutes,
        seconds=-seconds
    )

