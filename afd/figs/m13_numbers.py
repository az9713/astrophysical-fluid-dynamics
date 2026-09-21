"""Module 13 numbers: radiation hydrodynamics.  The Eddington limit derived
rather than borrowed, radiation pressure and the gas fraction beta, the
opacity that sets both, optical depth and the photosphere, radiative
diffusion and the criterion Module 4 deferred by name, and the two places
where the book's own shipped numbers disagree with each other.

Every physical number quoted in module13.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

STEP 4 OF SIX; PARTS L AND M were added at step 4.  Every published value
this file compares against was read
off its page at step 2; the record is .ignore/m13-source-verification.md.
Step 2 also found that step 1's CHECK 4 read the n = 3 column of
module03.html, and that the ratio CHECK 4 was built to find is already in
print at module03.html:885.  Gate D (.ignore/m13-gate-d.md) has ruled on
all four checks; the block below is the ruled design.

WHAT THIS MODULE OWES, AND TO WHOM.  The twelve debts seven shipped pages
have already printed against Module 13 are listed, each with the file and
line it was read from, in .ignore/m13-promises.md.  FIVE LIVE
<a href="module13.html"> LINKS ARE DEAD UNTIL THIS MODULE EXISTS:
module09.html:847, :914, :915, :944 and module11.html:666.

The four debts that drive the design:

  module09.html:944   "L_Edd = 4 pi G M m_p c/sigma_T ... STATED, NOT
                      DERIVED; ... derived in Module 13."  PART A derives
                      it and must reproduce the eight numbers Module 9
                      prints from it.
  module09.html:915   "its m_p is a genuine proton mass and NOT a mean
                      molecular weight."  PART A prices that choice: it is
                      the pure-ionised-hydrogen opacity, and the book never
                      says so.
  module11.html:666   "the AGN configuration runs at A TENTH of Eddington."
                      PART A checks that claim against Module 11's own
                      printed Mdot.  It is exact, and PART A says by how
                      much it is exact.
  module04.html:429   "That criterion is NOT EVALUATED FOR THE SUN in this
                      module ... the size of the failure is a subject of
                      Module 13."  The criterion is omega chi/c^2 << 1.
                      PART D evaluates it.  This is the book's one
                      explicitly deferred COMPUTATION, and it is cheap.

THE FOUR CHECKS, WITH THE VERDICTS FIXED AT GATE D (step 3).

  CHECK 1  THE LIMIT, REPRODUCED, AND ITS COMPOSITION.  CONFIRMED as a
           reproduction: Module 9's five printed numbers to 0.03 per cent
           and Eddington's own Sun bound, k < 13,200 (p. 115), to 1.1 per
           cent.  The finding is the composition: m_p means X = 1.  At the
           protosolar X = 0.7261 the limit is 15.9 per cent higher.
  CHECK 2  THE ANCHOR.  THE PHOTOSPHERE AT tau = 2/3.  REFUTED: the
           one-scale-height inference from Module 6's rho and H is LOW by
           2.36 to 2.92 against ATLAS9's kappa_R.  ATLAS9 is a model.
  CHECK 3  module04.html:429's CRITERION.  REFUTED: omega chi/c^2 is
           0.3445 to 0.4468 at the photosphere, below 1 and not << 1.
  CHECK 4  EDDINGTON'S GREY ATMOSPHERE AGAINST ATLAS9's T(tau_R).
           CONFIRMED within 3.1 per cent in T (13 per cent in T^4) for
           tau_R = 0.01 to 3.  Replaces step 1's CHECK 4, which is Module
           3's result (module03.html:885) and is cited, not re-checked.
           Step 1's CHECK 3 (Sgr A*) is Module 9's refutation and is cited.

WHAT THE BOOK ALREADY CARRIES THAT THIS MODULE MAY NOT RE-RULE.
  - eta_rad: module09.html:944 fixes 0.1.  module11.html DERIVES 1/12 at
    the Schwarzschild ISCO and computes 0.057191 from Bardeen, Press &
    Teukolsky.  THE BOOK CARRIES THREE VALUES OF ONE SYMBOL.  PART A
    computes Mdot_Edd at all three and prints the spread.  RULED BY SIMON,
    2026-09-21: Mdot_Edd stays defined at eta_rad = 0.1, and no shipped
    page moves.
  - tau is the optical depth: module06.html:1054 already rules it.
  - a_rad is the radiation constant WITH its subscript: module03.html:904.
  - Bare eta is FORBIDDEN as a new meaning: module12.html:927 prints "a
    fourth bare meaning would carry no meaning at all".  The emissivity is
    written j_nu in this module.  No notation row in the book claims j.

NOTATION INSIDE THIS FILE.  kappa is an OPACITY here and nothing else; the
thermal conductivity of module01.html:758 does not occur.  nu is a FREQUENCY
here and never the kinematic viscosity, which does not occur either.  Both
are collisions with shipped pages and both are Gate D questions (Q3, Q4 of
.ignore/m13-promises.md).
"""

import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m11_numbers.py rather than imported, so that each
# module's numbers script reads on its own.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
me = 9.1093837015e-28   # g
mp = 1.67262192369e-24  # g
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
h_planck = 6.62607015e-27   # erg s      (exact, SI definition)
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
sigma_SB = 5.670374419e-5   # erg cm^-2 s^-1 K^-4  (exact, SI definition)
sigma_T = 6.6524587321e-25   # cm^2      (Thomson cross-section)
a_rad = 4.0*sigma_SB/c  # erg cm^-3 K^-4  (radiation constant)
pc = 3.0856775814913673e18   # cm
AU = 1.495978707e13     # cm
yr = 3.15576e7          # s

GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
Rsun = 6.957e10         # cm             (IAU 2015 nominal)
Lsun = 3.828e33         # erg/s          (IAU 2015 nominal)
Msun = GMsun/G          # g

# Composition.  X, Y, Z are mass fractions.  VERIFIED AT STEP 2: the
# present-day SURFACE of BS2005-AGS,OP, the model Module 3 tabulated --
# the last row of data/bs05_agsop.dat, which Bahcall, Serenelli & Basu
# (2005), ApJ 621, L85, Table 1 confirms as Ysurf = 0.229, Zsurf = 0.0126.
# module04.html's photospheric mu = 1.2250 is built from the same row, so
# the book already uses this composition at the photosphere.  Step 1 had
# the unsourced round pair 0.70/0.28; the change moves CHECK 1's ratio
# from 1.1765 to 1.1375.
X_H = 0.75830           # hydrogen mass fraction, bs05_agsop.dat last row
Y_HE = 0.22905          # helium mass fraction, same row
# The same model's INITIAL composition, 1 - Yi - Zi with Yi = 0.2599 and
# Zi = 0.0140 from BS05 Table 1.  Gate D rules it the X for ACCRETED gas,
# which has not had the Sun's helium settling.  CHECK 1 uses it.
X_INITIAL = 1.0 - 0.2599 - 0.0140

# =========================================================================
# WHAT THE BOOK ALREADY PRINTS.  Every one of these was read off the shipped
# file at the line named.  They are not inputs to a calculation; they are
# the TARGETS this module's PART A must reproduce.  A mismatch is a finding
# about a shipped page, not a fitting problem.
# =========================================================================

# --- module09.html:913, Problem K2 solution -----------------------------
M9_K2_M = 10.0*Msun             # a 10 Msun black hole
M9_K2_LEDD = 1.257e39           # erg/s      module09.html:913
M9_K2_MDOTEDD = 1.399e19        # g/s        module09.html:913, at eta=0.1
M9_K2_MDOT_BONDI = 5.124e22     # g/s        module09.html:913
M9_K2_RATIO = 3664.0            # Bondi/Eddington                :913
M9_K2_DOUBLING = 1.23e4*yr      # s          module09.html:913

# --- module09.html:921, Problem K3 solution -----------------------------
M9_K3_M = 4.30e6*Msun           # Sgr A*
M9_K3_LEDD = 5.405e44           # erg/s      module09.html:921
M9_K3_MDOTEDD = 9.545e-2        # Msun/yr    module09.html:921, at eta=0.1
M9_K3_LX_OVER_LEDD = 3.70e-12   # module09.html:921
M9_K3_MDOT_OVER_EDD = 8.405e-5  # Bondi, module09.html:921
M9_K3_MARRONE_OVER_EDD = 2.095e-6   # equipartition bound,       :921
M9_K3_DECADES = 7.4             # "7.4 orders of magnitude"      :921

# --- module09.html:847, the captures/misses row -------------------------
M9_SGRA_ETA_RAD = 4.0e-9        # "eta_rad ~= 4e-9 against 0.1"  :847

# --- module11.html:370 and :666, the AGN configuration ------------------
M11_AGN_M = 1.0e8*Msun          # module11.html:370
M11_AGN_MDOT = 1.3987e25        # g/s        module11.html:370
# module11.html:666 says in print that this "runs at A TENTH of Eddington".
M11_AGN_EDDINGTON_FRACTION = 0.10   # the claim to be checked

# --- module11.html, the efficiency the module DERIVES -------------------
M11_ETA_NEWTONIAN_ISCO = 1.0/12.0   # exactly 1/12 at 6 R_g
M11_ETA_RELATIVISTIC = 0.057191     # 1 - sqrt(8/9), Bardeen et al.
M9_ETA_ASSUMED = 0.1                # module09.html:944 fixes this

# --- module03.html:885, Problem K3 solution -----------------------------
M3_K_1MSUN = 3.8409e14          # cgs        module03.html:885
M3_MU = 0.832                   # module03.html:881
M3_RHS_1MSUN = 1.4329e-3        # the quartic's right side        :885
M3_ONE_MINUS_BETA_1MSUN = 1.4247e-3     # its root                :885

