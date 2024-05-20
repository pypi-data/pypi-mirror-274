"""
Actual photosynthesis formalisms
"""
import math

from . import stomata
from .constants import standard_atmosphere
from .photo_params import arrhenius, jmax
from .weather import co2_partial_pressure, vpd_leaf


def electron_transport_rate(ppfd, jmax, k2ll, convexity):
    """Rate of electron transport (J).

    References: eqS16

    Args:
        ppfd (float): [µmol photon.m-2.s-1] PAR
        jmax (float): [µmol e-.m-2.s-1] maximum electron transport rate at
                      saturating light levels
        k2ll (float): [mol e-.mol-1 photons] conversion efficiency of incident
                      PAR into electron transport at limiting light levels
        convexity (float): [-] convexity factor

    Returns:
        (float): [µmol e-.m-2.s-1] electron transport rate (J)
    """
    fac = k2ll * ppfd + jmax

    num = fac - math.sqrt(fac ** 2 - 4 * convexity * jmax * k2ll * ppfd)
    return num / (2 * convexity)


def photo_net(t_leaf, ppfd, t_atm, rh):
    """Net photosynthesis rate.

    Args:
        t_leaf (float): [°C] temperature of leaf
        ppfd (float): [?]
        t_atm (float): [°C] temperature of atmosphere
        rh (float): [-] relative humidity in the atmosphere

    Returns:
        (float): [µmol CO2.m-2.s-1]
    """
    oxygen = 210  # [mbar] oxygen partial pressure of the air
    co2 = 440  # [ppm] or [µbar.bar-1] CO2 concentration in atmosphere
    # g0 = 0.012  # [mol.m-2.s-1] TODO problem with unit [µmol CO2.m-2.s-1.µbar-1]
    g0 = 0.01  # [mol.m-2.s-1.bar-1] eq [µmol CO2.m-2.s-1.µbar-1] residual stomatal conductance for CO2 at the light compensation point from yin2009 fig6
    # gm = 0.15  # [mol.m-2.s-1] TODO problem with unit
    gm = 0.4  # [mol.m-2.s-1.bar-1] eq [µmol CO2.m-2.s-1.µbar-1] mesophyll conductance for CO2 diffusion from yin2009 fig6
    a1 = 0.84  # [-] Zhu 2018, table S1
    a1 = 0.9  # [-] yin2009 fig6
    b1 = 0.14  # [kPa-1] Zhu 2018, table S1
    b1 = 0.15  # [kPa-1] yin2009 fig6

    k2ll = 0.2  # [mol e-.mol-1 photons] Zhu 2018, table S1 with unit correction
    k2ll = 0.33 * 0.75  # [mol e-.mol-1 photons] Yin2009 table2
    convexity = 0.87  # [-] Zhu 2018, table S1
    convexity = 0.7  # [-] Zhu 2018, table S1

    jmax25 = 80 * 1.5  # [µmol e-.m-2 leaf.s-1] gs_sim
    jmax_act = 63500  # [J.mol-1] Zhu 2018, table S1
    jmax_deact = 202900  # [J.mol-1] Zhu 2018, table S1
    jmax_s = 650  # [J.K-1.mol-1] Zhu 2018, table S1

    vcmax_25 = 80  # [µmol m-2.s-1] from gs_sim  # TODO all form gs_sim can be computed from zhu by estimating N
    vcmax_act = 87700  # [J.mol-1] Zhu 2018, table S1

    kmc_25 = 27.238 * 1e6 / standard_atmosphere  # [Pa] to [µbar] Zhu 2018, table S1
    kmc_act = 80990  # [J.mol-1]

    kmo_25 = 16.582 * 1e3 / standard_atmosphere  # [Pa] to [mbar] Zhu 2018, table S1
    kmo_act = 23720  # [J.mol-1]

    rd_25 = 0.649  # [µmol m-2.s-1] from gs_sim
    rd_act = 46390  # [J.mol-1] Zhu 2018, table S1

    sco_25 = 2.8  # [mbar.µbar-1] from [kPa.Pa-1] Zhu 2018, table S1
    sco_act = -24460  # [J.mol-1]

    kmc = arrhenius(t_leaf, kmc_25, kmc_act)  # needed [µbar]
    print("kmc", kmc)
    kmo = arrhenius(t_leaf, kmo_25, kmo_act)  # needed [mbar]
    print("kmmo", kmo)
    sco = arrhenius(t_leaf, sco_25, sco_act)  # needed [mbar.µbar-1]
    print("sco", sco)

    # rtb = 2.357 / 1.6  # [mol CO2.m-2.s-1] TODO pb with unit  # [m2.s.µbar.µmol-1]  combined turbulence and boundary layer resistance for CO2
    # print("gb", 1 / rtb)
    gb = 1.5  # [mol.m-2.s-1.bar-1] from yin2009 fig6
    print("gb", gb)
    rtb = 1 / gb

    fvpd = stomata.fvpd(vpd_leaf(t_leaf, t_atm, rh), a1, b1)  # [-]
    print("vpd_leaf", vpd_leaf(t_leaf, t_atm, rh))
    vcmax = arrhenius(t_leaf, vcmax_25, vcmax_act)  # needed [µmol CO2.m-2.s-1]
    vcmax = 120  # [µmol CO2.m-2.s-1]  Yin2009 fig6
    print("vcmax", vcmax)
    rd = arrhenius(t_leaf, rd_25, rd_act)  # needed [µmol CO2.m-2.s-1]
    rd = 0.01 * vcmax  # [µmol CO2.m-2.s-1]  Yin2009 fig6
    rd = 0
    print("rd", rd)
    ca = co2_partial_pressure(t_atm, co2)  # [µbar]
    ca = 360  # [µbar]  Yin2009 fig6
    print("ca", ca)

    jmax_val = jmax(t_leaf, jmax25, jmax_act, jmax_deact, jmax_s)
    jmax_val = 230  # [µmol CO2.m-2.s-1]  Yin2009 fig6
    print("jmax", jmax_val)
    j_maj = electron_transport_rate(ppfd, jmax_val, k2ll, convexity)  # [µmol e-.m-2.s-1]

    gamma_star = 0.5 * oxygen / sco  # eqS12 needed [µbar]

    # x1 [µmol CO2.m-2.s-1] eqS15a
    # x2 [µbar] eqS15b
    ans = []
    for x1, x2 in [(vcmax, kmc * (1 + oxygen / kmo)),  # rubisco limited
                   (j_maj / 4, 2 * gamma_star)]:  # e- transport limited
        a = g0 * (x2 + gamma_star) + (g0 / gm + fvpd) * (x1 - rd)  # eqS6a
        b = ca * (x1 - rd) - gamma_star * x1 - rd * x2  # eqS6b
        c = ca + x2 + (1 / gm + rtb) * (x1 - rd)  # eqS6c with (rtb = rt + rb)
        d = x2 + gamma_star + (x1 - rd) / gm  # eqS6d
        e = 1 / gm + (g0 / gm + fvpd) * (1 / gm + rtb)  # eqS6e with (rtb = rt + rb)

        p = -(d + (x1 - rd) / gm + a * (1 / gm + rtb) + (g0 / gm + fvpd) * c) / e  # eqS5a with (rtb = rt + rb)
        q = (d * (x1 - rd) + a * c + (g0 / gm + fvpd) * b) / e  # eqS5b
        r = - a * b / e  # eqS5c

        q_maj = (p ** 2 - 3 * q) / 9  # eqS8a
        r_maj = (2 * p ** 3 - 9 * p * q + 27 * r) / 54  # eqS8c
        try:
            theta = math.acos(r_maj / math.sqrt(q_maj ** 3))  # eqS8b

            an = -2 * math.sqrt(q_maj) * math.cos(theta / 3 + 4 * math.pi / 3) - p / 3  # eqS7
            ans.append(an)
        except ValueError:
            raise  # TODO temporary??

    ci = ca - min(ans) * (1 / (g0 * 10) + 1 / gb)
    cc = ci - min(ans) / gm

    print("res", 1 / g0, 1 / gb, 1 / gm)
    print("ci", ci)
    print("cc", cc)
    return min(ans)  # from eqS15
