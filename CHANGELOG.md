# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.15.0] - 2024-11-09

### Added
- `parse_fa` / `parse_gregorian_fa` for Persian written dates
  (`۱۸ آبان ۱۴۰۳`, optional weekday prefix)
- `JalaliDate.isoformat` / `fromisoformat`, `timestamp` / `fromtimestamp`
- `GregorianDate.isoformat` / `fromisoformat`, `timestamp` / `fromtimestamp`
- `parsidate.interop`: `from_datetime`, `to_datetime_naive`,
  `to_jdatetime`, `from_jdatetime` (optional extra `jdatetime`)

## [0.14.0] - 2024-11-09

### Added
- `parsidate.vector`: NumPy array conversion
  - `to_jalali_ymd` / `to_gregorian_ymd`
  - `gregorian_ordinal` / `jalali_from_ordinal`
- Extra: `pip install parsidate[vector]` (numpy)

### Notes
- Scalar and vector converters must match exactly (parity tests).
- Optional import: core package does not require numpy.

## [0.13.0] - 2024-11-09

### Added
- `parsidate.holidays`: `HolidaySet`, official Iranian solar holidays,
  curated lunar holidays for 1402–1404, `holidays_in_year` / `is_holiday`
- `parsidate.operations.business`: `is_business_day`, `networkdays`,
  `add_business_days`, `next_business_day`, `prev_business_day`
- Default Jalali weekend = Friday; Gregorian = Sat/Sun
- `docs/BUSINESS_CALENDAR.md`

### Notes
- Lunar holiday rows are published official Jalali dates (not astronomical
  computation). Coverage years are documented in `holidays.ir`.
- `add_business_days` follows Excel `WORKDAY` stepping semantics.

## [Unreleased]

### Added
- `ROADMAP.md`: planned R1–R5 phases for post-0.12 versions (backlog only)

## [0.12.0] - 2024-11-09

### Added
- `tzdata` dependency on Windows so `zoneinfo` works without OS tzdata
- Hypothesis property tests for conversion round-trips (optional if hypothesis missing)
- Year-length and month-span consistency tests for 1300-1500

### Removed
- Internal scratch docs `FINAL_REPORT.txt` and `FINAL_SETUP_GUIDE.txt`

## [0.11.0] - 2024-11-09

### Changed
- Project license moved from GPL-3.0-or-later to **Apache-2.0**
- `Period` is immutable; `total_days()` replaced by explicit
  `fixed_days()` and `approx_days()` helpers
- `ATTRIBUTION.md` rewritten to match actual Apache-2.0 obligations
- Added `NOTICE` file

### Notes
- Conversion algorithms are published Solar Hijri arithmetic.
  Historical GPL implementations are acknowledged for provenance only.

## [0.10.0] - 2024-11-09

### Changed
- Timezone stack migrated from `pytz` to stdlib `zoneinfo` (Python 3.9+)
- Runtime dependencies removed (stdlib only for core; pandas optional for dimdate)
- `Duration` stores integer microseconds with total ordering and exact equality
- `intervals.arithmetic` is a thin re-export of `operations.arithmetic`

### Added
- GitHub Actions CI matrix (Python 3.9-3.13)
- P1 architecture regression tests

## [0.9.0] - 2024-11-09

### Fixed
- `JalaliDate` date subtraction now respects leap years and time-of-day
- `GregorianDate` is immutable; `add`/`sub`/`replace` return new instances
- `ceil_*` / `floor_*` no longer mutate the input `GregorianDate`
- `JalaliDate.__eq__` / `__hash__` agree (microseconds included)
- `generate_dim_date` `full_date` uses standard `strftime` codes (`%Y/%m/%d`)
- Packaging installs all subpackages (`setuptools.packages.find`)
- pytest `testpaths` points at `parsidate/tests`
- `is_dst` accepts aware datetimes

### Changed
- Version downgraded from claimed 1.0.0 to 0.9.0 (beta) until P1 hardening
- `requires-python` is `>=3.9` (was incorrectly advertised as 3.8)
- Development Status classifier set to Beta

### Added
- `strptime_jalali` / `strptime_gregorian` with standard `strptime` format codes
- `JalaliDate.to_ordinal()` for leap-safe day arithmetic
- P0 regression suite `test_p0_correctness.py`

## [1.0.0] - 2024-11-08

### Added
- Initial draft of ParsiDate (superseded by 0.9.0 correctness pass)
- Jalali (Persian/Solar Hijri) calendar support
- Gregorian calendar support
- Date parsing helpers
- Date arithmetic operations
- Duration, Period, and Interval classes
- Timezone helpers
- Dimension Date table generator
