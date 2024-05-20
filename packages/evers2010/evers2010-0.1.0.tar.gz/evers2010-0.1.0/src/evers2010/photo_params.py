"""
Secondary parameters for photosynthesis
"""
import math

from .constants import gas_constant


def arrhenius(temp, v25, eact):
    """Typical temperature dependency formalism.

    References: eqS14

    Args:
        temp (float): [°C] object temperature
        v25 (float): [any]
        eact (float): [J.mol-1]

    Returns:
        (float): [same as v25]
    """
    t25 = 25 + 273.15
    tk = temp + 273.15

    return v25 * math.exp((1 / t25 - 1 / tk) * eact / gas_constant)


def _jmax_decr(jmax_s, jmax_deact, tk):
    return 1 + math.exp((jmax_s - jmax_deact / tk) / gas_constant)


def jmax(temp, jmax25, jmax_act, jmax_deact, jmax_s):
    """Maximum electron transport rate at saturating light levels.

    References: eqS17

    Notes: bug correction in original paper, use minus sign

    Args:
        temp (float): [°C] temperature
        jmax25 (float): [µmol e-.m-2 leaf.s-1] value of jmax at 25°C
        jmax_act (float): [J.mol-1] activation energy for jmax
        jmax_deact (float): [J.mol-1] deactivation energy
        jmax_s (float): [J.K-1.mol-1] entropy term

    Returns:
        (float): [µmol e-.m-2 leaf.s-1] Maximum electron transport rate (Jmax)
    """
    tk = temp + 273.15
    t25 = 25 + 273.15

    sca = _jmax_decr(jmax_s, jmax_deact, t25) / _jmax_decr(jmax_s, jmax_deact, tk)
    return jmax25 * math.exp((1 / t25 - 1 / tk) * jmax_act / gas_constant) * sca
