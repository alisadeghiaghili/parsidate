"""
Period: Calendar-based time interval class for ParsiDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from typing import Optional

class Period:
    """
    Represents a calendar period (years, months, weeks, days).

    Unlike Duration, a Period is measured in calendar units.
    Useful for adding/subtracting calendar time (months, years, etc).

    Examples:
        Period(years=1) + Period(months=2, days=5)
        JalaliDate(...) + Period(months=1)
    """

    def __init__(
        self,
        years: int = 0,
        months: int = 0,
        weeks: int = 0,
        days: int = 0
    ):
        """
        Initialize Period.

        Args:
            years: Number of years.
            months: Number of months.
            weeks: Number of weeks.
            days: Number of days.
        """
        self.years = years
        self.months = months
        self.weeks = weeks
        self.days = days

    def total_days(self) -> int:
        """Approximate total days (weeks*7 + days, months and years ignored)."""
        return self.weeks * 7 + self.days

    def __add__(self, other: "Period") -> "Period":
        """Combine two periods."""
        return Period(
            years=self.years + other.years,
            months=self.months + other.months,
            weeks=self.weeks + other.weeks,
            days=self.days + other.days
        )

    def __sub__(self, other: "Period") -> "Period":
        """Subtract period from another."""
        return Period(
            years=self.years - other.years,
            months=self.months - other.months,
            weeks=self.weeks - other.weeks,
            days=self.days - other.days
        )

    def __neg__(self) -> "Period":
        """Negate period."""
        return Period(
            years=-self.years,
            months=-self.months,
            weeks=-self.weeks,
            days=-self.days
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Period):
            return False
        return (self.years == other.years and
                self.months == other.months and
                self.weeks == other.weeks and
                self.days == other.days)

    def __repr__(self) -> str:
        return (f"Period(years={self.years}, months={self.months}, "
                f"weeks={self.weeks}, days={self.days})")

    def __str__(self) -> str:
        parts = []
        if self.years: parts.append(f"{self.years}y")
        if self.months: parts.append(f"{self.months}m")
        if self.weeks: parts.append(f"{self.weeks}w")
        if self.days: parts.append(f"{self.days}d")
        return " ".join(parts) if parts else "0d"

# SHORTCUT FACTORY FUNCTIONS

def years(n: int) -> Period:
    """Create a Period of n years."""
    return Period(years=n)

def months(n: int) -> Period:
    """Create a Period of n months."""
    return Period(months=n)

def weeks(n: int) -> Period:
    """Create a Period of n weeks."""
    return Period(weeks=n)

def days(n: int) -> Period:
    """Create a Period of n days."""
    return Period(days=n)

def period(**kwargs) -> Period:
    """
    Create a Period object using keyword arguments.

    Args:
        years: Number of years
        months: Number of months
        weeks: Number of weeks
        days: Number of days

    Returns:
        Period object

    Example:
        period(years=1, months=2, days=10)
    """
    return Period(**kwargs)
