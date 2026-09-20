"""Independent verification of every number in Module 12's problem set.

IT IMPORTS NOTHING FROM m12_numbers.py.  Physical constants are retyped
here from CODATA/IAU, and every modelling input is taken from the PROBLEM
STATEMENT as printed in module12.html -- not from the generator.  That is
the whole point of the script, and the rule comes from Module 9, where a
problem's printed answer needed two modelling facts that appeared only
inside the generator, so the problems check could not catch it: it read
the same two facts from the same place.

So for each slot below, the header comment quotes the inputs the statement
gives, and the code uses those and nothing else.  Where a statement gives
a derived quantity as well as the inputs that produce it -- K3 states the
mean free path AND the density, temperature and Coulomb logarithm -- both
routes are computed and compared, which turns a restatement into a test.

THREE CONVENTIONS THIS MODULE'S PROBLEMS TURN ON, all of them restated in
the statements and therefore usable here:
  * the gyroradius takes sqrt(2kT/m), the TWO perpendicular components;
  * a Spitzer mean free path is v_rms tau with sqrt(3kT/m), THREE;
  * Troland & Crutcher's mu = 2.8 is per H2 MOLECULE against the hydrogen
    mass, while this module's mu = 2.33 is per PARTICLE against m_u.

Usage:  python m12_problems_check.py
Exit 0 and "0 mismatches" is the only acceptable result.
"""
import math
import sys

# --- constants, retyped ---------------------------------------------------
kB = 1.380649e-16            # erg/K            (exact, SI)
m_u = 1.66053906660e-24      # g                (CODATA 2018)
m_p = 1.67262192369e-24      # g                (CODATA 2018)
m_e = 9.1093837015e-28       # g                (CODATA 2018)
e_esu = 4.80320471257e-10    # esu
hbar = 1.054571817e-27       # erg s
c_light = 2.99792458e10      # cm/s             (exact)
G = 6.67430e-8               # cm^3 g^-1 s^-2   (CODATA 2018)
pc = 3.0856775814913673e18   # cm
AU = 1.495978707e13          # cm               (IAU, exact)
yr = 3.15576e7               # s                (Julian)
day = 86400.0                # s
Rsun = 6.957e10              # cm               (IAU 2015 nominal)
GMsun = 1.3271244e26         # cm^3/s^2         (IAU 2015 nominal)
Msun = GMsun/G

NCHK = [0, 0]


def chk(name, expected, got, tol):
    """Compare, with a tolerance matched to the digits the module prints."""
    NCHK[0] += 1
    if expected == 0.0:
        ok = abs(got) <= tol
        rel = abs(got)
    else:
        rel = abs(got/expected - 1.0)
        ok = rel <= tol
    if not ok:
        NCHK[1] += 1
        print(f'  MISMATCH  {name}: printed {expected!r}, rebuilt {got!r} '
              f'(rel {rel:.3e} > tol {tol:.1e})')
    return ok


def chk_dp(name, printed, got, dp):
    """Test the claim the PAGE makes, which is a rounding and not a ratio.

    A value printed to `dp` decimal places asserts only that it rounds
    that way.  Using a relative tolerance on 0.39 degrees or on 12.71
    decades invents a precision the page never claimed -- the failure
    this project's own note on tolerances names.
    """
    NCHK[0] += 1
    ok = round(got, dp) == round(printed, dp)
    if not ok:
        NCHK[1] += 1
        print(f'  MISMATCH  {name}: printed {printed!r}, rebuilt {got!r} '
              f'(rounds to {round(got, dp)!r} at {dp} dp)')
    return ok


def head(s):
    print(f'\n{s}\n' + '-'*len(s))


