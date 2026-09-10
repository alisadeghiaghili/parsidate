"""Persian written-date parsing (``۱۸ آبان ۱۴۰۳``).

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

import re
import warnings
from typing import Optional

from parsidate.core.gregorian import GregorianDate
from parsidate.core.jalali import JalaliDate
from parsidate.formatting.locales import (
    PERSIAN_MONTH_NAMES_FA,
    PERSIAN_MONTH_NAMES_EN,
    PERSIAN_MONTH_NAMES_SHORT_EN,
    PERSIAN_WEEKDAY_NAMES_FA,
    GREGORIAN_MONTH_NAMES_EN,
)
from parsidate.utils.helpers import to_english_digits

__all__ = ["parse_fa", "parse_gregorian_fa"]

_FA_MONTHS = {name: i + 1 for i, name in enumerate(PERSIAN_MONTH_NAMES_FA)}
_EN_MONTHS = {name.lower(): i + 1 for i, name in enumerate(PERSIAN_MONTH_NAMES_EN)}
_EN_MONTHS_SHORT = {name.lower(): i + 1 for i, name in enumerate(PERSIAN_MONTH_NAMES_SHORT_EN)}
_FA_WEEKDAYS = {name: i for i, name in enumerate(PERSIAN_WEEKDAY_NAMES_FA)}
_GREG_EN_MONTHS = {name.lower(): i + 1 for i, name in enumerate(GREGORIAN_MONTH_NAMES_EN)}

_NUM = r"([0-9]{1,4})"


def _month_map(strict_month: bool):
    m = dict(_FA_MONTHS)
    m.update(_EN_MONTHS)
    if not strict_month:
        m.update(_EN_MONTHS_SHORT)
    return m


def parse_fa(
    text: str,
    *,
    strict_month: bool = True,
    check_weekday: bool = True,
    tz: Optional[str] = None,
) -> JalaliDate:
    """Parse a Persian written Jalali date.

    Accepts:

    - ``۱۸ آبان ۱۴۰۳`` / ``18 Aban 1403``
    - ``شنبه ۱ فروردین ۱۴۰۳`` (optional weekday prefix)
    - ``۱۴۰۳/۰۸/۱۸`` numeric

    Args:
        text: Input string (Persian or English digits).
        strict_month: Require full month names (default). If False, allow
            English 3-letter abbreviations.
        check_weekday: If a weekday prefix is present and does not match
            the date, emit a ``UserWarning``.
        tz: Optional IANA timezone name attached to the result.

    Returns:
        Parsed :class:`~parsidate.core.jalali.JalaliDate`.

    Raises:
        ValueError: If the string cannot be parsed.

    Example:
        >>> from parsidate.parsers import parse_fa
        >>> parse_fa("۱۸ آبان ۱۴۰۳").day()
        18
    """
    raw = text.strip()
    s = to_english_digits(raw)
    # normalize Arabic Yeh / Kaf if present
    s = s.replace("ي", "ی").replace("ك", "ک")
    # strip tatweel
    s = s.replace("ـ", "")

    tzinfo = None
    if tz:
        from zoneinfo import ZoneInfo

        tzinfo = ZoneInfo(tz)

    # numeric Y/M/D
    num = re.fullmatch(r"\s*(\d{1,4})[/.\-](\d{1,2})[/.\-](\d{1,2})\s*", s)
    if num:
        y, m, d = int(num.group(1)), int(num.group(2)), int(num.group(3))
        return JalaliDate(y, m, d, tzinfo=tzinfo)

    months = _month_map(strict_month)
    # optional weekday then day month year
    # day may be 1-2 digits
    pattern = re.compile(
        r"^\s*(?:(?P<wday>" + "|".join(map(re.escape, _FA_WEEKDAYS)) + r")\s+)?"
        r"(?P<day>\d{1,2})\s+"
        r"(?P<month>" + "|".join(sorted(map(re.escape, months), key=len, reverse=True)) + r")\s+"
        r"(?P<year>\d{3,4})\s*$",
        re.IGNORECASE,
    )
    match = pattern.match(raw if any(c in raw for c in "اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی") else s)
    if not match:
        match = pattern.match(s)

    if not match:
        raise ValueError(
            f"Cannot parse Persian date {text!r}. "
            f"Expected like '۱۸ آبان ۱۴۰۳' or '1403/08/18'."
        )

    day = int(match.group("day"))
    month_name = match.group("month")
    year = int(match.group("year"))
    month = months.get(month_name) or months.get(month_name.title())
    if month is None:
        # try lowercase for English
        month = months.get(month_name.lower())
    if month is None:
        raise ValueError(f"Unknown month name: {month_name!r}")

    result = JalaliDate(year, month, day, tzinfo=tzinfo)

    wday = match.group("wday")
    if wday and check_weekday:
        expected = _FA_WEEKDAYS.get(wday)
        if expected is not None and result.weekday() != expected:
            warnings.warn(
                f"Weekday prefix {wday!r} does not match {result.strftime('%Y/%m/%d')}",
                UserWarning,
                stacklevel=2,
            )
    return result


def parse_gregorian_fa(
    text: str,
    *,
    tz: Optional[str] = None,
) -> GregorianDate:
    """Parse an English Gregorian month-name date such as ``8 November 2024``.

    Args:
        text: Input string (Persian or English digits).
        tz: Optional IANA timezone name.

    Returns:
        Parsed :class:`~parsidate.core.gregorian.GregorianDate`.

    Raises:
        ValueError: If the string cannot be parsed.

    Example:
        >>> from parsidate.parsers import parse_gregorian_fa
        >>> parse_gregorian_fa("8 November 2024").month()
        11
    """
    s = to_english_digits(text.strip())
    months = _GREG_EN_MONTHS
    pattern = re.compile(
        r"^\s*(?P<day>\d{1,2})\s+"
        r"(?P<month>" + "|".join(sorted(map(re.escape, months), key=len, reverse=True)) + r")\s+"
        r"(?P<year>\d{3,4})\s*$",
        re.IGNORECASE,
    )
    match = pattern.match(s)
    if not match:
        raise ValueError(f"Cannot parse Gregorian date {text!r}")
    month = months.get(match.group("month").lower())
    if month is None:
        raise ValueError(f"Unknown month: {match.group('month')!r}")
    tzinfo = None
    if tz:
        from zoneinfo import ZoneInfo

        tzinfo = ZoneInfo(tz)
    return GregorianDate(int(match.group("year")), month, int(match.group("day")), tzinfo=tzinfo)
