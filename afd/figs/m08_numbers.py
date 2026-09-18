"""Module 8 numbers: shocks, the Rankine-Hugoniot conditions, and the
Sedov-Taylor blast wave, checked against Taylor's own Trinity table and
against a shock measured in situ by Voyager 2.

Every physical number quoted in module08.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

THE SHAPE OF THE CHECK, following Modules 2 and 3.  From ONE published
source, one exact prediction is CONFIRMED and one assumption is REFUTED.

THE ANCHOR IS TRINITY, and the reason is the reason Module 2 preferred
Venzmer & Bothmer.  Taylor's table was not built by anyone solving the
blast-wave equations.  It is 25 radii read off photographic film with a
length scale marked on it, against 25 shutter times read off the same film.
Nothing about the Sedov solution went into producing the numbers, so the
numbers can test it.  The solar-model circularity of Module 3 does not
arise here.  From that single table:

  CONFIRMED  R ~ t^(2/5).  The exponent 2/5 is fixed before any data is
             touched: it is forced by dimensional analysis on (E, rho_0, t)
             alone, and it is the only exponent those three can make.  A
             least-squares fit of log R on log t returns 0.4058 +/- 0.0076
             over all 25 rows, 0.3904 +/- 0.0024 over the 24 rows from
             0.24 ms (Taylor's own range), and 0.3989 +/- 0.0049 over rows
             2-20 (0.24-4.61 ms).  All three are within 2.4 per cent of
             0.400.

  REFUTED    The point-explosion, uniform-atmosphere, ideal-gas-with-
             gamma-1.4 model that produced that exponent.  The residuals
             of Taylor's fixed-slope line are not noise.  In (5/2) log10 R
             the 0.10 ms row sits 0.30 low; the band means then fall
             +0.0150 (0.24-1.93 ms) -> -0.0043 (3.26-4.61 ms) -> -0.0339
             (15-62 ms), a step of 0.049 that is 7.3 times the combined
             standard error of the two outer band means.  The three fits
             above disagree with each other inside their formal errors
             for the same reason.  The energy makes the
             same point with a number: the blast-wave energy recovered from
             the table is 17.3 kt, against the Department of Energy's 21 kt
             and Selby et al.'s 24.8 +/- 2 kt.  The Sedov solution assumes
             all of E is in the gas; the fireball radiated a large share of
             the yield before the hydrodynamic phase began.

A SECOND CHECK, ASTROPHYSICAL, from Richardson et al. (2008).  Voyager 2
crossed the solar-wind termination shock in 2007 and measured a shock with
its own plasma instrument.  The same paper compares it with Neptune's bow
shock measured by the same instrument on the same spacecraft.

  CONFIRMED  At Neptune's bow shock the density rises by a factor of four
             and the speed falls by a factor of four.  Four is (gamma+1)/
             (gamma-1) for gamma = 5/3, the strong-shock ceiling, and it is
             a pure number fixed by gamma alone.
  REFUTED    At the termination shock the single-fluid ideal-gas closure
             fails.  The authors state it in their own words: "If all the
             flow energy were transferred to the thermal ions as happens at
             planetary bow shocks, the heliosheath temperature would be
             10^6 K, whereas the observed temperature is 10^5 K."  A factor
             of ten, and the missing energy went to pickup ions.

A NOTE ON WHAT IS AND IS NOT CIRCULAR IN THE VOYAGER NUMBERS.  Table 1 of
Richardson et al. gives a compression ratio of 2.38 +/- 0.14 for crossing
TS-2 and a solar-wind fast-mode Mach number of 4.9 +/- 0.1.  Those two
numbers come from the SAME Rankine-Hugoniot minimisation, so comparing them
with each other tests the fit, not nature.  They are reported below and
used only to show how far a magnetised collisionless shock departs from the
gas-dynamic formula.  The two numbers that are NOT circular are the
measured temperatures, 10^5 K observed against 10^6 K predicted, and the
Fig. 5 comparison with Neptune's bow shock, which is a direct read of two
time series.

Sources for every published number compared against are listed in the
SOURCES block at the foot of this file and in module08.html.
"""
import math
import os
import numpy as np
from scipy.integrate import solve_ivp

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m01_numbers.py, m02_numbers.py and m03_numbers.py
# rather than imported, so that each module's numbers script reads on its own.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
mp = 1.67262192369e-24  # g
me = 9.1093837015e-28   # g
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
a_rad = 7.565733e-15    # erg cm^-3 K^-4 (radiation constant, 4 sigma_SB/c)
pc = 3.0856775814913673e18   # cm
kpc = 1e3*pc
AU = 1.495978707e13     # cm
yr = 3.15576e7          # s
Msun = 1.3271244e26/G   # g              (IAU 2015 nominal GM / CODATA G)

# Earth, for the terrestrial half of the module.
g_earth = 980.665       # cm/s^2         (standard gravity, definitional)
mu_air = 28.9647        # dimensionless  (mean molecular weight of dry air)

GAM_MONO = 5.0/3.0      # monatomic ideal gas: ionised hydrogen, helium
GAM_DIAT = 7.0/5.0      # diatomic ideal gas at room temperature: air

# --- Trinity, from Taylor (1950) -----------------------------------------
# All of these are READ FROM THE PAPER.  See the header of the data file for
# how the PDF was obtained and how the optical character recognition of the
# 1950 letterpress digits was cross-checked.
TAYLOR_INTERCEPT = 11.915    # his eq. (1): (5/2)log10 R - log10 t, R in cm
TAYLOR_R5T2 = 6.67e23        # his eq. (3), cm^5 s^-2
TAYLOR_RHO0 = 1.25e-3        # g/cm^3, the ambient density he assumed
TAYLOR_K14 = 0.856           # his Table 3, K for gamma = 1.40
TAYLOR_I1_14 = 0.185         # his Table 3, I_1 for gamma = 1.40
TAYLOR_I2_14 = 0.187         # his Table 3, I_2 for gamma = 1.40
TAYLOR_E14 = 7.14e20         # his Table 3, erg, for gamma = 1.40
TAYLOR_TONS14 = 16800.0      # his Table 3, tons of T.N.T., for gamma = 1.40
TAYLOR_ERG_PER_TON = 4.25e16 # his own conversion: 1000 cal/g on the long ton
TAYLOR_TONS167 = 9500.0      # his Table 3, tons of T.N.T., for gamma = 1.667
TAYLOR_ALT_TONS = 23700.0    # his abstract: the alternative, gamma near 1.3

KT_ERG = 4.184e19            # erg per kiloton, the MODERN convention
DOE_YIELD_KT = 21.0          # Department of Energy released value
SELBY_YIELD_KT = 24.8        # Selby et al. (2021)
SELBY_YIELD_ERR = 2.0

# --- published values of the Sedov constant, for verification ------------
# xi_0 is defined by  R(t) = xi_0 (E t^2 / rho_0)^(1/5).
# gamma = 7/5: Kamm & Timmes (2007) set the spherical, uniform-density,
#   gamma = 1.4 standard problem with rho_0 = 1 g/cm^3 and E = 0.851072 erg
#   so that the shock sits at r = 1.0 cm at t = 1.0 s.  That statement IS
#   the constant: xi_0 = 1/E^(1/5) = 0.851072^(-1/5).
KT07_EBLAST_SPH_G14 = 0.851072
# gamma = 5/3: Tang & Chevalier (2017) write R = (xi E t^2/rho)^(1/5) and
#   state xi = 2.026 for gamma = 5/3 in a uniform medium, citing Taylor
#   (1946), Sedov (1959) and Book (1994).  So xi_0 = 2.026^(1/5).
TC17_XI_G53 = 2.026

# --- Voyager 2 at the termination shock, Richardson et al. (2008) --------
V2_TS2_COMPRESSION = 2.38
V2_TS2_COMPRESSION_ERR = 0.14
V2_TS2_MACH_FAST_UP = 4.9
V2_TS2_MACH_FAST_UP_ERR = 0.1
V2_TS2_MACH_FAST_DOWN = 1.1
V2_TS2_MACH_FAST_DOWN_ERR = 0.1
V2_TS3_COMPRESSION = 1.58
V2_TS3_COMPRESSION_ERR = 0.71
V2_TS3_MACH_FAST_UP = 8.8
V2_TS3_MACH_FAST_UP_ERR = 1.2
V2_TS2_SHOCKSPEED = 94.0        # km/s, outward motion of the shock
V2_TS2_SHOCKSPEED_ERR = 3.4
V2_TS2_THETA_BN = 82.8          # degrees between shock normal and B
V2_TS_T_OBSERVED = 1.0e5        # K, heliosheath proton temperature
V2_TS_T_PREDICTED = 1.0e6       # K, if all flow energy went to thermal ions
V2_NEPTUNE_DENSITY_JUMP = 4.0   # their Fig. 5 caption, direct read
V2_NEPTUNE_SPEED_DROP = 4.0     # their Fig. 5 caption, direct read
V2_NEPTUNE_TEMP_JUMP = 100.0    # their Fig. 5 caption, direct read
V2_TS_TEMP_JUMP = 10.0          # their Fig. 5 caption, direct read
V2_TS_DENSITY_JUMP = 2.0        # their Fig. 5 caption, direct read

# --- the radiative transition, Cioffi, McKee & Bertschinger (1988) -------
# Their equations (3.33a) and (3.33b), for a metallicity factor zeta_m = 1:
CMB88_R_PDS_PC = 14.0           # pc, x E51^(2/7) n0^(-3/7)
CMB88_V_PDS_KMS = 413.0         # km/s, x n0^(1/7) E51^(1/14)
# Their eq. (3.10) gives the shell-formation time and their eq. (3.11) sets
# t_PDS = t_sf/e.  That is an independent route to the same t_PDS.
CMB88_T_SF_YR = 3.61e4          # yr, x E51^(3/14) n0^(-4/7) zeta_m^(-5/14)

# --- Tycho, and the Rayleigh-Taylor debt left by Module 7 -----------------
# Module 7 section 10 says its Rayleigh-Taylor half has no astronomical check.
# This is the check.  Every number here was read from the PDF text of the
# paper named, extracted locally; see .ignore/m08-source-verification.md.
#
# Warren et al. (2005), ApJ 634, 376 = astro-ph/0507478.  Abstract: the
# azimuthally averaged radii are BW 251", CD 241", RS 183", and "taking
# account of projection effects, we find ratios of 1 : 0.93 : 0.70".
W05_BW_ARCSEC = 251.0
W05_CD_ARCSEC = 241.0
W05_RS_ARCSEC = 183.0
W05_CD_OVER_BW = 0.93        # deprojected
W05_RS_OVER_BW = 0.70        # deprojected
W05_CD_OVER_BW_2SIG = 0.94   # their 2-sigma threshold radius, projected
W05_CD_OVER_BW_4SIG = 0.98   # their 4-sigma threshold radius, projected
W05_WC01_CD_1D = 0.77        # Warren's section 7, reading Wang & Chevalier's
#                              Figure 1.  NOT a number printed by W&C.
# Wang & Chevalier (2001), ApJ 549, 1119 = astro-ph/0005105, their own text:
# "at t' = 1.6, the region occupied by the unstable ejecta does not extend
# beyond 85% of the remnant radius"; at t' = 1.7 the forward shock has
# expansion parameter m = 0.47 and sits at 3.09 pc with the reverse shock at
# 2.08 pc.
WC01_FINGER_TIPS = 0.85
WC01_M_FORWARD = 0.47
# Katsuda et al. (2010), ApJ 709, 1387 = arXiv:1001.2484: the forward-shock
# expansion index varies from 0.26 to 0.65 with azimuth; the mean is 0.52.
K10_M_MEAN = 0.52
K10_M_MIN = 0.26
K10_M_MAX = 0.65
# Shimony et al. (2022), the laboratory measurement Module 7 verified.  It is
# the BUBBLE coefficient.  No source in this folder gives alpha for spikes,
# so no number for spikes is printed anywhere in this module.
SHIMONY_ALPHA_B = 0.038
SHIMONY_ALPHA_B_ERR = 0.008
SHIMONY_ALPHA_THEORY_3D = 0.05  # "a value of ~0.05 for 3D immiscible fluids"

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'data', 'taylor1950_trinity.dat')


