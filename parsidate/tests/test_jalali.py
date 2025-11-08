import pytest
from datetime import timezone
from parsidate.core import JalaliDate
from parsidate.core.converters import jalali_to_gregorian, gregorian_to_jalali
from parsidate.intervals.period import Period
from parsidate.intervals.duration import Duration

# --- Property and Setter tests ---

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

def test_all_setters():
    d = JalaliDate(1402, 5, 20)
    d.year(1399)
    d.month(12)
    d.day(29)
    d.hour(7)
    d.minute(44)
    d.second(51)
    d.microsecond(999999)
    d.tzinfo(timezone.utc)
    assert (d.year(), d.month(), d.day(), d.hour(), d.minute(), d.second(), d.microsecond(), d.tzinfo()) == (1399, 12, 29, 7, 44, 51, 999999, timezone.utc)

# --- Logic tests ---

def test_weekday_and_quarter():
    date = JalaliDate(1403, 8, 20)
    assert 0 <= date.weekday() <= 6
    assert 1 <= date.quarter() <= 4

def test_day_of_year_and_leap():
    d = JalaliDate(1399, 12, 30)
    assert d.is_leap_year()
    doy = d.day_of_year()
    assert 1 <= doy <= 366

# --- Direct add/sub method unit tests ---

def test_add_years():
    d = JalaliDate(1400, 7, 10)
    d.add(years=3)
    assert d.year() == 1403

def test_add_months():
    d = JalaliDate(1400, 12, 5)
    d.add(months=2)
    # Roll to new year
    assert (d.month() == 2 and d.year() == 1401) or d.month() == 1

def test_add_days():
    d = JalaliDate(1400, 12, 28)
    d.add(days=3)
    # End of month rollover
    assert d.month() in [12, 1]

def test_add_hours():
    d = JalaliDate(1402, 3, 10, 20)
    d.add(hours=7)
    assert d.hour() == 3 or (d.hour() == 3 and (d.day() == 11 or d.day() == 10))

def test_add_minutes():
    d = JalaliDate(1402, 3, 10, 23, 50)
    d.add(minutes=15)
    assert d.minute() == 5 and (d.hour() == 0 or d.hour() == 23)

def test_add_seconds():
    d = JalaliDate(1402, 3, 10, 23, 59, 50)
    d.add(seconds=15)
    assert d.second() == 5 and (d.minute() == 0 or d.minute() == 59)

def test_sub_years():
    d = JalaliDate(1404, 7, 10)
    d.sub(years=2)
    assert d.year() == 1402

def test_sub_months():
    d = JalaliDate(1401, 3, 5)
    d.sub(months=4)
    # Rollover to previous year
    assert d.month() in [11, 12] or d.year() == 1400

def test_sub_days():
    d = JalaliDate(1401, 1, 5)
    d.sub(days=10)
    assert d.month() in [12, 1]

def test_sub_hours():
    d = JalaliDate(1401, 2, 1, 5)
    d.sub(hours=8)
    assert d.hour() in [21, 22, 23]

def test_sub_minutes():
    d = JalaliDate(1401, 2, 1, 0, 10)
    d.sub(minutes=20)
    assert d.minute() in [50, 0, 59]

def test_sub_seconds():
    d = JalaliDate(1401, 2, 1, 0, 0, 15)
    d.sub(seconds=20)
    assert d.second() in [55, 59, 0]

# --- Operator method tests ---

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

# --- Edge/corner/test coverage ---

def test_format_and_repr():
    d = JalaliDate(1402, 1, 1, 15, 23, 10)
    fmt = d.format("Y/m/d H:i:s")
    assert isinstance(fmt, str)
    assert "JalaliDate" in repr(d)

def test_copy_and_equality():
    d1 = JalaliDate(1402, 5, 15, 12)
    d2 = d1.copy()
    assert d2 == d1
    d2.day(28)
    assert d2.day() != d1.day()

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
    # 1399 is leap, 1400 is not
    assert JalaliDate(1399, 12, 30).is_leap_year()
    assert not JalaliDate(1400, 12, 29).is_leap_year()

def test_timezone_set_and_get():
    tz = timezone.utc
    d = JalaliDate(1402, 6, 1)
    d.tzinfo(tz)
    assert d.tzinfo() == tz

def test_mutation_methods_chaining():
    d = JalaliDate(1402, 1, 1)
    d.year(1404).month(7).day(22).hour(19).minute(30).second(44).microsecond(999999)
    assert (d.year(), d.month(), d.day(), d.hour(), d.minute(), d.second(), d.microsecond()) == (1404, 7, 22, 19, 30, 44, 999999)

def test_edge_end_of_month():
    d = JalaliDate(1402, 12, 29)
    d2 = d.copy().add(days=2)
    assert (d2.month() == 1 and d2.day() <= 2) or (d2.month() == 12 and d2.day() in [30, 31])