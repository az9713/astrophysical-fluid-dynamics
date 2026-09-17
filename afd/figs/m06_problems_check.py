"""Independent verification of every number printed in Module 6's problems.

Nothing here is imported from m06_numbers.py.  The constants, the Saha
solution, the cooling function, the mixing-length relations and the reader
for bs05_agsop.dat are all written again from the definitions in
module06.html, so that an error in the drafting script cannot reproduce
itself here.  Each check asserts the value that module06.html prints.

Run:  python m06_problems_check.py
"""
import os

import numpy as np

# ---------------------------------------------------------------- constants
kB = 1.380649e-16          # erg/K
mu_u = 1.66053906660e-24   # g
me = 9.1093837015e-28      # g
h_pl = 6.62607015e-27      # erg s
G = 6.67430e-8             # cm^3 g^-1 s^-2
eV = 1.602176634e-12       # erg
pc = 3.0856775814913673e18  # cm
kpc = 1e3*pc
AU = 1.495978707e13        # cm
yr = 3.15576e7             # s
Myr = 1e6*yr
chi_H = 13.5984340*eV

GMsun = 1.3271244e26       # cm^3/s^2  (IAU 2015 nominal)
Rsun = 6.957e10            # cm
Lsun = 3.828e33            # erg/s
Msun = GMsun/G

RSUN_TAB = 6.9598e10       # cm        (printed at the foot of the data file)
LSUN_TAB = 3.8418e33       # erg/s

g_earth = 980.665          # cm/s^2
mu_air = 28.9647
gamma_air = 1.4
ISA_T0 = 288.15            # K
ISA_T_TROP = 216.65        # K
ISA_LAPSE = 6.5e-5         # K/cm

T_PHOT = 5772.0            # K
P_PHOT = 1.2e5             # dyn/cm^2
MU_PHOT = 1.2250

FAILURES = []


def check(label, got, want, tol=5e-3):
    """Assert a printed value, to a relative tolerance of 0.5 % by default."""
    ok = abs(got - want) <= tol*max(abs(want), 1e-300)
    mark = "ok  " if ok else "FAIL"
    print(f"  [{mark}] {label:<52} {got:>14.6g}  printed {want:>12.6g}")
    if not ok:
        FAILURES.append(label)


# ============================================================= shared physics
def saha_x(T, P):
    """Ionisation fraction of pure hydrogen, module06.html (5.1)-(5.2)."""
    A = (2.0*np.pi*me*kB*T/h_pl**2)**1.5*np.exp(-chi_H/(kB*T))
    B = A*kB*T/P
    return np.sqrt(B/(1.0 + B))


def grad_ad_ionising(T, P):
    """module06.html (5.3)."""
    x = saha_x(T, P)
    Phi = 2.5 + chi_H/(kB*T)
    q = x*(1.0 - x)
    return (2.0 + q*Phi)/(5.0 + q*Phi*Phi)


def ki_lambda_over_gamma(T):
    """module06.html (8.3), in cm^3."""
    return (1e7*np.exp(-1.184e5/(T + 1000.0))
            + 1.4e-2*np.sqrt(T)*np.exp(-92.0/T))


KI_GAMMA = 2e-26           # erg/s per hydrogen nucleus


def ki_lambda(T):
    return KI_GAMMA*ki_lambda_over_gamma(T)


def n_eq(T):
    """module06.html (8.4)."""
    return 1.0/ki_lambda_over_gamma(T)


def mlt_velocity(g, H, alpha, excess):
    """module06.html (6.2)."""
    return alpha*np.sqrt(g*H*excess/8.0)


def mlt_excess(rho, cP, T, g, H, alpha, F):
    """module06.html (6.3), inverted for grad - grad_ad."""
    return (F/(rho*cP*T*alpha**2*np.sqrt(g*H/32.0)))**(2.0/3.0)


def photosphere(alpha):
    """The tau = 2/3 layer of module06.html section 6.2."""
    g = GMsun/Rsun**2
    H = kB*T_PHOT/(MU_PHOT*mu_u*g)
    rho = P_PHOT*MU_PHOT*mu_u/(kB*T_PHOT)
    cP = 2.5*kB/(MU_PHOT*mu_u)
    F = Lsun/(4.0*np.pi*Rsun**2)
    exc = mlt_excess(rho, cP, T_PHOT, g, H, alpha, F)
    v = mlt_velocity(g, H, alpha, exc)
    cs = np.sqrt(5.0/3.0*P_PHOT/rho)
    return dict(g=g, H=H, rho=rho, cP=cP, F=F, excess=exc, v=v, cs=cs,
                l=alpha*H)


