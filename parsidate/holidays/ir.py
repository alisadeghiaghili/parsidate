"""Iranian official holiday tables.

Fixed Solar Hijri (Jalali) holidays always apply. Lunar-dependent
(Islamic) holidays are stored as **published official Jalali dates**
per year — not computed from astronomy.

Coverage is declared by :data:`LUNAR_COVERAGE_YEARS`. Requesting a year
outside solar-fixed handling without lunar rows still returns solar
holidays; use :func:`holidays_in_year` for the full official set when
data exists.

Sources for lunar rows: annual official Iranian government calendars
(time.ir / IRIB announcements). Update procedure: extend
:data:`LUNAR_HOLIDAYS` and bump :data:`~parsidate.holidays.registry.DATA_VERSION`.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from parsidate.core.jalali import JalaliDate
from parsidate.holidays.registry import HolidayDataMissing, HolidaySet

# Jalali weekday: 0=Saturday .. 6=Friday
IRAN_DEFAULT_WEEKEND: Tuple[int, ...] = (6,)

# Fixed solar holidays: (month, day, name_en, name_fa)
_FIXED_SOLAR: Tuple[Tuple[int, int, str, str], ...] = (
    (1, 1, "Nowruz", "جشن نوروز"),
    (1, 2, "Nowruz", "جشن نوروز"),
    (1, 3, "Nowruz", "جشن نوروز"),
    (1, 4, "Nowruz", "جشن نوروز"),
    (1, 12, "Islamic Republic Day", "روز جمهوری اسلامی"),
    (1, 13, "Nature Day", "روز طبیعت"),
    (3, 15, "Khordad 15 Uprising", "قیام ۱۵ خرداد"),
    (11, 22, "Victory of Islamic Revolution", "پیروزی انقلاب اسلامی"),
    (12, 29, "Nationalization of Oil", "ملی شدن صنعت نفت"),
)

# Lunar (Islamic) official holidays as published Jalali dates.
# (month, day, name_en, name_fa) — only years with curated rows.
LUNAR_HOLIDAYS: Dict[int, Tuple[Tuple[int, int, str, str], ...]] = {
    1402: (
        (2, 25, "Martyrdom of Imam Ali", "شهادت امام علی"),
        (3, 4, "Eid al-Fitr", "عید سعید فطر"),
        (3, 5, "Eid al-Fitr", "عید سعید فطر"),
        (4, 22, "Day of Arafah", "روز عرفه"),
        (4, 23, "Eid al-Adha", "عید سعید قربان"),
        (5, 1, "Tasu'a", "تاسوعای حسینی"),
        (5, 2, "Ashura", "عاشورای حسینی"),
        (6, 12, "Arba'een", "اربعین حسینی"),
        (7, 11, "Death of Prophet / Martyrdom Imam Hasan", "رحلت رسول اکرم و شهادت امام حسن"),
        (7, 13, "Martyrdom of Imam Reza", "شهادت امام رضا"),
        (8, 1, "Martyrdom of Imam Hasan Askari", "شهادت امام حسن عسکری"),
        (8, 13, "Birthday of Prophet / Imam Jafar Sadeq", "میلاد رسول اکرم و امام جعفر صادق"),
    ),
    1403: (
        (4, 25, "Tasu'a", "تاسوعای حسینی"),
        (4, 26, "Ashura", "عاشورای حسینی"),
        (6, 6, "Arba'een", "اربعین حسینی"),
        (7, 15, "Death of Prophet / Martyrdom Imam Hasan", "رحلت رسول اکرم و شهادت امام حسن"),
        (7, 17, "Martyrdom of Imam Reza", "شهادت امام رضا"),
        (8, 5, "Martyrdom of Imam Hasan Askari", "شهادت امام حسن عسکری"),
        (9, 2, "Birthday of Prophet / Imam Jafar Sadeq", "میلاد رسول اکرم و امام جعفر صادق"),
    ),
    1404: (
        (1, 10, "Eid al-Fitr", "عید سعید فطر"),
        (1, 11, "Eid al-Fitr", "عید سعید فطر"),
        (2, 16, "Eid al-Adha", "عید سعید قربان"),
        (3, 24, "Tasu'a", "تاسوعای حسینی"),
        (3, 25, "Ashura", "عاشورای حسینی"),
    ),
}

#: Years with curated lunar holiday rows.
LUNAR_COVERAGE_YEARS: Tuple[int, ...] = tuple(sorted(LUNAR_HOLIDAYS))


def iran_fixed_solar_holidays(year: int) -> List[JalaliDate]:
    """Return fixed (non-lunar) Iranian holidays for a Jalali year.

    Args:
        year: Jalali year.

    Returns:
        List of holiday dates (Nowruz, 12/13 Farvardin, 15 Khordad, 22 Bahman, 29 Esfand).

    Example:
        >>> from parsidate.holidays import iran_fixed_solar_holidays
        >>> len(iran_fixed_solar_holidays(1403)) >= 6
        True
    """
    from parsidate.utils.helpers import days_in_month

    out: List[JalaliDate] = []
    for month, day, _en, _fa in _FIXED_SOLAR:
        if day <= days_in_month(year, month, "jalali"):
            out.append(JalaliDate(year, month, day))
    return out


def iran_lunar_holidays(year: int) -> List[JalaliDate]:
    """Return curated lunar-dependent official holidays for a year.

    Args:
        year: Jalali year with bundled data.

    Returns:
        List of published holiday dates.

    Raises:
        HolidayDataMissing: If the year has no curated lunar rows.

    Example:
        >>> from parsidate.holidays import iran_lunar_holidays
        >>> iran_lunar_holidays(1403)[0].month() >= 1
        True
    """
    if year not in LUNAR_HOLIDAYS:
        raise HolidayDataMissing(
            f"No lunar holiday data for {year}. "
            f"Covered years: {list(LUNAR_COVERAGE_YEARS)}. "
            f"Use iran_fixed_solar_holidays() or add custom HolidaySet rows."
        )
    return [JalaliDate(year, m, d) for m, d, _en, _fa in LUNAR_HOLIDAYS[year]]


def iran_holidays(year: int, include_lunar: bool = True) -> HolidaySet:
    """Return the official Iranian holiday set for a Jalali year.

    Args:
        year: Jalali year.
        include_lunar: Include curated lunar rows when available.

    Returns:
        HolidaySet with solar and (optionally) lunar holidays.

    Example:
        >>> from parsidate.holidays import iran_holidays
        >>> from parsidate.core.jalali import JalaliDate
        >>> JalaliDate(1403, 1, 1) in iran_holidays(1403)
        True
    """
    dates: List[JalaliDate] = list(iran_fixed_solar_holidays(year))
    if include_lunar and year in LUNAR_HOLIDAYS:
        dates.extend(iran_lunar_holidays(year))
    return HolidaySet(dates=dates)


def holidays_in_year(year: int, include_lunar: bool = True) -> List[JalaliDate]:
    """Return official holidays for a year as a list of dates.

    Args:
        year: Jalali year.
        include_lunar: Include curated lunar holidays if present.

    Returns:
        Sorted unique holiday dates.

    Example:
        >>> from parsidate.holidays import holidays_in_year
        >>> holidays_in_year(1403)[0].day()
        1
    """
    return list(iran_holidays(year, include_lunar=include_lunar).dates)


def is_holiday(
    date: JalaliDate,
    extra: HolidaySet | None = None,
    include_lunar: bool = True,
) -> bool:
    """Return whether a Jalali date is an official Iranian holiday.

    Args:
        date: Date to test.
        extra: Optional additional holidays (e.g. company closures).
        include_lunar: Consider bundled lunar holidays for that year.

    Returns:
        ``True`` if the date is a holiday.

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> from parsidate.holidays import is_holiday
        >>> is_holiday(JalaliDate(1403, 1, 1))
        True
    """
    year = date.year()
    base = iran_holidays(year, include_lunar=include_lunar)
    if date in base:
        return True
    if extra is not None and date in extra:
        return True
    return False
