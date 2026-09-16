"""Module 1 numbers: mean free paths, Knudsen numbers, relaxation times.

Every physical number quoted in module01.html is produced here, so the
prose can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).
"""
import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
kB = 1.380649e-16       # erg/K          (exact, SI definition)
e = 4.80320471e-10      # esu            (elementary charge)
me = 9.1093837015e-28   # g
mp = 1.67262192369e-24  # g
hbar = 1.054571817e-27  # erg s
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
pc = 3.0856775814913673e18   # cm
kpc = 1e3*pc
AU = 1.495978707e13     # cm
Rsun = 6.957e10         # cm            (IAU 2015 nominal solar radius)
Msun = 1.98892e33       # g
yr = 3.15576e7          # s

# ---------------------------------------------------------------- neutral


def lam_neutral(n, sigma):
    """Mean free path of a hard-sphere gas: lambda = 1/(n sigma)."""
    return 1.0/(n*sigma)

# ---------------------------------------------------------------- Coulomb


def b90(T):
    """Impact parameter for a 90 deg deflection between two thermal
    like-charged particles: b90 = e^2 / (mu v_rel^2) = e^2/(3 kB T)."""
    return e*e/(3.0*kB*T)


def debye(n, T):
    """Electron Debye length, lambda_D = sqrt(kB T / (4 pi n e^2))."""
    return np.sqrt(kB*T/(4.0*np.pi*n*e*e))


def b_min_e(T):
    """Smallest usable impact parameter for ELECTRONS: the larger of the
    classical b90 and the thermal de Broglie length hbar/(m_e v_e),
    with v_e = sqrt(3 kB T/m_e)."""
    ve = np.sqrt(3.0*kB*T/me)
    return max(b90(T), hbar/(me*ve))


def lnLambda_e(n, T):
    """Coulomb logarithm for electrons, ln(lambda_D / b_min)."""
    return np.log(debye(n, T)/b_min_e(T))


SPITZER_C = 3.0**1.5/(4.0*np.sqrt(np.pi))   # = 0.7329
CRUDE_C = 9.0/(8.0*np.pi)                   # = 0.3581, single-speed estimate


def lam_coulomb(n, T, lnL=None, coef=SPITZER_C):
    """Thermal Coulomb mean free path,
        lambda = coef * (kB T)^2 / (n e^4 ln Lambda).
    The single-speed random-walk argument of the text gives
    coef = 9/(8 pi) = 0.358; the Maxwellian-averaged Spitzer (1962)
    result, as tabulated by Sarazin (1988) eq. 5.32, is
    coef = 3^(3/2)/(4 sqrt(pi)) = 0.733.  The two differ by 2.05x,
    which is the price of using one thermal speed for every particle.
    All numbers quoted in the text use the Spitzer coefficient."""
    if lnL is None:
        lnL = lnLambda_e(n, T)
    return coef*(kB*T)**2/(n*e**4*lnL)


# ------------------------------------------------------------ magnetisation
def gyroradius(T, B, m=mp, Z=1):
    """Thermal gyroradius r_g = m v_th /(Z e B / c), v_th = sqrt(2 kB T/m)."""
    vth = np.sqrt(2.0*kB*T/m)
    return m*vth*c/(Z*e*B)


# ------------------------------------------------------- stellar dynamics
def t_relax(N, R, v):
    """Binney & Tremaine (2008) eq. 1.38: t_relax ~ (0.1 N/ln N) t_cross,
    with t_cross = R/v.  R in cm, v in cm/s; returns seconds."""
    return 0.1*N/np.log(N)*(R/v)


def show(label, value, unit, extra=""):
    print(f"  {label:<44s} {value:>12.3g} {unit:<8s} {extra}")


