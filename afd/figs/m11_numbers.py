"""Module 11 numbers: accretion discs.  Keplerian shear and the Rayleigh
criterion, the timescale gap that molecular viscosity cannot close, the
Shakura-Sunyaev alpha prescription, vertical structure and the thin-disc
condition, the steady disc and its temperature profile, the radiative
efficiency, the Toomre criterion, centrifugal support, and the link to
the magnetorotational instability that Module 12 already derived.

Every physical number quoted in module11.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

STEP 1 OF SIX.  NO CONSTANT IN THIS FILE IS VERIFIED YET.  Every published
value carries the tag NOT YET VERIFIED and the paper it must be read from.
Step 2 fetches those papers, reads the page, and replaces the tag.  Nothing
here may be quoted in prose until it does.

WHAT THIS MODULE OWES, AND TO WHOM.  The eighteen debts eleven shipped pages
have already printed against Module 11 are listed, each with the file and
line it was read from, in .ignore/m11-promises.md.  The four that drive the
design:

  module12.html:700   Module 12 SS9 already prints the problem in one line.
                      A Keplerian disc has Omega ~ R^-3/2, so its specific
                      angular momentum ell = Omega R^2 ~ R^1/2 INCREASES
                      outward, the Rayleigh criterion calls that stable, and
                      a stable disc does not accrete.  PART B derives it.
  module12.html:782   The Keplerian q = 3/2 is ASSUMED there and not
                      derived.  PART B derives it from a point mass.
  module12.html:940   A shipped page has already fixed this module's alpha
                      as the disc viscosity parameter.  Not a Gate D choice.
  module09.html:757   A shipped REFUTED verdict rests on "a geometrically
                      thin accretion disc radiates with eta_rad ~ 0.1",
                      which Module 9 asserts and does not derive.  PART G
                      derives it and says what happens to Module 9's factor.

THE FOUR CHECKS, WITH THE VERDICTS NOT YET FIXED -- Gate D fixes them.

  CHECK 1  THE TIMESCALE GAP.  REFUTES molecular viscosity, and it is the
           reason the rest of the module exists.  index.html:78 has already
           promised this number in print: "the timescale gap that forces
           it".  Module 1 SS6 supplies the transport coefficients, which
           module01.html:623 says in print is what Module 11 needs them for.

  CHECK 2  ALPHA FROM AN OUTBURST.  The viscous time of a dwarf-nova disc
           set equal to an observed outburst timescale gives a number for
           alpha.  IT IS NOT INDEPENDENT of King, Pringle & Livio's range:
           their 0.1-0.4 comes from disc-instability modelling of the same
           observable.  The honest verdict is CONSISTENT at one order of
           magnitude, not CONFIRMED.  Gate D rules on the wording.

  CHECK 3  THE RADIATIVE EFFICIENCY.  Three numbers, not one: the Newtonian
           thin disc at the Schwarzschild innermost stable circular orbit
           gives exactly 1/12; the relativistic Schwarzschild value is
           1 - sqrt(8/9); and the Soltan-argument mean over the quasar
           population is near 0.1.  Module 9's 0.1 sits above both zero-spin
           values, which is a statement about spin.

  CHECK 4  ALPHA IS NOT A CONSTANT OF NATURE.  REFUTES the prescription read
           as a law.  The same dimensionless number measured in dwarf novae
           and in protoplanetary discs differs by more than two decades.
           King, Pringle & Livio's title asks exactly this question.

A NOTATION WARNING, FROM .ignore/m11-promises.md.  The glyph ell already
carries three meanings in this book: Module 6's mixing length alpha H,
Module 10's separation inside the inertial range, and -- undeclared in any
notation table -- the specific angular momentum Omega R^2 at
module12.html:700.  In THIS file ell is the specific angular momentum and
nothing else.  The mixing length does not occur here.
"""

import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m12_numbers.py rather than imported, so that each
# module's numbers script reads on its own.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
e = 4.80320471e-10      # esu            (elementary charge)
me = 9.1093837015e-28   # g
mp = 1.67262192369e-24  # g
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
hbar = 1.054571817e-27  # erg s
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
sigma_SB = 5.670374419e-5   # erg cm^-2 s^-1 K^-4  (exact, SI definition)
sigma_T = 6.6524587321e-25  # cm^2      (Thomson cross-section)
pc = 3.0856775814913673e18   # cm
kpc = 1e3*pc
AU = 1.495978707e13     # cm
yr = 3.15576e7          # s
day = 86400.0           # s

GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
Rsun = 6.957e10         # cm             (IAU 2015 nominal)
Msun = GMsun/G          # g

# Module 1's inputs, reused unchanged so the modules cannot diverge.
SPITZER_C = 3.0**1.5/(4.0*np.sqrt(np.pi))   # = 0.7329, Sarazin eq. 5.32
MU_IONISED_H = 0.6      # mean molecular weight, fully ionised H + He
MU_MOLECULAR = 2.34     # mean molecular weight, H2 + He, protoplanetary

# =========================================================================
# PUBLISHED VALUES COMPARED AGAINST.  Each block names the paper, the table
# or equation, and what the quoted error means.  AT STEP 1 NOT ONE OF THEM
# HAS BEEN READ.  The tag is the instruction to step 2.
# =========================================================================

# --- Shakura & Sunyaev (1973), A&A 24, 337-355. -------------------------
# The alpha prescription itself.  Their form is t_r,phi = alpha P, a
# stress proportional to the pressure, with 0 < alpha < 1 because the
# turbulent velocity cannot exceed the sound speed and the field cannot
# exceed equipartition.  NOT YET VERIFIED: step 2 must read the page that
# prints the bound and the page that prints nu = alpha c_T H, and must
# record whether they write the bound as alpha <= 1 or alpha < 1.
SS73_ALPHA_MAX = 1.0            # their upper bound      NOT YET VERIFIED

# --- King, Pringle & Livio (2007), MNRAS 376, 1740-1746. ----------------
# "Accretion disc viscosity: how big is alpha?"  Their review of dwarf-nova
# outburst modelling.  NOT YET VERIFIED: step 2 must read the abstract and
# the section that states the range, and must record whether 0.1-0.4 is the
# OUTBURST value and what the quiescent value is stated as.
KPL07_ALPHA_LO = 0.1            # outburst, dwarf novae  NOT YET VERIFIED
KPL07_ALPHA_HI = 0.4            # outburst, dwarf novae  NOT YET VERIFIED
KPL07_ALPHA_QUIESCENT = 0.01    # quiescent              NOT YET VERIFIED

# --- Flaherty et al. (2018), ApJ 856, 117. ------------------------------
# ALMA CO line widths toward the protoplanetary disc HD 163296, read as a
# bound on the non-thermal velocity and therefore on alpha.  NOT YET
# VERIFIED: step 2 must read the paper, record whether the bound is on
# delta v/c_T or on alpha directly, and record which molecular line and
# which radii it applies to.  A bound has a direction and step 2 must
# record which way it points.
FLAHERTY18_ALPHA_MAX = 3.0e-3   # upper bound            NOT YET VERIFIED

# --- Yu & Tremaine (2002), MNRAS 335, 965-976. --------------------------
# The Soltan argument: the mass in local black holes against the integrated
# quasar light gives a population-mean radiative efficiency.  NOT YET
# VERIFIED: step 2 must read the paper and record the value, its error, and
# whether it is quoted as a value or as a lower bound.  If it is a bound,
# CHECK 3's wording changes.
YT02_EFFICIENCY = 0.1           # population mean        NOT YET VERIFIED

# --- Toomre (1964), ApJ 139, 1217-1238. ---------------------------------
# The local stability criterion for a differentially rotating sheet.  NOT
# YET VERIFIED: step 2 must read the paper and record whether his criterion
# is written with the epicyclic frequency or with 2 Omega, and whether the
# coefficient for a GAS disc is pi (Toomre's stellar disc uses 3.36).  The
# difference is 7 per cent in Q and the module must not average them.
TOOMRE_GAS_COEFF = np.pi        # Q = c_T kappa_ep/(pi G Sigma)  NOT YET VER.
TOOMRE_STELLAR_COEFF = 3.36     # Toomre's own, stellar  NOT YET VERIFIED

