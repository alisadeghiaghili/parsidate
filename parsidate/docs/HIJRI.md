# Hijri (Qamari) — tabular basis

## What this is

`parsidate.core.hijri.HijriDate` uses the **tabular Islamic calendar**
(30-year arithmetic leap cycle). Typical accuracy **±1 day** versus
Umm al-Qura or state-published observational dates.

## What this is not

- Not Umm al-Qura official tables
- Not a global Islamic civil authority
- **Not** the source of Iranian official religious holidays — those are
  published Jalali dates in `parsidate.holidays`

## Usage

```python
from parsidate import HijriDate, JalaliDate

h = HijriDate(1446, 1, 10)  # Ashura (tabular)
h.to_gregorian()            # (Y, M, D)
h.to_jalali()
h.month_name("fa")          # محرم

HijriDate.from_jalali(JalaliDate(1403, 4, 26))
```

## Decision (R5)

Ship tabular `HijriDate` for civil I/O. Keep Iranian holidays on
published Jalali tables. Do not productize astronomical Hijri until a
concrete consumer requires Umm al-Qura tables.
