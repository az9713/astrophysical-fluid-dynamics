"""Module 3 numbers: hydrostatic equilibrium, scale heights, polytropes and
the Lane-Emden equation, checked against a tabulated standard solar model
and against a helioseismic measurement.

Every physical number quoted in module03.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

THE SHAPE OF THE CHECK, following Module 2.  One prediction that follows from
hydrostatic equilibrium plus a closure is CONFIRMED; a second prediction from
the same equations and the same source table is REFUTED.  Here:

  CONFIRMED  The solar convection zone is a polytrope of index n = 3/2.
             That index is fixed before any data is touched: efficient
             convection makes the stratification adiabatic, and an adiabatic
             monatomic ideal gas has P ~ rho^(5/3), hence n = 3/2 exactly.
             Read off the BS05(AGS,OP) table, the outer envelope gives
             n_eff = 1.527, a ratio of 1.018 to the predicted 1.500.

  REFUTED    Eddington's standard model, n = 3, for the Sun as a whole.
             It predicts rho_c/rhobar = 54.18; the table gives 106.9, a
             factor 1.97.  The reason is computable and is reported below:
             n = 3 follows from a constant ratio of gas to total pressure,
             which requires radiation pressure to be a fixed and significant
             share of the total.  In the Sun it is 6.2e-4 of the total, so
             the premise of the model is not met.

  AND ONE MEASUREMENT  The same n_eff(r) profile locates the base of the
             convection zone, where the stratification first becomes
             adiabatic.  Applied to BS05(AGS,OP) it returns 0.728 R_sun.
             Helioseismology measures (0.7133 +/- 0.0005) R_sun, Basu &
             Antia (2004).  The model is wrong by about 29 sigma.  This is
             the solar abundance problem.  Note carefully what fails: not
             hydrostatic equilibrium and not the polytropic closure, both of
             which are doing the measuring, but the opacity and heavy-element
             abundance that the model was built from.

A NOTE ON CIRCULARITY, stated here because it governs how the checks may be
worded.  A standard solar model is CONSTRUCTED by solving hydrostatic
equilibrium.  Nothing compared against it can therefore confirm hydrostatic
equilibrium itself; the table can only test a CLOSURE, given the equation.
Module 2's solar-wind check did not have this problem, because Venzmer &
Bothmer fitted their exponents with no continuity constraint imposed.  The
one statement here that is free of any closure is Chandrasekhar's bound,
which uses only the measured M and R; it is computed in PART F, and it is
satisfied by a wide factor rather than sharply, which is exactly why a
closure is needed at all.

Sources for every published number compared against are listed in the
SOURCES block at the foot of this file and in module03.html.
"""
import os
import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m01_numbers.py and m02_numbers.py rather than
# imported, so that each module's numbers script reads on its own.
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

# IAU 2015 nominal solar conversion constants.  GM is the measured quantity;
# M follows from it and from the CODATA G, which is why M carries G's
# relative uncertainty of 2.2e-5 and GM does not.
GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
Rsun = 6.957e10         # cm             (IAU 2015 nominal)
Lsun = 3.828e33         # erg/s          (IAU 2015 nominal)
Msun = GMsun/G          # g

# Earth, for the terrestrial half of the module.
g_earth = 980.665       # cm/s^2         (standard gravity, definitional)
mu_air = 28.9647        # dimensionless  (mean molecular weight of dry air)

# International Standard Atmosphere (ISO 2533 / US Standard Atmosphere 1976).
# These three are the DEFINING constants of the standard; the tropopause
# values below are derived from them, not measured independently.
ISA_T0 = 288.15         # K
ISA_P0 = 1.01325e6      # dyn/cm^2       (= 101325 Pa)
ISA_LAPSE = 6.5e-5      # K/cm           (= 6.5 K/km)
ISA_H_TROP = 1.1e6      # cm             (11 km geopotential)
ISA_T_TROP = 216.65     # K              (derived)
ISA_P_TROP = 2.2632e5   # dyn/cm^2       (= 22632 Pa, derived)

# Helioseismic measurement of the base of the solar convection zone.
# Basu & Antia (2004), ApJ 606, L85, from GONG and MDI p-mode frequencies.
RCZ_MEAS = 0.7133
RCZ_MEAS_ERR = 0.0005
# The value BS05 themselves quote for the same measurement, from the same
# authors, rounded: 0.713 +/- 0.001.  Used as a cross-check on the above.
RCZ_MEAS_BS05 = 0.713
RCZ_MEAS_BS05_ERR = 0.001
# The convection-zone base of the model whose table this module reads,
# as printed in Table 1 of Bahcall, Serenelli & Basu (2005).
RCZ_MODEL_PUBLISHED = 0.7280

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'data', 'bs05_agsop.dat')

# The table's own solar constants, printed at the foot of the data file.
# The table's radii and masses are fractions, so they must be converted with
# THESE values, not with the IAU nominal ones, or a 0.04% error is imported.
RSUN_TAB = 6.9598e10    # cm
LSUN_TAB = 3.8418e33    # erg/s


# =========================================================================
# PART A.  Why hydrostatic equilibrium is the default: three timescales
# =========================================================================

