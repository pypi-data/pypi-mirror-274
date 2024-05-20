"""
Formalisms related to stomata opening
"""


def fvpd(vpd_leaf, a1, b1):
    """Effect of VPD on stomata aperture.

    References: eqS10, modified to force [0-1] range

    Args:
        vpd_leaf (float): [kPa] leaf-to-air vapour pressure difference
        a1 (float): [-] empirical factor
        b1 (float): [kPa-1] empirical factor

    Returns:
        (float): [-]
    """
    fac = a1 - b1 * vpd_leaf
    if fac <= 0:
        return 0

    if fac >= 0.5:
        return 1

    return 1 / (1 / fac - 1)


def gs_C02(an, rd, ci, ci_star, g0, fvpd):
    """stomatal conductance for CO2 diffusion.

    References: eqS3a plus forcing of g0 as min

    Args:
        an (float): [µmol CO2.m-2.s-1] net photosynthesis rate
        rd (float):[µmol CO2.m-2.s-1] mitochondrial respiration rate in the light
        ci (float): [µbar]  intercellular CO2 partial pressure
        ci_star (float): [µbar] intercellular CO2 compensation point
        g0 (float): [µmol CO2.m-2.s-1.µbar-1] residual stomatal conductance for CO2
                    at the light compensation point
        fvpd (float): [-] vapour pressure deficit effect on stomatal conductance

    Returns:
        (float): [µmol CO2.m-2.s-1.µbar-1]
    """
    if an + rd <= 0:
        return g0

    return g0 + (an + rd) / (ci - ci_star) * fvpd
