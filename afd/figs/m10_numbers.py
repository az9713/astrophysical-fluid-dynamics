"""Module 10 numbers: turbulence.  Reynolds numbers, the Kolmogorov cascade,
the number of degrees of freedom, supersonic turbulence, and four checks
against published measurements.

Every physical number quoted in module10.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

THE SHAPE OF THE CHECK, following Modules 2 and 3.  From ONE published
source, one exact prediction is CONFIRMED and one assumption is REFUTED.

  THE ANCHOR IS CHECK 1, Podesta, Roberts & Goldstein (2007), Table 2.
  It is the anchor because it is the only source in this module that
  confirms and refutes FROM THE SAME TABLE, with stated errors, on the
  same instrument, in the same fit window, for the same four time
  intervals.  Four intervals of Wind spacecraft data at 1 au give, for
  each interval, a magnetic-field spectral index and a velocity spectral
  index measured side by side:

    CONFIRMED  The MEAN of the magnetic-field spectral index agrees
               with the Kolmogorov exponent 5/3.  The four measured
               indices are 1.66, 1.72, 1.66 and 1.58; their mean is
               1.6550 against 1.6667, a ratio of 0.993, and a one-sample
               t test on the four gives t = -0.41 on 3 degrees of
               freedom, p = 0.71.  Nothing was fitted to make this
               happen: 5/3 comes from dimensional analysis alone.

               WHAT IS NOT CONFIRMED is 5/3 interval by interval.  The
               departures in units of each interval's own 99% half-width
               are -0.3, +2.7, -0.7 and -4.3, so one interval sits above
               the prediction and three below, and interval 4 is 4.3
               half-widths -- 11.2 sigma -- away.  The
               interval-to-interval scatter is real and larger than the
               fit errors, and the prose must say that the confirmation
               is of the mean.

    REFUTED    The assumption that ONE index describes the turbulence.
               In the same four intervals, in the same fit window, the
               VELOCITY spectrum gives 1.50, 1.59, 1.52 and 1.50.  Every
               one is below 5/3, by 3.8 to 8.3 times its own quoted
               half-width, with no interval on the other side.  A
               cascade in which velocity and magnetic field are two
               faces of one Kolmogorov spectrum is therefore excluded by
               the measurement, not by a model.

               The contrast is the check, and it survives the most
               conservative error bar available.  Taking the
               interval-to-interval scatter of the four fits as the
               error - which is larger than any single fit's error, and
               so is the cautious choice - the magnetic mean sits 0.4
               standard errors from 5/3 and the velocity mean 6.5 below
               it, and against 3/2 the roles swap: velocity 1.3,
               magnetic 5.4.

               THOSE FOUR NUMBERS ARE NOT SIGMAS, and PART G now says so
               in print.  With n = 4 the statistic is Student's t on 3
               degrees of freedom.  The velocity mean's 6.5 is p =
               0.0073, equivalent to 2.7 Gaussian sigma; the magnetic
               mean's 5.4 against 3/2 is p = 0.0125, 2.5 sigma.  Both
               conclusions stand, at roughly a quarter of the strength
               the bare numbers suggest, and the module must quote the
               p-values rather than the standard-error counts.

               THE STRONGER FORM OF THE VELOCITY REFUTATION NEEDS NO n=4
               STATISTICS: every one of the four velocity indices is
               below 5/3 by 3.8 to 8.3 of its OWN 99% half-width, with
               no interval on the other side.  Lead with that.

  THREE CAVEATS ON CHECK 1, stated here because they govern the wording.
  (i) The errors printed in the paper's Table 2 are 99% confidence
      limits, NOT standard deviations, and the paper says they "have been
      rounded up in every case".  Dividing by 2.576 converts to a
      Gaussian sigma; both forms are printed below and the prose must say
      which it is quoting.
  (ii) A magnetic spectrum with exponent 5/3 is not evidence FOR the K41
      hydrodynamic cascade.  This is magnetised plasma, the fluctuations
      are Alfvenic, and 5/3 for the magnetic field is also what
      Goldreich & Sridhar (1995) predict from a quite different argument.
      What is confirmed is the EXPONENT, not the mechanism.
  (iii) These are spacecraft-frame FREQUENCY spectra converted to
      wavenumber by Taylor's frozen-flow hypothesis, which is excellent
      here because the wind speed is much larger than the wave speeds,
      but it is an assumption and the module must name it.

  CHECK 2, terrestrial.  Sreenivasan (1995) compiled more than a hundred
  measured spectra, from wind tunnels to a tidal channel, and found the
  Kolmogorov constant of the one-dimensional longitudinal spectrum to be
  0.53 with a standard deviation of 0.055.  K41 does not predict the
  NUMBER; it predicts that the number is the same everywhere.  That is
  what a 10% scatter across a hundred flows and three decades of Reynolds
  number confirms.  Converted with the exact isotropy factor 55/18 that
  the same paper states, the three-dimensional constant is 1.62 +/- 0.17.

  CHECK 3, the price of one of Module 3's idealisations.  SAY IT
  EXACTLY, because an earlier draft of this docstring did not: Module 3
  never named turbulence.  The word does not occur in module03.html.
  What Module 3 did was apply hydrostatic balance to an intracluster
  medium at r = 1 Mpc (its section 3 scale-height table, and Problem
  C3), and list "Static: u = 0" in its section 11 table of
  idealisations, repaid there through Module 4 alone.  CHECK 3 puts a
  number on that idealisation for one cluster core.  Hitomi
  measured the line-of-sight velocity dispersion of the Perseus cluster
  core directly, 164 +/- 10 km/s at 30-60 kpc.  This script reproduces
  the paper's own headline number, turbulent pressure = 4% of thermal,
  from that dispersion and the measured temperature, and turns it into a
  mass bias.  CONFIRMED: hydrostatic equilibrium, the assumption Module 3
  spent its length on, is good to about 4% in this cluster core.
  Whether Module 3's section 11 table gains a row pointing here is
  Simon's decision, open as of 2026-09-19 and bundled with the open
  Module 3 -> Module 9 Proposition 1 pointer.  This module does not
  edit Module 3.

  CHECK 4, the interstellar medium.  Larson (1981) and Solomon et al.
  (1987) fitted the velocity-dispersion-versus-size relation of molecular
  clouds.  Kolmogorov predicts an exponent 1/3; Burgers turbulence, a
  field of shocks, predicts 1/2.  Solomon's exponent is 0.50 +/- 0.05,
  where the +/-0.05 is NOT a formal error: their p. 737 says it "is
  larger than the formal fit error and represents an estimate of the
  systematic error based on several fits to the data with varying
  definitions of cloud boundaries".  So no sigma is quoted anywhere.
  What is quoted is the gap: 1/3 lies 3.3 of those whole envelopes below
  the measured exponent and 1/2 lies on it.  REFUTED: incompressible
  Kolmogorov turbulence does not describe a molecular cloud - and the
  authors say so themselves, "This hypothesis is ruled out by the data
  presented here".

  TWO CONDITIONS ON THAT REFUTATION, both stated in PART G.  FIRST, the
  two quantities are not the same quantity.  delta v(l) ~ l^(1/3) is a
  two-point statistic inside ONE flow; Solomon's exponent comes from a
  regression ACROSS 273 different clouds, one linewidth and one size
  each.  Larson (1981) made that identification explicitly and it is
  standard, but it is an assumption and it is named before the verdict,
  not after.  SECOND, THE DEGENERACY NOTE in PART G: the exponent 1/2 is also
  exactly what virial equilibrium at constant surface density gives, and
  that is how Solomon et al. themselves read it.  The exponent refutes
  Kolmogorov; it does not by itself prove Burgers.

A NOTE ON THE REYNOLDS NUMBERS, stated here because the answer is
uncomfortable and is kept rather than hidden.  Computed from the
COLLISIONAL viscosity with Module 1's mean free paths, the intracluster
medium and the solar wind come out at Reynolds numbers of 0.90 and 12
- far too small to support the cascade that CHECK 1 and CHECK 3 are
measuring.

READ THAT TOGETHER WITH THE KNUDSEN NUMBER, which PART D prints beside
it: 0.375 for the ICM and 1.94 for the solar wind.  By Module 2's
identity Re = 3 Ma_th/Kn the two statements are one statement.  Module 1
established that a Navier-Stokes viscosity requires Kn << 1, so these
are not two weakly turbulent fluids; they are two systems in which the
collisional fluid description does not apply, and the Reynolds numbers
above are formulae evaluated outside their own domain of validity.  That
is the sharper form of the argument and it is what forces the magnetic
rescue rather than merely motivating it.

The resolution is Module 1's magnetic rescue: the transport step across
the field is the gyroradius, not the Coulomb mean free path.  PART D
prints r_g v/3 as a BOUND, not as a value.  Classical Braginskii
perpendicular viscosity scales as (r_g/lambda)^2, not (r_g/lambda), so
r_g v/3 is an upper bound on nu_perp and therefore a LOWER bound on Re
across the field; the classical value is smaller by lambda/r_g, and
neither is the effective viscosity of the intracluster medium, which
microinstabilities set.  This module bounds Re across the field.  It
does not state it.  Both Braginskii coefficients behind that sentence -
eta_0 = 0.96 n T tau_i and eta_1 = (3/10) n T/(omega^2 tau_i) - are read
from the original 1965 Consultants Bureau translation, p. 218, and so is
his definition of tau_i, p. 215.  And the bound has been measured once:
Zhuravleva et al. (2019) find the effective viscosity of the Coma
Cluster suppressed below the Coulomb value "by at least a factor of ~10
to ~1000", so the collisional Reynolds numbers below are floors.

Sources for every published number compared against are listed in the
SOURCES block at the foot of this file and in module10.html.
"""
import math

import numpy as np
from scipy import stats

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m01_numbers.py and m03_numbers.py rather than
# imported, so that each module's numbers script reads on its own.
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
keV = 1.602176634e-9    # erg            (exact, from the SI electronvolt)

GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
Rsun = 6.957e10         # cm             (IAU 2015 nominal)
Msun = GMsun/G          # g

# Module 1's inputs, reused unchanged so the two modules cannot diverge.
SIGMA_H = 1.0e-15       # cm^2   order-of-magnitude neutral atomic cross-section
LAM_AIR = 6.8e-6        # cm     mean free path of room air
SPITZER_C = 3.0**1.5/(4.0*np.sqrt(np.pi))   # = 0.7329, Sarazin (1988) eq. 5.32
# mu of a proton measured against m_u, the Module 3 convention.  Module 9
# uses the same constant under the same name.
MU_H = mp/mu_u          # = 1.00728

# =========================================================================
# PUBLISHED VALUES COMPARED AGAINST.  Each block names the paper, the
# table or equation, and what the quoted error actually means.  Nothing
# in this block was written from memory; each was read out of the PDF.
# =========================================================================

# --- Podesta, Roberts & Goldstein (2007), ApJ 664, 543-548, Table 2. -----
# Wind spacecraft, ecliptic plane near 1 au.  Power-law exponents of the
# trace power spectral density, from linear least squares on log P vs
# log f over 1e-3 Hz <= f <= 1e-2 Hz.  The errors are 99% CONFIDENCE
# LIMITS from the regression, NOT standard deviations, and the paper
# states they "have been rounded up in every case".  The exponents are
# quoted by the paper as positive numbers, i.e. P ~ f^-index.
PODESTA_FIT_LO_HZ = 1.0e-3
PODESTA_FIT_HI_HZ = 1.0e-2
PODESTA_CI_LEVEL = 0.99
PODESTA_CI_TO_SIGMA = 2.5758293035489004   # two-sided Gaussian 99% point
PODESTA = [
    # (interval, start date, days, magnetic, dB, velocity, dV, kinetic, dK,
    #  total E, dE, Alfven ratio range)
    (1, "1995 May 23", 54, 1.66, 0.02, 1.50, 0.02, 1.50, 0.02, 1.60, 0.02,
     (0.5, 1.1)),
    (2, "1997 Dec 14", 54, 1.72, 0.02, 1.59, 0.02, 1.59, 0.02, 1.68, 0.02,
     (0.4, 0.85)),
    (3, "2000 Nov 15", 81, 1.66, 0.01, 1.52, 0.02, 1.57, 0.03, 1.63, 0.02,
     (0.5, 0.8)),
    (4, "2003 Jun 11", 53.854, 1.58, 0.02, 1.50, 0.02, 1.51, 0.02, 1.55,
     0.02, (0.6, 0.85)),
]
# Table 1's four intervals in full, read at step 2: 1995 May 23 to Jul 16
# (54 d), 1997 Dec 14 to 1998 Feb 06 (54 d), 2000 Nov 15 to 2001 Feb 04
# (81 d), 2003 Jun 11 to Aug 03 (53.854 d).  Three cover two solar
# rotations and one covers three; one sits near solar minimum, one near
# maximum, one on the ascending phase and one on the descending phase.
# Section 3 also bounds the fit-window sensitivity: moving the left
# endpoint over 7e-4 to 1.5e-3 Hz and the right over 7e-3 to 1.5e-2 Hz
# changes an exponent "typically by 1%", always less than the tabulated
# error.
PODESTA_WINDOW_SENSITIVITY = 0.01

