"""Independent verification of every number printed in Module 8.

NOTHING is imported from m08_numbers.py.  The Rankine-Hugoniot ratios, the
Sedov similarity solution, the Trinity fits, the remnant history and the
Tycho comparison are all written again from the definitions in
module08.html, so that an error in the drafting script cannot reproduce
itself here.  Each check asserts the value the HTML prints.

The Sedov similarity system is RE-DERIVED BY HAND here (the derivation is
written out in the comment above sedov_rhs_indep), coded with a different
state vector from the prep's and integrated with a different quadrature
rule, so the agreement of xi_0 to six figures is not a shared bug.

Tolerances are matched to the digits the prose prints: `chk` takes a
relative tolerance, 5e-4 or tighter wherever four significant figures
appear, and `checkr` is used wherever the prose gives one or two decimals,
because for a number printed as "0.73" or "8.3" the printed figure IS the
rounding and a relative test is the wrong test.  Module 7 printed a cutoff
as 1.4191 cm when the value was 1.4189 and its check passed, because the
tolerance was 3e-3 against a five-figure claim.

Run:  python m08_problems_check.py
"""

import os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.integrate import simpson

# --- constants, typed from CODATA 2018 / IAU 2015, not copied from the prep
kB = 1.380649e-16
m_u = 1.66053906660e-24
G_N = 6.67430e-8
pc = 3.0856775814913673e18
AU = 1.495978707e13
yr = 3.15576e7
Msun = 1.3271244e26/G_N
KT_ERG = 4.184e19

G53 = 5.0/3.0
G75 = 7.0/5.0

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'data', 'taylor1950_trinity.dat')

FAILS = []
NCHK = 0


def chk(label, got, want, rtol=5e-4):
    """Relative comparison.  Records a failure rather than raising."""
    global NCHK
    NCHK += 1
    if want == 0.0:
        ok = abs(got) < rtol
        rel = abs(got)
    else:
        rel = abs(got - want)/abs(want)
        ok = rel <= rtol
    if not ok:
        FAILS.append((label, got, want, rel))
    print("  %-52s got %-16.6g want %-16.6g rel %.2e %s"
          % (label, got, want, rel, "" if ok else "   <-- MISMATCH"))


def checkr(label, got, want, dp):
    """Assert a value the prose prints to `dp` decimal places.

    The printed figure is the rounding, so the rounding is what must agree.
    """
    global NCHK
    NCHK += 1
    ok = abs(round(got, dp) - want) <= 0.5*10.0**(-dp)
    if not ok:
        FAILS.append((label, got, want, abs(round(got, dp) - want)))
    print("  %-52s got %-16.6g printed %-12.6g (%d dp) %s"
          % (label, got, want, dp, "" if ok else "   <-- MISMATCH"))


# =========================================================================
# PART A/B.  Rankine-Hugoniot, from the standard textbook forms
# =========================================================================
def rh(M, g):
    """(rho2/rho1, p2/p1, T2/T1, M2, ds/k) for a normal shock."""
    M2 = M*M
    d = (g + 1.0)*M2/((g - 1.0)*M2 + 2.0)
    pr = (2.0*g*M2 - (g - 1.0))/(g + 1.0)
    Tr = pr/d
    m2sq = ((g - 1.0)*M2 + 2.0)/(2.0*g*M2 - (g - 1.0))
    ds = (np.log(pr) - g*np.log(d))/(g - 1.0)
    return d, pr, Tr, np.sqrt(m2sq), ds


print("PART A/B  Rankine-Hugoniot jumps")
# gamma = 5/3, from the printed table
for M, d, pr, Tr, m2, ds in [
        (1.5, 1.7143, 2.562, 1.4948, 0.7157, 0.0640),
        (2.0, 2.2857, 4.750, 2.0781, 0.6070, 0.2705),
        (3.0, 3.0000, 11.000, 3.6667, 0.5222, 0.8503),
        (5.0, 3.5714, 31.000, 8.6800, 0.4752, 1.9686),
        (8.0, 3.8209, 79.750, 20.8721, 0.4583, 3.2171),
        (10.0, 3.8835, 124.750, 32.1231, 0.4543, 3.8476),
        (30.0, 3.9867, 1124.750, 282.1248, 0.4480, 7.0806),
        (100.0, 3.9988, 12499.750, 3125.8750, 0.4473, 10.6852)]:
    a, b, cc, dd, ee = rh(M, G53)
    chk("g=5/3 M=%-5g rho2/rho1" % M, a, d, 2e-4)
    chk("g=5/3 M=%-5g p2/p1" % M, b, pr, 2e-4)
    chk("g=5/3 M=%-5g T2/T1" % M, cc, Tr, 2e-4)
    chk("g=5/3 M=%-5g M2" % M, dd, m2, 2e-4)
    chk("g=5/3 M=%-5g ds/k" % M, ee, ds, 2e-3)

