"""Independent verification of every number printed in Module 7.

Nothing here is imported from m07_numbers.py.  The dispersion relation, the
cutoffs, the viscous crossover, the shell deceleration, the Richardson
number, the compressible limit, the mixing law and every quantity of the
anchor are written again from the definitions in module07.html, so that an
error in the drafting script cannot reproduce itself here.  Each check
asserts the value module07.html prints.

Run:  python m07_problems_check.py
"""
import numpy as np

# ---------------------------------------------------------------- constants
kB = 1.380649e-16           # erg/K
mu_u = 1.66053906660e-24    # g
G = 6.67430e-8              # cm^3 g^-1 s^-2
pc = 3.0856775814913673e18  # cm
AU = 1.495978707e13         # cm
yr = 3.15576e7              # s
g_earth = 980.665           # cm/s^2
GMsun = 1.3271244e26        # cm^3/s^2  (IAU 2015 nominal)
Rsun = 6.957e10             # cm
mu_air = 28.9647

# laboratory fluids at 20 C, 1 atm (module07.html, Sources item 5)
RHO_W, RHO_A = 0.998207, 1.2041e-3
TS_WA, NU_W = 72.75, 1.0034e-2
RHO_BRINE = 1.0210
RHO_HG, TS_HG = 13.55, 487.0
RHO_GLY, NU_GLY, TS_GLY = 1.261, 11.8, 63.0

# the anchor's inputs (module07.html, table in section 9.1)
LAM_OBS = 7.0e8             # cm
DU_OBS = 2.0e6              # cm/s
VPROP_LO, VPROP_HI = 6.0e5, 1.4e6
A_LAYER = 8.0e7             # cm
EMIS = 5.0
NE_CORONA = 3.0e8           # cm^-3
X_H = 0.70

FAILURES = []


def check(label, got, want, tol=5e-3):
    ok = abs(got - want) <= tol*max(abs(want), 1e-300)
    mark = "ok  " if ok else "FAIL"
    print(f"  [{mark}] {label:<54} {got:>13.6g}  printed {want:>12.6g}")
    if not ok:
        FAILURES.append(label)


def checkr(label, got, want, dp):
    """Assert a value the prose prints to `dp` decimal places.

    A relative tolerance is the wrong test for a number printed as "0.2" or
    "8.3": the printed figure IS the rounding, so the rounding is what must
    agree.  Used only where the prose gives one or two decimals.
    """
    ok = abs(round(got, dp) - want) <= 0.5*10.0**(-dp)
    mark = "ok  " if ok else "FAIL"
    print(f"  [{mark}] {label:<54} {got:>13.6g}  printed {want:>12.6g}")
    if not ok:
        FAILURES.append(label)


# ============================================================= shared physics
def sigma2(k, rho_t, rho_b, dU=0.0, g=0.0, Ts=0.0, B_t=0.0, B_b=0.0,
           costheta=1.0):
    """module07.html (3.1), written again from the printed equation."""
    s = rho_t + rho_b
    A = (rho_t - rho_b)/s
    return (k*k*rho_t*rho_b*dU*dU/(s*s)
            + A*g*k
            - Ts*k**3/s
            - k*k*(B_t*B_t + B_b*B_b)*costheta*costheta/(4.0*np.pi*s))


def lam_c(Ts, drho, g=g_earth):
    """module07.html (4.2)."""
    return 2.0*np.pi*np.sqrt(Ts/(g*drho))


def lam_nu(nu, A, g=g_earth):
    """module07.html (4.4)."""
    return 2.0*np.pi*(4.0*nu*nu/(A*g))**(1.0/3.0)