# --- Sreenivasan (1995), Phys. Fluids 7(11), 2778-2784. -----------------
# His equation (2) defines the constant through the one-dimensional
# LONGITUDINAL spectral density: phi_1(k_1) = C_K <eps>^(2/3) k_1^(-5/3).
# Section V: "the average value of the Kolmogorov constant from Fig. 3 is
# 0.53 with a standard deviation of about 0.055", over R_lambda >~ 50.
# That 0.055 is the SCATTER OF THE POPULATION of >100 experiments, not the
# error on the mean.  Section I gives the exact isotropy conversions.
SREENI_CK = 0.53
SREENI_CK_SD = 0.055
SREENI_RLAMBDA_MIN = 50.0
SREENI_N_SPECTRA = 100          # "more than 100 spectra", Section I
SREENI_3D_FACTOR = 55.0/18.0    # C(3D spectrum)          = (55/18) C_K
SREENI_S2_FACTOR = 4.02         # C(2nd-order structure fn) = 4.02  C_K
# His own final revision, Section V, after allowing for the ~10% that the
# local-isotropy estimate of eps undercounts: "the mean value will have to
# be revised to something like 0.5.  We think that this is about the best
# estimate possible today".
SREENI_CK_REVISED = 0.50
# Table IV, row "Tidal channel / Grant et al.^67 / 50 ft below the water
# surface".  Reference 67 of that paper is H. L. Grant, R. W. Stewart and
# A. Moilliet, "Turbulence spectra from a tidal channel", J. Fluid Mech.
# 12, 241 (1962) - the first clean measurement of the -5/3 range.  The
# 1962 paper itself is behind a publisher paywall and was NOT read; this
# value is read from Sreenivasan's Table IV, and the module says so.
# Footnote k: the value is an average over 17 sets of data, estimated by
# the authors by drawing straight lines through log-log plots of spectra,
# and Kraichnan remarked the estimate would be more than 10% higher under
# a different reading.  Footnote j: the R_lambda range is Sreenivasan's
# estimate, not Grant et al.'s.
GRANT62_CK = 0.47
GRANT62_CK_ERR = 0.02
GRANT62_RLAMBDA = (3000.0, 18000.0)

# --- Hitomi Collaboration (2016), Nature 535, 117-121. -------------------
# "The Quiescent Intracluster Medium in the Core of the Perseus Cluster".
# ALL uncertainties in that paper are quoted at the 90% CONFIDENCE LEVEL,
# which the paper states explicitly; divide by 1.6449 for a Gaussian sigma.
HITOMI_CI_TO_SIGMA = 1.6448536269514722    # two-sided Gaussian 90% point
HITOMI_SIGMA_V = 1.64e7          # cm/s   164 +/- 10 km/s, outer region
HITOMI_SIGMA_V_ERR = 1.0e6       # cm/s   (90% confidence)
HITOMI_R_IN = 30.0*kpc           # inner edge of that region
HITOMI_R_OUT = 60.0*kpc          # outer edge of that region
HITOMI_KT_OUT = 4.1*keV          # 4.1 +/- 0.1 keV, the region measured
HITOMI_KT_OUT_ERR = 0.1*keV
HITOMI_KT_IN = 3.8*keV           # 3.8 +/- 0.1 keV, the central region
HITOMI_SIGMA_V_IN = 1.87e7       # cm/s   187 +/- 13 km/s, central region
HITOMI_SIGMA_V_IN_ERR = 1.3e6
HITOMI_VGRAD = 1.50e7            # cm/s   150 +/- 70 km/s gradient
HITOMI_VGRAD_ERR = 7.0e6
HITOMI_VGRAD_SCALE = 60.0*kpc    # across the 60 kpc image of the core
HITOMI_LYA_SIGMA = 1.60e7        # cm/s   160 +/- 16 km/s from H-like Ly-alpha
HITOMI_LYA_ERR = 1.6e6
# The body says "assuming isotropic turbulence, the ratio of turbulent
# pressure to thermal pressure in the ICM is low at 4%".  The ABSTRACT is
# one-sided and is the sentence the authors signed: "Turbulent pressure
# support in the gas is 4% or less of the thermodynamic pressure, with
# large scale shear at most doubling that estimate."  Step 2 searched the
# main text, the Methods and the Extended Data: NO value more precise than
# 4% exists anywhere in the paper.
HITOMI_PTURB_FRAC_PAPER = 0.04   # their headline "4% or less"
# Systematics the paper lists on the 164 km/s: +/-6 km/s from energy
# resolution, +/-2 km/s from plasma temperature, and an overestimate of
# not more than 3 km/s from the pixel self-calibration scatter.
HITOMI_SYS = (6.0e5, 2.0e5, 3.0e5)
MU_ICM = 0.61                    # mean molecular weight, fully ionised ICM

# --- Larson (1981), MNRAS 194, 809-826, equation (1). -------------------
# sigma(km/s) = 1.10 L(pc)^0.38, for 0.1 <~ L <~ 100 pc, where sigma is the
# THREE-dimensional internal velocity dispersion.  THE LINE IS EYE-FITTED:
# the paper says "the eye-fitted dashed straight line", so there is NO
# formal uncertainty on 0.38 and none may be quoted.  What the paper does
# give is the scatter: "The rms deviation of log sigma from this relation
# is 0.14, corresponding to a factor of 1.38 in sigma."
LARSON_A = 1.10                  # km/s at L = 1 pc
LARSON_EXP = 0.38
LARSON_RMS_LOG = 0.14
LARSON_L_RANGE = (0.1, 100.0)    # pc
# p. 814: sigma is "the total three-dimensional rms velocity of all internal
# motions", built by adding contributions to sigma^2, of which the third is
# thermal and "has been assumed to be sigma_s = 0.32 km s^-1, as appropriate
# for molecular gas at a temperature of 10 K".  It is added INTO a 3D sigma,
# so it is the THREE-dimensional thermal dispersion, and the arithmetic
# agrees: at T = 10 K and mu = 2.33, sqrt(3kT/mu m_u) = 0.327 km/s while
# sqrt(kT/mu m_u) = 0.189 km/s.  Never compare it with a 1D linewidth.
LARSON_SIGMA_THERMAL = 0.32      # km/s, his THREE-dimensional 10 K value

# --- Solomon, Rivolo, Barrett & Yahil (1987), ApJ 319, 730-741, eq. (1).
# sigma_v = (1.0 +/- 0.1) S^(0.5 +/- 0.05) km/s, S in parsecs, from a
# linear least-squares regression on the logs of the 273-cloud catalogue
# using the calibrator clouds only.  Verified against a rendered image of
# page 731, not against the OCR text layer.
#
# THE +/-0.05 IS NOT A FORMAL ERROR, and the paper says so on p. 737:
# "The quoted error in the exponent is larger than the formal fit error
# and represents an estimate of the systematic error based on several fits
# to the data with varying definitions of cloud boundaries."  So it is a
# spread over modelling choices - over what counts as the edge of a cloud
# - and NO NUMBER OF SIGMAS MAY BE COMPUTED FROM IT.  The step-1 prep
# treated it as 1 sigma and flagged the assumption; the source has now
# answered, and the answer is that the assumption is wrong in kind.  The
# refutation gets STRONGER: the formal statistical error is smaller than
# 0.05, so 1/3 lies further from 0.5 in statistical terms, not nearer.
SOLOMON_A = 1.0                  # km/s at S = 1 pc
SOLOMON_A_ERR = 0.1
SOLOMON_EXP = 0.5
SOLOMON_EXP_ERR = 0.05
SOLOMON_SCATTER_LOG = 0.11       # "The dispersion in log(sigma_v) is +/-0.11"
SOLOMON_N_CLOUDS = 273
SOLOMON_SIGMA_IS_1D = True       # sigma_v is a line-of-sight linewidth
SOLOMON_SURFACE_DENSITY = 170.0  # Msun/pc^2, their constant mean value
# p. 737: "We note that without the 2 km s^-1 extrapolation in velocity,
# the constant in equation (1) is 0.83 - a reduction of 17%."  SOLOMON_A
# is therefore a choice of line-width definition worth 17 per cent, and
# every Mach number printed along the relation inherits it.
SOLOMON_A_NO_EXTRAP = 0.83

# --- Federrath, Roman-Duval, Klessen, Schmidt & Mac Low (2010), ---------
# A&A 512, A81, equations (19) and (20) and Figure 8.
# sigma_s^2 = ln(1 + b^2 M^2) for the log density s = ln(rho/<rho>), and
# b falls smoothly from about 1 for purely compressive forcing to about
# 1/3 in 3D for purely solenoidal forcing.
FED_B_SOLENOIDAL = 1.0/3.0
FED_B_COMPRESSIVE = 1.0

# --- predictions, held as named constants so no magic number appears ----
KOLMOGOROV_SPEC = 5.0/3.0        # E(k) ~ k^-5/3
KOLMOGOROV_DELTA_V = 1.0/3.0     # delta v(l) ~ l^1/3
BURGERS_SPEC = 2.0               # E(k) ~ k^-2 for a field of shocks
BURGERS_DELTA_V = 1.0/2.0        # delta v(l) ~ l^1/2
IK_SPEC = 3.0/2.0                # Iroshnikov-Kraichnan / Boldyrev, k^-3/2
FOUR_FIFTHS = 4.0/5.0            # S_3(l) = -(4/5) eps l, exact


# =========================================================================
# PART A.  The Reynolds number
# =========================================================================

def reynolds(U, L, nu):
    """Re = U L / nu, the ratio of the inertial to the viscous term.

    Derived in Section 2 of module10.html: in the Navier-Stokes equation
    of Module 2, (u.grad)u scales as U^2/L and nu grad^2 u as nu U/L^2,
    and the ratio of the two is U L / nu.
    """
    return U*L/nu


def nu_kinetic(lam, v_th):
    """Kinematic viscosity of a dilute gas from kinetic theory, nu = lam v/3.

    The standard Chapman-Enskog result of Module 1: momentum is carried a
    mean free path between collisions by particles moving at the thermal
    speed, so the momentum diffusivity is of order lam v_th, with 1/3 from
    averaging over directions.  It is an order-of-magnitude coefficient,
    not an exact one; PART D prints the Braginskii value alongside.
    """
    return lam*v_th/3.0


def v_thermal(T, mu):
    """Mean thermal speed sqrt(8 k T / (pi mu m_u)), the kinetic-theory
    speed that enters the viscosity."""
    return np.sqrt(8.0*kB*T/(np.pi*mu*mu_u))


def sound_speed(T, mu, gamma=5.0/3.0):
    """Adiabatic sound speed sqrt(gamma k T/(mu m_u))."""
    return np.sqrt(gamma*kB*T/(mu*mu_u))


def debye(n, T):
    """Electron Debye length sqrt(k T/(4 pi n e^2)).  From m01_numbers.py."""
    return np.sqrt(kB*T/(4.0*np.pi*n*e*e))


def b_min_e(T):
    """Smallest usable impact parameter for electrons: the larger of the
    classical 90-degree impact parameter e^2/(3 k T) and the thermal de
    Broglie length.  From m01_numbers.py."""
    ve = np.sqrt(3.0*kB*T/me)
    return max(e*e/(3.0*kB*T), hbar/(me*ve))


def lnLambda_e(n, T):
    """Coulomb logarithm ln(lambda_D/b_min).  From m01_numbers.py, so the
    solar-wind viscosity below is derived, not guessed at."""
    return np.log(debye(n, T)/b_min_e(T))


def lam_coulomb(n, T, lnL, coef=SPITZER_C):
    """Thermal Coulomb mean free path, Module 1 equation and coefficient:
        lambda = coef (k T)^2 / (n e^4 ln Lambda),   coef = 3^(3/2)/(4 sqrt(pi)).

    NOTE THE MASS: there is none.  The same expression therefore gives the
    ion mean free path as the electron one, to leading order, which is why
    Module 1's 22.5 kpc may be used here for the ION viscosity.
    """
    return coef*(kB*T)**2/(n*e**4*lnL)


def gyroradius(T, B, m=mp, Z=1):
    """Thermal gyroradius r_g = m v_th c/(Z e B), v_th = sqrt(2 k T/m).
    Copied from m01_numbers.py."""
    vth = np.sqrt(2.0*kB*T/m)
    return m*vth*c/(Z*e*B)


def tau_braginskii(T, lam, m=mp):
    """Braginskii's ION COLLISION TIME, his eq. (2.5i), p. 215.

    He does not leave tau_i free.  He defines it:
        tau_i = 3 sqrt(m_i) T_i^(3/2)/(4 sqrt(pi) lnLambda e^4 Z^4 n_i),
    with T in energy units.  For Z = 1 that closed form is IDENTICALLY
    Module 1's Coulomb mean free path over the RMS thermal speed:
        lam/sqrt(3kT/m) = [3^(3/2)/(4 sqrt(pi))] (kT)^2/(n e^4 lnLambda)
                          x sqrt(m/(3kT))
                        = [3/(4 sqrt(pi))] sqrt(m) (kT)^(3/2)/(n e^4 lnL),
    because 3^(3/2)/(4 sqrt(pi)) divided by sqrt(3) is 3/(4 sqrt(pi)).

    THAT IS NOT A VALIDATION OF MODULE 1.  The Spitzer thermal mean free
    path is DEFINED as v_rms tau, so the two coefficients are one
    convention written two ways.  What it fixes is WHICH convention this
    book uses - Braginskii's, at the rms speed - and that is what makes
    nu_braginskii below exact rather than approximate.
    """
    return lam/np.sqrt(3.0*kB*T/m)


def nu_braginskii(T, lam, m=mp):
    """Braginskii unmagnetised ION viscosity, nu = 0.96 k T tau_i/m_i.

    His eq. (2.22), p. 218: eta_0^i = 0.96 n_i T_i tau_i.  Dividing by
    rho = n_i m_i gives the kinematic viscosity, and tau_i is his own
    eq. (2.5i), computed here rather than passed in.

    NO SPEED IS AN ARGUMENT, deliberately.  The earlier version took one,
    to stop the caller feeding this function and nu_kinetic two different
    thermal speeds - the prep review found exactly that, a sqrt(2kT/m_p)
    here against a mean speed at mu = 0.61 there, two errors cancelling to
    a ratio of 0.993 that looked like a validation.  A DEFINED tau_i does
    that job better: nothing is left for a caller to get wrong.

    With tau_i = lam/v_rms and kT/m = v_rms^2/3 the result collapses:
        nu_Braginskii = 0.96 (v_rms^2/3)(lam/v_rms) = 0.96 (lam v_rms/3),
    EXACTLY.  Braginskii's coefficient IS the correction to the elementary
    lam v/3 of kinetic theory, at the same rms speed: 0.96 against 1.

    This module's nu_kinetic uses the MEAN speed sqrt(8kT/(pi m)) instead,
    so the ratio it prints is
        nu_Braginskii/(lam v_mean/3) = 0.96 v_rms/v_mean
                                     = 0.96 sqrt(3 pi/8) = 1.0420,
    independent of temperature, density and mean free path.  Print both,
    each with the convention that produces it: 0.96 at one speed, 1.042
    across two.
    """
    return 0.96*kB*T*tau_braginskii(T, lam, m)/m