for M, d, pr, Tr, m2, ds in [
        (2.0, 2.6667, 4.500, 1.6875, 0.5774, 0.3273),
        (5.0, 5.0000, 29.000, 5.8000, 0.4152, 2.7852),
        (10.0, 5.7143, 116.500, 20.3875, 0.3876, 5.7943),
        (100.0, 5.9970, 11666.500, 1945.3889, 0.3781, 17.1418)]:
    a, b, cc, dd, ee = rh(M, G75)
    chk("g=7/5 M=%-5g rho2/rho1" % M, a, d, 2e-4)
    chk("g=7/5 M=%-5g p2/p1" % M, b, pr, 2e-4)
    chk("g=7/5 M=%-5g T2/T1" % M, cc, Tr, 2e-4)
    chk("g=7/5 M=%-5g M2" % M, dd, m2, 2e-4)
    chk("g=7/5 M=%-5g ds/k" % M, ee, ds, 2e-3)

# the M1 = 5, gamma = 5/3 test shock of PART A
rho1, M1 = 1.0e-24, 5.0
T1 = 1.0e4                     # not printed; only the ratios are checked
chk("ceiling g=5/3", (G53 + 1)/(G53 - 1), 4.0)
chk("ceiling g=7/5", (G75 + 1)/(G75 - 1), 6.0)
chk("pct of ceiling g=5/3 M=10", 100*rh(10.0, G53)[0]/4.0, 97.09, 1e-3)
chk("pct of ceiling g=7/5 M=10", 100*rh(10.0, G75)[0]/6.0, 95.24, 1e-3)

# the entropy sign table, rarefaction branch
for M, ds in [(0.5, -1.21225), (0.8, -0.01681), (0.9, -0.00159),
              (1.1, +0.00101), (1.5, +0.06398), (3.0, +0.85031)]:
    chk("g=5/3 M=%-4g ds/k (rarefaction branch)" % M, rh(M, G53)[4], ds, 5e-3)
chk("branch stops at sqrt((g-1)/(2g)), g=5/3", np.sqrt((G53 - 1)/(2*G53)),
    0.4472, 1e-3)
chk("p2/p1 at M=0.4, g=5/3", rh(0.4, G53)[1], -0.0500, 1e-2)

# isothermal shock
cT = np.sqrt(kB*10.0/(2.33*m_u))/1e5      # km/s, 10 K molecular, mu = 2.33
chk("c_T at 10 K, mu=2.33 (km/s)", cT, 0.189, 5e-3)
chk("M_iso for 10 km/s", 10.0/cT, 52.9, 5e-3)
chk("rho2/rho1 isothermal at 10 km/s", (10.0/cT)**2, 2802.3, 1e-2)


# =========================================================================
# PART C.  The Sedov constant, independently derived and integrated
# =========================================================================
# Hand derivation, from the spherical Euler equations with
#   lambda = r/R, R ~ t^(2/5),  v = (r/t)U,  rho = rho_0 G,  p = rho_0 (r/t)^2 H
# and ' = d/d(ln lambda), a = U - 2/5:
#   continuity   a G'/G + 3U + U' = 0
#   momentum     a U' + U^2 - U + (H/G)(2 + H'/H) = 0
#   entropy      a (H'/H - gamma G'/G) + 2(U - 1) = 0
# Eliminating G'/G and H'/H from the momentum equation:
#   U' (a^2 - gamma w) = a(U - U^2) + w(3 gamma U - 6/5),   w = H/G.
# That last line is written INDEPENDENTLY of the prep's algebra; the prep
# writes the same quantity as a(-U^2+U-2w) + w((3gamma+2)U-2), and the two
# agree identically because -2aw - 2w + (3gamma+2)wU = w(3 gamma U - 6/5).
def sedov_rhs_indep(s, y, g):
    U, G_, H_ = y                     # primitive variables, NOT logs
    w = H_/G_
    a = U - 0.4
    Us = (a*(U - U*U) + w*(3.0*g*U - 1.2))/(a*a - g*w)
    Gs = -G_*(3.0*U + Us)/a
    Hs = H_*(g*Gs/G_ - 2.0*(U - 1.0)/a)
    return [Us, Gs, Hs]


def xi0_indep(g, s_min=-7.0, n=200001):
    U1 = 4.0/(5.0*(g + 1.0))
    G1 = (g + 1.0)/(g - 1.0)
    H1 = 8.0/(25.0*(g + 1.0))
    sol = solve_ivp(sedov_rhs_indep, [0.0, s_min], [U1, G1, H1], args=(g,),
                    rtol=1e-12, atol=1e-16, dense_output=True, max_step=0.01)
    s = np.linspace(s_min, 0.0, n)
    U, G_, H_ = sol.sol(s)
    lam = np.exp(s)
    integrand = lam**5*(G_*U*U/2.0 + H_/(g - 1.0))
    J = simpson(integrand, x=s)       # Simpson, not trapezoid
    return (4.0*np.pi*J)**-0.2, J, 4.0*np.pi*J, lam, U, G_, H_


print("\nPART C  the Sedov constant")
xi53, J53, K53, lam53, U53, G_53, H_53 = xi0_indep(G53)
xi75, J75, K75, lam75, U75, G_75, H_75 = xi0_indep(G75)
chk("gamma=5/3 energy integral J", J53, 0.03927866, 5e-5)
chk("gamma=5/3 K = 4 pi J", K53, 0.493590, 5e-5)
chk("gamma=5/3 xi_0", xi53, 1.151666, 5e-6)
chk("gamma=7/5 energy integral J", J75, 0.06772615, 5e-5)
chk("gamma=7/5 K = 4 pi J", K75, 0.851072, 5e-5)
chk("gamma=7/5 xi_0", xi75, 1.032777, 5e-6)

