"""R3: Persian written dates, ISO/timestamp, datetime bridges."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.parsers import parse_fa, parse_gregorian_fa
from parsidate.core.jalali import JalaliDate as J


class TestParseFa:
    def test_long_month_digits_fa(self) -> None:
        d = parse_fa("۱۸ آبان ۱۴۰۳")
        assert (d.year(), d.month(), d.day()) == (1403, 8, 18)

    def test_long_month_digits_en(self) -> None:
        d = parse_fa("18 Aban 1403")
        assert (d.year(), d.month(), d.day()) == (1403, 8, 18)

    def test_with_weekday_prefix(self) -> None:
        d = parse_fa("شنبه ۴ فروردین ۱۴۰۳")
        assert (d.year(), d.month(), d.day()) == (1403, 1, 4)
        assert d.weekday() == 0  # Saturday

    def test_weekday_mismatch_warns(self) -> None:
        with pytest.warns(UserWarning):
            parse_fa("شنبه ۱۸ آبان ۱۴۰۳")  # not a Saturday

    def test_numeric_slash(self) -> None:
        d = parse_fa("۱۴۰۳/۰۸/۱۸")
        assert d.day() == 18

    def test_short_month_en(self) -> None:
        d = parse_fa("18 Aba 1403", strict_month=False)
        assert d.month() == 8

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_fa("نامعلوم")


class TestIsoFormat:
    def test_jalali_isoformat_roundtrip(self) -> None:
        d = JalaliDate(1403, 8, 18, 14, 30, 25)
        s = d.isoformat()
        assert s.startswith("1403-08-18T14:30:25")
        back = JalaliDate.fromisoformat(s)
        assert back == d

    def test_jalali_isoformat_date_only(self) -> None:
        d = JalaliDate(1403, 8, 18)
        assert d.isoformat() == "1403-08-18"
        assert JalaliDate.fromisoformat("1403-08-18") == d

    def test_gregorian_isoformat_roundtrip(self) -> None:
        d = GregorianDate(2024, 11, 8, 14, 30, 25)
        s = d.isoformat()
        assert s.startswith("2024-11-08T14:30:25")
        back = GregorianDate.fromisoformat(s)
        assert back == d


class TestTimestamp:
    def test_gregorian_timestamp_utc(self) -> None:
        d = GregorianDate(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert d.timestamp() == datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp()

    def test_jalali_timestamp_matches_gregorian(self) -> None:
        j = JalaliDate(1403, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        g = GregorianDate(2024, 3, 20, 0, 0, 0, tzinfo=timezone.utc)
        assert j.timestamp() == g.timestamp()

    def test_fromtimestamp_jalali(self) -> None:
        ts = datetime(2024, 3, 20, 12, 0, 0, tzinfo=timezone.utc).timestamp()
        j = JalaliDate.fromtimestamp(ts, tz=timezone.utc)
        assert (j.year(), j.month(), j.day(), j.hour()) == (1403, 1, 1, 12)


class TestDatetimeBridge:
    def test_jalali_from_datetime(self) -> None:
        dt = datetime(2024, 3, 20, 10, 0, 0)
        j = JalaliDate.from_datetime(dt)
        assert (j.year(), j.month(), j.day(), j.hour()) == (1403, 1, 1, 10)

    def test_jalali_to_datetime_naive(self) -> None:
        j = JalaliDate(1403, 1, 1, 10, 30)
        dt = j.to_datetime_naive()
        assert dt == datetime(2024, 3, 20, 10, 30)

    def test_gregorian_from_to_datetime(self) -> None:
        g = GregorianDate(2024, 11, 8, 9, 0)
        dt = g.to_datetime()
        back = GregorianDate.from_datetime(dt)
        assert back == g


class TestJdatetimeBridge:
    def test_roundtrip_optional(self) -> None:
        pytest.importorskip("jdatetime")
        from parsidate.interop import from_jdatetime, to_jdatetime

        jd = JalaliDate(1403, 8, 18, 14, 30)
        wrapped = to_jdatetime(jd)
        assert wrapped.year == 1403
        assert wrapped.month == 8
        assert wrapped.day == 18
        back = from_jdatetime(wrapped)
        assert back == jd