# =========================================================================
# C1.  STATEMENT GIVES: n = 1e9 cm^-3, T = 1e6 K, B = 10 G (from
#      module07.html:746, illustrative), mu = 0.61, gamma = 5/3.
#      Asked for: p_gas, p_mag, beta, v_A, c_s, and v_A/c_s BOTH ways.
# =========================================================================
head('C1  the active-region corona')
n1, T1, B1, mu1, gam = 1.0e9, 1.0e6, 10.0, 0.61, 5.0/3.0
rho1 = n1*mu1*m_u
chk('C1.rho', 1.0129e-15, rho1, 2e-4)
p_gas1 = n1*kB*T1
chk('C1.p_gas', 1.3806e-1, p_gas1, 2e-4)
p_mag1 = B1*B1/(8.0*math.pi)
chk('C1.p_mag', 3.9789, p_mag1, 2e-4)
beta1 = p_gas1/p_mag1
chk_dp('C1.beta', 0.0347, beta1, 4)
chk_dp('C1.inv_beta', 28.8, 1.0/beta1, 1)
vA1 = B1/math.sqrt(4.0*math.pi*rho1)
chk('C1.vA_kms', 886.4, vA1/1e5, 2e-4)
cs1 = math.sqrt(gam*kB*T1/(mu1*m_u))
chk('C1.cs_kms', 150.7, cs1/1e5, 2e-4)
chk('C1.ratio_speeds', 5.8807, vA1/cs1, 2e-4)
# the identity route, from beta alone -- no mass per particle enters
chk('C1.ratio_identity', 5.8807, math.sqrt(2.0/(gam*beta1)), 2e-4)
# and the two routes against EACH OTHER, which is what the problem asks
chk('C1.identity_closes', 1.0, (vA1/cs1)/math.sqrt(2.0/(gam*beta1)), 1e-12)


# =========================================================================
# C2.  STATEMENT GIVES: L = 1e10 cm, n = 1e9 cm^-3, T = 1e6 K,
#      U = 10 km/s (a LOOP flow speed), ln Lambda = 18.66, and
#      Braginskii sigma_par = 1.96 n e^2 tau_e/m_e with his (2.5e).
#      Asked for: eta_m, Rm, L^2/eta_m, L/U, and their ratio.
# =========================================================================
head('C2  a coronal loop')
L2, U2, lnL2 = 1.0e10, 1.0e6, 18.66
# Braginskii (2.5e), p. 215:  tau_e = 3 sqrt(m_e) (kT)^{3/2}
#                                     / (4 sqrt(2 pi) n lnL e^4)
tau_e2 = (3.0*math.sqrt(m_e)*(kB*T1)**1.5
          / (4.0*math.sqrt(2.0*math.pi)*n1*lnL2*e_esu**4))
sigma2 = 1.96*n1*e_esu*e_esu*tau_e2/m_e
eta_m2 = c_light**2/(4.0*math.pi*sigma2)
chk('C2.eta_m', 9.768e3, eta_m2, 3e-4)
Rm2 = U2*L2/eta_m2
chk('C2.Rm', 1.024e12, Rm2, 3e-4)
t_diff2 = L2*L2/eta_m2
chk('C2.t_diff_yr', 3.244e8, t_diff2/yr, 3e-4)
t_dyn2 = L2/U2
chk('C2.t_dyn_yr', 3.169e-4, t_dyn2/yr, 3e-4)
# The identity (2.4).  Both sides are built here; this is a test and not
# a restatement, because Rm above came from eta_m and U L, and the ratio
# below came from two times.
chk('C2.identity_closes', 1.0, (t_diff2/t_dyn2)/Rm2, 1e-12)


