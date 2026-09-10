"""Tests for utility helpers."""

import pytest
from parsidate.utils.helpers import (
    is_leap_year, days_in_month, month_name, weekday_name,
    to_persian_digits, to_english_digits, normalize_date_separator,
    get_season
)


class TestLeapYear:
    def test_jalali_leap(self):
        assert is_leap_year(1403, "jalali") == True
        assert is_leap_year(1402, "jalali") == False

    def test_gregorian_leap(self):
        assert is_leap_year(2024, "gregorian") == True
        assert is_leap_year(2023, "gregorian") == False
        assert is_leap_year(1900, "gregorian") == False
        assert is_leap_year(2000, "gregorian") == True


class TestDaysInMonth:
    def test_jalali_months(self):
        assert days_in_month(1403, 1, "jalali") == 31
        assert days_in_month(1403, 6, "jalali") == 31
        assert days_in_month(1403, 7, "jalali") == 30
        assert days_in_month(1403, 12, "jalali") == 30  # 1403 is leap year

    def test_jalali_leap_month(self):
        assert days_in_month(1403, 12, "jalali") == 30  # Leap year
        assert days_in_month(1402, 12, "jalali") == 29  # Non-leap

    def test_gregorian_months(self):
        assert days_in_month(2024, 1, "gregorian") == 31
        assert days_in_month(2024, 2, "gregorian") == 29  # Leap year
        assert days_in_month(2023, 2, "gregorian") == 28  # Non-leap
        assert days_in_month(2024, 4, "gregorian") == 30


class TestMonthName:
    def test_jalali_en(self):
        assert month_name(1, "en", "jalali") == "Farvardin"

    def test_jalali_fa(self):
        assert month_name(1, "fa", "jalali") == "فروردین"

    def test_gregorian(self):
        assert month_name(1, "en", "gregorian") == "January"


class TestWeekdayName:
    def test_jalali(self):
        assert weekday_name(0, "en", "jalali") == "Shanbe"

    def test_gregorian(self):
        assert weekday_name(0, "en", "gregorian") == "Monday"


class TestDigits:
    def test_to_persian(self):
        assert to_persian_digits("123") == "۱۲۳"

    def test_to_english(self):
        assert to_english_digits("۱۲۳") == "123"


class TestNormalize:
    def test_normalize_separator(self):
        assert normalize_date_separator("2024-11-08") == "2024/11/08"
        assert normalize_date_separator("2024.11.08") == "2024/11/08"
        assert normalize_date_separator("2024_11_08") == "2024/11/08"


class TestSeason:
    def test_jalali_seasons(self):
        assert get_season(1, "jalali") == "Spring"
        assert get_season(4, "jalali") == "Summer"
        assert get_season(7, "jalali") == "Fall"
        assert get_season(10, "jalali") == "Winter"

    def test_gregorian_seasons(self):
        assert get_season(3, "gregorian") == "Spring"
        assert get_season(6, "gregorian") == "Summer"
        assert get_season(9, "gregorian") == "Fall"
        assert get_season(12, "gregorian") == "Winter"
