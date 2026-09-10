# Business calendar (Iran)

Version: 0.13.0+

## Concepts

| Concept | Jalali default | Gregorian default |
|---------|----------------|-------------------|
| Weekend weekdays | Friday (`6` in Sat=0 numbering) | Saturday + Sunday (`5,6` in Mon=0) |
| Official holidays | Bundled Iranian solar + curated lunar years | none unless you pass `holidays=` |

## Holidays

```python
from parsidate.core.jalali import JalaliDate
from parsidate.holidays import iran_holidays, holidays_in_year, is_holiday, HolidaySet

hs = iran_holidays(1403)          # HolidaySet
holidays_in_year(1403)            # list[JalaliDate]
is_holiday(JalaliDate(1403, 1, 1))  # True (Nowruz)

company = HolidaySet(dates=[JalaliDate(1403, 8, 18)])
```

### Data policy

- **Fixed solar** holidays always available (Nowruz 1–4 Farvardin, 12/13 Farvardin,
  15 Khordad, 22 Bahman, 29 Esfand).
- **Lunar** holidays are **published official Jalali dates**, not computed from
  astronomy. Coverage: `1402–1404` in this release (`DATA_VERSION` in
  `parsidate.holidays.registry`).
- Missing lunar year → solar holidays still work; extend `LUNAR_HOLIDAYS` for more years.

## Business-day algebra

```python
from parsidate.operations import (
    is_business_day, networkdays, add_business_days,
    next_business_day, prev_business_day,
)
from parsidate.core.jalali import JalaliDate

start = JalaliDate(1403, 1, 5)
end = JalaliDate(1403, 1, 15)
networkdays(start, end)                 # excludes Fridays + official holidays
add_business_days(start, 3)             # Excel WORKDAY-like stepping
is_business_day(start, weekend=(5, 6))  # treat Thu+Fri as weekend
```

### Semantics

- `networkdays`: inclusive of `start` and (by default) `end` when they are business days.
- `add_business_days(date, n)`: steps `n` business days; does **not** pre-roll a
  non-business start (same idea as Excel `WORKDAY`).
- Gregorian dates: weekend Sat/Sun; holidays only if you pass them.

## Warehouse

When generating `dim_date`, pass holiday dates into `holidays=` so
`is_holiday` reflects the official calendar rather than a bare weekday flag.
