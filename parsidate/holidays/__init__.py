"""Iranian official holiday data and calendar containers.

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
from parsidate.holidays.calendar import HolidayCalendar

__all__ = [
    "DATA_VERSION",
    "HolidayDataMissing",
    "HolidaySet",
    "HolidayCalendar",
    "iran_fixed_solar_holidays",
    "iran_holidays",
    "holidays_in_year",
    "is_holiday",
]
