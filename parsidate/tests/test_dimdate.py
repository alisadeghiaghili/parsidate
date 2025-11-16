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
    assert "jalali_date" in dim.columns
    assert "gregorian_date" in dim.columns
    # Check that first and last date match
    assert str(dim.iloc[0]["jalali_date"]).startswith("1402/01/01")
    assert str(dim.iloc[-1]["jalali_date"]).startswith("1402/01/05")

def test_generate_dim_date_gregorian():
    dim = generate_dim_date(
        start="2024-03-20",
        end="2024-03-25",
        calendar="gregorian",
        include_fiscal=False
    )
    assert isinstance(dim, pd.DataFrame)
    assert len(dim) == 6
    assert "jalali_date" in dim.columns
    assert "gregorian_date" in dim.columns
    assert dim["gregorian_date"].iloc[0].startswith("2024-03-20")
    assert dim["gregorian_date"].iloc[-1].startswith("2024-03-25")

def test_dim_date_columns():
    dim = generate_dim_date(start="1402/01/01", end="1402/01/03")
    # Standard expected columns in dim_date
    cols = [
        "jalali_year",
        "jalali_month",
        "jalali_day",
        "gregorian_year",
        "gregorian_month",
        "gregorian_day",
        "day_of_week",
        "day_name_fa",
        "month_name_fa",
        "is_weekend"
    ]
    for col in cols:
        assert col in dim.columns

def test_dim_date_types_and_weekends():
    dim = generate_dim_date(start="1402/01/01", end="1402/01/07", calendar="jalali")
    for w in dim["is_weekend"]:
        assert isinstance(w, bool)
    assert set(dim["day_of_week"]) <= set(range(1, 8))

def test_dim_date_fiscal_columns():
    dim = generate_dim_date(start="1402/01/01", end="1402/01/10", calendar="jalali", include_fiscal=True)
    assert "fiscal_year" in dim.columns
    assert "fiscal_quarter" in dim.columns

def test_dim_date_invalid_input():
    with pytest.raises(Exception):
        generate_dim_date(start="abcd", end="1401/01/10")
    with pytest.raises(Exception):
        generate_dim_date(start="1402/01/15", end="1402/01/10")
    with pytest.raises(ValueError):
        generate_dim_date(start="2024-01-01", end="2024-01-31", calendar="marsian")

def test_dim_date_edge_cases():
    # Single day dimension
    dim = generate_dim_date(start="1402/04/01", end="1402/04/01", calendar="jalali")
    assert len(dim) == 1
    # Month boundary
    dim = generate_dim_date(start="1402/01/30", end="1402/02/02", calendar="jalali")
    assert len(dim) == 4

def test_generate_dim_date_jalali_basic():
    """Test basic Jalali dim date generation."""
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/01/10",
        calendar="jalali"
    )

    assert isinstance(dim, pd.DataFrame)
    assert len(dim) == 10  # 10 days
    assert "date_key" in dim.columns
    assert "full_date" in dim.columns
    assert "year" in dim.columns
    assert "month_name_fa" in dim.columns
    assert "weekday_name_fa" in dim.columns

    # Check first row
    first_row = dim.iloc[0]
    assert first_row["year"] == 1403
    assert first_row["month"] == 1
    assert first_row["day"] == 1
    assert first_row["date_key"] == 14030101


def test_generate_dim_date_gregorian_basic():
    """Test basic Gregorian dim date generation."""
    dim = generate_dim_date(
        start="2024-01-01",
        end="2024-01-10",
        calendar="gregorian"
    )

    assert isinstance(dim, pd.DataFrame)
    assert len(dim) == 10  # 10 days
    assert "date_key" in dim.columns
    assert "month_name_en" in dim.columns
    assert "weekday_name_en" in dim.columns
    assert "month_name_fa" not in dim.columns  # No Persian for Gregorian

    # Check first row
    first_row = dim.iloc[0]
    assert first_row["year"] == 2024
    assert first_row["month"] == 1
    assert first_row["day"] == 1


