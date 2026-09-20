"""Independent verification of every number in Module 10's problem set.

IT IMPORTS NOTHING FROM m10_numbers.py.  Physical constants are retyped
here from CODATA/IAU, and every modelling input is taken from the PROBLEM
STATEMENT as printed in module10.html -- not from the generator.  That is
the whole point of the script, and the rule comes from Module 9, where a
problem's printed answer needed two modelling facts (a hydrogen density
rather than a total density, and a helium fraction) that appeared only
inside m09_numbers.py.  The problems check could not catch it, because it
read the same two facts from the same place.

So for each slot below, the header comment quotes the inputs the statement
gives, and the code uses those and nothing else.  Where a statement gives
a derived quantity as well as the inputs that produce it -- D1 states the
mean free path AND the density, temperature and Coulomb logarithm -- both
routes are computed and compared, which turns a restatement into a test.

Usage:  python m10_problems_check.py
Exit 0 and "0 mismatches" is the only acceptable result.
"""
import math

# --- constants, retyped ---------------------------------------------------
kB = 1.380649e-16            # erg/K            (exact, SI)
m_u = 1.66053906660e-24      # g                (CODATA 2018)
m_p = 1.67262192369e-24      # g                (CODATA 2018)
e_esu = 4.80320471257e-10    # esu
pc = 3.0856775814913673e18   # cm
kpc = 1.0e3*pc
AU = 1.495978707e13          # cm               (IAU, exact)
yr = 3.15576e7               # s                (Julian)
keV = 1.602176634e-9         # erg              (exact, SI)

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


def head(s):
    print(f'\n{s}\n' + '-'*len(s))


# =========================================================================
# C1.  STATEMENT GIVES: nu = 0.15 cm^2/s (2 s.f., no primary source);
#      eps = 1e-3 W/kg.  Asked for: eps in CGS, eta, u_eta, tau_eta, and
#      the identity u_eta eta/nu.
# =========================================================================
head('C1  Kolmogorov microscales in the atmosphere')
nu_air = 0.15
eps_C1 = 1.0e-3 * 1.0e4          # W/kg -> erg/g/s: 1e7 erg / 1e3 g
chk('C1 eps in CGS (erg/g/s)', 10.0, eps_C1, 1e-12)
eta_C1 = (nu_air**3/eps_C1)**0.25
u_C1 = (nu_air*eps_C1)**0.25
tau_C1 = (nu_air/eps_C1)**0.5
chk('C1 eta (mm)', 1.355, eta_C1*10.0, 1e-3)
chk('C1 u_eta (cm/s)', 1.11, u_C1, 5e-3)
chk('C1 tau_eta (ms)', 122.47, tau_C1*1e3, 1e-4)
chk('C1 identity u_eta eta/nu', 1.0, u_C1*eta_C1/nu_air, 1e-12)
print(f'    [note] eta = {eta_C1*10:.4f} mm, u_eta = {u_C1:.4f} cm/s, '
      f'tau_eta = {tau_C1*1e3:.3f} ms; two significant figures are all '
      f'nu supports')

# =========================================================================
# C2.  STATEMENT GIVES: L = 10 pc; Larson's THREE-DIMENSIONAL sigma_L =
#      2.64 km/s; c_s = 0.244 km/s at T = 10 K, mu = 2.33, gamma = 5/3.
#      Asked for: turnover time, sound crossing time, and which matters.
# =========================================================================
head('C2  eddy turnover and sound crossing of a 10 pc cloud')
L_C2 = 10.0*pc
sig_C2 = 2.64e5
cs_C2 = 0.244e5
# The sound speed is ALSO rebuilt from the inputs the statement gives, so
# that "c_s = 0.244" is tested rather than trusted.
cs_rebuilt = math.sqrt((5.0/3.0)*kB*10.0/(2.33*m_u))
chk('C2 c_s rebuilt from T, mu, gamma (km/s)', 0.244, cs_rebuilt/1e5, 3e-3)
chk('C2 turnover L/sigma (Myr)', 3.70, L_C2/sig_C2/yr/1e6, 3e-3)
chk('C2 sound crossing L/c_s (Myr)', 40.1, L_C2/cs_C2/yr/1e6, 3e-3)
chk('C2 ratio of the two times = Mach number', 10.82, sig_C2/cs_C2, 2e-3)
chk('C2 L in cm', 3.0857e19, L_C2, 1e-4)