# =========================================================================
# PART A.  The Rankine-Hugoniot conditions
# =========================================================================

def rh_from_fluxes(rho1, v1, p1, rho2, v2, p2, gamma):
    """Residuals of the three conservation forms across a discontinuity.

    Module 2 wrote the fluid equations as conservation laws.  In a frame in
    which the discontinuity is at rest and the flow is normal to it, a
    steady one-dimensional flow makes each flux DIVERGENCE vanish, so each
    flux itself is the same on the two sides:

        mass       rho v
        momentum   rho v^2 + p
        energy     rho v (v^2/2 + h),   h = gamma p/((gamma-1) rho)

    Nothing has been assumed about what happens inside the discontinuity.
    That is the whole content of the Rankine-Hugoniot conditions: they are
    the Module 2 conservation laws integrated across a layer whose interior
    is not modelled.  Returns the three fractional residuals.
    """
    def h(p, rho):
        return gamma*p/((gamma - 1.0)*rho)
    f1a, f1b = rho1*v1, rho2*v2
    f2a, f2b = rho1*v1*v1 + p1, rho2*v2*v2 + p2
    f3a = rho1*v1*(0.5*v1*v1 + h(p1, rho1))
    f3b = rho2*v2*(0.5*v2*v2 + h(p2, rho2))
    return ((f1b - f1a)/f1a, (f2b - f2a)/f2a, (f3b - f3a)/f3a)


def rh_jumps(M1, gamma):
    """The three jump ratios across a normal shock of upstream Mach M1.

    Solving the three flux equalities for the downstream state gives, for
    an ideal gas of constant gamma,

        rho2/rho1 = v1/v2 = (gamma+1) M1^2 / ((gamma-1) M1^2 + 2)
        p2/p1     = (2 gamma M1^2 - (gamma-1)) / (gamma+1)
        T2/T1     = (p2/p1)(rho1/rho2)

    Returns (density ratio, pressure ratio, temperature ratio).
    """
    M2 = M1*M1
    r = (gamma + 1.0)*M2/((gamma - 1.0)*M2 + 2.0)
    pr = (2.0*gamma*M2 - (gamma - 1.0))/(gamma + 1.0)
    return r, pr, pr/r


def rh_downstream_mach(M1, gamma):
    """Mach number behind the shock.  Always less than 1 for M1 > 1."""
    M2 = M1*M1
    num = (gamma - 1.0)*M2 + 2.0
    den = 2.0*gamma*M2 - (gamma - 1.0)
    return np.sqrt(num/den)


def entropy_jump(M1, gamma):
    """Entropy change per particle across the shock, in units of k.

    s = c_v ln(p rho^-gamma) with c_v = k/(gamma-1) per particle, so

        Delta s / k = (1/(gamma-1)) ln[ (p2/p1) (rho1/rho2)^gamma ].

    This is the quantity that forbids rarefaction shocks.  It is positive
    for M1 > 1 and negative for M1 < 1, and the second law admits only the
    first.  A "rarefaction shock" is not ruled out by the conservation laws
    at all: it satisfies every one of them.  It is ruled out here.

    Below M1 = sqrt((gamma-1)/(2 gamma)) the formula for p2/p1 goes
    NEGATIVE, so the logarithm is undefined and the function returns nan.
    That threshold is 0.447 for gamma = 5/3 and 0.378 for gamma = 7/5.  A
    "shock" that weak in the rarefaction direction is not merely forbidden
    by the second law; it does not exist as a solution of the jump
    conditions at all.
    """
    r, pr, _ = rh_jumps(M1, gamma)
    return np.log(pr*r**(-gamma))/(gamma - 1.0)


def strong_shock_density(gamma):
    """The ceiling on compression, (gamma+1)/(gamma-1).

    Let M1 -> infinity in rh_jumps: the density ratio saturates.  No
    hydrodynamic shock in an ideal gas of this gamma can compress by more.
    4 for gamma = 5/3, 6 for gamma = 7/5.
    """
    return (gamma + 1.0)/(gamma - 1.0)


def strong_shock_temperature(v_shock, mu, gamma=GAM_MONO):
    """Post-shock temperature of a strong shock, in K.

    In the strong-shock limit p2 = 2 rho1 v_s^2/(gamma+1) and
    rho2 = rho1 (gamma+1)/(gamma-1), so

        T2 = (mu m_u / k) p2/rho2
           = 2(gamma-1)/(gamma+1)^2  mu m_u v_s^2 / k.

    For gamma = 5/3 the prefactor is 2(2/3)/(64/9) = 3/16, which is the
    familiar T2 = 3 mu m_u v_s^2/(16 k).  mu MUST be stated: 0.6 for an
    ionised cosmic-abundance gas, 1.0 for neutral atomic hydrogen, and the
    answer differs by a factor 1.7 between them.
    """
    pref = 2.0*(gamma - 1.0)/(gamma + 1.0)**2
    return pref*mu*mu_u*v_shock*v_shock/kB


def isothermal_shock_compression(M_iso):
    """Compression across an ISOTHERMAL shock: rho2/rho1 = M^2.

    If the gas radiates fast enough to hold T fixed across the layer, the
    energy flux equation is replaced by T2 = T1.  Mass and momentum alone
    then give rho1 v1 = rho2 v2 and rho1 v1^2 + rho1 c_T^2 =
    rho2 v2^2 + rho2 c_T^2, whose non-trivial root is rho2/rho1 = M^2 with
    M = v1/c_T.  There is NO ceiling.  This is why molecular clouds, which
    cool efficiently, form dense filaments that an adiabatic shock could
    never make: the factor 4 becomes a factor M^2.
    """
    return M_iso*M_iso


# =========================================================================
# PART B.  The Sedov-Taylor similarity solution
# =========================================================================
#
# Write  lambda = r/R(t)  with  R ~ t^(2/5), and
#
#     v(r,t) = (r/t) u(lambda)
#     rho(r,t) = rho_0 g(lambda)
#     p(r,t) = rho_0 (r/t)^2 h(lambda)
#
# Substituting into the spherical Euler equations of Module 2 and using
# d lambda/dt = -(2/5) lambda/t, d lambda/dr = lambda/r turns the three
# partial differential equations into three ordinary ones in ln lambda.
# Writing ' for d/d(ln lambda) and a = u - 2/5:
#
#     continuity  a g'/g + 3u + u' = 0
#     momentum    a u' + u^2 - u + (h/g)(2 + h'/h) = 0
#     entropy     a (h'/h - gamma g'/g) + 2(u - 1) = 0
#
# Eliminating g'/g and h'/h from the momentum equation gives u' explicitly.
# The derivation is set out in module08.html; the algebra is reproduced in
# sedov_rhs below so that the code and the prose cannot drift apart.

def sedov_rhs(s, y, gamma):
    """Right-hand side of the similarity system, in the variable s = ln lambda.

    State vector is (u, ln g, ln h).  Logarithms are integrated because g
    falls to zero and h rises without bound at the centre; both do so as
    pure powers of lambda, so their logarithms are linear in s and the
    integration stays well conditioned all the way in.
    """
    u, lg, lh = y
    w = np.exp(lh - lg)             # h/g = p/(rho (r/t)^2) = c^2/(gamma (r/t)^2)
    a = u - 0.4
    den = a*a - gamma*w             # vanishes only at a sonic point
    du = (a*(-u*u + u - 2.0*w) + w*((3.0*gamma + 2.0)*u - 2.0))/den
    dlg = -(3.0*u + du)/a
    dlh = gamma*dlg - 2.0*(u - 1.0)/a
    return [du, dlg, dlh]


def sedov_profile(gamma, s_min=-7.0, n_sample=200001):
    """Integrate the similarity system inward from the shock.

    The boundary values at lambda = 1 are the STRONG-SHOCK Rankine-Hugoniot
    conditions of PART A, evaluated with the shock speed D = dR/dt =
    (2/5) R/t that the similarity form itself supplies:

        rho2 = rho_0 (gamma+1)/(gamma-1)   ->  g(1) = (gamma+1)/(gamma-1)
        v2   = 2D/(gamma+1)                ->  u(1) = 4/(5(gamma+1))
        p2   = 2 rho_0 D^2/(gamma+1)       ->  h(1) = 8/(25(gamma+1))

    So PART B is not a new physical input.  It is PART A plus similarity.
    Returns (lambda, u, g, h) sampled from the shock inward.

    The integration stops at lambda = exp(s_min) = 9.1e-4 rather than at
    the centre, and the reason is not laziness.  As lambda -> 0 the system
    has the fixed point u = (2/5)/gamma with du/d(ln lambda) = -3(u - u*),
    so a perturbation grows as lambda^-3 going inward: the physical
    solution is the unstable one and rounding error overwhelms it below
    about lambda = 1e-4.  Nothing is lost.  The energy integrand carries a
    factor lambda^5, so everything inside lambda = 1e-3 contributes less
    than 1e-15 of the total, and xi_0 is unchanged in its eighth digit
    whether the integration stops at lambda = 6.7e-3 or at 3.4e-4.
    """
    u1 = 4.0/(5.0*(gamma + 1.0))
    g1 = (gamma + 1.0)/(gamma - 1.0)
    h1 = 8.0/(25.0*(gamma + 1.0))
    sol = solve_ivp(sedov_rhs, [0.0, s_min], [u1, np.log(g1), np.log(h1)],
                    args=(gamma,), rtol=1e-12, atol=1e-14,
                    dense_output=True, max_step=0.01)
    s = np.linspace(0.0, s_min, n_sample)
    u, lg, lh = sol.sol(s)
    return np.exp(s), u, np.exp(lg), np.exp(lh)


def sedov_xi0(gamma):
    """The Sedov constant xi_0 in R = xi_0 (E t^2/rho_0)^(1/5).

    The total energy inside the shock is

        E = int_0^R [rho v^2/2 + p/(gamma-1)] 4 pi r^2 dr
          = 4 pi rho_0 (R^5/t^2) J,
        J = int_0^1 lambda^4 [g u^2/2 + h/(gamma-1)] d lambda.

    But R^5/t^2 = xi_0^5 E/rho_0 by the definition of xi_0, so the E on
    both sides cancels and 1 = 4 pi xi_0^5 J.  The energy integral does not
    determine the energy; it determines the CONSTANT.  Returns
    (xi_0, J, K) with K = 1/xi_0^5 = 4 pi J, which is Taylor's K.
    """
    lam, u, g, h = sedov_profile(gamma)
    s = np.log(lam)
    integrand = lam**5*(g*u*u/2.0 + h/(gamma - 1.0))
    J = -np.trapezoid(integrand, s)      # s runs from 0 downward
    xi0 = (4.0*np.pi*J)**-0.2
    return xi0, J, 4.0*np.pi*J


def sedov_ode_residual(gamma, lam_test=(0.9, 0.7, 0.5, 0.3, 0.1)):
    """Check that the integrated profile satisfies the three ODEs.

    Differentiates the SAMPLED solution numerically and substitutes it back
    into the continuity and entropy equations, which sedov_rhs uses only
    after the algebra that eliminated them.  A small residual means the
    algebra is right, not merely that the integrator converged.
    """
    lam, u, g, h = sedov_profile(gamma)
    s = np.log(lam)
    du = np.gradient(u, s)
    dlg = np.gradient(np.log(g), s)
    dlh = np.gradient(np.log(h), s)
    a = u - 0.4
    r_cont = a*dlg + 3.0*u + du
    r_ent = a*(dlh - gamma*dlg) + 2.0*(u - 1.0)
    out = []
    for lt in lam_test:
        i = int(np.argmin(abs(lam - lt)))
        out.append((lam[i], r_cont[i], r_ent[i]))
    return out


