"""
Set of physical constants useful to compute weather/atmosphere related formalisms
"""

air_heat_capacity = 1006
"""[J kg-1 K-1] Isobaric heat capacity (Cp) of atmosphere.

References: https://www.engineeringtoolbox.com/air-specific-heat-capacity-d_705.html
"""

air_molar_mass = 28.9654
"""[g mol-1] Average molar mass of air.

References: https://en.wikipedia.org/wiki/Density_of_air
"""

gas_constant = 8.3144598
"""[J K-1 mol-1] Universal gas constant

References: scipy.constants.gas_constant
"""

gs_max = 1 / 70.0
"""[s-1 m] Theoretical maximal value for grass surface conductance

References: box 5 in Allen et al., 1998
"""

solar_cst = 1353.
"""[W m-2] mean amount of solar radiations received by earth above the atmosphere

References: https://www.pveducation.org/pvcdrom/properties-of-sunlight/solar-radiation-outside-the-earths-atmosphere
"""

standard_atmosphere = 101325
"""[Pa] Atmospheric pressure

References: scipy.constants.physical_constants['standard atmosphere']
"""

stephan_boltzmann = 5.670367e-08
"""[W m-2 K-4] Stefan-Boltzmann constant per surface area (σ).

References: scipy.constants.physical_constants['Stefan-Boltzmann constant']
"""

water_latent_heat_vaporization = 2264.705
"""[kJ kg-1] Latent heat of vaporization of water (λ).

References: https://en.wikipedia.org/wiki/Latent_heat
"""


def air_density(t_air, atm_pressure=standard_atmosphere):
    """Volumetric mass of dry atmosphere

    References: https://en.wikipedia.org/wiki/Density_of_air

    Args:
        t_air (float): [°C] air temperature
        atm_pressure (float): [Pa]

    Returns:
        (float): [kg m-3]
    """
    t = t_air + 273.15  # convert from [°C] to [K]
    spec_cte = gas_constant / air_molar_mass * 1e3  # [J kg-1 K-1] specific gaz constant for dry air
    return atm_pressure / (spec_cte * t)
