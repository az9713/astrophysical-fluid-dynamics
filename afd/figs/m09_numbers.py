"""Module 9 numbers: Bondi accretion and the Parker wind.

Every physical number quoted in module09.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

THE SHAPE OF THE CHECK, following Modules 2 and 3.  From one published
source table, one prediction that follows from the equations alone is
CONFIRMED, and one modelling assumption is REFUTED, with sigmas stated.

THE ANCHOR IS CHECK 1 (PART G).  It has the book's shape: Venzmer &
Bothmer (2018) Table 3 fitted four exponents to Helios 1+2 data over
0.29-0.98 au independently of one another, with no wind model imposed, so
nothing this module tests was put into the fit.  CHECK 2 (PART H, Sgr A*)
produces the LARGER ratio -- the Bondi rate exceeds the measured bound by a
factor of 40 to 160 -- but it compares two different papers against a
one-sided upper limit, so it carries no sigma.  CHECK 1 is the anchor
because it confirms and refutes from the same table and both sides carry a
sigma; CHECK 2 is the sharpest refutation by magnitude.

  CONFIRMED  The effective polytropic index of the solar wind lands inside
             the window that a transonic thermally driven wind requires.
             The critical-point analysis in PART D gives the exact
             quadratic (gamma+1) s^2 + 4(gamma-1) s + (4 gamma - 6) = 0 for
             the logarithmic slope s = dln v/dln r at the sonic point.  Its
             roots have product (4 gamma - 6)/(gamma + 1), which is
             negative -- so one root is positive and an ACCELERATING
             transonic solution exists -- if and only if gamma < 3/2.  That
             bound is fixed before any data is touched.  VB18 give
             gamma_eff = 1 + e_T/alpha = 1.394 +/- 0.016 (mean fits),
             1.436 +/- 0.021 (median fits): 6.7 and 3.0 sigma BELOW 3/2.
             The sign of the velocity exponent independently selects the
             wind branch over the breeze, which decays as v ~ r^-2.
             Note honestly what this is: an INEQUALITY satisfied, which is
             weaker than Module 2's equality alpha - beta = 2, and it
             assumes one polytropic index describes the flow from the
             sonic point outward.

  REFUTED    The isothermal assumption, three separate ways, all from the
             same table.  (i) Directly: the measured temperature exponent
             is -0.792 +/- 0.028 against the isothermal 0, a 28.3 sigma
             departure.  (Module 2 already reported the adiabatic closure
             failing at 19.6 sigma against the same number; that result is
             cited, not re-derived.)  (ii) By the acceleration: over
             0.29-0.98 au the isothermal Parker wind cannot produce the
             measured logarithmic slope 0.049 +/- 0.010 for any coronal
             temperature THAT LEAVES ITS BASE SUBSONIC.  PART F scans T_0
             from 0.5 MK to 6.26 MK, the temperature at which the sonic
             radius lands on the base r_0 = 1.03 R_sun, and the floor is
             0.1119, which is 6.3 sigma above the measurement.  The bound
             matters: the slope falls only as 1/(2 ln r/r_c), so it does
             keep falling above that ceiling, and T_0 = 1644 MK would
             reach 0.049 -- a factor 548 to 822 above the measured 2-3 MK
             corona.  PART F prints both halves.  (iii) By the
             base temperature: the T_0 that reproduces the measured 1-au
             speed is about 1 MK, while VB18 section 6 cites a near-Sun
             coronal temperature of 2-3 MK.  Read (iii) carefully: fitting
             one free parameter to one measured number is not a
             confirmation of anything.  The content is that the fitted T_0
             then DISAGREES with the independently measured corona by a
             factor of 2 to 3.

  AND THE SHARPEST RESULT, PART G3.  The critical-point equation
             (v^2 - c_s^2) dln v/dln r = 2 c_s^2 - GM/r holds for ANY
             steady spherical barotropic flow -- no wind model, no
             polytrope, no isothermal assumption.  Feed it the VB18 mean
             fits at 1 au and it predicts dln v/dln r = 0.0164.  The
             measured value is 0.049 +/- 0.010.  Proton thermal pressure
             supplies about one third of the measured acceleration at 1 au;
             the shortfall is about 3 sigma against the formal error and
             about 2.7 against the year-to-year scatter; PART G3 and
             PUNCHLINE 3 print the computed values, and this sentence is
             deliberately rounded so that the two cannot drift apart.  What this does NOT do
             is name the missing force.  It assumes T_e = T_p = T_He, which
             the solar wind does not obey at 1 au, and it applies power-law
             fits of ensemble medians inside a nonlinear equation.

A NOTE ON WHAT EACH CHECK CAN AND CANNOT TOUCH.  Module 3's solar-model
check could not test hydrostatic equilibrium, because the model was built
by solving it.  Module 9 does not have that problem on the Parker side:
VB18 fitted power laws to measured plasma parameters with no fluid equation
imposed.  It DOES have a weaker version of it on the Sgr A* side: Baganoff
et al. computed their own Bondi rate from their own measured n_e and kT, so
reproducing their 3e-6 M_sun/yr confirms only that this script implements
the same formula.  The test is the comparison of that rate against Marrone
et al.'s independent Faraday-rotation bound.

Sources for every published number compared against are listed in the
SOURCES block at the foot of this file and in module09.html.
"""
import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m01/m02/m03_numbers.py rather than imported, so that
# each module's numbers script reads on its own.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
mp = 1.67262192369e-24  # g
me = 9.1093837015e-28   # g
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
sigma_T = 6.6524587321e-25   # cm^2      (Thomson cross-section)
eV = 1.602176634e-12    # erg           (exact, SI definition)
keV = 1.0e3*eV
pc = 3.0856775814913673e18   # cm
kpc = 1e3*pc
AU = 1.495978707e13     # cm
yr = 3.15576e7          # s

# IAU 2015 nominal solar conversion constants.  GM is the measured
# quantity; M follows from it and from the CODATA G.
GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
Rsun = 6.957e10         # cm             (IAU 2015 nominal)
Lsun = 3.828e33         # erg/s          (IAU 2015 nominal)
Msun = GMsun/G          # g

# =========================================================================
# Composition, fixed ONCE and used for every pressure and every density in
# this file.  Mixing conventions between P and rho is a ~6% error and it is
# the easiest one to make.
#
# THE 5% HELIUM IS THIS MODULE'S OWN CHOICE, NOT VB18's CONVENTION.  The
# source-verification pass (2026-09-18) read the paper and found that VB18
# assume NO helium in their own analysis.  Their section 1, page 2: "In the
# analyses, we treat the solar wind as a proton plasma - the average helium
# abundance is about 4.5 % and in slow wind at solar cycle minimum is even
# less than 2 %."  Their Table 3 density is therefore a PROTON density on a
# proton-plasma assumption.  The 5% sentence that an earlier version of this
# comment leaned on is in their section 6 (page 11) and is about converting
# LEBLANC et al. (1998)'s electron densities for the near-Sun extrapolation
# of their Fig. 11, not about the Helios fits.
# So: y = 0.05 is adopted here as this module's composition, close to the
# 4.5% VB18 quote as typical, and module09.html must say it is a choice.
# Fully ionised, A_He = 4:
#     n_e   = n_p (1 + 2 y)          = 1.10 n_p
#     n_tot = n_p (1 + y + 1 + 2 y)  = 2.15 n_p
#     rho   = n_p m_p (1 + 4 y)      = 1.20 n_p m_p
#     mu    = rho/(n_tot m_p)        = 0.5581
# The isothermal sound speed squared is then kT/(mu m_p) = P/rho with
# P = n_tot k T, which is the identity every formula below relies on.
# =========================================================================
HE_FRAC = 0.05                 # helium/hydrogen by number, THIS MODULE'S
#                                choice; see the block above
MU_WIND = (1.0 + 4.0*HE_FRAC)/(2.0 + 3.0*HE_FRAC)     # = 0.55814


# --- Venzmer & Bothmer (2018) A&A 611 A36, Table 3 ------------------------
# Copied verbatim from m02_numbers.py, with the same citation.
# Combined Helios 1 + 2, solar distance range 0.29-0.98 au.
# Power law x(r) = d * r^e with r in au; d is the magnitude at 1 au.
# Parenthesised figures in the paper are errors on the last digits; they
# are expanded here.  "dse" is the yearly variation of the exponent, the
# weighted standard deviation over the yearly fits of their Fig. 9 --
# a more honest uncertainty than the formal fit error.
VB18 = {
    #              d_med   sd_med   e_med    se_med  d_avg  sd_avg  e_avg    se_avg  dse
    "density":    (5.61,   0.27,   -2.093,   0.046,  7.57,  0.30,  -2.010,   0.038,  0.072),
    "velocity":   (410.7,  2.8,     0.058,   0.013,  435.6, 2.4,    0.049,   0.010,  0.012),
    "temperature": (7.14e4, 0.23e4, -0.913,  0.039,  9.67e4, 0.21e4, -0.792,  0.028,  0.050),
    "bfield":     (5.377,  0.092,  -1.655,   0.017,  6.05,  0.10,  -1.546,   0.018,  0.11),
}
HELIOS_RMIN, HELIOS_RMAX = 0.29, 0.98      # au, Helios data range

# VB18 SECTION 6, page 11 (verified 2026-09-18 from the PDF; an earlier
# version of this comment said section 7, which is "Discussion and
# summary"), quoting Billings (1959) and Liebenberg et al. (1975), verbatim:
# "The extrapolated proton temperature increases from about 260 000 K at
# 0.25 au to about 1 690 000 K at 0.046 au ... and from 440 000 K to
# 2 860 000 K for a SSN of 200.  Knowing that near-Sun coronal temperatures
# are in the range of 2-3 MK (Billings 1959; Liebenberg et al. 1975), the
# model overestimates the extrapolated temperatures at the PSP perihelion
# distance."  This is a SECONDARY citation -- the two primary papers were
# not fetched -- and module09.html must say so, exactly as module01.html
# does for Maxwell (1867).
T_CORONA_LO, T_CORONA_HI = 2.0e6, 3.0e6     # K

# --- Verscharen, Bale & Velli (2021) MNRAS 506, 4993 ----------------------
# Radial mass flux per steradian F_m from Ulysses/SWOOPS, in the paper's
# units of au^2 g cm^-2 s^-1 sr^-1, so that the total mass-loss rate is
#     Mdot = 4 pi F_m AU^2.
# Their SECTION 3.1, "Mass, momentum, energy, and angular-momentum flux"
# (verified 2026-09-18; an earlier version of this comment said section 4),
# with F_m = r^2 N M U_r their eq. (13) and dF_m/dr = 0 their eq. (12):
# during solar minimum F_m is about 3.5e-16 over the POLAR
# regions (Fast Latitude Scan 1) and about 2.2e-16 during FLS3, while in
# the EQUATORIAL region (|latitude| < 20 deg) it varies between about
# 1e-16 and 15e-16.  Helios flew in the ecliptic, so the equatorial range
# is the one to compare a Helios-calibrated wind against; the polar FLS1
# value is quoted as the reference rung because 4 pi AU^2 times it is the
# familiar 1e12 g/s.
VBV21_FM_POLAR_FLS1 = 3.5e-16
VBV21_FM_POLAR_FLS3 = 2.2e-16
VBV21_FM_EQ_LO, VBV21_FM_EQ_HI = 1.0e-16, 15.0e-16
VBV21_FE_POLAR_FLS1 = 1.0        # au^2 g s^-3 sr^-1, radial energy flux

# --- Baumbach-Allen coronal electron density ------------------------------
# n_e(R) = 1e8 [1.55 R^-6 + 2.99 R^-16] cm^-3, R in solar radii, for the
# equatorial K corona.  Baumbach (1937); Allen (1947), MNRAS 107, 426; as
# tabulated in Allen, "Astrophysical Quantities".  NEITHER PRIMARY SOURCE
# WAS FETCHED for this module -- the formula is taken from standard
# secondary use and module09.html must carry a provenance note saying so.
# It is used as an INPUT to the mass-flux estimate, never as a check.
BA_C6, BA_C16 = 1.55, 2.99

