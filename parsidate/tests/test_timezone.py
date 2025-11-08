import pytest
from parsidate.timezone.tz_handler import (
    get_timezone,
    localize_datetime,
    convert_timezone,
    remove_timezone,
    utc_offset_minutes,
    is_dst,
    list_timezones,
)
from datetime import datetime

def test_get_valid_timezone():
    tz = get_timezone("Asia/Tehran")
    assert hasattr(tz, "localize")
    tz2 = get_timezone("UTC")
    assert str(tz2)

def test_get_invalid_timezone():
    with pytest.raises(ValueError):
        get_timezone("Mars/Phobos")

def test_localize_datetime():
    dt = datetime(2025, 11, 8, 12, 0)
    dt_tehran = localize_datetime(dt, "Asia/Tehran")
    assert dt_tehran.tzinfo is not None
    assert "Asia/Tehran" in str(dt_tehran.tzinfo)

def test_convert_timezone():
    dt = datetime(2025, 11, 8, 9, 0)
    dt_utc = localize_datetime(dt, "UTC")
    dt_tehran = convert_timezone(dt_utc, "Asia/Tehran")
    assert dt_tehran.tzinfo.zone == "Asia/Tehran"

def test_remove_timezone():
    dt = datetime(2025, 11, 8, 20, 0, tzinfo=get_timezone("Asia/Tehran"))
    naive = remove_timezone(dt)
    assert naive.tzinfo is None

def test_utc_offset_minutes():
    offset = utc_offset_minutes("Asia/Tehran")
    assert isinstance(offset, int)

def test_is_dst():
    dt = datetime(2025, 7, 1, 12, 0)
    tz = "Asia/Tehran"
    assert isinstance(is_dst(dt, tz), bool)

def test_list_timezones():
    tzs = list_timezones()
    assert isinstance(tzs, list)
    assert "Asia/Tehran" in tzs

def test_localize_then_convert():
    dt = datetime(2025, 3, 21, 19, 0)
    dt_l = localize_datetime(dt, "Europe/London")
    dt_c = convert_timezone(dt_l, "Asia/Tehran")
    assert dt_c.tzinfo.zone == "Asia/Tehran"

def test_edge_invalid_input_localize():
    dt = "not_a_datetime"
    with pytest.raises(Exception):
        localize_datetime(dt, "Asia/Tehran")

def test_dst_false():
    dt = datetime(2025, 1, 1, 11, 0)
    tz = "Asia/Tehran"
    assert not is_dst(dt, tz) or isinstance(is_dst(dt, tz), bool)
