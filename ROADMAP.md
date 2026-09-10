# ParsiDate Roadmap

**Status:** R1 (business calendar) shipped in **0.13.0**. R2–R5 remain planned.

**Positioning:** analytics-ready Persian (Solar Hijri) calendar toolkit for
data warehouses, pipelines, and Industry 4.0 reporting — not another thin
`jdatetime` clone.

**Current version:** 0.13.0 (beta)  
**Target stable:** 1.0.0 after R2–R4 land and soak

---

## Principles

1. TDD: red tests first, then implementation.
2. Standard `strftime` / `strptime` codes only for formats.
3. Immutable date types; pure functions for operations.
4. Optional heavy deps (`pandas`, `numpy`) behind extras.
5. Docstrings: Args, Returns, Raises, Examples, full type hints.
6. One human-week-sized PR per release slice; merge only when green.
7. No AI co-authorship or synthetic commit metadata.

---

## Non-goals (until after 1.0)

- Full Hijri *lunar* calendar productization (tracked as R5 research).
- Recurrence rules (RRULE) / cron calendars.
- UI components.
- Replacing `pandas` / `dateutil` as general datetime stack.

---

## Gap summary (why these phases)

| User need | Today | Phase |
|-----------|--------|-------|
| Iranian official holidays | missing | R1 |
| Fri/Thu business days, `networkdays` | missing | R1 |
| Vectorized Jalali↔Gregorian | per-row Python only | R2 |
| Persian written dates (`۱۸ آبان ۱۴۰۳`) | missing | R3 |
| ISO / timestamp / JSON interop | partial | R3 |
| `jdatetime` / `datetime.date` bridges | missing | R3 |
| `dim_date` warehouse-grade (SCD, fiscal IR) | basic | R4 |
| Hijri (Qamari) holidays | missing | R5 |

---

## R1 — Iranian business calendar  
**Version:** 0.13.0 · **Size:** ~1 week · **Priority:** P0 product

### Scope
New package `parsidate.calendar_ir` (or `parsidate.holidays`):

```text
parsidate/
  holidays/
    __init__.py
    dataset.py      # loaded official holidays (JSON/CSV resource)
    api.py          # is_holiday, holidays_in_year, next_holiday
  operations/
    business.py     # networkdays, add_business_days, is_business_day
```

### Public API (draft)
```python
from parsidate.holidays import holidays_in_year, is_holiday
from parsidate.operations.business import (
    is_business_day, networkdays, add_business_days, next_business_day,
)

holidays_in_year(1403) -> list[JalaliDate]
is_holiday(jmd("1403/01/01")) -> bool
is_business_day(d, weekend=(4, 5))  # Thu=4, Fri=5 in Jalali weekday
networkdays(start, end, holidays=None) -> int
add_business_days(date, n, holidays=None) -> JalaliDate
```

### Data policy
- Ship a **versioned** official holiday table for a declared year range
  (e.g. 1390–1410) as package data.
- Document source and update procedure in `docs/HOLIDAYS.md`.
- Do **not** invent dates; if a year is unknown, raise `HolidayDataMissing`.
- Lunar-dependent holidays: store the **published official Jalali date**
  for each year (Iran announces them); do not compute astronomy in R1.

### Acceptance
- [ ] `holidays_in_year(1403)` matches official Nowruz / Islamic holidays list
- [ ] `networkdays` equals manual count on sample invoices
- [ ] Default weekend = Thursday+Friday for Jalali weekday numbering
- [ ] Gregorian dates supported with Sat+Sun default
- [ ] Tests: dataset integrity, boundary days, empty custom holiday list
- [ ] Docs + changelog

### Risks
Holiday table drift; mitigate with explicit `DATA_VERSION` and year coverage test.

---

## R2 — Vectorized conversion  
**Version:** 0.14.0 · **Size:** ~1 week · **Priority:** P0 for DW/pipelines

### Scope
```text
parsidate/vector/
  __init__.py
  convert.py   # numpy-first; pandas optional thin wrapper
```

### API (draft)
```python
import numpy as np
from parsidate.vector import to_jalali_ymd, to_gregorian_ymd

gy, gm, gd = to_gregorian_ymd(jy_array, jm_array, jd_array)
jy, jm, jd = to_jalali_ymd(gy_array, gm_array, gd_array)
```

Implementation notes:
- Pure NumPy integer ops (same algorithm as scalar converters, no Python loops).
- Optional: `pandas.Series.dt` accessor `jdt` via entry point later (R4).
- Memory: three int32/int64 arrays in, three out; no object dtype.