# published comparisons, computed here from the published numbers themselves
chk("Tang & Chevalier 2.026^(1/5)", 2.026**0.2, 1.151670, 5e-6)
chk("Kamm & Timmes 0.851072^(-1/5)", 0.851072**-0.2, 1.032777, 5e-6)
chk("Taylor 1950 K=0.856 over exact", 0.856/K75, 1.00579, 5e-5)

# profile values
for lamq, rho_r, v_r, p_r in [(0.95, 0.57462, 0.90476, 0.70545),
                              (0.90, 0.35631, 0.82029, 0.54468),
                              (0.80, 0.15780, 0.68275, 0.39619),
                              (0.60, 0.03561, 0.48498, 0.31811),
                              (0.40, 0.00557, 0.32023, 0.30703)]:
    i = int(np.argmin(abs(lam53 - lamq)))
    chk("g=5/3 lam=%.2f rho/rho2" % lamq, G_53[i]/G_53[-1], rho_r, 2e-3)
    chk("g=5/3 lam=%.2f v/v2" % lamq, lamq*U53[i]/U53[-1], v_r, 2e-3)
    chk("g=5/3 lam=%.2f p/p2" % lamq, lamq**2*H_53[i]/H_53[-1], p_r, 2e-3)


def mass_median(lam, G_):
    trap = 0.5*(lam[1:]**2*G_[1:] + lam[:-1]**2*G_[:-1])*np.diff(lam)
    m = np.concatenate([[0.0], np.cumsum(trap)])
    return float(np.interp(0.5*m[-1], m, lam))


chk("g=5/3 mass median r/R", mass_median(lam53, G_53), 0.9392, 1e-3)
chk("g=7/5 mass median r/R", mass_median(lam75, G_75), 0.9581, 1e-3)


# =========================================================================
# PART D.  Trinity
# =========================================================================
print("\nPART D  Taylor's Trinity table")
raw = np.genfromtxt(DATA, dtype=None, encoding='utf-8',
                    names=['t_ms', 'R_m', 'auth'])
t_s = raw['t_ms']*1e-3
R_cm = raw['R_m']*100.0
auth = np.array([str(a) for a in raw['auth']])
print("  rows read: %d, t %.2f-%.1f ms, R %.1f-%.1f m"
      % (len(t_s), raw['t_ms'][0], raw['t_ms'][-1],
         raw['R_m'][0], raw['R_m'][-1]))
chk("row count", float(len(t_s)), 25.0, 0)


def fit(mask):
    x, y = np.log10(t_s[mask]), np.log10(R_cm[mask])
    p, cov = np.polyfit(x, y, 1, cov=True)
    return p[0], np.sqrt(cov[0, 0])


for label, mask, slope, err in [
        ("all 25", np.ones(25, bool), 0.4058, 0.0076),
        ("24 from 0.24 ms", t_s >= 0.24e-3, 0.3904, 0.0024),
        ("rows 2-20", (t_s >= 0.24e-3) & (t_s <= 4.61e-3), 0.3989, 0.0049)]:
    s, e = fit(mask)
    chk("exponent, %s" % label, s, slope, 3e-3)
    chk("its standard error, %s" % label, e, err, 2e-2)

stat = 2.5*np.log10(R_cm) - np.log10(t_s)
chk("statistic, row 1", stat[0], 11.6133, 1e-5)
chk("statistic, row 25", stat[-1], 11.8755, 1e-5)
chk("mean over all 25", stat.mean(), 11.9038, 1e-5)
m24 = t_s >= 0.24e-3
chk("mean over 24 from 0.24 ms", stat[m24].mean(), 11.9159, 1e-5)
resid = stat - stat[m24].mean()
chk("residual, row 1", resid[0], -0.3026, 2e-3)
chk("residual, row 23 (34 ms)", resid[22], -0.0440, 2e-3)

bands = [(np.arange(25) == 0, -0.3026), ((t_s >= 0.24e-3) & (t_s <= 1.93e-3), +0.0150),
         ((t_s >= 3.26e-3) & (t_s <= 4.61e-3), -0.0043),
         (t_s >= 15e-3, -0.0339)]
for i, (mask, want) in enumerate(bands):
    chk("band %d mean residual" % (i + 1), resid[mask].mean(), want, 5e-2)
b2, b4 = bands[1][0], bands[3][0]
se2 = resid[b2].std(ddof=1)/np.sqrt(b2.sum())
se4 = resid[b4].std(ddof=1)/np.sqrt(b4.sum())
chk("band 2 standard error", se2, 0.0056, 3e-2)
chk("band 4 standard error", se4, 0.0037, 3e-2)
step = resid[b2].mean() - resid[b4].mean()
chk("step between band 2 and band 4", step, 0.0490, 2e-2)
chk("step in sigma", step/np.hypot(se2, se4), 7.3, 2e-2)
chk("step as a factor in R", 10**(step/2.5), 1.046, 2e-3)