def t_freefall(rhobar):
    """Free-fall time of a uniform sphere of mean density rhobar.

    A shell released from rest at the surface of a pressureless uniform
    sphere reaches the centre in sqrt(3 pi / (32 G rhobar)).  This is the
    time in which a star with its pressure switched off would collapse.
    """
    return np.sqrt(3.0*np.pi/(32.0*G*rhobar))


def t_sound(R, cs):
    """Sound crossing time, the time for a pressure signal to cross."""
    return R/cs


def t_kelvin_helmholtz(M, R, L):
    """Kelvin-Helmholtz time, GM^2/(R L).

    The time to radiate the gravitational binding energy at the present
    luminosity; the timescale on which the THERMAL structure adjusts.
    """
    return G*M*M/(R*L)


# =========================================================================
# PART B.  Plane-parallel hydrostatic equilibrium: the scale height
# =========================================================================

def scale_height(T, mu, g):
    """Isothermal pressure scale height H = kT/(mu m_u g), in cm.

    From dP/dz = -rho g with P = rho k T/(mu m_u) and T, g constant:
    P(z) = P(0) exp(-z/H).  H is the e-folding length of the pressure.
    """
    return kB*T/(mu*mu_u*g)


def scale_height_self_grav(T, mu, M, r):
    """Scale height where gravity is that of a central mass M at radius r.

    Same formula with g = GM/r^2.  Valid when H << r, which is the
    condition for the plane-parallel approximation to hold at all.
    """
    return kB*T*r*r/(mu*mu_u*G*M)


def polytrope_index_from_lapse(lapse, mu, g):
    """Polytropic index n of a plane-parallel atmosphere with lapse rate.

    For P = K rho^(1+1/n) in plane-parallel hydrostatic equilibrium with an
    ideal gas, the temperature falls linearly with height at the rate
        |dT/dz| = mu m_u g / (k (n+1)),
    derived in Proposition 4 of module03.html.  Inverting gives n.
    """
    return mu*mu_u*g/(kB*lapse) - 1.0


def lapse_adiabatic(gamma, mu, g):
    """Adiabatic lapse rate g/c_p, with c_p = gamma k/((gamma-1) mu m_u)."""
    cp = gamma*kB/((gamma-1.0)*mu*mu_u)
    return g/cp


# =========================================================================
# PART C.  The Lane-Emden equation
# =========================================================================

def lane_emden(n, dxi=1e-5, xi_max=1e3):
    """Integrate theta'' + (2/xi) theta' + theta^n = 0, theta(0)=1,
    theta'(0)=0, by fourth-order Runge-Kutta.

    Returns (xi, theta, dtheta) sampled on the integration grid, truncated
    at the first zero of theta (the surface) if one exists.

    The origin is a regular singular point, so the integration is started
    from the series solution
        theta = 1 - xi^2/6 + n xi^4/120 - ...
    at xi = dxi rather than from xi = 0.
    """
    def deriv(xi, y):
        th, dth = y
        # theta^n is undefined for theta < 0; the surface is the first zero,
        # so clamp at zero and let the caller truncate there.
        thn = th**n if th > 0.0 else 0.0
        return np.array([dth, -thn - 2.0*dth/xi])

    xi = dxi
    th = 1.0 - xi*xi/6.0 + n*xi**4/120.0
    dth = -xi/3.0 + n*xi**3/30.0
    ys = [(xi, th, dth)]
    y = np.array([th, dth])
    h = dxi
    while xi < xi_max:
        # Grow the step smoothly once away from the origin, then freeze it.
        h = min(1e-4 + 1e-3*xi, 1e-3)
        k1 = deriv(xi, y)
        k2 = deriv(xi + h/2, y + h*k1/2)
        k3 = deriv(xi + h/2, y + h*k2/2)
        k4 = deriv(xi + h, y + h*k3)
        y = y + h*(k1 + 2*k2 + 2*k3 + k4)/6.0
        xi = xi + h
        ys.append((xi, y[0], y[1]))
        if y[0] <= 0.0:
            break
    arr = np.array(ys)
    return arr[:, 0], arr[:, 1], arr[:, 2]


def lane_emden_surface(n):
    """Return (xi_1, theta'(xi_1)) with xi_1 the first zero of theta.

    The zero is located by linear interpolation between the last positive
    and first negative sample, and theta' is interpolated to the same point.
    For n >= 5 there is no finite zero; the function raises.
    """
    xi, th, dth = lane_emden(n)
    if th[-1] > 0.0:
        raise ValueError(f'n = {n}: no finite surface found below xi = {xi[-1]:.1f}')
    i = len(th) - 1
    f = th[i-1]/(th[i-1] - th[i])          # fraction of the last step
    xi1 = xi[i-1] + f*(xi[i] - xi[i-1])
    dth1 = dth[i-1] + f*(dth[i] - dth[i-1])
    return xi1, dth1


def polytrope_constants(n):
    """Dimensionless structure constants of a polytrope of index n.

    Returns a dict with
      xi1      first zero of theta
      dtheta1  theta'(xi_1), negative
      mu1      -xi_1^2 theta'(xi_1), the dimensionless mass
      D_n      rho_c/rhobar = xi_1/(3 |theta'(xi_1)|)
      W_n      P_c R^4/(G M^2) = 1/(4 pi (n+1) theta'(xi_1)^2)

    Both D_n and W_n are pure numbers: given M and R, they fix the central
    density and central pressure with no further input.
    """
    xi1, dth1 = lane_emden_surface(n)
    mu1 = -xi1*xi1*dth1
    D = xi1/(3.0*abs(dth1))
    W = 1.0/(4.0*np.pi*(n+1.0)*dth1*dth1)
    return dict(n=n, xi1=xi1, dtheta1=dth1, mu1=mu1, D=D, W=W)