# --- the innermost stable circular orbit. -------------------------------
# Schwarzschild: R_isco = 6 G M/c^2, and the binding energy of a circular
# orbit there is 1 - sqrt(8/9) of the rest mass.  NOT YET VERIFIED: this is
# textbook general relativity and step 2 must cite a page for it, not a
# memory.  It is the one number in CHECK 3 this book cannot derive, because
# the book is Newtonian throughout.
ISCO_SCHWARZSCHILD_RG = 6.0     # in units of G M/c^2    NOT YET VERIFIED
ETA_SCHWARZSCHILD = 1.0 - np.sqrt(8.0/9.0)   # = 0.05719  NOT YET VERIFIED

# --- Module 9's asserted thin-disc efficiency. --------------------------
# module09.html:757, a SHIPPED page: "A geometrically thin accretion disc
# radiates with eta_rad ~ 0.1."  Asserted there, derived here.  Read off
# the file on 2026-09-20; the line is quoted in .ignore/m11-promises.md
# row 8.  This is not a published value and carries no tag: it is what this
# book already printed.
M09_ASSERTED_ETA = 0.1

# --- predictions, held as named constants so no magic number appears ----
KEPLER_Q = 1.5          # q = -d ln Omega/d ln R for a point mass
RAYLEIGH_Q_CRIT = 2.0   # kappa_ep^2 > 0 iff q < 2
MRI_GROWTH_FACTOR = 0.75        # gamma_max = (q/2) Omega, Module 12 SS9
MRI_KMAX_FACTOR = np.sqrt(15.0)/4.0     # (k v_A)_max = sqrt(15)/4 Omega
THIN_DISC_TEFF_INDEX = -0.75    # T_eff ~ R^-3/4 far from the inner edge


# =========================================================================
# PART A.  The three discs, and the one question that separates them
# =========================================================================

def kepler_omega(M, R):
    """Omega_K = sqrt(G M/R^3).

    COPIED FROM m12_numbers.py PART I, where it was written for the MRI
    and is the same function.  Retyping it is the mistake the Module 12
    editor pass named.
    """
    return np.sqrt(G*M/R**3)


def kepler_speed(M, R):
    """v_K = Omega_K R = sqrt(G M/R)."""
    return np.sqrt(G*M/R)


def specific_angular_momentum(M, R):
    """ell = Omega R^2 = sqrt(G M R).

    THE GLYPH ell MEANS THIS AND NOTHING ELSE IN THIS FILE.  See the
    notation warning in the module docstring.  module12.html:700 already
    prints ell = Omega R^2 and Module 12 carries no notation row for it.
    """
    return np.sqrt(G*M*R)


def isothermal_sound_speed(T, mu):
    """c_T = sqrt(k T/(mu m_u)), Module 9's isothermal speed.

    THE ISOTHERMAL SPEED, not the adiabatic one.  The vertical structure
    of a thin disc is set by the pressure the gas actually has at its own
    temperature, and the disc is cooled by radiation on a timescale short
    against the viscous one, so the isothermal speed is the right one.
    Module 9 wrote c_T for exactly this quantity; the book does not need a
    second symbol for it.
    """
    return np.sqrt(kB*T/(mu*mu_u))


def scale_height(T, mu, M, R):
    """H = c_T/Omega_K, from vertical hydrostatic balance.

    PART E proves it.
    """
    return isothermal_sound_speed(T, mu)/kepler_omega(M, R)


def midplane_density(Sigma, H):
    """rho_0 = Sigma/(sqrt(2 pi) H), for a Gaussian vertical profile.

    PART E derives rho(z) = rho_0 exp(-z^2/2H^2), whose integral over all
    z is sqrt(2 pi) rho_0 H.  The factor is sqrt(2 pi) = 2.5066 and NOT 2:
    writing Sigma = 2 rho_0 H would be the constant-density slab and would
    put the density 25.3 per cent high.
    """
    return Sigma/(np.sqrt(2.0*np.pi)*H)


# =========================================================================
# PART B.  Keplerian shear, and why a disc does not accrete
# =========================================================================

def shear_parameter(M, R, dR_rel=1.0e-6):
    """q = -d ln Omega/d ln R, computed numerically from Omega_K.

    NOT RETURNED AS 3/2.  module12.html:782 says in print that the 3/2 is
    ASSUMED there and that deriving it needs a disc model, so this module
    must produce it rather than name it.  The derivative is taken on the
    function, so if kepler_omega were wrong this would be wrong too and
    the assert below would fire.
    """
    lnR1 = np.log(R*(1.0 - dR_rel))
    lnR2 = np.log(R*(1.0 + dR_rel))
    lnO1 = np.log(kepler_omega(M, np.exp(lnR1)))
    lnO2 = np.log(kepler_omega(M, np.exp(lnR2)))
    return -(lnO2 - lnO1)/(lnR2 - lnR1)


def epicyclic_frequency(Omega, q):
    """kappa_ep^2 = 2 Omega^2 (2 - q), for Omega ~ R^-q.

    THE SYMBOL IS kappa_ep AND NOT kappa.  notation_table.md:74 reserved it
    in Module 12 against the thermal conductivity, and said it did so
    "because a reader who knows that literature will look for it".  This
    module inherits the reservation.

    At q = 3/2 this gives kappa_ep = Omega exactly, which is the degeneracy
    that makes a Keplerian orbit close.
    """
    return Omega*np.sqrt(2.0*(2.0 - q))


def rayleigh_discriminant(M, R, dR_rel=1.0e-6):
    """d(ell^2)/dR, the Rayleigh discriminant.  Positive means STABLE.

    ell^2 = G M R for a point mass, so d(ell^2)/dR = G M > 0 everywhere:
    a Keplerian disc is hydrodynamically stable at every radius, and that
    is the problem, not the answer.  module12.html:700 states it in prose.
    """
    R1, R2 = R*(1.0 - dR_rel), R*(1.0 + dR_rel)
    l1 = specific_angular_momentum(M, R1)
    l2 = specific_angular_momentum(M, R2)
    return (l2**2 - l1**2)/(R2 - R1)


# =========================================================================
# PART C.  The timescale gap.  CHECK 1
# =========================================================================

def debye(n, T):
    """Debye length sqrt(k T/(4 pi n e^2)).  COPIED FROM m12_numbers.py."""
    return np.sqrt(kB*T/(4.0*np.pi*n*e**2))


def b_min_e(T):
    """Classical/quantum turning point for an electron.

    COPIED FROM m12_numbers.py PART B.  The larger of the classical
    distance of closest approach and the thermal de Broglie wavelength.
    """
    b_cl = e**2/(3.0*kB*T)
    b_qm = hbar/np.sqrt(3.0*me*kB*T)
    return max(b_cl, b_qm)


def lnLambda_e(n, T):
    """Coulomb logarithm, ln(lambda_D/b_min).  COPIED FROM m12_numbers.py."""
    return np.log(debye(n, T)/b_min_e(T))


def lam_coulomb(n, T, lnL, coef=SPITZER_C):
    """Thermal Coulomb mean free path, Module 1's equation and coefficient.

        lambda = coef (k T)^2/(n e^4 ln Lambda),  coef = 3^(3/2)/(4 sqrt(pi))

    COPIED FROM m12_numbers.py, which copied it from m10_numbers.py.
    Retyping it once already put a spurious pi in the denominator.
    """
    return coef*(kB*T)**2/(n*e**4*lnL)


def v_thermal(T, mu):
    """Mean thermal speed sqrt(8 k T/(pi mu m_u)).  Module 1's definition."""
    return np.sqrt(8.0*kB*T/(np.pi*mu*mu_u))


def molecular_viscosity(n, T, mu, lnL):
    """nu_mol = (1/3) lambda v_th, the kinetic-theory kinematic viscosity.

    THE COEFFICIENT IS 1/3 AND IT IS A CONVENTION, not a measurement.
    Chapman-Enskog for a Lorentz plasma gives a number near 0.4 rather
    than 0.333, and Module 1 SS6 carries the exact coefficients.  CHECK 1
    is worth twelve decades, so a factor of 1.2 changes nothing in it --
    but the module must say that rather than hide it.
    """
    return lam_coulomb(n, T, lnL)*v_thermal(T, mu)/3.0


