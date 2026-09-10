"""Tests targeting remaining product-code coverage gaps (95% goal)."""

from __future__ import annotations

from datetime import timezone

import pytest

from parsidate.core.hijri import HijriDate
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.holidays import HolidayCalendar, HolidaySet
from parsidate.intervals.duration import Duration
from parsidate.intervals.period import Period
from parsidate.intervals.interval import Interval
from parsidate.operations.rounding import (
    ceil_to_week,
    ceil_to_quarter,
    ceil_to_year,
    floor_to_quarter,
    round_date,
)
from parsidate.operations.business import is_business_day
from parsidate.parsers import parse_gregorian_fa, parse_fa
from parsidate.formatting.formatters import format_gregorian_date, format_date_custom
from parsidate.utils.helpers import month_name, weekday_name, get_season
from parsidate.timezone.tz_handler import with_tz, utc_offset_minutes, list_timezones


class TestHijriCoverage:
    def test_leap_year_and_dhu_al_hijjah(self) -> None:
        # find a tabular leap year
        for y in range(1440, 1460):
            if HijriDate(y, 1, 1).is_leap_year():
                assert HijriDate(y, 12, 30).day() == 30
                break

    def test_add_months_and_years(self) -> None:
        h = HijriDate(1446, 1, 15)
        assert h.add(months=1).month() == 2
        assert h.add(months=12).year() == 1447
        assert h.add(months=-1).month() == 12
        assert h.add(years=1).year() == 1447

    def test_replace_and_comparisons(self) -> None:
        a = HijriDate(1446, 1, 1)
        b = a.replace(day=2)
        assert b.day() == 2
        assert a < b
        assert b > a
        assert a <= a
        assert b >= a
        assert a != b
        assert (a == "x") is False

    def test_repr_str(self) -> None:
        h = HijriDate(1446, 2, 3)
        assert "HijriDate" in repr(h)
        assert str(h) == "1446-02-03"

    def test_immutable(self) -> None:
        with pytest.raises(AttributeError):
            HijriDate(1446, 1, 1)._year = 2


class TestDimdateRanges:
    def test_date_range(self) -> None:
        from parsidate.dimdate.generator import date_range

        start = JalaliDate(1403, 1, 1)
        end = JalaliDate(1403, 1, 3)
        days = list(date_range(start, end))
        assert len(days) == 3
        assert days[0] == start

    def test_month_range(self) -> None:
        from parsidate.dimdate.generator import month_range

        out = list(month_range(JalaliDate(1403, 1, 15), JalaliDate(1403, 3, 1)))
        assert out[0].day() == 1
        assert len(out) >= 2

    def test_year_range(self) -> None:
        from parsidate.dimdate.generator import year_range

        out = list(year_range(JalaliDate(1402, 5, 1), JalaliDate(1404, 1, 1)))
        assert [d.year() for d in out] == [1402, 1403, 1404]

    def test_custom_range(self) -> None:
        from parsidate.dimdate.generator import custom_range

        out = list(custom_range(JalaliDate(1403, 1, 1), JalaliDate(1403, 3, 1), months=1))
        assert len(out) == 3


class TestParseGregorianFa:
    def test_basic(self) -> None:
        d = parse_gregorian_fa("8 November 2024")
        assert (d.year(), d.month(), d.day()) == (2024, 11, 8)

    def test_invalid(self) -> None:
        with pytest.raises(ValueError):
            parse_gregorian_fa("not a date")

    def test_tz(self) -> None:
        d = parse_gregorian_fa("8 November 2024", tz="UTC")
        assert d.tzinfo() is not None


class TestParseFaExtra:
    def test_strict_month_false_short(self) -> None:
        d = parse_fa("18 Aba 1403", strict_month=False)
        assert d.month() == 8

    def test_numeric(self) -> None:
        assert parse_fa("1403/08/18").day() == 18