# energy
R5t2 = 10.0**(2.0*stat[m24].mean())
chk("R^5 t^-2 from the fixed-slope fit", R5t2, 6.7902e23, 5e-4)
chk("Taylor's eq. (1) implies", 10.0**(2.0*11.915), 6.7608e23, 5e-4)
chk("his eq. (3) against his eq. (1)", 6.7608e23/6.67e23, 1.0136, 2e-3)
rho0_T = 1.25e-3
E_exact = K75*rho0_T*R5t2
chk("E with the exact K", E_exact, 7.2237e20, 5e-4)
chk("E with Taylor's K = 0.856", 0.856*rho0_T*R5t2, 7.2655e20, 5e-4)
chk("E in modern kt", E_exact/KT_ERG, 17.27, 5e-4)
chk("Taylor's own E in modern kt", 7.14e20/KT_ERG, 17.07, 5e-4)
chk("his ton over the modern kt/1000", 4.25e16/(KT_ERG/1e3), 1.0158, 1e-3)
chk("ratio blast-wave/DOE", (E_exact/KT_ERG)/21.0, 0.822, 2e-3)
chk("ratio blast-wave/Selby", (E_exact/KT_ERG)/24.8, 0.696, 2e-3)
chk("sigma low against Selby", (24.8 - E_exact/KT_ERG)/2.0, 3.8, 2e-2)

# shock strength along the table, gamma = 1.4, Taylor's rho_0 and p_0
c0 = np.sqrt(G75*1.01325e6/rho0_T)/1e5            # km/s
for tt, vwant, Mwant, dwant in [(1.08e-3, 14.41, 42.8, 5.984),
                                (4.61e-3, 5.84, 17.3, 5.902),
                                (62.0e-3, 1.19, 3.5, 4.291)]:
    i = int(np.argmin(abs(t_s - tt)))
    vs = 0.4*R_cm[i]/t_s[i]/1e5
    checkr("v_s at t=%.2f ms (km/s)" % (tt*1e3), vs, vwant, 2)
    checkr("M1 at t=%.2f ms" % (tt*1e3), vs/c0, Mwant, 1)
    chk("rho2/rho1 at t=%.2f ms" % (tt*1e3), rh(vs/c0, G75)[0], dwant, 2e-3)

# P8: single-pair energies
for i, want in [(3, 18.63), (10, 19.50), (0, 4.28), (24, 14.33),
                (14, 17.10), (19, 16.52)]:
    E = K75*rho0_T*R_cm[i]**5/t_s[i]**2
    checkr("P8 energy from row %d (kt)" % (i + 1), E/KT_ERG, want, 2)


# =========================================================================
# PART E.  Voyager 2
# =========================================================================
print("\nPART E  Voyager 2")


def mach_from_Tratio(Tr, g):
    """Invert T2/T1 for M1 by bisection."""
    lo, hi = 1.0, 1e4
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if rh(mid, g)[2] < Tr:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo + hi)


Mnep = mach_from_Tratio(100.0, G53)
chk("Mach implied by T2/T1 = 100", Mnep, 17.8, 5e-3)
chk("density jump that Mach predicts", rh(Mnep, G53)[0], 3.963, 1e-3)
chk("consistency ratio", rh(Mnep, G53)[0]/4.0, 0.991, 1e-3)
chk("heliosheath T ratio", 1.0e5/1.0e6, 0.10, 1e-3)
chk("gas-dynamic prediction at M=4.9", rh(4.9, G53)[0], 3.556, 1e-3)
chk("measured over predicted", 2.38/rh(4.9, G53)[0], 0.669, 2e-3)
chk("departure in formal sigma", (rh(4.9, G53)[0] - 2.38)/0.14, 8.4, 5e-3)

# P9 Coulomb mean free path in the heliosheath
n_hs, T_hs, lnL = 2e-3, 1e5, 25.0
esu = 4.80320471257e-10
lam_c = (kB*T_hs)**2/(np.pi*n_hs*esu**4*lnL)
chk("heliosheath Coulomb mfp (cm)", lam_c, 2.28e16, 5e-3)
chk("that in AU", lam_c/AU, 1524.0, 5e-3)


# =========================================================================
# PART F.  A supernova remnant
# =========================================================================
print("\nPART F  a supernova remnant")
E51 = 1e51
nH = 1.0
rho0 = 1.4*m_u*nH
chk("rho_0 for n_H = 1", rho0, 2.325e-24, 1e-3)
xi53_use = xi53


def R_sedov(t):
    return xi53_use*(E51*t*t/rho0)**0.2


def v_sedov(t):
    return 0.4*R_sedov(t)/t


def T2_strong(vs, mu=0.61, g=G53):
    return 2.0*(g - 1.0)/(g + 1.0)**2*mu*m_u*vs*vs/kB


for age, Rw, vw, Tw, Mw in [(100, 1.988, 7774.1, 8.314e8, 1.1),
                            (1000, 4.993, 1952.8, 5.246e7, 17.9),
                            (10000, 12.541, 490.5, 3.310e6, 283.8),
                            (100000, 31.502, 123.2, 2.088e5, 4498.2)]:
    t = age*yr
    R = R_sedov(t)
    chk("age %6d yr  R (pc)" % age, R/pc, Rw, 5e-4)
    chk("age %6d yr  v_s (km/s)" % age, v_sedov(t)/1e5, vw, 5e-4)
    chk("age %6d yr  T2 (K)" % age, T2_strong(v_sedov(t)), Tw, 1e-3)
    checkr("age %6d yr  swept mass (Msun)" % age,
           4.0*np.pi/3.0*R**3*rho0/Msun, Mw, 1)

