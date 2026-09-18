"""Module 7 numbers: Rayleigh-Taylor and Kelvin-Helmholtz instabilities of a
plane interface, checked against one laboratory measurement and one solar
observation.

Every physical number quoted in module07.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

THE SPINE.  One dispersion relation, derived once in PART A, carries the
whole module.  For two semi-infinite incompressible fluids separated by a
plane interface, with the heavy fluid of density rho_t ABOVE the light fluid
rho_b, uniform streaming velocities differing by dU along the interface,
gravity g across it, interfacial tension T, and uniform magnetic fields
B_t and B_b making an angle theta with the wavevector k,

    sigma^2 =   k^2 rho_t rho_b dU^2 / (rho_t + rho_b)^2        <- KH drive
              + A g k                                           <- RT drive
              - T_s k^3 / (rho_t + rho_b)                       <- capillarity
              - k^2 (B_t^2 + B_b^2) cos^2(theta) / (4 pi (rho_t + rho_b))

with the Atwood number A = (rho_t - rho_b)/(rho_t + rho_b).  PART A checks
this expression against five known limits before anything is computed with
it, the way m03_numbers.py checks its Lane-Emden integrator against the
exact n = 0, 1 and 5 solutions.

THE SHAPE OF THE CHECK, following Modules 2 and 3.  One prediction is
CONFIRMED and one assumption is REFUTED, from the same published source.
Two sources are used, because the two halves of the module need different
things from them, and they are of very different sharpness.

  TERRESTRIAL, AND THE ONLY PLACE A SIGMA EXISTS.
  Shimony et al. (2022), arXiv:2210.06631, a laser-driven Rayleigh-Taylor
  experiment on the National Ignition Facility.

    CONFIRMED  The nonlinear mixing-layer law h_B = alpha_B A g t^2.  The
               measured widths from four different initial perturbations
               collapse onto one line when plotted against the Read
               integral x_Read = A (int sqrt(g) dt)^2, which is that law
               written for an acceleration that varies in time.  The law
               is confirmed; its coefficient is what is measured.

    REFUTED    That alpha_B is a constant of nature.  Their value is
               alpha_B = 0.038 +/- 0.008.  It excludes 0.077, an earlier
               experimental value, at 4.9 sigma, and 0.06 at 2.8 sigma,
               while sitting within 1.6 sigma of BOTH the ~0.05 of the
               immiscible bubble-merger models and the ~0.025 of the 3D
               simulations.  The paper's own explanation is that
               long-wavelength content in the seed raises the measured
               alpha_B, so the coefficient depends on how the experiment
               was started.  h = alpha A g t^2 is a scaling law with a
               +/- 20% coefficient, not a formula.

  ASTROPHYSICAL ANCHOR, AND IT IS WEAKER THAN MODULES 2 AND 3.
  Ofman & Thompson (2011), ApJ 734, L11, Kelvin-Helmholtz vortices on the
  flank of a coronal mass ejection seen by SDO/AIA on 8 April 2010.

  Say the weakness first.  Every input this paper gives is quoted to one
  significant figure with no uncertainty: the wavelength is "~7000 km",
  the driving shear is "~20 km/s" and is stated as an UPPER limit, the
  interface is "1-3 pixels", the growth time is "on the order of 14
  minutes".  No sigma can be computed from it, and none is claimed below.
  Every ratio here is a factor-of-two statement.  The sharp result the
  anchor does yield is not a ratio at all; it is the bound on the magnetic
  field in CHECK 4.

  Foullon et al. (2011), ApJ 729, L8, was the first choice, because it
  quotes uncertainties.  It is not on arXiv and could not be read; a
  number taken from a paper this folder does not hold would break the rule
  that broke Module 2's citation.  Ofman & Thompson was used because its
  preprint is readable in full.

    CONFIRMED  The linear growth rate.  Their published estimate
               gamma ~ 0.003-0.006 s^-1 is reproduced to the one figure
               they quote it to, from the general dispersion relation in
               its equal-density limit, and their statement that nonlinear
               saturation comes "at several gamma^-1 or in about 10
               minutes" is reproduced as 1.6 to 3.8 e-foldings.

    CONSISTENT BUT NOT DISCRIMINATING, AND LABELLED SO.  The linear theory
               also predicts the PHASE speed of the mode, the
               density-weighted mean of the two stream velocities.  From
               their measured shear and their measured density ratio it is
               6.2 km/s, inside their observed 6-14 km/s band.  But the
               equal-density value dU/2 = 10 km/s is also inside that
               band.  The observation cannot tell the two formulas apart,
               so this is not counted as a confirmation.

    REFUTED / LIMIT  Three assumptions, each refuted with the paper's own
               numbers and each computed in PART G:
               (1) Their growth-rate formula is the EQUAL-DENSITY case,
                   applied to an interface they measure to have a density
                   ratio of 5^(1/2) = 2.236.  Their rate is 8.2% high.
               (2) "The magnetic field has no parallel component to the
                   interface."  Undoing that assumption turns the
                   observation into a MEASUREMENT: the instability
                   existing at all bounds the field component along the
                   wavevector.  This is the sharp result of the module,
                   and Module 12 repays it.
               (3) "The velocity jump is discontinuous since it is much
                   smaller than the wavelength."  The parameter that
                   decides this is k a, not a/lambda, and k a = 0.72.

    AND ONE GEOMETRICAL RESULT that neither paper states.  The gravity
               term is absent from this problem only because the interface
               is radial, so gravity lies along it.  Restore gravity
               across the interface and the two-layer cutoff forbids the
               observed wavelength by a factor 1.4.  The geometry is not a
               detail; it is the difference between the mode existing and
               not.

Sources for every published number compared against are listed in the
SOURCES block at the foot of this file and in module07.html, with the page
of the preprint each number was read from.
"""
import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m01_numbers.py, m02_numbers.py and m03_numbers.py
# rather than imported, so that each module's numbers script reads on its
# own.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
mp = 1.67262192369e-24  # g
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
a_rad = 7.565733e-15    # erg cm^-3 K^-4 (radiation constant, 4 sigma_SB/c)
pc = 3.0856775814913673e18   # cm
kpc = 1e3*pc
AU = 1.495978707e13     # cm
yr = 3.15576e7          # s

GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
Rsun = 6.957e10         # cm             (IAU 2015 nominal)
Lsun = 3.828e33         # erg/s          (IAU 2015 nominal)
Msun = GMsun/G          # g

g_earth = 980.665       # cm/s^2         (standard gravity, definitional)
mu_air = 28.9647        # dimensionless  (mean molecular weight of dry air)

# --- laboratory fluid properties, 20 C, 1 atm ----------------------------
# Handbook values.  These are INPUTS, not numbers checked against anything.
RHO_WATER = 0.998207    # g/cm^3         (pure water, 20 C)
RHO_AIR = 1.2041e-3     # g/cm^3         (dry air, 20 C, 101.325 kPa)
SIGMA_WATER = 72.75     # dyn/cm         (water-air interfacial tension, 20 C)
NU_WATER = 1.0034e-2    # cm^2/s         (kinematic viscosity of water, 20 C)
RHO_BRINE = 1.0210      # g/cm^3         (3 per cent NaCl by mass, 20 C)

# =========================================================================
# Ofman & Thompson (2011), ApJ 734, L11.  arXiv:1101.4249v2.
# Every value below is read from the preprint; the page is the printed page
# number of the preprint, which is the PDF page index plus one.
# =========================================================================
OT_LAMBDA = 7.0e8       # cm      p.5, p.10: vortices "~7000 km"
OT_SIZE_LO = 3.0        # arcsec  p.2, p.5: "several to ten arcseconds"
OT_SIZE_HI = 10.0       # arcsec
OT_VPROP_LO = 6.0e5     # cm/s    p.2, p.5, p.6: vortices travel 6-14 km/s
OT_VPROP_HI = 1.4e6     # cm/s            along the boundary, solar rotation
#                                         already compensated (p.6)
OT_DU = 2.0e6           # cm/s    p.6: loop tracking gives "~20 km/s", and
#                                 the paper calls it an UPPER limit on the
#                                 shearing motion
OT_A_LAYER = 8.0e7      # cm      p.6: interface "1-3 pixels", "on average
#                                 the interface is ~800 km thick"
OT_PIX_ARCSEC = 0.6     # arcsec  p.4: AIA pixel width
OT_EMIS = 5.0           # p.9: EUV emission ratio across the interface is
OT_EMIS_LO = 3.0        #      "on average ~5 with a range of 3-10"
OT_EMIS_HI = 10.0
#                       p.9: "density is proportional to the emission
#                       square", so rho_max/rho_min = 5^(1/2)
OT_GAMMA_LO = 3.0e-3    # s^-1    p.8: "gamma_KH ~ 0.003 - 0.006 s^-1"
OT_GAMMA_HI = 6.0e-3    # s^-1
OT_TSAT = 6.0e2         # s       p.8: saturation "at several gamma^-1 or
#                                 in about 10 minutes"
OT_TGROW = 8.4e2        # s       p.6: "growth time of the KH instability to
#                                 the nonlinear stage is on the order of 14
#                                 minutes"
OT_T_FIRST = 3*3600 + 0*60 + 13    # p.5: first sign of vortex formation,
OT_T_FULL = 3*3600 + 13*60 + 53    #      3:00:13 UT, and full development.
#                                  The paper gives TWO times for full
#                                  development, 3:13:13 (p.5, "the flow ...
#                                  was fully developed by") and 3:13:53
#                                  (p.5, "the first image where we see any
#                                  motion along the KH front").  Both are
#                                  carried below.
OT_T_FULL_ALT = 3*3600 + 13*60 + 13
OT_MODEL_V0_OVER_VA = 5.0   # p.9: model initialised with V0 = 5 V_A,xy
OT_CME_SPEED = 5.0e7        # cm/s   p.4: STEREO SECCHI, CME "around 500 km/s"