# --- module06.html:496-497, the solar photosphere -----------------------
# Module 6 computed these from a convection calculation that never
# mentions an opacity.  PART D turns them into one.
M6_PHOT_H = 142.9e5             # cm         module06.html:496, 142.9 km
M6_PHOT_RHO = 3.0631e-7         # g/cm^3     module06.html:497
M6_PHOT_CP = 1.6968e8           # erg/g/K    module06.html:498
M6_PHOT_MU = 1.225              # module04.html:316, the same atmosphere
M6_PHOT_G = 2.7398e4            # cm/s^2     module04.html:316
M6_TEFF = 5772.0                # K          module04.html:316
M6_PHOT_FLUX = 6.2939e10        # erg/cm^2/s module06.html:565
M6_PHOT_TAU = 2.0/3.0           # module06.html:1017, "photosphere, tau=2/3"

# --- module04.html:308 and :609, the deferred criterion -----------------
M4_NU_MAX = 3090.0e-6           # Hz         module04.html:308, 3090 microHz
M4_NU_AC = 4497.0e-6            # Hz         module04.html:611
M4_SOUND_SPEED = 8.081e5        # cm/s       module04.html:611

# --- module08.html:336, the radiating shock -----------------------------
M8_ISOTHERMAL_COMPRESSION = 2802.0      # module08.html:336

# =========================================================================
# PUBLISHED VALUES COMPARED AGAINST.  Each block names the paper, the table
# or equation, and what the quoted error means.  AT STEP 1 NOT ONE OF THEM
# HAS BEEN READ.  The tag is the instruction to step 2.
# =========================================================================

# --- Eddington, A. S. (1926), The Internal Constitution of the Stars ----
# The standard model and the quartic are his.  Module 3 already carries
# the quartic at module03.html:885 and credits him at :366.  This module
# needs his statement of the LIMIT, which is not in Module 3.
#     VERIFIED AT STEP 2, read off the rendered scan of the 1930 reprint
#     (whose preface says the text "has been reprinted unchanged" apart
#     from misprints).  Section 82, p. 115: from dp_G > 0 inward and his
#     (81.7), "k < 4 pi c G M/L < 25100 M/L", i.e. he states it as an
#     UPPER LIMIT ON THE OPACITY of a star of known L and M, "perfect gas
#     or not", and never as a limiting luminosity or with electron
#     scattering.  For the Sun he gets k < 13,200.  Eq. (83.4), p. 116,
#     is L = 4 pi c G M (1 - beta)/k_0.
EDDINGTON_1926_LIMIT_FORM = 'k < 4 pi c G M/L, sect. 82, p. 115'
EDDINGTON_1926_SUN_K_BOUND = 13200.0    # cm^2/g, p. 115

# --- the solar photospheric Rosseland mean opacity ----------------------
# CHECK 2 compares an INFERRED opacity against a tabulated one.  The
# candidates, in order of preference:
#   (a) OPAL (Iglesias & Rogers 1996, ApJ 464, 943) -- tables, not a
#       printed number at photospheric conditions.
#   (b) the Opacity Project (Badnell et al. 2005, MNRAS 360, 458).
#   (c) any stellar-structure text quoting kappa_R at T = 5772 K and
#       rho = 3e-7 g/cm^3.
# THE PHOTOSPHERE IS H-MINUS DOMINATED, not electron scattering, and the
# opacity there is a steep function of both T and rho.
#     VERIFIED AT STEP 2, and by a route that beats (a)-(c): a MODEL
#     ATMOSPHERE, which tabulates the Rosseland mean at every depth WITH
#     its T and P.  Castelli's ATLAS9 solar model, Teff = 5777 K,
#     log g = 4.4377, "NEW ODF ASPLUND ABUNDANCES" per the file's own
#     title card, fetched 2026-09-21 from
#     https://wwwuser.oats.inaf.it/castelli/sun/ap00t5777g44377k1asp.dat
#     and stored verbatim as data/castelli_atlas9_sun.dat.  Castelli &
#     Kurucz (2003), IAU Symp. 210, poster A20, describes the ATLAS9/ODF
#     method only; it does not contain this file.  Columns RHOX, T, P,
#     XNE, ABROSS.
#     atlas9_photosphere() integrates tau_R = int ABROSS d(RHOX) and reads
#     kappa_R off at tau_R = 2/3.  It is a MODEL, not a measurement, and
#     its opacities are ATLAS9's own ODFs, not OPAL.  Ferguson et al.
#     (2005), ApJ 623, 585, was read and prints NO value at photospheric
#     conditions -- its tables are a download.
ATLAS9_FILE = 'data/castelli_atlas9_sun.dat'

# --- a tabulated solar model, for CHECK 4 -------------------------------
# Module 3 used a tabulated model at module03.html:644-646 with
# rho_c = 76.293 g/cm^3 and T_c = 1.6233e7 K.  Those two numbers give
# 1 - beta directly and need no new source, but the MODEL does need one.
#     VERIFIED AT STEP 2.  The model is BS2005-AGS,OP (module03.html:620).
#     The paper does NOT print 1 - beta, rho_c or T_c; module03.html:628
#     computes 1 - beta_c = 6.1940e-4 from the first row of the data table,
#     as (9.1).
#     STEP 1 READ THE WRONG COLUMN.  76.293 and 1.6233e7 at
#     module03.html:644 and :646 are the n = 3 PREDICTION column, not the
#     tabulated model, so step 1's "1 - beta of the Sun" was Eddington's
#     polytrope checked against Eddington's polytrope.  Kept below under
#     their true name; the tabulated centre is the next three lines.
M3_N3_RHO_C = 76.293            # g/cm^3     module03.html:644, n=3 column
M3_N3_T_C = 1.6233e7            # K          module03.html:646, n=3 column
M3_RHO_C = 150.50               # g/cm^3     module03.html:620, tabulated
M3_T_C = 1.5480e7               # K          module03.html:620, tabulated
M3_P_C = 2.3380e17              # dyn/cm^2   module03.html:620, tabulated
M3_MU_C = 0.82851               # module03.html:624, effective, tabulated
M3_ONE_MINUS_BETA_C = 6.1940e-4         # module03.html:628, (9.1)
SOLAR_MODEL_SOURCE = 'BS2005-AGS,OP, ApJ 621, L85; data/bs05_agsop.dat'

# --- a super-Eddington source, for context ------------------------------
# Not a check at step 1.  If CHECK 1 or CHECK 3 needs an observed
# violation of the limit, the ultraluminous X-ray pulsars are the class.
#     NOT FETCHED AT STEP 2: optional, and no check needs it yet.  Gate D
#     decides whether CHECK 1 or CHECK 3 wants one.
ULX_SOURCE = None                       # NOT FETCHED

# --- Chandrasekhar (1939), Table 1, p. 59: Gamma_1 against 1 - beta ------
# Read off the rendered scan, three decimals as printed, gamma = 5/3.
CHANDRA_TABLE1_GAMMA1 = {
    0.0: 1.667, 0.1: 1.563, 0.2: 1.511, 0.3: 1.476, 0.4: 1.449,
    0.5: 1.426, 0.6: 1.405, 0.7: 1.386, 0.8: 1.368, 0.9: 1.350,
    1.0: 1.333}


# =========================================================================
# PART A.  The Eddington limit, derived
# =========================================================================

def kappa_electron_scattering(X=X_H):
    """kappa_es = sigma_T n_e/rho = (sigma_T/2 m_p)(1 + X), cm^2/g.

    A fully ionised gas of hydrogen mass fraction X and the rest helium
    has one free electron per proton and two per alpha particle, so
        n_e = (rho/m_p) X + 2 (rho/4 m_p)(1 - X) = (rho/2 m_p)(1 + X).
    Dividing by rho gives the mass opacity.  This is the ONLY opacity in
    astrophysics that contains no atomic physics: it is a cross-section
    and a book-keeping of electrons.

    At X = 1 this returns sigma_T/m_p, which is what Module 9's L_Edd
    assumes when it writes m_p.  module09.html:915 says the m_p is "a
    genuine proton mass and not a mean molecular weight" -- true, and it
    is also a COMPOSITION, namely pure ionised hydrogen, which that page
    does not say.
    """
    return sigma_T*(1.0 + X)/(2.0*mp)


def eddington_luminosity(M, kappa):
    """L_Edd = 4 pi G M c/kappa, erg/s.

    The derivation, which module09.html:944 says is owed to this module.
    A parcel of ionised gas at radius r from a source of luminosity L
    intercepts a radiative flux F = L/(4 pi r^2).  Radiation carries
    momentum F/c per unit area per unit time, and a mass dm of opacity
    kappa absorbs a fraction kappa dm of the flux crossing unit area, so
    the outward radiative force on it is kappa dm F/c.  The inward
    gravitational force is G M dm/r^2.  Both fall as 1/r^2, so the
    balance is independent of radius -- that is the whole content of the
    limit -- and setting them equal gives

        kappa L/(4 pi r^2 c) = G M/r^2   =>   L_Edd = 4 pi G M c/kappa.

    THE 1/r^2 CANCELLATION IS THE PROPOSITION.  Without it there would be
    a critical radius and not a critical luminosity.
    """
    return 4.0*np.pi*G*M*c/kappa


def eddington_luminosity_module9(M):
    """L_Edd = 4 pi G M m_p c/sigma_T, module09.html:944's exact form.

    Identical to eddington_luminosity(M, sigma_T/mp), i.e. to the general
    formula at X = 1.  Kept as its own function so that PART A can print
    the two side by side and name the composition the book never names.
    """
    return 4.0*np.pi*G*M*mp*c/sigma_T


