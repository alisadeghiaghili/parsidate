"""Regression tests that pin P0 correctness bugs.

These tests must fail on the broken baseline and stay green after the fix.
"""

from __future__ import annotations

import pytest

from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.core.converters import jalali_to_gregorian
from parsidate.intervals.interval import Interval
from parsidate.intervals.duration import Duration
from parsidate.utils.helpers import is_leap_year


class TestJalaliDateSubtraction:
    """Date difference must respect leap years and time-of-day."""

    def test_same_year_day_diff(self) -> None:
        later = JalaliDate(1403, 1, 10)
        earlier = JalaliDate(1403, 1, 1)
        assert (later - earlier).days() == 9

    def test_leap_year_full_year_diff(self) -> None:
        """1403 is leap; 1404/1/1 - 1403/1/1 is 366 days, not 365."""
        assert is_leap_year(1403, "jalali") is True
        later = JalaliDate(1404, 1, 1)
        earlier = JalaliDate(1403, 1, 1)
        assert (later - earlier).days() == 366

    def test_non_leap_full_year_diff(self) -> None:
        assert is_leap_year(1402, "jalali") is False
        later = JalaliDate(1403, 1, 1)
        earlier = JalaliDate(1402, 1, 1)
        assert (later - earlier).days() == 365

    def test_same_day_time_only_diff(self) -> None:
        later = JalaliDate(1403, 1, 1, 1, 0, 0)
        earlier = JalaliDate(1403, 1, 1, 0, 0, 0)
        diff = later - earlier
        assert diff.days() == 0
        assert diff.hours() == 1
        assert diff.total_seconds() == 3600

    def test_cross_day_with_time(self) -> None:
        later = JalaliDate(1403, 1, 2, 0, 0, 0)
        earlier = JalaliDate(1403, 1, 1, 23, 0, 0)
        diff = later - earlier
        assert diff.days() == 0
        assert diff.hours() == 1

    def test_negative_diff(self) -> None:
        later = JalaliDate(1403, 1, 10)
        earlier = JalaliDate(1403, 1, 1)
        assert (earlier - later).days() == -9

    def test_matches_gregorian_ordinal_span(self) -> None:
        a = JalaliDate(1399, 12, 30)
        b = JalaliDate(1400, 1, 1)
        gy_a, gm_a, gd_a = jalali_to_gregorian(1399, 12, 30)
        gy_b, gm_b, gd_b = jalali_to_gregorian(1400, 1, 1)
        from datetime import date

        expected = (date(gy_b, gm_b, gd_b) - date(gy_a, gm_a, gd_a)).days
        assert (b - a).days() == expected == 1


class TestImmutability:
    """Both calendar types must never mutate the receiver."""

    def test_jalali_add_returns_new(self) -> None:
        original = JalaliDate(1403, 8, 18)
        new = original.add(days=5)
        assert original.day() == 18
        assert new.day() == 23
        assert original is not new

    def test_gregorian_add_returns_new(self) -> None:
        original = GregorianDate(2024, 1, 15)
        new = original.add(months=1)
        assert original.month() == 1
        assert new.month() == 2
        assert original is not new

    def test_gregorian_getters_are_readonly(self) -> None:
        d = GregorianDate(2024, 1, 1)
        with pytest.raises(TypeError):
            d.year(2025)  # type: ignore[misc]

    def test_ceil_to_day_does_not_mutate_input(self) -> None:
        from parsidate.operations.rounding import ceil_to_day

        original = GregorianDate(2024, 3, 15, 10, 0)
        rounded = ceil_to_day(original)
        assert original.hour() == 10
        assert original.day() == 15
        assert rounded.day() == 16
        assert rounded.hour() == 0

    def test_ceil_to_month_does_not_mutate_input(self) -> None:
        from parsidate.operations.rounding import ceil_to_month

        original = GregorianDate(2024, 3, 15, 10, 0)
        rounded = ceil_to_month(original)
        assert original.month() == 3
        assert original.day() == 15
        assert rounded.month() == 4
        assert rounded.day() == 1

    def test_floor_to_month_does_not_mutate_input(self) -> None:
        from parsidate.operations.rounding import floor_to_month

        original = GregorianDate(2024, 3, 15, 10, 0)
        rounded = floor_to_month(original)
        assert original.day() == 15
        assert rounded.day() == 1
        assert rounded.hour() == 0


