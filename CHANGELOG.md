# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