# ================================================================== sections
def section_4():
    print("\nSection 4 -- Rayleigh-Taylor in a glass of water")
    A = (RHO_W - RHO_A)/(RHO_W + RHO_A)
    check("Atwood, water over air", A, 0.997590)
    drho = RHO_W - RHO_A
    check("capillary length [mm]", 10*np.sqrt(TS_WA/(g_earth*drho)), 2.728)
    lc = lam_c(TS_WA, drho)
    check("lambda_c [cm]", lc, 1.7139)
    check("lambda_max [cm]", np.sqrt(3.0)*lc, 2.9686)
    check("lambda_max/lambda_c", np.sqrt(3.0)*lc/lc, np.sqrt(3.0), 1e-9)
    k = 2.0*np.pi/(np.sqrt(3.0)*lc)
    smax = np.sqrt(sigma2(k, RHO_W, RHO_A, g=g_earth, Ts=TS_WA))
    check("sigma_max [s^-1]", smax, 37.15, 1e-3)
    check("1/sigma_max [ms]", 1e3/smax, 26.9, 2e-3)
    ln = lam_nu(NU_W, A)
    check("lambda_nu, water [mm]", 10*ln, 0.467, 3e-3)
    check("lambda_max/lambda_nu, water", np.sqrt(3.0)*lc/ln, 63.5, 3e-3)
    # rho_t + rho_b quoted in K1
    check("rho_t+rho_b, water over air", RHO_W + RHO_A, 0.999411, 1e-5)

    # 4.2, the miscible pair
    Ab = (RHO_BRINE - RHO_W)/(RHO_BRINE + RHO_W)
    check("Atwood, brine over fresh", Ab, 0.011288, 2e-3)
    check("ratio of the two Atwood numbers", A/Ab, 88.0, 6e-3)
    for lam_cm, want in ((1.0, 8.3399), (10.0, 2.6373)):
        s = np.sqrt(Ab*g_earth*2.0*np.pi/lam_cm)
        check(f"brine sigma at {lam_cm:.0f} cm [s^-1]", s, want, 3e-3)
    check("lambda_nu, brine [mm]", 10*lam_nu(NU_W, Ab), 2.08, 3e-3)
    check("lambda_nu ratio, brine/water", lam_nu(NU_W, Ab)/lam_nu(NU_W, A),
          4.45, 3e-3)
    check("the same as (A_water/A_brine)^(1/3)", (A/Ab)**(1.0/3.0), 4.45, 3e-3)


def section_5():
    print("\nSection 5 -- the decelerating shell")
    rows = ((0.4, 3.0, 400.0, 1.3943e-2),
            (0.70, 3.0, 400.0, 1.2200e-2),
            (0.4, 10.0, 2000.0, 1.8591e-3))
    for m, R_pc, t_yr, want in rows:
        g = m*(1.0 - m)*R_pc*pc/(t_yr*yr)**2
        check(f"g, m={m}, R={R_pc} pc, t={t_yr:.0f} yr", g, want)
    A = 0.9
    tab = ((0.4, 3.0, 400.0, 0.030, 34.3, 11.6),
           (0.4, 3.0, 400.0, 0.300, 108.6, 3.7),
           (0.70, 3.0, 400.0, 0.030, 36.7, 10.9),
           (0.70, 3.0, 400.0, 0.300, 116.1, 3.4),
           (0.4, 10.0, 2000.0, 0.100, 171.7, 11.6),
           (0.4, 10.0, 2000.0, 1.000, 542.9, 3.7))
    for m, R_pc, t_yr, lam_pc, want_t, want_n in tab:
        g = m*(1.0 - m)*R_pc*pc/(t_yr*yr)**2
        s = np.sqrt(A*g*2.0*np.pi/(lam_pc*pc))
        check(f"1/sigma, m={m}, lam={lam_pc} pc [yr]", 1.0/s/yr, want_t, 5e-3)
        checkr(f"e-foldings, m={m}, lam={lam_pc} pc", s*t_yr*yr, want_n, 1)


