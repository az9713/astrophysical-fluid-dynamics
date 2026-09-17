"""Module 4 numbers: sound waves and linear perturbation theory, checked
in air against a measured sound speed and in the Sun against the measured
large frequency separation of the p modes.

Every physical number quoted in module04.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K).

CONVENTION SHARED WITH MODULE 5.  Perturbations are taken proportional to
exp[i(k x - omega t)], and a dispersion relation is written as omega^2 = ...
so that omega^2 < 0 means growth.  m05_numbers.py writes the Jeans relation
as omega^2 = c_s^2 k^2 - 4 pi G rho_0 in the same form.

THE SHAPE OF THE CHECK, following Modules 2 and 3.

  CONFIRMED  Laplace's adiabatic sound speed sqrt(gamma P/rho) in dry air
  REFUTED    and Newton's isothermal sqrt(P/rho), against a measured speed
             of sound (ratios 0.9996 and 0.8448).

  REFUTED    The isothermal closure in the Sun, by a BOUND.  The acoustic
             radius tau = int dr/c of the tabulated interior alone gives
             Delta nu = 1/(2 tau) = 130.70 microHz with c^2 = P/rho.  Adding
             the untabulated outer layer can only lengthen tau, so this is an
             upper limit.  It lies 4.40 microHz (3.25%) below the measured
             135.1 and 7.91 microHz below the asymptotic 138.61.

  CONSISTENT The adiabatic closure in the interior.  With c^2 = (5/3) P/rho
             the table gives tau = 2963 s; the asymptotic Delta nu needs
             3607 s, so the outer 1.7% of the radius must supply 644 s
             (738 s with the uncorrected measured value).  The remainder is
             positive, as it must be.  That is consistency, not confirmation.

  FALLS SHORT  A perfect gas with fixed mu and Gamma_1 = 5/3 in that outer
             layer, with T linear between the table's top row and T_eff (an
             assumption: a Module 3 polytrope of fixed mu has T linear in
             depth).  Fully ionised it supplies 425.8 s, 66% of 644 s; even
             neutral mu throughout gives 613.5 s, 95%.  Closing the gap needs
             Gamma_1 below 5/3 or mu above neutral-equivalent, or a cooler
             profile.  The hydrogen and helium ionisation zones are the known
             mechanism.  The table's top rows show mu_eff rising from 0.601
             to 0.659 against a fully ionised 0.590.

CAVEAT ON THE MEASURED VALUE.  Huber et al. (2011) measure Delta nu from
VIRGO photometry around nu_max = 3090 microHz, not as the asymptotic
spacing (2 int dr/c)^-1.  Mosser et al. (2013) give Delta nu_as =
(1 + zeta) Delta nu_obs with zeta_sun ~ 2.6%, so the asymptotic value is
LARGER, 138.61 microHz.  Both are carried through.

Sources are listed in the SOURCES block at the foot of this file.
"""
import os
import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied from m03_numbers.py rather than imported, so the script reads alone.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
G = 6.67430e-8          # cm^3 g^-1 s^-2
a_rad = 7.565733e-15    # erg cm^-3 K^-4
R_gas = kB/mu_u         # erg g^-1 K^-1 per unit molecular weight
GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
TEFF_SUN = 5772.0       # K              (IAU 2015 nominal)

# --- terrestrial ---------------------------------------------------------
MU_AIR = 28.9647        # dimensionless  (dry air, as in Module 3)
GAMMA_AIR = 1.4         # diatomic ideal gas, 5 translational + rotational
T_AIR = 273.15          # K
# Measured zero-frequency speed of sound in dry air at 0 C.
# Smith & Harlow (1963), as quoted by Gavioso et al. (2025) sec. 2.3:
# (331.45 +/- 0.01) m/s, 273.15 K, 1 atm, zero frequency, 300 ppm CO2.
# Read second-hand: the 1963 full text is paywalled.
C_AIR_MEAS = 33145.0    # cm/s
C_AIR_MEAS_ERR = 1.0    # cm/s

