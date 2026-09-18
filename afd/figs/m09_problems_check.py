"""Independent verification of every number quoted in module09.html.

NOTHING IS IMPORTED FROM m09_numbers.py.  Constants are re-entered from
CODATA 2018 and IAU 2015, and every route below is chosen to be different
from the generator's wherever a different route exists:

  * the isothermal wind u(x) in CLOSED FORM through Lambert W.  Writing
    w = u^2 turns u^2 - 2 ln u = R into w e^{-w} = e^{-R}, so
    u = sqrt(-W_k(-e^{-R})) with k = 0 subsonic and k = -1 supersonic.
    The generator bisects.
  * the polytropic v(r) by brentq on the Bernoulli + continuity pair.  The
    generator integrates the ODE from the critical point by Runge-Kutta.
  * the critical slopes by numpy.roots.  The generator uses the quadratic
    formula.
  * lambda_c(gamma) rearranged by hand to
        ln lambda = -2 ln 2 - ((2-3e)/(2e)) ln(1 - 1.5e),   e = gamma - 1,
    which is Bondi's own eq. (18) and does not overflow as gamma -> 1.
    The generator uses [(5-3g)/4]^2 [2/(5-3g)]^((g+1)/(2(g-1))).

AND THE MODULE 8 LESSON, which is why this file exists at all.  A check that
calls the same helper with the same argument reproduces the generator's bug.
So every input that is a MODELLING CHOICE rather than an arithmetic step is
rebuilt here from the physical statement in the prose:

    mu       from "He/H = 0.05 by number, fully ionised", against m_u
    r_0      from "the base of the corona is placed at 1.03 R_sun"
    n_e(R)   from Allen's quoted formula, coefficient for coefficient
    rho_SgrA from Baganoff's own sentence, rho = n_e mu m_H
    mu = 0.6 / 2.33 / 1.27 from the problems' own stated assumptions

Run:  python m09_problems_check.py
"""
import numpy as np
from scipy.optimize import brentq
from scipy.special import lambertw

# ---------------------------------------------------------------- constants
# CODATA 2018 / IAU 2015 nominal, re-entered, not imported.
kB = 1.380649e-16
m_u = 1.66053906660e-24
m_p = 1.67262192369e-24
c_light = 2.99792458e10
G = 6.67430e-8
sigma_T = 6.6524587321e-25
eV = 1.602176634e-12
keV = 1.0e3*eV
pc = 3.0856775814913673e18
AU = 1.495978707e13
yr = 3.155693e7                 # Julian-ish year used for M_sun/yr
GM_sun = 1.32712440018e26       # IAU 2015 nominal, cm^3 s^-2
R_sun = 6.957e10
L_sun = 3.828e33
M_sun = GM_sun/G

FAIL = []
NCHK = 0


def chk(label, got, want, rtol=5e-4):
    """Relative check, with a tolerance matched to the digits the prose prints."""
    global NCHK
    NCHK += 1
    if want == 0:
        ok = abs(got) < rtol
    else:
        ok = abs(got - want)/abs(want) <= rtol
    if not ok:
        FAIL.append(f'{label}: got {got!r}, prose says {want!r}')


def chkr(label, got, want, dp):
    """Rounding-aware check, for a value the prose gives to dp decimals."""
    global NCHK
    NCHK += 1
    if round(got, dp) != round(want, dp):
        FAIL.append(f'{label}: got {got!r} -> {round(got, dp)}, '
                    f'prose says {want!r}')


# ------------------------------------------- modelling choices, rebuilt
# "a helium-to-hydrogen ratio y = 0.05 by number with both species fully
#  ionised", and mu measured against m_u (module09.html Definition 1).
Y_HE = 0.05
MU_WIND = (m_p/m_u)*(1.0 + 4.0*Y_HE)/(2.0 + 3.0*Y_HE)
chk('mu against m_u (2.1)', MU_WIND, 0.56220)
chk('mu against m_p, as the prose also prints it',
    MU_WIND*m_u/m_p, 0.55814)
chk('m_p/m_u conversion factor', m_p/m_u, 1.00728)

# "the base of the corona is placed at r_0 = 1.03 R_sun"
R0 = 1.03*R_sun


def c_T(T, mu=MU_WIND):
    """Isothermal sound speed, module09.html (3.1)."""
    return np.sqrt(kB*T/(mu*m_u))


def r_crit(T, mu=MU_WIND, GM=GM_sun):
    """Critical radius GM/(2 c_T^2), module09.html (3.1)."""
    return GM/(2.0*c_T(T, mu)**2)


def u_iso(x, branch):
    """u = v/c_T on the transonic (C = -3) isothermal solution, CLOSED FORM.

    u^2 - 2 ln u = 4 ln x + 4/x - 3 =: R.  With w = u^2 this is
    w - ln w = R, i.e. w e^{-w} = e^{-R}, so w = -W_k(-e^{-R}) with the
    principal branch k = 0 for w < 1 (subsonic) and k = -1 for w > 1.
    """
    R = 4.0*np.log(x) + 4.0/x - 3.0
    k = 0 if branch == 'sub' else -1
    w = -lambertw(-np.exp(-R), k=k).real
    return np.sqrt(w)


def chord_slope(T0):
    rc = r_crit(T0)
    return (np.log(float(u_iso(0.98*AU/rc, 'super'))
                   / float(u_iso(0.29*AU/rc, 'super')))
            / np.log(0.98/0.29))


# ---------------------------------------------------------------- SECTION 2
# Allen (1947) their Sect. 4, quoted formula, coefficient for coefficient.
def n_e_allen(R_over_Rsun):
    return 1.0e8*(1.55*R_over_Rsun**-6.0 + 2.99*R_over_Rsun**-16.0)


