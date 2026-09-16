"""Module 2 numbers: the fluid equations, their closure, and the solar wind
test of continuity.

Every physical number quoted in module02.html is produced here, so the
prose can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

The anchor result is CHECK 1.  Steady, spherically symmetric continuity
demands r^2 rho v = constant.  If measured fits give n ~ r^-alpha and
v ~ r^+beta, with no continuity constraint imposed on the fitting, then
the zeroth moment of the Boltzmann equation predicts

    alpha - beta = 2   exactly.

Venzmer & Bothmer (2018), A&A 611, A36, Table 3, fitted alpha and beta
independently to combined Helios 1 and Helios 2 data over 0.29-0.98 au.
Their mean and median fits are compared with 2 below.
"""
import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m01_numbers.py rather than imported: importing that
# module would run its __main__ block is avoided, but a copy also keeps each
# module's numbers script readable on its own.
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

# --- Coulomb transport, carried over from Module 1 ------------------------
SPITZER_C = 3.0**1.5/(4.0*np.sqrt(np.pi))   # = 0.7329


def debye(n, T):
    """Electron Debye length, lambda_D = sqrt(kB T / (4 pi n e^2))."""
    return np.sqrt(kB*T/(4.0*np.pi*n*e*e))


def b90(T):
    """Impact parameter for a 90 deg deflection, b90 = e^2/(3 kB T)."""
    return e*e/(3.0*kB*T)


def b_min_e(T):
    """Larger of the classical b90 and the electron de Broglie length."""
    ve = np.sqrt(3.0*kB*T/me)
    return max(b90(T), hbar/(me*ve))


def lnLambda_e(n, T):
    """Coulomb logarithm for electrons, ln(lambda_D / b_min).  Module 1 (5.5)."""
    return np.log(debye(n, T)/b_min_e(T))


def lam_coulomb(n, T, lnL=None, coef=SPITZER_C):
    """Thermal Coulomb mean free path.  Module 1, equation (5.6)."""
    if lnL is None:
        lnL = lnLambda_e(n, T)
    return coef*(kB*T)**2/(n*e**4*lnL)


SIGMA_H = 1.0e-15       # cm^2, neutral hydrogen hard-sphere cross-section,
                        # the same order-of-magnitude value used in Module 1


def lam_neutral(n, sigma=SIGMA_H):
    """Hard-sphere mean free path 1/(n sigma).  Module 1, equation (4.1).
    Used for the warm ISM, which Module 1 treats as a neutral gas."""
    return 1.0/(n*sigma)


def v_th(T, m=mp):
    """Thermal speed sqrt(2 kB T/m), the same convention as Module 1."""
    return np.sqrt(2.0*kB*T/m)


def c_s(T, gamma=5.0/3.0, mu=0.6):
    """Adiabatic sound speed sqrt(gamma kB T/(mu m_p)).

    mu = 0.6 is the mean molecular weight of a fully ionised gas of
    cosmic composition; mu = 1.0 would be pure ionised hydrogen counting
    protons only."""
    return np.sqrt(gamma*kB*T/(mu*mp))


def reynolds(rho, u, L, T, lam):
    """Reynolds number Re = rho u L / mu with the Module 1 estimate
    mu = (1/3) rho v_th lambda (Proposition 4, equation 6.2).
    The density cancels, leaving Re = 3 u L /(v_th lambda)."""
    mu_visc = rho*v_th(T)*lam/3.0
    return rho*u*L/mu_visc