### Acceptance
- [ ] 1M random dates convert in < 1s on typical laptop (order-of-magnitude)
- [ ] Matches scalar `gregorian_to_jalali` exactly on dense sample
- [ ] Works with `dtype=int32` and `int64`
- [ ] No hard pandas import in `parsidate.vector`
- [ ] Extra: `parsidate[vector]` installs numpy

### Risks
Algorithm must be rewritten branch-free or carefully vectorized leap logic.

---

## R3 — Input/output interop  
**Version:** 0.15.0 · **Size:** ~1 week · **Priority:** P1

### Scope
1. **Persian written dates**
   ```python
   parse_fa("۱۸ آبان ۱۴۰۳") -> JalaliDate
   parse_fa("شنبه ۱۸ آبان ۱۴۰۳") -> JalaliDate  # weekday check optional warn
   ```
2. **ISO / timestamps**
   ```python
   JalaliDate.fromisoformat("1403-08-18T14:30:25")
   jdate.isoformat() / isoformat(timespec=...)
   JalaliDate.fromtimestamp(ts, tz=...)
   jdate.timestamp() -> float
   ```
3. **Bridges**
   ```python
   JalaliDate.from_datetime(dt) -> JalaliDate
   jdate.to_datetime_naive() -> datetime  # Gregorian wall clock
   from_jdatetime(jd) / to_jdatetime()    # optional extra
   ```

### Acceptance
- [ ] Round-trip isoformat ↔ parse
- [ ] Persian digits + month names (fa/en)
- [ ] Rejected garbage raises `ValueError` with format hint
- [ ] Bridges tested against `datetime` and optional `jdatetime` extra

---

## R4 — Warehouse-grade `dim_date`  
**Version:** 0.16.0 · **Size:** ~1 week · **Priority:** P1

### Scope
Extend `generate_dim_date`:

| Column group | Additions |
|--------------|-----------|
| Business | `is_business_day`, `is_holiday`, `holiday_name` |
| Iranian fiscal | configurable FY start (default Farvardin) |
| SCD | `date_key`, `valid_from`, `valid_to` optional |
| ISO | `iso_year`, `iso_week`, `iso_weekday` |
| Periods | `month_start`, `month_end`, `ytd_flag`, `mtd_flag` |

- Use R1 holidays when provided.
- Vectorized via R2 when range > N rows (e.g. 10k).

### Acceptance
- [ ] Dim for full Jalali year has 365/366 rows, unique `date_key`
- [ ] `is_business_day` consistent with R1
- [ ] Documented column dictionary in `docs/DIM_DATE.md`
- [ ] Golden CSV for 1403 in tests

---

## R5 — Hijri (Qamari) research spike  
**Version:** 0.17.0 research / 0.18 implementation · **Size:** spike then build

### Spike questions
1. Umm al-Qura vs Iranian official announcements for religious days?
2. Is full Hijri calendar required, or only **fixed Jalali mappings** for
   Iranian religious holidays already in R1?
3. License/citation for any algorithm (public domain astronomical vs tables).

### Likely outcome
Prefer **published Jalali dates for Iranian holidays** (R1) over full lunar
calendar. Full `HijriDate` only if a concrete user demands civil Hijri I/O.

### Acceptance (if implemented)
- [ ] Documented calendar basis
- [ ] Conversion tests against published tables for sample years
- [ ] Clear non-goal: not a global Islamic civil calendar authority

---

## Release train

| Version | Content | Exit criteria |
|---------|---------|---------------|
| 0.12.0 | baseline | done |
| 0.13.0 | R1 holidays + business days | **shipped** |
| 0.14.0 | R2 vector | perf test + parity |
| 0.15.0 | R3 interop | iso + fa parse |
| 0.16.0 | R4 dim_date v2 | column dict + golden |
| 0.17.0 | R5 spike notes | decision recorded |
| **1.0.0** | API freeze | 0.13–0.16 soaked ≥ 2 weeks, no P0 |

Each release = one PR, tests green, CHANGELOG, version bump, branch deleted after merge.

---

## Testing strategy

1. Keep dense conversion suite (1900–2100).
2. Keep hypothesis property tests.
3. R1: dataset checksum + golden holiday lists per year.
4. R2: parity with scalar; micro-benchmark job (not flaky CI gate).
5. Interop: round-trip matrix.
6. Never lower coverage on `core/`.

---

## Suggested execution order (do not implement until scheduled)

Start **R1 only** when work on 0.13 begins. Highest user value; unblocks R4.
Do not start R2/R3 in parallel on `main` — serialize PRs.

Definition of done for the R1 PR (when started):
- `holidays` package + `operations/business.py`
- tests red→green
- docs + CHANGELOG 0.13.0
- PR merged, branch deleted

**This document is the backlog.** New features must land in a numbered
release with tests and changelog — not as drive-by commits on `main`.
