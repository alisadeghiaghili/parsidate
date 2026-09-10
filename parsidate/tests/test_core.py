"""Tests for core JalaliDate and GregorianDate classes."""

import pytest
from datetime import datetime, timezone, timedelta
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.core.converters import gregorian_to_jalali, jalali_to_gregorian


class TestJalaliDate:
    def test_creation(self):
        j = JalaliDate(1403, 1, 1)
        assert j.year() == 1403
        assert j.month() == 1
        assert j.day() == 1

    def test_creation_with_time(self):
        j = JalaliDate(1403, 1, 1, 14, 30, 45)
        assert j.hour() == 14
        assert j.minute() == 30
        assert j.second() == 45

    def test_invalid_month(self):
        with pytest.raises(ValueError):
            JalaliDate(1403, 13, 1)

    def test_invalid_day(self):
        with pytest.raises(ValueError):
            JalaliDate(1403, 1, 32)

    def test_invalid_hour(self):
        with pytest.raises(ValueError):
            JalaliDate(1403, 1, 1, 25)

    def test_copy(self):
        j1 = JalaliDate(1403, 1, 1)
        j2 = j1.copy()
        j3 = j2.add(days=5)
        assert j1.day() == 1
        assert j2.day() == 1  # copy returns new object, original unchanged
        assert j3.day() == 6  # add returns new object

    def test_add_days(self):
        j = JalaliDate(1403, 1, 1)
        j2 = j.add(days=5)
        assert j2.day() == 6

    def test_add_months(self):
        j = JalaliDate(1403, 1, 15)
        j2 = j.add(months=1)
        assert j2.month() == 2
        assert j2.day() == 15

    def test_add_months_year_boundary(self):
        j = JalaliDate(1403, 12, 15)
        j2 = j.add(months=1)
        assert j2.year() == 1404
        assert j2.month() == 1

    def test_sub_days(self):
        j = JalaliDate(1403, 1, 10)
        j2 = j.sub(days=5)
        assert j2.day() == 5

    def test_comparison(self):
        j1 = JalaliDate(1403, 1, 1)
        j2 = JalaliDate(1403, 1, 2)
        assert j1 < j2
        assert j2 > j1
        assert j1 <= j1
        assert j1 >= j1

    def test_equality(self):
        j1 = JalaliDate(1403, 1, 1, 14, 30)
        j2 = JalaliDate(1403, 1, 1, 14, 30)
        assert j1 == j2

    def test_hash(self):
        j1 = JalaliDate(1403, 1, 1)
        j2 = JalaliDate(1403, 1, 1)
        assert hash(j1) == hash(j2)
        assert len({j1, j2}) == 1

    def test_strftime(self):
        j = JalaliDate(1403, 8, 18, 14, 45, 30)
        assert j.strftime("%Y/%m/%d", locale="en") == "1403/08/18"
        assert j.strftime("%H:%M:%S", locale="en") == "14:45:30"

    def test_str(self):
        j = JalaliDate(1403, 8, 18, 14, 45, 30)
        s = str(j)
        assert "1403" in s
        assert "08" in s

    def test_repr(self):
        j = JalaliDate(1403, 8, 18, 14, 45, 30)
        r = repr(j)
        assert "JalaliDate" in r
        assert "1403" in r

    def test_weekday(self):
        j = JalaliDate(1403, 1, 1)
        wd = j.weekday()
        assert 0 <= wd <= 6

    def test_quarter(self):
        assert JalaliDate(1403, 1, 1).quarter() == 1
        assert JalaliDate(1403, 4, 1).quarter() == 2
        assert JalaliDate(1403, 7, 1).quarter() == 3
        assert JalaliDate(1403, 10, 1).quarter() == 4

    def test_day_of_year(self):
        j = JalaliDate(1403, 1, 1)
        assert j.day_of_year() == 1
        j2 = JalaliDate(1403, 2, 1)
        assert j2.day_of_year() == 32

    def test_is_leap_year(self):
        assert JalaliDate(1403, 1, 1).is_leap_year() == True
        assert JalaliDate(1402, 1, 1).is_leap_year() == False

    def test_to_gregorian(self):
        j = JalaliDate(1403, 1, 1)
        g = j.to_gregorian()
        assert g[0] == 2024
        assert g[1] == 3
        assert g[2] == 20

    def test_replace(self):
        j = JalaliDate(1403, 1, 1)
        j2 = j.replace(day=15)
        assert j.day() == 1
        assert j2.day() == 15


class TestGregorianDate:
    def test_creation(self):
        g = GregorianDate(2024, 1, 1)
        assert g.year() == 2024
        assert g.month() == 1
        assert g.day() == 1

    def test_creation_with_time(self):
        g = GregorianDate(2024, 1, 1, 14, 30, 45)
        assert g.hour() == 14
        assert g.minute() == 30
        assert g.second() == 45

    def test_copy(self):
        g1 = GregorianDate(2024, 1, 1)
        g2 = g1.copy()
        g3 = g2.add(days=5)
        assert g1.day() == 1
        assert g2.day() == 1
        assert g3.day() == 6

    def test_add_days(self):
        g = GregorianDate(2024, 1, 1)
        g2 = g.add(days=5)
        assert g2.day() == 6

    def test_add_months(self):
        g = GregorianDate(2024, 1, 15)
        g2 = g.add(months=1)
        assert g2.month() == 2
        assert g2.day() == 15

    def test_sub_days(self):
        g = GregorianDate(2024, 1, 10)
        g2 = g.sub(days=5)
        assert g2.day() == 5

    def test_comparison(self):
        g1 = GregorianDate(2024, 1, 1)
        g2 = GregorianDate(2024, 1, 2)
        assert g1 < g2
        assert g2 > g1

    def test_equality(self):
        g1 = GregorianDate(2024, 1, 1, 14, 30)
        g2 = GregorianDate(2024, 1, 1, 14, 30)
        assert g1 == g2

    def test_hash(self):
        g1 = GregorianDate(2024, 1, 1)
        g2 = GregorianDate(2024, 1, 1)
        assert hash(g1) == hash(g2)

    def test_is_leap_year(self):
        assert GregorianDate(2024, 1, 1).is_leap_year() == True
        assert GregorianDate(2023, 1, 1).is_leap_year() == False

    def test_weekday(self):
        g = GregorianDate(2024, 1, 1)
        wd = g.weekday()
        assert 0 <= wd <= 6

    def test_quarter(self):
        assert GregorianDate(2024, 1, 1).quarter() == 1
        assert GregorianDate(2024, 4, 1).quarter() == 2
        assert GregorianDate(2024, 7, 1).quarter() == 3
        assert GregorianDate(2024, 10, 1).quarter() == 4

    def test_to_datetime(self):
        g = GregorianDate(2024, 1, 1, 14, 30)
        dt = g.to_datetime()
        assert isinstance(dt, datetime)
        assert dt.year == 2024


class TestConverters:
    def test_gregorian_to_jalali(self):
        jy, jm, jd = gregorian_to_jalali(2024, 3, 20)
        assert jy == 1403
        assert jm == 1
        assert jd == 1

    def test_jalali_to_gregorian(self):
        gy, gm, gd = jalali_to_gregorian(1403, 1, 1)
        assert gy == 2024
        assert gm == 3
        assert gd == 20

    def test_roundtrip(self):
        jy, jm, jd = 1403, 8, 18
        gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
        jy2, jm2, jd2 = gregorian_to_jalali(gy, gm, gd)
        assert (jy, jm, jd) == (jy2, jm2, jd2)
