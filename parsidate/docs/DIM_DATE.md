# dim_date warehouse columns

Requires: `pip install parsidate[dimdate]` (pandas).

## Generate

```python
from parsidate.dimdate import generate_dim_date
from parsidate.core.jalali import JalaliDate

dim = generate_dim_date(
    start="1403/01/01",
    end="1403/12/30",
    calendar="jalali",
    include_fiscal=True,
    use_iran_holidays=True,   # official Iranian holidays
    as_of=JalaliDate(1403, 2, 15),  # for ytd/mtd flags
)
dim.to_csv("dim_date_1403.csv", index=False)
```

## Column dictionary (core)

| Column | Type | Meaning |
|--------|------|---------|
| date_key | int | YYYYMMDD |
| full_date | str | `strftime` pattern |
| is_weekend | bool | weekend_days config |
| is_holiday | bool | official or custom |
| is_business_day | bool | not weekend and not holiday |
| holiday_name | str | label if holiday |
| iso_year / iso_week / iso_weekday | int | ISO week of Gregorian equivalent |
| month_start / month_end | str | month bounds |
| ytd_flag / mtd_flag | bool | vs `as_of` |
| fiscal_year / fiscal_quarter / fiscal_month | int | IR fiscal defaults |

## Defaults

- Jalali weekend: Friday (`6` in Sat=0 numbering)
- Gregorian weekend: Sat+Sun
- Jalali holidays: bundled official set when `use_iran_holidays=True`
