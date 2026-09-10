"""GregorianDate: immutable Gregorian calendar date/time class.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from datetime import datetime, timedelta, tzinfo, timezone
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from parsidate.intervals.period import Period
    from parsidate.intervals.duration import Duration


class GregorianDate:
    """Immutable Gregorian calendar date and time.

    All mutating operations (``add``, ``sub``, ``replace``) return a new
    instance. Getters take no arguments and never change state.

    Attributes:
        year: Gregorian year (via ``year()``).
        month: Gregorian month 1-12 (via ``month()``).
        day: Day of month 1-31 (via ``day()``).
        hour: Hour 0-23 (via ``hour()``).
        minute: Minute 0-59 (via ``minute()``).
        second: Second 0-59 (via ``second()``).
        microsecond: Microsecond 0-999999 (via ``microsecond()``).
        tzinfo: Optional timezone (via ``tzinfo()``).

    Example:
        >>> d = GregorianDate(2024, 11, 8, 14, 30)
        >>> d.add(days=1).day()
        9
        >>> d.day()
        8
    """

    __slots__ = ("_dt",)

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: Optional[tzinfo] = None,
    ) -> None:
        """Initialize an immutable GregorianDate.

        Args:
            year: Gregorian year.
            month: Month (1-12).
            day: Day of month (1-31).
            hour: Hour (0-23).
            minute: Minute (0-59).
            second: Second (0-59).
            microsecond: Microsecond (0-999999).
            tzinfo: Optional timezone.

        Raises:
            ValueError: If any component is out of range.
        """
        self._dt = datetime(year, month, day, hour, minute, second, microsecond, tzinfo)

    def __setattr__(self, name: str, value: object) -> None:
        """Allow only construction-time assignment of ``_dt``."""
        if name == "_dt" and not hasattr(self, "_dt"):
            object.__setattr__(self, name, value)
            return
        raise AttributeError(f"GregorianDate is immutable. Cannot set {name}")

    def __delattr__(self, name: str) -> None:
        """Prevent deletion of attributes."""
        raise AttributeError(f"GregorianDate is immutable. Cannot delete {name}")

    def year(self) -> int:
        """Return the Gregorian year.

        Returns:
            Year as an integer.

        Example:
            >>> GregorianDate(2024, 11, 8).year()
            2024
        """
        return self._dt.year

    def month(self) -> int:
        """Return the month (1-12).

        Returns:
            Month number.

        Example:
            >>> GregorianDate(2024, 11, 8).month()
            11
        """
        return self._dt.month

    def day(self) -> int:
        """Return the day of month (1-31).

        Returns:
            Day of month.

        Example:
            >>> GregorianDate(2024, 11, 8).day()
            8
        """
        return self._dt.day

    def hour(self) -> int:
        """Return the hour (0-23).

        Returns:
            Hour component.

        Example:
            >>> GregorianDate(2024, 11, 8, 14).hour()
            14
        """
        return self._dt.hour

    def minute(self) -> int:
        """Return the minute (0-59).

        Returns:
            Minute component.

        Example:
            >>> GregorianDate(2024, 11, 8, 14, 30).minute()
            30
        """
        return self._dt.minute

    def second(self) -> int:
        """Return the second (0-59).

        Returns:
            Second component.

        Example:
            >>> GregorianDate(2024, 11, 8, 14, 30, 45).second()
            45
        """
        return self._dt.second

    def microsecond(self) -> int:
        """Return the microsecond (0-999999).

        Returns:
            Microsecond component.

        Example:
            >>> GregorianDate(2024, 11, 8, 14, 30, 45, 1).microsecond()
            1
        """
        return self._dt.microsecond

    def tzinfo(self) -> Optional[tzinfo]:
        """Return attached timezone info, if any.

        Returns:
            ``tzinfo`` or ``None`` when naive.

        Example:
            >>> GregorianDate(2024, 11, 8).tzinfo() is None
            True
        """
        return self._dt.tzinfo

    def weekday(self) -> int:
        """Return Python weekday (0=Monday .. 6=Sunday).

        Returns:
            Weekday index compatible with ``datetime.date.weekday``.

        Example:
            >>> GregorianDate(2024, 11, 8).weekday()
            4
        """
        return self._dt.weekday()

    def quarter(self) -> int:
        """Return calendar quarter (1-4).

        Returns:
            Quarter number.

        Example:
            >>> GregorianDate(2024, 4, 1).quarter()
            2
        """
        return (self._dt.month - 1) // 3 + 1

    def day_of_year(self) -> int:
        """Return day of year (1-366).

        Returns:
            Ordinal day within the year.

        Example:
            >>> GregorianDate(2024, 1, 1).day_of_year()
            1
        """
        return self._dt.timetuple().tm_yday

    def is_leap_year(self) -> bool:
        """Return whether the current year is a Gregorian leap year.

        Returns:
            ``True`` if leap, otherwise ``False``.

        Example:
            >>> GregorianDate(2020, 1, 1).is_leap_year()
            True
        """
        year = self._dt.year
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def replace(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        microsecond: Optional[int] = None,
        tzinfo: Optional[tzinfo] = None,
    ) -> "GregorianDate":
        """Return a new GregorianDate with selected fields replaced.

        Args:
            year: Replacement year.
            month: Replacement month.
            day: Replacement day.
            hour: Replacement hour.
            minute: Replacement minute.
            second: Replacement second.
            microsecond: Replacement microsecond.
            tzinfo: Replacement timezone. ``None`` keeps the current zone.

        Returns:
            New ``GregorianDate`` instance.

        Example:
            >>> GregorianDate(2024, 1, 1).replace(year=2025).year()
            2025
        """
        return GregorianDate(
            year if year is not None else self._dt.year,
            month if month is not None else self._dt.month,
            day if day is not None else self._dt.day,
            hour if hour is not None else self._dt.hour,
            minute if minute is not None else self._dt.minute,
            second if second is not None else self._dt.second,
            microsecond if microsecond is not None else self._dt.microsecond,
            tzinfo if tzinfo is not None else self._dt.tzinfo,
        )

    def strftime(self, pattern: str, locale: str = "en") -> str:
        """Format using standard ``strftime`` format codes.

        Args:
            pattern: Format string with codes such as ``%Y``, ``%m``, ``%d``.
            locale: ``\"fa\"`` or ``\"en\"``.

        Returns:
            Formatted date string.

        Example:
            >>> GregorianDate(2024, 11, 8).strftime("%Y-%m-%d")
            '2024-11-08'
        """
        from parsidate.formatting.formatters import format_gregorian_date

        return format_gregorian_date(self, pattern, locale)

    def format(self, pattern: str, locale: str = "en") -> str:
        """Alias of :meth:`strftime`.

        Args:
            pattern: ``strftime`` format string.
            locale: ``\"fa\"`` or ``\"en\"``.

        Returns:
            Formatted date string.

        Example:
            >>> GregorianDate(2024, 11, 8).format("%Y/%m/%d")
            '2024/11/08'
        """
        return self.strftime(pattern, locale)

    def copy(self) -> "GregorianDate":
        """Return an equal instance (kept for API symmetry).

        Returns:
            New ``GregorianDate`` equal to this one.

        Example:
            >>> GregorianDate(2024, 1, 1).copy() == GregorianDate(2024, 1, 1)
            True
        """
        return GregorianDate(
            self._dt.year,
            self._dt.month,
            self._dt.day,
            self._dt.hour,
            self._dt.minute,
            self._dt.second,
            self._dt.microsecond,
            self._dt.tzinfo,
        )

    def to_datetime(self) -> datetime:
        """Return the underlying ``datetime.datetime``.

        Returns:
            The wrapped datetime object.

        Example:
            >>> GregorianDate(2024, 1, 1).to_datetime().year
            2024
        """
        return self._dt

    def isoformat(self, sep: str = "T", timespec: str = "auto") -> str:
        """Return ISO-8601 string for the wrapped datetime.

        Args:
            sep: Date/time separator.
            timespec: Passed through to ``datetime.isoformat``.

        Returns:
            ISO-8601 string.

        Example:
            >>> GregorianDate(2024, 11, 8).isoformat()
            '2024-11-08T00:00:00'
        """
        return self._dt.isoformat(sep=sep, timespec=timespec)

    @classmethod
    def fromisoformat(cls, value: str) -> "GregorianDate":
        """Parse an ISO-8601 string.

        Args:
            value: ISO-8601 datetime/date string.

        Returns:
            Parsed GregorianDate.

        Example:
            >>> GregorianDate.fromisoformat("2024-11-08").day()
            8
        """
        dt = datetime.fromisoformat(value)
        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            dt.tzinfo,
        )

    @classmethod
    def from_datetime(cls, dt: datetime) -> "GregorianDate":
        """Build from a ``datetime``.

        Args:
            dt: Source datetime.

        Returns:
            Wrapped GregorianDate.

        Example:
            >>> from datetime import datetime
            >>> GregorianDate.from_datetime(datetime(2024, 1, 1)).year()
            2024
        """
        return cls(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo
        )

    @classmethod
    def fromtimestamp(cls, ts: float, tz=None) -> "GregorianDate":
        """Build from a POSIX timestamp.

        Args:
            ts: Seconds since epoch.
            tz: Optional timezone.

        Returns:
            GregorianDate.

        Example:
            >>> GregorianDate.fromtimestamp(0, tz=timezone.utc).year()
            1970
        """
        dt = datetime.fromtimestamp(ts, tz=tz) if tz is not None else datetime.fromtimestamp(ts)
        return cls.from_datetime(dt)

    def timestamp(self) -> float:
        """Return POSIX timestamp.

        Naive values are treated as UTC.

        Returns:
            Seconds since epoch.

        Example:
            >>> GregorianDate(1970, 1, 1, tzinfo=timezone.utc).timestamp()
            0.0
        """
        if self._dt.tzinfo is None:
            return self._dt.replace(tzinfo=timezone.utc).timestamp()
        return self._dt.timestamp()

    def add(
        self,
        years: int = 0,
        months: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
    ) -> "GregorianDate":
        """Return a new date with calendar/time units added.

        Month/year addition clamps the day to the target month length
        (e.g. Jan 31 + 1 month -> Feb 28/29). Time units use exact
        elapsed seconds via ``timedelta``.

        Args:
            years: Years to add.
            months: Months to add.
            days: Days to add.
            hours: Hours to add.
            minutes: Minutes to add.
            seconds: Seconds to add.

        Returns:
            New ``GregorianDate``.

        Example:
            >>> GregorianDate(2024, 1, 15).add(months=1).month()
            2
        """
        from parsidate.utils.helpers import days_in_month

        new_year = self._dt.year + years
        new_month = self._dt.month + months

        while new_month > 12:
            new_month -= 12
            new_year += 1
        while new_month < 1:
            new_month += 12
            new_year -= 1

        max_day = days_in_month(new_year, new_month, "gregorian")
        new_day = min(self._dt.day, max_day)

        result = GregorianDate(
            new_year,
            new_month,
            new_day,
            self._dt.hour,
            self._dt.minute,
            self._dt.second,
            self._dt.microsecond,
            self._dt.tzinfo,
        )

        extra_time = days * 86400 + hours * 3600 + minutes * 60 + seconds
        if extra_time:
            shifted = result._dt + timedelta(seconds=extra_time)
            result = GregorianDate(
                shifted.year,
                shifted.month,
                shifted.day,
                shifted.hour,
                shifted.minute,
                shifted.second,
                shifted.microsecond,
                shifted.tzinfo,
            )
        return result

    def sub(
        self,
        years: int = 0,
        months: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
    ) -> "GregorianDate":
        """Return a new date with calendar/time units subtracted.

        Args:
            years: Years to subtract.
            months: Months to subtract.
            days: Days to subtract.
            hours: Hours to subtract.
            minutes: Minutes to subtract.
            seconds: Seconds to subtract.

        Returns:
            New ``GregorianDate``.

        Example:
            >>> GregorianDate(2024, 3, 1).sub(months=1).month()
            2
        """
        return self.add(
            years=-years,
            months=-months,
            days=-days,
            hours=-hours,
            minutes=-minutes,
            seconds=-seconds,
        )

    def __str__(self) -> str:
        """ISO-like string representation."""
        return self._dt.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"GregorianDate({self._dt.year}, {self._dt.month}, {self._dt.day}, "
            f"{self._dt.hour}, {self._dt.minute}, {self._dt.second})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality including microseconds."""
        if not isinstance(other, GregorianDate):
            return False
        return self._dt == other._dt

    def __hash__(self) -> int:
        """Hash using the underlying datetime."""
        return hash(self._dt)

    def __lt__(self, other: "GregorianDate") -> bool:
        """Less than comparison."""
        return self._dt < other._dt

    def __le__(self, other: "GregorianDate") -> bool:
        """Less than or equal."""
        return self._dt <= other._dt

    def __gt__(self, other: "GregorianDate") -> bool:
        """Greater than."""
        return self._dt > other._dt

    def __ge__(self, other: "GregorianDate") -> bool:
        """Greater than or equal."""
        return self._dt >= other._dt

    def __add__(self, other: Union["Period", "Duration"]) -> "GregorianDate":
        """Add a Period or Duration. Returns a new instance.

        Args:
            other: ``Period`` or ``Duration`` to add.

        Returns:
            New ``GregorianDate``.

        Example:
            >>> from parsidate.intervals.period import Period
            >>> GregorianDate(2024, 1, 1) + Period(months=1)
            GregorianDate(2024, 2, 1, 0, 0, 0)
        """
        from parsidate.intervals.period import Period
        from parsidate.intervals.duration import Duration

        if isinstance(other, Period):
            return self.add(
                years=other.years,
                months=other.months,
                days=other.days + other.weeks * 7,
            )
        if isinstance(other, Duration):
            return self.add(seconds=other.total_seconds())
        return NotImplemented

    def __sub__(
        self,
        other: Union["GregorianDate", "Period", "Duration"],
    ) -> Union["Duration", "GregorianDate"]:
        """Subtract a date, Period, or Duration.

        Args:
            other: Value to subtract.

        Returns:
            ``Duration`` when subtracting dates, otherwise a new date.

        Example:
            >>> (GregorianDate(2024, 1, 10) - GregorianDate(2024, 1, 1)).days()
            9
        """
        from parsidate.intervals.period import Period
        from parsidate.intervals.duration import Duration

        if isinstance(other, GregorianDate):
            return Duration(seconds=(self._dt - other._dt).total_seconds())
        if isinstance(other, Period):
            return self.sub(
                years=other.years,
                months=other.months,
                days=other.days + other.weeks * 7,
            )
        if isinstance(other, Duration):
            return self.add(seconds=-other.total_seconds())
        return NotImplemented
