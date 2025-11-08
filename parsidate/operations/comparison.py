"""
Comparison operations for JalaliDate and GregorianDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under GPL-3.0-or-later
"""

def eq(date1, date2) -> bool:
    """Check if two dates are equal."""
    return date1 == date2

def ne(date1, date2) -> bool:
    """Check if two dates are NOT equal."""
    return date1 != date2

def lt(date1, date2) -> bool:
    """Check if date1 is less than date2."""
    return date1 < date2

def le(date1, date2) -> bool:
    """Check if date1 is less than or equal to date2."""
    return date1 <= date2

def gt(date1, date2) -> bool:
    """Check if date1 is greater than date2."""
    return date1 > date2

def ge(date1, date2) -> bool:
    """Check if date1 is greater than or equal to date2."""
    return date1 >= date2

def between(dt, start, end, inclusive: bool = True) -> bool:
    """
    Check whether dt is in [start, end] (inclusive) or (start, end) (exclusive).

    Args:
        dt: The date to check.
        start: Start date.
        end: End date.
        inclusive: If True (default) uses <= and >=, if False uses < and >.

    Returns:
        Boolean.
    """
    if inclusive:
        return start <= dt <= end
    else:
        return start < dt < end

def min_date(*args):
    """
    Return the minimum (earliest) date from args.

    Args:
        *args: Any number of date objects.

    Returns:
        The earliest date.
    """
    return min(args)

def max_date(*args):
    """
    Return the maximum (latest) date from args.

    Args:
        *args: Any number of date objects.

    Returns:
        The latest date.
    """
    return max(args)