def load_table():
    """Read bs05_agsop.dat: only the rows whose twelve fields all parse."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', 'data', 'bs05_agsop.dat')
    rows = []
    for line in open(path, encoding='utf-8'):
        f = line.split()
        if len(f) != 12:
            continue
        try:
            rows.append([float(v) for v in f])
        except ValueError:
            continue
    a = np.array(rows)
    return dict(mfrac=a[:, 0], rfrac=a[:, 1], T=a[:, 2], rho=a[:, 3],
                P=a[:, 4], lfrac=a[:, 5])


def slope(x, y, half=25):
    """Local least-squares slope dy/dx over +/- half samples."""
    n = len(x)
    out = np.full(n, np.nan)
    for i in range(n):
        lo, hi = max(0, i - half), min(n, i + half + 1)
        if hi - lo < 4:
            continue
        xc = x[lo:hi] - x[lo:hi].mean()
        yc = y[lo:hi] - y[lo:hi].mean()
        d = xc @ xc
        if d > 0.0:
            out[i] = (xc @ yc)/d
    return out



def cz_base(rfrac, grad, target):
    """Innermost radius at which grad reaches `target`, which may be an array.

    With a constant target this is the Schwarzschild locator; with
    0.99*plateau + grad_mu it is the Ledoux one.
    """
    t = np.broadcast_to(np.asarray(target, float), rfrac.shape)
    idx = np.where((rfrac > 0.60) & (rfrac < 0.95) & np.isfinite(grad))[0]
    for j in range(1, len(idx)):
        i0, i1 = idx[j-1], idx[j]
        if grad[i0] < t[i0] and grad[i1] >= t[i1]:
            num = t[i0] - grad[i0]
            den = (grad[i1] - grad[i0]) - (t[i1] - t[i0])
            f = num/den
            return rfrac[i0] + f*(rfrac[i1] - rfrac[i0])
    return float('nan')


def mlt_row(tab, rtarget, alpha=2.0):
    """Mixing-length quantities at one tabulated radius."""
    i = int(np.argmin(abs(tab['rfrac'] - rtarget)))
    r = tab['rfrac'][i]*RSUN_TAB
    g = G*tab['mfrac'][i]*Msun/r**2
    H = tab['P'][i]/(tab['rho'][i]*g)
    mu = tab['rho'][i]*kB*tab['T'][i]/(tab['P'][i]*mu_u)
    cP = 2.5*kB/(mu*mu_u)
    F = tab['lfrac'][i]*LSUN_TAB/(4.0*np.pi*r*r)
    exc = mlt_excess(tab['rho'][i], cP, tab['T'][i], g, H, alpha, F)
    v = mlt_velocity(g, H, alpha, exc)
    return dict(rfrac=tab['rfrac'][i], l=alpha*H, v=v, tau=alpha*H/v)


# ==================================================================== C1
def problem_C1():
    print("\nPROBLEM C1.  Is the Earth's troposphere convective?")
    cp = gamma_air/(gamma_air - 1.0)*kB/(mu_air*mu_u)
    check("c_p of dry air [erg/g/K]", cp, 1.0047e7)
    dry = g_earth/cp                       # K/cm
    check("dry adiabatic lapse rate [K/km]", dry*1e5, 9.761)
    ratio = ISA_LAPSE/dry
    check("ratio ISA/dry adiabatic", ratio, 0.6659)
    grad_ad = (gamma_air - 1.0)/gamma_air
    check("grad_ad = 2/7", grad_ad, 0.28571)
    grad = ratio*grad_ad
    check("grad of the ISA troposphere", grad, 0.19026)
    check("polytropic index 1/grad - 1", 1.0/grad - 1.0, 4.2558)
    assert grad < grad_ad, "the ISA troposphere must be Schwarzschild-stable"
    check("stability margin, per cent", 100.0*(1.0 - ratio), 33.0, tol=0.02)


# ==================================================================== C2
def window():
    """The turning points of P = Gamma T/Lambda(T), module06.html (9.1)."""
    T = np.logspace(1.0, np.log10(1.2e4), 400001)
    n = n_eq(T)
    P = n*T
    turn = np.where(np.diff(np.sign(np.diff(P))) != 0)[0] + 1
    i_min, i_max = turn[0], turn[1]
    return dict(T_min=T[i_min], n_min=n[i_min], P_min=P[i_min],
                T_max=T[i_max], n_max=n[i_max], P_max=P[i_max])


def problem_C2():
    print("\nPROBLEM C2.  The unstable band in three variables.")
    w = window()
    check("T at P_min [K]", w['T_min'], 184.0)
    check("T at P_max [K]", w['T_max'], 5039.4)
    check("n at P_min [cm^-3]", w['n_min'], 8.682)
    check("n at P_max [cm^-3]", w['n_max'], 0.994)
    check("P_min/k [K cm^-3]", w['P_min'], 1597.5)
    check("P_max/k [K cm^-3]", w['P_max'], 5007.0)
    check("temperature factor", w['T_max']/w['T_min'], 27.4)
    check("density factor", w['n_min']/w['n_max'], 8.7, tol=0.01)
    check("pressure factor", w['P_max']/w['P_min'], 3.13)


# ==================================================================== C3
def problem_C3():
    print("\nPROBLEM C3.  How superadiabatic is the surface?  alpha sweep.")
    want = {1.0: (1.5319, 2.74, 0.339, 143.0),
            1.5: (0.8922, 3.14, 0.388, 214.0),
            2.0: (0.6079, 3.45, 0.427, 286.0),
            3.0: (0.3541, 3.95, 0.489, 429.0)}
    got = {}
    for alpha, (we, wv, wr, wl) in want.items():
        p = photosphere(alpha)
        got[alpha] = p
        check(f"alpha = {alpha}: grad - grad_ad", p['excess'], we)
        check(f"alpha = {alpha}: v_c [km/s]", p['v']/1e5, wv, tol=0.01)
        check(f"alpha = {alpha}: v_c/c_s", p['v']/p['cs'], wr, tol=0.01)
        check(f"alpha = {alpha}: l [km]", p['l']/1e5, wl, tol=0.01)
    check("v_c(alpha=3)/v_c(alpha=1)", got[3.0]['v']/got[1.0]['v'], 1.44,
          tol=0.01)
    check("excess(alpha=1)/excess(alpha=3)",
          got[1.0]['excess']/got[3.0]['excess'], 4.3, tol=0.02)
    check("v_c(alpha=1)/measured 0.65 km/s", got[1.0]['v']/0.65e5, 4.2,
          tol=0.02)
    # the alpha^(1/3) scaling the solution asserts
    check("v_c ratio against alpha^(1/3)", got[3.0]['v']/got[1.0]['v'],
          3.0**(1.0/3.0), tol=1e-6)


# ==================================================================== D1
def problem_D1():
    print("\nPROBLEM D1.  The buoyancy frequency of the Earth's atmosphere.")
    cp = gamma_air/(gamma_air - 1.0)*kB/(mu_air*mu_u)
    for label, T, dTdz, wN2, wN, wP in (
            ("isothermal stratosphere", ISA_T_TROP, 0.0,
             4.4182e-4, 0.02102, 4.98),
            ("ISA troposphere", ISA_T0, -ISA_LAPSE,
             1.1098e-4, 0.01053, 9.94)):
        N2 = (g_earth/T)*(dTdz + g_earth/cp)
        check(f"{label}: N^2 [s^-2]", N2, wN2)
        check(f"{label}: N [rad/s]", np.sqrt(N2), wN)
        check(f"{label}: period [min]", 2*np.pi/np.sqrt(N2)/60.0, wP)


# ==================================================================== D2
def problem_D2():
    print("\nPROBLEM D2.  Ledoux against Schwarzschild in a mu gradient.")
    grad, grad_ad = 0.45, 0.4
    check("critical grad_mu = grad - grad_ad", grad - grad_ad, 0.050)
    for gm, wmargin in ((0.00, -0.050), (0.02, -0.030),
                        (0.05, 0.000), (0.10, 0.050)):
        margin = grad_ad + gm - grad
        ok = abs(margin - wmargin) < 1e-9
        print(f"  [{'ok  ' if ok else 'FAIL'}] grad_mu = {gm:.2f}: "
              f"Ledoux margin {margin:+.3f}  printed {wmargin:+.3f}")
        if not ok:
            FAILURES.append(f"D2 margin at grad_mu = {gm}")
    tab = load_table()
    lP = np.log(tab['P'])
    lmu = np.log(tab['rho']*kB*tab['T']/(tab['P']*mu_u))
    gmu = slope(lP, lmu)
    i10 = int(np.argmin(abs(tab['rfrac'] - 0.10)))
    check("grad_mu at 0.10 R", gmu[i10], 0.220, tol=0.02)
    band = (tab['rfrac'] >= 0.72) & (tab['rfrac'] <= 0.75) & np.isfinite(gmu)
    check("max |grad_mu| over 0.72-0.75 R", np.max(abs(gmu[band])), 0.0270,
          tol=0.02)
    lT = np.log(tab['T'])
    gr = slope(lP, lT)
    plateau = float(np.median(gr[(tab['rfrac'] > 0.80)
                                 & (tab['rfrac'] < 0.92) & np.isfinite(gr)]))
    inner = (tab['rfrac'] > 0.05) & (tab['rfrac'] < 0.20) & np.isfinite(gr)
    i05 = int(np.argmin(abs(tab['rfrac'] - 0.050)))
    i20 = int(np.argmin(abs(tab['rfrac'] - 0.200)))
    check("grad_ad - grad at 0.050 R", plateau - gr[i05], 0.0706,
          tol=0.01)
    check("grad_ad - grad at 0.200 R", plateau - gr[i20], 0.1328,
          tol=0.01)
    band2 = ((tab['rfrac'] >= 0.30) & (tab['rfrac'] <= 0.60)
             & np.isfinite(gmu))
    check("max |grad_mu| over 0.30-0.60 R", np.max(abs(gmu[band2])),
          0.00256, tol=0.01)
    check("adiabatic plateau", plateau, 0.3957, tol=1e-3)
    base_s = cz_base(tab['rfrac'], gr, 0.99*plateau)
    base_l = cz_base(tab['rfrac'], gr, 0.99*plateau + gmu)
    check("convection-zone base, Schwarzschild", base_s, 0.7269,
          tol=1e-3)
    check("convection-zone base, Ledoux", base_l, 0.7306, tol=1e-3)
    check("shift in the base [R]", base_l - base_s, 0.0037, tol=0.03)
    check("shift, per cent of R", 100*(base_l - base_s), 0.37,
          tol=0.03)


# ==================================================================== D3
def problem_D3():
    print("\nPROBLEM D3.  Cooling lengths of the two interstellar phases.")
    out = {}
    for label, T, wn, wP, wt_s, wt_Myr, wcs, wlen, wF_pc, wF_au in (
            ("CNM", 70.0, 31.777, 2224.0, 7.248e11, 0.023, 0.874,
             0.020, 0.00049, 101.0),
            ("WNM", 6000.0, 0.658, 3950.0, 6.213e13, 1.969, 8.091,
             16.29, 0.09627, 19857.0)):
        n = n_eq(T)
        check(f"{label}: n_eq [cm^-3]", n, wn)
        check(f"{label}: P/k [K cm^-3]", n*T, wP, tol=0.01)
        t_cool = 1.5*n*kB*T/(n*n*ki_lambda(T))
        check(f"{label}: t_cool [s]", t_cool, wt_s)
        check(f"{label}: t_cool [Myr]", t_cool/Myr, wt_Myr, tol=0.03)
        cs = np.sqrt(5.0/3.0*kB*T/(1.27*mu_u))
        check(f"{label}: c_s [km/s]", cs/1e5, wcs, tol=0.01)
        check(f"{label}: cooling length [pc]", cs*t_cool/pc, wlen, tol=0.03)
        kappa = 2.5e3*np.sqrt(T)
        lamF = np.sqrt(kappa*T/(n*n*ki_lambda(T)))
        check(f"{label}: Field length [pc]", lamF/pc, wF_pc, tol=0.02)
        check(f"{label}: Field length [au]", lamF/AU, wF_au, tol=0.02)
        out[label] = cs*t_cool
    check("cooling-length ratio WNM/CNM", out['WNM']/out['CNM'], 794.0,
          tol=0.02)


# ==================================================================== K1
def problem_K1():
    print("\nPROBLEM K1.  Where the hydrogen ionisation zone sits.")
    T = np.linspace(3000.0, 40000.0, 370001)
    for P, wmin, wT in ((1.0e4, 0.08097, 10580.0),
                        (1.0e5, 0.09337, 12126.0),
                        (1.2e5, 0.09448, 12266.0),
                        (1.0e6, 0.10912, 14129.0),
                        (1.0e7, 0.12933, 16798.0)):
        ga = grad_ad_ionising(T, P)
        i = int(np.argmin(ga))
        check(f"P = {P:.1e}: min grad_ad", ga[i], wmin)
        check(f"P = {P:.1e}: at T [K]", T[i], wT, tol=1e-3)
    ga = grad_ad_ionising(T, 1.2e5)
    i = int(np.argmin(ga))
    check("x at the minimum, P = 1.2e5", saha_x(T[i], 1.2e5), 0.3271,
          tol=0.01)
    check("depth factor 0.4/min at P = 1.2e5", 0.4/ga[i], 4.23, tol=0.01)
    ga4 = grad_ad_ionising(T, 1.0e4)
    ga7 = grad_ad_ionising(T, 1.0e7)
    check("depth factor at P = 1e4", 0.4/np.min(ga4), 4.94, tol=0.01)
    check("depth factor at P = 1e7", 0.4/np.min(ga7), 3.09, tol=0.01)


# ==================================================================== K2
def problem_K2():
    print("\nPROBLEM K2.  Convective turnover through the envelope.")
    tab = load_table()
    rows = ((0.750, 103941.0, 0.056, 21.66*86400.0),
            (0.849, 69541.0, 0.070, 11.43*86400.0),
            (0.900, 47703.0, 0.087, 6.38*86400.0),
            (0.950, 23985.0, 0.124, 2.24*86400.0),
            (0.9831, 7233.0, 0.240, 8.38*3600.0))
    first = None
    for rt, wl, wv, wtau in rows:
        d = mlt_row(tab, rt)
        if first is None:
            first = d
        check(f"r = {rt}: l [km]", d['l']/1e5, wl, tol=0.01)
        check(f"r = {rt}: v_c [km/s]", d['v']/1e5, wv, tol=0.02)
        check(f"r = {rt}: turnover [s]", d['tau'], wtau, tol=0.02)
    ph = photosphere(2.0)
    check("photosphere: l [km]", ph['l']/1e5, 286.0, tol=0.01)
    check("photosphere: v_c [km/s]", ph['v']/1e5, 3.45, tol=0.01)
    check("photosphere: turnover [min]", ph['l']/ph['v']/60.0, 1.38,
          tol=0.01)
    # module06.html prints this range to one significant figure,
    # "a factor 2e4"; 2.26e4 is what the ratio actually is.
    check("turnover range, base to photosphere",
          first['tau']/(ph['l']/ph['v']), 2.26e4, tol=0.02)
    check("l falls by", first['l']/ph['l'], 364.0, tol=0.01)
    check("v_c rises by", ph['v']/first['v'], 62.0, tol=0.02)


# ==================================================================== K3
def problem_K3():
    print("\nPROBLEM K3.  Is a galaxy cluster thermally unstable?")
    for label, n_H, T, R, wt_Gyr, wlamF_kpc, wratio, wtts in (
            ("outskirts", 1e-3, 1e8, 1e3*kpc, 59.90, 4504.0, 4.50, 93.1),
            ("cool core", 1e-2, 3e7, 50.0*kpc, 3.28, 74.0, 1.48, 55.9)):
        lam = 2.1e-27*np.sqrt(T)
        n_e, n_tot = 1.2*n_H, 2.3*n_H
        u_th = 1.5*n_tot*kB*T
        rate = n_e*n_H*lam
        t_cool = u_th/rate
        cs = np.sqrt(5.0/3.0*kB*T/(0.6*mu_u))
        t_sound = R/cs
        kappa = 1.84e-5*T**2.5/37.8
        lamF = np.sqrt(kappa*T/rate)
        check(f"{label}: t_cool [Gyr]", t_cool/yr/1e9, wt_Gyr, tol=0.01)
        check(f"{label}: Field length [kpc]", lamF/kpc, wlamF_kpc, tol=0.01)
        check(f"{label}: lambda_F/R", lamF/R, wratio, tol=0.01)
        check(f"{label}: t_cool/t_sound", t_cool/t_sound, wtts, tol=0.01)
        if label == "outskirts":
            check("Lambda at 1e8 K [erg cm^3/s]", lam, 2.1000e-23)
            check("thermal energy [erg/cm^3]", u_th, 4.7632e-11)
            check("radiated power [erg/cm^3/s]", rate, 2.5200e-29)
            check("t_cool [s]", t_cool, 1.8902e18)
            check("sound speed [km/s]", cs/1e5, 1520.0, tol=0.01)
            check("t_sound over 1 Mpc [s]", t_sound, 2.0304e16)
            check("Spitzer kappa [erg/s/cm/K]", kappa, 4.8677e13)


# ============================================== the body numbers C3/K2 lean on
def body_numbers():
    print("\nBODY.  The photospheric inputs and the section 7.3 worked example.")
    p = photosphere(2.0)
    check("H at tau = 2/3 [km]", p['H']/1e5, 142.9, tol=0.01)
    check("rho at tau = 2/3 [g/cm^3]", p['rho'], 3.0631e-7)
    check("c_P [erg/g/K]", p['cP'], 1.6968e8)
    check("F = L/(4 pi R^2) [erg/cm^2/s]", p['F'], 6.2939e10)
    check("g (IAU nominal) [cm/s^2]", p['g'], 2.7420e4)
    check("grad - grad_ad, upper bound", p['excess'], 0.6079)
    check("v_c [km/s]", p['v']/1e5, 3.451, tol=0.01)
    check("c_s [km/s]", p['cs']/1e5, 8.080, tol=0.01)
    check("v_c/c_s", p['v']/p['cs'], 0.4271)
    # the Planck conversion of the measured contrast
    c_light, lam = 2.99792458e10, 705.7e-7
    x = h_pl*c_light/(lam*kB*T_PHOT)
    dlnB = x*np.exp(x)/(np.exp(x) - 1.0)
    check("x = hc/(lambda k T)", x, 3.5322)
    check("d ln B/d ln T", dlnB, 3.6386)
    dTT = 0.155/dlnB
    check("delta T/T", dTT, 0.04260)
    check("delta T [K]", dTT*T_PHOT, 245.9, tol=0.01)
    F_conv = p['rho']*0.65e5*p['cP']*dTT*T_PHOT
    check("F_conv [erg/cm^2/s]", F_conv, 8.3067e8)
    check("F_conv/F_total", F_conv/p['F'], 0.0132, tol=0.01)
    check("over-drive factor in flux", p['F']/F_conv, 76.0, tol=0.01)
    check("over-drive factor in velocity", (p['F']/F_conv)**(1/3.0), 4.2,
          tol=0.01)
    exc2 = mlt_excess(p['rho'], p['cP'], T_PHOT, p['g'], p['H'], 2.0, F_conv)
    v2 = mlt_velocity(p['g'], p['H'], 2.0, exc2)
    check("grad - grad_ad on the measured flux", exc2, 0.0340, tol=0.01)
    check("v_c on the measured flux [km/s]", v2/1e5, 0.816, tol=0.01)
    check("ratio to the measured 0.65 km/s", v2/0.65e5, 1.25, tol=0.01)
    # section 7.1
    check("2 l [km]", 2*p['l']/1e5, 572.0, tol=0.01)
    check("ratio measured/2l", 1050.0/(2*p['l']/1e5), 1.84, tol=0.01)
    check("ratio measured/l", 1050.0/(p['l']/1e5), 3.67, tol=0.01)
    check("departure vs the error on the mean [sigma]",
          (1050.0 - 2*p['l']/1e5)/22.0, 21.7, tol=0.01)
    check("departure vs the population spread [sigma]",
          (1050.0 - 2*p['l']/1e5)/480.0, 1.00, tol=0.01)
    check("ratio predicted/measured, 0.65 km/s", p['v']/0.65e5, 5.3, tol=0.01)
    check("ratio predicted/measured, 0.6 km/s rms", p['v']/0.6e5, 5.8,
          tol=0.01)


if __name__ == "__main__":
    print("=" * 74)
    print("MODULE 6 PROBLEM-SET CHECK (independent re-derivation)")
    print("=" * 74)
    problem_C1()
    problem_C2()
    problem_C3()
    problem_D1()
    problem_D2()
    problem_D3()
    problem_K1()
    problem_K2()
    problem_K3()
    body_numbers()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S):")
        for f in FAILURES:
            print("   -", f)
        raise SystemExit(1)
    print("All printed problem-set numbers reproduced.")
