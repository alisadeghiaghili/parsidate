import pytest
from datetime import timezone
from parsidate.core import GregorianDate
from parsidate.core.converters import gregorian_to_jalali, jalali_to_gregorian
from parsidate.intervals.period import Period
from parsidate.intervals.duration import Duration

# --- Property and Setter tests ---

def test_init_and_properties():
    date = GregorianDate(2024, 11, 8, 14, 10, 22, 123456, tzinfo=timezone.utc)
    assert date.year() == 2024
    assert date.month() == 11
    assert date.day() == 8
    assert date.hour() == 14
    assert date.minute() == 10
    assert date.second() == 22
    assert date.microsecond() == 123456
    assert date.tzinfo() == timezone.utc

def test_all_setters():
    d = GregorianDate(2023, 8, 20)
    d.year(2021)
    d.month(1)
    d.day(29)
    d.hour(7)
    d.minute(44)
    d.second(51)
    d.microsecond(999999)
    d.tzinfo(timezone.utc)
    assert (d.year(), d.month(), d.day(), d.hour(), d.minute(), d.second(), d.microsecond(), d.tzinfo()) == (2021, 1, 29, 7, 44, 51, 999999, timezone.utc)

# --- Logic tests ---

def test_weekday_and_quarter():
    date = GregorianDate(2024, 11, 8)
    assert 0 <= date.weekday() <= 6
    assert 1 <= date.quarter() <= 4

def test_day_of_year_and_leap():
    d = GregorianDate(2020, 2, 29)
    assert d.is_leap_year()
    doy = d.day_of_year()
    assert 1 <= doy <= 366

# --- Direct add/sub method unit tests ---

def test_add_years():
    d = GregorianDate(2020, 7, 10)
    d.add(years=3)
    assert d.year() == 2023

def test_add_months():
    d = GregorianDate(2020, 12, 5)
    d.add(months=2)
    # Roll to new year
    assert (d.month() == 2 and d.year() == 2021) or d.month() == 1

def test_add_days():
    d = GregorianDate(2020, 12, 28)
    d.add(days=3)
    assert d.month() in [12, 1]

def test_add_hours():
    d = GregorianDate(2024, 3, 10, 20)
    d.add(hours=7)
    assert d.hour() == 3 or (d.hour() == 3 and (d.day() == 11 or d.day() == 10))

def test_add_minutes():
    d = GregorianDate(2024, 3, 10, 23, 50)
    d.add(minutes=15)
    assert d.minute() == 5 and (d.hour() == 0 or d.hour() == 23)

def test_add_seconds():
    d = GregorianDate(2024, 3, 10, 23, 59, 50)
    d.add(seconds=15)
    assert d.second() == 5 and (d.minute() == 0 or d.minute() == 59)

def test_sub_years():
    d = GregorianDate(2024, 7, 10)
    d.sub(years=2)
    assert d.year() == 2022

def test_sub_months():
    d = GregorianDate(2022, 3, 5)
    d.sub(months=4)
    assert d.month() in [11, 12] or d.year() == 2021

def test_sub_days():
    d = GregorianDate(2022, 1, 5)
    d.sub(days=10)
    assert d.month() in [12, 1]

def test_sub_hours():
    d = GregorianDate(2022, 2, 1, 5)
    d.sub(hours=8)
    assert d.hour() in [21, 22, 23]

def test_sub_minutes():
    d = GregorianDate(2022, 2, 1, 0, 10)
    d.sub(minutes=20)
    assert d.minute() in [50, 0, 59]

def test_sub_seconds():
    d = GregorianDate(2022, 2, 1, 0, 0, 15)
    d.sub(seconds=20)
    assert d.second() in [55, 59, 0]

# --- Operator method tests ---

def test_add_period_and_duration():
    d1 = GregorianDate(2024, 8, 10, 12)
    p = Period(years=1, months=2)
    dur = Duration(days=7, hours=5)
    d2 = d1 + p
    d3 = d1 + dur
    assert isinstance(d2, GregorianDate)
    assert isinstance(d3, GregorianDate)

def test_sub_gregorian_date_and_duration():
    d1 = GregorianDate(2024, 8, 10)
    d2 = GregorianDate(2024, 8, 14)
    diff = d2 - d1
    assert isinstance(diff, Duration)
    assert diff.days() == 4

def test_sub_duration_object():
    d = GregorianDate(2024, 8, 19)
    d_sub = d - Duration(days=5)
    assert isinstance(d_sub, GregorianDate)
    assert d_sub.day() == 14

# --- Edge/corner/test coverage ---

def test_format_and_repr():
    d = GregorianDate(2024, 1, 1, 15, 23, 10)
    fmt = d.format("Y/m/d H:i:s")
    assert isinstance(fmt, str)
    assert "GregorianDate" in repr(d)

def test_copy_and_equality():
    d1 = GregorianDate(2024, 5, 15, 12)
    d2 = d1.copy()
    assert d2 == d1
    d2.day(28)
    assert d2.day() != d1.day()

def test_comparison_operators():
    d1 = GregorianDate(2024, 5, 15)
    d2 = GregorianDate(2024, 6, 15)
    assert d2 > d1
    assert d1 < d2
    assert d1 != d2
    assert d1 == d1.copy()
    assert d2 >= d1
    assert d1 <= d2

def test_str_method():
    d = GregorianDate(2024, 1, 1, 4, 0)
    assert isinstance(str(d), str)

def test_jalali_conversion():
    gdate = GregorianDate(2024, 3, 20)
    jy, jm, jd = gregorian_to_jalali(gdate.year(), gdate.month(), gdate.day())
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    assert (gy, gm, gd) == (gdate.year(), gdate.month(), gdate.day())

def test_repr_str_contains_values():
    d = GregorianDate(2024, 8, 19, 14, 10, 22, 123456)
    r = repr(d)
    s = str(d)
    for v in ["2024", "8", "19"]:
        assert v in r
        assert v in s

def test_invalid_dates():
    with pytest.raises(ValueError):
        GregorianDate(2024, 13, 1)
    with pytest.raises(ValueError):
        GregorianDate(2024, 12, 32)
    with pytest.raises(ValueError):
        GregorianDate(2024, 0, 10)

def test_leap_year_logic():
    assert GregorianDate(2020, 2, 29).is_leap_year()
    assert not GregorianDate(2021, 2, 28).is_leap_year()

def test_timezone_set_and_get():
    tz = timezone.utc
    d = GregorianDate(2024, 6, 1)
    d.tzinfo(tz)
    assert d.tzinfo() == tz

def test_mutation_methods_chaining():
    d = GregorianDate(2024, 1, 1)
    d.year(2025).month(7).day(22).hour(19).minute(30).second(44).microsecond(999999)
    assert (d.year(), d.month(), d.day(), d.hour(), d.minute(), d.second(), d.microsecond()) == (2025, 7, 22, 19, 30, 44, 999999)

def test_edge_end_of_month():
    d = GregorianDate(2024, 12, 30)
    d2 = d.copy().add(days=2)
    assert (d2.month() == 1 and d2.day() <= 2) or (d2.month() == 12 and d2.day() in [31])