class TestRoundingCoverage:
    def test_ceil_week_identity(self) -> None:
        # Saturday midnight Jalali weekday 0
        d = JalaliDate(1403, 1, 4)  # Saturday
        assert ceil_to_week(d, week_start=0) == d

    def test_ceil_quarter_q4_wrap(self) -> None:
        d = JalaliDate(1403, 11, 1)
        r = ceil_to_quarter(d)
        assert r.month() in (1, 2)

    def test_ceil_quarter_at_start(self) -> None:
        d = JalaliDate(1403, 1, 1)
        assert ceil_to_quarter(d) == d

    def test_ceil_year_at_start(self) -> None:
        d = JalaliDate(1403, 1, 1)
        assert ceil_to_year(d) == d

    def test_floor_quarter(self) -> None:
        assert floor_to_quarter(JalaliDate(1403, 5, 20)).month() == 4

    def test_round_date_to_day(self) -> None:
        d = JalaliDate(1403, 1, 1, 0, 0)
        assert round_date(d, "day") == d


class TestHolidayCalendarCoverage:
    def test_years_and_in_year(self) -> None:
        hs = HolidaySet.from_strings(["1402/01/01", "1403/01/01"])
        assert hs.years() == [1402, 1403]
        assert len(hs.in_year(1403)) == 1

    def test_iter_len(self) -> None:
        hs = HolidaySet.from_strings(["1403/01/01"])
        assert list(hs)[0].day() == 1
        assert len(hs) == 1

    def test_immutability(self) -> None:
        with pytest.raises(AttributeError):
            HolidaySet()._dates = ()

    def test_calendar_eq_hash(self) -> None:
        a = HolidayCalendar.ir(years=[1403])
        b = HolidayCalendar.ir(years=[1403])
        assert a == b
        assert hash(a) == hash(b)
        assert a != "x"

    def test_calendar_roundtrip_payload(self) -> None:
        cal = HolidayCalendar.ir(years=[1403]).add_holidays(["1403/08/18"], label="x")
        back = HolidayCalendar.from_payload(cal.to_payload())
        assert back.is_holiday(JalaliDate(1403, 8, 18))

    def test_weekend_property(self) -> None:
        assert HolidayCalendar().weekend == (6,)


class TestDurationPeriodInterval:
    def test_duration_abs_and_from_seconds(self) -> None:
        assert abs(Duration(hours=-2)).hours() == 2
        d = Duration.from_seconds(90)
        assert d.minutes() == 1
        assert d.seconds() == 30
        assert d.total_seconds() == 90

    def test_duration_attrs(self) -> None:
        with pytest.raises(AttributeError):
            Duration()._us = 1

    def test_period_immutability_and_neg(self) -> None:
        with pytest.raises(AttributeError):
            Period(months=1).months = 2
        assert (-Period(months=1)).months == -1

    def test_interval_length_hours(self) -> None:
        s = JalaliDate(1403, 1, 5)
        e = JalaliDate(1403, 1, 6)
        assert Interval(s, e).length("hours") == 24
        with pytest.raises(ValueError):
            Interval(s, e).length("years")


class TestFormattingHelpers:
    def test_gregorian_fa_locale_month(self) -> None:
        g = GregorianDate(2024, 11, 8)
        s = format_gregorian_date(g, "%Y-%m-%d", "fa")
        assert "۲۰۲۴" in s

    def test_format_date_custom_dispatch(self) -> None:
        j = JalaliDate(1403, 1, 1)
        assert format_date_custom(j, "%Y", "en") == "1403"

    def test_helpers_month_weekday_season(self) -> None:
        assert month_name(1, "fa", "jalali")
        assert weekday_name(0, "en", "gregorian")
        assert get_season(1, "gregorian") in ("Winter", "Spring", "Summer", "Fall")


class TestBusinessAndTz:
    def test_business_invalid_weekend_iterable(self) -> None:
        # non-jalali without holidays
        g = GregorianDate(2024, 3, 25)
        assert is_business_day(g) is True

    def test_tz_helpers(self) -> None:
        assert "UTC" in list_timezones()
        assert utc_offset_minutes("UTC") == 0
        j2 = JalaliDate(1403, 8, 18, 14, 0, 0, tzinfo=timezone.utc)
        out = with_tz(j2, "Asia/Tehran")
        assert out.tzinfo() is not None


class TestJalaliGregorianEdges:
    def test_jalali_add_negative_days(self) -> None:
        d = JalaliDate(1403, 1, 1)
        assert d.add(days=-1).day() == 29

    def test_gregorian_add_negative(self) -> None:
        g = GregorianDate(2024, 3, 1)
        assert g.add(days=-1).day() == 29

    def test_jalali_immutability(self) -> None:
        with pytest.raises(AttributeError):
            JalaliDate(1403, 1, 1)._year = 1
