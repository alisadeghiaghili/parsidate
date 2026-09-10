"""
Calendar conversion functions for Jalali (Persian) & Gregorian dates.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from typing import Tuple
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate


def _is_gregorian_leap_year(year: int) -> bool:
    """Check if a Gregorian year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


G_DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
J_DAYS_IN_MONTH = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]


def gregorian_to_jalali(gy: int, gm: int, gd: int) -> Tuple[int, int, int]:
    """Convert Gregorian date to Jalali (Persian).

    Args:
        gy: Gregorian year (e.g. 2024)
        gm: Gregorian month (1-12)
        gd: Gregorian day (1-31)

    Returns:
        Tuple of (jy, jm, jd) - Jalali year, month, day
    """
    gy = gy - 1600
    gm = gm - 1

    j_day_no = (
        365 * gy
        + (gy + 3) // 4
        - (gy + 99) // 100
        + (gy + 399) // 400
        + gd - 1
        - 79
    )

    for i in range(gm):
        j_day_no += G_DAYS_IN_MONTH[i]

    if gm > 1 and _is_gregorian_leap_year(gy + 1600):
        j_day_no += 1

    j_np = j_day_no // 12053
    j_day_no %= 12053
    jy = 979 + 33 * j_np + 4 * (j_day_no // 1461)
    j_day_no %= 1461

    if j_day_no >= 366:
        j_day_no -= 1
        jy += j_day_no // 365
        j_day_no %= 365

    for i in range(11):
        if not j_day_no >= J_DAYS_IN_MONTH[i]:
            i -= 1
            break
        j_day_no -= J_DAYS_IN_MONTH[i]

    jm = i + 2
    jd = j_day_no + 1

    return (jy, jm, jd)


def jalali_to_gregorian(jy: int, jm: int, jd: int) -> Tuple[int, int, int]:
    """Convert Jalali (Persian) date to Gregorian.

    Args:
        jy: Jalali year (e.g. 1403)
        jm: Jalali month (1-12)
        jd: Jalali day (1-31)

    Returns:
        Tuple of (gy, gm, gd) - Gregorian year, month, day
    """
    jy = jy - 979

    g_day_no = (
        365 * jy
        + (jy // 33) * 8
        + (jy % 33 + 3) // 4
        + jd - 1
        + 79
    )

    for i in range(jm - 1):
        g_day_no += J_DAYS_IN_MONTH[i]

    gy = 1600 + 400 * (g_day_no // 146097)
    g_day_no %= 146097

    leap = 1
    if g_day_no >= 36525:
        g_day_no -= 1
        gy += 100 * (g_day_no // 36524)
        g_day_no %= 36524

        if g_day_no >= 365:
            g_day_no += 1
        else:
            leap = 0

    gy += 4 * (g_day_no // 1461)
    g_day_no %= 1461

    if g_day_no >= 366:
        leap = 0
        g_day_no -= 1
        gy += g_day_no // 365
        g_day_no %= 365

    i = 0
    while g_day_no >= G_DAYS_IN_MONTH[i] + (1 if (i == 1 and leap) else 0):
        g_day_no -= G_DAYS_IN_MONTH[i] + (1 if (i == 1 and leap) else 0)
        i += 1

    gm = i + 1
    gd = g_day_no + 1

    return (gy, gm, gd)


def to_gregorian(jalali_date: JalaliDate) -> GregorianDate:
    """Convert JalaliDate to GregorianDate."""
    jy, jm, jd = jalali_date.year(), jalali_date.month(), jalali_date.day()
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    return GregorianDate(
        gy, gm, gd,
        jalali_date.hour(), jalali_date.minute(),
        jalali_date.second(), jalali_date.microsecond(),
        jalali_date.tzinfo()
    )


def to_jalali(gregorian_date: GregorianDate) -> JalaliDate:
    """Convert GregorianDate to JalaliDate."""
    gy, gm, gd = gregorian_date.year(), gregorian_date.month(), gregorian_date.day()
    jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
    return JalaliDate(
        jy, jm, jd,
        gregorian_date.hour(), gregorian_date.minute(),
        gregorian_date.second(), gregorian_date.microsecond(),
        gregorian_date.tzinfo()
    )