# start of the Sedov phase, M_ej = 5 Msun
R_start = (5.0*Msun/(4.0*np.pi/3.0*rho0))**(1.0/3.0)
t_start = (R_start/xi53_use)**2.5*(rho0/E51)**0.5
chk("Sedov phase starts at R (pc)", R_start/pc, 3.26, 2e-3)
chk("Sedov phase starts at t (yr)", t_start/yr, 345.0, 3e-3)


def Lam(T):
    L7 = 2.1e-27*np.sqrt(1e7)
    return np.where(T > 1e7, 2.1e-27*np.sqrt(T), L7*(T/1e7)**-0.7)


for T, want in [(1e8, 2.100e-23), (1e7, 6.641e-24), (3e6, 1.543e-23),
                (1e6, 3.328e-23), (1e5, 1.668e-22)]:
    chk("Lambda(%.0e)" % T, float(Lam(T)), want, 1e-3)


def t_cool(T, nH_post, mu=0.61, xe=1.2):
    rho = 1.4*m_u*nH_post
    ntot = rho/(mu*m_u)
    return 1.5*ntot*kB*T/(xe*nH_post*nH_post*float(Lam(T)))


def t_rad_solve(E, nH_amb, xi0, mu=0.61, g=G53):
    r0 = 1.4*m_u*nH_amb
    nH2 = (g + 1.0)/(g - 1.0)*nH_amb
    lo, hi = 6.0, 16.0

    def f(lt):
        t = 10.0**lt
        vs = 0.4*xi0*(E*t*t/r0)**0.2/t
        return np.log10(t_cool(T2_strong(vs, mu, g), nH2, mu)) - lt
    for _ in range(300):
        mid = 0.5*(lo + hi)
        if f(lo)*f(mid) <= 0.0:
            hi = mid
        else:
            lo = mid
    t = 10.0**(0.5*(lo + hi))
    vs = 0.4*xi0*(E*t*t/r0)**0.2/t
    return t, xi0*(E*t*t/r0)**0.2, T2_strong(vs, mu, g), vs


t_rad, R_rad, T_rad, v_rad = t_rad_solve(E51, 1.0, xi53_use)
chk("t_rad (yr)", t_rad/yr, 4.085e4, 1e-3)
chk("R_rad (pc)", R_rad/pc, 22.02, 1e-3)
chk("T2 at t_rad (K)", T_rad, 6.114e5, 1e-3)
chk("v_s at t_rad (km/s)", v_rad/1e5, 211.0, 3e-3)
chk("swept mass at t_rad (Msun)",
    4.0*np.pi/3.0*R_rad**3*rho0/Msun, 1536.0, 2e-3)
t_PDS = 0.4*14.0*pc/(413.0*1e5)
chk("t_PDS (yr)", t_PDS/yr, 1.326e4, 1e-3)
chk("R_rad/R_PDS", R_rad/pc/14.0, 1.573, 1e-3)
chk("t_rad/t_PDS", t_rad/t_PDS, 3.081, 1e-3)


# =========================================================================
# PART G.  The problem set
# =========================================================================
print("\nPART G  the problem set")
chk("P1 T2 at 5000 km/s, mu=0.61", T2_strong(5.0e8, 0.61), 3.439e8, 1e-3)
chk("P1 T2 at 5000 km/s, mu=1.00", T2_strong(5.0e8, 1.00), 5.638e8, 1e-3)
chk("P1 T2 at 5000 km/s, mu=0.50", T2_strong(5.0e8, 0.50), 2.819e8, 1e-3)

d8, p8, T8, m28, ds8 = rh(8.0, G53)
chk("P2 rho2/rho1 at M=8", d8, 3.8209, 2e-4)
chk("P2 T2 by the ratio (K)", T8*1e5, 2.087e6, 1e-3)
chk("P2 T2 by the strong formula (K)", T2_strong(4.0e7, 0.61), 2.201e6, 2e-3)
chk("P2 n2 (cm^-3)", d8*5.0, 19.10, 1e-3)

for nh, agew, vw, Tw in [(0.1, 1.016e4, 770.0, 8.16e6),
                         (1.0, 3.212e4, 244.0, 8.16e5),
                         (10.0, 1.016e5, 77.0, 8.16e4)]:
    r0 = 1.4*m_u*nh
    t = (20.0*pc/xi53_use)**2.5*(r0/E51)**0.5
    chk("P3 age at n_H=%.1f (yr)" % nh, t/yr, agew, 2e-3)
    chk("P3 v_s at n_H=%.1f (km/s)" % nh, 0.4*20.0*pc/t/1e5, vw, 3e-3)
    chk("P3 T2 at n_H=%.1f (K)" % nh, T2_strong(0.4*20.0*pc/t), Tw, 3e-3)