# --- Sgr A*, CHECK 2 ------------------------------------------------------
# GRAVITY Collaboration (2022), A&A 657, L12, abstract: "a single central
# point mass, M = 4.30e6 M_sun, with a precision of about +/- 0.25%",
# distance R0 = 8277 pc.
SGRA_M_MSUN = 4.30e6
SGRA_M_RELERR = 0.0025
# Baganoff et al. (2003), ApJ 591, 891 (= arXiv:astro-ph/0102151), section
# 11.1.2, read verbatim: "The best-estimate ambient plasma conditions are
# ne ~ 130 cm^-3 and kTe ~ 2 keV; the corresponding emission measure
# EM ~ 2e3 cm^-6 pc, and the total mass of the plasma is ~2e-3 M_sun."
# "The sound speed is given by the equation cs = (gamma kT/mu m_H)^(1/2)
# ~ 670 km s^-1"; "we assume that the process is adiabatic (gamma = 5/3)
# and that the gas is fully ionized with twice solar abundances
# (mu ~ 0.70)"; "RB ~ 0.05 pc (1.3 arcsec)", and they adopt
# "RB = 0.06 pc (1.5 arcsec or 2e5 R_S)".  Their Bondi rate:
#   Mdot_B = 4 pi lambda (GM)^2 rho c_s^-3
#          ~ 3e-6 (ne/130 cm^-3)(kT/2 keV)^-3/2 M_sun/yr, lambda = 1/4.
# NOTE THE DENSITY CONVENTION: they write rho = ne mu m_H, i.e. mu is mass
# per PARTICLE multiplied by the ELECTRON density.  Mass per electron for
# this composition would be about 1.17 m_H, a factor 1.7 larger.  This
# script reproduces Baganoff's convention so that its number can be
# compared with theirs; PART H prints the alternative and shows it does not
# change the conclusion.
BAG_NE = 130.0          # cm^-3
BAG_KT_KEV = 2.0        # keV
BAG_MU = 0.70           # mass per particle in units of m_H, their value
BAG_GAMMA = 5.0/3.0
BAG_CS_PAPER = 6.7e7    # cm/s, their quoted ~670 km/s
BAG_RB_PAPER_PC = 0.05  # pc, their computed value
BAG_RB_ADOPTED_PC = 0.06  # pc, the outer radius they adopt
BAG_MDOT_PAPER = 3.0e-6   # M_sun/yr, their eq. in section 11.1.2
# Baganoff's Table 3 and abstract give the absorption-corrected 2-10 keV
# luminosity as (2.4 +3.0 -0.6)e33 erg/s, and the paper says it "is known
# only to within a factor of two".  The paper itself then rounds to
# ~2e33 throughout its discussion and in conclusion item 1, which is the
# figure used here; the range is carried so that nothing downstream is
# printed to more significant figures than it has.
BAG_LX = 2.0e33         # erg/s, the paper's own working figure
BAG_LX_LO, BAG_LX_HI = 1.8e33, 5.4e33   # erg/s, their Table 3 range
# Their local diffuse plasma, their SECTION 11.3, "Role of the Local Diffuse
# X-ray Medium" (verified 2026-09-18; an earlier version said section 12):
# kT ~ 1.3 keV, ne ~ 26 cm^-3, giving a Bondi-Hoyle rate ~1e-6 M_sun/yr if
# that gas is at rest.  Their 26 cm^-3 is an RMS electron density
# <n_e^2>^(1/2) at unity filling factor, from their section 7.
BAG_LOCAL_NE, BAG_LOCAL_KT_KEV, BAG_LOCAL_MDOT = 26.0, 1.3, 1.0e-6
# Marrone et al. (2007), ApJ 654, L57 (= arXiv:astro-ph/0611791), abstract
# and section 4, read verbatim: 10-epoch mean rotation measure
# (-5.6 +/- 0.7)e5 rad m^-2; "This rotation measure detection limits the
# accretion rate to less than 2e-7 M_sun/yr if the magnetic field is near
# equipartition, ordered, and largely radial, while a lower limit of
# 2e-9 M_sun/yr holds even for a sub-equipartition, disordered, or toroidal
# field."  Section 4: models with r_in between 30 and 100 Schwarzschild
# radii yield "upper limits for Mdot of 2e-7 to 5e-8 M_sun/yr"; taking
# r_in around 10 r_S or 3 r_S, "Mdot must be greater than 1-2e-8 M_sun/yr
# or 2-4e-9 M_sun/yr, respectively".
# TWO CONDITIONS ON THE UPPER LIMITS, verified 2026-09-18 and MISSING from
# an earlier version of this file.  Their section 4: "the assumptions of the
# M06 formalism ... are not constrained by existing observations.  In
# particular, the assumption of equipartition-strength fields cannot be
# justified observationally ... Magnetic fields that are a fraction epsilon
# of the equipartition strength will raise the accretion rate limits by
# epsilon^(-2/3) (a factor of 10 for epsilon = 3%)."  And for a reversed
# field with a small bias: "the accretion rate upper limits derived from our
# RM detection would no longer hold."  The LOWER limits are explicitly free
# of this: "these are not subject to the above caveats since the
# uncertainties act to raise the minimum accretion rate."  PART H prints the
# epsilon scaling, and module09.html must carry it with the factor of 40.
MAR_RM, MAR_RM_ERR = -5.6e5, 0.7e5     # rad m^-2
MAR_UPPER_HEAD = 2.0e-7     # M_sun/yr, r_in ~ 30 r_S
MAR_UPPER_TIGHT = 5.0e-8    # M_sun/yr, r_in ~ 100 r_S
MAR_LOWER_10RS = 1.5e-8     # M_sun/yr, midpoint of their 1-2e-8
MAR_LOWER_3RS = 3.0e-9      # M_sun/yr, midpoint of their 2-4e-9

# --- the coronal base, and the ceiling on an isothermal coronal temperature
# R0_BASE is the radius every wind in this file is launched from.
# T_BASE_SONIC is the temperature at which the Parker sonic radius
# r_c = GM/(2a^2) falls ON that base: above it the corona is supersonic from
# the base up and the model has no subsonic base to launch from.  It is
# computed once here because FOUR places need the same number -- PART F's
# scan, P8, PUNCHLINE 2 and the residual panel of m09_fig_parker.svg -- and
# a temperature ceiling stated in four places is a temperature ceiling that
# will disagree with itself.
R0_BASE = 1.03*Rsun
T_BASE_SONIC = GMsun*MU_WIND*mp/(2.0*kB*R0_BASE)      # = 6.26e6 K
T_SCAN_LO = 0.5e6       # K, the bottom of the isothermal scan in PART F

# --- problem-set inputs, all ASSUMED, none checked against anything -------
# Each needs a <span class="prov"> note in module09.html saying it is a
# representative value and not a measurement this module verified.
LIC_N = 0.2             # cm^-3, local interstellar cloud hydrogen density
LIC_T = 7.0e3           # K
LIC_MU = 0.6            # mass per particle: the cloud taken as FULLY IONISED.
#                         The local cloud is only partly ionised; neutral
#                         would give mu = 1.27 and c_s = 6.75 km/s instead of
#                         9.81.  Because v_rel^2 >> c_s^2 the rate moves by
#                         11 per cent, so the conclusion is unaffected -- but
#                         module09.html must state the assumption.
LIC_VREL = 2.6e6        # cm/s, the Sun's motion relative to the LIC
MC_N = 1.0e4            # cm^-3, dense molecular cloud TOTAL particle density
#                         (not the H2 density: reading it as H2 would raise
#                         rho by 20 per cent)
MC_T = 20.0             # K
MC_MU = 2.33            # mean molecular weight, H2 + He
BH_M_MSUN = 10.0        # M_sun, stellar-mass black hole
ETA_ACC = 0.1           # radiative efficiency assumed for the Eddington rate


# =========================================================================
# PART A.  Steady spherical flow: continuity and the critical point
# =========================================================================

def mass_flux(r, rho, v):
    """Mdot = 4 pi r^2 rho v, the constant of steady spherical continuity."""
    return 4.0*np.pi*r*r*rho*v


def sound_speed_iso(T, mu=MU_WIND):
    """Isothermal sound speed a = sqrt(kT/(mu m_p)) = sqrt(P/rho)."""
    return np.sqrt(kB*T/(mu*mp))


def sound_speed_adi(T, gamma, mu=MU_WIND):
    """Adiabatic sound speed c_s = sqrt(gamma k T/(mu m_p))."""
    return np.sqrt(gamma*kB*T/(mu*mp))


def dlnv_dlnr(r, v, cs2, GM=GMsun):
    """The critical-point equation, solved for the logarithmic slope.

        (v^2 - c_s^2) dln v/dln r = 2 c_s^2 - GM/r

    Derived in Proposition 2 of module09.html from steady continuity and
    the steady radial Euler equation with dP/dr = c_s^2 drho/dr.  IT NEEDS
    NO WIND MODEL: any steady, spherical, BAROTROPIC flow obeys it.

    NOTE WHICH EQUATION PART G3 USES.  Not this one.  G3 calls
    euler_slope_from_fits, which takes the pressure gradient from the
    MEASURED exponents and assumes no closure at all, barotropic or
    otherwise; it is steady radial Euler divided by v^2/r and nothing more.
    This function is used where a polytropic model has already been fixed
    (G5, and the PART B slopes), which is where barotropy holds by
    construction.
    """
    return (2.0*cs2 - GM/r)/(v*v - cs2)


def sonic_radius(cs2, GM=GMsun):
    """r_s = GM/(2 c_s^2), where the right side of the critical-point
    equation vanishes.  A solution that passes through v = c_s must do so
    here, or dv/dr is infinite."""
    return GM/(2.0*cs2)


def critical_slope_roots(gamma):
    """Roots of (gamma+1) s^2 + 4(gamma-1) s + (4 gamma - 6) = 0.

    s = dln v/dln r at the sonic point of a POLYTROPIC flow, P = K rho^gamma.
    Derivation, Proposition 5 of module09.html: differentiate the critical-
    point equation along ln r, use dln c_s^2/dln r = (gamma-1) dln rho/dln r
    and dln rho/dln r = -(s + 2) from continuity, and set v = c_s.

    The two facts this module uses:
      discriminant  16(gamma-1)^2 - 4(gamma+1)(4 gamma - 6) = 4(10 - 6 gamma)
        so the roots are real iff gamma <= 5/3;
      product of the roots  (4 gamma - 6)/(gamma + 1)
        so one root is POSITIVE -- an accelerating transonic solution --
        iff gamma < 3/2, the sum -4(gamma-1)/(gamma+1) being negative.
    Returns (s_plus, s_minus) with s_plus the larger, or (nan, nan) if the
    roots are complex.
    """
    a, b, cc = gamma + 1.0, 4.0*(gamma - 1.0), 4.0*gamma - 6.0
    disc = b*b - 4.0*a*cc
    # At gamma = 5/3 the discriminant 4(10 - 6 gamma) is EXACTLY zero and the
    # two roots are real and equal, both -1/2.  In IEEE doubles 5.0/3.0 makes
    # it -2.7e-15, and treating that as "complex" would print a complex pair
    # at the one gamma where the roots are real -- and would contradict the
    # sentence "the roots turn complex ABOVE gamma = 5/3" three lines below
    # the table.  Anything within rounding of zero is zero.
    if abs(disc) < 1e-9*max(1.0, b*b):
        disc = 0.0
    if disc < 0.0:
        return float('nan'), float('nan')
    rt = np.sqrt(disc)
    return (-b + rt)/(2.0*a), (-b - rt)/(2.0*a)


# =========================================================================
# PART B.  The isothermal wind: Parker's algebraic solution
# =========================================================================
# Integrating the critical-point equation for constant a gives
#
#     u^2 - 2 ln u = 4 ln x + 4/x + C,     u = v/a,  x = r/r_c,
#
# with r_c = GM/(2a^2).  Write h(u) = u^2 - 2 ln u; h has a single minimum
# h(1) = 1, so for a given right-hand side R there are two roots, one below
# u = 1 and one above, and they exist only where R >= 1.  The right-hand
# side R(x) = 4 ln x + 4/x + C has its own minimum at x = 1, of value
# 4 + C.  The transonic solutions are the case 4 + C = 1, i.e. C = -3.
# Everything about the topology follows from those two statements.

def _h(u):
    return u*u - 2.0*np.log(u)


def solve_h(rhs, branch):
    """Solve h(u) = u^2 - 2 ln u = rhs for u, by bisection.

    branch 'sub' returns the root with u < 1, 'sup' the root with u > 1.
    Returns nan if rhs < 1, where no real root exists.
    Bisection rather than Newton: h is flat near u = 1 and the subsonic
    root can be 1e-30, which Newton walks straight past.
    """
    if rhs < 1.0:
        return float('nan')
    if branch == 'sup':
        lo, hi = 1.0, 2.0
        while _h(hi) < rhs:
            hi *= 2.0
            if hi > 1e12:
                return float('nan')
    else:
        hi, lo = 1.0, 0.5
        while _h(lo) < rhs:
            lo *= 0.5
            if lo < 1e-300:
                return float('nan')
        lo, hi = lo, 1.0
    for _ in range(300):
        mid = 0.5*(lo + hi)
        if (_h(mid) < rhs) == (branch == 'sup'):
            lo = mid
        else:
            hi = mid
    return 0.5*(lo + hi)


def parker_u(x, branch='sup', C=-3.0):
    """u = v/a on the isothermal solution with constant C, at x = r/r_c.

    C = -3 is the transonic family: branch 'sup' with x > 1 is the WIND,
    branch 'sub' with x > 1 is the ACCRETION solution's mirror -- see
    parker_profile, which switches branch at the sonic point.
    """
    return solve_h(4.0*np.log(x) + 4.0/x + C, branch)


def parker_profile(x, kind='wind'):
    """The transonic isothermal solution, u(x), for an array of x = r/r_c.

    kind 'wind'      subsonic inside the sonic point, supersonic outside
    kind 'accretion' supersonic inside, subsonic outside
    kind 'breeze'    subsonic everywhere (C > -3; here C = -3 + 1, arbitrary)
    """
    x = np.atleast_1d(np.asarray(x, dtype=float))
    out = np.empty_like(x)
    for i, xi in enumerate(x):
        if kind == 'wind':
            br = 'sup' if xi >= 1.0 else 'sub'
            out[i] = parker_u(xi, br, -3.0)
        elif kind == 'accretion':
            br = 'sub' if xi >= 1.0 else 'sup'
            out[i] = parker_u(xi, br, -3.0)
        else:
            out[i] = parker_u(xi, 'sub', -2.0)
    return out


def parker_wind(r, T0, mu=MU_WIND, GM=GMsun):
    """Velocity of the transonic isothermal wind at radius r, in cm/s.

    r may be an array.  Returns (v, a, r_c).
    """
    a = sound_speed_iso(T0, mu)
    rc = sonic_radius(a*a, GM)
    x = np.atleast_1d(np.asarray(r, dtype=float))/rc
    u = parker_profile(x, 'wind')
    return a*u, a, rc


def parker_slope_local(r, T0, mu=MU_WIND, GM=GMsun):
    """dln v/dln r of the isothermal wind at r, from the critical-point eq."""
    v, a, _ = parker_wind(r, T0, mu, GM)
    return dlnv_dlnr(np.asarray(r, dtype=float), v, a*a, GM)


def parker_slope_chord(T0, r1=HELIOS_RMIN*AU, r2=HELIOS_RMAX*AU,
                       mu=MU_WIND, GM=GMsun):
    """The slope a power-law fit over [r1, r2] would return: the chord
    slope ln(v2/v1)/ln(r2/r1).  This is what VB18's beta actually is, so
    it, not the local slope, is the quantity to compare with beta."""
    v1 = parker_wind(r1, T0, mu, GM)[0][0]
    v2 = parker_wind(r2, T0, mu, GM)[0][0]
    return np.log(v2/v1)/np.log(r2/r1)