def viscous_time(R, nu):
    """t_nu = R^2/nu.  The time for the viscous diffusion of PART D to
    move material across a distance R."""
    return R*R/nu


def dynamical_time(Omega):
    """t_dyn = 1/Omega.  One radian of orbit, not one orbit."""
    return 1.0/Omega


# =========================================================================
# PART D.  The alpha prescription, and the three timescales
# =========================================================================

def alpha_viscosity(alpha, c_T, H):
    """nu = alpha c_T H.  Shakura & Sunyaev (1973).

    THIS IS NOT A DERIVATION AND THE MODULE MUST NOT PRETEND IT IS.  It is
    a dimensional parametrisation with one bound behind it: the turbulent
    eddy cannot be larger than H or faster than c_T without shocking, so
    alpha <= 1.  What supplies the stress is the magnetorotational
    instability of Module 12 SS9; what alpha's VALUE is, neither module
    derives.  module12.html:940 already fixes this symbol for this meaning.
    """
    return alpha*c_T*H


def alpha_from_viscous_time(R, t_nu, c_T, H):
    """Invert nu = alpha c_T H against a measured t_nu = R^2/nu."""
    return R*R/(t_nu*c_T*H)


def thermal_time(alpha, Omega):
    """t_th = 1/(alpha Omega).  The time to radiate the heat alpha supplies."""
    return 1.0/(alpha*Omega)


def viscous_time_alpha(alpha, Omega, H, R):
    """t_nu = (1/alpha)(R/H)^2 (1/Omega), the alpha-disc viscous time.

    The identity worth printing: with nu = alpha c_T H and H = c_T/Omega,
        t_nu = R^2/nu = R^2/(alpha c_T H) = R^2/(alpha Omega H^2)
             = (1/alpha)(R/H)^2 t_dyn.
    So the three timescales are ordered
        t_dyn : t_th : t_nu  =  1 : 1/alpha : (1/alpha)(R/H)^2,
    and for a thin disc (H/R << 1) with alpha < 1 that ordering is strict.
    """
    return (R/H)**2/(alpha*Omega)


# =========================================================================
# PART E.  Vertical structure and the thin-disc condition
# =========================================================================

def vertical_gravity(M, R, z):
    """g_z = G M z/(R^2 + z^2)^(3/2), the vertical pull of the central mass.

    For z << R this is Omega_K^2 z, which is what makes the vertical
    profile a Gaussian.  The function keeps the exact form so that PART E
    can price the error of the approximation rather than assume it.
    """
    return G*M*z/(R*R + z*z)**1.5


def vertical_gravity_thin(M, R, z):
    """Omega_K^2 z, the thin-disc approximation to vertical_gravity."""
    return kepler_omega(M, R)**2*z


def density_profile(rho0, z, H):
    """rho(z) = rho_0 exp(-z^2/2H^2), isothermal vertical hydrostatic."""
    return rho0*np.exp(-0.5*(z/H)**2)


def aspect_ratio(T, mu, M, R):
    """H/R = c_T/v_K.  The thin-disc condition is that this is small."""
    return isothermal_sound_speed(T, mu)/kepler_speed(M, R)


# =========================================================================
# PART F.  The steady thin disc
# =========================================================================

def nu_sigma_steady(Mdot, R, R_in):
    """nu Sigma = (Mdot/3 pi)[1 - sqrt(R_in/R)].

    The steady solution of the diffusion equation with a zero-torque inner
    boundary.  The bracket is what makes the disc radiate MORE than the
    local release rate at large R: a factor of three at R >> R_in, because
    the inner disc's angular momentum has to go somewhere.
    """
    return (Mdot/(3.0*np.pi))*(1.0 - np.sqrt(R_in/R))


def dissipation_per_area(Mdot, M, R, R_in):
    """D(R) = (3 G M Mdot/8 pi R^3)[1 - sqrt(R_in/R)], per unit area PER SIDE.

    PER SIDE.  The disc has two faces and radiates from both, so the
    quantity that equals sigma T_eff^4 is half the total dissipation per
    unit area of disc.  Getting this factor wrong moves T_eff by 2^(1/4)
    = 19 per cent.
    """
    return (3.0*G*M*Mdot/(8.0*np.pi*R**3))*(1.0 - np.sqrt(R_in/R))


def t_effective(Mdot, M, R, R_in):
    """T_eff = (D(R)/sigma_SB)^(1/4)."""
    return (dissipation_per_area(Mdot, M, R, R_in)/sigma_SB)**0.25


def t_eff_index(Mdot, M, R, R_in, dR_rel=1.0e-6):
    """d ln T_eff/d ln R, computed numerically.  Tends to -3/4 far out."""
    R1, R2 = R*(1.0 - dR_rel), R*(1.0 + dR_rel)
    t1 = t_effective(Mdot, M, R1, R_in)
    t2 = t_effective(Mdot, M, R2, R_in)
    return (np.log(t2) - np.log(t1))/(np.log(R2) - np.log(R1))


def disc_luminosity(Mdot, M, R_in):
    """L = G M Mdot/(2 R_in), the integral of 2 D(R) over the whole disc.

    HALF the binding energy at R_in, not all of it.  The other half is the
    kinetic energy of the orbit at R_in, which the disc has not radiated.
    """
    return G*M*Mdot/(2.0*R_in)


# =========================================================================
# PART G.  The radiative efficiency.  CHECK 3
# =========================================================================

def gravitational_radius(M):
    """R_g = G M/c^2."""
    return G*M/c**2


def efficiency_newtonian(R_in_over_Rg):
    """eta = L/(Mdot c^2) = 1/(2 x), with x = R_in/R_g.

    From PART F:  L = G M Mdot/(2 R_in), so
        eta = G M/(2 R_in c^2) = R_g/(2 R_in) = 1/(2 x).
    At the Schwarzschild innermost stable circular orbit, x = 6, this is
    EXACTLY 1/12.  The assert below is the trivial-limit check the Module
    12 editor pass asked every later module to copy.
    """
    return 1.0/(2.0*R_in_over_Rg)


def eddington_luminosity(M):
    """L_Edd = 4 pi G M m_p c/sigma_T.

    Module 9 states this and does not derive it; module09.html:944 sends
    the derivation to Module 13 and this module does NOT take it up.  It
    is used here only to set a scale for Mdot.
    """
    return 4.0*np.pi*G*M*mp*c/sigma_T


def eddington_rate(M, eta):
    """Mdot_Edd = L_Edd/(eta c^2).  Depends on the efficiency assumed."""
    return eddington_luminosity(M)/(eta*c*c)


# =========================================================================
# PART H.  Self-gravity: the Toomre criterion
# =========================================================================

def toomre_q(c_T, kappa_ep, Sigma, coeff=TOOMRE_GAS_COEFF):
    """Q = c_T kappa_ep/(coeff G Sigma).  Stable to axisymmetric
    modes if Q > 1.

    THE COEFFICIENT IS pi FOR A GAS DISC AND 3.36 FOR A STELLAR ONE, and
    the module must not average them.  Module 5 built the Jeans criterion
    for a non-rotating gas; this is the same competition with rotation
    added, which is the promise module05.html:764 printed.
    """
    return c_T*kappa_ep/(coeff*G*Sigma)


def toomre_q_steady(alpha, c_T, Mdot, R, R_in):
    """Q for a steady alpha-disc, in closed form.

    Substituting Sigma = nu_sigma_steady/nu with nu = alpha c_T H and
    H = c_T/Omega, and kappa_ep = Omega for a Keplerian disc:

        Sigma = (Mdot/3 pi) f Omega/(alpha c_T^2),   f = 1 - sqrt(R_in/R)
        Q = c_T Omega/(pi G Sigma) = 3 alpha c_T^3/(G Mdot f).

    OMEGA AND R HAVE BOTH CANCELLED.  Q depends on the LOCAL TEMPERATURE
    only, through c_T^3, and on two global numbers.  That is why the
    self-gravity radius of a disc is a statement about its temperature
    profile and not about its mass.
    """
    f = 1.0 - np.sqrt(R_in/R)
    return 3.0*alpha*c_T**3/(G*Mdot*f)


# =========================================================================
# PART I.  Centrifugal support, the promise of module03.html:792
# =========================================================================

