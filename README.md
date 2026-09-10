# ParsiDate: Persian & Gregorian Calendar Library for Python

[![PyPI version](https://badge.fury.io/py/parsidate.svg)](https://badge.fury.io/py/parsidate)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

**Date/time toolkit for Persian (Jalali/Solar Hijri) and Gregorian calendars.**
Inspired by R's [lubridate](https://lubridate.tidyverse.org) package.

Status: **0.11.0 (beta)** — Apache-2.0 license; architecture hardening.

---

## ✨ Features

- **Jalali (Persian) & Gregorian** date support
- **Conversion** between calendars
- **Date parsing & formatting** with **Python-standard `strftime` codes** ✅
- **Date arithmetic** (add/subtract days, weeks, months, years, intervals)
- **Comparison, min/max, rounding** (floor/ceil to day, week, month, quarter, year)
- **Timezone handling** & conversion (support for pytz zones)
- **Date ranges** & sequence generators
- **Complete test coverage** 
- **Pandas integration** for dimensional date tables (dimdate feature)

---

## 📦 Installation

```bash
pip install parsidate
```

---

## 🚀 Quick Start

```python
from parsidate.core import JalaliDate, GregorianDate
from parsidate.parsers import jmd, ymd

# Create dates
jdate = JalaliDate(1402, 8, 18, 14, 45)  # 1402/08/18 14:45
gdate = GregorianDate(2024, 11, 9)

# **Python-standard strftime formatting** ✅
print(jdate.strftime("%Y/%m/%d %H:%M"))           # 1402/08/18 14:45
print(jdate.strftime("%A، %d %B %Y", locale="fa")) # سه‌شنبه، ۱۸ آبان ۱۴۰۲
print(gdate.strftime("%Y-%m-%d"))                  # 2024-11-09

# Date arithmetic (returns new objects; inputs never mutate)
date2 = jdate.add(days=5)
days_diff = (jdate.add(months=1) - jdate).days()

# Parse strings
j = jmd("1402/08/19")  # Jalali YYYY/MM/DD
g = ymd("2024-11-09")  # Gregorian YYYY-MM-DD

# Standard strptime-style parsing
from parsidate.parsers import strptime_jalali, strptime_gregorian
j2 = strptime_jalali("18-08-1403", "%d-%m-%Y")
g2 = strptime_gregorian("2024-11-08", "%Y-%m-%d")
```

---

## 📝 Formatting (Python `strftime` Compatible) ✅

```python
jdate = JalaliDate(1402, 8, 18, 14, 45, 30)

# Common formats
print(jdate.strftime("%Y/%m/%d %H:%M:%S"))      # 1402/08/18 14:45:30
print(jdate.strftime("%Y-%m-%d"))               # 1402-08-18
print(jdate.strftime("%d/%m/%Y"))               # 18/08/1402

# Persian names
print(jdate.strftime("%A، %d %B %Y", locale="fa"))  # سه‌شنبه، ۱۸ آبان ۱۴۰۲

# 12-hour format
print(jdate.strftime("%I:%M %p", locale="fa"))  # ۰۲:۴۵ ب.ظ

# Backward compatible
print(jdate.format("%Y/%m/%d %H:%M"))           # Still works!
```

### Format Codes (Full `strftime` Support)
```
%Y - 4-digit year    %m - month (01-12)    %d - day (01-31)
%H - hour 24h        %I - hour 12h         %M - minute    %S - second
%p - AM/PM (ق.ظ/ب.ظ) %B - full month name %b - short month
%A - full weekday    %a - short weekday    %w - weekday number
%-m, %-d, %-H - no leading zero
```

---

## 🛠️ Package Structure

```
parsidate/
├── core/          # JalaliDate, GregorianDate, converters
├── parsers/       # jmd(), ymd(), parse_date()
├── formatting/    # strftime formatters
├── operations/    # add_days(), diff_in_days(), rounding
├── intervals/     # Period, Duration, Interval
├── timezone/      # get_timezone(), convert_timezone()
├── dimdate/       # generate_dim_date() for analytics
└── utils/         # helpers
```

---

## 📊 DimDate Table (Analytics)

```python
from parsidate.dimdate import generate_dim_date
import pandas as pd

df = generate_dim_date(
    start="1402/01/01", 
    end="1402/01/07", 
    calendar="jalali", 
    include_fiscal=True
)
print(df.head())
```

---

## 🧪 Testing

```bash
pytest
# or explicitly:
pytest parsidate/tests -v --cov=parsidate
```

Format strings use Python-standard `strftime` / `strptime` codes only
(`%Y`, `%m`, `%d`, `%H`, `%M`, `%S`, …). No custom date syntax.

---

## 📚 Documentation

- [Usage Guide](docs/USAGE_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md) 
- [Migration Guide](docs/MIGRATION_GUIDE.md) ← **New strftime format**
- [Changelog](CHANGELOG.md)

---

## ⚖️ License

**Apache License, Version 2.0**

```
Copyright 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
```

See [LICENSE](LICENSE) and [NOTICE](NOTICE).

---

## 🙌 Acknowledgments

Inspired by:
- [jalali](https://github.com/shobeiry/jalali) (GPL v3)
- [lubridate](https://lubridate.tidyverse.org) (R package)

---

## 🤝 Contribution

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m "Add amazing feature"`)
4. Push (`git push origin feature/amazing-feature`)
5. Open Pull Request

**See [CONTRIBUTING.md](docs/CONTRIBUTING.md)**

---

**👨‍💻 Author:** [Ali Sadeghi Aghili](mailto:alisadeghiaghili@gmail.com)  
**🌐 GitHub:** [alisadeghiaghili/parsidate](https://github.com/alisadeghiaghili/parsidate)

⭐ **Star this repo if it helps you!**
