# ParsiDate: Persian & Gregorian Calendar Library for Python

[![PyPI version](https://badge.fury.io/py/parsidate.svg)](https://badge.fury.io/py/parsidate)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Complete date/time toolkit for Persian (Jalali/Solar Hijri) and Gregorian calendars.
Inspired by R's powerful [lubridate](https://lubridate.tidyverse.org) package.

---

## Features

- Jalali (Persian) and Gregorian date support
- Conversion between calendars
- Date parsing and formatting (full, short, ISO, custom, English/Farsi)
- Date arithmetic (add/subtract days, weeks, months, years, intervals)
- Comparison, min/max, rounding (floor/ceil to day, week, month, quarter, year)
- Timezone handling and conversion (support for pytz zones)
- Date ranges and sequence generators
- Complete test coverage
- Pandas integration for dimensional date tables (dimdate feature)

---

## Installation

```bash
pip install parsidate
```

---

## Quick Usage
```python
from parsidate.core import JalaliDate, GregorianDate
from parsidate.parsers import jmd, ymd
from parsidate.operations import add_days, diff_in_days
from parsidate.formatting import format_jalali_date

jdate = JalaliDate(1402, 8, 18, 14, 45)
gdate = GregorianDate(2024, 11, 9)

print(jdate.format("Y/m/d H:i"))
print(gdate.format("Y-m-d"))

date2 = jdate.add(days=5)
date3 = gdate.sub(months=2, days=7)

from parsidate.core.converters import jalali_to_gregorian
gy, gm, gd = jalali_to_gregorian(jdate.year(), jdate.month(), jdate.day())

from parsidate.timezone import convert_timezone
```

---

## Package Structure

- parsidate/
- core/
- parsing/
- formatting/
- operations/
- intervals/
- timezone/
- generator/
- dimdate/
- README.md
- LICENSE
- setup.py
- py.typed

---

## Documentation

- [Complete Usage Guide](/parsidate/docs/README_COMPLETE.md)
- [Test Modules](/parsidate/tests/)
- [API Reference](/parsidate/docs/API_REFERENCE.md)

---

## Key Modules

- **core:** Main date classes and converters
- **parsers:** Input string parsing for both calendars
- **formatting:** Standardized string output
- **operations:** Arithmetic, comparison, rounding
- **intervals:** Period, Duration, Interval handling
- **timezone:** Full timezone support (get, convert, DST, offset)
- **generator:** Sequence/range generators
- **dimdate:** Pandas dimension date generator for analytics

---

## Sample: DimDate Table

```python
from parsidate.dimdate import generate_dim_date

dim = generate_dim_date(start="1402/01/01", end="1402/01/07", calendar="jalali", include_fiscal=True)
print(dim.head())
```

---

## License

GNU General Public License v3.0 or later (GPL-3.0-or-later)

- Include author: Ali Sadeghi Aghili
- Reference repository: https://github.com/alisadeghiaghili/parsidate

---

## Testing

```bash
pytest tests/ -v --cov=parsidate
```


---

## Acknowledgments

Inspired by:

- [jalali](https://github.com/shobeiry/jalali)
- [lubridate](https://lubridate.tidyverse.org)

---

## Contribution

Pull requests welcome! See [CONTRIBUTING.md](/parsidate/docs/CONTRIBUTING.md)