# =========================================================================
# PART C.  The polytropic wind
# =========================================================================
# For P = K rho^gamma the Bernoulli integral of the steady Euler equation is
#     v^2/2 + c_s^2/(gamma-1) - GM/r = E,
# and at the sonic point v = c_s = c_c with r_c = GM/(2 c_c^2), so
#     E = c_c^2 (5 - 3 gamma)/(2(gamma-1)).
# Launching from a base (r_0, v_0 ~ 0) with sound speed c_0 therefore fixes
#     c_c^2 = 2 [c_0^2 + (gamma-1) v_0^2/2 - (gamma-1) GM/r_0]/(5 - 3 gamma),
# which is POSITIVE only if c_0^2 > (gamma-1) GM/r_0.  That is the launch
# condition used in PART G4.

def poly_launch_Tmin(gamma, r0, mu=MU_WIND, GM=GMsun):
    """Minimum base temperature for a polytropic wind to exist at all.

    c_0^2 = gamma k T_0/(mu m_p) > (gamma-1) GM/r_0 gives
        T_0 > (gamma-1)/gamma * GM mu m_p/(k r_0).
    Below it the base enthalpy cannot pay the gravitational binding energy
    and the Bernoulli constant is negative, so no solution reaches infinity.
    """
    return (gamma - 1.0)/gamma * GM*mu*mp/(kB*r0)


def poly_cc2(gamma, T0, r0, mu=MU_WIND, GM=GMsun):
    """Sound speed squared at the sonic point, from the base conditions."""
    c02 = gamma*kB*T0/(mu*mp)
    return 2.0*(c02 - (gamma - 1.0)*GM/r0)/(5.0 - 3.0*gamma)


def poly_integrate(gamma, cc2, r_end, n=4000, GM=GMsun, inward=False):
    """Integrate the polytropic wind outward (or inward) from the sonic point.

    State variable is ln v against ln r, with

        dln v/dln r = (2 c_s^2 - GM/r)/(v^2 - c_s^2),
        c_s^2 = (gamma-1)(E + GM/r - v^2/2),      E from Bernoulli.

    Expressing c_s^2 through the Bernoulli constant rather than through
    the density avoids carrying rho, and it is exact.  The sonic point is
    a 0/0 point, so the integration starts one step away using the
    critical slope s_plus from critical_slope_roots.  Fourth-order
    Runge-Kutta in ln r.

    Returns (r, v).  For gamma >= 3/2 there is no positive critical slope
    and the function raises, which is itself the result PART D reports.
    """
    s_plus, _ = critical_slope_roots(gamma)
    if not np.isfinite(s_plus) or s_plus <= 0.0:
        sp, sm = critical_slope_roots(gamma)
        both = (f'{sp:+.4f} and {sm:+.4f}' if np.isfinite(sp)
                else 'complex')
        raise ValueError(
            f'gamma = {gamma}: no accelerating transonic solution, '
            f'critical slopes {both}')
    cc = np.sqrt(cc2)
    rc = GM/(2.0*cc2)
    E = cc2*(5.0 - 3.0*gamma)/(2.0*(gamma - 1.0))

    def deriv(lnr, lnv):
        r, v = np.exp(lnr), np.exp(lnv)
        cs2 = (gamma - 1.0)*(E + GM/r - 0.5*v*v)
        return (2.0*cs2 - GM/r)/(v*v - cs2)

    sgn = -1.0 if inward else 1.0
    eps = 1e-6
    lnr = np.log(rc) + sgn*eps
    lnv = np.log(cc) + s_plus*sgn*eps
    h = sgn*(np.log(r_end) - lnr)/abs(np.log(r_end) - lnr)*abs(
        np.log(r_end) - lnr)/n
    rs, vs = [np.exp(lnr)], [np.exp(lnv)]
    for _ in range(n):
        k1 = deriv(lnr, lnv)
        k2 = deriv(lnr + h/2, lnv + h*k1/2)
        k3 = deriv(lnr + h/2, lnv + h*k2/2)
        k4 = deriv(lnr + h, lnv + h*k3)
        lnv = lnv + h*(k1 + 2*k2 + 2*k3 + k4)/6.0
        lnr = lnr + h
        rs.append(np.exp(lnr))
        vs.append(np.exp(lnv))
    return np.array(rs), np.array(vs)


def poly_v_at(gamma, cc2, r, GM=GMsun):
    """Velocity of the polytropic wind at r, from the Bernoulli integral.

    Solve v^2/2 + (gamma-1)^-1 c_s^2(v) - GM/r = E for the supersonic root
    beyond the sonic point.  Using c_s^2 = (gamma-1)(E + GM/r - v^2/2) turns
    Bernoulli into an identity, so the density form is needed instead:
        c_s^2 = c_c^2 (rho/rho_c)^(gamma-1),  rho/rho_c = (v_c r_c^2)/(v r^2).
    """
    cc = np.sqrt(cc2)
    rc = GM/(2.0*cc2)
    E = cc2*(5.0 - 3.0*gamma)/(2.0*(gamma - 1.0))

    def f(v):
        cs2 = cc2*((cc*rc*rc)/(v*r*r))**(gamma - 1.0)
        return 0.5*v*v + cs2/(gamma - 1.0) - GM/r - E

    lo, hi = cc, cc
    while f(hi) < 0.0:
        hi *= 1.5
        if hi > 1e12:
            return float('nan')
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if f(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo + hi)


# =========================================================================
# PART D.  Bondi accretion
# =========================================================================

def bondi_lambda(gamma):
    """The Bondi eigenvalue lambda(gamma), derived in Proposition 7.

    Accretion from rest at infinity: Bernoulli gives, at the sonic point,
        c_s^2 = 2 c_inf^2/(5 - 3 gamma),   r_s = GM(5 - 3 gamma)/(4 c_inf^2),
    and rho_s/rho_inf = (c_s^2/c_inf^2)^(1/(gamma-1)).  Substituting into
    Mdot = 4 pi r_s^2 rho_s c_s gives

        lambda = [(5-3 gamma)/4]^2 [2/(5-3 gamma)]^((gamma+1)/(2(gamma-1))).

    lambda(5/3) = 1/4 exactly (the 0^2 and infinity^2 cancel), and
    lambda(1) = e^(3/2)/4 = 1.1201 in the limit.  Both are verified
    numerically in the report below.
    """
    if abs(gamma - 5.0/3.0) < 1e-12:
        return 0.25
    if abs(gamma - 1.0) < 1e-12:
        return np.exp(1.5)/4.0
    q = 5.0 - 3.0*gamma
    return (q/4.0)**2 * (2.0/q)**((gamma + 1.0)/(2.0*(gamma - 1.0)))


def bondi_rate(M, rho_inf, cs_inf, gamma):
    """Mdot = 4 pi lambda(gamma) rho_inf (GM)^2 / c_inf^3, in g/s."""
    return 4.0*np.pi*bondi_lambda(gamma)*rho_inf*(G*M)**2/cs_inf**3


def bondi_radius(M, cs_inf):
    """The Bondi radius as Baganoff et al. define it, R_B = 2GM/c_s^2.

    It is a LENGTH SCALE, not the location of the sonic point, and it is not
    the sonic radius of any flow: even for gamma = 1, where the sound speed
    is constant, the sonic point sits at GM/(2 c^2), which is R_B/4.  In
    general, from c_s^2(r_s) = 2 c_inf^2/(5-3 gamma) and r_s = GM/(2c_s^2),

        r_s = GM(5 - 3 gamma)/(4 c_inf^2) = R_B (5 - 3 gamma)/8,

    which is R_B/4 at gamma = 1 and zero at gamma = 5/3.
    """
    return 2.0*G*M/cs_inf**2


def bondi_hoyle_rate(M, rho_inf, cs_inf, v_rel, gamma=1.0):
    """Bondi-Hoyle-Lyttleton rate for an accretor moving at v_rel.

    Mdot = 4 pi lambda rho (GM)^2 (c_s^2 + v_rel^2)^(-3/2).  The
    interpolation in the denominator is the standard one and it is
    heuristic, not derived; module09.html must say so.
    """
    return 4.0*np.pi*bondi_lambda(gamma)*rho_inf*(G*M)**2 / \
        (cs_inf*cs_inf + v_rel*v_rel)**1.5


def eddington_luminosity(M):
    """L_Edd = 4 pi G M m_p c/sigma_T, for ionised hydrogen."""
    return 4.0*np.pi*G*M*mp*c/sigma_T


# =========================================================================
# PART E.  The VB18 fits as a solar-wind state at 1 au
# =========================================================================

def vb(key, which='avg'):
    """(amplitude, amplitude error, exponent, exponent error, yearly sigma)."""
    d_med, sd_med, e_med, se_med, d_avg, sd_avg, e_avg, se_avg, dse = VB18[key]
    if which == 'avg':
        return d_avg, sd_avg, e_avg, se_avg, dse
    return d_med, sd_med, e_med, se_med, dse


def gamma_eff(which='avg'):
    """Effective polytropic index from the measured exponents.

    T ~ rho^(gamma-1) with n ~ r^-alpha and T ~ r^e_T gives
        gamma - 1 = -e_T/(-alpha) = e_T/(-alpha) ... written out:
        gamma_eff = 1 + (-e_T)/alpha,  alpha = -e_n > 0, e_T < 0.
    Errors are propagated as independent, which they are not -- the two
    exponents come from the same spacecraft years -- so the quoted sigma is
    a lower bound on the true uncertainty.  Returns (gamma, sigma).
    """
    _, _, e_n, se_n, dse_n = vb('density', which)
    _, _, e_T, se_T, dse_T = vb('temperature', which)
    alpha, s_alpha = -e_n, se_n
    q = -e_T/alpha
    s_q = abs(q)*np.hypot(se_T/e_T, s_alpha/alpha)
    return 1.0 + q, s_q


def euler_slope_from_fits(which='avg', mu=MU_WIND, r=AU, GM=GMsun):
    """dln v/dln r at 1 au predicted by steady Euler from the VB18 fits.

    The critical-point equation with dP/dr taken from the MEASURED power
    laws, not from any closure:
        P = n_tot k T ~ r^(e_T - alpha),  so  -dln P/dln r = alpha - e_T,
        -(1/rho) dP/dr = (alpha - e_T) P/(rho r) = (alpha - e_T) c_T^2/r,
    with c_T^2 = P/rho = kT/(mu m_p).  Then

        dln v/dln r = [(alpha - e_T) c_T^2 - GM/r] / v^2

    exactly (the Eulerian form v dv/dr = -(1/rho)dP/dr - GM/r^2 divided by
    v^2/r), where v and T are the fitted 1-au amplitudes.

    ASSUMPTIONS, both of which module09.html must state.  (1) The single
    temperature T is applied to protons, alphas AND electrons.  VB18
    measured the PROTON temperature; at 1 au the electrons are hotter and
    fall off much more slowly, so this UNDERSTATES the pressure gradient.
    (2) The fits are power laws through ensemble medians, inserted into an
    equation that is nonlinear in v; <v^2> exceeds <v>^2 by of order the
    squared coefficient of variation.

    Returns (slope, sigma_slope) with sigma from a Monte Carlo over the
    four fitted quantities' formal errors.
    """
    d_v, sd_v, e_v, se_v, dse_v = vb('velocity', which)
    d_T, sd_T, e_T, se_T, _ = vb('temperature', which)
    d_n, sd_n, e_n, se_n, _ = vb('density', which)

    def s_of(dv, dT, en, eT):
        v = dv*1e5                       # km/s -> cm/s
        cT2 = kB*dT/(mu*mp)
        return ((-en - eT)*cT2 - GM/r)/(v*v)

    s0 = s_of(d_v, d_T, e_n, e_T)
    rng = np.random.default_rng(20260916)
    N = 40000
    samp = s_of(rng.normal(d_v, sd_v, N), rng.normal(d_T, sd_T, N),
                rng.normal(e_n, se_n, N), rng.normal(e_T, se_T, N))
    return s0, float(np.std(samp))


def n_proton_at(r_au, which='avg'):
    """Proton number density from the VB18 density fit, cm^-3."""
    d, _, e, _, _ = vb('density', which)
    return d*r_au**e


def rho_from_np(n_p):
    """Mass density from the proton density, with the module's composition."""
    return n_p*mp*(1.0 + 4.0*HE_FRAC)


def baumbach_allen_ne(R_over_Rsun):
    """Equatorial coronal electron density, cm^-3.  INPUT, not a check."""
    R = R_over_Rsun
    return 1e8*(BA_C6*R**-6.0 + BA_C16*R**-16.0)


def mdot_from_Fm(Fm):
    """Total mass-loss rate from Verscharen et al.'s per-steradian flux.

    F_m is quoted in au^2 g cm^-2 s^-1 sr^-1, meaning r^2 rho v with r
    measured in au; multiplying by AU^2 converts to g s^-1 sr^-1, and by
    4 pi to g/s.  This conversion is done here rather than quoted, because
    the paper states F_m and not the total.
    """
    return 4.0*np.pi*Fm*AU*AU


# =========================================================================
# Reporting
# =========================================================================

