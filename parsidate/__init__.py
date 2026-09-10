"""
ParsiDate: Comprehensive Persian/Gregorian Date Toolkit for Python.
"""

__version__ = "0.10.0"
__author__ = "Ali Sadeghi Aghili"
__email__ = "alisadeghiaghili@gmail.com"
__license__ = "GPL-3.0-or-later"
__url__ = "https://github.com/alisadeghiaghili/parsidate"

from parsidate.core.jalali import JalaliDate
from parsidate.core.gregorian import GregorianDate
from parsidate.core.converters import to_jalali, to_gregorian
from parsidate.parsers.parse import (
    jmd, ymd, jmd_hms, ymd_hms,
    parse_jalali, parse_gregorian, parse_date,
    strptime_jalali, strptime_gregorian,
    now_jalali, now_gregorian, today_jalali, today_gregorian
)
from parsidate.utils.helpers import is_leap_year
from parsidate.intervals.duration import Duration, duration
from parsidate.intervals.period import Period, period
from parsidate.intervals.interval import Interval, interval
from parsidate.operations.comparison import (
    is_before, is_after, is_between, between
)
from parsidate.operations.rounding import floor_date, ceiling_date, round_date
from parsidate.operations.arithmetic import add_days, add_months, add_years

__all__ = [
    "JalaliDate", "GregorianDate",
    "to_jalali", "to_gregorian",
    "jmd", "ymd", "jmd_hms", "ymd_hms",
    "parse_jalali", "parse_gregorian", "parse_date",
    "strptime_jalali", "strptime_gregorian",
    "now_jalali", "now_gregorian", "today_jalali", "today_gregorian",
    "is_leap_year",
    "Duration", "duration",
    "Period", "period",
    "Interval", "interval",
    "is_before", "is_after", "is_between", "between",
    "floor_date", "ceiling_date", "round_date",
    "add_days", "add_months", "add_years",
]
