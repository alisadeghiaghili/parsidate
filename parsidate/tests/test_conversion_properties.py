"""Property-style tests for calendar conversion (hypothesis optional)."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from parsidate.core.converters import gregorian_to_jalali, jalali_to_gregorian
from parsidate.core.jalali import JalaliDate
from parsidate.utils.helpers import days_in_month, is_leap_year

try:
    from hypothesis import given, settings, strategies as st
except ImportError:  # pragma: no cover
    st = None


MIN_ORD = date(1900, 1, 1).toordinal()
MAX_ORD = date(2100, 12, 31).toordinal()


def _jalali_year_bounds_ok(jy: int) -> None:
    total = sum(days_in_month(jy, m, "jalali") for m in range(1, 13))
    assert total == (366 if is_leap_year(jy, "jalali") else 365)


@pytest.mark.parametrize("jy", range(1300, 1501))
def test_jalali_year_lengths(jy: int) -> None:
    _jalali_year_bounds_ok(jy)


def test_month_lengths_match_converter_spans() -> None:
    for jy in range(1390, 1411):
        for jm in range(1, 13):
            g0 = jalali_to_gregorian(jy, jm, 1)
            if jm < 12:
                g1 = jalali_to_gregorian(jy, jm + 1, 1)
            else:
                g1 = jalali_to_gregorian(jy + 1, 1, 1)
            actual = (date(*g1) - date(*g0)).days
            assert actual == days_in_month(jy, jm, "jalali")


def test_add_sub_inverse_sample() -> None:
    base = JalaliDate(1403, 6, 15, 12, 0, 0)
    for n in range(-40, 41, 7):
        moved = base.add(days=n)
        back = moved.add(days=-n)
        assert back == base


if st is not None:

    @settings(max_examples=200, deadline=None)
    @given(ordinal=st.integers(min_value=MIN_ORD, max_value=MAX_ORD))
    def test_property_roundtrip_ordinal(ordinal: int) -> None:
        d = date.fromordinal(ordinal)
        jy, jm, jd = gregorian_to_jalali(d.year, d.month, d.day)
        gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
        assert (gy, gm, gd) == (d.year, d.month, d.day)

    @settings(max_examples=100, deadline=None)
    @given(
        jy=st.integers(min_value=1300, max_value=1499),
        offset=st.integers(min_value=0, max_value=364),
    )
    def test_property_jalali_add_days_matches_ordinal(jy: int, offset: int) -> None:
        start_g = jalali_to_gregorian(jy, 1, 1)
        start = JalaliDate(jy, 1, 1)
        moved = start.add(days=offset)
        expected = date(*start_g) + timedelta(days=offset)
        jy2, jm2, jd2 = gregorian_to_jalali(expected.year, expected.month, expected.day)
        assert (moved.year(), moved.month(), moved.day()) == (jy2, jm2, jd2)
else:

    def test_hypothesis_optional() -> None:
        pytest.skip("hypothesis not installed; dense deterministic tests still cover conversion")