# =========================================================================
# C3.  STATEMENT GIVES: sidereal period 25.38 d (NSSDC, at 16 deg),
#      r0 = 2.5 R_sun, theta = 90 deg, v = 435.6 km/s held CONSTANT.
#      Asked for: -B_phi/B_r and the spiral angle at 1 and 5 au, the
#      local index (5.2), and what dropping r0 does at 1 au.
# =========================================================================
head('C3  the Parker spiral at 1 au and 5 au')
P3_DAYS, P3_V = 25.38, 4.356e7
om3 = 2.0*math.pi/(P3_DAYS*day)
chk('C3.Omega', 2.86533e-6, om3, 3e-5)
r03 = 2.5*Rsun
chk_dp('C3.r0_au', 0.011626, r03/AU, 6)
for r_au, x_exp, ang_exp, idx_exp in ((1.0, 0.9726, 44.20, -1.5082),
                                      (5.0, 4.9088, 78.49, -1.0376)):
    r = r_au*AU
    x = om3*(r - r03)/P3_V
    chk(f'C3.x@{r_au:g}au', x_exp, x, 3e-4)
    chk(f'C3.angle@{r_au:g}au', ang_exp, math.degrees(math.atan(x)), 3e-4)
    # (5.2) at d ln v/d ln r = 0
    idx = -2.0 + (x*x/(1.0 + x*x))*(r/(r - r03))
    chk(f'C3.index@{r_au:g}au', idx_exp, idx, 3e-4)
x1_with = om3*(AU - r03)/P3_V
x1_without = om3*AU/P3_V
chk('C3.x_without_r0', 0.9840, x1_without, 3e-4)
chk_dp('C3.drop_raises_pct', 1.18, (x1_without/x1_with - 1.0)*100.0, 2)
chk_dp('C3.carry_lowers_pct', 1.16,
       (1.0 - x1_with/x1_without)*100.0, 2)


# =========================================================================
# D1.  STATEMENT GIVES: n_tot = 100 cm^-3 per PARTICLE at mu = 2.33, so
#      n(H2) = 83.3; R = 5 pc; B = 10 microgauss (census, no source at
#      this density); c_Phi = 0.53 sqrt5/3pi and 1/2pi.
#      Asked for: M, M_Phi and lambda_Phi for both geometries.
# =========================================================================
head('D1  the 10 pc cloud')
n_tot, mu_mc, B_mc, R_mc = 100.0, 2.33, 1.0e-5, 5.0*pc
# The statement's own conversion, checked rather than assumed: mu = 2.8
# per H2 molecule and 2.333 per particle are one density counted twice.
chk_dp('D1.nH2', 83.3, n_tot*(1.4/0.6)/(1.4/0.5), 1)
rho_mc = n_tot*mu_mc*m_u
chk('D1.rho', 3.8691e-22, rho_mc, 3e-4)
M_mc = (4.0/3.0)*math.pi*R_mc**3*rho_mc
chk('D1.M_Msun', 2.993e3, M_mc/Msun, 3e-4)
Phi_mc = math.pi*R_mc*R_mc*B_mc
chk('D1.Phi', 7.478e33, Phi_mc, 3e-4)
for tag, c_phi, crit_e, Mphi_e, lam_e in (
        ('sphere', 0.53*math.sqrt(5.0)/(3.0*math.pi), 4.8673e2, 1.831e3,
         1.635),
        ('sheet', 1.0/(2.0*math.pi), 6.1605e2, 2.317e3, 1.292)):
    crit = c_phi/math.sqrt(G)
    chk(f'D1.{tag}.crit', crit_e, crit, 3e-4)
    Mphi = crit*Phi_mc
    chk(f'D1.{tag}.Mphi_Msun', Mphi_e, Mphi/Msun, 3e-4)
    chk(f'D1.{tag}.lambda', lam_e, M_mc/Mphi, 3e-4)
chk('D1.c_phi_sphere', 0.125745, 0.53*math.sqrt(5.0)/(3.0*math.pi), 3e-5)
chk('D1.c_phi_sheet', 0.159155, 1.0/(2.0*math.pi), 3e-5)
chk('D1.geometry_factor', 1.2657,
    (1.0/(2.0*math.pi))/(0.53*math.sqrt(5.0)/(3.0*math.pi)), 3e-4)
# The statement's closing claim: that factor against the measured range
# 1.4 to 2.6, in log width.
chk_dp('D1.log_span', 0.381,
       math.log(1.2657)/math.log(2.6/1.4), 3)


