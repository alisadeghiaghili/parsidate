"""parsidate.vector: vectorized conversion helpers (requires numpy).

Copyright (C) 2024 Ali Sadeghi Aghili
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

try:
    import numpy as _np
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "parsidate.vector requires numpy. Install with: pip install parsidate[vector]"
    ) from exc

from parsidate.vector.convert import (
    gregorian_ordinal,
    jalali_from_ordinal,
    to_gregorian_ymd,
    to_jalali_ymd,
)

__all__ = [
    "to_jalali_ymd",
    "to_gregorian_ymd",
    "gregorian_ordinal",
    "jalali_from_ordinal",
]