if __name__ == "__main__":
    print("="*74)
    print("CHECK 0 -- how empty is the interstellar medium?")
    print("="*74)
    torr = 1333.22       # dyn/cm^2 per torr
    for label, P_torr in [("routine laboratory XHV, 1e-13 torr", 1e-13),
                          ("record laboratory vacuum, 1e-15 torr", 1e-15)]:
        n_lab = P_torr*torr/(kB*300.0)
        show(label, n_lab, "cm^-3", f"(warm ISM: 0.5 cm^-3)")
        show("  denser than the warm ISM by", n_lab/0.5, "x")
    print()

    print("="*74)
    print("CHECK 1 -- Coulomb mean free path against Sarazin (1988) eq. 5.32")
    print("  published: lambda_e = 23 kpc (T/1e8 K)^2 (n_e/1e-3 cm^-3)^-1,")
    print("             with ln Lambda = 37.8")
    print("="*74)
    T_icm, n_icm = 1.0e8, 1.0e-3
    show("ln Lambda, derived", lnLambda_e(n_icm, T_icm), "", "(Sarazin: 37.8)")
    show("Debye length", debye(n_icm, T_icm)/1e5, "km")
    show("b_90 (classical)", b90(T_icm), "cm")
    show("b_min (de Broglie, electrons)", b_min_e(T_icm), "cm")
    lam = lam_coulomb(n_icm, T_icm, lnL=37.8)
    show("lambda, Spitzer coefficient 0.733", lam/kpc, "kpc",
         "(Sarazin: 23 kpc)")
    show("ratio derived/published", (lam/kpc)/23.0, "", "<-- PUNCHLINE")
    lam_cr = lam_coulomb(n_icm, T_icm, lnL=37.8, coef=CRUDE_C)
    show("lambda, crude single-speed coefficient", lam_cr/kpc, "kpc")
    show("  Spitzer / crude", lam/lam_cr, "", "(the averaging penalty)")
    print()

    print("="*74)
    print("CHECK 2 -- the Knudsen census")
    print("="*74)
    sigma_H = 1.0e-15   # cm^2, order-of-magnitude H-H atomic cross-section

    # (a) solar photosphere: n from the measured pressure and temperature
    P_phot, T_phot = 1.2e5, 5772.0        # dyn/cm^2, K
    n_phot = P_phot/(kB*T_phot)
    lam_phot = lam_neutral(n_phot, sigma_H)
    H_phot = 1.5e7                        # cm, pressure scale height ~150 km
    show("photosphere n = P/kT", n_phot, "cm^-3")
    show("photosphere lambda", lam_phot*1e4, "micron")
    show("Kn vs R_sun", lam_phot/Rsun, "")
    show("Kn vs scale height H=150 km", lam_phot/H_phot, "")

    # (b) room air, for calibration
    lam_air, L_room = 6.8e-6, 300.0
    show("room air Kn (lambda 68 nm, L 3 m)", lam_air/L_room, "")

    # (c) warm neutral ISM
    n_ism, T_ism, L_ism = 0.5, 8000.0, 100*pc
    lam_ism = lam_neutral(n_ism, sigma_H)
    show("warm ISM lambda", lam_ism/AU, "AU")
    show("warm ISM Kn (L = 100 pc)", lam_ism/L_ism, "")

    # (d) solar wind at 1 AU
    n_sw, T_sw, B_sw = 5.0, 1.2e5, 5.0e-5   # cm^-3, K, gauss (5 nT)
    lnL_sw = lnLambda_e(n_sw, T_sw)
    lam_sw = lam_coulomb(n_sw, T_sw)
    show("solar wind ln Lambda", lnL_sw, "")
    show("solar wind lambda", lam_sw/AU, "AU")
    show("solar wind Kn (L = 1 AU)", lam_sw/AU, "",
         "<-- PUNCHLINE: order unity")
    show("solar wind proton gyroradius", gyroradius(T_sw, B_sw)/1e5, "km")
    show("  r_g / L", gyroradius(T_sw, B_sw)/AU, "")

    # (e) intracluster medium, core and outskirts
    for name, n_i, T_i, L_i in [("ICM cool core", 1.0e-2, 3.0e7, 100*kpc),
                                ("ICM bulk", 1.0e-3, 5.0e7, 500*kpc),
                                ("ICM outskirts", 1.0e-4, 1.0e8, 2000*kpc)]:
        li = lam_coulomb(n_i, T_i)
        show(f"{name} lambda", li/kpc, "kpc")
        show(f"{name} Kn", li/L_i, "")
    print()

    print("="*74)
    print("CHECK 3 -- when the particles are stars: two-body relaxation")
    print("="*74)
    tH = 1.38e10*yr
    for name, N, R, v in [("globular cluster", 1.0e5, 10*pc, 5.0e5),
                          ("Milky Way disc", 1.0e11, 10*kpc, 2.0e7),
                          ("galaxy cluster", 1.0e3, 1.0*kpc*1e3, 1.0e8)]:
        tr = t_relax(N, R, v)
        show(f"{name} t_cross", (R/v)/yr, "yr")
        show(f"{name} t_relax", tr/yr, "yr")
        show(f"{name} t_relax/t_Hubble", tr/tH, "")
    print()

    print("="*74)
    print("FIGURE DATA -- lambda(T) at fixed n, and the Kn ladder")
    print("="*74)
    Tg = np.logspace(3.5, 8.5, 6)
    for nn in (1e-3, 1.0, 1e3):
        row = " ".join(f"{lam_coulomb(nn, t)/pc:9.2e}" for t in Tg)
        print(f"  n={nn:<8g} lambda/pc at T={list(np.round(Tg, 0))}:")
        print(f"    {row}")
    print()
    print("  Kn ladder (log10 Kn):")
    ladder = [("room air", lam_air/L_room),
              ("solar photosphere", lam_phot/H_phot),
              ("warm ISM", lam_ism/L_ism),
              ("ICM cool core", lam_coulomb(1e-2, 3e7)/(100*kpc)),
              ("ICM outskirts", lam_coulomb(1e-4, 1e8)/(2000*kpc)),
              ("solar wind at 1 AU", lam_coulomb(n_sw, T_sw)/AU)]
    for nm, kn in ladder:
        print(f"    {nm:<22s} log10 Kn = {np.log10(kn):6.2f}")
    print()

    print("="*74)
    print("CHECK 4 -- two systems with no usable collisions at all")
    print("="*74)
    # (a) physical collisions between stars in the solar neighbourhood
    n_star = 0.1/pc**3                 # stars per cm^3
    sig_star = np.pi*(2*Rsun)**2       # geometric cross-section, cm^2
    lam_star = 1.0/(n_star*sig_star)
    v_star = 2.0e6                     # cm/s, ~20 km/s dispersion
    show("stellar collision mean free path", lam_star/pc/1e9, "Gpc")
    show("time between stellar collisions", lam_star/v_star/yr, "yr")
    show("  in Hubble times", lam_star/v_star/tH, "")

    # (b) dark matter, at the Randall et al. (2008) Bullet Cluster limit
    sigma_over_m = 0.7                 # cm^2/g, 68% upper limit
    rho_dm = 2.0e-26                   # g/cm^3, mean cluster density
    lam_dm = 1.0/(rho_dm*sigma_over_m)
    show("dark matter mfp at sigma/m = 0.7", lam_dm/(1e3*kpc), "Mpc")
    show("  Kn against a 1 Mpc cluster", lam_dm/(1e3*kpc)/1.0, "",
         "<-- PUNCHLINE: >1, so collisionless")
