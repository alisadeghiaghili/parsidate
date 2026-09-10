# Custom holidays (company / personal days)

## HolidayCalendar

Layer **official Iranian holidays** with **your own** closure days:

```python
from parsidate import JalaliDate, HolidayCalendar
from parsidate.dimdate import generate_dim_date

cal = (
    HolidayCalendar.ir(years=[1403, 1404])
    .add_holidays(
        ["1403/08/18", JalaliDate(1403, 8, 19)],
        label="company",
    )
    .add_holidays(["۱۴۰۳/۰۹/۰۱"], label="plant-shutdown")  # Persian digits OK
)

cal.is_holiday(JalaliDate(1403, 8, 18))       # True
cal.holiday_name(JalaliDate(1403, 8, 18))     # "company"
cal.is_business_day(JalaliDate(1403, 8, 18))  # False
cal.networkdays(JalaliDate(1403, 8, 15), JalaliDate(1403, 8, 25))
cal.add_business_days(JalaliDate(1403, 8, 15), 3)

# persist
payload = cal.to_payload()
back = HolidayCalendar.from_payload(payload)
```

## Pure custom (no official layer)

```python
cal = HolidayCalendar(holidays=["1403/08/18"])  # only these days
# or
from parsidate import HolidaySet
cal = HolidayCalendar(holidays=HolidaySet.from_strings(["1403/08/18"]))
```

## Weekend override

```python
# Thursday + Friday weekend
cal = HolidayCalendar.ir(years=[1403], weekend=(5, 6))
```

## dim_date

```python
dim = generate_dim_date("1403/01/01", "1403/01/15", holidays=cal)
# uses cal.weekend, cal.holidays, and holiday_name labels
```

## Notes

- Custom days **add** to the official set when you start from `HolidayCalendar.ir()`
- Business-day math skips both official and custom holidays
- Immutable: `add_holidays` returns a new calendar