# =========================================================================
# PART D.  Reading the standard solar model table
# =========================================================================

def load_ssm(path=DATA):
    """Read the BS2005-AGS,OP tabulated model.

    Columns, as documented in the header of the data file:
      0 m/Msun  1 r/Rsun  2 T[K]  3 rho[g/cm^3]  4 P[dyn/cm^2]  5 L/Lsun
      6 X(1H)   7 X(4He)  8 X(3He) 9 X(12C)  10 X(14N)  11 X(16O)
    Only rows with all twelve fields parsing as floats are kept, which
    skips the header and the two trailing constant definitions.
    """
    rows = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            parts = line.split()
            if len(parts) != 12:
                continue
            try:
                rows.append([float(x) for x in parts])
            except ValueError:
                continue
    a = np.array(rows)
    return dict(mfrac=a[:, 0], rfrac=a[:, 1], T=a[:, 2], rho=a[:, 3],
                P=a[:, 4], lfrac=a[:, 5], X=a[:, 6], Y=a[:, 7])


def sliding_slope(x, y, half):
    """Local least-squares slope dy/dx over a window of +/- half samples.

    The table quotes P, rho and T to four significant figures, so a
    two-point finite difference is dominated by the quantisation.  A
    least-squares slope over a wide window averages that noise down.  The
    window is centred before the fit, which is what keeps the normal
    equation well conditioned at ln P ~ 39.
    """
    n = len(x)
    s = np.full(n, np.nan)
    for i in range(n):
        lo, hi = max(0, i-half), min(n, i+half+1)
        if hi - lo < 4:
            continue
        xc = x[lo:hi] - x[lo:hi].mean()
        yc = y[lo:hi] - y[lo:hi].mean()
        denom = xc @ xc
        if denom <= 0.0:
            continue
        s[i] = (xc @ yc)/denom
    return s


def effective_polytropic_index(ssm, half=25):
    """n_eff(r) from the tabulated model.

    A polytrope has P = K rho^(1+1/n), hence T ~ P/rho ~ P^(1/(n+1)), so
        grad == d ln T / d ln P = 1/(n+1)   and   n_eff = 1/grad - 1.
    Working in the (ln P, ln T) plane rather than (ln rho, ln P) is the
    standard stellar-structure diagnostic: grad is the quantity the
    Schwarzschild criterion compares with grad_ad, and it is the one the
    table resolves best.
    """
    lP = np.log(ssm['P'])
    lT = np.log(ssm['T'])
    grad = sliding_slope(lP, lT, half)
    with np.errstate(divide='ignore', invalid='ignore'):
        neff = 1.0/grad - 1.0
    return grad, neff


def convection_zone_base(ssm, grad, frac=0.99, r_lo=0.60, r_hi=0.95):
    """Locate the base of the convection zone in the tabulated model.

    Efficient convection drives the stratification to the adiabatic value,
    so grad saturates at grad_ad going outward.  The base is the innermost
    radius at which grad has reached a fraction `frac` of the plateau value
    measured in the outer envelope.

    Returns (r_base/Rsun, grad_plateau, n_plateau).
    """
    r = ssm['rfrac']
    # Plateau: the median of grad over a band well inside the convective
    # envelope but below the surface ionisation zones, which depress grad_ad.
    band = (r > 0.80) & (r < 0.92) & np.isfinite(grad)
    plateau = float(np.median(grad[band]))
    target = frac*plateau
    sel = (r > r_lo) & (r < r_hi) & np.isfinite(grad)
    idx = np.where(sel)[0]
    rb = np.nan
    for j in range(1, len(idx)):
        i0, i1 = idx[j-1], idx[j]
        if grad[i0] < target <= grad[i1]:
            f = (target - grad[i0])/(grad[i1] - grad[i0])
            rb = r[i0] + f*(r[i1] - r[i0])
            break
    return rb, plateau, 1.0/plateau - 1.0


def mu_from_table(ssm):
    """Mean molecular weight implied by the table itself, mu = rho k T/(P m_u).

    Derived from the tabulated P, rho and T, so it needs no assumption about
    the ionisation state or the composition.  Where radiation pressure or
    electron degeneracy contribute to P this returns an EFFECTIVE mu that
    absorbs them; at the centre of the Sun both are small, quantified below.
    """
    return ssm['rho']*kB*ssm['T']/(ssm['P']*mu_u)


def virial_check(ssm, Mtot):
    """Test 3 int P dV = -Omega on the tabulated model.

    For any body in hydrostatic equilibrium, multiplying dP/dr = -Gm rho/r^2
    by 4 pi r^3 and integrating by parts gives
        3 int_0^R P dV = int_0^R (G m/r) dm = -Omega,
    provided the surface pressure vanishes.  The model is BUILT by solving
    hydrostatic equilibrium, so agreement here confirms that this script
    reads the table correctly; it is a check of the pipeline, not of nature.
    Returns (3 int P dV, -Omega, ratio).
    """
    r = ssm['rfrac']*RSUN_TAB
    m = ssm['mfrac']*Mtot
    P = ssm['P']
    # 3 int P dV = 3 int P 4 pi r^2 dr
    lhs = 3.0*np.trapezoid(P*4.0*np.pi*r*r, r)
    # -Omega = int (G m/r) dm
    rhs = np.trapezoid(G*m/r, m)
    return lhs, rhs, lhs/rhs


