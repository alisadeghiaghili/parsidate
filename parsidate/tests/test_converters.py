import pytest
from parsidate.core.converters import (
    jalali_to_gregorian,
    gregorian_to_jalali,
    jalali_to_jdn,
    gregorian_to_jdn,
    jdn_to_jalali,
    jdn_to_gregorian,
)
from parsidate.core import JalaliDate, GregorianDate

# --- Jalali ↔ Gregorian: Simple and round-trip tests ---

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

# --- JDN conversion and round-trip ---

def test_jalali_to_jdn_roundtrip():
    jy, jm, jd = 1300, 1, 1
    jdn = jalali_to_jdn(jy, jm, jd)
    jy2, jm2, jd2 = jdn_to_jalali(jdn)
    assert (jy, jm, jd) == (jy2, jm2, jd2)

def test_gregorian_to_jdn_roundtrip():
    gy, gm, gd = 1970, 1, 1
    jdn = gregorian_to_jdn(gy, gm, gd)
    gy2, gm2, gd2 = jdn_to_gregorian(jdn)
    assert (gy, gm, gd) == (gy2, gm2, gd2)

def test_jdn_to_jalali_and_gregorian():
    # Use JDN of a known date
    jdn = gregorian_to_jdn(2023, 11, 10)
    jy, jm, jd = jdn_to_jalali(jdn)
    gy, gm, gd = jdn_to_gregorian(jdn)
    # Ensure conversions agree
    assert jalali_to_gregorian(jy, jm, jd) == (gy, gm, gd)

# --- Date object helpers ---

def test_convert_with_date_objects():
    jdate = JalaliDate(1398, 12, 29)
    gdate = GregorianDate(2020, 3, 19)
    g_tuple = jalali_to_gregorian(jdate.year(), jdate.month(), jdate.day())
    j_tuple = gregorian_to_jalali(gdate.year(), gdate.month(), gdate.day())
    assert all(isinstance(i, int) for i in g_tuple+j_tuple)

# --- Leap year and edge cases ---

def test_leap_years():
    # Jalali leap: 1399/12/30 → Gregorian (2021/3/20)
    jy, jm, jd = 1399, 12, 30
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    jy2, jm2, jd2 = gregorian_to_jalali(gy, gm, gd)
    assert (jy, jm, jd) == (jy2, jm2, jd2)
    # Gregorian leap: 2016/2/29
    gy, gm, gd = 2016, 2, 29
    jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
    gy2, gm2, gd2 = jalali_to_gregorian(jy, jm, jd)
    assert (gy, gm, gd) == (gy2, gm2, gd2)

# --- Month/Day boundaries ---

def test_month_day_conversion():
    # Start/end of month
    assert jalali_to_gregorian(1400, 1, 1)
    assert gregorian_to_jalali(2022, 5, 31)

def test_invalid_jalali_inputs():
    with pytest.raises(ValueError):
        jalali_to_gregorian(1405, 13, 1)
    with pytest.raises(ValueError):
        jalali_to_gregorian(1402, 12, 32)
    with pytest.raises(ValueError):
        jalali_to_gregorian(1402, 0, 1)

def test_invalid_gregorian_inputs():
    with pytest.raises(ValueError):
        gregorian_to_jalali(2020, 13, 10)
    with pytest.raises(ValueError):
        gregorian_to_jalali(2020, 0, 10)
    with pytest.raises(ValueError):
        gregorian_to_jalali(2020, 4, 31)

def test_invalid_jdn():
    with pytest.raises(ValueError):
        jdn_to_jalali(-10000)
    with pytest.raises(ValueError):
        jdn_to_gregorian(-10000)

# --- Property, mutation, string, equality, edge ---

def test_conversion_property_methods():
    # Ensure int->tuple conversion works for valid range
    for jy, jm, jd in [(1360, 1, 1), (1402, 8, 19), (1386, 6, 31)]:
        gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
        jy2, jm2, jd2 = gregorian_to_jalali(gy, gm, gd)
        assert (jy, jm, jd) == (jy2, jm2, jd2)

def test_repr_and_str():
    # JDN numerics
    jdn = jalali_to_jdn(1402, 8, 19)
    assert isinstance(str(jdn), str)
    jy, jm, jd = jdn_to_jalali(jdn)
    rep = f"{jy}/{jm}/{jd}"
    assert "/" in rep
