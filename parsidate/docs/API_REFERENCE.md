# API_REFERENCE.md

## ParsiDate API Reference

---

### Core Classes

#### JalaliDate

class JalaliDate:
```python
def __init__(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
year() # Get/set year
month() # Get/set month
day() # Get/set day
hour() # Get/set hour
minute() # Get/set minute
second() # Get/set second
microsecond() # Get/set microsecond
tzinfo() # Get/set time zone
strftime(pattern: str, locale='fa'|'en') -> str  # Format using strftime codes
format(pattern: str, locale='fa'|'en') -> str    # Alias for strftime
copy() # Return a new copy
is_leap_year() # True if leap
weekday() # 0-6 (Saturday=0)
quarter() # 1-4
day_of_year() # 1-366
add(**kwargs) # Arithmetic: years, months, days, hours, minutes, seconds
sub(**kwargs) # Negative arithmetic
to_gregorian() # Tuple (year, month, day)
str, repr, comparison ops
```

**strftime Format Codes:**
```
%Y - 4-digit year (1402)
%y - 2-digit year (02)
%m - month with leading zero (01-12)
%d - day with leading zero (01-31)
%H - hour 24-hour format (00-23)
%I - hour 12-hour format (01-12)
%M - minute (00-59)
%S - second (00-59)
%f - microsecond (000000-999999)
%p - AM/PM (ق.ظ/ب.ظ in Farsi)
%B - full month name (Farvardin, فروردین)
%b - abbreviated month name (Far, فرو)
%A - full weekday name (Shanbe, شنبه)
%a - abbreviated weekday name (Sha, ش)
%w - weekday as number (0-6)
%j - day of year (001-366)
%% - literal %

Non-standard:
%-m, %-d, %-H, %-I, %-M, %-S - without leading zeros
```

#### GregorianDate

Similar attributes and methods as JalaliDate.

---

### Converters

```python
jalali_to_gregorian(year, month, day) -> (year, month, day)
gregorian_to_jalali(year, month, day) -> (year, month, day)
jalali_to_jdn(year, month, day) -> int (Julian Day Number)
gregorian_to_jdn(year, month, day) -> int
jdn_to_jalali(jdn) -> (year, month, day)
jdn_to_gregorian(jdn) -> (year, month, day)
```

---

### Parsers

```python
jmd(str) # Parse Jalali date string "YYYY/MM/DD"
ymd(str) # Parse Gregorian date string "YYYY-MM-DD"
jdm(str) # "DD-MM-YYYY" Jalali
dmy(str) # "DD/MM/YYYY" Gregorian
parse_jalali(str)
parse_gregorian(str)
parse_date(str) # Auto detect calendar
```

---

### Formatting

```python
format_jalali_date(date, pattern: str, locale='fa'|'en') # Using strftime codes
format_gregorian_date(date, pattern: str, locale='fa'|'en')

# Or use directly on date objects:
jdate.strftime("%Y/%m/%d %H:%M:%S")
gdate.strftime("%Y-%m-%d %H:%M:%S")
```

**Examples:**
```python
jdate = JalaliDate(1402, 8, 18, 14, 45, 30)
jdate.strftime("%Y/%m/%d %H:%M:%S")           # '1402/08/18 14:45:30'
jdate.strftime("%A، %d %B %Y", locale="fa")   # 'سه‌شنبه، ۱۸ آبان ۱۴۰۲'
jdate.strftime("%Y-%m-%d")                    # '1402-08-18'
jdate.strftime("%I:%M %p")                    # '02:45 PM' or '۰۲:۴۵ ب.ظ'
```

---

### Operations

Arithmetic

```python
add_days(date, n)
add_months(date, n)
add_years(date, n)
add_weeks(date, n)
```

Comparison

```python
eq(a, b), ne(a, b), lt(a, b), le(a, b), gt(a, b), ge(a, b)
between(date, lower, upper)
min_date([dates]), max_date([dates])
```

Rounding

```python
floor_to_day(date), ceil_to_day(date)
floor_to_week(date), ceil_to_week(date)
floor_to_month(date), ceil_to_month(date)
floor_to_quarter(date), ceil_to_quarter(date)
floor_to_year(date), ceil_to_year(date)
floor_date(date, unit), ceiling_date(date, unit), round_date(date, unit)
```

Ranges

```python
date_range(start, end, step_days=1)
month_range(start, end)
year_range(start, end)
custom_range(start, end, days=0, months=0, years=0)
```

---

### Intervals

```python
class Period:
    # years, months, days, hours, minutes, seconds
    def __init__(years=0, months=0, days=0, hours=0, minutes=0, seconds=0)

class Duration:
    # days, hours, minutes, seconds
    def __init__(days=0, hours=0, minutes=0, seconds=0)
    days(), hours(), minutes(), seconds()

class Interval:
    # start, end
    def __init__(start, end)
    length() # returns Duration
    contains(date)
```

---

### Timezone

```python
get_timezone(name: str)
localize_datetime(dt, zone: str)
convert_timezone(dt, target_zone: str)
remove_timezone(dt)
is_dst(dt, zone: str)
utc_offset_minutes(zone: str)
list_timezones()
```

---

### DimDate Table (Analytics)

```python
generate_dim_date(
    start: str,
    end: str,
    calendar: 'jalali'|'gregorian' = 'jalali',
    include_fiscal: bool = False
) -> pandas.DataFrame
```

---

### Utilities

```python
days_in_month(year, month, calendar)
is_jalali_leap(year)
is_gregorian_leap(year)
validate_jalali(year, month, day)
validate_gregorian(year, month, day)
```

---

### Exceptions

All key functions and constructors raise ValueError or TypeError for invalid arguments.
Check docs for per-function details.

---

Maintainer: Ali Sadeghi Aghili (alisadeghiaghili@gmail.com)
