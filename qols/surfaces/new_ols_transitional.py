"""New OLS concept — OES Transitional Surface defaults.

Per ICAO New OLS concept:
- Slope: 20 % default, user-editable.
- Upper edge: 60 m above the elevation of the highest threshold.
- Width: derived from the OFS Approach inner edge.
"""
from typing import Dict

DEFAULT_SLOPE_PCT: float = 20.0
DEFAULT_CAP_HEIGHT_M: float = 60.0


def get_new_ols_transitional_defaults() -> Dict[str, float]:
    """Return New OLS OES Transitional Surface defaults.

    Returns:
        Dict with keys:

        * ``slope_pct``     — float (as %, e.g. 20.0 — divide by 100 in scripts)
        * ``cap_height_m``  — float (upper edge above highest THR, always 60 m)
    """
    return {
        'slope_pct': DEFAULT_SLOPE_PCT,
        'cap_height_m': DEFAULT_CAP_HEIGHT_M,
    }


__all__ = [
    'DEFAULT_SLOPE_PCT',
    'DEFAULT_CAP_HEIGHT_M',
    'get_new_ols_transitional_defaults',
]
