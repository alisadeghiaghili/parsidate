"""Duration: exact time-span value object for ParsiDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from functools import total_ordering
from typing import Union


@total_ordering
class Duration:
    """Immutable exact time span stored in integer microseconds.

    Unlike :class:`~parsidate.intervals.period.Period`, a ``Duration``
    is calendar-independent (1 hour is always 3600 seconds).

    Example:
        >>> Duration(hours=1).total_seconds()
        3600.0
        >>> Duration(hours=1) < Duration(hours=2)
        True
    """

    __slots__ = ("_us",)

    def __init__(
        self,
        days: Union[int, float] = 0,
        hours: Union[int, float] = 0,
        minutes: Union[int, float] = 0,
        seconds: Union[int, float] = 0,
        microseconds: Union[int, float] = 0,
    ) -> None:
        """Initialize a Duration from unit parts.

        Args:
            days: Whole or fractional days.
            hours: Whole or fractional hours.
            minutes: Whole or fractional minutes.
            seconds: Whole or fractional seconds.
            microseconds: Whole microseconds (floats are rounded).

        Example:
            >>> Duration(days=1, hours=2).total_seconds()
            93600.0
        """
        us = (
            int(round(float(days) * 86_400_000_000))
            + int(round(float(hours) * 3_600_000_000))
            + int(round(float(minutes) * 60_000_000))
            + int(round(float(seconds) * 1_000_000))
            + int(round(float(microseconds)))
        )
        object.__setattr__(self, "_us", us)

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"Duration is immutable. Cannot set {name}")

    @property
    def microseconds_total(self) -> int:
        """Return the span as a signed integer microsecond count.

        Returns:
            Total microseconds (may be negative).
        """
        return self._us

    def total_seconds(self) -> float:
        """Return total seconds as a float.

        Returns:
            Elapsed seconds, negative for reverse spans.

        Example:
            >>> Duration(minutes=90).total_seconds()
            5400.0
        """
        return self._us / 1_000_000

    def days(self) -> int:
        """Return whole days (floor toward -inf for negatives).

        Returns:
            Whole day component of the span.

        Example:
            >>> Duration(hours=30).days()
            1
        """
        return int(self._us // 86_400_000_000)

    def hours(self) -> int:
        """Return hours remaining after whole days (0-23).

        Returns:
            Hour component.

        Example:
            >>> Duration(hours=30).hours()
            6
        """
        return int((self._us % 86_400_000_000) // 3_600_000_000)

    def minutes(self) -> int:
        """Return minutes remaining after whole hours (0-59).

        Returns:
            Minute component.

        Example:
            >>> Duration(minutes=90).minutes()
            30
        """
        return int((self._us % 3_600_000_000) // 60_000_000)

    def seconds(self) -> int:
        """Return seconds remaining after whole minutes (0-59).

        Returns:
            Second component.

        Example:
            >>> Duration(seconds=90).seconds()
            30
        """
        return int((self._us % 60_000_000) // 1_000_000)

    def microseconds(self) -> int:
        """Return microseconds remaining after whole seconds (0-999999).

        Returns:
            Microsecond component.

        Example:
            >>> Duration(microseconds=1500).microseconds()
            1500
        """
        return int(self._us % 1_000_000)

    def __add__(self, other: "Duration") -> "Duration":
        """Sum two durations.

        Args:
            other: Duration to add.

        Returns:
            New Duration equal to ``self + other``.
        """
        if not isinstance(other, Duration):
            return NotImplemented
        return Duration(microseconds=self._us + other._us)

    def __sub__(self, other: "Duration") -> "Duration":
        """Subtract two durations.

        Args:
            other: Duration to subtract.

        Returns:
            New Duration equal to ``self - other``.
        """
        if not isinstance(other, Duration):
            return NotImplemented
        return Duration(microseconds=self._us - other._us)

    def __neg__(self) -> "Duration":
        """Return the duration with reversed sign.

        Returns:
            New Duration equal to ``-self``.
        """
        return Duration(microseconds=-self._us)

    def __abs__(self) -> "Duration":
        """Return the non-negative magnitude of this duration.

        Returns:
            New Duration with absolute value.
        """
        return Duration(microseconds=abs(self._us))

    def __eq__(self, other: object) -> bool:
        """Exact microsecond equality."""
        if not isinstance(other, Duration):
            return False
        return self._us == other._us

    def __lt__(self, other: "Duration") -> bool:
        """Order by total microseconds."""
        if not isinstance(other, Duration):
            return NotImplemented
        return self._us < other._us

    def __hash__(self) -> int:
        """Hash using the microsecond total."""
        return hash(("Duration", self._us))

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Duration(days={self.days()}, hours={self.hours()}, "
            f"minutes={self.minutes()}, seconds={self.seconds()}, "
            f"microseconds={self.microseconds()})"
        )

    def __str__(self) -> str:
        """Human-readable compact form."""
        parts = []
        if self.days():
            parts.append(f"{self.days()}d")
        if self.hours():
            parts.append(f"{self.hours()}h")
        if self.minutes():
            parts.append(f"{self.minutes()}m")
        if self.seconds() or self.microseconds():
            parts.append(f"{self.seconds()}s")
        if self.microseconds():
            parts.append(f"{self.microseconds()}us")
        return " ".join(parts) if parts else "0s"

    @classmethod
    def from_seconds(cls, total_seconds: float) -> "Duration":
        """Create a Duration from a total second count.

        Args:
            total_seconds: Signed seconds (float or int).

        Returns:
            Duration representing that span.

        Example:
            >>> Duration.from_seconds(90).minutes()
            30
        """
        return cls(seconds=total_seconds)


def hours(n: int) -> Duration:
    """Create a Duration of ``n`` hours.

    Args:
        n: Number of hours.

    Returns:
        Duration spanning ``n`` hours.
    """
    return Duration(hours=n)


def minutes(n: int) -> Duration:
    """Create a Duration of ``n`` minutes.

    Args:
        n: Number of minutes.

    Returns:
        Duration spanning ``n`` minutes.
    """
    return Duration(minutes=n)


def seconds(n: int) -> Duration:
    """Create a Duration of ``n`` seconds.

    Args:
        n: Number of seconds.

    Returns:
        Duration spanning ``n`` seconds.
    """
    return Duration(seconds=n)


def duration(**kwargs) -> Duration:
    """Create a Duration from keyword unit arguments.

    Args:
        **kwargs: ``days``, ``hours``, ``minutes``, ``seconds``, ``microseconds``.

    Returns:
        Duration built from the provided units.

    Example:
        >>> duration(days=1, hours=5, minutes=30).days()
        1
    """
    return Duration(**kwargs)
