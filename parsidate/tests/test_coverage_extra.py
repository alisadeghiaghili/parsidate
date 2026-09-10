"""Additional coverage for product modules (95%+ goal)."""

from __future__ import annotations

from datetime import timezone

import pytest

from parsidate.core.gregorian import GregorianDate
from parsidate.core.jalali import JalaliDate
from parsidate.dimdate import generate_dim_date
from parsidate.holidays import HolidayCalendar, HolidaySet
from parsidate.intervals.duration import (
    Duration,
    hours as d_hours,
    minutes as d_minutes,
    seconds as d_seconds,
)
from parsidate.intervals.period import (
    Period,
    years as p_years,
    months as p_months,
    weeks as p_weeks,
    days as p_days,
)
from parsidate.operations.business import networkdays
from parsidate.timezone.tz_handler import convert_timezone, localize_datetime, remove_timezone
from datetime import datetime


class TestDurationEdges:
    def test_microseconds_total_property(self) -> None:
        assert Duration(seconds=1).microseconds_total == 1_000_000

    def test_add_sub_not_implemented(self) -> None:
        with pytest.raises(TypeError):
            Duration(hours=1) + 1  # type: ignore[operator]
        with pytest.raises(TypeError):
            Duration(hours=1) - 1  # type: ignore[operator]

    def test_eq_non_duration(self) -> None:
        assert (Duration(hours=1) == 1) is False

    def test_lt_not_implemented(self) -> None:
        assert Duration(hours=1).__lt__(1) is NotImplemented

    def test_str_with_seconds_and_us(self) -> None:
        assert "s" in str(Duration(seconds=1, microseconds=5))
        assert "us" in str(Duration(microseconds=5))

    def test_factories(self) -> None:
        assert d_hours(2).total_seconds() == 7200
        assert d_minutes(2).total_seconds() == 120
        assert d_seconds(2).total_seconds() == 2


class TestPeriodEdges:
    def test_delattr_raises(self) -> None:
        p = Period(days=1)
        with pytest.raises(AttributeError):
            p.__delattr__("days")

    def test_add_sub_not_implemented(self) -> None:
        with pytest.raises(TypeError):
            Period(days=1) + 1  # type: ignore[operator]
        with pytest.raises(TypeError):
            Period(days=1) - 1  # type: ignore[operator]

    def test_eq_non_period(self) -> None:
        assert (Period(days=1) == 1) is False

    def test_hash(self) -> None:
        assert hash(Period(days=1)) == hash(Period(days=1))

    def test_factories(self) -> None:
        assert p_years(1).years == 1
        assert p_months(2).months == 2
        assert p_weeks(3).weeks == 3
        assert p_days(4).days == 4

    def test_approx_days(self) -> None:
        assert Period(years=1, months=1, days=1).approx_days() == 365 + 30 + 1


class TestHolidayCalendarEdges:
    def test_setattr_raises(self) -> None:
        cal = HolidayCalendar()
        with pytest.raises(AttributeError):
            cal._weekend = ()

    def test_custom_holidays_property(self) -> None:
        cal = HolidayCalendar().add_holidays(["1403/08/18"])
        assert JalaliDate(1403, 8, 18) in cal.custom_holidays

    def test_holiday_name_fallbacks(self) -> None:
        cal = HolidayCalendar.ir(years=[1403])
        assert cal.holiday_name(JalaliDate(1403, 1, 1)) == "official"
        assert cal.holiday_name(JalaliDate(1403, 8, 18)) == ""
        bare = HolidayCalendar().add_holidays(["1403/08/18"])
        # label default custom
        assert bare.holiday_name(JalaliDate(1403, 8, 18)) == "custom"

    def test_networkdays_reversed(self) -> None:
        cal = HolidayCalendar.ir(years=[1403])
        assert cal.networkdays(JalaliDate(1403, 1, 10), JalaliDate(1403, 1, 5)) == 0

    def test_networkdays_exclusive_end(self) -> None:
        cal = HolidayCalendar()
        s = JalaliDate(1403, 1, 5)
        e = JalaliDate(1403, 1, 7)
        assert cal.networkdays(s, e, inclusive_end=False) == 2

    def test_add_business_days_zero(self) -> None:
        cal = HolidayCalendar()
        d = JalaliDate(1403, 1, 5)
        assert cal.add_business_days(d, 0) == d

    def test_is_weekend(self) -> None:
        cal = HolidayCalendar()
        fri = JalaliDate(1403, 1, 3)
        assert cal.is_weekend(fri) is True


class TestDimdateCalendarAndFiscal:
    def test_generate_with_holiday_calendar(self) -> None:
        cal = HolidayCalendar.ir(years=[1403]).add_holidays(["1403/01/06"], label="x")
        df = generate_dim_date("1403/01/01", "1403/01/07", holidays=cal)
        row = df[df["date_key"] == 14030106].iloc[0]
        assert bool(row["is_holiday"]) is True
        assert row["holiday_name"] == "x"
        assert bool(row["is_business_day"]) is False

    def test_fiscal_before_start_month(self) -> None:
        df = generate_dim_date(
            "1403/01/01",
            "1403/01/02",
            include_fiscal=True,
            fiscal_year_start_month=7,
            use_iran_holidays=False,
        )
        assert int(df.iloc[0]["fiscal_year"]) == 1402

    def test_holidays_as_date_objects_list(self) -> None:
        df = generate_dim_date(
            "1403/08/18",
            "1403/08/18",
            holidays=[JalaliDate(1403, 8, 18)],
            use_iran_holidays=False,
        )
        assert bool(df.iloc[0]["is_holiday"]) is True


class TestTzEdges:
    def test_localize_convert_remove(self) -> None:
        aware = localize_datetime(datetime(2024, 1, 1, 12, 0), "UTC")
        utc = convert_timezone(aware, "Asia/Tehran")
        assert utc.tzinfo is not None
        assert remove_timezone(utc).tzinfo is None

    def test_localize_already_aware_raises(self) -> None:
        aware = datetime(2024, 1, 1, tzinfo=timezone.utc)
        with pytest.raises(ValueError):
            localize_datetime(aware, "UTC")

    def test_convert_naive_raises(self) -> None:
        with pytest.raises(ValueError):
            convert_timezone(datetime(2024, 1, 1), "UTC")


class TestBusinessNetworkdays:
    def test_networkdays_reversed_globally(self) -> None:
        assert networkdays(JalaliDate(1403, 1, 10), JalaliDate(1403, 1, 5)) == 0


class TestGregorianTzSetterPath:
    def test_gregorian_replace_tzinfo(self) -> None:
        g = GregorianDate(2024, 1, 1)
        g2 = g.replace(tzinfo=timezone.utc)
        assert g2.tzinfo() == timezone.utc
        assert g.tzinfo() is None