# =========================================================================
# C3.  STATEMENT GIVES: the same cloud; eps = U^3/L with U = sigma_L,
#      NAMED AS A K41 RELATION AND NOT A MEASUREMENT; l = 1 pc.
#      Asked for: S_3(l), |S_3|^(1/3), (eps l)^(1/3), and the ratio.
# =========================================================================
head('C3  the four-fifths law at 1 pc in that cloud')
eps_C3 = sig_C2**3/L_C2
l_C3 = 1.0*pc
S3 = -0.8*eps_C3*l_C3
dv_S3 = abs(S3)**(1.0/3.0)
dv_dim = (eps_C3*l_C3)**(1.0/3.0)
chk('C3 eps = U^3/L (erg/g/s)', 5.963e-4, eps_C3, 5e-4)
chk('C3 S_3(1 pc) (cm^3/s^3)', -1.472e15, S3, 5e-4)
chk('C3 |S_3|^(1/3) (km/s)', 1.138, dv_S3/1e5, 5e-4)
chk('C3 (eps l)^(1/3) (km/s)', 1.225, dv_dim/1e5, 5e-4)
chk('C3 ratio', 0.9283, dv_S3/dv_dim, 1e-4)
# The ratio must be (4/5)^(1/3) EXACTLY, whatever eps and l are: that is
# the point the solution asks the student to see without arithmetic.
chk('C3 ratio == (4/5)^(1/3) identically', (0.8)**(1.0/3.0),
    dv_S3/dv_dim, 1e-12)

# =========================================================================
# D1.  STATEMENT GIVES: n = 1e-3 cm^-3, T = 1e8 K, lnLambda = 37.8,
#      "giving a Coulomb mean free path of 22.5 kpc and an ion mean
#      thermal speed of 1450 km/s"; U = 164 km/s, L = 60 kpc; B = 1 uG.
#      Asked for: eps and eta unmagnetised, THEN whether that answer is
#      admissible, THEN eta with the magnetised bound.
# =========================================================================
head('D1  the dissipation scale of the intracluster medium')
n_icm, T_icm, lnL_icm = 1.0e-3, 1.0e8, 37.8
# Rebuild the two quantities the statement supplies, from the three it
# also supplies.  Module 1's Spitzer coefficient is 3^(3/2)/(4 sqrt(pi)).
spitzer = 3.0**1.5/(4.0*math.sqrt(math.pi))
lam_icm = spitzer*(kB*T_icm)**2/(n_icm*e_esu**4*lnL_icm)
chk('D1 lambda rebuilt from n, T, lnLambda (kpc)', 22.5, lam_icm/kpc, 3e-3)
v_icm = math.sqrt(8.0*kB*T_icm/(math.pi*m_p))
chk('D1 ion mean thermal speed rebuilt (km/s)', 1450.0, v_icm/1e5, 1e-3)
nu_icm = lam_icm*v_icm/3.0
chk('D1 nu = lam v/3 (cm^2/s)', 3.3557e30, nu_icm, 5e-4)
U_icm, L_icm = 1.64e7, 60.0*kpc
eps_icm = U_icm**3/L_icm
chk('D1 eps = U^3/L (erg/g/s)', 2.382e-2, eps_icm, 5e-4)
eta_icm = (nu_icm**3/eps_icm)**0.25
chk('D1 eta unmagnetised (kpc)', 64.67, eta_icm/kpc, 5e-4)
chk('D1 eta/L -- the premise fails because this exceeds 1', 1.078,
    eta_icm/L_icm, 5e-4)
assert eta_icm > L_icm, 'D1 loses its point if eta <= L'
chk('D1 Kn = lam/L, the same failure seen from the other end', 0.375,
    lam_icm/L_icm, 5e-3)
B_icm = 1.0e-5
v_perp = math.sqrt(2.0*kB*T_icm/m_p)      # TWO components, across B
rg_icm = m_p*v_perp*2.99792458e10/(e_esu*B_icm)
chk('D1 r_g at 1 microgauss (cm)', 1.341e9, rg_icm, 1e-3)
nu_perp = rg_icm*v_icm/3.0
chk('D1 nu_perp upper bound (cm^2/s)', 6.4824e16, nu_perp, 5e-5)
chk('D1 eta magnetised lower bound (au)', 0.691,
    (nu_perp**3/eps_icm)**0.25/AU, 2e-3)
chk('D1 Re_perp lower bound', 4.684e13, U_icm*L_icm/nu_perp, 5e-4)

