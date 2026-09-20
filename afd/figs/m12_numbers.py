"""Module 12 numbers: magnetohydrodynamics.  The plasma beta, the induction
equation and flux freezing, magnetic pressure and tension, the Alfven and
magnetosonic speeds, the Parker spiral, the Alfven radius, magnetic support
against collapse, suppressed transport across a field, the magnetorotational
instability, and critical balance.

Every physical number quoted in module12.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

WHY THIS MODULE IS BUILT BEFORE MODULE 11.  module10.html:924 prints the
reason: of Module 10's four checks, the one that confirms Kolmogorov most
cleanly is a MAGNETIC spectral index in an Alfvenic plasma, and 5/3 for B
is also what Goldreich & Sridhar (1995) predict from a different argument.
The book confirms its central result on a quantity for which it has no
theory.  This module is that theory.  The twenty debts the ten shipped
modules have already printed against it are listed, each with the file and
line it was read from, in .ignore/m12-promises.md.

THE SHAPE OF THE CHECK, following Modules 2, 3 and 10.  From ONE published
source, one exact prediction is CONFIRMED and one assumption is REFUTED.

  THE ANCHOR IS CHECK 1, Venzmer & Bothmer (2018), A&A 611, A36, Table 3.
  Their power-law fits to combined Helios 1+2 data over 0.29-0.98 au give,
  from the same table and the same data, a magnetic-field index and a
  density index measured side by side.

    CONFIRMED  The Parker spiral.  Flux freezing plus a radial wind
               predicts B_r ~ r^-2 and B_phi ~ r^-1, so the TOTAL field
               falls off more slowly than r^-2 by an amount that depends
               only on the solar rotation rate and the wind speed --
               both of which this book already has.  Fitted over the
               same 0.29-0.98 au window, that prediction is an index
               near -1.74 with NOTHING adjusted, against a measured
               -1.655 +/- 0.017 (median fits).

    REFUTED    The unwound radial field.  A purely radial field gives
               exactly -2.000, and the same table excludes it.  The
               density index in the same row is -2.093 +/- 0.046, so the
               measurement CAN see an r^-2 falloff when there is one:
               the field's failure to show it is a measurement of the
               winding, not of the error bar.

  THE ERROR BAR USED IS THE YEAR-TO-YEAR SCATTER, not the formal fit
  error, following Module 9's treatment of the same table.  The paper's
  Fig. 9 gives 0.11 for the field index and 0.072 for the density; those
  are larger than the formal errors and are the cautious choice.

  CHECK 2 IS BRACKETED, AND IT IS THIS MODULE'S SHARPEST RESULT.
  THIS PARAGRAPH WAS WRONG UNTIL STEP 4 AND IS CORRECTED HERE: it said
  "near 23-25 R_sun" and "wrong by a factor of about two", which was the
  framing before step 1 defect 17 put the RADIAL field into the Alfven
  speed.  The eight extrapolated variants of PART F span 15.76 to 19.35
  R_sun.  Verscharen, Bale & Velli (2021) Table 3 measure 12.080 +/-
  0.236 R_sun (first fast-latitude scan) and 9.504 +/- 0.221 (third) --
  the table Module 9 quotes at module09.html:964 -- and Kasper et al.
  (2021) Table I put a LOWER bound of 19.8 R_sun on the surface along
  one Parker Solar Probe trajectory.  Every variant lies ABOVE the
  first and BELOW the second, so the extrapolation is bracketed by two
  published numbers and matches neither.  It cannot match both: they
  are not the same quantity.

A NOTE ON ONE NUMBER THAT MUST NOT BE PRINTED ALONE.  module09.html:846
prints the solar wind's Alfven surface as "near 12 R_sun", sourced at
module09.html:964 to Verscharen's FLS1 value.  afd/figs/m09_numbers.py:1301
prints, in its own run, "the Alfven surface near 19 R_sun" -- the Parker
Solar Probe crossing value, a different method and a different definition
of the surface, and NOT in Module 9's sources list.  Module 9's HTML is
right and its generator's aside is not.  This module prints an Alfven
radius, so it names both or it creates a contradiction across two modules.

TWO CONSTRAINTS THAT ARE ALREADY IN PRINT AND ARE THEREFORE NOT OPEN.
module08.html:728 names the magnetorotational instability in a list of
what Module 12 builds, so PART I is not optional; it is done locally,
with d ln Omega/d ln R = -3/2 ASSUMED rather than derived from a disc
model, because disc structure is Module 11.  And module08.html:970 calls
Module 8's refusal of a Voyager comparison "permanent rather than
provisional" ON THE GROUNDS THAT MODULE 12 DOES NOT DERIVE the oblique
magnetohydrodynamic jump conditions.  This module therefore does not
derive them, and says so in print.

WHAT IS NOT YET SOURCE-VERIFIED.  This is step 1 of six.  Every constant
below that carries a NEEDS-STEP-2 comment was written from standard
results and has NOT been read out of a PDF in this project.  Step 2 must
read each one or the module must print it as "stated, not derived" with
no check resting on it.  The three check sources that ARE already
verified in this repo are marked VERIFIED, with the module that verified
them.

Sources for every published number compared against are listed in the
SOURCES block at the foot of this file and in module12.html.
"""
import math

import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m10_numbers.py rather than imported, so that each
# module's numbers script reads on its own.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
e = 4.80320471e-10      # esu            (elementary charge)
me = 9.1093837015e-28   # g
mp = 1.67262192369e-24  # g
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
hbar = 1.054571817e-27  # erg s
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
pc = 3.0856775814913673e18   # cm
kpc = 1e3*pc
Mpc = 1e6*pc
AU = 1.495978707e13     # cm
yr = 3.15576e7          # s
day = 86400.0           # s

GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
Rsun = 6.957e10         # cm             (IAU 2015 nominal)
Msun = GMsun/G          # g

# Module 1's inputs, reused unchanged so the modules cannot diverge.
SPITZER_C = 3.0**1.5/(4.0*np.sqrt(np.pi))   # = 0.7329, Sarazin eq. 5.32
MU_H = mp/mu_u          # = 1.00728, a proton measured against m_u
MU_ICM = 0.61           # mean molecular weight, fully ionised ICM
SIGMA_H = 1.0e-15       # cm^2, order-of-magnitude neutral cross-section

# =========================================================================
# PUBLISHED VALUES COMPARED AGAINST.  Each block names the paper, the
# table or equation, and what the quoted error actually means.
# =========================================================================

# --- Venzmer & Bothmer (2018), A&A 611, A36, eq. (10) and Table 3. -------
# VERIFIED for Module 9 (see HANDOFF "Sources already verified"); the PDF
# is arxiv.org/pdf/1711.07534, Table 3 on page 7.  Power-law fits
# x(r) = d r^e to combined Helios 1+2 data over 0.29-0.98 au, with d the
# 1-au value.  The bracketed figures are the formal fit errors on the last
# digits.  THE ERROR USED IN CHECK 1 IS NOT THESE: it is the year-to-year
# exponent scatter of their Fig. 9, which is larger.
VB18_R_LO_AU = 0.29
VB18_R_HI_AU = 0.98
# (1-au value, its error, exponent, its formal error)
VB18_MEAN = {
    'density': (7.57, 0.30, -2.010, 0.038),      # cm^-3
    'velocity': (435.6, 2.4, +0.049, 0.010),     # km/s
    'temperature': (9.67e4, 0.21e4, -0.792, 0.028),   # K
    'field': (6.05, 0.10, -1.546, 0.018),        # nT
}
VB18_MEDIAN = {
    'density': (5.61, 0.27, -2.093, 0.046),
    'velocity': (410.7, 2.8, +0.058, 0.013),
    'temperature': (7.14e4, 0.23e4, -0.913, 0.039),
    'field': (5.377, 0.092, -1.655, 0.017),
}
# Their Fig. 9, the year-to-year scatter of the fitted exponents.
VB18_SCATTER = {
    'density': 0.072,
    'velocity': 0.012,
    'temperature': 0.050,
    'field': 0.11,
}

# --- Verscharen, Bale & Velli (2021), MNRAS 506(4), 4993-5004, Table 3. --
# VERIFIED for Module 9 and quoted at module09.html:964.  Alfven radius
# from Ulysses fast-latitude scans; the errors are the paper's own.
VBV21_RA_FLS1 = 12.080          # R_sun
VBV21_RA_FLS1_ERR = 0.236
VBV21_RA_FLS3 = 9.504
VBV21_RA_FLS3_ERR = 0.221
# Their sonic radius, which the paper itself calls a LOWER limit.  Quoted
# here only so that this module cannot confuse the two surfaces.
VBV21_RS = 0.309                # R_sun, lower limit
VBV21_RS_ERR = 0.004

# --- Kasper et al. (2021), Phys. Rev. Lett. 127, 255101. ----------------
# VERIFIED at step 2 from the APS open-access PDF (CC-BY),
# link.aps.org/pdf/10.1103/PhysRevLett.127.255101.  THE PREP HAD THE
# RANGE WRONG: it wrote 19-20 R_sun, which is the start of the FIRST
# interval only.  Their own summary sentence (p. 5) reads "PSP crossed
# below the Alfven critical surface for the first time in 2021 and at
# distances of 16-20 R_sun from the Sun", and their Table I lists three
# sub-Alfvenic intervals during encounter 8, with R_sun = 6.95e5 km:
#   I1  2021-04-28 09:33-14:42  19.8 -> 18.4 R_sun  median M_A = 0.79
#   I2  2021-04-29 07:18-07:52  16.0 -> 16.0 R_sun  median M_A = 0.49
#   I3  2021-04-29 23:40-04-30 01:24  17.7 -> 18.0  median M_A = 0.88
# EVERY M_A IS BELOW 1, so each figure is a point INSIDE the surface and
# not the surface itself; 19.8 R_sun is a lower bound on the surface
# along that one trajectory.  This is a local crossing of an irregular
# boundary and not a spherically averaged radius, which is the whole of
# Gate D question 6.
KASPER21_RA_LO = 16.0           # R_sun, their quoted range    VERIFIED
KASPER21_RA_HI = 20.0           # R_sun, their quoted range    VERIFIED
KASPER21_RA_OUTERMOST = 19.8    # R_sun, start of interval I1  VERIFIED
KASPER21_MA = [0.79, 0.49, 0.88]    # median M_A, I1, I2, I3   VERIFIED

# --- Podesta, Roberts & Goldstein (2007), ApJ 664, 543, Table 2. --------
# VERIFIED for Module 10 step 2.  The four magnetic spectral indices and
# their 99% confidence half-widths, copied from m10_numbers.py so that the
# two modules quote one set of numbers.  Module 10's anchor; this module
# uses it only to state the tension it inherits, and checks nothing new
# against it at step 1.
PODESTA_B_INDEX = [1.66, 1.72, 1.66, 1.58]
PODESTA_B_ERR = [0.02, 0.02, 0.01, 0.02]

# --- Braginskii (1965), Reviews of Plasma Physics 1, 205-311. -----------
# ALL SEVEN COEFFICIENTS ARE NOW VERIFIED from the original Consultants
# Bureau translation, the image scan at
# static.ias.edu/pitp/2016/sites/pitp/files/braginskii_1965-1.pdf.  The
# scan has NO TEXT LAYER, so the pages were rendered at 120-400 dpi and
# read as images.  THE PAGE MAP IS CONFIRMED, not assumed: PDF page 7
# carries printed pages 214 (left) and 215 (right), so article page =
# 2*(PDF page) + 200 on the left half and +201 on the right.
# The ion viscosity coefficients on p. 218 (eq. 2.22, eq. 2.23) were
# read for Module 10 and are reused unchanged.  The five read at step 2
# are on pp. 216-217, all of them EXPLICITLY FOR Z = 1; his Table 1 on
# p. 216 tabulates the Z-dependence, and the electron conduction
# coefficient runs 3.16, 4.9, 6.1, 6.9, 12.5 for Z = 1, 2, 3, 4, inf
# while the perpendicular one runs 4.66, 4.0, 3.7, 3.6, 3.2.  Every
# plasma in this module is hydrogenic, Z = 1.
BRAG_ETA0_ION = 0.96            # eta_0^i = 0.96 n_i T_i tau_i    VERIFIED
BRAG_ETA1_ION = 3.0/10.0        # eta_1^i, /(omega^2 tau_i)       VERIFIED
BRAG_KAPPA_PAR_E = 3.16         # eq. (2.12), p. 217, Z = 1       VERIFIED
BRAG_KAPPA_PERP_E = 4.66        # eq. (2.13), p. 217, Z = 1       VERIFIED
BRAG_KAPPA_PAR_I = 3.9          # eq. (2.15), p. 217              VERIFIED
BRAG_KAPPA_PERP_I = 2.0         # eq. (2.16), p. 217              VERIFIED
BRAG_SIGMA_PAR = 1.96           # eq. (2.8), p. 216, Z = 1        VERIFIED
# His eq. (2.6) on p. 216 writes the friction force with 0.51 u_par,
# and 1/0.51 = 1.9608, which is where the 1.96 of eq. (2.8) comes from.
# Table 1 tabulates the 0.51, not the 1.96: 0.51, 0.44, 0.40, 0.38, 0.29
# for Z = 1, 2, 3, 4, inf.
BRAG_ALPHA_PAR = 0.51           # eq. (2.6), p. 216, Z = 1        VERIFIED
# His Coulomb logarithm, p. 215, in eV and cm^-3, recorded but NOT used
# -- Modules 1 and 10 own that quantity and this file copies theirs:
#   T_e <  50 eV:  lambda = 23.4 - 1.15 log n + 3.45 log T_e
#   T_e >= 50 eV:  lambda = 25.3 - 1.15 log n + 2.30 log T_e

# --- Zhuravleva et al. (2019), Nature Astronomy 3, 832-837. -------------
# VERIFIED for Module 10 step 2.  A one-sided bound, not a value.
ZHURAVLEVA_SUPPRESSION_LO = 10.0
ZHURAVLEVA_SUPPRESSION_HI = 1000.0

# --- Solar rotation. ----------------------------------------------------
# BOTH VERIFIED AT STEP 2, AND THEY DIFFER BY MORE THAN LATITUDE.
# 25.38 d is the NASA NSSDC Sun Fact Sheet's sidereal rotation period,
# printed there as 609.12 hours (609.12/24 = 25.380 exactly), with the
# footnote "This is the adopted period at 16 deg. latitude - the actual
# rotation rate varies with latitude L as (14.37 - 2.33 sin^2 L - 1.56
# sin^4 L) deg/day".  That law at L = 16 deg gives 14.1840 deg/day and
# 360/14.1840 = 25.3808 d, so the fact sheet is self-consistent.  IT
# NAMES NO TRACER.  Its law is 2.36 per cent slower than Snodgrass &
# Ulrich's, and they say theirs is about 2 per cent faster than the
# magnetic rate, so the NSSDC law is CONSISTENT WITH a magnetic-feature
# rate -- which is an inference from two papers and not something the
# fact sheet says.
# 24.47 d IS NOT THAT SAME LAW AT THE EQUATOR.  That law at L = 0 gives
# 14.3700 deg/day and 25.0522 d.  24.47 d is Snodgrass & Ulrich (1990),
# ApJ 351, 309-316, whose Doppler cross-correlation of the
# supergranulation network gives omega = 14.71 - 2.39 sin^2 L - 1.78
# sin^4 L deg/day sidereal; 360/14.71 = 24.4731 d.  Their abstract says
# their rate is about 2 per cent faster than the magnetic one.
# SO THE 3.71 PER CENT SPREAD PART E PRICES IS TWO EFFECTS, NOT ONE:
# 2.36 per cent is WHICH TRACER, at either latitude, and 1.32 per cent
# is WHICH LATITUDE, on either tracer.  1.0236 x 1.0132 = 1.0371.
CARRINGTON_SIDEREAL_DAYS = 25.38    # NSSDC, 16 deg, magnetic  VERIFIED
EQUATORIAL_SIDEREAL_DAYS = 24.47    # Snodgrass & Ulrich 1990  VERIFIED
NSSDC_OMEGA_DEG_DAY = (14.37, -2.33, -1.56)     # 1, sin^2 L, sin^4 L
SU90_OMEGA_DEG_DAY = (14.71, -2.39, -1.78)      # 1, sin^2 L, sin^4 L
CARRINGTON_LATITUDE_DEG = 16.0
# The source surface, where the coronal field is taken radial.  A MODEL
# PARAMETER, not a measurement; 2.5 R_sun is the conventional choice and
# PART E prices the spread from 2.0 to 3.0.  Step 2 note: Kasper et al.
# (2021) chose 2.0 R_sun for their own PFSS solution, "selected to
# accurately reproduce low latitude coronal holes observed in STEREO
# ... extreme ultraviolet images of the Sun during the encounter".  That
# is inside the priced spread, and it is evidence the parameter is
# fitted per event rather than known.
R_SOURCE_SURFACE = 2.5          # R_sun

