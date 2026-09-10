"""R4: warehouse-grade dim_date columns."""

from __future__ import annotations

import pytest

pytest.importorskip("pandas")

from parsidate.dimdate import generate_dim_date
from parsidate.core.jalali import JalaliDate


@pytest.fixture(scope="module")
def dim_1403():
    return generate_dim_date(
        start="1403/01/01",
        end="1403/12/30",
        calendar="jalali",
        include_fiscal=True,
        use_iran_holidays=True,
    )


def test_full_year_row_count(dim_1403) -> None:
    # 1403 is leap → 366 days
    assert len(dim_1403) == 366
    assert dim_1403["date_key"].is_unique


def test_nowruz_flags(dim_1403) -> None:
    row = dim_1403[dim_1403["date_key"] == 14030101].iloc[0]
    assert bool(row["is_holiday"]) is True
    assert bool(row["is_business_day"]) is False
    assert row["holiday_name"]


def test_first_business_after_nowruz(dim_1403) -> None:
    row = dim_1403[dim_1403["date_key"] == 14030105].iloc[0]
    assert bool(row["is_business_day"]) is True


def test_friday_weekend(dim_1403) -> None:
    row = dim_1403[dim_1403["date_key"] == 14030103].iloc[0]
    assert int(row["weekday"]) == 6
    assert bool(row["is_weekend"]) is True


def test_iso_columns(dim_1403) -> None:
    row = dim_1403[dim_1403["date_key"] == 14030101].iloc[0]
    assert int(row["iso_year"]) >= 2024
    assert 1 <= int(row["iso_week"]) <= 53
    assert 1 <= int(row["iso_weekday"]) <= 7


def test_month_bounds(dim_1403) -> None:
    row = dim_1403[dim_1403["date_key"] == 14030115].iloc[0]
    assert str(row["month_start"]).endswith("01")
    assert str(row["month_end"]).endswith("31")  # Farvardin has 31 days


def test_fiscal_columns(dim_1403) -> None:
    assert "fiscal_year" in dim_1403.columns
    assert "fiscal_quarter" in dim_1403.columns
    assert "fiscal_month" in dim_1403.columns
    row = dim_1403[dim_1403["date_key"] == 14030101].iloc[0]
    assert int(row["fiscal_month"]) == 1


def test_ytd_mtd_flags(dim_1403) -> None:
    as_of = JalaliDate(1403, 2, 15)
    df = generate_dim_date(
        start="1403/01/01",
        end="1403/02/20",
        calendar="jalali",
        as_of=as_of,
        use_iran_holidays=True,
    )
    assert bool(df.loc[df["date_key"] == 14030210, "ytd_flag"].iloc[0]) is True
    assert bool(df.loc[df["date_key"] == 14030210, "mtd_flag"].iloc[0]) is True
    assert bool(df.loc[df["date_key"] == 14030110, "ytd_flag"].iloc[0]) is True
    assert bool(df.loc[df["date_key"] == 14030110, "mtd_flag"].iloc[0]) is False


def test_custom_holiday_name() -> None:
    from parsidate.holidays import HolidaySet

    hs = HolidaySet(dates=[JalaliDate(1403, 8, 18)])
    df = generate_dim_date(
        start="1403/08/18",
        end="1403/08/18",
        calendar="jalali",
        holidays=hs,
        use_iran_holidays=False,
    )
    assert bool(df.iloc[0]["is_holiday"]) is True


def test_gregorian_business_default() -> None:
    df = generate_dim_date(
        start="2024-03-23",
        end="2024-03-25",
        calendar="gregorian",
        use_iran_holidays=False,
    )
    # Sat, Sun, Mon
    assert bool(df.iloc[0]["is_business_day"]) is False
    assert bool(df.iloc[1]["is_business_day"]) is False
    assert bool(df.iloc[2]["is_business_day"]) is True


def test_column_dictionary_stable(dim_1403) -> None:
    required = {
        "date_key", "full_date", "year", "quarter", "month", "day",
        "is_weekend", "is_holiday", "is_business_day", "holiday_name",
        "iso_year", "iso_week", "iso_weekday",
        "month_start", "month_end",
        "day_of_year", "week_of_year", "days_in_month", "season",
        "fiscal_year", "fiscal_quarter", "fiscal_month",
    }
    assert required.issubset(set(dim_1403.columns))
