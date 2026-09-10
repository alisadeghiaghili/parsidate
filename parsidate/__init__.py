"""
ParsiDate: Comprehensive Persian/Gregorian Date Toolkit for Python.
"""

__version__ = "0.18.0"
__author__ = "Ali Sadeghi Aghili"
__email__ = "alisadeghiaghili@gmail.com"
__license__ = "Apache-2.0"
__url__ = "https://github.com/alisadeghiaghili/parsidate"

from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.core.hijri import HijriDate
from parsidate.core.converters import to_jalali, to_gregorian
from parsidate.parsers.parse import (
    jmd, ymd, jmd_hms, ymd_hms,
    parse_jalali, parse_gregorian, parse_date,
    strptime_jalali, strptime_gregorian,
    now_jalali, now_gregorian, today_jalali, today_gregorian
)
from parsidate.parsers.persian_text import parse_fa, parse_gregorian_fa
from parsidate.utils.helpers import is_leap_year
from parsidate.intervals.duration import Duration, duration
from parsidate.intervals.period import Period, period
from parsidate.intervals.interval import Interval, interval
from parsidate.operations.comparison import (
    is_before, is_after, is_between, between
)
from parsidate.operations.rounding import floor_date, ceiling_date, round_date
from parsidate.operations.arithmetic import add_days, add_months, add_years
from parsidate.operations.business import (
    is_business_day, networkdays, add_business_days,
    next_business_day, prev_business_day,
)
from parsidate.holidays import (
    HolidaySet, HolidayCalendar, holidays_in_year, is_holiday, iran_holidays,
)

__all__ = [
    "JalaliDate", "GregorianDate", "HijriDate",
    "to_jalali", "to_gregorian",
    "jmd", "ymd", "jmd_hms", "ymd_hms",
    "parse_jalali", "parse_gregorian", "parse_date",
    "strptime_jalali", "strptime_gregorian",
    "parse_fa", "parse_gregorian_fa",
    "now_jalali", "now_gregorian", "today_jalali", "today_gregorian",
    "is_leap_year",
    "Duration", "duration",
    "Period", "period",
    "Interval", "interval",
    "is_before", "is_after", "is_between", "between",
    "floor_date", "ceiling_date", "round_date",
    "add_days", "add_months", "add_years",
    "is_business_day", "networkdays", "add_business_days",
    "next_business_day", "prev_business_day",
    "HolidaySet", "HolidayCalendar", "holidays_in_year", "is_holiday", "iran_holidays",
]