# --- Venzmer & Bothmer (2018) A&A 611 A36, Table 3 ------------------------
# Combined Helios 1 + 2, solar distance range 0.29-0.98 au.
# Power law x(r) = d * r^e with r in au; d is the magnitude at 1 au.
# Parenthesised figures in the paper are errors on the last digits; they
# are expanded here.  "dse" is the yearly variation of the exponent, the
# weighted standard deviation over the yearly fits of their Fig. 9 --
# a more honest uncertainty than the formal fit error.
VB18 = {
    #              d_med   sd_med   e_med    se_med  d_avg  sd_avg  e_avg    se_avg  dse
    "density":    (5.61,   0.27,   -2.093,   0.046,  7.57,  0.30,  -2.010,   0.038,  0.072),
    "velocity":   (410.7,  2.8,     0.058,   0.013,  435.6, 2.4,    0.049,   0.010,  0.012),
    "temperature": (7.14e4, 0.23e4, -0.913,  0.039,  9.67e4, 0.21e4, -0.792,  0.028,  0.050),
    "bfield":     (5.377,  0.092,  -1.655,   0.017,  6.05,  0.10,  -1.546,   0.018,  0.11),
}
HELIOS_RMIN, HELIOS_RMAX = 0.29, 0.98      # au, Helios data range


def continuity_residual(which="avg"):
    """Return (alpha - beta, formal error, yearly-variation error).

    n ~ r^-alpha and v ~ r^+beta are fitted independently by Venzmer &
    Bothmer with no continuity constraint imposed.  Steady spherically
    symmetric continuity requires alpha - beta = 2 exactly."""
    dn, sdn, en, sen, dna, sdna, ena, sena, dse_n = VB18["density"]
    dv, sdv, ev, sev, dva, sdva, eva, seva, dse_v = VB18["velocity"]
    if which == "avg":
        alpha, s_alpha, beta, s_beta = -ena, sena, eva, seva
    else:
        alpha, s_alpha, beta, s_beta = -en, sen, ev, sev
    diff = alpha - beta
    formal = np.hypot(s_alpha, s_beta)
    yearly = np.hypot(dse_n, dse_v)
    return diff, formal, yearly


def mdot(n_1au, v_1au_kms, helium=False):
    """Solar mass loss rate from 1 au values, Mdot = 4 pi r^2 rho v.

    With helium=False the mass is carried by protons alone.  With
    helium=True a helium abundance of 4% by number is added, which raises
    the mass per proton by a factor 1 + 4*0.04 = 1.16."""
    mu_mass = mp*(1.16 if helium else 1.0)
    rho = n_1au*mu_mass
    return 4.0*np.pi*AU**2*rho*(v_1au_kms*1e5)


def show(label, value, unit, extra=""):
    print(f"  {label:<44s} {value:>12.3g} {unit:<8s} {extra}")


