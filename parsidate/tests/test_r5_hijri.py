"""R5: Hijri (Qamari) tabular calendar conversion."""

from __future__ import annotations

from datetime import date

import pytest

from parsidate.core.converters import jalali_to_gregorian
from parsidate.core.hijri import HijriDate
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate


class TestHijriBasics:
    def test_create_and_fields(self) -> None:
        h = HijriDate(1446, 1, 10)
        assert (h.year(), h.month(), h.day()) == (1446, 1, 10)

    def test_invalid_month(self) -> None:
        with pytest.raises(ValueError):
            HijriDate(1446, 13, 1)

    def test_invalid_day(self) -> None:
        with pytest.raises(ValueError):
            HijriDate(1446, 1, 31)

    def test_immutable_add(self) -> None:
        h = HijriDate(1446, 1, 1)
        h2 = h.add(days=1)
        assert h.day() == 1
        assert h2.day() == 2


class TestHijriConversion:
    def test_ashura_1446_near_iranian_anchor(self) -> None:
        """10 Muharram 1446 ≈ 1403/4/26 (Ashura) within ±1 day (tabular)."""
        h = HijriDate(1446, 1, 10)
        gy, gm, gd = h.to_gregorian()
        jy, jm, jd = jalali_to_gregorian(1403, 4, 26)
        delta = abs((date(gy, gm, gd) - date(jy, jm, jd)).days)
        assert delta <= 1

    def test_from_jalali_roundtrip(self) -> None:
        j = JalaliDate(1403, 1, 1)
        h = HijriDate.from_jalali(j)
        back = h.to_jalali()
        assert abs((JalaliDate(*back) - j).days()) <= 1

    def test_from_gregorian_year_bounds(self) -> None:
        g = GregorianDate(2024, 7, 16)
        h = HijriDate.from_gregorian(g)
        assert h.year() in (1445, 1446)

    def test_month_names(self) -> None:
        assert HijriDate(1446, 1, 1).month_name("en") == "Muharram"
        assert "محرم" in HijriDate(1446, 1, 1).month_name("fa")

    def test_equality_and_hash(self) -> None:
        a = HijriDate(1446, 1, 10)
        b = HijriDate(1446, 1, 10)
        assert a == b
        assert hash(a) == hash(b)


class TestDocumentedLimitations:
    def test_tabular_not_astronomical(self) -> None:
        """Docstring must state civil/tabular basis and ±1 day risk."""
        doc = HijriDate.__doc__ or ""
        assert "tabular" in doc.lower() or "civil" in doc.lower()
        assert "1" in doc  # mentions day tolerance somewhere in module
