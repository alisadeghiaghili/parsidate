"""Tests for rounding operations."""

import pytest
from parsidate.core.jalali import JalaliDate
from parsidate.operations.rounding import (
    floor_to_day, ceil_to_day, floor_to_week, ceil_to_week,
    floor_to_month, ceil_to_month, floor_to_quarter, ceil_to_quarter,
    floor_to_year, ceil_to_year, floor_date, ceiling_date, round_date
)


class TestRounding:
    def test_floor_to_day(self):
        j = JalaliDate(1403, 8, 18, 14, 30, 45)
        j2 = floor_to_day(j)
        assert j2.hour() == 0
        assert j2.minute() == 0
        assert j2.second() == 0

    def test_ceil_to_day(self):
        j = JalaliDate(1403, 8, 18, 14, 30, 45)
        j2 = ceil_to_day(j)
        assert j2.day() == 19
        assert j2.hour() == 0

    def test_ceil_to_day_already_floor(self):
        j = JalaliDate(1403, 8, 18, 0, 0, 0)
        j2 = ceil_to_day(j)
        assert j2.day() == 18

    def test_floor_to_week(self):
        j = JalaliDate(1403, 8, 18)
        j2 = floor_to_week(j, week_start=6)
        assert j2.weekday() == 6

    def test_floor_to_month(self):
        j = JalaliDate(1403, 8, 18)
        j2 = floor_to_month(j)
        assert j2.day() == 1

    def test_ceil_to_month(self):
        j = JalaliDate(1403, 8, 18)
        j2 = ceil_to_month(j)
        assert j2.month() == 9
        assert j2.day() == 1

    def test_ceil_to_month_already_first(self):
        j = JalaliDate(1403, 8, 1, 0, 0, 0)
        j2 = ceil_to_month(j)
        assert j2.month() == 8

    def test_floor_to_quarter(self):
        j = JalaliDate(1403, 8, 18)
        j2 = floor_to_quarter(j)
        assert j2.month() == 7

    def test_ceil_to_quarter(self):
        j = JalaliDate(1403, 8, 18)
        j2 = ceil_to_quarter(j)
        assert j2.month() == 10

    def test_floor_to_year(self):
        j = JalaliDate(1403, 8, 18)
        j2 = floor_to_year(j)
        assert j2.month() == 1
        assert j2.day() == 1

    def test_ceil_to_year(self):
        j = JalaliDate(1403, 8, 18)
        j2 = ceil_to_year(j)
        assert j2.year() == 1404
        assert j2.month() == 1

    def test_floor_date(self):
        j = JalaliDate(1403, 8, 18)
        assert floor_date(j, "day").day() == 18
        assert floor_date(j, "month").day() == 1
        assert floor_date(j, "year").month() == 1

    def test_ceiling_date(self):
        j = JalaliDate(1403, 8, 18)
        j2 = ceiling_date(j, "month")
        assert j2.month() == 9

    def test_round_date(self):
        j = JalaliDate(1403, 8, 15)
        j2 = round_date(j, "month")
        assert j2.month() in [8, 9]

    def test_invalid_unit(self):
        j = JalaliDate(1403, 8, 18)
        with pytest.raises(ValueError):
            floor_date(j, "invalid")
        with pytest.raises(ValueError):
            ceiling_date(j, "invalid")
