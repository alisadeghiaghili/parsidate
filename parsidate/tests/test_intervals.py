import pytest
from parsidate.intervals.period import Period
from parsidate.intervals.duration import Duration
from parsidate.intervals.interval import Interval
from parsidate.core import JalaliDate, GregorianDate

def test_period_init_and_properties():
    p = Period(years=2, months=5)
    assert p.years == 2 and p.months == 5
    assert isinstance(str(p), str)
    p2 = Period(days=10)
    assert p2.days == 10

def test_duration_init_and_properties():
    d = Duration(days=3, hours=7, minutes=25)
    assert d.days == 3 and d.hours == 7 and d.minutes == 25
    assert isinstance(str(d), str)
    d2 = Duration(seconds=1800)
    assert d2.seconds == 1800

def test_period_addition():
    p1 = Period(years=1, months=2)
    p2 = Period(months=5, days=7)
    p3 = p1 + p2
    assert isinstance(p3, Period)
    assert p3.years == 1 and p3.months == 7 and p3.days == 7

def test_duration_addition():
    d1 = Duration(days=2, hours=3)
    d2 = Duration(days=1, hours=5, minutes=10)
    d3 = d1 + d2
    assert isinstance(d3, Duration)
    assert d3.days == 3 and d3.hours == 8 and d3.minutes == 10

def test_period_subtraction():
    p1 = Period(months=10)
    p2 = Period(months=2)
    p3 = p1 - p2
    assert p3.months == 8

def test_duration_subtraction():
    d1 = Duration(days=5)
    d2 = Duration(days=2)
    d3 = d1 - d2
    assert d3.days == 3

def test_interval_basic():
    start = JalaliDate(1402, 2, 1, 10)
    end = JalaliDate(1402, 3, 1, 8)
    interval = Interval(start, end)
    assert interval.start == start and interval.end == end
    assert isinstance(str(interval), str)
    assert interval.length().days > 0

def test_interval_contains():
    start = GregorianDate(2024, 1, 1)
    end = GregorianDate(2024, 2, 1)
    interval = Interval(start, end)
    inside = GregorianDate(2024, 1, 15)
    outside = GregorianDate(2023, 12, 31)
    assert interval.contains(inside)
    assert not interval.contains(outside)

def test_period_apply_on_date():
    date = JalaliDate(1402, 1, 1)
    p = Period(years=2, months=3, days=10)
    result = date + p
    assert result.year() == 1404 or result.month() == 4

def test_duration_apply_on_date():
    date = GregorianDate(2024, 11, 8, 22)
    d = Duration(days=7, hours=5)
    result = date + d
    assert isinstance(result, GregorianDate)
    assert result.day() >= 15 or result.hour() == 3

def test_interval_length():
    start = JalaliDate(1402, 5, 15)
    end = JalaliDate(1402, 5, 20)
    interval = Interval(start, end)
    dur = interval.length()
    assert isinstance(dur, Duration)
    assert dur.days == 5

def test_period_and_duration_equality():
    p1 = Period(years=1, months=2)
    p2 = Period(years=1, months=2)
    d1 = Duration(days=3, hours=4)
    d2 = Duration(days=3, hours=4)
    assert p1 == p2
    assert d1 == d2

def test_str_repr_period_duration_interval():
    p = Period(years=2)
    d = Duration(days=5)
    start = JalaliDate(1400, 4, 1)
    end = JalaliDate(1400, 4, 10)
    i = Interval(start, end)
    assert isinstance(str(p), str)
    assert isinstance(str(d), str)
    assert isinstance(str(i), str)

def test_invalid_interval():
    start = JalaliDate(1401, 8, 20)
    end = JalaliDate(1400, 8, 20)
    with pytest.raises(ValueError):
        Interval(start, end)