n_e0 = n_e_allen(1.03)
chk('n_e(1.03 R_sun), Baumbach-Allen', n_e0, 3.161e8, 1e-3)
# rho = n_H m_p (1+4y) and n_tot = n_H (2+3y); n_e = n_H (1 + 2y) for full
# ionisation of H and He, so n_H = n_e/(1+2y).
n_H = n_e0/(1.0 + 2.0*Y_HE)
n_tot = n_H*(2.0 + 3.0*Y_HE)
chk('n_H at the base', n_H, 2.874e8, 1e-3)
chk('n_tot at the base', n_tot, 6.179e8, 1e-3)

P0 = n_tot*kB*2.0e6
chk('P_0 at 2 MK, (2.5)', P0, 1.706e-1, 1e-3)

# (2.3): P(inf)/P(r_0) = exp[-GM mu m_u/(k T r_0)] = exp(-2 r_c/r_0)
for T0, want in [(1.0e6, 3.642e-6), (2.0e6, 1.908e-3), (3.0e6, 1.539e-2)]:
    ratio = np.exp(-2.0*r_crit(T0)/R0)
    chk(f'P(inf)/P(r_0) at {T0/1e6:.0f} MK', ratio, want, 1e-3)

P_inf = P0*np.exp(-2.0*r_crit(2.0e6)/R0)
chk('P(infinity) at 2 MK, (2.6)', P_inf, 3.256e-4, 1e-3)
P_ism = 1.0*kB*1.0e4
chk('round ISM pressure', P_ism, 1.381e-12, 1e-3)
chk('P(inf)/P_ISM, the Check 1 number', P_inf/P_ism, 2.358e8, 1e-3)
# "Even at 1 MK the absolute floor is 6.2e-7 dyn/cm^2, still 4e5 times the
#  interstellar value"
P_inf_1MK = n_tot*kB*1.0e6*np.exp(-2.0*r_crit(1.0e6)/R0)
chk('P(infinity) at 1 MK', P_inf_1MK, 3.107e-7, 5e-3)
chk('that over the ISM value', P_inf_1MK/P_ism, 2.25e5, 5e-3)
# Parker's own numbers, arithmetic only
chk("Parker's own ratio 4.3e7", 0.6e-5/1.4e-13, 4.3e7, 2e-2)
chk('the factor 5.5 between his and ours', (P_inf/P_ism)/(0.6e-5/1.4e-13),
    5.5, 2e-2)

# ---------------------------------------------------------------- SECTION 3
# Proposition 3's minima, verified rather than asserted.
chk('h(u) minimum value h(1)', 1.0**2 - 2.0*np.log(1.0), 1.0)
chk('R(x) minimum at C = -3 is exactly 1', 4.0*np.log(1.0) + 4.0/1.0 - 3.0,
    1.0)
for C, x, want in [(-3.0, 1.0, 1.00), (-2.0, 1.0, 2.00), (-4.0, 1.0, 0.00)]:
    chkr(f'R(1) at C = {C}', 4.0*np.log(x) + 4.0/x + C, want, 2)

wind_tab = [(1.0, 1.000, 1.0000), (2.0, 1.674, 0.5545), (5.0, 2.457, 0.3178),
            (10.0, 2.964, 0.2313), (30.0, 3.651, 0.1568),
            (100.0, 4.286, 0.1140)]
for x, u_want, s_want in wind_tab:
    u = 1.0 if x == 1.0 else u_iso(x, 'super')
    chkr(f'transonic wind u at x = {x:g}', float(u), u_want, 3)
    # dln u/dln x from (3.2): (u - 1/u) du/dx = 2/x - 2/x^2
    if x != 1.0:
        slope = (2.0/x - 2.0/x**2)*x/(u*(u - 1.0/u))
        chkr(f'dln u/dln x at x = {x:g}', float(slope), s_want, 4)

# the breeze at C = -2, subsonic branch
def u_breeze(x, C=-2.0):
    R = 4.0*np.log(x) + 4.0/x + C
    return np.sqrt(-lambertw(-np.exp(-R), 0).real)


for x, want in [(1.0, 3.9824e-1), (2.0, 2.5849e-1), (5.0, 7.3080e-2),
                (10.0, 2.2261e-2), (30.0, 2.8255e-3), (100.0, 2.6645e-4)]:
    chk(f'breeze u at x = {x:g}', float(u_breeze(x)), want, 1e-3)

bs = (np.log(u_breeze(100.0)) - np.log(u_breeze(30.0)))/(np.log(100.0/30.0))
chkr('breeze logarithmic slope, 30 to 100', float(bs), -1.9612, 4)

for x, u_want, asy_want, slope_want in [(3e1, 3.651, 3.688, 0.1470),
                                        (1e3, 5.288, 5.257, 0.0724),
                                        (1e6, 7.503, 7.434, 0.0362)]:
    chkr(f'wind u at x = {x:g}', float(u_iso(x, 'super')), u_want, 3)
    chkr(f'2 sqrt(ln x) at x = {x:g}', 2.0*np.sqrt(np.log(x)), asy_want, 3)
    chkr(f'1/(2 ln x) at x = {x:g}', 1.0/(2.0*np.log(x)), slope_want, 4)

# ---------------------------------------------------------------- SECTION 4
def crit_slopes(g):
    """Roots of (4.1), by numpy.roots rather than the quadratic formula."""
    r = np.roots([g + 1.0, 4.0*(g - 1.0), 4.0*g - 6.0])
    if np.iscomplexobj(r) and np.abs(r.imag).max() > 1e-9:
        return None, None
    r = np.sort(r.real)[::-1]
    return float(r[0]), float(r[1])


slope_tab = [
    (1.0000, 1.0000, -1.0000, -1.0000), (1.1000, 0.7828, -0.9733, -0.7619),
    (1.2000, 0.5788, -0.9424, -0.5455), (1.3000, 0.3840, -0.9058, -0.3478),
    (1.3940, 0.2051, -0.8634, -0.1771), (1.4000, 0.1937, -0.8604, -0.1667),
    (1.4360, 0.1250, -0.8409, -0.1051), (1.4900, 0.0199, -0.8071, -0.0161),
    (1.5000, 0.0000, -0.8000, 0.0000), (1.5500, -0.1033, -0.7595, 0.0784),
    (1.6000, -0.2183, -0.7048, 0.1538),
]
for g, sp, sm, prod in slope_tab:
    a, b = crit_slopes(g)
    chkr(f's_+ at gamma = {g}', a, sp, 4)
    chkr(f's_- at gamma = {g}', b, sm, 4)
    chkr(f'root product at gamma = {g}', (4.0*g - 6.0)/(g + 1.0), prod, 4)