# =========================================================================
# PART B.  Kolmogorov 1941 by dimensional analysis
# =========================================================================

def kolmogorov_scale(nu, eps):
    """eta = (nu^3/eps)^(1/4), the only length that can be built from a
    viscosity (cm^2/s) and a dissipation rate per unit mass (cm^2/s^3)."""
    return (nu**3/eps)**0.25


def kolmogorov_velocity(nu, eps):
    """u_eta = (nu eps)^(1/4).  Note u_eta eta/nu = 1 exactly: the
    Reynolds number of the smallest eddy is one, by construction."""
    return (nu*eps)**0.25


def kolmogorov_time(nu, eps):
    """tau_eta = (nu/eps)^(1/2), the turnover time of the smallest eddy."""
    return np.sqrt(nu/eps)


def eps_from_outer(U, L):
    """eps = U^3/L, the dissipation rate the cascade must carry.

    In steady state the energy fed in at the outer scale is passed down
    unchanged, so eps is fixed by the outer scale alone and does NOT
    depend on the viscosity.  This is the single most useful consequence
    of K41 and it is what makes every number in PART E computable.
    """
    return U**3/L


def delta_v(eps, l):
    """delta v(l) = (eps l)^(1/3), the K41 velocity increment."""
    return (eps*l)**(1.0/3.0)


def E_of_k(C, eps, k):
    """E(k) = C eps^(2/3) k^(-5/3), the K41 inertial-range spectrum."""
    return C*eps**(2.0/3.0)*k**(-KOLMOGOROV_SPEC)


def S3_exact(eps, l):
    """The 4/5 law: S_3(l) = <(delta u_L)^3> = -(4/5) eps l.

    This is the one exact non-trivial result of turbulence theory,
    derived from Navier-Stokes with no closure, for homogeneous isotropic
    turbulence at high Reynolds number.  Its sign is the direction of the
    cascade: energy flows to small scales.
    """
    return -FOUR_FIFTHS*eps*l


def dof_from_reynolds(Re):
    """Degrees of freedom (L/eta)^3 = Re^(9/4).

    L/eta = (U L/nu)^(3/4) = Re^(3/4) follows from eta = (nu^3/eps)^(1/4)
    with eps = U^3/L; cubing it gives the number of grid points a direct
    numerical simulation needs.  Proposition 7 of module10.html.
    """
    return Re**2.25


def grid_side_from_reynolds(Re):
    """L/eta = Re^(3/4), the number of grid points along one side."""
    return Re**0.75


# =========================================================================
# PART F.  Supersonic turbulence
# =========================================================================

def lognormal_sigma_s(b, M):
    """sigma_s^2 = ln(1 + b^2 M^2), Federrath et al. (2010) eq. (19),
    with s = ln(rho/<rho>) and M the RMS sonic Mach number."""
    return np.sqrt(np.log(1.0 + b*b*M*M))


def lognormal_sigma_rho(b, M):
    """sigma_rho/<rho> = b M, Federrath et al. (2010) eq. (18)."""
    return b*M


def lognormal_peak_s(sigma_s):
    """The log-normal PDF of s has mean s0 = -sigma_s^2/2, forced by
    <rho/<rho>> = 1.  The most probable DENSITY is therefore below the
    mean density by exp(-sigma_s^2/2)."""
    return -0.5*sigma_s*sigma_s


def volume_fraction_above(x, sigma_s):
    """Fraction of the VOLUME with rho/<rho> > x, for a log-normal PDF.

    With s = ln(rho/<rho>) normally distributed with mean s_0 =
    -sigma_s^2/2 and width sigma_s, the fraction above the threshold is
        f(>x) = (1/2) erfc[ (ln x - s_0)/(sigma_s sqrt(2)) ].
    The mean s_0 is not free: it is forced by <rho/<rho>> = 1, which for
    a log-normal means exp(s_0 + sigma_s^2/2) = 1.
    """
    s0 = -0.5*sigma_s*sigma_s
    return 0.5*math.erfc((math.log(x) - s0)/(sigma_s*math.sqrt(2.0)))


def larson_sigma(L_pc):
    """Larson (1981) eq. (1): sigma(km/s) = 1.10 L(pc)^0.38, 3D."""
    return LARSON_A*L_pc**LARSON_EXP


def solomon_sigma(S_pc):
    """Solomon et al. (1987) eq. (1): sigma_v(km/s) = 1.0 S(pc)^0.50, 1D."""
    return SOLOMON_A*S_pc**SOLOMON_EXP


# =========================================================================
# CHECK support
# =========================================================================

def sigma_departure(measured, err, predicted):
    """(measured - predicted)/err, with err in whatever units the caller
    passes.  Returns a signed number of error widths."""
    return (measured - predicted)/err


def turbulent_pressure_fraction(sigma_1d, kT, mu=MU_ICM):
    """P_turb/P_thermal for isotropic turbulence with 1D dispersion sigma.

    For isotropic turbulence the turbulent pressure is (1/3) rho <v^2> =
    (1/3) rho (3 sigma_1d^2) = rho sigma_1d^2.  The thermal pressure of an
    ideal gas is rho k T/(mu m_u).  The ratio is therefore
        mu m_u sigma_1d^2/(k T),
    in which the density cancels: it needs no density measurement at all,
    which is exactly why Hitomi could quote it from a line width and a
    temperature.
    """
    return mu*mu_u*sigma_1d*sigma_1d/kT


def mass_bias(alpha):
    """Fractional underestimate of a cluster mass from ignoring turbulence.

    Hydrostatic equilibrium with the total pressure gives
        G M_true rho/r^2 = -d(P_th + P_turb)/dr,
    while the X-ray observer, who sees only P_th, infers M_HSE from
        G M_HSE rho/r^2 = -dP_th/dr.
    IF P_turb/P_th = alpha is constant with radius - which is an
    assumption, and is stated as one - then M_true = (1+alpha) M_HSE, and
    the fractional bias is 1 - M_HSE/M_true = alpha/(1+alpha).
    """
    return alpha/(1.0 + alpha)


def alpha_for_bias(b):
    """Invert mass_bias: the P_turb/P_th needed to bias a mass by b."""
    return b/(1.0 - b)


def sigma_for_alpha(alpha, kT, mu=MU_ICM):
    """The 1D velocity dispersion that gives a stated P_turb/P_th."""
    return np.sqrt(alpha*kT/(mu*mu_u))


# =========================================================================
# Reporting
# =========================================================================