# --- solar measurements ----------------------------------------------------
# Huber et al. (2011), ApJ 743, 143, section 2: VIRGO, 111 30-day subsets.
DNU_MEAS = 135.1e-6     # Hz
DNU_MEAS_ERR = 0.1e-6   # Hz
NUMAX_MEAS = 3090e-6    # Hz  (+/- 30 microHz)
# Jimenez, Garcia & Palle (2011), ApJ 743, 99, Conclusions: "the mean value
# being around 5000 microHz", with a 100-150 microHz activity-cycle swing.
# No formal uncertainty is given.
NUAC_MEAS = 5000e-6     # Hz
NUAC_SWING = 150e-6     # Hz, maximum minus minimum (a full range)
# Mosser et al. (2013), A&A 550, A126, eqs. (7), (19), (20) and sec. 4.2:
# the asymptotic large separation (2 int dr/c)^-1 exceeds the one measured
# near nu_max, Delta nu_as = (1 + zeta) Delta nu_obs, with the solar
# correction zeta_sun ~ 2.6 per cent.
ZETA_SUN = 0.026
MU_M03 = 1.3            # Module 3's round photospheric input, for comparison

# thermal diffusivity of dry air at 0 C, from k = 0.0243 W/(m K),
# rho = 1.293 kg/m^3, c_p = 1005 J/(kg K): a handbook input, not checked.
CHI_AIR = 0.0243/(1.293*1005)*1e4   # cm^2/s
LAM_AIR = 6.8e-6        # cm, mean free path of room air (Module 1 input)

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'data', 'bs05_agsop.dat')
RSUN_TAB = 6.9598e10    # cm, the table's own radius (Module 3 gotcha)


def P(*s):
    print(*s)


# =========================================================================
# PART A.  Sound speeds
# =========================================================================

def c_isothermal(T, mu):
    """Newton's sound speed sqrt(P/rho) = sqrt(kT/(mu m_u)), cm/s."""
    return np.sqrt(kB*T/(mu*mu_u))


def c_adiabatic(T, mu, gamma):
    """Laplace's sound speed sqrt(gamma P/rho), cm/s."""
    return np.sqrt(gamma*kB*T/(mu*mu_u))


def dispersion_uniform(k, cs):
    """omega^2 = c_s^2 k^2 for a uniform, static, adiabatic gas."""
    return (cs*k)**2


# =========================================================================
# PART B.  Acoustic cutoff of an isothermal atmosphere
# =========================================================================

def nu_cutoff(T, mu, gamma, g):
    """nu_ac = c/(4 pi H) with c adiabatic and H = kT/(mu m_u g).

    Equivalently gamma g/(4 pi c).  An isothermal atmosphere carries
    adiabatic perturbations with omega^2 = c^2 k_z^2 + omega_ac^2 and
    omega_ac = c/(2H); waves below nu_ac are evanescent.
    """
    c = c_adiabatic(T, mu, gamma)
    H = kB*T/(mu*mu_u*g)
    return c/(4*np.pi*H), c, H


def T_for_cutoff(nu, mu, gamma, g):
    """Invert nu_ac(T): T = (gamma g/(4 pi nu))^2 mu m_u/(gamma k)."""
    c = gamma*g/(4*np.pi*nu)
    return c*c*mu*mu_u/(gamma*kB)


# =========================================================================
# PART C.  The acoustic radius and the large separation
# =========================================================================

def load_ssm(path=DATA):
    rows = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) != 12:
                continue
            try:
                rows.append([float(x) for x in p])
            except ValueError:
                pass
    a = np.array(rows)
    return dict(m=a[:, 0], r=a[:, 1], T=a[:, 2], rho=a[:, 3], P=a[:, 4],
                X=a[:, 6], Y=a[:, 7])


