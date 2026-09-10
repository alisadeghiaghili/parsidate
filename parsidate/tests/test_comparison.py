"""Tests for comparison operations."""

import pytest
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.operations.comparison import (
    eq, ne, lt, le, gt, ge, between, min_date, max_date,
    is_before, is_after, is_between
)


class TestComparison:
    def test_eq(self):
        d1 = JalaliDate(1403, 1, 1)
        d2 = JalaliDate(1403, 1, 1)
        assert eq(d1, d2) == True

    def test_ne(self):
        d1 = JalaliDate(1403, 1, 1)
        d2 = JalaliDate(1403, 1, 2)
        assert ne(d1, d2) == True

    def test_lt(self):
        d1 = JalaliDate(1403, 1, 1)
        d2 = JalaliDate(1403, 1, 2)
        assert lt(d1, d2) == True
        assert lt(d2, d1) == False

    def test_le(self):
        d1 = JalaliDate(1403, 1, 1)
        d2 = JalaliDate(1403, 1, 1)
        assert le(d1, d2) == True
        d3 = JalaliDate(1403, 1, 2)
        assert le(d1, d3) == True

    def test_gt(self):
        d1 = JalaliDate(1403, 1, 2)
        d2 = JalaliDate(1403, 1, 1)
        assert gt(d1, d2) == True

    def test_ge(self):
        d1 = JalaliDate(1403, 1, 1)
        d2 = JalaliDate(1403, 1, 1)
        assert ge(d1, d2) == True

    def test_between_inclusive(self):
        d = JalaliDate(1403, 6, 15)
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 12, 29)
        assert between(d, start, end, inclusive=True) == True

    def test_between_exclusive(self):
        d = JalaliDate(1403, 1, 1)
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 12, 29)
        assert between(d, start, end, inclusive=False) == False

    def test_min_date(self):
        d1 = JalaliDate(1403, 1, 1)
        d2 = JalaliDate(1403, 1, 2)
        d3 = JalaliDate(1403, 1, 3)
        assert min_date(d1, d2, d3) == d1

    def test_max_date(self):
        d1 = JalaliDate(1403, 1, 1)
        d2 = JalaliDate(1403, 1, 2)
        d3 = JalaliDate(1403, 1, 3)
        assert max_date(d1, d2, d3) == d3

    def test_is_before(self):
        d1 = JalaliDate(1403, 1, 1)
        d2 = JalaliDate(1403, 1, 2)
        assert is_before(d1, d2) == True
        assert is_before(d2, d1) == False

    def test_is_after(self):
        d1 = JalaliDate(1403, 1, 2)
        d2 = JalaliDate(1403, 1, 1)
        assert is_after(d1, d2) == True

    def test_is_between(self):
        d = JalaliDate(1403, 6, 15)
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 12, 29)
        assert is_between(d, start, end) == True

    def test_gregorian_comparison(self):
        d1 = GregorianDate(2024, 1, 1)
        d2 = GregorianDate(2024, 1, 2)
        assert is_before(d1, d2) == True
        assert is_after(d2, d1) == True