# =========================================================================
# D2.  STATEMENT GIVES: n = 7.57 cm^-3, |B| = 6.05 nT, v = 435.6 km/s
#      (MEAN fits), protons only, -B_phi/B_r = 0.9726 from C3, v held
#      CONSTANT, B_r ~ r^-2 and rho ~ r^-2 v^-1.
#      Asked for: B_r, v_A(radial), r_A, and the wrong |B| answer.
# =========================================================================
head('D2  the Alfven radius by hand')
n_sw, Btot_sw, v_sw, x1_sw = 7.57, 6.05e-5, 4.356e7, 0.9726
wind_factor = math.sqrt(1.0 + x1_sw*x1_sw)
chk('D2.wind_factor', 1.3950, wind_factor, 3e-4)
Br_sw = Btot_sw/wind_factor
chk('D2.Br_nT', 4.3370, Br_sw*1e5, 3e-4)
rho_sw = n_sw*m_p
chk('D2.rho', 1.2662e-23, rho_sw, 3e-4)
vA_sw = Br_sw/math.sqrt(4.0*math.pi*rho_sw)
chk('D2.vA_kms', 34.38, vA_sw/1e5, 3e-4)
chk('D2.v_over_vA', 12.669, v_sw/vA_sw, 3e-4)
# At constant v, (6.1) gives v_A ~ 1/r, so the crossing is at
# r_A = 1 au * v_A(1 au)/v.
rA = AU*vA_sw/v_sw
chk('D2.rA_Rsun', 16.97, rA/Rsun, 3e-4)
chk('D2.rA_au', 0.07893, rA/AU, 3e-4)
vA_wrong = Btot_sw/math.sqrt(4.0*math.pi*rho_sw)
chk('D2.rA_wrong_Rsun', 23.68, AU*vA_wrong/v_sw/Rsun, 3e-4)
# and that the wrong answer is exactly wind_factor times the right one
chk('D2.wrong_over_right', wind_factor,
    (AU*vA_wrong/v_sw)/rA, 1e-12)


# =========================================================================
# D3.  STATEMENT GIVES: n = 1e-3 cm^-3, T = 1e8 K, B = 1 microgauss,
#      derived ln Lambda = 37.08 (census 37.8), Braginskii tau_e with
#      4 sqrt(2 pi), kappa_par = 3.16 and kappa_perp = 4.66 at Z = 1;
#      Zhuravleva's 10 to 1000.  Asked for: omega_e tau_e,
#      kappa_perp/kappa_par, then nu_perp/nu_par and the decades.
# =========================================================================
head('D3  the intracluster medium')
n_i, T_i, B_i, lnL_d = 1.0e-3, 1.0e8, 1.0e-6, 37.08
tau_e3 = (3.0*math.sqrt(m_e)*(kB*T_i)**1.5
          / (4.0*math.sqrt(2.0*math.pi)*n_i*lnL_d*e_esu**4))
chk('D3.tau_e', 7.4227e12, tau_e3, 3e-4)
om_e3 = e_esu*B_i/(m_e*c_light)
chk('D3.omega_e', 17.588, om_e3, 3e-4)
wt_e3 = om_e3*tau_e3
chk('D3.wt_e', 1.3055e14, wt_e3, 3e-4)
kap_ratio = (4.66/3.16)/(wt_e3*wt_e3)
chk('D3.kappa_ratio', 8.6523e-29, kap_ratio, 3e-4)
# Braginskii (2.5i), p. 215: the ion time, 4 sqrt(pi) and m_p.
tau_i3 = (3.0*math.sqrt(m_p)*(kB*T_i)**1.5
          / (4.0*math.sqrt(math.pi)*n_i*lnL_d*e_esu**4))