# =========================================================================
# D2.  STATEMENT GIVES: M = 10, the RMS SONIC Mach number; b = 1/3
#      (purely solenoidal in 3-D) and b = 1 (purely compressive), both
#      from Federrath et al. (2010); threshold rho > 100 <rho>.
# =========================================================================
head('D2  the log-normal width and its tail at Mach 10')
MACH = 10.0
for b, s_exp, f_exp in ((1.0/3.0, 1.5793, 1.054e-4), (1.0, 2.1483, 6.459e-4)):
    sig_s = math.sqrt(math.log(1.0 + b*b*MACH*MACH))
    s0 = -0.5*sig_s*sig_s
    f100 = 0.5*math.erfc((math.log(100.0) - s0)/(sig_s*math.sqrt(2.0)))
    chk(f'D2 sigma_s at b = {b:.3f}', s_exp, sig_s, 5e-5)
    chk(f'D2 f(>100) at b = {b:.3f}', f_exp, f100, 5e-4)
sig_lo = math.sqrt(math.log(1.0 + MACH*MACH/9.0))
sig_hi = math.sqrt(math.log(1.0 + MACH*MACH))
chk('D2 width ratio', 1.36, sig_hi/sig_lo, 5e-3)
f_lo = 0.5*math.erfc((math.log(100.0) + 0.5*sig_lo**2)/(sig_lo*math.sqrt(2)))
f_hi = 0.5*math.erfc((math.log(100.0) + 0.5*sig_hi**2)/(sig_hi*math.sqrt(2)))
chk('D2 tail ratio at 100 <rho>', 6.1, f_hi/f_lo, 1e-2)
g_lo = 0.5*math.erfc((math.log(1e3) + 0.5*sig_lo**2)/(sig_lo*math.sqrt(2)))
g_hi = 0.5*math.erfc((math.log(1e3) + 0.5*sig_hi**2)/(sig_hi*math.sqrt(2)))
chk('D2 tail ratio at 1000 <rho>', 73.9, g_hi/g_lo, 5e-3)
chk('D2 s_0 at b = 1/3', -1.247, -0.5*sig_lo**2, 1e-3)
chk('D2 s_0 at b = 1', -2.308, -0.5*sig_hi**2, 1e-3)

# =========================================================================
# D3.  STATEMENT GIVES: n = 1e2 cm^-3 of H2, T = 10 K, mu = 2.33,
#      sigma_H = 1e-15 cm^2, L = 10 pc, and Larson's THREE-DIMENSIONAL
#      sigma_L = 2.64 km/s as the outer-scale speed.
# =========================================================================
head('D3  the Reynolds number and the scale range of a 10 pc cloud')
n_mc, T_mc, mu_mc, sigH = 1.0e2, 10.0, 2.33, 1.0e-15
lam_mc = 1.0/(n_mc*sigH)
v_mc = math.sqrt(8.0*kB*T_mc/(math.pi*mu_mc*m_u))
nu_mc = lam_mc*v_mc/3.0
Re_mc = sig_C2*L_C2/nu_mc
chk('D3 lambda (cm)', 1.0e13, lam_mc, 1e-12)
chk('D3 lambda (au)', 0.67, lam_mc/AU, 5e-3)
chk('D3 mean thermal speed (km/s)', 0.3014, v_mc/1e5, 5e-4)
chk('D3 nu (cm^2/s)', 1.0048e17, nu_mc, 5e-5)
chk('D3 Re', 8.107e7, Re_mc, 5e-4)
chk('D3 L/eta from Re^(3/4)', 8.54e5, Re_mc**0.75, 2e-3)
eta_mc = (nu_mc**3/eps_C3)**0.25
chk('D3 eta directly (au)', 2.4, eta_mc/AU, 2e-2)
chk('D3 L/eta directly agrees with Re^(3/4)', Re_mc**0.75,
    L_C2/eta_mc, 1e-9)
# 3.2e-7 is printed to TWO significant figures, so half a unit in the
# last digit is 0.05/3.2 = 1.6 per cent.  A tighter tolerance here would
# fail a number the module never claimed to more precision than this.
chk('D3 Kn -- the licence this Reynolds number needs', 3.2e-7,
    lam_mc/L_C2, 1.6e-2)

# =========================================================================
# K1.  STATEMENT GIVES: Re = 1e6; 24 bytes per point (three components at
#      eight bytes); the CFL count Re^3 is the one asked for.
# =========================================================================
head('K1  the cost of a direct numerical simulation at Re = 1e6')
Re_K1 = 1.0e6
chk('K1 grid side Re^(3/4)', 31623.0, Re_K1**0.75, 1e-4)
chk('K1 total points Re^(9/4)', 3.162e13, Re_K1**2.25, 5e-4)
chk('K1 one snapshot (bytes)', 7.589e14, 24.0*Re_K1**2.25, 5e-4)
chk('K1 one snapshot (TB, 1e12 B)', 759.0, 24.0*Re_K1**2.25/1e12, 5e-4)
chk('K1 work, CFL count Re^3', 1.0e18, Re_K1**3, 1e-12)
chk('K1 softer count Re^(11/4)', 3.16e16, Re_K1**2.75, 1e-3)
chk('K1 the two differ by Re^(1/4)', 31.6, Re_K1**0.25, 2e-3)
chk('K1 and that equals U/u_eta by construction', Re_K1**3/Re_K1**2.75,
    Re_K1**0.25, 1e-12)

