"""Vectorized Jalali ↔ Gregorian conversion for numpy integer arrays.

Implementation mirrors the scalar algorithms in
:mod:`parsidate.core.converters` using vector operations only.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from typing import Tuple

import numpy as np

__all__ = [
    "to_jalali_ymd",
    "to_gregorian_ymd",
    "gregorian_ordinal",
    "jalali_from_ordinal",
]

_G_DAYS = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], dtype=np.int64)
_J_DAYS = np.array([31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29], dtype=np.int64)
_G_CUM = np.concatenate([[0], np.cumsum(_G_DAYS)])  # len 13
_J_CUM = np.concatenate([[0], np.cumsum(_J_DAYS)])


def _as_int64(a) -> np.ndarray:
    arr = np.asarray(a, dtype=np.int64)
    return np.atleast_1d(arr)


def _check_same_shape(*arrays: np.ndarray) -> None:
    shape = arrays[0].shape
    for a in arrays[1:]:
        if a.shape != shape:
            raise ValueError(f"Array shapes must match, got {shape} and {a.shape}")


def _is_gregorian_leap(year: np.ndarray) -> np.ndarray:
    return ((year % 4 == 0) & (year % 100 != 0)) | (year % 400 == 0)


def gregorian_ordinal(gy: np.ndarray, gm: np.ndarray, gd: np.ndarray) -> np.ndarray:
    """Return proleptic Gregorian ordinals (same as ``datetime.date.toordinal``).

    Args:
        gy: Gregorian years.
        gm: Months 1-12.
        gd: Days 1-31.

    Returns:
        int64 ordinals, shape matching inputs.

    Example:
        >>> import numpy as np
        >>> from parsidate.vector import gregorian_ordinal
        >>> int(gregorian_ordinal(np.array([1]), np.array([1]), np.array([1]))[0])
        1
    """
    gy = _as_int64(gy)
    gm = _as_int64(gm)
    gd = _as_int64(gd)
    _check_same_shape(gy, gm, gd)
    # Hinnant days_from_civil → shift to Python ordinal (0001-01-01 = 1)
    y = gy - np.where(gm <= 2, 1, 0)
    era = np.where(y >= 0, y, y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (np.where(gm > 2, gm - 3, gm + 9)) + 2) // 5 + gd - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    # days since 1970-01-01 + offset of that day in Python ordinals
    return (era * 146097 + doe - 719468 + 719163).astype(np.int64)


def to_jalali_ymd(
    gy: np.ndarray,
    gm: np.ndarray,
    gd: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert Gregorian Y/M/D arrays to Jalali Y/M/D arrays.

    Args:
        gy: Gregorian year array.
        gm: Gregorian month array (1-12).
        gd: Gregorian day array (1-31).

    Returns:
        Tuple ``(jy, jm, jd)`` of int64 arrays.

    Raises:
        ValueError: If input shapes differ.

    Example:
        >>> import numpy as np
        >>> from parsidate.vector import to_jalali_ymd
        >>> jy, jm, jd = to_jalali_ymd(np.array([2024]), np.array([3]), np.array([20]))
        >>> int(jy[0]), int(jm[0]), int(jd[0])
        (1403, 1, 1)
    """
    gy = _as_int64(gy)
    gm = _as_int64(gm)
    gd = _as_int64(gd)
    _check_same_shape(gy, gm, gd)

    gy0 = gy - 1600
    gm0 = gm - 1
    leap = _is_gregorian_leap(gy)

    # days from month starts (vectorized equivalent of the scalar for-loop)
    g_month_days = np.where(
        leap[:, None],
        _G_DAYS + np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int64),
        _G_DAYS,
    )
    # sum of days in months 0..gm-1
    g_cum = np.cumsum(g_month_days, axis=1)
    prefix = np.where(gm0 > 0, g_cum[np.arange(gm0.shape[0]), np.clip(gm0 - 1, 0, 11)], 0)

    j_day_no = (
        365 * gy0
        + (gy0 + 3) // 4
        - (gy0 + 99) // 100
        + (gy0 + 399) // 400
        + gd
        - 1
        - 79
        + prefix
    )

    j_np = j_day_no // 12053
    j_day_no = j_day_no % 12053
    jy = 979 + 33 * j_np + 4 * (j_day_no // 1461)
    j_day_no = j_day_no % 1461

    after_leap = j_day_no >= 366
    j_day_no = np.where(after_leap, j_day_no - 1, j_day_no)
    jy = np.where(after_leap, jy + j_day_no // 365, jy)
    j_day_no = np.where(after_leap, j_day_no % 365, j_day_no)

    # month index: number of complete months in j_day_no (max 11)
    j_cum11 = np.cumsum(_J_DAYS[:11])
    month_idx = np.searchsorted(j_cum11, j_day_no, side="right").astype(np.int64)
    day_in_month = j_day_no - np.where(month_idx > 0, j_cum11[np.clip(month_idx - 1, 0, 10)], 0)

    jm = month_idx + 1
    # scalar algorithm ends with i=10 (month 12) if loop finishes
    # searchsorted handles that: day_no >= sum(11 months) → month_idx=11, jm=12
    jd = day_in_month + 1
    return jy.astype(np.int64), jm.astype(np.int64), jd.astype(np.int64)


def to_gregorian_ymd(
    jy: np.ndarray,
    jm: np.ndarray,
    jd: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert Jalali Y/M/D arrays to Gregorian Y/M/D arrays.

    Args:
        jy: Jalali year array.
        jm: Jalali month array (1-12).
        jd: Jalali day array (1-31).

    Returns:
        Tuple ``(gy, gm, gd)`` of int64 arrays.

    Raises:
        ValueError: If input shapes differ.

    Example:
        >>> import numpy as np
        >>> from parsidate.vector import to_gregorian_ymd
        >>> gy, gm, gd = to_gregorian_ymd(np.array([1403]), np.array([1]), np.array([1]))
        >>> int(gy[0]), int(gm[0]), int(gd[0])
        (2024, 3, 20)
    """
    jy = _as_int64(jy)
    jm = _as_int64(jm)
    jd = _as_int64(jd)
    _check_same_shape(jy, jm, jd)

    jy0 = jy - 979
    prefix = np.where(
        jm > 1,
        np.concatenate([[0], np.cumsum(_J_DAYS[:11])])[np.clip(jm - 1, 0, 11)],
        0,
    )

    g_day_no = 365 * jy0 + (jy0 // 33) * 8 + (jy0 % 33 + 3) // 4 + jd - 1 + 79 + prefix

    gy = 1600 + 400 * (g_day_no // 146097)
    g_day_no = g_day_no % 146097

    leap = np.ones_like(g_day_no)
    big = g_day_no >= 36525
    gd_tmp = np.where(big, g_day_no - 1, g_day_no)
    gy = np.where(big, gy + 100 * (gd_tmp // 36524), gy)
    gd_tmp = np.where(big, gd_tmp % 36524, gd_tmp)
    leap = np.where(big & (gd_tmp < 365), 0, leap)
    g_day_no = np.where(big & (gd_tmp >= 365), gd_tmp + 1, gd_tmp)

    gy = gy + 4 * (g_day_no // 1461)
    g_day_no = g_day_no % 1461

    after = g_day_no >= 366
    g_day_no = np.where(after, g_day_no - 1, g_day_no)
    gy = np.where(after, gy + g_day_no // 365, gy)
    g_day_no = np.where(after, g_day_no % 365, g_day_no)
    leap = np.where(after, 0, leap)

    # month walk with leap February
    month_len = _G_DAYS + leap[:, None] * np.array(
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int64
    )
    cum = np.cumsum(month_len, axis=1)  # (n, 12)
    month_idx = (g_day_no[:, None] >= cum).sum(axis=1).astype(np.int64)
    day_in_month = g_day_no - np.where(
        month_idx > 0, cum[np.arange(len(gy)), np.clip(month_idx - 1, 0, 11)], 0
    )
    gm = month_idx + 1
    gd = day_in_month + 1
    return gy.astype(np.int64), gm.astype(np.int64), gd.astype(np.int64)


def jalali_from_ordinal(ordinals: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert Gregorian ordinals to Jalali Y/M/D.

    Args:
        ordinals: int array of proleptic Gregorian ordinals.

    Returns:
        Tuple ``(jy, jm, jd)``.

    Example:
        >>> import numpy as np
        >>> from parsidate.vector import jalali_from_ordinal, gregorian_ordinal
        >>> o = gregorian_ordinal(np.array([2024]), np.array([3]), np.array([20]))
        >>> jy, jm, jd = jalali_from_ordinal(o)
        >>> int(jy[0]), int(jm[0]), int(jd[0])
        (1403, 1, 1)
    """
    ords = _as_int64(ordinals)
    # Python ordinal → days since 1970-01-01 (ordinal 719163), then Hinnant shift
    z = ords - 719163 + 719468
    era = np.where(z >= 0, z, z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = np.where(mp < 10, mp + 3, mp - 9)
    y = np.where(m <= 2, y + 1, y)
    return to_jalali_ymd(y, m, d)
