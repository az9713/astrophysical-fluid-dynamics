"""Module 5 numbers: the Jeans instability, the Jeans swindle and its
repairs, and the Bonnor-Ebert sphere, checked against a published table of
Bonnor-Ebert fits to Bok globules.

Every physical number quoted in module05.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

WHAT IS CHECKED, AND WHAT IS NOT (revised 2026-09-17 after reading the
sources; see module05.html section 7).

  VALIDATION, NOT A CHECK.  Kandori et al. (2005), AJ 130, 2166, Table 4
             lists xi_max and a centre-to-edge contrast n_c/n_edge for
             fifteen rows.  Its footnote b says the contrast was
             "determined from xi_max value", so the column is the authors'
             own integration of the isothermal Lane-Emden equation.  PART F
             reproduces it to 2.2 per cent at worst.  That tests this
             script's integrator, not nature.

  CHECK 1    REFUTED: the reading of these fits as long-lived STABLE
             equilibria.  xi_crit = 6.4508 computed here; Kandori's own
             count (page 12) is three stable and eight unstable starless
             globules.  Barnard 68 sits 2.25 sigma above critical.  The
             stable-oscillation reading (Lada et al. 2003) needs an age
             above tau_dyn = 2R/V = 3e6 yr (Burkert & Alves 2009 page 1,
             who state it in order to argue against it), 17.6 times the
             free-fall time.

  ANCHOR     Barnard 68, where the two criteria this module derives give
             opposite verdicts from the same fitted numbers: M_J/M = 1.41
             (Jeans: stable) against xi_max = 6.9 +/- 0.2 above 6.4508
             (Bonnor-Ebert: unstable).  M_J/M is invariant under the T/d
             degeneracy of the fit (PART H prints both Table 5 rows).

  CHECK 2    REFUTED: the isothermal closure of the OUTER profile.
             Nielbock et al. (2012) measure n_H ~ r^-3.5 outside the inner
             plateau; no isothermal sphere is ever steeper than 2.5176
             (PART I).

The empirical content behind CHECK 1 is the one-parameter fit itself:
Alves, Lada & Lada (2001) fitted xi_max = 6.9 +/- 0.2 to the extinction
profile of Barnard 68.  That Nature paper is not on arXiv and was not read;
its goodness-of-fit statistic is not quoted.

The mass comparison of PART H is reported two ways, from P_ext and from R,
because the published row is not internally consistent to better than 13
per cent.  That spread is printed, not smoothed.

Sources for every published number compared against are listed in the
SOURCES block at the foot of this file and in module05.html.
"""
import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m01_numbers.py, m02_numbers.py and m03_numbers.py
# rather than imported, so that each module's numbers script reads on its own.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
mp = 1.67262192369e-24  # g
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
a_rad = 7.565733e-15    # erg cm^-3 K^-4 (radiation constant, 4 sigma_SB/c)
pc = 3.0856775814913673e18   # cm
kpc = 1e3*pc
Mpc = 1e6*pc
AU = 1.495978707e13     # cm
yr = 3.15576e7          # s
Myr = 1e6*yr

GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
Rsun = 6.957e10         # cm             (IAU 2015 nominal)
Lsun = 3.828e33         # erg/s          (IAU 2015 nominal)
Msun = GMsun/G          # g

# --- mean molecular weights, all per FREE PARTICLE ------------------------
# The factor of 1.2 between "per particle" and "per hydrogen molecule" is the
# commonest arithmetic trap in this subject, so both are written out.
#
# Cold molecular gas, hydrogen fully molecular, helium atomic, He/H = 0.1 by
# number.  Then n(He) = 0.2 n(H2), and per H2 molecule the mass is
# (2.016 + 0.2*4.003) m_u = 2.8 m_u while the particle count is 1.2.  Hence
#   mu = 2.8/1.2 = 2.33   and   rho = 2.8 m_u n(H2).
MU_MOL = 2.33           # per particle; Kandori et al. (2005) use this value
MASS_PER_H2 = 2.8       # in m_u; converts n(H2) to a mass density
# Warm neutral atomic gas, same helium abundance: mass per H atom
# (1.008 + 0.1*4.003) = 1.4 m_u over 1.1 particles.
MU_HI = 1.4/1.1         # = 1.2727
MASS_PER_H = 1.4        # in m_u
# Primordial neutral gas, X = 0.76, Y = 0.24 by mass, helium atomic:
# particles per unit mass are (X/1 + Y/4)/m_u = 0.82/m_u.
X_PRIM, Y_PRIM = 0.76, 0.24
MU_PRIM = 1.0/(X_PRIM + Y_PRIM/4.0)      # = 1.2195

# --- adiabatic index used where the perturbation is NOT isothermal --------
GAMMA_MONO = 5.0/3.0

# =========================================================================
# PUBLISHED VALUES COMPARED AGAINST.  Transcribed from the papers, with the
# page of the arXiv PDF from which each was read.
# =========================================================================

# Kandori et al. (2005), AJ 130, 2166, Table 4 (arXiv PDF page 27).
# Fifteen rows covering fourteen globules; the Coalsack appears twice, from
# two different papers.  Columns kept: name, theta_R in arcsec, xi_max,
# its 1 sigma, the published
# centre-to-edge density contrast, Kandori's own stability label, and
# whether the globule is starless.  A None error means the paper prints
# none for that entry.
KANDORI_T4 = [
    # name,          theta_R, xi_max, sigma, contrast, label,      starless
    ("CB 87",           87.5,   5.1,   0.4,     8.1,   "Stable",   True),
    ("CB 110",          61.1,  14.0,   3.0,    94.3,   "Unstable", True),
    ("CB 131",         103.0,  16.3,   5.1,   139.0,   "Unstable", True),
    ("CB 134",          59.6,  18.5,   4.9,   187.0,   "Unstable", True),
    ("CB 161",          62.5,   8.1,   1.4,    25.1,   "Unstable", True),
    ("CB 184",         112.0,   8.1,   1.6,    24.9,   "Unstable", True),
    ("CB 188",         127.0,  16.0,   2.9,   132.0,   "Unstable", False),
    ("FeSt 1-457",     144.0,  12.6,   2.0,    74.5,   "Unstable", True),
    ("Lynds 495",       75.0,   7.2,   1.4,    18.6,   "Unstable", True),
    ("Lynds 498",       75.0,   4.7,   0.4,     6.63,  "Stable",   True),
    ("Barnard 68",     100.0,   6.9,   0.2,    16.6,   "Unstable", True),
    ("Barnard 335",    125.0,  12.5,   2.6,    73.1,   "Unstable", False),
    ("Coalsack",       290.0,   5.8,  None,    10.9,   "Stable",   True),
    ("Coalsack (Racca+02)", 140.0, 7.0,  0.3,    17.2,  "Unstable", True),
    ("Lynds 694-2",     54.0,  25.0,   3.0,   364.0,   "Unstable", False),
]
# Kandori's own count, page 12 of the arXiv PDF, quoted verbatim in the
# docstring: "there are three stable starless globules and eight unstable
# starless globules."
# That count is over ELEVEN starless globules; his Table 4 has fifteen rows
# because CB 188, Barnard 335 and Lynds 694-2 are star-forming and the
# Coalsack appears twice, from two different papers.
KANDORI_STARLESS_STABLE = 3
KANDORI_STARLESS_UNSTABLE = 8

# Barnard 68's own Table 4 entries, named so the reporting code below can
# refer to them without indexing into the list.
B68_T4_XI = 6.9
B68_T4_SIG = 0.2
B68_T4_CONTRAST = 16.6

# Kandori et al. (2005), Table 5 (arXiv PDF page 28), row "Barnard 68".
# FIRST line, attributed there to reference (B) = Alves, Lada & Lada (2001):
B68_T_BE = 16.0            # K,        temperature the Bonnor-Ebert fit needs
B68_D = 125.0              # pc,       assumed distance
B68_R_AU = 1.25e4          # AU,       = theta_R * D = 100 arcsec * 125 pc
B68_M = 2.10               # Msun
B68_PEXT_K = 1.8e5         # K cm^-3,  P_ext/k
# SECOND line, attributed there to reference (G) = Hotzel, Harju & Juvela
# (2002a), A&A 395, L5, which is the same fit rescaled to the measured
# effective temperature.  Kandori's section 4.2.2 explains why only the
# product is determined: substituting R = theta_R d and rho_c ~ 1/d into the
# definition of xi_max gives d^-1 T = constant (he credits Lai et al. 2003).
B68_T_EFF = 10.0           # K
B68_T_EFF_ERR = 1.2        # K
B68_D_RESCALED = 85.0      # pc
B68_R_AU_RESCALED = 0.85e4  # AU
B68_M_RESCALED = 0.90      # Msun
B68_PEXT_K_RESCALED = 1.7e5  # K cm^-3

# Lada, Bergin, Alves & Huard (2003), ApJ 586, 286, arXiv:astro-ph/0211507.
# Abstract and page 1: measured gas kinetic temperature, and linewidths.
B68_T_GAS = 10.5           # K,   measured gas kinetic temperature
B68_DV_C18O = 0.18         # km/s, FWHM, +/- 0.01
B68_DV_C34S = 0.15         # km/s, FWHM, +/- 0.01
# Their conclusion, page 1: thermal pressure exceeds non-thermal pressure by
# a factor 4-5 in the central regions.
B68_PTH_OVER_PNT = (4.0, 5.0)

# Burkert & Alves (2009), ApJ 695, 1308, arXiv:0809.1457, page 1.
# Quoted there as properties of Barnard 68 from Alves et al. (2001b).
B68_RHOBAR_PUB = 1.5e-19   # g/cm^3, "the average mass density"
B68_TCOLL_PUB = 0.17e6*yr  # s,      (3 pi/(32 G rho))^(1/2)
B68_CS_PUB = 0.2e5         # cm/s,   "isothermal sound speed cs ~ 0.2 km/s"
B68_TDYN_PUB = 3.0e6*yr    # s,      2R/V oscillation timescale, V ~ 0.04 km/s

