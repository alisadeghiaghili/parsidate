# PARSIDATE_SUMMARY.md

## Overview

ParsiDate is a Python library for professional date management based on Persian (Jalali/Solar Hijri) and Gregorian calendars.

- JalaliDate and GregorianDate main classes
- Conversion methods for Jalali ↔ Gregorian
- Rich parsing/formatting utilities (English and Persian support)
- Date arithmetic and comparison operators
- Complete timezone support (pytz compatible)
- Rounding, range generation, intervals (Period, Duration, Interval)
- Integration with pandas for analytics

---

## Core Classes

- `JalaliDate`: Solar Hijri (Persian) date and time class
- `GregorianDate`: Standard Gregorian date and time class

### Common Attributes

- year, month, day, hour, minute, second, microsecond, tzinfo
- Methods for arithmetic (`add`, `sub`), formatting, copying, comparison

### Example

```
jdate = JalaliDate(1402, 8, 19, 10, 45)
gdate = GregorianDate(2024, 11, 10, 10, 45)
```

---

## Conversion

- `jalali_to_gregorian(year, month, day)` → (year, month, day)
- `gregorian_to_jalali(year, month, day)` → (year, month, day)
- `jalali_to_jdn(year, month, day)` and `gregorian_to_jdn(year, month, day)` for Julian day numbers

---

## Parsing Utilities

- `jmd`, `jdm`: Parse Jalali dates from string (Y/M/D, D/M/Y, with/without time)
- `ymd`, `dmy`: Parse Gregorian dates from string
- Auto parser: `parse_date(str)` (returns appropriate class)

---

## Formatting Utilities

- `format_jalali_date(date, ...)`
- `format_gregorian_date(date, ...)`
- `format_full`, `format_short`, `format_iso`, `format_date_custom`

---

## Operations

### Arithmetic

- `add_days(date, n)`
- `add_months(date, n)`
- `add_years(date, n)`
- `add_weeks(date, n)`

### Comparison

- `eq(a, b)`, `ne(a, b)`, `lt(a, b)`, `le(a, b)`, `gt(a, b)`, `ge(a, b)`
- `between(date, lower, upper)`

### Rounding

- `floor_to_day(date)`, `ceil_to_day(date)`
- `floor_to_week(date)`, `ceil_to_week(date)`
- `floor_to_month(date)`, `ceil_to_month(date)`
- `floor_to_quarter(date)`, `ceil_to_quarter(date)`
- `floor_to_year(date)`, `ceil_to_year(date)`

### Range Generation

- `date_range(start, end, step_days=1)`
- `month_range(start, end)`
- `year_range(start, end)`
- `custom_range(start, end, days=0, months=0, years=0)`

---

## Intervals

- `Period`: Structured period (years, months, days, etc.)
- `Duration`: Elapsed time (days, hours, minutes, ...)
- `Interval`: Time interval with start/end, length

---

## Timezone

- `get_timezone(name)`
- `convert_timezone(datetime, target_zone)`
- `utc_offset_minutes(zone)`
- `is_dst(datetime, zone)`
- Full tz-aware localizing and conversion

---

## Utilities

- `days_in_month(year, month, calendar)`
- `is_jalali_leap(year)`, `is_gregorian_leap(year)`
- `validate_jalali(year, month, day)`, `validate_gregorian(year, month, day)`

---

## DimDate Analytics

- `generate_dim_date(start, end, calendar="jalali", include_fiscal=False)`
- Returns pandas DataFrame dimension with standard columns (`jalali_date`, `gregorian_date`, year/month/day, weekday, fiscal, etc.)

---

## API Notes

- All classes and functions type-annotated
- Full property, operator and mutator support (setter chaining)
- Edge-case and error handling for date/math/timezone

---

## Testing

- Comprehensive tests for:
    - Core classes and properties
    - Conversion, parsing, formatting
    - Arithmetic, comparison, rounding
    - Timezone, intervals, utility helpers
    - dimdate table generation

---

## Further Reading

- [README_COMPLETE.md](README_COMPLETE.md)
- [USAGE_GUIDE.md](USAGE_GUIDE.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

---

Ali Sadeghi Aghili 2025 | GPL v3