# gamma = 5/3: the discriminant is exactly zero and both roots are -1/2
g53 = 5.0/3.0
chk('discriminant 4(10-6g) at gamma = 5/3', 4.0*(10.0 - 6.0*g53), 0.0, 1e-12)
chkr('the degenerate root -b/2a at gamma = 5/3',
     -4.0*(g53 - 1.0)/(2.0*(g53 + 1.0)), -0.5000, 4)
chkr('root product at gamma = 5/3', (4.0*g53 - 6.0)/(g53 + 1.0), 0.2500, 4)
chkr('root product at gamma = 1.7', (4.0*1.7 - 6.0)/(1.7 + 1.0), 0.2963, 4)
assert crit_slopes(1.7)[0] is None, 'gamma = 1.7 must give complex roots'

# ---------------------------------------------------------------- SECTION 5
def lambda_c(g):
    """Bondi's eq. (18), rearranged by hand so gamma -> 1 does not overflow."""
    if abs(g - 1.0) < 1e-9:
        return np.exp(1.5)/4.0
    if abs(g - 5.0/3.0) < 1e-12:
        return 0.25
    e = g - 1.0
    return np.exp(-2.0*np.log(2.0) - ((2.0 - 3.0*e)/(2.0*e))
                  * np.log(1.0 - 1.5*e))


lam_tab = [(1.000000, 1.120422, 0.2500), (1.100000, 0.995128, 0.2125),
           (1.200000, 0.871158, 0.1750), (1.300000, 0.748069, 0.1375),
           (1.400000, 0.625000, 0.1000), (1.500000, 0.500000, 0.0625),
           (1.600000, 0.366950, 0.0250), (5.0/3.0, 0.250000, 0.0000)]
for g, lam, rat in lam_tab:
    chk(f'lambda_c({g:.4f})', lambda_c(g), lam, 2e-6)
    chkr(f'r_c/R_B = (5-3g)/8 at gamma = {g:.4f}', (5.0 - 3.0*g)/8.0, rat, 4)
chk('exact e^(3/2)/4', np.exp(1.5)/4.0, 1.120422, 1e-6)
chk('lambda_c(1.4) is exactly 5/8', lambda_c(1.4), 0.625, 1e-9)
chk('lambda_c(5/3) is exactly 1/4', lambda_c(5.0/3.0), 0.25, 1e-12)
chk('r_c/R_B at gamma = 1 is exactly 1/4', (5.0 - 3.0)/8.0, 0.25, 1e-12)

# ---------------------------------------------------------------- SECTION 6
chk('escape speed at r_0 = 1.03 R_sun',
    np.sqrt(2.0*GM_sun/R0)/1e5, 608.6, 1e-3)

sun_tab = [(0.50e6, 86.0, 12.899, 0.05999, 209.0, 283.7, 0.2477),
           (1.00e6, 121.6, 6.449, 0.02999, 357.6, 451.3, 0.1885),
           (1.50e6, 148.9, 4.300, 0.02000, 478.2, 585.8, 0.1645),
           (2.00e6, 172.0, 3.225, 0.01500, 583.2, 702.3, 0.1505),
           (3.00e6, 210.6, 2.150, 0.01000, 764.9, 902.9, 0.1343)]
for T0, cT, rcRs, rcau, v029, v1, chord in sun_tab:
    a = c_T(T0)
    rc = r_crit(T0)
    chkr(f'c_T at {T0/1e6:g} MK [km/s]', a/1e5, cT, 1)
    chkr(f'r_c at {T0/1e6:g} MK [R_sun]', rc/R_sun, rcRs, 3)
    chkr(f'r_c at {T0/1e6:g} MK [au]', rc/AU, rcau, 5)
    va = float(u_iso(0.29*AU/rc, 'super'))*a/1e5
    vb = float(u_iso(1.00*AU/rc, 'super'))*a/1e5
    chkr(f'v(0.29 au) at {T0/1e6:g} MK', va, v029, 1)
    chkr(f'v(1 au) at {T0/1e6:g} MK', vb, v1, 1)
    # the chord is over 0.29-0.98 au, the Helios range, NOT 0.29-1.00
    v98 = float(u_iso(0.98*AU/rc, 'super'))*a/1e5
    chkr(f'chord slope at {T0/1e6:g} MK',
         np.log(v98/va)/np.log(0.98/0.29), chord, 4)

# Proposition 7: the base speed and the rate
rho0 = n_H*m_p*(1.0 + 4.0*Y_HE)
chk('rho at the base', rho0, 5.7685e-16, 1e-3)
for T0, v0_want, md_want in [(1.0e6, 77.82, 2.897e11),
                             (1.5e6, 2753.71, 1.025e13),
                             (2.0e6, 14468.42, 5.385e13)]:
    a = c_T(T0)
    v0 = float(u_iso(R0/r_crit(T0), 'sub'))*a
    chk(f'v(r_0) at {T0/1e6:g} MK [cm/s]', v0*1e-2, v0_want, 2e-3)
    chk(f'Mdot at {T0/1e6:g} MK', 4.0*np.pi*R0**2*rho0*v0, md_want, 2e-3)
# The prose gives both: 12.5 at 1 MK and 13.2 at the fitted 0.947 MK.
# The prep printed only 13.2 and attributed it to 1 MK; this check is what
# caught that, and module09.html now states each with its temperature.
chk('sensitivity 2 r_c/r_0 at 1 MK', 2.0*r_crit(1.0e6)/R0, 12.5, 5e-3)
chk('r_c at the fitted 0.947 MK [R_sun]', r_crit(0.947e6)/R_sun, 6.808, 3e-3)
chk('sensitivity there', 2.0*r_crit(0.947e6)/R0, 13.2, 5e-3)
chk('a factor of 2 in T moves the rate by 186',
    (4*np.pi*R0**2*rho0*c_T(2e6)*float(u_iso(R0/r_crit(2e6), 'sub')))
    / (4*np.pi*R0**2*rho0*c_T(1e6)*float(u_iso(R0/r_crit(1e6), 'sub'))),
    186.0, 2e-2)