# Nielbock et al. (2012), A&A 547, A11, arXiv:1208.4512, abstract.
# Herschel dust temperature and density structure of the same cloud.
B68_TDUST_EDGE = 16.7      # K,  +1.3 -1.0
B68_TDUST_CENTRE = 8.2     # K,  +2.1 -0.7
B68_NH_CENTRE = 3.4e5      # cm^-3, total hydrogen nuclei, +0.9 -2.5
B68_OUTER_SLOPE = 3.5      # n_H ~ r^-3.5 outside the inner plateau
# Their ADOPTED profile, eq. (8) with the "best" row of Table 3 (PDF p10):
# n_H(r) = dn/[1 + (r/r0)^2]^(eta/2) + n_out, n0 = dn + n_out.
B68_N_R0 = 35.0            # arcsec
B68_N_ETA = 4.0
B68_N_N0 = 3.4e5           # cm^-3
B68_N_NOUT = 4.0e2         # cm^-3
B68_THETA_R = 100.0        # arcsec, outer radius of the Alves et al. BE fit
B68_D_NIELBOCK = 150.0     # pc, their assumed distance -- NOT 125 pc
B68_M_NIELBOCK = 3.1       # Msun, of material with A_K > 0.2 mag, at 150 pc

# Planck Collaboration (Aghanim et al. 2020), A&A 641, A6,
# arXiv:1807.06209, Table 2, column TT,TE,EE+lowE+lensing (PDF page 15).
PLANCK_OMBH2 = 0.02237     # +/- 0.00015
PLANCK_H0 = 67.36          # km/s/Mpc, +/- 0.54
PLANCK_ZSTAR = 1089.92     # +/- 0.25


# =========================================================================
# PART A.  The linearised system and the dispersion relation
# =========================================================================

def sound_speed(T, mu):
    """Isothermal sound speed c_s = sqrt(kT/(mu m_u)), cm/s.

    Isothermal, not adiabatic, because every application below is a cold
    cloud whose cooling time is far shorter than its dynamical time, and
    because the Bonnor-Ebert sphere is defined isothermally.  The adiabatic
    speed is sqrt(gamma) times larger and is returned by sound_speed_ad.
    """
    return np.sqrt(kB*T/(mu*mu_u))


def sound_speed_ad(T, mu, gamma=GAMMA_MONO):
    """Adiabatic sound speed sqrt(gamma k T/(mu m_u)), cm/s."""
    return np.sqrt(gamma*kB*T/(mu*mu_u))


def omega2(k, cs, rho0):
    """The Jeans dispersion relation omega^2 = c_s^2 k^2 - 4 pi G rho_0.

    Linearise continuity, Euler and Poisson about a uniform static medium of
    density rho_0 and sound speed c_s, take perturbations proportional to
    exp(i(k.x - omega t)), and this is what falls out.  Note the form: a
    straight line in the (k^2, omega^2) plane, of slope c_s^2 and intercept
    -4 pi G rho_0.  Nothing else in this module is that simple.
    """
    return cs*cs*k*k - 4.0*np.pi*G*rho0


def k_jeans(cs, rho0):
    """The wavenumber at which omega^2 changes sign, sqrt(4 pi G rho_0)/c_s."""
    return np.sqrt(4.0*np.pi*G*rho0)/cs


def lambda_jeans(cs, rho0):
    """Jeans length lambda_J = 2 pi/k_J = c_s sqrt(pi/(G rho_0)), cm."""
    return cs*np.sqrt(np.pi/(G*rho0))


def mass_jeans(cs, rho0):
    """Jeans mass, the mass of a sphere of DIAMETER lambda_J.

    M_J = (4 pi/3) rho_0 (lambda_J/2)^3.  This is the convention used
    throughout module05.html.  The other common convention, the mass of a
    CUBE of side lambda_J, is larger by 6/pi = 1.9099; it is returned by
    mass_jeans_cube so that the prose can name the factor rather than leave
    the reader to discover it in someone else's textbook.
    """
    lam = lambda_jeans(cs, rho0)
    return (4.0*np.pi/3.0)*rho0*(lam/2.0)**3


def mass_jeans_cube(cs, rho0):
    """Jeans mass in the cube convention, rho_0 lambda_J^3."""
    return rho0*lambda_jeans(cs, rho0)**3


def growth_rate(k, cs, rho0):
    """Growth rate s = sqrt(-omega^2) for unstable k, s^-1; 0 if stable."""
    w2 = omega2(k, cs, rho0)
    return np.sqrt(-w2) if w2 < 0.0 else 0.0


def t_grow(rho0):
    """Longest-wavelength growth time, 1/sqrt(4 pi G rho_0), s.

    The k -> 0 limit of 1/sqrt(-omega^2).  Pressure has been sent to zero,
    so this is the fastest the instability ever grows at fixed rho_0.
    """
    return 1.0/np.sqrt(4.0*np.pi*G*rho0)


def t_freefall(rho0):
    """Free-fall time of a uniform pressureless sphere, sqrt(3 pi/(32 G rho))."""
    return np.sqrt(3.0*np.pi/(32.0*G*rho0))


def tff_over_tgrow():
    """The exact ratio t_ff/t_grow = pi sqrt(3/8), a pure number.

    Both times scale as (G rho)^(-1/2), so the ratio is independent of
    everything.  It is 1.9238: the free-fall time is not the e-folding time,
    it is 1.92 e-foldings' worth of time.
    """
    return np.pi*np.sqrt(3.0/8.0)


def rho_from_nH2(nH2):
    """Mass density of molecular gas from the H2 number density, g/cm^3."""
    return MASS_PER_H2*mu_u*nH2


def rho_from_nH(nH):
    """Mass density of atomic gas from the hydrogen number density, g/cm^3."""
    return MASS_PER_H*mu_u*nH


# =========================================================================
# PART B.  The Jeans swindle, and two repairs that do not need a sphere
# =========================================================================

def swindle_residual(rho0, L):
    """How badly the uniform static background fails to be an equilibrium.

    Momentum balance in the unperturbed state needs grad P_0 = -rho_0 grad
    Phi_0.  With rho_0 and P_0 uniform the left side is zero, so grad Phi_0
    must vanish; but Poisson then gives 0 = laplacian Phi_0 = 4 pi G rho_0,
    which is false for rho_0 > 0.  There is no uniform static equilibrium.

    To put a number on it, integrate Poisson over a sphere of radius L in
    the uniform medium: the enclosed mass gives g(L) = (4/3) pi G rho_0 L,
    an acceleration that the swindle sets to zero.  Returned with the
    crossing time sqrt(L/g).  (The time to fall L from rest at constant g
    is sqrt(2 L/g), larger by sqrt(2); either is the same order.)
    """
    g = (4.0/3.0)*np.pi*G*rho0*L
    t = np.sqrt(L/g)
    return g, t


def sheet_scale_height(cs, rho0):
    """Scale height of the self-gravitating isothermal sheet, c_s/sqrt(8 pi G rho_0).

    REPAIR ONE.  In plane-parallel geometry an isothermal equilibrium DOES
    exist, so nothing has to be swindled away.  Writing u = ln(rho/rho_0),
    hydrostatic balance c_s^2 u' = -Phi' and Poisson Phi'' = 4 pi G rho give
        c_s^2 u'' = -4 pi G rho_0 e^u,
    solved by u = -2 ln cosh(z/(2H)), that is rho = rho_0 sech^2(z/(2H)),
    provided H = c_s/sqrt(8 pi G rho_0).  Verified numerically in PART F.
    """
    return cs/np.sqrt(8.0*np.pi*G*rho0)


def sheet_profile(z, rho0, H):
    """rho(z) = rho_0 sech^2(z/(2H)) for the isothermal sheet."""
    return rho0/np.cosh(z/(2.0*H))**2


def sheet_surface_density(rho0, H):
    """Surface density of the sheet, Sigma = 4 rho_0 H."""
    return 4.0*rho0*H


def sheet_omega2(k, cs, Sigma, kappa=0.0):
    """Thin-sheet dispersion relation, omega^2 = c_s^2 k^2 - 2 pi G Sigma |k| + kappa^2.

    The razor-thin limit of the sheet: the self-gravity term is linear in
    |k|, not constant, because a sheet of finite extent in z has no gravity
    at wavelengths much shorter than its own thickness.  kappa is the
    epicyclic frequency, zero for a non-rotating sheet; with kappa included
    this is the Toomre dispersion relation, and Module 12 uses it.
    """
    return cs*cs*k*k - 2.0*np.pi*G*Sigma*np.abs(k) + kappa*kappa


def sheet_lambda_crit(cs, Sigma):
    """Longest stable wavelength of a non-rotating thin sheet, c_s^2/(G Sigma).

    Setting omega^2 = 0 with kappa = 0 gives k_crit = 2 pi G Sigma/c_s^2,
    hence lambda_crit = 2 pi/k_crit = c_s^2/(G Sigma).  Wavelengths LONGER
    than this grow.
    """
    return cs*cs/(G*Sigma)


def sheet_fastest(cs, Sigma):
    """Fastest-growing mode of a non-rotating thin sheet.

    Minimising omega^2 over k gives k_m = pi G Sigma/c_s^2 = k_crit/2, so
    the fastest-growing wavelength is TWICE the critical one, and the growth
    rate there is s_max = pi G Sigma/c_s.  Returns (lambda_m, s_max).
    """
    k_m = np.pi*G*Sigma/(cs*cs)
    return 2.0*np.pi/k_m, np.pi*G*Sigma/cs


def toomre_Q(cs, kappa, Sigma):
    """Toomre Q = c_s kappa/(pi G Sigma) for a gaseous disc.

    The minimum of sheet_omega2 over k is non-negative exactly when
    kappa^2 c_s^2 >= (pi G Sigma)^2, i.e. Q >= 1.  Module 12 proves it; it
    is previewed here because it is the same dispersion relation with one
    extra term, and because it shows what stabilises a galactic disc that
    the Jeans analysis says must collapse.
    """
    return cs*kappa/(np.pi*G*Sigma)


def rho_crit_cosmo(H0_kms_Mpc):
    """Critical density 3 H0^2/(8 pi G) from H0 in km/s/Mpc, g/cm^3."""
    H0 = H0_kms_Mpc*1e5/Mpc
    return 3.0*H0*H0/(8.0*np.pi*G)


