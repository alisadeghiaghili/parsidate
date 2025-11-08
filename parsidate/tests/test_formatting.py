import pytest
from parsidate.formatting import (
    format_jalali_date,
    format_gregorian_date,
    format_full,
    format_short,
    format_iso,
    format_date_custom,
)
from parsidate.core import JalaliDate, GregorianDate

def test_format_jalali_default():
    date = JalaliDate(1402, 8, 19, 13, 5, 7)
    res = format_jalali_date(date)
    assert isinstance(res, str)
    assert "1402" in res

def test_format_gregorian_default():
    date = GregorianDate(2024, 11, 8, 23, 45, 12)
    res = format_gregorian_date(date)
    assert isinstance(res, str)
    assert "2024" in res

def test_format_full_jalali():
    date = JalaliDate(1402, 8, 19, 14, 32)
    res = format_full(date, locale="fa")
    assert "جمعه" in res or "Friday" in res

def test_format_full_gregorian():
    date = GregorianDate(2024, 11, 8, 14, 32)
    res = format_full(date, locale="en")
    assert "Friday" in res

def test_format_short_jalali():
    date = JalaliDate(1402, 8, 19)
    res = format_short(date, locale="fa")
    assert "1402/08/19" in res or "۱۴۰۲/۰۸/۱۹" in res

def test_format_short_gregorian():
    date = GregorianDate(2024, 11, 8)
    res = format_short(date, locale="en")
    assert "2024-11-08" in res

def test_format_iso_jalali():
    date = JalaliDate(1402, 8, 19, 5, 3, 7)
    res = format_iso(date)
    assert "T" in res and res.startswith("1402-08-19T")

def test_format_iso_gregorian():
    date = GregorianDate(2024, 11, 8, 17, 15, 55)
    res = format_iso(date)
    assert res.startswith("2024-11-08T")

def test_format_date_custom_jalali():
    date = JalaliDate(1402, 8, 19, 13, 5, 7)
    res = format_date_custom(date, "Y/m/d H:i:s", locale="fa")
    assert res.startswith("1402/08/19") or res.startswith("۱۴۰۲/۰۸/۱۹")

def test_format_date_custom_gregorian():
    date = GregorianDate(2024, 11, 8, 23, 45, 12)
    res = format_date_custom(date, "Y-m-d H:i:s", locale="en")
    assert res.startswith("2024-11-08")

def test_format_with_locale_en_and_fa():
    date = JalaliDate(1402, 8, 19)
    en_string = format_full(date, locale="en")
    fa_string = format_full(date, locale="fa")
    assert isinstance(en_string, str) and isinstance(fa_string, str)
    assert (("Friday" in en_string) or ("جمعه" in fa_string))

def test_format_edge_cases():
    date = JalaliDate(1399, 12, 30, 23, 59, 59)
    res = format_iso(date)
    assert res.endswith("T23:59:59")
    date2 = GregorianDate(2020, 2, 29, 0, 0, 0)
    res2 = format_date_custom(date2, "Y-m-d", locale="en")
    assert res2 == "2020-02-29"
