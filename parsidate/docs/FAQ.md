# FAQ.md

## Frequently Asked Questions — ParsiDate

---

### 1. What is ParsiDate?

ParsiDate is a Python toolkit for handling Persian (Jalali/Solar Hijri) and Gregorian calendar dates, featuring objects, converters, formatters, date arithmetic, intervals, timezone support, and analytics integration.

---

### 2. How do I install ParsiDate?

`pip install parsidate`

You need Python 3.8 or higher.

---

### 3. What are the main date classes?

- `JalaliDate`: Supports Persian (Jalali/Solar Hijri) calendar.
- `GregorianDate`: Standard Gregorian calendar.

---

### 4. How do I convert between Jalali and Gregorian dates?

Use the converters:

```
from parsidate.core.converters import jalali_to_gregorian, gregorian_to_jalali

gy, gm, gd = jalali_to_gregorian(1402, 8, 19)
jy, jm, jd = gregorian_to_jalali(2024, 11, 10)
```

---

### 5. How do I parse date strings?

ParsiDate provides several string parsers:

```
from parsidate.parsers import jmd, ymd, jdm, dmy, parse_date
jdate = jmd("1402/08/19")
gdate = ymd("2024-11-10")
```

`parse_date` auto-detects the calendar.

---

### 6. Does it support timezones?

Yes, ParsiDate fully supports timezone conversion and localization with pytz-compatible zones:

```
from parsidate.timezone import get_timezone, localize_datetime
tz = get_timezone("Asia/Tehran")
```

---

### 7. How can I generate a date range?

```
from parsidate.operations import date_range
for d in date_range(JalaliDate(1402,1,1), JalaliDate(1402,1,10)):
print(d)
```

---

### 8. Is ParsiDate compatible with pandas?

Yes. There's direct support for date dimension tables:

```
from parsidate.dimdate import generate_dim_date
df = generate_dim_date(start="1402/01/01", end="1402/01/10", calendar="jalali")
```

---

### 9. Is type checking supported?

Yes, ParsiDate includes a `py.typed` marker for PEP 561 compatibility.

---

### 10. How do I contribute or report bugs?

Read the [CONTRIBUTING.md](CONTRIBUTING.md).  
Report bugs or request features via GitHub issues, or email the maintainer.

---

### 11. What about Islamic Hijri or other calendars?

Currently, only Jalali and Gregorian calendars are supported.  
Support for other calendars may be planned for future versions.

---

### 12. Who maintains ParsiDate?

Ali Sadeghi Aghili (alisadeghiaghili@gmail.com)

---

### 13. License

GNU General Public License v3.0 or later.

---

For more details and advanced usage, refer to the [USAGE_GUIDE.md](USAGE_GUIDE.md), [README.md](README.md), and API docs.