def section_6():
    print("\nSection 6 -- Kelvin-Helmholtz and the Richardson number")
    T, lapse = 220.0, 6.0e-5           # K, K/cm
    cp = 3.5*kB/(mu_air*mu_u)          # diatomic, erg g^-1 K^-1
    N2 = (g_earth/T)*(g_earth/cp - lapse)
    check("N^2 [s^-2]", N2, 1.6764e-4, 3e-3)
    check("N [s^-1]", np.sqrt(N2), 0.01295, 3e-3)
    check("buoyancy period [min]", 2.0*np.pi/np.sqrt(N2)/60.0, 8.1, 5e-3)
    check("Ri at 10 m/s per km", N2/1.0e-4, 1.676, 3e-3)
    check("Ri at 30 m/s per km", N2/9.0e-4, 0.186, 5e-3)
    check("shear for Ri = 1/4 [s^-1]", np.sqrt(4.0*N2), 2.5895e-2, 3e-3)
    check("the same, per km [m/s]", np.sqrt(4.0*N2)*1e5/100.0, 25.9, 3e-3)


def section_7():
    print("\nSection 7 -- the compressible limit and the jet")
    check("2 sqrt(2)", 2.0*np.sqrt(2.0), 2.8284, 1e-4)
    for M, want in ((5.0, 55.6), (10.0, 73.6)):
        check(f"oblique angle at M={M:.0f} [deg]",
              np.degrees(np.arccos(2.0*np.sqrt(2.0)/M)), want, 3e-3)
    T_amb, mu_amb, gam = 1.0e7, 0.60, 5.0/3.0
    cs = np.sqrt(gam*kB*T_amb/(mu_amb*mu_u))
    check("c_s ambient [km/s]", cs/1e5, 480.6, 3e-3)
    dU = 5.0*cs
    check("dU = 5 c_s [km/s]", dU/1e5, 2403.0, 3e-3)
    eta = 0.010
    pref = np.sqrt(eta)/(1.0 + eta)
    check("sqrt(eta)/(1+eta)", pref, 0.09901, 1e-4)
    k = 1.0/(100.0*pc)
    check("k = 1/R [cm^-1]", k, 3.2408e-21)
    s = k*pref*dU
    check("sigma, jet [s^-1]", s, 7.7102e-14, 3e-3)
    check("1/sigma, jet [yr]", 1.0/s/yr, 4.110e5, 3e-3)
    t_kpc = 1000.0*pc/dU
    check("travel time over 1 kpc [yr]", t_kpc/yr, 4.069e5, 3e-3)
    check("e-foldings over 1 kpc", s*t_kpc, 0.99, 6e-3)
    cphi = 2.0*np.sqrt(2.0)/5.0        # cos of the exact angle, not of 55.6
    check("projected shear at 55.6 deg [km/s]", dU*cphi/1e5, 1359.0, 3e-3)
    checkr("K3: oblique rate as a fraction", cphi, 0.57, 2)
    checkr("K3: oblique e-foldings over 1 kpc", s*t_kpc*cphi, 0.56, 2)


