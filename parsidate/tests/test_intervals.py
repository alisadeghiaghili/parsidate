"""Tests for Duration, Period, and Interval classes."""

import pytest
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.intervals.duration import Duration, duration
from parsidate.intervals.period import Period, period
from parsidate.intervals.interval import Interval, interval


class TestDuration:
    def test_creation(self):
        d = Duration(days=1, hours=5, minutes=30)
        assert d.days() == 1
        assert d.hours() == 5
        assert d.minutes() == 30

    def test_total_seconds(self):
        d = Duration(hours=1)
        assert d.total_seconds() == 3600

    def test_add(self):
        d1 = Duration(hours=1)
        d2 = Duration(hours=2)
        d3 = d1 + d2
        assert d3.hours() == 3

    def test_sub(self):
        d1 = Duration(hours=3)
        d2 = Duration(hours=1)
        d3 = d1 - d2
        assert d3.hours() == 2

    def test_neg(self):
        d = Duration(hours=1)
        d2 = -d
        assert d2.total_seconds() == -3600

    def test_equality(self):
        d1 = Duration(hours=1)
        d2 = Duration(hours=1)
        assert d1 == d2

    def test_repr(self):
        d = Duration(days=1, hours=5)
        r = repr(d)
        assert "Duration" in r

    def test_str(self):
        d = Duration(days=1, hours=5, minutes=30)
        s = str(d)
        assert "1d" in s
        assert "5h" in s

    def test_from_seconds(self):
        d = Duration.from_seconds(3661)
        assert d.hours() == 1
        assert d.minutes() == 1
        assert d.seconds() == 1


class TestDurationFactory:
    def test_hours(self):
        d = duration(hours=5)
        assert d.hours() == 5

    def test_minutes(self):
        d = duration(minutes=30)
        assert d.minutes() == 30

    def test_days(self):
        d = duration(days=7)
        assert d.days() == 7


class TestPeriod:
    def test_creation(self):
        p = Period(years=1, months=2, weeks=3, days=4)
        assert p.years == 1
        assert p.months == 2
        assert p.weeks == 3
        assert p.days == 4

    def test_add(self):
        p1 = Period(months=2)
        p2 = Period(months=3)
        p3 = p1 + p2
        assert p3.months == 5

    def test_sub(self):
        p1 = Period(months=5)
        p2 = Period(months=2)
        p3 = p1 - p2
        assert p3.months == 3

    def test_neg(self):
        p = Period(months=2)
        p2 = -p
        assert p2.months == -2

    def test_equality(self):
        p1 = Period(months=2, days=5)
        p2 = Period(months=2, days=5)
        assert p1 == p2

    def test_fixed_days(self):
        p = Period(weeks=1, days=3)
        assert p.fixed_days() == 10
        assert p.approx_days() == 10

    def test_period_immutable(self):
        p = Period(months=1)
        try:
            p.months = 2  # type: ignore[misc]
            raise AssertionError("Period should be immutable")
        except AttributeError:
            pass

    def test_repr(self):
        p = Period(years=1, months=2)
        r = repr(p)
        assert "Period" in r

    def test_str(self):
        p = Period(years=1, months=2, weeks=3, days=4)
        s = str(p)
        assert "1y" in s
        assert "2m" in s


class TestPeriodFactory:
    def test_years(self):
        p = period(years=2)
        assert p.years == 2

    def test_months(self):
        p = period(months=3)
        assert p.months == 3


class TestInterval:
    def test_creation(self):
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 10)
        iv = Interval(start, end)
        assert iv.start == start
        assert iv.end == end

    def test_invalid_order(self):
        start = JalaliDate(1403, 1, 10)
        end = JalaliDate(1403, 1, 1)
        with pytest.raises(ValueError):
            Interval(start, end)

    def test_contains(self):
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 10)
        iv = Interval(start, end)
        mid = JalaliDate(1403, 1, 5)
        assert mid in iv

    def test_length(self):
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 10)
        iv = Interval(start, end)
        assert iv.length("days") == 9

    def test_repr(self):
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 10)
        iv = Interval(start, end)
        r = repr(iv)
        assert "Interval" in r

    def test_str(self):
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 10)
        iv = Interval(start, end)
        s = str(iv)
        assert "[" in s


class TestIntervalFactory:
    def test_interval(self):
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 10)
        iv = interval(start, end)
        assert isinstance(iv, Interval)

    def test_duration(self):
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 10)
        iv = Interval(start, end)
        dur = iv.duration()
        assert dur.days() == 9

    def test_length_hours(self):
        start = JalaliDate(1403, 1, 1, 0, 0, 0)
        end = JalaliDate(1403, 1, 2, 0, 0, 0)
        iv = Interval(start, end)
        assert iv.length("hours") == 24

    def test_length_minutes(self):
        start = JalaliDate(1403, 1, 1, 0, 0, 0)
        end = JalaliDate(1403, 1, 1, 1, 0, 0)
        iv = Interval(start, end)
        assert iv.length("minutes") == 60

    def test_length_seconds(self):
        start = JalaliDate(1403, 1, 1, 0, 0, 0)
        end = JalaliDate(1403, 1, 1, 0, 1, 0)
        iv = Interval(start, end)
        assert iv.length("seconds") == 60

    def test_length_invalid_unit(self):
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 10)
        iv = Interval(start, end)
        with pytest.raises(ValueError):
            iv.length("invalid")

    def test_different_types_error(self):
        j = JalaliDate(1403, 1, 1)
        g = GregorianDate(2024, 1, 1)
        with pytest.raises(TypeError):
            Interval(j, g)
