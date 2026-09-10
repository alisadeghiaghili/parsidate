# Vectorized conversion

Requires: `pip install parsidate[vector]` (NumPy).

## API

```python
import numpy as np
from parsidate.vector import to_jalali_ymd, to_gregorian_ymd

gy = np.array([2024, 2023], dtype=np.int64)
gm = np.array([3, 11], dtype=np.int64)
gd = np.array([20, 9], dtype=np.int64)

jy, jm, jd = to_jalali_ymd(gy, gm, gd)
# jy[0] == 1403, jm[0] == 1, jd[0] == 1

gy2, gm2, gd2 = to_gregorian_ymd(jy, jm, jd)
```

Ordinals:

```python
from parsidate.vector import gregorian_ordinal, jalali_from_ordinal

ords = gregorian_ordinal(gy, gm, gd)
jy, jm, jd = jalali_from_ordinal(ords)
```

## Guarantees

- Results match `parsidate.core.converters` element-wise (parity tests).
- Inputs are cast to `int64`; shapes must match.
- Empty arrays are valid.

## Performance

Intended for 10⁵–10⁷ rows. Prefer this over Python loops in ETL / dim_date bulk loads.
