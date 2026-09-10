"""Tests for JalaliDate class."""

import pytest
from datetime import timezone
from parsidate.core import JalaliDate
from parsidate.core.converters import jalali_to_gregorian, gregorian_to_jalali
from parsidate.intervals.period import Period
from parsidate.intervals.duration import Duration


def test_init_and_properties():
    date = JalaliDate(1402, 8, 19, 14, 10, 22, 123456, tzinfo=timezone.utc)
    assert date.year() == 1402
    assert date.month() == 8
    assert date.day() == 19
    assert date.hour() == 14
    assert date.minute() == 10
    assert date.second() == 22
    assert date.microsecond() == 123456
    assert date.tzinfo() == timezone.utc


def test_read_only_properties():
    d = JalaliDate(1402, 5, 20)
    with pytest.raises(AttributeError):
        d.year = 1399
    with pytest.raises(AttributeError):
        d.month = 12


def test_replace():
    d = JalaliDate(1402, 5, 20, 7, 44, 51, 999999, tzinfo=timezone.utc)
    d2 = d.replace(year=1399, month=12, day=29, hour=7, minute=44, second=51, microsecond=999999, tzinfo=timezone.utc)
    assert (d2.year(), d2.month(), d2.day(), d2.hour(), d2.minute(), d2.second(), d2.microsecond(), d2.tzinfo()) == (1399, 12, 29, 7, 44, 51, 999999, timezone.utc)
    # Original unchanged
    assert d.year() == 1402


def test_weekday_and_quarter():
    date = JalaliDate(1403, 8, 20)
    assert 0 <= date.weekday() <= 6
    assert 1 <= date.quarter() <= 4


def test_day_of_year_and_leap():
    d = JalaliDate(1399, 12, 30)
    assert d.is_leap_year()
    doy = d.day_of_year()
    assert 1 <= doy <= 366


def test_add_years():
    d = JalaliDate(1400, 7, 10)
    d2 = d.add(years=3)
    assert d2.year() == 1403
    assert d.year() == 1400  # Original unchanged


def test_add_months():
    d = JalaliDate(1400, 12, 5)
    d2 = d.add(months=2)
    assert d2.year() == 1401
    assert d2.month() == 2


def test_add_days():
    d = JalaliDate(1400, 12, 24)
    d2 = d.add(days=7)
    # Should cross into 1401
    assert d2.year() == 1401


def test_add_hours():
    d = JalaliDate(1402, 3, 10, 20)
    d2 = d.add(hours=7)
    assert d2.hour() == 3


def test_add_minutes():
    d = JalaliDate(1402, 3, 10, 23, 50)
    d2 = d.add(minutes=15)
    assert d2.hour() == 0
    assert d2.minute() == 5


def test_add_seconds():
    d = JalaliDate(1402, 3, 10, 23, 59, 50)
    d2 = d.add(seconds=15)
    assert d2.hour() == 0
    assert d2.minute() == 0
    assert d2.second() == 5


def test_sub_years():
    d = JalaliDate(1404, 7, 10)
    d2 = d.sub(years=2)
    assert d2.year() == 1402


def test_sub_months():
    d = JalaliDate(1401, 3, 5)
    d2 = d.sub(months=4)
    assert d2.year() == 1400
    assert d2.month() == 11


def test_sub_days():
    d = JalaliDate(1401, 1, 5)
    d2 = d.sub(days=10)
    assert d2.month() == 12


def test_sub_hours():
    d = JalaliDate(1401, 2, 1, 5)
    d2 = d.sub(hours=8)
    assert d2.hour() == 21


def test_sub_minutes():
    d = JalaliDate(1401, 2, 1, 0, 10)
    d2 = d.sub(minutes=20)
    assert d2.minute() == 50


def test_sub_seconds():
    d = JalaliDate(1401, 2, 1, 0, 0, 15)
    d2 = d.sub(seconds=20)
    assert d2.second() == 55


def test_add_period_and_duration():
    d1 = JalaliDate(1402, 8, 10, 12)
    p = Period(years=1, months=2)
    dur = Duration(days=7, hours=5)
    d2 = d1 + p
    d3 = d1 + dur
    assert isinstance(d2, JalaliDate)
    assert isinstance(d3, JalaliDate)


def test_sub_jalali_date_and_duration():
    d1 = JalaliDate(1402, 8, 10)
    d2 = JalaliDate(1402, 8, 14)
    diff = d2 - d1
    assert isinstance(diff, Duration)
    assert diff.days() == 4


def test_sub_duration_object():
    d = JalaliDate(1402, 8, 19)
    d_sub = d - Duration(days=5)
    assert isinstance(d_sub, JalaliDate)
    assert d_sub.day() == 14


def test_format_and_repr():
    d = JalaliDate(1402, 1, 1, 15, 23, 10)
    fmt = d.format("%Y/%m/%d", "en")
    assert isinstance(fmt, str)
    assert "1402" in fmt
    assert "JalaliDate" in repr(d)


def test_copy_and_equality():
    d1 = JalaliDate(1402, 5, 15, 12)
    d2 = d1.copy()
    assert d2 == d1
    d3 = d2.replace(day=28)
    assert d3.day() != d1.day()


def test_comparison_operators():
    d1 = JalaliDate(1402, 5, 15)
    d2 = JalaliDate(1402, 6, 15)
    assert d2 > d1
    assert d1 < d2
    assert d1 != d2
    assert d1 == d1.copy()
    assert d2 >= d1
    assert d1 <= d2


def test_str_method():
    d = JalaliDate(1402, 1, 1, 4, 0)
    assert isinstance(str(d), str)


def test_gregorian_conversion():
    jdate = JalaliDate(1403, 1, 1)
    gy, gm, gd = jalali_to_gregorian(jdate.year(), jdate.month(), jdate.day())
    jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
    assert jy == 1403


def test_repr_str_contains_values():
    d = JalaliDate(1402, 8, 19, 14, 10, 22, 123456)
    r = repr(d)
    s = str(d)
    for v in ["1402", "8", "19"]:
        assert v in r
        assert v in s


def test_invalid_dates():
    with pytest.raises(ValueError):
        JalaliDate(1402, 13, 1)
    with pytest.raises(ValueError):
        JalaliDate(1402, 12, 32)
    with pytest.raises(ValueError):
        JalaliDate(1402, 0, 10)


def test_leap_year_logic():
    assert JalaliDate(1399, 12, 30).is_leap_year()
    assert not JalaliDate(1400, 12, 29).is_leap_year()


def test_timezone_replace():
    tz = timezone.utc
    d = JalaliDate(1402, 6, 1)
    d2 = d.replace(tzinfo=tz)
    assert d2.tzinfo() == tz


def test_replace_chaining():
    d = JalaliDate(1402, 1, 1)
    d2 = d.replace(year=1404, month=7, day=22, hour=19, minute=30, second=44, microsecond=999999)
    assert (d2.year(), d2.month(), d2.day(), d2.hour(), d2.minute(), d2.second(), d2.microsecond()) == (1404, 7, 22, 19, 30, 44, 999999)


def test_edge_end_of_month():
    d = JalaliDate(1402, 12, 29)
    d2 = d.add(days=2)
    assert d2.month() == 1
    assert d2.day() <= 2