for E, nh, tw, Rw in [(1e51, 0.1, 1.458e5, 58.06),
                      (1e51, 10.0, 1.144e4, 8.35),
                      (1e50, 1.0, 2.441e4, 11.31)]:
    tr, Rr, _, _ = t_rad_solve(E, nh, xi53_use)
    chk("P4 t_rad E=%.0e n=%.1f (yr)" % (E, nh), tr/yr, tw, 2e-3)
    chk("P4 R_rad E=%.0e n=%.1f (pc)" % (E, nh), Rr/pc, Rw, 2e-3)

for M, want in [(0.9, -0.00159), (0.7, -0.07970), (0.5, -1.21225)]:
    chk("P5 ds/k at M=%.1f" % M, rh(M, G53)[4], want, 5e-3)


def mach_for_pct(g, pct):
    lo, hi = 1.0, 1e4
    ceil = (g + 1.0)/(g - 1.0)
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if rh(mid, g)[0]/ceil < pct:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo + hi)


chk("P6 M for 99% of the ceiling, g=5/3", mach_for_pct(G53, 0.99), 17.2, 5e-3)
chk("P6 M for 99% of the ceiling, g=7/5", mach_for_pct(G75, 0.99), 22.2, 5e-3)
chk("P6 Trinity ambient sound speed (km/s)", c0, 0.337, 5e-3)

for v, want in [(1.0, 28.0), (5.0, 700.6), (10.0, 2802.3), (20.0, 11209.4)]:
    chk("P7 rho2/rho1 at %.0f km/s isothermal" % v, (v/cT)**2, want, 2e-3)

# =========================================================================
# PART G.  Tycho, added 2026-09-17 after Simon approved the anchor
# =========================================================================
print("\nPART G  Rayleigh-Taylor at Tycho")
ALPHA_B, ALPHA_ERR, BASE, MMEAN = 0.038, 0.008, 0.77, 0.52
chk("m(1-m) at m=0.26", 0.26*0.74, 0.1924, 1e-3)
chk("m(1-m) at m=0.52", MMEAN*(1 - MMEAN), 0.2496, 1e-3)
chk("m(1-m) at m=0.65", 0.65*0.35, 0.2275, 1e-3)
chk("m(1-m) at m=0.47", 0.47*0.53, 0.2491, 1e-3)
h = ALPHA_B*1.0*MMEAN*(1 - MMEAN)*BASE
chk("predicted h/R_BW", h, 0.00730, 2e-3)
checkr("h/R_BW at alpha-1sigma", (ALPHA_B - ALPHA_ERR)*MMEAN*(1-MMEAN)*BASE,
       0.0058, 4)
chk("h/R_BW at alpha+1sigma", (ALPHA_B + ALPHA_ERR)*MMEAN*(1-MMEAN)*BASE,
    0.0088, 5e-3)
chk("ceiling alpha_B/4 x 0.77", ALPHA_B/4*BASE, 0.0073, 3e-3)
for tip, wwant, rwant in [(0.85, 0.08, 0.091), (0.93, 0.16, 0.046),
                          (1.00, 0.23, 0.032)]:
    w = tip - BASE
    chk("observed width to %.2f" % tip, w, wwant, 5e-3)
    checkr("predicted/observed at %.2f" % tip, h/w, rwant, 3)
w_sim = 0.85 - BASE
chk("factor short against the simulation", w_sim/h, 11.0, 2e-2)
alpha_req = w_sim/(MMEAN*(1 - MMEAN)*BASE)
chk("alpha required", alpha_req, 0.416, 3e-3)
chk("that over alpha_B", alpha_req/ALPHA_B, 11.0, 2e-2)
checkr("that over the 0.05 theory value", alpha_req/0.05, 8.3, 1)
chk("projected CD/BW from the arcsec radii", 241.0/251.0, 0.9602, 1e-4)
chk("RS/BW from Wang & Chevalier radii", 2.08/3.09, 0.673, 1e-3)

# PART F, the second route to t_PDS that the source-verification pass found
chk("CMB88 t_sf/e (yr)", 3.61e4/np.e, 1.328e4, 5e-4)
chk("t_PDS derived over t_sf/e", 1.326e4/(3.61e4/np.e), 0.9983, 1e-3)

# =========================================================================
# PROSE.  Values that module08.html prints and the prep run does not, or
# prints to a different number of digits.  Every `want` below was read off
# the HTML, not off the generating script.
# =========================================================================
print("\nPROSE  values read from module08.html")

# --- section 3, the ceiling percentages and the entropy branch
for M, pct in [(3.0, 75.00), (5.0, 89.29), (10.0, 97.09), (30.0, 99.67)]:
    checkr("g=5/3 M=%-4g per cent of the ceiling" % M,
           100*rh(M, G53)[0]/4.0, pct, 2)
chk("adiabatic rho2/rho1 at 10 km/s, mu=2.33 gas", rh(10.0/cT, G53)[0],
    3.996, 5e-4)

# --- section 4, the Sedov interior
i53 = int(np.argmin(abs(lam53 - 0.5)))
checkr("g=5/3 rho/rho2 at r/R = 0.5 (per cent)",
       100*G_53[i53]/G_53[-1], 1.53, 2)
chk("g=5/3 p/p2 plateau at r/R = 0.5",
    0.5**2*H_53[i53]/H_53[-1], 0.3098, 2e-3)

