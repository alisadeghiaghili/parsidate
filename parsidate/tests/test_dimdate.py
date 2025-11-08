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
