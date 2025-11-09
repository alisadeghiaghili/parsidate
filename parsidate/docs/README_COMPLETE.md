# ParsiDate: Comprehensive Persian/Gregorian Date Toolkit

[![PyPI version](https://badge.fury.io/py/parsidate.svg)](https://badge.fury.io/py/parsidate)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat)](https://pycqa.github.io/isort/)

**ParsiDate** is a comprehensive Python library for working with Persian (Jalali/Solar Hijri) and Gregorian calendars. Inspired by R's powerful [lubridate](https://lubridate.tidyverse.org) package, it provides an intuitive and elegant interface for parsing, manipulating, formatting, and analyzing dates in both calendar systems.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Features](#core-features)
- [Complete API Reference](#complete-api-reference)
  - [Date Parsing](#date-parsing)
  - [Date Components Access](#date-components-access)
  - [Date Arithmetic](#date-arithmetic)
  - [Date Formatting](#date-formatting)
  - [Date Rounding](#date-rounding)
  - [Calendar Conversion](#calendar-conversion)
  - [Date Comparison](#date-comparison)
  - [Timezone Operations](#timezone-operations)
  - [Intervals and Durations](#intervals-and-durations)
  - [Dimension Date Generation](#dimension-date-generation)
  - [Utility Functions](#utility-functions)
- [Examples](#examples)
- [FAQ](#faq)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

### Via pip (Recommended)

```bash
pip install parsidate
```

### For Development

```bash
git clone https://github.com/alisadeghiaghili/parsidate.git
cd parsidate
pip install -e ".[dev]"
```

### Optional Dependencies

For dimension date generation (data warehouse):

```bash
pip install parsidate[dimdate]
```

For all features:

```bash
pip install parsidate[all]
```

## Quick Start

### Basic Date Operations

```python
from parsidate import jmd, ymd, now_jalali

# Parse Persian date
date = jmd("1403/08/18")
print(date)  # JalaliDate(1403, 8, 18, 0, 0, 0)

# Parse Gregorian date
gdate = ymd("2024-11-08")
print(gdate)  # GregorianDate(2024, 11, 8, 0, 0, 0)

# Get current Jalali date
today = now_jalali()
print(today)  # Current date in Jalali calendar
```

### Date Arithmetic

```python
from parsidate import jmd, days, months, years

date = jmd("1403/08/18")

# Add time periods
date_plus = date + months(2) + days(5)
print(date_plus.format("Y/m/d"))  # 1403/10/23

# Subtract time periods
date_minus = date - years(1) - days(10)
print(date_minus.format("Y/m/d"))  # 1402/07/08
```

### Calendar Conversion

```python
from parsidate import jmd, to_gregorian, ymd, to_jalali

# Jalali to Gregorian
jdate = jmd("1403/08/18")
gdate = to_gregorian(jdate)
print(gdate.format("Y-m-d"))  # 2024-11-08

# Gregorian to Jalali
gdate = ymd("2024-11-08")
jdate = to_jalali(gdate)
print(jdate.format("Y/m/d"))  # 1403/08/18
```

## Core Features

- **Dual Calendar Support**: Seamlessly work with Persian and Gregorian calendars
- **Intuitive Parsing**: Multiple date format parsing (jmd, ymd, jdm, dmy, etc.)
- **Comprehensive Arithmetic**: Add, subtract, and manipulate dates effortlessly
- **Flexible Formatting**: Format dates with custom patterns and Persian/English output
- **Timezone Support**: Handle timezone conversions automatically
- **Data Warehousing**: Generate complete date dimension tables
- **Type-Safe**: Full type hints for better IDE support
- **Well-Tested**: Comprehensive test suite with >90% coverage

## Complete API Reference

### Date Parsing

#### Parse Persian Dates

```python
from parsidate import jmd, jdm, jmdy, jdmy, jmd_hms

# Year/Month/Day format
date1 = jmd("1403/08/18")
date2 = jmd("1403-08-18")  # Also supports dashes
print(date1.year())   # 1403
print(date1.month())  # 8
print(date1.day())    # 18

# Day/Month/Year format
date3 = jdm("18/08/1403")
print(date3 == date1)  # True

# Month/Day/Year format
date4 = jmdy("08/18/1403")
print(date4 == date1)  # True

# Day/Month/Year (alias)
date5 = jdmy("18/08/1403")
print(date5 == date1)  # True

# With time component
date_time = jmd_hms("1403/08/18 14:30:25")
print(date_time.hour())    # 14
print(date_time.minute())  # 30
print(date_time.second())  # 25

# With timezone
import pytz
date_tz = jmd_hms("1403/08/18 14:30:00", tz="Asia/Tehran")
print(date_tz.tzinfo())  # Asia/Tehran
```

#### Parse Gregorian Dates

```python
from parsidate import ymd, ydm, mdy, dmy, ymd_hms

# Year-Month-Day format
date1 = ymd("2024-11-08")
date2 = ymd("2024/11/08")  # Also works with slashes

# Day-Month-Year format
date3 = dmy("08-11-2024")
print(date3 == date1)  # True

# Month-Day-Year format
date4 = mdy("11-08-2024")
print(date4 == date1)  # True

# Year-Day-Month format
date5 = ydm("2024-08-11")
print(date5 == date1)  # True

# With time
date_time = ymd_hms("2024-11-08 14:30:25")
print(date_time)  # 2024-11-08 14:30:25
```

#### Current Date and Time

```python
from parsidate import now_jalali, now_gregorian, today_jalali, today_gregorian

# Get current Jalali date and time
now_j = now_jalali()
print(now_j)  # Current Jalali date with time

# Get current Gregorian date and time
now_g = now_gregorian()
print(now_g)  # Current Gregorian date with time

# Get today's Jalali date (without time)
today_j = today_jalali()
print(today_j)  # Current Jalali date at 00:00:00

# Get today's Gregorian date (without time)
today_g = today_gregorian()
print(today_g)  # Current Gregorian date at 00:00:00
```

### Date Components Access

```python
from parsidate import jmd

date = jmd("1403/08/18")

# Get components
year = date.year()      # 1403
month = date.month()    # 8
day = date.day()        # 18
hour = date.hour()      # 0
minute = date.minute()  # 0
second = date.second()  # 0

# Derived values
weekday = date.weekday()      # 0-6 (0=Saturday, 6=Friday)
quarter = date.quarter()      # 1-4
day_of_year = date.day_of_year()  # 1-365/366
is_leap = date.is_leap_year()     # True/False

# Set components (returns self for chaining)
date.year(1404)
date.month(1)
date.day(1)
date.hour(12)
date.minute(30)
date.second(45)

print(date)  # JalaliDate(1404, 1, 1, 12, 30, 45)
```

### Date Arithmetic

#### Adding Time

```python
from parsidate import jmd, days, months, years, weeks, hours, minutes, seconds

date = jmd("1403/08/18")

# Add days
new_date = date + days(10)
print(new_date.format("Y/m/d"))  # 1403/08/28

# Add months
new_date = date + months(3)
print(new_date.format("Y/m/d"))  # 1403/11/18

# Add years
new_date = date + years(1)
print(new_date.format("Y/m/d"))  # 1404/08/18

# Add weeks
new_date = date + weeks(2)
print(new_date.format("Y/m/d"))  # 1403/09/01

# Combine multiple periods
new_date = date + years(1) + months(2) + days(5)
print(new_date.format("Y/m/d"))  # 1404/10/23

# Add time components
new_date = date + hours(5) + minutes(30) + seconds(15)
print(new_date.format("Y/m/d H:i:s"))  # 1403/08/18 05:30:15
```

#### Subtracting Time

```python
from parsidate import jmd, days, months, years

date = jmd("1403/08/18")

# Subtract days
new_date = date - days(5)
print(new_date.format("Y/m/d"))  # 1403/08/13

# Subtract months
new_date = date - months(2)
print(new_date.format("Y/m/d"))  # 1403/06/18

# Subtract years
new_date = date - years(1)
print(new_date.format("Y/m/d"))  # 1402/08/18

# Combine multiple periods
new_date = date - years(1) - months(3) - days(10)
print(new_date.format("Y/m/d"))  # 1402/05/08

# Direct method calls
date2 = date.copy()
date2.sub(days=10, months=2)
print(date2.format("Y/m/d"))  # 1403/06/08
```

#### Method Chaining

```python
from parsidate import jmd, months, days

date = jmd("1403/08/18")

# Chain operations
result = date.copy().add(months=1).add(days=5).add(hours=3)
print(result.format("Y/m/d H:i:s"))  # 1403/09/23 03:00:00
```

### Date Formatting

#### Format Codes

```python
from parsidate import jmd

date = jmd("1403/08/18")

# Basic components
print(date.format("Y/m/d"))              # 1403/08/18 (4-digit year, leading zeros)
print(date.format("y/m/d"))              # 03/08/18 (2-digit year)
print(date.format("Y/n/j"))              # 1403/8/18 (no leading zeros for month/day)
print(date.format("Y-m-d"))              # 1403-08-18 (with dashes)

# Time components
print(date.format("H:i:s"))              # 00:00:00
print(date.format("H:i"))                # 00:00
print(date.format("Y/m/d H:i:s"))        # 1403/08/18 00:00:00

# Names and descriptions
print(date.format("E", "en"))            # Aban (month name in English)
print(date.format("E", "fa"))            # آبان (month name in Persian)
print(date.format("l", "en"))            # Friday (weekday name in English)
print(date.format("l", "fa"))            # جمعه (weekday name in Persian)
print(date.format("M", "en"))            # Aba (short month name)

# Combined formats
print(date.format("l, j E Y", "en"))     # Friday, 18 Aban 1403
print(date.format("l, j E Y", "fa"))     # جمعه, ۱۸ آبان ۱۴۰۳

# Other codes
print(date.format("q"))                  # 3 (quarter)
print(date.format("w"))                  # 4 (weekday number: 0=Saturday)
print(date.format("L"))                  # 1 (1 if leap year, 0 otherwise)
```

#### Persian Output

```python
from parsidate import jmd

date = jmd("1403/08/18")

# English locale (default)
print(date.format("Y/m/d", "en"))  # 1403/08/18

# Persian locale (Persian numerals)
print(date.format("Y/m/d", "fa"))  # ۱۴۰۳/۰۸/۱۸

# Custom format with Persian output
print(date.format("l, j E Y", "fa"))  # جمعه, ۱۸ آبان ۱۴۰۳
```

### Date Rounding

```python
from parsidate import jmd, floor_date, ceiling_date, round_date

date = jmd("1403/08/18")

# Floor to start of period
start_of_year = floor_date(date, "year")
print(start_of_year.format("Y/m/d"))    # 1403/01/01

start_of_month = floor_date(date, "month")
print(start_of_month.format("Y/m/d"))   # 1403/08/01

start_of_day = floor_date(date, "day")
print(start_of_day.format("Y/m/d"))     # 1403/08/18

# Ceiling to start of next period
next_year = ceiling_date(date, "year")
print(next_year.format("Y/m/d"))        # 1404/01/01

next_month = ceiling_date(date, "month")
print(next_month.format("Y/m/d"))       # 1403/09/01

# Round to nearest period
nearest_month = round_date(date, "month")
print(nearest_month.format("Y/m/d"))    # Depends on day
```

### Calendar Conversion

```python
from parsidate import jmd, ymd, to_gregorian, to_jalali

# Jalali to Gregorian
jdate = jmd("1403/08/18")
gdate = to_gregorian(jdate)
print(gdate.format("Y-m-d"))            # 2024-11-08

# Gregorian to Jalali
gdate = ymd("2024-11-08")
jdate = to_jalali(gdate)
print(jdate.format("Y/m/d"))            # 1403/08/18

# Round-trip conversion
jdate1 = jmd("1403/08/18")
gdate = to_gregorian(jdate1)
jdate2 = to_jalali(gdate)
print(jdate1 == jdate2)                 # True
```

### Date Comparison

```python
from parsidate import jmd, is_before, is_after, is_between

date1 = jmd("1403/08/18")
date2 = jmd("1403/08/25")
date3 = jmd("1403/09/01")

# Using methods
print(is_before(date1, date2))          # True
print(is_after(date3, date2))           # True
print(is_between(date2, date1, date3))  # True

# Using operators
print(date1 < date2)                    # True
print(date1 <= date2)                   # True
print(date2 > date1)                    # True
print(date2 >= date1)                   # True
print(date1 == date1)                   # True
print(date1 != date2)                   # True

# Sorting dates
dates = [date3, date1, date2]
sorted_dates = sorted(dates)
print([d.format("Y/m/d") for d in sorted_dates])
# ['1403/08/18', '1403/08/25', '1403/09/01']
```

### Timezone Operations

```python
from parsidate import jmd_hms, with_tz, force_tz

# Create date with timezone
date_tehran = jmd_hms("1403/08/18 14:30:00", tz="Asia/Tehran")
print(date_tehran.format("Y/m/d H:i:s"))  # 1403/08/18 14:30:00

# Convert to different timezone
date_utc = with_tz(date_tehran, "UTC")
print(date_utc.format("Y/m/d H:i:s"))     # 1403/08/18 11:00:00 (UTC)

date_ny = with_tz(date_tehran, "America/New_York")
print(date_ny.format("Y/m/d H:i:s"))      # 1403/08/18 06:00:00 (NY)

# Force timezone without conversion (time unchanged)
date_forced = force_tz(date_tehran, "UTC")
print(date_forced.format("Y/m/d H:i:s"))  # 1403/08/18 14:30:00 (but in UTC)
```

### Intervals and Durations

#### Duration (Exact Time)

```python
from parsidate import jmd, duration, days, hours, minutes, seconds

date = jmd("1403/08/18")

# Create durations
dur1 = duration(days=10, hours=5, minutes=30)
dur2 = days(5) + hours(3) + minutes(15) + seconds(30)

# Add to date
date_plus = date + dur1
print(date_plus.format("Y/m/d"))  # 1403/08/28

# Get duration info
print(dur1.days())           # 10
print(dur1.total_seconds())  # 902400 (+ 5 hours 30 minutes)
```

#### Period (Calendar-based)

```python
from parsidate import jmd, period, years, months, weeks

date = jmd("1403/08/18")

# Create periods
per1 = period(years=1, months=2, days=10)
per2 = years(1) + months(3) + weeks(2)

# Add to date
date_plus = date + per1
print(date_plus.format("Y/m/d"))  # 1404/10/28

# Period arithmetic (calendar-based, not exact seconds)
```

#### Interval (Date Range)

```python
from parsidate import jmd, interval

start = jmd("1403/08/01")
end = jmd("1403/08/31")

# Create interval
inv = interval(start, end)

# Check membership
check_date = jmd("1403/08/15")
print(check_date in inv)      # True

check_date2 = jmd("1403/09/01")
print(check_date2 in inv)     # False

# Get interval length
length = inv.length(unit="days")
print(length)                 # 30
```

### Dimension Date Generation

```python
from parsidate.dimdate import generate_dim_date
import pandas as pd

# Generate Jalali date dimension
dim_jalali = generate_dim_date(
    start="1400/01/01",
    end="1400/12/29",
    calendar="jalali",
    include_fiscal=True,
    fiscal_year_start_month=1
)

# Display structure
print(dim_jalali.head())
print(dim_jalali.shape)  # (365, XX) rows and columns

# Columns included:
# date_key, full_date, year, quarter, month, day,
# month_name_fa, month_name_en, weekday, weekday_name_fa, weekday_name_en,
# is_weekend, is_holiday, is_leap_year, day_of_year, week_of_year,
# days_in_month, season, fiscal_year, fiscal_quarter, fiscal_month

# Export to CSV
dim_jalali.to_csv("dim_date_jalali.csv", index=False)

# Generate Gregorian date dimension
dim_gregorian = generate_dim_date(
    start="2021-01-01",
    end="2021-12-31",
    calendar="gregorian",
    include_fiscal=True,
    fiscal_year_start_month=1
)

# With holidays
holidays = ["1400/01/01", "1400/02/11", "1400/12/29"]
dim_with_holidays = generate_dim_date(
    start="1400/01/01",
    end="1400/12/29",
    calendar="jalali",
    holidays=holidays
)
```

### Utility Functions

```python
from parsidate.utils import (
    is_leap_year, days_in_month, month_name, weekday_name,
    get_season, to_persian_digits, to_english_digits
)

# Leap year check
print(is_leap_year(1403, "jalali"))      # True
print(is_leap_year(1402, "jalali"))      # False
print(is_leap_year(2024, "gregorian"))   # True

# Days in month
print(days_in_month(1403, 12, "jalali"))    # 30
print(days_in_month(1402, 12, "jalali"))    # 29

# Month names
print(month_name(8, "en", "jalali"))        # "Aban"
print(month_name(8, "fa", "jalali"))        # "آبان"
print(month_name(11, "en", "gregorian"))    # "November"

# Weekday names
print(weekday_name(4, "en", "jalali"))      # "Chaharshanbe"
print(weekday_name(4, "fa", "jalali"))      # "چهارشنبه"

# Season
print(get_season(1, "jalali"))              # "Spring"
print(get_season(7, "jalali"))              # "Fall"

# Digit conversion
print(to_persian_digits("1403/08/18"))      # "۱۴۰۳/۰۸/۱۸"
print(to_english_digits("۱۴۰۳/۰۸/۱۸"))     # "1403/08/18"
```

## Examples

### Real-World Use Cases

#### Calculate Age

```python
from parsidate import now_jalali, jmd

birthdate = jmd("1360/05/15")
today = now_jalali()

age = today.year() - birthdate.year()
if (today.month(), today.day()) < (birthdate.month(), birthdate.day()):
    age -= 1

print(f"Age: {age} years")  # Age: 43 years
```

#### Working with Business Calendars

```python
from parsidate import jmd, is_leap_year, weekday_name

fiscal_year_start = jmd("1403/01/01")
fiscal_year_end = jmd("1403/12/29")

print(f"Fiscal year: {fiscal_year_start.format('Y/m/d')}")
print(f"Days: {(fiscal_year_end - fiscal_year_start).days()}")
print(f"Start day: {weekday_name(fiscal_year_start.weekday(), 'en')}")
```

#### Persian Date Range Iteration

```python
from parsidate import jmd, days

start = jmd("1403/08/01")
end = jmd("1403/08/10")

current = start.copy()
while current <= end:
    print(current.format("Y/m/d l", "en"))
    current = current.copy()
    current.add(days=1)
```

#### Convert Multiple Dates

```python
from parsidate import jmd, to_gregorian

jalali_dates = ["1403/08/18", "1403/09/20", "1403/10/15"]
gregorian_dates = []

for jdate_str in jalali_dates:
    jdate = jmd(jdate_str)
    gdate = to_gregorian(jdate)
    gregorian_dates.append(gdate.format("Y-m-d"))

print(gregorian_dates)
# ['2024-11-08', '2024-12-10', '2025-01-04']
```

#### Generate Monthly Reports

```python
from parsidate import jmd, floor_date, ceiling_date, is_between

report_date = jmd("1403/08/15")

month_start = floor_date(report_date, "month")
month_end = ceiling_date(report_date, "month")

print(f"Report for: {report_date.format('E Y', 'en')}")
print(f"Period: {month_start.format('Y/m/d')} to {month_end.format('Y/m/d')}")
```

## FAQ

### General Questions

**Q: What is the difference between Jalali and Gregorian calendars?**

A: Jalali (Persian/Solar Hijri) calendar is used in Iran and Afghanistan. It's a solar calendar based on the vernal equinox. Gregorian is the Western calendar used internationally.

**Q: Can I use ParsiDate for historical dates?**

A: Yes, ParsiDate supports dates from year 1 onwards for both calendars. However, accuracy for very ancient dates may vary due to calendar reform history.

**Q: Does ParsiDate handle daylight saving time?**

A: ParsiDate uses pytz for timezone handling. DST is handled automatically through timezone definitions.

### Usage Questions

**Q: How do I work with time zones?**

A: Use `jmd_hms()` or `ymd_hms()` with the `tz` parameter, or use `with_tz()` and `force_tz()` functions.

**Q: Can I perform arithmetic with mixed calendars?**

A: No. All arithmetic must be within the same calendar. Use conversion functions to switch calendars.

**Q: How do I compare dates from different calendars?**

A: Convert to the same calendar first using `to_gregorian()` or `to_jalali()`, then compare.

**Q: What's the performance for large date ranges?**

A: ParsiDate is optimized for typical use cases. For very large datasets (millions of dates), consider using dimension date tables (see `generate_dim_date()`).

### Development Questions

**Q: Is ParsiDate production-ready?**

A: Yes. ParsiDate has >90% test coverage and is used in production environments.

**Q: Can I contribute to ParsiDate?**

A: Absolutely! See the [Contributing](#contributing) section below.

**Q: How do I report bugs?**

A: Open an issue on [GitHub Issues](https://github.com/alisadeghiaghili/parsidate/issues).

## Requirements

- **Python**: 3.8 or higher
- **Core Dependencies**:
  - `python-dateutil >= 2.8.0`
  - `pytz >= 2021.1`
- **Optional Dependencies**:
  - `pandas >= 1.5.0` (for dimension date generation)
  - `numpy >= 1.21.0` (for advanced operations)

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ -v --cov=parsidate --cov-report=html
```

### Check Code Quality

```bash
# Format code
black parsidate/

# Sort imports
isort parsidate/

# Type checking
mypy parsidate/

# Linting
flake8 parsidate/ --max-line-length=88
```

## Contributing

We welcome contributions from everyone! Here's how you can help:

### Getting Started

1. **Fork the Repository**
   ```bash
   # Go to https://github.com/alisadeghiaghili/parsidate
   # Click "Fork" button
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/alisadeghiaghili/parsidate.git
   cd parsidate
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

4. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

### Making Changes

1. **Write Code** following PEP 8 standards
2. **Add Tests** for new functionality
3. **Update Documentation** as needed
4. **Run Quality Checks**
   ```bash
   black parsidate/
   isort parsidate/
   flake8 parsidate/
   mypy parsidate/
   pytest tests/ -v --cov=parsidate
   ```

### Submitting Changes

1. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

2. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Go to https://github.com/alisadeghiaghili/parsidate/pulls
   - Click "New Pull Request"
   - Fill in the PR template
   - Submit!

### Guidelines

- Follow PEP 8 style guide
- Write meaningful commit messages
- Include tests for new features
- Update documentation
- Keep PRs focused and concise

### What We're Looking For

- **Bug Fixes**: Report or fix bugs
- **Features**: New functionality or enhancements
- **Documentation**: Improvements to docs or examples
- **Tests**: Additional test coverage
- **Performance**: Optimizations
- **Translations**: Support for additional languages

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Support

### Getting Help

1. **Read Documentation**: Check [complete API reference](#complete-api-reference)
2. **Search Issues**: Look for similar questions/issues on GitHub
3. **Open New Issue**: If not found, open a new issue with:
   - Clear description
   - Code example
   - Expected vs actual behavior
   - Python version

### Report Bugs

Open an issue with:
- **Title**: Brief description
- **Description**: Detailed explanation
- **Steps to Reproduce**: Code example
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Python version, OS, etc.

### Request Features

Open a discussion/issue with:
- **Title**: Feature description
- **Motivation**: Why this is needed
- **Use Cases**: Real-world examples
- **Proposed Solution**: How it should work

## License

**GNU General Public License v3.0 or later (GPL-3.0-or-later)**

ParsiDate is free and open-source software. You can use, modify, and distribute it under the terms of the GPL-3.0-or-later license.

### Attribution Requirement

When you use ParsiDate, you **MUST**:
1. Include the author name: **Ali Sadeghi Aghili**
2. Reference the repository: https://github.com/alisadeghiaghili/parsidate
3. Include the license: GPL-3.0-or-later
4. Document any modifications

See [ATTRIBUTION.md](../../ATTRIBUTION.md) for complete details and examples.

### What This Means

- **Free to Use**: No licensing fees
- **Free to Modify**: Change the code as needed
- **Free to Distribute**: Share with others
- **Must Share Modifications**: Any improvements should be shared back
- **Must Provide Source**: If distributed, source code must be available
- **Must Attribute**: Always credit the original author
- **Derivative Works**: Must use same license

## Acknowledgments

ParsiDate stands on the shoulders of giants:

### Projects We're Built On

- **[jalali](https://github.com/shobeiry/jalali)** by Shobeiry
  - Persian calendar algorithms
  - License: GPL-3.0
  - [Repository](https://github.com/shobeiry/jalali)

- **[lubridate](https://lubridate.tidyverse.org)** by Hadley Wickham, Garrett Grolemund, Vitalie Spinu
  - Date manipulation API design
  - Intuitive interface concepts
  - License: GPL-3.0
  - [Repository](https://github.com/tidyverse/lubridate)

### Contributors

We thank all contributors who have helped improve ParsiDate!

### Special Thanks

- Persian developer community for feedback and support
- Open-source maintainers for inspiration and guidance
- Everyone who reports bugs and suggests improvements

## Changelog

See [CHANGELOG.md](../../CHANGELOG.md) for version history and updates.

## Roadmap

### Planned Features

- [ ] Islamic (Hijri Qamari) calendar support
- [ ] Performance optimizations
- [ ] Additional locale support

### Community Requests

Have a feature request? [Open an issue](https://github.com/alisadeghiaghili/parsidate/issues)!

## Related Projects

- **[jalaali-js](https://github.com/jalaali/jalaali-js)** - JavaScript Jalali calendar
- **[jalali](https://github.com/shobeiry/jalali)** - Python Jalali calendar
- **[datetime](https://docs.python.org/3/library/datetime.html)** - Python's built-in datetime
- **[python-dateutil](https://dateutil.readthedocs.io/)** - Extended datetime support

## Getting in Touch

- **Email**: alisadeghiaghili@gmail.com
- **GitHub**: [alisadeghiaghili/parsidate](https://github.com/alisadeghiaghili/parsidate)
- **Issues**: [GitHub Issues](https://github.com/alisadeghiaghili/parsidate/issues)
- **Discussions**: [GitHub Discussions](https://github.com/alisadeghiaghili/parsidate/discussions)

## Star History

If you find ParsiDate useful, please consider giving us a star on GitHub!

[![Star History Chart](https://api.github.com/repos/alisadeghiaghili/parsidate/stargazers)](https://github.com/alisadeghiaghili/parsidate)

---

**Made with care for the Persian developer community** ❤️

*ParsiDate: Making Persian dates easy since 2024*