def centrifugal_flattening(Omega, M, R):
    """Omega^2 R^3/(G M), the ratio of centrifugal to gravitational pull.

    module03.html:792 printed "Excludes centrifugal flattening and the
    rotational support of discs" and sent it here.  For a Keplerian disc
    this ratio is exactly 1 in the plane -- the disc is entirely
    centrifugally supported radially -- and the assert below checks it.
    A hydrostatic star has this ratio near zero; that is the whole
    difference between Module 3's object and this one.
    """
    return Omega**2*R**3/(G*M)


def circularisation_radius(M, ell):
    """R_circ = ell^2/(G M).  Where gas of specific angular momentum ell
    stops falling and starts orbiting.

    module09.html:832 printed that Sgr A*'s gas circularises near 100 r_S
    and that transporting its angular momentum outward "is Module 11's
    subject".  This is the function that makes that sentence a number.
    """
    return ell*ell/(G*M)


# =========================================================================
# PART J.  The link to the magnetorotational instability
# =========================================================================

def mri_growth_rate(omega, q=KEPLER_Q):
    """gamma_max = (q/2) Omega.  COPIED FROM m12_numbers.py PART I.

    Module 12 SS9 derived this with q ASSUMED.  PART B of this file derives
    the q.  The instability itself is NOT re-derived here:
    module08.html:728 lists it among what Module 12 builds, and deriving it
    twice would make one of the two modules redundant in print.
    """
    return 0.5*q*omega


def mri_wavelength_max(vA, omega):
    """2 pi v_A/(sqrt(15)/4 Omega).  COPIED FROM m12_numbers.py PART I."""
    return 2.0*np.pi*vA/(MRI_KMAX_FACTOR*omega)


def alfven_speed(B, rho):
    """v_A = B/sqrt(4 pi rho).  COPIED FROM m12_numbers.py PART A."""
    return B/np.sqrt(4.0*np.pi*rho)


def mri_containment_ratio(alpha):
    """lambda_max/(2H) = 4 pi sqrt(alpha)/sqrt(15), a PURE NUMBER.

    THE FIRST DRAFT OF THIS FILE PRINTED THIS AS A TWO-ROW TABLE OVER THE
    CENSUS AND BOTH ROWS CAME OUT 1.0260.  They had to.  Putting
    B = sqrt(4 pi alpha rho c_T^2) into v_A = B/sqrt(4 pi rho) gives
    v_A = c_T sqrt(alpha), and H = c_T/Omega, so

        lambda_max = 2 pi v_A/((sqrt(15)/4) Omega)
                   = (8 pi/sqrt(15)) sqrt(alpha) H

    and every disc property cancels.  A table of identical rows pretends
    to be a census result and is not one.  The real content is the bound
    below.
    """
    return 4.0*np.pi*np.sqrt(alpha)/np.sqrt(15.0)


def alpha_max_for_containment():
    """The largest alpha for which lambda_max < 2H: alpha < 15/(16 pi^2).

    A DERIVED BOUND, not a fitted one.  Setting mri_containment_ratio to
    1 and squaring gives alpha = 15/(16 pi^2) = 0.094993.  Above it the
    fastest-growing MRI mode is longer than the disc is thick, so the
    equipartition identification B^2 ~ 4 pi alpha P cannot be the whole
    story for the alpha that CHECK 2 infers.
    """
    return 15.0/(16.0*np.pi**2)


def field_for_alpha(alpha, rho, c_T):
    """The field whose Maxwell stress supplies a given alpha.

    The MRI's saturated stress is of order B_R B_phi/4 pi, and the alpha
    prescription writes that stress as alpha rho c_T^2.  Taking
    B_R B_phi ~ B^2 gives B ~ sqrt(4 pi alpha rho c_T^2) = sqrt(4 pi alpha
    P).  THIS IS AN ORDER-OF-MAGNITUDE IDENTIFICATION AND NOT A RESULT:
    simulations put B_R B_phi/B^2 near 0.3, and the module says so rather
    than printing a number to three figures.
    """
    return np.sqrt(4.0*np.pi*alpha*rho*c_T**2)


# =========================================================================
# THE CENSUS, AT MODULE SCOPE.  m11_build_figs.py imports these, so the
# figures and the prose cannot diverge -- m10_build_figs.py's rule.
#
# THESE THREE DISCS ARE A CONFIGURATION AND NOT AN OBJECT, in the sense
# module07.html:453 and module12.html:782 use the phrase, EXCEPT for the
# dwarf nova, which CHECK 1 and CHECK 2 do compare against measurement.
# Every entry is a round choice inside the range its class occupies.
# =========================================================================

# Dwarf nova in outburst.  A short-period cataclysmic variable: a white
# dwarf accreting from a Roche-lobe-filling companion.  NOT YET VERIFIED:
# step 2 must source the white-dwarf mass, the outer disc radius, the
# outburst temperature and the surface density, and must find a named
# system rather than a class average if CHECK 2 is to be a measurement.
M_WD = 0.6*Msun                 # g                      NOT YET VERIFIED
R_DN = 1.0e10                   # cm, outer disc         NOT YET VERIFIED
T_DN = 3.0e4                    # K, outburst            NOT YET VERIFIED
SIGMA_DN = 1.0e2                # g cm^-2, outburst      NOT YET VERIFIED
T_OUTBURST_OBSERVED = 5.0*day   # s, outburst duration   NOT YET VERIFIED

# Protoplanetary disc around a T Tauri star, at 10 au.
M_TT = 1.0*Msun                 # g                      NOT YET VERIFIED
R_TT = 10.0*AU                  # cm                     NOT YET VERIFIED
T_TT = 50.0                     # K                      NOT YET VERIFIED
SIGMA_TT = 10.0                 # g cm^-2                NOT YET VERIFIED

# The inner disc of a 10^8 M_sun active galactic nucleus, at 100 R_g.
M_AGN = 1.0e8*Msun              # g
R_AGN_RG = 100.0                # in units of R_g
MDOT_AGN_EDD_FRACTION = 0.1     # of the Eddington rate at eta = 0.1

DISC_ROWS = [
    # name, M, R, T, mu, Sigma
    ('dwarf nova, outburst', M_WD, R_DN, T_DN, MU_IONISED_H, SIGMA_DN),
    ('protoplanetary, 10 au', M_TT, R_TT, T_TT, MU_MOLECULAR, SIGMA_TT),
]


# =========================================================================
# ASSERTS.  Each one fails if a formula above is wrong, and each was
# written before the run rather than fitted to it.
# =========================================================================

