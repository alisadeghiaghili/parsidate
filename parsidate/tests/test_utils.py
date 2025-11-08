import pytest
from parsidate.utils.helpers import (
    days_in_month,
    is_gregorian_leap,
    is_jalali_leap,
    validate_jalali,
    validate_gregorian,
)
from parsidate.core import JalaliDate, GregorianDate

def test_days_in_month_gregorian():
    assert days_in_month(2024, 2, "gregorian") == 29
    assert days_in_month(2023, 2, "gregorian") == 28
    assert days_in_month(2020, 4, "gregorian") == 30
    assert days_in_month(2020, 1, "gregorian") == 31

def test_days_in_month_jalali():
    assert days_in_month(1402, 12, "jalali") in [29, 30]
    assert days_in_month(1400, 1, "jalali") == 31
    assert days_in_month(1400, 7, "jalali") == 30

def test_is_gregorian_leap():
    assert is_gregorian_leap(2020)
    assert not is_gregorian_leap(2021)
    assert is_gregorian_leap(2000)
    assert not is_gregorian_leap(2100)

def test_is_jalali_leap():
    assert is_jalali_leap(1399)
    assert not is_jalali_leap(1400)
    assert is_jalali_leap(1364) or is_jalali_leap(1370) or is_jalali_leap(1391)

def test_validate_jalali():
    assert validate_jalali(1390, 8, 22)
    assert validate_jalali(1399, 12, 30)
    assert not validate_jalali(1390, 13, 1)
    assert not validate_jalali(1390, 12, 32)
    assert not validate_jalali(1390, 0, 1)

def test_validate_gregorian():
    assert validate_gregorian(2023, 8, 17)
    assert validate_gregorian(2020, 2, 29)
    assert not validate_gregorian(2021, 2, 29)
    assert not validate_gregorian(2021, 13, 10)
    assert not validate_gregorian(2021, 0, 10)

def test_days_in_month_invalid_calendar():
    with pytest.raises(ValueError):
        days_in_month(2024, 8, "viking")

def test_days_in_month_invalid_date():
    with pytest.raises(ValueError):
        days_in_month(2020, 13, "gregorian")
    with pytest.raises(ValueError):
        days_in_month(1400, 13, "jalali")

def test_leap_consistency_with_date_classes():
    # Cross-check leap property from helpers with class instances
    jd = JalaliDate(1399, 12, 30)
    gd = GregorianDate(2020, 2, 29)
    assert is_jalali_leap(jd.year()) == jd.is_leap_year()
    assert is_gregorian_leap(gd.year()) == gd.is_leap_year()

def test_days_in_month_vs_class_validation():
    for y, m in [(1399, 12), (1402, 1), (1402, 7)]:
        max_day = days_in_month(y, m, "jalali")
        assert validate_jalali(y, m, max_day)
    for y, m in [(2020, 2), (2021, 2), (2024, 2)]:
        max_day = days_in_month(y, m, "gregorian")
        assert validate_gregorian(y, m, max_day)

def test_edge_invalid_jalali_and_gregorian():
    # Test with values below min year/month/day boundaries
    assert not validate_jalali(1, 1, 1)
    assert not validate_gregorian(1, 1, 1)