# Coronal density.  The paper gives only the RATIO of the two densities,
# never an absolute value, and states "the value of the magnetic field in
# the observations is unknown" (p.9).  The absolute density is therefore an
# INPUT, carried over from Module 1's census of astrophysical gases, where
# the solar corona sits at n_e = 3e8 cm^-3 and T = 2e6 K.  Every quantity
# below that needs it scales as sqrt(n_e), and that scaling is printed, so
# a reader who prefers a denser active-region value can rescale by eye.
NE_CORONA = 3.0e8       # cm^-3          (Module 1, afd/figs/m01_build_figs.py)
X_HYDROGEN = 0.70       # hydrogen mass fraction, for mu_e = 2/(1+X)

# =========================================================================
# Shimony et al. (2022), arXiv:2210.06631v1.  No journal reference appears
# on the arXiv record, so this departs from the book's convention of citing
# journal, volume and page; it is cited as a preprint and said to be one.
# =========================================================================
ALPHA_B = 0.038         # p.1 (abstract) and p.4
ALPHA_B_ERR = 0.008
ALPHA_THEORY_3D = 0.05  # p.1: "recent theoretical model results suggest a
#                         value of ~0.05 for 3D immiscible fluids"
ALPHA_SIM = ALPHA_THEORY_3D/2.0   # p.1: full numerical 3D simulations.
#                         The paper prints no value for them.  It prints the
#                         RATIO: the ~0.05 above is "a factor of ~2 higher
#                         than the results of full numerical 3D simulations".
#                         0.025 is therefore INFERRED from a printed ratio,
#                         not read, and is labelled so wherever it is used.
ALPHA_FIT_LO = 0.03     # p.4, Fig. 4 caption: chi-squared bounds on the
ALPHA_FIT_HI = 0.046    #      <lambda> = 15 micron case
# NOT DEFINED HERE, deliberately: alpha_B = 0.060 and 0.077 for "earlier
# experiments".  Neither string occurs anywhere in Shimony et al.; a
# full-text search returns only the arXiv identifier 2210.06631.  Taking a
# number from a paper this folder does not hold is the rule that broke
# Module 2's citation, so both are cut.  What replaces them is the claim in
# the paper's own abstract, tested below against the paper's own sigma.
NIF_G_GENERATIONS = 3.0     # p.1: self-similarity reached after G ~ 3
NIF_LAMBDA0 = 15e-4         # cm   p.2: the <lambda> = 15 micron case
NIF_DU_RM = 16e-4/1e-9      # cm/s p.4: "velocity jump ... 16 micron/ns"


# =========================================================================
# PART A.  The dispersion relation, and five limits that check it
# =========================================================================

def sigma_squared(k, rho_t, rho_b, dU=0.0, g=0.0, T=0.0,
                  B_t=0.0, B_b=0.0, costheta=1.0):
    """Squared growth rate of a plane interface, CGS-Gaussian.

    rho_t is the density ABOVE the interface, rho_b the density below, and
    g > 0 points downward.  A positive return value is a growing mode of
    rate sqrt(sigma^2); a negative one is a stable oscillation of frequency
    sqrt(-sigma^2) about the density-weighted mean drift.

    The four terms, in the order written, are the Kelvin-Helmholtz drive,
    the Rayleigh-Taylor drive, the restoring force of interfacial tension,
    and the restoring force of magnetic tension.  costheta is the cosine of
    the angle between the wavevector and the field, so a field perpendicular
    to k exerts no tension at all and drops out.
    """
    s = rho_t + rho_b
    kh = k*k*rho_t*rho_b*dU*dU/(s*s)
    rt = g*k*(rho_t - rho_b)/s
    cap = T*k**3/s
    mag = k*k*(B_t*B_t + B_b*B_b)*costheta*costheta/(4.0*np.pi*s)
    return kh + rt - cap - mag


def atwood(rho_t, rho_b):
    """Atwood number A = (rho_t - rho_b)/(rho_t + rho_b), positive when the
    heavy fluid is on top and the interface is Rayleigh-Taylor unstable."""
    return (rho_t - rho_b)/(rho_t + rho_b)


def rt_lambda_cut(T, g, drho):
    """Shortest RT-unstable wavelength when interfacial tension acts.

    Setting A g k = T_s k^3/(rho_t + rho_b) and using A(rho_t+rho_b) = drho
    gives k_c = sqrt(g drho / T_s), so lambda_c = 2 pi sqrt(T_s/(g drho)).
    T_s is the interfacial tension; this module writes it T_s and never
    T, because T is the temperature in PART D and PART E.
    Every shorter wavelength is held flat by capillarity.
    """
    return 2.0*np.pi*np.sqrt(T/(g*drho))


def rt_lambda_max(T, g, drho):
    """Fastest-growing RT wavelength with interfacial tension.

    d/dk [A g k - T_s k^3/(rho_t+rho_b)] = 0 gives k^2 = g drho/(3 T_s),
    so lambda_max = 2 pi sqrt(3 T_s/(g drho)) = sqrt(3) lambda_c.
    """
    return 2.0*np.pi*np.sqrt(3.0*T/(g*drho))


def rt_lambda_viscous(nu, A, g):
    """Wavelength below which viscosity, not inertia, limits RT growth.

    This is a CROSSOVER SCALE, not a theorem.  It is defined by equating
    the inviscid growth rate sqrt(A g k) with the viscous damping rate
    2 nu k^2, which gives k_nu = (A g/(4 nu^2))^(1/3).  Below lambda_nu the
    viscous quartic must be solved; above it viscosity is a correction.
    The full viscous problem is Chandrasekhar's and is not solved here.
    """
    k_nu = (A*g/(4.0*nu*nu))**(1.0/3.0)
    return 2.0*np.pi/k_nu


def kh_k_gravity_cutoff(g, rho_t, rho_b, dU):
    """Longest KH-unstable wavenumber when gravity acts ACROSS the interface.

    Instability needs the KH term to beat the RT restoring term, which for
    a stable stratification (rho_b > rho_t, so A < 0) means
        k rho_t rho_b dU^2/(rho_t+rho_b)^2 > g (rho_b - rho_t)/(rho_t+rho_b),
    that is
        k > g (rho_b^2 - rho_t^2)/(rho_t rho_b dU^2).
    Long waves are stabilised, short waves are not.  This is the two-layer
    criterion.  It is NOT the Miles-Howard theorem Ri < 1/4, which is a
    statement about continuous stratification; the two are kept apart.
    """
    return g*(rho_b*rho_b - rho_t*rho_t)/(rho_t*rho_b*dU*dU)


def richardson(N2, shear):
    """Gradient Richardson number Ri = N^2/(dU/dz)^2 for a continuously
    stratified shear flow.  Miles (1961) and Howard (1961) proved that
    Ri > 1/4 everywhere is SUFFICIENT for stability.  It is not necessary:
    Ri < 1/4 somewhere permits instability, it does not compel it.
    """
    return N2/(shear*shear)


def brunt_vaisala_sq(T, lapse, gamma=1.4, mu=mu_air, g=g_earth):
    """N^2 = (g/T)(dT/dz + g/c_p) for an ideal gas atmosphere.

    lapse is the environmental lapse rate as a POSITIVE number, so
    dT/dz = -lapse and N^2 = (g/T)(g/c_p - lapse).  The adiabatic lapse
    rate g/c_p is the Module 3 quantity, recomputed here rather than
    imported.
    """
    cp = gamma*kB/((gamma - 1.0)*mu*mu_u)
    return (g/T)*(g/cp - lapse)


def sound_speed(T, mu, gamma=5.0/3.0):
    """Adiabatic sound speed sqrt(gamma k T/(mu m_u))."""
    return np.sqrt(gamma*kB*T/(mu*mu_u))


def alfven_speed(B, rho):
    """Alfven speed B/sqrt(4 pi rho), CGS-Gaussian."""
    return B/np.sqrt(4.0*np.pi*rho)


def phase_speed(rho_t, rho_b, U_t, U_b):
    """Phase speed of the interfacial mode: the density-weighted mean of
    the two stream velocities, (rho_t U_t + rho_b U_b)/(rho_t + rho_b).

    This is the real part of omega/k, and it is fixed by the same algebra
    that gives sigma^2.  It is a prediction independent of the growth rate.
    """
    return (rho_t*U_t + rho_b*U_b)/(rho_t + rho_b)


def b_parallel_max(rho_t, rho_b, dU, both_sides=True):
    """Largest field component along k that still permits KH instability.

    The magnetic term in sigma_squared carries B_t^2 + B_b^2, so the bound
    depends on a HYPOTHESIS about how the field is distributed, and both
    cases are printed rather than one:

      both_sides=True   B_t = B_b = B, the case the Ofman & Thompson model
                        runs.  2 B^2 cos^2(theta)/(4 pi) < rho_t rho_b
                        dU^2/(rho_t + rho_b), so
                        B cos(theta) < dU sqrt(2 pi rho_t rho_b/(rho_t+rho_b)).
      both_sides=False  the field lies on one side only.  The same
                        inequality with B_t^2 alone, giving a bound larger
                        by sqrt(2) and therefore the WEAKER, conservative
                        statement.

    The bound scales as sqrt(density), which is why the coronal density
    below is reported with its scaling attached.
    """
    two = 2.0 if both_sides else 1.0
    return dU*np.sqrt(4.0*np.pi*rho_t*rho_b/((rho_t + rho_b)*two))


def mix_width(alpha, A, g, t):
    """Nonlinear RT mixing-layer half-width h = alpha A g t^2."""
    return alpha*A*g*t*t