def _self_check():
    """Every check here is a limit whose answer is known in advance."""
    # q = 3/2 for a point mass, to the accuracy of the numerical derivative.
    q = shear_parameter(M_WD, R_DN)
    assert abs(q - KEPLER_Q) < 1e-6, f'shear parameter is {q}, not 3/2'

    # kappa_ep = Omega exactly at q = 3/2.  The Keplerian degeneracy.
    Om = kepler_omega(M_WD, R_DN)
    assert abs(epicyclic_frequency(Om, KEPLER_Q)/Om - 1.0) < 1e-12

    # The Rayleigh discriminant is G M at every radius, and positive.
    d = rayleigh_discriminant(M_WD, R_DN)
    assert abs(d/(G*M_WD) - 1.0) < 1e-5, f'discriminant/GM = {d/(G*M_WD)}'
    assert d > 0.0, 'a Keplerian disc must come out Rayleigh-stable'

    # A Keplerian disc is exactly centrifugally supported in its plane.
    cf = centrifugal_flattening(Om, M_WD, R_DN)
    assert abs(cf - 1.0) < 1e-12, f'centrifugal ratio is {cf}, not 1'

    # THE TRIVIAL LIMIT OF CHECK 3.  At the Schwarzschild ISCO the
    # Newtonian efficiency is exactly 1/12.  If this ever fails, PART F's
    # factor of two in disc_luminosity is wrong.
    eta = efficiency_newtonian(ISCO_SCHWARZSCHILD_RG)
    assert abs(eta - 1.0/12.0) < 1e-15, f'eta is {eta}, not 1/12'

    # The efficiency must also equal the luminosity route, which uses
    # disc_luminosity and gravitational_radius and shares no line of code.
    R_in = ISCO_SCHWARZSCHILD_RG*gravitational_radius(M_AGN)
    Mdot = 1.0                  # 1 g/s, so L/(Mdot c^2) is eta directly
    assert abs(disc_luminosity(Mdot, M_AGN, R_in)/(Mdot*c*c)
               - 1.0/12.0) < 1e-12

    # T_eff -> R^-3/4 far from the inner edge.
    idx = t_eff_index(1.0e18, M_AGN, 1.0e6*gravitational_radius(M_AGN),
                      ISCO_SCHWARZSCHILD_RG*gravitational_radius(M_AGN))
    assert abs(idx - THIN_DISC_TEFF_INDEX) < 1e-3, f'T_eff index {idx}'

    # The closed-form Toomre Q must equal the long route.
    alpha, Mdot2 = 0.1, 1.0e25
    M, R = M_AGN, 1.0e4*gravitational_radius(M_AGN)
    R_in2 = ISCO_SCHWARZSCHILD_RG*gravitational_radius(M_AGN)
    Om2 = kepler_omega(M, R)
    T = t_effective(Mdot2, M, R, R_in2)
    cT = isothermal_sound_speed(T, MU_IONISED_H)
    H = cT/Om2
    nu = alpha_viscosity(alpha, cT, H)
    Sig = nu_sigma_steady(Mdot2, R, R_in2)/nu
    q_long = toomre_q(cT, epicyclic_frequency(Om2, KEPLER_Q), Sig)
    q_short = toomre_q_steady(alpha, cT, Mdot2, R, R_in2)
    assert abs(q_long/q_short - 1.0) < 1e-10, f'{q_long} vs {q_short}'

    # The MRI containment ratio must be the identity, on BOTH census
    # rows and for the closed form.  This is the assert that would have
    # caught the decorative two-row table on the first run.
    for _n, _M, _R, _T, _mu, _S in DISC_ROWS:
        _Om = kepler_omega(_M, _R)
        _cT = isothermal_sound_speed(_T, _mu)
        _H = _cT/_Om
        _rho = midplane_density(_S, _H)
        _B = field_for_alpha(0.1, _rho, _cT)
        _lam = mri_wavelength_max(alfven_speed(_B, _rho), _Om)
        assert abs(_lam/(2.0*_H)/mri_containment_ratio(0.1) - 1.0) < 1e-12
    assert abs(mri_containment_ratio(alpha_max_for_containment())
               - 1.0) < 1e-12

    # The three timescales must be ordered for a thin disc.
    cT_dn = isothermal_sound_speed(T_DN, MU_IONISED_H)
    H_dn = cT_dn/Om
    t1 = dynamical_time(Om)
    t2 = thermal_time(0.2, Om)
    t3 = viscous_time_alpha(0.2, Om, H_dn, R_DN)
    assert t1 < t2 < t3, f'timescales out of order: {t1} {t2} {t3}'

    # viscous_time_alpha and viscous_time must agree.
    nu_dn = alpha_viscosity(0.2, cT_dn, H_dn)
    assert abs(viscous_time(R_DN, nu_dn)/t3 - 1.0) < 1e-12

    # The Gaussian column must integrate to Sigma.
    z = np.linspace(-20.0*H_dn, 20.0*H_dn, 200001)
    rho0 = midplane_density(SIGMA_DN, H_dn)
    col = np.trapezoid(density_profile(rho0, z, H_dn), z)
    assert abs(col/SIGMA_DN - 1.0) < 1e-6, f'column is {col/SIGMA_DN} Sigma'

    # The thin-disc vertical gravity must approach the exact one.
    zt = 0.01*R_DN
    assert abs(vertical_gravity_thin(M_WD, R_DN, zt)
               / vertical_gravity(M_WD, R_DN, zt) - 1.0) < 2e-4