def eddington_accretion_rate(M, eta_rad, kappa=None):
    """Mdot_Edd = L_Edd/(eta_rad c^2), g/s.

    module09.html:944's definition, with eta_rad the radiative efficiency
    L/(Mdot c^2).  The rate is NOT a property of the hole alone: it
    carries eta_rad, and the book prints three different values of that
    symbol.  Passing kappa=None uses Module 9's pure-hydrogen form.
    """
    L = eddington_luminosity_module9(M) if kappa is None \
        else eddington_luminosity(M, kappa)
    return L/(eta_rad*c*c)


def eddington_ratio(Mdot, M, eta_rad, kappa=None):
    """Mdot/Mdot_Edd, dimensionless."""
    return Mdot/eddington_accretion_rate(M, eta_rad, kappa)


def salpeter_time(eta_rad, kappa=None, M=Msun):
    """t_Sal = eta_rad c^2 kappa/(4 pi G c), the e-folding time of a hole
    accreting at exactly the Eddington rate, s.

    M dM/dt = Mdot_Edd = 4 pi G M c/(kappa eta_rad c^2) is linear in M,
    so the mass grows exponentially and the time is INDEPENDENT of M.
    That independence is why the number is worth printing at all.  The
    M argument is carried only to let the assert check the cancellation.
    """
    return M/eddington_accretion_rate(M, eta_rad, kappa)


# =========================================================================
# PART B.  Radiation pressure, the gas fraction, and gamma
# =========================================================================

def radiation_pressure(T):
    """P_rad = a_rad T^4/3, erg/cm^3.

    The third comes from the isotropy of the radiation field: the momentum
    flux through a surface is the energy density times <cos^2 theta>
    averaged over the sphere, which is 1/3.
    """
    return a_rad*T**4/3.0


def gas_pressure(rho, T, mu):
    """P_gas = rho k_B T/(mu m_u), erg/cm^3.  Module 3's (3.2)."""
    return rho*kB*T/(mu*mu_u)


def beta_gas_fraction(rho, T, mu):
    """beta = P_gas/P, module03.html:904's meaning exactly.

    Module 12's beta is the plasma beta and does not occur here.
    """
    Pg = gas_pressure(rho, T, mu)
    return Pg/(Pg + radiation_pressure(T))


def eddington_quartic_rhs(K, mu):
    """(1 - beta)/beta^4 = (a_rad/3)(mu m_u/k_B)^4 K^3.

    Module 3's (5.2) reads K = [3(1-beta)/(a_rad beta^4)]^(1/3)
    (k_B/(mu m_u))^(4/3).  Cubing and rearranging gives the line above.
    module03.html:885 prints the right side as 1.4329e-3 at 1 Msun with
    K = 3.8409e14 and mu = 0.832, and the root as 1 - beta = 1.4247e-3.
    Reproducing both is how PART B proves it inherited Module 3 correctly.
    """
    return (a_rad/3.0)*(mu*mu_u/kB)**4*K**3


def solve_one_minus_beta(rhs, tol=1.0e-15):
    """Solve (1-beta)/beta^4 = rhs for beta in (0,1), by bisection.

    module03.html:885: the left side decreases monotonically from +infinity
    to 0 as beta rises from 0 to 1, so the root is unique.  Returns 1-beta,
    which is the radiation share and the quantity Module 3 prints.
    """
    lo, hi = 1.0e-300, 1.0 - 1.0e-16
    for _ in range(400):
        mid = 0.5*(lo + hi)
        if (1.0 - mid)/mid**4 > rhs:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol*max(hi, 1.0e-300):
            break
    return 1.0 - 0.5*(lo + hi)


def gamma_effective(beta):
    """The effective adiabatic index of a gas-plus-radiation mixture.

    Chandrasekhar's Gamma_1 for a mixture, evaluated at the local beta
    (beta itself changes along an adiabat):
        Gamma_1 = beta + (4 - 3 beta)^2 (gamma_g - 1)
                         / [beta + 12(gamma_g - 1)(1 - beta)]
    with gamma_g = 5/3 for a monatomic gas.  The two limits are what
    module02.html:688 was promised: Gamma_1 -> 5/3 as beta -> 1 (pure gas)
    and Gamma_1 -> 4/3 as beta -> 0 (pure radiation).

    VERIFIED AT STEP 2 off the rendered scan: Chandrasekhar, An
    Introduction to the Study of Stellar Structure (Chicago, 1939),
    Chapter II, eq. (131), p. 57, derived from his (122), (127) and the
    definition (129) of beta.  He states both limits himself under it:
    Gamma_1 = gamma at beta = 1 and 4/3 at beta = 0.  His Table 1, p. 59,
    tabulates Gamma_1 for gamma = 5/3; CHANDRA_TABLE1_GAMMA1 is that
    column, and main() asserts this function reproduces all eleven rows.
    """
    gg = 5.0/3.0
    num = (4.0 - 3.0*beta)**2*(gg - 1.0)
    den = beta + 12.0*(gg - 1.0)*(1.0 - beta)
    return beta + num/den


# =========================================================================
# PART C.  Optical depth and the photosphere
# =========================================================================

def optical_depth(kappa, rho, length):
    """tau = kappa rho L, dimensionless.  The mean number of interactions a
    photon has crossing a slab of that column.

    module06.html:1054 already rules tau the optical depth in this book,
    "in tau = 2/3 only".  Module 13 takes the glyph over in full and the
    notation table names the four other tau in print: Module 1's collision
    time, Module 2's radial exponent, Module 4's acoustic radius and
    Module 12's Braginskii collision times.
    """
    return kappa*rho*length


def opacity_from_optical_depth(tau, rho, length):
    """kappa = tau/(rho L), the inverse of optical_depth.

    CHECK 2 uses this.  Module 6 computed rho and H at the solar
    photosphere from a CONVECTION calculation -- mixing length, the
    Schwarzschild criterion, a flux -- and never wrote an opacity.
    Demanding tau = 2/3 over one scale height turns its two numbers into
    an opacity, which can then be compared against a tabulated Rosseland
    mean.  Nothing in Module 6 knew about that comparison.
    """
    return tau/(rho*length)


def photon_mean_free_path(kappa, rho):
    """l_ph = 1/(kappa rho), cm.  Module 1's lambda is a PARTICLE mean free
    path and this is a photon's; the notation table must say so, because
    module10.html:1011 and module12.html:928 both fix bare lambda as
    Module 1's.  Written l_ph here and never bare lambda.
    """
    return 1.0/(kappa*rho)


def random_walk_steps(tau):
    """N = tau^2, the number of scatterings to cross an optically thick
    slab of optical depth tau.

    A photon taking N steps of length l in random directions covers a net
    distance l sqrt(N).  Setting l sqrt(N) = L = tau l gives N = tau^2.
    This is the whole reason a star is opaque in time as well as in
    intensity.
    """
    return tau*tau


def atlas9_profile():
    """The whole ATLAS9 column as arrays: (tau_R, T, P, rho, kappa_R, n_e,
    RHOX), top layer first.  Step 4 added it for Figs. 2 and 3, which need
    the profile and not one interpolated level; atlas9_photosphere() is
    built on it and returns exactly what it returned before.
    """
    import os
    import re
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                        ATLAS9_FILE)
    lines = open(path).read().splitlines()
    ab = {}
    for ln in lines:
        if 'ABUNDANCE CHANGE' in ln:
            for z, v in re.findall(r'(\d+)\s+(-?\d+\.\d+)',
                                   ln.split('CHANGE', 1)[1]):
                ab[int(z)] = float(v)
    mass = {1: 1.008, 2: 4.0026, 6: 12.011, 7: 14.007, 8: 15.999,
            10: 20.180, 11: 22.990, 12: 24.305, 13: 26.982, 14: 28.085,
            16: 32.06, 18: 39.95, 20: 40.078, 26: 55.845, 28: 58.693}
    frac = {z: (v if z <= 2 else 10.0**v) for z, v in ab.items()}
    mbar = (sum(f*mass.get(z, 2.0*z) for z, f in frac.items())
            / sum(frac.values()))
    i0 = next(i for i, ln in enumerate(lines) if ln.startswith('READ DECK6'))
    n = int(lines[i0].split()[2])
    rows = np.array([[float(x) for x in ln.split()[:5]]
                     for ln in lines[i0 + 1:i0 + 1 + n]])
    rhox, T, P, xne, kR = rows.T
    rho = (P/(kB*T) - xne)*mbar*mu_u
    tau = kR[0]*rhox[0] + np.concatenate(
        ([0.0], np.cumsum(0.5*(kR[1:] + kR[:-1])*np.diff(rhox))))
    return tau, T, P, rho, kR, xne, rhox


def atlas9_photosphere(tau_target=2.0/3.0, T_target=None):
    """Read the ATLAS9 solar model and return (T, P, rho, kappa_R, tau_R)
    at Rosseland optical depth tau_target, or at temperature T_target.

    tau_R = int ABROSS d(RHOX), starting from ABROSS RHOX at the top layer.
    ATLAS9 gives P and the electron density but not rho, so
        rho = (P/k_B T - n_e) m_bar,
    with m_bar the mean mass per nucleus from the file's own abundance
    cards (H and He as number fractions, Z >= 3 as log10 of them).
    Elements outside the mass table use A = 2Z; their share of m_bar is
    below 1e-4.  Interpolation is linear in log tau_R.
    """
    tau, T, P, rho, kR, xne, rhox = atlas9_profile()
    if T_target is None:
        x, xs = np.log(tau_target), np.log(tau)
    else:
        x, xs = T_target, T

    def at(y):
        return np.interp(x, xs, y)
    return (at(T), np.exp(at(np.log(P))), np.exp(at(np.log(rho))),
            np.exp(at(np.log(kR))), np.exp(at(np.log(tau))), rhox, P)


def grey_eddington_T(tau, Teff):
    """T(tau) = Teff [(3/4)(tau + 2/3)]^(1/4), K.  CHECK 4.

    The grey atmosphere under the Eddington closure K = J/3.  T = Teff at
    tau = 2/3 by construction, so the check at that level tests the grey
    assumption and nothing else.
    """
    return Teff*(0.75*(tau + 2.0/3.0))**0.25