# Proposition 8: the ceiling, two ways -- closed form, and by solving r_c = r_0
T_ceil_closed = GM_sun*MU_WIND*m_u/(2.0*kB*R0)
T_ceil_solved = brentq(lambda T: r_crit(T) - R0, 1.0e6, 50.0e6)
chk('T_ceiling closed form, (6.2)', T_ceil_closed, 6.26e6, 2e-3)
chk('T_ceiling by solving r_c = r_0', T_ceil_solved, T_ceil_closed, 1e-9)
chkr('the corona is 2.1 to 3.1 below the ceiling',
     T_ceil_closed/3.0e6, 2.1, 1)
chkr('  and 3.1 at 2 MK', T_ceil_closed/2.0e6, 3.1, 1)

# ---------------------------------------------------------------- SECTION 7
# Venzmer & Bothmer (2018) Table 3, re-entered from the paper.
VB = {'n_mean': (7.57, 0.30, -2.010, 0.038, 0.072),
      'v_mean': (435.6, 2.4, 0.049, 0.010, 0.012),
      'T_mean': (9.67e4, 0.21e4, -0.792, 0.028, 0.050),
      'n_med': (5.61, 0.27, -2.093, 0.046, 0.072),
      'v_med': (410.7, 2.8, 0.058, 0.013, 0.012),
      'T_med': (7.14e4, 0.23e4, -0.913, 0.039, 0.050)}

for tag, a_key, t_key, g_want, g_err, s32, s1, s53 in [
        ('mean', 'n_mean', 'T_mean', 1.3940, 0.0158, 6.7, 24.9, 17.3),
        ('median', 'n_med', 'T_med', 1.4362, 0.0210, 3.0, 20.8, 11.0)]:
    al, dal = VB[a_key][2], VB[a_key][3]
    eT, deT = VB[t_key][2], VB[t_key][3]
    g = 1.0 + (-eT)/(-al)*(-1.0)     # = 1 + (-e_T)/alpha with alpha = -e_n
    g = 1.0 + (-eT)/(-al)
    dg = abs(g - 1.0)*np.hypot(deT/eT, dal/al)
    chkr(f'gamma_eff ({tag})', g, g_want, 4)
    chkr(f'its error ({tag})', dg, g_err, 4)
    chkr(f'sigma below 3/2 ({tag})', (1.5 - g)/dg, s32, 1)
    chkr(f'sigma above 1 ({tag})', (g - 1.0)/dg, s1, 1)
    chkr(f'sigma below 5/3 ({tag})', (5.0/3.0 - g)/dg, s53, 1)
chkr('gamma_eff/(3/2), mean', (1.0 + 0.792/2.010)/1.5, 0.9294, 4)
chkr('gamma_eff/(3/2), median', (1.0 + 0.913/2.093)/1.5, 0.9575, 4)

# Check 4: the sign of beta
for tag, key, sf, sy in [('mean', 'v_mean', 4.9, 4.1),
                         ('median', 'v_med', 4.5, 4.8)]:
    _, _, b, db, dy = VB[key]
    chkr(f'beta > 0, formal ({tag})', b/db, sf, 1)
    chkr(f'beta > 0, yearly ({tag})', b/dy, sy, 1)

# Check 6(i)
chkr('e_T against 0, formal sigma', 0.792/0.028, 28.3, 1)
chkr('e_T against 0, yearly sigma', 0.792/0.050, 15.8, 1)

# Check 6(ii): the scan, and the floor at the ceiling
scan = [(0.50e6, 0.2477), (1.00e6, 0.1885), (1.50e6, 0.1645),
        (2.00e6, 0.1505), (3.00e6, 0.1343), (4.00e6, 0.1246),
        (5.00e6, 0.1179), (T_ceil_closed, 0.1119)]
for T0, want in scan:
    rc = r_crit(T0)
    chkr(f'chord slope at {T0/1e6:.2f} MK', chord_slope(T0), want, 4)
chkr('the floor against 0.049 +/- 0.010, in sigma',
     (0.1119 - 0.049)/0.010, 6.3, 1)


for lo, want in [(0.5e6, 52.0), (1.0e6, 46.0), (2.0e6, 41.0), (5.0e6, 36.0)]:
    fall = 100.0*(1.0 - chord_slope(10.0*lo)/chord_slope(lo))
    chkr(f'per cent fall per decade from {lo/1e6:g} MK', fall, want, 0)

T_reach = brentq(lambda T: chord_slope(T) - 0.049, 1.0e6, 1.0e13)
chk('the T_0 that does reach 0.049 [MK]', T_reach/1e6, 1644.0, 5e-3)
chkr('  which is this many times 3 MK', T_reach/3.0e6, 548.0, 0)
chkr('  and this many times 2 MK', T_reach/2.0e6, 822.0, 0)
chkr('  and this many times the ceiling', T_reach/T_ceil_closed, 263.0, 0)

# Check 6(iii): fit T_0 to the 1-au speed
def v_1au(T0):
    return float(u_iso(AU/r_crit(T0), 'super'))*c_T(T0)/1e5


T_fit_mean = brentq(lambda T: v_1au(T) - 435.6, 0.3e6, 6.0e6)
T_fit_med = brentq(lambda T: v_1au(T) - 410.7, 0.3e6, 6.0e6)
chk('T_0 fitted to 435.6 km/s [MK]', T_fit_mean/1e6, 0.947, 2e-3)
chk('T_0 fitted to 410.7 km/s [MK]', T_fit_med/1e6, 0.866, 2e-3)
chkr('2 MK / fitted', 2.0e6/T_fit_mean, 2.11, 2)
chkr('3 MK / fitted', 3.0e6/T_fit_mean, 3.17, 2)
chkr('v(1 au) at 2 MK over measured', v_1au(2.0e6)/435.6, 1.61, 2)
chkr('v(1 au) at 3 MK over measured', v_1au(3.0e6)/435.6, 2.07, 2)

