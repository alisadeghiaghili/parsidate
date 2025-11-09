# USAGE_GUIDE.md

## ParsiDate Usage Guide

This guide demonstrates how to use ParsiDate for Jalali/Persian and Gregorian calendar date management.

---

## Create Date Objects

```python
from parsidate.core import JalaliDate, GregorianDate

jdate = JalaliDate(1402, 8, 19, 14, 15, 20)
gdate = GregorianDate(2024, 11, 10, 14, 15, 20)
```

You can set and get individual attributes:

```python
jdate.year(1403).month(9).day(5).hour(9).minute(44)
print(jdate.year(), jdate.month(), jdate.day())
```

---

## Parsing Strings

```python
from parsidate.parsers import jmd, ymd, jdm, dmy, parse_date

date1 = jmd("1402/08/19")
date2 = ymd("2024-11-08")
date3 = jdm("19-08-1402")
date4 = dmy("08/11/2024")
date5 = parse_date("1402/08/19 12:51:20")
```

---

## Formatting Dates

```python
from parsidate.formatting import format_jalali_date, format_gregorian_date

jdate = JalaliDate(1402, 8, 19, 14, 15, 20)
gdate = GregorianDate(2024, 11, 10, 14, 15, 20)

print(format_jalali_date(jdate))
print(format_gregorian_date(gdate))
print(jdate.format("Y/m/d H:i:s"))
print(gdate.format("Y-m-d H:i"))
```

Alternate formats:

```python
from parsidate.formatting import format_full, format_short, format_iso, format_date_custom

print(format_full(jdate, locale="fa"))
print(format_short(gdate, locale="en"))
print(format_iso(jdate))
print(format_date_custom(gdate, "Y-m-d H:i:s", locale="en"))
```

---

## Arithmetic Operations

```python
from parsidate.operations import add_days, add_months, add_years, add_weeks, diff_in_days

jd = JalaliDate(1401, 12, 30)
jd2 = add_days(jd, 7)
jd3 = add_months(jd, 2)
jd4 = add_years(jd, 1)
days_between = diff_in_days(jd2, jd)

gd = GregorianDate(2022, 2, 28)
gd2 = add_weeks(gd, 4)
```

Date subtraction:

```python
d1 = JalaliDate(1402, 1, 10)
d2 = JalaliDate(1402, 1, 18)
duration = d2 - d1
print(duration.days()) # 8
```

Similarly for GregorianDate

---

## Comparison

```python
from parsidate.operations.comparison import eq, ne, gt, lt, ge, le, between

a = JalaliDate(1402, 1, 5)
b = JalaliDate(1402, 1, 12)
assert lt(a, b)
assert ge(b, a)
assert between(a, JalaliDate(1402, 1, 1), JalaliDate(1402, 1, 10)) == True
```

---

## Rounding

```python
from parsidate.operations.rounding import floor_to_week, ceil_to_month

jdate = JalaliDate(1402, 8, 19)
print(floor_to_week(jdate))
print(ceil_to_month(jdate))

gdate = GregorianDate(2024, 11, 10)
print(floor_to_week(gdate))
print(ceil_to_year(gdate))
```

---

## Timezone Handling

```python
from parsidate.timezone import get_timezone, localize_datetime, convert_timezone

import datetime
dt = datetime.datetime(2025, 11, 8, 12, 0)
tz_tehran = get_timezone("Asia/Tehran")
dt_tehran = localize_datetime(dt, "Asia/Tehran")
dt_london = convert_timezone(dt_tehran, "Europe/London")
```

---

## Period, Duration, Interval

```python
from parsidate.intervals.period import Period
from parsidate.intervals.duration import Duration
from parsidate.intervals.interval import Interval

p = Period(years=1, months=5, days=3)
d = Duration(days=10, hours=5)
start = JalaliDate(1402, 8, 19)
end = JalaliDate(1402, 9, 19)
interval = Interval(start, end)
print(interval.length().days)
```

Apply on date:

```python
result = start + p
result2 = start + d
```

---

## DimDate: Date Dimension Table

```python
from parsidate.dimdate import generate_dim_date

df = generate_dim_date(start="1402/01/01", end="1402/01/10", calendar="jalali", include_fiscal=True)
print(df.shape, df.columns)
print(df.head())
```

---

## Utilities

```python
from parsidate.utils.helpers import days_in_month, is_jalali_leap, is_gregorian_leap

print(days_in_month(1401, 12, "jalali"))
print(is_jalali_leap(1399))
print(is_gregorian_leap(2024))
```

---

## Error Handling

All functions and classes raise appropriate exceptions (ValueError, TypeError) for invalid input, edge cases, and improper calendar boundaries.

---

## Testing & Contribution

Run all tests via: `pytest tests/ -v`


For contributions, fork the repository and submit pull requests. All code must comply with GPL-3.0-or-later.

---

Ali Sadeghi Aghili | ParsiDate | Python 2025