def acoustic_radius_table(ssm, gamma1):
    """tau = int_0^r_top dr/c with c^2 = gamma1 P/rho.

    The first row sits at r = 0.00161 R; the centre-to-first-row piece is
    added as r_0/c_0, which is 2.2 s.
    """
    R = ssm['r']*RSUN_TAB
    c = np.sqrt(gamma1*ssm['P']/ssm['rho'])
    return np.trapezoid(1/c, R) + R[0]/c[0]


def mu_fully_ionised(X, Y):
    Z = 1 - X - Y
    return 1/(2*X + 0.75*Y + 0.5*Z)


def mu_neutral(X, Y):
    Z = 1 - X - Y
    return 1/(X + Y/4 + Z/16)


def mu_eff_table(ssm):
    """mu from the table's own P, rho, T, with radiation pressure removed."""
    Pg = ssm['P'] - a_rad*ssm['T']**4/3
    return ssm['rho']*kB*ssm['T']/(Pg*mu_u)


def layer_time(T_top, T_surf, depth, gamma1, mu):
    """Acoustic crossing time of a layer with T linear in depth.

    c^2 = gamma1 k T/(mu m_u), T = T_surf + s z, s = (T_top - T_surf)/depth.
    int_0^depth dz/c = 2 (sqrt(T_top) - sqrt(T_surf)) / (s sqrt(A)),
    A = gamma1 k/(mu m_u).  A Module 3 polytrope with fixed mu and gamma1
    has exactly this linear T(z), which is why the form is used.
    """
    s = (T_top - T_surf)/depth
    A = gamma1*kB/(mu*mu_u)
    return 2*(np.sqrt(T_top) - np.sqrt(T_surf))/(s*np.sqrt(A))