# Check 5: steady Euler with the measured pressure gradient, (7.2)
for tag, nk, vk, Tk, dlnP, cT2, pterm, gterm, pred, perr, ratio, sf, sy in [
        ('mean', 'n_mean', 'v_mean', 'T_mean', 2.802, 1.4301e13,
         0.02112, -0.00468, 0.01644, 0.00061, 2.98, 3.2, 2.7),
        ('median', 'n_med', 'v_med', 'T_med', 3.006, 1.0559e13,
         0.01882, -0.00526, 0.01356, 0.00074, 4.28, 3.4, 3.7)]:
    alpha = -VB[nk][2]
    eT = VB[Tk][2]
    v = VB[vk][0]*1e5
    T = VB[Tk][0]
    chkr(f'-dlnP/dlnr = alpha - e_T ({tag})', alpha - eT, dlnP, 3)
    a2 = kB*T/(MU_WIND*m_u)
    chk(f'c_T^2 at 1 au ({tag})', a2, cT2, 2e-3)
    p = (alpha - eT)*a2/v**2
    gterm_c = -GM_sun/(AU*v**2)
    chk(f'pressure term ({tag})', p, pterm, 3e-3)
    chk(f'gravity term ({tag})', gterm_c, gterm, 3e-3)
    chk(f'predicted slope ({tag})', p + gterm_c, pred, 3e-3)
    chkr(f'measured/predicted ({tag})', VB[vk][2]/(p + gterm_c), ratio, 2)
    chkr(f'shortfall, formal sigma ({tag})',
         (VB[vk][2] - pred)/np.hypot(VB[vk][3], perr), sf, 1)
    chkr(f'shortfall, yearly sigma ({tag})',
         (VB[vk][2] - pred)/np.hypot(VB[vk][4], perr), sy, 1)

# the pure-proton variant: mu = 1/2 against m_p, VB18's own convention
MU_PROTON = (m_p/m_u)*0.5
a2_p = kB*VB['T_mean'][0]/(MU_PROTON*m_u)
chkr('c_T^2 rises by this factor at mu = 1/2',
     a2_p/(kB*VB['T_mean'][0]/(MU_WIND*m_u)), 1.1163, 4)
chk('c_T^2 at mu = 1/2', a2_p, 1.5964e13, 2e-3)
v_m = VB['v_mean'][0]*1e5
pred_p = (2.802*a2_p - GM_sun/AU)/v_m**2
chk('predicted slope at mu = 1/2', pred_p, 0.01890, 3e-3)
chkr('ratio at mu = 1/2', 0.049/pred_p, 2.59, 2)
chkr('sigma at mu = 1/2', (0.049 - pred_p)/np.hypot(0.010, 0.00068), 3.0, 1)

# the continuity-tied variant quoted in the small-print paragraph
pred_tied = (((2.0 + 0.049) - VB['T_mean'][2])
             * kB*VB['T_mean'][0]/(MU_WIND*m_u) - GM_sun/AU)/v_m**2
chk('predicted slope with alpha tied to 2 + beta', pred_tied, 0.01674, 5e-3)
chkr('  which moves the prediction by this many per cent',
     100.0*(pred_tied/0.01644 - 1.0), 1.8, 1)

# Check 7: the single-polytrope repair
def poly_launch_Tmin(g, r0=R0, GM=GM_sun, mu=MU_WIND):
    """Minimum base temperature for a transonic polytropic wind from r0.

    Bernoulli with v(r0) -> 0: c_0^2/(g-1) - GM/r0 must exceed the value at
    the critical point, which gives c_0^2 > (g-1)/g * GM/r0.
    """
    # c_0^2 = g k T/(mu m_u) > (g-1) GM/r_0, so
    #   T_0 > (g-1)/g * GM mu m_u/(k r_0).
    return (g - 1.0)/g*GM*mu*m_u/(kB*r0)


chk('minimum launch T at gamma = 1.3940 [MK]',
    poly_launch_Tmin(1.3940)/1e6, 3.540, 3e-3)
chk('minimum launch T at gamma = 1.4362 [MK]',
    poly_launch_Tmin(1.4362)/1e6, 3.804, 3e-3)
chkr('  which exceeds 3 MK by', poly_launch_Tmin(1.3940)/3.0e6, 1.18, 2)
chkr('  and 2 MK by', poly_launch_Tmin(1.3940)/2.0e6, 1.77, 2)
chkr('  median, over 3 MK', poly_launch_Tmin(1.4362)/3.0e6, 1.27, 2)
chkr('  median, over 2 MK', poly_launch_Tmin(1.4362)/2.0e6, 1.90, 2)


def poly_wind(g, T0, r, r0=R0, GM=GM_sun, mu=MU_WIND):
    """v(r) for a polytropic transonic wind, by brentq on Bernoulli.

    Bernoulli: v^2/2 + c^2/(g-1) - GM/r = c_0^2/(g-1) - GM/r0, with
    continuity rho v r^2 const and c^2 = c_0^2 (rho/rho_0)^(g-1).  The
    generator integrates the ODE from the critical point instead.
    """
    c0sq = g*kB*T0/(mu*m_u)
    # critical point: c_c^2 = GM/(2 r_c) and Bernoulli there
    def f(rc):
        ccsq = GM/(2.0*rc)
        return (0.5*ccsq + ccsq/(g - 1.0) - GM/rc
                - (c0sq/(g - 1.0) - GM/r0))
    rc = brentq(f, 1e-4*r0, 1e4*r0)
    ccsq = GM/(2.0*rc)
    vc = np.sqrt(ccsq)
    B = c0sq/(g - 1.0) - GM/r0

    def g_of_v(v, rr):
        # continuity from the critical point fixes rho, hence c^2
        rho_ratio = (vc*rc**2)/(v*rr**2)
        csq = ccsq*rho_ratio**(g - 1.0)
        return 0.5*v*v + csq/(g - 1.0) - GM/rr - B
    lo, hi = (vc*1.0000001, 3.0e9) if rr_super(rr=r, rc=rc) else (1e-3, vc*0.99)
    return brentq(g_of_v, lo, hi, args=(r,)), rc


