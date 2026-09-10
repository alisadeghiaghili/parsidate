"""Tests for converters module."""

import pytest
from parsidate.core.converters import (
    jalali_to_gregorian,
    gregorian_to_jalali,
    to_jalali,
    to_gregorian,
)
from parsidate.core import JalaliDate, GregorianDate


def test_jalali_to_gregorian_basic():
    jy, jm, jd = 1402, 8, 19
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    assert isinstance(gy, int) and isinstance(gm, int) and isinstance(gd, int)


def test_gregorian_to_jalali_basic():
    gy, gm, gd = 2023, 11, 10
    jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
    assert isinstance(jy, int) and isinstance(jm, int) and isinstance(jd, int)


def test_roundtrip_jalali_gregorian():
    jy, jm, jd = 1401, 2, 25
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    jy2, jm2, jd2 = gregorian_to_jalali(gy, gm, gd)
    assert (jy2, jm2, jd2) == (jy, jm, jd)


def test_roundtrip_gregorian_jalali():
    gy, gm, gd = 2020, 2, 29
    jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
    gy2, gm2, gd2 = jalali_to_gregorian(jy, jm, jd)
    assert (gy2, gm2, gd2) == (gy, gm, gd)


def test_convert_with_date_objects():
    jdate = JalaliDate(1398, 12, 29)
    gdate = GregorianDate(2020, 3, 19)
    g_tuple = jalali_to_gregorian(jdate.year(), jdate.month(), jdate.day())
    j_tuple = gregorian_to_jalali(gdate.year(), gdate.month(), gdate.day())
    assert all(isinstance(i, int) for i in g_tuple + j_tuple)


def test_leap_years():
    jy, jm, jd = 1399, 12, 30
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    jy2, jm2, jd2 = gregorian_to_jalali(gy, gm, gd)
    assert (jy, jm, jd) == (jy2, jm2, jd2)


def test_month_day_conversion():
    assert jalali_to_gregorian(1400, 1, 1)
    assert gregorian_to_jalali(2022, 5, 31)


def test_known_date():
    jy, jm, jd = 1403, 1, 1
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    assert gy == 2024
    assert gm == 3
    assert gd == 20


def test_to_jalali():
    g = GregorianDate(2024, 3, 20)
    j = to_jalali(g)
    assert j.year() == 1403
    assert j.month() == 1
    assert j.day() == 1


def test_to_gregorian():
    j = JalaliDate(1403, 1, 1)
    g = to_gregorian(j)
    assert g.year() == 2024
    assert g.month() == 3
    assert g.day() == 20
