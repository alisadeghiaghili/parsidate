"""HijriDate: tabular (civil arithmetic) Islamic calendar date.

Calendar basis
--------------
This module implements the **tabular Islamic calendar** (30-year
leap cycle). It is *not* Umm al-Qura observational data and *not*
the official Iranian announcement of religious holidays.

Expected accuracy: **±1 day** versus official Umm al-Qura or
state-published dates. For Iranian official holidays use
:mod:`parsidate.holidays` (published Jalali dates).

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from datetime import date, tzinfo
from typing import Optional

__all__ = ["HijriDate"]

# JDN of 1 Muharram 1 AH (civil epoch used by this implementation)
_HIJRI_EPOCH_JDN = 1948439

_MONTH_DAYS = (30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29)

_MONTHS_EN = (
    "Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani",
    "Jumada al-awwal", "Jumada al-thani", "Rajab", "Sha'ban",
    "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah",
)
_MONTHS_FA = (
    "محرم", "صفر", "ربیع‌الاول", "ربیع‌الثانی",
    "جمادی‌الاول", "جمادی‌الثانی", "رجب", "شعبان",
    "رمضان", "شوال", "ذی‌القعده", "ذی‌الحجه",
)


def _is_leap(year: int) -> bool:
    """Return whether a Hijri year is leap in the tabular cycle."""
    return (11 * year + 14) % 30 < 11


def _days_in_month(year: int, month: int) -> int:
    if month == 12 and _is_leap(year):
        return 30
    return _MONTH_DAYS[month - 1]


def _hijri_to_jdn(year: int, month: int, day: int) -> int:
    """JDN for a tabular Hijri date (civil algorithm)."""
    months_before = 0
    for m in range(1, month):
        months_before += _days_in_month(year, m)
    y = year - 1
    return (
        _HIJRI_EPOCH_JDN
        + y * 354
        + (3 + 11 * year) // 30
        + months_before
        + day
    )


def _jdn_to_hijri(jdn: int):
    days = jdn - _HIJRI_EPOCH_JDN
    # year estimate then correct
    year = (days * 30 + 10646) // 10631
    # days before this year
    before = (year - 1) * 354 + (3 + 11 * year) // 30
    remain = days - before
    while remain < 1:
        year -= 1
        before = (year - 1) * 354 + (3 + 11 * year) // 30
        remain = days - before
    month = 1
    while month < 12 and remain > _days_in_month(year, month):
        remain -= _days_in_month(year, month)
        month += 1
    return year, month, remain


def _gregorian_to_jdn(gy: int, gm: int, gd: int) -> int:
    return date(gy, gm, gd).toordinal() - date(1, 1, 1).toordinal() + 1721426


def _jdn_to_gregorian(jdn: int):
    # Python ordinal = jdn - 1721425 for 0001-01-01?
    # date(1,1,1).toordinal() == 1 → jdn(1,1,1) = 1721426
    ordinal = jdn - 1721425
    d = date.fromordinal(ordinal)
    return d.year, d.month, d.day


class HijriDate:
    """Immutable tabular (civil) Hijri calendar date.

    **Not observational.** Suitable for civil I/O and approximate
    cross-calendar work; official Iranian holidays live in
    :mod:`parsidate.holidays`. Accuracy typically ±1 day vs Umm al-Qura.

    Example:
        >>> h = HijriDate(1446, 1, 10)
        >>> h.month_name("en")
        "Muharram"
    """

    __slots__ = ("_year", "_month", "_day")

    def __init__(self, year: int, month: int, day: int) -> None:
        """Initialize a HijriDate.

        Args:
            year: Hijri year (AH).
            month: Month 1-12.
            day: Day 1-29/30 depending on month and leap year.

        Raises:
            ValueError: If a component is out of range.
        """
        if not 1 <= month <= 12:
            raise ValueError(f"Month must be 1-12, got {month}")
        max_d = _days_in_month(year, month)
        if not 1 <= day <= max_d:
            raise ValueError(f"Day must be 1-{max_d} for {year}/{month}, got {day}")
        object.__setattr__(self, "_year", int(year))
        object.__setattr__(self, "_month", int(month))
        object.__setattr__(self, "_day", int(day))

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"HijriDate is immutable. Cannot set {name}")

    def year(self) -> int:
        """Return Hijri year."""
        return self._year

    def month(self) -> int:
        """Return month 1-12."""
        return self._month

    def day(self) -> int:
        """Return day of month."""
        return self._day

    def is_leap_year(self) -> bool:
        """Return whether this Hijri year is tabular-leap."""
        return _is_leap(self._year)

    def month_name(self, locale: str = "en") -> str:
        """Return the month name.

        Args:
            locale: ``\"en\"`` or ``\"fa\"``.

        Returns:
            Localized month name.

        Example:
            >>> HijriDate(1446, 9, 1).month_name("en")
            'Ramadan'
        """
        return _MONTHS_FA[self._month - 1] if locale == "fa" else _MONTHS_EN[self._month - 1]

    def to_jdn(self) -> int:
        """Return Julian Day Number for this tabular date."""
        return _hijri_to_jdn(self._year, self._month, self._day)

    def to_gregorian(self):
        """Convert to Gregorian (Y, M, D).

        Returns:
            Tuple of Gregorian year, month, day.
        """
        return _jdn_to_gregorian(self.to_jdn())

    def to_jalali(self):
        """Convert to Jalali (Y, M, D).

        Returns:
            Tuple of Jalali year, month, day.
        """
        from parsidate.core.converters import gregorian_to_jalali

        return gregorian_to_jalali(*self.to_gregorian())

    @classmethod
    def from_gregorian(cls, g) -> "HijriDate":
        """Build from a GregorianDate or (y, m, d).

        Args:
            g: GregorianDate or 3-tuple.

        Returns:
            HijriDate.
        """
        if hasattr(g, "year"):
            y, m, d = g.year(), g.month(), g.day()
        else:
            y, m, d = g
        hy, hm, hd = _jdn_to_hijri(_gregorian_to_jdn(y, m, d))
        return cls(hy, hm, hd)

    @classmethod
    def from_jalali(cls, j) -> "HijriDate":
        """Build from a JalaliDate.

        Args:
            j: JalaliDate.

        Returns:
            HijriDate.
        """
        return cls.from_gregorian(j.to_gregorian())

    def add(self, days: int = 0, months: int = 0, years: int = 0) -> "HijriDate":
        """Return a new date shifted by calendar units.

        Args:
            days: Days to add.
            months: Months to add (calendar, not 30-day months).
            years: Years to add.

        Returns:
            New HijriDate.
        """
        y, m, d = self._year + years, self._month, self._day
        m += months
        while m > 12:
            m -= 12
            y += 1
        while m < 1:
            m += 12
            y -= 1
        d = min(d, _days_in_month(y, m))
        jdn = _hijri_to_jdn(y, m, d) + days
        return HijriDate(*_jdn_to_hijri(jdn))

    def replace(self, year=None, month=None, day=None) -> "HijriDate":
        """Return a new date with fields replaced."""
        y = self._year if year is None else year
        m = self._month if month is None else month
        d = self._day if day is None else day
        return HijriDate(y, m, d)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HijriDate):
            return False
        return (self._year, self._month, self._day) == (other._year, other._month, other._day)

    def __hash__(self) -> int:
        return hash(("HijriDate", self._year, self._month, self._day))

    def __lt__(self, other: "HijriDate") -> bool:
        return self.to_jdn() < other.to_jdn()

    def __le__(self, other: "HijriDate") -> bool:
        return self.to_jdn() <= other.to_jdn()

    def __gt__(self, other: "HijriDate") -> bool:
        return self.to_jdn() > other.to_jdn()

    def __ge__(self, other: "HijriDate") -> bool:
        return self.to_jdn() >= other.to_jdn()

    def __repr__(self) -> str:
        return f"HijriDate({self._year}, {self._month}, {self._day})"

    def __str__(self) -> str:
        return f"{self._year:04d}-{self._month:02d}-{self._day:02d}"
