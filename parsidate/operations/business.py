"""Business-day arithmetic for Jalali and Gregorian dates.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence, Tuple, Union

from parsidate.core.gregorian import GregorianDate
from parsidate.core.jalali import JalaliDate
from parsidate.holidays.ir import IRAN_DEFAULT_WEEKEND, iran_holidays
from parsidate.holidays.registry import HolidaySet

DateLike = Union[JalaliDate, GregorianDate]


def _default_weekend(date: DateLike) -> Tuple[int, ...]:
    """Return default weekend weekday indices for a date type.

    Jalali uses Saturday=0 .. Friday=6 (Iran: Friday).
    Gregorian uses Python weekday Monday=0 .. Sunday=6 (Sat+Sun).
    """
    if isinstance(date, JalaliDate):
        return IRAN_DEFAULT_WEEKEND
    return (5, 6)


def _as_holiday_set(
    holidays: Optional[Union[HolidaySet, Iterable[JalaliDate]]],
    date: DateLike,
    use_iran_default: bool,
) -> HolidaySet:
    if holidays is None:
        if use_iran_default and isinstance(date, JalaliDate):
            return iran_holidays(date.year())
        return HolidaySet()
    if isinstance(holidays, HolidaySet):
        return holidays
    return HolidaySet(dates=list(holidays))


def is_business_day(
    date: DateLike,
    weekend: Optional[Sequence[int]] = None,
    holidays: Optional[Union[HolidaySet, Iterable[JalaliDate]]] = None,
    use_iran_holidays: bool = True,
) -> bool:
    """Return whether a date is a business day.

    Args:
        date: JalaliDate or GregorianDate.
        weekend: Weekday indices treated as weekend. Defaults: Jalali Friday
            (``(6,)``); Gregorian Saturday+Sunday (``(5, 6)`` in Python numbering).
        holidays: Extra holiday set/dates. For Jalali, defaults to official
            Iranian holidays of that year when ``use_iran_holidays`` is True.
        use_iran_holidays: Apply bundled Iranian holidays for Jalali dates
            when ``holidays`` is ``None``.

    Returns:
        ``True`` if not weekend and not holiday.

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> from parsidate.operations.business import is_business_day
        >>> is_business_day(JalaliDate(1403, 1, 5))  # Sunday after Nowruz
        True
    """
    wd = date.weekday()
    wk = tuple(weekend) if weekend is not None else _default_weekend(date)
    if wd in wk:
        return False
    if isinstance(date, JalaliDate):
        hs = _as_holiday_set(holidays, date, use_iran_holidays)
        return date not in hs
    return True


def networkdays(
    start: DateLike,
    end: DateLike,
    weekend: Optional[Sequence[int]] = None,
    holidays: Optional[Union[HolidaySet, Iterable[JalaliDate]]] = None,
    inclusive_end: bool = True,
    use_iran_holidays: bool = True,
) -> int:
    """Count business days from ``start`` to ``end``.

    Args:
        start: Inclusive start date.
        end: End date.
        weekend: Weekend weekday indices (see :func:`is_business_day`).
        holidays: Holiday set or dates.
        inclusive_end: Include ``end`` when it is a business day (default True).
        use_iran_holidays: Apply bundled Iranian holidays for Jalali when
            ``holidays`` is ``None``.

    Returns:
        Number of business days (0 if ``end`` < ``start``).

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> from parsidate.operations.business import networkdays
        >>> networkdays(JalaliDate(1403, 1, 5), JalaliDate(1403, 1, 5))
        1
    """
    if end < start:
        return 0
    count = 0
    current = start.copy()
    last = end.copy()
    # iterate inclusive range
    while current < end or current == end:
        at_end = current == end
        if at_end and not inclusive_end:
            break
        if is_business_day(
            current, weekend=weekend, holidays=holidays, use_iran_holidays=use_iran_holidays
        ):
            count += 1
        if at_end:
            break
        current = current.add(days=1)
    return count


def add_business_days(
    date: DateLike,
    n: int,
    weekend: Optional[Sequence[int]] = None,
    holidays: Optional[Union[HolidaySet, Iterable[JalaliDate]]] = None,
    use_iran_holidays: bool = True,
) -> DateLike:
    """Add ``n`` business days to a date.

    If the start date is a weekend/holiday it is first moved forward
    (for ``n > 0``) or backward (for ``n < 0``) to a business day, then
    ``n`` steps are applied.

    Args:
        date: Start date.
        n: Signed number of business days to add.
        weekend: Weekend weekday indices.
        holidays: Holiday set or dates.
        use_iran_holidays: Apply bundled Iranian holidays for Jalali.

    Returns:
        New date of the same type.

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> from parsidate.operations.business import add_business_day
        >>> add_business_days(JalaliDate(1403, 1, 5), 1)
        JalaliDate(1403, 1, 6, 0, 0, 0)
    """
    if n == 0:
        return date.copy()

    step = 1 if n > 0 else -1
    remaining = abs(n)
    current = date.copy()

    # Excel WORKDAY-compatible: count only business days stepped over.
    # A non-business start is not pre-rolled; the first step lands on the
    # next business day when n=1.
    while remaining > 0:
        current = current.add(days=step)
        if is_business_day(
            current, weekend=weekend, holidays=holidays, use_iran_holidays=use_iran_holidays
        ):
            remaining -= 1
    return current


def next_business_day(
    date: DateLike,
    weekend: Optional[Sequence[int]] = None,
    holidays: Optional[Union[HolidaySet, Iterable[JalaliDate]]] = None,
    use_iran_holidays: bool = True,
) -> DateLike:
    """Return the next business day strictly after ``date``.

    Args:
        date: Starting date.
        weekend: Weekend weekday indices.
        holidays: Holiday set or dates.
        use_iran_holidays: Apply bundled Iranian holidays for Jalali.

    Returns:
        Next business day.

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> from parsidate.operations.business import next_business_day
        >>> next_business_day(JalaliDate(1403, 1, 3))  # Friday + Nowruz
        JalaliDate(1403, 1, 5, 0, 0, 0)
    """
    current = date.add(days=1)
    while not is_business_day(
        current, weekend=weekend, holidays=holidays, use_iran_holidays=use_iran_holidays
    ):
        current = current.add(days=1)
    return current


def prev_business_day(
    date: DateLike,
    weekend: Optional[Sequence[int]] = None,
    holidays: Optional[Union[HolidaySet, Iterable[JalaliDate]]] = None,
    use_iran_holidays: bool = True,
) -> DateLike:
    """Return the previous business day strictly before ``date``.

    Args:
        date: Starting date.
        weekend: Weekend weekday indices.
        holidays: Holiday set or dates.
        use_iran_holidays: Apply bundled Iranian holidays for Jalali.

    Returns:
        Previous business day.

    Example:
        >>> from parsidate.core.jalali import JalaliDate
        >>> from parsidate.operations.business import prev_business_day
        >>> prev_business_day(JalaliDate(1403, 1, 3))  # Friday
        JalaliDate(1403, 1, 2, 0, 0, 0)
    """
    current = date.add(days=-1)
    while not is_business_day(
        current, weekend=weekend, holidays=holidays, use_iran_holidays=use_iran_holidays
    ):
        current = current.add(days=-1)
    return current
