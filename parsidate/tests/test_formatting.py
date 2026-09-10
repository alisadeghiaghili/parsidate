"""Tests for formatting module."""

import pytest
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.formatting.formatters import (
    to_persian_digits, to_english_digits,
    format_jalali_date, format_gregorian_date
)
from parsidate.formatting.locales import (
    get_month_name, get_weekday_name, PERSIAN_DIGITS, ENGLISH_DIGITS
)


class TestDigitConversion:
    def test_to_persian_digits(self):
        result = to_persian_digits("12345")
        assert result == "۱۲۳۴۵"

    def test_to_english_digits(self):
        result = to_english_digits("۱۲۳۴۵")
        assert result == "12345"


class TestJalaliFormatting:
    def test_format_year_month_day(self):
        j = JalaliDate(1403, 8, 18)
        result = j.strftime("%Y/%m/%d", locale="en")
        assert result == "1403/08/18"

    def test_format_time(self):
        j = JalaliDate(1403, 8, 18, 14, 45, 30)
        result = j.strftime("%H:%M:%S", locale="en")
        assert result == "14:45:30"

    def test_format_persian_locale(self):
        j = JalaliDate(1403, 8, 18)
        result = j.strftime("%B", locale="fa")
        assert result == "آبان"

    def test_format_persian_digits(self):
        j = JalaliDate(1403, 8, 18)
        result = j.strftime("%Y/%m/%d", locale="fa")
        assert "۱۴۰۳" in result

    def test_format_weekday(self):
        j = JalaliDate(1403, 1, 1)
        result = j.strftime("%A")
        assert result is not None


class TestGregorianFormatting:
    def test_format_year_month_day(self):
        g = GregorianDate(2024, 11, 8)
        result = g.strftime("%Y-%m-%d")
        assert result == "2024-11-08"

    def test_format_month_name(self):
        g = GregorianDate(2024, 11, 8)
        result = g.strftime("%B")
        assert result == "November"

    def test_format_weekday(self):
        g = GregorianDate(2024, 1, 1)
        result = g.strftime("%A")
        assert result == "Monday"


class TestLocales:
    def test_get_month_name_jalali_en(self):
        name = get_month_name(1, "en", "jalali")
        assert name == "Farvardin"

    def test_get_month_name_jalali_fa(self):
        name = get_month_name(1, "fa", "jalali")
        assert name == "فروردین"

    def test_get_month_name_gregorian(self):
        name = get_month_name(1, "en", "gregorian")
        assert name == "January"

    def test_get_weekday_name(self):
        name = get_weekday_name(0, "en", "jalali")
        assert name == "Shanbe"

    def test_invalid_month(self):
        with pytest.raises(ValueError):
            get_month_name(13, "en", "jalali")

    def test_invalid_weekday(self):
        with pytest.raises(ValueError):
            get_weekday_name(7, "en", "jalali")
