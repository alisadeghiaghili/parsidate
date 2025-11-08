import pytest
from parsidate.parsers import (
    jmd,
    ymd,
    jdm,
    dmy,
    parse_jalali,
    parse_gregorian,
    parse_date,
)
from parsidate.core import JalaliDate, GregorianDate

def test_jmd():
    date = jmd("1402/08/19")
    assert isinstance(date, JalaliDate)
    assert date.year() == 1402 and date.month() == 8 and date.day() == 19

def test_ymd():
    date = ymd("2024-11-08")
    assert isinstance(date, GregorianDate)
    assert date.year() == 2024 and date.month() == 11 and date.day() == 8

def test_jdm():
    date = jdm("19-08-1402")
    assert isinstance(date, JalaliDate)
    assert date.year() == 1402 and date.month() == 8 and date.day() == 19

def test_dmy():
    date = dmy("08/11/2024")
    assert isinstance(date, GregorianDate)
    assert date.year() == 2024 and date.month() == 11 and date.day() == 8

def test_parse_jalali_string():
    date = parse_jalali("1401-12-30 14:23:50")
    assert date.year() == 1401 and date.month() == 12 and date.day() == 30
    assert date.hour() == 14 and date.minute() == 23 and date.second() == 50
    date2 = parse_jalali("1350/7/1")
    assert date2.month() == 7 and date2.day() == 1

def test_parse_gregorian_string():
    date = parse_gregorian("2020-02-29 23:59:59")
    assert date.year() == 2020 and date.month() == 2 and date.day() == 29
    assert date.hour() == 23 and date.minute() == 59 and date.second() == 59
    date2 = parse_gregorian("2001/01/01")
    assert date2.month() == 1 and date2.day() == 1

def test_parse_date_auto():
    d1 = parse_date("1402/08/19")
    d2 = parse_date("2024-11-08")
    assert isinstance(d1, JalaliDate)
    assert isinstance(d2, GregorianDate)
    d3 = parse_date("19-08-1402")
    assert isinstance(d3, JalaliDate)
    d4 = parse_date("08/11/2024")
    assert isinstance(d4, GregorianDate)

def test_parse_invalid_format():
    with pytest.raises(ValueError):
        jmd("abcd")
    with pytest.raises(ValueError):
        ymd("19-11-2023")
    with pytest.raises(ValueError):
        parse_date("2025/15/50")
    with pytest.raises(ValueError):
        parse_gregorian("2020/00/12")

def test_leading_trailing_whitespace():
    d1 = jmd("  1400/01/01  ")
    d2 = ymd("\t2020-01-01\n")
    assert d1.year() == 1400 and d2.year() == 2020

def test_time_components():
    d = parse_date("1402/08/19 12:01:32")
    assert d.hour() == 12 and d.minute() == 1 and d.second() == 32
    d2 = parse_gregorian("2020-02-29 00:00:00")
    assert d2.hour() == 0 and d2.minute() == 0 and d2.second() == 0

def test_partial_dates():
    d = jmd("1401/02")
    assert d.year() == 1401 and d.month() == 2
    d2 = ymd("2022-05")
    assert d2.year() == 2022 and d2.month() == 5

def test_parse_edge_dates():
    d = jmd("1399/12/30")
    assert d.day() == 30
    d2 = ymd("2020-02-29")
    assert d2.day() == 29
