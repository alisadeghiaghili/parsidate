"""Period: calendar-unit time span for ParsiDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from typing import Union


class Period:
    """Immutable calendar period in years/months/weeks/days.

    Unlike :class:`~parsidate.intervals.duration.Duration`, a Period is
    calendar-relative: adding one month depends on the anchor date.

    Example:
        >>> Period(months=1).months
        1
        >>> Period(weeks=2).fixed_days()
        14
    """

    __slots__ = ("_years", "_months", "_weeks", "_days")

    def __init__(
        self,
        years: int = 0,
        months: int = 0,
        weeks: int = 0,
        days: int = 0,
    ) -> None:
        """Initialize a calendar period.

        Args:
            years: Whole years.
            months: Whole months (not reduced modulo 12).
            weeks: Whole weeks.
            days: Whole days.

        Example:
            >>> Period(years=1, months=2, days=5)
            Period(years=1, months=2, weeks=0, days=5)
        """
        object.__setattr__(self, "_years", int(years))
        object.__setattr__(self, "_months", int(months))
        object.__setattr__(self, "_weeks", int(weeks))
        object.__setattr__(self, "_days", int(days))

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"Period is immutable. Cannot set {name}")

    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"Period is immutable. Cannot delete {name}")

    @property
    def years(self) -> int:
        """Years component."""
        return self._years

    @property
    def months(self) -> int:
        """Months component."""
        return self._months

    @property
    def weeks(self) -> int:
        """Weeks component."""
        return self._weeks

    @property
    def days(self) -> int:
        """Days component."""
        return self._days

    def fixed_days(self) -> int:
        """Return only the calendar-fixed day span (weeks*7 + days).

        Months and years are excluded because their length depends on
        the anchor date.

        Returns:
            Whole days from weeks and days only.

        Example:
            >>> Period(weeks=1, days=3).fixed_days()
            10
        """
        return self._weeks * 7 + self._days

    def approx_days(
        self,
        days_per_month: int = 30,
        days_per_year: int = 365,
    ) -> int:
        """Return a rough day estimate for reporting only.

        Args:
            days_per_month: Assumed month length.
            days_per_year: Assumed year length.

        Returns:
            Approximate total days. Never use for exact arithmetic.

        Example:
            >>> Period(months=1).approx_days()
            30
        """
        return (
            self._years * days_per_year
            + self._months * days_per_month
            + self.fixed_days()
        )

    def __add__(self, other: "Period") -> "Period":
        """Combine two periods component-wise.

        Args:
            other: Period to add.

        Returns:
            New Period with summed components (not normalized).
        """
        if not isinstance(other, Period):
            return NotImplemented
        return Period(
            years=self._years + other.years,
            months=self._months + other.months,
            weeks=self._weeks + other.weeks,
            days=self._days + other.days,
        )

    def __sub__(self, other: "Period") -> "Period":
        """Subtract periods component-wise.

        Args:
            other: Period to subtract.

        Returns:
            New Period with differenced components.
        """
        if not isinstance(other, Period):
            return NotImplemented
        return Period(
            years=self._years - other.years,
            months=self._months - other.months,
            weeks=self._weeks - other.weeks,
            days=self._days - other.days,
        )

    def __neg__(self) -> "Period":
        """Negate all components.

        Returns:
            New Period with flipped signs.
        """
        return Period(
            years=-self._years,
            months=-self._months,
            weeks=-self._weeks,
            days=-self._days,
        )

    def __eq__(self, other: object) -> bool:
        """Component-wise equality."""
        if not isinstance(other, Period):
            return False
        return (
            self._years == other.years
            and self._months == other.months
            and self._weeks == other.weeks
            and self._days == other.days
        )

    def __hash__(self) -> int:
        """Hash all components."""
        return hash(("Period", self._years, self._months, self._weeks, self._days))

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Period(years={self._years}, months={self._months}, "
            f"weeks={self._weeks}, days={self._days})"
        )

    def __str__(self) -> str:
        """Compact human-readable form."""
        parts = []
        if self._years:
            parts.append(f"{self._years}y")
        if self._months:
            parts.append(f"{self._months}m")
        if self._weeks:
            parts.append(f"{self._weeks}w")
        if self._days:
            parts.append(f"{self._days}d")
        return " ".join(parts) if parts else "0d"


def years(n: int) -> Period:
    """Create a Period of ``n`` years.

    Args:
        n: Number of years.

    Returns:
        Period with years set.
    """
    return Period(years=n)


def months(n: int) -> Period:
    """Create a Period of ``n`` months.

    Args:
        n: Number of months.

    Returns:
        Period with months set.
    """
    return Period(months=n)


def weeks(n: int) -> Period:
    """Create a Period of ``n`` weeks.

    Args:
        n: Number of weeks.

    Returns:
        Period with weeks set.
    """
    return Period(weeks=n)


def days(n: int) -> Period:
    """Create a Period of ``n`` days.

    Args:
        n: Number of days.

    Returns:
        Period with days set.
    """
    return Period(days=n)


def period(**kwargs) -> Period:
    """Create a Period from keyword components.

    Args:
        **kwargs: ``years``, ``months``, ``weeks``, ``days``.

    Returns:
        Period built from the provided components.

    Example:
        >>> period(years=1, months=2, days=10).months
        2
    """
    return Period(**kwargs)
