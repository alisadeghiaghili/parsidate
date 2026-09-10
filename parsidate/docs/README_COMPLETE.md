# 📖 ParsiDate Complete Documentation

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Classes](#core-classes)
- [Parsing](#parsing)
- [Formatting (strftime)](#formatting-strftime)
- [Date Arithmetic](#date-arithmetic)
- [Comparison](#comparison)
- [Rounding](#rounding)
- [Intervals](#intervals)
- [Timezone](#timezone)
- [DimDate Tables](#dimdate-tables)
- [Utilities](#utilities)
- [API Reference](#api-reference)
- [Examples](#examples)

---

## Introduction {#introduction}

**ParsiDate** is a comprehensive date/time library for **Persian (Jalali/Solar Hijri)** and **Gregorian** calendars in Python.

**Key Features:**
- ✅ **Full strftime compatibility** (Python standard)
- ✅ **Bidirectional calendar conversion**
- ✅ **Date arithmetic** (add/subtract years, months, days, etc.)
- ✅ **Timezone support** (Asia/Tehran, etc.)
- ✅ **Pandas integration** for analytics
- ✅ **100% test coverage**

Inspired by R's [lubridate](https://lubridate.tidyverse.org).

---

## Installation {#installation}

```bash
pip install parsidate
```

---

## Quick Start {#quick-start}

```python
from parsidate.core import JalaliDate, GregorianDate
from parsidate.parsers import jmd, ymd

# Create dates
jdate = JalaliDate(1402, 8, 18, 14, 45, 30)  # 1402/08/18 14:45:30
gdate = GregorianDate(2024, 11, 9, 10, 30)   # 2024-11-09 10:30

# Formatting (Python strftime ✅)
print(jdate.strftime("%Y/%m/%d %H:%M:%S"))           # 1402/08/18 14:45:30
print(jdate.strftime("%A، %d %B %Y", locale="fa"))   # سه‌شنبه، ۱۸ آبان ۱۴۰۲
print(gdate.strftime("%Y-%m-%d %I:%M %p"))           # 2024-11-09 10:30 AM

# Arithmetic
future = jdate.add(months=2, days=5)
days_diff = (future - jdate).days

# Parsing
j_parsed = jmd("1402/08/19 12:30")
g_parsed = ymd("2024-11-09")
```

---

## Core Classes {#core-classes}

### JalaliDate
```python
jdate = JalaliDate(1402, 8, 18, 14, 45, 30)

# Getters/Setters (chainable)
print(jdate.year(), jdate.month(), jdate.day())     # 1402 8 18
jdate.year(1403).month(9).day(5)                    # Chainable

# Properties
print(jdate.weekday())      # 0=Saturday, 6=Friday
print(jdate.quarter())      # 1-4
print(jdate.day_of_year())  # 1-366
print(jdate.is_leap_year()) # True/False
```

### GregorianDate
```python
gdate = GregorianDate(2024, 11, 9)
# Same interface as JalaliDate
print(gdate.strftime("%Y-%m-%d"))  # 2024-11-09
```

---

## Parsing {#parsing}

```python
from parsidate.parsers import jmd, ymd, jdm, dmy, parse_date

# Jalali formats
j1 = jmd("1402/08/19")      # YYYY/MM/DD
j2 = jdm("19-08-1402")      # DD-MM-YYYY

# Gregorian formats
g1 = ymd("2024-11-09")      # YYYY-MM-DD
g2 = dmy("09/11/2024")      # DD/MM/YYYY

# Auto-detect
auto = parse_date("1402/08/19 14:30")  # JalaliDate
```

---

## Formatting (strftime) {#formatting-strftime}

**ParsiDate uses Python-standard `strftime` format codes** ✅

### Basic Examples
```python
jdate = JalaliDate(1402, 8, 18, 14, 45, 30)

# Date only
print(jdate.strftime("%Y/%m/%d"))           # 1402/08/18
print(jdate.strftime("%d/%m/%Y"))           # 18/08/1402
print(jdate.strftime("%Y-%m-%d"))           # 1402-08-18

# Date + Time
print(jdate.strftime("%Y/%m/%d %H:%M:%S"))  # 1402/08/18 14:45:30

# Persian names
print(jdate.strftime("%A، %d %B %Y", locale="fa"))  # سه‌شنبه، ۱۸ آبان ۱۴۰۲

# 12-hour format
print(jdate.strftime("%I:%M %p", locale="fa"))  # ۰۲:۴۵ ب.ظ
```

### Complete Format Codes

| Code | Description | Example (fa) | Example (en) |
|------|-------------|--------------|--------------|
| `%Y` | 4-digit year | `1402` | `2024` |
| `%y` | 2-digit year | `02` | `24` |
| `%m` | Month (01-12) | `08` | `11` |
| `%-m` | Month (1-12) | `8` | `11` |
| `%d` | Day (01-31) | `18` | `09` |
| `%-d` | Day (1-31) | `18` | `9` |
| `%H` | Hour 24h (00-23) | `14` | `14` |
| `%I` | Hour 12h (01-12) | `02` | `02` |
| `%M` | Minute (00-59) | `45` | `45` |
| `%S` | Second (00-59) | `30` | `30` |
| `%p` | AM/PM | `ب.ظ` | `PM` |
| `%B` | Full month | `آبان` | `November` |
| `%b` | Short month | `آبا` | `Nov` |
| `%A` | Full weekday | `سه‌شنبه` | `Tuesday` |
| `%a` | Short weekday | `س` | `Tue` |
| `%w` | Weekday number | `2` | `2` |

**Backward compatibility:** `jdate.format()` still works (redirects to `strftime`)

---

## Date Arithmetic {#date-arithmetic}

### Method Chaining
```python
jdate = JalaliDate(1402, 8, 18)
future = jdate.add(years=1, months=2, days=5, hours=3)
```

### Operations Module
```python
from parsidate.operations import add_days, add_months, diff_in_days

jd1 = JalaliDate(1402, 1, 1)
jd2 = add_days(jd1, 30)
days = diff_in_days(jd2, jd1)  # 30
```

### Operators
```python
d1 = JalaliDate(1402, 1, 10)
d2 = JalaliDate(1402, 1, 18)
duration = d2 - d1  # Duration(days=8)
```

---

## Comparison {#comparison}

```python
from parsidate.operations.comparison import eq, lt, gt, between

d1 = JalaliDate(1402, 1, 5)
d2 = JalaliDate(1402, 1, 12)

eq(d1, d2)      # False
lt(d1, d2)      # True
between(d1, JalaliDate(1402, 1, 1), d2)  # True
```

---

## Rounding {#rounding}

```python
from parsidate.operations.rounding import floor_to_month, ceil_to_week

jdate = JalaliDate(1402, 8, 19, 10, 30)

floor_to_month(jdate)   # 1402/08/01 00:00:00
ceil_to_week(jdate)     # Next Saturday 00:00:00
```

---

## Intervals {#intervals}

```python
from parsidate.intervals import Period, Duration, Interval

p = Period(years=1, months=3, days=5)
d = Duration(days=10, hours=5)

start = JalaliDate(1402, 8, 1)
result = start + p  # 1403/11/06

interval = Interval(start, start.add(months=1))
print(interval.length().days)  # ~30
```

---

## Timezone {#timezone}

```python
from parsidate.timezone import get_timezone, convert_timezone
import datetime

dt = datetime.datetime(2025, 1, 1, 12, 0)
tehran_tz = get_timezone("Asia/Tehran")
localized = localize_datetime(dt, "Asia/Tehran")
london_time = convert_timezone(localized, "Europe/London")
```

---

## DimDate Tables {#dimdate-tables}

```python
from parsidate.dimdate import generate_dim_date
import pandas as pd

df = generate_dim_date(
    start="1402/01/01",
    end="1402/01/07",
    calendar="jalali",
    include_fiscal=True
)
# Returns pandas DataFrame with:
# date, year, month, day, weekday, quarter, is_holiday, fiscal_year, etc.
```

---

## Utilities {#utilities}

```python
from parsidate.utils.helpers import (
    days_in_month, is_jalali_leap, 
    jalali_to_gregorian, gregorian_to_jalali
)

print(days_in_month(1402, 8, "jalali"))         # 31
print(is_jalali_leap(1403))                     # True/False
gy, gm, gd = jalali_to_gregorian(1402, 8, 18)   # (2023, 11, 9)
```

---

## API Reference {#api-reference}

See detailed [API docs](API_REFERENCE.md)

---

## Examples {#examples}

### Persian Date Pipeline
```python
from parsidate.core import JalaliDate
from parsidate.parsers import jmd
from parsidate.operations import add_months

# Parse → Transform → Format
raw = "1402/08/18"
jdate = jmd(raw)
next_month = add_months(jdate, 1)
formatted = next_month.strftime("%Y/%m/%d (%A)", locale="fa")
print(formatted)  # 1402/09/18 (چهارشنبه)
```

### Calendar Conversion
```python
jdate = JalaliDate(1402, 8, 18)
gy, gm, gd = jdate.to_gregorian()  # (2023, 11, 9)
gdate = GregorianDate(*jdate.to_gregorian())
```

### Analytics Prep
```python
df = generate_dim_date("1402/01/01", "1402/12/29", include_fiscal=True)
df['jalali_date'] = df['date'].apply(lambda x: x.strftime("%Y/%m/%d"))
```

---

**👨‍💻 Author:** Ali Sadeghi Aghili  
**📧 Email:** alisadeghiaghili@gmail.com  
**🌐 GitHub:** [alisadeghiaghili/parsidate](https://github.com/alisadeghiaghili/parsidate)

**⭐ Star if helpful!**