# =========================================================================
# Reporting
# =========================================================================

def main():
    P = print
    P('=' * 74)
    P('MODULE 3 NUMBERS: hydrostatic equilibrium, scale heights, polytropes')
    P('=' * 74)

    ssm = load_ssm()
    nrow = len(ssm['rfrac'])
    rhoc = ssm['rho'][0]
    Pc = ssm['P'][0]
    Tc = ssm['T'][0]
    Mtot = Msun                      # the table's mass fractions are of Msun
    rhobar = 3.0*Mtot/(4.0*np.pi*RSUN_TAB**3)

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  Why hydrostatic equilibrium is the default')
    P('-'*74)
    tff = t_freefall(rhobar)
    cs_mean = np.sqrt(Pc/rhoc)       # order-of-magnitude central sound speed
    tKH = t_kelvin_helmholtz(Msun, Rsun, Lsun)
    tnuc = 0.007*0.1*Msun*c*c/Lsun   # 0.7% of rest mass, core 10% of the star
    P(f'  mean solar density rhobar          = {rhobar:.4f} g/cm^3')
    P(f'  free-fall time t_ff                = {tff:.1f} s = {tff/60:.1f} min')
    P(f'  central isothermal sound speed     = {cs_mean/1e5:.1f} km/s')
    P(f'  sound crossing time R/c_s          = {Rsun/cs_mean:.1f} s '
      f'= {Rsun/cs_mean/60:.1f} min')
    P(f'  Kelvin-Helmholtz time GM^2/(RL)    = {tKH:.4e} s = {tKH/yr:.3e} yr')
    P(f'  nuclear time 0.007 x 0.1 Mc^2/L    = {tnuc/yr:.3e} yr')
    P(f'  ratio t_KH/t_ff                    = {tKH/tff:.4e}')
    P(f'  (t_ff/t_KH)^2, the fractional force imbalance that contraction')
    P(f'  on the Kelvin-Helmholtz time requires = {(tff/tKH)**2:.3e}')
    P(f'  (t_ff/t_nuc)^2, the same on the nuclear time '
      f'= {(tff/tnuc)**2:.3e}')
    # Proposition 2 of the module carries an exact coefficient.  With
    # t_ff = sqrt(3 pi/(32 G rhobar)) one gets t_ff^2 = pi^2 R^3/(8 G M),
    # so |Rddot|/(GM/R^2) = R^3/(G M t^2) = (8/pi^2) (t_ff/t)^2.
    coef = 8.0/np.pi**2
    P(f'  exact coefficient 8/pi^2 in Proposition 2 = {coef:.4f}')
    P(f'  so the imbalance on the Kelvin-Helmholtz time is '
      f'{coef*(tff/tKH)**2:.3e}')
    P(f'  and on the nuclear time                    '
      f'{coef*(tff/tnuc)**2:.3e}')
    P('  READ: if the Sun contracted as fast as it can radiate its binding')
    P('  energy, gravity and the pressure gradient would still have to')
    P(f'  balance to {(tff/tKH)**2:.0e} of themselves.  On the nuclear timescale it')
    P('  actually evolves on, the requirement is smaller still.  The first')
    P('  figure is the conservative one, and it is the licence to drop the')
    P('  acceleration term.  Note the DIRECTION of the argument: a small')
    P('  imbalance is not assumed, it is forced by the observed luminosity.')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  Scale heights across the regimes')
    P('-'*74)
    H_air = scale_height(ISA_T0, mu_air, g_earth)
    P(f'  Earth, isothermal at 288.15 K, mu = {mu_air}')
    P(f'    H = kT/(mu m_u g)                = {H_air/1e5:.3f} km')
    # Solar photosphere.  T and P at tau = 2/3 carried over from Module 1.
    T_phot, P_phot, mu_phot = 5772.0, 1.2e5, 1.30
    g_sun = GMsun/Rsun**2
    H_phot = scale_height(T_phot, mu_phot, g_sun)
    P(f'  Solar photosphere, T = {T_phot:.0f} K, mu = {mu_phot}, '
      f'g = {g_sun:.3e} cm/s^2')
    P(f'    H                                = {H_phot/1e5:.1f} km '
      f'= {H_phot/Rsun:.2e} R_sun')
    P(f'    H/R_sun << 1, so plane-parallel is safe by a factor '
      f'{Rsun/H_phot:.0f}')
    # Intracluster medium, the Module 1 system.
    T_icm, mu_icm = 1e8, 0.6
    M_cluster, r_cluster = 5e14*Msun, 1e3*kpc
    H_icm = scale_height_self_grav(T_icm, mu_icm, M_cluster, r_cluster)
    P(f'  Intracluster medium at 1e8 K, M = 5e14 Msun, r = 1 Mpc')
    P(f'    H                                = {H_icm/kpc:.0f} kpc '
      f'= {H_icm/r_cluster:.2f} r')
    P('    H is NOT small compared with r, so the plane-parallel form fails')
    P('    and the spherical equation must be used.  Section 3 says why.')
    # Molecular cloud.
    T_mc, mu_mc = 10.0, 2.33
    M_mc, r_mc = 1e3*Msun, 2.0*pc
    H_mc = scale_height_self_grav(T_mc, mu_mc, M_mc, r_mc)
    P(f'  Molecular cloud at 10 K, M = 1e3 Msun, r = 2 pc')
    P(f'    H                                = {H_mc/pc:.3f} pc '
      f'= {H_mc/r_mc:.3f} r')

    # ---------------------------------------------------------------- C
    # Supplementary numbers quoted in the prose of Sections 1 and 3.
    R_earth = 6.371e8
    age_sun = 4.6e9*yr
    P('  Supplementary, for the census table and Section 1:')
    P(f'    g in the molecular cloud          = {G*M_mc/r_mc**2:.2e} cm/s^2')
    P(f'    g in the intracluster medium      = '
      f'{G*M_cluster/r_cluster**2:.2e} cm/s^2')
    P(f'    Earth H/R_earth (R = 6371 km)     = {H_air/R_earth:.2e}, '
      f'factor {R_earth/H_air:.0f}')
    P(f'    molecular cloud r/H               = {r_mc/H_mc:.0f}')
    P(f'    solar age 4.6 Gyr in free-fall times = {age_sun/tff:.1e}')
    P('')
    P('PART C.  The terrestrial troposphere is a polytrope')
    P('-'*74)
    n_earth = polytrope_index_from_lapse(ISA_LAPSE, mu_air, g_earth)
    lapse_dry = lapse_adiabatic(1.4, mu_air, g_earth)
    n_dry = polytrope_index_from_lapse(lapse_dry, mu_air, g_earth)
    P(f'  ISA lapse rate (definitional)      = {ISA_LAPSE*1e5:.2f} K/km')
    P(f'    implied polytropic index n       = {n_earth:.4f}')
    P(f'  dry adiabatic lapse rate g/c_p     = {lapse_dry*1e5:.3f} K/km')
    P(f'    implied polytropic index n       = {n_dry:.4f}  '
      f'(exactly 1/(gamma-1) = 2.5 for gamma = 7/5)')
    P(f'  dry adiabat colder than ISA at 11 km by '
      f'{(lapse_dry-ISA_LAPSE)*ISA_H_TROP:.1f} K')
    P(f'  c_p of dry air                     = '
      f'{1.4*kB/(0.4*mu_air*mu_u)/1e4:.1f} J/(kg K)')
    # Self-consistency: the ISA tropopause values should follow from the
    # polytropic solution P ~ T^(n+1) with the three defining constants.
    P_trop_pred = ISA_P0*(ISA_T_TROP/ISA_T0)**(n_earth + 1.0)
    T_trop_pred = ISA_T0 - ISA_LAPSE*ISA_H_TROP
    P(f'  tropopause T predicted from lapse  = {T_trop_pred:.2f} K '
      f'(tabulated {ISA_T_TROP:.2f} K, ratio {T_trop_pred/ISA_T_TROP:.5f})')
    P(f'  tropopause P from P ~ T^(n+1)      = {P_trop_pred/1e3:.2f} hPa '
      f'(tabulated {ISA_P_TROP/1e3:.2f} hPa, '
      f'ratio {P_trop_pred/ISA_P_TROP:.5f})')
    P('  READ: the aviation standard atmosphere IS a polytrope, of index')
    P(f'  {n_earth:.2f}.  Its index is not the dry adiabat {n_dry:.2f}, and the')
    P('  gap is latent heat released by condensing water.  The same gap, for')
    P('  the Sun, is what PART G measures and finds absent.')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  Lane-Emden: validating the integrator against exact solutions')
    P('-'*74)
    # n = 0: theta = 1 - xi^2/6, xi_1 = sqrt(6), theta'(xi_1) = -sqrt(6)/3
    c0 = polytrope_constants(0.0)
    P(f'  n = 0  xi_1 = {c0["xi1"]:.6f}  exact sqrt(6) = {np.sqrt(6):.6f}  '
      f'ratio {c0["xi1"]/np.sqrt(6):.6f}')
    P(f'         theta\'(xi_1) = {c0["dtheta1"]:.6f}  '
      f'exact -sqrt(6)/3 = {-np.sqrt(6)/3:.6f}  '
      f'ratio {c0["dtheta1"]/(-np.sqrt(6)/3):.6f}')
    # n = 1: theta = sin(xi)/xi, xi_1 = pi, theta'(xi_1) = -1/pi
    c1 = polytrope_constants(1.0)
    P(f'  n = 1  xi_1 = {c1["xi1"]:.6f}  exact pi = {np.pi:.6f}  '
      f'ratio {c1["xi1"]/np.pi:.6f}')
    P(f'         theta\'(xi_1) = {c1["dtheta1"]:.6f}  '
      f'exact -1/pi = {-1/np.pi:.6f}  '
      f'ratio {c1["dtheta1"]/(-1/np.pi):.6f}')
    # n = 5 has no finite surface: theta = (1 + xi^2/3)^(-1/2) -> 0 as xi -> inf
    xi5, th5, dth5 = lane_emden(5.0, xi_max=200.0)
    exact5 = (1.0 + xi5[-1]**2/3.0)**-0.5
    P(f'  n = 5  theta({xi5[-1]:.1f}) = {th5[-1]:.6e}  '
      f'exact (1+xi^2/3)^(-1/2) = {exact5:.6e}  '
      f'ratio {th5[-1]/exact5:.6f}')
    P(f'         -xi^2 theta\' = {-xi5[-1]**2*dth5[-1]:.6f}  '
      f'exact limit sqrt(3) = {np.sqrt(3):.6f}  '
      f'(finite mass, infinite radius)')
    P(f'         ratio to the limit = {-xi5[-1]**2*dth5[-1]/np.sqrt(3):.6f}')
    P('  READ: three exact solutions reproduced.  The largest departure is')
    P('  1.3e-4, on theta\'(xi_1) for n = 0, where the solution meets the')
    P('  surface at a finite slope and the step lands just past it.  The')
    P('  integrator may now be trusted on n = 3/2 and n = 3, which have none.')

    P('')
    P('  Structure constants of the polytropes this module uses:')
    P(f'  {"n":>5} {"xi_1":>10} {"-xi_1^2 th\'":>12} {"D=rho_c/rhobar":>15} '
      f'{"W=P_c R^4/GM^2":>15}')
    consts = {}
    for n in (0.0, 1.0, 1.5, 3.0, 4.0):
        cc = polytrope_constants(n)
        consts[n] = cc
        P(f'  {n:>5.1f} {cc["xi1"]:>10.5f} {cc["mu1"]:>12.5f} '
          f'{cc["D"]:>15.4f} {cc["W"]:>15.5f}')
    P('  Published values for n = 3 (Chandrasekhar 1939, Table 4):')
    P('    xi_1 = 6.89685, -xi_1^2 theta\' = 2.01824, rho_c/rhobar = 54.1825')
    c3 = consts[3.0]
    P(f'    ratios here: {c3["xi1"]/6.89685:.6f}  {c3["mu1"]/2.01824:.6f}  '
      f'{c3["D"]/54.1825:.6f}')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  The tabulated solar model')
    P('-'*74)
    P(f'  BS2005-AGS,OP, {nrow} rows, r/R from {ssm["rfrac"][0]:.5f} '
      f'to {ssm["rfrac"][-1]:.5f}')
    P(f'  central T                          = {Tc:.4e} K')
    P(f'  central rho                        = {rhoc:.4e} g/cm^3')
    P(f'  central P                          = {Pc:.4e} dyn/cm^2')
    P(f'  surface Y (helium mass fraction)   = {ssm["Y"][-1]:.5f}  '
      f'(paper Table 1: 0.229)')
    mu_tab = mu_from_table(ssm)
    P(f'  mu implied by the table at centre  = {mu_tab[0]:.5f}')
    Xc, Yc = ssm['X'][0], ssm['Y'][0]
    Zc = 1.0 - Xc - Yc
    mu_comp = 1.0/(2.0*Xc + 0.75*Yc + 0.5*Zc)
    P(f'  mu from central composition        = {mu_comp:.5f}  '
      f'(X={Xc:.5f}, Y={Yc:.5f}, Z={Zc:.5f}, fully ionised)')
    P(f'  ratio                              = {mu_tab[0]/mu_comp:.5f}')
    Prad_c = a_rad*Tc**4/3.0
    P(f'  central radiation pressure aT^4/3  = {Prad_c:.4e} dyn/cm^2')
    P(f'  1 - beta = P_rad/P at the centre   = {Prad_c/Pc:.4e}')
    P('  READ: radiation carries 6.2e-4 of the central pressure.  Hold that')
    P('  number; it is why CHECK 1 of PART G, n = 3, misses by a factor 2.')
    lhs, rhs, vr = virial_check(ssm, Mtot)
    P(f'  virial check 3 int P dV            = {lhs:.4e} erg')
    P(f'               -Omega = int Gm/r dm  = {rhs:.4e} erg')
    P(f'               ratio                 = {vr:.5f}')
    P('  This confirms the table is read correctly.  It cannot confirm')
    P('  hydrostatic equilibrium: the model was BUILT by solving it.')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  What hydrostatic equilibrium gives with NO closure')
    P('-'*74)
    # Use the TABLE's own radius, not the IAU nominal one.  Both the bound
    # and W are comparisons against this table, and mixing the two radii
    # made P_c/bound (521.6) disagree with W/(1/8 pi) (522.4), which are
    # the same number written two ways.
    P_chandra = G*Msun**2/(8.0*np.pi*RSUN_TAB**4)
    W_true = Pc*RSUN_TAB**4/(G*Msun**2)
    P(f'  Chandrasekhar bound P_c >= GM^2/(8 pi R^4)')
    P(f'    bound                            = {P_chandra:.4e} dyn/cm^2')
    P(f'    tabulated P_c                    = {Pc:.4e} dyn/cm^2')
    P(f'    P_c / bound                      = {Pc/P_chandra:.1f}')
    P(f'  W = P_c R^4/(G M^2) for the table  = {W_true:.4f}')
    P(f'    the bound is W >= 1/(8 pi)       = {1.0/(8.0*np.pi):.5f}')
    P(f'    W divided by 1/(8 pi), the same ratio again = '
      f'{W_true*8.0*np.pi:.1f}')
    P(f'    n = 3 polytrope gives W          = {c3["W"]:.4f}')
    P('  READ: the closure-free statement is a true INEQUALITY, satisfied by')
    P(f'  a factor {Pc/P_chandra:.0f}.  It rules out almost nothing.  That gap is')
    P('  precisely the work a closure has to do.')

    # ---------------------------------------------------------------- G
    P('')
    P('PART G.  THE CHECKS')
    P('-'*74)

    # --- CHECK 1: Eddington's n = 3 against the table.
    c15 = consts[1.5]
    P('  CHECK 1.  Eddington\'s standard model, n = 3, for the Sun entire.')
    rhoc_n3 = c3['D']*rhobar
    Pc_n3 = c3['W']*G*Msun**2/RSUN_TAB**4
    Tc_n3 = mu_tab[0]*mu_u*Pc_n3/(kB*rhoc_n3)
    P(f'    predicted rho_c = D_3 rhobar     = {rhoc_n3:.3f} g/cm^3')
    P(f'    tabulated rho_c                  = {rhoc:.3f} g/cm^3')
    P(f'    ratio predicted/tabulated        = {rhoc_n3/rhoc:.4f}')
    P(f'    predicted P_c = W_3 GM^2/R^4     = {Pc_n3:.4e} dyn/cm^2')
    P(f'    tabulated P_c                    = {Pc:.4e} dyn/cm^2')
    P(f'    ratio                            = {Pc_n3/Pc:.4f}')
    P(f'    predicted T_c (same mu)          = {Tc_n3:.4e} K')
    P(f'    tabulated T_c                    = {Tc:.4e} K')
    P(f'    ratio                            = {Tc_n3/Tc:.4f}')
    P(f'    tabulated rho_c/rhobar           = {rhoc/rhobar:.2f}')
    P(f'    n = 3 predicts                   = {c3["D"]:.2f}')
    P(f'    PUNCHLINE ratio                  = {c3["D"]/(rhoc/rhobar):.4f}')
    P('    REFUTED.  Density and pressure are each wrong by about a factor')
    P(f'    of two, but T_c is wrong by only {abs(Tc_n3/Tc-1)*100:.1f}%, because T ~ P/rho')
    P('    and the two errors are in the same direction and nearly cancel.')
    P('    That cancellation is why the 1926 estimate was still useful.')
    P('    WHY it fails: n = 3 follows from a constant ratio of gas to total')
    P(f'    pressure with radiation significant.  Here 1-beta = {Prad_c/Pc:.2e},')
    P('    so the premise does not hold.  n = 3 is the right model for a')
    P('    radiation-dominated massive star; the Sun is not one.')

    # --- CHECK 2: n_eff(r), the convection zone as an n = 3/2 polytrope.
    P('')
    P('  CHECK 2.  The convection zone as a polytrope of index 3/2.')
    grad, neff = effective_polytropic_index(ssm, half=25)
    rb, plateau, n_plateau = convection_zone_base(ssm, grad)
    grad_ad = 0.4                         # (gamma-1)/gamma for gamma = 5/3
    P(f'    grad_ad for a monatomic ideal gas = {grad_ad:.4f}  '
      f'-> n = {1/grad_ad - 1:.4f} exactly')
    P(f'    plateau grad measured, 0.80-0.92 R = {plateau:.4f}')
    P(f'    n_eff on the plateau              = {n_plateau:.4f}')
    P(f'    PUNCHLINE ratio n_eff/1.5         = {n_plateau/1.5:.4f}')
    P(f'    CONFIRMED to {abs(n_plateau/1.5-1)*100:.1f}%.  The index was fixed before the')
    P('    table was opened, by adiabatic convection in a monatomic gas')
    P('    alone.  Nothing was fitted.')
    P('    Values of n_eff through the star:')
    for x in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.45, 0.55, 0.65,
              0.70, 0.75, 0.85, 0.92):
        i = int(np.argmin(abs(ssm['rfrac'] - x)))
        P(f'      r/R = {ssm["rfrac"][i]:.4f}  grad = {grad[i]:.4f}  '
          f'n_eff = {neff[i]:.3f}  L(r)/L = {ssm["lfrac"][i]:.4f}')
    rad = (ssm['rfrac'] > 0.02) & (ssm['rfrac'] < 0.70) & np.isfinite(neff)
    imax = int(np.where(rad)[0][int(np.argmax(neff[rad]))])
    imin = int(np.where(rad)[0][int(np.argmin(neff[rad]))])
    P(f'    over the radiative interior 0.02-0.70 R, n_eff runs from '
      f'{neff[imin]:.2f} at r/R = {ssm["rfrac"][imin]:.3f}')
    P(f'    to a maximum of {neff[imax]:.2f} at r/R = {ssm["rfrac"][imax]:.3f}')
    # Where does n_eff pass through Eddington's value of 3?
    rr, nn = ssm['rfrac'][rad], neff[rad]
    crossings = []
    for j in range(1, len(nn)):
        if (nn[j-1] - 3.0)*(nn[j] - 3.0) < 0.0:
            f = (3.0 - nn[j-1])/(nn[j] - nn[j-1])
            crossings.append(rr[j-1] + f*(rr[j] - rr[j-1]))
    P(f'    n_eff = 3 is crossed at r/R = '
      + ', '.join(f'{x:.3f}' for x in crossings))
    P('    The radiative interior is NOT an n = 3 polytrope either.  n_eff')
    P('    is about 2.1 inside 0.15 R, where nuclear burning is still adding')
    P(f'    luminosity (L(r)/L reaches 0.78 only at r = 0.15 R); it then rises')
    P(f'    to {neff[imax]:.2f} near {ssm["rfrac"][imax]:.2f} R and falls again.  It passes through')
    P('    Eddington\'s value of 3, but it does not sit there, so no single')
    P('    polytrope describes the whole Sun.  Section 10.2 draws the')
    P('    consequence.')

    # --- CHECK 3: the base of the convection zone against helioseismology.
    P('')
    P('  CHECK 3.  Where that index changes, against a measurement.')
    P(f'    base recovered from this table    = {rb:.4f} R_sun')
    P(f'    model value published in Table 1  = {RCZ_MODEL_PUBLISHED:.4f} R_sun')
    P(f'    ratio                             = {rb/RCZ_MODEL_PUBLISHED:.5f}')
    P(f'    helioseismic measurement          = {RCZ_MEAS:.4f} '
      f'+/- {RCZ_MEAS_ERR:.4f} R_sun   (Basu & Antia 2004)')
    sig = (RCZ_MODEL_PUBLISHED - RCZ_MEAS)/RCZ_MEAS_ERR
    sig_loose = (RCZ_MODEL_PUBLISHED - RCZ_MEAS_BS05)/RCZ_MEAS_BS05_ERR
    P(f'    PUNCHLINE departure               = {sig:.1f} sigma '
      f'(and {sig_loose:.1f} sigma against the rounded +/- 0.001)')
    P(f'    fractional error                  = '
      f'{(RCZ_MODEL_PUBLISHED/RCZ_MEAS - 1)*100:.2f}%')
    P('    REFUTED, and note precisely what is refuted.  Hydrostatic')
    P('    equilibrium and the polytropic closure are the INSTRUMENT here,')
    P('    and the instrument is sharp: it locates a boundary to better than')
    P('    1% of a solar radius.  What fails is the composition and opacity')
    P('    fed into this particular model.  This is the solar abundance')
    P('    problem, open since Asplund et al. (2005).')

    # --- sensitivity of the locator, so the 29 sigma is not an artefact.
    P('')
    P('  Robustness of the CHECK 3 locator:')
    grid = []
    for half in (10, 25, 50):
        g2, _ = effective_polytropic_index(ssm, half=half)
        for frac in (0.98, 0.99, 0.995):
            rb2, pl2, _ = convection_zone_base(ssm, g2, frac=frac)
            P(f'    half = {half:>2}  frac = {frac:.3f}  '
              f'r_base = {rb2:.4f}  plateau grad = {pl2:.4f}')
            grid.append(rb2)
    lo, hi = min(grid), max(grid)
    P(f'    grid range of r_base              = {lo:.4f} to {hi:.4f}, '
      f'spread {hi-lo:.4f} R_sun')
    P(f'    recovered base 0.99/25 vs measurement = '
      f'{(rb - RCZ_MEAS)/RCZ_MEAS_ERR:.1f} sigma')
    P(f'    grid value nearest the measurement    = '
      f'{(lo - RCZ_MEAS)/RCZ_MEAS_ERR:.1f} sigma')
    P(f'    spread / model-measurement gap        = '
      f'{(hi-lo)/(RCZ_MODEL_PUBLISHED-RCZ_MEAS):.2f}')

    P('')
    P('=' * 74)
    P('SOURCES')
    P('=' * 74)
    P('  Bahcall, Serenelli & Basu (2005), ApJ 621, L85-L88,')
    P('    "New solar opacities, abundances, helioseismology, and neutrino')
    P('    fluxes".  arXiv:astro-ph/0412440.  Table 1 gives Rcz/Rsun = 0.7280')
    P('    and Ysurf = 0.229 for BS05(AGS,OP); equations (1) and (2) quote')
    P('    the measured values 0.713 +/- 0.001 and 0.249 +/- 0.003.')
    P('    Tabulated model: afd/data/bs05_agsop.dat, downloaded from')
    P('    http://www.sns.ias.edu/~jnb/SNdata/Export/BS2005/bs05_agsop.dat')
    P('  Basu & Antia (2004), ApJ 606, L85, "Constraining solar abundances')
    P('    using helioseismology".  arXiv:astro-ph/0403485.  Convection-zone')
    P('    base rb = (0.7133 +/- 0.0005) Rsun from GONG and (0.7132 +/-')
    P('    0.0005) Rsun from MDI p-mode frequencies.')
    P('  Chandrasekhar (1939), "An Introduction to the Study of Stellar')
    P('    Structure", ch. IV, Table 4: polytrope constants for n = 3.')
    P('  ISO 2533:1975 / US Standard Atmosphere 1976: T0 = 288.15 K,')
    P('    P0 = 101325 Pa, tropospheric lapse rate 6.5 K/km.')
    P('  IAU 2015 Resolution B3: nominal GM_sun, R_sun, L_sun.')


if __name__ == '__main__':
    main()