chk('D3.tau_ratio_exact', math.sqrt(2.0*m_p/m_e), tau_i3/tau_e3, 1e-12)
om_i3 = e_esu*B_i/(m_p*c_light)
wt_i3 = om_i3*tau_i3
chk('D3.wt_i', 4.3087e12, wt_i3, 3e-4)
nu_ratio = (0.3/0.96)/(wt_i3*wt_i3)
chk('D3.nu_ratio', 1.6833e-26, nu_ratio, 3e-4)
chk('D3.classical_factor', 5.941e25, 1.0/nu_ratio, 3e-4)
chk_dp('D3.decades_lo', 22.8, math.log10(1.0/nu_ratio/1000.0), 1)
chk_dp('D3.decades_hi', 24.8, math.log10(1.0/nu_ratio/10.0), 1)


# =========================================================================
# K1.  STATEMENT GIVES: R = 1 au, M = 1 Msun, B = 1 G, n = 1e14 cm^-3,
#      T = 300 K, mu = 2.33, q = 3/2 ASSUMED.  Asked for: Omega_K,
#      gamma_max, e-folds per orbit, v_A, c_s, H, lambda_marg, verdict.
# =========================================================================
head('K1  the MRI in a protoplanetary disc')
R_d, B_d, n_d, T_d, mu_d, q_d = AU, 1.0, 1.0e14, 300.0, 2.33, 1.5
om_K = math.sqrt(GMsun/R_d**3)
chk('K1.Omega_K', 1.9910e-7, om_K, 3e-4)
chk_dp('K1.period_yr', 1.00, (2.0*math.pi/om_K)/yr, 2)
gam_max = (q_d/2.0)*om_K
chk('K1.gamma_max', 1.4932e-7, gam_max, 3e-4)
chk('K1.efolds', 4.712, 2.0*math.pi*gam_max/om_K, 3e-4)
# the identity the problem asks about: it is 3 pi/2 with no inputs
chk('K1.efolds_identity', 3.0*math.pi/2.0, 2.0*math.pi*(q_d/2.0), 1e-12)
rho_d = n_d*mu_d*m_u
vA_d = B_d/math.sqrt(4.0*math.pi*rho_d)
chk('K1.vA_kms', 0.1434, vA_d/1e5, 3e-3)
cs_d = math.sqrt((5.0/3.0)*kB*T_d/(mu_d*m_u))
chk('K1.cs_kms', 1.3357, cs_d/1e5, 3e-4)
H_d = cs_d/om_K
chk('K1.H_au', 0.04485, H_d/AU, 3e-4)
lam_marg = 2.0*math.pi*vA_d/(math.sqrt(3.0)*om_K)
chk('K1.lam_marg_au', 0.01747, lam_marg/AU, 3e-3)
chk('K1.lam_marg_over_H', 0.3895, lam_marg/H_d, 3e-3)
chk_dp('K1.beta', 104.1,
       (n_d*kB*T_d)/(B_d*B_d/(8.0*math.pi)), 1)
if lam_marg >= H_d:
    NCHK[1] += 1
    print('  MISMATCH  K1.verdict: module says unstable, rebuilt says not')
NCHK[0] += 1


# =========================================================================
# K2.  STATEMENT GIVES: rho_h = 5.8609e-16, rho_l = 2.6211e-16 g/cm^3
#      (from module07.html:638), Delta_U = 20 km/s an UPPER LIMIT, and
#      (4.2) with 2 pi, or 4 pi one-sided.  Asked for: both bounds and
#      the angle at 1 G and 10 G, measured FROM PERPENDICULAR.
# =========================================================================
head("K2  Module 7's one-degree bound")
rho_h, rho_l, dU = 5.8609e-16, 2.6211e-16, 2.0e6
pref = math.sqrt(2.0*math.pi*rho_h*rho_l/(rho_h + rho_l))
b_two = dU*pref
chk('K2.bound_two_sided', 0.06747, b_two, 3e-4)
b_one = dU*math.sqrt(2.0)*pref
chk('K2.bound_one_sided', 0.09541, b_one, 3e-4)
# Module 7's own printed numbers, retyped from module07.html section 9.5.
chk('K2.vs_M7_two', 0.9995, b_two/0.0675, 3e-4)
chk('K2.vs_M7_one', 1.0001, b_one/0.0954, 3e-4)
for B_g, ct_exp, ang_exp in ((1.0, 0.06747, 3.87), (10.0, 0.006747, 0.39)):
    ct = b_two/B_g
    chk(f'K2.cos@{B_g:g}G', ct_exp, ct, 3e-4)
    chk_dp(f'K2.angle@{B_g:g}G', ang_exp,
           math.degrees(math.asin(ct)), 2)
