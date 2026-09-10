"""Tests for immutable GregorianDate and standard strftime formatting."""

from __future__ import annotations

from datetime import timezone

import pytest

from parsidate.core import GregorianDate
from parsidate.core.converters import gregorian_to_jalali, jalali_to_gregorian
from parsidate.intervals.period import Period
from parsidate.intervals.duration import Duration


def test_init_and_properties() -> None:
    date = GregorianDate(2024, 11, 8, 14, 10, 22, 123456, tzinfo=timezone.utc)
    assert date.year() == 2024
    assert date.month() == 11
    assert date.day() == 8
    assert date.hour() == 14
    assert date.minute() == 10
    assert date.second() == 22
    assert date.microsecond() == 123456
    assert date.tzinfo() == timezone.utc


def test_getters_do_not_mutate() -> None:
    d = GregorianDate(2023, 8, 20)
    assert d.year() == 2023
    assert d.month() == 8
    assert d.day() == 20
    with pytest.raises(TypeError):
        d.year(2021)  # type: ignore[misc]


def test_replace_returns_new_instance() -> None:
    d = GregorianDate(2023, 8, 20)
    d2 = d.replace(year=2021, month=1, day=29, hour=7, minute=44, second=51, microsecond=999999, tzinfo=timezone.utc)
    assert (d.year(), d.month(), d.day()) == (2023, 8, 20)
    assert (d2.year(), d2.month(), d2.day(), d2.hour(), d2.minute(), d2.second(), d2.microsecond()) == (
        2021,
        1,
        29,
        7,
        44,
        51,
        999999,
    )


def test_weekday_and_quarter() -> None:
    date = GregorianDate(2024, 11, 8)
    assert date.weekday() == 4
    assert 1 <= date.quarter() <= 4


def test_day_of_year_and_leap() -> None:
    d = GregorianDate(2020, 2, 29)
    assert d.is_leap_year()
    assert 1 <= d.day_of_year() <= 366


def test_add_years_returns_new() -> None:
    d = GregorianDate(2020, 7, 10)
    d2 = d.add(years=3)
    assert d.year() == 2020
    assert d2.year() == 2023


def test_add_months_rolls_year() -> None:
    d = GregorianDate(2020, 12, 5)
    d2 = d.add(months=2)
    assert d2.year() == 2021
    assert d2.month() == 2


def test_add_days() -> None:
    d = GregorianDate(2020, 12, 28)
    d2 = d.add(days=3)
    assert (d2.year(), d2.month(), d2.day()) == (2020, 12, 31)
    assert d.day() == 28
    d3 = d.add(days=4)
    assert (d3.year(), d3.month(), d3.day()) == (2021, 1, 1)


def test_add_hours() -> None:
    d = GregorianDate(2024, 3, 10, 20)
    d2 = d.add(hours=7)
    assert d2.day() == 11
    assert d2.hour() == 3


def test_add_minutes() -> None:
    d = GregorianDate(2024, 3, 10, 23, 50)
    d2 = d.add(minutes=15)
    assert (d2.day(), d2.hour(), d2.minute()) == (11, 0, 5)


def test_add_seconds() -> None:
    d = GregorianDate(2024, 3, 10, 23, 59, 50)
    d2 = d.add(seconds=15)
    assert (d2.hour(), d2.minute(), d2.second()) == (0, 0, 5)


def test_sub_years() -> None:
    d = GregorianDate(2024, 7, 10)
    d2 = d.sub(years=2)
    assert d2.year() == 2022


def test_sub_months() -> None:
    d = GregorianDate(2022, 3, 5)
    d2 = d.sub(months=4)
    assert d2.year() == 2021
    assert d2.month() == 11


def test_sub_days() -> None:
    d = GregorianDate(2022, 1, 5)
    d2 = d.sub(days=10)
    assert (d2.year(), d2.month(), d2.day()) == (2021, 12, 26)


def test_sub_hours() -> None:
    d = GregorianDate(2022, 2, 1, 5)
    d2 = d.sub(hours=8)
    assert d2.day() == 31
    assert d2.hour() == 21


def test_sub_minutes() -> None:
    d = GregorianDate(2022, 2, 1, 0, 10)
    d2 = d.sub(minutes=20)
    assert (d2.day(), d2.hour(), d2.minute()) == (31, 23, 50)


