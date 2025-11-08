"""
Calendar conversion functions for Jalali (Persian) & Gregorian dates.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later

Uses 'jalali' algorithm (from: https://github.com/shobeiry/jalali)
"""

from typing import Tuple
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from datetime import datetime

def gregorian_to_jalali(gy: int, gm: int, gd: int) -> Tuple[int, int, int]:
    """
    Converts a Gregorian date to Jalali (Persian).

    Args:
        gy (int): Gregorian year (e.g. 2024)
        gm (int): Gregorian month (1 - 12)
        gd (int): Gregorian day (1 - 31)

    Returns:
        Tuple[int, int, int]: (jy, jm, jd) - Jalali year, month, day

    Algorithm from: https://github.com/shobeiry/jalali
    """
    g_d_m = [0,31,59,90,120,151,181,212,243,273,304,334]
    if (gy > 1600):
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99)//100) + ((gy2 + 399)//400) - 80 + gd + g_d_m[gm-1]
    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + days // 31
        jd = 1 + (days % 31)
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + ((days - 186) % 30)
    jy += 1
    return (jy, jm, jd)

def jalali_to_gregorian(jy: int, jm: int, jd: int) -> Tuple[int, int, int]:
    """
    Converts a Jalali (Persian) date to Gregorian.

    Args:
        jy (int): Jalali year (e.g. 1403)
        jm (int): Jalali month (1 - 12)
        jd (int): Jalali day (1 - 31)

    Returns:
        Tuple[int, int, int]: (gy, gm, gd) - Gregorian year, month, day

    Algorithm from: https://github.com/shobeiry/jalali
    """
    jy -= 979
    days = 365 * jy + ((jy // 33) * 8) + (((jy % 33) + 3)//4)
    for i in range(1, jm):
        if i <= 6:
            days += 31
        else:
            days += 30
    days += (jd - 1)
    gy = 1600 + 400 * (days // 146097)
    days %= 146097
    leap = True
    if days >= 36525:
        days -= 1
        gy += 100 * (days // 36524)
        days = days % 36524
        if days >= 365:
            days += 1
        else:
            leap = False
    gy += 4 * (days // 1461)
    days %= 1461
    if days >= 366:
        leap = False
        days -= 1
        gy += days // 365
        days = days % 365
    else:
        leap = True
    gd = days + 1
    months = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    if leap:
        months[2] = 29
    gm = 1
    while gd > months[gm]:
        gd -= months[gm]
        gm += 1
    return (gy, gm, gd)

def to_gregorian(jalali_date: JalaliDate) -> GregorianDate:
    """
    Converts a JalaliDate object to GregorianDate.

    Args:
        jalali_date (JalaliDate): Jalali date

    Returns:
        GregorianDate: Equivalent Gregorian date
    """
    jy, jm, jd = jalali_date.year(), jalali_date.month(), jalali_date.day()
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    return GregorianDate(gy, gm, gd,
                         jalali_date.hour(), jalali_date.minute(),
                         jalali_date.second(), jalali_date.microsecond(),
                         jalali_date.tzinfo())

def to_jalali(gregorian_date: GregorianDate) -> JalaliDate:
    """
    Converts a GregorianDate object to JalaliDate.

    Args:
        gregorian_date (GregorianDate): Gregorian date

    Returns:
        JalaliDate: Equivalent Jalali (Persian) date
    """
    gy, gm, gd = (gregorian_date.year(), gregorian_date.month(), gregorian_date.day())
    jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
    return JalaliDate(jy, jm, jd,
                      gregorian_date.hour(), gregorian_date.minute(),
                      gregorian_date.second(), gregorian_date.microsecond(),
                      gregorian_date.tzinfo())
