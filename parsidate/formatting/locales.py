"""
Locale data for Jalali (Persian) and Gregorian calendars.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

# Jalali (Persian) Months and Weekdays
PERSIAN_MONTH_NAMES_EN = [
    "Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad", "Shahrivar",
    "Mehr", "Aban", "Azar", "Dey", "Bahman", "Esfand"
]
PERSIAN_MONTH_NAMES_FA = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]
PERSIAN_MONTH_NAMES_SHORT_EN = [
    "Far", "Ord", "Kho", "Tir", "Mor", "Sha", "Meh", "Aba", "Aza", "Dey", "Bah", "Esf"
]
PERSIAN_MONTH_NAMES_SHORT_FA = [
    "فرو", "ارد", "خرد", "تیر", "مرد", "شهر", "مهر", "آبا", "آذر", "دی", "بهم", "اسف"
]

PERSIAN_WEEKDAY_NAMES_EN = [
    "Shanbe", "Yekshanbe", "Doshanbe", "Seshanbe", "Chaharshanbe", "Panjshanbe", "Jome"
]
PERSIAN_WEEKDAY_NAMES_FA = [
    "شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"
]
PERSIAN_WEEKDAY_NAMES_SHORT_EN = [
    "Sha", "Yek", "Do", "Se", "Cha", "Panj", "Jom"
]
PERSIAN_WEEKDAY_NAMES_SHORT_FA = [
    "ش", "ی", "د", "س", "چ", "پ", "ج"
]

# Gregorian Months and Weekdays
GREGORIAN_MONTH_NAMES_EN = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
GREGORIAN_MONTH_NAMES_FA = [
    "ژانویه", "فوریه", "مارس", "آوریل", "مه", "ژوئن",
    "جولای", "اوت", "سپتامبر", "اکتبر", "نوامبر", "دسامبر"
]
GREGORIAN_MONTH_NAMES_SHORT_EN = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
GREGORIAN_MONTH_NAMES_SHORT_FA = [
    "ژان", "فور", "مار", "آور", "مه", "ژوئ",
    "جول", "اوت", "سپت", "اکت", "نوا", "دسا"
]

GREGORIAN_WEEKDAY_NAMES_EN = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]
GREGORIAN_WEEKDAY_NAMES_FA = [
    "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"
]
GREGORIAN_WEEKDAY_NAMES_SHORT_EN = [
    "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
]
GREGORIAN_WEEKDAY_NAMES_SHORT_FA = [
    "دو", "سه", "چه", "پنج", "جم", "شن", "یک"
]

# Digits and Symbols
PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ENGLISH_DIGITS = "0123456789"
DATE_SEPARATORS = ["-", "/", ".", "_"]

# Locale registry (for future i18n extension)
LOCALES = {
    "fa": {
        "month_names": PERSIAN_MONTH_NAMES_FA,
        "month_names_short": PERSIAN_MONTH_NAMES_SHORT_FA,
        "weekday_names": PERSIAN_WEEKDAY_NAMES_FA,
        "weekday_names_short": PERSIAN_WEEKDAY_NAMES_SHORT_FA,
        "digits": PERSIAN_DIGITS,
    },
    "en": {
        "month_names": PERSIAN_MONTH_NAMES_EN,
        "month_names_short": PERSIAN_MONTH_NAMES_SHORT_EN,
        "weekday_names": PERSIAN_WEEKDAY_NAMES_EN,
        "weekday_names_short": PERSIAN_WEEKDAY_NAMES_SHORT_EN,
        "digits": ENGLISH_DIGITS,
    },
    "gregorian_en": {
        "month_names": GREGORIAN_MONTH_NAMES_EN,
        "month_names_short": GREGORIAN_MONTH_NAMES_SHORT_EN,
        "weekday_names": GREGORIAN_WEEKDAY_NAMES_EN,
        "weekday_names_short": GREGORIAN_WEEKDAY_NAMES_SHORT_EN,
        "digits": ENGLISH_DIGITS,
    },
    "gregorian_fa": {
        "month_names": GREGORIAN_MONTH_NAMES_FA,
        "month_names_short": GREGORIAN_MONTH_NAMES_SHORT_FA,
        "weekday_names": GREGORIAN_WEEKDAY_NAMES_FA,
        "weekday_names_short": GREGORIAN_WEEKDAY_NAMES_SHORT_FA,
        "digits": PERSIAN_DIGITS,
    },
}

def get_month_name(month: int, locale: str = "en", calendar: str = "jalali", short: bool = False) -> str:
    """Retrieve the month name for a given number, locale, and calendar system."""
    if not 1 <= month <= 12:
        raise ValueError(f"Month must be between 1 and 12, got {month}")
    key = f"{calendar}_{locale}" if calendar == "gregorian" else locale
    names = LOCALES[key]["month_names_short"] if short else LOCALES[key]["month_names"]
    return names[month - 1]

def get_weekday_name(weekday: int, locale: str = "en", calendar: str = "jalali", short: bool = False) -> str:
    """Retrieve the weekday name for a given number, locale, and calendar system."""
    if not 0 <= weekday <= 6:
        raise ValueError(f"Weekday must be between 0 and 6, got {weekday}")
    key = f"{calendar}_{locale}" if calendar == "gregorian" else locale
    names = LOCALES[key]["weekday_names_short"] if short else LOCALES[key]["weekday_names"]
    return names[weekday % 7]