def hopf_q(tau_out, tmax=30.0, n=3001):
    """The exact grey (Milne) solution's Hopf function q(tau).

    S = (3/4) F (tau + q) solves S = Lambda[S].  Because Lambda[tau] =
    tau + E3(tau)/2, q obeys q = Lambda[q] + E3/2, solved directly with
    Lambda integrated exactly over piecewise-constant cells and q held at
    q(inf) = 0.7104460 beyond tmax.  Its limits, q(0) = 1/sqrt(3) and
    q(inf), are the check.  Used only to show that the exact grey
    solution moves T at tau = 2/3 by under 0.5 per cent.
    """
    from scipy.special import expn
    t = np.linspace(0.0, tmax, n)
    dt = t[1] - t[0]
    edges = np.concatenate(([0.0], 0.5*(t[1:] + t[:-1]), [tmax + 0.5*dt]))

    def prim(ti, s):   # int E1(|ti - s|) ds, up to a constant
        d = s - ti
        return np.sign(d)*(1.0 - expn(2, np.abs(d)))
    ti = t[:, None]
    A = 0.5*(prim(ti, edges[None, 1:]) - prim(ti, edges[None, :-1]))
    q_inf = 0.7104460
    tail = 0.5*expn(2, edges[-1] - t)*q_inf
    src = 0.5*expn(3, t)
    # q = A q + tail + src, solved directly: Lambda iteration converges
    # too slowly at large tau to be worth running.
    q = np.linalg.solve(np.eye(n) - A, tail + src)
    return np.interp(tau_out, t, q)


# =========================================================================
# PART D.  Radiative diffusion, and the criterion Module 4 deferred
# =========================================================================

def radiative_flux_diffusion(kappa, rho, T, dTdz):
    """F = -(4 a_rad c T^3)/(3 kappa rho) dT/dz, erg/cm^2/s.

    Valid where the photon mean free path is short against the scale over
    which T changes -- i.e. where tau >> 1.  The bracket is the radiative
    conductivity; dividing it by rho c_P gives the diffusivity below.
    """
    return -(4.0*a_rad*c*T**3)/(3.0*kappa*rho)*dTdz


def radiative_diffusivity(kappa, rho, T, c_P):
    """chi = 16 sigma_SB T^3/(3 kappa rho^2 c_P), cm^2/s.

    module04.html:673 already calls chi the thermal diffusivity and
    module04.html:429 already calls it "the radiative diffusivity of the
    stellar gas".  Module 4 set the symbol up for this module and there is
    no collision to rule.

    The identity: 4 a_rad c = 16 sigma_SB, because a_rad = 4 sigma_SB/c.
    """
    return 16.0*sigma_SB*T**3/(3.0*kappa*rho**2*c_P)


def adiabaticity_parameter(omega, chi, c_sound):
    """omega chi/c^2, module04.html:429's criterion, dimensionless.

    Module 4 wrote: "By (3.4) it [the adiabatic assumption] requires
    omega chi/c^2 << 1 ... That criterion is NOT EVALUATED FOR THE SUN in
    this module ... the size of the failure is a subject of Module 13."

    Reading it: chi/c^2 is a time -- the time for heat to diffuse across a
    wavelength divided by the square of the sound speed -- and omega times
    a time is the number of radians of oscillation in it.  Small means the
    compression has no time to leak heat, which is what adiabatic means.
    """
    return omega*chi/(c_sound*c_sound)


def diffusion_time(kappa, rho, R):
    """t_diff = 3 kappa rho R^2/c, s -- the random-walk crossing time.

    From N = tau^2 steps of length l = 1/(kappa rho) at speed c:
        t = N l/c = tau^2/(kappa rho c) = kappa rho R^2/c,
    and the 3 is DERIVED, not sourced (Gate D): the diffusion flux above,
    F = -(c/(3 kappa rho)) dE/dz, makes the photon diffusivity
    D = c l/3, and t = R^2/D = 3 kappa rho R^2/c exactly.  It is the 1/3
    of module01.html:363's (1/3) rho v lambda.  R^2/D is itself an order
    of magnitude, and the module prints it as one.
    """
    return 3.0*kappa*rho*R*R/c


# =========================================================================
# PART E.  Where radiation takes over
# =========================================================================

def prad_equals_pgas_density(T, mu):
    """The density at which P_rad = P_gas, at fixed T.  g/cm^3.

    rho k_B T/(mu m_u) = a_rad T^4/3  =>  rho = a_rad mu m_u T^3/(3 k_B).
    Below this density radiation dominates the pressure.  Because it goes
    as T^3 while the gas term goes as rho T, the boundary in the (rho, T)
    plane is a line of slope 3 in the logs -- which is why radiation
    dominates in massive stars and not in the Sun.
    """
    return a_rad*mu*mu_u*T**3/(3.0*kB)


def eddington_ratio_of_a_star(M, L, kappa):
    """Gamma = L/L_Edd for a star.  Dimensionless.

    Gamma is the fraction of gravity that radiation already carries.  A
    star at Gamma = 1 cannot be in hydrostatic equilibrium at all, which
    is the statement Module 3 assumed away in its (3.1).
    """
    return L/eddington_luminosity(M, kappa)


# =========================================================================
# THE RUN
# =========================================================================

