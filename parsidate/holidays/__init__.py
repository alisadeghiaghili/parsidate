"""Iranian official holiday data and HolidaySet container.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from parsidate.holidays.registry import (
    HolidayDataMissing,
    HolidaySet,
    DATA_VERSION,
)
from parsidate.holidays.ir import (
    iran_fixed_solar_holidays,
    holidays_in_year,
    is_holiday,
    iran_holidays,
)

__all__ = [
    "DATA_VERSION",
    "HolidayDataMissing",
    "HolidaySet",
    "iran_fixed_solar_holidays",
    "iran_holidays",
    "holidays_in_year",
    "is_holiday",
]