def rho_baryon_at_z(z, ombh2=PLANCK_OMBH2, H0=PLANCK_H0):
    """Mean baryon density at redshift z, g/cm^3.

    REPAIR TWO.  The expanding background IS a solution of the equations:
    a homogeneous FRW universe solves continuity, Euler and Poisson
    together, with the expansion absorbing the gravity that the static
    swindle had to discard.  Perturbing about it gives

        delta'' + 2 (adot/a) delta' = (4 pi G rhobar - c_s^2 k^2/a^2) delta,

    the same sign structure as omega^2 = c_s^2 k^2 - 4 pi G rho_0, with the
    Hubble drag term 2 (adot/a) delta' added.  The drag turns the unstable
    branch from exponential growth into a power law: in an Einstein-de
    Sitter matter era the growing mode is delta proportional to a.

    Omega_b h^2 is the measured combination, so rho_b = Omega_b h^2 x
    (3 (100 km/s/Mpc)^2/(8 pi G)) x (1+z)^3 and H0 cancels out; H0 is kept
    in the signature only for the note printed in PART E.
    """
    H100 = 100.0*1e5/Mpc
    rho_b0 = ombh2*3.0*H100*H100/(8.0*np.pi*G)
    return rho_b0*(1.0 + z)**3


# =========================================================================
# PART C.  The isothermal Lane-Emden equation and the Bonnor-Ebert sphere
# =========================================================================

def isothermal_lane_emden(xi_max=200.0, h=1e-3, xi0=1e-5):
    """Integrate (1/xi^2) d/dxi (xi^2 dpsi/dxi) = e^(-psi), psi(0)=psi'(0)=0.

    Returns (xi, psi, dpsi) sampled on the integration grid.  This is the
    n -> infinity limit of the Lane-Emden equation of Module 3, written in
    the logarithmic variable psi = -ln(rho/rho_c), which is the form in
    which it stays finite: theta = rho/rho_c never reaches zero, so the
    polytropic variable has no surface and the sphere has no edge of its
    own.  That is precisely why an EXTERNAL pressure must bound it, and
    that is what makes the Bonnor-Ebert sphere a different object from a
    polytrope.

    Fourth-order Runge-Kutta, started from the series solution
        psi = xi^2/6 - xi^4/120 + ...
    at xi = xi0 rather than from the regular singular point at the origin.
    """
    def deriv(xi, y):
        psi, dpsi = y
        return np.array([dpsi, np.exp(-psi) - 2.0*dpsi/xi])

    xi = xi0
    psi = xi*xi/6.0 - xi**4/120.0
    dpsi = xi/3.0 - xi**3/30.0
    out = [(xi, psi, dpsi)]
    y = np.array([psi, dpsi])
    while xi < xi_max:
        # Fine step where every published xi_max lives (all are below 25)
        # and where the critical point and the slope maximum sit; coarse
        # step beyond 30, which is only used to display the oscillation of
        # the solution about the singular isothermal sphere.  Halving both
        # steps moves xi_crit by less than 1e-6 and m_crit by less than
        # 1e-7, which is checked in PART D.
        step = h if xi < 30.0 else 20.0*h
        k1 = deriv(xi, y)
        k2 = deriv(xi + step/2.0, y + step*k1/2.0)
        k3 = deriv(xi + step/2.0, y + step*k2/2.0)
        k4 = deriv(xi + step, y + step*k3)
        y = y + step*(k1 + 2.0*k2 + 2.0*k3 + k4)/6.0
        xi = xi + step
        out.append((xi, y[0], y[1]))
    a = np.array(out)
    return a[:, 0], a[:, 1], a[:, 2]


# One integration, cached, used by everything below.
_XI, _PSI, _DPSI = isothermal_lane_emden()


def be_state(xi_max):
    """(psi, dpsi) of the isothermal sphere at xi = xi_max, interpolated.

    Raises outside the integrated range: np.interp clamps silently at the
    ends, which would return a plausible-looking wrong number.
    """
    if not (_XI[0] <= xi_max <= _XI[-1]):
        raise ValueError(f'xi = {xi_max} outside the integrated range '
                         f'[{_XI[0]:.0e}, {_XI[-1]:.1f}]')
    psi = float(np.interp(xi_max, _XI, _PSI))
    dpsi = float(np.interp(xi_max, _XI, _DPSI))
    return psi, dpsi


def be_slope(xi_max):
    """Local logarithmic density slope -d ln rho/d ln r = xi psi'(xi).

    The same number as be_mu_R; named separately because the prose uses it
    in two different roles, as a profile slope and as a mass coefficient.
    """
    return be_mu_R(xi_max)


def be_max_slope():
    """The steepest local slope any Bonnor-Ebert sphere reaches, and where.

    The isothermal sphere does not approach the singular solution
    rho = c_s^2/(2 pi G r^2) monotonically: it OSCILLATES about it with
    decaying amplitude, so the local slope overshoots 2 before settling.
    The global maximum of xi psi'(xi) is therefore a real ceiling on how
    steep a Bonnor-Ebert profile can be anywhere, at any xi_max.
    """
    sel = _XI > 1.0
    s = _XI[sel]*_DPSI[sel]
    i = int(np.argmax(s))
    return float(_XI[sel][i]), float(s[i])


def be_contrast(xi_max):
    """Centre-to-edge density contrast rho_c/rho_R = exp(psi(xi_max)).

    An exact function of xi_max alone.  This is the quantity Kandori's
    Table 4 lists beside xi_max, and PART F checks every row.
    """
    return np.exp(be_state(xi_max)[0])


def be_xi_from_contrast(contrast):
    """Invert be_contrast: the xi_max that produces a given contrast."""
    return float(np.interp(np.log(contrast), _PSI, _XI))


def be_m(xi_max):
    """Dimensionless mass m = M G^(3/2) P_ext^(1/2)/c_s^4.

    With rho = rho_c e^(-psi), xi = r/alpha and alpha = c_s/sqrt(4 pi G rho_c),

        M(xi)     = 4 pi rho_c alpha^3 xi^2 psi'(xi)     [since (xi^2 psi')' = xi^2 e^-psi]
        P_ext(xi) = rho_c c_s^2 e^(-psi(xi))

    and eliminating rho_c between them leaves

        m(xi) = xi^2 psi'(xi) e^(-psi(xi)/2) / sqrt(4 pi),

    a pure number.  Its MAXIMUM over xi is the Bonnor-Ebert coefficient, and
    the maximum is what makes the criterion a mass criterion at all.
    """
    psi, dpsi = be_state(xi_max)
    return xi_max*xi_max*dpsi*np.exp(-psi/2.0)/np.sqrt(4.0*np.pi)


def be_mu_R(xi_max):
    """Dimensionless mass in the radius form, M = (c_s^2 R/G) xi psi'(xi).

    Since R = alpha xi and 4 pi rho_c alpha^2 = c_s^2/G, the same M(xi)
    above collapses to M = (c_s^2 R/G) xi psi'(xi).  This is the second,
    independent route to a mass used in PART G: it takes R and not P_ext.
    """
    return xi_max*be_state(xi_max)[1]


def be_r(xi_max):
    """Dimensionless radius r = R G^(1/2) P_ext^(1/2)/c_s^2 = xi e^(-psi/2)/sqrt(4 pi)."""
    return xi_max*np.exp(-be_state(xi_max)[0]/2.0)/np.sqrt(4.0*np.pi)


def nielbock_slope(theta):
    """-d ln n_H/d ln r of the Nielbock et al. (2012) eq. (8) fit, theta in arcsec."""
    x2 = (theta/B68_N_R0)**2
    core = (B68_N_N0 - B68_N_NOUT)/(1.0 + x2)**(B68_N_ETA/2.0)
    return B68_N_ETA*x2/(1.0 + x2)*core/(core + B68_N_NOUT)


def be_critical():
    """Locate the maximum of m(xi): (xi_crit, m_crit, contrast_crit).

    The maximum is found on the integration grid and then refined by fitting
    a parabola through the three samples bracketing it, which is exact for a
    smooth maximum to the order of the step size squared.
    """
    m = np.array([be_m(x) for x in _XI[(_XI > 3.0) & (_XI < 12.0)]])
    xs = _XI[(_XI > 3.0) & (_XI < 12.0)]
    i = int(np.argmax(m))
    x0, x1, x2 = xs[i-1], xs[i], xs[i+1]
    y0, y1, y2 = m[i-1], m[i], m[i+1]
    denom = (y0 - 2.0*y1 + y2)
    xc = x1 - 0.5*(x2 - x0)*0.5*(y2 - y0)/denom if denom != 0.0 else x1
    return xc, be_m(xc), be_contrast(xc)



def _refine_check(h=5e-4):
    """Re-integrate at half the step and re-locate the critical point.

    Returns (xi_crit, m_crit) from the finer grid, so PART D can print the
    shift rather than assert convergence.
    """
    xi, psi, dpsi = isothermal_lane_emden(xi_max=12.0, h=h)
    sel = (xi > 3.0) & (xi < 12.0)
    x, p, d = xi[sel], psi[sel], dpsi[sel]
    m = x*x*d*np.exp(-p/2.0)/np.sqrt(4.0*np.pi)
    i = int(np.argmax(m))
    x0, x1, x2 = x[i-1], x[i], x[i+1]
    y0, y1, y2 = m[i-1], m[i], m[i+1]
    denom = (y0 - 2.0*y1 + y2)
    xc = x1 - 0.25*(x2 - x0)*(y2 - y0)/denom if denom != 0.0 else x1
    pc = float(np.interp(xc, x, p))
    dc = float(np.interp(xc, x, d))
    return xc, xc*xc*dc*np.exp(-pc/2.0)/np.sqrt(4.0*np.pi)


def mass_bonnor_ebert(cs, P_ext, coeff=None):
    """Critical Bonnor-Ebert mass M_BE = m_crit c_s^4/(G^(3/2) P_ext^(1/2)).

    P_ext in dyn/cm^2.  coeff defaults to the computed m_crit, so the
    number 1.18 is never typed in as a constant anywhere in this file.
    """
    if coeff is None:
        coeff = be_critical()[1]
    return coeff*cs**4/(G**1.5*np.sqrt(P_ext))


