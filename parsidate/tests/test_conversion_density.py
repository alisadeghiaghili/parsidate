"""Dense conversion correctness tests (no external property library)."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from parsidate.core.converters import gregorian_to_jalali, jalali_to_gregorian


def test_roundtrip_dense_modern_range() -> None:
    """Every day from 1900-01-01 to 2100-12-31 must round-trip."""
    d = date(1900, 1, 1)
    end = date(2100, 12, 31)
    checked = 0
    while d <= end:
        jy, jm, jd = gregorian_to_jalali(d.year, d.month, d.day)
        gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
        assert (gy, gm, gd) == (d.year, d.month, d.day), (
            f"roundtrip failed at {d} -> {(jy, jm, jd)} -> {(gy, gm, gd)}"
        )
        checked += 1
        d += timedelta(days=1)
    assert checked > 70000


def test_known_nowruz_dates() -> None:
    """Spot-check official Nowruz / historical anchors."""
    cases = [
        ((1403, 1, 1), (2024, 3, 20)),
        ((1400, 1, 1), (2021, 3, 21)),
        ((1399, 12, 30), (2021, 3, 20)),
        ((1357, 11, 22), (1979, 2, 11)),
    ]
    for j, g in cases:
        assert jalali_to_gregorian(*j) == g
        assert gregorian_to_jalali(*g) == j


@pytest.mark.parametrize("jy", list(range(1300, 1500, 7)))
def test_year_boundaries_are_contiguous(jy: int) -> None:
    """Farvardin 1 of year+1 is the day after Esfand's last day."""
    g0 = jalali_to_gregorian(jy, 1, 1)
    g1 = jalali_to_gregorian(jy + 1, 1, 1)
    span = (date(*g1) - date(*g0)).days
    assert span in (365, 366)
