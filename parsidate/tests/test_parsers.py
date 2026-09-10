"""Tests for parsers module."""

import pytest
from parsidate.parsers.parse import (
    jmd, jdm, jmdy, jdmy, jmd_hms, ymd, dmy, mdy, ydm, ymd_hms,
    parse_date, now_jalali, now_gregorian, today_jalali, today_gregorian,
    parse_jalali, parse_gregorian
)
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate


class TestJalaliParsers:
    def test_jmd(self):
        j = jmd("1403/08/18")
        assert j.year() == 1403
        assert j.month() == 8
        assert j.day() == 18

    def test_jmd_with_separator(self):
        j = jmd("1403-08-18")
        assert j.year() == 1403

    def test_jdm(self):
        j = jdm("18/08/1403")
        assert j.year() == 1403
        assert j.day() == 18

    def test_jmd_hms(self):
        j = jmd_hms("1403/08/18 14:30:25")
        assert j.hour() == 14
        assert j.minute() == 30
        assert j.second() == 25

    def test_jmd_with_persian_digits(self):
        j = jmd("۱۴۰۳/۰۸/۱۸")
        assert j.year() == 1403


class TestGregorianParsers:
    def test_ymd(self):
        g = ymd("2024/11/08")
        assert g.year() == 2024
        assert g.month() == 11
        assert g.day() == 8

    def test_ymd_with_dash(self):
        g = ymd("2024-11-08")
        assert g.year() == 2024

    def test_dmy(self):
        g = dmy("08/11/2024")
        assert g.year() == 2024
        assert g.day() == 8

    def test_mdy(self):
        g = mdy("11/08/2024")
        assert g.year() == 2024
        assert g.month() == 11

    def test_ymd_hms(self):
        g = ymd_hms("2024/11/08 14:30:25")
        assert g.hour() == 14
        assert g.minute() == 30
        assert g.second() == 25


class TestSmartParser:
    def test_parse_jalali(self):
        j = parse_jalali("1403/08/18")
        assert isinstance(j, JalaliDate)
        assert j.year() == 1403

    def test_parse_gregorian(self):
        g = parse_gregorian("2024-11-08")
        assert isinstance(g, GregorianDate)
        assert g.year() == 2024

    def test_parse_date_auto_detect(self):
        j = parse_date("1403/08/18")
        assert isinstance(j, JalaliDate)

    def test_parse_date_gregorian(self):
        g = parse_date("2024/11/08", calendar="gregorian")
        assert isinstance(g, GregorianDate)


class TestNowFunctions:
    def test_now_jalali(self):
        j = now_jalali()
        assert isinstance(j, JalaliDate)
        assert j.year() > 1300

    def test_now_gregorian(self):
        g = now_gregorian()
        assert isinstance(g, GregorianDate)
        assert g.year() > 2000

    def test_today_jalali(self):
        j = today_jalali()
        assert j.hour() == 0
        assert j.minute() == 0

    def test_today_gregorian(self):
        g = today_gregorian()
        assert g.hour() == 0
        assert g.minute() == 0

    def test_now_jalali_with_tz(self):
        j = now_jalali(tz="UTC")
        assert isinstance(j, JalaliDate)

    def test_now_gregorian_with_tz(self):
        g = now_gregorian(tz="UTC")
        assert isinstance(g, GregorianDate)

    def test_today_jalali_with_tz(self):
        j = today_jalali(tz="UTC")
        assert j.hour() == 0

    def test_today_gregorian_with_tz(self):
        g = today_gregorian(tz="UTC")
        assert g.hour() == 0


class TestExtraParsers:
    def test_jmdy(self):
        j = jmdy("08/18/1403")
        assert j.year() == 1403
        assert j.month() == 8
        assert j.day() == 18

    def test_jdmy(self):
        j = jdmy("18/08/1403")
        assert j.year() == 1403
        assert j.day() == 18

    def test_ydm(self):
        g = ydm("2024/08/11")
        assert g.year() == 2024
        assert g.day() == 8

    def test_ymd_hms_without_time(self):
        g = ymd_hms("2024/11/08")
        assert g.hour() == 0
        assert g.minute() == 0
        assert g.second() == 0

    def test_jmd_hms_without_time(self):
        j = jmd_hms("1403/08/18")
        assert j.hour() == 0

    def test_parse_date_gregorian_fallback(self):
        g = parse_date("2024/11/08")
        assert isinstance(g, GregorianDate)

    def test_parse_date_invalid(self):
        with pytest.raises(ValueError):
            parse_date("invalid")

    def test_parse_jalali_with_time(self):
        j = parse_jalali("1403/08/18 14:30:25")
        assert j.hour() == 14
        assert j.minute() == 30

    def test_parse_jalali_without_time(self):
        j = parse_jalali("1403/08/18")
        assert j.hour() == 0

    def test_parse_gregorian_with_time(self):
        g = parse_gregorian("2024-11-08 14:30:25")
        assert g.hour() == 14

    def test_parse_gregorian_without_time(self):
        g = parse_gregorian("2024-11-08")
        assert g.hour() == 0

    def test_jmd_with_tz(self):
        j = jmd("1403/08/18", tz="UTC")
        assert j.tzinfo() is not None

    def test_ymd_with_tz(self):
        g = ymd("2024/11/08", tz="UTC")
        assert g.tzinfo() is not None

    def test_parse_jalali_with_tz(self):
        j = parse_jalali("1403/08/18", tz="UTC")
        assert j.tzinfo() is not None

    def test_parse_gregorian_with_tz(self):
        g = parse_gregorian("2024-11-08", tz="UTC")
        assert g.tzinfo() is not None
