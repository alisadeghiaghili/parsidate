"""R1: Iranian official holidays and business-day algebra."""

from __future__ import annotations

import pytest

from parsidate.core.jalali import JalaliDate
from parsidate.holidays import (
    HolidaySet,
    holidays_in_year,
    is_holiday,
    iran_fixed_solar_holidays,
)
from parsidate.operations.business import (
    add_business_days,
    is_business_day,
    networkdays,
    next_business_day,
    prev_business_day,
)

# Jalali weekday: 0=Sat ... 5=Thu, 6=Fri


class TestHolidayDataset:
    def test_fixed_nowruz_1403(self) -> None:
        hs = iran_fixed_solar_holidays(1403)
        days = {(d.month(), d.day()) for d in hs}
        assert (1, 1) in days
        assert (1, 2) in days
        assert (1, 3) in days
        assert (1, 4) in days

    def test_fixed_other_solar(self) -> None:
        days = {(d.month(), d.day()) for d in iran_fixed_solar_holidays(1403)}
        assert (1, 12) in days
        assert (1, 13) in days
        assert (3, 15) in days
        assert (11, 22) in days

    def test_holidays_in_year_includes_lunar_when_available(self) -> None:
        all_days = holidays_in_year(1403)
        assert len(all_days) >= 6

    def test_is_holiday(self) -> None:
        assert is_holiday(JalaliDate(1403, 1, 1)) is True
        assert is_holiday(JalaliDate(1403, 1, 5)) is False

    def test_holiday_set_custom(self) -> None:
        hs = HolidaySet(dates=[JalaliDate(1403, 8, 18)])
        assert JalaliDate(1403, 8, 18) in hs
        assert JalaliDate(1403, 8, 19) not in hs

    def test_holiday_set_serializable(self) -> None:
        hs = HolidaySet(dates=[JalaliDate(1403, 1, 1)])
        payload = hs.to_payload()
        back = HolidaySet.from_payload(payload)
        assert back == hs


class TestWeekendDefaults:
    def test_friday_is_weekend_jalali(self) -> None:
        fri = JalaliDate(1403, 1, 3)
        assert fri.weekday() == 6
        assert is_business_day(fri, use_iran_holidays=False) is False

    def test_saturday_is_business_when_not_holiday(self) -> None:
        sat = JalaliDate(1403, 1, 11)
        assert sat.weekday() == 0
        assert is_business_day(sat) is True

    def test_holiday_is_not_business(self) -> None:
        assert is_business_day(JalaliDate(1403, 1, 1)) is False

    def test_thursday_is_business_by_default(self) -> None:
        thu = JalaliDate(1403, 1, 9)
        assert thu.weekday() == 5
        assert is_business_day(thu) is True
        assert is_business_day(thu, weekend=(5, 6)) is False


class TestNetworkdays:
    def test_same_day_business(self) -> None:
        d = JalaliDate(1403, 1, 5)  # Sunday after Nowruz
        assert networkdays(d, d) == 1

    def test_same_day_weekend(self) -> None:
        fri = JalaliDate(1403, 1, 3)
        assert networkdays(fri, fri) == 0

    def test_week_excluding_nowruz_and_friday(self) -> None:
        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 7)
        # days 1-4 Nowruz holidays; 5 Sun, 6 Mon, 7 Tue business
        assert networkdays(start, end) == 3

    def test_exclusive_end_option(self) -> None:
        start = JalaliDate(1403, 1, 5)
        end = JalaliDate(1403, 1, 8)
        assert networkdays(start, end, inclusive_end=False) == networkdays(start, end) - 1

    def test_custom_holidays(self) -> None:
        start = JalaliDate(1403, 1, 5)
        end = JalaliDate(1403, 1, 7)
        hs = HolidaySet(dates=[JalaliDate(1403, 1, 6)])
        assert networkdays(start, end, holidays=hs) == 2


class TestAddBusinessDays:
    def test_add_positive_skips_weekend(self) -> None:
        d = JalaliDate(1403, 1, 5)
        assert add_business_days(d, 1) == JalaliDate(1403, 1, 6)

    def test_add_zero_returns_same(self) -> None:
        d = JalaliDate(1403, 1, 5)
        assert add_business_days(d, 0) == d

    def test_add_across_friday(self) -> None:
        thu = JalaliDate(1403, 1, 9)
        assert add_business_days(thu, 1) == JalaliDate(1403, 1, 11)

    def test_subtract_business_days(self) -> None:
        sat = JalaliDate(1403, 1, 11)
        assert add_business_days(sat, -1) == JalaliDate(1403, 1, 9)

    def test_start_on_weekend(self) -> None:
        fri = JalaliDate(1403, 1, 3)
        assert add_business_days(fri, 1) == JalaliDate(1403, 1, 5)


class TestNextPrevBusiness:
    def test_next_from_friday(self) -> None:
        assert next_business_day(JalaliDate(1403, 1, 3)) == JalaliDate(1403, 1, 5)

    def test_prev_from_friday(self) -> None:
        # 1403/1/2 is Nowruz; first business day before Friday is 1402/12/28
        assert prev_business_day(JalaliDate(1403, 1, 3)) == JalaliDate(1402, 12, 28)

    def test_prev_from_friday_no_iran_holidays(self) -> None:
        assert prev_business_day(
            JalaliDate(1403, 1, 3), use_iran_holidays=False
        ) == JalaliDate(1403, 1, 2)

    def test_next_skips_nowruz(self) -> None:
        d = JalaliDate(1403, 1, 12)
        assert next_business_day(d) == JalaliDate(1403, 1, 14)


class TestGregorianWeekend:
    def test_gregorian_saturday_sunday_weekend(self) -> None:
        from parsidate.core.gregorian import GregorianDate

        sat = GregorianDate(2024, 3, 23)
        sun = GregorianDate(2024, 3, 24)
        assert is_business_day(sat) is False
        assert is_business_day(sun) is False
        mon = GregorianDate(2024, 3, 25)
        assert is_business_day(mon) is True
