"""HolidayCalendar: official + custom company/holiday days.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from typing import Any, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

from parsidate.core.jalali import JalaliDate
from parsidate.holidays.ir import IRAN_DEFAULT_WEEKEND, iran_holidays
from parsidate.holidays.registry import HolidaySet

DateLike = Union[JalaliDate, str]
HolidayInput = Union[HolidaySet, Iterable[DateLike], None]

__all__ = ["HolidayCalendar"]


def _parse_date(value: DateLike) -> JalaliDate:
    if isinstance(value, JalaliDate):
        return value
    from parsidate.parsers import jmd

    return jmd(str(value))


def _to_holiday_set(holidays: HolidayInput) -> HolidaySet:
    if holidays is None:
        return HolidaySet()
    if isinstance(holidays, HolidaySet):
        return holidays
    return HolidaySet(dates=[_parse_date(h) for h in holidays])


class HolidayCalendar:
    """Immutable calendar with weekend rules and layered holidays.

    Layers:

    1. **Base** — typically official Iranian holidays
    2. **Custom** — company closures, plant shutdowns, personal days

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> cal = HolidayCalendar.ir(years=[1403]).add_holidays(["1403/08/18"])
        >>> cal.is_holiday(JalaliDate(1403, 8, 18))
        True
        >>> cal.is_business_day(JalaliDate(1403, 8, 18))
        False
    """

    __slots__ = ("_weekend", "_base", "_custom", "_labels")

    def __init__(
        self,
        holidays: HolidayInput = None,
        weekend: Optional[Sequence[int]] = None,
        base_holidays: HolidayInput = None,
    ) -> None:
        """Initialize a calendar.

        Args:
            holidays: Custom holiday dates or strings (``1403/08/18``).
            weekend: Weekday indices (Jalali: 0=Sat … 6=Fri). Default Friday.
            base_holidays: Lower-layer holidays (e.g. official set).

        Example:
            >>> HolidayCalendar().weekend
            (6,)
        """
        custom = _to_holiday_set(holidays)
        base = _to_holiday_set(base_holidays)
        object.__setattr__(self, "_weekend", tuple(weekend) if weekend is not None else IRAN_DEFAULT_WEEKEND)
        object.__setattr__(self, "_base", base)
        object.__setattr__(self, "_custom", custom)
        object.__setattr__(self, "_labels", {})

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"HolidayCalendar is immutable. Cannot set {name}")

    @classmethod
    def ir(
        cls,
        years: Optional[Iterable[int]] = None,
        weekend: Optional[Sequence[int]] = None,
    ) -> "HolidayCalendar":
        """Official Iranian holidays for the given Jalali years.

        Args:
            years: Jalali years to load (default: current civil range hint
                is the caller's responsibility — pass explicitly).
            weekend: Optional weekend override.

        Returns:
            Calendar with official base holidays.

        Example:
            >>> HolidayCalendar.ir(years=[1403]).is_holiday(
            ...     __import__("parsidate").JalaliDate(1403, 1, 1)
            ... )
            True
        """
        acc = HolidaySet()
        for y in years or ():
            acc = acc | iran_holidays(y)
        return cls(base_holidays=acc, weekend=weekend)

    @property
    def weekend(self) -> Tuple[int, ...]:
        """Weekend weekday indices."""
        return self._weekend

    @property
    def holidays(self) -> HolidaySet:
        """Union of base and custom holidays."""
        return self._base | self._custom

    @property
    def custom_holidays(self) -> HolidaySet:
        """Only custom (non-base) holidays."""
        return self._custom

    def with_holidays(
        self,
        dates: Iterable[DateLike],
        label: str = "custom",
    ) -> "HolidayCalendar":
        """Return a new calendar with additional labeled holidays.

        Args:
            dates: JalaliDate instances or ``YYYY/MM/DD`` strings
                (Persian digits accepted).
            label: Name stored for dim_date / queries.

        Returns:
            New HolidayCalendar.

        Example:
            >>> cal = HolidayCalendar().with_holidays(["1403/08/18"], label="plant")
            >>> cal.holiday_name(
            ...     __import__("parsidate").JalaliDate(1403, 8, 18)
            ... )
            'plant'
        """
        new_custom = self._custom | _to_holiday_set(dates)
        cal = HolidayCalendar(
            holidays=new_custom,
            weekend=self._weekend,
            base_holidays=self._base,
        )
        labels = dict(self._labels)
        parsed = _to_holiday_set(dates)
        for d in parsed:
            labels[(d.year(), d.month(), d.day())] = label
        object.__setattr__(cal, "_labels", labels)
        return cal

    def add_holidays(self, dates: Iterable[DateLike], label: str = "custom") -> "HolidayCalendar":
        """Alias of :meth:`with_holidays`."""
        return self.with_holidays(dates, label=label)

    def is_holiday(self, date: JalaliDate) -> bool:
        """Return whether the date is a holiday in this calendar."""
        return date in self.holidays

    def holiday_name(self, date: JalaliDate) -> str:
        """Return the custom label for a date, or ``\"official\"`` / ``\"\"``."""
        key = (date.year(), date.month(), date.day())
        if key in self._labels:
            return self._labels[key]
        if date in self._custom:
            return "custom"
        if date in self._base:
            return "official"
        return ""

    def is_weekend(self, date: JalaliDate) -> bool:
        """Return whether the date falls on a weekend weekday."""
        return date.weekday() in self._weekend

    def is_business_day(self, date: JalaliDate) -> bool:
        """Return whether the date is a business day under this calendar."""
        return not self.is_weekend(date) and not self.is_holiday(date)

    def networkdays(self, start: JalaliDate, end: JalaliDate, inclusive_end: bool = True) -> int:
        """Count business days between dates using this calendar."""
        if end < start:
            return 0
        count = 0
        current = start.copy()
        while current < end or current == end:
            if current == end and not inclusive_end:
                break
            if self.is_business_day(current):
                count += 1
            if current == end:
                break
            current = current.add(days=1)
        return count

    def add_business_days(self, date: JalaliDate, n: int) -> JalaliDate:
        """Add ``n`` business days (Excel WORKDAY-like stepping)."""
        if n == 0:
            return date.copy()
        step = 1 if n > 0 else -1
        remaining = abs(n)
        current = date.copy()
        while remaining > 0:
            current = current.add(days=step)
            if self.is_business_day(current):
                remaining -= 1
        return current

    def to_payload(self) -> dict:
        """Serialize for JSON storage (warehouse / config files)."""
        return {
            "weekend": list(self._weekend),
            "base": self._base.to_payload(),
            "custom": self._custom.to_payload(),
            "labels": {
                f"{y:04d}/{m:02d}/{d:02d}": label
                for (y, m, d), label in self._labels.items()
            },
        }

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "HolidayCalendar":
        """Deserialize from :meth:`to_payload`."""
        cal = cls(
            holidays=HolidaySet.from_payload(payload.get("custom", {"dates": []})),
            weekend=tuple(payload.get("weekend", IRAN_DEFAULT_WEEKEND)),
            base_holidays=HolidaySet.from_payload(payload.get("base", {"dates": []})),
        )
        labels = {}
        for raw, label in payload.get("labels", {}).items():
            y, m, d = (int(p) for p in str(raw).split("/"))
            labels[(y, m, d)] = label
        object.__setattr__(cal, "_labels", labels)
        return cal

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HolidayCalendar):
            return False
        return (
            self._weekend == other._weekend
            and self._base == other._base
            and self._custom == other._custom
        )

    def __hash__(self) -> int:
        return hash(("HolidayCalendar", self._weekend, self._base, self._custom))

    def __repr__(self) -> str:
        return (
            f"HolidayCalendar(weekend={self._weekend}, "
            f"base={len(self._base)}, custom={len(self._custom)})"
        )