# the wrong function, which the statement asks the reader to identify
chk('K2.arccos_trap', 86.13, math.degrees(math.acos(b_two/1.0)), 3e-4)


# =========================================================================
# K3.  STATEMENT GIVES: n = 1e-3, T = 1e8, B = 1 microgauss; lambda is
#      Module 1's Coulomb mean free path at ln Lambda = 37.8; r_g uses
#      v_perp = sqrt(2kT/m_p); and Braginskii's tau_i uses the derived
#      ln Lambda = 37.081.  Asked for: both magnetisations, the ratio,
#      and its exact account.
# =========================================================================
head('K3  the two magnetisations of one plasma')
lnL_c = 37.8
# Module 1's Spitzer coefficient, retyped: 3^{3/2}/(4 sqrt(pi)).
SPITZER_C = 3.0**1.5/(4.0*math.sqrt(math.pi))
lam_k3 = SPITZER_C*(kB*T_i)**2/(n_i*e_esu**4*lnL_c)
chk('K3.lambda_kpc', 22.5, lam_k3/(1.0e3*pc), 3e-3)
v_perp = math.sqrt(2.0*kB*T_i/m_p)
chk('K3.v_perp_kms', 1285.0, v_perp/1e5, 1e-3)
v_rms = math.sqrt(3.0*kB*T_i/m_p)
chk('K3.v_rms_kms', 1574.0, v_rms/1e5, 1e-3)
om_k3 = e_esu*B_i/(m_p*c_light)
chk('K3.omega_c', 9.579e-3, om_k3, 3e-4)
r_g = v_perp/om_k3
chk('K3.r_g_km', 1.3414e5, r_g/1e5, 3e-4)
route_A = lam_k3/r_g
chk('K3.lam_over_rg', 5.1767e12, route_A, 3e-4)
# The OTHER route to the same quantity: omega tau with tau = lam/v_perp.
# Two expressions, one number -- which is the identity the module claims.
chk('K3.route_A_identity', 1.0, (om_k3*(lam_k3/v_perp))/route_A, 1e-12)
lnL_e_k3 = 37.081
tau_i_k3 = (3.0*math.sqrt(m_p)*(kB*T_i)**1.5
            / (4.0*math.sqrt(math.pi)*n_i*lnL_e_k3*e_esu**4))
route_B = om_k3*tau_i_k3
chk('K3.omega_i_tau_i', 4.3087e12, route_B, 3e-4)
chk('K3.ratio', 1.2015, route_A/route_B, 3e-4)
chk('K3.sqrt32', 1.224745, math.sqrt(1.5), 1e-6)
chk('K3.lnL_ratio', 0.980985, lnL_e_k3/lnL_c, 1e-5)
chk('K3.product', 1.2015, math.sqrt(1.5)*lnL_e_k3/lnL_c, 3e-4)
# THE TEST, not the restatement: the decomposition must reproduce the
# ratio built from the two independent routes above, to machine precision
# once the two Coulomb logarithms are the only difference left.
chk('K3.decomposition_closes', route_A/route_B,
    math.sqrt(1.5)*lnL_e_k3/lnL_c, 1e-5)
chk_dp('K3.log10_count', 12.71, math.log10(route_A), 2)
# The page prints this to TWO decimals.  The first draft of both the
# page and this line said 1.444; the ratio squared is 1.4435, which
# rounds to 1.44 and not to 1.444.
chk_dp('K3.suppression_penalty', 1.44, (route_A/route_B)**2, 2)


print(f'\n[m12_problems_check] {NCHK[0]} checks, {NCHK[1]} mismatch(es)')
sys.exit(1 if NCHK[1] else 0)
