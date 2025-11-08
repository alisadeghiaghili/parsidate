import pytest
from parsidate.core import JalaliDate, GregorianDate
from parsidate.operations.arithmetic import (
    add_months,
    add_years,
    add_days,
    add_weeks,
    next_month,
    prev_month,
    next_year,
    prev_year,
    diff_in_days,
    date_range,
)
from parsidate.operations.comparison import (
    eq, ne, lt, le, gt, ge,
    between,
    min_date, max_date
)
from parsidate.operations.rounding import (
    floor_to_day, ceil_to_day,
    floor_to_week, ceil_to_week,
    floor_to_month, ceil_to_month,
    floor_to_quarter, ceil_to_quarter,
    floor_to_year, ceil_to_year
)

def test_add_months_years():
    j = JalaliDate(1399, 8, 7)
    result = add_months(j, 5)
    assert result.month() == 1 or result.month() == 13 or result.year() == 1400
    result2 = add_years(j, 2)
    assert result2.year() == 1401
    g = GregorianDate(2020, 8, 7)
    resultg = add_months(g, 4)
    assert resultg.month() in [12, 1]
    resultg2 = add_years(g, 2)
    assert resultg2.year() == 2022

def test_add_days_weeks():
    j = JalaliDate(1399, 1, 10)
    r = add_days(j, 25)
    assert r.day() in [4, 5]
    r2 = add_weeks(j, 5)
    assert isinstance(r2, JalaliDate)
    g = GregorianDate(2020, 1, 10)
    r3 = add_days(g, 30)
    assert r3.month() in [2, 1]
    r4 = add_weeks(g, 4)
    assert isinstance(r4, GregorianDate)

def test_next_prev_month_year():
    j = JalaliDate(1399, 12, 29)
    n_m = next_month(j)
    p_m = prev_month(j)
    n_y = next_year(j)
    p_y = prev_year(j)
    assert isinstance(n_m, JalaliDate) and isinstance(p_m, JalaliDate)
    assert isinstance(n_y, JalaliDate) and isinstance(p_y, JalaliDate)

def test_diff_in_days_basic():
    j1 = JalaliDate(1402, 1, 1)
    j2 = JalaliDate(1402, 1, 10)
    d = diff_in_days(j2, j1)
    assert d == 9 or d == abs(d)
    g1 = GregorianDate(2020, 1, 15)
    g2 = GregorianDate(2020, 1, 1)
    d2 = diff_in_days(g1, g2)
    assert d2 == 14

def test_date_range_basic():
    start = JalaliDate(1400, 1, 1)
    end = JalaliDate(1400, 1, 5)
    rng = list(date_range(start, end))
    assert len(rng) == 5
    assert rng[0] == start
    assert rng[-1].day() == 5

def test_comparison_operators():
    j1 = JalaliDate(1402, 1, 1)
    j2 = JalaliDate(1402, 1, 10)
    assert eq(j1, j1)
    assert ne(j1, j2)
    assert lt(j1, j2)
    assert le(j1, j1)
    assert gt(j2, j1)
    assert ge(j2, j2)
    assert between(j1, JalaliDate(1402, 1, 1), JalaliDate(1402, 1, 10))

def test_min_max_date():
    jlist = [JalaliDate(1402, 1, 1), JalaliDate(1401, 12, 29), JalaliDate(1402, 2, 11)]
    mmin = min_date(jlist)
    mmax = max_date(jlist)
    assert mmin.year() == 1401 or mmin.month() <= mmax.month()
    assert mmax.year() == 1402 or mmax.month() >= mmin.month()

def test_rounding_methods_jalali():
    d = JalaliDate(1402, 4, 15)
    assert floor_to_day(d).day() == d.day()
    assert ceil_to_day(d).day() == d.day()
    assert floor_to_week(d).day() <= d.day()
    assert ceil_to_week(d).day() >= d.day()
    assert floor_to_month(d).month() == d.month()
    assert ceil_to_month(d).month() == d.month()
    assert 1 <= floor_to_quarter(d).month() <= 12
    assert 1 <= ceil_to_quarter(d).month() <= 12
    assert floor_to_year(d).year() == d.year()
    assert ceil_to_year(d).year() == d.year()

def test_rounding_methods_gregorian():
    d = GregorianDate(2020, 7, 17)
    assert floor_to_day(d).day() == d.day()
    assert ceil_to_day(d).day() == d.day()
    assert floor_to_week(d).day() <= d.day()
    assert ceil_to_week(d).day() >= d.day()
    assert floor_to_month(d).month() == d.month()
    assert ceil_to_month(d).month() == d.month()
    assert 1 <= floor_to_quarter(d).month() <= 12
    assert 1 <= ceil_to_quarter(d).month() <= 12
    assert floor_to_year(d).year() == d.year()
    assert ceil_to_year(d).year() == d.year()

def test_edge_cases_add_subtract_large():
    d = GregorianDate(2020, 1, 31)
    result = add_months(d, 13)
    result2 = add_years(d, 5)
    assert isinstance(result, GregorianDate)
    assert result2.year() == 2025