def section_8():
    print("\nSection 8 -- the mixing law and the NIF measurement")
    a0, sa = 0.038, 0.008
    a_thy = 0.05
    a_sim = a_thy/2.0
    check("inferred alpha_B for 3D simulations", a_sim, 0.025, 1e-9)
    check("sigma distance to 0.050", abs(a0 - a_thy)/sa, 1.50, 3e-3)
    check("sigma distance to 0.025", abs(a0 - a_sim)/sa, 1.62, 5e-3)
    check("sigma distance to 0.030", abs(a0 - 0.030)/sa, 1.00, 3e-3)
    check("the span 0.050/0.025", a_thy/a_sim, 2.0, 1e-9)
    A, g, t = 0.90, 1.0e-3, 100.0*yr
    for al, want_cm, want_au in ((0.025, 2.2407e14, 15.0),
                                 (0.038, 3.4059e14, 22.8),
                                 (0.050, 4.4815e14, 30.0)):
        h = al*A*g*t*t
        check(f"h at alpha={al:.3f} [cm]", h, want_cm)
        check(f"h at alpha={al:.3f} [AU]", h/AU, want_au, 5e-3)
    # the Read integral reduces to A g t^2 for constant g
    x_read = A*(np.sqrt(g)*t)**2
    check("x_Read/(A g t^2)", x_read/(A*g*t*t), 1.0, 1e-12)
    # (8.4) in its two limits, with C_a = 1, C_d = 2 pi
    Ca, Cd = 1.0, 2.0*np.pi
    for b in (0.5, 1.0, 2.0):
        heavy = 1.0/(2.0*Ca + 4.0*b*Cd)          # rho_1 << rho_2
        equal = 1.0/((1.0 + Ca) + 2.0*b*Cd)      # rho_1 = rho_2
        check(f"(8.4) heavy limit at b={b}", heavy, 1.0/(2.0 + 8.0*np.pi*b),
              1e-12)
        check(f"(8.4) equal limit at b={b}", equal, 1.0/(2.0 + 4.0*np.pi*b),
              1e-12)