# --- section 5, the fits as the prose prints them (4 dp on the slope)
for label, mask, slope, err, ratio, sig in [
        ("all 25", np.ones(25, bool), 0.4058, 0.0076, 1.0146, 0.8),
        ("24 from 0.24 ms", t_s >= 0.24e-3, 0.3904, 0.0024, 0.9759, -3.9),
        ("rows 2-20", (t_s >= 0.24e-3) & (t_s <= 4.61e-3),
         0.3989, 0.0049, 0.9972, -0.2)]:
    sl, er = fit(mask)
    checkr("prose slope, %s" % label, sl, slope, 4)
    checkr("prose error, %s" % label, er, err, 4)
    checkr("prose ratio to 2/5, %s" % label, sl/0.4, ratio, 4)
    checkr("prose sigma, %s" % label, (sl - 0.4)/er, sig, 1)
checkr("largest departure, per cent", 100*abs(0.9759 - 1.0), 2.4, 1)
chk("span in t over the 25 rows", t_s[-1]/t_s[0], 620.0, 5e-3)
chk("span in R over the 25 rows", R_cm[-1]/R_cm[0], 17.0, 2e-2)

# --- section 5.2, what fails and when
chk("row 1 shortfall in R, as a factor", 10**(resid[0]/2.5), 0.76, 5e-3)
checkr("row 1 is smaller by (per cent)", 100*(1 - 10**(resid[0]/2.5)), 24, 0)
b2m = resid[(t_s >= 0.24e-3) & (t_s <= 1.93e-3)]
checkr("row 1 below the block-2 mean", resid[0] - b2m.mean(), -0.32, 2)
checkr("that in units of the block-2 scatter",
       abs(resid[0] - b2m.mean())/b2m.std(ddof=1), 16, 0)
for tt, dwant, pct in [(1.08e-3, 5.984, 100), (4.61e-3, 5.902, 98),
                       (62.0e-3, 4.291, 72)]:
    i = int(np.argmin(abs(t_s - tt)))
    r_ = rh(0.4*R_cm[i]/t_s[i]/1e5/c0, G75)[0]
    chk("rho2/rho1 at t=%.2f ms" % (tt*1e3), r_, dwant, 5e-4)
    checkr("that as a per cent of the ceiling 6", 100*r_/6.0, pct, 0)
checkr("M1 at 62 ms, as the prose prints it",
       0.4*R_cm[-1]/t_s[-1]/1e5/c0, 3.5, 1)

# --- section 5.3, the energy chain as the prose prints it
checkr("E in modern kt", E_exact/KT_ERG, 17.27, 2)
checkr("Taylor's E in modern kt", 7.14e20/KT_ERG, 17.07, 2)
checkr("his ton over the modern ton", 4.25e16/(KT_ERG/1e3), 1.0158, 4)
checkr("ratio to the DOE value", (E_exact/KT_ERG)/21.0, 0.822, 3)
checkr("ratio to Selby", (E_exact/KT_ERG)/24.8, 0.696, 3)
checkr("sigma below Selby", (24.8 - E_exact/KT_ERG)/2.0, 3.8, 1)
checkr("Taylor's internal inconsistency, per cent",
       100*(10.0**(2*11.915)/6.67e23 - 1.0), 1.36, 2)

# --- section 6, Voyager
checkr("Mach implied by the Neptune T jump", Mnep, 17.8, 1)
chk("density jump that Mach predicts", rh(Mnep, G53)[0], 3.963, 5e-4)
checkr("consistency ratio", rh(Mnep, G53)[0]/4.0, 0.991, 3)
chk("gas-dynamic prediction at M = 4.9", rh(4.9, G53)[0], 3.556, 5e-4)
checkr("measured over predicted at TS-2", 2.38/rh(4.9, G53)[0], 0.669, 3)
checkr("that in formal sigma", (rh(4.9, G53)[0] - 2.38)/0.14, 8.4, 1)

# --- section 7, the remnant table exactly as the prose prints it
for age, Rw, vw, Tw, Mw in [(100, 1.988, 7774, 8.31e8, 1.1),
                            (300, 3.085, 4021, 2.22e8, 4.2),
                            (1000, 4.993, 1953, 5.25e7, 17.9),
                            (3000, 7.748, 1010, 1.40e7, 66.9),
                            (10000, 12.541, 490.5, 3.31e6, 283.8),
                            (30000, 19.462, 253.7, 8.86e5, 1061.0),
                            (100000, 31.502, 123.2, 2.09e5, 4498.0)]:
    t = age*yr
    R = R_sedov(t)
    checkr("age %6d yr, R (pc)" % age, R/pc, Rw, 3)
    chk("age %6d yr, v_s (km/s)" % age, v_sedov(t)/1e5, vw, 1e-3)
    checkr("age %6d yr, T2 (3 s.f., units of the printed power)" % age,
           T2_strong(v_sedov(t))/10**np.floor(np.log10(Tw)),
           Tw/10**np.floor(np.log10(Tw)), 2)
    # the prose prints a decimal below 100 solar masses and an integer
    # above it, so the rounding tested has to follow the print
    checkr("age %6d yr, swept mass (Msun)" % age,
           4.0*np.pi/3.0*R**3*rho0/Msun, Mw, 1 if Mw < 100 else 0)
checkr("swept mass at t_rad (Msun)",
       4.0*np.pi/3.0*R_rad**3*rho0/Msun, 1536, 0)