# =========================================================================
# K2.  STATEMENT GIVES: (a) a 20 per cent mass bias, kT = 4.1 keV,
#      mu = 0.61, and Hitomi's measured 164 km/s.  (b) the cloud of D3,
#      k = 1/(1 pc), C = 1.62 -- with the range 1.53-1.62 named.
# =========================================================================
head('K2  the dispersion a 20 per cent bias needs, and E(k) in the cloud')
bias = 0.20
alpha_K2 = bias/(1.0 - bias)
chk('K2a alpha from bias/(1-bias)', 0.2500, alpha_K2, 1e-12)
kT_K2, mu_K2 = 4.1*keV, 0.61
sig_K2 = math.sqrt(alpha_K2*kT_K2/(mu_K2*m_u))
chk('K2a required sigma_v (km/s)', 403.0, sig_K2/1e5, 3e-3)
chk('K2a ratio to Hitomi 164 km/s', 2.46, sig_K2/1.64e7, 3e-3)
chk('K2a and the pressure ratio goes as the square', 6.0,
    (sig_K2/1.64e7)**2, 1e-2)
k_K2 = 1.0/pc
E_162 = 1.62*eps_C3**(2.0/3.0)*k_K2**(-5.0/3.0)
E_153 = 1.53*eps_C3**(2.0/3.0)*k_K2**(-5.0/3.0)
chk('K2b E(k) at C = 1.62 (cm^3/s^2)', 7.503e28, E_162, 5e-4)
# The module prints the low end only to two figures, so that is what is
# checked; a four-figure expectation here would be a number the module
# does not contain.
print(f'    [note] E(1/pc) spans {E_153:.3e} to {E_162:.3e} cm^3/s^2 over '
      f'the constant range 1.53-1.62, which is why the module prints '
      f'"7.1 to 7.5 x 10^28"')
chk('K2b low end to two figures (1e28)', 7.1, E_153/1e28, 5e-3)
chk('K2b high end to two figures (1e28)', 7.5, E_162/1e28, 5e-3)

# =========================================================================
# K3.  STATEMENT GIVES: the intracluster medium of D1, with and without a
#      field; and N = 1e9 grid points.
# =========================================================================
head('K3  the two Reynolds numbers of the cluster, and a grid budget')
# 0.90, two figures: half a unit in the last digit is 0.005/0.90.
chk('K3a Re unmagnetised', 0.90, U_icm*L_icm/nu_icm, 5.6e-3)
chk('K3a Kn printed beside it', 0.375, lam_icm/L_icm, 5e-3)
Ma_icm = U_icm/v_icm
chk('K3a Ma_th', 0.113, Ma_icm, 5e-3)
chk('K3a 3 Ma_th, the threshold Kn exceeds', 0.34, 3.0*Ma_icm, 2e-2)
assert lam_icm/L_icm > 3.0*Ma_icm, 'K3a: Re < 1 because Kn > 3 Ma_th'
chk('K3a identity 3 Ma_th/Kn == U L/nu', U_icm*L_icm/nu_icm,
    3.0*Ma_icm/(lam_icm/L_icm), 1e-9)
chk('K3a Re_perp lower bound', 4.68e13, U_icm*L_icm/nu_perp, 2e-3)
chk('K3b Re at which N = 1e9', 1.000e4, (1.0e9)**(4.0/9.0), 1e-6)
Re_phot = 1.398e9
# 3.8e20, two figures: 0.05/3.8 = 1.3 per cent.
chk('K3b photosphere N = Re^(9/4)', 3.8e20, Re_phot**2.25, 1.3e-2)
chk('K3b that is how many orders of magnitude above 1e9', 11.58,
    math.log10(Re_phot**2.25/1.0e9), 5e-3)
chk('K3b and the Reynolds numbers differ by this many orders', 5.15,
    math.log10(Re_phot/1.0e4), 5e-3)

print('\n' + '='*74)
print(f'{NCHK[0]} checks, {NCHK[1]} mismatches')
print('='*74)
if NCHK[1] == 0:
    print('  every printed problem-set number was rebuilt from the inputs')
    print('  its own STATEMENT gives, with nothing imported from')
    print('  m10_numbers.py')
raise SystemExit(1 if NCHK[1] else 0)