def section_9():
    print("\nSection 9 -- the anchor")
    k = 2.0*np.pi/LAM_OBS
    check("k [cm^-1]", k, 8.9760e-9)
    mu_e = 2.0/(1.0 + X_H)
    check("mu_e", mu_e, 1.1765, 1e-4)
    rho_h = mu_e*NE_CORONA*mu_u
    rho_l = rho_h/np.sqrt(EMIS)
    check("rho_h [g/cm^3]", rho_h, 5.8607e-16)
    check("rho_l [g/cm^3]", rho_l, 2.6210e-16)
    check("density ratio", np.sqrt(EMIS), 2.2361, 1e-4)
    arcsec = AU*np.radians(1.0/3600.0)
    check("1 arcsec at 1 AU [km]", arcsec/1e5, 725.3, 3e-3)
    check("AIA pixel [km]", 0.6*arcsec/1e5, 435.2, 3e-3)
    check("10 arcsec [km]", 10.0*arcsec/1e5, 7253.0, 3e-3)
    check("lambda/(10 arcsec)", LAM_OBS/(10.0*arcsec), 0.9652, 3e-3)
    check("820 s in minutes", 820.0/60.0, 13.7, 3e-3)

    # 9.2
    for dU, want, want_ratio, printed in ((VPROP_LO, 0.00269, 0.8976, 0.003),
                                          (VPROP_HI, 0.00628, 1.0472, 0.006)):
        s = np.sqrt(sigma2(k, 1.0, 1.0, dU=dU))
        check(f"sigma at dU={dU/1e5:.0f} km/s [s^-1]", s, want, 3e-3)
        check(f"computed/published at {dU/1e5:.0f} km/s", s/printed,
              want_ratio, 3e-3)
    s20 = 0.5*k*DU_OBS
    check("(1/2) k dU at 20 km/s [s^-1]", s20, 0.00898, 3e-3)
    check("ratio to their 0.006", s20/6e-3, 1.5, 6e-3)
    check("ratio to their 0.003", s20/3e-3, 3.0, 6e-3)
    s_lo = np.sqrt(sigma2(k, 1.0, 1.0, dU=VPROP_LO))
    s_hi = np.sqrt(sigma2(k, 1.0, 1.0, dU=VPROP_HI))
    check("e-foldings in 600 s, low", 600.0*s_lo, 1.62, 5e-3)
    check("e-foldings in 600 s, high", 600.0*s_hi, 3.77, 5e-3)

    # 9.3
    c_ph = DU_OBS/(1.0 + rho_h/rho_l)
    check("phase speed [km/s]", c_ph/1e5, 6.18, 3e-3)
    check("phase speed, emission 3 [km/s]",
          DU_OBS/(1.0 + np.sqrt(3.0))/1e5, 7.32, 3e-3)
    check("phase speed, emission 10 [km/s]",
          DU_OBS/(1.0 + np.sqrt(10.0))/1e5, 4.81, 3e-3)
    check("equal-density value [km/s]", DU_OBS/2e5, 10.0, 1e-9)
    check("ratio to the low edge of the band", c_ph/VPROP_LO, 1.030, 3e-3)
    check("width of the observed band", VPROP_HI/VPROP_LO, 2.3, 2e-2)
    check("separation of the two predictions", (DU_OBS/2.0)/c_ph, 1.62, 5e-3)

    # 9.4
    f_dens = np.sqrt(rho_h*rho_l)/(rho_h + rho_l)
    check("two-density prefactor", f_dens, 0.46209, 1e-4)
    check("ratio to 0.5", f_dens/0.5, 0.92418, 1e-4)
    check("per cent too high", (0.5/f_dens - 1.0)*100.0, 8.2, 5e-3)
    check("two-density rate at 20 km/s [s^-1]", k*f_dens*DU_OBS, 0.00830, 3e-3)
    check("1/sigma, two-density [s]", 1.0/(k*f_dens*DU_OBS), 120.5, 3e-3)
    check("1/sigma, equal-density [s]", 1.0/(0.5*k*DU_OBS), 111.4, 3e-3)
    brack = np.sqrt(1.0 - (2.0/5.0)**2)
    check("MHD bracket", brack, 0.91652, 1e-4)
    checkr("model below quoted [per cent]", (1.0 - brack)*100.0, 8.3, 1)
    check("compounded", f_dens/0.5*brack, 0.84702, 1e-4)
    check("total per cent below", (1.0 - f_dens/0.5*brack)*100.0, 15.3, 5e-3)
    check("published/corrected, the other way", 1.0/(f_dens/0.5*brack),
          1.181, 3e-3)
    for r, want_f, want_pc in ((2.0, 0.47140, 5.7), (3.0, 0.43301, 13.4)):
        f = np.sqrt(r)/(1.0 + r)
        check(f"prefactor at density ratio {r:.0f}", f, want_f, 1e-4)
        check(f"per cent below 0.5 at ratio {r:.0f}",
              (1.0 - f/0.5)*100.0, want_pc, 5e-3)
    check("e-foldings in 820 s, corrected", 820.0*k*f_dens*DU_OBS, 6.80, 3e-3)

    # 9.5, both hypotheses about where the field is
    both = DU_OBS*np.sqrt(2.0*np.pi*rho_h*rho_l/(rho_h + rho_l))
    one = DU_OBS*np.sqrt(4.0*np.pi*rho_h*rho_l/(rho_h + rho_l))
    check("field bound, equal both sides [G]", both, 0.0675, 3e-3)
    check("field bound, one side only [G]", one, 0.0954, 3e-3)
    check("their ratio", one/both, np.sqrt(2.0), 1e-6)
    check("bound at n_e = 1e9 [G]", both*np.sqrt(1e9/NE_CORONA), 0.1232, 3e-3)
    check("bound at n_e = 1e8 [G]", both*np.sqrt(1e8/NE_CORONA), 0.0390, 3e-3)
    for B, want_cos, want_ang in ((1.0, 0.06747, 3.87), (2.0, 0.03373, 1.93),
                                  (5.0, 0.01349, 0.77), (10.0, 0.00675, 0.39),
                                  (50.0, 0.00135, 0.08)):
        check(f"cos theta bound at B={B:.0f} G", both/B, want_cos, 3e-3)
        checkr(f"angle from perpendicular at B={B:.0f} G [deg]",
               90.0 - np.degrees(np.arccos(both/B)), want_ang, 2)
    checkr("one-sided angle at B=10 G [deg]",
           90.0 - np.degrees(np.arccos(one/10.0)), 0.55, 2)

    # 9.6
    check("k a", k*A_LAYER, 0.7181, 1e-3)
    check("a/lambda", A_LAYER/LAM_OBS, 0.1143, 3e-3)
    check("lambda/a", LAM_OBS/A_LAYER, 8.75, 3e-3)
    check("k a at 1 pixel", k*0.6*arcsec, 0.3906, 3e-3)
    check("k a at 3 pixels", k*1.8*arcsec, 1.1718, 3e-3)
    lam_fast = 5.0*np.pi*A_LAYER
    check("5 pi a [km]", lam_fast/1e5, 12566.0, 3e-3)
    check("k a of the tanh fastest mode", 2.0*np.pi/(5.0*np.pi), 0.400, 3e-3)
    check("ratio of the two wavelengths", lam_fast/LAM_OBS, 1.795, 3e-3)

    # 9.7
    g_surf = GMsun/Rsun**2
    check("solar surface gravity [cm/s^2]", g_surf, 2.7420e4)
    k_cut = g_surf*(rho_h**2 - rho_l**2)/(rho_h*rho_l*DU_OBS**2)
    check("KH cutoff wavenumber [cm^-1]", k_cut, 1.2263e-8, 3e-3)
    check("KH cutoff wavelength [km]", 2.0*np.pi/k_cut/1e5, 5124.0, 3e-3)
    check("lambda_obs/lambda_cut", LAM_OBS/(2.0*np.pi/k_cut), 1.366, 3e-3)