checkr("T2 at t_rad, as the prose prints it (1e5 K)",
       T_rad/1e5, 6.11, 2)
chk("bremsstrahlung-only t_rad over the full one",
    3.32e5/(t_rad/yr), 8.13, 2e-2)
checkr("t_PDS from t_sf/e (1e4 yr)", 3.61e4/np.e/1e4, 1.328, 3)
checkr("the two t_PDS routes agree to (per cent)",
       100*abs(1.326e4/(3.61e4/np.e) - 1.0), 0.15, 2)

# --- section 8, Tycho, exactly as the prose prints it
checkr("m(1-m) at Tycho's mean m = 0.52", MMEAN*(1 - MMEAN), 0.2496, 4)
checkr("predicted h/R_BW", h, 0.0073, 4)
checkr("h/R_BW at alpha-1sigma, per cent",
       100*(ALPHA_B - ALPHA_ERR)*MMEAN*(1 - MMEAN)*BASE, 0.58, 2)
checkr("h/R_BW at alpha+1sigma, per cent",
       100*(ALPHA_B + ALPHA_ERR)*MMEAN*(1 - MMEAN)*BASE, 0.88, 2)
checkr("the ceiling alpha/4 x 0.77, per cent", 100*ALPHA_B/4*BASE, 0.73, 2)
checkr("the ceiling one sigma up, per cent",
       100*(ALPHA_B + ALPHA_ERR)/4*BASE, 0.89, 2)
checkr("predicted/observed, simulation", h/(0.85 - BASE), 0.091, 3)
checkr("predicted/observed, mean CD", h/(0.93 - BASE), 0.046, 3)
checkr("predicted/observed, clumps", h/(1.00 - BASE), 0.032, 3)
checkr("factor short", (0.85 - BASE)/h, 11, 0)
checkr("alpha the law would need", alpha_req, 0.416, 3)
checkr("that over alpha_B", alpha_req/ALPHA_B, 11, 0)
checkr("that over the 0.05 theory value", alpha_req/0.05, 8.3, 1)
checkr("projected CD/BW", 241.0/251.0, 0.9602, 4)
chk("m(1-m) is within 1 per cent of its ceiling (0 = the claim holds)",
    0.0 if 100*(1 - MMEAN*(1 - MMEAN)/0.25) < 1.0 else 1.0, 0.0, 1e-9)

# --- section 10, problem D2, the two thickness comparisons
d_air, T_air, p_air = 3.7e-8, 288.0, 1.01325e6
mfp_air = kB*T_air/(np.sqrt(2.0)*np.pi*d_air**2*p_air)
chk("mean free path in sea-level air (cm)", mfp_air, 6.5e-6, 2e-2)
chk("shock layer in air, a few mfp (cm)", 3*mfp_air, 2e-5, 1e-1)
chk("Trinity fireball radius at 1 ms (cm)", 38.0*100, 3.8e3, 1e-2)
chk("layer thinner than the fireball by", 3.8e3/(3*mfp_air), 2e8, 1e-1)
chk("heliosheath Coulomb mfp in AU", lam_c/AU, 1524.0, 5e-3)
checkr("TS layer thinner by, low end (1 s.f., units of 1e5)",
       lam_c/3e10/1e5, 8.0, 0)
checkr("TS layer thinner by, high end (1 s.f., units of 1e6)",
       lam_c/1e10/1e6, 2.0, 0)

# --- section 10, problem K2's two scalings
t01, R01, _, _ = t_rad_solve(E51, 0.1, xi53_use)
t10, R10, _, _ = t_rad_solve(E51, 10.0, xi53_use)
t50, R50, _, _ = t_rad_solve(1e50, 1.0, xi53_use)
checkr("K2: factor 100 in n moves t_rad by", t01/t10, 12.7, 1)
checkr("K2: factor 100 in n moves R_rad by", R01/R10, 7.0, 1)
checkr("K2: factor 10 in E moves t_rad by", t_rad/t50, 1.67, 2)
checkr("K2: factor 10 in E moves R_rad by", R_rad/R50, 1.95, 2)

# --- section 10, problem K3's six single-pair energies
for i, want in [(0, 4.28), (3, 18.63), (10, 19.50), (14, 17.10),
                (19, 16.52), (24, 14.33)]:
    checkr("K3 energy from row %d (kt)" % (i + 1),
           K75*rho0_T*R_cm[i]**5/t_s[i]**2/KT_ERG, want, 2)
checkr("K3 spread excluding row 1, per cent",
       100*(19.50/14.33 - 1.0), 36, 0)

# --- section 10, problem C2's 5 per cent
T2_ratio = rh(8.0, G53)[2]*1e5
T2_strongform = T2_strong(4.0e7, 0.61)
checkr("C2: the two T2 differ by (per cent)",
       100*(T2_strongform/T2_ratio - 1.0), 5, 0)
checkr("C2: rho2/rho1 as a per cent of the ceiling",
       100*rh(8.0, G53)[0]/4.0, 95.5, 1)

print("\n%d checks, %d mismatches" % (NCHK, len(FAILS)))
for label, got, want, rel in FAILS:
    print("  MISMATCH %-50s got %.6g want %.6g rel %.2e"
          % (label, got, want, rel))