# --- Mouschovias & Spitzer (1976), ApJ 210, 326-327. --------------------
# VERIFIED at step 2 from the ADS scan, bibcode 1976ApJ...210..326M.
# THE PAPER NEVER PRINTS 0.13.  It is a two-page note, and its eq. (2)
# on p. 326 reads
#       M_cPhi = (c_1/(3 pi)) (5/G)^(1/2) Phi  =  c_1 x M,
# where c_1 is a correction factor that the virial-theorem analysis sets
# to unity and their fit to exact equilibrium models sets to c_1 = 0.53
# in their eq. (4) on p. 327 (with c_2 = 0.60 for the external
# pressure).  So c_Phi is COMPUTED from their c_1 and never retyped,
# which is the rule step 1 earned.  The value is 0.125745 and the prep
# printed 0.13, which is 3.38 per cent high.
MS76_C1 = 0.53                  # their eq. (4), p. 327        VERIFIED
MS76_C_PHI = MS76_C1*np.sqrt(5.0)/(3.0*np.pi)   # = 0.125745   VERIFIED

# --- Nakano & Nakamura (1978), PASJ 30, 671-679. ------------------------
# VERIFIED at step 2 from the ADS scan, bibcode 1978PASJ...30..671N.
# Their abstract, p. 671: an isothermal gaseous DISK threaded
# perpendicularly by a uniform frozen-in field "is stable when
# sigma_0/B_0 < (4 pi^2 G)^(-1/2), where sigma_0 and B_0 are the column
# density of the disk and magnetic field strength".  (4 pi^2 G)^(-1/2)
# = 1/(2 pi sqrt(G)), so c_Phi = 1/(2 pi) = 0.15915 -- and it is a
# COLUMN DENSITY over a field, a sheet and not a sphere.
NN78_C_PHI = 1.0/(2.0*np.pi)    # = 0.15915, the disc value    VERIFIED

# --- Troland & Crutcher (2008), ApJ 680, 457-465. -----------------------
# VERIFIED at step 2 from arXiv:0802.2253, fetched and read with PyMuPDF.
# THIS REPLACES CRUTCHER (2012) AS PART G's CHECK.  The ARA&A review is
# paywalled, has no open-access copy that OpenAlex or Semantic Scholar
# knows of, and WAS NOT READ.  Troland & Crutcher is the primary survey
# behind the part of it PART G wanted: 500 h of Arecibo OH Zeeman
# observations toward 34 dark cloud cores, and they define lambda
# against NAKANO & NAKAMURA's critical ratio -- the same constant as
# NN78_C_PHI above.  Their eq. (2) is lambda = 7.6e-21 N(H2)/B_los with
# N(H2) in cm^-2 and B_los in microgauss; PART G rebuilds that
# coefficient from NN78_C_PHI and mu = 2.8 per H2 molecule, gets
# 7.6022e-21, and that agreement is the check that the two files mean
# the same critical ratio.
# Their results, after the geometrical correction the prep did not know
# about: raw weighted-mean B_los = 8.2 +/- 2.2 microgauss giving lambda
# = 4.2, median lambda_1/2 = 5.2, total mean |B| = 16.4 microgauss.  The
# correction lies between 1/2 (only B_los is measured) and 1/3 (disc
# morphology), and their corrected ranges are below.
TC08_LAMBDA_MEAN_LO = 1.4       # lambda_c, disc correction    VERIFIED
TC08_LAMBDA_MEAN_HI = 2.1       # lambda_c, l.o.s. only        VERIFIED
TC08_LAMBDA_MED_LO = 1.7        # lambda_1/2,c                 VERIFIED
TC08_LAMBDA_MED_HI = 2.6        # lambda_1/2,c                 VERIFIED
TC08_B_LOS = 8.2                # microgauss, weighted mean    VERIFIED
TC08_B_LOS_ERR = 2.2            # microgauss                   VERIFIED
TC08_B_TOTAL = 16.4             # microgauss, |B| = 2 B_los    VERIFIED
TC08_LAMBDA_COEFF = 7.6e-21     # their eq. (2)                VERIFIED
TC08_N_CORES = 34               # dark cloud cores observed    VERIFIED
TC08_DENSITY = 3.0e3            # cm^-3, "a few times 10^3"    VERIFIED
MU_PER_H2 = 2.8                 # mass per H2 molecule, with He

# --- predictions, held as named constants so no magic number appears ----
PARKER_BR_INDEX = -2.0          # B_r r^2 = const, from div B = 0
PARKER_BPHI_INDEX = -1.0        # B_phi ~ 1/r at large r
KOLMOGOROV_SPEC = 5.0/3.0       # E(k) ~ k^-5/3, Module 10's exponent
GS95_PARALLEL = 2.0/3.0         # k_par ~ k_perp^(2/3), critical balance
KEPLER_Q = 1.5                  # q = -d ln Omega/d ln R, Keplerian
MRI_GROWTH_FACTOR = 0.75        # gamma_max = (q/2) Omega = 0.75 Omega
MRI_KMAX_FACTOR = np.sqrt(15.0)/4.0     # (k v_A)_max = sqrt(15)/4 Omega
MRI_KCRIT_FACTOR = np.sqrt(3.0)         # marginal at k v_A = sqrt(3) Omega


# =========================================================================
# PART A.  Is the fluid magnetised?
# =========================================================================

def alfven_speed(B, rho):
    """v_A = B/sqrt(4 pi rho), the speed of a transverse field disturbance.

    Derived in Section 5 of module12.html from the linearised induction
    and momentum equations: magnetic tension B^2/4pi supplies a restoring
    force on a field line of mass per unit length rho, and the resulting
    wave speed is the same sqrt(tension/density) as a string's.
    """
    return B/np.sqrt(4.0*np.pi*rho)


def plasma_beta(n, T, B):
    """beta = p_gas/p_mag = 8 pi n k T/B^2.

    n is the TOTAL particle density, so that p_gas = n k T is the total
    thermal pressure.  Rows below that quote an electron or proton density
    convert first; the conversion is printed beside each row.
    """
    return 8.0*np.pi*n*kB*T/(B*B)


def magnetic_pressure(B):
    """p_mag = B^2/(8 pi), in erg/cm^3."""
    return B*B/(8.0*np.pi)


def gyrofrequency(B, m=mp, Z=1):
    """omega_c = Z e B/(m c), the cyclotron angular frequency."""
    return Z*e*B/(m*c)


def gyroradius(T, B, m=mp, Z=1):
    """Thermal gyroradius r_g = m v_th c/(Z e B), v_th = sqrt(2 k T/m).

    COPIED FROM m10_numbers.py, WHICH COPIED IT FROM m01_numbers.py, so
    that three modules print one gyroradius for one plasma.  The speed is
    sqrt(2 k T/m) and NOT the mean speed sqrt(8 k T/pi m); the two differ
    by sqrt(4/pi) = 1.128, and Module 10 section 6.4 exists because that
    factor was got wrong in three consecutive modules.
    """
    vth = np.sqrt(2.0*kB*T/m)
    return m*vth*c/(Z*e*B)


def lam_coulomb(n, T, lnL, coef=SPITZER_C):
    """Thermal Coulomb mean free path, Module 1's equation and coefficient.

        lambda = coef (k T)^2/(n e^4 ln Lambda),  coef = 3^(3/2)/(4 sqrt(pi))

    COPIED FROM m10_numbers.py.  Retyping it here from the algebra put a
    spurious pi in the denominator and gave 7.2 kpc for the intracluster
    medium against Module 1's 22.5 kpc; the prep review of 2026-09-19
    caught it on the first run because the docstring of the Module 10
    original prints the expected answer beside the formula.
    """
    return coef*(kB*T)**2/(n*e**4*lnL)


def v_thermal(T, mu):
    """Mean thermal speed sqrt(8 k T/(pi mu m_u)), Module 1's definition."""
    return np.sqrt(8.0*kB*T/(np.pi*mu*mu_u))


def sound_speed(T, mu, gamma=5.0/3.0):
    """Adiabatic sound speed sqrt(gamma k T/(mu m_u))."""
    return np.sqrt(gamma*kB*T/(mu*mu_u))


# =========================================================================
# PART B.  The induction equation, and the magnetic Reynolds number
# =========================================================================

def tau_electron(n, T, lnL):
    """Braginskii's electron collision time, his eq. (2.5e).

    tau_e = 3 sqrt(m_e) (k T)^(3/2) / (4 sqrt(2 pi) n e^4 ln Lambda).

    VERIFIED at step 2.  His eq. (2.5e) on p. 215 of the original
    translation reads

        tau_e = 3 sqrt(m_e) T_e^(3/2) / (4 sqrt(2 pi) lambda e^4 Z^2 n_i)

    with T in energy units, lambda his Coulomb logarithm, and -- note --
    Z^2 n_i in the denominator and not n_e.  At Z = 1 the two are the
    same number, and every plasma in this module is hydrogenic, so the
    n below is right.  The sqrt(2 pi) is his and is the whole difference
    from the ion form in tau_ion.
    """
    return (3.0*np.sqrt(me)*(kB*T)**1.5
            / (4.0*np.sqrt(2.0*np.pi)*n*e**4*lnL))


def tau_ion(n, T, lnL, Z=1):
    """Braginskii's ion collision time, his eq. (2.5i), p. 215.

    tau_i = 3 sqrt(m_i) (k T)^(3/2)/(4 sqrt(pi) n Z^4 e^4 ln Lambda).

    The SAME expression as tau_electron with m_e -> m_p, except for the
    sqrt(2): Braginskii's ion time has 4 sqrt(pi) where the electron time
    has 4 sqrt(2 pi).  At T_e = T_i and Z = 1 the ratio is therefore
    tau_i/tau_e = sqrt(2 m_p/m_e) = 60.60, and PART H checks that the
    computed ratio reproduces it.  BOTH FORMS ARE NOW VERIFIED from
    p. 215 of the original translation -- the ion one for Module 10 and
    the electron one at Module 12 step 2.  His denominators are Z^4 n_i
    for the ion and Z^2 n_i for the electron; at Z = 1 both are n.
    """
    return (3.0*np.sqrt(mp)*(kB*T)**1.5
            / (4.0*np.sqrt(np.pi)*n*Z**4*e**4*lnL))


def resistivity(n, T, lnL):
    """Magnetic diffusivity eta = c^2/(4 pi sigma), Spitzer parallel value.

    sigma_par = 1.96 n e^2 tau_e/m_e.  VERIFIED at step 2: his eq. (2.7)
    on p. 216 gives sigma_perp = e^2 n_e tau_e/m_e and his eq. (2.8) on
    the same page gives sigma_par = 1.96 sigma_perp, at Z = 1.  So

        eta = c^2 m_e / (4 pi * 1.96 n e^2 tau_e).

    n cancels against the n inside tau_e, so eta depends on T and ln
    Lambda alone -- which is the whole point, and the reason a bigger
    plasma is a better conductor only through its SIZE.
    """
    tau = tau_electron(n, T, lnL)
    return c*c*me/(4.0*np.pi*BRAG_SIGMA_PAR*n*e*e*tau)


def debye(n, T):
    """Electron Debye length sqrt(k T/(4 pi n e^2)).  From m01_numbers.py
    by way of m10_numbers.py."""
    return np.sqrt(kB*T/(4.0*np.pi*n*e*e))


def b_min_e(T):
    """Smallest usable impact parameter for electrons: the larger of the
    classical 90-degree impact parameter e^2/(3 k T) and the thermal de
    Broglie length.  From m01_numbers.py by way of m10_numbers.py."""
    ve = np.sqrt(3.0*kB*T/me)
    return max(e*e/(3.0*kB*T), hbar/(me*ve))


def lnLambda_e(n, T):
    """Coulomb logarithm ln(lambda_D/b_min).  From m01_numbers.py.

    COPIED, not retyped.  The first draft of this file wrote the quantum
    branch as hbar/(2 sqrt(3 k T m_e)), a factor of two smaller than
    hbar/(m_e v_e) with v_e = sqrt(3 k T/m_e).  It is the same defect as
    the lam_coulomb pi and the gyroradius speed, for the third time in
    one file, and it is why the rule is COPY and not RE-DERIVE.
    """
    return np.log(debye(n, T)/b_min_e(T))


def magnetic_reynolds(U, L, eta):
    """Rm = U L/eta, the ratio of the induction to the diffusion term."""
    return U*L/eta


def diffusion_time(L, eta):
    """t_diff = L^2/eta, the ohmic decay time of a structure of size L."""
    return L*L/eta


# =========================================================================
# PART E.  The Parker spiral
# =========================================================================

def parker_ratio(r, v, omega, r0=0.0):
    """-B_phi/B_r = omega (r - r0) sin(theta)/v, at sin(theta) = 1.

    The equatorial plane is taken throughout, which is where Helios flew.
    r0 is the source surface, below which the field is held radial.
    """
    return omega*(r - r0)/v


def parker_field_index(r, v, omega, r0=0.0, dlnv_dlnr=0.0):
    """Local d ln|B|/d ln r for a Parker spiral.

    |B| = B_r sqrt(1 + (B_phi/B_r)^2) with B_r ~ r^-2 exactly, from
    div B = 0 on a radial field.  Writing x = omega (r - r0)/v,

        d ln|B|/d ln r = -2 + x^2/(1 + x^2) * d ln x/d ln r,

    and d ln x/d ln r = r/(r - r0) - d ln v/d ln r.  At r0 = 0 and a
    constant wind speed this is the familiar -2 + x^2/(1 + x^2), which
    runs from -2 close in to -1 far out.
    """
    x = parker_ratio(r, v, omega, r0)
    dlnx = r/(r - r0) - dlnv_dlnr
    return -2.0 + x*x/(1.0 + x*x)*dlnx


def parker_field(r, v1, omega, r1, r0=0.0, alpha_v=0.0):
    """|B|(r)/|B|(r1) for a Parker spiral with v(r) = v1 (r/r1)^alpha_v.

    Returns the shape only; the normalisation cancels in a log-log fit.
    """
    v = v1*(r/r1)**alpha_v
    x = parker_ratio(r, v, omega, r0)
    x1 = parker_ratio(r1, v1, omega, r0)
    return (r/r1)**PARKER_BR_INDEX*np.sqrt(1.0 + x*x)/np.sqrt(1.0 + x1*x1)


def loglog_fit_index(r, y):
    """Least-squares slope of ln y against ln r.

    This is what a published power-law fit reports, and it is NOT the
    local logarithmic derivative at any one radius.  Comparing a local
    slope with a fitted exponent over a wide range is the error this
    function exists to prevent.
    """
    lr, ly = np.log(r), np.log(y)
    return float(np.polyfit(lr, ly, 1)[0])


def spiral_angle(r, v, omega, r0=0.0):
    """Angle between the field and the radial direction, in degrees."""
    return math.degrees(math.atan(parker_ratio(r, v, omega, r0)))


# =========================================================================
# PART F.  The Alfven radius
# =========================================================================