def main():
    P = print
    P('=' * 74)
    P('MODULE 10 NUMBERS: turbulence')
    P('=' * 74)

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  The Reynolds number, and what it is made of')
    P('-'*74)
    P('  Re = U L / nu.  The transition to turbulence in a smooth pipe is')
    P('  at Re of about 2300; a flat-plate boundary layer goes at about')
    P('  5e5.  Both are quoted as inputs, not checked here.')
    P('  Module 2 closed with Re = 3 Ma_th / Kn, which says the same thing')
    P('  in Module 1\'s variables: turbulence needs a SMALL Knudsen number.')
    P('  Ma_th is U divided by the MEAN THERMAL SPEED, not by the sound')
    P('  speed; the two differ by a factor of order one that is carried')
    P('  through rather than rounded away.')
    P(f'  {"system":<26} {"Kn = lam/L":>11} {"Ma_th = U/v":>12} {"3 Ma/Kn":>12}')
    # Every Kn below is computed from the same mean free paths PART D uses.
    # Module 1's photosphere: n = P/kT at tau = 2/3, P = 1.2e5 dyn/cm^2.
    n_phot = 1.2e5/(kB*5772.0)
    lam_phot = 1.0/(n_phot*SIGMA_H)
    H_phot = 1.5e7                      # cm, the 150 km scale height
    v_phot = v_thermal(5772.0, 1.30)
    A_ROWS = [
        ('laboratory air, L = 1 m', LAM_AIR, 1.0e2,
         1.0e3, v_thermal(288.15, 28.9647)),
        ('solar photosphere, L = H', lam_phot, H_phot, 2.0e5, v_phot),
    ]
    for name, lam, L, U, vth in A_ROWS:
        Kn, Ma = lam/L, U/vth
        P(f'  {name:<26} {Kn:>11.3e} {Ma:>12.4f} {3.0*Ma/Kn:>12.3e}')
    P('  The photosphere line uses Module 1\'s photospheric number density')
    P(f'  n = P/kT = {n_phot:.3e} cm^-3 at P = 1.2e5 dyn/cm^2, T = 5772 K,')
    P(f'  giving lam = {lam_phot*1e4:.0f} micron against a 150 km scale height.')
    P('  PART D computes the same quantity for the four fluids this module')
    P('  cares about, and checks U L/nu against 3 Ma/Kn line by line.')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  Kolmogorov 1941 by dimensional analysis')
    P('-'*74)
    P('  Inputs available in the inertial range: eps [cm^2/s^3] and k [1/cm].')
    P('  E(k) has dimensions cm^3/s^2, because integrating it over k must')
    P('  give an energy per unit mass, cm^2/s^2.  Write E = C eps^a k^b:')
    P('    seconds:      -2 = -3a          ->  a = 2/3')
    P('    centimetres:   3 =  2a - b      ->  b = 2a - 3 = -5/3')
    P(f'    E(k) = C eps^(2/3) k^(-{KOLMOGOROV_SPEC:.4f}), with C the one number')
    P('    dimensional analysis cannot supply.  CHECK 2 measures it.')
    P('  Dissipation scale: the only length from nu [cm^2/s] and eps is')
    P('    eta = (nu^3/eps)^(1/4).')
    P('  Velocity increment: the only speed from eps and l is')
    P(f'    delta v(l) = (eps l)^(1/3), i.e. exponent {KOLMOGOROV_DELTA_V:.4f}.')
    P(f'  The exact 4/5 law: S_3(l) = -(4/5) eps l = -{FOUR_FIFTHS:.1f} eps l,')
    P('    the only exact non-trivial result in the subject, and the only')
    P('    one with no adjustable constant.  Its minus sign is the')
    P('    direction of the cascade.')
    P(f'  Kolmogorov constant, three ways, from C_K = {SREENI_CK} (CHECK 2):')
    P(f'    one-dimensional longitudinal spectrum  C_K  = {SREENI_CK:.3f}')
    P(f'    three-dimensional spectrum   (55/18) C_K   = '
      f'{SREENI_3D_FACTOR*SREENI_CK:.3f}')
    P(f'    second-order structure fn     4.02  C_K    = '
      f'{SREENI_S2_FACTOR*SREENI_CK:.3f}')

    # ---------------------------------------------------------------- C
    P('')
    P('PART C.  The number of degrees of freedom')
    P('-'*74)
    P('  L/eta = Re^(3/4), so N = (L/eta)^3 = Re^(9/4).')
    P('  The number of TIME STEPS is set by the CFL condition, not by the')
    P('  Kolmogorov time.  A code is limited by the LARGEST velocity on the')
    P('  SMALLEST cell, dt ~ eta/U, so one outer turnover L/U costs')
    P('    (L/U)/(eta/U) = L/eta = Re^(3/4) steps,')
    P('  and Re^(9/4) x Re^(3/4) = Re^3 point-updates.  Re^3 is the')
    P('  standard result (Pope, Turbulent Flows, sec. 9.1.2).')
    P('  The softer count, L/U divided by the Kolmogorov time')
    P('  tau_eta = (nu/eps)^(1/2), gives Re^(1/2) steps and Re^(11/4)')
    P('  updates.  It is the turnover count of the smallest eddy, not the')
    P('  step a code takes, and it UNDERSTATES the cost by U/u_eta =')
    P('  Re^(1/4).  Both columns are printed so the difference is visible.')
    P(f'  {"Re":>10} {"L/eta":>10} {"N = Re^9/4":>12} {"snapshot":>12} '
      f'{"CFL steps":>10} {"work Re^3":>11} {"Re^(11/4)":>11}')
    for Re in (1e3, 1e4, 1e6, 1e8, 1e10, 1e12):
        N = dof_from_reynolds(Re)
        P(f'  {Re:>10.0e} {grid_side_from_reynolds(Re):>10.4g} '
          f'{N:>12.4g} {24.0*N:>11.4g}B {Re**0.75:>10.3g} '
          f'{Re**3:>11.3g} {N*np.sqrt(Re):>11.3g}')
    P('  READ: three velocity components at 8 bytes each, so 24 bytes per')
    P(f'  point.  At Re = 1e6 a single snapshot is {24.0*dof_from_reynolds(1e6)/1e12:.0f} TB and one outer')
    P(f'  turnover costs {1e6**3:.1e} point-updates on the CFL count, or')
    P(f'  {dof_from_reynolds(1e6)*np.sqrt(1e6):.1e} on the Kolmogorov-time count.  Section 8 puts the')
    P('  interstellar Reynolds number into this table; PART E does the')
    P('  arithmetic.  This is why Module 14 exists.')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  Reynolds numbers of four fluids')
    P('-'*74)

    # (a) Earth's atmosphere.
    T_air, mu_air = 288.15, 28.9647
    v_air = v_thermal(T_air, mu_air)
    nu_air_kin = nu_kinetic(LAM_AIR, v_air)
    # STILL UNSOURCED after step 2, and now printed to TWO figures because
    # of it.  The NIST-standard reference for air viscosity - Kadoya,
    # Matsunaga & Nagashima (1985), JPCRD 14, 947, DOI 10.1063/1.555744,
    # whose existence Crossref confirms - is not served by NIST, ADS or
    # AIP at any URL tried, and the ISA route (Sutherland at 288.15 K over
    # rho = 1.225 kg/m^3, giving 0.146) would mean importing two constants
    # this module needs for nothing else.  The book has not measured a
    # third digit here, so it does not print one: every ratio against this
    # number below carries two significant figures.
    NU_AIR_MEAS = 0.15       # cm^2/s, sea-level dry air near 288 K, 2 s.f.
    P('  (a) Earth\'s atmosphere, 288.15 K, mu = 28.96')
    P(f'      mean thermal speed                 = {v_air/1e2:.1f} m/s')
    P(f'      lam v/3 with Module 1\'s lam = 68 nm = {nu_air_kin:.4f} cm^2/s')
    P(f'      measured kinematic viscosity       = {NU_AIR_MEAS:.2f} cm^2/s '
      f'(2 s.f., NO PRIMARY SOURCE)')
    P(f'      ratio kinetic theory / measured    = {nu_air_kin/NU_AIR_MEAS:.2f}')
    P('      (kinetic theory is right to 30% with a coefficient of 1/3;')
    P('       every Reynolds number below uses the measured value where')
    P('       one exists and the kinetic-theory value where none does)')
    U_atm, L_atm = 1.0e3, 1.0e5     # 10 m/s over 1 km
    Re_atm = reynolds(U_atm, L_atm, NU_AIR_MEAS)
    P(f'      Re for U = 10 m/s, L = 1 km        = {Re_atm:.3e}')
    P(f'      Re for U = 10 m/s, L = 1 m         = '
      f'{reynolds(U_atm, 1.0e2, NU_AIR_MEAS):.3e}')

    # (b) molecular cloud.
    T_mc, mu_mc, n_mc = 10.0, 2.33, 1.0e2
    lam_mc = 1.0/(n_mc*SIGMA_H)
    v_mc = v_thermal(T_mc, mu_mc)
    nu_mc = nu_kinetic(lam_mc, v_mc)
    cs_mc = sound_speed(T_mc, mu_mc)
    L_mc, U_mc = 10.0*pc, 2.64e5    # 10 pc, and Larson's sigma there
    Re_mc = reynolds(U_mc, L_mc, nu_mc)
    P('')
    P('  (b) Molecular cloud, 10 K, mu = 2.33, n = 1e2 cm^-3')
    P(f'      neutral mean free path 1/(n sigma) = {lam_mc:.3e} cm '
      f'= {lam_mc/AU:.2f} au')
    P(f'      mean thermal speed                 = {v_mc/1e5:.4f} km/s')
    P(f'      sound speed (gamma = 5/3)          = {cs_mc/1e5:.4f} km/s')
    P(f'      nu = lam v/3                       = {nu_mc:.4e} cm^2/s')
    P(f'      Larson sigma at L = 10 pc          = {larson_sigma(10.0):.3f} km/s')
    P(f'      Re = sigma L / nu                  = {Re_mc:.3e}')
    P(f'      Mach number sigma_3d/c_s           = '
      f'{larson_sigma(10.0)*1e5/cs_mc:.2f}  (supersonic)')
    P(f'      eddy turnover time L/sigma         = '
      f'{L_mc/U_mc/yr/1e6:.2f} Myr')
    P(f'      DNS grid this Re needs             = '
      f'{dof_from_reynolds(Re_mc):.3e} points')

    # (c) intracluster medium.
    n_icm, T_icm, lnL_icm = 1.0e-3, 1.0e8, 37.8
    lam_icm = lam_coulomb(n_icm, T_icm, lnL_icm)
    # THE VISCOSITY OF A PLASMA IS AN ION VISCOSITY: momentum is carried by
    # the ions, so the speed in lam v/3 is the ION mean thermal speed, not
    # the mean speed of an average particle at mu = 0.61.  MU_ICM = 0.61 is
    # a mass per PARTICLE, electrons included, and it belongs in the sound
    # speed and in the pressure ratio of CHECK 3, not here.  Using it here
    # inflated nu by sqrt(1.00728/0.61) = 1.285.
    v_icm = v_thermal(T_icm, MU_H)
    nu_icm_kin = nu_kinetic(lam_icm, v_icm)
    v_icm_rms = np.sqrt(3.0*kB*T_icm/mp)   # Braginskii's speed, not ours
    nu_icm_brag = nu_braginskii(T_icm, lam_icm)
    L_icm, U_icm = HITOMI_R_OUT, HITOMI_SIGMA_V
    Re_icm = reynolds(U_icm, L_icm, nu_icm_kin)
    B_icm = 1.0e-5                   # 1 microgauss, a typical ICM field
    rg_icm = gyroradius(T_icm, B_icm)
    # NOT the classical perpendicular viscosity.  Braginskii (1965) p. 218
    # eq. (2.23) gives eta_1^i = (3/10) n_i T_i/(omega_i^2 tau_i) against
    # eq. (2.22)'s eta_0^i = 0.96 n_i T_i tau_i, so nu_perp/nu_par =
    # (3/10)/0.96 (omega_i tau_i)^-2 = 0.3125 (r_g/lam)^2, using
    # omega_i tau_i = lam/r_g.  Both equations were read from the original
    # Consultants Bureau translation, not from a review.  A SQUARED ratio,
    # because the step shrinks to r_g but
    # the randomisation time is still the collision time.  Substituting
    # r_g for lam in lam v/3 uses the gyro transit as the decorrelation
    # time instead, which is what "magnetised" says does not happen.  What
    # it therefore is, is an UPPER BOUND on nu_perp: a random walk of step
    # r_g cannot decorrelate faster than the gyro period, so
    # D_perp = r_g^2/tau <= r_g v whenever omega_c tau > 1.  An upper
    # bound on nu is a LOWER bound on Re, and every number below says so.
    nu_icm_mag = nu_kinetic(rg_icm, v_icm)
    nu_icm_perp_class = 0.3125*nu_icm_brag*(rg_icm/lam_icm)**2
    P('')
    P('  (c) Intracluster medium, n = 1e-3 cm^-3, T = 1e8 K, ln Lambda = 37.8')
    P(f'      Coulomb mean free path             = {lam_icm/kpc:.1f} kpc '
      f'(Module 1: 22.5 kpc)')
    P(f'      ion mean thermal speed sqrt(8kT/pi m_p) = {v_icm/1e5:.0f} km/s')
    P(f'      nu = lam v/3                       = {nu_icm_kin:.4e} cm^2/s')
    P(f'      ion RMS speed sqrt(3kT/m_p)        = {v_icm_rms/1e5:.0f} km/s')
    P(f'      Braginskii tau_i, his eq. (2.5i)   = '
      f'{tau_braginskii(T_icm, lam_icm):.4e} s')
    P('        which is lam/v_rms EXACTLY: 3^(3/2)/(4 sqrt(pi)) over')
    P('        sqrt(3) is 3/(4 sqrt(pi)), his coefficient.  That does NOT')
    P('        validate Module 1 - a Spitzer mean free path IS v_rms tau.')
    P('        It fixes which convention this book uses: Braginskii\'s.')
    P(f'      nu Braginskii, 0.96 kT tau_i/m_i   = {nu_icm_brag:.4e} cm^2/s')
    P(f'      ratio to lam v_rms/3               = '
      f'{nu_icm_brag/nu_kinetic(lam_icm, v_icm_rms):.4f}')
    P('        = 0.96 exactly, since kT/m = v_rms^2/3.  Braginskii\'s')
    P('        coefficient IS the correction to the elementary lam v/3 of')
    P('        kinetic theory, at the same speed: 0.96 against 1.  THAT is')
    P('        the check on the COEFFICIENT, and it is on nothing else.')
    P(f'      ratio to lam v_mean/3 as printed above = '
      f'{nu_icm_brag/nu_icm_kin:.4f}')
    P('        = 0.96 sqrt(3 pi/8), whatever the temperature, density or')
    P('        mean free path.  The extra 8.5 per cent is the mean speed')
    P('        against the rms speed, NOT a second coefficient.')
    P(f'      v_mean/v_rms = sqrt(8/(3 pi))      = {v_icm/v_icm_rms:.4f}')
    P('        which is the whole of the gap between the 0.9600 above and')
    P('        the 1.0420 above it: 0.96/0.9213 = 1.0420.  It is a')
    P('        COMPONENT-COUNT statement, not a physical one - both')
    P('        speeds are 3-D, and they differ only in whether the')
    P('        average is taken of v or of v^2.')
    P(f'      Re at Hitomi\'s L = 60 kpc, V = 164 km/s = {Re_icm:.2f}')
    P(f'      Re at L = 1 Mpc, V = 300 km/s      = '
      f'{reynolds(3.0e7, Mpc, nu_icm_kin):.1f}')
    P(f'        READ THAT ROW NARROWLY.  It carries the CORE mean free')
    P(f'        path, {lam_icm/kpc:.1f} kpc at n = 1e-3 and T = 1e8, out to a')
    P('        larger L.  It is NOT a cluster outskirts: lam scales as')
    P('        T^2/(n ln Lambda), and a real cluster at 1 Mpc has a lower')
    P('        density, which raises lam and lowers Re again.  Module 3')
    P('        section 3 put its ICM at r = 1 Mpc but gave no density')
    P('        there, so this book has no sourced (n, T) pair at that')
    P('        radius and the row may not be read as one.  What the two')
    P('        rows together DO support, and NOTHING WIDER, is this.  The')
    P('        only ICM Knudsen number this book sources is Hitomi\'s, at')
    P('        30-60 kpc, and it is 0.375.  Zhuravleva\'s offset Coma')
    P('        region has lam about 30 kpc, but this book has no scale L')
    P('        for her fluctuation spectrum, so NO Knudsen number may be')
    P('        computed from it - what may be quoted is her own')
    P('        conclusion, that "the assumption of a')
    P('        Coulomb-collision-dominated plasma is ruled out for the')
    P('        Coma Cluster".  One sourced Kn of 0.375, and one paper')
    P('        ruling the collisional description out in a second')
    P('        cluster, is the whole of the evidence, and the prose may')
    P('        not widen it into "everywhere the data reach".')
    P(f'      Kn = lam/L at 60 kpc               = {lam_icm/L_icm:.3f}')
    P('      READ THE TWO TOGETHER.  Re < 1 BECAUSE Kn > 1/3, and by')
    P('      Module 2\'s identity Re = 3 Ma_th/Kn those are one statement,')
    P('      not two.  At Kn = 0.375 the Chapman-Enskog expansion of')
    P('      Module 1 is failing, so the number above is a formula')
    P('      evaluated outside its own domain of validity.  It does not')
    P('      say the ICM is a barely turbulent fluid.  It says the')
    P('      collisional fluid description does not apply to the ICM.')
    P(f'      Proton gyroradius at B = 1 microgauss = {rg_icm:.3e} cm '
      f'= {rg_icm/AU:.2e} au')
    P(f'      lam / r_g                          = {lam_icm/rg_icm:.3e}')
    P(f'      nu across the field, lam -> r_g    = {nu_icm_mag:.4e} cm^2/s')
    P(f'      Re across the field                >= '
      f'{reynolds(U_icm, L_icm, nu_icm_mag):.3e}')
    P('      THAT is the cascade CHECK 3 measures.  It exists because the')
    P('      field, not the collisions, sets the transport step.')
    P(f'      For contrast, the CLASSICAL perpendicular viscosity,')
    P(f'      0.3125 nu_par (r_g/lam)^2         = '
      f'{nu_icm_perp_class:.4e} cm^2/s,')
    P(f'      which would give Re_perp           = '
      f'{reynolds(U_icm, L_icm, nu_icm_perp_class):.3e}.')
    # STEP 4 CORRECTION.  This line used to print lam/r_g = 5.18e13 as the
    # factor between the two bounds, which is NOT what the two printed
    # viscosities differ by.  nu_Bohm/nu_perp_class =
    # (r_g v_mean/3)/(0.3125 * 0.96 * lam v_rms/3 * (r_g/lam)^2)
    #   = (v_mean/v_rms)/0.3 * (lam/r_g) = 3.07 lam/r_g,
    # because the classical value is built on BRAGINSKII's nu_par, which
    # carries his 0.96 and his RMS speed, not this module's lam v_mean/3.
    # The spot-check did not catch it: it compared lam/r_g against
    # lam/r_g and never asked whether that ratio was the bracket.
    P(f'      The two bracket the truth by a factor '
      f'{nu_icm_mag/nu_icm_perp_class:.2e}, which is')
    P(f'      {(nu_icm_mag/nu_icm_perp_class)/(lam_icm/rg_icm):.2f} times '
      f'lam/r_g = {lam_icm/rg_icm:.2e} and NOT lam/r_g itself, because')
    P('      the classical value is built on Braginskii nu_par, which')
    P('      carries his 0.96 and his RMS speed.  And')
    P('      NEITHER is the effective viscosity of the intracluster medium,')
    P('      which is set by pressure-anisotropy microinstabilities that')
    P('      scatter ions far more often than Coulomb collisions do.  This')
    P('      module BOUNDS Re across the field.  It does not state it.')
    P('      AND THE BOUND HAS BEEN MEASURED ONCE.  Zhuravleva et al.')
    P('      (2019), Nat. Astron. 3, 832, compared a 12-day Chandra image')
    P('      of an offset region of the Coma Cluster - where the lower')
    P('      density raises lam to about 30 kpc - against direct numerical')
    P('      simulation, and found no viscous cutoff where a')
    P('      Coulomb-collisional plasma must have one.  Their conclusion:')
    P('      "the effective viscosity must be suppressed by at least a')
    P('      factor of ~10 to ~1000 for Pr <= 1".  So the collisional')
    P(f'      Re of {Re_icm:.2f} printed above is a FLOOR that one')
    P('      observation lifts by one to three orders of magnitude.')
    P('      TWO CAVEATS, both theirs: the factor depends on the Prandtl')
    P('      number, which they leave as a free parameter; and "it is not')
    P('      at present possible to prove that the observed fluctuations')
    P('      are associated with the turbulence in clusters as we do not')
    P('      have direct velocity measurements".')

    # (d) solar wind.
    n_sw, T_sw, B_sw = 5.0, 1.2e5, 5.0e-5
    lnL_sw = lnLambda_e(n_sw, T_sw)  # derived, as in m01_numbers.py
    lam_sw = lam_coulomb(n_sw, T_sw, lnL_sw)
    # MU_H, not 1.0: the mean thermal speed of a PROTON.  Module 1's
    # census gas is hydrogen, and m_p/m_u = 1.00728, so mass 1.0 m_u
    # overstated v by sqrt(1.00728) = 1.0036 and nu with it.  This is
    # Module 9's "mu = 1/2 was the m_p convention in m_u clothing" at
    # 0.36 per cent: nu 4.8668e19 -> 4.8492e19, Re 12.30 -> 12.34.
    v_sw_th = v_thermal(T_sw, MU_H)
    nu_sw = nu_kinetic(lam_sw, v_sw_th)
    U_sw, L_sw = 4.0e7, AU
    rg_sw = gyroradius(T_sw, B_sw)
    nu_sw_mag = nu_kinetic(rg_sw, v_sw_th)
    # The same four quantities on Module 9's inputs, printed as a
    # sensitivity below.  Constants copied verbatim from m09_numbers.py
    # lines 174-177, Venzmer & Bothmer (2018) A&A 611 A36 Table 3,
    # MEDIAN-fit column at 1 au, already verified in Module 9's step 2.
    N_SW_VB, T_SW_VB, B_SW_VB, U_SW_VB = 7.57, 9.67e4, 6.05e-5, 4.356e7
    lnL_sw_vb = lnLambda_e(N_SW_VB, T_SW_VB)
    lam_sw_vb = lam_coulomb(N_SW_VB, T_SW_VB, lnL_sw_vb)
    nu_sw_vb = nu_kinetic(lam_sw_vb, v_thermal(T_SW_VB, MU_H))
    rg_sw_vb = gyroradius(T_SW_VB, B_SW_VB)
    P('')
    P('  (d) Solar wind at 1 au, n = 5 cm^-3, T = 1.2e5 K, B = 5 nT')
    P(f'      ln Lambda, derived                 = {lnL_sw:.2f}')
    P(f'      Coulomb mean free path             = {lam_sw/AU:.3f} au')
    P(f'      nu = lam v/3                       = {nu_sw:.4e} cm^2/s')
    P(f'      Re for U = 400 km/s, L = 1 au      = '
      f'{reynolds(U_sw, L_sw, nu_sw):.2f}')
    P(f'      proton gyroradius                  = {rg_sw/1e5:.0f} km')
    P(f'      lam / r_g                          = {lam_sw/rg_sw:.3e}')
    P(f'      Re across the field                >= '
      f'{reynolds(U_sw, L_sw, nu_sw_mag):.3e}')
    P('      (the same Bohm-like upper bound on nu as the ICM row, so the')
    P('      same lower bound on Re)')
    P(f'      Kn = lam/L at 1 au                 = {lam_sw/L_sw:.3f}')
    # STEP 4 ADDITION.  Section 7's Taylor-hypothesis paragraph needs a
    # number rather than the phrase "tens of kilometres per second".  The
    # Alfven speed on the SAME census inputs, v_A = B/sqrt(4 pi rho) with
    # rho = n m_p, is what the frozen-flow assumption must be compared
    # with: Taylor's hypothesis needs the wind to sweep structures past
    # the spacecraft faster than they propagate.
    rho_sw = n_sw*mp
    v_alfven = B_sw/np.sqrt(4.0*np.pi*rho_sw)
    P(f'      Alfven speed B/sqrt(4 pi rho)      = {v_alfven/1e5:.1f} km/s')
    P(f'      U / v_A, the Taylor-hypothesis ratio = {U_sw/v_alfven:.1f}')
    P('      That ratio is what Section 7 needs: the wind sweeps a')
    P('      structure past the spacecraft this many times faster than')
    P('      the structure can propagate, so a frequency spectrum may be')
    P('      read as a wavenumber spectrum.  It is a ratio of order ten,')
    P('      not of order a hundred, and the prose says ten.')
    P('      Same story as the ICM and worse: the mean free path is TWICE')
    P('      the system size, so there is no Navier-Stokes viscosity to')
    P('      put into U L/nu at all.  Module 1 called the way out the')
    P('      magnetic rescue; here is what it buys.')
    P('')
    P('      WHICH SOLAR WIND IS THIS?  The four inputs above are Module')
    P('      1\'s, to one significant figure, and this module reuses them')
    P('      unchanged so that the two modules cannot diverge: Module 1')
    P('      section 8 prints lam = 1.9 au and r_g = 93 km from exactly')
    P('      these.  Module 9 uses a DIFFERENT set - Venzmer & Bothmer')
    P('      (2018) Table 3, median fits, n = 7.57 cm^-3, T = 9.67e4 K,')
    P('      B = 6.05 nT, U = 435.6 km/s - because its job is an')
    P('      acceleration along a fitted radial profile, not a census.')
    P('      Here is what those inputs would give, so that the')
    P('      difference is priced and not hidden:')
    P(f'        lam  = {lam_sw_vb/AU:.4f} au   (against {lam_sw/AU:.4f})')
    P(f'        Kn   = {lam_sw_vb/L_sw:.4f}      (against {lam_sw/L_sw:.4f})')
    P(f'        Re   = {reynolds(U_SW_VB, L_sw, nu_sw_vb):.2f}       '
      f'(against {reynolds(U_sw, L_sw, nu_sw):.2f})')
    P(f'        r_g  = {rg_sw_vb/1e5:.0f} km       (against {rg_sw/1e5:.0f} km)')
    P('      THE CONCLUSION DOES NOT MOVE.  Kn is of order one on both')
    P('      sets, so the collisional viscosity is outside its domain on')
    P('      both, and the magnetic rescue is needed on both.  What DOES')
    P('      move is the phrase "twice the system size", which belongs to')
    P('      Module 1\'s census values alone; on Venzmer & Bothmer\'s the')
    P('      mean free path is 0.85 of the system size.  Their T is the')
    P('      PROTON temperature, and ln Lambda above is evaluated at the')
    P('      same T for both sets, which is a further reason not to mix')
    P('      the two: an electron temperature belongs in ln Lambda.')

    # Module 2's identity, checked line by line.  Re = U L/nu with
    # nu = lam v/3 is 3 (U/v)(L/lam) = 3 Ma_th/Kn identically, so these
    # two columns must agree to rounding.  If they ever stop agreeing,
    # one of the mean free paths above has been changed and not the other.
    P('')
    P('  Module 2\'s identity Re = 3 Ma_th / Kn, checked against U L/nu:')
    P('  The Kn column is also the verdict on each row: only the cloud is')
    P('  a collisional fluid.  The other two have Kn of order 1 and their')
    P('  Re is a formula outside its domain, not a property of the gas.')
    P(f'  {"fluid":<26} {"Kn":>10} {"Ma_th":>9} {"3 Ma/Kn":>11} '
      f'{"U L/nu":>11} {"ratio":>7}')
    D_ROWS = [
        ('molecular cloud, 10 pc', lam_mc, L_mc, U_mc, v_mc, nu_mc),
        ('ICM, 60 kpc', lam_icm, L_icm, U_icm, v_icm, nu_icm_kin),
        ('solar wind, 1 au', lam_sw, L_sw, U_sw, v_sw_th, nu_sw),
    ]
    for name, lam, L, U, vth, nu in D_ROWS:
        Kn, Ma = lam/L, U/vth
        pred, direct = 3.0*Ma/Kn, reynolds(U, L, nu)
        P(f'  {name:<26} {Kn:>10.3e} {Ma:>9.3f} {pred:>11.3e} '
          f'{direct:>11.3e} {pred/direct:>7.4f}')
    P('  The air row is omitted because it uses the MEASURED viscosity,')
    P('  not lam v/3, so the identity does not hold there by construction;')
    P(f'  the discrepancy is exactly the {nu_air_kin/NU_AIR_MEAS:.2f} ratio printed in (a).')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  Kolmogorov scales, and what a simulation would cost')
    P('-'*74)
    # 1 W = 1e7 erg/s and 1 kg = 1e3 g, so 1 W/kg = 1e4 erg/(g s) and
    # 1e-3 W/kg = 1e1 erg/(g s).  A boundary layer runs at 1e-3 to
    # 1e-2 W/kg, and the millimetre eta below is the value that goes
    # with it.  This constant read 1.0e4 until the prep review; that
    # was 1 W/kg wearing a 1e-3 W/kg label, and it made eta 5.6 times
    # too small.
    eps_atm = 1.0e1                  # erg/g/s == 1e-3 W/kg
    P(f'  (a) Atmosphere at eps = 1e-3 W/kg = {eps_atm:.0e} erg/g/s, '
      f'nu = {NU_AIR_MEAS} cm^2/s')
    P(f'      eta   = (nu^3/eps)^(1/4)           = '
      f'{kolmogorov_scale(NU_AIR_MEAS, eps_atm)*10:.3f} mm')
    P(f'      u_eta = (nu eps)^(1/4)             = '
      f'{kolmogorov_velocity(NU_AIR_MEAS, eps_atm):.2f} cm/s')
    P(f'      tau_eta = (nu/eps)^(1/2)           = '
      f'{kolmogorov_time(NU_AIR_MEAS, eps_atm)*1e3:.2f} ms')
    P('      PRECISION, stated once and inherited everywhere below: nu')
    P('      here has TWO significant figures and no primary source, so')
    P('      eta, u_eta and tau_eta have two as well, whatever width they')
    P('      are printed at.  The extra digits are carried only so that')
    P('      the dimensionless check below closes to 1.000000.')
    P(f'      check u_eta eta/nu                 = '
      f'{kolmogorov_velocity(NU_AIR_MEAS, eps_atm)*kolmogorov_scale(NU_AIR_MEAS, eps_atm)/NU_AIR_MEAS:.6f}'
      f'   (must be exactly 1)')
    eps_icm = eps_from_outer(U_icm, L_icm)
    P(f'  (b) ICM, U = 164 km/s over 60 kpc: eps = U^3/L = {eps_icm:.3e} erg/g/s')
    P(f'      eta (unmagnetised nu)              = '
      f'{kolmogorov_scale(nu_icm_kin, eps_icm)/kpc:.2f} kpc')
    P(f'      eta/L                              = '
      f'{kolmogorov_scale(nu_icm_kin, eps_icm)/L_icm:.3f}')
    P('      READ: eta > L.  There is no inertial range, so this is a')
    P('      DEMONSTRATION that the unmagnetised description refutes')
    P('      itself, not a dissipation scale.  Note also that eps = U^3/L')
    P('      is itself a K41 relation, so the line uses the cascade to')
    P('      locate the end of a cascade it has just shown cannot exist.')
    P('      It is the Kn = 0.375 of PART D(c) seen from the other end.')
    P(f'      eta (magnetised nu)                = '
      f'{kolmogorov_scale(nu_icm_mag, eps_icm)/AU:.3e} au')
    P(f'      turnover time at 60 kpc            = '
      f'{L_icm/U_icm/yr/1e6:.0f} Myr')
    eps_mc = eps_from_outer(U_mc, L_mc)
    P(f'  (c) Molecular cloud, sigma = 2.64 km/s over 10 pc: eps = '
      f'{eps_mc:.3e} erg/g/s')
    P(f'      eta                                = '
      f'{kolmogorov_scale(nu_mc, eps_mc)/AU:.1f} au')
    P(f'      L/eta                              = '
      f'{L_mc/kolmogorov_scale(nu_mc, eps_mc):.3e}')
    P('  (d) A direct numerical simulation at Re = 1e6:')
    P(f'      grid side  Re^(3/4)                = '
      f'{grid_side_from_reynolds(1e6):.0f} points')
    P(f'      total      Re^(9/4)                = '
      f'{dof_from_reynolds(1e6):.3e} points')
    P(f'      one snapshot, 3 doubles per point  = '
      f'{24.0*dof_from_reynolds(1e6)/1e12:.0f} TB')
    P(f'      the same for the cloud, Re = {Re_mc:.1e}    = '
      f'{dof_from_reynolds(Re_mc):.2e} points')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  Supersonic turbulence')
    P('-'*74)
    P(f'  A field of shocks gives E(k) ~ k^-{BURGERS_SPEC:.0f} (Burgers), because a step')
    P('  function has a Fourier amplitude falling as 1/k and the power as')
    P(f'  1/k^2.  Its velocity increment exponent is {BURGERS_DELTA_V:.2f}, against')
    P(f'  Kolmogorov\'s {KOLMOGOROV_DELTA_V:.4f}.  CHECK 4 measures that exponent.')
    P('  Log-normal density PDF, sigma_s^2 = ln(1 + b^2 M^2):')
    P(f'  {"M":>6} {"b":>7} {"sigma_s":>9} {"sigma_rho/rho":>14} '
      f'{"peak s":>8} {"rho_peak/<rho>":>15}')
    for M in (1.0, 5.0, 10.0, 20.0):
        for b in (FED_B_SOLENOIDAL, FED_B_COMPRESSIVE):
            ss = lognormal_sigma_s(b, M)
            P(f'  {M:>6.0f} {b:>7.3f} {ss:>9.4f} '
              f'{lognormal_sigma_rho(b, M):>14.2f} '
              f'{lognormal_peak_s(ss):>8.3f} '
              f'{np.exp(lognormal_peak_s(ss)):>15.4f}')
    ss10 = lognormal_sigma_s(FED_B_SOLENOIDAL, 10.0)
    ss10c = lognormal_sigma_s(FED_B_COMPRESSIVE, 10.0)
    P(f'  READ: at M = 10 the width of ln(rho/<rho>) is {ss10:.3f} for purely')
    P(f'  solenoidal forcing and {ss10c:.3f} for purely compressive, a ratio of')
    P(f'  {ss10c/ss10:.2f}.  The consequence is in the TAIL, not the width.  The')
    P('  fraction of the volume denser than a threshold x times the mean is')
    P('    f(>x) = (1/2) erfc[ (ln x - s_0)/(sigma_s sqrt(2)) ],  s_0 = -sigma_s^2/2,')
    P('  which for M = 10 gives')
    P(f'  {"x":>8} {"f(>x) b=1/3":>14} {"f(>x) b=1":>14} {"ratio":>8}')
    for x in (10.0, 100.0, 1000.0):
        f_sol = volume_fraction_above(x, ss10)
        f_com = volume_fraction_above(x, ss10c)
        P(f'  {x:>8.0f} {f_sol:>14.3e} {f_com:>14.3e} {f_com/f_sol:>8.1f}')
    r100 = (volume_fraction_above(100.0, ss10c)
            / volume_fraction_above(100.0, ss10))
    P(f'  At 100 times the mean density, compressive forcing puts {r100:.1f} times')
    P('  as much volume above the threshold as solenoidal forcing does, from')
    P(f'  a width that is only {ss10c/ss10:.2f} times larger.  Star formation happens')
    P('  in that tail, which is why the forcing matters.')

    # ---------------------------------------------------------------- G
    P('')
    P('PART G.  THE CHECKS')
    P('-'*74)

    # --- CHECK 1: the anchor.
    P('  CHECK 1 (ANCHOR).  Solar-wind spectral indices at 1 au.')
    P('  Podesta, Roberts & Goldstein (2007), ApJ 664, 543, Table 2.')
    P(f'  Fit window {PODESTA_FIT_LO_HZ:.0e} to {PODESTA_FIT_HI_HZ:.0e} Hz.  '
      f'Errors are {PODESTA_CI_LEVEL:.0%} confidence')
    P(f'  limits, not standard deviations: divide by {PODESTA_CI_TO_SIGMA:.3f} for sigma.')
    P(f'  Their Section 3 bounds the window itself: moving the endpoints')
    P(f'  over 7e-4 to 1.5e-3 Hz and 7e-3 to 1.5e-2 Hz changes an exponent')
    P(f'  "typically by {PODESTA_WINDOW_SENSITIVITY:.0%}", always less than the tabulated error.')
    P('')
    P(f'  {"int":>4} {"magnetic":>12} {"d(5/3)/CI":>11} {"d(5/3)/sig":>11} '
      f'{"velocity":>12} {"d(5/3)/CI":>11} {"d(5/3)/sig":>11}')
    mags, vels = [], []
    for iv, _, _, B, dB, V, dV, K, dK, E, dE, ar in PODESTA:
        mags.append(B)
        vels.append(V)
        sB = dB/PODESTA_CI_TO_SIGMA
        sV = dV/PODESTA_CI_TO_SIGMA
        P(f'  {iv:>4} {B:>7.2f}+/-{dB:.2f} '
          f'{sigma_departure(B, dB, KOLMOGOROV_SPEC):>11.2f} '
          f'{sigma_departure(B, sB, KOLMOGOROV_SPEC):>11.1f} '
          f'{V:>7.2f}+/-{dV:.2f} '
          f'{sigma_departure(V, dV, KOLMOGOROV_SPEC):>11.2f} '
          f'{sigma_departure(V, sV, KOLMOGOROV_SPEC):>11.1f}')
    mags, vels = np.array(mags), np.array(vels)
    P('')
    P(f'    magnetic indices     {mags} ')
    P(f'      spread {mags.min():.2f} to {mags.max():.2f}, mean {mags.mean():.4f}, '
      f'prediction 5/3 = {KOLMOGOROV_SPEC:.4f}')
    P(f'      ratio mean/(5/3)                 = {mags.mean()/KOLMOGOROV_SPEC:.4f}')
    dep_m = [sigma_departure(B, dB, KOLMOGOROV_SPEC)
             for _, _, _, B, dB, _, _, _, _, _, _, _ in PODESTA]
    n_above = sum(1 for d in dep_m if d > 0)
    P('      CONFIRMED OF THE MEAN, and here is the exact sense of it.')
    P('      The four departures from 5/3, in units of each interval\'s')
    P('      own 99% half-width, are '
      + ', '.join(f'{d:+.1f}' for d in dep_m) + ',')
    P(f'      so {n_above} of the four sits above the prediction and '
      f'{len(dep_m)-n_above} below, and the')
    P(f'      largest single departure is {max(abs(np.array(dep_m))):.1f} half-widths, or '
      f'{max(abs(np.array(dep_m)))*PODESTA_CI_TO_SIGMA:.1f} sigma.')
    P('      Only two of the four agree with 5/3 within their own fit')
    P('      errors, so the interval-to-interval variation is real and')
    P('      larger than the fit errors.  NOTHING HERE CONFIRMS 5/3')
    P('      INTERVAL BY INTERVAL, and the prose must not say it does;')
    P('      what is consistent with 5/3 is the MEAN of the four, tested')
    P('      below against the scatter of the four.')
    P('')
    # Interval-to-interval scatter as the error: the four intervals are
    # different epochs, so their sample standard deviation measures the
    # real variation, and the standard error of the mean is sd/sqrt(4).
    # With n = 4 this is crude, and it is larger than every fit error,
    # which makes it the cautious choice.
    sem_B = mags.std(ddof=1)/np.sqrt(len(mags))
    sem_V = vels.std(ddof=1)/np.sqrt(len(vels))
    P('    Using the scatter of the four intervals as the error:')
    P(f'      magnetic  mean {mags.mean():.4f}  sd {mags.std(ddof=1):.4f}  '
      f'sem {sem_B:.4f}')
    P(f'      velocity  mean {vels.mean():.4f}  sd {vels.std(ddof=1):.4f}  '
      f'sem {sem_V:.4f}')
    zB53 = sigma_departure(mags.mean(), sem_B, KOLMOGOROV_SPEC)
    zV53 = sigma_departure(vels.mean(), sem_V, KOLMOGOROV_SPEC)
    zB32 = sigma_departure(mags.mean(), sem_B, IK_SPEC)
    zV32 = sigma_departure(vels.mean(), sem_V, IK_SPEC)
    P(f'      {"":<10} {"vs 5/3":>9} {"vs 3/2":>9}   (standard errors)')
    P(f'      {"magnetic":<10} {zB53:>9.2f} {zB32:>9.2f}')
    P(f'      {"velocity":<10} {zV53:>9.2f} {zV32:>9.2f}')
    P('')
    P('    THOSE ARE NOT SIGMAS.  With n = 4 the statistic is Student\'s t')
    P('    with 3 degrees of freedom, and the p-value it earns is far')
    P('    weaker than the bare number reads:')
    P(f'      {"":<22} {"t (3 dof)":>10} {"p":>9} {"= Gaussian sigma":>18}')
    for nm, arr, tgt, tname in (('magnetic vs 5/3', mags, KOLMOGOROV_SPEC, ''),
                                ('velocity vs 5/3', vels, KOLMOGOROV_SPEC, ''),
                                ('magnetic vs 3/2', mags, IK_SPEC, ''),
                                ('velocity vs 3/2', vels, IK_SPEC, '')):
        t_stat, p_two = stats.ttest_1samp(arr, tgt)
        P(f'      {nm:<22} {t_stat:>+10.2f} {p_two:>9.4f} '
          f'{stats.norm.isf(p_two/2.0):>18.2f}')
    tV53 = stats.ttest_1samp(vels, KOLMOGOROV_SPEC)
    tB32 = stats.ttest_1samp(mags, IK_SPEC)
    P(f'    PUNCHLINE CHECK 1.  The magnetic mean is consistent with 5/3')
    P(f'      (t = {stats.ttest_1samp(mags, KOLMOGOROV_SPEC).statistic:+.2f}, p = '
      f'{stats.ttest_1samp(mags, KOLMOGOROV_SPEC).pvalue:.2f}): CONFIRMED.  The velocity mean is')
    P(f'      below it at p = {tV53.pvalue:.4f}, equivalent to '
      f'{stats.norm.isf(tV53.pvalue/2.0):.1f} sigma: REFUTED.')
    P(f'      Against 3/2 the roles swap, and weakly: the magnetic mean')
    P(f'      departs at p = {tB32.pvalue:.4f} ('
      f'{stats.norm.isf(tB32.pvalue/2.0):.1f} sigma) and the velocity mean not at all.')
    P('      THE STRONGER FORM OF THE VELOCITY RESULT NEEDS NO n = 4')
    P('      STATISTICS AT ALL, and it is printed below: every one of the')
    P('      four intervals excludes 5/3 by its own fit error, on the')
    P('      same side.')
    P('')
    P(f'    velocity indices     {vels}')
    P(f'      spread {vels.min():.2f} to {vels.max():.2f}, mean {vels.mean():.4f}')
    dep = [sigma_departure(V, dV, KOLMOGOROV_SPEC)
           for _, _, _, _, _, V, dV, _, _, _, _, _ in PODESTA]
    P(f'      departures from 5/3, in 99% half-widths: '
      + ', '.join(f'{d:.1f}' for d in dep))
    P(f'      every velocity index is below 5/3, by {min(abs(np.array(dep))):.1f} to '
      f'{max(abs(np.array(dep))):.1f}')
    P('      of its own 99% half-width.  REFUTED: one Kolmogorov exponent')
    P('      does not describe both fields.')
    dep32 = [sigma_departure(V, dV, IK_SPEC)
             for _, _, _, _, _, V, dV, _, _, _, _, _ in PODESTA]
    P(f'      Against 3/2 instead: departures '
      + ', '.join(f'{d:.1f}' for d in dep32) + ' half-widths.')
    P('      Three of four are consistent with 3/2; interval 2 is not.')
    P('      So: 5/3 is excluded for the velocity in all four intervals,')
    P('      and 3/2 fits three of them.  That is weaker than "the')
    P('      velocity spectrum is 3/2" and it is what the table supports.')
    tot = np.array([E for _, _, _, _, _, _, _, _, _, E, _, _ in PODESTA])
    ars = [ar for _, _, _, _, _, _, _, _, _, _, _, ar in PODESTA]
    P(f'      Total-energy indices {tot}, mean {tot.mean():.4f}: the total')
    P('      sits between the two, nearer the magnetic one because the')
    P('      magnetic energy is the larger of the pair in most of these')
    P('      intervals.  The paper\'s Alfven ratio E_kin/E_mag over the')
    P('      fit band is')
    P('        ' + ',  '.join(f'{lo:.2f}-{hi:.2f}' for lo, hi in ars) + ',')
    P(f'      so it reaches {max(hi for _, hi in ars):.2f} in interval 1: the magnetic energy')
    P('      is comparable to or larger than the kinetic, and the prose')
    P('      must not write "dominates".')

    # --- CHECK 2: terrestrial.
    P('')
    P('  CHECK 2.  The Kolmogorov constant, terrestrial.')
    P('  Sreenivasan (1995), Phys. Fluids 7, 2778, Fig. 3 and Section V.')
    C3 = SREENI_3D_FACTOR*SREENI_CK
    C3sd = SREENI_3D_FACTOR*SREENI_CK_SD
    P(f'    compiled C_K (1D longitudinal)     = {SREENI_CK:.3f} '
      f'+/- {SREENI_CK_SD:.3f}')
    P(f'    that error is the SCATTER of >{SREENI_N_SPECTRA} experiments, not the')
    P(f'    error on the mean; the flows run from grids to a tidal channel')
    P(f'    and R_lambda from {SREENI_RLAMBDA_MIN:.0f} to about 1e4.')
    P(f'    PUNCHLINE fractional scatter       = '
      f'{SREENI_CK_SD/SREENI_CK*100:.1f}%')
    P(f'    CONFIRMED - and note what is confirmed.  K41 does not predict')
    P(f'    the VALUE of C_K.  It predicts that there is one value.  A')
    P(f'    {SREENI_CK_SD/SREENI_CK*100:.0f}% scatter across a hundred flows is that prediction, met.')
    P(f'    THE SPAN, stated in the right variable.  R_lambda from '
      f'{SREENI_RLAMBDA_MIN:.0f} to 1e4 is')
    P(f'    {np.log10(1e4/SREENI_RLAMBDA_MIN):.2f} decades in R_lambda and, since Re ~ R_lambda^2,')
    P(f'    {2*np.log10(1e4/SREENI_RLAMBDA_MIN):.2f} decades in Re.  Neither is "three decades"; the prose')
    P('    must name which variable it means.  Step 2 must confirm what')
    P('    range the paper itself claims.')
    P(f'    three-dimensional constant (55/18) C_K = {C3:.3f} +/- {C3sd:.3f}')
    P(f'    second-order structure constant 4.02 C_K = '
      f'{SREENI_S2_FACTOR*SREENI_CK:.3f} +/- {SREENI_S2_FACTOR*SREENI_CK_SD:.3f}')
    P(f'    Sreenivasan\'s own revised value     = {SREENI_CK_REVISED:.2f}, after allowing')
    P('      that the local-isotropy estimate of eps undercounts by ~10%.')
    P(f'      That moves the 3D constant to {SREENI_3D_FACTOR*SREENI_CK_REVISED:.2f}.  Quote the range,')
    P('      not a single digit.')
    P(f'    Grant, Stewart & Moilliet (1962), tidal channel, as tabulated')
    P(f'      in that compilation: C_K = {GRANT62_CK:.2f} +/- {GRANT62_CK_ERR:.2f} at R_lambda '
      f'{GRANT62_RLAMBDA[0]:.0f}-{GRANT62_RLAMBDA[1]:.0f}')
    P(f'      3D form: C = {SREENI_3D_FACTOR*GRANT62_CK:.3f} +/- {SREENI_3D_FACTOR*GRANT62_CK_ERR:.3f}')
    P(f'      departure from the compiled mean  = '
      f'{sigma_departure(GRANT62_CK, SREENI_CK_SD, SREENI_CK):.2f} population sigma')
    P('      CAVEAT: the 1962 paper is paywalled and was NOT read.  This')
    P('      value comes from Sreenivasan\'s Table IV, whose footnote says')
    P('      it is an average over 17 data sets read off log-log plots by')
    P('      straight-edge, and that Kraichnan judged a different reading')
    P('      would raise it by more than 10%.  The R_lambda range is')
    P('      Sreenivasan\'s estimate, not Grant et al.\'s measurement.')
    P('    GAP, stated plainly: this module has NO terrestrial fitted')
    P('    SLOPE with a published error bar.  The measured slopes it')
    P('    quotes are the solar-wind ones of CHECK 1.  What the')
    P('    terrestrial data contribute is the constant and its')
    P('    universality, which is a different and weaker claim.')

    # --- CHECK 3: the repayment to Module 3.
    P('')
    P('  CHECK 3.  Is the intracluster medium hydrostatic?  The price of')
    P('  one of Module 3\'s idealisations.')
    P('  Hitomi Collaboration (2016), Nature 535, 117.')
    alpha = turbulent_pressure_fraction(HITOMI_SIGMA_V, HITOMI_KT_OUT)
    cs_icm = sound_speed(HITOMI_KT_OUT/kB, MU_ICM)
    M1d = HITOMI_SIGMA_V/cs_icm
    M3d = np.sqrt(3.0)*M1d
    P(f'    measured l.o.s. dispersion         = '
      f'{HITOMI_SIGMA_V/1e5:.0f} +/- {HITOMI_SIGMA_V_ERR/1e5:.0f} km/s (90% conf.)')
    P(f'      as a 1-sigma error                = '
      f'+/- {HITOMI_SIGMA_V_ERR/HITOMI_CI_TO_SIGMA/1e5:.1f} km/s')
    P(f'      region                            = '
      f'{HITOMI_R_IN/kpc:.0f}-{HITOMI_R_OUT/kpc:.0f} kpc from the nucleus')
    P(f'      independent Ly-alpha value        = '
      f'{HITOMI_LYA_SIGMA/1e5:.0f} +/- {HITOMI_LYA_ERR/1e5:.0f} km/s, consistent')
    P(f'    measured temperature of that region = '
      f'{HITOMI_KT_OUT/keV:.1f} +/- {HITOMI_KT_OUT_ERR/keV:.1f} keV')
    P(f'    sound speed of that gas             = {cs_icm/1e5:.0f} km/s')
    P(f'    1D Mach number sigma/c_s            = {M1d:.3f}')
    P(f'    3D Mach number sqrt(3) sigma/c_s    = {M3d:.3f}  (subsonic)')
    P(f'    P_turb/P_th = mu m_u sigma^2/(kT)   = {alpha*100:.2f}%')
    P(f'      the paper\'s own headline value     = '
      f'{HITOMI_PTURB_FRAC_PAPER*100:.0f}% OR LESS')
    P('      Their abstract, in full: "Turbulent pressure support in the')
    P('      gas is 4% or less of the thermodynamic pressure, with large')
    P('      scale shear at most doubling that estimate."  Step 2 checked')
    P('      the Methods and the Extended Data: nothing tighter exists.')
    P(f'      PUNCHLINE: the recomputed {alpha*100:.2f}% AGREES with the paper\'s')
    P('      stated 4%, and no ratio tighter than that may be quoted.  "4%"')
    P('      carries ONE significant figure; it spans 3.5% to 4.5%, against')
    P(f'      which {alpha*100:.2f}% gives a ratio anywhere from '
      f'{alpha/0.045:.2f} to {alpha/0.035:.2f}.')
    P('      A ratio printed to three decimals would claim a discrepancy')
    P('      had been measured when none has been.')
    P('      The density cancels, which is why a line width and a')
    P(f'      temperature suffice.  What does NOT cancel is mu = {MU_ICM},')
    P('      the mean mass per particle of a fully ionised plasma: the')
    P('      ratio is linear in it, and the prose and every problem')
    P('      statement must name it.')
    b = mass_bias(alpha)
    b2 = mass_bias(2.0*alpha)
    P(f'    hydrostatic mass bias alpha/(1+alpha) = {b*100:.2f}%')
    P(f'      with the large-scale shear the paper says could at most')
    P(f'      double the estimate                 = {b2*100:.2f}%')
    P('      ASSUMPTION, stated: P_turb/P_th constant with radius.  Drop')
    P('      it and the bias depends on the two pressure scale lengths.')
    P('    CONFIRMED.  Module 3 applied hydrostatic balance to an ICM at')
    P('    1 Mpc and listed "Static: u = 0" among its idealisations.  It')
    P('    did NOT name turbulence; that word does not occur in Module 3,')
    P('    and this module must not say it does.  What CHECK 3 supplies is')
    P('    the price of that idealisation, measured, in one cluster core:')
    P(f'    {b*100:.1f}% of the mass, or {b2*100:.1f}% if the shear doubles it.')
    P('    SCOPE, stated: Hitomi saw ONE pointing, 30-60 kpc, in ONE')
    P('    cluster core.  The paper itself says "in the central regions".')
    P('    Cluster masses for cosmology are measured near r_500, far')
    P('    outside this, where no comparable measurement exists.')
    P(f'    Central region, for contrast: {HITOMI_SIGMA_V_IN/1e5:.0f} +/- '
      f'{HITOMI_SIGMA_V_IN_ERR/1e5:.0f} km/s at '
      f'{HITOMI_KT_IN/keV:.1f} keV,')
    P(f'      P_turb/P_th = '
      f'{turbulent_pressure_fraction(HITOMI_SIGMA_V_IN, HITOMI_KT_IN)*100:.2f}% - higher, and it contains the AGN.')
    P(f'    Velocity gradient across the core   = '
      f'{HITOMI_VGRAD/1e5:.0f} +/- {HITOMI_VGRAD_ERR/1e5:.0f} km/s over '
      f'{HITOMI_VGRAD_SCALE/kpc:.0f} kpc')
    P(f'    Systematics on the 164: energy resolution +/-'
      f'{HITOMI_SYS[0]/1e5:.0f}, temperature')
    P(f'      +/-{HITOMI_SYS[1]/1e5:.0f}, calibration scatter -{HITOMI_SYS[2]/1e5:.0f} km/s (all km/s).')

    # --- CHECK 4: the interstellar medium.
    P('')
    P('  CHECK 4.  The exponent of the size-linewidth relation.')
    P('  Larson (1981), MNRAS 194, 809, eq. (1); Solomon et al. (1987),')
    P('  ApJ 319, 730, eq. (1).')
    P(f'    predicted by Kolmogorov, delta v ~ l^(1/3)  = '
      f'{KOLMOGOROV_DELTA_V:.4f}')
    P(f'    predicted by Burgers,     delta v ~ l^(1/2) = '
      f'{BURGERS_DELTA_V:.4f}')
    P(f'    Larson (1981)   sigma = {LARSON_A} L^{LARSON_EXP}, 3D, '
      f'{LARSON_L_RANGE[0]}-{LARSON_L_RANGE[1]:.0f} pc')
    P(f'      NO error bar exists: the paper calls it an eye-fitted line.')
    P(f'      Its stated scatter is rms(log sigma) = {LARSON_RMS_LOG}, a factor '
      f'{10**LARSON_RMS_LOG:.2f} in sigma.')
    P(f'      distance from 1/3 = {LARSON_EXP - KOLMOGOROV_DELTA_V:+.4f}; from 1/2 = '
      f'{LARSON_EXP - BURGERS_DELTA_V:+.4f}.  No sigma may be quoted.')
    P('      Larson himself (p. 816): "it is perhaps remarkable that the')
    P('      observed relation sigma ~ L^0.38 is so close to the')
    P('      Kolmogoroff law sigma ~ L^0.33".')
    P(f'    Solomon et al. (1987)  sigma_v = ({SOLOMON_A} +/- {SOLOMON_A_ERR}) '
      f'S^({SOLOMON_EXP} +/- {SOLOMON_EXP_ERR}), 1D,')
    P(f'      least squares on {SOLOMON_N_CLOUDS} clouds, calibrators only, '
      f'scatter {SOLOMON_SCATTER_LOG} dex')
    # NOT sigmas.  The +/-0.05 is the authors' own systematic envelope, and
    # p. 737 says it is LARGER than the formal fit error, so a Gaussian
    # sigma count would be both the wrong kind of number and too small.
    # What may be printed is the gap measured in envelopes.
    gap_kol = SOLOMON_EXP - KOLMOGOROV_DELTA_V
    gap_bur = SOLOMON_EXP - BURGERS_DELTA_V
    P('      WHAT THE +/-0.05 IS, before any comparison: p. 737, "The')
    P('      quoted error in the exponent is larger than the formal fit')
    P('      error and represents an estimate of the systematic error')
    P('      based on several fits to the data with varying definitions')
    P('      of cloud boundaries."  It is a spread over where a cloud')
    P('      ends.  NO SIGMA MAY BE QUOTED FROM IT, and none is below.')
    P(f'      gap to Kolmogorov 1/3              = {gap_kol:+.4f} '
      f'= {gap_kol/SOLOMON_EXP_ERR:.2f} envelopes')
    P(f'      gap to Burgers    1/2              = {gap_bur:+.4f} '
      f'= {gap_bur/SOLOMON_EXP_ERR:.2f} envelopes')
    P(f'      PUNCHLINE: 1/3 sits {gap_kol/SOLOMON_EXP_ERR:.1f} times the whole systematic')
    P('      envelope below the measured exponent, and 1/2 sits on it.')
    P('      The formal statistical error is SMALLER than that envelope,')
    P('      so the statistical case against 1/3 is stronger than this,')
    P('      not weaker.  The envelope is the honest number to print')
    P('      because it is the one the authors stand behind.')
    P('      ASSUMPTION FIRST, because the refutation depends on it.')
    P('      delta v(l) ~ l^(1/3) is a TWO-POINT statistic INSIDE one')
    P('      flow: the typical velocity difference between two points a')
    P('      distance l apart.  Solomon\'s exponent comes from a')
    P(f'      regression ACROSS {SOLOMON_N_CLOUDS} DIFFERENT CLOUDS, each contributing')
    P('      one linewidth and one size.  Reading the second as the first')
    P('      assumes a cloud\'s internal dispersion samples the same')
    P('      cascade a structure function would, and that the')
    P('      cloud-to-cloud ensemble is statistically one object.  Larson')
    P('      (1981) made that identification explicitly and it is')
    P('      standard.  It is still an assumption, and it is named here')
    P('      BEFORE the word REFUTED, not after.')
    P('      REFUTED: incompressible Kolmogorov scaling does not hold in')
    P('      a molecular cloud.  A gap of three systematic envelopes is a')
    P('      refutation, not a demolition, and the module must print the')
    P('      gap rather than a confidence level it cannot compute.')
    P('      AND THE AUTHORS SAY IT THEMSELVES, p. 737: "Larson (1981),')
    P('      from a literature search, suggested that the observed')
    P('      exponent was close to 1/3 and reflected a Kolmogorov')
    P('      turbulent spectrum.  This hypothesis is ruled out by the')
    P('      data presented here."')
    P(f'      ONE SENSITIVITY, also p. 737: without their 2 km/s velocity')
    P(f'      extrapolation the constant of eq. (1) is {SOLOMON_A_NO_EXTRAP}, not '
      f'{SOLOMON_A}')
    P(f'      - a reduction of {100*(1 - SOLOMON_A_NO_EXTRAP/SOLOMON_A):.0f} per cent, which moves every Mach')
    P('      number below but not the exponent.')
    P('      DEGENERACY, stated: sigma ~ S^(1/2) is ALSO exactly what')
    P('      virial equilibrium at constant surface density gives, since')
    P('      sigma^2 ~ GM/S and M ~ Sigma S^2 give sigma ~ (G Sigma)^(1/2)')
    P(f'      S^(1/2).  Solomon et al. read it that way: their constant')
    P(f'      surface density is {SOLOMON_SURFACE_DENSITY:.0f} Msun/pc^2.  The exponent')
    P('      refutes Kolmogorov.  It does not distinguish Burgers from')
    P('      virial equilibrium, and this module does not claim it does.')
    # The surface density implied by Solomon's own normalisation, as a
    # consistency check on the virial reading.
    sig_cgs = SOLOMON_A*1e5                     # sigma_v at S = 1 pc, cm/s
    Sigma_vir = 3.0*sig_cgs**2/(np.pi*G*pc)     # g/cm^2, sigma^2 = pi G Sigma S/3
    P(f'      Order-of-magnitude cross-check: their normalisation sigma_v(1 pc)')
    P(f'      = {SOLOMON_A} km/s, put into sigma_1d^2 = pi G Sigma S/3, gives Sigma = '
      f'{Sigma_vir*pc*pc/Msun:.0f} Msun/pc^2,')
    P(f'      against the {SOLOMON_SURFACE_DENSITY:.0f} they quote: ratio '
      f'{Sigma_vir*pc*pc/Msun/SOLOMON_SURFACE_DENSITY:.2f}.  The factor pi/3 is')
    P('      THIS script\'s choice of a uniform sphere, not Solomon et al.\'s')
    P('      virial coefficient, so a ratio of order one is all it shows.')
    P(f'    ONE MORE THING THE PROSE MUST CARRY: Larson\'s sigma is')
    P(f'    THREE-dimensional and Solomon\'s is ONE-dimensional '
      f'(1D: {SOLOMON_SIGMA_IS_1D}).')
    P(f'    The exponents are unaffected, but every Mach number is, and so')
    P(f'    is the cloud outer-scale U of PART D(b), which uses Larson\'s')
    P(f'    3D sigma.  Larson\'s own thermal term is {LARSON_SIGMA_THERMAL} km/s and is')
    P(f'    THREE-dimensional too, since he adds it into a 3D sigma^2; the')
    P(f'    matching 1D speed is {LARSON_SIGMA_THERMAL/np.sqrt(3.0):.3f} km/s, and THAT is the one a 1D')
    P(f'    linewidth must be compared with.  Every entry below is')
    P(f'    supersonic against either.')
    P(f'    Mach numbers along Solomon\'s relation, c_s = {cs_mc/1e5:.3f} km/s at 10 K:')
    for S in (1.0, 10.0, 100.0):
        P(f'      S = {S:>5.0f} pc  sigma_v = {solomon_sigma(S):>6.2f} km/s  '
          f'M_1d = {solomon_sigma(S)*1e5/cs_mc:>6.2f}')
    P('      Every one is supersonic, which is the physical reason the')
    P('      incompressible theory should not have been expected to hold.')

    # ---------------------------------------------------------------- H
    P('')
    P('PART H.  Numbers for the problem set')
    P('-'*74)
    P(f'  P1  eta in the atmosphere at eps = 1e-3 W/kg        = '
      f'{kolmogorov_scale(NU_AIR_MEAS, eps_atm)*10:.3f} mm')
    P(f'      u_eta {kolmogorov_velocity(NU_AIR_MEAS, eps_atm):.2f} cm/s, '
      f'tau_eta {kolmogorov_time(NU_AIR_MEAS, eps_atm)*1e3:.2f} ms')
    P(f'  P2  eta in the ICM, unmagnetised nu                 = '
      f'{kolmogorov_scale(nu_icm_kin, eps_icm)/kpc:.2f} kpc')
    P(f'      eta/L = {kolmogorov_scale(nu_icm_kin, eps_icm)/L_icm:.3f}: the point of the problem is that the')
    P('      student should notice eta > L and reject the premise')
    P(f'      eta in the ICM, magnetised nu                   = '
      f'{kolmogorov_scale(nu_icm_mag, eps_icm)/AU:.3e} au')
    P(f'  P3  DNS grid for Re = 1e6: side {grid_side_from_reynolds(1e6):.0f}, '
      f'total {dof_from_reynolds(1e6):.3e}')
    P(f'      one snapshot at 3 doubles/point                 = '
      f'{24.0*dof_from_reynolds(1e6)/1e12:.0f} TB')
    P(f'  P4  eddy turnover time, 10 pc cloud at 2.64 km/s    = '
      f'{L_mc/U_mc/yr/1e6:.2f} Myr')
    P(f'      crossing time in sound speeds                   = '
      f'{L_mc/cs_mc/yr/1e6:.1f} Myr')
    P(f'  P5  sigma_s at M = 10, b = 1/3                      = {ss10:.4f}')
    P(f'      sigma_s at M = 10, b = 1                        = {ss10c:.4f}')
    P(f'      volume fraction above 100 <rho>, b = 1/3 / b = 1  = '
      f'{volume_fraction_above(100.0, ss10):.3e} / '
      f'{volume_fraction_above(100.0, ss10c):.3e}')
    a20 = alpha_for_bias(0.20)
    s20 = sigma_for_alpha(a20, HITOMI_KT_OUT)
    P(f'  P6  P_turb/P_th for a 20% mass bias                 = {a20:.4f}')
    P(f'      the dispersion that needs, at 4.1 keV           = '
      f'{s20/1e5:.0f} km/s')
    P(f'      times the Hitomi value                          = '
      f'{s20/HITOMI_SIGMA_V:.2f}')
    P(f'  P7  Re of the ICM, unmagnetised / magnetised        = '
      f'{Re_icm:.2f} / at least {reynolds(U_icm, L_icm, nu_icm_mag):.2e}')
    P(f'      the unmagnetised figure is evaluated at Kn = '
      f'{lam_icm/L_icm:.3f}, outside')
    P('      the Chapman-Enskog domain; that is the point of the problem')
    P(f'  P8  Re of a 10 pc molecular cloud                   = {Re_mc:.3e}')
    P(f'      its L/eta                                       = '
      f'{L_mc/kolmogorov_scale(nu_mc, eps_mc):.2e}')
    P(f'  P9  S_3(l) = -(4/5) eps l in the cloud at l = 1 pc  = '
      f'{S3_exact(eps_mc, pc):.3e} cm^3/s^3')
    P(f'      the implied delta v = |S_3|^(1/3)               = '
      f'{abs(S3_exact(eps_mc, pc))**(1/3)/1e5:.3f} km/s')
    P(f'      against (eps l)^(1/3)                           = '
      f'{delta_v(eps_mc, pc)/1e5:.3f} km/s, ratio '
      f'{abs(S3_exact(eps_mc, pc))**(1/3)/delta_v(eps_mc, pc):.4f}')
    P(f'  P10 E(k) at k = 1/(1 pc) in the cloud, C = {C3:.2f}       = '
      f'{E_of_k(C3, eps_mc, 1.0/pc):.3e} cm^3/s^2')
    P(f'      Reynolds number at which N = 1e9 grid points    = '
      f'{1e9**(1/2.25):.3e}')

    P('')
    P('=' * 74)
    P('SOURCES')
    P('=' * 74)
    P('  EIGHT PAPERS WERE LISTED FOR STEP 2 AND ALL EIGHT WERE FETCHED')
    P('  as PDFs and read locally with PyMuPDF, 2026-09-19; where the OCR')
    P('  layer was unreliable the page was rendered and read as an image.')
    P('  No web summariser was used.  Volume, page and year for every DOI')
    P('  below were confirmed at Crossref, not recalled.  TWO ENTRIES')
    P('  BELOW WERE NOT READ and say so in place: Grant et al. (1962),')
    P('  quoted only through Sreenivasan\'s Table IV, and Kadoya et al.')
    P('  (1985), which no server would serve.  The record of the pass is')
    P('  .ignore/m10-source-verification.md.')
    P('  Podesta, J. J., Roberts, D. A. & Goldstein, M. L. (2007),')
    P('    "Spectral exponents of kinetic and magnetic energy spectra in')
    P('    solar wind turbulence", ApJ 664, 543-548.  DOI 10.1086/519211.')
    P('    Table 2 gives the four intervals\' magnetic, velocity, kinetic')
    P('    and total-energy exponents with 99% confidence limits; Table 1')
    P('    gives the intervals.  Wind spacecraft, ecliptic plane, 1 au.')
    P('    THE ANCHOR OF THIS MODULE.')
    P('  Sreenivasan, K. R. (1995), "On the universality of the Kolmogorov')
    P('    constant", Phys. Fluids 7(11), 2778-2784.  DOI 10.1063/1.868656.')
    P('    Eq. (2) defines C_K through the 1D longitudinal spectrum;')
    P('    Section I gives the isotropy factors 55/18 and 4.02; Fig. 3 and')
    P('    Section V give 0.53 +/- 0.055 and the revision to about 0.5;')
    P('    Table IV, row "Tidal channel / Grant et al.", gives 0.47 +/-')
    P('    0.02 at R_lambda 3000-18000.  Author\'s copy at')
    P('    http://users.ictp.it/~krs/pdf/1995_003.pdf')
    P('  Grant, H. L., Stewart, R. W. & Moilliet, A. (1962), "Turbulence')
    P('    spectra from a tidal channel", J. Fluid Mech. 12, 241.  The')
    P('    first clean -5/3 measurement.  NOT READ: the publisher\'s copy')
    P('    is paywalled.  Its C_K is quoted here only as reference 67 of')
    P('    Sreenivasan (1995) Table IV, and the module says so.')
    P('  Hitomi Collaboration (2016), "The quiescent intracluster medium')
    P('    in the core of the Perseus cluster", Nature 535, 117-121.')
    P('    arXiv:1607.04487.  Abstract and p. 3: l.o.s. velocity dispersion')
    P('    164 +/- 10 km/s at 30-60 kpc, all errors at 90% confidence;')
    P('    p. 4: kT = 4.1 +/- 0.1 keV in that region and 3.8 +/- 0.1 keV')
    P('    in the centre; p. 5: turbulent pressure "low at 4%".')
    P('  Larson, R. B. (1981), "Turbulence and star formation in molecular')
    P('    clouds", MNRAS 194, 809-826.  Eq. (1), p. 814: sigma = 1.10')
    P('    L^0.38 km/s, an EYE-FITTED line, rms(log sigma) = 0.14, valid')
    P('    for 0.1 <~ L <~ 100 pc.  ADS scan.  His sigma and his thermal')
    P('    term 0.32 km/s are both THREE-dimensional (p. 814).  In the')
    P('    p. 816 quotation he writes "sigma PROPORTIONAL TO L^0.38", with')
    P('    the proportionality sign; this ASCII file cannot carry it and')
    P('    module10.html must.')
    P('  Solomon, P. M., Rivolo, A. R., Barrett, J. & Yahil, A. (1987),')
    P('    "Mass, luminosity, and line width relations of Galactic')
    P('    molecular clouds", ApJ 319, 730-741.  Eq. (1), p. 731:')
    P('    sigma_v = (1.0 +/- 0.1) S^(0.5 +/- 0.05) km/s, 273 clouds,')
    P('    dispersion in log sigma_v +/- 0.11; abstract: constant mean')
    P('    surface density 170 Msun/pc^2.  ADS scan; eq. (1) was verified')
    P('    against a rendered image of the page, not the OCR layer.')
    P('    p. 737 settles what the +/-0.05 is: "larger than the formal fit')
    P('    error ... an estimate of the systematic error based on several')
    P('    fits to the data with varying definitions of cloud boundaries",')
    P('    so it is NOT a sigma.  The same page rules on Larson: "This')
    P('    hypothesis is ruled out by the data presented here."  And it')
    P('    gives the sensitivity: without the 2 km/s extrapolation the')
    P('    constant of eq. (1) is 0.83, a reduction of 17%.')
    P('  Federrath, C., Roman-Duval, J., Klessen, R. S., Schmidt, W. &')
    P('    Mac Low, M.-M. (2010), "Comparing the statistics of interstellar')
    P('    turbulence in simulations and observations", A&A 512, A81.')
    P('    arXiv:0905.1060.  Eq. (19) sigma_s^2 = ln(1 + b^2 M^2), citing')
    P('    Padoan et al. (1997) and Federrath et al. (2008b); Fig. 8 and')
    P('    eq. (20): b falls from about 1 for purely compressive forcing')
    P('    to about 1/3 in 3D for purely solenoidal forcing.')
    P('  Sarazin, C. L. (1988), section 5.4 - the Coulomb mean free path')
    P('    and ln Lambda = 37.8 reused from Module 1.')
    P('  Braginskii, S. I. (1965), "Transport processes in a plasma", in')
    P('    Reviews of Plasma Physics, Vol. 1, ed. M. A. Leontovich,')
    P('    Consultants Bureau, New York, pp. 205-311, translated by')
    P('    Herbert Lashinsky.  THE ORIGINAL TRANSLATION WAS READ, not a')
    P('    review restating it; the scan has no text layer, so every')
    P('    equation below was read from a rendered page.  p. 215')
    P('    eq. (2.5i) defines tau_i; p. 217 eq. (2.19) gives')
    P('    pi_ab = -eta_0 W_ab; p. 218 eq. (2.22) gives')
    P('    eta_0^i = 0.96 n_i T_i tau_i and eq. (2.23) gives')
    P('    eta_1^i = (3/10) n_i T_i/(omega_i^2 tau_i) with eta_2 = 4 eta_1.')
    P('    The electron values on the same page are 0.73 and 0.51 at Z=1.')
    P('  Zhuravleva, I., Churazov, E., Schekochihin, A. A., Allen, S. W.,')
    P('    Vikhlinin, A. & Werner, N. (2019), "Suppressed effective')
    P('    viscosity in the bulk intergalactic plasma", Nature Astronomy')
    P('    3, 832-837.  arXiv:1906.06346.  DOI 10.1038/s41550-019-0794-z.')
    P('    A 12-day Chandra observation of an offset region of the Coma')
    P('    Cluster against DNS: "the effective viscosity must be')
    P('    suppressed by at least a factor of ~10 to ~1000 for Pr <= 1".')
    P('    THE SOURCE FOR THE ICM VISCOSITY BEING CONTESTED, and it gives')
    P('    a one-sided bound rather than only an open question.')
    P('  Kadoya, K., Matsunaga, N. & Nagashima, A. (1985), "Viscosity and')
    P('    thermal conductivity of dry air in the gaseous phase", J. Phys.')
    P('    Chem. Ref. Data 14, 947-970.  DOI 10.1063/1.555744, confirmed')
    P('    at Crossref.  NOT READ: no copy is served by NIST, ADS or AIP.')
    P('    NU_AIR_MEAS therefore carries two significant figures and is')
    P('    labelled in PART D(a) as having no primary source.')
    P('  Kolmogorov, A. N. (1941), Dokl. Akad. Nauk SSSR 30, 299 - the')
    P('    original.  NOT READ; cited for the result only, as Module 1')
    P('    does for Maxwell (1867).')


if __name__ == '__main__':
    main()