class TestEqualityAndHash:
    """__eq__ and __hash__ must agree on the same field set."""

    def test_jalali_eq_includes_microsecond(self) -> None:
        a = JalaliDate(1403, 1, 1, 0, 0, 0, 1)
        b = JalaliDate(1403, 1, 1, 0, 0, 0, 2)
        assert a != b
        assert hash(a) != hash(b)

    def test_jalali_equal_objects_share_hash(self) -> None:
        a = JalaliDate(1403, 1, 1, 12, 0, 0, 999)
        b = JalaliDate(1403, 1, 1, 12, 0, 0, 999)
        assert a == b
        assert hash(a) == hash(b)

    def test_gregorian_equal_objects_share_hash(self) -> None:
        a = GregorianDate(2024, 1, 1, 12, 0, 0, 999)
        b = GregorianDate(2024, 1, 1, 12, 0, 0, 999)
        assert a == b
        assert hash(a) == hash(b)

    def test_usable_as_dict_keys(self) -> None:
        a = JalaliDate(1403, 1, 1)
        b = JalaliDate(1403, 1, 1)
        mapping = {a: "first"}
        mapping[b] = "second"
        assert mapping == {a: "second"}


class TestIntervalLength:
    """Interval.length must use elapsed time, not calendar-day guess."""

    def test_length_minutes_same_day(self) -> None:
        start = JalaliDate(1403, 1, 1, 0, 0, 0)
        end = JalaliDate(1403, 1, 1, 1, 0, 0)
        assert Interval(start, end).length("minutes") == 60

    def test_length_seconds_same_day(self) -> None:
        start = JalaliDate(1403, 1, 1, 0, 0, 0)
        end = JalaliDate(1403, 1, 1, 0, 1, 0)
        assert Interval(start, end).length("seconds") == 60

    def test_length_hours_across_leap_year(self) -> None:
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1404, 1, 1)
        assert Interval(start, end).length("hours") == 366 * 24


class TestDimDateStrftime:
    """dim_date full_date must use standard strftime codes."""

    def test_jalali_full_date_uses_strftime_pattern(self) -> None:
        from parsidate.dimdate import generate_dim_date

        dim = generate_dim_date(start="1402/01/01", end="1402/01/01", calendar="jalali")
        assert dim.iloc[0]["full_date"] == "1402/01/01"

    def test_gregorian_full_date_uses_strftime_pattern(self) -> None:
        from parsidate.dimdate import generate_dim_date

        dim = generate_dim_date(start="2024-03-20", end="2024-03-20", calendar="gregorian")
        assert dim.iloc[0]["full_date"] == "2024-03-20"


class TestPackagingInvariants:
    """Import surface must work as a real installed package layout."""

    def test_public_imports_resolve(self) -> None:
        import parsidate

        assert hasattr(parsidate, "JalaliDate")
        assert hasattr(parsidate, "to_jalali")
        assert parsidate.__version__

    def test_subpackage_imports(self) -> None:
        from parsidate.core import JalaliDate as J
        from parsidate.parsers import jmd
        from parsidate.formatting.formatters import format_jalali_date

        assert J is not None
        assert callable(jmd)
        assert callable(format_jalali_date)


class TestStrptimeFormat:
    """Date parsing must accept standard strptime format codes."""

    def test_strptime_jalali_default(self) -> None:
        from parsidate.parsers import strptime_jalali

        d = strptime_jalali("1403/08/18")
        assert (d.year(), d.month(), d.day()) == (1403, 8, 18)

    def test_strptime_jalali_custom_order(self) -> None:
        from parsidate.parsers import strptime_jalali

        d = strptime_jalali("18-08-1403 14:30:25", "%d-%m-%Y %H:%M:%S")
        assert (d.year(), d.month(), d.day(), d.hour(), d.minute(), d.second()) == (
            1403,
            8,
            18,
            14,
            30,
            25,
        )

    def test_strptime_jalali_persian_digits(self) -> None:
        from parsidate.parsers import strptime_jalali

        d = strptime_jalali("۱۴۰۳/۰۸/۱۸", "%Y/%m/%d")
        assert d.day() == 18

    def test_strptime_gregorian(self) -> None:
        from parsidate.parsers import strptime_gregorian

        d = strptime_gregorian("2024-11-08 14:30:25", "%Y-%m-%d %H:%M:%S")
        assert (d.year(), d.month(), d.day(), d.hour()) == (2024, 11, 8, 14)

    def test_strptime_mismatch_raises(self) -> None:
        from parsidate.parsers import strptime_jalali

        with pytest.raises(ValueError):
            strptime_jalali("2024-11-08", "%Y/%m/%d")
