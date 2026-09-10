"""
parsidate.dimdate: Date dimension table generator for data warehousing.

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from .generator import (
    generate_dim_date,
    date_range,
    month_range,
    year_range,
    custom_range,
)

__all__ = [
    "generate_dim_date",
    "date_range",
    "month_range",
    "year_range",
    "custom_range",
]