def test_sub_seconds() -> None:
    d = GregorianDate(2022, 2, 1, 0, 0, 15)
    d2 = d.sub(seconds=20)
    assert (d2.day(), d2.hour(), d2.minute(), d2.second()) == (31, 23, 59, 55)


def test_add_period_and_duration() -> None:
    d1 = GregorianDate(2024, 8, 10, 12)
    p = Period(years=1, months=2)
    dur = Duration(days=7, hours=5)
    d2 = d1 + p
    d3 = d1 + dur
    assert isinstance(d2, GregorianDate)
    assert isinstance(d3, GregorianDate)
    assert d1.year() == 2024


def test_sub_gregorian_date_and_duration() -> None:
    d1 = GregorianDate(2024, 8, 10)
    d2 = GregorianDate(2024, 8, 14)
    diff = d2 - d1
    assert isinstance(diff, Duration)
    assert diff.days() == 4


def test_sub_duration_object() -> None:
    d = GregorianDate(2024, 8, 19)
    d_sub = d - Duration(days=5)
    assert isinstance(d_sub, GregorianDate)
    assert d_sub.day() == 14


def test_format_uses_strftime_codes() -> None:
    d = GregorianDate(2024, 1, 1, 15, 23, 10)
    assert d.strftime("%Y-%m-%d %H:%M:%S") == "2024-01-01 15:23:10"
    assert d.format("%Y/%m/%d") == "2024/01/01"
    assert "GregorianDate" in repr(d)


def test_copy_and_equality() -> None:
    d1 = GregorianDate(2024, 5, 15, 12)
    d2 = d1.copy()
    assert d2 == d1
    d3 = d2.replace(day=28)
    assert d3.day() != d1.day()
    assert d2.day() == d1.day()


def test_comparison_operators() -> None:
    d1 = GregorianDate(2024, 5, 15)
    d2 = GregorianDate(2024, 6, 15)
    assert d2 > d1
    assert d1 < d2
    assert d1 != d2
    assert d1 == d1.copy()
    assert d2 >= d1
    assert d1 <= d2


def test_str_method() -> None:
    d = GregorianDate(2024, 1, 1, 4, 0)
    assert isinstance(str(d), str)


def test_jalali_conversion() -> None:
    gdate = GregorianDate(2024, 3, 20)
    jy, jm, jd = gregorian_to_jalali(gdate.year(), gdate.month(), gdate.day())
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    assert (gy, gm, gd) == (gdate.year(), gdate.month(), gdate.day())


def test_repr_str_contains_values() -> None:
    d = GregorianDate(2024, 8, 19, 14, 10, 22, 123456)
    r = repr(d)
    s = str(d)
    for v in ["2024", "8", "19"]:
        assert v in r
        assert v in s


def test_invalid_dates() -> None:
    with pytest.raises(ValueError):
        GregorianDate(2024, 13, 1)
    with pytest.raises(ValueError):
        GregorianDate(2024, 12, 32)
    with pytest.raises(ValueError):
        GregorianDate(2024, 0, 10)


def test_leap_year_logic() -> None:
    assert GregorianDate(2020, 2, 29).is_leap_year()
    assert not GregorianDate(2021, 2, 28).is_leap_year()


def test_timezone_set_and_get() -> None:
    tz = timezone.utc
    d = GregorianDate(2024, 6, 1)
    d2 = d.replace(tzinfo=tz)
    assert d.tzinfo() is None
    assert d2.tzinfo() == tz


def test_immutability_chaining() -> None:
    d = GregorianDate(2024, 1, 1)
    d2 = (
        d.replace(year=2025)
        .replace(month=7)
        .replace(day=22)
        .replace(hour=19)
        .replace(minute=30)
        .replace(second=44)
        .replace(microsecond=999999)
    )
    assert (d.year(), d.month(), d.day()) == (2024, 1, 1)
    assert (d2.year(), d2.month(), d2.day(), d2.hour(), d2.minute(), d2.second(), d2.microsecond()) == (
        2025,
        7,
        22,
        19,
        30,
        44,
        999999,
    )


def test_edge_end_of_month() -> None:
    d = GregorianDate(2024, 12, 30)
    d2 = d.add(days=2)
    assert (d2.month(), d2.day()) == (1, 1)