def problems():
    print("\nProblems C1-C3, D1-D3, K1-K3")
    A_w = (RHO_W - RHO_A)/(RHO_W + RHO_A)

    # C1: mercury
    lc_hg = lam_c(TS_HG, RHO_HG - RHO_A)
    check("C1 mercury lambda_c [cm]", lc_hg, 1.2029, 3e-3)
    check("C1 mercury lambda_max [cm]", np.sqrt(3.0)*lc_hg, 2.0835, 3e-3)

    # C2: the student's own arithmetic, which is right and irrelevant
    drho_b = RHO_BRINE - RHO_W
    check("C2 drho, brine over fresh", drho_b, 0.022793, 1e-3)
    check("C2 the student's lambda_c [cm]", lam_c(TS_WA, drho_b), 11.336, 3e-3)

    # D1: the general power-law ratio
    for p, q, want in ((1.0, 3.0, np.sqrt(3.0)), (1.0, 2.0, 2.0)):
        check(f"D1 (q/p)^(1/(q-p)) for p={p:.0f}, q={q:.0f}",
              (q/p)**(1.0/(q - p)), want, 1e-9)

    # D2: the prominence, both orderings
    mu_e = 2.0/(1.0 + X_H)
    rho_h = mu_e*NE_CORONA*mu_u
    rho_prom = 100.0*rho_h
    A100 = (rho_prom - rho_h)/(rho_prom + rho_h)
    check("D2 Atwood at density ratio 100", A100, 0.9802, 1e-4)
    g_surf = GMsun/Rsun**2
    s_p = np.sqrt(sigma2(2.0*np.pi/1e8, rho_prom, rho_h, g=g_surf))
    check("D2 sigma at 1000 km [s^-1]", s_p, 0.04109, 3e-3)
    check("D2 1/sigma at 1000 km [s]", 1.0/s_p, 24.3, 3e-3)
    checkr("D2 1/sigma at 1000 km [min]", 1.0/s_p/60.0, 0.41, 2)
    k_cut = g_surf*(rho_prom**2 - rho_h**2)/(rho_prom*rho_h*DU_OBS**2)
    check("D2 KH cutoff, inverted [km]", 2.0*np.pi/k_cut/1e5, 92.0, 1e-2)

    # D3
    check("D3 m(1-m) at m=2/5", 0.4*0.6, 6.0/25.0, 1e-12)
    g_old = 0.4*0.6*10.0*pc/(2000.0*yr)**2
    check("D3 ratio of 1e-3 to the older remnant", g_old/1e-3, 1.86, 6e-3)
    g_young = 0.4*0.6*3.0*pc/(400.0*yr)**2
    check("D3 ratio of the young remnant to 1e-3", g_young/1e-3, 14.0, 4e-2)

    # K1: water at five wavelengths, then glycerol
    for lam_cm, want in ((2.0, 28.573), (2.969, 37.154),
                         (10.0, 24.426), (100.0, 7.839)):
        s = np.sqrt(sigma2(2.0*np.pi/lam_cm, RHO_W, RHO_A,
                           g=g_earth, Ts=TS_WA))
        check(f"K1 sigma at {lam_cm} cm [s^-1]", s, want, 3e-3)
    s2 = sigma2(2.0*np.pi/0.5, RHO_W, RHO_A, g=g_earth, Ts=TS_WA)
    check("K1 oscillation at 0.5 cm [rad/s]", np.sqrt(-s2), 363.53, 3e-3)
    check("K1 its period [ms]", 2.0*np.pi/np.sqrt(-s2)*1e3, 17.3, 5e-3)
    for lam_cm, want in ((2.0, 35.00), (2.969, 26.91),
                         (10.0, 40.94), (100.0, 127.57)):
        s = np.sqrt(sigma2(2.0*np.pi/lam_cm, RHO_W, RHO_A,
                           g=g_earth, Ts=TS_WA))
        check(f"K1 1/sigma at {lam_cm} cm [ms]", 1e3/s, want, 3e-3)
    A_gly = (RHO_GLY - RHO_A)/(RHO_GLY + RHO_A)
    check("K1 glycerol Atwood", A_gly, 0.998092, 1e-4)
    lc_gly = lam_c(TS_GLY, RHO_GLY - RHO_A)
    check("K1 glycerol lambda_c [cm]", lc_gly, 1.4189, 5e-4)
    check("K1 glycerol lambda_max [cm]", np.sqrt(3.0)*lc_gly, 2.4575, 5e-4)
    ln_gly = lam_nu(NU_GLY, A_gly)
    check("K1 glycerol lambda_nu [cm]", ln_gly, 5.207, 3e-3)
    check("K1 glycerol lambda_nu/lambda_max",
          ln_gly/(np.sqrt(3.0)*lc_gly), 2.12, 5e-3)
    ln_w = lam_nu(NU_W, A_w)
    lm_w = np.sqrt(3.0)*lam_c(TS_WA, RHO_W - RHO_A)
    check("K1 water lambda_nu/lambda_max", ln_w/lm_w, 0.0157, 1e-2)

    # K2
    A, g = 0.90, 1.0e-3
    for t_yr, want_cm, want_au in ((10.0, 3.4059e12, 0.2),
                                   (100.0, 3.4059e14, 22.8),
                                   (1000.0, 3.4059e16, 2276.7)):
        h = 0.038*A*g*(t_yr*yr)**2
        check(f"K2 h at t={t_yr:.0f} yr [cm]", h, want_cm)
        checkr(f"K2 h at t={t_yr:.0f} yr [AU]", h/AU, want_au, 1)
    check("K2 h at 1000 yr [pc]", 0.038*A*g*(1000.0*yr)**2/pc, 0.01104, 3e-3)
    check("K2 alpha_B A g", 0.038*A*g, 3.42e-5, 3e-3)

    # K3 is verified in section_7


def main():
    print("=" * 74)
    print("MODULE 7 PROBLEM AND BODY CHECK -- nothing imported from "
          "m07_numbers.py")
    print("=" * 74)
    section_4()
    section_5()
    section_6()
    section_7()
    section_8()
    section_9()
    problems()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S):")
        for f in FAILURES:
            print("   -", f)
        raise SystemExit(1)
    print("All printed numbers reproduced.")


if __name__ == "__main__":
    main()
