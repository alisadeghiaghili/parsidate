"""R6: custom/company holiday days and HolidayCalendar."""

from __future__ import annotations

import pytest

from parsidate.core.jalali import JalaliDate
from parsidate.holidays import (
    HolidayCalendar,
    HolidaySet,
    iran_holidays,
)
from parsidate.operations.business import add_business_days, networkdays


def test_holiday_set_from_strings() -> None:
    hs = HolidaySet.from_strings(["1403/08/18", "1403/08/19"])
    assert JalaliDate(1403, 8, 18) in hs
    assert len(hs) == 2


def test_holiday_set_from_persian_digits() -> None:
    hs = HolidaySet.from_strings(["۱۴۰۳/۰۸/۱۸"])
    assert JalaliDate(1403, 8, 18) in hs


def test_calendar_with_custom_days() -> None:
    cal = HolidayCalendar.ir(years=[1403]).with_holidays(
        ["1403/08/18", JalaliDate(1403, 8, 19)],
        label="company",
    )
    assert cal.is_holiday(JalaliDate(1403, 8, 18))
    assert cal.holiday_name(JalaliDate(1403, 8, 18)) == "company"
    assert cal.is_holiday(JalaliDate(1403, 1, 1))  # official Nowruz


def test_calendar_add_holidays_fluent() -> None:
    cal = HolidayCalendar.ir(years=[1403]).add_holidays(["1403/09/01"])
    assert cal.is_holiday(JalaliDate(1403, 9, 1))


def test_calendar_is_business_day() -> None:
    cal = HolidayCalendar.ir(years=[1403]).add_holidays(["1403/01/05"])
    assert cal.is_business_day(JalaliDate(1403, 1, 5)) is False
    assert cal.is_business_day(JalaliDate(1403, 1, 6)) is True


def test_calendar_networkdays_skips_custom() -> None:
    cal = HolidayCalendar.ir(years=[1403]).add_holidays(["1403/01/06"])
    # 1403/1/5 Sun, 1/6 Mon custom holiday, 1/7 Tue
    assert cal.networkdays(JalaliDate(1403, 1, 5), JalaliDate(1403, 1, 7)) == 2


def test_calendar_weekend_override() -> None:
    cal = HolidayCalendar(weekend=(5, 6), holidays=HolidaySet())
    thu = JalaliDate(1403, 1, 9)
    assert thu.weekday() == 5
    assert cal.is_business_day(thu) is False


def test_calendar_serialize() -> None:
    cal = HolidayCalendar.ir(years=[1403]).add_holidays(["1403/08/18"])
    payload = cal.to_payload()
    back = HolidayCalendar.from_payload(payload)
    assert back.is_holiday(JalaliDate(1403, 8, 18))
    assert back.is_holiday(JalaliDate(1403, 1, 1))


def test_calendar_add_business_days() -> None:
    cal = HolidayCalendar.ir(years=[1403]).add_holidays(["1403/01/06"])
    # from Sun 1/5 + 1 business → skip Mon holiday → Tue 1/7
    assert cal.add_business_days(JalaliDate(1403, 1, 5), 1) == JalaliDate(1403, 1, 7)


def test_empty_custom_still_has_official() -> None:
    cal = HolidayCalendar.ir(years=[1403])
    assert cal.is_holiday(JalaliDate(1403, 1, 1))


def test_pure_custom_no_official() -> None:
    cal = HolidayCalendar(holidays=HolidaySet.from_strings(["1403/08/18"]))
    assert cal.is_holiday(JalaliDate(1403, 8, 18))
    assert cal.is_holiday(JalaliDate(1403, 1, 1)) is False
