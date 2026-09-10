import pytest
import pandas as pd
from parsidate.dimdate import generate_dim_date


def test_generate_dim_date_jalali():
    dim = generate_dim_date(
        start="1402/01/01",
        end="1402/01/05",
        calendar="jalali",
        include_fiscal=True
    )
    assert isinstance(dim, pd.DataFrame)
    assert len(dim) == 5
    assert "full_date" in dim.columns
    assert "year" in dim.columns
    assert dim.iloc[0]["year"] == 1402
    assert dim.iloc[-1]["year"] == 1402


def test_generate_dim_date_gregorian():
    dim = generate_dim_date(
        start="2024-03-20",
        end="2024-03-25",
        calendar="gregorian",
        include_fiscal=False
    )
    assert isinstance(dim, pd.DataFrame)
    assert len(dim) == 6
    assert "full_date" in dim.columns
    assert dim["year"].iloc[0] == 2024


def test_dim_date_columns():
    dim = generate_dim_date(start="1402/01/01", end="1402/01/03")
    expected_cols = [
        "date_key", "full_date", "year", "quarter", "month", "day",
        "month_name_en", "month_name_fa", "month_short_en",
        "weekday", "weekday_name_en", "weekday_name_fa",
        "is_weekend", "is_holiday", "is_leap_year",
        "day_of_year", "week_of_year", "days_in_month", "season"
    ]
    for col in expected_cols:
        assert col in dim.columns, f"Missing column: {col}"


def test_dim_date_types_and_weekends():
    dim = generate_dim_date(start="1402/01/01", end="1402/01/07", calendar="jalali")
    for w in dim["is_weekend"]:
        assert isinstance(w, bool)


def test_dim_date_fiscal_columns():
    dim = generate_dim_date(start="1402/01/01", end="1402/01/10", calendar="jalali", include_fiscal=True)
    assert "fiscal_year" in dim.columns
    assert "fiscal_quarter" in dim.columns
    assert "fiscal_month" in dim.columns


def test_dim_date_invalid_input():
    with pytest.raises(Exception):
        generate_dim_date(start="abcd", end="1401/01/10")
    with pytest.raises(Exception):
        generate_dim_date(start="1402/01/15", end="1402/01/10")


def test_dim_date_edge_cases():
    dim = generate_dim_date(start="1402/04/01", end="1402/04/01", calendar="jalali")
    assert len(dim) == 1
    dim = generate_dim_date(start="1402/01/30", end="1402/02/02", calendar="jalali")
    assert len(dim) == 4


def test_generate_dim_date_jalali_basic():
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/01/10",
        calendar="jalali"
    )
    assert isinstance(dim, pd.DataFrame)
    assert len(dim) == 10
    assert "date_key" in dim.columns
    assert "full_date" in dim.columns
    assert "year" in dim.columns
    assert "month_name_fa" in dim.columns
    assert "weekday_name_fa" in dim.columns

    first_row = dim.iloc[0]
    assert first_row["year"] == 1403
    assert first_row["month"] == 1
    assert first_row["day"] == 1
    assert first_row["date_key"] == 14030101


def test_generate_dim_date_gregorian_basic():
    dim = generate_dim_date(
        start="2024-01-01",
        end="2024-01-10",
        calendar="gregorian"
    )
    assert isinstance(dim, pd.DataFrame)
    assert len(dim) == 10
    assert "date_key" in dim.columns
    assert "month_name_en" in dim.columns
    assert "weekday_name_en" in dim.columns

    first_row = dim.iloc[0]
    assert first_row["year"] == 2024
    assert first_row["month"] == 1
    assert first_row["day"] == 1


def test_generate_dim_date_with_fiscal():
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/01/10",
        calendar="jalali",
        include_fiscal=True,
        fiscal_year_start_month=1
    )
    assert "fiscal_year" in dim.columns
    assert "fiscal_quarter" in dim.columns
    assert "fiscal_month" in dim.columns
    assert all(dim["fiscal_year"] == 1403)


def test_generate_dim_date_with_holidays():
    holidays = ["1403/01/01", "1403/01/05"]
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/01/10",
        calendar="jalali",
        holidays=holidays
    )
    assert dim.iloc[0]["is_holiday"] == True
    assert dim.iloc[4]["is_holiday"] == True
    assert dim.iloc[1]["is_holiday"] == False


def test_generate_dim_date_weekend():
    dim = generate_dim_date(
        start="1403/08/18",
        end="1403/08/25",
        calendar="jalali"
    )
    assert "is_weekend" in dim.columns
    assert dim["is_weekend"].sum() >= 1


def test_generate_dim_date_full_year():
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/12/29",
        calendar="jalali"
    )
    assert len(dim) == 365
    assert all(dim["year"] == 1403)
    assert dim["month"].min() == 1
    assert dim["month"].max() == 12


def test_generate_dim_date_leap_year():
    dim = generate_dim_date(
        start="1399/12/29",
        end="1399/12/30",
        calendar="jalali"
    )
    assert len(dim) == 2
    assert all(dim["is_leap_year"] == True)
    assert dim.iloc[1]["day"] == 30


def test_generate_dim_date_export_csv(tmp_path):
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/01/10",
        calendar="jalali"
    )
    csv_path = tmp_path / "test_dim_date.csv"
    dim.to_csv(csv_path, index=False)
    dim_loaded = pd.read_csv(csv_path)
    assert len(dim_loaded) == 10
    assert list(dim_loaded.columns) == list(dim.columns)


def test_generate_dim_date_gregorian_full_year():
    dim = generate_dim_date(
        start="2024-01-01",
        end="2024-12-31",
        calendar="gregorian"
    )
    assert len(dim) == 366
    assert all(dim["year"] == 2024)


def test_dimdate_quarter_values():
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/12/29",
        calendar="jalali"
    )
    q1 = dim[dim["quarter"] == 1]
    q2 = dim[dim["quarter"] == 2]
    q3 = dim[dim["quarter"] == 3]
    q4 = dim[dim["quarter"] == 4]
    assert all(q1["month"].isin([1, 2, 3]))
    assert all(q2["month"].isin([4, 5, 6]))
    assert all(q3["month"].isin([7, 8, 9]))
    assert all(q4["month"].isin([10, 11, 12]))
