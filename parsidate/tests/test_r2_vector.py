"""R2: vectorized calendar conversion (numpy)."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from parsidate.core.converters import gregorian_to_jalali, jalali_to_gregorian

np = pytest.importorskip("numpy")

from parsidate.vector import (  # noqa: E402
    to_jalali_ymd,
    to_gregorian_ymd,
    gregorian_ordinal,
    jalali_from_ordinal,
)


def test_scalar_parity_sample() -> None:
    d = date(1900, 1, 1)
    years, months, days = [], [], []
    while d <= date(2050, 12, 31):
        years.append(d.year)
        months.append(d.month)
        days.append(d.day)
        d += timedelta(days=97)

    jy, jm, jd = to_jalali_ymd(np.array(years), np.array(months), np.array(days))
    for i in range(len(years)):
        exp = gregorian_to_jalali(years[i], months[i], days[i])
        assert (int(jy[i]), int(jm[i]), int(jd[i])) == exp

    gy, gm, gd = to_gregorian_ymd(jy, jm, jd)
    assert gy.tolist() == years
    assert gm.tolist() == months
    assert gd.tolist() == days


def test_nowruz_1403() -> None:
    jy, jm, jd = to_jalali_ymd(np.array([2024]), np.array([3]), np.array([20]))
    assert (int(jy[0]), int(jm[0]), int(jd[0])) == (1403, 1, 1)


def test_int32_dtype() -> None:
    gy = np.array([2024, 2023], dtype=np.int32)
    gm = np.array([3, 11], dtype=np.int32)
    gd = np.array([20, 9], dtype=np.int32)
    jy, jm, jd = to_jalali_ymd(gy, gm, gd)
    assert jy.dtype.kind in "iu"
    assert (int(jy[0]), int(jm[0]), int(jd[0])) == (1403, 1, 1)


def test_roundtrip_hundred_years() -> None:
    start = date(1950, 1, 1)
    n = 365 * 100
    ords = np.arange(start.toordinal(), start.toordinal() + n)
    jy, jm, jd = jalali_from_ordinal(ords)
    gy, gm, gd = to_gregorian_ymd(jy, jm, jd)
    back = gregorian_ordinal(gy, gm, gd)
    assert np.array_equal(back, ords)


def test_leap_esfand_30() -> None:
    # 1399/12/30 exists
    gy, gm, gd = to_gregorian_ymd(np.array([1399]), np.array([12]), np.array([30]))
    assert (int(gy[0]), int(gm[0]), int(gd[0])) == (2021, 3, 20)
    jy, jm, jd = to_jalali_ymd(np.array([2021]), np.array([3]), np.array([20]))
    assert (int(jy[0]), int(jm[0]), int(jd[0])) == (1399, 12, 30)


def test_empty_input() -> None:
    empty = np.array([], dtype=np.int64)
    jy, jm, jd = to_jalali_ymd(empty, empty, empty)
    assert jy.size == 0


def test_mismatched_shapes_raise() -> None:
    with pytest.raises(ValueError):
        to_jalali_ymd(np.array([2024, 2023]), np.array([3]), np.array([1, 1]))


def test_faster_than_python_loop_on_50k() -> None:
    import time

    n = 50_000
    base = date(2000, 1, 1).toordinal()
    ords = np.arange(base, base + n)
    # vector path
    t0 = time.perf_counter()
    jy, jm, jd = jalali_from_ordinal(ords)
    t_vec = time.perf_counter() - t0
    # python path
    t0 = time.perf_counter()
    for o in ords[:5000]:
        dd = date.fromordinal(int(o))
        gregorian_to_jalali(dd.year, dd.month, dd.day)
    t_py = time.perf_counter() - t0
    # vectorizing 50k should not be slower than 5k python rows by more than 5x
    # (loose gate — still proves it is not accidental O(n) python)
    assert t_vec < max(t_py * 5, 0.05)
