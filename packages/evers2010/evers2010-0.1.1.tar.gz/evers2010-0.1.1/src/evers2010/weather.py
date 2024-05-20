"""
Weather, physical atmosphere, related formalisms
"""
import math

from .constants import gas_constant


def vapour_sat(temp):
    """Saturated vapour pressure of the air.

    References: eqS23

    Args:
        temp (float): [°C] temperature of air

    Returns:
        (float): [kPa]
    """
    return 0.611 * math.exp(17.4 * temp / (239 + temp))


def vpd(temp, rh):
    """Vapour pressure difference in the air.

    References: eqS22 + eqS24

    Args:
        temp (float): [°C] temperature of air
        rh (float): [-] relative humidity of the air

    Returns:
        (float): [kPa]
    """
    return (1 - rh) * vapour_sat(temp)


def vpd_leaf(t_leaf, t_atm, rh):
    """leaf-to-air vapour pressure difference.

    References: eqS22 + eqS24

    Args:
        t_leaf (float): [°C] temperature of leaf
        t_atm (float): [°C] temperature of air
        rh (float): [-] relative humidity of the air

    Returns:
        (float): [kPa]
    """
    return vapour_sat(t_leaf) - rh * vapour_sat(t_atm)


def co2_partial_pressure(temp, co2_conc):
    """CO2 partial pressure of the air.

    References: eqS21

    Args:
        temp (float): [°C] temperature of air
        co2_conc (float): [µmol.mol-1] CO2 concentration in the air

    Returns:
        (float): [µbar]
    """
    return co2_conc * gas_constant * 1e-3 * (273.15 + temp) * 10 / 22.4136
