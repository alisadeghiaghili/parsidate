"""Tests for timezone handler."""

import pytest
from parsidate.timezone.tz_handler import (
    get_timezone, localize_datetime, convert_timezone,
    remove_timezone, utc_offset_minutes, is_dst,
    list_timezones, with_tz, force_tz
)
from datetime import datetime


class TestTimezone:
    def test_get_timezone(self):
        tz = get_timezone("Asia/Tehran")
        assert tz is not None

    def test_get_invalid_timezone(self):
        with pytest.raises(ValueError):
            get_timezone("Invalid/Timezone")

    def test_utc_offset_minutes(self):
        offset = utc_offset_minutes("Asia/Tehran")
        assert offset == 210  # +3:30

    def test_list_timezones(self):
        tzs = list_timezones()
        assert "Asia/Tehran" in tzs

    def test_localize_datetime(self):
        dt = datetime(2024, 1, 1, 12, 0, 0)
        aware_dt = localize_datetime(dt, "Asia/Tehran")
        assert aware_dt.tzinfo is not None

    def test_convert_timezone(self):
        dt = datetime(2024, 1, 1, 12, 0, 0)
        aware_dt = localize_datetime(dt, "Asia/Tehran")
        utc_dt = convert_timezone(aware_dt, "UTC")
        assert utc_dt.tzinfo is not None

    def test_remove_timezone(self):
        dt = datetime(2024, 1, 1, 12, 0, 0)
        aware_dt = localize_datetime(dt, "Asia/Tehran")
        naive_dt = remove_timezone(aware_dt)
        assert naive_dt.tzinfo is None

    def test_is_dst(self):
        dt = datetime(2024, 7, 1, 12, 0, 0)
        aware_dt = localize_datetime(dt, "Asia/Tehran")
        result = is_dst(aware_dt, "Asia/Tehran")
        assert isinstance(result, bool)

    def test_with_tz_jalali(self):
        from parsidate.parsers.parse import jmd_hms
        date_tehran = jmd_hms("1403/08/18 14:30:00", tz="Asia/Tehran")
        date_utc = with_tz(date_tehran, "UTC")
        assert date_utc.tzinfo() is not None

    def test_with_tz_gregorian(self):
        from parsidate.parsers.parse import ymd_hms
        date_tehran = ymd_hms("2024/11/08 14:30:00", tz="Asia/Tehran")
        date_utc = with_tz(date_tehran, "UTC")
        assert date_utc.tzinfo() is not None

    def test_force_tz_jalali(self):
        from parsidate.parsers.parse import jmd
        date = jmd("1403/08/18")
        date_tehran = force_tz(date, "Asia/Tehran")
        assert date_tehran.tzinfo() is not None

    def test_force_tz_gregorian(self):
        from parsidate.parsers.parse import ymd
        date = ymd("2024/11/08")
        date_tehran = force_tz(date, "Asia/Tehran")
        assert date_tehran.tzinfo() is not None

    def test_convert_timezone_naive_error(self):
        dt = datetime(2024, 1, 1, 12, 0, 0)
        with pytest.raises(ValueError):
            convert_timezone(dt, "UTC")

    def test_utc_offset_utc(self):
        offset = utc_offset_minutes("UTC")
        assert offset == 0
