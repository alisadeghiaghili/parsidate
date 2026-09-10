"""Tests for intervals/arithmetic module."""

from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.intervals.arithmetic import (
    add_months, add_years, diff_in_days, next_month, prev_month,
    next_year, prev_year, add_days, add_weeks, date_range
)


def test_add_months_jalali():
    j = JalaliDate(1403, 1, 15)
    j2 = add_months(j, 1)
    assert j2.month() == 2
    assert j2.day() == 15


def test_add_months_gregorian():
    g = GregorianDate(2024, 1, 15)
    g2 = add_months(g, 1)
    assert g2.month() == 2


def test_add_years_jalali():
    j = JalaliDate(1403, 1, 1)
    j2 = add_years(j, 1)
    assert j2.year() == 1404


def test_add_years_gregorian():
    g = GregorianDate(2024, 1, 1)
    g2 = add_years(g, 1)
    assert g2.year() == 2025


def test_diff_in_days():
    j1 = JalaliDate(1403, 1, 10)
    j2 = JalaliDate(1403, 1, 1)
    assert diff_in_days(j1, j2) == 9


def test_next_month():
    j = JalaliDate(1403, 1, 1)
    j2 = next_month(j)
    assert j2.month() == 2


def test_prev_month():
    j = JalaliDate(1403, 2, 1)
    j2 = prev_month(j)
    assert j2.month() == 1


def test_next_year():
    j = JalaliDate(1403, 1, 1)
    j2 = next_year(j)
    assert j2.year() == 1404


def test_prev_year():
    j = JalaliDate(1403, 1, 1)
    j2 = prev_year(j)
    assert j2.year() == 1402


def test_add_days():
    j = JalaliDate(1403, 1, 1)
    j2 = add_days(j, 5)
    assert j2.day() == 6


def test_add_weeks():
    j = JalaliDate(1403, 1, 1)
    j2 = add_weeks(j, 1)
    assert j2.day() == 8


def test_date_range():
    start = JalaliDate(1403, 1, 1)
    end = JalaliDate(1403, 1, 5)
    dates = list(date_range(start, end))
    assert len(dates) == 5


def test_date_range_with_step():
    start = JalaliDate(1403, 1, 1)
    end = JalaliDate(1403, 1, 10)
    dates = list(date_range(start, end, step_days=2))
    assert len(dates) == 5
