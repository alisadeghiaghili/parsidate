"""Tests for arithmetic operations."""

import pytest
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.operations.arithmetic import (
    add_months, add_years, diff_in_days, next_month, prev_month,
    next_year, prev_year, add_days, add_weeks, date_range
)


class TestArithmetic:
    def test_add_months(self):
        j = JalaliDate(1403, 1, 15)
        j2 = add_months(j, 1)
        assert j2.month() == 2
        assert j2.day() == 15

    def test_add_months_year_boundary(self):
        j = JalaliDate(1403, 12, 15)
        j2 = add_months(j, 1)
        assert j2.year() == 1404
        assert j2.month() == 1

    def test_add_years(self):
        j = JalaliDate(1403, 1, 1)
        j2 = add_years(j, 1)
        assert j2.year() == 1404

    def test_diff_in_days(self):
        j1 = JalaliDate(1403, 1, 10)
        j2 = JalaliDate(1403, 1, 1)
        diff = diff_in_days(j1, j2)
        assert diff == 9

    def test_next_month(self):
        j = JalaliDate(1403, 1, 1)
        j2 = next_month(j)
        assert j2.month() == 2

    def test_prev_month(self):
        j = JalaliDate(1403, 2, 1)
        j2 = prev_month(j)
        assert j2.month() == 1

    def test_next_year(self):
        j = JalaliDate(1403, 1, 1)
        j2 = next_year(j)
        assert j2.year() == 1404

    def test_prev_year(self):
        j = JalaliDate(1403, 1, 1)
        j2 = prev_year(j)
        assert j2.year() == 1402

    def test_add_days(self):
        j = JalaliDate(1403, 1, 1)
        j2 = add_days(j, 5)
        assert j2.day() == 6

    def test_add_weeks(self):
        j = JalaliDate(1403, 1, 1)
        j2 = add_weeks(j, 1)
        assert j2.day() == 8

    def test_date_range(self):
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 5)
        dates = list(date_range(start, end))
        assert len(dates) == 5

    def test_gregorian_arithmetic(self):
        g = GregorianDate(2024, 1, 1)
        g2 = add_months(g, 1)
        assert g2.month() == 2
        g3 = add_years(g, 1)
        assert g3.year() == 2025
