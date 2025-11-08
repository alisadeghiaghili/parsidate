"""
Duration: Precise time interval class for ParsiDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

from typing import Optional

class Duration:
    """
    Represents an exact time duration (interval).
    Can be used for time difference, addition, subtraction.

    Attributes:
        seconds: Total seconds in duration (float).
    """

    def __init__(
        self,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        microseconds: int = 0
    ):
        """
        Initialize Duration.

        Args:
            days: Number of days.
            hours: Number of hours.
            minutes: Number of minutes.
            seconds: Number of seconds.
            microseconds: Number of microseconds.
        """
        self._total_seconds = (
            days * 86400 +
            hours * 3600 +
            minutes * 60 +
            seconds +
            microseconds / 1_000_000
        )

    def total_seconds(self) -> float:
        """Return total seconds as float."""
        return self._total_seconds

    def days(self) -> int:
        """Get total days (rounded down)."""
        return int(self._total_seconds // 86400)

    def hours(self) -> int:
        """Get total hours (excluding days, rounded down)."""
        return int((self._total_seconds % 86400) // 3600)

    def minutes(self) -> int:
        """Get total minutes (excluding hours/days, rounded down)."""
        return int((self._total_seconds % 3600) // 60)

    def seconds(self) -> int:
        """Get seconds (excluding larger units, rounded down)."""
        return int(self._total_seconds % 60)

    def microseconds(self) -> int:
        """Get microseconds (excluding seconds)."""
        return int((self._total_seconds - int(self._total_seconds)) * 1_000_000)

    def __add__(self, other: "Duration") -> "Duration":
        """Sum two durations."""
        return Duration(seconds=self._total_seconds + other._total_seconds)

    def __sub__(self, other: "Duration") -> "Duration":
        """Subtract two durations."""
        return Duration(seconds=self._total_seconds - other._total_seconds)

    def __neg__(self) -> "Duration":
        """Reverse duration sign."""
        return Duration(seconds=-self._total_seconds)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return False
        return abs(self._total_seconds - other._total_seconds) < 1e-6

    def __repr__(self) -> str:
        return (f"Duration(days={self.days()}, hours={self.hours()}, "
                f"minutes={self.minutes()}, seconds={self.seconds()}, "
                f"microseconds={self.microseconds()})")

    def __str__(self) -> str:
        s = []
        if self.days():
            s.append(f"{self.days()}d")
        if self.hours():
            s.append(f"{self.hours()}h")
        if self.minutes():
            s.append(f"{self.minutes()}m")
        if self.seconds() or self.microseconds():
            s.append(f"{self.seconds()}s")
        if self.microseconds():
            s.append(f"{self.microseconds()}μs")
        return " ".join(s) if s else "0s"

    @classmethod
    def from_seconds(cls, total_seconds: float) -> "Duration":
        """
        Create Duration from seconds.

        Args:
            total_seconds: Number of seconds.
        Returns:
            Duration object.
        """
        return cls(seconds=total_seconds)