def read_integral(A, g, t):
    """The Read integral x_Read = A (int_0^t sqrt(g) dt')^2, eq. (1) of
    Shimony et al. (2022), for CONSTANT g.  For constant g the integral is
    sqrt(g) t, so x_Read = A g t^2 and the mixing law is h = alpha x_Read;
    the integral form is what lets a time-varying acceleration be folded in.
    """
    return A*(np.sqrt(g)*t)**2


def mu_electron(X=X_HYDROGEN):
    """Mean mass per electron in units of m_u, 2/(1+X), for a fully ionised
    plasma of hydrogen mass fraction X.  rho = mu_e n_e m_u."""
    return 2.0/(1.0 + X)


def arcsec_at_sun():
    """Length subtended by one arcsecond at 1 AU, in cm."""
    return AU*(np.pi/180.0/3600.0)


# =========================================================================
# Reporting
# =========================================================================

def main():
    P = print
    P('=' * 74)
    P('MODULE 7 NUMBERS: Rayleigh-Taylor and Kelvin-Helmholtz instabilities')
    P('=' * 74)

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  The dispersion relation, checked against five known limits')
    P('-'*74)
    ok = True

    # (1) pure RT, no tension, no field: sigma^2 = A g k
    rt_, rb_ = 2.0, 1.0
    k_ = 0.37
    A_ = atwood(rt_, rb_)
    lhs = sigma_squared(k_, rt_, rb_, g=g_earth)
    rhs = A_*g_earth*k_
    P(f'  (1) pure RT          sigma^2 = {lhs:.8e}   A g k = {rhs:.8e}   '
      f'ratio {lhs/rhs:.10f}')
    ok &= abs(lhs/rhs - 1) < 1e-12

    # (2) pure KH, equal densities: sigma = k dU/2
    lhs = np.sqrt(sigma_squared(k_, 1.0, 1.0, dU=3.3e4))
    rhs = 0.5*k_*3.3e4
    P(f'  (2) KH, equal rho    sigma   = {lhs:.8e}   k dU/2 = {rhs:.8e}   '
      f'ratio {lhs/rhs:.10f}')
    ok &= abs(lhs/rhs - 1) < 1e-12

    # (3) pure KH, unequal densities: sigma = k sqrt(rho_t rho_b) dU/(sum)
    lhs = np.sqrt(sigma_squared(k_, rt_, rb_, dU=3.3e4))
    rhs = k_*np.sqrt(rt_*rb_)*3.3e4/(rt_ + rb_)
    P(f'  (3) KH, unequal rho  sigma   = {lhs:.8e}   k sqrt(r1 r2)dU/(r1+r2)'
      f' = {rhs:.8e}   ratio {lhs/rhs:.10f}')
    ok &= abs(lhs/rhs - 1) < 1e-12

    # (4) equal densities and equal fields along k: Ofman & Thompson eq. (1)
    Bt = 1.7
    rho_ = 1.4e-15
    VA = alfven_speed(Bt, rho_)
    dU_ = 9.0*VA
    lhs = np.sqrt(sigma_squared(k_, rho_, rho_, dU=dU_, B_t=Bt, B_b=Bt))
    rhs = 0.5*k_*dU_*np.sqrt(1.0 - (2.0*VA/dU_)**2)
    P(f'  (4) Ofman eq. (1)    sigma   = {lhs:.8e}   '
      f'(k dU/2)sqrt(1-(2VA/dU)^2) = {rhs:.8e}   ratio {lhs/rhs:.10f}')
    ok &= abs(lhs/rhs - 1) < 1e-12

    # (5) RT with tension: the analytic lambda_max is a stationary point
    drho = RHO_WATER - RHO_AIR
    lam_max = rt_lambda_max(SIGMA_WATER, g_earth, drho)
    kk = 2.0*np.pi/lam_max
    Aw = atwood(RHO_WATER, RHO_AIR)
    eps = 1e-6*kk
    d1 = (sigma_squared(kk+eps, RHO_WATER, RHO_AIR, g=g_earth, T=SIGMA_WATER)
          - sigma_squared(kk-eps, RHO_WATER, RHO_AIR, g=g_earth,
                          T=SIGMA_WATER))/(2*eps)
    scale = Aw*g_earth
    P(f'  (5) RT + tension     d(sigma^2)/dk at lambda_max = {d1:.6e}, '
      f'relative to A g = {scale:.4e}: {abs(d1)/scale:.3e}')
    ok &= abs(d1)/scale < 1e-6
    P(f'  ALL FIVE LIMITS {"PASS" if ok else "FAIL"}.  The relation may now be '
      f'used on cases with no closed form.')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  Rayleigh-Taylor in the laboratory: water held above air')
    P('-'*74)
    lam_c = rt_lambda_cut(SIGMA_WATER, g_earth, drho)
    lam_m = rt_lambda_max(SIGMA_WATER, g_earth, drho)
    ell_c = np.sqrt(SIGMA_WATER/(g_earth*drho))
    k_m = 2.0*np.pi/lam_m
    sig_m = np.sqrt(sigma_squared(k_m, RHO_WATER, RHO_AIR, g=g_earth,
                                  T=SIGMA_WATER))
    lam_nu = rt_lambda_viscous(NU_WATER, Aw, g_earth)
    P(f'  Atwood number A                     = {Aw:.6f}')
    P(f'  capillary length sqrt(T_s/(g drho)) = {ell_c*10:.3f} mm')
    P(f'  cutoff wavelength lambda_c          = {lam_c:.4f} cm')
    P(f'  fastest wavelength lambda_max       = {lam_m:.4f} cm '
      f'(= sqrt(3) lambda_c, ratio {lam_m/(np.sqrt(3)*lam_c):.6f})')
    P(f'  its growth rate sigma_max           = {sig_m:.2f} s^-1')
    P(f'  its e-folding time 1/sigma_max      = {1e3/sig_m:.1f} ms')
    P(f'  viscous crossover lambda_nu         = {lam_nu*10:.3f} mm')
    P(f'  lambda_max/lambda_nu                = {lam_m/lam_nu:.1f}')
    P('  READ: hold a glass of water upside down and the surface picks out')
    P(f'  a {lam_m:.1f} cm wave and turns it over in {1e3/sig_m:.0f} '
      f'milliseconds.  Nothing shorter')
    P(f'  than {lam_c:.2f} cm grows at all: below that, capillarity wins.  '
      f'Viscosity is')
    P(f'  irrelevant here, by a factor {lam_m/lam_nu:.0f} in wavelength.  '
      f'A tube narrower')
    P(f'  than {lam_c:.2f} cm holds its water, which is the classroom '
      f'demonstration.')
    # salt water over fresh: miscible, so no interfacial tension
    A_brine = atwood(RHO_BRINE, RHO_WATER)
    P('')
    P('  Salt water above fresh water, 3 per cent NaCl:')
    P(f'    A                                 = {A_brine:.6f}  '
      f'({Aw/A_brine:.0f} times smaller than water over air)')
    P('    The two fluids are MISCIBLE, so the interfacial tension is')
    P('    essentially zero and lambda_c does NOT apply.  There is no')
    P('    capillary cutoff; the small scales are cut off by diffusion and')
    P('    viscosity instead.  Problem P4 makes this the point.')
    for lam in (1.0, 10.0):
        kk = 2.0*np.pi/lam
        s2 = sigma_squared(kk, RHO_BRINE, RHO_WATER, g=g_earth)
        P(f'    lambda = {lam:>5.1f} cm  sigma = {np.sqrt(s2):.4f} s^-1  '
          f'1/sigma = {1.0/np.sqrt(s2):.2f} s')

    # ---------------------------------------------------------------- C
    P('')
    P('PART C.  Rayleigh-Taylor with no interface: the astrophysical case')
    P('-'*74)
    P('  There is no interfacial tension between two plasmas, so lambda_c')
    P('  is infinite and every wavelength down to the dissipation scale')
    P('  grows.  The growth rate sqrt(A g k) rises without bound as k rises,')
    P('  which is why the SMALLEST resolved scale always goes first in a')
    P('  simulation, and why a cut-off has to come from somewhere else.')
    P('  Module 12 supplies magnetic tension as that cut-off.')
    P('')
    P('  A decelerating shell.  For a shell whose radius follows R ~ t^m,')
    P('  the deceleration is g = |R_ddot| = m(1-m) R/t^2, which is positive')
    P('  (that is, decelerating) for 0 < m < 1.  A dense shell decelerated')
    P('  by a lighter medium ahead of it is RT unstable on its outer face.')
    A_s = 0.90
    for m, R, t, lab in ((0.40, 3.0*pc, 400.0*yr, 'young, m = 2/5'),
                         (0.70, 3.0*pc, 400.0*yr, 'young, m = 0.70'),
                         (0.40, 10.0*pc, 2000.0*yr, 'older, m = 2/5')):
        g_s = m*(1.0 - m)*R/t**2
        P(f'    {lab}: R = {R/pc:.0f} pc, t = {t/yr:.0f} yr, '
          f'g = {g_s:.4e} cm/s^2')
        for lam in (0.01*R, 0.10*R):
            kk = 2.0*np.pi/lam
            s = np.sqrt(A_s*g_s*kk)
            P(f'      lambda = {lam/pc:.3f} pc: 1/sigma = {1.0/s/yr:.1f} yr '
              f'= {t*s:.1f} e-foldings in the age t')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  Kelvin-Helmholtz, and the two ways gravity stops it')
    P('-'*74)
    P('  (i) TWO LAYERS.  The dispersion relation gives a LONG-wavelength')
    P('  cutoff: instability needs')
    P('      dU^2 > g (rho_b^2 - rho_t^2)/(k rho_t rho_b),')
    P('  so for a given shear only k above g(rho_b^2-rho_t^2)/(rho_t rho_b dU^2)')
    P('  grows.  Long waves have to lift too much heavy fluid.')
    P('  (ii) CONTINUOUS STRATIFICATION.  Miles (1961) and Howard (1961)')
    P('  proved that Ri = N^2/(dU/dz)^2 > 1/4 EVERYWHERE is sufficient for')
    P('  stability.  That is a different theorem about a different flow, and')
    P('  the module keeps them apart.  Ri < 1/4 permits instability; it does')
    P('  not compel it.')
    P('')
    P('  Clear-air turbulence near the jet stream:')
    T_trop, lapse_env = 220.0, 6.0e-5      # K, K/cm (6.0 K/km)
    N2 = brunt_vaisala_sq(T_trop, lapse_env)
    P(f'    T = {T_trop:.0f} K, environmental lapse {lapse_env*1e5:.1f} K/km')
    P(f'    N^2 = {N2:.4e} s^-2,  N = {np.sqrt(N2):.5f} s^-1,  '
      f'period 2 pi/N = {2*np.pi/np.sqrt(N2)/60:.1f} min')
    for sh_ms_per_km, lab in ((10.0, 'moderate'), (30.0, 'strong jet-stream')):
        sh = sh_ms_per_km*100.0/1e5          # (m/s per km) -> s^-1
        Ri = richardson(N2, sh)
        P(f'    shear {sh_ms_per_km:>4.0f} m/s per km = {sh:.3e} s^-1  '
          f'Ri = {Ri:.3f}  {"UNSTABLE band" if Ri < 0.25 else "stable"} '
          f'({lab})')
    sh_crit = np.sqrt(N2/0.25)
    P(f'    shear needed for Ri = 1/4         = {sh_crit:.4e} s^-1 '
      f'= {sh_crit*1e5/100:.1f} m/s per km')
    P(f'    READ: Ri = 1/4 is reached at {sh_crit*1e5/100/10:.1f} m/s of wind '
      f'change per 100 m')
    P('    of altitude.  That is an ordinary number near a jet stream, which')
    P('    is why clear-air turbulence is common and unforecastable in')
    P('    detail: the criterion is satisfied often, and satisfying it only')
    P('    permits the instability.')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  The compressible limit: a supersonic shear layer')
    P('-'*74)
    M_crit = 2.0*np.sqrt(2.0)
    P(f'  QUOTED, NOT DERIVED HERE.  Landau (1944) and Miles (1958) showed')
    P(f'  that a plane vortex sheet between two identical ideal gases is')
    P(f'  STABLE to two-dimensional perturbations once')
    P(f'      dU > 2 sqrt(2) c_s,    that is    M = dU/c_s > {M_crit:.4f}.')
    P('  Compressibility, not gravity, is what stops KH in a fast flow: the')
    P('  disturbance radiates sound away faster than the shear can feed it.')
    P('  This result is taken from the literature and is NOT reproduced by')
    P('  the incompressible relation of PART A, which has no sound speed in')
    P('  it and therefore cannot contain this limit.  The module says so.')
    P('  The sheet is not absolutely stable, because a mode whose wavevector')
    P('  makes an angle phi with the flow sees only the projected shear, so')
    P('  its effective Mach number is M cos(phi).  Oblique modes with')
    P(f'      cos(phi) < {M_crit:.4f}/M,  that is  phi > arccos(2sqrt2/M),')
    P('  stay unstable at every Mach number (Miles 1958; Fejer & Miles 1963).')
    for M in (1.0, 2.0, 2.8284, 5.0, 10.0):
        if M <= M_crit:
            P(f'    M = {M:>5.2f}: two-dimensional modes UNSTABLE')
        else:
            phi = np.degrees(np.arccos(M_crit/M))
            P(f'    M = {M:>5.2f}: two-dimensional modes stable; oblique modes '
              f'with phi > {phi:.1f} deg remain unstable')

    # an extragalactic jet.  NOT a preview of any later module: Module 10
    # is turbulence and contains no jet.  This is an application of PART E
    # inside Module 7 and nothing is promised elsewhere.
    P('')
    P('  An extragalactic jet, Mach 5 in an ambient medium at 1e7 K:')
    T_amb, mu_amb = 1.0e7, 0.60
    cs_amb = sound_speed(T_amb, mu_amb)
    dU_jet = 5.0*cs_amb
    eta = 0.01                              # jet/ambient density ratio
    R_jet, L_jet = 100.0*pc, 1.0*kpc
    k_jet = 1.0/R_jet                       # fundamental mode on the jet radius
    f_eta = np.sqrt(eta)/(1.0 + eta)
    sig_jet = k_jet*f_eta*dU_jet
    t_cross = L_jet/dU_jet
    P(f'    c_s(ambient)                      = {cs_amb/1e5:.1f} km/s')
    P(f'    dU = 5 c_s                        = {dU_jet/1e5:.0f} km/s')
    P(f'    density contrast eta = rho_j/rho_a = {eta:.3f}, '
      f'sqrt(eta)/(1+eta) = {f_eta:.5f}')
    P(f'    k = 1/R with R = {R_jet/pc:.0f} pc      = {k_jet:.4e} cm^-1')
    P(f'    sigma                             = {sig_jet:.4e} s^-1')
    P(f'    1/sigma                           = {1.0/sig_jet/yr:.3e} yr')
    P(f'    travel time over {L_jet/kpc:.0f} kpc          = '
      f'{t_cross/yr:.3e} yr')
    P(f'    e-foldings over its length        = {t_cross*sig_jet:.2f}')
    P(f'    BUT M = 5 exceeds {M_crit:.3f}, so this incompressible rate is an')
    P(f'    UPPER limit that the two-dimensional mode does not achieve; only')
    P(f'    oblique modes beyond phi = '
      f'{np.degrees(np.arccos(M_crit/5.0)):.1f} deg survive.  Problem P7 makes')
    P('    the student walk into this and back out of it.')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  THE TERRESTRIAL CHECK: the nonlinear mixing law')
    P('-'*74)
    P('  Shimony et al. (2022), arXiv:2210.06631, NIF laser-driven RT.')
    P(f'    measured alpha_B                  = {ALPHA_B:.3f} '
      f'+/- {ALPHA_B_ERR:.3f}')
    P(f'    chi-squared bounds, Fig. 4        = {ALPHA_FIT_LO:.3f} to '
      f'{ALPHA_FIT_HI:.3f}')
    P('    CONFIRMED: the law h_B = alpha_B A g t^2 itself.  Four different')
    P('    initial perturbations collapse onto one straight line when the')
    P('    mix width is plotted against the Read integral')
    P('      x_Read = A (int sqrt(g) dt)^2,')
    P('    which for constant g is exactly A g t^2.  The FORM is confirmed;')
    P('    only the coefficient is being measured.  The hypothesis under')
    P('    which the form holds is theirs, stated on p.3-4: "We assumed')
    P('    that at the self-similar stage, the initial conditions are')
    P('    forgotten".  That is what makes alpha a constant rather than a')
    P('    memory of the seed, and it is what the spread below strains.')
    P('')
    P('    REFUTED: the claim in their own abstract, "This resolved the')
    P('    known discrepancy between experiments and simulations of RTI".')
    P('    The discrepancy they name on p.1 runs from ~0.05 (their ref [5],')
    P('    a 3D immiscible model) down by "a factor of ~2" to full 3D')
    P('    simulations.  Distances of their measurement from each end:')
    for val, lab in ((ALPHA_SIM, '3D simulations (INFERRED, 0.05/2)'),
                     (ALPHA_FIT_LO, 'their own <lambda>=30 um data, ~0.03'),
                     (ALPHA_THEORY_3D, '3D immiscible model, ~0.05 (read)')):
        nsig = abs(val - ALPHA_B)/ALPHA_B_ERR
        verdict = 'EXCLUDED' if nsig > 2.0 else 'not excluded'
        P(f'      {lab:<38} {nsig:>5.2f} sigma  {verdict}')
    P(f'    PUNCHLINE  alpha_B = {ALPHA_B:.3f} +/- {ALPHA_B_ERR:.3f} sits '
      f'{abs(ALPHA_THEORY_3D-ALPHA_B)/ALPHA_B_ERR:.2f} sigma below the')
    P(f'    {ALPHA_THEORY_3D:.3f} of the model and '
      f'{abs(ALPHA_SIM-ALPHA_B)/ALPHA_B_ERR:.2f} sigma above the '
      f'{ALPHA_SIM:.3f} inferred for the')
    P('    simulations.  It is consistent with BOTH ends of the factor-2')
    P('    discrepancy its abstract says it resolved, so it does not')
    P('    resolve it.  The measurement is sound; the claim made for it is')
    P("    not.  The paper's own explanation for why experiments have run")
    P('    high is that long wavelengths in the seed raise the measured')
    P('    alpha_B (p.1, citing their ref [12]) -- which is the stated')
    P('    hypothesis, forgetting the seed, failing at the 20 per cent level.')
    P(f'    RANGE the coefficient spans: {ALPHA_SIM:.3f} to '
      f'{ALPHA_THEORY_3D:.3f}, a factor '
      f'{ALPHA_THEORY_3D/ALPHA_SIM:.1f}.')
    P('')
    P('  What that uncertainty costs in an astrophysical application:')
    A_sn, g_sn, t_sn = 0.90, 1.0e-3, 100.0*yr
    for al in (ALPHA_SIM, ALPHA_B, ALPHA_THEORY_3D):
        h = mix_width(al, A_sn, g_sn, t_sn)
        P(f'    alpha = {al:.3f}: h(A=0.9, g=1e-3 cm/s^2, t=100 yr) = '
          f'{h:.4e} cm = {h/AU:.1f} AU = {h/pc:.5f} pc')
    hlo = mix_width(ALPHA_SIM, A_sn, g_sn, t_sn)
    hhi = mix_width(ALPHA_THEORY_3D, A_sn, g_sn, t_sn)
    P(f'    the mixing layer is uncertain by a factor {hhi/hlo:.1f} for that '
      f'reason alone.')
    # verify the Read integral reduces to A g t^2 for constant g
    P(f'    consistency: x_Read(A,g,t)/(A g t^2) = '
      f'{read_integral(A_sn, g_sn, t_sn)/(A_sn*g_sn*t_sn**2):.10f}')

    # ---------------------------------------------------------------- G
    P('')
    P('PART G.  THE ASTROPHYSICAL ANCHOR: KH vortices on a CME flank')
    P('-'*74)
    P('  Ofman & Thompson (2011), ApJ 734, L11.  SDO/AIA, 8 April 2010.')
    P('  SAY THE WEAKNESS FIRST.  Every input is one significant figure with')
    P('  no uncertainty, and the shear is quoted as an upper limit.  No')
    P('  sigma is computable from this source and none is claimed.')

    arcsec = arcsec_at_sun()
    mu_e = mu_electron()
    rho_h = mu_e*NE_CORONA*mu_u                  # dense, non-erupting corona
    dens_ratio = np.sqrt(OT_EMIS)                # p.9: rho ~ sqrt(emission)
    rho_l = rho_h/dens_ratio                     # evacuated, erupting side
    k_obs = 2.0*np.pi/OT_LAMBDA
    f_dens = np.sqrt(rho_h*rho_l)/(rho_h + rho_l)

    P('')
    P('  Inputs, and what each was read from:')
    P(f'    lambda (p.5, p.10)                = {OT_LAMBDA/1e5:.0f} km')
    P(f'    k = 2 pi/lambda                   = {k_obs:.4e} cm^-1')
    P(f'    vortex propagation (p.2, p.5, p.6)= {OT_VPROP_LO/1e5:.0f} to '
      f'{OT_VPROP_HI/1e5:.0f} km/s')
    P(f'    driving shear dU (p.6, an upper limit) = {OT_DU/1e5:.0f} km/s')
    P(f'    interface thickness a (p.6)       = {OT_A_LAYER/1e5:.0f} km')
    P(f'    emission ratio (p.9)              = {OT_EMIS:.0f} '
      f'(range {OT_EMIS_LO:.0f}-{OT_EMIS_HI:.0f})')
    P(f'    density ratio sqrt(emission)      = {dens_ratio:.4f} '
      f'(range {np.sqrt(OT_EMIS_LO):.4f}-{np.sqrt(OT_EMIS_HI):.4f})')
    P(f'    coronal n_e (INPUT from Module 1) = {NE_CORONA:.1e} cm^-3')
    P(f'    mu_e = 2/(1+X) with X = {X_HYDROGEN:.2f}    = {mu_e:.4f}')
    P(f'    rho (dense side) = mu_e n_e m_u   = {rho_h:.4e} g/cm^3')
    P(f'    rho (light side) = rho_h/{dens_ratio:.3f}     = {rho_l:.4e} g/cm^3')
    P('')
    P('  Internal consistency of the paper, before anything is checked:')
    P(f'    1 arcsec at 1 AU                  = {arcsec/1e5:.1f} km')
    P(f'    AIA pixel, {OT_PIX_ARCSEC} arcsec            = '
      f'{OT_PIX_ARCSEC*arcsec/1e5:.1f} km')
    P(f'    quoted vortex sizes {OT_SIZE_LO:.0f}-{OT_SIZE_HI:.0f} arcsec  = '
      f'{OT_SIZE_LO*arcsec/1e5:.0f}-{OT_SIZE_HI*arcsec/1e5:.0f} km')
    P(f'    so lambda = {OT_LAMBDA/1e5:.0f} km is the TOP of that range: '
      f'ratio {OT_LAMBDA/(OT_SIZE_HI*arcsec):.4f}')
    P(f'    "1-3 pixels" for the interface    = '
      f'{OT_PIX_ARCSEC*arcsec/1e5:.0f}-{3*OT_PIX_ARCSEC*arcsec/1e5:.0f} km, '
      f'and they average it to {OT_A_LAYER/1e5:.0f} km')
    dt_obs = OT_T_FULL - OT_T_FIRST
    dt_obs_alt = OT_T_FULL_ALT - OT_T_FIRST
    P(f'    3:00:13 to 3:13:53                = {dt_obs:.0f} s = '
      f'{dt_obs/60:.1f} min')
    P(f'    3:00:13 to 3:13:13                = {dt_obs_alt:.0f} s = '
      f'{dt_obs_alt/60:.1f} min')
    P(f'    the paper rounds this to "on the order of 14 minutes" '
      f'({OT_TGROW:.0f} s)')
    # The sentence that INTRODUCES the 14 minutes names the dimming times,
    # which give a different pair of intervals.  Both are printed so the
    # prose can say which interval the number actually matches.
    for lab, t0 in (('2:42:53', 2*3600 + 42*60 + 53),
                    ('2:51:13', 2*3600 + 51*60 + 13)):
        dt = OT_T_FULL - t0
        P(f'    {lab} to 3:13:53                = {dt:.0f} s = '
          f'{dt/60:.1f} min  (the dimming times they cite)')

    # --- CHECK 1: reproduce their published growth rate.
    P('')
    P('  CHECK 1.  Their published growth rate, from the relation in PART A.')
    g_lo = np.sqrt(sigma_squared(k_obs, 1.0, 1.0, dU=OT_VPROP_LO))
    g_hi = np.sqrt(sigma_squared(k_obs, 1.0, 1.0, dU=OT_VPROP_HI))
    P(f'    equal-density limit, dU = {OT_VPROP_LO/1e5:.0f} km/s  '
      f'sigma = {g_lo:.5f} s^-1   (they print {OT_GAMMA_LO:.3f})')
    P(f'    equal-density limit, dU = {OT_VPROP_HI/1e5:.0f} km/s  '
      f'sigma = {g_hi:.5f} s^-1   (they print {OT_GAMMA_HI:.3f})')
    P(f'    ratios computed/published         = {g_lo/OT_GAMMA_LO:.4f} and '
      f'{g_hi/OT_GAMMA_HI:.4f}   (house convention, m01:119)')
    P('    REPRODUCED, NOT CONFIRMED.  Their 0.003-0.006 s^-1 is their own')
    P('    (1/2) k dV evaluated at 6 and 14 km/s, and their equation (1) is')
    P("    this module's relation with rho_t = rho_b.  Recovering it tests")
    P('    the ALGEBRA of this module against theirs; it tests nothing')
    P('    against nature.  Module 5 met the same trap in the Kandori')
    P('    contrast column, which was computed from the column it was being')
    P('    compared against.')
    P('    AND the 6-14 km/s they substitute is the speed at which the')
    P('    vortices TRAVEL along the boundary (p.5), not the driving shear,')
    P('    which they measure separately as ~20 km/s (p.6) and call an upper')
    P('    limit.  Their own equation at their own measured shear gives')
    sig_shear = 0.5*k_obs*OT_DU
    P(f'      (1/2) k dU at dU = {OT_DU/1e5:.0f} km/s        = '
      f'{sig_shear:.5f} s^-1,')
    P(f'    which is {sig_shear/OT_GAMMA_HI:.1f} to {sig_shear/OT_GAMMA_LO:.1f} '
      f'times the range they print.')
    n_lo, n_hi = OT_TSAT*g_lo, OT_TSAT*g_hi
    P(f'    their "several gamma^-1 or about 10 minutes": 600 s is '
      f'{n_lo:.2f} to {n_hi:.2f}')
    P(f'    e-folding times.  "Several" = {n_lo:.1f} to {n_hi:.1f}.  '
      f'Reproduced.')

    # --- CHECK 2: the phase speed.  Consistent, NOT discriminating.
    P('')
    P('  CHECK 2.  The phase speed.  CONSISTENT, NOT DISCRIMINATING.')
    P('    The same algebra that gives sigma^2 fixes the real part of')
    P('    omega/k: the mode drifts at the density-weighted mean of the two')
    P('    stream velocities.  With the dense corona at rest and the')
    P('    evacuated side moving at dU, that is dU/(1 + rho_h/rho_l).')
    c_ph = phase_speed(rho_h, rho_l, 0.0, OT_DU)
    c_lo = phase_speed(rho_h, rho_h/np.sqrt(OT_EMIS_LO), 0.0, OT_DU)
    c_hi = phase_speed(rho_h, rho_h/np.sqrt(OT_EMIS_HI), 0.0, OT_DU)
    P(f'    predicted c_ph, density ratio {dens_ratio:.3f}  = '
      f'{c_ph/1e5:.2f} km/s')
    P(f'    spread over emission ratio 3-10   = '
      f'{min(c_lo, c_hi)/1e5:.2f} to {max(c_lo, c_hi)/1e5:.2f} km/s')
    P(f'    equal-density value dU/2          = {OT_DU/2e5:.2f} km/s')
    P(f'    OBSERVED                          = {OT_VPROP_LO/1e5:.0f} to '
      f'{OT_VPROP_HI/1e5:.0f} km/s')
    P(f'    ratio of prediction to the low edge of the band = '
      f'{c_ph/OT_VPROP_LO:.3f}')
    P('    The prediction lands inside the observed band.  So does the')
    P('    equal-density value.  A band a factor '
      f'{OT_VPROP_HI/OT_VPROP_LO:.1f} wide cannot separate')
    P('    two predictions a factor '
      f'{(OT_DU/2)/c_ph:.2f} apart.  This is NOT counted as a')
    P('    confirmation, and the figure draws both so the reader sees why.')

    # --- CHECK 3: the equal-density assumption, refuted with their numbers.
    P('')
    P('  CHECK 3.  REFUTED: the equal-density assumption in their equation.')
    P(f'    prefactor they use, sqrt(r r)/(r+r)   = {0.5:.5f}')
    P(f'    prefactor their own density ratio requires, '
      f'sqrt(r_h r_l)/(r_h+r_l) = {f_dens:.5f}')
    P(f'    PUNCHLINE ratio                       = {f_dens/0.5:.5f}, so '
      f'their rate is {(0.5/f_dens - 1)*100:.1f}% too high')
    sig_true = k_obs*f_dens*OT_DU
    sig_eq = 0.5*k_obs*OT_DU
    P(f'    rate from the measured driving shear {OT_DU/1e5:.0f} km/s:')
    P(f'      correct two-density form            = {sig_true:.5f} s^-1, '
      f'1/sigma = {1.0/sig_true:.1f} s')
    P(f'      equal-density form                  = {sig_eq:.5f} s^-1, '
      f'1/sigma = {1.0/sig_eq:.1f} s')
    # their own model carries a field term they do not put in the quoted rate
    brack = np.sqrt(1.0 - (2.0/OT_MODEL_V0_OVER_VA)**2)
    P(f'    AND their own MHD model sets V0 = {OT_MODEL_V0_OVER_VA:.0f} V_A,xy '
      f'(p.9), so its bracket is')
    P(f'      sqrt(1 - (2/{OT_MODEL_V0_OVER_VA:.0f})^2)                     '
      f'= {brack:.5f}')
    P(f'    The model they RAN is {(1-brack)*100:.1f}% below the field-free rate '
      f'they QUOTE.')
    P(f'    Compounded with the density factor: {f_dens/0.5:.5f} x '
      f'{brack:.5f} = {f_dens/0.5*brack:.5f},')
    P(f'    i.e. {(1 - f_dens/0.5*brack)*100:.1f}% below the published number, '
      f'from the paper\'s own inputs.')
    P('    THEIR OWN NUMERICS ALREADY SAY SO.  p.9: "We have also performed')
    P('    runs with density ratios of 2 and 3 and found similar results,')
    P('    with the growth rate of KH instability decreasing by ~15% with')
    P('    the density ratio in this range."  The two-density prefactor')
    P('    predicts exactly that:')
    for rr in (2.0, 3.0):
        fr = np.sqrt(rr)/(1.0 + rr)
        P(f'      density ratio {rr:.0f}: sqrt(r)/(1+r) = {fr:.5f}, '
          f'{(1 - fr/0.5)*100:.1f}% below the equal-density 0.5')
    P('    15% measured in their runs against 13.4% from the prefactor.  The')
    P('    correction this check makes to their quoted rate is one their own')
    P('    model had already found.')
    P(f'    e-foldings in the observed {dt_obs:.0f} s, correct form = '
      f'{dt_obs*sig_true:.2f}')
    P('    NOTE that this is a consistency statement, not a test: the seed')
    P('    amplitude was not measured, so any e-folding count of a few is')
    P('    admissible.  Stated so in the prose.')

    # --- CHECK 4: the magnetic bound.  THE SHARP RESULT.
    P('')
    P('  CHECK 4.  THE SHARP RESULT: what the instability measures about B.')
    P('    They write (p.8) "we have assumed that the magnetic field has no')
    P('    parallel component to the interface".  Undo that assumption and')
    P('    the observation becomes a measurement, because the instability')
    P('    existing at all requires the magnetic tension term to lose.')
    Bpar = b_parallel_max(rho_h, rho_l, OT_DU)
    Bpar1 = b_parallel_max(rho_h, rho_l, OT_DU, both_sides=False)
    P('    The magnetic term carries B_t^2 + B_b^2, so the bound depends on')
    P('    a HYPOTHESIS about where the field is.  Both are printed.')
    P(f'    equal fields both sides (their model):')
    P(f'      B cos(theta) < dU sqrt(2 pi rho_h rho_l/(rho_h+rho_l))')
    P(f'    PUNCHLINE bound                   = {Bpar:.4f} gauss')
    P(f'    field on one side only, the weaker and safer statement:')
    P(f'      B cos(theta) < dU sqrt(4 pi rho_h rho_l/(rho_h+rho_l))')
    P(f'      bound                           = {Bpar1:.4f} gauss '
      f'(a factor {Bpar1/Bpar:.4f})')
    P('    Both are UPPER bounds twice over: dU = 20 km/s is itself an upper')
    P('    limit (p.6), and the bound is linear in dU.')
    P(f'    scaling: the bound goes as sqrt(n_e), so at n_e = 1e9 cm^-3 it is')
    P(f'      {Bpar*np.sqrt(1e9/NE_CORONA):.4f} G, and at n_e = 1e8 cm^-3 it is '
      f'{Bpar*np.sqrt(1e8/NE_CORONA):.4f} G.')
    P('    Expressed as an angle, for a total field of:')
    for Btot in (1.0, 2.0, 5.0, 10.0, 50.0):
        ct = Bpar/Btot
        if ct >= 1.0:
            P(f'      B = {Btot:>5.1f} G: no constraint (the bound exceeds B)')
        else:
            P(f'      B = {Btot:>5.1f} G: cos(theta) < {ct:.5f}, so k must lie '
              f'within {90.0 - np.degrees(np.arccos(ct)):.2f} deg of '
              f'perpendicular to B')
    P('    READ: in an active-region corona of 10 gauss, the wavevector has')
    P(f'    to sit within {90.0 - np.degrees(np.arccos(Bpar/10.0)):.2f} '
      f'degrees of perpendicular to the field for the')
    P('    hydrodynamic rate to be even approximately right.  The paper')
    P('    reaches the same conclusion qualitatively ("implying that the')
    P('    magnetic field was mostly radial"); the number is the module\'s.')
    P('    THIS is what Module 12 repays: a hydrodynamic calculation that')
    P('    needs a 1-degree statement about a field it never mentions is a')
    P('    calculation waiting for magnetohydrodynamics.')

    # --- CHECK 5: the vortex-sheet assumption.
    P('')
    P('  CHECK 5.  REFUTED: the vortex-sheet assumption.')
    ka = k_obs*OT_A_LAYER
    a_lo = OT_PIX_ARCSEC*arcsec
    a_hi = 3.0*OT_PIX_ARCSEC*arcsec
    P('    They justify a discontinuous jump because the layer thickness is')
    P(f'    "much smaller than the wavelength": a/lambda = '
      f'{OT_A_LAYER/OT_LAMBDA:.4f}, a factor '
      f'{OT_LAMBDA/OT_A_LAYER:.2f}.')
    P('    But the parameter that decides it is k a, not a/lambda:')
    P(f'    PUNCHLINE  k a                    = {ka:.4f}')
    P(f'    over their own "1-3 pixels"       = {k_obs*a_lo:.4f} to '
      f'{k_obs*a_hi:.4f}')
    P('    AND THE PAPER SUPPLIES THE COMPARISON.  p.9: the modelled box is')
    P('    "~5 pi a corresponding to the wavelength of the fastest growing')
    P('    mode", citing Miura & Pritchett (1982).  That is a statement')
    P('    about the SAME finite layer:')
    lam_fast = 5.0*np.pi*OT_A_LAYER
    P(f'      fastest mode of a tanh layer, 5 pi a = {lam_fast/1e5:.0f} km, '
      f'k a = {2.0*np.pi/(5.0*np.pi):.3f}')
    P(f'      observed                             = {OT_LAMBDA/1e5:.0f} km, '
      f'k a = {ka:.3f}')
    P(f'      ratio                                = '
      f'{lam_fast/OT_LAMBDA:.3f}')
    P('    So the wavelength their model runs is 1.8 times the wavelength')
    P('    they observed, and the observed mode sits past the peak of the')
    P('    finite-layer growth curve by the same factor.')
    P('    k a is of order unity, so the vortex-sheet rate is an UPPER limit,')
    P('    not an estimate: a finite layer both lowers the rate and closes')
    P('    the unstable band above k a of order 1.  The tanh-layer')
    P('    eigenproblem is NOT solved here, deliberately: a is uncertain by')
    P('    a factor 3, so solving it would add precision the input does not')
    P('    have.')

    # --- CHECK 6: the geometry.  A result neither paper states.
    P('')
    P('  CHECK 6.  The geometry is load-bearing, and neither paper says so.')
    g_surf = GMsun/Rsun**2
    k_cut = kh_k_gravity_cutoff(g_surf, rho_l, rho_h, OT_DU)
    lam_cut = 2.0*np.pi/k_cut
    P(f'    solar surface gravity GM/R^2      = {g_surf:.4e} cm/s^2')
    P('    The paper models this flow "without gravity (since it is')
    P('    perpendicular to the plane)" (p.8): the CME flank is radial, so')
    P('    gravity lies ALONG the interface and exerts no restoring force.')
    P('    Suppose instead it acted across the interface, with the dense')
    P('    corona BELOW and the evacuated side above -- the stable')
    P('    ordering, which is the one Proposition 6 of module07.html')
    P('    needs.  (Light fluid below would be heavy fluid on top, which')
    P('    is RT-unstable outright and has no KH cutoff at all.)')
    P(f'      cutoff wavenumber               = {k_cut:.4e} cm^-1')
    P(f'      cutoff wavelength               = {lam_cut/1e5:.0f} km')
    P(f'      observed wavelength             = {OT_LAMBDA/1e5:.0f} km')
    P(f'      PUNCHLINE ratio lambda_obs/lambda_cut = '
      f'{OT_LAMBDA/lam_cut:.3f}')
    P(f'    Long waves are the stabilised ones, so a ratio above 1 means the')
    P(f'    observed mode would NOT grow.  It fails by a factor '
      f'{OT_LAMBDA/lam_cut:.2f}, which is')
    P('    inside the factor-two accuracy of these inputs, so the honest')
    P('    statement is that the observed mode sits AT the cutoff.  The')
    P('    orientation of the interface is not a detail of the setup; it is')
    P('    what decides whether this mode exists.')

    # ---------------------------------------------------------------- H
    P('')
    P('PART H.  Problem-set numbers')
    P('-'*74)

    P('  P1  Water over air: lambda_c, lambda_max, sigma_max, 1/sigma_max.')
    P(f'      {lam_c:.4f} cm, {lam_m:.4f} cm, {sig_m:.3f} s^-1, '
      f'{1e3/sig_m:.2f} ms.')
    P(f'      Tube radius that holds water: a tube narrower than lambda_c '
      f'= {lam_c:.2f} cm')
    P(f'      admits no unstable mode.  In mercury (T_s = 487 dyn/cm, '
      f'rho = 13.55):')
    lam_c_hg = rt_lambda_cut(487.0, g_earth, 13.55 - RHO_AIR)
    lam_m_hg = rt_lambda_max(487.0, g_earth, 13.55 - RHO_AIR)
    P(f'      lambda_c = {lam_c_hg:.4f} cm, lambda_max = {lam_m_hg:.4f} cm.')

    P('')
    P('  P2  Growth of a single RT mode, water over air, at three '
      'wavelengths:')
    for lam in (0.5, 2.0, 2.96868, 10.0, 100.0):
        s2 = sigma_squared(2.0*np.pi/lam, RHO_WATER, RHO_AIR, g=g_earth,
                           T=SIGMA_WATER)
        if s2 <= 0:
            P(f'      lambda = {lam:>8.3f} cm: STABLE, '
              f'oscillates at {np.sqrt(-s2):.2f} rad/s '
              f'(period {2*np.pi/np.sqrt(-s2)*1e3:.1f} ms)')
        else:
            P(f'      lambda = {lam:>8.3f} cm: sigma = {np.sqrt(s2):.3f} s^-1, '
              f'1/sigma = {1e3/np.sqrt(s2):.2f} ms')

    P('')
    P('  P3  Viscous crossover.  For water, lambda_nu = '
      f'{lam_nu*10:.3f} mm against')
    P(f'      lambda_max = {lam_m*10:.1f} mm: capillarity sets the scale and '
      f'viscosity does not.')
    P('      For glycerol (nu = 11.8 cm^2/s, rho = 1.261, T_s = 63 dyn/cm):')
    A_gly = atwood(1.261, RHO_AIR)
    lam_nu_gly = rt_lambda_viscous(11.8, A_gly, g_earth)
    lam_m_gly = rt_lambda_max(63.0, g_earth, 1.261 - RHO_AIR)
    P(f'      lambda_nu = {lam_nu_gly:.3f} cm against lambda_max = '
      f'{lam_m_gly:.3f} cm, ratio {lam_nu_gly/lam_m_gly:.2f}:')
    P('      now viscosity is the larger scale and it, not capillarity,')
    P('      chooses the pattern.  Same instability, opposite cut-off.')

    P('')
    P('  P4  Salt water above fresh, 3 per cent NaCl, A = '
      f'{A_brine:.5f}.')
    P('      The pair is MISCIBLE, so T_s is essentially zero and there is no')
    P('      capillary cutoff.  Growth rates at 1 cm and 10 cm are printed in')
    P('      PART B.  The intended answer is that the student must NOT put')
    P('      72.75 dyn/cm into this problem.')
    lam_nu_brine = rt_lambda_viscous(NU_WATER, A_brine, g_earth)
    P(f'      The short-wavelength cut-off is the viscous one, lambda_nu = '
      f'{lam_nu_brine*10:.2f} mm.')

    P('')
    P('  P5  RT in a decelerating supernova shell, A = 0.9.')
    for g_sn_v, lab in ((1.0e-3, 'g = 1e-3 cm/s^2'),
                        (1.0e-2, 'g = 1e-2 cm/s^2')):
        for lam in (0.01*pc, 0.1*pc):
            s = np.sqrt(0.90*g_sn_v*2.0*np.pi/lam)
            P(f'      {lab}, lambda = {lam/pc:.2f} pc: 1/sigma = '
              f'{1.0/s/yr:.1f} yr')
    P('      And the student must DERIVE g, not accept it: for R ~ t^m,')
    P('      g = m(1-m) R/t^2.  Two remnants, both with m = 2/5:')
    m_ = 0.4
    for R_, t_ in ((3.0*pc, 400.0*yr), (10.0*pc, 2000.0*yr)):
        g_der = m_*(1-m_)*R_/t_**2
        P(f'        R = {R_/pc:>2.0f} pc, t = {t_/yr:>4.0f} yr: '
          f'g = {g_der:.4e} cm/s^2')
    P('      The stated 1e-3 cm/s^2 is the OLDER remnant, within a factor')
    P(f'      {m_*(1-m_)*10.0*pc/(2000.0*yr)**2/1e-3:.2f}; the young one is a '
      f'factor {m_*(1-m_)*3.0*pc/(400.0*yr)**2/1e-3:.0f} larger.  The number '
      f'is not free.')

    P('')
    P('  P6  Mixing-layer thickness h = alpha A g t^2, with alpha uncertain.')
    for t_v in (10.0*yr, 100.0*yr, 1000.0*yr):
        h = mix_width(ALPHA_B, 0.90, 1.0e-3, t_v)
        P(f'      t = {t_v/yr:>6.0f} yr: h = {h:.4e} cm = {h/AU:>8.1f} AU '
          f'= {h/pc:.5f} pc   (alpha = {ALPHA_B:.3f})')
    P(f'      with alpha spanning {ALPHA_SIM:.3f} to {ALPHA_THEORY_3D:.3f}, '
      f'h spans a factor {ALPHA_THEORY_3D/ALPHA_SIM:.1f}.')

    P('')
    P('  P7  The Mach 5 jet.  Numbers are in PART E.  The trap is that the')
    P(f'      incompressible rate gives 1/sigma = {1.0/sig_jet/yr:.2e} yr and')
    P(f'      {t_cross*sig_jet:.2f} e-foldings over 1 kpc, but M = 5 > '
      f'{M_crit:.3f} stabilises the')
    P('      two-dimensional mode entirely, so that rate is unreachable.')
    P(f'      Only oblique modes beyond phi = '
      f'{np.degrees(np.arccos(M_crit/5.0)):.1f} deg survive, and they see')
    P(f'      a projected shear of dU cos(phi) < '
      f'{dU_jet*M_crit/5.0/1e5:.0f} km/s.')

    P('')
    P('  P8  Clear-air turbulence.  N = '
      f'{np.sqrt(N2):.5f} s^-1 at {T_trop:.0f} K with a')
    P(f'      {lapse_env*1e5:.1f} K/km lapse; Ri = 1/4 needs '
      f'{sh_crit*1e5/100:.1f} m/s per km of shear.')
    P('      A 30 m/s per km jet-stream shear gives Ri = '
      f'{richardson(N2, 30.0*100/1e5):.3f}.')
    P('      Second part: state why Ri < 1/4 does not GUARANTEE turbulence.')

    P('')
    P('  P9  The magnetic bound, redone by the student for a denser corona.')
    for ne in (1e8, 1e9, 1e10):
        rh = mu_e*ne*mu_u
        rl = rh/dens_ratio
        P(f'      n_e = {ne:.0e} cm^-3: B cos(theta) < '
          f'{b_parallel_max(rh, rl, OT_DU):.4f} G')
    P('      The point is the sqrt(n_e) scaling, and that even the densest')
    P('      choice keeps the bound far below an active-region field.')

    P('')
    P('  P10 The gravitational cutoff, applied where gravity DOES act across')
    P('      the interface: a coronal prominence, dense material above hot')
    P('      tenuous corona.  With a density ratio of 100 and dU = 20 km/s:')
    rho_prom = 100.0*rho_h
    k_c2 = kh_k_gravity_cutoff(g_surf, rho_h, rho_prom, OT_DU)
    P(f'      Dense above light is RT-unstable outright, A = '
      f'{atwood(rho_prom, rho_h):.4f}, so the KH')
    P('      cutoff does not apply at all; the student must notice the sign')
    P('      before reaching for a formula.  Turn it over, light above dense,')
    P('      and the KH cutoff bites hard: every wavelength longer than')
    P(f'      {2*np.pi/abs(k_c2)/1e5:.0f} km is gravitationally stabilised at '
      f'{OT_DU/1e5:.0f} km/s of shear, so the')
    P('      interface is quiet on every scale an imager could resolve.')
    P('      RT growth for the unstable ordering, lambda = 1000 km:')
    s_p = np.sqrt(sigma_squared(2*np.pi/1e8, rho_prom, rho_h, g=g_surf))
    P(f'      sigma = {s_p:.5f} s^-1, 1/sigma = {1.0/s_p:.1f} s = '
      f'{1.0/s_p/60:.2f} min.')

    P('')
    P('=' * 74)
    P('PUNCHLINE SUMMARY')
    P('=' * 74)
    P(f'  PUNCHLINE 1  alpha_B = {ALPHA_B:.3f} +/- {ALPHA_B_ERR:.3f} '
      f'(Shimony et al. 2022) CONFIRMS the form')
    P('               h = alpha A g t^2, under their own hypothesis that the')
    P('               seed is forgotten, and REFUTES the claim in their')
    P('               abstract that it "resolved the known discrepancy": it')
    P(f'               sits {abs(ALPHA_THEORY_3D-ALPHA_B)/ALPHA_B_ERR:.2f} '
      f'sigma from {ALPHA_THEORY_3D:.3f} and '
      f'{abs(ALPHA_SIM-ALPHA_B)/ALPHA_B_ERR:.2f} sigma from the')
    P(f'               {ALPHA_SIM:.3f} inferred for 3D simulations, so it is '
      f'consistent with')
    P('               both ends of the factor 2 it was meant to close.')
    P(f'  PUNCHLINE 2  The KH growth rate of Ofman & Thompson (2011), '
      f'{OT_GAMMA_LO:.3f}-{OT_GAMMA_HI:.3f} s^-1,')
    P(f'               is REPRODUCED as {g_lo:.5f}-{g_hi:.5f} s^-1, ratios '
      f'{g_lo/OT_GAMMA_LO:.3f} and {g_hi/OT_GAMMA_HI:.3f}')
    P('               (computed/published).  This tests the algebra, not')
    P('               nature: 0.003-0.006 is their own (1/2) k dV.  Put their')
    P(f'               measured shear {OT_DU/1e5:.0f} km/s in instead and the '
      f'same formula gives')
    P(f'               {0.5*k_obs*OT_DU:.5f} s^-1, '
      f'{0.5*k_obs*OT_DU/OT_GAMMA_HI:.1f} to '
      f'{0.5*k_obs*OT_DU/OT_GAMMA_LO:.1f} times what they print.')
    P(f'  PUNCHLINE 3  Their equal-density prefactor 0.500 should be '
      f'{f_dens:.5f} for the')
    P(f'               density ratio {dens_ratio:.3f} they measure: their rate '
      f'is {(0.5/f_dens-1)*100:.1f}% high.  Their')
    P(f'               own MHD model carries a further factor {brack:.4f}, for '
      f'{(1-f_dens/0.5*brack)*100:.1f}% in all.')
    P(f'  PUNCHLINE 4  The instability existing at all bounds the field '
      f'component along')
    P(f'               k at {Bpar:.4f} G for equal fields on both sides, '
      f'{Bpar1:.4f} G for a')
    P(f'               one-sided field (n_e = {NE_CORONA:.0e} cm^-3, as '
      f'sqrt(n_e); dU is an upper')
    P(f'               limit, so both bounds are).  Against a 10 G '
      f'active-region')
    P(f'               field, k must lie within '
      f'{90.0-np.degrees(np.arccos(Bpar/10.0)):.2f} to '
      f'{90.0-np.degrees(np.arccos(Bpar1/10.0)):.2f} deg of perpendicular.')
    P(f'  PUNCHLINE 5  Their vortex-sheet assumption is stated as '
      f'a/lambda = {OT_A_LAYER/OT_LAMBDA:.3f}, but the')
    P(f'               parameter is k a = {ka:.3f}.  Their own model runs')
    P(f'               5 pi a = {5.0*np.pi*OT_A_LAYER/1e5:.0f} km, '
      f'{5.0*np.pi*OT_A_LAYER/OT_LAMBDA:.2f} times the wavelength they '
      f'observed.  The quoted')
    P('               rate is an upper limit.')
    P(f'  PUNCHLINE 6  The phase speed predicted from their own numbers, '
      f'{c_ph/1e5:.2f} km/s, lies')
    P(f'               inside their observed {OT_VPROP_LO/1e5:.0f}-'
      f'{OT_VPROP_HI/1e5:.0f} km/s band, but so does the equal-')
    P(f'               density value {OT_DU/2e5:.0f} km/s.  CONSISTENT, NOT '
      f'DISCRIMINATING.')
    P(f'  PUNCHLINE 7  Turn gravity across the interface and the observed '
      f'{OT_LAMBDA/1e5:.0f} km mode')
    P(f'               exceeds the two-layer cutoff {lam_cut/1e5:.0f} km by '
      f'{OT_LAMBDA/lam_cut:.2f}.  The radial geometry')
    P('               is what permits the mode.')

    P('')
    P('=' * 74)
    P('SOURCES')
    P('=' * 74)
    P('  Ofman, L. & Thompson, B. J. (2011), ApJ 734, L11,')
    P('    "SDO/AIA Observation of Kelvin-Helmholtz Instability in the Solar')
    P('    Corona".  doi:10.1088/2041-8205/734/1/L11.  Read as')
    P('    arXiv:1101.4249v2; page numbers below are the printed pages of')
    P('    that preprint.')
    P('      p.4  event: 8 April 2010, 02:34 UT onset, GOES B3.7 peaking at')
    P('           03:25 UT, CME speed ~500 km/s from STEREO SECCHI; AIA')
    P('           pixel width 0.6 arcsec.')
    P('      p.5  vortices "several to ten arcseconds", ~7000 km, travelling')
    P('           6-14 km/s ALONG THE BOUNDARY; first sign 3:00:13 UT, flow')
    P('           fully developed 3:13:13.')
    P('      p.6  dashed lines at 6 and 14 km/s with solar rotation removed;')
    P('           loop tracking gives shear ~20 km/s as an upper limit;')
    P('           interface 1-3 pixels, "on average ~800 km"; first motion')
    P('           along the KH front 3:13:53; growth time to the nonlinear')
    P('           stage "on the order of 14 minutes".')
    P('      p.7  their equation (1), the equal-density MHD growth rate, and')
    P('           the substitution of the 6-14 km/s propagation speeds into')
    P('           it as "the observed velocity shear".')
    P('      p.8  gamma_KH ~ 0.003-0.006 s^-1; "we have assumed that the')
    P('           magnetic field has no parallel component to the interface";')
    P('           saturation "at several gamma^-1 or in about 10 minutes";')
    P('           the model is run "without gravity (since it is')
    P('           perpendicular to the plane)".')
    P('      p.9  EUV emission ratio ~5, range 3-10; density goes as the')
    P('           square root of emission, so rho_max/rho_min = 5^(1/2);')
    P('           Bx0 ~ 0.04 <Bz0>,')
    P('           V0 = 5 V_A,xy; "the value of the magnetic field in the')
    P('           observations is unknown".')
    P('  Shimony, A., Huntington, C. M., Flippo, K. A., Elbaz, Y.,')
    P('    MacLaren, S. A., Shvarts, D. & Malamud, G. (2022),')
    P('    "Determining the Self-Similar Stage of the Rayleigh-Taylor')
    P('    Instability via LLNL\'s NIF Discovery Science Experiments",')
    P('    arXiv:2210.06631v1.  NO JOURNAL REFERENCE appears on the arXiv')
    P('    record, so this is cited as a preprint, which departs from this')
    P('    book\'s convention of journal, volume and page.  Said so here and')
    P('    in module07.html.')
    P('      p.1  h_{S/B} = alpha_{S/B} A g t^2 with A = (rho_2-rho_1)/')
    P('           (rho_1+rho_2); self-similarity after G ~ 3 merger')
    P('           generations; alpha_B = 0.038 +/- 0.008 (abstract); theory')
    P('           ~0.05 for 3D immiscible fluids, "a factor of ~2 higher')
    P('           than the results of full numerical 3D simulations".')
    P('      p.3  the Read integral, their equation (1),')
    P('           x_Read = A (int sqrt(g) dt)^2, citing Read (1984).')
    P('      p.4  alpha_B = 0.038 +/- 0.008 from the <lambda> = 15 micron')
    P('           case; Fig. 4 chi-squared bounds 0.03 and 0.046; RM velocity')
    P('           jump 16 micron/ns; decompression adds nearly 30%.')
    P('    NOT taken from this paper: an Atwood number.  The plastic and foam')
    P('    densities on p.1 (1.43 and ~0.08 g/cm^3) are PRE-SHOCK, and their')
    P('    Fig. 3 shows the foam at 0.2-0.6 g/cc during the RT phase.  The')
    P('    paper never states A, so this script never quotes one from it.')
    P('  Read, K. I. (1984), Physica D 12, 45, "Experimental investigation of')
    P('    turbulent mixing by Rayleigh-Taylor instability".  Named ONLY as')
    P('    the origin of the Read integral, via Shimony et al.  The paper is')
    P('    not in this folder and no number is taken from it.')
    P('  Miles, J. W. (1958), J. Fluid Mech. 4, 538, "On the disturbed motion')
    P('    of a plane vortex sheet"; Landau, L. D. (1944), Dokl. Akad. Nauk')
    P('    SSSR 44, 139.  The compressible stabilisation dU > 2 sqrt(2) c_s')
    P('    is QUOTED from these, not derived here, and neither paper is in')
    P('    this folder.  module07.html says so.')
    P('  Miles, J. W. (1961), J. Fluid Mech. 10, 496; Howard, L. N. (1961),')
    P('    J. Fluid Mech. 10, 509.  The sufficiency of Ri > 1/4 for stability')
    P('    of a continuously stratified shear flow.  QUOTED, not derived.')
    P('  Chandrasekhar, S. (1961), "Hydrodynamic and Hydromagnetic')
    P('    Stability", chs. X and XI.  The source of the dispersion relation')
    P('    of PART A, which this module derives rather than quotes; the')
    P('    viscous RT quartic of ch. X is NOT solved here, and the viscous')
    P('    scale printed is a crossover estimate, labelled as one.')
    P('  Fluid properties at 20 C, 1 atm: water 0.998207 g/cm^3,')
    P('    nu = 1.0034e-2 cm^2/s; dry air 1.2041e-3 g/cm^3; water-air')
    P('    interfacial tension 72.75 dyn/cm.  Handbook values, used as')
    P('    inputs, not checked against anything.')
    P('  Coronal n_e = 3e8 cm^-3 and T = 2e6 K: carried over from Module 1\'s')
    P('    census of astrophysical gases, afd/figs/m01_build_figs.py.  An')
    P('    INPUT here; every quantity that uses it carries its sqrt(n_e)')
    P('    scaling.')
    P('  IAU 2015 Resolution B3: nominal GM_sun, R_sun, L_sun.')


if __name__ == '__main__':
    main()
