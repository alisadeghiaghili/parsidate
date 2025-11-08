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
    """Jalali (Persian/Solar Hijri) date and time class.

    This class provides functionality for working with Persian calendar dates,
    including parsing, formatting, arithmetic operations, and conversions.

    Attributes:
        year: Jalali year.
        month: Jalali month (1-12).
        day: Jalali day (1-31).
        hour: Hour (0-23).
        minute: Minute (0-59).
        second: Second (0-59).
        microsecond: Microsecond (0-999999).
        tzinfo: Timezone information.

    Examples:
        >>> date = JalaliDate(1403, 8, 18)
        >>> date.format("Y/m/d")
        "1403/08/18"
        >>> date.add(months=2, days=5)
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
        """Initialize a JalaliDate object.

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
        """
        from parsidate.utils.helpers import days_in_month as get_days_in_month

        self._validate_date(year, month, day)
        self._validate_time(hour, minute, second, microsecond)

        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo

    @staticmethod
    def _validate_date(year: int, month: int, day: int) -> None:
        """Validate date components."""
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
    def _validate_time(
        hour: int,
        minute: int,
        second: int,
        microsecond: int
    ) -> None:
        """Validate time components."""
        if not 0 <= hour <= 23:
            raise ValueError(f"Hour must be between 0 and 23, got {hour}")
        if not 0 <= minute <= 59:
            raise ValueError(f"Minute must be between 0 and 59, got {minute}")
        if not 0 <= second <= 59:
            raise ValueError(f"Second must be between 0 and 59, got {second}")
        if not 0 <= microsecond <= 999999:
            raise ValueError(
                f"Microsecond must be between 0 and 999999, got {microsecond}"
            )

    def year(self, new_year: Optional[int] = None) -> Union[int, "JalaliDate"]:
        """Get or set year.

        Args:
            new_year: New year value, or None to get current year.

        Returns:
            Current year if new_year is None, else self for chaining.
        """
        if new_year is None:
            return self._year
        from parsidate.utils.helpers import days_in_month as get_days_in_month
        self._validate_date(new_year, self._month, self._day)
        self._year = new_year
        return self

    def month(self, new_month: Optional[int] = None) -> Union[int, "JalaliDate"]:
        """Get or set month."""
        if new_month is None:
            return self._month
        self._validate_date(self._year, new_month, self._day)
        self._month = new_month
        return self

    def day(self, new_day: Optional[int] = None) -> Union[int, "JalaliDate"]:
        """Get or set day."""
        if new_day is None:
            return self._day
        self._validate_date(self._year, self._month, new_day)
        self._day = new_day
        return self

    def hour(self, new_hour: Optional[int] = None) -> Union[int, "JalaliDate"]:
        """Get or set hour."""
        if new_hour is None:
            return self._hour
        self._validate_time(new_hour, self._minute, self._second, self._microsecond)
        self._hour = new_hour
        return self

    def minute(self, new_minute: Optional[int] = None) -> Union[int, "JalaliDate"]:
        """Get or set minute."""
        if new_minute is None:
            return self._minute
        self._validate_time(self._hour, new_minute, self._second, self._microsecond)
        self._minute = new_minute
        return self

    def second(self, new_second: Optional[int] = None) -> Union[int, "JalaliDate"]:
        """Get or set second."""
        if new_second is None:
            return self._second
        self._validate_time(self._hour, self._minute, new_second, self._microsecond)
        self._second = new_second
        return self

    def microsecond(
        self,
        new_microsecond: Optional[int] = None
    ) -> Union[int, "JalaliDate"]:
        """Get or set microsecond."""
        if new_microsecond is None:
            return self._microsecond
        self._validate_time(
            self._hour,
            self._minute,
            self._second,
            new_microsecond
        )
        self._microsecond = new_microsecond
        return self

    def tzinfo(
        self,
        new_tzinfo: Optional[tzinfo] = None
    ) -> Union[Optional[tzinfo], "JalaliDate"]:
        """Get or set timezone info."""
        if new_tzinfo is None:
            return self._tzinfo
        self._tzinfo = new_tzinfo
        return self

    def weekday(self) -> int:
        """Get day of week (0=Saturday, 6=Friday).

        Returns:
            Day of week as integer.
        """
        from parsidate.core.converters import jalali_to_gregorian
        gy, gm, gd = jalali_to_gregorian(self._year, self._month, self._day)
        from datetime import date
        greg_date = date(gy, gm, gd)
        py_weekday = greg_date.weekday()
        return (py_weekday + 2) % 7

    def quarter(self) -> int:
        """Get quarter of year (1-4)."""
        return (self._month - 1) // 3 + 1

    def day_of_year(self) -> int:
        """Get day number in year (1-365/366)."""
        from parsidate.utils.helpers import days_in_month as get_days_in_month
        days = 0
        for m in range(1, self._month):
            days += get_days_in_month(self._year, m, "jalali")
        return days + self._day

    def is_leap_year(self) -> bool:
        """Check if current year is leap year.

        Returns:
            True if leap year, False otherwise.
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
        """Add time periods to date.

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
        from parsidate.utils.helpers import days_in_month as get_days_in_month

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

        self._year = new_year
        self._month = new_month
        self._day = new_day

        self._day += days
        while self._day > get_days_in_month(self._year, self._month, "jalali"):
            self._day -= get_days_in_month(self._year, self._month, "jalali")
            self._month += 1
            if self._month > 12:
                self._month = 1
                self._year += 1

        while self._day < 1:
            self._month -= 1
            if self._month < 1:
                self._month = 12
                self._year -= 1
            self._day += get_days_in_month(self._year, self._month, "jalali")

        self._second += seconds
        self._minute += self._second // 60
        self._second %= 60

        self._minute += minutes
        self._hour += self._minute // 60
        self._minute %= 60

        self._hour += hours
        extra_days = self._hour // 24
        self._hour %= 24

        if extra_days > 0:
            self.add(days=extra_days)

        return self

    def sub(
        self,
        years: int = 0,
        months: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0
    ) -> "JalaliDate":
        """Subtract time periods from date.

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

    def format(self, pattern: str, locale: Literal["fa", "en"] = "en") -> str:
        """Format date according to pattern.

        Format codes:
            Y - 4-digit year (1403)
            y - 2-digit year (03)
            m - Month with leading zero (08)
            n - Month without leading zero (8)
            d - Day with leading zero (18)
            j - Day without leading zero (18)
            H - Hour 24-format with leading zero (14)
            i - Minute with leading zero (30)
            s - Second with leading zero (25)
            E - Full month name
            M - Short month name
            l - Full weekday name
            w - Weekday number (4)
            q - Quarter (3)
            L - Is leap year (0 or 1)

        Args:
            pattern: Format pattern string.
            locale: Locale for names ("fa" or "en").

        Returns:
            Formatted date string.
        """
        from parsidate.formatting.formatters import format_jalali_date
        return format_jalali_date(self, pattern, locale)

    def copy(self) -> "JalaliDate":
        """Create a copy of this date.

        Returns:
            New JalaliDate instance with same values.
        """
        return JalaliDate(
            self._year, self._month, self._day,
            self._hour, self._minute, self._second,
            self._microsecond, self._tzinfo
        )

    def __str__(self) -> str:
        """String representation."""
        return self.format("Y/m/d H:i:s", "en")

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"JalaliDate({self._year}, {self._month}, {self._day}, "
            f"{self._hour}, {self._minute}, {self._second})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, JalaliDate):
            return False
        return (
            self._year == other._year and
            self._month == other._month and
            self._day == other._day and
            self._hour == other._hour and
            self._minute == other._minute and
            self._second == other._second
        )

    def __lt__(self, other: "JalaliDate") -> bool:
        """Less than comparison."""
        if self._year != other._year:
            return self._year < other._year
        if self._month != other._month:
            return self._month < other._month
        if self._day != other._day:
            return self._day < other._day
        if self._hour != other._hour:
            return self._hour < other._hour
        if self._minute != other._minute:
            return self._minute < other._minute
        return self._second < other._second

    def __le__(self, other: "JalaliDate") -> bool:
        """Less than or equal comparison."""
        return self == other or self < other

    def __gt__(self, other: "JalaliDate") -> bool:
        """Greater than comparison."""
        return not self <= other

    def __ge__(self, other: "JalaliDate") -> bool:
        """Greater than or equal comparison."""
        return not self < other

    def __add__(self, other: Union["Period", "Duration"]) -> "JalaliDate":
        """Add Period or Duration to date."""
        from parsidate.intervals.period import Period
        from parsidate.intervals.duration import Duration

        new_date = self.copy()

        if isinstance(other, Period):
            new_date.add(
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
            new_date.add(
                days=days_to_add,
                hours=hours_to_add,
                minutes=minutes_to_add,
                seconds=seconds_to_add
            )

        return new_date

    def __sub__(
        self,
        other: Union["JalaliDate", "Period", "Duration"]
    ) -> Union["Duration", "JalaliDate"]:
        """Subtract date, Period, or Duration."""
        if isinstance(other, JalaliDate):
            from parsidate.intervals.duration import Duration
            days_diff = self.day_of_year() - other.day_of_year()
            years_diff = self._year - other._year
            days_diff += years_diff * 365
            return Duration(days=days_diff)
        else:
            from parsidate.intervals.period import Period
            from parsidate.intervals.duration import Duration

            new_date = self.copy()

            if isinstance(other, Period):
                new_date.sub(
                    years=other.years,
                    months=other.months,
                    days=other.days + other.weeks * 7
                )
            elif isinstance(other, Duration):
                total_seconds = other.total_seconds()
                days_to_sub = int(total_seconds // 86400)
                remaining = int(total_seconds % 86400)
                hours_to_sub = remaining // 3600
                remaining %= 3600
                minutes_to_sub = remaining // 60
                seconds_to_sub = remaining % 60
                new_date.sub(
                    days=days_to_sub,
                    hours=hours_to_sub,
                    minutes=minutes_to_sub,
                    seconds=seconds_to_sub
                )

            return new_date