def sedov_radius(E, rho0, t, xi0):
    """R(t) = xi_0 (E t^2/rho_0)^(1/5), in cm."""
    return xi0*(E*t*t/rho0)**0.2


def sedov_shockspeed(E, rho0, t, xi0):
    """dR/dt = (2/5) R/t, in cm/s."""
    return 0.4*sedov_radius(E, rho0, t, xi0)/t


def sedov_energy_from_Rt(R, t, rho0, xi0):
    """E = rho_0 R^5/(xi_0^5 t^2), the inversion Taylor performed."""
    return rho0*R**5/(xi0**5*t*t)


# =========================================================================
# PART C.  Reading Taylor's Trinity table
# =========================================================================

def load_trinity(path=DATA):
    """Read Taylor (1950) Table 1.  Returns t in seconds, R in cm, authority."""
    t, R, auth = [], [], []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            if line.lstrip().startswith('#'):
                continue
            parts = line.split()
            if len(parts) != 3:
                continue
            t.append(float(parts[0])*1e-3)
            R.append(float(parts[1])*100.0)
            auth.append(parts[2])
    return np.array(t), np.array(R), np.array(auth)


def fit_powerlaw(t, R):
    """Least squares of log10 R on log10 t.  Returns (slope, err, intercept).

    The formal error is the ordinary least-squares standard error on the
    slope, computed from the residual variance.  It assumes independent,
    identically distributed errors.  It is quoted below, and then it is
    immediately said to be an underestimate, because the residuals of this
    particular fit are plainly structured rather than random.
    """
    x, y = np.log10(t), np.log10(R)
    n = len(x)
    A = np.vstack([x, np.ones(n)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    s2 = (resid @ resid)/(n - 2)
    cov = s2*np.linalg.inv(A.T @ A)
    return coef[0], np.sqrt(cov[0, 0]), coef[1]


def taylor_intercept(t, R):
    """Taylor's own statistic: n = (5/2) log10 R - log10 t, R in cm, t in s.

    He fixed the slope at 1 in the (log t, (5/2) log R) plane and read the
    intercept off the 45-degree line.  This function returns the value for
    each row, so the scatter and the STRUCTURE of the scatter can both be
    seen.
    """
    return 2.5*np.log10(R) - np.log10(t)


# =========================================================================
# PART D.  The radiative transition
# =========================================================================

def cooling_function(T):
    """Radiative cooling coefficient Lambda(T), erg cm^3 s^-1.

    Two branches, both stated rather than fitted here:

      T > 1e7 K     Lambda = 2.1e-27 sqrt(T), thermal bremsstrahlung from a
                    fully ionised cosmic-abundance plasma.  This is the
                    standard free-free coefficient.
      1e4 < T <= 1e7  Lambda = Lambda_7 (T/1e7)^(-0.7), the usual power-law
                    representation of collisionally excited line cooling,
                    normalised by Lambda_7 = 2.1e-27 sqrt(1e7) so the two
                    branches join continuously at 1e7 K.

    The second branch matters and must not be omitted.  Bremsstrahlung
    alone underestimates the cooling rate by a factor of 25 at 1e5 K, which
    would move the radiative transition of a supernova remnant by more than
    an order of magnitude in time.  Lambda is defined here per unit
    n_e n_H, the usual convention.
    """
    L7 = 2.1e-27*np.sqrt(1e7)
    T = np.asarray(T, dtype=float)
    return np.where(T > 1e7, 2.1e-27*np.sqrt(T), L7*(T/1e7)**-0.7)


def cooling_time(T, nH, mu=0.61, xe=1.2):
    """Cooling time of post-shock gas, in seconds.

    t_cool = (3/2) n_tot k T / (n_e n_H Lambda(T)),
    with n_tot = rho/(mu m_u) the TOTAL particle density (ions plus
    electrons), n_e = xe n_H, and rho = 1.4 m_u n_H allowing for helium at
    cosmic abundance.  mu = 0.61 and xe = 1.2 are the standard fully
    ionised values.
    """
    rho = 1.4*mu_u*nH
    ntot = rho/(mu*mu_u)
    return 1.5*ntot*kB*T/(xe*nH*nH*cooling_function(T))


def rt_width_fraction(alpha, A, m, R_cd_over_R):
    """Rayleigh-Taylor mixing width as a fraction of the outer shock radius.

    Module 7 measures the self-similar mixing law h = alpha A g t^2 for a
    plane interface under a CONSTANT acceleration g, and derives
    g = m(1-m) R/t^2 for a shell whose radius follows R ~ t^m.  Putting the
    second into the first,

        h = alpha A m(1-m) R_cd,

    so h/R_shock = alpha A m(1-m) (R_cd/R_shock).  BOTH t AND R CANCEL.  The
    comparison needs no distance and no age, only alpha, A and the expansion
    index m.

    Two hard bounds follow, and they are what make this a test rather than a
    fit.  A <= 1 by its definition, and m(1-m) <= 1/4 with equality at
    m = 1/2, so

        h/R_shock <= alpha/4 x (R_cd/R_shock)

    for every possible shell.  No choice of A or m can raise it.
    """
    return alpha*A*m*(1.0 - m)*R_cd_over_R


def radiative_transition(E, nH_ambient, xi0, mu=0.61, gamma=GAM_MONO):
    """Solve t_cool(post-shock gas) = t for the Sedov solution.

    The remnant is adiabatic while it expands faster than it can radiate.
    The post-shock temperature falls as t^(-6/5) and the cooling time
    therefore falls too, while the age rises: the two cross once.  Returns
    (t_rad in s, R_rad in cm, T2 at that moment in K, v_s in cm/s).
    """
    rho0 = 1.4*mu_u*nH_ambient
    nH2 = strong_shock_density(gamma)*nH_ambient

    def f(logt):
        t = 10.0**logt
        vs = sedov_shockspeed(E, rho0, t, xi0)
        T2 = strong_shock_temperature(vs, mu, gamma)
        return np.log10(cooling_time(T2, nH2, mu)) - logt

    lo, hi = 6.0, 16.0                      # log10 t, 1e6 s to 3e8 yr
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if f(lo)*f(mid) <= 0.0:
            hi = mid
        else:
            lo = mid
    t = 10.0**(0.5*(lo + hi))
    vs = sedov_shockspeed(E, rho0, t, xi0)
    return t, sedov_radius(E, rho0, t, xi0), \
        strong_shock_temperature(vs, mu, gamma), vs


# =========================================================================
# Reporting
# =========================================================================

def main():
    P = print
    P('=' * 74)
    P('MODULE 8 NUMBERS: shocks and the Sedov-Taylor blast wave')
    P('=' * 74)

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  The Rankine-Hugoniot conditions are Module 2 integrated')
    P('-'*74)
    # Build a shock from the jump formulae, then verify the three fluxes
    # match.  This is a check that PART A is self-consistent, not a check
    # against nature.
    gamma = GAM_MONO
    M1 = 5.0
    rho1, p1 = 1.0e-24, 1.0e-12
    c1 = np.sqrt(gamma*p1/rho1)
    v1 = M1*c1
    r, pr, tr = rh_jumps(M1, gamma)
    rho2, p2, v2 = rho1*r, p1*pr, v1/r
    res = rh_from_fluxes(rho1, v1, p1, rho2, v2, p2, gamma)
    P(f'  test shock: gamma = 5/3, M1 = {M1}, rho1 = {rho1:.1e} g/cm^3')
    P(f'    upstream  v1 = {v1/1e5:.2f} km/s, c1 = {c1/1e5:.2f} km/s')
    P(f'    jumps     rho2/rho1 = {r:.5f}  p2/p1 = {pr:.5f}  '
      f'T2/T1 = {tr:.5f}')
    P(f'    flux residuals (mass, momentum, energy) = '
      f'{res[0]:+.2e} {res[1]:+.2e} {res[2]:+.2e}')
    P(f'    downstream Mach number M2 = {rh_downstream_mach(M1, gamma):.5f}')
    P('    READ: the three jump ratios were derived by solving the three')
    P('    flux equalities, and substituting them back reproduces those')
    P('    equalities to machine precision.  Nothing about the interior of')
    P('    the shock was used, which is the point: the layer is thinner')
    P('    than anything the fluid equations resolve.')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  Jump ratios against upstream Mach number')
    P('-'*74)
    P(f'  {"M1":>6} | {"rho2/rho1":>10} {"p2/p1":>9} {"T2/T1":>9} '
      f'{"M2":>7} {"ds/k":>8} | {"rho2/rho1":>10} {"p2/p1":>9} '
      f'{"T2/T1":>9} {"M2":>7} {"ds/k":>8}')
    P(f'  {"":>6} | {"gamma = 5/3":^48} | {"gamma = 7/5":^48}')
    for m in (1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 10.0, 30.0, 100.0):
        a = rh_jumps(m, GAM_MONO)
        b = rh_jumps(m, GAM_DIAT)
        P(f'  {m:>6.1f} | {a[0]:>10.4f} {a[1]:>9.3f} {a[2]:>9.4f} '
          f'{rh_downstream_mach(m, GAM_MONO):>7.4f} '
          f'{entropy_jump(m, GAM_MONO):>8.4f} | '
          f'{b[0]:>10.4f} {b[1]:>9.3f} {b[2]:>9.4f} '
          f'{rh_downstream_mach(m, GAM_DIAT):>7.4f} '
          f'{entropy_jump(m, GAM_DIAT):>8.4f}')
    P('')
    P(f'  strong-shock density ceiling (gamma+1)/(gamma-1):')
    P(f'    gamma = 5/3  ->  {strong_shock_density(GAM_MONO):.4f}   '
      f'(within 1% of it at M1 = '
      f'{np.sqrt(198.0/(GAM_MONO-1.0)):.1f}, see P6)')
    P(f'    gamma = 7/5  ->  {strong_shock_density(GAM_DIAT):.4f}')
    for g, name in ((GAM_MONO, '5/3'), (GAM_DIAT, '7/5')):
        lim = strong_shock_density(g)
        for m in (3.0, 5.0, 10.0, 30.0):
            P(f'    gamma = {name}: M1 = {m:>4.0f} gives '
              f'{rh_jumps(m, g)[0]/lim*100:.2f}% of the ceiling')
    P('  The pressure and temperature ratios have NO ceiling: p2/p1 grows')
    P('  as M1^2 and T2/T1 as M1^2.  A strong shock is a device for making')
    P('  a hot gas, not a dense one.')
    P('')
    P('  Entropy and why rarefaction shocks do not exist:')
    for m in (0.5, 0.8, 0.9, 1.0, 1.1, 1.5, 3.0):
        P(f'    M1 = {m:>4.1f}  ds/k = {entropy_jump(m, GAM_MONO):>+9.5f} '
          f'(gamma = 5/3)   {entropy_jump(m, GAM_DIAT):>+9.5f} '
          f'(gamma = 7/5)')
    P('  The conservation laws admit BOTH signs of M1 - 1.  The second law')
    P('  admits only M1 > 1.  A jump from rarefied to dense with M1 < 1 -')
    P('  a rarefaction shock - would destroy entropy, so a rarefaction')
    P('  spreads out as a smooth fan instead.  This is the only place in')
    P('  Modules 1-8 where thermodynamics, not dynamics, selects the')
    P('  solution.')
    P('')
    P('  The isothermal shock: no ceiling at all.')
    for m in (2.0, 5.0, 10.0, 20.0):
        P(f'    M = v1/c_T = {m:>4.1f}  ->  rho2/rho1 = '
          f'{isothermal_shock_compression(m):>7.1f}  '
          f'(adiabatic gamma = 5/3 would give '
          f'{rh_jumps(m, GAM_MONO)[0]:.3f})')
    P('  A 10 km/s shock into 10 K molecular gas, c_T = '
      f'{np.sqrt(kB*10.0/(2.33*mu_u))/1e5:.3f} km/s, has M = '
      f'{1e6/np.sqrt(kB*10.0/(2.33*mu_u)):.1f}')
    P(f'  and compresses by {1e6**2/(kB*10.0/(2.33*mu_u)):.0f}, not by 4.')

    # ---------------------------------------------------------------- C
    P('')
    P('PART C.  The Sedov-Taylor solution')
    P('-'*74)
    P('  Dimensional argument first.  From E [g cm^2 s^-2], rho_0 [g cm^-3]')
    P('  and t [s] there is exactly one length: (E t^2/rho_0)^(1/5).  So')
    P('  R = xi_0 (E t^2/rho_0)^(1/5) with xi_0 a pure number, and the')
    P('  exponent 2/5 is fixed with no dynamics at all.  Only xi_0 needs')
    P('  the similarity solution.')
    P('')
    consts = {}
    for g, name in ((GAM_MONO, '5/3'), (GAM_DIAT, '7/5')):
        xi0, J, K = sedov_xi0(g)
        consts[name] = (xi0, J, K)
        P(f'  gamma = {name}  energy integral J = {J:.8f}')
        P(f'                K = 4 pi J = 1/xi_0^5 = {K:.6f}')
        P(f'                xi_0 = {xi0:.6f}')
    P('')
    P('  VERIFICATION 1 - the integrated profile satisfies the equations')
    P('  that were eliminated during the algebra:')
    for g, name in ((GAM_MONO, '5/3'), (GAM_DIAT, '7/5')):
        for lam, rc, re_ in sedov_ode_residual(g):
            P(f'    gamma = {name}  lambda = {lam:.3f}  '
              f'continuity residual {rc:+.2e}  entropy residual {re_:+.2e}')
    P('')
    P('  VERIFICATION 2 - against published values:')
    xi0_53 = consts['5/3'][0]
    xi0_14 = consts['7/5'][0]
    pub_53 = TC17_XI_G53**0.2
    pub_14 = KT07_EBLAST_SPH_G14**-0.2
    P(f'    gamma = 5/3: Tang & Chevalier (2017) quote xi = 2.026 in')
    P(f'      R = (xi E t^2/rho)^(1/5), citing Taylor (1946), Sedov (1959)')
    P(f'      and Book (1994).  That is xi_0 = 2.026^(1/5) = {pub_53:.6f}')
    P(f'      computed here                                = {xi0_53:.6f}')
    P(f'      PUNCHLINE ratio                              = '
      f'{xi0_53/pub_53:.6f}')
    P(f'    gamma = 7/5: Kamm & Timmes (2007) set the spherical standard')
    P(f'      problem with rho_0 = 1 and E = 0.851072 erg so the shock is')
    P(f'      at r = 1.0 cm at t = 1.0 s.  That is xi_0 = '
      f'0.851072^(-1/5) = {pub_14:.6f}')
    P(f'      computed here                                = {xi0_14:.6f}')
    P(f'      PUNCHLINE ratio                              = '
      f'{xi0_14/pub_14:.6f}')
    P(f'      and K = 1/xi_0^5 computed here = {consts["7/5"][2]:.6f} '
      f'against their 0.851072, ratio '
      f'{consts["7/5"][2]/KT07_EBLAST_SPH_G14:.6f}')
    P('')
    P(f'    THIRD, INDEPENDENT: Taylor\'s own K for gamma = 1.40, obtained in')
    P(f'      1941 by hand integration, is {TAYLOR_K14}.  Exact value here: '
      f'{consts["7/5"][2]:.6f}.')
    P(f'      ratio Taylor/exact = {TAYLOR_K14/consts["7/5"][2]:.5f}, so his')
    P(f'      approximate formulae were good to '
      f'{abs(TAYLOR_K14/consts["7/5"][2]-1)*100:.2f}% - and that error')
    P(f'      propagates to the energy as itself, since E is linear in K.')
    P('')
    P('  Profiles at selected radii (values relative to the post-shock state):')
    for g, name in ((GAM_MONO, '5/3'), (GAM_DIAT, '7/5')):
        lam, u, gg, hh = sedov_profile(g)
        u1 = 4.0/(5.0*(g + 1.0))
        g1 = (g + 1.0)/(g - 1.0)
        h1 = 8.0/(25.0*(g + 1.0))
        P(f'    gamma = {name}: {"r/R":>6} {"rho/rho2":>10} {"v/v2":>10} '
          f'{"p/p2":>10}')
        for lt in (1.0, 0.95, 0.9, 0.8, 0.6, 0.4, 0.2, 0.05):
            i = int(np.argmin(abs(lam - lt)))
            # v/v2 = (r/t)u / ((R/t) u1) = lambda u/u1
            P(f'    {"":>13} {lam[i]:>6.3f} {gg[i]/g1:>10.5f} '
              f'{lam[i]*u[i]/u1:>10.5f} {hh[i]*lam[i]**2/h1:>10.5f}')
        i50 = int(np.argmin(abs(lam - 0.5)))
        P(f'      half the mass sits outside r/R = ' +
          f'{_mass_median(lam, gg):.4f}; the interior is nearly empty '
          f'(rho/rho2 = {gg[i50]/g1:.4f} at r/R = 0.5)')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  THE ANCHOR CHECK: Taylor\'s Trinity table')
    P('-'*74)
    t, R, auth = load_trinity()
    P(f'  {len(t)} rows read from afd/data/taylor1950_trinity.dat,')
    P(f'  t from {t[0]*1e3:.2f} to {t[-1]*1e3:.1f} ms, '
      f'R from {R[0]/100:.1f} to {R[-1]/100:.1f} m')

    slope, slope_err, icept = fit_powerlaw(t, R)
    slope24, slope24_err, icept24 = fit_powerlaw(t[1:], R[1:])
    slope19, slope19_err, _ = fit_powerlaw(t[1:20], R[1:20])
    P('')
    P('  CHECK 1 (CONFIRMED).  The exponent.')
    P('    Predicted, from dimensional analysis alone: 0.400000, exactly.')
    P('    Nothing was fitted to get it and no property of air entered it.')
    P(f'    {"rows used":<32} {"t range (ms)":>14} {"exponent":>18} '
      f'{"ratio":>7} {"sigma":>7}')
    fits = (("all 25", slope, slope_err, t[0], t[-1]),
            ("24, from 0.24 ms (his range)", slope24, slope24_err,
             t[1], t[-1]),
            ("19, 0.24 to 4.61 ms", slope19, slope19_err, t[1], t[19]))
    for lbl, sl, se, ta, tb in fits:
        P(f'    {lbl:<32} {ta*1e3:>6.2f}-{tb*1e3:<7.2f} '
          f'{sl:>10.4f} +/- {se:.4f} {sl/0.4:>7.4f} '
          f'{(sl-0.4)/se:>7.1f}')
    worst = max(abs(sl/0.4 - 1.0) for _, sl, _, _, _ in fits)
    P(f'    PUNCHLINE.  Every fitting choice returns an exponent within '
      f'{worst*100:.1f}%')
    P('    of 2/5, over 25 rows spanning a factor 620 in time and 17 in')
    P('    radius.  Taylor published the prediction in 1941, four years')
    P('    before the explosion and nine before he saw the film.')
    P('    Read the sigma column too, and read it as a WARNING rather')
    P('    than as a result: the three choices do not agree with each')
    P('    other inside their formal errors, so those errors are not')
    P('    describing the real uncertainty.  CHECK 2 says why.')

    n_i = taylor_intercept(t, R)
    n_fixed = float(np.mean(n_i[1:]))       # Taylor drops the 0.10 ms point
    P('')
    P('  Taylor\'s own statistic, (5/2) log10 R - log10 t with R in cm:')
    P(f'    {"t (ms)":>8} {"R (m)":>8} {"auth":>5} {"(5/2)lgR - lg t":>16} '
      f'{"residual":>10}')
    for ti, Ri, ai, ni in zip(t, R, auth, n_i):
        P(f'    {ti*1e3:>8.2f} {Ri/100:>8.1f} {ai:>5} {ni:>16.4f} '
          f'{ni-n_fixed:>+10.4f}')
    P(f'    mean over all 25 rows                = {np.mean(n_i):.4f}')
    P(f'    mean over the 24 rows from 0.24 ms   = {n_fixed:.4f}')
    P(f'    Taylor\'s printed line, his eq. (1)   = {TAYLOR_INTERCEPT:.4f}')
    P(f'    PUNCHLINE ratio of R^5 t^-2 implied  = '
      f'{10**(2*n_fixed)/10**(2*TAYLOR_INTERCEPT):.5f}')
    P('    Reproducing his intercept to 4 decimal places is the check that')
    P('    the 1950 letterpress digits were transcribed correctly.  It is')
    P('    a check of the DATA FILE, not of the physics.')

    P('')
    P('  CHECK 2 (REFUTED).  The model behind the exponent.')
    resid = n_i - n_fixed
    bands = ((0, 1, 'row 1 alone, 0.10 ms'),
             (1, 14, 'rows 2-14, 0.24-1.93 ms'),
             (14, 20, 'rows 15-20, 3.26-4.61 ms'),
             (20, 25, 'rows 21-25, 15-62 ms'))
    P('    Mean residual in four bands of time:')
    for lo, hi, lbl in bands:
        P(f'      {lbl:<28} {np.mean(resid[lo:hi]):>+9.4f}   '
          f'scatter within band {np.std(resid[lo:hi]):.4f}')
    b1 = float(np.mean(resid[1:14]))
    b2 = float(np.mean(resid[14:20]))
    b3 = float(np.mean(resid[20:25]))
    step = b1 - b3
    P(f'    The three later band means fall monotonically: {b1:+.4f} -> '
      f'{b2:+.4f} -> {b3:+.4f},')
    P(f'    with row 1 far below all three at {resid[0]:+.4f}.  The fall from')
    P(f'    the first of those bands to the last is {step:.4f} in '
      f'(5/2) log10 R,')
    P(f'    which is a factor {10**(step/2.5):.3f} in R at fixed t, '
      f'{(10**(step/2.5)-1)*100:.1f}%.')
    se1 = float(np.std(resid[1:14], ddof=1)/np.sqrt(13))
    se3 = float(np.std(resid[20:25], ddof=1)/np.sqrt(5))
    P(f'    Standard errors of those two band means: {se1:.4f} and {se3:.4f}.')
    P(f'    The step is {step/np.hypot(se1, se3):.1f} times their combined error.  A structured')
    P('    residual is a failed model, not a noisy measurement, and it')
    P('    means the formal errors in CHECK 1 are underestimates: they')
    P('    assume independent scatter, and this scatter is not.')
    P('    ONE HONEST CAVEAT.  The bands coincide with Taylor\'s three')
    P('    photographic sources - his "authority" column, reproduced in')
    P('    the data file - so part of the step between bands could be a')
    P('    change of instrument rather than of physics.  Two things')
    P('    cannot be explained that way.  First, the trend INSIDE one')
    P('    source: rows 21-23 are all authority C and fall steadily,')
    P(f'    {resid[20]:+.4f} -> {resid[21]:+.4f} -> {resid[22]:+.4f}.  Second, the 0.10 ms point,')
    P('    which comes from the SAME source as rows 2-14 and sits')
    P(f'    {abs(resid[0]-b1):.2f} below their mean, {abs(resid[0]-b1)/np.std(resid[1:14], ddof=1):.0f} times their scatter.')
    P('    WHAT FAILS, in order of the time at which it shows:')
    P(f'      t = 0.10 ms the residual is low by {abs(resid[0]):.2f}: the observed ball')
    P(f'                  is {(1-10**(resid[0]/2.5))*100:.0f}% SMALLER in radius than a point')
    P('                  explosion of this energy would make it.  Two')
    P('                  candidate causes, NEITHER computed in this script:')
    P('                  energy still in radiation rather than in the gas,')
    P('                  and a source of finite size and mass.')
    c_air = np.sqrt(GAM_DIAT*1.01325e6/TAYLOR_RHO0)
    for k in (7, 19, 24):
        vs_k = 0.4*R[k]/t[k]
        M_k = vs_k/c_air
        P(f'      at t = {t[k]*1e3:>5.2f} ms  v_s = (2/5)R/t = {vs_k/1e5:>6.2f} km/s, '
          f'M1 = {M_k:>5.1f}, rho2/rho1 = {rh_jumps(M_k, GAM_DIAT)[0]:.3f} '
          f'= {rh_jumps(M_k, GAM_DIAT)[0]/6.0*100:.0f}% of the strong limit')
    P('      t > 5 ms    the strong-shock boundary values that the Sedov')
    P('                  solution is built on stop holding: by 62 ms the')
    P('                  shock (sound speed from p0 = 1.01325e6 dyn/cm^2 and')
    P('                  Taylor\'s rho_0) is compressing to well under the')
    P('                  ceiling of 6, and the neglected ambient pressure')
    P('                  is doing work.  The residual falls.')
    P('      t < 1 ms    Taylor notes the ball of fire reached the ground')
    P('                  "in less than 1 msec"; the device was fired 100 ft')
    P('                  up, so from about 1 ms onward the flow is a sphere')
    P('                  cut by a plane, not a free sphere.')
    P('      throughout  gamma = 1.4 is wrong behind the shock.  Taylor')
    P('                  says so himself: vibrational excitation lowers')
    P('                  gamma, dissociation and radiation raise it, and')
    P('                  he argues the effects cancel.  They cancel well')
    P('                  enough for the exponent and not for the energy.')

    P('')
    P('  CHECK 3.  The energy, and how far the refutation costs.')
    R5t2 = 10.0**(2.0*n_fixed)
    xi0_air = consts['7/5'][0]
    K_air = consts['7/5'][2]
    E_here = K_air*TAYLOR_RHO0*R5t2
    E_taylorK = TAYLOR_K14*TAYLOR_RHO0*R5t2
    P(f'    R^5 t^-2 from the fixed-slope fit    = {R5t2:.4e} cm^5 s^-2')
    P(f'    Taylor\'s printed value, his eq. (3)  = {TAYLOR_R5T2:.4e} '
      f'(ratio {R5t2/TAYLOR_R5T2:.4f})')
    P(f'      NOTE: his own eq. (1) intercept of {TAYLOR_INTERCEPT} implies')
    P(f'      10^(2 x {TAYLOR_INTERCEPT}) = {10**(2*TAYLOR_INTERCEPT):.4e}, not the '
      f'{TAYLOR_R5T2:.4e} he prints')
    P(f'      two paragraphs later.  That is a '
      f'{abs(10**(2*TAYLOR_INTERCEPT)/TAYLOR_R5T2-1)*100:.1f}% inconsistency inside the')
    P('      paper itself, and it propagates straight into his energy.')
    P(f'    rho_0 he assumed                     = {TAYLOR_RHO0:.3e} g/cm^3')
    P(f'    E = K rho_0 R^5 t^-2 with exact K    = {E_here:.4e} erg')
    P(f'      with Taylor\'s K = {TAYLOR_K14}            = {E_taylorK:.4e} erg')
    P(f'    Taylor\'s printed E, his Table 3      = {TAYLOR_E14:.4e} erg '
      f'(ratio {E_here/TAYLOR_E14:.4f})')
    P(f'    in modern kilotons, 1 kt = {KT_ERG:.3e} erg:')
    P(f'      this script                        = {E_here/KT_ERG:.2f} kt')
    P(f'      Taylor\'s energy in modern kt       = '
      f'{TAYLOR_E14/KT_ERG:.2f} kt')
    P(f'      Taylor\'s own quoted figure         = {TAYLOR_TONS14:.0f} tons')
    P(f'        (he used 1 g T.N.T. = 1000 cal = 4.18e10 erg on the LONG')
    P(f'         ton, 1 ton = {TAYLOR_ERG_PER_TON:.3e} erg; the modern kt is')
    P(f'         {KT_ERG/1e3/TAYLOR_ERG_PER_TON:.4f} times his ton, so his 16,800 tons is')
    P(f'         {TAYLOR_E14/KT_ERG:.2f} kt in the modern convention, not 16.8)')
    P(f'      Department of Energy released value = {DOE_YIELD_KT:.1f} kt')
    P(f'      Selby et al. (2021) radiochemistry  = {SELBY_YIELD_KT:.1f} '
      f'+/- {SELBY_YIELD_ERR:.1f} kt')
    P(f'    PUNCHLINE ratio blast-wave/DOE        = '
      f'{E_here/KT_ERG/DOE_YIELD_KT:.3f}')
    P(f'    PUNCHLINE ratio blast-wave/Selby      = '
      f'{E_here/KT_ERG/SELBY_YIELD_KT:.3f}  '
      f'({(SELBY_YIELD_KT-E_here/KT_ERG)/SELBY_YIELD_ERR:.1f} sigma low)')
    P('    READ THE DIRECTION.  The blast wave sees only the energy that')
    P('    was in the GAS when the similarity solution took hold.  It')
    P(f'    misses {(1-E_here/KT_ERG/SELBY_YIELD_KT)*100:.0f}% of the yield, and that is not an error in')
    P('    the hydrodynamics: it is radiation that escaped the fireball')
    P('    plus energy still locked in dissociation and ionisation.')
    P('    Note also the direction of the density error.  The site was a')
    P('    desert well above sea level (its elevation is NOT sourced in')
    P('    this script - flag it before quoting a number), so its air was')
    P('    less dense than the 1.25e-3 g/cm^3 Taylor assumed.  E is linear')
    P('    in rho_0, so a more honest rho_0 makes the recovered energy')
    P('    SMALLER and the gap WIDER.  Nothing here closes it.')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  THE ASTROPHYSICAL CHECK: Voyager 2 at a real shock')
    P('-'*74)
    P('  Richardson, Kasper, Wang, Belcher & Lazarus (2008), Nature 454,')
    P('  63-66.  Voyager 2 crossed the solar-wind termination shock at')
    P('  84 AU between 30 August and 1 September 2007.')
    P('')
    P('  CONFIRMED.  Their Fig. 5 compares that crossing with Neptune\'s')
    P('  inbound bow shock, measured by the SAME instrument on the SAME')
    P('  spacecraft in August 1989.  Their caption, read directly:')
    P(f'    Neptune bow shock, density jump        = '
      f'{V2_NEPTUNE_DENSITY_JUMP:.1f}')
    P(f'    Neptune bow shock, speed drop          = '
      f'{V2_NEPTUNE_SPEED_DROP:.1f}')
    P(f'    predicted ceiling (gamma+1)/(gamma-1)  = '
      f'{strong_shock_density(GAM_MONO):.1f}   (gamma = 5/3, fixed by')
    P('      the gas being monatomic; no data went into it)')
    P(f'    PUNCHLINE ratio                        = '
      f'{V2_NEPTUNE_DENSITY_JUMP/strong_shock_density(GAM_MONO):.3f}')
    P('    And the density jump and the speed drop are the SAME number,')
    P('    which is mass conservation across the layer, rho1 v1 = rho2 v2,')
    P('    holding to the precision of the read.')
    P(f'    Their temperature jump at Neptune      = '
      f'{V2_NEPTUNE_TEMP_JUMP:.0f}')
    # what Mach number does a temperature jump of 100 imply?
    M_from_T = _mach_from_Tratio(V2_NEPTUNE_TEMP_JUMP, GAM_MONO)
    P(f'    Mach number implied by T2/T1 = '
      f'{V2_NEPTUNE_TEMP_JUMP:.0f}          = {M_from_T:.1f}')
    P(f'    density jump that Mach number predicts = '
      f'{rh_jumps(M_from_T, GAM_MONO)[0]:.3f}')
    P(f'    PUNCHLINE consistency ratio            = '
      f'{rh_jumps(M_from_T, GAM_MONO)[0]/V2_NEPTUNE_DENSITY_JUMP:.3f}')
    P('    One Mach number, two independent Rankine-Hugoniot relations,')
    P('    one consistent answer.  That is the shape of a real test.')
    P('')
    P('  REFUTED.  The termination shock, same paper, same instrument.')
    P(f'    heliosheath proton temperature observed = '
      f'{V2_TS_T_OBSERVED:.1e} K')
    P(f'    predicted if all flow energy thermalised = '
      f'{V2_TS_T_PREDICTED:.1e} K')
    P(f'    PUNCHLINE ratio                          = '
      f'{V2_TS_T_OBSERVED/V2_TS_T_PREDICTED:.2f}, a factor '
      f'{V2_TS_T_PREDICTED/V2_TS_T_OBSERVED:.0f} short')
    P(f'    temperature jump at the termination shock = '
      f'{V2_TS_TEMP_JUMP:.0f}, against {V2_NEPTUNE_TEMP_JUMP:.0f} at Neptune')
    P(f'    density jump at the termination shock     = '
      f'{V2_TS_DENSITY_JUMP:.0f}, against {V2_NEPTUNE_DENSITY_JUMP:.0f} at Neptune')
    P('    The authors\' explanation, and the reason this refutes the')
    P('    CLOSURE and not the conservation laws: the energy per proton')
    P('    falls by 80% across the shock, and it goes to pickup ions -')
    P('    hot protons made by ionising interstellar neutrals - not to the')
    P('    thermal plasma.  A single-fluid ideal gas has nowhere to put')
    P('    that energy, so it predicts a hot thermal population that is')
    P('    not there.  Module 1 already said why this is possible: the')
    P('    solar wind at 84 AU is collisionless, so there is no mechanism')
    P('    forcing one temperature on all the ions.')
    P('')
    P('  Their Table 1, and why it is NOT used as the check:')
    P(f'    TS-2 compression ratio       = {V2_TS2_COMPRESSION:.2f} +/- '
      f'{V2_TS2_COMPRESSION_ERR:.2f}')
    P(f'    TS-2 upstream fast-mode Mach = {V2_TS2_MACH_FAST_UP:.1f} +/- '
      f'{V2_TS2_MACH_FAST_UP_ERR:.1f}')
    P(f'    TS-2 shock speed             = {V2_TS2_SHOCKSPEED:.1f} +/- '
      f'{V2_TS2_SHOCKSPEED_ERR:.1f} km/s, outward')
    P(f'    TS-2 angle normal to B       = {V2_TS2_THETA_BN:.1f} deg '
      f'(quasi-perpendicular)')
    P(f'    TS-3 compression ratio       = {V2_TS3_COMPRESSION:.2f} +/- '
      f'{V2_TS3_COMPRESSION_ERR:.2f}')
    P(f'    gas-dynamic prediction from M1 = {V2_TS2_MACH_FAST_UP:.1f}, gamma = 5/3: '
      f'{rh_jumps(V2_TS2_MACH_FAST_UP, GAM_MONO)[0]:.3f}')
    P(f'    measured                                          : '
      f'{V2_TS2_COMPRESSION:.3f}')
    P(f'    ratio {V2_TS2_COMPRESSION/rh_jumps(V2_TS2_MACH_FAST_UP, GAM_MONO)[0]:.3f}, a departure of '
      f'{abs(V2_TS2_COMPRESSION-rh_jumps(V2_TS2_MACH_FAST_UP, GAM_MONO)[0])/V2_TS2_COMPRESSION_ERR:.1f} formal sigma.')
    P('    That number is NOT quoted as a refutation, for two reasons.')
    P('    First it is partly circular: the compression ratio and the Mach')
    P('    number in that table come from the SAME Rankine-Hugoniot')
    P('    minimisation applied to the same data window, so the comparison')
    P('    tests the fit against itself.  Second the gas-dynamic formula')
    P('    is the wrong formula for a quasi-perpendicular MHD shock at')
    P(f'    {V2_TS2_THETA_BN:.1f} degrees to the field.  The right formula is the')
    P('    oblique magnetohydrodynamic jump condition, which this book does')
    P('    not derive: Module 12 builds magnetohydrodynamics but stops at')
    P('    flux freezing, magnetic pressure and tension, Alfven waves and the')
    P('    magnetorotational instability.')
    P('    The temperature comparison above has neither defect.')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  A supernova remnant through its phases')
    P('-'*74)
    E51 = 1.0e51
    nH0 = 1.0
    rho0_ism = 1.4*mu_u*nH0
    xi53 = consts['5/3'][0]
    P(f'  E = 1e51 erg, ambient n_H = 1 cm^-3, rho_0 = 1.4 m_u n_H = '
      f'{rho0_ism:.3e} g/cm^3')
    P(f'  mu = 0.61 (fully ionised, cosmic abundance), gamma = 5/3, '
      f'xi_0 = {xi53:.5f}')
    P('')
    P(f'  {"age":>10} {"R (pc)":>9} {"v_s (km/s)":>11} {"T2 (K)":>11} '
      f'{"M_swept (Msun)":>15}')
    for age_yr in (100.0, 300.0, 1e3, 3e3, 1e4, 3e4, 1e5, 3e5):
        tt = age_yr*yr
        RR = sedov_radius(E51, rho0_ism, tt, xi53)
        vv = sedov_shockspeed(E51, rho0_ism, tt, xi53)
        TT = strong_shock_temperature(vv, 0.61, GAM_MONO)
        Ms = 4.0/3.0*np.pi*RR**3*rho0_ism/Msun
        P(f'  {age_yr:>10.0f} {RR/pc:>9.3f} {vv/1e5:>11.1f} {TT:>11.3e} '
          f'{Ms:>15.1f}')
    P('  R ~ t^(2/5), v_s ~ t^(-3/5), T2 ~ v_s^2 ~ t^(-6/5).')
    P('')
    P('  Where the Sedov phase BEGINS: when the swept mass matches the')
    P('  ejecta mass.  For M_ej = 5 Msun:')
    M_ej = 5.0*Msun
    R_sweep = (3.0*M_ej/(4.0*np.pi*rho0_ism))**(1.0/3.0)
    t_sweep = np.sqrt(rho0_ism*(R_sweep/xi53)**5/E51)
    P(f'    R = {R_sweep/pc:.2f} pc, reached at t = {t_sweep/yr:.0f} yr')
    P('')
    P('  Where it ENDS: when the cooling time of the post-shock gas equals')
    P('  the age.  Cooling function, stated in cooling_function():')
    for TT in (1e8, 1e7, 3e6, 1e6, 3e5, 1e5):
        P(f'    T = {TT:.1e} K  Lambda = {float(cooling_function(TT)):.3e} '
          f'erg cm^3 s^-1  (bremsstrahlung alone would give '
          f'{2.1e-27*np.sqrt(TT):.3e})')
    t_rad, R_rad, T_rad, v_rad = radiative_transition(E51, nH0, xi53)
    P('')
    P(f'    t_rad (t_cool = age)             = {t_rad/yr:.3e} yr')
    P(f'    R_rad                            = {R_rad/pc:.2f} pc')
    P(f'    T2 at that moment                = {T_rad:.3e} K')
    P(f'    v_s at that moment               = {v_rad/1e5:.0f} km/s')
    P(f'    swept mass                       = '
      f'{4.0/3.0*np.pi*R_rad**3*rho0_ism/Msun:.0f} Msun')
    P(f'    Cioffi, McKee & Bertschinger (1988) eq. (3.33a):')
    P(f'      R_PDS = 14.0 E51^(2/7) n0^(-3/7) pc = '
      f'{CMB88_R_PDS_PC:.1f} pc for E51 = n0 = 1')
    P(f'      v_PDS = 413 n0^(1/7) E51^(1/14) km/s = '
      f'{CMB88_V_PDS_KMS:.0f} km/s')
    t_pds = 0.4*CMB88_R_PDS_PC*pc/(CMB88_V_PDS_KMS*1e5)
    P(f'      t_PDS = (2/5) R_PDS/v_PDS = {t_pds/yr:.3e} yr')
    P('      CHECKED A SECOND WAY, inside the same paper.  Their eq. (3.10)')
    P(f'      gives a shell-formation time t_sf = {CMB88_T_SF_YR:.2e} yr for')
    P('      E51 = n0 = zeta_m = 1, and their eq. (3.11) sets t_PDS = t_sf/e:')
    P(f'        t_sf/e = {CMB88_T_SF_YR/math.e:.3e} yr against the '
      f'{t_pds/yr:.3e} yr above,')
    P(f'        ratio {(t_pds/yr)/(CMB88_T_SF_YR/math.e):.4f}.  Two routes '
      'through one paper agree.')
    P(f'    PUNCHLINE ratio R_rad/R_PDS       = {R_rad/pc/CMB88_R_PDS_PC:.3f}')
    P(f'    PUNCHLINE ratio t_rad/t_PDS       = {t_rad/t_pds:.3f}')
    P(f'    A one-line criterion, t_cool = age, applied to a stated')
    P(f'    cooling function gives a radius {R_rad/pc/CMB88_R_PDS_PC:.2f} times and a time')
    P(f'    {t_rad/t_pds:.2f} times those of a full radiative-hydrodynamic')
    P('    simulation.  The time is less accurate than the radius because')
    P('    R ~ t^(2/5): a factor 3.1 in t is only a factor 1.57 in R.')
    P('    That is what should be claimed for the criterion, and no')
    P('    more.  After t_rad the shell is thin, dense and driven by the')
    P('    pressure of the hot interior: R ~ t^0.30, not t^0.40, and the')
    P('    similarity solution of PART C no longer applies.')
    P('')
    P('  What bremsstrahlung ALONE would have given:')
    P(f'    using Lambda = 2.1e-27 sqrt(T) at all T, t_rad = '
      f'{_brems_only_transition(E51, nH0, xi53)/yr:.2e} yr')
    P('    - larger by a factor '
      f'{_brems_only_transition(E51, nH0, xi53)/t_rad:.0f}.  Line cooling is not a '
      'refinement here;')
    P('    it is the dominant term everywhere below 1e7 K, and the')
    P('    remnant spends almost its whole life below 1e7 K.')

    # ---------------------------------------------------------------- G
    P('')
    P("PART G.  THE DEBT FROM MODULE 7: Rayleigh-Taylor at Tycho")
    P('-'*74)
    P('  Module 7 section 10 states that its Rayleigh-Taylor half is checked')
    P('  only against a laboratory measurement, and that no module from 1 to')
    P('  10 repays it.  This part repays it, and the answer is a refutation.')
    P('')
    P('  WHY THE COMPARISON NEEDS NO DISTANCE AND NO AGE.')
    P('    Module 7 gives h = alpha A g t^2 for a plane interface under a')
    P('    constant acceleration, and g = m(1-m) R/t^2 for a shell with')
    P('    R ~ t^m.  Substituting, h = alpha A m(1-m) R_cd, so')
    P('      h/R_BW = alpha A m(1-m) (R_cd/R_BW).')
    P('    Both t and R cancel.  Published distances to Tycho disagree with')
    P('    one another, and no distance is quoted anywhere in this part,')
    P('    because none is needed: every number below is a ratio of radii.')
    P('')
    P('  THE TWO BOUNDS THAT MAKE IT A TEST.')
    P('    A <= 1 by definition, and m(1-m) <= 1/4 with equality at m = 1/2.')
    P(f'    Katsuda et al. (2010) measure m from {K10_M_MIN} to {K10_M_MAX} '
      f'around the rim, mean {K10_M_MEAN}:')
    for m_ in (K10_M_MIN, K10_M_MEAN, K10_M_MAX, WC01_M_FORWARD):
        P(f'      m = {m_:.2f}  ->  m(1-m) = {m_*(1.0 - m_):.4f}')
    P('    Tycho sits essentially at the maximum, so the bound is tight and')
    P('    the azimuthal spread in m changes nothing.')
    P('')
    hmax = SHIMONY_ALPHA_B/4.0*W05_WC01_CD_1D
    h_best = rt_width_fraction(SHIMONY_ALPHA_B, 1.0, K10_M_MEAN, W05_WC01_CD_1D)
    h_lo = rt_width_fraction(SHIMONY_ALPHA_B - SHIMONY_ALPHA_B_ERR, 1.0,
                             K10_M_MEAN, W05_WC01_CD_1D)
    h_hi = rt_width_fraction(SHIMONY_ALPHA_B + SHIMONY_ALPHA_B_ERR, 1.0,
                             K10_M_MEAN, W05_WC01_CD_1D)
    P('  WHAT THE PLANAR LAW PREDICTS.')
    P(f'    alpha_B = {SHIMONY_ALPHA_B} +/- {SHIMONY_ALPHA_B_ERR} '
      '(Shimony et al. 2022, the value Module 7 verified),')
    P('    A = 1 (the largest it can be; the 1-D solution has a density peak')
    P('    at the contact discontinuity, Wang & Chevalier 2001), and the')
    P(f'    1-D contact discontinuity at {W05_WC01_CD_1D} of the blast-wave '
      'radius:')
    P(f'      h/R_BW = {h_best:.5f}, i.e. {100*h_best:.2f} per cent of R_BW')
    P(f'      the alpha_B error alone spans {100*h_lo:.2f} to '
      f'{100*h_hi:.2f} per cent')
    P('      and for ANY A and ANY m the ceiling is alpha/4 x '
      f'{W05_WC01_CD_1D}, which is')
    P(f'      {100*hmax:.2f} per cent at alpha_B and '
      f'{100*(SHIMONY_ALPHA_B + SHIMONY_ALPHA_B_ERR)/4.0*W05_WC01_CD_1D:.2f} '
      'per cent one sigma above it.')
    P('')
    P('  WHAT IS OBSERVED, four rungs, each from a paper read in full.')
    obs = [(W05_WC01_CD_1D, '1-D contact discontinuity, pure hydrodynamics',
            'Warren et al. (2005) sect. 7, reading Wang & Chevalier fig. 1'),
           (WC01_FINGER_TIPS, '2-D Rayleigh-Taylor finger tips, pure hydro',
            "Wang & Chevalier (2001), their own text at t' = 1.6"),
           (W05_CD_OVER_BW, "Tycho's mean contact discontinuity, deprojected",
            'Warren et al. (2005), abstract'),
           (1.0, "Tycho's ejecta clumps at several azimuths",
            'Warren et al. (2005), sect. 3')]
    for r_, what, where in obs:
        P(f'    R/R_BW = {r_:.2f}   {what}')
        P(f'                     {where}')
    P('')
    P('  THE COMPARISON.  A width against a width, never against a position:')
    for tip, label in ((WC01_FINGER_TIPS, 'simulated finger tips'),
                       (W05_CD_OVER_BW, "Tycho's mean CD, deprojected"),
                       (1.0, "Tycho's farthest clumps")):
        w = tip - W05_WC01_CD_1D
        P(f'    observed width from {label:32s} = {w:.2f} R_BW,'
          f'  predicted/observed = {h_best/w:.3f}')
    w_sim = WC01_FINGER_TIPS - W05_WC01_CD_1D
    P(f'    PUNCHLINE ratio predicted/simulated = {h_best/w_sim:.3f}, '
      f'a factor {w_sim/h_best:.0f} short')
    P('')
    P('  AND NOTHING INSIDE THE LAW CAN CLOSE IT.')
    alpha_req = w_sim/(1.0*K10_M_MEAN*(1.0 - K10_M_MEAN)*W05_WC01_CD_1D)
    P(f'    To reach even the simulated {w_sim:.2f} R_BW the law would need')
    P(f'      alpha = {alpha_req:.3f}, which is {alpha_req/SHIMONY_ALPHA_B:.0f} '
      f'times the measured {SHIMONY_ALPHA_B}')
    P(f'      and {alpha_req/SHIMONY_ALPHA_THEORY_3D:.1f} times the largest '
      f'theoretical value, {SHIMONY_ALPHA_THEORY_3D}, that Module 7 found.')
    P('    A cannot help: it is already at its ceiling of 1.  m cannot help:')
    P('    m(1-m) is already within 1 per cent of its ceiling of 1/4.')
    P('')
    P('  WHAT IS REFUTED, AND WHAT IS NOT.')
    P('    Refuted: the TRANSFER of the plane-interface, constant-g,')
    P('    two-uniform-fluid, forgotten-seed mixing law to a decelerating')
    P('    supernova shell.  Not refuted: the law itself, which Module 7')
    P('    checked in the regime it was measured in.')
    P('    Three reasons the transfer fails, in order of size:')
    P('      1. alpha_B is the BUBBLE coefficient.  The observed quantity is')
    P('         a SPIKE penetration, and at A near 1 spikes outrun bubbles.')
    P('         The direction is known; no paper in this folder gives a')
    P('         number for alpha_spike, so none is printed here.')
    P('      2. The seed is not forgotten.  The law assumes the initial')
    P('         conditions are lost after about three merger generations.')
    P('         At the contact discontinuity the reverse shock feeds the')
    P('         interface continuously, and Wang & Chevalier need ejecta')
    P('         clumps with a density contrast of at least 100 to reproduce')
    P("         Tycho's protrusions at all.")
    P('      3. g is not constant.  g = m(1-m)R/t^2 falls as t^(m-2), and')
    P('         the double time integral from t = 0 does not converge, so')
    P('         the coefficient depends on when deceleration began.  This is')
    P('         a scaling, good to a factor of a few, not a theorem.')
    P('')
    P('  ONE HONEST CAVEAT, AND IT PUSHES THE SAME WAY.')
    P('    Warren et al. conclude that the measured 0.93 is "inconsistent')
    P('    with adiabatic hydrodynamical models, even when Rayleigh-Taylor')
    P('    instabilities are taken into account", and they attribute the')
    P('    small gap to cosmic-ray acceleration raising the compression')
    P('    factor at the blast wave.  So part of the observed width is not')
    P('    Rayleigh-Taylor at all.  Take their reading at face value and use')
    P(f'    only the pure-hydrodynamic simulation: the shortfall is still a')
    P(f'    factor {w_sim/h_best:.0f}.  Nothing here rests on the 0.93.')
    P('    Their projection corrections are also unequal - the blast wave is')
    P(f'    overestimated by about 3 per cent and the contact discontinuity')
    P('    by about 6 per cent - and their contact-discontinuity radius moves')
    P(f'    from {W05_CD_OVER_BW_2SIG} to {W05_CD_OVER_BW_4SIG} of R_BW as '
      'the threshold goes from 2 to 4 sigma.')
    P('    The projected ratio is '
      f'{W05_CD_ARCSEC/W05_BW_ARCSEC:.4f} ({W05_CD_ARCSEC:.0f}"/'
      f'{W05_BW_ARCSEC:.0f}"), against {W05_CD_OVER_BW} deprojected.')
    P('')
    P('  WHAT IS NOT USED, AND WHY.')
    P("    Warren's strongest single azimuthal mode of the contact")
    P('    discontinuity, n = 6, has an amplitude of 3.3 per cent of the mean')
    P('    radius - but they add that "the BW shows nearly the same value",')
    P('    and the blast wave is not Rayleigh-Taylor unstable.  A number that')
    P('    both surfaces share cannot measure an instability only one of them')
    P('    has.  What IS specific is their high-wavenumber power: the contact')
    P('    discontinuity carries nearly an order of magnitude more of it.')
    P('    That is qualitative, and it is quoted as qualitative.')

    # ---------------------------------------------------------------- H
    P('')
    P('PART H.  NUMBERS FOR THE PROBLEM SET')
    P('-'*74)

    P('  P1.  Post-shock temperature of a 5000 km/s supernova shock.')
    for mu_, lbl in ((0.61, 'ionised cosmic abundance'),
                     (1.0, 'neutral atomic hydrogen'),
                     (0.5, 'fully ionised pure hydrogen')):
        P(f'       mu = {mu_:.2f} ({lbl}): T2 = '
          f'{strong_shock_temperature(5.0e8, mu_):.3e} K')
    P('       The three differ by a factor 2.0 across the range of mu, so')
    P('       mu must be stated with the answer.')

    P('')
    P('  P2.  Earth\'s bow shock at M1 = 8.')
    r8, p8, T8 = rh_jumps(8.0, GAM_MONO)
    P(f'       rho2/rho1 = {r8:.4f}  ({r8/4.0*100:.1f}% of the ceiling 4)')
    P(f'       p2/p1 = {p8:.2f}   T2/T1 = {T8:.2f}   '
      f'M2 = {rh_downstream_mach(8.0, GAM_MONO):.4f}')
    P(f'       ds/k = {entropy_jump(8.0, GAM_MONO):.4f}')
    v_sw, n_sw, T_sw = 4.0e7, 5.0, 1.0e5
    P(f'       with v_sw = {v_sw/1e5:.0f} km/s, n = {n_sw:.0f} cm^-3, '
      f'T = {T_sw:.0e} K upstream:')
    P(f'         T2 = {T8*T_sw:.3e} K by the ratio, and '
      f'{strong_shock_temperature(v_sw, 0.61):.3e} K by the strong-shock')
    P(f'         formula - they differ by '
      f'{abs(strong_shock_temperature(v_sw, 0.61)/(T8*T_sw)-1)*100:.0f}% because M = 8 is not infinite.')
    P(f'         n2 = {r8*n_sw:.2f} cm^-3')

    P('')
    P('  P3.  Sedov age of a 20 pc remnant.')
    for n_ in (0.1, 1.0, 10.0):
        rho_ = 1.4*mu_u*n_
        tt = np.sqrt(rho_*(20.0*pc/xi53)**5/E51)
        vv = 0.4*20.0*pc/tt
        P(f'       n_H = {n_:>4.1f} cm^-3, E = 1e51 erg: age = '
          f'{tt/yr:.3e} yr, v_s = {vv/1e5:.0f} km/s, '
          f'T2 = {strong_shock_temperature(vv, 0.61):.2e} K')
    P('       The age scales as n^(1/2) at fixed R, so a factor 100 in')
    P('       density is only a factor 10 in the inferred age.')

    P('')
    P('  P4.  The radiative transition time, scaled.')
    for E_, n_ in ((1e51, 1.0), (1e51, 0.1), (1e51, 10.0), (1e50, 1.0)):
        tr, Rr, Tr, vr = radiative_transition(E_, n_, xi53)
        P(f'       E = {E_:.0e} erg, n_H = {n_:>4.1f}: t_rad = '
          f'{tr/yr:.3e} yr, R_rad = {Rr/pc:.2f} pc, '
          f'T2 = {Tr:.2e} K, v_s = {vr/1e5:.0f} km/s')

    P('')
    P('  P5.  Entropy jump at M = 3.')
    for g, name in ((GAM_MONO, '5/3'), (GAM_DIAT, '7/5')):
        rr, pp, TT = rh_jumps(3.0, g)
        P(f'       gamma = {name}: rho2/rho1 = {rr:.4f}, p2/p1 = {pp:.4f}, '
          f'ds/k = {entropy_jump(3.0, g):.4f}')
    P('       Now reverse the direction, M1 < 1, which the three')
    P('       conservation laws permit exactly as readily:')
    for m in (0.9, 0.7, 0.5):
        rr, pp, _ = rh_jumps(m, GAM_MONO)
        P(f'         M1 = {m:.1f}: rho2/rho1 = {rr:.4f}, p2/p1 = {pp:.4f}, '
          f'ds/k = {entropy_jump(m, GAM_MONO):+.5f}')
    Mneg = np.sqrt((GAM_MONO - 1.0)/(2.0*GAM_MONO))
    P('       Every one is negative, so every one is forbidden.  And below')
    P(f'       M1 = sqrt((gamma-1)/(2 gamma)) = {Mneg:.4f} the formula gives a')
    P(f'       NEGATIVE p2/p1 ({rh_jumps(0.4, GAM_MONO)[1]:+.4f} at M1 = 0.4), so that')
    P('       branch stops existing before the second law is consulted.')

    P('')
    P('  P6.  How strong is "strong"?  The Mach number at which the')
    P('       density ratio reaches 99% of its ceiling.')
    for g, name in ((GAM_MONO, '5/3'), (GAM_DIAT, '7/5')):
        # r/r_inf = 1/(1 + 2/((gamma-1)M^2)) = 0.99  ->  M^2 = 198/(gamma-1)
        Mc = np.sqrt(198.0/(g - 1.0))
        P(f'       gamma = {name}: M1 = {Mc:.1f}, and the ratio there is '
          f'{rh_jumps(Mc, g)[0]:.4f} against {strong_shock_density(g):.4f}')
    P('       Trinity at 1 ms: v_s = (2/5) R/t = '
      f'{0.4*38.9e2/1.08e-3/1e5:.1f} km/s, ambient sound speed '
      f'{np.sqrt(1.4*1.013e6/1.25e-3)/1e5:.3f} km/s,')
    P(f'       M1 = {0.4*38.9e2/1.08e-3/np.sqrt(1.4*1.013e6/1.25e-3):.0f}. '
      f'Strong by any measure.')

    P('')
    P('  P7.  The isothermal shock in a molecular cloud.')
    cT = np.sqrt(kB*10.0/(2.33*mu_u))
    for v_ in (1e5, 5e5, 1e6, 2e6):
        P(f'       v1 = {v_/1e5:>4.0f} km/s, c_T = {cT/1e5:.3f} km/s: '
          f'M = {v_/cT:>6.1f}, rho2/rho1 = {(v_/cT)**2:>9.1f}, '
          f'against {rh_jumps(v_/cT, GAM_MONO)[0]:.3f} adiabatic')

    P('')
    P('  P8.  Trinity, worked as a student exercise from two rows only.')
    for i, j in ((3, 10), (0, 24), (14, 19)):
        Ei = sedov_energy_from_Rt(R[i], t[i], TAYLOR_RHO0, xi0_air)
        Ej = sedov_energy_from_Rt(R[j], t[j], TAYLOR_RHO0, xi0_air)
        P(f'       row {i+1:>2} (t = {t[i]*1e3:>6.2f} ms): E = '
          f'{Ei/KT_ERG:>6.2f} kt   row {j+1:>2} (t = {t[j]*1e3:>6.2f} ms): '
          f'E = {Ej/KT_ERG:>6.2f} kt')
    P('       A single (t, R) pair gives an energy, and different pairs')
    P('       give different energies.  That spread IS the refutation; a')
    P('       one-point estimate hides it.')

    P('')
    P('  P9.  Shock thickness against mean free path, the Module 1 link.')
    P('       An ideal-gas shock has no thickness at all in the equations')
    P('       of Module 2, because they contain no length.  Add viscosity')
    P('       and the layer becomes a few mean free paths wide.')
    lam_air = 6.5e-6         # cm, air at sea level, from Module 1
    P(f'       air at sea level: mfp ~ {lam_air:.1e} cm, so a shock layer')
    P(f'       is ~{3*lam_air:.0e} cm - {38.9e2/(3*lam_air):.0e} times thinner than the Trinity')
    P('       fireball at 1 ms.  The discontinuity idealisation is safe by')
    P('       eight orders of magnitude.')
    P('       At the termination shock the layer measured by Voyager 2 was')
    P('       100,000-300,000 km wide, "a few times the ion inertial')
    P('       length".  The collisional mean free path, for proton-')
    P('       proton Coulomb collisions, lambda = (kT)^2/(pi n e^4 lnL):')
    e_esu = 4.80320471e-10
    n_hs, T_hs, lnL = 2.0e-3, 1.0e5, 25.0
    lam_c = (kB*T_hs)**2/(np.pi*n_hs*e_esu**4*lnL)
    P(f'       with n = {n_hs:.0e} cm^-3 and T = {T_hs:.0e} K (read off the')
    P('       axes of their Figs 1 and 3; approximate) and ln Lambda = 25,')
    P(f'       lambda = {lam_c:.2e} cm = {lam_c/AU:.0f} AU.')
    P(f'       The layer, 1e10-3e10 cm, is {lam_c/3e10:.0e}-{lam_c/1e10:.0e} times THINNER than')
    P('       a mean free path.  That is what "collisionless shock"')
    P('       means, and it is why the one-fluid closure fails there.')

    P('')
    P('  P10. The similarity solution\'s interior.')
    for g, name in ((GAM_MONO, '5/3'), (GAM_DIAT, '7/5')):
        lam, u, gg, hh = sedov_profile(g)
        g1 = (g + 1.0)/(g - 1.0)
        h1 = 8.0/(25.0*(g + 1.0))
        i9 = int(np.argmin(abs(lam - 0.9)))
        i5 = int(np.argmin(abs(lam - 0.5)))
        i1 = int(np.argmin(abs(lam - 0.01)))
        P(f'       gamma = {name}: mass median radius r/R = '
          f'{_mass_median(lam, gg):.4f}')
        P(f'         rho/rho2 at r/R = 0.9 is {gg[i9]/g1:.4f}, '
          f'at 0.5 is {gg[i5]/g1:.5f}, at 0.01 is {gg[i1]/g1:.3e}')
        P(f'         p/p2 at r/R = 0.5 is {hh[i5]*lam[i5]**2/h1:.4f}, '
          f'at 0.01 is {hh[i1]*lam[i1]**2/h1:.4f} - flat, which is what')
        P('           an interior with almost no mass in it must be')
    P('       Nearly all the mass is in a thin shell just behind the')
    P('       shock; the interior is hot, nearly uniform in pressure, and')
    P('       nearly empty.  The snowplough phase is the limit of this,')
    P('       and PART F is where it arrives.')

    P('')
    P('=' * 74)
    P('SOURCES')
    P('=' * 74)
    P('  Taylor, Sir Geoffrey, F.R.S. (1950), "The formation of a blast wave')
    P('    by a very intense explosion.  II.  The atomic explosion of 1945",')
    P('    Proc. Roy. Soc. London A 201 (1065), 175-186.')
    P('    DOI 10.1098/rspa.1950.0050.  Received 10 November 1949.')
    P('    Table 1 (p. 176) gives the 25 (t, R) pairs, transcribed into')
    P('    afd/data/taylor1950_trinity.dat; his eq. (1) gives the line')
    P('    (5/2) log10 R - log10 t = 11.915 with R in cm and t in s; his')
    P('    eq. (3) gives R^5 t^-2 = 6.67e23; his Table 3 (p. 180) gives')
    P('    I_1 = 0.185, I_2 = 0.187, K = 0.856, E = 7.14e20 erg and a')
    P('    T.N.T. equivalent of 16,800 tons for gamma = 1.40; p. 180 states')
    P('    rho_0 = 1.25e-3 g/cm^3 and 1 ton of T.N.T. = 4.25e16 erg.')
    P('    The publisher returns HTTP 403; the PDF was read through the')
    P('    Internet Archive and extracted with PyMuPDF.  Part I of the same')
    P('    paper is Proc. Roy. Soc. London A 201 (1065), 159-174.')
    P('  Mack, J. E. (1946/47), "Semi-popular motion-picture record of the')
    P('    Trinity explosion", U.S. Atomic Energy Commission MDDC-221,')
    P('    declassified 17 July 1947.  The source of Taylor\'s photographs.')
    P('    Cited here through Taylor; not read directly.')
    P('  Kamm, J. R. & Timmes, F. X. (2007), "On efficient generation of')
    P('    numerically robust Sedov solutions", LA-UR-07-2849, Los Alamos')
    P('    National Laboratory.  Their spherical standard problem has')
    P('    rho_0 = 1 g/cm^3, omega = 0, gamma = 1.4 and E = 0.851072 erg,')
    P('    which puts the shock at r = 1.0 cm at t = 1.0 s; that fixes')
    P('    xi_0 = 0.851072^(-1/5) = 1.032777 for gamma = 7/5.')
    P('    https://cococubed.com/papers/la-ur-07-2849.pdf')
    P('  Tang, X. & Chevalier, R. A. (2017), "Shock evolution in')
    P('    non-radiative supernova remnants", MNRAS; arXiv:1607.06391,')
    P('    Appendix A: "For an ideal gas with specific heat index')
    P('    gamma = 5/3, the dimensionless constant xi(s) defined in the ST')
    P('    solution equals 2.026 when s = 0", citing Taylor (1946), Sedov')
    P(f'    (1959) and Book (1994).  That is xi_0 = 2.026^(1/5) = '
      f'{TC17_XI_G53**0.2:.6f}.')
    P('  Richardson, J. D., Kasper, J. C., Wang, C., Belcher, J. W. &')
    P('    Lazarus, A. J. (2008), "Cool heliosheath plasma and deceleration')
    P('    of the upstream solar wind at the termination shock", Nature 454,')
    P('    63-66, doi:10.1038/nature07024.  Table 1 gives the TS-2 and TS-3')
    P('    shock parameters; p. 65 states the observed heliosheath')
    P('    temperature of 1e5 K against the 1e6 K that full thermalisation')
    P('    would give; the Fig. 5 caption gives the Neptune bow-shock')
    P('    factors of 4 in density, 4 in speed and 100 in temperature.')
    P('  Cioffi, D. F., McKee, C. F. & Bertschinger, E. (1988), "Dynamics')
    P('    of radiative supernova remnants", ApJ 334, 252-265.  Their')
    P('    eqs. (3.33a) and (3.33b): R_PDS = 14.0 E51^(2/7) n0^(-3/7)')
    P('    zeta_m^(-1/7) pc and v_PDS = 413 n0^(1/7) zeta_m^(3/14)')
    P('    E51^(1/14) km/s.  Read from the ADS scan of the journal page.')
    P('    Their eq. (3.10) gives t_sf = 3.61e4 E51^(3/14) n0^(-4/7)')
    P('    zeta_m^(-5/14) yr and their eq. (3.11) sets t_PDS = t_sf/e.')
    P('    NOTE the difference in closure: their analytic cooling function is')
    P('    Lambda = 1.6e-19 zeta_m T^(-1/2) for 1e5 K < T < 10^7.5 K, not the')
    P('    T^(-0.7) line-cooling branch used above, so the ratios 1.573 and')
    P('    3.081 test the criterion AND the cooling curve together.')
    P('    Their quoted simulation shell-formation time of 1.3e5 yr is for a')
    P('    lower ambient density and is NOT comparable with the numbers here.')
    P('  Selby, H. D. et al. (2021), "A new assessment statement for the')
    P('    Trinity nuclear test, 75 years later", LA-UR-21-20675, Los')
    P('    Alamos National Laboratory; published in Nuclear Technology.')
    P('    Final yield determination 24.8 +/- 2 kt, "substantially higher')
    P('    than the previous DOE released value of 21 kilotons".')
    P('    arXiv:2103.06258.  Their own caveat, quoted because it changes')
    P('    the comparison: the DOE 21 kt carries no published uncertainty,')
    P('    and the "21 +/- 2 kt" in their text uses an uncertainty THEY')
    P('    assign, "a conservative 10% relative uncertainty on its value".')
    P('  Warren, J. S. et al. (2005), "Cosmic-ray acceleration at the')
    P("    forward shock in Tycho's supernova remnant\", ApJ 634, 376;")
    P('    astro-ph/0507478.  Abstract: azimuthally averaged radii BW 251",')
    P('    CD 241", RS 183", and "taking account of projection effects, we')
    P('    find ratios of 1 : 0.93 : 0.70 (BW : CD : RS)".  Section 3 gives')
    P('    the projected 96%, the 2-sigma and 4-sigma radii of 94% and 98%,')
    P('    the clumps reaching the blast wave, and the n = 6 amplitude of')
    P('    3.3% that the blast wave shares.  Section 4 gives P ~ k^-1.5 for')
    P('    the contact discontinuity against k^-2.2 for the blast wave.')
    P('    Section 7 reads Wang & Chevalier fig. 1 as putting the 1-D contact')
    P('    discontinuity at 77% of the blast-wave radius.  Their summary:')
    P('    the 0.93 ratio is "inconsistent with adiabatic hydrodynamical')
    P('    models, even when Rayleigh-Taylor instabilities are taken into')
    P('    account", which they explain by cosmic-ray acceleration.')
    P('  Wang, C.-Y. & Chevalier, R. A. (2001), "Instabilities and clumping')
    P('    in Type Ia supernova remnants", ApJ 549, 1119; astro-ph/0005105.')
    P('    Read directly, not through Warren: "at t\' = 1.6, the region')
    P('    occupied by the unstable ejecta does not extend beyond 85% of the')
    P('    remnant radius"; at t\' = 1.7 the forward shock is at 3.09 pc and')
    P('    the reverse shock at 2.08 pc, with expansion parameters m = 0.47')
    P('    and m = 0.15; a clump needs a density contrast of at least 100 to')
    P('    bulge the forward shock; the fingers stop growing because "the')
    P('    forward growth of the caps is blocked by the drag of the flow".')
    P('  Katsuda, S. et al. (2010), "X-ray measured dynamics of Tycho\'s')
    P('    supernova remnant", ApJ 709, 1387; arXiv:1001.2484.  The')
    P('    forward-shock expansion index varies from 0.26 to 0.65 with')
    P('    azimuth and averages 0.52, consistent with the radio value.')
    P('  Shimony, A., Huntington, C. M., Flippo, K. A., Elbaz, Y.,')
    P('    MacLaren, S. A., Shvarts, D. & Malamud, G. (2022), "Determining')
    P('    the Self-Similar Stage of the Rayleigh-Taylor Instability via')
    P("    LLNL's NIF Discovery Science Experiments\", arXiv:2210.06631v1.")
    P('    A PREPRINT: the arXiv record carries no journal reference and no')
    P('    DOI but its own, which is the same departure from this book\'s')
    P('    citation convention that Module 7 flagged.  Used here only for')
    P('    alpha_B = 0.038 +/- 0.008, which was read from the paper during')
    P('    Module 7 and verified there.  It is the BUBBLE coefficient.')


# --- small helpers used above, kept out of the narrative ------------------

def _mass_median(lam, g):
    """Radius inside which half the shocked mass lies, in units of R."""
    order = np.argsort(lam)
    x, y = lam[order], g[order]
    m = np.concatenate(([0.0], np.cumsum(0.5*(y[1:]*x[1:]**2 +
                                              y[:-1]*x[:-1]**2)*np.diff(x))))
    return float(np.interp(0.5*m[-1], m, x))


def _mach_from_Tratio(Tratio, gamma):
    """Invert T2/T1 for M1 by bisection.  Monotonic for M1 > 1."""
    lo, hi = 1.0, 1e4
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if rh_jumps(mid, gamma)[2] > Tratio:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo + hi)


def _brems_only_transition(E, nH, xi0, mu=0.61):
    """radiative_transition with the line-cooling branch switched off."""
    rho0 = 1.4*mu_u*nH
    nH2 = strong_shock_density(GAM_MONO)*nH

    def f(logt):
        t = 10.0**logt
        vs = sedov_shockspeed(E, rho0, t, xi0)
        T2 = strong_shock_temperature(vs, mu, GAM_MONO)
        ntot = 1.4*mu_u*nH2/(mu*mu_u)
        tc = 1.5*ntot*kB*T2/(1.2*nH2*nH2*2.1e-27*np.sqrt(T2))
        return np.log10(tc) - logt

    lo, hi = 6.0, 20.0
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if f(lo)*f(mid) <= 0.0:
            hi = mid
        else:
            lo = mid
    return 10.0**(0.5*(lo + hi))


if __name__ == '__main__':
    main()