def alfven_radius_constant_v(r1, v, vA1):
    """Radius where v = v_A, for v_A ~ 1/r and a constant wind speed.

    With B_r ~ r^-2 from div B = 0 and rho ~ r^-2 from mass conservation
    at constant v, v_A = B/sqrt(4 pi rho) ~ r^-1 exactly.  Setting
    v_A(r_A) = v then gives r_A = r1 v_A(r1)/v.

    THE ASSUMPTION IS THE CONSTANT SPEED, and Module 9 measured that it
    is false: Venzmer & Bothmer's velocity exponent is +0.049 (mean) or
    +0.058 (median), so the wind is still accelerating at 1 au.  This
    function is therefore an extrapolation whose failure is the result.
    """
    return r1*vA1/v


def alfven_radius_power_law(r1, v1, vA1, alpha_v):
    """Same crossing with v(r) = v1 (r/r1)^alpha_v and v_A ~ r^(-2+alpha_v).

    Mass conservation with a varying speed gives rho ~ r^-2 v^-1, so
    v_A ~ B/sqrt(rho) ~ r^-2 / r^-1 v^(-1/2) = r^-1 v^(1/2), i.e.
    v_A(r) = vA1 (r/r1)^(-1 + alpha_v/2).  Setting it equal to v(r):

        (r/r1)^(-1 - alpha_v/2) = v1/vA1.
    """
    return r1*(v1/vA1)**(-1.0/(1.0 + alpha_v/2.0))


# =========================================================================
# PART G.  Magnetic support against collapse
# =========================================================================

def mass_to_flux_critical(c_phi):
    """(M/Phi)_crit = c_phi/sqrt(G), in g per maxwell."""
    return c_phi/np.sqrt(G)


def magnetic_critical_mass(B, R, c_phi):
    """M_Phi = c_phi Phi/sqrt(G) with Phi = pi R^2 B."""
    return c_phi*np.pi*R*R*B/np.sqrt(G)


def mass_to_flux_ratio(M, B, R, c_phi):
    """lambda = (M/Phi)/(M/Phi)_crit.  Above 1 the cloud cannot be held."""
    return M/(np.pi*R*R*B)/mass_to_flux_critical(c_phi)


# =========================================================================
# PART H.  Transport across a field
# =========================================================================

def conduction_suppression(omega_tau, par=BRAG_KAPPA_PAR_E,
                           perp=BRAG_KAPPA_PERP_E):
    """kappa_perp/kappa_par = (perp/par)/(omega_c tau)^2.

    The same SQUARED form Module 10 used for the viscosity, and for the
    same reason: the step across the field shrinks to a gyroradius while
    the randomisation time is still the collision time.  Both
    coefficients are VERIFIED at step 2 from Braginskii pp. 216-217,
    eqs. (2.12) and (2.13), at Z = 1.
    """
    return (perp/par)/(omega_tau*omega_tau)


def viscosity_suppression(omega_tau):
    """nu_perp/nu_par from Braginskii's ion coefficients, both VERIFIED.

    eta_1^i/eta_0^i = (3/10)/0.96 (omega_i tau_i)^-2, read from p. 218 of
    the original translation for Module 10 and reused unchanged.
    """
    return (BRAG_ETA1_ION/BRAG_ETA0_ION)/(omega_tau*omega_tau)


# =========================================================================
# PART I.  The magnetorotational instability
# =========================================================================

def mri_growth_rate(omega, q=KEPLER_Q):
    """Maximum MRI growth rate, gamma_max = (q/2) Omega.

    q = -d ln Omega/d ln R.  Keplerian q = 3/2 gives (3/4) Omega, which
    is the number module08.html:728 is promised.  THE SHEAR IS ASSUMED,
    not derived: a disc model is Module 11.
    """
    return 0.5*q*omega


def mri_wavelength_max(vA, omega):
    """Wavelength of the fastest-growing mode, 2 pi v_A/(sqrt(15)/4 Omega)."""
    return 2.0*np.pi*vA/(MRI_KMAX_FACTOR*omega)


def mri_wavelength_crit(vA, omega):
    """Longest stable wavelength: marginal at k v_A = sqrt(3) Omega."""
    return 2.0*np.pi*vA/(MRI_KCRIT_FACTOR*omega)


def kepler_omega(M, R):
    """Omega_K = sqrt(G M/R^3)."""
    return np.sqrt(G*M/R**3)


# =========================================================================
# THE CENSUS, AT MODULE SCOPE.  m12_build_figs.py imports these, so the
# figures and the prose cannot diverge -- which is m10_build_figs.py's
# fluid_rows() rule applied to the census instead of to the functions.
# =========================================================================

# Module 1's photosphere: n = P/kT at tau = 2/3, P = 1.2e5 dyn/cm^2.
n_phot = 1.2e5/(kB*5772.0)
# The photospheric field is the QUIET-SUN mean, not a spot.  STILL
# UNSOURCED AFTER STEP 2; a spot is 3000 G and the difference is four
# decades in beta, which is why the row is labelled and not averaged.
# The NASA NSSDC Sun Fact Sheet, read at step 2, prints polar 1-2 G,
# sunspots 3000 G, prominences 10-100 G, plages 200 G and bright
# chromospheric network 25 G, and NO quiet-Sun mean and NO coronal
# value.  Gate D either sources these two rows or relabels them as
# order-of-magnitude census entries with no check on them.
B_phot = 5.0                     # G, quiet Sun   STILL UNSOURCED
T_phot = 5772.0
MU_PHOT = 1.30                   # Module 10's photosphere row
# Corona: Module 1's values for the 1e6 K corona.
n_cor, T_cor = 1.0e9, 1.0e6
B_cor = 10.0                     # G, active region  UNSOURCED
# Solar wind at 1 au: Module 1's census, reused by Module 10.
n_sw, T_sw, B_sw = 5.0, 1.2e5, 5.0e-5
# ICM: Module 10's values, including the one-microgauss field whose
# factor of ten the Module 10 editor pass caught.  ONE microgauss.
n_icm, T_icm, lnL_icm = 1.0e-3, 1.0e8, 37.8
B_icm = 1.0e-6
# Molecular cloud: Module 10's 10 pc cloud.  THE FIELD IS STILL
# UNSOURCED AFTER STEP 2 and Gate D must settle it.  Crutcher (2012)
# is paywalled and was not read.  Troland & Crutcher (2008) WAS
# read, and it gives a total mean |B| of 16.4 microgauss -- but at
# n(H2) of a few times 10^3 cm^-3, thirty times the density of this
# row, so it is not a source for 10 microgauss at n = 1e2 cm^-3.
# Nothing is checked against B_mc; PART G checks the critical ratio
# and not this cloud's lambda.
# n = 1e2 cm^-3 at mu = 2.33, COPIED FROM m10_numbers.py:802 so the two
# modules cannot diverge.  The first draft of this file wrote 2e2 under
# a comment converting an H2 density to a total, which double-counted
# against mu = 2.33 and moved beta by a factor of two.
n_mc, T_mc = 1.0e2, 10.0
B_mc = 1.0e-5                    # 10 microgauss  STILL UNSOURCED

A_ROWS = [
    ('solar photosphere', n_phot, T_phot, B_phot, MU_PHOT),
    ('solar corona', n_cor, T_cor, B_cor, 0.61),
    ('solar wind, 1 au', n_sw, T_sw, B_sw, 0.61),
    ('intracluster medium', n_icm, T_icm, B_icm, MU_ICM),
    ('molecular cloud', n_mc, T_mc, B_mc, 2.33),
]