def main():
    P('=' * 74)
    P('PART A.  Newton against Laplace in dry air at 0 C')
    P('=' * 74)
    cN = c_isothermal(T_AIR, MU_AIR)
    cL = c_adiabatic(T_AIR, MU_AIR, GAMMA_AIR)
    P(f'  Newton  sqrt(kT/mu m_u)        = {cN/100:.2f} m/s')
    P(f'  Laplace sqrt(gamma kT/mu m_u)  = {cL/100:.2f} m/s')
    P(f'  ratio Laplace/Newton = sqrt(1.4) = {cL/cN:.4f}')
    if C_AIR_MEAS is not None:
        P(f'  measured                        = {C_AIR_MEAS/100:.2f} m/s')
        P(f'    PUNCHLINE Newton/measured     = {cN/C_AIR_MEAS:.4f}')
        P(f'    PUNCHLINE Laplace/measured    = {cL/C_AIR_MEAS:.4f}')
    else:
        P('  measured value: NOT YET VERIFIED, comparison not printed')
    P(f'  residuals: Newton {(C_AIR_MEAS-cN)/100:.3f} m/s, Laplace '
      f'{(C_AIR_MEAS-cL)/100:.4f} m/s, ratio {(C_AIR_MEAS-cN)/(C_AIR_MEAS-cL):.1f}')
    P(f'  thermal diffusivity chi_air = {CHI_AIR:.4f} cm^2/s')
    for nu in (1e3, 2e4):
        w = 2*np.pi*nu
        P(f'  nu = {nu:.0f} Hz: omega chi/c^2 = {w*CHI_AIR/cL**2:.3e}, '
          f'wavelength = {cL/nu:.2f} cm')
    nu_eq = cL**2/(2*np.pi*CHI_AIR)
    P(f'  omega chi/c^2 = 1 at nu = {nu_eq:.3e} Hz, wavelength '
      f'{cL/nu_eq*1e7:.0f} nm = {cL/nu_eq/LAM_AIR:.2f} mean free paths')
    P(f'  ell = wavelength/2pi = {cL/nu_eq/(2*np.pi)*1e7:.1f} nm; '
      f'10^3 x ratio at 20 kHz = {2*np.pi*2e4*CHI_AIR/cL**2*1e3:.4f}')

    P('')
    P('=' * 74)
    P('PART B.  Acoustic cutoff of the solar atmosphere')
    P('=' * 74)
    g_sun = GMsun/RSUN_TAB**2
    ssm = load_ssm()
    X_s, Y_s = ssm['X'][-1], ssm['Y'][-1]
    mu_n = mu_neutral(X_s, Y_s)
    nu_eff, c_eff, H_eff = nu_cutoff(TEFF_SUN, mu_n, 5/3, g_sun)
    P(f'  g_sun (table radius)          = {g_sun:.1f} cm/s^2')
    P(f'  mu, neutral surface mixture    = {mu_n:.4f}')
    P(f'  at T_eff = {TEFF_SUN:.0f} K: c = {c_eff/1e5:.3f} km/s, '
      f'H = {H_eff/1e5:.1f} km')
    P(f'  nu_ac = c/(4 pi H)             = {nu_eff*1e6:.0f} microHz')
    T_match = T_for_cutoff(NUAC_MEAS, mu_n, 5/3, g_sun)
    P(f'  measured nu_ac ~ {NUAC_MEAS*1e6:.0f} microHz '
      f'(activity swing {NUAC_SWING*1e6:.0f})')
    P(f'    PUNCHLINE nu_ac(T_eff)/measured = {nu_eff/NUAC_MEAS:.4f}')
    P(f'    temperature that reproduces it  = {T_match:.0f} K '
      f'({T_match/TEFF_SUN:.3f} T_eff)')
    for dnu in (-NUAC_SWING/2, NUAC_SWING/2):
        Tq = T_for_cutoff(NUAC_MEAS+dnu, mu_n, 5/3, g_sun)
        P(f'    at {(NUAC_MEAS+dnu)*1e6:.0f} microHz: T = '
          f'{Tq:.0f} K = {Tq/TEFF_SUN:.3f} T_eff')
    nu13, c13, H13 = nu_cutoff(TEFF_SUN, MU_M03, 5/3, g_sun)
    P(f'  with Module 3 mu = {MU_M03}: H = {H13/1e5:.1f} km, '
      f'nu_ac = {nu13*1e6:.0f} microHz')
    om, oac = 2*np.pi*NUMAX_MEAS, 2*np.pi*nu_eff
    kap = np.sqrt(oac**2 - om**2)/c_eff
    P(f'  at nu_max: kappa = {kap:.4e} /cm, 1/(2H) = {1/(2*H_eff):.4e} /cm,'
      f' energy e-fold 1/(2 kappa) = {1/(2*kap)/1e5:.1f} km')
    P(f'  nu_ac / nu_max = {NUAC_MEAS/NUMAX_MEAS:.3f}; '
      f'period at nu_max = {1/NUMAX_MEAS/60:.2f} min')

    P('')
    P('=' * 74)
    P('PART C.  Acoustic radius of BS05(AGS,OP) and the large separation')
    P('=' * 74)
    r_top = ssm['r'][-1]
    depth = RSUN_TAB*(1 - r_top)
    tau_ad = acoustic_radius_table(ssm, 5/3)
    tau_iso = acoustic_radius_table(ssm, 1.0)
    tau_meas = 1/(2*DNU_MEAS)
    tau_meas_err = tau_meas*DNU_MEAS_ERR/DNU_MEAS
    P(f'  table spans r = {ssm["r"][0]:.5f} to {r_top:.5f} R; '
      f'untabulated outer layer = {depth/1e5:.0f} km')
    P(f'  tau_table, Gamma_1 = 5/3       = {tau_ad:.1f} s '
      f'-> Delta nu <= {1e6/(2*tau_ad):.2f} microHz')
    P(f'  tau_table, isothermal c^2=P/rho = {tau_iso:.1f} s '
      f'-> Delta nu <= {1e6/(2*tau_iso):.2f} microHz')
    P(f'  measured Delta nu = {DNU_MEAS*1e6:.1f} +/- '
      f'{DNU_MEAS_ERR*1e6:.1f} microHz -> tau = {tau_meas:.1f} +/- '
      f'{tau_meas_err:.1f} s')
    # convergence of the quadrature: every second row, and Simpson
    R = ssm['r']*RSUN_TAB
    ic = 1/np.sqrt(5/3*ssm['P']/ssm['rho'])
    from scipy.integrate import simpson
    keep = np.r_[0:len(R):2, len(R)-1] if (len(R) - 1) % 2 else \
        np.r_[0:len(R):2]
    t2 = np.trapezoid(ic[keep], R[keep]) + R[0]*ic[0]
    ts = simpson(ic, x=R) + R[0]*ic[0]
    P(f'  quadrature: trapezoid all rows {tau_ad:.2f} s, every 2nd row, last kept '
      f'{t2:.2f} s, Simpson {ts:.2f} s')
    dnu_as = (1 + ZETA_SUN)*DNU_MEAS
    tau_as = 1/(2*dnu_as)
    P(f'  radial order near nu_max = {NUMAX_MEAS/DNU_MEAS:.1f}; '
      f'zeta from eq. 20 = 0.57 n_max/... : '
      f'{0.57/(NUMAX_MEAS/DNU_MEAS):.4f}; statistical error of Delta nu '
      f'= {DNU_MEAS_ERR/DNU_MEAS:.3%}')
    P(f'  asymptotic Delta nu = (1 + {ZETA_SUN}) x measured = '
      f'{dnu_as*1e6:.2f} microHz -> tau = {tau_as:.1f} s')
    gap = DNU_MEAS - 1/(2*tau_iso)
    P(f'    PUNCHLINE isothermal bound {1e6/(2*tau_iso):.2f} falls short '
      f'of measured by {gap*1e6:.2f} microHz ({gap/DNU_MEAS:.2%}) and of '
      f'asymptotic by {(dnu_as-1/(2*tau_iso))*1e6:.2f} microHz '
      f'({(dnu_as-1/(2*tau_iso))/dnu_as:.2%})')
    P(f'      it would survive a correction of the other sign up to '
      f'{gap/DNU_MEAS:.2%}')
    need = tau_meas - tau_ad
    P(f'  tau_iso - tau_table = {tau_iso - tau_ad:.1f} s')
    need_as = tau_as - tau_ad
    P(f'    PUNCHLINE adiabatic: layer must supply {need:.1f} s (measured) '
      f'or {need_as:.1f} s (asymptotic) = {need_as/tau_as:.3f} of tau, '
      f'over {1-r_top:.4f} of the radius')

    P('')
    P('  mu_eff from the table (radiation pressure removed):')
    mu_eff = mu_eff_table(ssm)
    mu_i = mu_fully_ionised(ssm['X'], ssm['Y'])
    for rr in (0.85, 0.95, 0.97, 0.98, r_top):
        i = int(np.argmin(abs(ssm['r'] - rr)))
        P(f'    r = {ssm["r"][i]:.4f}  T = {ssm["T"][i]:.3e} K  '
          f'mu_eff = {mu_eff[i]:.4f}  fully ionised = {mu_i[i]:.4f}  '
          f'excess = {mu_eff[i]/mu_i[i]-1:+.3f}')

    P('')
    P('  outer layer, T linear from the top row to T_eff:')
    T_top = ssm['T'][-1]
    mu_i_top = mu_i[-1]
    cases = [('fully ionised, Gamma_1 = 5/3', 5/3, mu_i_top),
             ('top-row mu_eff, Gamma_1 = 5/3', 5/3, mu_eff[-1]),
             ('neutral, Gamma_1 = 5/3', 5/3, mu_n)]
    for lab, g1, mu in cases:
        t = layer_time(T_top, TEFF_SUN, depth, g1, mu)
        P(f'    {lab:<32} tau_layer = {t:6.1f} s = {t/need:.3f} of needed'
          f' ({t/need_as:.3f} asymptotic), short by {need-t:.1f} / '
          f'{need_as-t:.1f} s -> Delta nu = {1e6/(2*(tau_ad+t)):.2f} '
          f'microHz')
    # the Gamma_1/mu the layer needs: tau scales as sqrt(mu/Gamma_1)
    t_ref = layer_time(T_top, TEFF_SUN, depth, 5/3, mu_i_top)
    for lab, nd in (('measured', need), ('asymptotic', need_as)):
        ratio_need = (5/3/mu_i_top)*(t_ref/nd)**2
        P(f'    {lab}: Gamma_1/mu required = {ratio_need:.4f}; '
          f'Gamma_1 at fully ionised mu = {ratio_need*mu_i_top:.3f}, '
          f'at neutral mu = {ratio_need*mu_n:.3f}')
    P(f'    fully ionised mu = 1/(2X + 3Y/4 + Z/2) = {mu_i_top:.4f}; '
      f'Z = {1-X_s-Y_s:.5f}; neutral mu with Z/2 instead of Z/16 = '
      f'{1/(X_s + Y_s/4 + (1-X_s-Y_s)/2):.4f}')
    P(f'      fully ionised 5/3/mu = {5/3/mu_i_top:.4f}, '
      f'neutral 5/3/mu = {5/3/mu_n:.4f}')
    # is a linear T(z) plausible?  An n = 3/2 layer of fixed mu has
    # dT/dz = (2/5) g mu m_u / k (Module 3, eq. 4.2).
    for lab, mu in (('fully ionised', mu_i_top), ('neutral', mu_n)):
        slope = 0.4*g_sun*mu*mu_u/kB
        P(f'    n = 3/2 lapse rate, {lab}: {slope*1e5:.2f} K/km -> '
          f'T at depth {depth/1e5:.0f} km = {TEFF_SUN + slope*depth:.0f} K')
    P(f'    linear T from table: {(T_top-TEFF_SUN)/depth*1e5:.2f} K/km, '
      f'T_top = {T_top:.0f} K')

    P('')
    P('=' * 74)
    P('SOURCES')
    P('=' * 74)
    P('  Smith, D. H. & Harlow, R. G. (1963), Br. J. Appl. Phys. 14, 102:')
    P('    dry air at 0 C, 1 atm, zero frequency, 300 ppm CO2, 331.45 +/-')
    P('    0.01 m/s.  Read as quoted in Gavioso, Astrua, Zucco & Pisani')
    P('    (2025), J. Phys. Chem. Ref. Data 54, 043101, sec. 2.3;')
    P('    doi:10.1063/5.0294663.  The 1963 full text was not read.')
    P('  Huber, D., Bedding, T. R., Stello, D., et al. (2011), ApJ 743, 143,')
    P('    section 2: "solar reference values of numax = 3090 +/- 30 microHz')
    P('    and Delta nu = 135.1 +/- 0.1 microHz", VIRGO, 111 30-day subsets.')
    P('    arXiv:1109.3460.')
    P('  Jimenez, A., Garcia, R. A. & Palle, P. L. (2011), ApJ 743, 99,')
    P('    Conclusions: nu_ac "mean value being around 5000 microHz", swing')
    P('    100-150 microHz with the activity cycle.  arXiv:1109.3326.')
    P('  Bahcall, Serenelli & Basu (2005), ApJ 621, L85: BS05(AGS,OP) table,')
    P('    afd/data/bs05_agsop.dat.')
    P('  Mosser, B., Michel, E., Belkacem, K., et al. (2013), A&A 550, A126:')
    P('    eq. (7) Delta nu_as = (2 int dr/c)^-1; eq. (19) Delta nu_as =')
    P('    (1 + zeta) Delta nu_obs; sec. 4.2 zeta_sun ~ 2.6 %. arXiv:1212.1687.')
    P('  Tassoul, M. (1980), ApJS 43, 469: the asymptotic p-mode relation.')
    P('  IAU 2015 Resolution B2/B3: GM_sun, T_eff,sun = 5772 K.')


if __name__ == '__main__':
    main()
