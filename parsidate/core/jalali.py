"""
JalaliDate: Persian (Solar Hijri) calendar date class.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Portions of this software are inspired by or derived from:
- jalali (https://github.com/shobeiry/jalali) - GPL v3
- lubridate (https://lubridate.tidyverse.org) - GPL

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

from datetime import datetime, timezone as dt_timezone, tzinfo
from typing import Optional, Union, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from parsidate.intervals.period import Period
    from parsidate.intervals.duration import Duration


class JalaliDate:
    """Immutable Jalali (Persian/Solar Hijri) date and time class.

    All operations return NEW objects. Original objects are never modified.

    Attributes:
        year: Jalali year (read-only).
        month: Jalali month (1-12, read-only).
        day: Jalali day (1-31, read-only).
        hour: Hour (0-23, read-only).
        minute: Minute (0-59, read-only).
        second: Second (0-59, read-only).
        microsecond: Microsecond (0-999999, read-only).
        tzinfo: Timezone information (read-only).

    Example:
        >>> jdate = JalaliDate(1403, 8, 18)
        >>> new_date = jdate.add(months=2)
        >>> jdate.month()
        8
        >>> new_date.month()
        10
        >>> (JalaliDate(1403, 1, 10) - JalaliDate(1403, 1, 1)).days()
        9
    """

    __slots__ = ('_year', '_month', '_day', '_hour', '_minute', '_second', '_microsecond', '_tzinfo')

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
        """Initialize an immutable JalaliDate object.

        Args:
            year: Jalali year.
            month: Jalali month (1-12).
            day: Jalali day (1-31).
            hour: Hour (0-23), default 0.
            minute: Minute (0-59), default 0.
            second: Second (0-59), default 0.
            microsecond: Microsecond (0-999999), default 0.
            tzinfo: Timezone info, default None.

        Raises:
            ValueError: If date components are invalid.

        Example:
            >>> jdate = JalaliDate(1402, 8, 18, 14, 45, 30)
            >>> print(jdate.year(), jdate.month(), jdate.day())
            1402 8 18
            >>> jdate_simple = JalaliDate(1403, 1, 1) # Midnight by default
            >>> print(jdate_simple.hour(), jdate_simple.minute())
            0 0
        """
        self._validate_date(year, month, day)
        self._validate_time(hour, minute, second, microsecond)

        object.__setattr__(self, '_year', year)
        object.__setattr__(self, '_month', month)
        object.__setattr__(self, '_day', day)
        object.__setattr__(self, '_hour', hour)
        object.__setattr__(self, '_minute', minute)
        object.__setattr__(self, '_second', second)
        object.__setattr__(self, '_microsecond', microsecond)
        object.__setattr__(self, '_tzinfo', tzinfo)

    def __setattr__(self, name, value):
        """Prevent modification after initialization."""
        raise AttributeError(f"JalaliDate is immutable. Cannot set {name}")

    def __delattr__(self, name):
        """Prevent deletion of attributes."""
        raise AttributeError(f"JalaliDate is immutable. Cannot delete {name}")

    @staticmethod
    def _validate_date(year: int, month: int, day: int) -> None:
        """Validate date components.

        Example:
            >>> JalaliDate._validate_date(1402, 13, 1)  # Raises ValueError
            >>> JalaliDate._validate_date(1402, 12, 29)  # OK
        """
        from parsidate.utils.helpers import days_in_month as get_days_in_month
        if not 1 <= month <= 12:
            raise ValueError(f"Month must be between 1 and 12, got {month}")
        max_day = get_days_in_month(year, month, "jalali")
        if not 1 <= day <= max_day:
            raise ValueError(
                f"Day must be between 1 and {max_day} for month {month} "
                f"of year {year}, got {day}"
            )

    @staticmethod
    def _validate_time(hour: int, minute: int, second: int, microsecond: int) -> None:
        """Validate time components.

        Example:
            >>> JalaliDate._validate_time(14, 30, 45, 0)  # OK
            >>> JalaliDate._validate_time(25, 30, 45, 0)  # Raises ValueError
        """
        if not 0 <= hour <= 23:
            raise ValueError(f"Hour must be between 0 and 23, got {hour}")
        if not 0 <= minute <= 59:
            raise ValueError(f"Minute must be between 0 and 59, got {minute}")
        if not 0 <= second <= 59:
            raise ValueError(f"Second must be between 0 and 59, got {second}")
        if not 0 <= microsecond <= 999999:
            raise ValueError(f"Microsecond must be between 0 and 999999, got {microsecond}")

    # Read-only properties
    def year(self) -> int:
        """Get year (read-only).

        Example:
            >>> jdate = JalaliDate(1402, 8, 18)
            >>> jdate.year()
            1402
        """
        return self._year

    def month(self) -> int:
        """Get month (read-only).

        Example:
            >>> jdate = JalaliDate(1402, 8, 18)
            >>> jdate.month()
            8
        """
        return self._month

    def day(self) -> int:
        """Get day (read-only).

        Example:
            >>> jdate = JalaliDate(1402, 8, 18)
            >>> jdate.day()
            18
        """
        return self._day

    def hour(self) -> int:
        """Get hour (read-only).

        Example:
            >>> jdate = JalaliDate(1402, 8, 18, 14, 30)
            >>> jdate.hour()
            14
        """
        return self._hour

    def minute(self) -> int:
        """Get minute (read-only).

        Example:
            >>> jdate = JalaliDate(1402, 8, 18, 14, 30)
            >>> jdate.minute()
            30
        """
        return self._minute

    def second(self) -> int:
        """Get second (read-only).

        Example:
            >>> jdate = JalaliDate(1402, 8, 18, 14, 30, 45)
            >>> jdate.second()
            45
        """
        return self._second

    def microsecond(self) -> int:
        """Get microsecond (read-only).

        Example:
            >>> jdate = JalaliDate(1402, 8, 18, 14, 30, 45, 123456)
            >>> jdate.microsecond()
            123456
        """
        return self._microsecond

    def tzinfo(self) -> Optional[tzinfo]:
        """Get timezone info (read-only).

        Example:
            >>> jdate = JalaliDate(1402, 8, 18)
            >>> jdate.tzinfo() is None
            True
        """
        return self._tzinfo

    def to_ordinal(self) -> int:
        """Return proleptic Gregorian ordinal for this calendar day.

        Independent of time-of-day; safe for day-count arithmetic
        across Jalali leap years.

        Returns:
            Gregorian ordinal (days since 0001-01-01).

        Example:
            >>> d = JalaliDate(1403, 1, 1)
            >>> d.to_ordinal() == d.to_ordinal()
            True
        """
        from datetime import date as _date
        from parsidate.core.converters import jalali_to_gregorian

        gy, gm, gd = jalali_to_gregorian(self._year, self._month, self._day)
        return _date(gy, gm, gd).toordinal()

    def _seconds_from_midnight(self) -> float:
        """Return seconds elapsed since midnight, including microseconds."""
        return (
            self._hour * 3600
            + self._minute * 60
            + self._second
            + self._microsecond / 1_000_000
        )

    def replace(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        microsecond: Optional[int] = None,
        tzinfo: Optional[tzinfo] = None
    ) -> "JalaliDate":
        """Return new JalaliDate with specified fields replaced.

        Similar to datetime.replace(). Returns a NEW object.

        Args:
            year: New year value (optional).
            month: New month value (optional).
            day: New day value (optional).
            hour: New hour value (optional).
            minute: New minute value (optional).
            second: New second value (optional).
            microsecond: New microsecond value (optional).
            tzinfo: New timezone info (optional).

        Returns:
            New JalaliDate object with replaced values.

        Example:
            >>> jdate = JalaliDate(1402, 8, 18, 14, 30)
            >>> new_date = jdate.replace(year=1403, month=10)
            >>> jdate.year()  # Original unchanged
            1402
            >>> new_date.year()  # New object
            1403
        """
        return JalaliDate(
            year if year is not None else self._year,
            month if month is not None else self._month,
            day if day is not None else self._day,
            hour if hour is not None else self._hour,
            minute if minute is not None else self._minute,
            second if second is not None else self._second,
            microsecond if microsecond is not None else self._microsecond,
            tzinfo if tzinfo is not None else self._tzinfo
        )

    def weekday(self) -> int:
        """Get day of week (0=Shanbeh, 6=Jom'eh).

        Example:
            >>> jdate = JalaliDate(1404, 10, 4, 0, 0, 0, 0, 'Iran')
            >>> jdate.weekday()
            6
        """
        from parsidate.core.converters import jalali_to_gregorian
        gy, gm, gd = jalali_to_gregorian(self._year, self._month, self._day)
        from datetime import date
        greg_date = date(gy, gm, gd)
        py_weekday = greg_date.weekday()
        return (py_weekday + 2) % 7

    def quarter(self) -> int:
        """Get quarter of year (1-4).

        Example:
            >>> JalaliDate(1402, 2, 15).quarter()
            1
            >>> JalaliDate(1402, 8, 18).quarter()
            3
        """
        return (self._month - 1) // 3 + 1

    def day_of_year(self) -> int:
        """Get day number in year (1-365/366).

        Example:
            >>> JalaliDate(1402, 1, 1).day_of_year()
            1
            >>> JalaliDate(1402, 2, 1).day_of_year()
            32
        """
        from parsidate.utils.helpers import days_in_month as get_days_in_month
        days = 0
        for m in range(1, self._month):
            days += get_days_in_month(self._year, m, "jalali")
        return days + self._day

    def is_leap_year(self) -> bool:
        """Check if current year is leap year.

        Example:
            >>> JalaliDate(1403, 1, 1).is_leap_year()
            True
            >>> JalaliDate(1402, 1, 1).is_leap_year()
            False
        """
        from parsidate.utils.helpers import is_leap_year as check_leap_year
        return check_leap_year(self._year, "jalali")

    def add(
        self,
        years: int = 0,
        months: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0
    ) -> "JalaliDate":
        """Return NEW date with added time periods.

        Original object remains unchanged (immutable).

        Args:
            years: Years to add.
            months: Months to add.
            days: Days to add.
            hours: Hours to add.
            minutes: Minutes to add.
            seconds: Seconds to add.

        Returns:
            New JalaliDate object with added time.

        Example:
            >>> jdate = JalaliDate(1402, 8, 18)
            >>> new_date = jdate.add(months=2, days=5)
            >>> jdate.month()  # Original unchanged
            8
            >>> new_date.month()  # New object
            10
            >>> 
            >>> # Crossing year boundary
            >>> jdate2 = JalaliDate(1402, 12, 29)
            >>> result = jdate2.add(days=5)
            >>> result.strftime("%Y/%m/%d")
            '1403/01/04'
        """
        from parsidate.utils.helpers import days_in_month as get_days_in_month

        # Calculate new date
        new_year = self._year + years
        new_month = self._month + months

        while new_month > 12:
            new_month -= 12
            new_year += 1
        while new_month < 1:
            new_month += 12
            new_year -= 1

        max_day = get_days_in_month(new_year, new_month, "jalali")
        new_day = min(self._day, max_day)

        # Add days
        new_day += days
        while new_day > get_days_in_month(new_year, new_month, "jalali"):
            new_day -= get_days_in_month(new_year, new_month, "jalali")
            new_month += 1
            if new_month > 12:
                new_month = 1
                new_year += 1

        while new_day < 1:
            new_month -= 1
            if new_month < 1:
                new_month = 12
                new_year -= 1
            new_day += get_days_in_month(new_year, new_month, "jalali")

        # Add time
        new_second = self._second + seconds
        new_minute = self._minute + (new_second // 60) + minutes
        new_second = new_second % 60

        new_hour = self._hour + (new_minute // 60) + hours
        new_minute = new_minute % 60

        extra_days = new_hour // 24
        new_hour = new_hour % 24

        # Create new object
        result = JalaliDate(new_year, new_month, new_day, new_hour, new_minute, new_second, self._microsecond, self._tzinfo)

        if extra_days > 0:
            result = result.add(days=extra_days)

        return result

    def sub(
        self,
        years: int = 0,
        months: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0
    ) -> "JalaliDate":
        """Return NEW date with subtracted time periods.

        Original object remains unchanged (immutable).

        Args:
            years: Years to subtract.
            months: Months to subtract.
            days: Days to subtract.
            hours: Hours to subtract.
            minutes: Minutes to subtract.
            seconds: Seconds to subtract.

        Returns:
            New JalaliDate object with subtracted time.

        Example:
            >>> jdate = JalaliDate(1402, 10, 15)
            >>> new_date = jdate.sub(months=2, days=5)
            >>> jdate.month()  # Original unchanged
            10
            >>> new_date.month()  # New object
            8
        """
        return self.add(
            years=-years,
            months=-months,
            days=-days,
            hours=-hours,
            minutes=-minutes,
            seconds=-seconds
        )

    def strftime(self, pattern: str, locale: str = "fa") -> str:
        """Format date using strftime-style format codes.

        Args:
            pattern: Format string (e.g., "%Y/%m/%d %H:%M:%S")
            locale: Locale for month/weekday names ("fa" or "en")

        Returns:
            Formatted date string

        Example:
            >>> jdate = JalaliDate(1402, 8, 18, 14, 45, 30)
            >>> jdate.strftime("%Y/%m/%d %H:%M:%S")
            '1402/08/18 14:45:30'
            >>> jdate.strftime("%A، %d %B %Y", locale="fa")
            'سه‌شنبه، ۱۸ آبان ۱۴۰۲'
        """
        from parsidate.formatting.formatters import format_jalali_date
        return format_jalali_date(self, pattern, locale)

    def format(self, pattern: str, locale: str = "fa") -> str:
        """Format date (alias for strftime).

        Example:
            >>> jdate = JalaliDate(1402, 8, 18)
            >>> jdate.format("%Y/%m/%d")
            '1402/08/18'
        """
        return self.strftime(pattern, locale)

    def copy(self) -> "JalaliDate":
        """Return a copy (though unnecessary for immutable objects).

        Since JalaliDate is immutable, this returns self.

        Example:
            >>> jdate = JalaliDate(1402, 8, 18)
            >>> jdate2 = jdate.copy()
            >>> jdate is jdate2  # Same object (immutable)
            True
        """
        return self  # Immutable, no need to copy

    def to_gregorian(self) -> tuple[int, int, int]:
        """Convert to Gregorian calendar date.

        Returns:
            Tuple of (year, month, day) in Gregorian calendar.

        Example:
            >>> jdate = JalaliDate(1402, 8, 18)
            >>> jdate.to_gregorian()
            (2023, 11, 9)
        """
        from parsidate.core.converters import jalali_to_gregorian
        return jalali_to_gregorian(self._year, self._month, self._day)

    def __str__(self) -> str:
        """String representation."""
        return self.strftime("%Y/%m/%d %H:%M:%S", "en")

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"JalaliDate({self._year}, {self._month}, {self._day}, "
            f"{self._hour}, {self._minute}, {self._second})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality including microseconds.

        Timezone is intentionally ignored so naive and aware instances
        that share wall-clock fields compare equal.
        """
        if not isinstance(other, JalaliDate):
            return False
        return (
            self._year == other._year
            and self._month == other._month
            and self._day == other._day
            and self._hour == other._hour
            and self._minute == other._minute
            and self._second == other._second
            and self._microsecond == other._microsecond
        )

    def _cmp_key(self) -> tuple:
        """Return ordering key including microseconds."""
        return (
            self._year,
            self._month,
            self._day,
            self._hour,
            self._minute,
            self._second,
            self._microsecond,
        )

    def __hash__(self) -> int:
        """Hash using the same fields as ``__eq__``."""
        return hash(self._cmp_key())

    def __lt__(self, other: "JalaliDate") -> bool:
        """Less than comparison."""
        return self._cmp_key() < other._cmp_key()

    def __le__(self, other: "JalaliDate") -> bool:
        """Less than or equal."""
        return self == other or self < other

    def __gt__(self, other: "JalaliDate") -> bool:
        """Greater than."""
        return not self <= other

    def __ge__(self, other: "JalaliDate") -> bool:
        """Greater than or equal."""
        return not self < other

    def __add__(self, other: Union["Period", "Duration"]) -> "JalaliDate":
        """Add Period or Duration. Returns NEW object.

        Example:
            >>> from parsidate.intervals import Period
            >>> jdate = JalaliDate(1402, 8, 18)
            >>> p = Period(months=2, days=5)
            >>> new_date = jdate + p
            >>> jdate.month()  # Original unchanged
            8
            >>> new_date.month()
            10
        """
        from parsidate.intervals.period import Period
        from parsidate.intervals.duration import Duration

        if isinstance(other, Period):
            return self.add(
                years=other.years,
                months=other.months,
                days=other.days + other.weeks * 7
            )
        elif isinstance(other, Duration):
            total_seconds = other.total_seconds()
            days_to_add = int(total_seconds // 86400)
            remaining = int(total_seconds % 86400)
            hours_to_add = remaining // 3600
            remaining %= 3600
            minutes_to_add = remaining // 60
            seconds_to_add = remaining % 60
            return self.add(
                days=days_to_add,
                hours=hours_to_add,
                minutes=minutes_to_add,
                seconds=seconds_to_add
            )
        return NotImplemented

    def __sub__(
        self,
        other: Union["JalaliDate", "Period", "Duration"]
    ) -> Union["Duration", "JalaliDate"]:
        """Subtract a date, Period, or Duration.

        When ``other`` is a ``JalaliDate``, returns a ``Duration`` equal
        to the elapsed wall-clock time (leap years and time-of-day included).

        Args:
            other: Value to subtract from this date.

        Returns:
            ``Duration`` for date subtraction, or a new ``JalaliDate``
            for Period/Duration subtraction.

        Raises:
            TypeError: If ``other`` is an unsupported type.

        Example:
            >>> j1 = JalaliDate(1403, 1, 10)
            >>> j0 = JalaliDate(1403, 1, 1)
            >>> (j1 - j0).days()
            9
        """
        from parsidate.intervals.period import Period
        from parsidate.intervals.duration import Duration

        if isinstance(other, JalaliDate):
            day_diff = self.to_ordinal() - other.to_ordinal()
            sec_diff = day_diff * 86400 + (
                self._seconds_from_midnight() - other._seconds_from_midnight()
            )
            return Duration(seconds=sec_diff)
        if isinstance(other, Period):
            return self.sub(
                years=other.years,
                months=other.months,
                days=other.days + other.weeks * 7,
            )
        if isinstance(other, Duration):
            total_seconds = other.total_seconds()
            days_to_sub = int(total_seconds // 86400)
            remaining = int(total_seconds % 86400)
            hours_to_sub = remaining // 3600
            remaining %= 3600
            minutes_to_sub = remaining // 60
            seconds_to_sub = remaining % 60
            return self.sub(
                days=days_to_sub,
                hours=hours_to_sub,
                minutes=minutes_to_sub,
                seconds=seconds_to_sub,
            )
        return NotImplemented