def main():
    P = print
    P('=' * 74)
    P('MODULE 12 NUMBERS: magnetohydrodynamics')
    P('=' * 74)
    P('STEPS 1 AND 2 OF SIX.  Every constant in the source is now marked')
    P('VERIFIED with the page it was read from, except the three census')
    P('fields of PART A and Crutcher (2012), which is paywalled and was')
    P('NOT READ; PART G checks against Troland & Crutcher (2008)')
    P('instead, which was fetched and read.  See')
    P('.ignore/m12-source-verification.md.')

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  Is the fluid magnetised?  Three questions, three numbers')
    P('-'*74)
    P('  beta = 8 pi n k T/B^2 asks whether the field can push the gas.')
    P('  v_A/c_s = sqrt(2/(gamma beta)) asks how fast the news travels.')
    P('  omega_c tau asks whether a particle completes a gyro-orbit')
    P('  between collisions - the question Module 1 raised and left open.')
    P('  Every row reuses Module 1 and Module 10 census inputs unchanged.')
    P('')
    P(f'  {"system":<24} {"n (cm^-3)":>10} {"T (K)":>9} {"B (G)":>9} '
      f'{"beta":>10} {"v_A (km/s)":>11}')

    beta_of = {}
    vA_of = {}
    for name, n, T, B, mu in A_ROWS:
        rho = n*mu*mu_u
        beta = plasma_beta(n, T, B)
        vA = alfven_speed(B, rho)
        beta_of[name] = beta
        vA_of[name] = vA
        P(f'  {name:<24} {n:>10.3g} {T:>9.3g} {B:>9.2g} '
          f'{beta:>10.3g} {vA/1e5:>11.4g}')
    P('')
    P('  WHERE EACH FIELD COMES FROM.  GATE D RULED: this column is an')
    P('  ORDER-OF-MAGNITUDE CENSUS and nothing in the module is')
    P('  checked against any of its five entries.  beta spans five')
    P('  decades down the column and no row\'s verdict turns on a')
    P('  factor of two.')
    P('    photosphere        5 G      UNSOURCED.  The NSSDC fact')
    P('                               sheet, which WAS read, prints')
    P('                               polar 1-2 G, sunspots 3000 G,')
    P('                               prominences 10-100 G, plages')
    P('                               200 G, bright network 25 G --')
    P('                               and none of them is this.')
    P('    corona            10 G      module07.html:746 prints "an')
    P('                               active-region corona of 10')
    P('                               gauss" and says "the number is')
    P('                               this module\'s", so it is')
    P('                               illustrative there too.')
    P('    solar wind      5 nT       Module 1\'s census, reused')
    P('                               unchanged by module10.html:506.')
    P('    intracluster     1 uG      module10.html:452 and its')
    P('                               Problem D1.')
    P('    cloud           10 uG      UNSOURCED AT THIS DENSITY.')
    P('                               Troland & Crutcher give a mean')
    P('                               |B| of 16.4 uG at n(H2) of a')
    P('                               few times 10^3 cm^-3, thirty')
    P('                               times this row.')
    P('')
    P('  The mean molecular weight used in rho for each row, so that the')
    P('  Alfven speed is a speed and not a convention:')
    for name, n, T, B, mu in A_ROWS:
        P(f'    {name:<24} mu = {mu}')
    P('')
    P('  v_A/c_s = sqrt(2/(gamma beta)) at gamma = 5/3, checked against')
    P('  the ratio of the two speeds computed separately.  If these two')
    P('  columns ever disagree, one of the mu values above has been')
    P('  changed in one place and not the other.')
    P(f'  {"system":<24} {"c_s (km/s)":>11} {"v_A/c_s":>10} '
      f'{"sqrt(2/g beta)":>15} {"ratio":>8}')
    for name, n, T, B, mu in A_ROWS:
        cs = sound_speed(T, mu)
        direct = vA_of[name]/cs
        identity = np.sqrt(2.0/((5.0/3.0)*beta_of[name]))
        P(f'  {name:<24} {cs/1e5:>11.4g} {direct:>10.4g} '
          f'{identity:>15.4g} {direct/identity:>8.4f}')
    P('')
    P('  WHY THE IDENTITY IS EXACT.  v_A^2/c_s^2 = (B^2/4 pi rho)/')
    P('  (gamma p/rho) = B^2/(4 pi gamma p) = 2/(gamma beta).  rho')
    P('  cancels, so the mu in the Alfven speed and the mu in the sound')
    P('  speed cancel against each other.  The ratio is a property of the')
    P('  field and the pressure alone.  THIS IS WHY beta IS THE VARIABLE')
    P('  and not v_A: v_A needs a mass per particle and beta does not.')

    # --- omega_c tau, the magnetisation proper.
    P('')
    P('  (a) omega_c tau, the magnetisation.  Module 1 asked whether the')
    P('      gyroradius replaces the mean free path; this is the same')
    P('      question as a pure number.  omega_i tau_i = lam/r_g when')
    P('      tau = lam/v and r_g = v/omega, so the two forms must agree.')
    lam_icm = lam_coulomb(n_icm, T_icm, lnL_icm)
    rg_icm = gyroradius(T_icm, B_icm)
    om_icm = gyrofrequency(B_icm)
    # THE SPEED MUST BE THE SAME SPEED IN BOTH FORMS.  r_g = v/omega with
    # v = sqrt(2 k T/m), so tau = lam/v must use sqrt(2 k T/m) too or the
    # identity omega tau = lam/r_g fails by a factor of order one and the
    # check below stops being a check.  Module 10's VISCOSITY uses the
    # mean speed sqrt(8 k T/pi m) instead, and the two are printed side by
    # side so the difference is visible rather than silently inherited.
    v_2kT = np.sqrt(2.0*kB*T_icm/mp)
    v_mean = v_thermal(T_icm, MU_H)
    tau_icm = lam_icm/v_2kT
    n_gyro = lam_icm/rg_icm
    P(f'      ICM Coulomb mean free path lam     = {lam_icm/kpc:.1f} kpc '
      f'(Module 1 and Module 10: 22.5 kpc)')
    P(f'      sqrt(2kT/m_p)                      = {v_2kT/1e5:.0f} km/s')
    P(f'      mean speed sqrt(8kT/pi m_p)        = {v_mean/1e5:.0f} km/s '
      f'(ratio {v_mean/v_2kT:.4f} = sqrt(4/pi))')
    P(f'      ICM proton gyroradius r_g at 1 uG  = {rg_icm/1e5:.3e} km')
    P(f'      lam/r_g                            = {n_gyro:.4e}')
    P(f'      omega_i tau_i, computed separately = '
      f'{om_icm*tau_icm:.4e}')
    P(f'      ratio of the two forms             = '
      f'{(om_icm*tau_icm)/n_gyro:.6f}')
    P(f'      log10(lam/r_g)                     = '
      f'{np.log10(n_gyro):.2f}')
    P(f'      An ICM proton completes 10^{np.log10(n_gyro):.2f} gyro-orbits '
      f'between')
    P('      collisions.  THE EXPONENT IS PRINTED AND NOT WRITTEN INTO A')
    P('      SENTENCE: Module 10 step 4 found three wrong')
    P('      order-of-magnitude claims in prose that no check reads, and')
    P('      "twelve orders" and "thirteen orders" are both wrong for')
    P(f'      {np.log10(n_gyro):.2f}.  This is the answer to the question '
      f'Module 1 left')
    P('      open.')
    P('      GATE D RULED: THIS NUMBER IS A COUNT OF GYRO-ORBITS AND')
    P('      NOT THE MAGNETISATION OF DEFINITION 2.  The module\'s')
    P('      omega_c tau is Braginskii\'s, because PART H\'s transport')
    P('      coefficients 1.96, 3.16, 4.66, 3.9 and 2 are DEFINED on')
    P('      his tau.  PART H prints the two side by side and')
    P('      decomposes the ratio exactly.')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  The induction equation, and why flux freezing is not an')
    P('         assumption but a measurement of Rm')
    P('-'*74)
    P('  dB/dt = curl(u x B) + eta grad^2 B, with eta = c^2/(4 pi sigma).')
    P('  The ratio of the two terms is Rm = U L/eta.  eta depends on T')
    P('  and ln Lambda ONLY - the density cancels between sigma and')
    P('  tau_e - so a large plasma is a good conductor through its SIZE.')
    P('  ALL FOUR NUMBERS IN THIS PART USE Braginskii\'s sigma = 1.96 n')
    P('  e^2 tau_e/m_e, VERIFIED at step 2 from his eqs. (2.7) and')
    P('  (2.8) on p. 216 of the Consultants Bureau translation, Z = 1.')
    P('')
    P(f'  {"system":<24} {"T (K)":>9} {"ln Lam":>7} {"eta (cm^2/s)":>13} '
      f'{"L (cm)":>10} {"Rm":>11}')
    # (name, n, T, L, U).  L and U are each named in the text below; none
    # of them is checked against anything, and the Rm they give is an
    # order of magnitude, not a measurement.
    #   corona          a 100 Mm loop at 10 km/s
    #   solar wind      1 au at Module 1's census speed, 400 km/s
    #   ICM             Hitomi's 60 kpc at Module 10's 164 km/s
    #   molecular cloud Module 10's 10 pc at Larson's 2.64 km/s
    B_ROWS = [
        ('solar corona', n_cor, T_cor, 1.0e10, 1.0e6),
        ('solar wind, 1 au', n_sw, T_sw, AU, 4.0e7),
        ('intracluster medium', n_icm, T_icm, 60.0*kpc, 1.64e7),
        ('molecular cloud', n_mc, T_mc, 10.0*pc, 2.64e5),
    ]
    for name, n, T, L, U in B_ROWS:
        lnL = lnLambda_e(n, T)
        eta = resistivity(n, T, lnL)
        Rm = magnetic_reynolds(U, L, eta)
        P(f'  {name:<24} {T:>9.3g} {lnL:>7.2f} {eta:>13.4e} '
          f'{L:>10.3e} {Rm:>11.3e}')
    P('')
    P('  THE MOLECULAR CLOUD ROW IS WRONG AND IS PRINTED ANYWAY, because')
    P('  the reason it is wrong is the physics.  A 10 K cloud is not')
    P('  fully ionised; its resistivity is set by ion-neutral collisions')
    P('  (ambipolar diffusion), not by electron-ion ones, and the Spitzer')
    P('  formula above is a formula outside its domain in exactly the')
    P('  sense Module 10 Proposition 6 names.  GATE D RULED: THE')
    P('  MODULE REFUSES THE ROW IN PRINT AND DOES NOT DERIVE')
    P('  AMBIPOLAR DIFFUSION.  The refusal is made ONCE, here, and')
    P('  cross-referenced twice: PART I\'s protoplanetary disc is')
    P('  very nearly neutral for the same reason, and PART G\'s')
    P('  mass-to-flux criterion is an EQUILIBRIUM statement whose')
    P('  missing mechanism is exactly this -- a subcritical cloud')
    P('  leaks flux and becomes supercritical.  The captures/misses')
    P('  row reads "ideal Ohm\'s law: no ambipolar diffusion, no')
    P('  Hall term", repaid by NOBODY in this book.  NOTHING IS')
    P('  CHECKED AGAINST THIS ROW.')
    P('')
    P('  (a) Ohmic decay times L^2/eta, against EACH SYSTEM\'S OWN')
    P('      dynamical time L/U.  Comparing a coronal diffusion time')
    P('      with the age of the universe would be meaningless; the')
    P('      comparison that means something is with the time the system')
    P('      takes to do anything.  And the ratio of the two IS Rm:')
    P('      (L^2/eta)/(L/U) = U L/eta identically, so the last column')
    P('      below must reproduce the Rm column above to rounding.  If it')
    P('      ever stops doing so, one of the two has been edited alone.')
    P('')
    P(f'      {"system":<24} {"t_diff (yr)":>12} {"L/U (yr)":>12} '
      f'{"ratio":>11}')
    ratios = {}
    for name, n, T, L, U in B_ROWS:
        lnL = lnLambda_e(n, T)
        eta = resistivity(n, T, lnL)
        t = diffusion_time(L, eta)
        t_dyn = L/U
        ratios[name] = t/t_dyn
        P(f'      {name:<24} {t/yr:>12.3e} {t_dyn/yr:>12.3e} '
          f'{t/t_dyn:>11.3e}')
    worst = min(ratios, key=ratios.get)
    P('      THAT IS FLUX FREEZING: not an idealisation adopted for')
    P('      convenience but a ratio that has been computed.  The')
    P(f'      smallest of the four is the {worst}, at '
      f'{ratios[worst]:.3e},')
    P(f'      which is {np.log10(ratios[worst]):.1f} decades.  The word')
    P('      "decades" is printed beside the exponent that produced it.')

    # ---------------------------------------------------------------- C
    P('')
    P('PART C.  Magnetic pressure and tension')
    P('-'*74)
    P('  The Lorentz force density (1/c) j x B = (1/4pi)(curl B) x B')
    P('  splits into -grad(B^2/8pi) and (B.grad)B/4pi.  The first is an')
    P('  isotropic pressure; the second is a tension B^2/4pi along the')
    P('  field, with a force per volume B^2/(4 pi R_c) toward the centre')
    P('  of curvature.  This is what module02.html:687 and')
    P('  module03.html:793 are promised, and what module07.html:352 asks')
    P('  for as a Kelvin-Helmholtz cut-off.')
    P('')
    P(f'  {"system":<24} {"p_gas":>12} {"p_mag":>12} {"p_mag/p_gas":>12}')
    for name, n, T, B, mu in A_ROWS:
        pg = n*kB*T
        pm = magnetic_pressure(B)
        P(f'  {name:<24} {pg:>12.4e} {pm:>12.4e} {pm/pg:>12.4e}')
    P('      p_mag/p_gas is 1/beta by construction; the column is printed')
    P('      so that a reader can see the two pressures as pressures.')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  Wave speeds, and Module 7\'s one-degree bound recomputed')
    P('-'*74)
    P('  The three MHD wave speeds at an angle theta to the field:')
    P('    Alfven:      v_A cos(theta)')
    P('    fast/slow:   v^2 = (1/2)(v_A^2 + c_s^2) +/-')
    P('                 (1/2) sqrt((v_A^2 + c_s^2)^2 - 4 v_A^2 c_s^2')
    P('                 cos^2(theta))')
    P('  At theta = 0 the fast speed is max(v_A, c_s) and the slow is')
    P('  min(v_A, c_s); at theta = 90 deg the slow speed and the Alfven')
    P('  speed both vanish and only the fast magnetosonic wave survives,')
    P('  at sqrt(v_A^2 + c_s^2).  THIS IS WHAT MODULE 4 IS PROMISED at')
    P('  module04.html:569.')
    P('')
    P(f'  {"system":<24} {"c_s":>9} {"v_A":>9} {"fast(90d)":>10} '
      f'{"fast(0d)":>9} {"slow(0d)":>9}')
    for name, n, T, B, mu in A_ROWS:
        cs = sound_speed(T, mu)
        vA = vA_of[name]
        fast90 = np.sqrt(vA*vA + cs*cs)
        P(f'  {name:<24} {cs/1e5:>9.4g} {vA/1e5:>9.4g} '
          f'{fast90/1e5:>10.4g} {max(vA, cs)/1e5:>9.4g} '
          f'{min(vA, cs)/1e5:>9.4g}')
    P('      All speeds in km/s.')
    P('')
    P('  (a) Module 7\'s one-degree bound, recomputed from this module\'s')
    P('      own dispersion relation.  module07.html:748 says the debt in')
    P('      one line: "A purely hydrodynamic calculation that needs a')
    P('      one-degree statement about a field it never mentions is a')
    P('      calculation waiting for magnetohydrodynamics."  Module 7')
    P('      Proposition 9 (module07.html, section 9.5) states it as')
    P('        B cos(theta) < Delta_U sqrt(2 pi rho_t rho_b/(rho_t+rho_b))')
    P('      for equal fields on both sides, with 4 pi for a one-sided')
    P('      field.  THE THREE INPUTS ARE READ OUT OF module07.html, not')
    P('      recalled: n_e, mu_e and the density ratio from the')
    P('      provenance note at :638, and Delta_U from the sentence that')
    P('      calls 20 km/s "the shear measured on the flank of a coronal')
    P('      mass ejection".  The bound is then computed, not copied, so')
    P('      the comparison below can fail.')
    # module07.html:638: rho_h = mu_e n_e m_u at n_e = 3e8 cm^-3,
    # mu_e = 2/(1+X) = 1.1765 at X = 0.70, and rho_l = rho_h/2.236.
    M07_NE = 3.0e8
    M07_MU_E = 1.1765
    M07_DENSITY_RATIO = 2.236
    # module07.html prints it as a measurement: "Delta U = 20 km/s is the
    # shear measured on the flank of a coronal mass ejection".  It is READ
    # FROM THAT SENTENCE, not back-solved from the bound; a bound divided
    # by its own prefactor would reproduce itself and could not fail.
    M07_DU = 2.0e6                  # cm/s
    M07_BOUND_TWO_SIDED = 0.0675    # G, module07.html section 9.5
    M07_BOUND_ONE_SIDED = 0.0954    # G, same box
    rho_h = M07_MU_E*M07_NE*mu_u
    rho_l = rho_h/M07_DENSITY_RATIO
    pref = np.sqrt(2.0*np.pi*rho_h*rho_l/(rho_h + rho_l))
    b_two = M07_DU*pref
    b_one = M07_DU*pref*np.sqrt(2.0)
    P(f'      rho_h = {rho_h:.4e} g/cm^3 (module07.html:638 prints '
      f'5.8607e-16)')
    P(f'      rho_l = {rho_l:.4e} g/cm^3 (module07.html:638 prints '
      f'2.6210e-16)')
    P(f'      Delta_U = {M07_DU/1e5:.1f} km/s, an UPPER LIMIT')
    P(f'      B cos(theta) <  {b_two:.5f} G  (both sides; Module 7 prints '
      f'{M07_BOUND_TWO_SIDED})')
    P(f'      B cos(theta) <  {b_one:.5f} G  (one side;   Module 7 prints '
      f'{M07_BOUND_ONE_SIDED})')
    P(f'      ratio recomputed/printed = {b_two/M07_BOUND_TWO_SIDED:.4f} '
      f'and {b_one/M07_BOUND_ONE_SIDED:.4f}')
    P('      The angle, which is the form that carries the argument:')
    P(f'        {"total B (G)":>12} {"cos(theta) <":>13} '
      f'{"within (deg)":>13} {"M7 prints":>10}')
    M07_ANGLES = {1.0: 3.87, 2.0: 1.93, 5.0: 0.77, 10.0: 0.39, 50.0: 0.08}
    for B_tot, printed in M07_ANGLES.items():
        ct = b_two/B_tot
        # The table's angle is measured FROM PERPENDICULAR to B, so it is
        # 90 - arccos(ct) = arcsin(ct), not arccos(ct).
        within = math.degrees(math.asin(min(ct, 1.0)))
        P(f'        {B_tot:>12.1f} {ct:>13.5f} {within:>13.2f} '
          f'{printed:>10.2f}')
    P('      The right-hand column is read off Module 7\'s own table in')
    P('      section 9.5; the check is that the two agree.  The angle is')
    P('      measured FROM PERPENDICULAR to B, so it is arcsin(cos theta)')
    P('      and not arccos(cos theta) - a 90-degree error that would')
    P('      have gone unnoticed if Module 7 had not printed the table.')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  CHECK 1, THE ANCHOR.  The Parker spiral')
    P('-'*74)
    P('  Flux freezing plus a radial wind winds the field into a spiral.')
    P('  B_r r^2 is constant from div B = 0 alone.  B_phi/B_r =')
    P('  -Omega (r - r0)/v from the kinematics of a field line whose foot')
    P('  rotates.  NOTHING IS FITTED: Omega is the solar rotation rate')
    P('  and v is Module 9\'s wind speed, both already in this book.')
    omega_sun = 2.0*np.pi/(CARRINGTON_SIDEREAL_DAYS*day)
    omega_eq = 2.0*np.pi/(EQUATORIAL_SIDEREAL_DAYS*day)
    r0 = R_SOURCE_SURFACE*Rsun
    P('')
    P(f'  Omega (Carrington sidereal, {CARRINGTON_SIDEREAL_DAYS} d)  = '
      f'{omega_sun:.5e} rad/s')
    P(f'  Omega (equatorial sidereal, {EQUATORIAL_SIDEREAL_DAYS} d) = '
      f'{omega_eq:.5e} rad/s   ({omega_eq/omega_sun:.4f} times)')
    P(f'  source surface r0                    = '
      f'{R_SOURCE_SURFACE} R_sun = {r0/AU:.5f} au')

    # Everything the punchline quotes is stored here and f-stringed into
    # it, so no number appears in the prose that the run did not produce.
    # Module 10 step 4 found three wrong order-of-magnitude claims in
    # prose precisely because they were typed rather than printed.
    E = {}
    for label, fits in (('mean', VB18_MEAN), ('median', VB18_MEDIAN)):
        v1 = fits['velocity'][0]*1e5
        alpha_v = fits['velocity'][2]
        b_idx, b_err = fits['field'][2], fits['field'][3]
        P('')
        P(f'  ({label} fits)  v(1 au) = {fits["velocity"][0]} km/s, '
          f'v ~ r^{alpha_v:+.3f}')
        x1 = parker_ratio(AU, v1, omega_sun, r0)
        P(f'    -B_phi/B_r at 1 au                 = {x1:.4f}')
        P(f'    spiral angle at 1 au               = '
          f'{spiral_angle(AU, v1, omega_sun, r0):.2f} deg')
        P(f'    local d ln|B|/d ln r at 1 au       = '
          f'{parker_field_index(AU, v1, omega_sun, r0, alpha_v):+.4f}')
        r_lo = VB18_R_LO_AU*AU
        v_lo = v1*VB18_R_LO_AU**alpha_v
        P(f'    local d ln|B|/d ln r at 0.29 au    = '
          f'{parker_field_index(r_lo, v_lo, omega_sun, r0, alpha_v):+.4f}')
        # The fitted index over the SAME window the paper fitted.
        rgrid = np.exp(np.linspace(np.log(VB18_R_LO_AU*AU),
                                   np.log(VB18_R_HI_AU*AU), 400))
        shape = parker_field(rgrid, v1, omega_sun, AU, r0, alpha_v)
        idx_fit = loglog_fit_index(rgrid, shape)
        P(f'    FITTED index over {VB18_R_LO_AU}-{VB18_R_HI_AU} au    '
          f'= {idx_fit:+.4f}   <- the number to compare')
        P(f'    measured index (Table 3)           = {b_idx:+.4f} '
          f'+/- {b_err:.3f} (formal)')
        P(f'    year-to-year scatter (their Fig. 9)= '
          f'{VB18_SCATTER["field"]:.3f}')
        gap = idx_fit - b_idx
        P(f'    prediction - measurement           = {gap:+.4f} = '
          f'{abs(gap)/VB18_SCATTER["field"]:.2f} scatter units, '
          f'{abs(gap)/b_err:.1f} formal errors')
        gap_radial = PARKER_BR_INDEX - b_idx
        P(f'    an UNWOUND radial field, -2.000    = {gap_radial:+.4f} = '
          f'{abs(gap_radial)/VB18_SCATTER["field"]:.2f} scatter units, '
          f'{abs(gap_radial)/b_err:.1f} formal errors')
        # The density index in the same row: the control, and also the
        # premise CHECK 2 rests on.  Mass conservation through a sphere
        # gives rho v r^2 = const, so rho ~ r^(-2-alpha_v) and NOT r^-2
        # exactly.  The first draft compared against -2, which is a
        # rounder statement about a different prediction.
        d_idx, d_err = fits['density'][2], fits['density'][3]
        d_pred = -2.0 - alpha_v
        P(f'    CONTROL: the density index in the same row = {d_idx:+.4f} '
          f'+/- {d_err:.3f}')
        P(f'      mass conservation predicts -2 - alpha_v = {d_pred:+.4f}')
        P(f'      gap {abs(d_idx - d_pred):.4f} = '
          f'{abs(d_idx - d_pred)/VB18_SCATTER["density"]:.2f} scatter '
          f'units, {abs(d_idx - d_pred)/d_err:.2f} formal errors')
        P(f'      against -2 exactly, for comparison: '
          f'{abs(d_idx + 2.0):.4f} = '
          f'{abs(d_idx + 2.0)/VB18_SCATTER["density"]:.2f} scatter units')
        E[label] = {
            'fit': idx_fit,
            'scat': abs(gap)/VB18_SCATTER['field'],
            'formal': abs(gap)/b_err,
            'radial_scat': abs(gap_radial)/VB18_SCATTER['field'],
            'err': b_err,
            'dens_scat': abs(d_idx - d_pred)/VB18_SCATTER['density'],
            'dens_pred': d_pred,
        }

    P('')
    P('  PUNCHLINE CHECK 1, AND THE VERDICT IS NOT FIXED AT STEP 1.')
    P(f'  On the MEDIAN fits the Parker prediction lands '
      f'{E["median"]["scat"]:.2f} year-to-year')
    P('  scatters from the measured index with nothing adjusted, while an')
    P(f'  unwound radial field is {E["median"]["radial_scat"]:.2f} away.  '
      f'On the MEAN fits the same')
    P(f'  two numbers are {E["mean"]["scat"]:.2f} and '
      f'{E["mean"]["radial_scat"]:.2f}.  The CONTROL is what makes this')
    P('  a measurement rather than a coincidence: the DENSITY index in')
    P(f'  the same row of the SAME fit set sits '
      f'{E["median"]["dens_scat"]:.2f} scatter units from')
    P(f'  the {E["median"]["dens_pred"]:+.4f} that mass conservation '
      f'predicts, so this data set')
    P('  CAN see a near-inverse-square falloff when there is one.  The')
    P('  field does not show one because it is wound.  THE CONTROL AND')
    P('  THE CHECK NOW USE THE SAME FIT SET; the first draft quoted the')
    P('  median field against the mean density, which is choosing two')
    P('  denominators from one table.')
    P('')
    P('  THE VERDICT DEPENDS ON WHICH ERROR BAR IS USED, AND THAT MUST BE')
    P(f'  SAID BEFORE THE VERDICT.  Against the FORMAL fit error of '
      f'{E["median"]["err"]:.3f}')
    P(f'  the median prediction is {E["median"]["formal"]:.1f} errors away '
      f'and the check is')
    P(f'  REFUTED; against the year-to-year scatter of '
      f'{VB18_SCATTER["field"]:.2f} it is '
      f'{E["median"]["scat"]:.2f}')
    P('  away and the check is CONFIRMED.  The scatter is the defensible')
    P('  choice and Module 9 already made it on this same table, because')
    P('  the formal error describes a regression and the scatter')
    P('  describes the solar wind.  But Gate D must WRITE THAT DOWN and')
    P('  print both numbers in the module, or the check is a choice of')
    P('  denominator presented as a result.')
    P('  A THIRD FRAMING IS AVAILABLE and may be the honest headline: the')
    P('  prediction and the measurement bracket each other far more')
    P('  tightly than either brackets -2.  The wound field is confirmed;')
    P('  the exact winding is not resolved by this data set.')
    P('')
    P('  (a) Sensitivity, priced rather than hidden.')
    v1m = VB18_MEDIAN['velocity'][0]*1e5
    av = VB18_MEDIAN['velocity'][2]
    rgrid = np.exp(np.linspace(np.log(VB18_R_LO_AU*AU),
                               np.log(VB18_R_HI_AU*AU), 400))
    base = loglog_fit_index(rgrid,
                            parker_field(rgrid, v1m, omega_sun, AU, r0, av))
    variants = [
        ('equatorial Omega, 24.47 d',
         parker_field(rgrid, v1m, omega_eq, AU, r0, av)),
        ('source surface 2.0 R_sun',
         parker_field(rgrid, v1m, omega_sun, AU, 2.0*Rsun, av)),
        ('source surface 3.0 R_sun',
         parker_field(rgrid, v1m, omega_sun, AU, 3.0*Rsun, av)),
        ('r0 = 0 (the textbook form)',
         parker_field(rgrid, v1m, omega_sun, AU, 0.0, av)),
        ('constant wind speed',
         parker_field(rgrid, v1m, omega_sun, AU, r0, 0.0)),
        ('mean-fit wind speed, 435.6 km/s',
         parker_field(rgrid, VB18_MEAN['velocity'][0]*1e5, omega_sun, AU,
                      r0, VB18_MEAN['velocity'][2])),
    ]
    P(f'      {"variant":<34} {"index":>9} {"shift":>8}')
    P(f'      {"baseline (median fits)":<34} {base:>+9.4f} {0.0:>8.4f}')
    for name, shape in variants:
        idx = loglog_fit_index(rgrid, shape)
        P(f'      {name:<34} {idx:>+9.4f} {idx - base:>+8.4f}')
    P('      The largest of these shifts is smaller than the year-to-year')
    P('      scatter of 0.11, so the verdict does not turn on any of')
    P('      them.  THAT SENTENCE IS THE POINT OF THE TABLE.')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  CHECK 2.  The Alfven radius, which is BRACKETED by two')
    P('         published values and matches neither')
    P('-'*74)
    P('  With B_r ~ r^-2 and rho ~ r^-2 v^-1, v_A ~ r^-1 v^(1/2).  The')
    P('  wind crosses its own Alfven speed once, and the radius at which')
    P('  it does is measurable.')
    P('')
    P('  THE FIELD IN THIS ALFVEN SPEED IS B_r, NOT |B|, AND THE FIRST')
    P('  DRAFT OF THIS FILE USED |B|.  Two reasons, and either alone')
    P('  settles it.  (i) PART E has just shown that |B| does NOT scale')
    P('  as r^-2; B_r does, by div B = 0, and it is the r^-2 scaling')
    P('  that the extrapolation inward uses.  (ii) The measured quantity')
    P('  is the Weber-Davis Alfven radius, which Verscharen, Bale &')
    P('  Velli define on the RADIAL Alfven speed B_r/sqrt(4 pi rho),')
    P('  because it is the radial components that enter the flow')
    P('  deflection they fit.  Using |B| inflated every r_A below by')
    P('  sqrt(1 + x1^2), where x1 = -B_phi/B_r at 1 au is of order one -')
    P('  a factor near 1.44, which is most of what the first draft')
    P('  reported as a "factor of two".')
    for label, fits in (('mean', VB18_MEAN), ('median', VB18_MEDIAN)):
        n1 = fits['density'][0]
        v1 = fits['velocity'][0]*1e5
        av = fits['velocity'][2]
        B_tot = fits['field'][0]*1e-5      # nT -> gauss: 1 nT = 1e-5 G
        x1 = parker_ratio(AU, v1, omega_sun, r0)
        wind_factor = np.sqrt(1.0 + x1*x1)
        B1 = B_tot/wind_factor             # the RADIAL component at 1 au
        # rho at 1 au.  The 4 per cent helium of Module 9's census raises
        # the mass per proton by a factor 1 + 4*0.04 = 1.16; the row is
        # printed both ways because the choice moves r_A by 8 per cent.
        rho_H = n1*mp
        rho_He = n1*mp*1.16
        vA_H = alfven_speed(B1, rho_H)
        vA_He = alfven_speed(B1, rho_He)
        P('')
        P(f'  ({label} fits)  n = {n1} cm^-3, |B| = {fits["field"][0]} nT, '
          f'v = {fits["velocity"][0]} km/s')
        P(f'    -B_phi/B_r at 1 au (from PART E)   = {x1:.4f}')
        P(f'    sqrt(1 + x1^2)                     = {wind_factor:.4f}')
        P(f'    B_r at 1 au = |B|/sqrt(1+x1^2)     = {B1*1e5:.4f} nT')
        P(f'    v_A(radial) at 1 au, protons only  = {vA_H/1e5:.2f} km/s')
        P(f'    v_A(radial) at 1 au, with 4% He    = {vA_He/1e5:.2f} km/s')
        P(f'    v/v_A at 1 au (protons only)       = {v1/vA_H:.3f}')
        for tag, vA1 in (('protons only', vA_H), ('with 4% He', vA_He)):
            rA_c = alfven_radius_constant_v(AU, v1, vA1)
            rA_p = alfven_radius_power_law(AU, v1, vA1, av)
            P(f'    r_A, constant v   ({tag:<12})  = '
              f'{rA_c/Rsun:.2f} R_sun = {rA_c/AU:.4f} au')
            P(f'    r_A, v ~ r^{av:+.3f} ({tag:<12})  = '
              f'{rA_p/Rsun:.2f} R_sun = {rA_p/AU:.4f} au')
        P(f'    (|B| in place of B_r would give     '
          f'{alfven_radius_power_law(AU, v1, vA_He*wind_factor, av)/Rsun:.2f}'
          f' R_sun, the first draft\'s answer)')
    P('')
    P(f'  MEASURED (Verscharen, Bale & Velli 2021, Table 3, the same')
    P(f'  table module09.html:964 quotes):')
    P(f'    r_A (first fast-latitude scan)     = {VBV21_RA_FLS1:.3f} '
      f'+/- {VBV21_RA_FLS1_ERR:.3f} R_sun')
    P(f'    r_A (third fast-latitude scan)     = {VBV21_RA_FLS3:.3f} '
      f'+/- {VBV21_RA_FLS3_ERR:.3f} R_sun')
    P(f'    their sonic radius, a LOWER limit  = {VBV21_RS:.3f} '
      f'+/- {VBV21_RS_ERR:.3f} R_sun  (a DIFFERENT surface)')
    # The headline ratio, on the median fits with helium.
    n1 = VB18_MEDIAN['density'][0]
    v1 = VB18_MEDIAN['velocity'][0]*1e5
    av1 = VB18_MEDIAN['velocity'][2]
    x1 = parker_ratio(AU, v1, omega_sun, r0)
    B1 = VB18_MEDIAN['field'][0]*1e-5/np.sqrt(1.0 + x1*x1)
    vA1 = alfven_speed(B1, n1*mp*1.16)
    rA_med = alfven_radius_power_law(AU, v1, vA1, av1)/Rsun
    P('')
    P('  PUNCHLINE CHECK 2, AND IT CHANGED WHEN THE RADIAL FIELD WAS PUT')
    P(f'  IN.  The extrapolation gives {rA_med:.2f} R_sun.  Against '
      f'Verscharen, Bale &')
    P(f'  Velli\'s {VBV21_RA_FLS1:.3f} +/- {VBV21_RA_FLS1_ERR:.3f} that is '
      f'a ratio of {rA_med/VBV21_RA_FLS1:.2f}; against Parker Solar')
    P(f'  Probe\'s outermost sub-Alfvenic point, '
      f'{KASPER21_RA_OUTERMOST} R_sun, it is SHORT BY')
    P(f'  a factor of {KASPER21_RA_OUTERMOST/rA_med:.2f}.')
    P('  STEP 2 CORRECTED BOTH THE RANGE AND THE SIGN OF THE')
    P('  COMPARISON.  The prep wrote 19-20 R_sun from memory; Kasper et')
    P('  al. print 16-20 R_sun, over three separate intervals whose')
    P(f'  median Alfven Mach numbers are {KASPER21_MA[0]}, '
      f'{KASPER21_MA[1]} and {KASPER21_MA[2]}.  ALL THREE')
    P('  ARE BELOW 1, so each radius is a point the spacecraft was')
    P('  ALREADY INSIDE the surface, never the surface itself.  The')
    P(f'  outermost, {KASPER21_RA_OUTERMOST} R_sun, is therefore a '
      f'LOWER BOUND: r_A >= 19.8')
    P('  R_sun along that one ray, on that one day.  A MODEL VALUE')
    P(f'  BELOW A LOWER BOUND VIOLATES IT.  {rA_med:.2f} R_sun puts the')
    P(f'  surface {100*(1.0 - rA_med/KASPER21_RA_OUTERMOST):.0f} per '
      f'cent too close to the Sun along interval I1,')
    P('  sits at the edge of I3 (17.7-18.0, M_A = 0.88), and is')
    P('  comfortable only against I2 (16.0, M_A = 0.49).  "Inside their')
    P('  16-20 range" would be true and would mean nothing: that range')
    P('  is a UNION over three longitudes and two days, not a surface')
    P('  anything can be inside of.')
    P('  THE CALCULATION IS THEREFORE BRACKETED BY THE TWO PUBLISHED')
    P(f'  NUMBERS AND MATCHES NEITHER: '
      f'{rA_med/VBV21_RA_FLS1:.2f} times Verscharen, Bale &')
    P(f'  Velli, and {KASPER21_RA_OUTERMOST/rA_med:.2f} times too small '
      f'against PSP I1.  That is the')
    P('  result, and it is a sharper one than an agreement would be.')
    P('  It is why this module may not print one of the two numbers')
    P('  alone.  They are not the same quantity: Verscharen, Bale &')
    P('  Velli fit a steady axisymmetric Weber-Davis surface to Ulysses')
    P('  fast-latitude scans, and Parker Solar Probe reports crossings')
    P('  of a corrugated boundary along one trajectory.  A single')
    P('  spherically symmetric extrapolation cannot match both, and')
    P('  which one it should match is a question about the definition,')
    P('  not about the arithmetic.  BOTH ARE NOW READ - Verscharen for')
    P('  Module 9, Kasper at Module 12 step 2 - and Gate D fixes the')
    P('  verdict before the prose is written.')
    P('')
    P('  TWO EXTRAPOLATIONS ARE PRICED HERE AND NEITHER IS HIDDEN.')
    P(f'  (i) v ~ r^{av1:+.3f} is a fit over {VB18_R_LO_AU}-'
      f'{VB18_R_HI_AU} au and it is being used at')
    P(f'      {rA_med*Rsun/AU:.4f} au, a factor '
      f'{VB18_R_LO_AU/(rA_med*Rsun/AU):.1f} outside its own range.  It '
      f'moves r_A by')
    rA_const = alfven_radius_constant_v(AU, v1, vA1)/Rsun
    P(f'      {100*(rA_med - rA_const)/rA_med:.1f}'
      f' per cent against a constant speed, so the extrapolation')
    P('      is small here, but the book prices this kind of thing.')
    P('  (ii) The real wind is much slower close in than any power law')
    P('      fitted beyond 0.29 au says, which is the physical reason')
    P('      the Weber-Davis radius comes out smaller than this.')
    P('  m09_numbers.py:1301 prints 19 R_sun with no source and')
    P('  module09.html:846 prints 12 R_sun with one; Module 9\'s HTML is')
    P('  right and its generator\'s aside is not.')

    # ---------------------------------------------------------------- G
    P('')
    P('PART G.  Magnetic support against collapse')
    P('-'*74)
    P('  module05.html:763 is promised magnetic pressure and tension as')
    P('  support against collapse.  The statement is a critical')
    P('  mass-to-flux ratio: below it no field strength can be')
    P('  compressed enough to hold the cloud, and above it the cloud is')
    P('  held for as long as the flux stays with the gas.')
    P('  BOTH COEFFICIENTS ARE NOW VERIFIED, and so is a measured')
    P('  lambda to check them against.  Gate D question 4 is ANSWERED:')
    P('  PART G survives without Crutcher (2012).')
    P('')
    P(f'  (M/Phi)_crit, uniform sphere  c_Phi = {MS76_C_PHI:.5f}  = '
      f'{mass_to_flux_critical(MS76_C_PHI):.4e} g/Mx')
    P(f'      = 0.53 sqrt(5)/(3 pi), computed from Mouschovias &')
    P(f'      Spitzer\'s own c_1 and not from the 0.13 the prep typed,')
    P(f'      which was {0.13/MS76_C_PHI:.4f} times it.')
    P(f'  (M/Phi)_crit, flattened cloud c_Phi = {NN78_C_PHI:.5f}  = '
      f'{mass_to_flux_critical(NN78_C_PHI):.4e} g/Mx')
    P(f'  the two differ by a factor            = '
      f'{NN78_C_PHI/MS76_C_PHI:.4f}')
    R_mc = 10.0*pc/2.0
    M_mc = (4.0/3.0)*np.pi*R_mc**3*n_mc*2.33*mu_u
    for c_phi, tag in ((MS76_C_PHI, 'sphere'), (NN78_C_PHI, 'disc')):
        lam = mass_to_flux_ratio(M_mc, B_mc, R_mc, c_phi)
        M_phi = magnetic_critical_mass(B_mc, R_mc, c_phi)
        P(f'  10 pc cloud, B = {B_mc*1e6:.0f} uG, M = {M_mc/Msun:.3e} '
          f'Msun ({tag}):')
        P(f'      M_Phi = {M_phi/Msun:.3e} Msun, lambda = M/M_Phi = '
          f'{lam:.3f}')
    P('  A lambda above 1 is supercritical: the field cannot hold it.')
    P('')
    P('  THE CHECK ON THE CRITICAL RATIO ITSELF.  Troland & Crutcher')
    P('  (2008), ApJ 680, 457, eq. (2), convert a Zeeman measurement to')
    P('  a mass-to-flux ratio with')
    P(f'      lambda = {TC08_LAMBDA_COEFF:.1e} N(H2)/B_los,  N(H2) in '
      f'cm^-2, B_los in microgauss,')
    P('  and say in the line above it that their critical ratio is')
    P('  Nakano & Nakamura\'s.  Rebuilding that coefficient here from')
    P(f'  NN78_C_PHI = {NN78_C_PHI:.5f} and mu = {MU_PER_H2} per H2'
      f' molecule:')
    tc_u = MU_PER_H2*mu_u/(1.0e-6*mass_to_flux_critical(NN78_C_PHI))
    tc_p = MU_PER_H2*mp/(1.0e-6*mass_to_flux_critical(NN78_C_PHI))
    P(f'      with the atomic mass unit m_u = {tc_u:.4e}'
      f'   ratio {tc_u/TC08_LAMBDA_COEFF:.4f}')
    P(f'      with the proton mass    m_p = {tc_p:.4e}'
      f'   ratio {tc_p/TC08_LAMBDA_COEFF:.4f}')
    P(f'      against their               {TC08_LAMBDA_COEFF:.1e}')
    P('  THEIR COEFFICIENT CARRIES TWO SIGNIFICANT FIGURES, so the')
    P('  discriminating statement is a rounding and not a ratio:')
    P(f'  {tc_p:.4e} rounds to 7.6e-21 and {tc_u:.4e} rounds to')
    P('  7.5e-21.  THE ATOMIC MASS UNIT IS EXCLUDED AND THE HYDROGEN')
    P('  MASS IS NOT.  The 0.7 per cent between the two lines is')
    P('  m_p/m_u = 1.00728.  m_p and m_H differ by a further 0.05 per')
    P('  cent, which is INVISIBLE at their precision, so this fixes')
    P('  the convention to a hydrogen mass and no finer.  The module')
    P('  must use the same one wherever it converts a column density')
    P('  to a mass-to-flux ratio.')
    P('  The two files therefore mean the same critical ratio.  Their')
    P('  2.8 is also PER H2 MOLECULE, while this module carries')
    P('  mu = 2.33 per PARTICLE.  Those are the same mass density')
    P('  counted two ways -- with He/H = 0.1 by number,')
    P('  rho/(n_H2 m_H) = 1.4/0.5 = 2.8 and')
    P('  rho/(n_tot m_H) = 1.4/0.6 = 2.333 -- so the row above, at')
    P(f'  n_tot = {n_mc:.0f} cm^-3, is n(H2) = {n_mc*0.5/0.6:.1f} cm^-3.')
    P('  A module that prints one of these against the other is wrong')
    P('  by 20 per cent and nothing in the check battery reads it.')
    P('')
    P('  THE MEASURED LAMBDA.  Troland & Crutcher observed')
    P(f'  {TC08_N_CORES} dark cloud cores for about 500 h with Arecibo '
      f'in OH Zeeman,')
    P(f'  found a weighted-mean B_los = {TC08_B_LOS} +/- '
      f'{TC08_B_LOS_ERR} microgauss and hence |B| = '
      f'{TC08_B_TOTAL} microgauss,')
    P(f'  and a raw lambda of 4.2 (mean) and 5.2 (median).  THOSE ARE')
    P('  NOT THE NUMBERS TO QUOTE: they correct for geometry by between')
    P('  1/2, because only B_los is measured, and 1/3, for a disc')
    P('  morphology, which gives')
    P(f'      lambda_c        = {TC08_LAMBDA_MEAN_LO} to '
      f'{TC08_LAMBDA_MEAN_HI}   (mean)')
    P(f'      lambda_1/2,c    = {TC08_LAMBDA_MED_LO} to '
      f'{TC08_LAMBDA_MED_HI}   (median)')
    P('  and their own sentence, which is the one to print: the cores')
    P(f'  "appear to be slightly supercritical by about a factor of 2"')
    P(f'  at a typical density of a few times 10^3 cm^-3.')
    P('  SO THE MEASURED RANGE IS 1.4 to 2.6 AND NOT 2 to 3, AND IT IS')
    P('  MEASURED AT THIRTY TIMES THE DENSITY OF THE ROW ABOVE.  The')
    P('  10 pc cloud here is not one of their cores, so this is a check')
    P('  on the CRITICAL RATIO and on the sign of the answer, not on')
    P('  the value of lambda for this particular cloud.')
    P('  Crutcher (2012), ARA&A 50, 29, WAS NOT READ: it is paywalled,')
    P('  and neither OpenAlex nor Semantic Scholar knows of an open')
    P('  copy.  Nothing in this file rests on it.')

    # ---------------------------------------------------------------- H
    P('')
    P('PART H.  Transport across a field: conduction and viscosity')
    P('         TOGETHER, which is what module02.html:521 promises')
    P('-'*74)
    P('  Both suppressions are (omega_c tau)^-2, and PART A computed')
    P('  omega_i tau_i for the ICM.  The electron magnetisation is what')
    P('  conduction needs, and it differs from the ion one by the mass')
    P('  ratio through both omega_c and tau.')
    lnL_icm_e = lnLambda_e(n_icm, T_icm)
    tau_e_icm = tau_electron(n_icm, T_icm, lnL_icm_e)
    tau_i_icm = tau_ion(n_icm, T_icm, lnL_icm_e)
    om_e_icm = gyrofrequency(B_icm, m=me)
    wt_e = om_e_icm*tau_e_icm
    wt_i = om_icm*tau_i_icm
    kap_sup = conduction_suppression(wt_e)
    nu_sup = viscosity_suppression(wt_i)
    P('')
    P(f'  ICM at n = {n_icm} cm^-3, T = {T_icm:.0e} K, B = '
      f'{B_icm*1e6:.0f} microgauss:')
    P(f'    ln Lambda (electron branch, derived) = {lnL_icm_e:.2f} '
      f'(Module 1 census value 37.8)')
    P(f'    Braginskii tau_e                     = {tau_e_icm:.4e} s')
    P(f'    Braginskii tau_i                     = {tau_i_icm:.4e} s')
    P(f'    tau_i/tau_e                          = '
      f'{tau_i_icm/tau_e_icm:.4f}')
    P(f'    sqrt(2 m_p/m_e), which it must equal = '
      f'{np.sqrt(2.0*mp/me):.4f}   ratio '
      f'{(tau_i_icm/tau_e_icm)/np.sqrt(2.0*mp/me):.6f}')
    P(f'    omega_e tau_e                        = {wt_e:.4e}')
    P(f'    omega_i tau_i                        = {wt_i:.4e}')
    P(f'    ratio                                = {wt_e/wt_i:.4f}')
    P('    NOTE that PART A printed a different omega_i tau_i, '
      f'{om_icm*tau_icm:.4e}.')
    P('    PART A used tau = lam/v with Module 1\'s mean free path, so')
    P('    that the identity omega tau = lam/r_g could be checked;')
    P('    Braginskii\'s tau_i is a different definition of the same')
    P(f'    physical time and the two differ by '
      f'{(om_icm*tau_icm)/wt_i:.4f}.  NEITHER IS')
    P('    WRONG.  GATE D RULED: THE MODULE\'S MAGNETISATION IS')
    P('    BRAGINSKII\'S, because the coefficients 1.96, 3.16, 4.66,')
    P('    3.9 and 2 below are DEFINED on his tau.  PART A\'s lam/r_g')
    P('    is kept as a COUNT of gyro-orbits and never as a')
    P('    magnetisation.  The ratio decomposes exactly:')
    P(f'      sqrt(3/2)                          = '
      f'{np.sqrt(1.5):.6f}')
    P(f'      lnLambda_e(derived)/lnLambda(census) = '
      f'{lnL_icm_e:.3f}/{lnL_icm:.1f} = {lnL_icm_e/lnL_icm:.6f}')
    P(f'      their product                      = '
      f'{np.sqrt(1.5)*lnL_icm_e/lnL_icm:.4f}')
    P(f'      the printed ratio, for comparison  = '
      f'{(om_icm*tau_icm)/wt_i:.4f}')
    P('    sqrt(3/2) IS EXACT AND IT IS A COMPONENT COUNT: a Spitzer')
    P('    mean free path IS v_rms tau with the 3-D rms speed')
    P('    sqrt(3kT/m), while PART A divides it by sqrt(2kT/m), the')
    P('    rms of the TWO components perpendicular to B, which is')
    P('    the speed a gyroradius takes.  This is Module 10 Q8\'s')
    P('    speed table one module later, and section 1 of the module')
    P('    prints the same kind of table before any two speeds are')
    P('    compared.')
    P(f'    kappa_perp/kappa_par (Braginskii)    = {kap_sup:.4e}'
      f'   VERIFIED')
    P(f'    nu_perp/nu_par  (Braginskii, VERIFIED) = {nu_sup:.4e}')
    P('')
    P('  THE SUPPRESSION IS NOT THE ANSWER, AND SAYING SO IS THE POINT.')
    P(f'  A classical perpendicular conductivity of {kap_sup:.2e} of the')
    P('  parallel value would leave a cluster core with no conduction at')
    P('  all, which is also not what is observed.  The field is TANGLED,')
    P('  so heat follows field lines that wander; the effective')
    P('  conductivity is set by the field-line random walk and by')
    P('  microinstabilities, not by Braginskii\'s coefficient.  Module 10')
    P('  printed the measured bound and this module reuses it:')
    P(f'    Zhuravleva et al. (2019): the effective viscosity of the Coma')
    P(f'    Cluster is suppressed below the Coulomb value by at least a')
    P(f'    factor of ~{ZHURAVLEVA_SUPPRESSION_LO:.0f} to '
      f'~{ZHURAVLEVA_SUPPRESSION_HI:.0f}.')
    P(f'    Braginskii\'s classical factor is {1.0/nu_sup:.3e}, which is')
    P(f'    larger than the measured suppression by between '
      f'{np.log10(1.0/nu_sup/ZHURAVLEVA_SUPPRESSION_HI):.1f} and')
    P(f'    {np.log10(1.0/nu_sup/ZHURAVLEVA_SUPPRESSION_LO):.1f} decades.  '
      f'THE TWO DECADE FIGURES ARE PRINTED')
    P('    rather than rounded into a phrase, because a phrase cannot be')
    P('    checked and this one would have read "twenty-odd".')
    P('  SO THE HONEST STATEMENT IS A BRACKET, not a value: the')
    P('  perpendicular transport lies between the classical Braginskii')
    P('  value and the unsuppressed Coulomb one, and the measurement')
    P('  sits far nearer the second.  Module 10 bounded this and refused')
    P('  to state it; this module must do the same or find a source.')

    # ---------------------------------------------------------------- I
    P('')
    P('PART I.  The magnetorotational instability')
    P('-'*74)
    P('  module08.html:728 names the MRI in the list of what Module 12')
    P('  builds, so it is not optional.  It is done LOCALLY: q = -d ln')
    P('  Omega/d ln R = 3/2 is ASSUMED, not derived from a disc model,')
    P('  because disc structure is Module 11.')
    P(f'  gamma_max = (q/2) Omega = {MRI_GROWTH_FACTOR} Omega at q = '
      f'{KEPLER_Q}')
    P(f'  fastest mode at k v_A = sqrt(15)/4 Omega = '
      f'{MRI_KMAX_FACTOR:.5f} Omega')
    P(f'  marginal at   k v_A = sqrt(3) Omega      = '
      f'{MRI_KCRIT_FACTOR:.5f} Omega')
    P('')
    P('  A worked disc, at 1 au around a solar mass.  THE DISC NUMBERS')
    P('  ARE A CONFIGURATION, NOT AN OBJECT, in the sense')
    P('  module07.html:453 uses: nothing is checked against them.')
    for R_au, B_d, n_d, T_d in ((1.0, 1.0, 1.0e14, 300.0),
                                (10.0, 1.0e-2, 1.0e12, 50.0)):
        R_d = R_au*AU
        om_d = kepler_omega(Msun, R_d)
        rho_d = n_d*2.33*mu_u
        vA_d = alfven_speed(B_d, rho_d)
        cs_d = sound_speed(T_d, 2.33)
        H_d = cs_d/om_d
        P('')
        P(f'    R = {R_au} au, B = {B_d} G, n = {n_d:.0e} cm^-3, '
          f'T = {T_d} K')
        P(f'      Omega_K                  = {om_d:.4e} rad/s '
          f'(period {2*np.pi/om_d/yr:.2f} yr)')
        P(f'      gamma_max                = '
          f'{mri_growth_rate(om_d):.4e} /s')
        # This is 2 pi (q/2) = 3 pi/2 for every Keplerian disc, whatever
        # its field, density or temperature.  It is printed inside the
        # loop so that a reader sees it NOT change, which is the point.
        P(f'      e-folds per orbit        = '
          f'{mri_growth_rate(om_d)*2*np.pi/om_d:.3f}  (= 3 pi/2 = '
          f'{3.0*np.pi/2.0:.3f}, the same in every row)')
        P(f'      v_A                      = {vA_d/1e5:.4f} km/s')
        P(f'      c_s                      = {cs_d/1e5:.4f} km/s')
        P(f'      scale height H = c_s/Om  = {H_d/AU:.5f} au = '
          f'{H_d/R_d:.4f} R')
        P(f'      lambda(fastest)          = '
          f'{mri_wavelength_max(vA_d, om_d)/AU:.5f} au = '
          f'{mri_wavelength_max(vA_d, om_d)/H_d:.4f} H')
        lam_crit = mri_wavelength_crit(vA_d, om_d)
        P(f'      lambda(marginal)         = {lam_crit/AU:.5f} au = '
          f'{lam_crit/H_d:.4f} H')
        P(f'      beta                     = '
          f'{plasma_beta(n_d, T_d, B_d):.4e}')
        P(f'      lambda(marginal)/H < 1?  = '
          f'{"YES, unstable" if lam_crit < H_d else "NO, stabilised"} '
          f'({lam_crit/H_d:.4f})')
    P('')
    P('  THE CONDITION THAT MATTERS is lambda(marginal) < H: a disc too')
    P('  strongly magnetised has no unstable wavelength that fits inside')
    P('  it.  Each row prints its own verdict above rather than leaving')
    P('  a reader to compare two columns by eye.')
    P('  AND THE CONDITION THIS BOOK CANNOT CHECK is ionisation: the MRI')
    P('  needs the gas coupled to the field, and a 300 K protoplanetary')
    P('  disc at n = 1e14 is very nearly neutral.  PART B\'s molecular')
    P('  cloud row is the same defect and this module must say so once,')
    P('  in print, rather than twice by accident.')

    # ---------------------------------------------------------------- J
    P('')
    P('PART J.  Critical balance, and the debt Module 10 printed')
    P('-'*74)
    P('  module10.html:668 and :914 say it plainly: the confirmed 5/3 is')
    P('  a MAGNETIC spectrum in an Alfvenic plasma, and 5/3 for B is')
    P('  also what Goldreich & Sridhar (1995) predict from a quite')
    P('  different argument.  Agreement of an exponent does not select')
    P('  between two derivations that give the same exponent.')
    P('  CRITICAL BALANCE says the cascade keeps the linear Alfven time')
    P('  and the nonlinear turnover time equal at every scale:')
    P('    k_par v_A ~ k_perp delta_v_perp,  delta_v_perp ~ k_perp^(-1/3)')
    P(f'    => k_par ~ k_perp^{GS95_PARALLEL:.4f}, and E(k_perp) ~ '
      f'k_perp^-{KOLMOGOROV_SPEC:.4f}')
    P('  SO THE EXPONENT IS NOT THE DISCRIMINANT.  The discriminant is')
    P('  the ANISOTROPY: K41 predicts none and critical balance predicts')
    P('  eddies that grow more elongated along the field at every')
    P('  smaller scale.  A check that separates the two must measure')
    P('  anisotropy, not a spectral index.')
    b_mean = float(np.mean(PODESTA_B_INDEX))
    P('')
    P(f'  Module 10\'s anchor, reprinted so this module quotes one set:')
    P(f'    Podesta magnetic indices           = {PODESTA_B_INDEX}')
    P(f'    their mean                         = {b_mean:.4f} against '
      f'{KOLMOGOROV_SPEC:.4f}, ratio {b_mean/KOLMOGOROV_SPEC:.4f}')
    P('  GATE D RULED: THE DISCRIMINATING MEASUREMENT IS DECLARED')
    P('  OUTSIDE THIS BOOK, IN PRINT.  No anisotropy measurement was')
    P('  fetched at step 2 and none is in this repo, so the module')
    P('  derives the two exponents, says 5/3 is not the')
    P('  discriminant, and states that it does not measure the')
    P('  anisotropy that is.  NO CHECK IS BUILT ON PART J.')
    P('  AND GOLDREICH & SRIDHAR\'S OWN RESTRICTION TRAVELS IN THE')
    P('  SAME SENTENCE AS THEIR RESULT, EVERY TIME.  Their abstract,')
    P('  third and fourth sentences: they treat only the symmetric')
    P('  case, and that "precludes application to the solar wind in')
    P('  which the outward flux significantly exceeds the ingoing')
    P('  one."  So GS95 may NOT be quoted as a prediction for the')
    P('  Podesta indices above, and module10.html:668 and :914 do')
    P('  exactly that -- a prose attribution on which no number')
    P('  depends (module10.html:1064 says GS95 is "not used')
    P('  numerically anywhere").  The replacement text is written')
    P('  out in .ignore/m12-gate-d.md Q12 and the edit is Simon\'s,')
    P('  on the 170c4da precedent.  Module 12 carries the caveat')
    P('  whether or not Module 10 is edited.')
    P('  NOTE ALSO that k_par ~ k_perp^(2/3) L^(-1/3) carries an')
    P('  OUTER SCALE: the bare exponent above is not dimensional,')
    P('  and the module prints their form with the L^(-1/3).')

    # ---------------------------------------------------------------- K
    P('')
    P('PART K.  What this module does NOT do, and why it is in print')
    P('-'*74)
    P('  Oblique magnetohydrodynamic shock jump conditions.')
    P('    module08.html:970 calls Module 8\'s refusal of a Voyager')
    P('    comparison "permanent rather than provisional" ON THE GROUND')
    P('    that Module 12 does not derive them.  Deriving them here')
    P('    makes a shipped module false.  If Gate D wants them,')
    P('    module08.html:728 and :970 are edited in the SAME commit.')
    P('  Disc structure, the alpha prescription, the thin-disc solution.')
    P('    Module 11.  PART I assumes the shear and derives nothing')
    P('    about the disc that produces it.')
    P('  Magnetic reconnection.  No shipped module promises it.')
    P('  The two-temperature closure (module02.html:686,')
    P('    module09.html:848).  It is a plasma result rather than an MHD')
    P('    one - single-fluid MHD has one temperature by construction -')
    P('    so this module may have to declare the debt UNPAID in print.')
    P('    Gate D decides.')

    # ---------------------------------------------------------------- L
    P('')
    P('PART L.  The nine problems, C1-C3, D1-D3, K1-K3')
    P('-'*74)
    P('  The slots and the modelling inputs each STATEMENT must carry are')
    P('  fixed in .ignore/m12-gate-d.md.  afd/figs/m12_problems_check.py')
    P('  rebuilds every answer below FROM THE PROBLEM STATEMENT and')
    P('  imports nothing from this file, so a statement that omits an')
    P('  input is a defect the check finds.')

    P('')
    P('  P1 (C1).  The active-region corona: beta, v_A, c_s, v_A/c_s.')
    p1_n, p1_T, p1_B, p1_mu = 1.0e9, 1.0e6, 10.0, 0.61
    p1_beta = plasma_beta(p1_n, p1_T, p1_B)
    p1_rho = p1_n*p1_mu*mu_u
    p1_vA = alfven_speed(p1_B, p1_rho)
    p1_cs = sound_speed(p1_T, p1_mu)
    p1_id = np.sqrt(2.0/((5.0/3.0)*p1_beta))
    P(f'      n = {p1_n:.0e} cm^-3, T = {p1_T:.0e} K, B = {p1_B:.0f} G, '
      f'mu = {p1_mu}, gamma = 5/3')
    P(f'      rho = n mu m_u                     = {p1_rho:.4e} g/cm^3')
    P(f'      p_gas = n k T                      = {p1_n*kB*p1_T:.4e} '
      f'dyn/cm^2')
    P(f'      p_mag = B^2/8pi                    = '
      f'{magnetic_pressure(p1_B):.4e} dyn/cm^2')
    P(f'      beta                               = {p1_beta:.4f}')
    P(f'      v_A = B/sqrt(4 pi rho)             = {p1_vA/1e5:.1f} km/s')
    P(f'      c_s = sqrt(gamma k T/mu m_u)       = {p1_cs/1e5:.1f} km/s')
    P(f'      v_A/c_s, two speeds                = {p1_vA/p1_cs:.4f}')
    P(f'      sqrt(2/(gamma beta)), the identity = {p1_id:.4f}')
    P(f'      ratio of the two                   = '
      f'{(p1_vA/p1_cs)/p1_id:.6f}')
    P(f'      THE CORONA IS MAGNETICALLY DOMINATED: beta = '
      f'{p1_beta:.4f}, so the field')
    P(f'      carries {1.0/p1_beta:.1f} times the gas pressure, and news '
      f'travels at')
    P(f'      {p1_vA/p1_cs:.2f} times the sound speed.')

    P('')
    P('  P2 (C2).  A coronal loop: eta_m, Rm, the ohmic time, and the')
    P('            identity (L^2/eta_m)/(L/U) = Rm.')
    p2_n, p2_T = 1.0e9, 1.0e6
    p2_L, p2_U = 1.0e10, 1.0e6
    p2_lnL = lnLambda_e(p2_n, p2_T)
    p2_eta = resistivity(p2_n, p2_T, p2_lnL)
    p2_Rm = magnetic_reynolds(p2_U, p2_L, p2_eta)
    p2_td = diffusion_time(p2_L, p2_eta)
    P(f'      n = {p2_n:.0e} cm^-3, T = {p2_T:.0e} K, L = {p2_L:.0e} cm '
      f'(100 Mm), U = {p2_U/1e5:.0f} km/s')
    P(f'      ln Lambda (electron branch)        = {p2_lnL:.2f}')
    P(f'      eta_m = c^2/(4 pi sigma_par)       = {p2_eta:.4e} cm^2/s')
    P(f'      Rm = U L/eta_m                     = {p2_Rm:.4e}')
    P(f'      t_diff = L^2/eta_m                 = {p2_td/yr:.4e} yr')
    P(f'      t_dyn  = L/U                       = {p2_L/p2_U/yr:.4e} yr')
    P(f'      t_diff/t_dyn                       = '
      f'{p2_td/(p2_L/p2_U):.4e}')
    P(f'      ratio to Rm, which must be 1       = '
      f'{p2_td/(p2_L/p2_U)/p2_Rm:.6f}')
    P('      THE POINT: the same number is computed twice by two routes,')
    P('      because (L^2/eta_m)/(L/U) = U L/eta_m identically.')

    P('')
    P('  P3 (C3).  The Parker spiral at 1 au and at 5 au, constant wind.')
    p3_v = VB18_MEAN['velocity'][0]*1e5
    p3_om = 2.0*np.pi/(CARRINGTON_SIDEREAL_DAYS*day)
    p3_r0 = R_SOURCE_SURFACE*Rsun
    P(f'      Omega (sidereal {CARRINGTON_SIDEREAL_DAYS} d, NSSDC at '
      f'{CARRINGTON_LATITUDE_DEG:.0f} deg) = {p3_om:.5e} rad/s')
    P(f'      v = {p3_v/1e5:.1f} km/s, held CONSTANT; r0 = '
      f'{R_SOURCE_SURFACE} R_sun; theta = 90 deg')
    for p3_r_au in (1.0, 5.0):
        p3_r = p3_r_au*AU
        p3_ratio = parker_ratio(p3_r, p3_v, p3_om, r0=p3_r0)
        p3_ang = spiral_angle(p3_r, p3_v, p3_om, r0=p3_r0)
        p3_idx = parker_field_index(p3_r, p3_v, p3_om, r0=p3_r0)
        P(f'      at r = {p3_r_au:.0f} au:  -B_phi/B_r = {p3_ratio:.4f},  '
          f'angle = {p3_ang:.2f} deg,  d ln|B|/d ln r = {p3_idx:.4f}')
    P('      THE SPIRAL TIGHTENS OUTWARD: by 5 au the field is nearly')
    P('      azimuthal and its local index has risen toward -1.')
    p3_with = parker_ratio(AU, p3_v, p3_om, r0=p3_r0)
    p3_without = parker_ratio(AU, p3_v, p3_om, r0=0.0)
    P(f'      PARKER\'S (r - r0) AGAINST A BARE r AT 1 au.  Carrying r0')
    P(f'      LOWERS -B_phi/B_r from {p3_without:.4f} to {p3_with:.4f}, by')
    P(f'      {(1.0 - p3_with/p3_without)*100.0:.2f} per cent; dropping it '
      f'RAISES the ratio by')
    P(f'      {(p3_without/p3_with - 1.0)*100.0:.2f} per cent.  The two '
      f'percentages are one term')
    P(f'      seen from its two ends, and r0/1 au = '
      f'{p3_r0/AU:.5f} is why.')

    P('')
    P('  P4 (D1).  A 10 pc cloud: M, M_Phi and lambda_Phi, both')
    P('            geometries.')
    p4_n, p4_mu, p4_B = 1.0e2, 2.33, 1.0e-5
    p4_R = 5.0*pc
    p4_rho = p4_n*p4_mu*mu_u
    p4_M = (4.0/3.0)*np.pi*p4_R**3*p4_rho
    P(f'      n_tot = {p4_n:.0f} cm^-3 per PARTICLE at mu = {p4_mu}, so')
    P(f'      n(H2) = n_tot x 2.333/2.8        = {p4_n*2.3333/2.8:.1f} '
      f'cm^-3')
    P(f'      R = 5 pc, B = {p4_B*1e6:.0f} microgauss (census, no source '
      f'at this density)')
    P(f'      rho = n mu m_u                   = {p4_rho:.4e} g/cm^3')
    P(f'      M = (4/3) pi R^3 rho             = {p4_M/Msun:.4e} Msun')
    for p4_tag, p4_c in (('sphere', MS76_C_PHI), ('sheet', NN78_C_PHI)):
        p4_crit = mass_to_flux_critical(p4_c)
        p4_Mphi = magnetic_critical_mass(p4_B, p4_R, p4_c)
        p4_lam = mass_to_flux_ratio(p4_M, p4_B, p4_R, p4_c)
        P(f'      {p4_tag:<7} c_Phi = {p4_c:.5f}: (M/Phi)_crit = '
          f'{p4_crit:.4e} g/Mx, M_Phi = {p4_Mphi/Msun:.4e} Msun, '
          f'lambda_Phi = {p4_lam:.4f}')
    p4_geom = NN78_C_PHI/MS76_C_PHI
    P(f'      the geometry factor              = {p4_geom:.4f}')
    p4_span = (np.log(p4_geom)
               / np.log(TC08_LAMBDA_MED_HI/TC08_LAMBDA_MEAN_LO))
    P(f'      BOTH ANSWERS ARE SUPERCRITICAL, and the geometry moves the')
    P(f'      answer by {p4_geom:.4f} -- which is why neither may be quoted')
    P(f'      alone.  Troland & Crutcher measure {TC08_LAMBDA_MEAN_LO} to '
      f'{TC08_LAMBDA_MED_HI}, and this one')
    P(f'      geometric factor spans {p4_span:.3f} of that log width.')

    P('')
    P('  P5 (D2).  The Alfven radius by hand, mean fits, protons only,')
    P('            constant wind speed.')
    p5_n = VB18_MEAN['density'][0]
    p5_B = VB18_MEAN['field'][0]*1e-5       # nT -> gauss
    p5_v = VB18_MEAN['velocity'][0]*1e5
    # -B_phi/B_r at 1 au, COMPUTED from the same call PART E makes, not
    # retyped from its output.  Retyping a sibling's number is the defect
    # this file found four times at step 1.
    p5_x1 = parker_ratio(AU, p5_v,
                         2.0*np.pi/(CARRINGTON_SIDEREAL_DAYS*day),
                         r0=R_SOURCE_SURFACE*Rsun)
    p5_Br = p5_B/np.sqrt(1.0 + p5_x1*p5_x1)
    p5_rho = p5_n*mp
    p5_vA = alfven_speed(p5_Br, p5_rho)
    p5_rA = alfven_radius_constant_v(AU, p5_v, p5_vA)
    p5_rA_wrong = alfven_radius_constant_v(
        AU, p5_v, alfven_speed(p5_B, p5_rho))
    P(f'      n = {p5_n} cm^-3, |B| = {VB18_MEAN["field"][0]} nT, '
      f'v = {p5_v/1e5:.1f} km/s (MEAN fits), protons only')
    P(f'      -B_phi/B_r at 1 au               = {p5_x1:.4f}')
    P(f'      sqrt(1 + x1^2)                   = '
      f'{np.sqrt(1.0 + p5_x1*p5_x1):.4f}')
    P(f'      B_r = |B|/sqrt(1 + x1^2)         = {p5_Br*1e5:.4f} nT')
    P(f'      v_A(radial) at 1 au              = {p5_vA/1e5:.2f} km/s')
    P(f'      v/v_A at 1 au                    = {p5_v/p5_vA:.3f}')
    P(f'      r_A, constant v                  = {p5_rA/Rsun:.2f} R_sun')
    P(f'      using |B| instead would give      = '
      f'{p5_rA_wrong/Rsun:.2f} R_sun, on THESE inputs')
    P('      (PART F\'s parenthetical 23.22 R_sun is the same mistake on')
    P('      a different row -- helium included and v ~ r^+0.049 -- so')
    P('      the two are not in conflict.)')
    P('      THE ALFVEN SPEED TAKES B_r AND NOT |B|, twice over: B_r is')
    P('      what scales as r^-2 by div B = 0, and the Weber-Davis')
    P('      surface is defined on the radial Alfven speed.')

    P('')
    P('  P6 (D3).  The ICM: omega_e tau_e, kappa_perp/kappa_par, and')
    P('            the comparison that must be made before quoting it.')
    p6_lnL = lnLambda_e(n_icm, T_icm)
    p6_taue = tau_electron(n_icm, T_icm, p6_lnL)
    p6_wt = gyrofrequency(B_icm, m=me)*p6_taue
    p6_sup = conduction_suppression(p6_wt)
    P(f'      n = {n_icm} cm^-3, T = {T_icm:.0e} K, B = '
      f'{B_icm*1e6:.0f} microgauss')
    P(f'      ln Lambda (derived; census is 37.8) = {p6_lnL:.2f}')
    P(f'      Braginskii tau_e                   = {p6_taue:.4e} s')
    P(f'      omega_e = e B/(m_e c)              = '
      f'{gyrofrequency(B_icm, m=me):.4e} rad/s')
    P(f'      omega_e tau_e                      = {p6_wt:.4e}')
    P(f'      kappa_perp/kappa_par               = {p6_sup:.4e}')
    p6_wti = gyrofrequency(B_icm)*tau_ion(n_icm, T_icm, p6_lnL)
    p6_nu = viscosity_suppression(p6_wti)
    P(f'      omega_i tau_i, the ION magnetisation = {p6_wti:.4e}')
    P(f'      nu_perp/nu_par                     = {p6_nu:.4e}')
    P(f'      Zhuravleva\'s measured suppression  = '
      f'{ZHURAVLEVA_SUPPRESSION_LO:.0f} to '
      f'{ZHURAVLEVA_SUPPRESSION_HI:.0f}')
    P('      ZHURAVLEVA MEASURE A VISCOSITY, so the comparison is with')
    P('      nu_perp/nu_par and NOT with kappa_perp/kappa_par.  Comparing')
    P('      a conduction ratio with a viscosity bound is two quantities')
    P('      in one sentence, and this problem exists to stop it.')
    P(f'      classical viscous suppression factor = {1.0/p6_nu:.4e}')
    P(f'      larger than the measured one by between '
      f'{np.log10(1.0/p6_nu/ZHURAVLEVA_SUPPRESSION_HI):.1f} and')
    P(f'      {np.log10(1.0/p6_nu/ZHURAVLEVA_SUPPRESSION_LO):.1f} '
      f'decades, which is PART H\'s bracket')
    P(f'      THE ANSWER MUST BE CHECKED BEFORE IT IS QUOTED: '
      f'{p6_sup:.2e} of the')
    P('      parallel value would leave a cluster core with no')
    P('      conduction at all, and that is not what is observed.')

    P('')
    P('  P7 (K1).  The MRI in a protoplanetary disc at 1 au.')
    p7_R, p7_B, p7_n, p7_T, p7_mu = AU, 1.0, 1.0e14, 300.0, 2.33
    p7_om = kepler_omega(Msun, p7_R)
    p7_gam = mri_growth_rate(p7_om)
    p7_rho = p7_n*p7_mu*mu_u
    p7_vA = alfven_speed(p7_B, p7_rho)
    p7_cs = sound_speed(p7_T, p7_mu)
    p7_H = p7_cs/p7_om
    p7_lam_max = mri_wavelength_max(p7_vA, p7_om)
    p7_lam_crit = mri_wavelength_crit(p7_vA, p7_om)
    P(f'      M = 1 Msun, R = 1 au, B = {p7_B:.0f} G, n = {p7_n:.0e} '
      f'cm^-3, T = {p7_T:.0f} K, mu = {p7_mu}')
    P(f'      q = -d ln Omega/d ln R = {KEPLER_Q} is ASSUMED, not derived')
    P(f'      Omega_K = sqrt(G M/R^3)          = {p7_om:.4e} rad/s')
    P(f'      orbital period                   = '
      f'{2.0*np.pi/p7_om/yr:.4f} yr')
    P(f'      gamma_max = (q/2) Omega          = {p7_gam:.4e} /s')
    P(f'      e-folds per orbit = 2 pi gamma/Omega = '
      f'{2.0*np.pi*p7_gam/p7_om:.4f}')
    P(f'      3 pi/2, which it equals for ANY Keplerian disc = '
      f'{3.0*np.pi/2.0:.4f}')
    P(f'      v_A                              = {p7_vA/1e5:.4f} km/s')
    P(f'      c_s                              = {p7_cs/1e5:.4f} km/s')
    P(f'      H = c_s/Omega                    = {p7_H/AU:.5f} au')
    P(f'      lambda(fastest), at k v_A = sqrt(15)/4 Omega = '
      f'{p7_lam_max/AU:.5f} au = {p7_lam_max/p7_H:.4f} H')
    P(f'      lambda(marginal)                 = {p7_lam_crit/AU:.5f} au '
      f'= {p7_lam_crit/p7_H:.4f} H')
    P(f'      lambda(marginal)/H < 1?          = '
      f'{"YES, unstable" if p7_lam_crit < p7_H else "NO, stabilised"}')
    P('      THE 4.712 DOES NOT DEPEND ON B, n OR T.  gamma_max/Omega is')
    P('      q/2 for every Keplerian disc, so 2 pi (q/2) = 3 pi/2 is an')
    P('      identity and not a property of this disc.')

    P('')
    P('  P8 (K2).  Module 7\'s one-degree bound, recomputed.')
    p8_rho_h = M07_MU_E*M07_NE*mu_u
    p8_rho_l = p8_rho_h/M07_DENSITY_RATIO
    p8_pref = np.sqrt(2.0*np.pi*p8_rho_h*p8_rho_l/(p8_rho_h + p8_rho_l))
    p8_two = M07_DU*p8_pref
    p8_one = M07_DU*np.sqrt(2.0)*p8_pref
    P(f'      rho_h = mu_e n_e m_u at n_e = {M07_NE:.0e} cm^-3, mu_e = '
      f'{M07_MU_E}  = {p8_rho_h:.4e} g/cm^3')
    P(f'      rho_l = rho_h/{M07_DENSITY_RATIO}'
      f'                                 = {p8_rho_l:.4e} g/cm^3')
    P(f'      Delta_U = {M07_DU/1e5:.0f} km/s, an UPPER LIMIT')
    P(f'      B cos(theta) < Delta_U sqrt(2 pi rho_h rho_l/(rho_h+rho_l))'
      f' = {p8_two:.5f} G')
    P(f'      one-sided field, with 4 pi                                '
      f' = {p8_one:.5f} G')
    P(f'      Module 7 prints {M07_BOUND_TWO_SIDED} and '
      f'{M07_BOUND_ONE_SIDED}; ratios '
      f'{p8_two/M07_BOUND_TWO_SIDED:.4f} and '
      f'{p8_one/M07_BOUND_ONE_SIDED:.4f}')
    for p8_B in (1.0, 10.0):
        p8_cos = p8_two/p8_B
        P(f'      at B = {p8_B:>4.0f} G: cos(theta) < {p8_cos:.5f}, so the '
          f'wavevector must lie within {np.degrees(np.arcsin(p8_cos)):.2f} '
          f'deg of PERPENDICULAR')
    P('      THE ANGLE IS MEASURED FROM PERPENDICULAR, so it is')
    P('      arcsin(cos theta) and not arccos(cos theta): the second')
    P('      gives 86.13 degrees where Module 7 prints 3.87.')

    P('')
    P('  P9 (K3).  The two magnetisations of one plasma, accounted for')
    P('            exactly.')
    p9_lam = lam_coulomb(n_icm, T_icm, lnL_icm)
    p9_v2 = np.sqrt(2.0*kB*T_icm/mp)
    p9_rg = gyroradius(T_icm, B_icm)
    p9_om = gyrofrequency(B_icm)
    p9_A = p9_om*(p9_lam/p9_v2)
    p9_lnLe = lnLambda_e(n_icm, T_icm)
    p9_H = p9_om*tau_ion(n_icm, T_icm, p9_lnLe)
    P(f'      lam at ln Lambda = {lnL_icm}          = '
      f'{p9_lam/kpc:.1f} kpc')
    P(f'      sqrt(2kT/m_p), the gyroradius speed  = {p9_v2/1e5:.0f} km/s')
    P(f'      sqrt(3kT/m_p), the rms speed         = '
      f'{np.sqrt(3.0*kB*T_icm/mp)/1e5:.0f} km/s')
    P(f'      r_g                                  = {p9_rg/1e5:.4e} km')
    P(f'      lam/r_g = omega tau with tau = lam/v = {p9_A:.4e}')
    P(f'      omega_i tau_i with Braginskii tau_i  = {p9_H:.4e}')
    P(f'      their ratio                          = {p9_A/p9_H:.4f}')
    P(f'      sqrt(3/2)                            = {np.sqrt(1.5):.6f}')
    P(f'      ln Lambda_e/ln Lambda                = '
      f'{p9_lnLe/lnL_icm:.6f}')
    P(f'      product, which must be the ratio     = '
      f'{np.sqrt(1.5)*p9_lnLe/lnL_icm:.4f}')
    P('      THE ONE THAT BELONGS IN (omega_c tau)^-2 IS BRAGINSKII\'S,')
    P('      because his transport coefficients are defined on his tau.')

    P('')
    P('SOURCES')
    P('-'*74)
    P('  Venzmer, M. S. & Bothmer, V. (2018), "Solar-wind predictions for')
    P('    the Parker Solar Probe orbit", A&A 611, A36.  arXiv:1711.07534.')
    P('    Eq. (10) and Table 3; Fig. 9 for the year-to-year exponent')
    P('    scatter.  VERIFIED FOR MODULE 9: the PDF does not extract')
    P('    through a web summariser; fetch arxiv.org/pdf/1711.07534 and')
    P('    read it with PyMuPDF, page 6 for the discussion and page 7 for')
    P('    Table 3.  THE ANCHOR OF CHECK 1.')
    P('  Verscharen, D., Bale, S. D. & Velli, M. (2021), "Flow')
    P('    deflections and Alfven radii", MNRAS 506(4), 4993-5004.')
    P('    Table 3.  VERIFIED FOR MODULE 9 and quoted at')
    P('    module09.html:964.  THE SOURCE OF CHECK 2.')
    P('  Podesta, J. J., Roberts, D. A. & Goldstein, M. L. (2007), ApJ')
    P('    664, 543-548, Table 2.  VERIFIED FOR MODULE 10 step 2.  Used')
    P('    here only to restate Module 10\'s anchor, not for a new check.')
    P('  Braginskii, S. I. (1965), Reviews of Plasma Physics 1, 205-311,')
    P('    Consultants Bureau, translated by Herbert Lashinsky.  ALL')
    P('    SEVEN COEFFICIENTS THIS FILE USES ARE NOW READ FROM THE')
    P('    ORIGINAL SCAN.  The ion viscosity (eq. 2.22, eq. 2.23,')
    P('    p. 218) came in at Module 10; at Module 12 step 2 the pages')
    P('    were rendered as images and read, giving eq. (2.5e) on')
    P('    p. 215 for tau_e with its 4 sqrt(2 pi) and its Z^2 n_i,')
    P('    eqs. (2.7) and (2.8) on p. 216 for sigma_par = 1.96')
    P('    sigma_perp, and eqs. (2.12), (2.13), (2.15) and (2.16) on')
    P('    p. 217 for 3.16, 4.66, 3.9 and 2.  EVERY ONE IS FOR Z = 1;')
    P('    his Table 1 on p. 216 gives the Z-dependence, and the')
    P('    electron conduction coefficient runs 3.16, 4.9, 6.1, 6.9,')
    P('    12.5 for Z = 1, 2, 3, 4, infinity.  Scan:')
    P('    static.ias.edu/pitp/2016/sites/pitp/files/braginskii_1965-1.pdf')
    P('    - no text layer, two article pages per PDF page, article page')
    P('    = 2*(PDF page) + 200 for the left half, CONFIRMED against the')
    P('    printed 214 and 215 on PDF page 7.')
    P('  Zhuravleva, I. et al. (2019), Nature Astronomy 3, 832-837.')
    P('    arXiv:1906.06346.  VERIFIED FOR MODULE 10 step 2.  A one-sided')
    P('    bound on the effective ICM viscosity, not a value.')
    P('  Goldreich, P. & Sridhar, S. (1995), "Toward a theory of')
    P('    interstellar turbulence. II. Strong Alfvenic turbulence",')
    P('    ApJ 438, 763-775.  VERIFIED at step 2 from the ADS scan,')
    P('    1995ApJ...438..763G, rendered and read as images.  Their')
    P('    abstract gives k_z ~ k_perp^(2/3) L^(-1/3) and a')
    P('    one-dimensional spectrum proportional to k_perp^(-5/3).')
    P('    IT ALSO SAYS, IN THE THIRD SENTENCE, that they treat only')
    P('    the symmetric case and that this "precludes application to')
    P('    the solar wind in which the outward flux significantly')
    P('    exceeds the ingoing one" -- so GS95 may not be quoted as a')
    P('    prediction for Module 10\'s solar-wind anchor.')
    P('  Kasper, J. C. et al. (2021), "Parker Solar Probe enters the')
    P('    magnetically dominated solar corona", Phys. Rev. Lett. 127,')
    P('    255101.  VERIFIED at step 2 from the APS open-access PDF.')
    P('    Their range is 16-20 R_sun over three intervals, not the')
    P('    19-20 the prep wrote, and every median M_A is below 1.')
    P('  Mouschovias, T. Ch. & Spitzer, L. (1976), "Note on the')
    P('    collapse of magnetic interstellar clouds", ApJ 210, 326-327.')
    P('    VERIFIED at step 2 from the ADS scan.  Their eq. (2) and')
    P('    eq. (4); the paper prints c_1 = 0.53, never 0.13.')
    P('  Nakano, T. & Nakamura, T. (1978), "Gravitational instability')
    P('    of magnetized gaseous disks", PASJ 30, 671-679.  VERIFIED at')
    P('    step 2 from the ADS scan.  Abstract, p. 671.')
    P('  Troland, T. H. & Crutcher, R. M. (2008), "Magnetic fields in')
    P('    dark cloud cores: Arecibo OH Zeeman observations", ApJ 680,')
    P('    457-465, arXiv:0802.2253.  VERIFIED at step 2.  PART G\'s')
    P('    CHECK, and the reason PART G survives.')
    P('  Crutcher, R. M. (2012), ARA&A 50, 29-63.  NOT READ -- paywalled,')
    P('    with no open-access copy known to OpenAlex or Semantic')
    P('    Scholar.  Volume, page and year confirmed at Crossref.')
    P('    NOTHING IN THIS FILE RESTS ON IT.')
    P('  Snodgrass, H. B. & Ulrich, R. K. (1990), "Rotation of Doppler')
    P('    features in the solar photosphere", ApJ 351, 309-316.')
    P('    VERIFIED at step 2 from the ADS scan.  Their')
    P('    14.71 - 2.39 sin^2 L - 1.78 sin^4 L deg/day sidereal is')
    P('    where 24.47 d comes from, and it is a DIFFERENT TRACER from')
    P('    the NSSDC law, not just a different latitude.')
    P('  NASA NSSDC Sun Fact Sheet,')
    P('    nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html.  Read')
    P('    as HTML at step 2.  Sidereal rotation period 609.12 hours =')
    P('    25.380 d, adopted at 16 deg latitude, with the law')
    P('    14.37 - 2.33 sin^2 L - 1.56 sin^4 L deg/day.  It also prints')
    P('    the field census this module did NOT take its numbers from:')
    P('    polar 1-2 G, sunspots 3000 G, prominences 10-100 G, plages')
    P('    200 G, bright chromospheric network 25 G.')
    P('  Parker, E. N. (1958), ApJ 128, 664.  VERIFIED: Sect. II for')
    P('    Module 9, and his eq. (26) on p. 673 at Module 12 step 2 --')
    P('    B_r = B(b/r)^2, B_theta = 0, B_phi = B (omega/v_m)(r - b)')
    P('    (b/r)^2 sin theta, with the pi/4 surface at r = (v_m/omega)')
    P('    sin theta in his eq. (27).  NOTE THE (r - b), NOT r.')
    P('  Alfven, H. (1942), "Existence of electromagnetic-hydrodynamic')
    P('    waves", Nature 150, 405-406.  Cited for the result only, as')
    P('    Module 1 does for Maxwell (1867); title, volume, page and')
    P('    date confirmed at Crossref, DOI 10.1038/150405d0.  The')
    P('    paper itself was not fetched and the module says so.')


if __name__ == '__main__':
    main()
