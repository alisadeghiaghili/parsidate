import pytest
from datetime import timezone
from parsidate.core import JalaliDate, GregorianDate
from parsidate.core.converters import gregorian_to_jalali, jalali_to_gregorian

def test_jalalidate_vs_gregoriandate_equality():
    jd = JalaliDate(1402, 8, 19, 14, 32)
    g_ymd = jalali_to_gregorian(1402, 8, 19)
    gd = GregorianDate(*g_ymd, 14, 32)
    assert gd == GregorianDate(gd.year(), gd.month(), gd.day(), gd.hour(), gd.minute())
    assert jd != gd

def test_cross_conversion_consistency():
    jdate = JalaliDate(1399, 12, 30, 17, 20)
    gy, gm, gd = jdate.to_gregorian()
    jback = GregorianDate(gy, gm, gd, 17, 20).to_jalali()
    assert jback == (1399, 12, 30)
    gdate = GregorianDate(2017, 3, 21, 9, 15)
    jy, jm, jd = gdate.to_jalali()
    gback = JalaliDate(jy, jm, jd, 9, 15).to_gregorian()
    assert gback == (2017, 3, 21)

def test_copy_independence():
    jd = JalaliDate(1401, 5, 8, 20)
    jd2 = jd.copy()
    jd2.day(28)
    assert jd.day() != jd2.day()
    gd = GregorianDate(2020, 2, 2, 3)
    gd2 = gd.copy()
    gd2.month(9)
    assert gd.month() != gd2.month()

def test_str_repr_type():
    jd = JalaliDate(1397, 1, 1)
    gd = GregorianDate(2023, 8, 29)
    assert "JalaliDate" in repr(jd)
    assert "GregorianDate" in repr(gd)
    assert isinstance(str(jd), str)
    assert isinstance(str(gd), str)

def test_gregorian_and_jalalidate_addition_and_subtraction_consistency():
    base_j = JalaliDate(1403, 2, 10, 3, 50)
    base_g = GregorianDate(*jalali_to_gregorian(1403, 2, 10), 3, 50)
    nj = base_j.copy().add(days=17, months=1, years=2)
    ng = base_g.copy().add(days=17, months=1, years=2)
    gy, gm, gd = nj.to_gregorian()
    jy, jm, jd = ng.to_jalali()
    assert (gy, gm, gd) == (ng.year(), ng.month(), ng.day())
    assert (jy, jm, jd) == (nj.year(), nj.month(), nj.day())

def test_comparison_between_objects():
    jd1 = JalaliDate(1388, 9, 1, 13)
    jd2 = JalaliDate(1388, 9, 1, 13)
    gd1 = GregorianDate(*jalali_to_gregorian(1388, 9, 1), 13)
    gd2 = GregorianDate(*jalali_to_gregorian(1388, 9, 1), 13)
    assert jd1 == jd2
    assert gd1 == gd2
    assert jd1 != gd1
    assert not (jd1 < jd2)
    assert gd1 <= gd2
    assert not (gd1 > gd2)

def test_timezone_awareness_and_inheritance():
    tz = timezone.utc
    jd = JalaliDate(1400, 4, 5, 12, 30, 15, tzinfo=tz)
    gd = GregorianDate(*jd.to_gregorian(), 12, 30, 15, tzinfo=tz)
    assert jd.tzinfo() == gd.tzinfo() == tz
    n_jd = jd.copy().add(days=1)
    n_gd = gd.copy().add(days=1)
    assert n_jd.tzinfo() == tz and n_gd.tzinfo() == tz

def test_invalid_type_comparison():
    jd = JalaliDate(1403, 3, 21)
    assert jd != "2024-03-21"
    with pytest.raises(TypeError):
        _ = jd < 123
    with pytest.raises(TypeError):
        _ = jd > object()

def test_edge_same_datetime_different_calendars():
    j = JalaliDate(1403, 1, 1, 0, 0, 0)
    g = GregorianDate(*jalali_to_gregorian(1403, 1, 1), 0, 0, 0)
    assert j != g
    assert g.year() == j.to_gregorian()[0]
    assert g.month() == j.to_gregorian()[1]
    assert g.day() == j.to_gregorian()[2]