def mass_be_at_xi_from_P(cs, P_ext, xi_max):
    """Mass of the Bonnor-Ebert sphere with this xi_max at this P_ext, g."""
    return be_m(xi_max)*cs**4/(G**1.5*np.sqrt(P_ext))


def mass_be_at_xi_from_R(cs, R, xi_max):
    """Mass of the Bonnor-Ebert sphere with this xi_max and this radius, g."""
    return be_mu_R(xi_max)*cs*cs*R/G


def be_central_density(cs, R, xi_max):
    """Central density implied by a radius and a xi_max, g/cm^3.

    From xi_max = R sqrt(4 pi G rho_c)/c_s.
    """
    return (xi_max*cs/R)**2/(4.0*np.pi*G)


# =========================================================================
# Reporting
# =========================================================================

def main():
    P = print
    P('=' * 74)
    P('MODULE 5 NUMBERS: the Jeans instability and the Bonnor-Ebert sphere')
    P('=' * 74)

    xi_crit, m_crit, contrast_crit = be_critical()

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  The dispersion relation and the two timescales')
    P('-'*74)
    P('  omega^2 = c_s^2 k^2 - 4 pi G rho_0    (linearised about uniform,')
    P('  static, self-gravitating medium; see the swindle note in PART C)')
    P(f'  exact ratio t_ff/t_grow = pi sqrt(3/8) = {tff_over_tgrow():.4f}')
    P('  READ: the free-fall time is NOT the e-folding time.  A pressureless')
    P(f'  sphere collapses in {tff_over_tgrow():.2f} e-folding times of the k -> 0 mode.')
    P('  The two agree to a factor of two and differ by exactly that factor,')
    P('  which is why the literature uses them interchangeably and why this')
    P('  module does not.')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  Jeans length and Jeans mass across three regimes')
    P('-'*74)
    P(f'  mean molecular weights per particle: molecular {MU_MOL}, '
      f'atomic {MU_HI:.4f}, primordial {MU_PRIM:.4f}')
    P(f'  conversions: rho = {MASS_PER_H2} m_u n(H2) for molecular gas, '
      f'rho = {MASS_PER_H} m_u n(H) for atomic gas')
    P(f'  the ratio of the two conventions is {MASS_PER_H2/MU_MOL:.4f}, the 1.2 '
      f'particles per H2 molecule')
    P('  (one H2 plus 0.2 He); it is exactly 1.2 if mu is written as 7/3')
    P('  rather than the rounded 2.33 that Kandori et al. (2005) use.')
    P('')

    regimes = []

    # 1. cold molecular cloud core
    T1, n1 = 10.0, 1.0e4
    rho1 = rho_from_nH2(n1)
    cs1 = sound_speed(T1, MU_MOL)
    regimes.append(("molecular cloud core", T1, MU_MOL, rho1, cs1,
                    f"n(H2) = {n1:.0e} cm^-3"))
    # 2. warm neutral ISM
    T2, n2 = 8000.0, 0.5
    rho2 = rho_from_nH(n2)
    cs2 = sound_speed(T2, MU_HI)
    regimes.append(("warm neutral ISM", T2, MU_HI, rho2, cs2,
                    f"n(H) = {n2} cm^-3"))
    # 3. primordial gas at recombination
    T3 = 3000.0
    rho3 = rho_baryon_at_z(PLANCK_ZSTAR)
    cs3 = sound_speed(T3, MU_PRIM)
    regimes.append(("primordial gas at recombination", T3, MU_PRIM, rho3, cs3,
                    f"z = {PLANCK_ZSTAR}, Planck 2018 Omega_b h^2"))

    for name, T, mu, rho, cs, note in regimes:
        lam = lambda_jeans(cs, rho)
        MJ = mass_jeans(cs, rho)
        tg = t_grow(rho)
        tf = t_freefall(rho)
        P(f'  {name}  ({note})')
        P(f'    T = {T:g} K, mu = {mu:.4f}, rho = {rho:.4e} g/cm^3')
        P(f'    c_s (isothermal)                 = {cs/1e5:.4f} km/s')
        P(f'    c_s (adiabatic, gamma = 5/3)     = '
          f'{sound_speed_ad(T, mu)/1e5:.4f} km/s')
        if lam > 0.5*pc:
            P(f'    lambda_J                         = {lam/pc:.4f} pc')
        else:
            P(f'    lambda_J                         = {lam/AU:.1f} AU '
              f'= {lam/pc:.5f} pc')
        P(f'    M_J (sphere of diameter lambda_J) = {MJ/Msun:.4e} Msun')
        P(f'    M_J (cube of side lambda_J)       = '
          f'{mass_jeans_cube(cs, rho)/Msun:.4e} Msun  '
          f'(ratio {mass_jeans_cube(cs, rho)/MJ:.4f} = 6/pi)')
        P(f'    growth time 1/sqrt(4 pi G rho)    = {tg/yr:.4e} yr')
        P(f'    free-fall time                    = {tf/yr:.4e} yr')
        P('')
    P('  READ, the three in one place:')
    for name, T, mu, rho, cs, note in regimes:
        P(f'    {name:<34} rho = {rho:.3e} g/cm^3   '
          f'M_J = {mass_jeans(cs, rho)/Msun:.3g} Msun')
    P('  The warm neutral medium cannot make anything smaller than a giant')
    P('  molecular cloud; the recombination-era value is the classic')
    P('  globular-cluster scale.  A star is nowhere on this list, which is')
    P('  the first sign that a uniform-density criterion is the wrong tool.')

    # ---------------------------------------------------------------- C
    P('')
    P('PART C.  The Jeans swindle, stated openly')
    P('-'*74)
    P('  The unperturbed state assumed in PART A is NOT a solution of the')
    P('  equations.  grad P_0 = 0 forces grad Phi_0 = 0, and Poisson then')
    P('  demands 4 pi G rho_0 = 0.  Jeans discarded the background potential')
    P('  and kept only its perturbation.  That is the swindle.')
    g1, ts1 = swindle_residual(rho1, lambda_jeans(cs1, rho1))
    P(f'  Size of what is discarded, for the 10 K core at one Jeans length:')
    P(f'    g = (4/3) pi G rho_0 L            = {g1:.4e} cm/s^2')
    P(f'    crossing time sqrt(L/g)           = {ts1/yr:.4e} yr')
    P(f'    Jeans growth time at the same rho = {t_grow(rho1)/yr:.4e} yr')
    P(f'    ratio                             = {ts1/t_grow(rho1):.4f}')
    P(f'    that ratio is exactly sqrt(3) = {np.sqrt(3.0):.4f}, independent of')
    P('    density, temperature and of the length L chosen')
    P('  READ: the neglected background acceleration acts on the SAME')
    P('  timescale as the instability it is used to derive.  It is not a')
    P('  small correction.  This is why the rest of the module works only')
    P('  with backgrounds that really are equilibria.')

    P('')
    P('  REPAIR ONE: the self-gravitating isothermal sheet.')
    H1 = sheet_scale_height(cs1, rho1)
    Sig1 = sheet_surface_density(rho1, H1)
    # numerical verification that sech^2 solves the equation
    z = np.linspace(-6.0*H1, 6.0*H1, 200001)
    rho_z = sheet_profile(z, rho1, H1)
    u = np.log(rho_z/rho1)
    upp = np.gradient(np.gradient(u, z), z)
    resid = cs1*cs1*upp + 4.0*np.pi*G*rho_z
    interior = np.abs(z) < 4.0*H1        # drop the finite-difference edges
    resid, scale = resid[interior], 4.0*np.pi*G*rho1
    P(f'    rho(z) = rho_0 sech^2(z/(2H)), H = c_s/sqrt(8 pi G rho_0)')
    P(f'    H for the 10 K core               = {H1/AU:.1f} AU '
      f'= {H1/pc:.5f} pc')
    P(f'    Sigma = 4 rho_0 H                 = {Sig1:.4e} g/cm^2 '
      f'= {Sig1/(Msun/pc**2):.1f} Msun/pc^2')
    P(f'    residual of c_s^2 u\'\' + 4 pi G rho, max/(4 pi G rho_0) '
      f'= {np.max(np.abs(resid))/scale:.3e}')
    lam_c = sheet_lambda_crit(cs1, Sig1)
    lam_m, s_max = sheet_fastest(cs1, Sig1)
    P(f'    lambda_crit = c_s^2/(G Sigma)     = {lam_c/pc:.5f} pc '
      f'= {lam_c/AU:.0f} AU')
    P(f'    fastest-growing lambda            = {lam_m/pc:.5f} pc '
      f'(exactly 2 lambda_crit, ratio {lam_m/lam_c:.4f})')
    P(f'    its growth time 1/s_max           = {1.0/s_max/yr:.4e} yr')
    P('    An equilibrium exists here, so nothing is swindled: the sheet is')
    P('    an exact static solution and its instability is an honest one.')

    P('')
    P('  REPAIR TWO: the expanding background.')
    P(f'    Planck 2018: Omega_b h^2 = {PLANCK_OMBH2}, '
      f'H0 = {PLANCK_H0} km/s/Mpc, z_* = {PLANCK_ZSTAR}')
    P(f'    rho_crit today                    = '
      f'{rho_crit_cosmo(PLANCK_H0):.4e} g/cm^3')
    P(f'    mean baryon density today         = '
      f'{rho_baryon_at_z(0.0):.4e} g/cm^3')
    P(f'    mean baryon density at z_*        = {rho3:.4e} g/cm^3 '
      f'(a factor {(1+PLANCK_ZSTAR)**3:.3e} larger)')
    P(f'    n(H) at z_* if X = {X_PRIM}          = '
      f'{X_PRIM*rho3/mu_u:.1f} cm^-3')
    P('    delta\'\' + 2 (adot/a) delta\' = (4 pi G rhobar - c_s^2 k^2/a^2) delta')
    P('    Same sign structure, one new term.  The Hubble drag converts')
    P('    exponential growth into the power law delta ~ a in matter')
    P('    domination, so the amplification from z_* to z = 0 is a factor')
    P(f'    of about {1.0+PLANCK_ZSTAR:.0f}, not e to some large power.  That is why')
    P('    structure formation needs dark matter perturbations that started')
    P('    growing before recombination.  Module 14 takes this up.')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  The Bonnor-Ebert sphere: numerics and validation')
    P('-'*74)
    # Validate the integrator against the series solution near the origin.
    for xt in (0.05, 0.1, 0.2):
        psi_n = float(np.interp(xt, _XI, _PSI))
        psi_s = xt**2/6.0 - xt**4/120.0 + xt**6/1890.0
        P(f'  series check at xi = {xt:.2f}: psi numeric = {psi_n:.9f}, '
          f'series = {psi_s:.9f}, ratio {psi_n/psi_s:.9f}')
    # Validate against the singular isothermal sphere, the xi -> infinity
    # limit.  The approach is OSCILLATORY, not monotonic, so what is checked
    # is that the oscillation about the singular solution decays, not that
    # the ratio marches to one.
    for xt in (10.0, 20.0, 30.0, 50.0, 100.0, 200.0):
        rho_ratio = np.exp(-be_state(xt)[0])
        P(f'  SIS check at xi = {xt:5.0f}: rho/rho_c = {rho_ratio:.6e}, '
          f'asymptote 2/xi^2 = {2.0/xt**2:.6e}, '
          f'ratio {rho_ratio/(2.0/xt**2):.4f}')
    xs_max, sl_max = be_max_slope()
    P('  READ: the density oscillates about the singular isothermal sphere')
    P('  rho = c_s^2/(2 pi G r^2) with a decaying amplitude, and never')
    P('  reaches zero.  The sphere has no surface of its own.  It must be')
    P('  cut off by an external pressure, and that is the whole difference')
    P('  from the polytropes of Module 3.  Because the approach overshoots,')
    P(f'  the local slope xi psi-prime rises past 2 to a global maximum of')
    P(f'  {sl_max:.4f} at xi = {xs_max:.3f} before settling back.  PART I uses')
    P('  that ceiling.')
    P('')
    xi_c2, m_c2 = _refine_check()
    P(f'  step halved, xi_crit                = {xi_c2:.6f} '
      f'(shift {abs(xi_c2-xi_crit):.2e})')
    P(f'  step halved, m_crit                 = {m_c2:.6f} '
      f'(shift {abs(m_c2-m_crit):.2e})')
    P(f'  xi_crit (maximum of m(xi))          = {xi_crit:.6f}')
    P(f'    PUNCHLINE: xi_crit = {xi_crit:.4f}, rounded to 6.5 by Bonnor (1956),')
    P(f'    by Alves, Lada & Lada (2001) and by Kandori et al. (2005).')
    P(f'  m_crit = M_BE G^(3/2) P^(1/2)/c_s^4 = {m_crit:.6f}')
    P(f'    PUNCHLINE: the Bonnor-Ebert coefficient is {m_crit:.4f}, the 1.18 of')
    P(f'    M_BE = 1.18 c_s^4/(G^(3/2) P_ext^(1/2)).')
    P(f'  rho_c/rho_R at the critical point    = {contrast_crit:.4f}')
    P(f'    Kandori et al. (2005) page 10 give "14"; ratio '
      f'{contrast_crit/14.0:.4f}')
    P(f'  xi psi\'(xi) at the critical point    = '
      f'{be_mu_R(xi_crit):.6f}   (M = (c_s^2 R/G) xi psi\')')
    P('  Shape of m(xi) either side of the maximum, which is the whole')
    P('  reason a mass criterion cannot decide stability on its own:')
    for x in (4.0, 5.0, 6.0, xi_crit, 7.0, 8.0, 10.0, 15.0, 25.0):
        P(f'    xi = {x:7.4f}   m = {be_m(x):.5f}   '
          f'rho_c/rho_R = {be_contrast(x):9.3f}   '
          f'm/m_crit = {be_m(x)/m_crit:.5f}')
    P('  Two spheres, one on each branch, can carry the SAME mass at the')
    P('  same external pressure.  Mass alone never distinguishes them;')
    P('  the density contrast does, and the contrast is what is measured.')
    P('')
    P('  The static criterion at FIXED mass.  With m = M G^1.5 P^0.5/c_s^4 and')
    P('  r = R G^0.5 P^0.5/c_s^2 = xi e^(-psi/2)/sqrt(4 pi), at fixed M and c_s')
    P('  P ~ m(xi)^2 and R ~ r(xi)/m(xi).  Stable while dlnP/dlnR < 0:')
    for x in (0.5, 3.0, 6.0, 6.4, 6.5, 7.0, 10.0):
        h = 1e-3
        lp = lambda z: 2.0*np.log(be_m(z))
        lr = lambda z: np.log(be_r(z)/be_m(z))
        d = (lp(x+h) - lp(x-h))/(lr(x+h) - lr(x-h))
        dr = (lr(x+h) - lr(x-h))/(2*h)
        P(f'    xi = {x:5.2f}   dlnP/dlnR = {d:+10.4f}   dlnR/dxi = {dr:+.4f}')
    P(f'    r at the critical point = {be_r(xi_crit):.6f}')
    # Where the fixed-mass radius R ~ r/m has its first extremum, and the
    # sign of dlnP/dlnR on a fine grid up to there.
    lr_ = lambda z: np.log(be_r(z)/be_m(z))
    lp_ = lambda z: 2.0*np.log(be_m(z))
    grid = np.linspace(0.05, 12.0, 2400)
    dlr = np.array([(lr_(z+1e-4) - lr_(z-1e-4))/2e-4 for z in grid])
    j = int(np.argmax(dlr > 0.0))
    xi_R = grid[j-1] - dlr[j-1]*(grid[j]-grid[j-1])/(dlr[j]-dlr[j-1])
    sub = grid[grid < xi_R - 0.02]
    dd = np.array([(lp_(z+1e-4) - lp_(z-1e-4))/(lr_(z+1e-4) - lr_(z-1e-4))
                   for z in sub])
    flips = sub[1:][np.sign(dd[1:]) != np.sign(dd[:-1])]
    P(f'    first extremum of R at fixed M: xi_R = {xi_R:.4f} '
      f'(contrast {be_contrast(xi_R):.2f})')
    P(f'    on 0.05 < xi < xi_R, dlnP/dlnR changes sign only at '
      f'{", ".join(f"{f:.3f}" for f in flips)}')
    P(f'    dlnR/dxi at xi_crit = {(lr_(xi_crit+1e-4)-lr_(xi_crit-1e-4))/2e-4:+.5f}')
    P('  READ: dlnP/dlnR -> -3 (Boyle, P R^3 fixed) as xi -> 0, and changes')
    P('  sign exactly where m has its maximum, because dlnR/dxi stays')
    P('  negative through it.  The static criterion and the mass maximum')
    P('  are the same statement.')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  Barnard 68 as measured')
    P('-'*74)
    cs_b68 = sound_speed(B68_T_BE, MU_MOL)
    R_b68 = B68_R_AU*AU
    P_b68 = B68_PEXT_K*kB
    P(f'  Kandori et al. (2005) Table 5, row "Barnard 68", first line,')
    P(f'  attributed there to Alves, Lada & Lada (2001), Nature 409, 159:')
    P(f'    xi_max                            = {B68_T4_XI:.1f} '
      f'+/- {B68_T4_SIG:.1f}   (Table 4)')
    P(f'    rho_c/rho_R printed in Table 4    = {B68_T4_CONTRAST:.1f}')
    P(f'    T (needed by the fit)             = {B68_T_BE:.0f} K')
    P(f'    distance assumed                  = {B68_D:.0f} pc')
    P(f'    R = theta_R x D                   = {B68_R_AU:.3e} AU '
      f'= {R_b68/pc:.4f} pc')
    P(f'    M                                 = {B68_M:.2f} Msun')
    P(f'    P_ext/k                           = {B68_PEXT_K:.1e} K cm^-3 '
      f'-> P_ext = {P_b68:.4e} dyn/cm^2')
    P(f'    c_s at 16 K, mu = {MU_MOL}            = {cs_b68/1e5:.4f} km/s')
    rho_c_b68 = be_central_density(cs_b68, R_b68, B68_T4_XI)
    P(f'  Implied central density from R and xi_max:')
    P(f'    rho_c                             = {rho_c_b68:.4e} g/cm^3')
    P(f'    n(H2) = rho_c/(2.8 m_u)           = '
      f'{rho_c_b68/(MASS_PER_H2*mu_u):.3e} cm^-3')
    P(f'    n(H) equivalent, 2 n(H2)          = '
      f'{2.0*rho_c_b68/(MASS_PER_H2*mu_u):.3e} cm^-3')
    P(f'    Nielbock et al. (2012) measure n_H = {B68_NH_CENTRE:.1e} cm^-3 '
      f'at 150 pc; ratio {2.0*rho_c_b68/(MASS_PER_H2*mu_u)/B68_NH_CENTRE:.3f}')
    P('    NOT a like-for-like comparison: Nielbock assume 150 pc, this row')
    P('    assumes 125 pc, and rho_c scales as 1/d.  Reported as context.')
    rhobar_b68 = 3.0*B68_M*Msun/(4.0*np.pi*R_b68**3)
    P(f'  Mean density from the published M and R:')
    P(f'    rhobar = 3M/(4 pi R^3)            = {rhobar_b68:.4e} g/cm^3')
    P(f'    Burkert & Alves (2009) page 1 quote {B68_RHOBAR_PUB:.1e} g/cm^3; '
      f'ratio {rhobar_b68/B68_RHOBAR_PUB:.4f}')
    tf_b68 = t_freefall(rhobar_b68)
    P(f'    free-fall time at that density    = {tf_b68/yr:.4e} yr')
    P(f'    Burkert & Alves quote             = {B68_TCOLL_PUB/yr:.4e} yr; '
      f'ratio {tf_b68/B68_TCOLL_PUB:.4f}')
    P(f'    growth time 1/sqrt(4 pi G rhobar) = {t_grow(rhobar_b68)/yr:.4e} yr')
    P(f'    tau_dyn = 2R/V, V ~ 0.04 km/s     = {B68_TDYN_PUB/yr:.2e} yr '
      f'(Burkert & Alves 2009, page 1)')
    P('      the minimum age IF B68 is a stable oscillating cloud; Burkert &')
    P('      Alves state it to argue against that reading.')
    P(f'    tau_dyn / free-fall time          = {B68_TDYN_PUB/tf_b68:.1f}')
    P(f'  Measured gas temperature, Lada et al. (2003): {B68_T_GAS} K, from')
    P(f'    C18O FWHM {B68_DV_C18O} +/- 0.01 km/s and '
      f'C34S FWHM {B68_DV_C34S} +/- 0.01 km/s;')
    P(f'    thermal pressure exceeds non-thermal by a factor '
      f'{B68_PTH_OVER_PNT[0]:.0f}-{B68_PTH_OVER_PNT[1]:.0f}.')
    dv_th_c18o = np.sqrt(8.0*np.log(2.0)*kB*B68_T_GAS/(30.0*mu_u))/1e5
    dv_th_mean = np.sqrt(8.0*np.log(2.0)*kB*B68_T_GAS/(MU_MOL*mu_u))/1e5
    dv_nt = np.sqrt(max(B68_DV_C18O**2 - dv_th_c18o**2, 0.0))
    P(f'    Thermal FWHM of C18O (30 amu) at {B68_T_GAS} K = '
      f'{dv_th_c18o:.4f} km/s; measured {B68_DV_C18O}.')
    P(f'    Non-thermal part, in quadrature  = {dv_nt:.4f} km/s')
    P(f'    Thermal FWHM of the MEAN particle (2.33 amu) = '
      f'{dv_th_mean:.4f} km/s,')
    P(f'      which is {dv_th_mean/dv_nt:.2f} times that non-thermal width.')
    P('    READ: a non-thermal component IS present, but it is far below the')
    P('    mean-particle thermal width, so the support is thermal.  Lada et')
    P('    al. state the thermal to non-thermal PRESSURE ratio as 4-5 from')
    P('    their own analysis; that number is quoted, not re-derived.  The')
    P('    isothermal premise of the Bonnor-Ebert sphere is therefore not')
    P('    absurd; PART I says where it nevertheless breaks.')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  VALIDATION, not a check: the contrast column')
    P('-'*74)
    P('  Kandori et al. (2005) Table 4 lists xi_max and n_c/n_edge.  Its')
    P('  footnote b: the contrast was "determined from xi_max value".  So the')
    P('  column is their integration; this reproduces it:')
    P('')
    P(f'  {"globule":<20} {"xi_max":>7} {"published":>10} {"computed":>9} '
      f'{"ratio":>7} {"d(xi)":>7} {"fit 1sig":>9}')
    worst = 0.0
    worst_dxi = 0.0
    for name, th, xi, sig, contrast, label, starless in KANDORI_T4:
        cc = be_contrast(xi)
        ratio = cc/contrast
        worst = max(worst, abs(ratio - 1.0))
        # The sharp statement is not the contrast residual itself but the
        # shift in xi_max that would remove it.  Compare that shift with the
        # fit's own quoted 1 sigma, and with the 0.05 that Kandori's
        # one-decimal printing already allows.
        dxi = be_xi_from_contrast(contrast) - xi
        worst_dxi = max(worst_dxi, abs(dxi))
        sigs = f'{sig:.1f}' if sig is not None else '  -'
        P(f'  {name:<20} {xi:>7.1f} {contrast:>10.2f} {cc:>9.2f} '
          f'{ratio:>7.4f} {dxi:>+7.3f} {sigs:>9}')
    P('')
    P(f'  PUNCHLINE: {len(KANDORI_T4)} published (xi_max, contrast) pairs, '
      f'contrasts spanning')
    P(f'  {min(r[4] for r in KANDORI_T4):.2f} to '
      f'{max(r[4] for r in KANDORI_T4):.1f}, a factor '
      f'{max(r[4] for r in KANDORI_T4)/min(r[4] for r in KANDORI_T4):.0f}. '
      f'Largest residual {worst*100:.1f} per cent;')
    P(f'  and the largest shift in xi_max that would remove any residual is')
    P(f'  {worst_dxi:.3f}, against fit errors quoted between 0.2 and 5.1 and against')
    P('  the 0.05 that Kandori\'s one-decimal printing allows (exceeded by')
    P('  CB 110 and CB 161).')
    P('  WHAT THIS TESTS: this integrator against Kandori\'s.  NOT nature.')
    P(f'  Barnard 68 fit precision: +/- {B68_T4_SIG} on {B68_T4_XI}, '
      f'{B68_T4_SIG/B68_T4_XI*100:.1f} per cent.')

    # ---------------------------------------------------------------- G
    P('')
    P('PART G.  CHECK 1 (REFUTED): these are not stable equilibria')
    P('-'*74)
    P(f'  {"globule":<18} {"xi_max":>12} {"(xi-xi_c)/sig":>14} '
      f'{"Kandori":>10} {"starless":>9}')
    nun = 0
    for name, th, xi, sig, contrast, label, starless in KANDORI_T4:
        if sig is None:
            s = '     -'
        else:
            s = f'{(xi - xi_crit)/sig:6.2f}'
        if xi > xi_crit:
            nun += 1
        xs = f'{xi:.1f}' + (f' +/- {sig}' if sig is not None else '')
        P(f'  {name:<18} {xs:>12} {s:>14} {label:>10} '
          f'{"yes" if starless else "no":>9}')
    P('')
    P(f'  {nun} of {len(KANDORI_T4)} rows sit above xi_crit = {xi_crit:.4f}.')
    P(f'  Kandori\'s own count over the eleven STARLESS globules, page 12,')
    P(f'  verbatim: "there are three stable starless globules and eight')
    P(f'  unstable starless globules."  {KANDORI_STARLESS_STABLE} stable, '
      f'{KANDORI_STARLESS_UNSTABLE} unstable.')
    sig_b68 = (B68_T4_XI - xi_crit)/B68_T4_SIG
    sig_l694 = (25.0 - xi_crit)/3.0
    P(f'  PUNCHLINE: Barnard 68 is {sig_b68:.2f} sigma above critical '
      f'({B68_T4_XI} +/- {B68_T4_SIG} against {xi_crit:.4f});')
    P(f'  Lynds 694-2 is {sig_l694:.2f} sigma above (25 +/- 3).  The only')
    P('  rate an isothermal sphere carries is sqrt(G rho_c) times a function')
    P('  of xi, so an unstable one departs on the free-fall scale, for')
    P(f'  Barnard 68 {tf_b68/1e5/yr:.2f}e5 yr.  A stable oscillating B68 would '
      f'be older than {B68_TDYN_PUB/yr:.1e} yr.')
    P('  REFUTED: the reading of the fit as a long-lived static object.')
    P('  NOT refuted: hydrostatic equilibrium, the isothermal closure or the')
    P('  fit itself, all three of which are the instrument doing the')
    P('  measuring.  Kandori\'s own resolution, page 17: a sphere collapsing')
    P('  from a nearly critical state has column-density profiles that mimic')
    P('  static unstable Bonnor-Ebert spheres "for a long time", so the')
    P('  population may be collapsing rather than sitting.')

    # ---------------------------------------------------------------- H
    P('')
    P('PART H.  THE ANCHOR: two criteria, opposite verdicts, one cloud')
    P('-'*74)
    MJ_b68 = mass_jeans(cs_b68, rhobar_b68)
    lam_b68 = lambda_jeans(cs_b68, rhobar_b68)
    P('  The naive Jeans criterion, applied to Barnard 68 at its own mean')
    P('  density and at the temperature its own fit requires:')
    P(f'    rhobar                            = {rhobar_b68:.4e} g/cm^3')
    P(f'    c_s at {B68_T_BE:.0f} K                        = '
      f'{cs_b68/1e5:.4f} km/s')
    P(f'    lambda_J                          = {lam_b68/AU:.0f} AU '
      f'= {lam_b68/pc:.4f} pc')
    P(f'    core diameter 2R                  = {2.0*B68_R_AU:.0f} AU '
      f'= {2.0*R_b68/pc:.4f} pc')
    P(f'    lambda_J / 2R                     = {lam_b68/(2.0*R_b68):.4f}')
    P(f'    M_J                               = {MJ_b68/Msun:.4f} Msun')
    P(f'    measured M                        = {B68_M:.2f} Msun')
    P(f'    PUNCHLINE M_J/M                   = {MJ_b68/(B68_M*Msun):.4f}')
    P('    VERDICT of the Jeans criterion: M < M_J, therefore STABLE.')
    # The fit fixes only T/d (PART I).  M ~ T d, rho ~ M/R^3 ~ T/d^2, and
    # M_J ~ T^(3/2) rho^(-1/2) ~ T d, so M_J/M is invariant along that line.
    R2 = B68_R_AU_RESCALED*AU
    rho_rs = 3.0*B68_M_RESCALED*Msun/(4.0*np.pi*R2**3)
    MJ2 = mass_jeans(sound_speed(B68_T_EFF, MU_MOL), rho_rs)
    P('    Same verdict on the rescaled row of Table 5 (10 K, 85 pc, 0.90 Msun):')
    P(f'    rhobar = {rho_rs:.4e} g/cm^3, M_J = {MJ2/Msun:.4f} Msun, '
      f'M_J/M = {MJ2/(B68_M_RESCALED*Msun):.4f}')
    P('    M_J/M ~ (T d)/(T d) is invariant under the T/d degeneracy; the two')
    P(f'    rows agree to {MJ2/(B68_M_RESCALED*Msun)/(MJ_b68/(B68_M*Msun)):.4f}, '
      'the rounding of the table.')
    MJ3 = mass_jeans(sound_speed(B68_T_GAS, MU_MOL), rhobar_b68)
    P(f'    Mixing rows (10.5 K gas at the 125 pc density) gives M_J/M = '
      f'{MJ3/(B68_M*Msun):.4f};')
    P('    that pair is not a solution of the fit, so it is not a verdict.')
    P('')
    P('  The Bonnor-Ebert criterion, on the same cloud, same numbers:')
    P(f'    xi_max measured                   = {B68_T4_XI} '
      f'+/- {B68_T4_SIG}')
    P(f'    xi_crit computed                  = {xi_crit:.4f}')
    P(f'    PUNCHLINE departure               = {sig_b68:.2f} sigma ABOVE '
      f'critical')
    P('    VERDICT of the Bonnor-Ebert criterion: UNSTABLE.')
    P('')
    P('  The two criteria disagree in SIGN on the best-observed dense core')
    P('  in the sky.  They disagree because the Jeans criterion asks whether')
    P('  a uniform medium of that mean density is unstable, and the core is')
    P(f'  not uniform: its centre-to-edge contrast is {B68_T4_CONTRAST}, and the')
    P('  contrast is exactly the quantity the stability boundary is stated')
    P('  in.  That is what the swindle cost.')
    P('')
    P('  Masses from the theory, both routes, against the published 2.10:')
    M_from_P = mass_be_at_xi_from_P(cs_b68, P_b68, B68_T4_XI)
    M_from_R = mass_be_at_xi_from_R(cs_b68, R_b68, B68_T4_XI)
    M_BE_max = mass_bonnor_ebert(cs_b68, P_b68)
    P(f'    route 1, from P_ext and xi_max    = {M_from_P/Msun:.4f} Msun  '
      f'(ratio to published {M_from_P/(B68_M*Msun):.4f})')
    P(f'    route 2, from R and xi_max        = {M_from_R/Msun:.4f} Msun  '
      f'(ratio to published {M_from_R/(B68_M*Msun):.4f})')
    P(f'    spread between the two routes     = '
      f'{abs(M_from_P/M_from_R - 1.0)*100:.1f} per cent')
    P(f'    critical mass 1.18 c_s^4/(G^1.5 P^0.5) = {M_BE_max/Msun:.4f} Msun')
    P(f'    M(xi=6.9)/M_BE predicted          = {be_m(B68_T4_XI)/m_crit:.4f}')
    P(f'    M(published)/M_BE                 = {B68_M*Msun/M_BE_max:.4f}')
    P('    READ, and do not smooth this over: the published R and P_ext are')
    P('    not mutually consistent at better than 13 per cent, so no mass')
    P('    statement about this core is good to better than that.  The')
    P('    stability verdict does not depend on the mass at all, which is')
    P('    exactly why the contrast, not the mass, is the sharp measurement.')
    P('    Note also that M(xi=6.9) is only '
      f'{(1.0-be_m(B68_T4_XI)/m_crit)*100:.2f} per cent below the')
    P('    maximum: a mass just under M_BE is compatible with BOTH branches.')

    # ---------------------------------------------------------------- I
    P('')
    P('PART I.  THE LIMIT: what the isothermal premise costs')
    P('-'*74)
    P(f'  The fit determines only the product: substituting R = theta_R d')
    P(f'  and rho_c ~ 1/d into xi_max gives T/d = constant (Kandori section')
    P(f'  4.2.2, crediting Lai et al. 2003).  The same fitted shape therefore')
    P(f'  reads as either row of Table 5:')
    P(f'    T = {B68_T_BE:.0f} K, d = {B68_D:.0f} pc  -> '
      f'R = {B68_R_AU:.2e} AU, M = {B68_M:.2f} Msun, '
      f'P_ext/k = {B68_PEXT_K:.1e}')
    P(f'    T = {B68_T_EFF:.0f} +/- {B68_T_EFF_ERR} K, d = '
      f'{B68_D_RESCALED:.0f} pc -> R = {B68_R_AU_RESCALED:.2e} AU, '
      f'M = {B68_M_RESCALED:.2f} Msun, P_ext/k = {B68_PEXT_K_RESCALED:.1e}')
    P(f'    ratio of the two masses           = '
      f'{B68_M/B68_M_RESCALED:.4f}')
    P(f'    M ~ c_s^2 R ~ T d at fixed xi, so predicted ratio = '
      f'{(B68_T_BE/B68_T_EFF)*(B68_R_AU/B68_R_AU_RESCALED):.4f}')
    P(f'    agreement between the two         = '
      f'{(B68_M/B68_M_RESCALED)/((B68_T_BE/B68_T_EFF)*(B68_R_AU/B68_R_AU_RESCALED)):.4f}')
    P('  The shape parameter xi_max is robust; the SCALE is not.  Nothing in')
    P('  the profile fixes the temperature, and the measured gas temperature')
    P(f'  is {B68_T_GAS} K (Lada et al. 2003), not the {B68_T_BE:.0f} K the '
      f'first row assumes.')
    P('')
    P('  And the isothermal premise itself is measurably false.  Nielbock et')
    P('  al. (2012), A&A 547, A11, resolve the DUST temperature of the same')
    P(f'  cloud: {B68_TDUST_EDGE} (+1.3 -1.0) K at the edge falling to '
      f'{B68_TDUST_CENTRE} (+2.1 -0.7) K')
    P(f'  in the centre, a range of a factor '
      f'{B68_TDUST_EDGE/B68_TDUST_CENTRE:.2f}.')
    P('  A Bonnor-Ebert sphere assumes that factor is 1.')
    P(f'  They also find n_H ~ r^-{B68_OUTER_SLOPE} outside the inner plateau.')
    slope_be = be_mu_R(B68_T4_XI)
    xs_max_i, sl_max_i = be_max_slope()
    P(f'  The Bonnor-Ebert local slope -d ln rho/d ln r = xi psi\'(xi) at')
    P(f'  xi = {B68_T4_XI} is {slope_be:.4f}, against the measured '
      f'{B68_OUTER_SLOPE}; ratio '
      f'{B68_OUTER_SLOPE/slope_be:.3f}.')
    P('  The slope is NOT bounded by 2: because the solution overshoots the')
    P('  singular isothermal sphere before oscillating back onto it, the')
    P(f'  local slope peaks at {sl_max_i:.4f} at xi = {xs_max_i:.3f} and then decays')
    P('  towards 2.  That peak is the ceiling on any Bonnor-Ebert sphere:')
    for x in (6.9, 8.993, 10.0, 20.0, 30.0, 100.0, 200.0):
        P(f'    xi = {x:6.2f}   xi psi-prime = {be_mu_R(x):.4f}')
    P(f'  PUNCHLINE: measured {B68_OUTER_SLOPE} against a ceiling of '
      f'{sl_max_i:.4f}, a ratio of')
    P(f'  {B68_OUTER_SLOPE/sl_max_i:.3f}.  The measured outer slope is steeper than ANY')
    P('  Bonnor-Ebert sphere can be anywhere.  That is a limit on the')
    P('  closure, not on the fluid equations.')
    P('')
    P('  The same test at matched radius, with Nielbock\'s ADOPTED eq. (8) fit')
    P(f'  (r0 = {B68_N_R0:.0f}", eta = {B68_N_ETA}, n0 = {B68_N_N0:.1e}, '
      f'n_out = {B68_N_NOUT:.0f} cm^-3)')
    P(f'  against the BE sphere xi = {B68_T4_XI} r/{B68_THETA_R:.0f}" of '
      'Alves et al.  Angles, so no distance enters.')
    n_slope = nielbock_slope
    for th in (20.0, 40.0, 45.0, 60.0, 80.0, 100.0):
        P(f'    r = {th:5.1f}"   measured slope {n_slope(th):.4f}   '
          f'BE slope {be_slope(B68_T4_XI*th/B68_THETA_R):.4f}   '
          f'ratio {n_slope(th)/be_slope(B68_T4_XI*th/B68_THETA_R):.3f}')
    lo, hi = 30.0, 60.0
    for _ in range(60):
        mid = 0.5*(lo + hi)
        lo, hi = (mid, hi) if n_slope(mid) < sl_max_i else (lo, mid)
    P(f'  measured slope exceeds the 2.5176 ceiling for r > {lo:.1f}", i.e. over')
    P(f'  the outer {100.0*(1.0 - lo/B68_THETA_R):.1f} per cent of the fitted '
      'radius.')
    P('  CAUTION: dust temperature is not gas temperature, and Nielbock')
    P('  assume 150 pc where the fit above assumes 125 pc.  Their 3.1 Msun')
    P('  is not comparable with 2.10 Msun without rescaling by distance.')

    # ---------------------------------------------------------------- J
    P('')
    P('PART J.  Numbers for the problem set')
    P('-'*74)

    P('  P1.  Jeans length and mass of the 10 K core, n(H2) = 1e4 cm^-3.')
    P(f'       lambda_J = {lambda_jeans(cs1, rho1)/AU:.0f} AU, '
      f'M_J = {mass_jeans(cs1, rho1)/Msun:.4f} Msun, '
      f't_grow = {t_grow(rho1)/yr:.3e} yr')

    P('  P2.  Warm neutral ISM, 8000 K, n(H) = 0.5 cm^-3.')
    P(f'       lambda_J = {lambda_jeans(cs2, rho2)/pc:.1f} pc, '
      f'M_J = {mass_jeans(cs2, rho2)/Msun:.3e} Msun')
    P(f'       M_J with the ADIABATIC sound speed = '
      f'{mass_jeans(sound_speed_ad(T2, MU_HI), rho2)/Msun:.3e} Msun '
      f'(factor {(GAMMA_MONO)**1.5:.3f} = gamma^(3/2))')

    P('  P3.  Primordial gas at recombination, 3000 K.')
    P(f'       rho = {rho3:.4e} g/cm^3, lambda_J = '
      f'{lambda_jeans(cs3, rho3)/pc:.1f} pc, '
      f'M_J = {mass_jeans(cs3, rho3)/Msun:.4e} Msun')
    P('       Compare a globular cluster, 1e5-1e6 Msun.')

    P('  P4.  The k -> 0 limit.')
    P(f'       t_ff/t_grow = pi sqrt(3/8) = {tff_over_tgrow():.6f} exactly,')
    P('       independent of density, temperature and composition.')

    P('  P5.  Bonnor-Ebert mass of a core at P_ext/k = 1e5 K cm^-3, T = 10 K.')
    cs_p5 = sound_speed(10.0, MU_MOL)
    P_p5 = 1.0e5*kB
    P(f'       c_s = {cs_p5/1e5:.4f} km/s, '
      f'M_BE = {mass_bonnor_ebert(cs_p5, P_p5)/Msun:.4f} Msun')
    P(f'       radius at the critical point R = alpha xi_crit = '
      f'{(mass_bonnor_ebert(cs_p5, P_p5)*G/(cs_p5**2*be_mu_R(xi_crit)))/AU:.0f} AU')
    P(f'       central density there = '
      f'{be_central_density(cs_p5, mass_bonnor_ebert(cs_p5, P_p5)*G/(cs_p5**2*be_mu_R(xi_crit)), xi_crit):.3e} g/cm^3')
    P(f'       Jeans mass at that central density = '
      f'{mass_jeans(cs_p5, be_central_density(cs_p5, mass_bonnor_ebert(cs_p5, P_p5)*G/(cs_p5**2*be_mu_R(xi_crit)), xi_crit))/Msun:.4f} Msun')

    P('  P6.  Invert the contrast.  A core measured to have rho_c/rho_R = 30')
    P(f'       has xi_max = {be_xi_from_contrast(30.0):.4f}, which is '
      f'{(be_xi_from_contrast(30.0)-xi_crit)/xi_crit*100:.1f} per cent above')
    P(f'       critical; contrast 10 gives xi_max = '
      f'{be_xi_from_contrast(10.0):.4f}, below it.')
    P(f'       The stability boundary in contrast is {contrast_crit:.4f}.')

    P('  P7.  Toomre preview.  Take Sigma = 50 Msun/pc^2, c_s = 7 km/s,')
    P('       kappa = 36 km/s/kpc.  THESE ARE ROUND NUMBERS GIVEN IN THE')
    P('       PROBLEM, not measured values; the module claims nothing from')
    P('       them and Module 12 sources them properly.')
    Sig7 = 50.0*Msun/pc**2
    cs7 = 7.0e5
    kap7 = 36.0*1e5/kpc
    P(f'       Sigma = {Sig7:.4e} g/cm^2, kappa = {kap7:.4e} s^-1')
    Q7 = toomre_Q(cs7, kap7, Sig7)
    P(f'       Q = c_s kappa/(pi G Sigma) = {Q7:.4f}')
    P(f'       Q < 1, so this disc IS unstable, and the band of unstable')
    P(f'       wavenumbers is where c_s^2 k^2 - 2 pi G Sigma k + kappa^2 < 0.')
    kpm = np.pi*G*Sig7/(cs7*cs7)
    disc = np.sqrt(max(1.0 - Q7*Q7, 0.0))
    k_lo, k_hi = kpm*(1.0 - disc), kpm*(1.0 + disc)
    P(f'       unstable wavelengths run from '
      f'{2.0*np.pi/k_hi/kpc:.4f} kpc to {2.0*np.pi/k_lo/kpc:.4f} kpc')
    P(f'       lambda_crit with kappa = 0      = '
      f'{sheet_lambda_crit(cs7, Sig7)/kpc:.4f} kpc')
    P(f'       most unstable lambda, kappa = 0 = '
      f'{sheet_fastest(cs7, Sig7)[0]/kpc:.4f} kpc')
    P(f'       the c_s that would give Q = 1 is '
      f'{np.pi*G*Sig7/kap7/1e5:.2f} km/s; rotation alone cannot')
    P('       stabilise this disc at 7 km/s, which is the point Module 12')
    P('       develops.')

    P('  P8.  Size of the swindle at the Jeans length, warm neutral ISM.')
    g8, t8 = swindle_residual(rho2, lambda_jeans(cs2, rho2))
    P(f'       g = {g8:.3e} cm/s^2, crossing time {t8/yr:.3e} yr, '
      f'growth time {t_grow(rho2)/yr:.3e} yr, ratio {t8/t_grow(rho2):.4f}')

    P('  P9.  Barnard 68, the two verdicts.')
    P(f'       M_J/M = {MJ_b68/(B68_M*Msun):.4f} (Jeans says stable); '
      f'xi_max - xi_crit = {B68_T4_XI - xi_crit:+.4f} = '
      f'{sig_b68:.2f} sigma (Bonnor-Ebert says unstable)')

    P('  P10. The isothermal sheet at the 10 K core density.')
    P(f'       H = {H1/AU:.1f} AU, Sigma = {Sig1/(Msun/pc**2):.1f} Msun/pc^2,')
    P(f'       lambda_crit = {lam_c/pc:.5f} pc, '
      f'lambda_fastest = {lam_m/pc:.5f} pc = 2 lambda_crit,')
    P(f'       s_max = pi G Sigma/c_s = {s_max:.4e} s^-1, '
      f'1/s_max = {1.0/s_max/yr:.3e} yr')
    P(f'       Compare the spherical Jeans growth time at the same rho_0: '
      f'{t_grow(rho1)/yr:.3e} yr')

    P('')
    P('=' * 74)
    P('SOURCES')
    P('=' * 74)
    P('  Kandori, R., Nakajima, Y., Tamura, M., Tatematsu, K., Aikawa, Y.,')
    P('    Naoi, T., Sugitani, K., Nakaya, H., Nagayama, T., Nagata, T.,')
    P('    Kurita, M., Kato, D., Nagashima, C., & Sato, S. (2005),')
    P('    "Near-Infrared Imaging Survey of Bok Globules: Density')
    P('    Structure", AJ 130, 2166-2184.  doi:10.1086/444619,')
    P('    arXiv:astro-ph/0506205.  THE ANCHOR SOURCE.  Table 4 (arXiv PDF')
    P('    page 27) gives xi_max and rho_c/rho_R for fifteen rows;')
    P('    Table 5 (page 28) gives T, distance, R, mass and P_ext; equations')
    P('    (8)-(11) (pages 9-10) define the model; the critical state and')
    P('    contrast "14" are on page 10; the count of stable and unstable')
    P('    starless globules is on page 12; the T/d degeneracy is in')
    P('    section 4.2.2 on page 11; the collapsing-sphere resolution is on')
    P('    pages 16-17.  Author list read from the paper, not from memory.')
    P('  Alves, J. F., Lada, C. J., & Lada, E. A. (2001), Nature 409, 159,')
    P('    "Internal structure of a cold dark molecular cloud inferred from')
    P('    the extinction of background starlight".  The original Barnard 68')
    P('    fit.  NOT READ: this paper is not on arXiv.  Every number')
    P('    attributed to it here was read from Kandori et al. (2005) Tables')
    P('    4 and 5, where it is reference (B), and the citation string was')
    P('    read from Kandori\'s reference list (arXiv PDF page 19).')
    P('  Lada, C. J., Bergin, E. A., Alves, J. F., & Huard, T. L. (2003),')
    P('    ApJ 586, 286-295, "The Dynamical State of Barnard 68: A Thermally')
    P('    Supported, Pulsating Dark Cloud".  doi:10.1086/367610,')
    P('    arXiv:astro-ph/0211507.  Gas temperature 10.5 K, C18O FWHM')
    P('    0.18 +/- 0.01 km/s, C34S FWHM 0.15 +/- 0.01 km/s, thermal over')
    P('    non-thermal pressure 4-5; abstract and pages 1-2.')
    P('  Burkert, A., & Alves, J. (2009), ApJ 695, 1308, "The Inevitable')
    P('    Future of the Starless Core Barnard 68".')
    P('    doi:10.1088/0004-637X/695/2/1308, arXiv:0809.1457.  Page 1:')
    P('    M = 2.1 Msun within R = 12500 AU at ~125 pc, mean density')
    P('    1.5e-19 g/cm^3, collapse timescale 0.17e6 yr, c_s ~ 0.2 km/s,')
    P('    oscillation timescale 3e6 yr, and xi_max = 6.9 +/- 0.2 against')
    P('    the critical 6.5.')
    P('  Nielbock, M., Launhardt, R., Steinacker, J., Stutz, A. M., Balog,')
    P('    Z., Beuther, H., Bouwman, J., Henning, Th., Hily-Blant, P.,')
    P('    Kainulainen, J., Krause, O., Linz, H., Lippok, N., Ragan, S.,')
    P('    Risacher, C., & Schmiedeke, A. (2012), A&A 547, A11, "The')
    P('    Earliest Phases of Star formation (EPoS) observed with Herschel:')
    P('    the dust temperature and density distributions of B68".')
    P('    doi:10.1051/0004-6361/201219139, arXiv:1208.4512.  Abstract:')
    P('    dust T from 16.7 (+1.3 -1.0) K at the edge to 8.2 (+2.1 -0.7) K')
    P('    at the centre, n_H = 3.4e5 cm^-3 central, n_H ~ r^-3.5 outside')
    P('    the plateau, M = 3.1 Msun at an assumed 150 pc.')
    P('  Bonnor, W. B. (1956), MNRAS 116, 351; Ebert, R. (1955),')
    P('    Zeitschrift fuer Astrophysik 37, 217.  The two independent')
    P('    derivations of the critical mass.  Citation strings read from')
    P('    Kandori\'s reference list, not from memory; the papers themselves')
    P('    are not in this folder and nothing is attributed to their text')
    P('    beyond the criterion, which is re-derived here.')
    P('  Hotzel, S., Harju, J., & Juvela, M. (2002a), A&A 395, L5.  The')
    P('    rescaled Barnard 68 row of Kandori Table 5 (T = 10 +/- 1.2 K,')
    P('    d = 85 pc, M = 0.90 Msun).  Read from Kandori, not from the paper.')
    P('  Lai, S., Velusamy, T., Langer, W. D., & Kuiper, T. B. H. (2003),')
    P('    AJ 126, 311.  Credited by Kandori for the T/d degeneracy.')
    P('  Planck Collaboration (Aghanim, N., et al.) (2020), A&A 641, A6,')
    P('    "Planck 2018 results. VI. Cosmological parameters".')
    P('    doi:10.1051/0004-6361/201833910, arXiv:1807.06209.  Table 2,')
    P('    column TT,TE,EE+lowE+lensing (arXiv PDF page 15): Omega_b h^2 =')
    P('    0.02237 +/- 0.00015, H0 = 67.36 +/- 0.54 km/s/Mpc, z_* =')
    P('    1089.92 +/- 0.25.  Used as INPUTS to the recombination-era Jeans')
    P('    mass; nothing is checked against them.')
    P('  IAU 2015 Resolution B3: nominal GM_sun, R_sun, L_sun.')



if __name__ == '__main__':
    main()