def test_generate_dim_date_with_fiscal():
    """Test dim date with fiscal year columns."""
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

    # All days should be in fiscal year 1403
    assert all(dim["fiscal_year"] == 1403)


def test_generate_dim_date_with_holidays():
    """Test dim date with holidays."""
    holidays = ["1403/01/01", "1403/01/05"]

    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/01/10",
        calendar="jalali",
        holidays=holidays
    )

    # Check holiday flags
    assert dim.iloc[0]["is_holiday"] == True  # 1403/01/01
    assert dim.iloc[4]["is_holiday"] == True  # 1403/01/05
    assert dim.iloc[1]["is_holiday"] == False  # 1403/01/02


def test_generate_dim_date_weekend():
    """Test weekend detection."""
    dim = generate_dim_date(
        start="1403/08/18",
        end="1403/08/25",
        calendar="jalali"
    )

    # Should have is_weekend column
    assert "is_weekend" in dim.columns
    # At least one weekend day in a week
    assert dim["is_weekend"].sum() >= 1


def test_generate_dim_date_columns():
    """Test all expected columns are present."""
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/01/01",
        calendar="jalali",
        include_fiscal=True
    )

    expected_cols = [
        "date_key", "full_date", "year", "quarter", "month", "day",
        "month_name_en", "month_name_fa", "month_short_en",
        "weekday", "weekday_name_en", "weekday_name_fa",
        "is_weekend", "is_holiday", "is_leap_year",
        "day_of_year", "week_of_year", "days_in_month", "season",
        "fiscal_year", "fiscal_quarter", "fiscal_month"
    ]

    for col in expected_cols:
        assert col in dim.columns, f"Missing column: {col}"


def test_generate_dim_date_full_year():
    """Test generating full year dimension."""
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/12/29",
        calendar="jalali"
    )

    # 1403 is not leap year, so 365 days
    assert len(dim) == 365

    # Check year consistency
    assert all(dim["year"] == 1403)

    # Check all months present
    assert dim["month"].min() == 1
    assert dim["month"].max() == 12


def test_generate_dim_date_leap_year():
    """Test leap year handling."""
    # 1399 is leap year in Jalali
    dim = generate_dim_date(
        start="1399/12/29",
        end="1399/12/30",
        calendar="jalali"
    )

    assert len(dim) == 2
    assert all(dim["is_leap_year"] == True)
    assert dim.iloc[1]["day"] == 30  # Last day exists


def test_generate_dim_date_export_csv(tmp_path):
    """Test exporting to CSV."""
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/01/10",
        calendar="jalali"
    )

    # Export to CSV
    csv_path = tmp_path / "test_dim_date.csv"
    dim.to_csv(csv_path, index=False)

    # Read back
    dim_loaded = pd.read_csv(csv_path)
    assert len(dim_loaded) == 10
    assert list(dim_loaded.columns) == list(dim.columns)


def test_generate_dim_date_gregorian_full_year():
    """Test Gregorian full year."""
    dim = generate_dim_date(
        start="2024-01-01",
        end="2024-12-31",
        calendar="gregorian"
    )

    # 2024 is leap year, so 366 days
    assert len(dim) == 366
    assert all(dim["year"] == 2024)


def test_dimdate_quarter_values():
    """Test quarter calculations."""
    dim = generate_dim_date(
        start="1403/01/01",
        end="1403/12/29",
        calendar="jalali"
    )

    # Check quarters
    q1 = dim[dim["quarter"] == 1]
    q2 = dim[dim["quarter"] == 2]
    q3 = dim[dim["quarter"] == 3]
    q4 = dim[dim["quarter"] == 4]

    # All months 1-3 should be Q1
    assert all(q1["month"].isin([1, 2, 3]))
    # All months 4-6 should be Q2
    assert all(q2["month"].isin([4, 5, 6]))
    # All months 7-9 should be Q3
    assert all(q3["month"].isin([7, 8, 9]))
    # All months 10-12 should be Q4
    assert all(q4["month"].isin([10, 11, 12]))
