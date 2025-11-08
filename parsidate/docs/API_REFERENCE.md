# API_REFERENCE.md

## ParsiDate API Reference

---

### Core Classes

#### JalaliDate

class JalaliDate:
```
def init(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
year() # Get/set year
month() # Get/set month
day() # Get/set day
hour() # Get/set hour
minute() # Get/set minute
second() # Get/set second
microsecond() # Get/set microsecond
tzinfo() # Get/set time zone
format(fmt: str, locale='fa'|'en') -> str
copy() # Return a new copy
is_leap_year() # True if leap
weekday() # 0-6 (Monday=0)
quarter() # 1-4
day_of_year() # 1-366
add(**kwargs) # Arithmetic: years, months, days, hours, minutes, seconds
sub(**kwargs) # Negative arithmetic
to_gregorian() # Tuple (year, month, day)
str, repr, comparison ops
```

#### GregorianDate

Similar attributes and methods as JalaliDate.

---

### Converters

```
jalali_to_gregorian(year, month, day) -> (year, month, day)
gregorian_to_jalali(year, month, day) -> (year, month, day)
jalali_to_jdn(year, month, day) -> int (Julian Day Number)
gregorian_to_jdn(year, month, day) -> int
jdn_to_jalali(jdn) -> (year, month, day)
jdn_to_gregorian(jdn) -> (year, month, day)
```

---

### Parsers

```
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

```
format_jalali_date(date, locale='fa'|'en') # Standard fa/en
format_gregorian_date(date, locale='fa'|'en')
format_full(date, locale='fa'|'en')
format_short(date, locale='fa'|'en')
format_iso(date) # ISO 8601
format_date_custom(date, fmt: str, locale='fa'|'en')
```

---

### Operations

Arithmetic

```
add_days(date, n)
add_months(date, n)
add_years(date, n)
add_weeks(date, n)
```

Comparison

```
eq(a, b), ne(a, b), lt(a, b), le(a, b), gt(a, b), ge(a, b)
between(date, lower, upper)
min_date([dates]), max_date([dates])
```

Rounding

```
floor_to_day(date), ceil_to_day(date)
floor_to_week(date), ceil_to_week(date)
floor_to_month(date), ceil_to_month(date)
floor_to_quarter(date), ceil_to_quarter(date)
floor_to_year(date), ceil_to_year(date)
```

Ranges

```
date_range(start, end, step_days=1)
month_range(start, end)
year_range(start, end)
custom_range(start, end, days=0, months=0, years=0)
```

---

### Intervals

```
class Period:
# years, months, days, hours, minutes, seconds
def init(years=0, months=0, days=0, hours=0, minutes=0, seconds=0)

class Duration:
# days, hours, minutes, seconds
def init(days=0, hours=0, minutes=0, seconds=0)
days(), hours(), minutes(), seconds()

class Interval:
# start, end
def init(start, end)
length() # returns Duration
contains(date)
```

---

### Timezone

```
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

```
generate_dim_date(
start: str,
end: str,
calendar: 'jalali'|'gregorian' = 'jalali',
include_fiscal: bool = False
) -> pandas.DataFrame
```

---

### Utilities

```
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

