"""
Comparison operations for JalaliDate and GregorianDate.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
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

def is_before(date1, date2) -> bool:
    """
    Check if date1 is before date2.

    Alias for lt(date1, date2).

    Args:
        date1: First date
        date2: Second date

    Returns:
        True if date1 < date2

    Example:
        is_before(jmd("1403/01/01"), jmd("1403/12/29"))  # True
    """
    return lt(date1, date2)


def is_after(date1, date2) -> bool:
    """
    Check if date1 is after date2.

    Alias for gt(date1, date2).

    Args:
        date1: First date
        date2: Second date

    Returns:
        True if date1 > date2

    Example:
        is_after(jmd("1403/12/29"), jmd("1403/01/01"))  # True
    """
    return gt(date1, date2)


def is_between(date, start, end, inclusive: bool = True) -> bool:
    """
    Check if date is between start and end.

    Alias for between(date, start, end, inclusive).

    Args:
        date: Date to check
        start: Start of range
        end: End of range
        inclusive: If True (default), includes boundaries

    Returns:
        True if date is in range

    Example:
        is_between(jmd("1403/06/15"), jmd("1403/01/01"), jmd("1403/12/29"))  # True
    """
    return between(date, start, end, inclusive)