def main():
    P = print
    P('=' * 74)
    P('MODULE 9 NUMBERS: Bondi accretion and the Parker wind')
    P('=' * 74)
    P(f'  composition: He/H = {HE_FRAC} by number, fully ionised')
    P(f'  mu = rho/(n_tot m_p)              = {MU_WIND:.5f}')
    P(f'  M_sun = GM/G                      = {Msun:.5e} g')

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  Why a static corona is impossible (Parker 1958)')
    P('-'*74)
    r0 = R0_BASE
    for T0 in (1.0e6, 2.0e6, 3.0e6):
        a = sound_speed_iso(T0)
        rc = sonic_radius(a*a)
        # Hydrostatic isothermal atmosphere around a point mass:
        #   P(r) = P0 exp[-(GM mu m_p/k T)(1/r0 - 1/r)],
        # so P(infinity)/P0 = exp(-GM mu m_p/(k T r0)) = exp(-2 r_c/r0).
        ratio = np.exp(-2.0*rc/r0)
        P(f'  T_0 = {T0/1e6:.1f} MK: a = {a/1e5:6.1f} km/s, '
          f'r_c = {rc/Rsun:6.2f} R_sun, P(inf)/P(r_0) = {ratio:.3e}')
    # The coronal base pressure, for the comparison with the ISM.
    ne0 = baumbach_allen_ne(1.03)
    np0 = ne0/(1.0 + 2.0*HE_FRAC)
    ntot0 = np0*(2.0 + 3.0*HE_FRAC)
    P0 = ntot0*kB*2.0e6
    P(f'  Baumbach-Allen n_e(1.03 R_sun)     = {ne0:.3e} cm^-3')
    P(f'    -> n_p = {np0:.3e}, n_tot = {ntot0:.3e} cm^-3')
    P(f'    -> P_0 at 2 MK                   = {P0:.3e} dyn/cm^2')
    a2 = sound_speed_iso(2.0e6)
    rc2 = sonic_radius(a2*a2)
    P_inf = P0*np.exp(-2.0*rc2/r0)
    # A round interstellar thermal pressure, n ~ 1 cm^-3 at 1e4 K.  It is an
    # order-of-magnitude figure, not a measurement; the argument needs only
    # that it falls far below P(infinity).
    P_ism = 1.0*kB*1e4
    P(f'    -> P(infinity) of a STATIC 2 MK corona = {P_inf:.3e} dyn/cm^2')
    P(f'    -> a round interstellar pressure n k T = {P_ism:.3e} dyn/cm^2')
    P(f'    -> ratio                               = {P_inf/P_ism:.3e}')
    P('  READ: a hydrostatic isothermal corona does not fall to zero')
    P('  pressure at infinity, because 1/r is bounded.  It settles at a')
    P(f'  pressure {P_inf/P_ism:.0e} times the interstellar value, so the')
    P('  interstellar medium cannot confine it.  The corona must expand.')
    P('  The ISM pressure here is a round order-of-magnitude figure, not a')
    P('  measurement; the argument needs only that it is far below P(inf).')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  The isothermal solution topology')
    P('-'*74)
    P('  h(u) = u^2 - 2 ln u has its only minimum at u = 1, h(1) = 1.')
    P('  R(x) = 4 ln x + 4/x + C has its only minimum at x = 1, R(1) = 4+C.')
    P('  So a solution passes through u = 1 only if C = -3, and then only')
    P('  at x = 1.  Everything else follows:')
    P(f'    C = -3  and branch switching at x = 1 -> the transonic WIND '
      f'or the transonic ACCRETION solution')
    P(f'    C > -3  -> R(x) > 1 for all x: two branches that never meet,')
    P('               the BREEZE and the SUPERSONIC-EVERYWHERE solution')
    P(f'    C < -3  -> R(x) < 1 in a band about x = 1: no solution there,')
    P('               and two DOUBLE-VALUED families')
    P('  The six families are named, not numbered.  The Roman numerals')
    P('  I-VI in common use are the standard textbook presentation; Parker')
    P('  (1958) was fetched on 2026-09-18 and contains no such numbering,')
    P('  so nothing here cites one.')
    for C in (-3.0, -2.0, -4.0):
        xlo = 4.0*np.log(0.3) + 4.0/0.3 + C
        xhi = 4.0*np.log(5.0) + 4.0/5.0 + C
        P(f'    C = {C:+.1f}: R(1) = {4.0+C:+.2f}, R(0.3) = {xlo:.2f}, '
          f'R(5) = {xhi:.2f}')
    P('  Transonic wind, u(x) at a few x (C = -3, supersonic branch):')
    for x in (1.0, 2.0, 5.0, 10.0, 30.0, 100.0):
        u = parker_u(x, 'sup') if x > 1.0 else 1.0
        sl = 2.0*(1.0 - 1.0/x)/(u*u - 1.0) if x > 1.0 else 1.0
        P(f'    x = {x:6.1f}  u = {u:6.3f}  dln u/dln x = {sl:.4f}')
    P('  The breeze, same x, C = -2 (subsonic branch):')
    for x in (1.0, 2.0, 5.0, 10.0, 30.0, 100.0):
        u = parker_u(x, 'sub', -2.0)
        P(f'    x = {x:6.1f}  u = {u:.4e}')
    xb = np.array([30.0, 100.0])
    ub = np.array([parker_u(x, 'sub', -2.0) for x in xb])
    P(f'    breeze logarithmic slope between x = 30 and 100: '
      f'{np.log(ub[1]/ub[0])/np.log(xb[1]/xb[0]):.4f}')
    P('    -> the breeze decays as v ~ r^-2, so its exponent is negative.')
    P('    The SIGN of a measured velocity exponent therefore separates')
    P('    the wind from the breeze with no fitting at all.')
    P('  Asymptotics of the wind: u^2 -> 4 ln x, so v ~ a sqrt(4 ln r) and')
    P('  dln v/dln r -> 1/(2 ln x).  The slope falls only LOGARITHMICALLY,')
    P('  which is the fact that makes PART F\'s refutation unavoidable.')
    for x in (30.0, 1e3, 1e6):
        u = parker_u(x, 'sup')
        P(f'    x = {x:8.0e}  u = {u:7.3f}  2 sqrt(ln x) = '
          f'{2*np.sqrt(np.log(x)):7.3f}  1/(2 ln x) = {1/(2*np.log(x)):.4f}')

    # ---------------------------------------------------------------- C
    P('')
    P('PART C.  The polytropic critical point and the gamma < 3/2 bound')
    P('-'*74)
    P(f'  {"gamma":>7} {"s_plus":>10} {"s_minus":>10} {"product":>10} '
      f'{"transonic wind?":>18}')
    for g in (1.0, 1.1, 1.2, 1.3, 1.394, 1.4, 1.436, 1.49, 1.5, 1.55,
              1.6, 5.0/3.0, 1.7):
        sp, sm = critical_slope_roots(g)
        prod = (4.0*g - 6.0)/(g + 1.0)
        ok = 'yes' if (np.isfinite(sp) and sp > 0.0) else 'no'
        sps = f'{sp:10.4f}' if np.isfinite(sp) else f'{"complex":>10}'
        sms = f'{sm:10.4f}' if np.isfinite(sm) else f'{"complex":>10}'
        P(f'  {g:>7.4f} {sps} {sms} {prod:>10.4f} {ok:>18}')
    P('  gamma = 1 gives s = +1 and -1 exactly, the isothermal result.')
    P('  The discriminant is 4(10-6g): it vanishes AT gamma = 5/3, where the')
    P('  two roots coincide at -1/2, and the roots turn complex only ABOVE')
    P('  5/3.  They are both NEGATIVE for 3/2 < gamma <= 5/3, so a transonic')
    P('  solution exists there but decelerates: it is an accretion flow,')
    P('  not a wind.  gamma < 3/2 is the exact condition for a wind.')
    P('  Numerical confirmation by integrating the ODE from the sonic point.')
    P('  This is an EXISTENCE test for the integrator, not a model of the')
    P('  Sun: at this base temperature the sonic point falls BELOW the base,')
    P('  so no real corona could launch this particular solution.')
    T_demo = 6.0e6
    cc2_demo = poly_cc2(1.394, T_demo, R0_BASE)
    rr, vv = poly_integrate(1.394, cc2_demo, 3.0*AU)
    P(f'    gamma = 1.394, T_0 = {T_demo/1e6:.1f} MK at r_0 = 1.03 R_sun, '
      f'r_c = {GMsun/(2*cc2_demo)/Rsun:.3f} R_sun')
    P(f'    integrated to {rr[-1]/AU:.2f} au: '
      f'v rises from {vv[0]/1e5:.1f} to {vv[-1]/1e5:.1f} km/s')
    try:
        poly_integrate(1.6, 1e14, 3.0*AU)
        P('    gamma = 1.600: INTEGRATED -- this should not happen')
    except ValueError as exc:
        P(f'    {exc} -- the integrator refuses, as PART C predicts')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  Bondi accretion: verifying lambda(gamma)')
    P('-'*74)
    P(f'  {"gamma":>8} {"lambda":>12} {"r_s/R_B":>10}  note')
    for g, note in ((1.0, 'isothermal, e^(3/2)/4 = %.6f' % (np.exp(1.5)/4)),
                    (1.000001, 'numerical limit gamma -> 1'),
                    (1.1, ''), (1.2, ''), (1.3, ''), (1.4, 'exactly 5/8'),
                    (1.5, ''), (1.6, ''),
                    (5.0/3.0, 'adiabatic monatomic, exactly 1/4')):
        lam = bondi_lambda(g)
        rs_over_RB = (5.0 - 3.0*g)/8.0 if g < 5.0/3.0 else 0.0
        P(f'  {g:>8.6f} {lam:>12.6f} {rs_over_RB:>10.4f}  {note}')
    P(f'  isothermal exact e^(3/2)/4         = {np.exp(1.5)/4.0:.6f}')
    P(f'  gamma = 1.000001 from the formula  = {bondi_lambda(1.000001):.6f}')
    P(f'  ratio                              = '
      f'{bondi_lambda(1.000001)/(np.exp(1.5)/4.0):.6f}')
    P(f'  gamma = 1.4 exact 5/8              = {0.625:.6f}, '
      f'formula {bondi_lambda(1.4):.6f}')
    # Independent numerical check: build the transonic accretion solution
    # from scratch for gamma = 1.4 and read Mdot off it.
    g = 1.4
    Mtest, rho_inf, cs_inf = Msun, 1e-24, 1e6
    cs_s2 = 2.0*cs_inf**2/(5.0 - 3.0*g)
    r_s = G*Mtest/(2.0*cs_s2)
    rho_s = rho_inf*(cs_s2/cs_inf**2)**(1.0/(g - 1.0))
    Mdot_direct = 4.0*np.pi*r_s*r_s*rho_s*np.sqrt(cs_s2)
    Mdot_formula = bondi_rate(Mtest, rho_inf, cs_inf, g)
    P(f'  built from the sonic point:  Mdot = {Mdot_direct:.6e} g/s')
    P(f'  from 4 pi lambda rho (GM)^2/c^3:   {Mdot_formula:.6e} g/s')
    P(f'  ratio                              = '
      f'{Mdot_direct/Mdot_formula:.8f}')
    P('  The two agree to eight figures, so lambda is not a fitted number:')
    P('  it is the coefficient of the solution that passes through its own')
    P('  sonic point.  BUT SAY EXACTLY WHAT BONDI PROVED, because it is less')
    P('  than this module first claimed.  His Summary: "The factor of')
    P('  proportionality is NOT DETERMINED by the steady-state equations,')
    P('  though it is confined within certain limits.  Arguments are given')
    P('  suggesting that the case physically most likely to occur is that')
    P('  with the MAXIMUM rate of accretion."  His section 4 derives')
    P('  lambda <= lambda_c and his (19) reads "the accretion rate cannot')
    P('  exceed" 4 pi lambda_c (GM)^2 c^-3 rho_inf.  So the steady spherical')
    P('  equations BOUND the rate; selecting the transonic branch is Bondi\'s')
    P('  physical argument, not a consequence of the algebra.  PART H must')
    P('  not rest its refutation on "the algebra fixes lambda".')
    P('  Bondi\'s own Table I, read from the ADS scan, gives lambda_c =')
    P('  e^(3/2)/4 = 1.12 at gamma = 1, 0.625 at 1.4, 0.500 at 1.5 and')
    P('  0.250 at 5/3 -- four of its five entries legible, all four matching')
    P('  the table above.  The gamma = 1.2 entry is illegible in the scan,')
    P('  so the 0.871158 printed above is unchecked against the source.')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  The Parker wind for the Sun')
    P('-'*74)
    P(f'  base radius r_0 = 1.03 R_sun       = {r0:.4e} cm')
    P(f'  escape speed at r_0                = '
      f'{np.sqrt(2*GMsun/r0)/1e5:.1f} km/s')
    P(f'  {"T_0 [MK]":>9} {"a [km/s]":>9} {"r_c [R_sun]":>12} '
      f'{"r_c [au]":>10} {"v(0.29au)":>10} {"v(1au)":>9} {"chord beta":>11}')
    for T0 in (0.5e6, 1.0e6, 1.5e6, 2.0e6, 3.0e6):
        v, a, rc = parker_wind(np.array([HELIOS_RMIN*AU, AU]), T0)
        P(f'  {T0/1e6:>9.2f} {a/1e5:>9.1f} {rc/Rsun:>12.3f} '
          f'{rc/AU:>10.5f} {v[0]/1e5:>10.1f} {v[1]/1e5:>9.1f} '
          f'{parker_slope_chord(T0):>11.4f}')
    P('  Mass-loss rate of the isothermal wind, base density from the')
    P('  Baumbach-Allen formula (an INPUT with a provenance caveat):')
    rho0 = rho_from_np(np0)
    P(f'    rho(1.03 R_sun)                  = {rho0:.4e} g/cm^3')
    for T0 in (1.0e6, 1.5e6, 2.0e6):
        v0 = parker_wind(r0, T0)[0][0]
        md = mass_flux(r0, rho0, v0)
        P(f'    T_0 = {T0/1e6:.1f} MK: v(r_0) = {v0/1e2:8.2f} m/s, '
          f'Mdot = {md:.3e} g/s')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  Can ANY isothermal temperature give the measured slope?')
    P('-'*74)
    P('  The scan runs from 0.5 MK to the ceiling computed in P8: at')
    P(f'  T_0 = {T_BASE_SONIC/1e6:.2f} MK the sonic radius GM/(2a^2) falls ON')
    P('  the base r_0 = 1.03 R_sun, and above it the corona is supersonic')
    P('  from the base up, so the model has no subsonic base to launch from.')
    P('  The ceiling is part of the claim and is stated before the numbers.')
    Ts = np.linspace(T_SCAN_LO, T_BASE_SONIC, 121)
    chords = np.array([parker_slope_chord(T) for T in Ts])
    imin = int(np.argmin(chords))
    P(f'  scanning T_0 from {Ts[0]/1e6:.1f} to {Ts[-1]/1e6:.2f} MK, chord '
      f'slope over {HELIOS_RMIN}-{HELIOS_RMAX} au:')
    for T in (0.5e6, 1.0e6, 1.5e6, 2.0e6, 3.0e6, 4.0e6, 5.0e6, T_BASE_SONIC):
        P(f'    T_0 = {T/1e6:.2f} MK -> beta_pred = '
          f'{parker_slope_chord(T):.4f}')
    P(f'  minimum over the scan              = {chords[imin]:.4f} '
      f'at T_0 = {Ts[imin]/1e6:.2f} MK')
    d_v, sd_v, e_v, se_v, dse_v = vb('velocity', 'avg')
    P(f'  measured (VB18 mean fit)           = {e_v:.3f} +/- {se_v:.3f}')
    P(f'  smallest possible departure        = '
      f'{(chords[imin] - e_v)/se_v:.1f} sigma')
    P('  The slope falls only as 1/(2 ln(r/r_c)), so raising T_0 buys')
    P('  little: a factor of 10 in T_0 moves r_c by a factor of 10, but the')
    for T1 in (0.5e6, 1.0e6, 2.0e6, 5.0e6):
        b1, b2 = parker_slope_chord(T1), parker_slope_chord(10.0*T1)
        P(f'    slope only from {b1:.4f} to {b2:.4f} over '
          f'{T1/1e6:.1f} -> {10*T1/1e6:.0f} MK, a fall of '
          f'{100*(1-b2/b1):.0f} per cent')
    P('  So: NO isothermal temperature that leaves the corona subsonic at')
    P('  its base reproduces the measured acceleration.  That is the claim,')
    P('  and the ceiling is what makes it a claim rather than a scan.  The')
    P('  slope does keep falling above the ceiling, so state the price:')
    lo_T, hi_T = T_BASE_SONIC, 1.0e14
    for _ in range(200):
        mid = 0.5*(lo_T + hi_T)
        if parker_slope_chord(mid) > e_v:
            lo_T = mid
        else:
            hi_T = mid
    T_reach = 0.5*(lo_T + hi_T)
    P(f'    the T_0 that DOES reach {e_v:.3f} is {T_reach/1e6:.0f} MK,')
    P(f'    a factor {T_reach/T_CORONA_HI:.0f} to {T_reach/T_CORONA_LO:.0f} '
      f'above the measured 2-3 MK corona,')
    P(f'    and {T_reach/T_BASE_SONIC:.0f} times the temperature at which '
      f'the model breaks.')

    # ---------------------------------------------------------------- G
    P('')
    P('PART G.  CHECK 1 -- THE ANCHOR.  The wind against Helios')
    P('-'*74)
    P('  Source: Venzmer & Bothmer (2018), A&A 611, A36, Table 3.  Four')
    P('  exponents fitted INDEPENDENTLY to Helios 1+2 over 0.29-0.98 au,')
    P('  with no fluid equation imposed on the fit.')

    # --- G1: the confirmed inequality.
    P('')
    P('  G1.  CONFIRMED: gamma_eff lies inside the transonic window.')
    for which, label in (('avg', 'mean  '), ('med', 'median')):
        _, _, e_n, se_n, _ = vb('density', which)
        _, _, e_T, se_T, _ = vb('temperature', which)
        ge, sge = gamma_eff(which)
        P(f'    {label} fits: alpha = {-e_n:.3f} +/- {se_n:.3f}, '
          f'e_T = {e_T:.3f} +/- {se_T:.3f}')
        P(f'             gamma_eff = 1 + (-e_T)/alpha = {ge:.4f} '
          f'+/- {sge:.4f}')
        P(f'             below 3/2 by {(1.5-ge)/sge:.1f} sigma')
        P(f'             above 1 (isothermal) by {(ge-1.0)/sge:.1f} sigma')
        P(f'             below 5/3 (adiabatic) by {(5/3-ge)/sge:.1f} sigma')
        sp, sm = critical_slope_roots(ge)
        P(f'             critical slopes at that gamma: '
          f'{sp:+.4f}, {sm:+.4f}  -> accelerating wind exists')
    P('    PUNCHLINE ratio gamma_eff/(3/2)  = '
      f'{gamma_eff("avg")[0]/1.5:.4f} (mean), '
      f'{gamma_eff("med")[0]/1.5:.4f} (median)')
    P('    What this is: an INEQUALITY satisfied, not an equality met.  It')
    P('    is weaker than Module 2\'s alpha - beta = 2.  It also assumes a')
    P('    SINGLE polytropic index from the sonic point to 1 au, which G4')
    P('    shows is false.  Its force is that the bound 3/2 comes out of')
    P('    the critical-point quadratic alone, and the measured index had')
    P('    no reason to respect it.')

    # --- G2: the sign of beta.
    P('')
    P('  G2.  CONFIRMED: the sign of beta selects the wind over the breeze.')
    for which, label in (('avg', 'mean  '), ('med', 'median')):
        d, sd, e, se, dse = vb('velocity', which)
        P(f'    {label} fit: v = {d:.1f}({sd:.1f}) r^{e:+.3f}({se:.3f}) km/s')
        P(f'             beta > 0 by {e/se:.1f} sigma (formal), '
          f'{e/dse:.1f} sigma (yearly scatter)')
    P('    the breeze asymptote is beta = -2 (PART B), so the measurement')
    P('    sits 2.05 above it in a quantity whose formal error is 0.010.')
    P('    DO NOT TURN THAT INTO A SIGMA.  The -2 is the breeze\'s')
    P('    ASYMPTOTIC slope, and 0.29-0.98 au is not the asymptotic region;')
    P('    dividing 2.05 by 0.010 would state a 200-sigma result that the')
    P('    comparison does not support.  What the sign carries is the')
    P('    QUALITATIVE separation: a breeze decelerates and a wind')
    P('    accelerates, and the measured exponent is positive by the')
    P('    sigmas printed above, which are the ones to quote.')
    P('    A static corona has v = 0 and no exponent at all.')

    # --- G3: the direct Euler test.  The sharpest new result.
    P('')
    P('  G3.  THE SHARPEST RESULT: steady Euler against the measurement.')
    P('    The critical-point equation needs no wind model.  Feed it the')
    P('    measured pressure gradient at 1 au and compare with the')
    P('    measured acceleration.')
    for which, label in (('avg', 'mean  '), ('med', 'median')):
        d_v, sd_v, e_v, se_v, dse_v = vb('velocity', which)
        d_T, sd_T, e_T, se_T, _ = vb('temperature', which)
        d_n, sd_n, e_n, se_n, _ = vb('density', which)
        s_pred, s_err = euler_slope_from_fits(which)
        cT2 = kB*d_T/(MU_WIND*mp)
        v1 = d_v*1e5
        press = (-e_n - e_T)*cT2/(v1*v1)
        grav = GMsun/(AU*v1*v1)
        P(f'    {label} fits at 1 au: v = {d_v:.1f} km/s, T = {d_T:.3e} K, '
          f'n_p = {d_n:.2f} cm^-3')
        P(f'      -dln P/dln r = alpha - e_T  = {-e_n - e_T:.3f}')
        P(f'      c_T^2 = kT/(mu m_p)         = {cT2:.4e} cm^2/s^2 '
          f'(= ({np.sqrt(cT2)/1e5:.1f} km/s)^2)')
        P(f'      pressure term               = {press:+.5f}')
        P(f'      gravity term -GM/(r v^2)    = {-grav:+.5f}')
        P(f'      predicted dln v/dln r       = {s_pred:.5f} '
          f'+/- {s_err:.5f}')
        P(f'      measured beta               = {e_v:.3f} '
          f'+/- {se_v:.3f} (formal), +/- {dse_v:.3f} (yearly)')
        tot_f = np.hypot(se_v, s_err)
        tot_y = np.hypot(dse_v, s_err)
        P(f'      PUNCHLINE ratio measured/predicted = {e_v/s_pred:.2f}')
        P(f'      shortfall {(e_v - s_pred)/tot_f:.1f} sigma (formal), '
          f'{(e_v - s_pred)/tot_y:.1f} sigma (yearly scatter)')
    P('    The prediction\'s own error is small enough that it barely moves')
    P('    the sigma, which is the point of printing it.')
    P('    READ: proton thermal pressure supplies about one third of the')
    P('    measured acceleration at 1 au.  What this does NOT establish is')
    P('    what supplies the rest.  Two assumptions stand between this')
    P('    number and that conclusion: T_e = T_p = T_He (false at 1 au,')
    P('    and relaxing it RAISES the predicted pressure term), and power')
    P('    laws through ensemble medians used inside an equation that is')
    P('    nonlinear in v.  The honest statement is a shortfall, not a')
    P('    named force.')
    # The composition is this module's choice, not VB18's -- they treat the
    # wind as a pure proton plasma.  Show that using THEIR convention does
    # not rescue the prediction, so the reader can see it is unmoved.
    s0, e0 = euler_slope_from_fits('avg', mu=0.5)
    P('    AND THE COMPOSITION DOES NOT RESCUE IT.  VB18 treat the wind as')
    P('    a pure proton plasma (their section 1); this module chooses 5 per')
    P('    cent helium.  Redo the mean-fit prediction at mu = 1/2:')
    P(f'      c_T^2 rises by a factor {(1.0/0.5)/(1.0/MU_WIND):.4f} to '
      f'{kB*vb("temperature")[0]/(0.5*mp):.4e} cm^2/s^2')
    P(f'      predicted dln v/dln r       = {s0:.5f} +/- {e0:.5f}')
    P(f'      ratio measured/predicted    = {vb("velocity")[2]/s0:.2f}, '
      f'against {vb("velocity")[2]/euler_slope_from_fits("avg")[0]:.2f}')
    P(f'      shortfall {(vb("velocity")[2] - s0)/np.hypot(vb("velocity")[3], e0):.1f}'
      f' sigma (formal), against '
      f'{(vb("velocity")[2] - euler_slope_from_fits("avg")[0])/np.hypot(vb("velocity")[3], euler_slope_from_fits("avg")[1]):.1f}')
    P('      The composition is worth about 12 per cent in c_T^2 and moves')
    P('      the ratio by less than half a unit.  It is not the missing')
    P('      force either.')

    # --- G4: the isothermal refutation, three ways.
    P('')
    P('  G4.  REFUTED: the isothermal assumption, three ways.')
    _, _, e_T, se_T, dse_T = vb('temperature', 'avg')
    P(f'    (i)  measured e_T = {e_T:.3f} +/- {se_T:.3f} against the')
    P(f'         isothermal prediction 0: {abs(e_T)/se_T:.1f} sigma '
      f'(formal), {abs(e_T)/dse_T:.1f} sigma (yearly)')
    P('         Module 2 already reported the ADIABATIC closure failing at')
    P('         19.6 sigma against the same exponent; that result is cited')
    P('         in module09.html, not re-derived here.')
    P(f'    (ii) no isothermal T_0 reaches the measured slope: floor '
      f'{chords[imin]:.4f} against {vb("velocity")[2]:.3f} '
      f'+/- {vb("velocity")[3]:.3f}, '
      f'{(chords[imin]-vb("velocity")[2])/vb("velocity")[3]:.1f} sigma')
    # (iii) fit T_0 to the measured 1-au speed, then compare with the corona.
    d_v = vb('velocity', 'avg')[0]
    lo, hi = 0.2e6, 20.0e6
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if parker_wind(AU, mid)[0][0]/1e5 < d_v:
            lo = mid
        else:
            hi = mid
    T_fit = 0.5*(lo + hi)
    v_fit = parker_wind(AU, T_fit)[0][0]/1e5
    d_v_med = vb('velocity', 'med')[0]
    lo, hi = 0.2e6, 20.0e6
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if parker_wind(AU, mid)[0][0]/1e5 < d_v_med:
            lo = mid
        else:
            hi = mid
    T_fit_med = 0.5*(lo + hi)
    P(f'    (iii) T_0 FITTED so that v(1 au) = {d_v:.1f} km/s: '
      f'T_0 = {T_fit/1e6:.3f} MK')
    P(f'          check: that model gives v(1 au) = {v_fit:.1f} km/s')
    P(f'          same for the median fit {d_v_med:.1f} km/s: '
      f'T_0 = {T_fit_med/1e6:.3f} MK')
    P(f'          measured near-Sun corona {T_CORONA_LO/1e6:.0f}-'
      f'{T_CORONA_HI/1e6:.0f} MK (VB18 their Sect. 6, p. 11, citing')
    P('          Billings 1959 and')
    P('          Liebenberg et al. 1975 -- a SECONDARY citation)')
    P(f'          PUNCHLINE ratio T_corona/T_fitted = '
      f'{T_CORONA_LO/T_fit:.2f} to {T_CORONA_HI/T_fit:.2f}')
    P('          Fitting one parameter to one number confirms nothing.  The')
    P('          content is the DISAGREEMENT that follows: the temperature')
    P('          the isothermal model needs is 2 to 3 times below the')
    P('          temperature the corona is measured to have.  Put the')
    P('          measured 2-3 MK in instead and the wind overshoots:')
    for T0 in (2.0e6, 3.0e6):
        P(f'            T_0 = {T0/1e6:.0f} MK -> v(1 au) = '
          f'{parker_wind(AU, T0)[0][0]/1e5:.0f} km/s, ratio to measured '
          f'{parker_wind(AU, T0)[0][0]/1e5/d_v:.2f}')

    # --- G5: the single-polytrope model fails too.
    P('')
    P('  G5.  And the single-polytrope repair does not work either.')
    for which, label in (('avg', 'mean  '), ('med', 'median')):
        ge, sge = gamma_eff(which)
        Tmin = poly_launch_Tmin(ge, r0)
        P(f'    {label} gamma_eff = {ge:.4f}: minimum launch temperature at')
        P(f'             r_0 = 1.03 R_sun is T_0 > {Tmin/1e6:.3f} MK')
        P(f'             the measured corona is {T_CORONA_LO/1e6:.0f}-'
          f'{T_CORONA_HI/1e6:.0f} MK, so the requirement exceeds even the')
        P(f'             top of that range by a factor '
          f'{Tmin/T_CORONA_HI:.2f}, and its bottom by '
          f'{Tmin/T_CORONA_LO:.2f}')
    ge = gamma_eff('avg')[0]
    lo, hi = poly_launch_Tmin(ge, r0)*1.0000001, 40.0e6
    for _ in range(200):
        mid = 0.5*(lo + hi)
        cc2 = poly_cc2(ge, mid, r0)
        if poly_v_at(ge, cc2, AU)/1e5 < d_v:
            lo = mid
        else:
            hi = mid
    T_poly = 0.5*(lo + hi)
    cc2 = poly_cc2(ge, T_poly, r0)
    rc_poly = GMsun/(2.0*cc2)
    v_1au = poly_v_at(ge, cc2, AU)
    E_poly = cc2*(5.0 - 3.0*ge)/(2.0*(ge - 1.0))
    cs2_1au = (ge - 1.0)*(E_poly + GMsun/AU - 0.5*v_1au*v_1au)
    T_1au_poly = cs2_1au*MU_WIND*mp/(ge*kB)
    s_poly = dlnv_dlnr(AU, v_1au, cs2_1au)
    P(f'    Forcing gamma = {ge:.4f} to give v(1 au) = {d_v:.1f} km/s needs')
    P(f'      T_0                              = {T_poly/1e6:.2f} MK')
    P(f'      sonic radius r_c                 = {rc_poly/Rsun:.3f} R_sun')
    P(f'      T at 1 au from that solution     = {T_1au_poly:.3e} K')
    P(f'      measured T at 1 au               = {vb("temperature")[0]:.3e} K')
    P(f'      ratio                            = '
      f'{T_1au_poly/vb("temperature")[0]:.3f}')
    P(f'      dln v/dln r at 1 au              = {s_poly:+.5f}')
    P(f'      measured beta                    = {vb("velocity")[2]:+.3f} '
      f'+/- {vb("velocity")[3]:.3f}')
    P(f'      ratio measured/predicted         = '
      f'{vb("velocity")[2]/s_poly:.1f}')
    P('    Three failures at once, each computed above.  The base has to be')
    P(f'    at {T_poly/1e6:.2f} MK, above the measured 2-3 MK corona.  The '
      f'sonic radius')
    P(f'    comes out at {rc_poly/Rsun:.3f} R_sun, BELOW the base at 1.03 '
      f'R_sun, so the')
    P('    flow would be supersonic from the base up, which contradicts')
    P('    the model\'s own premise of a subsonic base.  No observed sonic')
    P('    radius is quoted here: none has been sourced for this module, and')
    P('    the contradiction is internal and needs none.  (Do not reach for')
    P('    the Alfven surface near 19 R_sun instead: it is a different')
    P('    surface.)  And the acceleration at 1 au is')
    P(f'    {s_poly:+.4f} against the measured {vb("velocity")[2]:+.3f}, '
      f'too small by a factor of {vb("velocity")[2]/s_poly:.0f}.')
    P('    The single-polytrope assumption is what fails: gamma is near 1')
    P('    low down, where the heat is deposited, and near 1.4 beyond')
    P('    0.3 au, so no one index describes both.')

    # --- G6: the mass flux.
    P('')
    P('  G6.  The mass flux, and why it is a WEAK test.')
    P(f'    Verscharen et al. (2021) F_m, converted by Mdot = 4 pi F_m au^2:')
    P(f'      polar solar min FLS1  F_m = {VBV21_FM_POLAR_FLS1:.1e} -> '
      f'{mdot_from_Fm(VBV21_FM_POLAR_FLS1):.3e} g/s')
    P(f'      polar solar min FLS3  F_m = {VBV21_FM_POLAR_FLS3:.1e} -> '
      f'{mdot_from_Fm(VBV21_FM_POLAR_FLS3):.3e} g/s')
    P(f'      EQUATORIAL range      F_m = {VBV21_FM_EQ_LO:.1e} to '
      f'{VBV21_FM_EQ_HI:.1e} -> {mdot_from_Fm(VBV21_FM_EQ_LO):.3e} to '
      f'{mdot_from_Fm(VBV21_FM_EQ_HI):.3e} g/s')
    P('      Helios flew in the ECLIPTIC, so the equatorial range is the')
    P('      one to compare against; the polar FLS1 rung is quoted because')
    P('      4 pi au^2 times it is the familiar 1e12 g/s.')
    P('    Cross-check from the VB18 fits themselves, which is independent')
    P('    of Ulysses:')
    np_1au = n_proton_at(1.0, 'avg')
    md_vb = mass_flux(AU, rho_from_np(np_1au), vb('velocity')[0]*1e5)
    P(f'      n_p(1 au) = {np_1au:.2f} cm^-3, v = {vb("velocity")[0]:.1f} '
      f'km/s -> Mdot = {md_vb:.3e} g/s')
    P(f'      that sits at F_m = {md_vb/(4*np.pi*AU*AU):.2e}, inside the')
    P('      equatorial range above.')
    P('    Now the Parker prediction with the Baumbach-Allen base density:')
    for T0 in (1.0e6, T_fit, 2.0e6):
        v0 = parker_wind(r0, T0)[0][0]
        md = mass_flux(r0, rho0, v0)
        P(f'      T_0 = {T0/1e6:.3f} MK -> Mdot = {md:.3e} g/s, ratio to '
          f'{mdot_from_Fm(VBV21_FM_POLAR_FLS1):.2e} g/s = '
          f'{md/mdot_from_Fm(VBV21_FM_POLAR_FLS1):.3f}')
    a_fit = sound_speed_iso(T_fit)
    rc_fit = sonic_radius(a_fit*a_fit)
    sens = 2.0*rc_fit/r0
    P(f'    SENSITIVITY: ln(v_0/a) = -(2 r_c/r_0) to leading order, so')
    P(f'      dln Mdot/dln T_0 ~ 2 r_c/r_0   = {sens:.1f}')
    P(f'      A factor of 3 in Mdot is therefore a {np.log(3.0)/sens*100:.1f}'
      f' per cent test of T_0.')
    P('      Agreement to a factor of a few here is NOT evidence that the')
    P('      model is right; it is evidence that the exponential was')
    P('      evaluated at roughly the right temperature.')
    P('    The inverse, which is the more honest direction:')
    for T0 in (1.0e6, 1.5e6, 2.0e6):
        v0 = parker_wind(r0, T0)[0][0]
        need_rho = mdot_from_Fm(VBV21_FM_POLAR_FLS1)/(4*np.pi*r0*r0*v0)
        need_ne = need_rho/(mp*(1+4*HE_FRAC))*(1+2*HE_FRAC)
        P(f'      T_0 = {T0/1e6:.1f} MK needs n_e(1.03 R_sun) = '
          f'{need_ne:.3e} cm^-3 (Baumbach-Allen gives {ne0:.3e})')

    # ---------------------------------------------------------------- H
    P('')
    P('PART H.  CHECK 2.  Bondi accretion onto Sgr A*')
    P('-'*74)
    M_sgra = SGRA_M_MSUN*Msun
    kT = BAG_KT_KEV*keV
    cs_sgra = np.sqrt(BAG_GAMMA*kT/(BAG_MU*mp))
    rho_sgra = BAG_NE*BAG_MU*mp
    P(f'  M (GRAVITY 2022)                   = {SGRA_M_MSUN:.2e} M_sun '
      f'+/- {SGRA_M_RELERR*100:.2f}% = {M_sgra:.4e} g')
    P(f'  n_e (Baganoff 2003 sec. 11.1.2)    = {BAG_NE:.0f} cm^-3')
    P(f'  kT                                 = {BAG_KT_KEV:.1f} keV '
      f'= {kT/kB:.3e} K')
    P(f'  mu (their value, mass per particle)= {BAG_MU:.2f}')
    P(f'  rho = n_e mu m_H (their convention)= {rho_sgra:.4e} g/cm^3')
    P(f'  c_s = sqrt(gamma kT/(mu m_H))      = {cs_sgra/1e5:.1f} km/s')
    P(f'    the paper quotes                 = {BAG_CS_PAPER/1e5:.0f} km/s, '
      f'ratio {cs_sgra/BAG_CS_PAPER:.4f}')
    R_B = bondi_radius(M_sgra, cs_sgra)
    P(f'  R_B = 2GM/c_s^2                    = {R_B/pc:.4f} pc')
    P(f'    the paper computes               = {BAG_RB_PAPER_PC:.2f} pc '
      f'at its own M; it adopts {BAG_RB_ADOPTED_PC:.2f} pc')
    # What M does the paper's own R_B imply?  A pipeline check.
    M_implied = BAG_RB_PAPER_PC*pc*BAG_CS_PAPER**2/(2.0*G)
    P(f'    their 0.05 pc and 670 km/s imply M = {M_implied/Msun:.2e} M_sun,')
    P('    which is the 2.6e6 M_sun standard in 2001.  Their Mdot must be')
    P('    rescaled by (M_new/M_old)^2 before it can be compared with ours.')
    rs_sgra = R_B*(5.0 - 3.0*BAG_GAMMA)/8.0
    P(f'  actual sonic radius r_s = R_B(5-3g)/8 = {rs_sgra/pc:.2e} pc  '
      f'(zero for gamma = 5/3 exactly: the adiabatic flow has no')
    P('    interior sonic point, which is why lambda is a limit)')
    Mdot_sgra = bondi_rate(M_sgra, rho_sgra, cs_sgra, BAG_GAMMA)
    Mdot_msun_yr = Mdot_sgra*yr/Msun
    P(f'  lambda(5/3)                        = {bondi_lambda(BAG_GAMMA):.4f}')
    P(f'  Mdot_Bondi                         = {Mdot_sgra:.4e} g/s')
    P(f'                                     = {Mdot_msun_yr:.3e} M_sun/yr')
    scaled = BAG_MDOT_PAPER*(SGRA_M_MSUN/(M_implied/Msun))**2
    P(f'  Baganoff\'s own value               = {BAG_MDOT_PAPER:.1e} M_sun/yr')
    P(f'    scaled to the GRAVITY mass by M^2 = {scaled:.2e} M_sun/yr')
    P(f'    ratio of that to ours            = {scaled/Mdot_msun_yr:.3f}')
    P('    This is a PIPELINE check: Baganoff computed their number from')
    P('    their own n_e and kT with this same formula, so agreement here')
    P('    confirms only that the formula is implemented identically.  It')
    P('    is not a test of nature.  The test is the next block.')
    # The alternative density convention.
    rho_alt = BAG_NE*mp*(1.0 + 4.0*0.1)/(1.0 + 2.0*0.1)
    P(f'  ALTERNATIVE convention, rho = n_e m_p (1+4y)/(1+2y) at y = 0.1')
    P(f'    (twice solar helium, mass per ELECTRON) = {rho_alt:.3e} g/cm^3, '
      f'a factor {rho_alt/rho_sgra:.2f}')
    P(f'    Mdot then                        = '
      f'{Mdot_msun_yr*rho_alt/rho_sgra:.2e} M_sun/yr -- the conclusion')
    P('    below moves by less than a factor of two and does not change.')
    P('')
    P('  THE COMPARISON.  Marrone et al. (2007), Faraday rotation:')
    P(f'    RM = ({MAR_RM/1e5:.1f} +/- {MAR_RM_ERR/1e5:.1f})e5 rad m^-2, '
      f'{abs(MAR_RM/MAR_RM_ERR):.1f} sigma from zero')
    for lab, val in (('upper limit, r_in ~ 30 r_S', MAR_UPPER_HEAD),
                     ('upper limit, r_in ~ 100 r_S', MAR_UPPER_TIGHT),
                     ('lower limit, r_in ~ 10 r_S', MAR_LOWER_10RS),
                     ('lower limit, r_in ~ 3 r_S', MAR_LOWER_3RS)):
        P(f'    {lab:<28} {val:.1e} M_sun/yr   '
          f'Bondi/this = {Mdot_msun_yr/val:8.1f}')
    P(f'    PUNCHLINE ratio against the headline bound = '
      f'{Mdot_msun_yr/MAR_UPPER_HEAD:.0f}')
    P(f'    range against the two upper bounds        = '
      f'{Mdot_msun_yr/MAR_UPPER_HEAD:.0f} to '
      f'{Mdot_msun_yr/MAR_UPPER_TIGHT:.0f}')
    P('')
    P('    CARRY THE CONDITION WITH THE NUMBER.  Marrone et al. state in')
    P('    their section 4 that "the assumptions of the M06 formalism ...')
    P('    are not constrained by existing observations.  In particular, the')
    P('    assumption of equipartition-strength fields cannot be justified')
    P('    observationally ... Magnetic fields that are a fraction epsilon of')
    P('    the equipartition strength will raise the accretion rate limits by')
    P('    epsilon^(-2/3) (a factor of 10 for epsilon = 3%)."  And if the')
    P('    field is reversed with a small bias, "the accretion rate upper')
    P('    limits derived from our RM detection would no longer hold".')
    for eps in (1.0, 0.1, 0.03):
        lim = MAR_UPPER_HEAD*eps**(-2.0/3.0)
        P(f'      epsilon = {eps:.2f}: upper limit {lim:.1e} M_sun/yr, '
          f'Bondi/this = {Mdot_msun_yr/lim:.0f}')
    P('    So the headline factor of 40 is the EQUIPARTITION number.  At 3')
    P('    per cent of equipartition it is 4.  The refutation does not rest')
    P('    on it alone -- the two legs below are independent of the field:')
    P('    Marrone\'s LOWER limits, which their section 4 says are "not')
    P('    subject to the above caveats since the uncertainties act to raise')
    P(f'    the minimum accretion rate" (ratios '
      f'{Mdot_msun_yr/MAR_LOWER_10RS:.0f} to '
      f'{Mdot_msun_yr/MAR_LOWER_3RS:.0f} above), and the X-ray radiative')
    P('    efficiency below.')
    P('')
    P('    REFUTED.  Note exactly what is refuted.  Not Bondi\'s algebra,')
    P('    which PART D verified to eight figures -- though note that PART D')
    P('    also records that Bondi\'s algebra does not by itself FIX lambda;')
    P('    it bounds it, and the transonic choice is his physical argument.')
    P('    What fails are its three physical premises, each of which Sgr A*')
    P('    violates:')
    P('      (1) no angular momentum -- the gas has some, and it')
    P('          circularises near 100 r_S rather than falling in;')
    P('      (2) no outflow -- the density profile is shallower than the')
    P('          r^-3/2 Bondi law, so Mdot falls with decreasing radius;')
    P('      (3) adiabatic and radiatively unimportant -- the flow is')
    P('          radiatively inefficient, which is the whole ADAF/CDAF')
    P('          literature Baganoff et al. section 11 reviews.')
    P('    The X-ray luminosity makes the same point independently:')
    eff = BAG_LX/(Mdot_sgra*c*c)
    P(f'      L_X (2-10 keV, Baganoff)        = {BAG_LX:.1e} erg/s')
    P(f'      Mdot_Bondi c^2                  = {Mdot_sgra*c*c:.3e} erg/s')
    P(f'      implied radiative efficiency    = {eff:.0e}')
    P(f'        (Baganoff give L_X = 2.4 +3.0/-0.6 e33 and say the 2-10 keV')
    P(f'         luminosity is "known only to within a factor of two", so')
    P(f'         this is one significant figure and no more: the range on')
    P(f'         L_X alone spans {BAG_LX_LO/(Mdot_sgra*c*c):.0e} to '
      f'{BAG_LX_HI/(Mdot_sgra*c*c):.0e})')
    P(f'      a thin disc would give ~0.1, a factor {0.1/eff:.0e} larger')
    P('  Local-ISM cross-check, Baganoff their Sect. 11.3: their diffuse '
      'plasma')
    kT_loc = BAG_LOCAL_KT_KEV*keV
    cs_loc = np.sqrt(BAG_GAMMA*kT_loc/(BAG_MU*mp))
    rho_loc = BAG_LOCAL_NE*BAG_MU*mp
    md_loc = bondi_rate(M_implied, rho_loc, cs_loc, BAG_GAMMA)*yr/Msun
    P(f'    kT = {BAG_LOCAL_KT_KEV} keV, n_e = {BAG_LOCAL_NE:.0f} cm^-3 at '
      f'their M: Mdot = {md_loc:.2e} M_sun/yr')
    P(f'    they quote ~{BAG_LOCAL_MDOT:.0e} M_sun/yr, ratio '
      f'{md_loc/BAG_LOCAL_MDOT:.2f}')

    # ---------------------------------------------------------------- I
    P('')
    P('PART I.  Problem-set numbers')
    P('-'*74)

    # P1. Bondi radius of the Sun in the local ISM.
    cs_lic = sound_speed_iso(LIC_T, LIC_MU)
    rho_lic = LIC_N*1.4*mp          # 1.4 for helium by mass, assumed
    rB_sun = 2.0*GMsun/(cs_lic**2 + LIC_VREL**2)
    md_sun = bondi_hoyle_rate(Msun, rho_lic, cs_lic, LIC_VREL, 1.0)
    P(f'  P1. Sun through the local ISM (ASSUMED n = {LIC_N} cm^-3, '
      f'T = {LIC_T:.0e} K, v = {LIC_VREL/1e5:.0f} km/s,')
    P(f'      mu = {LIC_MU} -- the cloud taken as FULLY IONISED; neutral '
      f'would give')
    P(f'      mu = 1.27 and c_s = '
      f'{sound_speed_iso(LIC_T, 1.27)/1e5:.2f} km/s, moving Mdot by '
      f'{100*abs((cs_lic**2+LIC_VREL**2)**1.5/((sound_speed_iso(LIC_T,1.27))**2+LIC_VREL**2)**1.5-1):.0f} per cent)')
    P(f'      c_s = {cs_lic/1e5:.2f} km/s, so motion dominates: '
      f'v/c_s = {LIC_VREL/cs_lic:.2f}')
    P(f'      R_B = 2GM/(c_s^2+v^2)          = {rB_sun:.3e} cm '
      f'= {rB_sun/AU:.1f} au')
    P(f'      Bondi-Hoyle Mdot               = {md_sun:.3e} g/s '
      f'= {md_sun*yr/Msun:.2e} M_sun/yr')
    md_wind = mdot_from_Fm(VBV21_FM_POLAR_FLS1)
    P(f'      compare the solar WIND, outward = {md_wind:.2e} g/s')
    P(f'      wind/accretion                 = {md_wind/md_sun:.0f}')
    P(f'      The Sun sheds mass {md_wind/md_sun:.0f} times faster than it')
    P('      gathers it, so its accretion is irrelevant to its mass budget.')
    P(f'      R_B = {rB_sun/AU:.1f} au also sits inside the heliosphere '
      f'(~120 au), so')
    P('      the interstellar gas never reaches that radius in any case.')

    # P2. 10 Msun black hole in a molecular cloud.
    M_bh = BH_M_MSUN*Msun
    cs_mc = sound_speed_iso(MC_T, MC_MU)
    rho_mc = MC_N*MC_MU*mp
    md_bh = bondi_rate(M_bh, rho_mc, cs_mc, 1.0)
    L_edd = eddington_luminosity(M_bh)
    md_edd = L_edd/(ETA_ACC*c*c)
    rB_bh = 2.0*G*M_bh/cs_mc**2
    P(f'  P2. 10 M_sun black hole in a molecular cloud (ASSUMED '
      f'n = {MC_N:.0e} cm^-3 TOTAL')
    P(f'      particle density, not H2; T = {MC_T:.0f} K, mu = {MC_MU}, so '
      f'rho = n mu m_p.  Reading n')
    P('      as the H2 density instead would raise rho by 20 per cent.)')
    P(f'      c_s (isothermal)               = {cs_mc/1e5:.4f} km/s')
    P(f'      lambda(1) = e^(3/2)/4          = {bondi_lambda(1.0):.4f}')
    P(f'      R_B = 2GM/c_s^2                = {rB_bh:.3e} cm '
      f'= {rB_bh/AU:.0f} au = {rB_bh/pc:.4f} pc')
    P(f'      Mdot                           = {md_bh:.3e} g/s '
      f'= {md_bh*yr/Msun:.3e} M_sun/yr')
    P(f'      L_Edd                          = {L_edd:.3e} erg/s')
    P(f'      Mdot_Edd at eta = {ETA_ACC}         = {md_edd:.3e} g/s')
    P(f'      Eddington ratio Mdot/Mdot_Edd  = {md_bh/md_edd:.3e}')
    P(f'      time to double its mass        = {M_bh/md_bh/yr:.2e} yr')

    # P3. Parker sonic point at 1 MK.
    a1 = sound_speed_iso(1.0e6)
    rc1 = sonic_radius(a1*a1)
    P(f'  P3. Parker sonic point at T_0 = 1 MK')
    P(f'      a                              = {a1/1e5:.2f} km/s')
    P(f'      r_c = GM/(2a^2)                = {rc1:.4e} cm '
      f'= {rc1/Rsun:.3f} R_sun = {rc1/AU:.5f} au')
    P(f'      escape speed at r_c            = '
      f'{np.sqrt(2*GMsun/rc1)/1e5:.1f} km/s = 2a, as it must be')
    P(f'      v(1 au)                        = '
      f'{parker_wind(AU, 1.0e6)[0][0]/1e5:.1f} km/s = '
      f'{parker_wind(AU, 1.0e6)[0][0]/a1:.2f} a')

    # P4. Kinetic energy flux of the wind.
    md_ref = mdot_from_Fm(VBV21_FM_POLAR_FLS1)
    v_1 = vb('velocity')[0]*1e5
    KE = 0.5*md_ref*v_1*v_1
    P(f'  P4. Kinetic energy flux of the solar wind (Mdot is Verscharen '
      f'et al.\'s')
    P('      POLAR rung and v is VB18\'s ECLIPTIC fit: an '
      'order-of-magnitude')
    P('      figure, not a matched pair)')
    P(f'      Mdot = {md_ref:.3e} g/s, v = {v_1/1e5:.1f} km/s')
    P(f'      (1/2) Mdot v^2                 = {KE:.4e} erg/s')
    P(f'      / L_sun                        = {KE/Lsun:.3e}')
    P(f'      gravitational term GM Mdot/R_sun= '
      f'{GMsun*md_ref/Rsun:.3e} erg/s = {GMsun*md_ref/(Rsun*Lsun):.2e} L_sun')
    P(f'      Verscharen F_E = {VBV21_FE_POLAR_FLS1} au^2 g s^-3 sr^-1 -> '
      f'{4*np.pi*VBV21_FE_POLAR_FLS1*AU*AU:.3e} erg/s = '
      f'{4*np.pi*VBV21_FE_POLAR_FLS1*AU*AU/Lsun:.2e} L_sun')

    # P5. A polytropic wind with gamma = 1.1.
    g11 = 1.1
    sp11, sm11 = critical_slope_roots(g11)
    Tmin11 = poly_launch_Tmin(g11, r0)
    cc2_11 = poly_cc2(g11, 2.0e6, r0)
    vinf11 = np.sqrt(cc2_11*(5.0 - 3.0*g11)/(g11 - 1.0))
    P(f'  P5. Polytropic wind with gamma = {g11}')
    P(f'      critical slopes                = {sp11:+.4f}, {sm11:+.4f}')
    P(f'      minimum launch T_0 at 1.03 R_sun= {Tmin11/1e6:.4f} MK')
    P(f'      at T_0 = 2 MK: c_c             = {np.sqrt(cc2_11)/1e5:.1f} km/s')
    P(f'                     r_c             = '
      f'{GMsun/(2*cc2_11)/Rsun:.3f} R_sun')
    P(f'                     v(infinity)     = {vinf11/1e5:.1f} km/s')
    P(f'                     v(1 au)         = '
      f'{poly_v_at(g11, cc2_11, AU)/1e5:.1f} km/s')
    P(f'      lambda for accretion at this gamma = {bondi_lambda(g11):.4f}')

    # P6. Time for the Sun to lose 1e-4 of its mass.
    dt = 1e-4*Msun/md_ref
    P(f'  P6. Time for the Sun to lose 1e-4 of its mass at '
      f'{md_ref:.2e} g/s')
    P(f'      t = 1e-4 M_sun/Mdot            = {dt:.4e} s = {dt/yr:.3e} yr')
    P(f'      compare the Sun\'s age 4.57e9 yr: ratio {dt/yr/4.57e9:.2f}')
    P(f'      mass lost over 4.57e9 yr at this rate = '
      f'{md_ref*4.57e9*yr/Msun:.2e} M_sun')

    # P7. Bondi-Hoyle velocity scaling.
    P(f'  P7. The v^-3 scaling of Bondi-Hoyle')
    for vr in (0.0, 0.5, 1.0, 2.0, 5.0):
        md = bondi_hoyle_rate(Msun, rho_lic, cs_lic, vr*cs_lic, 1.0)
        md0 = bondi_hoyle_rate(Msun, rho_lic, cs_lic, 0.0, 1.0)
        P(f'      v/c_s = {vr:4.1f}: Mdot/Mdot(0) = {md/md0:.4f} '
          f'(asymptote (1+v^2/c^2)^-3/2 = '
          f'{(1+vr*vr)**-1.5:.4f})')

    # P8. When does the sonic point reach the coronal base?
    # r_c = r_0 requires GM/(2a^2) = r_0, i.e. T = GM mu m_p/(2 k r_0).
    T_unbound = T_BASE_SONIC     # GM mu m_p/(2 k r_0), the PART F ceiling
    P(f'  P8. The temperature at which the sonic point reaches the base')
    P(f'      T such that r_c = 1.03 R_sun   = {T_unbound/1e6:.2f} MK')
    P(f'      = GM mu m_p/(2 k r_0); above it the corona is supersonic')
    P(f'      everywhere and there is no subsonic base.')
    P(f'      The measured corona, {T_CORONA_LO/1e6:.0f}-'
      f'{T_CORONA_HI/1e6:.0f} MK, is a factor {T_unbound/T_CORONA_HI:.1f} '
      f'to {T_unbound/T_CORONA_LO:.1f} below')
    P('      that, so the real base is comfortably subsonic.')

    # P9. Bondi radius of Sgr A* in Schwarzschild radii.
    rS = 2.0*G*M_sgra/(c*c)
    P(f'  P9. Sgr A* length scales')
    P(f'      Schwarzschild radius 2GM/c^2   = {rS:.4e} cm = {rS/AU:.3f} au')
    P(f'      R_B/r_S with the GRAVITY mass  = {R_B/rS:.3e}')
    P(f'      Baganoff adopt R_B = 0.06 pc and call it 2e5 r_S at their')
    P(f'      2.6e6 M_sun; at the GRAVITY mass 0.06 pc is '
      f'{BAG_RB_ADOPTED_PC*pc/rS:.2e} r_S')
    P(f'      free-fall time from R_B        = '
      f'{np.pi/2*np.sqrt(R_B**3/(2*G*M_sgra))/yr:.1f} yr')

    # P10. The Eddington ratio of Sgr A*.
    L_edd_sgra = eddington_luminosity(M_sgra)
    P(f'  P10. Sgr A* against Eddington')
    P(f'      L_Edd                          = {L_edd_sgra:.3e} erg/s')
    P(f'      L_X/L_Edd                      = {BAG_LX/L_edd_sgra:.2e}')
    P(f'      Mdot_Edd at eta = {ETA_ACC}         = '
      f'{L_edd_sgra/(ETA_ACC*c*c)*yr/Msun:.3e} M_sun/yr')
    P(f'      Mdot_Bondi/Mdot_Edd            = '
      f'{Mdot_sgra/(L_edd_sgra/(ETA_ACC*c*c)):.3e}')
    P(f'      Marrone upper bound/Mdot_Edd   = '
      f'{MAR_UPPER_HEAD*Msun/yr/(L_edd_sgra/(ETA_ACC*c*c)):.3e}')

    # ---------------------------------------------------------------- end
    P('')
    P('=' * 74)
    P('PUNCHLINES')
    P('=' * 74)
    ge_a, sge_a = gamma_eff('avg')
    ge_m, sge_m = gamma_eff('med')
    s_pred, s_err = euler_slope_from_fits('avg')
    d_v, sd_v, e_v, se_v, dse_v = vb('velocity', 'avg')
    P(f'  PUNCHLINE 1 (CONFIRMED).  A thermally driven wind can pass '
      f'through its')
    P(f'  sonic point and keep accelerating only if gamma < 3/2, a bound '
      f'that')
    P(f'  comes from the critical-point quadratic alone.  Venzmer & Bothmer')
    P(f'  (2018) Table 3 fitted the density and temperature exponents')
    P(f'  independently; they give gamma_eff = {ge_a:.3f} +/- {sge_a:.3f} '
      f'(mean fits) and')
    P(f'  {ge_m:.3f} +/- {sge_m:.3f} (median fits), which are '
      f'{(1.5-ge_a)/sge_a:.1f} and {(1.5-ge_m)/sge_m:.1f} sigma below 3/2.')
    P('')
    P(f'  PUNCHLINE 2 (REFUTED).  The same table kills the isothermal wind '
      f'three')
    P(f'  ways: the temperature exponent is {vb("temperature")[2]:.3f} '
      f'+/- {vb("temperature")[3]:.3f} against 0, a')
    P(f'  {abs(vb("temperature")[2])/vb("temperature")[3]:.1f} sigma '
      f'departure; no coronal temperature between 0.5 MK and the '
      f'{T_BASE_SONIC/1e6:.2f} MK at which')
    P(f'  the sonic point reaches the coronal base gives a velocity '
      f'exponent')
    P(f'  below {chords[imin]:.3f} over '
      f'0.29-0.98 au against the')
    P(f'  measured {e_v:.3f} +/- {se_v:.3f}, a floor '
      f'{(chords[imin]-e_v)/se_v:.0f} sigma too high; and the T_0 that')
    P(f'  reproduces the measured 1-au speed, {T_fit/1e6:.2f} MK, is a '
      f'factor {T_CORONA_LO/T_fit:.1f} to')
    P(f'  {T_CORONA_HI/T_fit:.1f} below the 2-3 MK corona that VB18 cite.')
    P('')
    P(f'  PUNCHLINE 3 (THE SHARPEST MEASUREMENT).  Steady Euler with the')
    P(f'  measured pressure gradient and no wind model predicts '
      f'dln v/dln r =')
    P(f'  {s_pred:.4f} +/- {s_err:.4f} at 1 au; the measured value is '
      f'{e_v:.3f} +/- {se_v:.3f}.  Proton')
    P(f'  thermal pressure supplies 1/{e_v/s_pred:.1f} of the observed '
      f'acceleration, a')
    P(f'  {(e_v-s_pred)/np.hypot(se_v, s_err):.1f} sigma shortfall against '
      f'the formal error and '
      f'{(e_v-s_pred)/np.hypot(dse_v, s_err):.1f} sigma against')
    P(f'  the year-to-year scatter.')
    P('')
    P(f'  PUNCHLINE 4 (REFUTED, LARGEST RATIO).  Bondi accretion onto Sgr '
      f'A* at')
    P(f'  M = {SGRA_M_MSUN:.2e} M_sun (GRAVITY 2022) with Baganoff et al.\'s '
      f'measured')
    P(f'  n_e = 130 cm^-3 and kT = 2 keV gives {Mdot_msun_yr:.2e} M_sun/yr. '
      f'Marrone et al.')
    P(f'  (2007) bound the actual rate to below {MAR_UPPER_HEAD:.0e} '
      f'M_sun/yr from Faraday')
    P(f'  rotation, and below {MAR_UPPER_TIGHT:.0e} for the steeper inner '
      f'radius.  The Bondi rate')
    P(f'  is too large by a factor of {Mdot_msun_yr/MAR_UPPER_HEAD:.0f} '
      f'to {Mdot_msun_yr/MAR_UPPER_TIGHT:.0f}.  Since the algebra checks to '
      f'eight')
    P(f'  figures, what fails is the physics assumed: no angular momentum, '
      f'no')
    P(f'  outflow, and an adiabatic radiatively unimportant flow.')

    P('')
    P('=' * 74)
    P('SOURCES')
    P('=' * 74)
    P('  Venzmer, M. S. & Bothmer, V. (2018), A&A 611, A36, "Solar-wind')
    P('    predictions for the Parker Solar Probe orbit".  arXiv:1711.07534.')
    P('    ALL OF THE BELOW READ FROM THE PDF, 2026-09-18.')
    P('    Table 3 (p. 8): power-law fits x(r) = d r^e to combined Helios')
    P('    1+2 data over 0.29-0.98 au, d the 1-au value.  Mean fits used')
    P('    here: n = 7.57(30) r^-2.010(38) cm^-3, v = 435.6(24) r^+0.049(10)')
    P('    km/s, T = 9.67(21)e4 r^-0.792(28) K.  Median fits:')
    P('    5.61(27) r^-2.093(46), 410.7(28) r^+0.058(13),')
    P('    7.14(23)e4 r^-0.913(39).  Yearly exponent scatter from their')
    P('    Fig. 9: 0.072 density, 0.012 velocity, 0.050 temperature.')
    P('    Their eq. (10), section 4: "x(r) = d . r^e ... with r being the')
    P('    solar distance in astronomical units, d the magnitude at 1 au".')
    P('    Section 6 (p. 11): "Knowing that near-Sun coronal temperatures')
    P('    are in the range of 2-3 MK (Billings 1959; Liebenberg et al.')
    P('    1975), the model overestimates the extrapolated temperatures at')
    P('    the PSP perihelion distance."  THE TWO PRIMARY PAPERS FOR THAT')
    P('    TEMPERATURE WERE NOT FETCHED; it is used here as a secondary')
    P('    citation and module09.html must say so.')
    P('    THE 5% HELIUM IS NOT THEIRS.  Their section 1 (p. 2): "In the')
    P('    analyses, we treat the solar wind as a proton plasma - the')
    P('    average helium abundance is about 4.5 % and in slow wind at solar')
    P('    cycle minimum is even less than 2 %."  The 5% sentence in their')
    P('    section 6 is about converting Leblanc et al. (1998) electron')
    P('    densities for Fig. 11.  This module chooses y = 0.05 itself.')
    P('  Verscharen, D., Bale, S. D. & Velli, M. (2021), MNRAS 506, 4993,')
    P('    "Flux conservation, radial scalings, Mach numbers, and critical')
    P('    distances in the solar wind".  arXiv:2107.06540.  Section 3.1 and')
    P('    Fig. 1: radial mass flux per steradian F_m = 3.5e-16 au^2 g')
    P('    cm^-2 s^-1 sr^-1 over the poles at solar minimum (FLS1),')
    P('    2.2e-16 (FLS3), and 1e-16 to 15e-16 in the equatorial region.')
    P('    Radial energy flux F_E about 1 au^2 g s^-3 sr^-1 over the poles.')
    P('    The total mass-loss rate 4 pi F_m au^2 is computed here, not')
    P('    quoted from the paper.')
    P('  Baganoff, F. K. et al. (2003), ApJ 591, 891, "Chandra X-ray')
    P('    Spectroscopic Imaging of Sgr A* and the Central Parsec of the')
    P('    Galaxy".  arXiv:astro-ph/0102151 (the only arXiv version; its')
    P('    journal reference is the 2003 paper).  Section 11.1.2:')
    P('    n_e ~ 130 cm^-3, kT_e ~ 2 keV, EM ~ 2e3 cm^-6 pc, plasma mass')
    P('    ~2e-3 M_sun, c_s ~ 670 km/s with gamma = 5/3 and mu ~ 0.70,')
    P('    R_B ~ 0.05 pc (1.3") with 0.06 pc adopted, and')
    P('    Mdot_B = 4 pi lambda (GM)^2 rho c_s^-3 ~ 3e-6 (n_e/130)')
    P('    (kT/2 keV)^-3/2 M_sun/yr with lambda = 1/4.  Their section 11.3:')
    P('    local')
    P('    diffuse plasma kT ~ 1.3 keV, n_e ~ 26 cm^-3, giving ~1e-6')
    P('    M_sun/yr.  Absorption-corrected 2-10 keV luminosity ~2e33 erg/s.')
    P('    NOTE: their 3e-6 M_sun/yr assumes M = 2.6e6 M_sun, which this')
    P('    script back-derives from their own R_B and c_s.')
    P('  Marrone, D. P., Moran, J. M., Zhao, J.-H. & Rao, R. (2007),')
    P('    ApJ 654, L57, "An Unambiguous Detection of Faraday Rotation in')
    P('    Sagittarius A*".  arXiv:astro-ph/0611791.  Abstract: 10-epoch')
    P('    mean RM = (-5.6 +/- 0.7)e5 rad m^-2; accretion rate "less than')
    P('    2e-7 M_sun/yr if the magnetic field is near equipartition,')
    P('    ordered, and largely radial", lower limit 2e-9 M_sun/yr')
    P('    otherwise.  Section 4: r_in between 30 and 100 r_S gives upper')
    P('    limits 2e-7 to 5e-8 M_sun/yr; r_in of 10 r_S or 3 r_S gives')
    P('    lower limits 1-2e-8 or 2-4e-9 M_sun/yr.')
    P('  GRAVITY Collaboration (2022), A&A 657, L12, "Mass distribution in')
    P('    the Galactic Center based on interferometric astrometry of')
    P('    multiple stellar orbits".  arXiv:2112.07478.  Abstract: a single')
    P('    central point mass M = 4.30e6 M_sun to about +/- 0.25%".  Their')
    P('    SECTION 4, not the abstract, gives R0 = (8277 +/- 9) pc.')
    P('  Parker, E. N. (1958), ApJ 128, 664, "Dynamics of the Interplanetary')
    P('    Gas and Magnetic Fields".  FETCHED 2026-09-18 from the ADS scan.')
    P('    His section II is PART A of this module: "Since we know of no')
    P('    general pressure at infinity which could balance the p(infinity)')
    P('    computed from equation (9) ... we conclude that probably it is')
    P('    not possible for the solar corona, or, indeed, perhaps the')
    P('    atmosphere of any star, to be in complete hydrostatic')
    P('    equilibrium out to large distances."  His own numbers, for a')
    P('    CONDUCTING (not isothermal) corona with N_0 = 3e7 cm^-3 and')
    P('    T_0 = 1.5e6 K: p_0 = 1.3e-2 dyn/cm^2, lambda = 5.35,')
    P('    p(inf) = 0.55e-3 p_0 = 0.6e-5 dyn/cm^2, against an interstellar')
    P('    1.4e-13 dyn/cm^2 from "10 hydrogen atoms/cm3 at 100 deg. K" --')
    P('    a ratio of 4.3e7.  PART A above gets 2.4e8 for an ISOTHERMAL')
    P('    2 MK corona with a Baumbach-Allen base and a ten-times-higher')
    P('    interstellar pressure.  Same argument, same conclusion, a factor')
    P('    5.5 apart for stated reasons.')
    P('    HE HAS NO CLASS I-VI NUMBERING.  The six-family classification')
    P('    labelled in m09_fig_topology.svg is the standard textbook')
    P('    presentation and is NOT cited to this paper.')
    P('  Bondi, H. (1952), MNRAS 112, 195, "On Spherically Symmetrical')
    P('    Accretion".  FETCHED 2026-09-18 from the ADS scan.  His Summary:')
    P('    "The factor of proportionality is not determined by the')
    P('    steady-state equations, though it is confined within certain')
    P('    limits.  Arguments are given suggesting that the case physically')
    P('    most likely to occur is that with the maximum rate of')
    P('    accretion."  His (18) gives lambda_c and his (19) says the rate')
    P('    "cannot exceed" 4 pi lambda_c (GM)^2 c^-3 rho_inf.  His Table I,')
    P('    four of five entries legible: e^(3/2)/4 = 1.12 at gamma = 1,')
    P('    0.625 at 1.4, 0.500 at 1.5, 0.250 at 5/3 -- all four match PART')
    P('    D.  The gamma = 1.2 entry is illegible in the scan.')
    P('  Allen, C. W. (1947), MNRAS 107, 426, "Interpretation of Electron')
    P('    Densities from Corona Brightness".  FETCHED 2026-09-18 from the')
    P('    ADS scan.  His section 4: "the electron density resulting from')
    P('    (2) is readily found to be: N(p) = 10^8(1.55 p^-6 + 2.99 p^-16)"')
    P('    -- the formula used above, coefficient for coefficient.  His')
    P('    paper exists to REMOVE Baumbach\'s third term, 0.0532 p^-2.5,')
    P('    which he identifies as the non-electron (F) corona.')
    P('    THE FIT RANGE IS p = 1.2 TO 2.6: "in the range p = 1.2 to 2.6,')
    P('    the intensity which is scattered by electrons follows the')
    P('    formula (2)".  This module evaluates it at p = 1.03, BELOW the')
    P('    fitted range and in the steep p^-16 term.  It is used only as an')
    P('    INPUT to a mass-flux estimate that PART G6 shows is a weak test,')
    P('    and module09.html must carry both caveats.')
    P('  IAU 2015 Resolution B3: nominal GM_sun, R_sun, L_sun.')
    P('  CODATA 2018: k_B, m_p, G, sigma_T, and the eV.')


if __name__ == '__main__':
    main()
