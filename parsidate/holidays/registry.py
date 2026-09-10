"""HolidaySet value type and dataset errors.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from typing import Iterable, List, Optional, Sequence

from parsidate.core.jalali import JalaliDate

#: Version of the bundled official holiday tables.
DATA_VERSION = "2024.11.ir"


class HolidayDataMissing(LookupError):
    """Raised when a requested year is not covered by bundled holiday data."""


class HolidaySet:
    """Immutable set of holiday dates with membership and JSON payload support.

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> hs = HolidaySet(dates=[JalaliDate(1403, 1, 1)])
        >>> JalaliDate(1403, 1, 1) in hs
        True
    """

    __slots__ = ("_dates", "_keys")

    def __init__(self, dates: Optional[Iterable[JalaliDate]] = None) -> None:
        """Initialize a HolidaySet.

        Args:
            dates: Holiday dates. Duplicates are removed; order is not kept.

        Example:
            >>> HolidaySet().is_empty()
            True
        """
        unique = {(d.year(), d.month(), d.day()) for d in (dates or [])}
        ordered = [JalaliDate(y, m, d) for y, m, d in sorted(unique)]
        object.__setattr__(self, "_dates", tuple(ordered))
        object.__setattr__(self, "_keys", frozenset(unique))

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"HolidaySet is immutable. Cannot set {name}")

    @property
    def dates(self) -> tuple:
        """Return sorted unique holiday dates.

        Returns:
            Tuple of :class:`~parsidate.core.jalali.JalaliDate`.
        """
        return self._dates

    def is_empty(self) -> bool:
        """Return whether this set has no holidays.

        Returns:
            ``True`` if empty.
        """
        return not self._dates

    def years(self) -> List[int]:
        """Return distinct Jalali years present in the set.

        Returns:
            Sorted list of years.
        """
        return sorted({d.year() for d in self._dates})

    def in_year(self, year: int) -> List[JalaliDate]:
        """Return holidays that fall in a Jalali year.

        Args:
            year: Jalali year.

        Returns:
            Dates in that year (possibly empty).
        """
        return [d for d in self._dates if d.year() == year]

    def __contains__(self, date: JalaliDate) -> bool:
        """Return whether a date is a holiday."""
        return (date.year(), date.month(), date.day()) in self._keys

    def __iter__(self):
        """Iterate holiday dates."""
        return iter(self._dates)

    def __len__(self) -> int:
        """Return number of holidays."""
        return len(self._dates)

    def __or__(self, other: "HolidaySet") -> "HolidaySet":
        """Return union of two holiday sets."""
        if not isinstance(other, HolidaySet):
            return NotImplemented
        return HolidaySet(list(self._dates) + list(other._dates))

    def __eq__(self, other: object) -> bool:
        """Compare by date membership."""
        if not isinstance(other, HolidaySet):
            return False
        return set(self._dates) == set(other._dates)

    def __hash__(self) -> int:
        """Hash by date keys."""
        return hash(
            ("HolidaySet", tuple(sorted((d.year(), d.month(), d.day()) for d in self._dates)))
        )

    def __repr__(self) -> str:
        """Developer representation."""
        return f"HolidaySet({len(self._dates)} holidays)"

    def to_payload(self) -> dict:
        """Serialize to a JSON-friendly dict.

        Returns:
            Dict with ``data_version`` and ISO-like ``YYYY/MM/DD`` strings.

        Example:
            >>> HolidaySet(dates=[JalaliDate(1403, 1, 1)])["dates"]  # doctest: +SKIP
        """
        return {
            "data_version": DATA_VERSION,
            "dates": [f"{d.year():04d}/{d.month():02d}/{d.day():02d}" for d in self._dates],
        }

    @classmethod
    def from_payload(cls, payload: dict) -> "HolidaySet":
        """Deserialize from :meth:`to_payload` output.

        Args:
            payload: Dict with a ``dates`` list of ``YYYY/MM/DD`` strings.

        Returns:
            Reconstructed HolidaySet.

        Raises:
            ValueError: If a date string is malformed.
        """
        dates: List[JalaliDate] = []
        for raw in payload.get("dates", []):
            parts = str(raw).split("/")
            if len(parts) != 3:
                raise ValueError(f"Invalid holiday date: {raw!r}")
            y, m, d = (int(p) for p in parts)
            dates.append(JalaliDate(y, m, d))
        return cls(dates=dates)