def main():
    _self_check()
    P = print
    P('=' * 74)
    P('MODULE 11 NUMBERS: accretion discs')
    P('=' * 74)
    P('STEP 1 OF SIX.  NOT ONE PUBLISHED CONSTANT IN THIS FILE HAS BEEN')
    P('READ YET.  Every one carries the tag NOT YET VERIFIED and the paper')
    P('step 2 must fetch.  No number below may be quoted in prose until')
    P('step 2 replaces the tag.  The four checks have no verdicts yet:')
    P('Gate D fixes them in advance, as Modules 7 to 12 did.')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  Keplerian shear, and why a disc does not accrete')
    P('-'*74)
    P('  module12.html:700 prints the argument and module12.html:782 says')
    P('  the q = 3/2 behind it is ASSUMED.  Here it is derived.')
    P('')
    q = shear_parameter(M_WD, R_DN)
    Om_dn = kepler_omega(M_WD, R_DN)
    kap = epicyclic_frequency(Om_dn, q)
    P(f'  q = -d ln Omega/d ln R, differentiated numerically = {q:.10f}')
    P(f'  exactly 3/2 to {abs(q - KEPLER_Q):.2e}, and the assert requires it')
    P(f'  kappa_ep/Omega at q = 3/2                          = '
      f'{kap/Om_dn:.10f}')
    P('  so the epicyclic and orbital frequencies are EQUAL, which is why')
    P('  a Keplerian orbit closes on itself and does not precess.')
    P('')
    P('  THE RAYLEIGH CRITERION.  A rotating flow is stable to')
    P('  axisymmetric displacements where d(ell^2)/dR > 0.  For a point')
    P('  mass ell^2 = G M R, so')
    d = rayleigh_discriminant(M_WD, R_DN)
    P(f'    d(ell^2)/dR             = {d:.6e} cm^3 s^-2')
    P(f'    G M                     = {G*M_WD:.6e} cm^3 s^-2')
    P(f'    ratio                   = {d/(G*M_WD):.10f}')
    P('  POSITIVE AT EVERY RADIUS, and independent of radius.  The disc')
    P('  is stable, and a stable disc transports no angular momentum and')
    P('  therefore does not accrete.  THAT IS THE PROBLEM OF THIS MODULE.')
    P(f'  Instability would need q > {RAYLEIGH_Q_CRIT:.1f}, and a point')
    P('  mass gives 3/2 and can give nothing else.')

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  The census.  TWO rows here, and a third at PART F')
    P('-'*74)
    P('  THESE ARE CONFIGURATIONS AND NOT OBJECTS, except that CHECK 1')
    P('  and CHECK 2 do compare the dwarf-nova row against measurement.')
    P('  Every entry is NOT YET VERIFIED.  The active-galactic-nucleus')
    P('  disc is NOT in this table: it has no independent temperature,')
    P('  because PART F computes T_eff for it from the accretion rate.')
    P('  Putting it here would have meant inventing a temperature.')
    P('')
    P(f'  {"disc":<24} {"T (K)":>8} {"Omega (s^-1)":>13} {"c_T (km/s)":>11} '
      f'{"H/R":>10} {"n (cm^-3)":>11}')
    census = {}
    for name, M, R, T, mu, Sigma in DISC_ROWS:
        Om = kepler_omega(M, R)
        cT = isothermal_sound_speed(T, mu)
        H = cT/Om
        rho0 = midplane_density(Sigma, H)
        n0 = rho0/(mu*mu_u)
        census[name] = dict(M=M, R=R, T=T, mu=mu, Sigma=Sigma, Om=Om,
                            cT=cT, H=H, rho0=rho0, n0=n0)
        P(f'  {name:<24} {T:>8.3g} {Om:>13.4e} {cT/1e5:>11.4g} '
          f'{H/R:>10.5f} {n0:>11.4g}')
    P('')
    P('  BOTH ARE THIN: H/R is a few per cent, so the thin-disc')
    P('  approximation of PART E is self-consistent in both rows.')

    # ---------------------------------------------------------------- C
    P('')
    P('PART C.  CHECK 1.  The timescale gap')
    P('-'*74)
    P('  index.html:78 has already promised this number in print.')
    P('  module01.html:623 says Module 1 SS6 supplies the coefficients')
    P('  and that Module 11 needs them for accretion discs.  Here they')
    P('  are used.')
    P('')
    dn = census['dwarf nova, outburst']
    lnL = lnLambda_e(dn['n0'], dn['T'])
    lam = lam_coulomb(dn['n0'], dn['T'], lnL)
    vth = v_thermal(dn['T'], dn['mu'])
    nu_mol = molecular_viscosity(dn['n0'], dn['T'], dn['mu'], lnL)
    t_nu_mol = viscous_time(dn['R'], nu_mol)
    t_dyn = dynamical_time(dn['Om'])
    P(f'  dwarf-nova disc at R      = {dn["R"]:.3e} cm')
    P(f'    midplane n              = {dn["n0"]:.4e} cm^-3')
    P(f'    ln Lambda               = {lnL:.4f}')
    P(f'    Coulomb mean free path  = {lam:.4e} cm')
    P(f'      lambda/H              = {lam/dn["H"]:.4e}')
    P(f'    mean thermal speed      = {vth/1e5:.4f} km/s')
    P(f'    nu_mol = lambda v_th/3  = {nu_mol:.4f} cm^2 s^-1')
    P('')
    P(f'    t_dyn = 1/Omega         = {t_dyn:.4e} s '
      f'= {t_dyn/day:.4f} d')
    P(f'    t_nu = R^2/nu_mol       = {t_nu_mol:.4e} s '
      f'= {t_nu_mol/yr:.4e} yr')
    P(f'    observed outburst       = {T_OUTBURST_OBSERVED:.4e} s '
      f'= {T_OUTBURST_OBSERVED/day:.1f} d   NOT YET VERIFIED')
    P('')
    P('  PUNCHLINE CHECK 1, AND THE VERDICT IS NOT FIXED AT STEP 1.')
    gap = t_nu_mol/T_OUTBURST_OBSERVED
    P(f'    t_nu(molecular)/t_observed = {gap:.4e}')
    P(f'    that is {np.log10(gap):.2f} DECADES.')
    P('    Molecular viscosity is not slow by a factor.  It is slow by')
    P(f'    {np.log10(gap):.2f} decades, and no refinement of the transport')
    P('    coefficient closes a gap of that size: the 1/3 in nu_mol is a')
    P('    convention worth 20 per cent and ln Lambda is worth a factor')
    P('    of two.  SOMETHING OTHER THAN COLLISIONS MOVES THE ANGULAR')
    P('    MOMENTUM.')
    alpha_needed = nu_mol/(dn['cT']*dn['H'])
    P(f'    alpha_equivalent of nu_mol = {alpha_needed:.4e}')
    P(f'    against the measured {KPL07_ALPHA_LO}-{KPL07_ALPHA_HI}: short')
    P(f'    by {np.log10(KPL07_ALPHA_LO/alpha_needed):.2f} to '
      f'{np.log10(KPL07_ALPHA_HI/alpha_needed):.2f} decades.')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  CHECK 2.  alpha from an outburst, and the three timescales')
    P('-'*74)
    alpha_inferred = alpha_from_viscous_time(
        dn['R'], T_OUTBURST_OBSERVED, dn['cT'], dn['H'])
    P(f'  Setting t_nu = R^2/(alpha c_T H) equal to the observed')
    P(f'  outburst timescale gives')
    P(f'    alpha_inferred          = {alpha_inferred:.4f}')
    P(f'    King, Pringle & Livio   = {KPL07_ALPHA_LO}-{KPL07_ALPHA_HI}'
      f'   NOT YET VERIFIED')
    P('')
    P('  PUNCHLINE CHECK 2, AND IT IS NOT AN INDEPENDENT CONFIRMATION.')
    P('  King, Pringle & Livio infer their range from disc-instability')
    P('  modelling of the SAME observable, so agreement here tests the')
    P('  arithmetic and the order of magnitude, not the physics.  The')
    P('  honest verdict is CONSISTENT, and Gate D rules on the wording.')
    if alpha_inferred > KPL07_ALPHA_HI:
        P(f'    ratio to the top of their range = '
          f'{alpha_inferred/KPL07_ALPHA_HI:.4f}, ABOVE it')
    elif alpha_inferred < KPL07_ALPHA_LO:
        P(f'    ratio to the bottom of their range = '
          f'{alpha_inferred/KPL07_ALPHA_LO:.4f}, BELOW it')
    else:
        P('    inside their range')
    P('')
    P('  THE THREE TIMESCALES, at alpha = 0.2 and the dwarf-nova row:')
    a0 = 0.2
    tt = thermal_time(a0, dn['Om'])
    tv = viscous_time_alpha(a0, dn['Om'], dn['H'], dn['R'])
    P(f'    t_dyn                   = {t_dyn:.4e} s')
    P(f'    t_th  = t_dyn/alpha     = {tt:.4e} s   '
      f'ratio {tt/t_dyn:.2f}')
    P(f'    t_nu  = t_th (R/H)^2    = {tv:.4e} s   '
      f'ratio {tv/t_dyn:.4e}')
    P(f'    (R/H)^2                 = {(dn["R"]/dn["H"])**2:.4e}')
    P('    The ordering t_dyn < t_th < t_nu is what makes a thin disc a')
    P('    well-posed object: it can be treated as hydrostatic vertically')
    P('    and in thermal balance locally while it evolves radially.')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  Vertical structure, and the price of the thin approximation')
    P('-'*74)
    z_test = 2.0*dn['H']
    exact = vertical_gravity(dn['M'], dn['R'], z_test)
    thin = vertical_gravity_thin(dn['M'], dn['R'], z_test)
    P(f'  At z = 2H = {z_test:.4e} cm, z/R = {z_test/dn["R"]:.5f}:')
    P(f'    exact g_z               = {exact:.6e} cm s^-2')
    P(f'    thin-disc Omega^2 z     = {thin:.6e} cm s^-2')
    P(f'    error                   = {100*(thin/exact - 1.0):.4f} per cent')
    P('  0.31 PER CENT AT TWO SCALE HEIGHTS, and 95.45 per cent of a')
    P('  Gaussian column lies inside 2H.  The error grows as (z/R)^2, so')
    P('  it is the ASPECT RATIO and not the height that prices it: at')
    P(f'  H/R = {dn["H"]/dn["R"]:.5f} the disc is thin enough that the')
    P('  approximation costs less than half a per cent where the mass is.')
    rho0 = dn['rho0']
    P(f'    rho_0 = Sigma/(sqrt(2 pi) H) = {rho0:.4e} g cm^-3')
    P('    The factor is sqrt(2 pi) = 2.5066 and not 2; a constant-density')
    P('    slab would put rho_0 25.3 per cent high.')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  The steady thin disc')
    P('-'*74)
    Rg_agn = gravitational_radius(M_AGN)
    R_in_agn = ISCO_SCHWARZSCHILD_RG*Rg_agn
    eta_assumed = M09_ASSERTED_ETA
    Mdot_agn = MDOT_AGN_EDD_FRACTION*eddington_rate(M_AGN, eta_assumed)
    P(f'  A 10^8 M_sun black hole, R_g = {Rg_agn:.4e} cm')
    P(f'    R_in = 6 R_g            = {R_in_agn:.4e} cm')
    P(f'    L_Edd                   = {eddington_luminosity(M_AGN):.4e} erg/s')
    P(f'    Mdot at 0.1 Edd, eta=0.1= {Mdot_agn:.4e} g/s '
      f'= {Mdot_agn*yr/Msun:.4f} M_sun/yr')
    P('')
    P(f'  {"R/R_g":>10} {"T_eff (K)":>12} {"d ln T/d ln R":>15}')
    for x in [10.0, 30.0, 1.0e2, 1.0e3, 1.0e4, 1.0e5]:
        R = x*Rg_agn
        if R <= R_in_agn:
            continue
        P(f'  {x:>10.4g} {t_effective(Mdot_agn, M_AGN, R, R_in_agn):>12.4f} '
          f'{t_eff_index(Mdot_agn, M_AGN, R, R_in_agn):>15.5f}')
    P('')
    P('  The index tends to -3/4 outward and is NOT -3/4 near the inner')
    P('  edge, where the bracket [1 - sqrt(R_in/R)] still bites.  The')
    P('  temperature has a MAXIMUM at R = (49/36) R_in, which is a')
    P('  derived number and not a fitted one:')
    R_peak = (49.0/36.0)*R_in_agn
    P(f'    R_max = (49/36) R_in    = {R_peak/Rg_agn:.6f} R_g')
    P(f'    T_eff there             = '
      f'{t_effective(Mdot_agn, M_AGN, R_peak, R_in_agn):.4f} K')
    grid = np.linspace(1.0001*R_in_agn, 4.0*R_in_agn, 200001)
    num_peak = grid[np.argmax(t_effective(Mdot_agn, M_AGN, grid, R_in_agn))]
    P(f'    numerical maximum       = {num_peak/R_in_agn:.6f} R_in '
      f'against 49/36 = {49.0/36.0:.6f}')

    # ---------------------------------------------------------------- G
    P('')
    P('PART G.  CHECK 3.  The radiative efficiency, and Module 9\'s 0.1')
    P('-'*74)
    eta_newt = efficiency_newtonian(ISCO_SCHWARZSCHILD_RG)
    P(f'  Newtonian thin disc at R_in = 6 R_g:')
    P(f'    eta = R_g/(2 R_in) = 1/12 = {eta_newt:.6f}   DERIVED HERE')
    P(f'  Relativistic Schwarzschild:')
    P(f'    eta = 1 - sqrt(8/9)       = {ETA_SCHWARZSCHILD:.6f}'
      f'   NOT YET VERIFIED')
    P(f'  Soltan argument, Yu & Tremaine (2002):')
    P(f'    eta (population mean)     = {YT02_EFFICIENCY:.6f}'
      f'   NOT YET VERIFIED')
    P(f'  module09.html:757, asserted in a SHIPPED page:')
    P(f'    eta_rad ~ {M09_ASSERTED_ETA}')
    P('')
    P('  PUNCHLINE CHECK 3.')
    P(f'    0.1 / (1/12)              = {M09_ASSERTED_ETA/eta_newt:.4f}')
    P(f'    0.1 / (1 - sqrt(8/9))     = '
      f'{M09_ASSERTED_ETA/ETA_SCHWARZSCHILD:.4f}')
    P('    The round 0.1 lies ABOVE both zero-spin values.  It is not a')
    P('    thin-disc number at a Schwarzschild ISCO; it is a number that')
    P('    requires the hole to spin, or the population to contain')
    P('    spinning holes.  A NON-ROTATING hole gives 0.057 and a')
    P('    maximally rotating one gives about 0.4.')
    P('')
    P('  WHAT THIS DOES TO MODULE 9, WHICH IS GATE D QUESTION 1.')
    P('    module09.html:757 divides 0.1 by its measured eta and prints')
    P('    a factor of 2e7 to one significant figure.  BOTH DERIVED')
    P('    VALUES ARE SMALLER THAN 0.1, so both make that factor')
    P('    SMALLER.  The direction matters and the ratios are:')
    P(f'      with 1/12         factor x {eta_newt/M09_ASSERTED_ETA:.4f}'
      f'  (down {1.0 - eta_newt/M09_ASSERTED_ETA:.1%})')
    P(f'      with 1-sqrt(8/9)  factor x '
      f'{ETA_SCHWARZSCHILD/M09_ASSERTED_ETA:.4f}'
      f'  (down {1.0 - ETA_SCHWARZSCHILD/M09_ASSERTED_ETA:.1%})')
    P('    Neither moves it off 10^7, so no shipped sentence becomes')
    P('    false -- but the module may not assert that without the')
    P('    number.  STEP 2 MUST RUN m09_numbers.py and read its printed')
    P('    eta, because the exact factor is computed there and this file')
    P('    may not retype it.  A number typed into a record passes no')
    P('    check.')

    # ---------------------------------------------------------------- H
    P('')
    P('PART H.  Self-gravity: the Toomre criterion')
    P('-'*74)
    P('  module05.html:764 printed "Omits the stabilisation of long')
    P('  wavelengths by rotation in a disc" and sent it here.  Module 5')
    P('  built the Jeans criterion without rotation; this is the same')
    P('  competition with rotation added.')
    P('')
    P('  For a steady alpha-disc the closed form of PART H gives')
    P('    Q = 3 alpha c_T^3/(G Mdot [1 - sqrt(R_in/R)]),')
    P('  in which Omega and R have both CANCELLED.  Q depends on the')
    P('  local temperature and on two global numbers, and on nothing')
    P('  else.')
    P('')
    P(f'  {"R/R_g":>10} {"T_eff (K)":>12} {"Sigma (g/cm^2)":>16} {"Q":>12}')
    alpha_agn = 0.1
    for x in [1.0e2, 1.0e3, 1.0e4, 1.0e5]:
        R = x*Rg_agn
        T = t_effective(Mdot_agn, M_AGN, R, R_in_agn)
        cT = isothermal_sound_speed(T, MU_IONISED_H)
        Om = kepler_omega(M_AGN, R)
        H = cT/Om
        nu = alpha_viscosity(alpha_agn, cT, H)
        Sig = nu_sigma_steady(Mdot_agn, R, R_in_agn)/nu
        Q = toomre_q_steady(alpha_agn, cT, Mdot_agn, R, R_in_agn)
        P(f'  {x:>10.4g} {T:>12.4f} {Sig:>16.4e} {Q:>12.4e}')
    P('')
    xs = np.logspace(2.0, 5.0, 300001)
    Rs = xs*Rg_agn
    Ts = t_effective(Mdot_agn, M_AGN, Rs, R_in_agn)
    Qs = toomre_q_steady(alpha_agn, isothermal_sound_speed(Ts, MU_IONISED_H),
                         Mdot_agn, Rs, R_in_agn)
    j = int(np.argmin(np.abs(np.log(Qs))))
    x_sg, R_sg = xs[j], Rs[j]
    P('')
    P(f'  Q = 1 at R = {x_sg:.1f} R_g = {R_sg:.4e} cm = '
      f'{R_sg/pc:.3e} pc')
    P(f'    Q there = {Qs[j]:.6f}, found on a 3e5-point log grid.')
    P('')
    P('  Q FALLS OUTWARD AND PASSES THROUGH 1.  Beyond that radius the')
    P('  disc is unstable to its own gravity and the thin steady solution')
    P('  of PART F does not describe it.')
    P('  THE MIDPLANE TEMPERATURE IS NOT T_eff.  An optically thick disc')
    P('  has T_mid^4 = (3 tau/4) T_eff^4 with tau = kappa Sigma/2, so the')
    P('  true c_T is LARGER and the true Q is LARGER, and the radius at')
    P('  which Q = 1 moves OUTWARD.  Using T_eff therefore gives a LOWER')
    P('  BOUND on that radius, and the module must print it as a bound.')
    P('  [NUMBER NOT YET COMPUTED: the optically thick correction.  Gate')
    P('  D decides whether this module carries it or states the bound.]')
    P('')
    P('  The protoplanetary row, where self-gravity is the physics of a')
    P('  real object rather than a caveat:')
    tt_row = census['protoplanetary, 10 au']
    kap_tt = epicyclic_frequency(tt_row['Om'], KEPLER_Q)
    Q_tt = toomre_q(tt_row['cT'], kap_tt, tt_row['Sigma'])
    q_tt_stellar = toomre_q(tt_row['cT'], kap_tt, tt_row['Sigma'],
                            TOOMRE_STELLAR_COEFF)
    P(f'    Q (gas, coefficient pi) = {Q_tt:.4f}')
    P(f'    Q (stellar, 3.36)       = '
      f'{q_tt_stellar:.4f}')
    P('    The two coefficients differ by 7 per cent and the module must')
    P('    not average them; the gas value is the one that applies.')
    Sigma_crit = tt_row['cT']*kap_tt/(TOOMRE_GAS_COEFF*G)
    P(f'    Sigma at which Q = 1    = {Sigma_crit:.4f} g cm^-2')
    P(f'    against the row\'s       = {tt_row["Sigma"]:.4f} g cm^-2')

    # ---------------------------------------------------------------- I
    P('')
    P('PART I.  Centrifugal support, and where gas circularises')
    P('-'*74)
    P('  module03.html:792 printed "Excludes centrifugal flattening and')
    P('  the rotational support of discs" and sent it here.')
    P(f'    Omega^2 R^3/(G M) for a Keplerian disc = '
      f'{centrifugal_flattening(Om_dn, M_WD, R_DN):.12f}')
    P('    EXACTLY ONE, at every radius, by construction.  A disc is not')
    P('    partly rotationally supported; radially it is supported by')
    P('    rotation and by nothing else.  Module 3\'s hydrostatic star has')
    P('    this ratio near zero, and that single number is the whole')
    P('    difference between the two objects.')
    P('')
    P('  module09.html:832 printed that Sgr A*\'s gas circularises near')
    P('  100 r_S.  As a number:')
    M_SGRA = 4.3e6*Msun         # NOT YET VERIFIED: Module 9 owns this mass
    r_S = 2.0*gravitational_radius(M_SGRA)
    R_circ = 100.0*r_S
    ell_needed = np.sqrt(G*M_SGRA*R_circ)
    P(f'    M (Module 9\'s value)    = {M_SGRA/Msun:.3e} M_sun'
      f'   NOT YET VERIFIED')
    P(f'    r_S = 2 G M/c^2         = {r_S:.4e} cm')
    P(f'    R_circ = 100 r_S        = {R_circ:.4e} cm')
    P(f'    ell required            = {ell_needed:.4e} cm^2 s^-1')
    P(f'    back through R = ell^2/GM = '
      f'{circularisation_radius(M_SGRA, ell_needed)/r_S:.6f} r_S')
    P('    STEP 2 MUST READ MODULE 9\'S MASS off module09.html rather than')
    P('    retyping 4.3e6 here.  Grep the other file before citing it.')

    # ---------------------------------------------------------------- J
    P('')
    P('PART J.  What supplies the stress: the link to Module 12 SS9')
    P('-'*74)
    P('  THE MRI IS NOT RE-DERIVED HERE.  module08.html:728 lists it')
    P('  among what Module 12 builds and module12.html:698 builds it.')
    P('  What this module owes Module 12 is the q that section assumed,')
    P('  and PART B has now supplied it.')
    P('')
    P(f'    gamma_max = (q/2) Omega, q from PART B = '
      f'{mri_growth_rate(Om_dn, q)/Om_dn:.10f} Omega')
    P(f'    Module 12 SS9\'s assumed value          = '
      f'{MRI_GROWTH_FACTOR:.10f} Omega')
    P(f'    difference                             = '
      f'{abs(mri_growth_rate(Om_dn, q)/Om_dn - MRI_GROWTH_FACTOR):.2e}')
    P('')
    P('  DOES THE UNSTABLE WAVELENGTH FIT INSIDE THE DISC?  The MRI needs')
    P('  lambda_max < 2H or the mode has nowhere to grow.  The field that')
    P('  supplies a given alpha is B ~ sqrt(4 pi alpha rho c_T^2), an')
    P('  ORDER-OF-MAGNITUDE identification and not a result.')
    P('')
    P('  THE CENSUS CANNOT ANSWER THIS, AND THE FIRST DRAFT PRETENDED IT')
    P('  COULD.  Every disc property cancels:')
    P('    lambda_max/(2H) = 4 pi sqrt(alpha)/sqrt(15),  a pure number.')
    for name in census:
        row = census[name]
        B = field_for_alpha(0.1, row['rho0'], row['cT'])
        vA = alfven_speed(B, row['rho0'])
        lam_mri = mri_wavelength_max(vA, row['Om'])
        P(f'    {name:<24} B = {B:.4e} G  ratio = '
          f'{lam_mri/(2.0*row["H"]):.6f}')
    P(f'    the identity                                  ratio = '
      f'{mri_containment_ratio(0.1):.6f}')
    _ns = [census[k]['n0'] for k in census]
    P(f'    Two discs {np.log10(max(_ns)/min(_ns)):.2f} decades apart in '
      f'midplane density give the')
    P('    SAME ratio to six figures.  That is the identity and not a')
    P('    coincidence, and a table of it would be decoration.')
    P('')
    P('  WHAT THE IDENTITY DOES SAY IS A BOUND.')
    a_max = alpha_max_for_containment()
    P(f'    lambda_max < 2H  requires  alpha < 15/(16 pi^2) = '
      f'{a_max:.6f}')
    P(f'    CHECK 2 inferred alpha      = {alpha_inferred:.4f}, which is '
      f'{alpha_inferred/a_max:.2f} times the bound.')
    P(f'    King, Pringle & Livio range {KPL07_ALPHA_LO}-'
      f'{KPL07_ALPHA_HI} lies ENTIRELY ABOVE it,')
    P(f'    by factors {KPL07_ALPHA_LO/a_max:.2f} to '
      f'{KPL07_ALPHA_HI/a_max:.2f}.')
    P('    So the equipartition identification B^2 ~ 4 pi alpha P is')
    P('    marginal exactly where the measured alpha lives.  THIS IS NOT')
    P('    A REFUTATION OF ANYTHING: it says the crude identification is')
    P('    at its limit, which is what an order-of-magnitude argument is')
    P('    entitled to be.  Gate D decides whether the module prints it.')

    # ---------------------------------------------------------------- K
    P('')
    P('PART K.  CHECK 4.  alpha is not a constant of nature')
    P('-'*74)
    P('  King, Pringle & Livio titled their paper with this question.')
    P(f'    dwarf novae, outburst     = {KPL07_ALPHA_LO}-{KPL07_ALPHA_HI}'
      f'   NOT YET VERIFIED')
    P(f'    dwarf novae, quiescent    = {KPL07_ALPHA_QUIESCENT}'
      f'   NOT YET VERIFIED')
    P(f'    protoplanetary, bound     < {FLAHERTY18_ALPHA_MAX}'
      f'   NOT YET VERIFIED')
    P('')
    P('  PUNCHLINE CHECK 4, AND THE VERDICT IS NOT FIXED AT STEP 1.')
    lo = np.log10(KPL07_ALPHA_LO/FLAHERTY18_ALPHA_MAX)
    hi = np.log10(KPL07_ALPHA_HI/FLAHERTY18_ALPHA_MAX)
    P(f'    The dwarf-nova range exceeds the protoplanetary BOUND by')
    P(f'    {lo:.2f} to {hi:.2f} decades.')
    P(f'    Within dwarf novae alone, outburst over quiescent = '
      f'{KPL07_ALPHA_LO/KPL07_ALPHA_QUIESCENT:.0f} to '
      f'{KPL07_ALPHA_HI/KPL07_ALPHA_QUIESCENT:.0f}.')
    P('    A BOUND HAS A DIRECTION, and this one points down: the')
    P('    protoplanetary number is an upper limit, so the true gap is at')
    P('    least this large and may be larger.  What is refuted is not')
    P('    the prescription -- nu = alpha c_T H remains a definition of')
    P('    alpha -- but the reading of alpha as a constant of nature.')
    P('    Shakura & Sunyaev never claimed it was one; alpha <= 1 is the')
    P('    only bound their argument gives.')

    # ---------------------------------------------------------------- L
    P('')
    P('PART L.  The nine problems')
    P('-'*74)
    P('  [NUMBER NOT YET COMPUTED: PART L is written at step 4, after')
    P('  Gate D fixes the nine problem slots and the modelling inputs')
    P('  each STATEMENT must carry.  Module 12 wrote its PART L at step 4')
    P('  for the same reason.]')

    P('')
    P('=' * 74)
    P('END OF STEP 1.  WHAT STEP 2 MUST DO, in one list:')
    P('  1. Shakura & Sunyaev (1973) -- the prescription and its bound.')
    P('  2. King, Pringle & Livio (2007) -- the alpha range and what')
    P('     observable it came from.  CHECK 2 and CHECK 4 both need it.')
    P('  3. Flaherty et al. (2018) -- the protoplanetary bound, and')
    P('     WHICH WAY IT POINTS.')
    P('  4. Yu & Tremaine (2002) -- value or lower bound?  CHECK 3\'s')
    P('     wording depends on the answer.')
    P('  5. Toomre (1964) -- the gas coefficient, pi or 3.36.')
    P('  6. A general-relativity page for 1 - sqrt(8/9) and for 6 R_g.')
    P('  7. The dwarf-nova parameters, from a NAMED SYSTEM if CHECK 2 is')
    P('     to be a measurement rather than a class average.')
    P('  8. RUN m09_numbers.py and read its printed eta_rad.  Do not')
    P('     retype 4e-9 or 2e7 from module09.html.')
    P('  9. Read Module 9\'s black-hole mass off module09.html.')
    P('=' * 74)


if __name__ == '__main__':
    main()