def rr_super(rr, rc):
    return rr > rc


T_poly = brentq(lambda T: poly_wind(1.3940, T, AU)[0]/1e5 - 435.6,
                3.6e6, 20.0e6)
v_p, rc_p = poly_wind(1.3940, T_poly, AU)
chk('T_0 forcing gamma = 1.3940 to 435.6 km/s [MK]', T_poly/1e6, 5.39, 3e-3)
chk('its critical radius [R_sun]', rc_p/R_sun, 1.020, 3e-3)
# its temperature at 1 au, from c^2 at that radius
c0sq_p = 1.3940*kB*T_poly/(MU_WIND*m_u)
ccsq_p = GM_sun/(2.0*rc_p)
rho_ratio = (np.sqrt(ccsq_p)*rc_p**2)/(v_p*AU**2)
csq_1au = ccsq_p*rho_ratio**(1.3940 - 1.0)
T_1au = csq_1au*MU_WIND*m_u/(1.3940*kB)
chk('T at 1 au from that solution', T_1au, 5.817e4, 3e-3)
chkr('  over the measured 9.670e4 K', T_1au/9.670e4, 0.602, 3)
chkr('measured beta over its predicted slope', 0.049/0.00802, 6.1, 1)

# Check 8: the mass flux
for Fm, want in [(3.5e-16, 9.843e11), (2.2e-16, 6.187e11),
                 (1.0e-16, 2.812e11), (1.5e-15, 4.218e12)]:
    chk(f'4 pi Fm au^2 at Fm = {Fm:g}', 4.0*np.pi*Fm*AU**2, want, 1e-3)
md_vb = 4.0*np.pi*AU**2*(7.57*MU_WIND*m_u)*(435.6e5)
# the prose's cross-check uses n_p m_p (1+4y), the same rho as the base
md_vb = 4.0*np.pi*AU**2*(7.57*m_p*(1.0 + 4.0*Y_HE))*(435.6e5)
chk('Mdot from the VB18 fits', md_vb, 1.861e12, 2e-3)
chk('  as an F_m', md_vb/(4.0*np.pi*AU**2), 6.62e-16, 2e-3)
for T0, want_md, want_ratio in [(1.0e6, 2.897e11, 0.294),
                                (T_fit_mean, 1.566e11, 0.159),
                                (2.0e6, 5.385e13, 54.712)]:
    v0 = float(u_iso(R0/r_crit(T0), 'sub'))*c_T(T0)
    md = 4.0*np.pi*R0**2*rho0*v0
    chk(f'Mdot at {T0/1e6:.3f} MK', md, want_md, 3e-3)
    chkr(f'  over 9.843e11', md/9.843e11, want_ratio, 3)
chkr('a factor 3 is this per cent in T_0', 100.0*np.log(3.0)/13.2, 8.3, 1)
for T0, want in [(1.0e6, 1.074e9), (1.5e6, 3.036e7), (2.0e6, 5.778e6)]:
    v0 = float(u_iso(R0/r_crit(T0), 'sub'))*c_T(T0)
    rho_need = 9.843e11/(4.0*np.pi*R0**2*v0)
    n_e_need = rho_need/(m_p*(1.0 + 4.0*Y_HE))*(1.0 + 2.0*Y_HE)
    chk(f'base n_e needed at {T0/1e6:g} MK', n_e_need, want, 3e-3)

# ---------------------------------------------------------------- SECTION 8
# Baganoff et al. (2003) their Sect. 11.1.2, and their OWN convention
# rho = n_e mu m_H, rebuilt from their sentence rather than shared.
BAG_NE = 130.0
BAG_KT = 2.0*keV
BAG_MU = 0.70
BAG_GAMMA = 5.0/3.0
M_SGRA = 4.30e6*M_sun
rho_sgra = BAG_NE*BAG_MU*m_p
cs_sgra = np.sqrt(BAG_GAMMA*BAG_KT/(BAG_MU*m_p))
chk('Sgr A* mass in grams', M_SGRA, 8.5502e39, 1e-3)
chk('kT = 2 keV in kelvin', BAG_KT/kB, 2.321e7, 1e-3)
chk('rho = n_e mu m_H', rho_sgra, 1.5221e-22, 1e-3)
chk('c_s at the Bondi radius [km/s]', cs_sgra/1e5, 675.4, 1e-3)
chkr('  over the 670 km/s the paper quotes', cs_sgra/1e5/670.0, 1.0080, 4)
R_B = 2.0*G*M_SGRA/cs_sgra**2
chk('R_B [pc]', R_B/pc, 0.0811, 2e-3)
md_bondi = 4.0*np.pi*0.25*rho_sgra*(G*M_SGRA)**2/cs_sgra**3
chk('Mdot_Bondi [g/s], (8.1)', md_bondi, 5.0549e20, 1e-3)
chk('  in M_sun/yr', md_bondi*yr/M_sun, 8.022e-6, 2e-3)
# their own mass, back-derived from their R_B and c_s
M_bag = 0.05*pc*(670e5)**2/(2.0*G)
chk("Baganoff's implied mass [M_sun]", M_bag/M_sun, 2.61e6, 5e-3)
chk('their 3e-6 rescaled by (M_new/M_old)^2',
    3.0e-6*(4.30e6/(M_bag/M_sun))**2, 8.15e-6, 5e-3)
chkr('Check 9 ratio', 8.15e-6/8.022e-6, 1.016, 3)
rho_alt = BAG_NE*m_p*(1.0 + 4.0*0.1)/(1.0 + 2.0*0.1)
chkr('the alternative density convention, as a factor',
     rho_alt/rho_sgra, 1.67, 2)
