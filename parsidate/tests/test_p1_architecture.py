"""P1 architecture and API-quality tests."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from parsidate.intervals.duration import Duration
from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate


class TestDurationOrdering:
    """Duration must be a total order with exact microsecond equality."""

    def test_total_ordering(self) -> None:
        assert Duration(hours=1) < Duration(hours=2)
        assert Duration(hours=2) > Duration(hours=1)
        assert Duration(hours=1) <= Duration(hours=1)
        assert Duration(hours=1) >= Duration(hours=1)
        assert Duration(hours=1) != Duration(hours=2)

    def test_exact_equality_no_epsilon(self) -> None:
        a = Duration(microseconds=1)
        b = Duration(microseconds=2)
        assert a != b
        assert Duration(microseconds=5) == Duration(microseconds=5)

    def test_negative_and_zero(self) -> None:
        assert Duration() == Duration(seconds=0)
        assert -Duration(hours=1) < Duration()
        assert Duration(hours=1) > Duration(hours=-1)

    def test_hashable(self) -> None:
        assert hash(Duration(hours=1)) == hash(Duration(minutes=60))

    def test_float_seconds_round_to_microsecond(self) -> None:
        d = Duration(seconds=1.0000004)
        assert d.total_seconds() == pytest.approx(1.000000)

    def test_sortable_list(self) -> None:
        items = [Duration(hours=3), Duration(minutes=1), Duration(days=1)]
        assert sorted(items)[0] == Duration(minutes=1)
        assert sorted(items)[-1] == Duration(days=1)


class TestArithmeticModuleSurface:
    """One public arithmetic module; no duplicate dead twins."""

    def test_operations_reexports_are_canonical(self) -> None:
        from parsidate.operations import arithmetic as ops
        from parsidate.intervals import arithmetic as intervals_arith

        assert ops.add_days is intervals_arith.add_days
        assert ops.add_months is intervals_arith.add_months

    def test_add_days_returns_new(self) -> None:
        from parsidate.operations.arithmetic import add_days

        d = JalaliDate(1403, 1, 1)
        d2 = add_days(d, 5)
        assert d.day() == 1
        assert d2.day() == 6


class TestLayering:
    """utils.helpers must not import formatting.formatters."""

    def test_helpers_does_not_import_formatters(self) -> None:
        import ast
        from pathlib import Path

        src = Path("parsidate/utils/helpers.py").read_text(encoding="utf-8")
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert "formatters" not in node.module
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "formatters" not in alias.name


class TestTimezoneModern:
    """Timezone helpers should use zoneinfo when available."""

    def test_get_timezone_returns_zoneinfo(self) -> None:
        from zoneinfo import ZoneInfo

        from parsidate.timezone.tz_handler import get_timezone

        tz = get_timezone("Asia/Tehran")
        assert isinstance(tz, ZoneInfo)

    def test_force_tz_jalali(self) -> None:
        from parsidate.parsers import jmd
        from parsidate.timezone.tz_handler import force_tz

        d = jmd("1403/08/18")
        aware = force_tz(d, "Asia/Tehran")
        assert aware.tzinfo() is not None
        assert d.tzinfo() is None

    def test_now_with_tz_is_aware(self) -> None:
        from parsidate.parsers import now_gregorian

        g = now_gregorian(tz="UTC")
        assert g.tzinfo() is not None

    def test_datetime_roundtrip(self) -> None:
        g = GregorianDate(2024, 11, 8, 14, 30, tzinfo=timezone.utc)
        dt = g.to_datetime()
        assert dt.tzinfo is not None
        assert dt.year == 2024


class TestDocstringContract:
    """Public callables in core modules need Args/Returns in docstrings."""

    def test_duration_methods_documented(self) -> None:
        for name in ("total_seconds", "days", "hours"):
            doc = getattr(Duration, name).__doc__ or ""
            assert "Returns:" in doc or "Return" in doc

    def test_jalali_to_ordinal_documented(self) -> None:
        doc = JalaliDate.to_ordinal.__doc__ or ""
        assert "Returns:" in doc
