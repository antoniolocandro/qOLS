"""New OLS concept — Approach Surface ICAO defaults.

Tables 4-1 (Non-instrument runways) and 4-2 (Instrument runways) keyed by
Aeroplane Design Group (ADG: I, IIA-IIB, IIC, III, IV, V) instead of the
current OLS classification + code scheme.

Inner edge lengths have width-conditional adjustments per ICAO footnotes.
``slope_pct`` is returned as a percentage (e.g. 3.33), NOT as a ratio, so the
UI can display it directly as an editable field — the geometry script divides
by 100 before use.
"""
from typing import Dict

# ---------------------------------------------------------------------------
# ADG group constants
# ---------------------------------------------------------------------------
ADG_I = "I"
ADG_IIA_IIB = "IIA-IIB"
ADG_IIC = "IIC"
ADG_III = "III"
ADG_IV = "IV"
ADG_V = "V"

ADG_GROUPS = [ADG_I, ADG_IIA_IIB, ADG_IIC, ADG_III, ADG_IV, ADG_V]

RWY_NON_INSTRUMENT = "Non-instrument"
RWY_INSTRUMENT = "Instrument"

RWY_TYPES = [RWY_NON_INSTRUMENT, RWY_INSTRUMENT]

# ---------------------------------------------------------------------------
# Table 4-1  Non-instrument runways
# ---------------------------------------------------------------------------
_DIST_THR_NI: Dict[str, float] = {
    ADG_I:       30.0,
    ADG_IIA_IIB: 60.0,
    ADG_IIC:     60.0,
    ADG_III:     60.0,
    ADG_IV:      60.0,
    ADG_V:       60.0,
}

_INNER_EDGE_BASE_NI: Dict[str, float] = {
    ADG_I:        60.0,
    ADG_IIA_IIB:  80.0,
    ADG_IIC:     100.0,
    ADG_III:     125.0,
    ADG_IV:      135.0,
    ADG_V:       150.0,
}

_LENGTH_NI: Dict[str, float] = {
    ADG_I:       1600.0,
    ADG_IIA_IIB: 2500.0,
    ADG_IIC:     2500.0,
    ADG_III:     2500.0,
    ADG_IV:      2500.0,
    ADG_V:       2500.0,
}

_SLOPE_PCT_NI: Dict[str, float] = {
    ADG_I:       5.0,
    ADG_IIA_IIB: 4.0,
    ADG_IIC:     3.33,
    ADG_III:     3.33,
    ADG_IV:      3.33,
    ADG_V:       3.33,
}

# ---------------------------------------------------------------------------
# Table 4-2  Instrument runways
# ---------------------------------------------------------------------------
_DIST_THR_I: Dict[str, float] = {
    ADG_I:       60.0,
    ADG_IIA_IIB: 60.0,
    ADG_IIC:     60.0,
    ADG_III:     60.0,
    ADG_IV:      60.0,
    ADG_V:       60.0,
}

_INNER_EDGE_BASE_I: Dict[str, float] = {
    ADG_I:       110.0,
    ADG_IIA_IIB: 125.0,
    ADG_IIC:     155.0,
    ADG_III:     175.0,
    ADG_IV:      185.0,
    ADG_V:       200.0,
}

_LENGTH_I: Dict[str, float] = {
    ADG_I:       4500.0,
    ADG_IIA_IIB: 4500.0,
    ADG_IIC:     4500.0,
    ADG_III:     4500.0,
    ADG_IV:      4500.0,
    ADG_V:       4500.0,
}

_SLOPE_PCT_I: Dict[str, float] = {
    ADG_I:       3.33,
    ADG_IIA_IIB: 3.33,
    ADG_IIC:     3.33,
    ADG_III:     3.33,
    ADG_IV:      3.33,
    ADG_V:       3.33,
}

# Divergence is 10 % for all groups and both runway types
_DIVERGENCE_PCT = 10.0


# ---------------------------------------------------------------------------
# Width-based inner edge footnote adjustments
# ---------------------------------------------------------------------------

def get_inner_edge_adjusted(adg: str, rwy_type: str, runway_width_m: float) -> float:
    """Return the inner edge length after applying ICAO width-based footnote adjustments.

    Args:
        adg: Aeroplane Design Group string (e.g. ``"I"``, ``"IIA-IIB"``).
        rwy_type: ``RWY_NON_INSTRUMENT`` or ``RWY_INSTRUMENT``.
        runway_width_m: Runway pavement width in metres.

    Returns:
        Adjusted inner edge length in metres.
    """
    w = float(runway_width_m)
    if rwy_type == RWY_NON_INSTRUMENT:
        base = _INNER_EDGE_BASE_NI.get(adg, 125.0)
        if adg == ADG_I:
            if w > 30.0:
                return 100.0
            if w > 23.0:
                return 80.0
        elif adg == ADG_IIA_IIB:
            if w > 45.0:
                return 110.0
            if w > 30.0:
                return 100.0
        elif adg == ADG_IIC:
            if w > 45.0:
                return 110.0
        return base
    else:  # RWY_INSTRUMENT
        base = _INNER_EDGE_BASE_I.get(adg, 175.0)
        if adg == ADG_I:
            if w > 30.0:
                return 125.0
        elif adg == ADG_IIA_IIB:
            if w > 30.0 and w <= 45.0:
                return 140.0
        elif adg == ADG_IIC:
            if w <= 30.0:
                return 140.0
        return base


def get_new_ols_approach_defaults(
    rwy_type: str,
    adg: str,
    runway_width_m: float,
) -> Dict[str, float]:
    """Return New OLS Approach Surface defaults for the given ADG group and runway type.

    Args:
        rwy_type: ``"Non-instrument"`` or ``"Instrument"``.
        adg: Aeroplane Design Group (``"I"``, ``"IIA-IIB"``, ``"IIC"``,
             ``"III"``, ``"IV"``, ``"V"``).
        runway_width_m: Runway width in metres — used for inner edge footnote adjustments.

    Returns:
        Dict with keys:

        * ``distance_from_threshold_m`` — float
        * ``inner_edge_m``              — float (footnote-adjusted)
        * ``divergence_pct``            — float (always 10.0)
        * ``length_m``                  — float
        * ``slope_pct``                 — float (as %, e.g. 3.33 — divide by 100 in scripts)
    """
    if rwy_type == RWY_NON_INSTRUMENT:
        dist = _DIST_THR_NI.get(adg, 60.0)
        length = _LENGTH_NI.get(adg, 2500.0)
        slope = _SLOPE_PCT_NI.get(adg, 3.33)
    else:
        dist = _DIST_THR_I.get(adg, 60.0)
        length = _LENGTH_I.get(adg, 4500.0)
        slope = _SLOPE_PCT_I.get(adg, 3.33)

    inner_edge = get_inner_edge_adjusted(adg, rwy_type, runway_width_m)

    return {
        'distance_from_threshold_m': dist,
        'inner_edge_m': inner_edge,
        'divergence_pct': _DIVERGENCE_PCT,
        'length_m': length,
        'slope_pct': slope,
    }


__all__ = [
    'ADG_I', 'ADG_IIA_IIB', 'ADG_IIC', 'ADG_III', 'ADG_IV', 'ADG_V',
    'ADG_GROUPS',
    'RWY_NON_INSTRUMENT', 'RWY_INSTRUMENT', 'RWY_TYPES',
    'get_inner_edge_adjusted',
    'get_new_ols_approach_defaults',
]