chk('Mdot under it', md_bondi*rho_alt/rho_sgra*yr/M_sun, 1.34e-5, 5e-3)

for lim, want in [(2.0e-7, 40.1), (5.0e-8, 160.4), (1.5e-8, 534.8),
                  (3.0e-9, 2674.2)]:
    chk(f'Bondi over {lim:g}', md_bondi*yr/M_sun/lim, want, 1e-3)
# Marrone's epsilon^(-2/3) scaling, rebuilt from their sentence
for eps, lim_want, ratio_want in [(1.00, 2.0e-7, 40.0), (0.10, 9.3e-7, 9.0),
                                  (0.03, 2.1e-6, 4.0)]:
    lim = 2.0e-7*eps**(-2.0/3.0)
    chk(f'upper limit at eps = {eps}', lim, lim_want, 2e-2)
    chkr(f'  and the ratio', md_bondi*yr/M_sun/lim, ratio_want, 0)
chkr('their own "a factor of 10 for 3%"', 0.03**(-2.0/3.0), 10.0, 0)

L_X = 2.0e33
chk('Mdot c^2', md_bondi*c_light**2, 4.543e41, 1e-3)
eta = L_X/(md_bondi*c_light**2)
chkr('implied radiative efficiency, one figure', eta*1e9, 4.0, 0)
chk('the efficiency range from L_X alone, low',
    2.4e33*0.75/(md_bondi*c_light**2), 4e-9, 0.2)
chk('the efficiency range from L_X alone, high',
    5.4e33/(md_bondi*c_light**2), 1.1e-8, 0.2)
chkr('a thin disc is this many times more efficient', 0.1/eta/1e7, 2.0, 0)
# Baganoff's local diffuse plasma, their Sect. 11.3
rho_loc = 26.0*BAG_MU*m_p
cs_loc = np.sqrt(BAG_GAMMA*1.3*keV/(BAG_MU*m_p))
md_loc = 4.0*np.pi*0.25*rho_loc*(G*M_bag)**2/cs_loc**3
chk('local-ISM Bondi rate at their mass', md_loc*yr/M_sun, 1.13e-6, 2e-2)
chkr('  over the ~1e-6 they quote', md_loc*yr/M_sun/1.0e-6, 1.13, 2)

# ---------------------------------------------------------------- PROBLEMS
# C1
a1 = c_T(1.0e6)
rc1 = r_crit(1.0e6)
chk('C1 c_T [km/s]', a1/1e5, 121.61, 1e-4)
chk('C1 r_c [cm]', rc1, 4.4868e11, 1e-3)
chkr('C1 r_c [R_sun]', rc1/R_sun, 6.449, 3)
chkr('C1 r_c [au]', rc1/AU, 0.02999, 5)
chk('C1 escape speed at r_c [km/s]', np.sqrt(2.0*GM_sun/rc1)/1e5, 243.2, 1e-3)
chk('C1 that equals 2 c_T', np.sqrt(2.0*GM_sun/rc1)/(2.0*a1), 1.0, 1e-9)
chkr('C1 v(1 au) [km/s]', v_1au(1.0e6), 451.3, 1)
chkr('C1 v(1 au) in units of c_T', v_1au(1.0e6)*1e5/a1, 3.71, 2)

# C2
t_c2 = 1e-4*M_sun/9.843e11
chk('C2 t [s]', t_c2, 2.0201e17, 2e-3)
chk('C2 t [yr]', t_c2/yr, 6.401e9, 2e-3)
chkr('C2 over the Sun age', t_c2/yr/4.57e9, 1.40, 2)
chk('C2 mass lost over 4.57 Gyr', 9.843e11*4.57e9*yr/M_sun, 7.14e-5, 3e-3)
chk('C2 the rate in M_sun/yr', 9.843e11*yr/M_sun, 1.56e-14, 5e-3)
chk("C2 Module 2's own 7.9e-5 from 1.72e-14 over 4.6 Gyr",
    1.72e-14*4.6e9, 7.9e-5, 5e-3)

# C3
r_S = 2.0*G*M_SGRA/c_light**2
chk('C3 r_S [cm]', r_S, 1.2699e12, 1e-3)
chkr('C3 r_S [au]', r_S/AU, 0.085, 3)
chk('C3 R_B/r_S', R_B/r_S, 1.970e5, 2e-3)
chk('C3 free-fall time from R_B [yr]',
    (np.pi/2.0)*np.sqrt(R_B**3/(2.0*G*M_SGRA))/yr, 184.4, 5e-3)
chk('C3 0.06 pc in r_S at the GRAVITY mass', 0.06*pc/r_S, 1.46e5, 5e-3)

# D1
for vr, want in [(0.0, 1.0000), (0.5, 0.7155), (1.0, 0.3536), (2.0, 0.0894),
                 (5.0, 0.0075)]:
    chkr(f'D1 ratio at v/c = {vr}', (1.0 + vr*vr)**-1.5, want, 4)
chkr('D1 the factor at v = 5c', 1.0/(1.0 + 25.0)**-1.5, 133.0, 0)
chk('D1 Bondi 2 pi is 4 pi lambda_c(3/2)',
    4.0*np.pi*lambda_c(1.5), 2.0*np.pi, 1e-9)