if __name__ == "__main__":
    print("="*74)
    print("CHECK 1 -- ANCHOR: does the measured solar wind obey the zeroth")
    print("  moment of the Boltzmann equation?")
    print("  Steady + spherical continuity:  r^2 rho v = const,")
    print("  so with n ~ r^-alpha and v ~ r^+beta,  alpha - beta = 2 exactly.")
    print("  Fits: Venzmer & Bothmer (2018) A&A 611 A36, Table 3,")
    print("        Helios 1+2, 0.29-0.98 au, alpha and beta fitted separately.")
    print("="*74)
    for which, name in (("avg", "mean fits"), ("med", "median fits")):
        d, sf, sy = continuity_residual(which)
        dn = VB18["density"]
        dv = VB18["velocity"]
        a = -(dn[6] if which == "avg" else dn[2])
        b = (dv[6] if which == "avg" else dv[2])
        print(f"  --- {name} ---")
        show("  alpha (density)", a, "")
        show("  beta  (velocity)", b, "")
        show("  alpha - beta", d, "", "(continuity demands 2)")
        show("  ratio to 2", d/2.0, "", "<-- PUNCHLINE")
        show("  departure from 2, formal fit sigma", abs(d-2.0)/sf, "sigma")
        show("  departure from 2, yearly-variation sigma", abs(d-2.0)/sy, "sigma")
    d_a, _, _ = continuity_residual("avg")
    d_m, _, _ = continuity_residual("med")
    show("mean and median bracket 2: midpoint", 0.5*(d_a+d_m), "",
         "<-- PUNCHLINE")
    print()

    print("="*74)
    print("CHECK 2 -- how far does the mass flux actually drift?")
    print("  4 pi r^2 rho v propto r^(2 - alpha + beta); the exponent is the")
    print("  residual, and the drift is that residual over the Helios range.")
    print("="*74)
    span = HELIOS_RMAX/HELIOS_RMIN
    show("radial span of the Helios data", span, "x",
         f"({HELIOS_RMIN}-{HELIOS_RMAX} au)")
    for which, name in (("avg", "mean fits"), ("med", "median fits")):
        d, _, _ = continuity_residual(which)
        resid = 2.0 - d                       # exponent of r in the mass flux
        drift = span**resid
        show(f"  {name}: mass-flux exponent", resid, "")
        show(f"  {name}: flux change over the range", (drift-1.0)*100, "%",
             "<-- PUNCHLINE")
    print()

    print("="*74)
    print("CHECK 3 -- the solar mass loss rate, as a calibration")
    print("  Published: 4 pi r^2 U_r N M approx 1e12 g/s at 1 au, ecliptic,")
    print("  solar minimum -- Hoeksema-type value quoted by MNRAS 506, 4993")
    print("  (2021), eq. 12 discussion.  This is a WEAKER test than CHECK 1:")
    print("  it compares a number against a number, not a fitted exponent")
    print("  against an exact prediction.")
    print("="*74)
    n_med, v_med = VB18["density"][0], VB18["velocity"][0]
    n_avg, v_avg = VB18["density"][4], VB18["velocity"][4]
    for nm, nn, vv in (("median 1 au values", n_med, v_med),
                       ("mean   1 au values", n_avg, v_avg)):
        M = mdot(nn, vv)
        show(f"{nm}: n, v", nn, "cm^-3", f"v = {vv:.1f} km/s")
        show("  Mdot, protons only", M, "g/s", "(published ~1e12)")
        show("  ratio to 1e12 g/s", M/1e12, "",
             "<-- PUNCHLINE" if nm.startswith("median") else "")
        show("  Mdot with 4% helium by number", mdot(nn, vv, helium=True),
             "g/s")
        show("  in Msun/yr", M*yr/Msun, "Msun/yr")
    M_med = mdot(n_med, v_med)
    show("mass lost in 4.6 Gyr at this rate", M_med*4.6e9*yr/Msun, "Msun")
    show("  as a fraction of Msun", M_med*4.6e9*yr/Msun, "",
         "<-- negligible: the wind does not change the Sun's mass")
    print()

    print("="*74)
    print("CHECK 4 -- why Modules 3-11 may drop viscosity: Re = 3 Ma / Kn")
    print("  Re = rho u L / mu with mu = (1/3) rho v_th lambda (Module 1,")
    print("  eq. 6.2) gives Re = 3 (u/v_th)(L/lambda) = 3 Ma_th / Kn, with")
    print("  Ma_th = u/v_th and Kn = lambda/L.  Density cancels.")
    print("="*74)
    # (label, n [cm^-3], T [K], L [cm], u [cm/s], ionised?)
    # Densities, temperatures and lengths match the Module 1 census so the
    # two modules cannot disagree about the same system.
    systems = [
        ("solar convection zone", 1e23, 2e6, 2e10, 1e4, True),
        ("ICM, cluster core",     1e-2, 3e7, 100*kpc, 3e7, True),
        ("warm ISM",              0.5,  8e3, 100*pc, 1e6, False),
        ("solar wind at 1 AU",    5.0,  1.2e5, AU, 4.107e7, True),
    ]

    def mfp(n, T, ionised):
        """Module 1's mean free path: Coulomb if ionised, hard sphere if not."""
        return lam_coulomb(n, T) if ionised else lam_neutral(n)

    for nm, n, T, L, u, ion in systems:
        lam = mfp(n, T, ion)
        rho = n*mp
        Kn = lam/L
        Ma_th = u/v_th(T)
        Re_direct = reynolds(rho, u, L, T, lam)
        show(f"{nm}: Kn", Kn, "")
        if ion:
            show("  ln Lambda", lnLambda_e(n, T), "",
                 "<-- marginal below ~5" if lnLambda_e(n, T) < 5 else "")
        show("  Ma_th = u / v_th", Ma_th, "")
        show("  Re = 3 Ma_th / Kn", 3.0*Ma_th/Kn, "")
        show("  Re, computed from rho u L / mu", Re_direct, "",
             "<-- must equal the line above")
        assert abs(Re_direct/(3.0*Ma_th/Kn) - 1.0) < 1e-9, nm
    print("  All four identities agree to machine precision.")
    print()

    print("="*74)
    print("CHECK 5 -- the viscous term against the inertial term")
    print("  |mu grad^2 u| / |rho (u.grad) u| ~ 1/Re.  Quoted in the text as")
    print("  the licence to use Euler rather than Navier-Stokes.")
    print("="*74)
    for nm, n, T, L, u, ion in systems:
        lam = mfp(n, T, ion)
        Re = 3.0*(u/v_th(T))/(lam/L)
        show(f"{nm}: viscous/inertial ~ 1/Re", 1.0/Re, "", f"(Re = {Re:.3g})")
    print()

    print("="*74)
    print("CHECK 6 -- sound speed and Mach number of the measured solar wind")
    print("  Needed for the 'what it misses' section: the wind is supersonic")
    print("  at 1 au, which is why Module 9 can treat it as a steady flow")
    print("  through a critical point.")
    print("="*74)
    T_p_1au = VB18["temperature"][0]            # median proton temperature
    show("median proton temperature at 1 au", T_p_1au, "K")
    cs = c_s(T_p_1au)
    show("adiabatic sound speed, mu = 0.6", cs/1e5, "km/s")
    show("median wind speed at 1 au", v_med, "km/s")
    show("Mach number", (v_med*1e5)/cs, "", "<-- PUNCHLINE: supersonic")
    print()

    print("="*74)
    print("CHECK 7 -- the closure ordering, restated numerically")
    print("  Chapman-Enskog: P_ij = p delta_ij + O(Kn), q = O(Kn).")
    print("  The fractional error made by setting P_ij = p delta_ij is Kn.")
    print("="*74)
    for nm, n, T, L, u, ion in systems:
        show(f"{nm}: Kn = fractional error of Euler", mfp(n, T, ion)/L, "")
    print()
    print("  The solar wind is the exception Module 1 already named:")
    print("  its Knudsen number is of order unity, so the Euler closure is")
    print("  not licensed there by this argument.  Module 1 section 8.1 gives")
    print("  the magnetic rescue that licenses it anyway.")

    print()
    print("="*74)
    print("CHECK 8 -- the same data BREAKS the adiabatic energy equation.")
    print("  Continuity passes because it is exact.  The energy equation as")
    print("  closed in section 8 assumes no heating and no conduction, and")
    print("  that assumption is false in the solar wind.  Adiabatic flow has")
    print("  p rho^-gamma constant, so T propto rho^(gamma-1) and, with")
    print("  rho propto r^-alpha,  T propto r^(-alpha (gamma-1)).")
    print("="*74)
    gamma = 5.0/3.0
    for which, ia, it in (("mean fits", 6, 6), ("median fits", 2, 2)):
        alpha = -VB18["density"][ia]
        eT = VB18["temperature"][it]
        seT = VB18["temperature"][it+1]
        pred = -alpha*(gamma-1.0)
        print(f"  --- {which} ---")
        show("  alpha (density)", alpha, "")
        show("  adiabatic prediction for the T exponent", pred, "")
        show("  measured T exponent", eT, "", f"+/- {seT:.3f} formal")
        show("  ratio measured/adiabatic", eT/pred, "", "<-- PUNCHLINE")
        show("  shortfall", (1.0-eT/pred)*100, "%",
             "of the adiabatic cooling is not happening")
        show("  departure, in formal sigma", abs(eT-pred)/seT, "sigma")
    print()
    print("  Continuity is verified to 2%; the adiabatic closure of the")
    print("  energy equation is wrong by about 40% in the same data, at")
    print("  many sigma.  The wind is heated as it expands.  That is a")
    print("  result, not a failure of the method: the test is sharp enough")
    print("  to tell an exact conservation law from a modelling assumption.")