def main():
    P = print
    P('=' * 72)
    P('MODULE 13 NUMBERS -- radiation hydrodynamics.  STEP 4 OF SIX.')
    P('Gate D is .ignore/m13-gate-d.md.  Every published value below was')
    P('read at step 2; the record is')
    P('.ignore/m13-source-verification.md.  Every comparison against a')
    P('SHIPPED PAGE of this book is final, because the page is on disk.')
    P('=' * 72)

    # ------------------------------------------------------------------
    P('')
    P('PART A.  The Eddington limit, derived and checked against the book')
    P('-' * 72)

    kap_H = sigma_T/mp                  # pure ionised hydrogen
    kap_solar = kappa_electron_scattering(X_H)
    P('  kappa_es, pure ionised hydrogen (X = 1)   = %.5f cm^2/g' % kap_H)
    P('  kappa_es at X = %.4f                     = %.5f cm^2/g'
      % (X_H, kap_solar))
    P('  ratio                                      = %.5f'
      % (kap_H/kap_solar))
    P('  The conventional round number is 0.2(1+X) = %.4f cm^2/g,'
      % (0.2*(1.0 + X_H)))
    P('    which differs from the exact value by %.3f per cent.'
      % (100.0*abs(0.2*(1.0 + X_H) - kap_solar)/kap_solar))
    assert abs(kappa_electron_scattering(1.0) - kap_H) < 1e-12*kap_H, \
        'kappa_es at X=1 must be sigma_T/m_p, which is what Module 9 uses'

    # --- the two Module 9 problems, reproduced ------------------------
    P('')
    P('  MODULE 9 PROBLEM K2, module09.html:913, a 10 Msun hole:')
    L2 = eddington_luminosity_module9(M9_K2_M)
    P('    L_Edd computed  = %.6e erg/s' % L2)
    P('    L_Edd in print  = %.6e erg/s' % M9_K2_LEDD)
    P('    ratio           = %.6f' % (L2/M9_K2_LEDD))
    assert abs(L2/M9_K2_LEDD - 1.0) < 1.0e-3, \
        'module09.html:913 L_Edd does not reproduce'

    md2 = eddington_accretion_rate(M9_K2_M, M9_ETA_ASSUMED)
    P('    Mdot_Edd computed = %.6e g/s  (eta_rad = %.3f)'
      % (md2, M9_ETA_ASSUMED))
    P('    Mdot_Edd in print = %.6e g/s' % M9_K2_MDOTEDD)
    P('    ratio             = %.6f' % (md2/M9_K2_MDOTEDD))
    assert abs(md2/M9_K2_MDOTEDD - 1.0) < 1.0e-3, \
        'module09.html:913 Mdot_Edd does not reproduce'

    r2 = M9_K2_MDOT_BONDI/md2
    P('    Bondi/Eddington computed = %.1f' % r2)
    P('    in print                 = %.1f' % M9_K2_RATIO)
    P('    ratio                    = %.6f' % (r2/M9_K2_RATIO))
    assert abs(r2/M9_K2_RATIO - 1.0) < 2.0e-3, \
        'module09.html:913 Bondi/Eddington ratio does not reproduce'

    tdouble = M9_K2_M/M9_K2_MDOT_BONDI
    P('    M/Mdot at the Bondi rate = %.4e yr  (in print: %.2e yr)'
      % (tdouble/yr, M9_K2_DOUBLING/yr))
    P('    ratio                    = %.4f' % (tdouble/M9_K2_DOUBLING))
    # m09_numbers.py:1545 prints M_bh/md_bh as "time to double its mass".
    # That is exact AT CONSTANT Mdot, which is the reading the page takes.
    # It is NOT a defect.  What the page leaves unsaid is the growth law:
    #   constant Mdot       -> doubling = M/Mdot
    #   Mdot ~ M (Eddington) -> doubling = ln2 M/Mdot
    #   Mdot ~ M^2 (Bondi)   -> doubling = M/(2 Mdot)
    P('    That is the doubling time AT CONSTANT Mdot, as m09_numbers.py:1545')
    P('    computes it.  Bondi\'s Mdot grows as M^2, which halves it to')
    P('    %.4e yr; an Eddington-limited Mdot ~ M gives ln 2 of it,'
      % (0.5*tdouble/yr))
    P('    %.4e yr.  The page states no growth law.  Not a defect; a'
      % (np.log(2.0)*tdouble/yr))
    P('    sentence Module 13 may add when it discusses growth.')

    P('')
    P('  MODULE 9 PROBLEM K3, module09.html:921, Sgr A*:')
    L3 = eddington_luminosity_module9(M9_K3_M)
    P('    L_Edd computed  = %.6e erg/s   (in print %.6e)'
      % (L3, M9_K3_LEDD))
    P('    ratio           = %.6f' % (L3/M9_K3_LEDD))
    assert abs(L3/M9_K3_LEDD - 1.0) < 1.0e-3, \
        'module09.html:921 L_Edd does not reproduce'

    md3 = eddington_accretion_rate(M9_K3_M, M9_ETA_ASSUMED)/(Msun/yr)
    P('    Mdot_Edd computed = %.6e Msun/yr  (in print %.6e)'
      % (md3, M9_K3_MDOTEDD))
    P('    ratio             = %.6f' % (md3/M9_K3_MDOTEDD))
    assert abs(md3/M9_K3_MDOTEDD - 1.0) < 1.0e-3, \
        'module09.html:921 Mdot_Edd does not reproduce'

    gap = M9_K3_MDOT_OVER_EDD/M9_K3_LX_OVER_LEDD
    P('    (Mdot/Mdot_Edd)/(L_X/L_Edd) = %.4e = %.3f decades'
      % (gap, np.log10(gap)))
    P('    module09.html:921 prints %.1f orders of magnitude.'
      % M9_K3_DECADES)
    assert abs(np.log10(gap) - M9_K3_DECADES) < 0.1, \
        'module09.html:921 decade count does not reproduce'

    eta_implied = M9_ETA_ASSUMED*M9_K3_LX_OVER_LEDD/M9_K3_MDOT_OVER_EDD
    P('    The efficiency that gap implies = %.4e' % eta_implied)
    P('    module09.html:847 prints eta_rad ~= %.1e.' % M9_SGRA_ETA_RAD)
    P('    ratio = %.3f' % (eta_implied/M9_SGRA_ETA_RAD))
    assert abs(np.log10(eta_implied/M9_SGRA_ETA_RAD)) < 0.15, \
        'module09.html:847 eta_rad does not follow from :921 numbers'

    # --- the AGN tenth ------------------------------------------------
    P('')
    P('  MODULE 11 AGN CONFIGURATION, module11.html:370 and :666:')
    mdE_agn = eddington_accretion_rate(M11_AGN_M, M9_ETA_ASSUMED)
    frac = M11_AGN_MDOT/mdE_agn
    P('    Mdot_Edd(1e8 Msun, eta = 0.1) = %.6e g/s' % mdE_agn)
    P('    Module 11 prints Mdot          = %.6e g/s' % M11_AGN_MDOT)
    P('    fraction of Eddington          = %.6f' % frac)
    P('    module11.html:666 says "a tenth".  It is exact to %.3f per cent.'
      % (100.0*abs(frac - M11_AGN_EDDINGTON_FRACTION)
         / M11_AGN_EDDINGTON_FRACTION))
    assert abs(frac/M11_AGN_EDDINGTON_FRACTION - 1.0) < 1.0e-3, \
        'module11.html:666 "a tenth of Eddington" does not reproduce'

    # --- the three efficiencies ---------------------------------------
    P('')
    P('  THE BOOK CARRIES THREE VALUES OF eta_rad, AND Mdot_Edd CARRIES IT:')
    for label, eta in (('module09.html:944, assumed ', M9_ETA_ASSUMED),
                       ('module11, Newtonian 1/12  ', M11_ETA_NEWTONIAN_ISCO),
                       ('module11, Bardeen et al.  ', M11_ETA_RELATIVISTIC)):
        md = eddington_accretion_rate(M9_K2_M, eta)
        P('    %s eta = %.6f  Mdot_Edd = %.4e g/s  (%+.1f%% on print)'
          % (label, eta, md, 100.0*(md/M9_K2_MDOTEDD - 1.0)))
    P('    Against the computed 0.1 value, Module 11\'s 1/12 would move')
    P('    module09.html:913 by %+.1f per cent and the relativistic value'
      % (100.0*(M9_ETA_ASSUMED/M11_ETA_NEWTONIAN_ISCO - 1.0)))
    P('    by %+.1f; the table\'s +74.8 is against the rounded print.'
      % (100.0*(M9_ETA_ASSUMED/M11_ETA_RELATIVISTIC - 1.0)))
    P('    RULED BY SIMON, 2026-09-21 (Gate D Q2): Mdot_Edd stays defined')
    P('    at eta_rad = 0.1.  No shipped page moves; the module prints this')
    P('    table so the reader sees what the convention costs.')

    # --- CHECK 1 ------------------------------------------------------
    P('')
    P('  CHECK 1.  THE COMPOSITION INSIDE module09.html:944\'s FORMULA.')
    L_solar = eddington_luminosity(M9_K2_M, kap_solar)
    kap_init = kappa_electron_scattering(X_INITIAL)
    L_init = eddington_luminosity(M9_K2_M, kap_init)
    P('    L_Edd with kappa = sigma_T/m_p (X = 1)  = %.4e erg/s' % L2)
    P('    L_Edd at X = %.4f (BS05 initial)       = %.4e erg/s  ratio %.4f'
      % (X_INITIAL, L_init, L_init/L2))
    P('    L_Edd at X = %.4f (BS05 present surface) = %.4e erg/s  ratio %.4f'
      % (X_H, L_solar, L_solar/L2))
    P('    The limit scales as 2/(1+X): the m_p of module09.html:944 means')
    P('    X = 1, PURE IONISED HYDROGEN, and no shipped page says so.')
    P('    Gate D rules X = %.4f for accreted gas, so Module 9\'s value is'
      % X_INITIAL)
    P('    %.1f per cent BELOW the limit for protosolar gas.'
      % (100.0*(L_init/L2 - 1.0)))
    assert abs(L_init/L2 - 2.0/(1.0 + X_INITIAL)) < 1.0e-12, \
        'the composition factor must be exactly 2/(1+X)'
    assert L_init > L_solar > L2, \
        'a lower X must give a lower opacity and a HIGHER limit'
    eb = 4.0*np.pi*c*G*Msun/Lsun
    P('    Eddington\'s own Sun bound, p. 115: k < %.0f; recomputed %.0f,'
      % (EDDINGTON_1926_SUN_K_BOUND, eb))
    P('    ratio %.4f.  His 1926 L and M were not read; the %.1f per cent'
      % (eb/EDDINGTON_1926_SUN_K_BOUND,
         100.0*(1.0 - eb/EDDINGTON_1926_SUN_K_BOUND)))
    P('    is not traced.  CHECK 1 VERDICT: CONFIRMED as a reproduction.')
    assert abs(eb/EDDINGTON_1926_SUN_K_BOUND - 1.0) < 0.02, \
        'Eddington\'s p. 115 Sun bound does not reproduce to 2 per cent'

    # --- the Salpeter time --------------------------------------------
    P('')
    t_sal = salpeter_time(M9_ETA_ASSUMED)
    P('  Salpeter time at eta = %.2f, kappa = sigma_T/m_p: %.4e yr'
      % (M9_ETA_ASSUMED, t_sal/yr))
    t_sal_big = salpeter_time(M9_ETA_ASSUMED, M=1.0e8*Msun)
    P('  the same at 1e8 Msun                            : %.4e yr'
      % (t_sal_big/yr))
    P('  INDEPENDENT OF MASS, to %.2e relative -- which is the point.'
      % abs(t_sal_big/t_sal - 1.0))
    assert abs(t_sal_big/t_sal - 1.0) < 1.0e-12, \
        'the Salpeter time must not depend on M'
    # Gate D: the hole keeps (1 - eta) of what falls in, so the e-folding
    # time of M itself is t_Sal/(1 - eta).  The module prints this one.
    P('  the hole keeps (1 - eta) of Mdot, so M e-folds in t/(1 - eta)'
      ' = %.4e yr' % (t_sal/(1.0 - M9_ETA_ASSUMED)/yr))

    # ------------------------------------------------------------------
    P('')
    P('PART B.  Radiation pressure and the gas fraction')
    P('-' * 72)
    P('  a_rad = 4 sigma_SB/c = %.6e erg cm^-3 K^-4' % a_rad)

    rhs = eddington_quartic_rhs(M3_K_1MSUN, M3_MU)
    P('')
    P('  MODULE 3 PROBLEM K3, module03.html:885, at 1 Msun:')
    P('    quartic right side computed = %.6e' % rhs)
    P('    in print                    = %.6e' % M3_RHS_1MSUN)
    P('    ratio                       = %.6f' % (rhs/M3_RHS_1MSUN))
    assert abs(rhs/M3_RHS_1MSUN - 1.0) < 2.0e-3, \
        'module03.html:885 quartic right side does not reproduce'

    omb = solve_one_minus_beta(rhs)
    P('    1 - beta computed           = %.6e' % omb)
    P('    in print                    = %.6e' % M3_ONE_MINUS_BETA_1MSUN)
    P('    ratio                       = %.6f'
      % (omb/M3_ONE_MINUS_BETA_1MSUN))
    assert abs(omb/M3_ONE_MINUS_BETA_1MSUN - 1.0) < 2.0e-3, \
        'module03.html:885 root does not reproduce'
    # the solver must invert its own forward map
    beta_chk = 1.0 - omb
    assert abs((1.0 - beta_chk)/beta_chk**4/rhs - 1.0) < 1.0e-8, \
        'solve_one_minus_beta does not invert eddington_quartic_rhs'

    P('')
    P('  THE SUN\'S CENTRE, from Module 3\'s TABULATED model, BS2005-AGS,OP:')
    P('    rho_c = %.2f g/cm^3, T_c = %.4e K, P_c = %.4e  (module03.html:620)'
      % (M3_RHO_C, M3_T_C, M3_P_C))
    omb_c = radiation_pressure(M3_T_C)/M3_P_C
    P('    1 - beta_c = P_rad/P_c   = %.6e' % omb_c)
    P('    module03.html:628, (9.1) = %.6e' % M3_ONE_MINUS_BETA_C)
    P('    ratio                    = %.6f' % (omb_c/M3_ONE_MINUS_BETA_C))
    assert abs(omb_c/M3_ONE_MINUS_BETA_C - 1.0) < 1.0e-3, \
        'module03.html:628 (9.1) does not reproduce'
    b_c = beta_gas_fraction(M3_RHO_C, M3_T_C, M3_MU_C)
    P('    the same from rho_c, T_c at mu = %.5f  = %.6e  (ratio %.6f)'
      % (M3_MU_C, 1.0 - b_c, (1.0 - b_c)/omb_c))
    P('    Eddington\'s standard model, module03.html:885 = %.6e'
      % M3_ONE_MINUS_BETA_1MSUN)
    P('    standard model / tabulated Sun = %.4f'
      % (M3_ONE_MINUS_BETA_1MSUN/omb_c))
    P('    The standard model puts %.2f times the tabulated radiation'
      % (M3_ONE_MINUS_BETA_1MSUN/omb_c))
    P('    share at the Sun\'s centre.  Both numbers are in print, and SO')
    P('    IS THE RATIO: module03.html:885, Problem K3\'s solution, says')
    P('    "Eddington\'s 1 Msun value is 2.30 times the tabulated central')
    P('    value".  Gate D: CITED as Module 3\'s result, NOT a check here.')
    b_n3 = beta_gas_fraction(M3_N3_RHO_C, M3_N3_T_C, M3_MU)
    P('')
    P('    STEP 1\'s CHECK 4 read the n = 3 PREDICTION column of')
    P('    module03.html:644-646 as the Sun.  From it, 1 - beta = %.6e,'
      % (1.0 - b_n3))
    P('    which is %.4f of the standard model: Eddington against'
      % ((1.0 - b_n3)/M3_ONE_MINUS_BETA_1MSUN))
    P('    Eddington, a check that could not fail.  Kept here as the')
    P('    record of the defect, and never as a check.')

    P('')
    P('  gamma OF A GAS-PLUS-RADIATION MIXTURE, module02.html:688\'s debt:')
    for b in (1.0, 0.99, 0.9, 0.5, 0.1, 0.01, 1.0e-6):
        P('    beta = %-10.6g Gamma_1 = %.6f' % (b, gamma_effective(b)))
    P('    against Chandrasekhar (1939) Table 1, p. 59, three decimals:')
    worst = 0.0
    for omb_t, g_t in sorted(CHANDRA_TABLE1_GAMMA1.items()):
        g_c = gamma_effective(1.0 - omb_t)
        worst = max(worst, abs(g_c - g_t))
        P('      1 - beta = %.1f   computed %.4f   printed %.3f'
          % (omb_t, g_c, g_t))
    P('    largest difference = %.2e, inside the 5e-4 of a three-decimal'
      % worst)
    P('    table.  Eq. (131), p. 57, is the formula this file computes.')
    assert worst <= 5.0e-4 + 1.0e-12, \
        'gamma_effective does not reproduce Chandrasekhar Table 1'
    assert abs(gamma_effective(1.0) - 5.0/3.0) < 1.0e-12, \
        'the pure-gas limit of Gamma_1 must be 5/3'
    assert abs(gamma_effective(1.0e-12) - 4.0/3.0) < 1.0e-8, \
        'the pure-radiation limit of Gamma_1 must be 4/3'
    P('    THE TRIVIAL LIMITS ARE THE CHECK: beta -> 1 gives exactly 5/3')
    P('    and beta -> 0 gives exactly 4/3, which is what')
    P('    module02.html:688 was promised in print.')

    # ------------------------------------------------------------------
    P('')
    P('PART C.  Optical depth and the photosphere')
    P('-' * 72)
    P('  Module 6 computed the solar photosphere from CONVECTION and never')
    P('  wrote an opacity.  Demanding tau = 2/3 over one scale height')
    P('  turns its two numbers into one.')
    P('    H   = %.4e cm   (module06.html:496)' % M6_PHOT_H)
    P('    rho = %.4e g/cm^3 (module06.html:497)' % M6_PHOT_RHO)
    kap_inferred = opacity_from_optical_depth(M6_PHOT_TAU, M6_PHOT_RHO,
                                              M6_PHOT_H)
    P('    kappa inferred at tau = 2/3 over one H = %.5f cm^2/g'
      % kap_inferred)
    P('    electron scattering at X = %.4f would be %.5f cm^2/g,'
      % (X_H, kap_solar))
    P('    which is %.2f times larger.  The photosphere is NOT'
      % (kap_solar/kap_inferred))
    P('    electron-scattering dominated, and this is the arithmetic')
    P('    that says so: it is H-minus, and H-minus is atomic physics')
    P('    this book does not do.')
    assert kap_inferred < kap_solar, \
        'the inferred photospheric opacity must be below electron scattering'

    P('')
    P('    THE TABULATED TARGET: Castelli\'s ATLAS9 solar model, %s' %
      ATLAS9_FILE)
    Ta, Pa, rhoa, ka, taua, rhox_all, P_all = atlas9_photosphere(2.0/3.0)
    P('      at tau_R = %.4f: T = %.1f K, P = %.4e dyn/cm^2,'
      % (taua, Ta, Pa))
    P('        rho = %.4e g/cm^3, kappa_R = %.4f cm^2/g' % (rhoa, ka))
    Tb, Pb, rhob, kb_, taub = atlas9_photosphere(T_target=M6_TEFF)[:5]
    P('      at T = %.0f K: tau_R = %.4f, rho = %.4e, kappa_R = %.4f'
      % (Tb, taub, rhob, kb_))
    # ATLAS9 gives rho through an equation of state this file rebuilt;
    # hydrostatic balance P = g RHOX checks that rebuild's input side
    # without it.
    g_atl = 10.0**4.4377
    hs = P_all[-1]/(g_atl*rhox_all[-1])
    P('      hydrostatic check at the deepest layer, P/(g RHOX) = %.4f'
      % hs)
    assert abs(hs - 1.0) < 0.05, 'ATLAS9 file does not satisfy P = g m'
    P('    Module 6\'s rho / ATLAS9 rho at tau_R = 2/3 = %.4f'
      % (M6_PHOT_RHO/rhoa))
    P('    ATLAS9 kappa_R / inferred kappa: %.3f at tau_R = 2/3, %.3f at'
      % (ka/kap_inferred, kb_/kap_inferred))
    P('    T = Teff.  CHECK 2, THE ANCHOR: the one-scale-height inference')
    P('    is LOW by a factor %.2f to %.2f.  It assumes kappa constant over'
      % (kb_/kap_inferred, ka/kap_inferred))
    P('    the column; kappa_R in the file rises from %.3f to %.3f between'
      % (kb_, atlas9_photosphere(1.0)[3]))
    P('    tau_R = %.3f and 1.  VERDICT (Gate D): REFUTED as a digit.'
      % taub)
    assert kb_/kap_inferred > 2.0 and ka/kap_inferred > 2.0, \
        'CHECK 2 is REFUTED only while the miss exceeds a factor 2'

    lph = photon_mean_free_path(kap_inferred, M6_PHOT_RHO)
    P('')
    P('    photon mean free path there = %.4e cm = %.1f km'
      % (lph, lph/1.0e5))
    P('    one scale height            = %.1f km' % (M6_PHOT_H/1.0e5))
    P('    ratio                       = %.4f' % (lph/M6_PHOT_H))
    P('    which is 1/tau = %.4f, as it must be.' % (1.0/M6_PHOT_TAU))
    assert abs(lph/M6_PHOT_H - 1.0/M6_PHOT_TAU) < 1.0e-9, \
        'the mean free path must be H/tau by construction'

    tau_sun = optical_depth(kap_solar, M6_PHOT_RHO, Rsun)
    P('')
    P('    tau across a solar radius at photospheric rho = %.4e' % tau_sun)
    P('    random-walk steps to cross it = tau^2 = %.4e'
      % random_walk_steps(tau_sun))
    P('    THIS IS NOT THE SUN\'S OPTICAL DEPTH.  It uses the photospheric')
    P('    density over the whole radius, which is wrong by orders of')
    P('    magnitude, and it is printed only to show the tau^2 scaling.')
    P('    The module must label it as an illustration or drop it.')

    # ------------------------------------------------------------------
    P('')
    P('PART D.  The criterion module04.html:429 deferred BY NAME')
    P('-' * 72)
    P('  Module 4: "omega chi/c^2 << 1 ... That criterion is not evaluated')
    P('  for the Sun in this module ... the size of the failure is a')
    P('  subject of Module 13."  It is evaluated here.')
    chi_phot = radiative_diffusivity(kap_inferred, M6_PHOT_RHO, M6_TEFF,
                                     M6_PHOT_CP)
    omega_max = 2.0*np.pi*M4_NU_MAX
    par = adiabaticity_parameter(omega_max, chi_phot, M4_SOUND_SPEED)
    P('    chi at the photosphere      = %.6e cm^2/s' % chi_phot)
    P('    omega at nu_max = %.0f microHz = %.6e rad/s'
      % (M4_NU_MAX*1.0e6, omega_max))
    P('    c (module04.html:611)       = %.4e cm/s' % M4_SOUND_SPEED)
    P('    omega chi/c^2               = %.6e' % par)
    P('')
    P('    THE CRITERION IS << 1, NOT < 1, AND %.4f IS NEITHER.' % par)
    P('    At order unity the compression leaks about one radian\'s worth')
    P('    of heat per radian of oscillation, so the mode is neither')
    P('    adiabatic nor isothermal.  module04.html:563 predicted exactly')
    P('    this in print -- "fails near the photosphere where radiation')
    P('    carries heat out of a compression within a period" -- and')
    P('    %.4f is that failure AT THE INFERRED OPACITY OF PART C,' % par)
    P('    which step 2 found low; the ATLAS9 values follow.')
    P('    *** chi above carries the INFERRED opacity of PART C, which')
    P('    *** step 2 found LOW against ATLAS9.  With the ATLAS9 kappa_R')
    P('    *** and ATLAS9 rho at the same two levels (c_P and c held at')
    P('    *** Module 6\'s and Module 4\'s values):')
    pars = []
    for lab, Tl, rl, kl in (('T = Teff', Tb, rhob, kb_),
                            ('tau_R = 2/3', Ta, rhoa, ka)):
        chi_l = radiative_diffusivity(kl, rl, Tl, M6_PHOT_CP)
        par_l = adiabaticity_parameter(omega_max, chi_l, M4_SOUND_SPEED)
        pars.append(par_l)
        P('    ***   %-11s  chi = %.4e  omega chi/c^2 = %.4f'
          % (lab, chi_l, par_l))
    P('    *** Both lie between %.4f and %.4f: below 1, and not << 1.'
      % (min(pars), max(pars)))
    P('    *** CHECK 3 VERDICT (Gate D Q5): REFUTED.  The module prints')
    P('    *** BOTH levels; %.4f above is the inferred-opacity value and'
      % par)
    P('    *** is superseded, printed only to show what CHECK 2 moved. ***')
    assert 0.1 < min(pars) and max(pars) < 1.0, \
        'the ATLAS9 adiabaticity parameter left the range the text states'

    P('')
    P('    The same at the acoustic cutoff, nu_ac = %.0f microHz:'
      % (M4_NU_AC*1.0e6))
    par_ac = adiabaticity_parameter(2.0*np.pi*M4_NU_AC, chi_phot,
                                    M4_SOUND_SPEED)
    P('      omega chi/c^2 = %.6e  (ratio to nu_max: %.4f)'
      % (par_ac, par_ac/par))
    assert abs(par_ac/par - M4_NU_AC/M4_NU_MAX) < 1.0e-9, \
        'the parameter is linear in omega; the ratio must be nu_ac/nu_max'

    P('')
    P('    THE SAME NUMBER, READ AS TWO TIMES.  omega chi/c^2 is not a')
    P('    scale-height statement at all: with a wavelength lam = c/nu,')
    P('    the diffusion time across one wavelength divided by one period')
    P('    is c^2/(nu chi), and omega chi/c^2 is 2 pi divided by it.  The')
    P('    two must therefore satisfy one identity, which is the check:')
    lam_mode = M4_SOUND_SPEED/M4_NU_MAX
    t_diff_mode = lam_mode*lam_mode/chi_phot
    P('      wavelength at nu_max   = %.4e cm = %.1f km'
      % (lam_mode, lam_mode/1.0e5))
    P('      diffusion time across it = %.4e s' % t_diff_mode)
    P('      the period               = %.4e s' % (1.0/M4_NU_MAX))
    ratio_tp = t_diff_mode*M4_NU_MAX
    P('      ratio (diffusion/period) = %.4e' % ratio_tp)
    P('      2 pi/ratio               = %.6f' % (2.0*np.pi/ratio_tp))
    P('      omega chi/c^2            = %.6f' % par)
    assert abs(2.0*np.pi/ratio_tp/par - 1.0) < 1.0e-9, \
        'omega chi/c^2 must be 2 pi over the diffusion-time-to-period ratio'
    P('      IDENTICAL, so the two readings are one quantity.  Adiabatic')
    P('      wants the ratio LARGE; %.2f periods is not large.' % ratio_tp)

    # ------------------------------------------------------------------
    P('')
    P('PART E.  Where radiation takes over')
    P('-' * 72)
    P('  The density at which P_rad = P_gas, at mu = %.3f:' % M3_MU)
    for T in (1.0e4, 1.0e5, 1.0e6, M3_T_C, 1.0e8):
        rho_eq = prad_equals_pgas_density(T, M3_MU)
        P('    T = %.2e K   rho = %.4e g/cm^3' % (T, rho_eq))
    ratio_check = M3_RHO_C/prad_equals_pgas_density(M3_T_C, M3_MU_C)
    P('  The Sun\'s tabulated centre, at mu = %.5f, sits at rho = %.2f'
      % (M3_MU_C, M3_RHO_C))
    P('  g/cm^3 against %.4e,' % prad_equals_pgas_density(M3_T_C, M3_MU_C))
    P('  i.e. %.1f times denser than the crossover -- and that ratio is'
      % ratio_check)
    P('  beta/(1-beta) = %.1f, the same statement as 1 - beta = %.3e.'
      % (b_c/(1.0 - b_c), 1.0 - b_c))
    assert abs(ratio_check*(1.0 - b_c)/b_c - 1.0) < 1.0e-9, \
        'rho/rho_eq must equal beta/(1-beta) exactly'

    P('')
    P('  The Sun as a whole, against its own Eddington limit:')
    gam_sun = eddington_ratio_of_a_star(Msun, Lsun, kap_solar)
    P('    L_sun/L_Edd(1 Msun, kappa_es at X = %.4f) = %.4e'
      % (X_H, gam_sun))
    P('    i.e. radiation carries %.2e of the Sun\'s gravity.' % gam_sun)
    P('    Module 3\'s (3.1) drops it, and this is the size of what it')
    P('    dropped -- module03.html:795\'s debt, priced.')

    # ------------------------------------------------------------------
    P('')
    P('PART F.  CHECK 4: Eddington\'s grey atmosphere against ATLAS9')
    P('-' * 72)
    TEFF_A9 = 5777.0     # the file's own header, not the IAU 5772
    P('  T(tau) = Teff [(3/4)(tau + 2/3)]^(1/4), Teff = %.0f K (the file\'s'
      % TEFF_A9)
    P('  own header; the book\'s IAU 5772 K is %.3f per cent lower).'
      % (100.0*(1.0 - M6_TEFF/TEFF_A9)))
    P('    tau_R     ATLAS9 T    grey T    grey/ATLAS9')
    worst_T = 0.0
    for tv in (0.01, 0.1, 0.3, 2.0/3.0, 1.0, 2.0, 3.0):
        Tat = atlas9_photosphere(tv)[0]
        Tg = grey_eddington_T(tv, TEFF_A9)
        worst_T = max(worst_T, abs(Tg/Tat - 1.0))
        P('    %6.4f   %8.1f  %8.1f     %.4f' % (tv, Tat, Tg, Tg/Tat))
    P('    largest |grey/ATLAS9 - 1| = %.4f in T, %.4f in T^4.'
      % (worst_T, (1.0 + worst_T)**4 - 1.0))
    assert worst_T < 0.031, \
        'CHECK 4: grey T(tau) left the 3.1 per cent band fixed at Gate D'
    q0, q23, q001 = hopf_q(np.array([0.0, 2.0/3.0, 0.01]))
    P('  The exact grey solution replaces 2/3 by the Hopf function q(tau):')
    P('    q(0) = %.5f against 1/sqrt(3) = %.5f' % (q0, 1.0/np.sqrt(3.0)))
    assert abs(q0 - 1.0/np.sqrt(3.0)) < 2.0e-4, \
        'the Hopf iteration must reproduce q(0) = 1/sqrt(3)'
    shift = ((2.0/3.0 + q23)/(4.0/3.0))**0.25 - 1.0
    P('    q(2/3) = %.5f, which moves T at tau = 2/3 by %.3f per cent.'
      % (q23, 100.0*shift))
    assert abs(shift) < 0.005, \
        'the exact grey solution must move T(2/3) by under 0.5 per cent'
    Ta23 = atlas9_photosphere(2.0/3.0)[0]
    P('    ATLAS9 at tau_R = 2/3 is %.1f K, %.2f per cent above Teff.'
      % (Ta23, 100.0*(Ta23/TEFF_A9 - 1.0)))
    P('    The closure accounts for %.2f per cent of it; the rest is what'
      % (100.0*shift))
    P('    the grey model leaves out.  This check does not separate')
    P('    non-grey opacity from ATLAS9\'s convection (l/H = 1.25).')
    h001 = ((0.01 + q001)/(0.01 + 2.0/3.0))**0.25
    P('    At tau = 0.01 the other way round: Hopf multiplies grey T by')
    P('    %.4f, so grey/ATLAS9 becomes %.4f -- the closure is the error.'
      % (h001, h001*grey_eddington_T(0.01, TEFF_A9)
         / atlas9_photosphere(0.01)[0]))
    P('  CHECK 4 VERDICT (Gate D): CONFIRMED within 3.1 per cent in T.')

    # ------------------------------------------------------------------
    # PART L.  Added at step 4.  Every answer is computed from the numbers
    # the problem STATEMENT prints, so that m13_problems_check.py, which
    # imports nothing from here, can recompute it from the statement and
    # parse the expected value out of this run.  Labels carry no digits,
    # because a digit inside a label is what grab() finds first.
    P('')
    P('PART L.  The nine problems')
    P('-' * 72)
    xg, wg = np.polynomial.legendre.leggauss(8)
    P('  C1 isotropic field, P_rad/u_rad        = %.6f'
      % (np.sum(wg*xg*xg)/np.sum(wg)))
    P('  C1 one open hemisphere, P_rad/u_rad    = %.6f'
      % (np.sum(wg*(0.5*xg + 0.5)**2)/np.sum(wg)))
    P('  C1 parallel beam, P_rad/u_rad          = %.6f' % 1.0)
    assert abs(np.sum(wg*xg*xg)/np.sum(wg) - 1.0/3.0) < 1.0e-14, \
        'C1: the isotropic angular average of cos^2 must be 1/3'

    M_ns = 1.4*Msun
    L_ns_H = eddington_luminosity(M_ns, kappa_electron_scattering(1.0))
    L_ns_i = eddington_luminosity(M_ns, kap_init)
    P('  C2 neutron-star mass, g               = %.6e' % M_ns)
    P('  C2 L_Edd, pure hydrogen, erg/s        = %.6e' % L_ns_H)
    P('  C2 L_Edd, protosolar X, erg/s         = %.6e' % L_ns_i)
    P('  C2 Mdot_Edd, pure hydrogen, g/s       = %.6e'
      % (L_ns_H/(M9_ETA_ASSUMED*c*c)))
    P('  C2 Mdot_Edd, protosolar X, g/s        = %.6e'
      % (L_ns_i/(M9_ETA_ASSUMED*c*c)))
    P('  C2 ratio of the two limits            = %.6f' % (L_ns_i/L_ns_H))

    for lab, tv in (('surface', 0.0), ('two-thirds', 2.0/3.0),
                    ('depth two', 2.0)):
        P('  C3 grey T at the %s, K = %.1f'
          % (lab, grey_eddington_T(tv, M6_TEFF)))
    P('  C3 surface T over Teff                = %.6f'
      % (grey_eddington_T(0.0, M6_TEFF)/M6_TEFF))

    def dlnT_dlnrho(beta, gg=5.0/3.0):
        return ((4.0 - 3.0*beta)*(gg - 1.0)
                / (beta + 12.0*(gg - 1.0)*(1.0 - beta)))
    P('  D1 Gamma_one, pure gas                = %.6f' % gamma_effective(1.0))
    P('  D1 Gamma_one, pure radiation          = %.6f'
      % gamma_effective(0.0))
    P('  D1 Gamma_one, half and half           = %.6f'
      % gamma_effective(0.5))
    P('  D1 dlnT/dlnrho, pure gas              = %.6f' % dlnT_dlnrho(1.0))
    P('  D1 dlnT/dlnrho, pure radiation        = %.6f' % dlnT_dlnrho(0.0))
    # the product rule of the proof, checked against eq. (131)
    for bt in (0.0, 0.3, 0.5, 0.9, 1.0):
        assert abs(bt + (4.0 - 3.0*bt)*dlnT_dlnrho(bt)
                   - gamma_effective(bt)) < 1.0e-12, \
            'D1: beta + (4 - 3 beta) dlnT/dlnrho must be eq. (131)'

    # D2: P6 at depth, fed to P4 in its optical-depth form, must carry
    # sigma Teff^4 exactly.  T^4 is linear in tau, so a difference is exact.
    t1, t2 = 100.0, 101.0
    dT4 = (grey_eddington_T(t2, M6_TEFF)**4
           - grey_eddington_T(t1, M6_TEFF)**4)/(t2 - t1)
    P('  D2 deep flux from the diffusion law over sigma Teff^4 = %.6f'
      % ((c*a_rad/3.0)*dT4/(sigma_SB*M6_TEFF**4)))

    bound_sun = 4.0*np.pi*c*G*Msun/Lsun
    P('  D3 Eddington opacity bound for the Sun, cm^2/g = %.1f' % bound_sun)
    P('  D3 kappa_es over that bound            = %.4e'
      % (kap_solar/bound_sun))
    P('  D3 L_sun/L_Edd from the limit          = %.4e'
      % eddington_ratio_of_a_star(Msun, Lsun, kap_solar))

    t_e = t_sal/(1.0 - M9_ETA_ASSUMED)
    nfold = np.log(1.0e9/10.0)
    P('  K1 e-folding time with the kept fraction, yr    = %.4e'
      % (t_e/yr))
    P('  K1 number of e-folds                            = %.6f' % nfold)
    P('  K1 growth time with the kept fraction, yr       = %.4e'
      % (nfold*t_e/yr))
    P('  K1 growth time if all the inflow were kept, yr  = %.4e'
      % (nfold*t_sal/yr))

    L_k2 = M9_ETA_ASSUMED*M9_K2_MDOT_BONDI*c*c
    P('  K2 luminosity at the book efficiency, erg/s = %.4e' % L_k2)
    P('  K2 that luminosity over L_Edd               = %.1f' % (L_k2/L2))
    P('  K2 efficiency that would sit at L_Edd       = %.4e'
      % (L2/(M9_K2_MDOT_BONDI*c*c)))

    k3 = dict(kap=0.4447, rho=2.6721e-7, T=5910.1, cP=1.6968e8,
              cs=8.081e5, nu=4497.0e-6)
    chi_k3 = radiative_diffusivity(k3['kap'], k3['rho'], k3['T'], k3['cP'])
    par_k3 = adiabaticity_parameter(2.0*np.pi*k3['nu'], chi_k3, k3['cs'])
    P('  K3 chi from the stated inputs, cm^2/s  = %.4e' % chi_k3)
    P('  K3 adiabaticity parameter at the cutoff = %.4f' % par_k3)
    P('  K3 diffusion time over period at the cutoff = %.3f'
      % (2.0*np.pi/par_k3))
    P('  K3 against the same level at nu_max, ratio = %.4f'
      % (par_k3/pars[1]))

    # ------------------------------------------------------------------
    # PART M.  Added at step 4: numbers the draft prints that no earlier
    # part printed.  Each is arithmetic on values above, done here so the
    # prose copies it from a run and does not type it.
    P('')
    P('PART M.  Numbers the draft prints that earlier parts did not')
    P('-' * 72)
    k_one = atlas9_photosphere(1.0)[3]
    P('  CHECK 2 spread of the two levels, kappa ratio   = %.4f'
      % (ka/kb_))
    P('  CHECK 2 input spread, rho ratio times level ratio = %.4f'
      % ((M6_PHOT_RHO/rhoa)*(ka/kb_)))
    P('  CHECK 2 kappa_R rise over the averaged column   = %.4f'
      % (k_one/kb_))
    tau_p, T_p, P_p, rho_p, kR_p, xne_p, _ = atlas9_profile()
    ne23 = np.exp(np.interp(np.log(2.0/3.0), np.log(tau_p), np.log(xne_p)))
    kes_true = sigma_T*ne23/rhoa
    P('  electron density at tau_R = 2/3, ATLAS9, cm^-3 = %.4e' % ne23)
    P('  electron scattering with that n_e, cm^2/g      = %.4e' % kes_true)
    P('  kappa_R over that electron scattering          = %.1f'
      % (ka/kes_true))
    P('  fully ionised kappa_es over it                  = %.1f'
      % (kap_solar/kes_true))
    P('    PART C said the inferred 0.15231 below the fully ionised')
    P('    0.34966 shows the photosphere is not electron-scattering.')
    P('    ATLAS9 kappa_R = %.4f is ABOVE 0.34966, so that argument does'
      % ka)
    P('    not survive CHECK 2.  The reason is ionisation: with the')
    P('    electrons ATLAS9 actually has, electron scattering is the')
    P('    number above, and kappa_R exceeds it by the ratio above.')
    P('  photon mean free path at tau_R = 2/3, ATLAS9, km = %.1f'
      % (photon_mean_free_path(ka, rhoa)/1.0e5))
    P('  P_rad/P at tau_R = 2/3, ATLAS9                  = %.4e'
      % (radiation_pressure(Ta)/Pa))
    P('  ATLAS9 T at tau_R = 2/3 minus its Teff, K       = %.1f'
      % (Ta23 - TEFF_A9))
    P('  the part of the 2/3 miss the closure leaves, per cent = %.2f'
      % (100.0*(Ta23/TEFF_A9 - 1.0) - 100.0*shift))
    P('  diffusion time over period, T = Teff level      = %.2f'
      % (2.0*np.pi/pars[0]))
    P('  diffusion time over period, tau_R = 2/3 level   = %.2f'
      % (2.0*np.pi/pars[1]))
    P('  Gamma_one at the Sun\'s centre, beta_c           = %.6f'
      % gamma_effective(b_c))
    P('  its shortfall below five-thirds                 = %.4e'
      % (5.0/3.0 - gamma_effective(b_c)))

    # ------------------------------------------------------------------
    P('')
    P('PART G.  What steps 2 and 3 settled, and what is still open')
    P('-' * 72)
    P('  Read at step 2, each off the page:')
    P('    1. kappa_R at the solar photosphere: ATLAS9, PART C.')
    P('    2. Gamma_1: Chandrasekhar (1939) eq. (131) p. 57, Table 1 p. 59.')
    P('    3. Eddington (1926): %s.' % EDDINGTON_1926_LIMIT_FORM)
    P('       His Sun bound is k < %.0f; this file\'s constants give %.0f.'
      % (EDDINGTON_1926_SUN_K_BOUND, 4.0*np.pi*c*G*Msun/Lsun))
    P('    4. BS2005-AGS,OP prints no 1 - beta; module03.html:628 does.')
    P('  Ruled at Gate D: diffusion_time\'s factor 3 is derived, not')
    P('  sourced.  Still open: no ULX (optional); Eddington\'s 1926')
    P('  printing was not seen, only the 1930 reprint.')
    P('  And three things the run has FOUND that are not about papers:')
    P('    (a) module09.html:913\'s doubling time is M/Mdot, exact at')
    P('        constant Mdot; the page states no growth law.  NOT a defect.')
    P('    (b) module09.html:944\'s m_p is a COMPOSITION -- pure ionised')
    P('        hydrogen -- and no shipped page says so.  CHECK 1.')
    P('    (c) the book carries three values of eta_rad and Mdot_Edd')
    P('        carries it.  Simon ruled 0.1 stays; nothing shipped moves.')
    P('')
    P('=' * 72)
    P('END OF RUN.  All asserts passed.')
    P('=' * 72)


if __name__ == '__main__':
    main()