# D2
a2_, b2_ = crit_slopes(1.1)
chkr('D2 s_+', a2_, 0.7828, 4)
chkr('D2 s_-', b2_, -0.9733, 4)
chk('D2 minimum launch T [MK]', poly_launch_Tmin(1.1)/1e6, 1.1385, 3e-3)
v_d2, rc_d2 = poly_wind(1.1, 2.0e6, AU)
chk('D2 c_c [km/s]', np.sqrt(GM_sun/(2.0*rc_d2))/1e5, 128.4, 3e-3)
chk('D2 r_c [R_sun]', rc_d2/R_sun, 5.785, 3e-3)
chk('D2 v(1 au) [km/s]', v_d2/1e5, 371.8, 3e-3)
# v(infinity): all enthalpy plus the binding energy converted
c0sq_d2 = 1.1*kB*2.0e6/(MU_WIND*m_u)
v_inf = np.sqrt(2.0*(c0sq_d2/(1.1 - 1.0) - GM_sun/R0))
chk('D2 v(infinity) [km/s]', v_inf/1e5, 529.4, 3e-3)
chkr('D2 v(1 au) as a fraction of terminal', v_d2/v_inf, 0.70, 2)
chk('D2 lambda_c(1.1)', lambda_c(1.1), 0.9951, 1e-3)
chkr('D2 the isothermal comparison at 2 MK', v_1au(2.0e6), 702.3, 1)

# D3
MD = 9.843e11
V1 = 435.6e5
chk('D3 kinetic flux', 0.5*MD*V1**2, 9.3384e26, 1e-3)
chk('D3 as a fraction of L_sun', 0.5*MD*V1**2/L_sun, 2.440e-7, 2e-3)
chk('D3 gravitational term', GM_sun*MD/R_sun, 1.878e27, 1e-3)
chk('D3 as a fraction of L_sun', GM_sun*MD/(R_sun*L_sun), 4.91e-7, 3e-3)
chk('D3 Verscharen F_E total', 4.0*np.pi*AU**2*1.0, 2.812e27, 1e-3)
chk('D3 as a fraction of L_sun', 4.0*np.pi*AU**2/L_sun, 7.35e-7, 2e-3)
chkr('D3 gravity over kinetic', (GM_sun*MD/R_sun)/(0.5*MD*V1**2), 2.0, 1)

# K1 -- the ionisation assumption is rebuilt from the problem's own sentence
LIC_N, LIC_T, LIC_V = 0.2, 7.0e3, 2.6e6
mu_lic = (m_p/m_u)*0.6
mu_lic_neutral = (m_p/m_u)*1.27
cs_lic = np.sqrt(kB*LIC_T/(mu_lic*m_u))
chk('K1 c_s [km/s]', cs_lic/1e5, 9.81, 1e-3)
chkr('K1 v/c_s', LIC_V/cs_lic, 2.65, 2)
rB_sun = 2.0*GM_sun/(cs_lic**2 + LIC_V**2)
chk('K1 R_B [cm]', rB_sun, 3.437e13, 2e-3)
chkr('K1 R_B [au]', rB_sun/AU, 2.3, 1)
rho_lic = LIC_N*1.4*m_p
md_lic = (4.0*np.pi*lambda_c(1.0)*rho_lic*(GM_sun)**2
          / (cs_lic**2 + LIC_V**2)**1.5)
chk('K1 Mdot [g/s]', md_lic, 5.411e9, 3e-3)
chk('K1 Mdot [M_sun/yr]', md_lic*yr/M_sun, 8.59e-17, 5e-3)
chkr('K1 wind over accretion', 9.843e11/md_lic, 182.0, 0)
cs_neu = np.sqrt(kB*LIC_T/(mu_lic_neutral*m_u))
chkr('K1 neutral c_s [km/s]', cs_neu/1e5, 6.75, 2)
chkr('K1 the 11 per cent',
     100.0*abs(((cs_lic**2 + LIC_V**2)**1.5
                / (cs_neu**2 + LIC_V**2)**1.5) - 1.0), 11.0, 0)

# K2
MC_N, MC_T = 1.0e4, 20.0
mu_mc = (m_p/m_u)*2.33
M_BH = 10.0*M_sun
cs_mc = np.sqrt(kB*MC_T/(mu_mc*m_u))
chk('K2 c_s [km/s]', cs_mc/1e5, 0.2662, 1e-3)
RB_mc = 2.0*G*M_BH/cs_mc**2
chk('K2 R_B [cm]', RB_mc, 3.746e18, 2e-3)
chkr('K2 R_B [au]', RB_mc/AU, 250413.0, 0)
chkr('K2 R_B [pc]', RB_mc/pc, 1.2140, 4)
rho_mc = MC_N*mu_mc*m_u
md_mc = 4.0*np.pi*lambda_c(1.0)*rho_mc*(G*M_BH)**2/cs_mc**3
chk('K2 Mdot [g/s]', md_mc, 5.124e22, 2e-3)
chk('K2 Mdot [M_sun/yr]', md_mc*yr/M_sun, 8.133e-4, 3e-3)
L_edd_10 = 4.0*np.pi*G*M_BH*m_p*c_light/sigma_T
chk('K2 L_Edd', L_edd_10, 1.257e39, 2e-3)
md_edd_10 = L_edd_10/(0.1*c_light**2)
chk('K2 Mdot_Edd', md_edd_10, 1.399e19, 2e-3)
chkr('K2 Eddington ratio', md_mc/md_edd_10, 3664.0, 0)
chk('K2 doubling time [yr]', M_BH/md_mc/yr, 1.23e4, 5e-3)

# K3
L_edd_sgra = 4.0*np.pi*G*M_SGRA*m_p*c_light/sigma_T
chk('K3 L_Edd', L_edd_sgra, 5.405e44, 2e-3)
chk('K3 L_X/L_Edd', L_X/L_edd_sgra, 3.70e-12, 3e-3)
md_edd_sgra = L_edd_sgra/(0.1*c_light**2)
chk('K3 Mdot_Edd [M_sun/yr]', md_edd_sgra*yr/M_sun, 9.545e-2, 3e-3)
chk('K3 Mdot_Bondi/Mdot_Edd', md_bondi/md_edd_sgra, 8.405e-5, 3e-3)
chk('K3 Marrone bound over Eddington',
    2.0e-7/(md_edd_sgra*yr/M_sun), 2.095e-6, 3e-3)


# ---------------------------------------------------------------- report
if __name__ == '__main__':
    print(f'{NCHK} checks, {len(FAIL)} mismatch(es)')
    for f in FAIL:
        print('  MISMATCH', f)
    if not FAIL:
        print('  every number in module09.html verified independently')
