"""Module 6 numbers: convection and thermal instability.

Every physical number quoted in module06.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

THE SHAPE OF THE CHECK, following Modules 2 and 3.  From ONE published
source, one prediction is CONFIRMED and one is REFUTED, with ratios stated.

  THE ANCHOR, and it is the ISM half, not the solar half.

  CONFIRMED  Thermal bistability predicts that the cold neutral medium can
             exist only inside a narrow pressure window.  Wolfire, McKee,
             Hollenbach & Tielens (2003) computed that window at the solar
             circle from heating and cooling microphysics alone, with no
             pressure measurement used as input: P_min/k = 1960 and
             P_max/k = 4810 K cm^-3, geometric mean 3070 K cm^-3.  Jenkins &
             Tripp (2011) then measured the pressure distribution of the CNM
             from C I fine-structure excitation along 89 sight lines and
             found a mass-weighted lognormal centred on log(p/k) = 3.58,
             that is 3802 K cm^-3.  It lies inside the window, at a ratio of
             1.238 to the predicted geometric mean.  Both edges of the
             window were fixed before the measurement existed.

  REFUTED    The strict two-phase picture says essentially ALL the cold gas
             lies in that window, because below P_min a static CNM cannot
             exist at all.  Jenkins & Tripp measure 29% of the CNM mass
             below Wolfire's P_min, using Wolfire's own number.  Their own
             fitted lognormal puts 5.0% there.  The measured excess is a
             factor 5.8.  What fails is not the criterion but the
             ASSUMPTION OF STATIC EQUILIBRIUM: turbulent rarefactions carry
             gas out of the window faster than it can return.  Heiles &
             Troland (2003) see the same failure from the other side, with
             at least 48% of the warm neutral medium by mass sitting at
             500-5000 K, temperatures the equilibrium curve forbids.

  AND A SECOND, SMALLER CHECK, solar, reported as a split verdict.
             Mixing-length theory with the solar-calibrated alpha = 2 gets
             the SIZE of a granule right to a factor of 1.84 against the
             measured 1050 km (Abramenko et al. 2012).  Asked to carry the
             whole solar flux at tau = 2/3 it gives 3.45 km/s against the
             measured 0.65 km/s (Oba et al. 2017), too fast by 5.3 -- but
             PART D A3 shows that those same two measurements say
             convection carries only 1.3% of the flux there, and that fed
             the measured flux the same formula returns 0.816 km/s, a ratio
             of 1.25.  So what the solar check refutes is the assumption
             that convection carries the photospheric flux, by a factor of
             76, not the mixing-length velocity law.  All four ratios are
             printed, in that order.

A NOTE ON WHAT THE STANDARD SOLAR MODEL CAN AND CANNOT TEST, carried over
from Module 3.  The BS2005-AGS,OP table was BUILT by solving hydrostatic
equilibrium with mixing-length convection, so nothing computed from it can
confirm either.  It is used here only as a stratification to differentiate:
to produce grad(r), grad_mu(r), the Brunt-Vaisala frequency and the
superadiabatic excess.  Those are properties of the table, and they are
reported as such.  The two CHECKS are against measurements made without it.

A NOTE ON ONE NUMBER THAT MUST NOT BE OVERSTATED.  Efficient convection
drives grad to grad_ad to about one part in 10^6 at 0.9 R, computed in
PART D.  That explains why Module 3's plateau is FLAT.  It does not explain
why Module 3's n_eff came out 1.527 rather than 1.500, a 1.8% offset: that
offset is grad_ad itself departing from (gamma-1)/gamma = 0.4, a property of
the equation of state used to build the model, not of convection.  The two
effects differ by six orders of magnitude and are reported separately.

Sources for every published number compared against are listed in the
SOURCES block at the foot of this file and in module06.html.
"""
import os
import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m01_numbers.py, m02_numbers.py and m03_numbers.py
# rather than imported, so that each module's numbers script reads on its
# own and cannot be broken by an edit to another module.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
mp = 1.67262192369e-24  # g
me = 9.1093837015e-28   # g
h_pl = 6.62607015e-27   # erg s          (exact, SI definition)
e_esu = 4.80320471e-10  # statcoulomb
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
a_rad = 7.565733e-15    # erg cm^-3 K^-4 (radiation constant, 4 sigma_SB/c)
eV = 1.602176634e-12    # erg            (exact)
pc = 3.0856775814913673e18   # cm
kpc = 1e3*pc
AU = 1.495978707e13     # cm
yr = 3.15576e7          # s
Myr = 1e6*yr

chi_H = 13.5984340*eV   # erg            (hydrogen ionisation energy)

# IAU 2015 nominal solar conversion constants.
GMsun = 1.3271244e26    # cm^3/s^2
Rsun = 6.957e10         # cm
Lsun = 3.828e33         # erg/s
Msun = GMsun/G          # g

# Earth, for the terrestrial half of the module.
g_earth = 980.665       # cm/s^2         (standard gravity, definitional)
mu_air = 28.9647        # dimensionless  (mean molecular weight of dry air)
gamma_air = 1.4         # diatomic ideal gas
ISA_T0 = 288.15         # K              (ISO 2533 / US Std Atm 1976)
ISA_P0 = 1.01325e6      # dyn/cm^2
ISA_LAPSE = 6.5e-5      # K/cm           (= 6.5 K/km, definitional)
ISA_T_TROP = 216.65     # K              (11 km, derived)
ISA_P_TROP = 2.2632e5   # dyn/cm^2       (derived)

# Solar photosphere at tau = 2/3, carried over from Modules 1 and 3 with the
# same provenance note: these are INPUTS, not checked quantities.
T_PHOT = 5772.0         # K              (IAU 2015 nominal effective T)
P_PHOT = 1.2e5          # dyn/cm^2       (gas pressure at tau = 2/3)
MU_PHOT = 1.2250        # dimensionless  (neutral, from the model's surface
                        # X, Y; Module 4 eq. (4.7).  Module 3 used a round
                        # 1.3.  See module04.html:329 for the reconciliation.

# The table's own solar constants, printed at the foot of the data file.
RSUN_TAB = 6.9598e10    # cm
LSUN_TAB = 3.8418e33    # erg/s

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'data', 'bs05_agsop.dat')

# =========================================================================
# PUBLISHED VALUES COMPARED AGAINST.  Every one was read from the paper.
# =========================================================================

# Oba, Iida & Shimizu (2017), ApJ 836, 40.  Hinode/SOT spectropolarimeter,
# bisector analysis of Fe I 630.15 nm with a subsonic filter applied to
# remove the 5-minute oscillation.  Their Table 1 fixes the geometrical
# height of each intensity level; their Fig. 8 and Fig. 9 give the speeds.
OBA_H_LO = 40.0         # km   geometrical height at I/I0 = 0.75, tau500=0.55
OBA_H_HI = 163.0        # km   geometrical height at I/I0 = 0.40, tau500=0.10
OBA_UP_LO = 0.65e5      # cm/s upward speed at the LOWEST height measured
OBA_UP_HI = 0.40e5      # cm/s upward speed at the highest height measured
OBA_DOWN_LO = 0.30e5    # cm/s downward speed, shallowest
OBA_DOWN_HI = 0.50e5    # cm/s downward speed, deepest
OBA_RMS_LO = 0.6e5      # cm/s rms filtered convective velocity at I/I0=0.75
OBA_RMS_HI = 0.3e5      # cm/s rms filtered convective velocity at I/I0=0.40
OBA_ERR = 0.18e5        # cm/s their stated worst-case velocity error

# Abramenko, Yurchyshyn, Goode, Kitiashvili & Kosovichev (2012), ApJ 756,
# L27.  1.6 m New Solar Telescope, TiO 705.7 nm, 36 disk-centre images,
# diffraction limit 77 km.  Their two-component fit to the size histogram:
# the regular granules are Gaussian with mean d0 and width sigma; the
# mini-granules below 600 km are a power law of index kappa.
GRAN_D0 = 1050e5        # cm   mean granule diameter
GRAN_D0_ERR = 22e5      # cm   formal uncertainty ON THE MEAN
GRAN_SIG = 480e5        # cm   population standard deviation (not an error)
GRAN_SIG_ERR = 11e5     # cm
GRAN_KAPPA = -1.82      # power-law index of the mini-granule population
GRAN_AREA_LO = 1080e5   # cm   the "dominant scale" from the area function
GRAN_AREA_HI = 1300e5   # cm
GRAN_CONTRAST = 0.155   # rms intensity contrast of their images
GRAN_CONTRAST_ERR = 0.006
GRAN_LAMBDA = 705.7e-7  # cm   the TiO band they imaged in

# Wolfire, McKee, Hollenbach & Tielens (2003), ApJ 587, 278.  Table 3, the
# row R = 8.5 kpc with the fiducial cloud column N_cl = 1e19 cm^-2.  These
# are computed from heating and cooling microphysics; no measured pressure
# enters them.  P/k = 1.1 n T in their convention, the 1.1 counting helium.
W03_PMIN = 1960.0       # K cm^-3   below this only WNM can exist
W03_PMAX = 4810.0       # K cm^-3   above this only CNM can exist
W03_PAVE = 3070.0       # K cm^-3   their geometric mean, their eq. (26)

# Wolfire et al. (2003) Table 4, "Dependence on Model Parameters", read from
# the arXiv LaTeX source astro-ph/0207098 at ms.tex:4527-4539, column order
# from the header at ms.tex:4528-4532 and the model footnotes at :4560-4566.
# phi_PAH is the factor multiplying the collisional rates of C+ with PAH^-; it
# enters the photoelectric heating efficiency and the PAH-recombination
# cooling, and so sets where the equilibrium curve turns over.  FIVE variants,
# of which three vary phi_PAH and two hold it at the standard 0.5.
# Rows: (label, phi_PAH, P_min/k, P_max/k, P_ave/k, how Wolfire treats it).
W03_TABLE4 = (
    ('Standard',      0.50, 1960.0, 4810.0, 3070.0, 'adopted'),
    ('Low phi_PAH',   0.25, 1560.0, 3150.0, 2220.0, 'poorly matched'),
    ('High phi_PAH',  1.00, 2270.0, 5970.0, 3680.0, 'ruled out'),
    # Wolfire's prose calls this row "Low PAH"; Table 4's column head is
    # "Low n_PAH/n" (footnote e: phi_PAH stays 0.5, n_PAH/n = 4e-7).
    ('Low n_PAH/n',   0.50, 1580.0, 3920.0, 2490.0, 'poorly matched'),
    ('Low G0',        0.50, 1460.0, 3980.0, 2410.0, 'ruled out'),
)
W03_PHI_PAH_STD = 0.50
W03_T_CNM_AT_PMIN = 258.0   # K     hottest a CNM parcel can be
W03_T_CNM_AT_PMAX = 61.6    # K
W03_T_WNM_AT_PMIN = 8310.0  # K
W03_T_WNM_AT_PMAX = 5040.0  # K     coldest a WNM parcel can be
W03_N_CNM_AT_PMIN = 6.91    # cm^-3
W03_N_CNM_AT_PMAX = 71.0    # cm^-3
W03_N_WNM_AT_PMIN = 0.209   # cm^-3
W03_N_WNM_AT_PMAX = 0.860   # cm^-3
W03_T_CNM_AVE = 85.0    # K         CNM temperature at P_ave
W03_N_CNM_AVE = 32.9    # cm^-3

# Jenkins & Tripp (2011), ApJ 734, 65.  C I fine-structure excitation in
# STIS echelle spectra of 89 stars.  Their eq. (3), the mass-weighted
# (that is, dN(H)/d log p) lognormal fitted to the central portion:
#   dN(H)/dlog(p/k) = 2.30e23 exp[ -(log(p/k) - 3.58)^2 / (2 (0.175)^2) ]
JT11_LOGP_MEAN = 3.58   # dex
JT11_LOGP_SIG = 0.175   # dex     "an rms dispersion of AT LEAST 0.175"
JT11_NORM = 2.30e23     # cm^-2 per dex
JT11_FIT_LO = 3.2       # dex     outside 3.2 < log(p/k) < 4.0 the fit
JT11_FIT_HI = 4.0       # dex     understates the observed wings
JT11_FRAC_BELOW_PMIN = 0.29   # measured mass fraction below W03_PMIN
JT11_FRAC_BELOW_LOWI = 0.23   # same, low-starlight-intensity subsample
JT11_FRAC_EXTREME = 5e-4      # fraction with log(p/k) > 5.5
JT11_LOGP_EXTREME = 5.5       # dex
JT11_MACH_LO, JT11_MACH_HI = 1.0, 4.0   # their inferred turbulent Mach range

# Heiles & Troland (2003), ApJ 586, 1067, sections 2.3.2 and 9.2.1.
# Millennium Arecibo 21-cm absorption survey, Gaussian decomposition.
HT03_F_UNSTABLE = 0.48  # >= this fraction of WNM mass at 500-5000 K
HT03_T_UNST_LO = 500.0  # K
HT03_T_UNST_HI = 5000.0  # K
HT03_F_WNM = 0.61       # WNM share of total H I column at |b| > 10 deg
HT03_TS_MEDIAN = 70.0   # K   CNM spin temperature, weighted by N(HI)
HT03_TS_PEAK = 40.0     # K   peak of the CNM spin temperature histogram

# Koyama & Inutsuka (2002), ApJ 564, L97, their eqs. (4) and (5), WITH the
# two typographical errors corrected.  The corrected form is printed as
# eqs. (3) and (4) of Vazquez-Semadeni, Gomez, Jappsen, Ballesteros-Paredes,
# Gonzalez & Klessen (2007), ApJ 657, 870, whose footnote 5 reads: "Note
# that eq. (4) in Koyama & Inutsuka (2002) contains two typographical
# errors.  The form used here incorporates the necesary corrections, kindly
# provided by H. Koyama."  The two corrections are 114800 -> 1.184e5 in the
# exponent and 14 -> 1.4e-2 in the coefficient of the second term.  With the
# printed values the equilibrium pressure comes out near 2 K cm^-3, three
# orders of magnitude below every measured interstellar pressure; that is
# the test this script runs in PART E before using the function.
KI_GAMMA = 2.0e-26      # erg/s        heating per hydrogen nucleus
KI_A1 = 1.0e7           # cm^3         first term coefficient
KI_E1 = 1.184e5         # K            CORRECTED (printed: 114800)
KI_T1 = 1000.0          # K
KI_A2 = 1.4e-2          # cm^3 K^-1/2  CORRECTED (printed: 14)
KI_E2 = 92.0            # K
KI_A2_PRINTED = 14.0    # the uncorrected value, used only to show it fails

# Module 1's Coulomb logarithm for the intracluster medium, reused in the
# conduction problems.  Sarazin (1988) section 5.4.
LN_LAMBDA_ICM = 37.8

# Electron thermal conductivity for a hydrogen plasma,
# kappa = 1.84e-5 T^(5/2) / ln Lambda  erg s^-1 cm^-1 K^-1.
# READ THROUGH Sarazin (1988) eq. (5.37), which attributes it to Spitzer
# (1956).  Spitzer's book was not opened, and 1956 and 1962 are the first
# and second editions of it, so this module cites Sarazin for the value.
SPITZER_A = 1.84e-5

# Parker (1953) conductivity for neutral atomic gas, as adopted by Koyama &
# Inutsuka (2002) immediately below their eq. (3):
#   K = 2.5e3 T^(1/2) erg cm^-1 K^-1 s^-1.
KI_COND_A = 2.5e3


# =========================================================================
# PART A.  The displaced parcel: adiabatic gradient and Schwarzschild
# =========================================================================

def grad_ad_ideal(gamma):
    """The adiabatic logarithmic temperature gradient (d ln T/d ln P)_S.

    For an ideal gas with constant ratio of specific heats gamma, an
    adiabatic change obeys P ~ rho^gamma and P ~ rho T, so T ~ P^((gamma-1)
    /gamma).  Hence grad_ad = (gamma-1)/gamma exactly: 2/5 = 0.4 for a
    monatomic gas, 2/7 = 0.285714 for a diatomic one.
    """
    return (gamma - 1.0)/gamma


def saha_x(T, P):
    """Ionisation fraction of pure hydrogen in Saha equilibrium at (T, P).

    Saha's equation for H with statistical weights g_II/g_I = 1/2 is
        n_e n_II / n_I = (2 pi m_e k T / h^2)^(3/2) exp(-chi/kT) == A.
    Write x = n_II/n_H with n_H the total hydrogen nucleus density, so
    n_e = n_II = x n_H, n_I = (1-x) n_H, and the total particle density is
    n_H (1+x).  Then P = n_H (1+x) k T eliminates n_H and gives
        x^2/(1-x^2) = A k T / P == B,   hence   x = sqrt(B/(1+B)),
    a closed form with no iteration.
    """
    A = (2.0*np.pi*me*kB*T/h_pl**2)**1.5 * np.exp(-chi_H/(kB*T))
    B = A*kB*T/P
    return np.sqrt(B/(1.0 + B))


def grad_ad_ionising(T, P):
    """grad_ad for a partially ionised pure-hydrogen ideal gas.

    Kippenhahn & Weigert, "Stellar Structure and Evolution", section 14.3:
        grad_ad = (2 + x(1-x) Phi) / (5 + x(1-x) Phi^2),
        Phi     = 5/2 + chi_H/(k T),
    with x the ionisation fraction.  At x = 0 and x = 1 this returns 2/5,
    the fully neutral and fully ionised monatomic value.  In between,
    energy put into the parcel goes into ionising hydrogen rather than into
    raising its temperature, so the parcel's temperature rises less for the
    same compression and grad_ad falls.  The minimum is at x = 1/2.

    Returns (grad_ad, x).
    """
    x = saha_x(T, P)
    Phi = 2.5 + chi_H/(kB*T)
    q = x*(1.0 - x)
    return (2.0 + q*Phi)/(5.0 + q*Phi*Phi), x


def brunt_vaisala_sq(g, HP, grad_ad, grad, grad_mu=0.0, phi_over_delta=1.0):
    """N^2 = (g/H_P) [ grad_ad - grad + (phi/delta) grad_mu ].

    The first two terms are the Schwarzschild form: a parcel displaced
    upward by dr adiabatically arrives with a density contrast
    d(rho)/rho = -(delta/H_P)(grad_ad - grad) dr relative to its new
    surroundings, and the restoring buoyancy per unit mass is -g times that.
    N^2 > 0 means oscillation about the starting height (stable, and N is
    the buoyancy frequency); N^2 < 0 means exponential growth, which is
    convection.  N^2 > 0 is therefore the Schwarzschild criterion for
    stability, grad < grad_ad.

    The third term is Ledoux's: a mean molecular weight that increases
    inward makes the displaced parcel LIGHTER than its new surroundings and
    stabilises the stratification even when grad > grad_ad.  For an ideal
    gas delta = -(d ln rho/d ln T)_P = 1 and phi = (d ln rho/d ln mu)_P,T
    = 1, so phi/delta = 1.
    """
    return (g/HP)*(grad_ad - grad + phi_over_delta*grad_mu)


# =========================================================================
# PART B.  Reading the standard solar model table
# =========================================================================

def load_ssm(path=DATA):
    """Read the BS2005-AGS,OP tabulated model.

    Columns, as documented in the header of the data file:
      0 m/Msun  1 r/Rsun  2 T[K]  3 rho[g/cm^3]  4 P[dyn/cm^2]  5 L/Lsun
      6 X(1H)   7 X(4He)  8 X(3He) 9 X(12C)  10 X(14N)  11 X(16O)
    Only rows with all twelve fields parsing as floats are kept, which
    skips the header and the two trailing constant definitions.
    Copied verbatim from m03_numbers.py.
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
    least-squares slope over a wide window averages that noise down.
    Copied verbatim from m03_numbers.py.
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


def structure(ssm, half=25):
    """Everything the Brunt-Vaisala frequency needs, as arrays over the table.

    Returns a dict with r, m, g, HP, mu, grad, grad_mu, cP, plus the
    adiabatic plateau measured in the convective envelope.

    grad     = d ln T / d ln P, from a sliding least-squares fit.
    grad_mu  = d ln mu / d ln P, from the same fit applied to mu(P), with mu
               taken from the table's own P, rho and T rather than from its
               composition columns, so no ionisation assumption enters.
    g        = G m(r) / r^2 from the tabulated mass fraction.
    HP       = P/(rho g), the pressure scale height.
    cP       = (5/2) k/(mu m_u), the monatomic ideal-gas value.

    The plateau is the median of grad over 0.80 < r/R < 0.92: inside the
    convective envelope, above the boundary layer, below the surface
    ionisation zones.  Module 3 measured the same number and got 0.3957.
    """
    r = ssm['rfrac']*RSUN_TAB
    m = ssm['mfrac']*Msun
    P, rho, T = ssm['P'], ssm['rho'], ssm['T']
    g = G*m/r**2
    g[0] = g[1]                       # r -> 0 with m -> 0; the first row is
    HP = P/(rho*g)                    # a placeholder, never used below
    mu = rho*kB*T/(P*mu_u)
    lP, lT, lmu = np.log(P), np.log(T), np.log(mu)
    grad = sliding_slope(lP, lT, half)
    grad_mu = sliding_slope(lP, lmu, half)
    cP = 2.5*kB/(mu*mu_u)
    band = (ssm['rfrac'] > 0.80) & (ssm['rfrac'] < 0.92) & np.isfinite(grad)
    plateau = float(np.median(grad[band]))
    return dict(r=r, m=m, g=g, HP=HP, mu=mu, grad=grad, grad_mu=grad_mu,
                cP=cP, plateau=plateau, rfrac=ssm['rfrac'], T=T, P=P,
                rho=rho, lfrac=ssm['lfrac'])


def convection_zone_base(st, frac=0.99, r_lo=0.60, r_hi=0.95):
    """Innermost radius at which grad reaches `frac` of the adiabatic plateau.

    The same locator as Module 3's, repeated here so this script stands
    alone.  Returns r_base/Rsun.
    """
    r, grad, plateau = st['rfrac'], st['grad'], st['plateau']
    target = frac*plateau
    idx = np.where((r > r_lo) & (r < r_hi) & np.isfinite(grad))[0]
    for j in range(1, len(idx)):
        i0, i1 = idx[j-1], idx[j]
        if grad[i0] < target <= grad[i1]:
            f = (target - grad[i0])/(grad[i1] - grad[i0])
            return r[i0] + f*(r[i1] - r[i0])
    return np.nan



def ledoux_zone_base(st, frac=0.99, r_lo=0.60, r_hi=0.95):
    """convection_zone_base with the Ledoux term added to the threshold.

    The target is frac*plateau + grad_mu, which varies row to row, so the
    linear interpolation carries the target's own slope.  Quoted in the
    module as an UPPER bound on the shift, because beyond about 0.72 R the
    table's grad_mu is partly an ionisation effect (see main()).
    """
    r, grad, plateau, gmu = (st['rfrac'], st['grad'], st['plateau'],
                             st['grad_mu'])
    target = frac*plateau + gmu
    idx = np.where((r > r_lo) & (r < r_hi) & np.isfinite(grad)
                   & np.isfinite(gmu))[0]
    for j in range(1, len(idx)):
        i0, i1 = idx[j-1], idx[j]
        if grad[i0] < target[i0] and grad[i1] >= target[i1]:
            num = target[i0] - grad[i0]
            den = (grad[i1] - grad[i0]) - (target[i1] - target[i0])
            return r[i0] + (num/den)*(r[i1] - r[i0])
    return np.nan


# =========================================================================
# PART C.  Mixing-length theory
# =========================================================================

def mlt_flux(rho, cP, T, g, HP, alpha, excess):
    """Convective flux carried by mixing-length theory, erg cm^-2 s^-1.

    Kippenhahn & Weigert section 7.2, in the efficient limit where the
    parcel loses no heat in transit, so grad_e -> grad_ad.  With
    l = alpha H_P and delta = 1 for an ideal gas:

        v_c = (l/H_P) sqrt( g H_P (grad - grad_ad) / 8 ),
        dT  = T (grad - grad_ad) l / (2 H_P),
        F   = rho v_c c_P dT
            = rho c_P T (l/H_P)^2 sqrt(g H_P/32) (grad - grad_ad)^(3/2).

    The 1/2 in dT and the 1/8 in v_c^2 are the two averaging conventions of
    the standard theory: the parcel is followed for half a mixing length on
    average, and half the work done by buoyancy goes into the surroundings.
    A different convention changes alpha, not the physics; alpha is
    calibrated, which is the theory's weakness and is said so in the prose.
    """
    return rho*cP*T*alpha**2*np.sqrt(g*HP/32.0)*excess**1.5


def mlt_excess(rho, cP, T, g, HP, alpha, F):
    """Invert mlt_flux for the superadiabatic excess grad - grad_ad."""
    return (F/(rho*cP*T*alpha**2*np.sqrt(g*HP/32.0)))**(2.0/3.0)


def mlt_velocity(g, HP, alpha, excess):
    """Convective velocity v_c = (l/H_P) sqrt(g H_P (grad-grad_ad)/8)."""
    return alpha*np.sqrt(g*HP*excess/8.0)


def mlt_at(st, rfrac_target, alpha=2.0):
    """Apply mixing-length theory at one tabulated radius.

    Uses the LOCAL luminosity L(r) from the table, not L_sun, because
    inside 0.3 R not all of the luminosity has yet been generated; in the
    convection zone L(r) = L to five figures, so the distinction only
    matters for the problems.
    """
    i = int(np.argmin(abs(st['rfrac'] - rfrac_target)))
    r = st['r'][i]
    F = st['lfrac'][i]*LSUN_TAB/(4.0*np.pi*r*r)
    exc = mlt_excess(st['rho'][i], st['cP'][i], st['T'][i], st['g'][i],
                     st['HP'][i], alpha, F)
    v = mlt_velocity(st['g'][i], st['HP'][i], alpha, exc)
    cs = np.sqrt(5.0/3.0*st['P'][i]/st['rho'][i])
    return dict(i=i, rfrac=st['rfrac'][i], r=r, F=F, excess=exc, v=v, cs=cs,
                HP=st['HP'][i], g=st['g'][i], T=st['T'][i],
                rho=st['rho'][i], l=alpha*st['HP'][i], tau=alpha*st['HP'][i]/v)


def mlt_photosphere(alpha=2.0, mu=MU_PHOT, T=T_PHOT, P=P_PHOT):
    """Mixing-length theory at the photosphere, from the tau = 2/3 numbers.

    The BS05 table stops at r = 0.983 R, well below the photosphere, so the
    surface layer is done with the independent photospheric inputs.  Two
    warnings, both printed by main():

      1. At tau = 2/3 radiation already carries most of the flux, so
         demanding that convection carry all of L over-estimates the
         excess and the velocity.  The number is therefore an UPPER bound
         on what MLT predicts there, and it is quoted as one.
      2. The resulting v_c/c_s is not small, so the theory's own premise --
         a slow, pressure-equilibrated parcel -- has already failed.
    """
    g = GMsun/Rsun**2
    HP = kB*T/(mu*mu_u*g)
    rho = P*mu*mu_u/(kB*T)
    cP = 2.5*kB/(mu*mu_u)
    F = Lsun/(4.0*np.pi*Rsun**2)
    exc = mlt_excess(rho, cP, T, g, HP, alpha, F)
    v = mlt_velocity(g, HP, alpha, exc)
    cs = np.sqrt(5.0/3.0*P/rho)
    return dict(g=g, HP=HP, rho=rho, cP=cP, F=F, excess=exc, v=v, cs=cs,
                l=alpha*HP, tau=alpha*HP/v)


# =========================================================================
# PART D.  Thermal instability: the cooling function and Field's criteria
# =========================================================================

def ki_lambda_over_gamma(T, a2=KI_A2):
    """Koyama & Inutsuka (2002) eq. (4), corrected, in cm^3.

        Lambda(T)/Gamma = 1e7 exp(-1.184e5/(T+1000))
                        + 1.4e-2 sqrt(T) exp(-92/T).

    The first term is Lyman-alpha cooling, switching on above about 8000 K.
    The second is [C II] 158 micron fine-structure cooling, whose 92 K
    excitation temperature appears explicitly in the exponent; it is what
    cools the cold neutral medium.  The heating Gamma = 2e-26 erg/s per
    hydrogen nucleus is photoelectric emission from small grains and PAHs
    and is taken to be independent of density and temperature.
    """
    return (KI_A1*np.exp(-KI_E1/(T + KI_T1))
            + a2*np.sqrt(T)*np.exp(-KI_E2/T))


def ki_lambda(T, a2=KI_A2):
    """The cooling coefficient itself, erg cm^3 s^-1."""
    return KI_GAMMA*ki_lambda_over_gamma(T, a2)


def ki_equilibrium(T, a2=KI_A2):
    """Thermal-equilibrium density and pressure at temperature T.

    The energy equation of Koyama & Inutsuka (2002) eq. (3) has heating
    (rho/m_H) Gamma and cooling (rho/m_H)^2 Lambda per unit volume, so
    equilibrium n^2 Lambda = n Gamma gives n = Gamma/Lambda(T) directly.
    Returns (n in cm^-3, P/k in K cm^-3).
    """
    n = 1.0/ki_lambda_over_gamma(T, a2)
    return n, n*T


def dln_lambda_dlnT(T, a2=KI_A2, rel=1e-5):
    """d ln Lambda / d ln T by centred differences in log T."""
    lo, hi = T*(1.0 - rel), T*(1.0 + rel)
    return ((np.log(ki_lambda_over_gamma(hi, a2))
             - np.log(ki_lambda_over_gamma(lo, a2)))
            / (np.log(hi) - np.log(lo)))


def field_isobaric(T, a2=KI_A2):
    """Field (1965) criterion (4b) applied to this cooling function.

    Field defines a generalised heat-loss function L(rho, T), energy losses
    minus energy gains per gram per second, exclusive of conduction, and
    writes the criteria (his p. 532, equations 4a and 4b)

        (dL/dT)_rho < 0                                  (isochoric)
        (dL/dT)_P = (dL/dT)_rho - (rho_0/T_0)(dL/drho)_T < 0  (isobaric).

    Here, with rho = n m_H,
        L = rho Lambda(T)/m_H^2 - Gamma/m_H,
        (dL/dT)_rho = (rho/m_H^2) dLambda/dT,
        (dL/drho)_T = Lambda/m_H^2,
    so
        (dL/dT)_P = (rho/m_H^2) [ dLambda/dT - Lambda/T ],
    and the isobaric criterion collapses to the pure statement

        d ln Lambda / d ln T < 1.

    Returns (dlnL/dlnT, isobaric_unstable, isochoric_unstable).  The
    isochoric criterion is dLambda/dT < 0, that is dlnLambda/dlnT < 0, so
    the isobaric condition is strictly weaker: every isochorically unstable
    state is isobarically unstable, and not conversely.
    """
    s = dln_lambda_dlnT(T, a2)
    return s, bool(s < 1.0), bool(s < 0.0)


def two_phase_window(a2=KI_A2, T_lo=10.0, T_hi=1.2e4, n_pts=400001):
    """Locate P_max and P_min on the thermal-equilibrium curve.

    Walking along the curve from low density (high T) to high density (low
    T), the equilibrium pressure rises, turns over at P_max, falls through
    the thermally unstable branch, bottoms out at P_min, and rises again.
    Above P_max only the cold phase exists; below P_min only the warm one;
    between them both are available at the same pressure, which is the
    two-phase medium.  The turning points are exactly the ends of the
    unstable branch, because on the equilibrium curve

        P = Gamma T/Lambda(T)  =>  d ln P/d ln T = 1 - d ln Lambda/d ln T,

    so dP/dT changes sign precisely where d ln Lambda/d ln T passes 1,
    which is Field's isobaric criterion (4b).  The two statements are the
    same statement, and this function checks that numerically.

    Returns a dict with T, n, P/k arrays and the two turning points.
    """
    T = np.logspace(np.log10(T_lo), np.log10(T_hi), n_pts)
    n, P = ki_equilibrium(T, a2)
    dP = np.diff(P)
    turn = np.where(np.diff(np.sign(dP)) != 0)[0] + 1
    out = dict(T=T, n=n, P=P, turning=turn)
    if len(turn) >= 2:
        # the lower-T turning point is P_min, the higher-T one is P_max
        i_min, i_max = turn[0], turn[1]
        out.update(T_pmin=T[i_min], n_pmin=n[i_min], Pmin=P[i_min],
                   T_pmax=T[i_max], n_pmax=n[i_max], Pmax=P[i_max])
    return out


def field_length(T, n, cond_a=KI_COND_A, cond_pow=0.5):
    """The Field length, the shortest unstable wavelength.

    Thermal conduction erases a temperature contrast of size lambda in a
    time of order lambda^2 rho c_P/(4 pi^2 kappa); radiative cooling builds
    one in the cooling time.  Setting them equal defines the wavelength
    below which conduction wins.  With the customary definition

        lambda_F = sqrt( kappa T / (n^2 Lambda) ),

    kappa = cond_a T^cond_pow.  Perturbations shorter than lambda_F are
    conduction-damped, so a thermally unstable medium fragments into
    condensations no smaller than about lambda_F.  Field (1965) section II
    is where the conduction term enters the dispersion relation; the
    combination above is the standard shorthand for the result.
    """
    kappa = cond_a*T**cond_pow
    return np.sqrt(kappa*T/(n*n*ki_lambda(T)))


def spitzer_kappa(T, lnLambda=LN_LAMBDA_ICM):
    """Electron conductivity via Sarazin eq. (5.37), erg s^-1 cm^-1 K^-1."""
    return SPITZER_A*T**2.5/lnLambda


# =========================================================================
# PART E.  The measured pressure distribution
# =========================================================================

def _phi(z):
    """Standard normal cumulative distribution, via the error function."""
    from math import erf, sqrt
    if np.isscalar(z):
        return 0.5*(1.0 + erf(z/sqrt(2.0)))
    return np.array([0.5*(1.0 + erf(v/sqrt(2.0))) for v in np.asarray(z)])


def jt11_fraction(p_lo, p_hi):
    """Mass fraction of CNM between two pressures, from Jenkins & Tripp's fit.

    Their eq. (3) is a Gaussian in log(p/k) with mean 3.58 and sigma 0.175
    weighted by hydrogen column, so the fraction of the mass between two
    pressures is just the Gaussian integral between the two logs.  Pass
    None for an open end.
    """
    z_hi = (np.log10(p_hi) - JT11_LOGP_MEAN)/JT11_LOGP_SIG if p_hi else np.inf
    z_lo = (np.log10(p_lo) - JT11_LOGP_MEAN)/JT11_LOGP_SIG if p_lo else -np.inf
    hi = 1.0 if np.isinf(z_hi) else _phi(z_hi)
    lo = 0.0 if np.isinf(z_lo) else _phi(z_lo)
    return hi - lo


def jt11_pdf(logp):
    """The fitted lognormal as a normalised probability density in log(p/k)."""
    z = (logp - JT11_LOGP_MEAN)/JT11_LOGP_SIG
    return np.exp(-0.5*z*z)/(JT11_LOGP_SIG*np.sqrt(2.0*np.pi))


# =========================================================================
# Reporting
# =========================================================================

def main():
    P = print
    P('=' * 74)
    P('MODULE 6 NUMBERS: convection and thermal instability')
    P('=' * 74)

    ssm = load_ssm()
    st = structure(ssm)
    r = st['rfrac']

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  The displaced parcel and the adiabatic gradient')
    P('-'*74)
    ga_mono = grad_ad_ideal(5.0/3.0)
    ga_di = grad_ad_ideal(1.4)
    P(f'  grad_ad = (gamma-1)/gamma')
    P(f'    monatomic, gamma = 5/3            = {ga_mono:.6f}  (exactly 2/5)')
    P(f'    diatomic,  gamma = 7/5            = {ga_di:.6f}  (exactly 2/7)')
    P('  The Schwarzschild criterion for STABILITY is grad < grad_ad.')
    P('  A parcel displaced up by dr expands adiabatically to its new')
    P('  ambient pressure.  If the surroundings cool faster with height')
    P('  than the parcel does, the parcel arrives hotter and lighter, and')
    P('  keeps rising.  That is the whole argument, and it needs no')
    P('  transport theory.')
    P('')
    P('  The ionisation-zone reduction of grad_ad, pure hydrogen, Saha:')
    P(f'  {"T [K]":>8} {"x":>8} {"grad_ad":>9} {"grad_ad/0.4":>12}')
    for TT in (4e3, 6e3, 8e3, 1.0e4, 1.2e4, 1.5e4, 2.0e4, 3.0e4, 1.0e5):
        ga, x = grad_ad_ionising(TT, P_PHOT)
        P(f'  {TT:>8.0f} {x:>8.4f} {ga:>9.5f} {ga/ga_mono:>12.4f}')
    # locate the minimum on a fine grid at photospheric pressure
    Tg = np.linspace(3e3, 5e4, 40000)
    gag = np.array([grad_ad_ionising(t, P_PHOT)[0] for t in Tg])
    xg = np.array([saha_x(t, P_PHOT) for t in Tg])
    j = int(np.argmin(gag))
    P(f'  minimum at P = {P_PHOT:.1e} dyn/cm^2:  grad_ad = {gag[j]:.5f} '
      f'at T = {Tg[j]:.0f} K, x = {xg[j]:.4f}')
    P(f'  PUNCHLINE the hydrogen ionisation zone drops grad_ad from 0.4000')
    P(f'  to {gag[j]:.4f}, a factor {ga_mono/gag[j]:.2f}.')
    rb_A = convection_zone_base(st)
    T_rb = float(np.interp(rb_A, st['rfrac'], st['T']))
    r_out, T_out = float(st['rfrac'][-1]), float(st['T'][-1])
    iA = int(np.argmin(np.abs(st['rfrac'] - 0.40)))
    iB = int(np.argmin(np.abs(st['rfrac'] - 0.75)))
    plateau = st['plateau']
    P('  NAME WHAT THIS EXPLAINS, AND WHAT IT DOES NOT.  The collapse sits')
    P(f'  at T = {Tg[j]:.0f} K.  PART B finds the base of the solar convection')
    P(f'  zone at {rb_A:.4f} R, where the table gives T = {T_rb:.3g} K, and the')
    P(f'  table\'s outermost row, {r_out:.5f} R, is already at T = {T_out:.3g} K --')
    P('  above the whole collapse band.  So the ionisation zone lies')
    P(f'  outside {r_out:.3f} R, in the outermost {100*(1.0-r_out):.1f}% of the radius.  It')
    P('  does NOT make the outer 30% of the Sun convective.  What it')
    P('  explains is that convection reaches all the way to the')
    P('  photosphere, and that the superadiabatic layer of PART C sits')
    P('  there.  The base is set the other way round: PART B shows grad')
    P(f'  RISING from {st["grad"][iA]:.4f} at {st["rfrac"][iA]:.4f} R to {st["grad"][iB]:.4f} at')
    P(f'  {st["rfrac"][iB]:.4f} R, a factor {st["grad"][iB]/st["grad"][iA]:.3f}, across the flat plateau')
    P(f'  {plateau:.4f}.')
    P('  The parcel spends its compression energy ionising hydrogen instead')
    jhalf = int(np.argmin(abs(xg - 0.5)))
    P(f'  of heating itself.  At the MINIMUM, T = {Tg[j]:.0f} K, '
      f'chi_H/kT = {chi_H/(kB*Tg[j]):.2f};')
    P(f'  at HALF IONISATION, T = {Tg[jhalf]:.0f} K, '
      f'chi_H/kT = {chi_H/(kB*Tg[jhalf]):.2f}.  The two are')
    P('  different temperatures and the 12.9 belongs to the first: the')
    P('  ionisation reservoir is about twelve times the thermal one.')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  The Brunt-Vaisala frequency through the Sun')
    P('-'*74)
    rb = convection_zone_base(st)
    P(f'  adiabatic plateau grad measured, 0.80-0.92 R = {st["plateau"]:.4f}')
    P(f'  convection-zone base recovered by the same locator = {rb:.4f} R')
    P(f'  (Module 3 got the same two numbers; they are reproduced here only')
    P('  to show this script reads the table identically.)')
    P('')
    P('  N^2 is computed two ways, and the difference is the point:')
    P('    (i)  grad_ad = 0.4 exactly, the ideal monatomic value;')
    P('    (ii) grad_ad = the measured plateau, which is what the model')
    P('         itself used -- its equation of state includes Coulomb')
    P('         corrections and a little radiation pressure.')
    N2_ideal = brunt_vaisala_sq(st['g'], st['HP'], ga_mono, st['grad'])
    N2_plat = brunt_vaisala_sq(st['g'], st['HP'], st['plateau'], st['grad'])
    N2_led = brunt_vaisala_sq(st['g'], st['HP'], st['plateau'], st['grad'],
                              grad_mu=st['grad_mu'])
    N2_schw = N2_plat
    ok = np.isfinite(N2_ideal) & (r > 0.02)
    P('')
    P(f'  {"r/R":>7} {"grad":>8} {"grad_mu":>9} {"H_P [cm]":>10} '
      f'{"N (uHz) ideal":>14} {"N (uHz) plateau":>16} {"+Ledoux":>10}')
    for x in (0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.68, 0.71,
              0.75, 0.85, 0.95, 0.98):
        i = int(np.argmin(abs(r - x)))
        def uHz(v):
            return 1e6*np.sqrt(v)/(2.0*np.pi) if v > 0 else -1.0
        a, b, cc = uHz(N2_ideal[i]), uHz(N2_plat[i]), uHz(N2_led[i])
        fa = f'{a:.2f}' if a > 0 else 'imaginary'
        fb = f'{b:.2f}' if b > 0 else 'imaginary'
        fc = f'{cc:.2f}' if cc > 0 else 'imaginary'
        P(f'  {r[i]:>7.4f} {st["grad"][i]:>8.4f} {st["grad_mu"][i]:>9.5f} '
          f'{st["HP"][i]:>10.3e} {fa:>14} {fb:>16} {fc:>10}')
    rad = (r > 0.05) & (r < 0.65) & np.isfinite(N2_schw)
    idx = np.where(rad)[0]
    imax = idx[int(np.argmax(N2_schw[idx]))]
    Nmax = np.sqrt(N2_schw[imax])
    P('')
    P(f'  PUNCHLINE maximum of N in the radiative interior (0.05-0.65 R):')
    P(f'    N_max                             = {Nmax:.4e} rad/s '
      f'= {1e6*Nmax/(2.0*np.pi):.2f} uHz')
    P(f'    at r/R                            = {r[imax]:.4f}')
    P(f'    buoyancy period 2 pi/N            = {2.0*np.pi/Nmax/60.0:.1f} min')
    P('    Read it against the 5-minute p modes, which are ACOUSTIC.  A')
    P('    g mode cannot have a period shorter than 2 pi/N_max, so every')
    P(f'    solar g mode must have a period longer than {2.0*np.pi/Nmax/60.0:.0f} minutes; the')
    P('    two mode families cannot be confused.')
    # the Ledoux contribution
    led_frac = np.full_like(N2_schw, np.nan)
    good = np.isfinite(st['grad_mu']) & np.isfinite(st['grad'])
    denom = (st['plateau'] - st['grad'])[good] + st['grad_mu'][good]
    with np.errstate(divide='ignore', invalid='ignore'):
        led_frac[good] = st['grad_mu'][good]/denom
    P('')
    P('  The Ledoux term, from the table\'s own mu(r):')
    for x in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.60):
        i = int(np.argmin(abs(r - x)))
        P(f'    r/R = {r[i]:.3f}  mu = {st["mu"][i]:.5f}  '
          f'grad_mu = {st["grad_mu"][i]:+.5f}  '
          f'share of N^2 = {100*led_frac[i]:+.2f}%')
    cz = (r > 0.75) & (r < 0.93) & np.isfinite(st['grad_mu'])
    P('    The composition gradient left by 4.6 Gyr of hydrogen burning is')
    P('    LARGE where it exists: at 0.10 R it supplies 75% of N^2, and')
    P('    inside 0.15 R it dominates the Schwarzschild term outright.  It')
    P('    then dies away: by 0.30 R it is 1.4% and by 0.40 R it is 0.7%,')
    P('    because outside the burning core mu is flat.')
    P('    THIS DOES NOT CHANGE ANY BOUNDARY IN THE SUN, and the size of')
    P('    the "no" is MEASURED, not asserted.  The Ledoux term only')
    P('    matters where the two criteria could disagree, that is where')
    P('    grad is close to grad_ad.')
    i05 = int(np.argmin(abs(r - 0.050)))
    i20 = int(np.argmin(abs(r - 0.200)))
    P(f'    (a) Where grad_mu is LARGE, inside 0.2 R, the Schwarzschild')
    P(f'        margin grad_ad - grad runs from '
      f'{plateau - st["grad"][i05]:.4f} at {r[i05]:.3f} R')
    P(f'        to {plateau - st["grad"][i20]:.4f} at {r[i20]:.3f} R, so '
      f'those layers are stable by a')
    P('        wide margin under either criterion.')
    rad = (r >= 0.30) & (r <= 0.60) & np.isfinite(st['grad_mu'])
    P(f'    (b) Through the radiative zone outside the burning core, over')
    P(f'        0.30-0.60 R, |grad_mu| <= '
      f'{np.nanmax(np.abs(st["grad_mu"][rad])):.5f}.  Over 0.75-0.93 R, inside')
    P(f'        the convection zone, '
      f'|grad_mu| <= {np.nanmax(np.abs(st["grad_mu"][cz])):.5f}.')
    base_s = convection_zone_base(st)
    base_l = ledoux_zone_base(st)
    P(f'    (c) Locating the base again with grad_ad + grad_mu in place of')
    P(f'        grad_ad, same locator: {base_s:.4f} R -> {base_l:.4f} R, a')
    P(f'        shift of {base_l - base_s:.4f} R = '
      f'{100*(base_l - base_s):.2f} per cent of the radius.')
    P('        That is an UPPER BOUND, because the grad_mu the table gives')
    P('        near the base is partly the effective-mu artefact below.')
    P('    Ledoux and Schwarzschild put the')
    P('    base of the solar convection zone in the same place.  They do')
    P('    not in a star with a receding convective core; PROBLEM 4 is')
    P('    that case.')
    P('    One caution on the outer rows.  Beyond about 0.72 R the mu')
    P('    printed here is an EFFECTIVE mu, rho k T/(P m_u), which absorbs')
    P('    the changing ionisation state of hydrogen and helium as well as')
    P('    the composition.  Its gradient there is an ionisation effect,')
    P('    not a composition gradient, and it must not be fed into the')
    P('    Ledoux criterion.  That is why the table above stops at 0.60 R.')
    P('')
    P('  HONEST LIMIT on the sign of N^2 inside the convection zone.')
    i90 = int(np.argmin(abs(r - 0.90)))
    P(f'    At r = 0.90 R the table gives grad = {st["grad"][i90]:.6f} and the')
    P(f'    plateau is {st["plateau"]:.6f}; the difference is '
      f'{st["grad"][i90]-st["plateau"]:+.2e}.')
    P(f'    PART C shows the true excess there is of order 1e-6.  The table')
    P('    quotes P, rho and T to four significant figures, so it cannot')
    P('    resolve a difference that small.  N^2 in the convection zone is')
    P('    reported as ZERO TO WITHIN THE TABLE\'S PRECISION, not as')
    P('    measured negative.  The radiative-interior maximum above is')
    P('    robust, because there grad_ad - grad is of order 0.1.')

    # ---------------------------------------------------------------- C
    P('')
    P('PART C.  Mixing-length theory: how superadiabatic must the Sun be?')
    P('-'*74)
    alpha = 2.0
    P(f'  alpha = l/H_P = {alpha}, the usual solar-calibrated value.')
    P(f'  {"r/R":>7} {"T [K]":>10} {"H_P [cm]":>10} {"F [erg/cm2/s]":>14} '
      f'{"grad-grad_ad":>13} {"v_c [cm/s]":>11} {"v_c/c_s":>9} {"l/v [s]":>9}')
    rows = {}
    for x in (0.72, 0.75, 0.80, 0.85, 0.90, 0.95, 0.98, 0.9831):
        d = mlt_at(st, x, alpha)
        rows[x] = d
        P(f'  {d["rfrac"]:>7.4f} {d["T"]:>10.3e} {d["HP"]:>10.3e} '
          f'{d["F"]:>14.4e} {d["excess"]:>13.3e} {d["v"]:>11.4e} '
          f'{d["v"]/d["cs"]:>9.5f} {d["tau"]:>9.1f}')
    d90 = rows[0.90]
    ph = mlt_photosphere(alpha)
    P('')
    P(f'  PUNCHLINE at r = 0.90 R the superadiabatic excess needed to carry')
    P(f'  the whole solar luminosity is grad - grad_ad = {d90["excess"]:.3e},')
    P(f'  that is {d90["excess"]/st["plateau"]*100:.1e}% of grad_ad itself.  Convection there is so')
    P(f'  efficient that the stratification is adiabatic to one part in')
    P(f'  {1.0/d90["excess"]:.0e}.  THAT is why a polytrope of index 3/2 works at all.')
    P('')
    P('  At the photosphere, from the tau = 2/3 inputs (T = 5772 K,')
    P(f'  P = {P_PHOT:.1e} dyn/cm^2, mu = {MU_PHOT}):')
    P(f'    g                                 = {ph["g"]:.4e} cm/s^2')
    P(f'    H_P                               = {ph["HP"]/1e5:.1f} km')
    P(f'    rho                               = {ph["rho"]:.4e} g/cm^3')
    P(f'    F = L/(4 pi R^2)                  = {ph["F"]:.4e} erg/cm^2/s')
    P(f'    grad - grad_ad (UPPER BOUND)      = {ph["excess"]:.4f}')
    P(f'    v_c                               = {ph["v"]/1e5:.3f} km/s')
    P(f'    c_s                               = {ph["cs"]/1e5:.3f} km/s')
    P(f'    v_c/c_s                           = {ph["v"]/ph["cs"]:.4f}')
    P(f'    l = alpha H_P                     = {ph["l"]/1e5:.0f} km')
    P(f'    turnover time l/v_c               = {ph["tau"]/60.0:.2f} min')
    P(f'  PUNCHLINE the excess runs from {d90["excess"]:.1e} at 0.90 R to '
      f'{ph["excess"]:.2f} at the')
    P(f'  photosphere, a factor {ph["excess"]/d90["excess"]:.0e}.  Efficient convection deep,')
    P('  inefficient convection at the surface: the parcel near the top is')
    P('  optically thin and radiates its heat excess away before it has')
    P('  travelled a mixing length.  The excess is an UPPER BOUND because')
    P('  radiation already carries most of the flux at tau = 2/3, so')
    P('  requiring convection to carry all of L overstates it.')
    P(f'  And v_c/c_s = {ph["v"]/ph["cs"]:.2f} there: the theory assumes a subsonic parcel')
    P('  in instantaneous pressure balance, and that assumption is spent.')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  CHECK A (solar).  Mixing-length theory against granulation')
    P('-'*74)
    P('  Two predictions, two measurements, two verdicts.  Both')
    P('  measurements are of the solar photosphere at disk centre; neither')
    P('  used a stellar model.')
    P('')
    P('  A1.  THE SIZE.  MLT says the overturning eddy is one mixing')
    P('       length across, l = alpha H_P, so a convection cell seen from')
    P('       above should be about 2 l wide (up in the middle, down at the')
    P('       edges, one mixing length each way).')
    d_cell = 2.0*ph['l']
    P(f'       H_P at tau = 2/3                = {ph["HP"]/1e5:.0f} km')
    P(f'       l = alpha H_P                   = {ph["l"]/1e5:.0f} km')
    P(f'       predicted cell diameter 2 l     = {d_cell/1e5:.0f} km')
    P(f'       measured granule diameter       = {GRAN_D0/1e5:.0f} +/- '
      f'{GRAN_D0_ERR/1e5:.0f} km (mean), spread {GRAN_SIG/1e5:.0f} km')
    P(f'       PUNCHLINE ratio measured/2l     = {GRAN_D0/d_cell:.2f}')
    P(f'       departure, against the error ON THE MEAN ({GRAN_D0_ERR/1e5:.0f} km) = '
      f'{(GRAN_D0-d_cell)/GRAN_D0_ERR:.1f} sigma')
    P(f'       departure, against the POPULATION SPREAD ({GRAN_SIG/1e5:.0f} km) = '
      f'{(GRAN_D0-d_cell)/GRAN_SIG:.2f} sigma')
    P(f'       against l alone the ratio is    = {GRAN_D0/ph["l"]:.2f}')
    P('       BOTH DENOMINATORS ARE PRINTED AND EACH IS NAMED, because they')
    P('       say different things.  Abramenko section 3 gives d0 = 1050')
    P('       +/- 22 km and sigma = 480 +/- 11 km: 22 km is the error on')
    P('       the mean, 480 km is the width of the granule population and')
    P('       is not an uncertainty.  Their Conclusions print "1050 +/-')
    P('       480 km", which reads as an error bar and is not one.')
    P(f'       Read the two: {(GRAN_D0-d_cell)/GRAN_D0_ERR:.1f} sigma says the MEAN granule is not')
    P(f'       {d_cell/1e5:.0f} km; {(GRAN_D0-d_cell)/GRAN_SIG:.2f} sigma says a {d_cell/1e5:.0f} km cell is an ordinary')
    P('       member of that population.')
    P('       VERDICT: THE SCALE IS CONFIRMED, THE NUMBER DISAGREES.  H_P')
    P(f'       sets the granule size -- {ph["HP"]/1e5:.0f} km against a {GRAN_D0/1e5:.0f} km granule,')
    P('       with alpha of order unity, is the content of the agreement,')
    P(f'       and the identification itself is ambiguous: 2l gives {GRAN_D0/d_cell:.2f} and')
    P(f'       l alone gives {GRAN_D0/ph["l"]:.2f}.  The specific prediction 2l = {d_cell/1e5:.0f} km')
    P(f'       is {(GRAN_D0-d_cell)/GRAN_D0_ERR:.1f} sigma from the measured mean.  Module 3 prints')
    P('       its 29.4 sigma the same way and calls it a DISAGREEMENT, not')
    P('       a refutation; this module follows that precedent.')
    P('       Note also that alpha = 2 was CALIBRATED on the solar radius,')
    P('       so this is not a parameter-free prediction.  What is')
    P('       parameter-free is that the scale is set by H_P at all.')
    P('')
    P('  A2.  THE SPEED.  Same theory, same alpha, same layer.')
    P(f'       predicted v_c (upper bound)     = {ph["v"]/1e5:.2f} km/s')
    P(f'       measured, upflow at h = {OBA_H_LO:.0f} km    = '
      f'{OBA_UP_LO/1e5:.2f} km/s')
    P(f'       measured, upflow at h = {OBA_H_HI:.0f} km   = '
      f'{OBA_UP_HI/1e5:.2f} km/s')
    P(f'       measured, rms convective        = {OBA_RMS_LO/1e5:.1f} km/s '
      f'(deepest) to {OBA_RMS_HI/1e5:.1f} km/s (highest)')
    P(f'       stated velocity error           = {OBA_ERR/1e5:.2f} km/s')
    P(f'       PUNCHLINE ratio predicted/measured = '
      f'{ph["v"]/OBA_UP_LO:.1f} against the 0.65 km/s upflow')
    P(f'                                        = {ph["v"]/OBA_RMS_LO:.1f} '
      f'against the 0.6 km/s rms')
    P(f'       Too fast by {ph["v"]/OBA_UP_LO:.1f} is far outside a factor of 2.  But do')
    P('       not stop here.  The calculation above contains an assumption')
    P('       that is no part of mixing-length theory at all: that')
    P('       convection carries the WHOLE luminosity at tau = 2/3.  Test')
    P('       that assumption, against the same two measurements.')
    P(f'       Note also v_c/c_s = {ph["v"]/ph["cs"]:.2f} in this over-driven version, an')
    P('       independent warning that MLT has been pushed past its own')
    P('       premise of a slow, pressure-balanced parcel.')
    P('')
    P('  A3.  WHAT FLUX DOES THE MEASURED GRANULATION ACTUALLY CARRY?')
    P('       PART C warned that the photospheric excess is an upper bound')
    P('       because radiation carries most of the flux at tau = 2/3.')
    P('       Turn that warning into a number.  This uses no stellar model')
    P('       beyond the photospheric inputs already in use, and it rests')
    P('       on two assumptions that must be stated: rho at tau = 2/3 is')
    P('       an INPUT carried from Module 3, not a measurement; and the')
    P('       contrast is converted through a Planck source function, as')
    P('       if it formed at one depth.')
    P('       Step 1.  Convert the measured intensity contrast to a')
    P('       temperature contrast.  Abramenko et al. (2012) report an rms')
    P(f'       contrast of {100*GRAN_CONTRAST:.1f} +/- {100*GRAN_CONTRAST_ERR:.1f}% at {GRAN_LAMBDA*1e7:.1f} nm.  For a Planck')
    P('       function, dI/I = (d ln B/d ln T)(dT/T), with')
    P('         d ln B_lambda/d ln T = x e^x/(e^x - 1),  x = hc/(lambda k T).')
    x_pl = h_pl*c/(GRAN_LAMBDA*kB*T_PHOT)
    dlnB = x_pl*np.exp(x_pl)/(np.exp(x_pl) - 1.0)
    dT_over_T = GRAN_CONTRAST/dlnB
    dT = dT_over_T*T_PHOT
    P(f'         x at {GRAN_LAMBDA*1e7:.1f} nm and {T_PHOT:.0f} K     = {x_pl:.4f}')
    P(f'         d ln B/d ln T                 = {dlnB:.4f}')
    P(f'         dT/T                          = {dT_over_T:.5f}')
    P(f'         dT                            = {dT:.1f} K')
    P(f'       The bandpass amplifies contrast by {dlnB:.2f}, so a {100*GRAN_CONTRAST:.1f}%')
    P(f'       intensity contrast is only a {100*dT_over_T:.1f}% temperature contrast.')
    P('       Reading the contrast as a temperature contrast directly')
    P('       would overstate the flux by that same factor.')
    P('       Step 2.  Feed the measured dT and the measured velocity into')
    P('       the mixing-length flux expression F = rho v c_P dT.')
    F_meas = ph['rho']*OBA_UP_LO*ph['cP']*dT
    P(f'         rho at tau = 2/3 (input)      = {ph["rho"]:.4e} g/cm^3')
    P(f'         v measured (Oba et al. 2017)  = {OBA_UP_LO/1e5:.2f} km/s')
    P(f'         c_P                           = {ph["cP"]:.4e} erg/(g K)')
    P(f'         F_conv from measurements      = {F_meas:.4e} erg/cm^2/s')
    P(f'         F_total = L/(4 pi R^2)        = {ph["F"]:.4e} erg/cm^2/s')
    P(f'         PUNCHLINE F_conv/F_total      = {F_meas/ph["F"]:.4f}')
    P(f'       Convection carries {100*F_meas/ph["F"]:.1f}% of the flux at tau = 2/3.')
    P(f'       The other {100*(1-F_meas/ph["F"]):.0f}% is radiation.  So the PART C')
    P('       calculation, which demanded that convection carry all of it,')
    P(f'       over-drove the theory by a factor {ph["F"]/F_meas:.0f} in flux.  Since')
    P(f'       v_c ~ F^(1/3) at fixed alpha, that is {(ph["F"]/F_meas)**(1.0/3.0):.1f} in velocity --')
    P(f'       which is most of the factor {ph["v"]/OBA_UP_LO:.1f} above.')
    v_fair = mlt_velocity(ph['g'], ph['HP'], 2.0,
                          mlt_excess(ph['rho'], ph['cP'], T_PHOT, ph['g'],
                                     ph['HP'], 2.0, F_meas))
    P('       Run MLT again, asking it to carry only that measured flux:')
    P(f'         grad - grad_ad                = '
      f'{mlt_excess(ph["rho"], ph["cP"], T_PHOT, ph["g"], ph["HP"], 2.0, F_meas):.4f}')
    P(f'         v_c                           = {v_fair/1e5:.3f} km/s')
    P(f'         ratio to the measured {OBA_UP_LO/1e5:.2f} km/s = {v_fair/OBA_UP_LO:.2f}')
    P('       THE VERDICT, IN THIS ORDER.  REFUTED: the proposition')
    P('       "convection carries the solar flux at tau = 2/3", which')
    P(f'       fails by a factor of {ph["F"]/F_meas:.0f}.  SURVIVES: the mixing-length')
    P(f'       velocity law itself, to {abs(v_fair/OBA_UP_LO - 1)*100:.0f}%, once it is asked a')
    P('       question it can answer.  What remains genuinely outside MLT')
    P('       is the flux SPLIT between radiation and convection, which')
    P('       needs an atmosphere model with radiative transfer that this')
    P('       module does not build.')
    P('       Deep in the zone, where the premises do hold, there is')
    P('       nothing to measure directly: the excess is 1e-6.  That is')
    P('       the honest position, and it is uncomfortable.  The theory is')
    P('       directly checkable only in the layer where it works worst.')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  The cooling function, and a test of it before use')
    P('-'*74)
    P('  Koyama & Inutsuka (2002) eq. (4) as PRINTED has coefficient 14 on')
    P('  the second term and 114800 in the first exponent.  Test it:')
    for a2, lab in ((KI_A2_PRINTED, 'as printed, a2 = 14'),
                    (KI_A2, 'corrected,  a2 = 1.4e-2')):
        n1, p1 = ki_equilibrium(100.0, a2)
        n2, p2 = ki_equilibrium(8000.0, a2)
        P(f'    {lab:<26}  T=100 K: n = {n1:.4e}, P/k = {p1:.4e}')
        P(f'    {"":<26}  T=8000K: n = {n2:.4e}, P/k = {p2:.4e}')
    P(f'  Measured interstellar pressures are near {10**JT11_LOGP_MEAN:.0f} '
      f'K cm^-3 (Jenkins &')
    P('  Tripp 2011).  The printed form misses by three orders of')
    P('  magnitude; the corrected form does not.  The correction is not a')
    P('  guess: Vazquez-Semadeni et al. (2007) print the corrected equation')
    P('  and their footnote 5 says the corrections came from H. Koyama.')
    P('  USING THE PRINTED EQUATION WOULD HAVE DESTROYED THIS MODULE.')
    P('')
    P('  The corrected function, and Field\'s isobaric criterion on it:')
    P(f'  {"T [K]":>8} {"Lambda [erg cm3/s]":>19} {"dlnL/dlnT":>10} '
      f'{"n_eq":>10} {"P/k":>10} {"isobaric":>10} {"isochoric":>10}')
    for TT in (20, 40, 80, 100, 184, 300, 600, 1000, 2000, 5039, 6000,
               8000, 10000):
        s, iso_p, iso_v = field_isobaric(float(TT))
        n_e, p_e = ki_equilibrium(float(TT))
        P(f'  {TT:>8} {ki_lambda(float(TT)):>19.4e} {s:>10.4f} '
          f'{n_e:>10.4f} {p_e:>10.1f} '
          f'{"UNSTABLE" if iso_p else "stable":>10} '
          f'{"UNSTABLE" if iso_v else "stable":>10}')
    P('  Note what the two columns say.  The isochoric criterion (Field 4a,')
    P('  dLambda/dT < 0) is satisfied almost nowhere; the isobaric one')
    P('  (Field 4b, which reduces to dlnLambda/dlnT < 1 for this heating')
    P('  law) is satisfied over a wide band.  Field\'s point in 1965 was')
    P('  exactly this: Parker had used the isochoric criterion, which is')
    P('  incompatible with the force equation, because a parcel at fixed')
    P('  density but changed temperature is at the wrong pressure and')
    P('  will move.  The isobaric criterion is the one that matters, and')
    P('  it is far weaker, so far more of the ISM is unstable.')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  The two-phase window, computed and compared')
    P('-'*74)
    tp = two_phase_window()
    P(f'  From the corrected Koyama-Inutsuka cooling function:')
    P(f'    P_min/k = {tp["Pmin"]:.1f} K cm^-3 at T = {tp["T_pmin"]:.1f} K, '
      f'n = {tp["n_pmin"]:.3f} cm^-3')
    P(f'    P_max/k = {tp["Pmax"]:.1f} K cm^-3 at T = {tp["T_pmax"]:.1f} K, '
      f'n = {tp["n_pmax"]:.3f} cm^-3')
    ki_geo = np.sqrt(tp['Pmin']*tp['Pmax'])
    P(f'    geometric mean                   = {ki_geo:.1f} K cm^-3')
    P(f'    window width P_max/P_min         = {tp["Pmax"]/tp["Pmin"]:.3f}')
    P('')
    P('  Against Wolfire, McKee, Hollenbach & Tielens (2003), Table 3,')
    P('  R = 8.5 kpc, N_cl = 1e19 cm^-2, which is a full calculation of the')
    P('  heating and cooling with real abundances and grain physics:')
    P(f'    {"":<12} {"KI02 fit":>10} {"W03 full":>10} {"ratio":>8}')
    P(f'    {"P_min/k":<12} {tp["Pmin"]:>10.1f} {W03_PMIN:>10.1f} '
      f'{tp["Pmin"]/W03_PMIN:>8.3f}')
    P(f'    {"P_max/k":<12} {tp["Pmax"]:>10.1f} {W03_PMAX:>10.1f} '
      f'{tp["Pmax"]/W03_PMAX:>8.3f}')
    P(f'    {"geom. mean":<12} {ki_geo:>10.1f} {W03_PAVE:>10.1f} '
      f'{ki_geo/W03_PAVE:>8.3f}')
    P(f'    {"T at P_max":<12} {tp["T_pmax"]:>10.1f} '
      f'{W03_T_WNM_AT_PMAX:>10.1f} {tp["T_pmax"]/W03_T_WNM_AT_PMAX:>8.4f}')
    P(f'    {"T at P_min":<12} {tp["T_pmin"]:>10.1f} '
      f'{W03_T_CNM_AT_PMIN:>10.1f} {tp["T_pmin"]/W03_T_CNM_AT_PMIN:>8.3f}')
    P(f'    {"n at P_max":<12} {tp["n_pmax"]:>10.3f} '
      f'{W03_N_WNM_AT_PMAX:>10.3f} {tp["n_pmax"]/W03_N_WNM_AT_PMAX:>8.3f}')
    P(f'    {"n at P_min":<12} {tp["n_pmin"]:>10.3f} '
      f'{W03_N_CNM_AT_PMIN:>10.3f} {tp["n_pmin"]/W03_N_CNM_AT_PMIN:>8.3f}')
    P('  A two-term analytic fit reproduces both edges of the window to')
    P('  better than 20%, and the coldest temperature the warm phase can')
    P(f'  reach to {abs(tp["T_pmax"]/W03_T_WNM_AT_PMAX - 1)*100:.2f}%.  That is a check on the ARITHMETIC of')
    P('  this section, not on nature; both numbers are calculations.')
    P('  Wolfire et al. also quote the general result, from Field,')
    P('  Goldsmith & Habing (1969), that P_max is at most about 3 P_min.')
    P(f'  Here: {tp["Pmax"]/tp["Pmin"]:.2f} from the fit, '
      f'{W03_PMAX/W03_PMIN:.2f} from the full calculation.')
    P('')
    P('  The thermally unstable branch, where dP/dn < 0 on the equilibrium')
    P('  curve and Field (4b) is satisfied:')
    P(f'    temperatures  {tp["T_pmin"]:.1f} K  <  T  <  {tp["T_pmax"]:.1f} K')
    P(f'    densities     {tp["n_pmax"]:.3f} cm^-3  <  n  <  '
      f'{tp["n_pmin"]:.3f} cm^-3')
    P(f'    Heiles & Troland (2003) call {HT03_T_UNST_LO:.0f}-{HT03_T_UNST_HI:.0f} K the unstable range for')
    P(f'    the warm neutral medium; the curve here gives '
      f'{tp["T_pmin"]:.0f}-{tp["T_pmax"]:.0f} K.  The')
    P(f'    upper edges match to {abs(tp["T_pmax"]/HT03_T_UNST_HI-1)*100:.1f}%, which is the edge that matters')
    P('    for their measurement, because a WNM parcel becomes unstable by')
    P('    cooling THROUGH that edge.  The lower edges are not the same')
    P(f'    quantity: {HT03_T_UNST_LO:.0f} K is a round number they adopt to classify 21-cm')
    P(f'    components, and {tp["T_pmin"]:.0f} K is where this particular cooling fit')
    P('    turns over.  Do not report the two lower numbers as a check.')

    # ---------------------------------------------------------------- G
    P('')
    P('PART G.  THE ANCHOR CHECK.  Jenkins & Tripp (2011) against the window')
    P('-'*74)
    p_med = 10.0**JT11_LOGP_MEAN
    P(f'  The measurement.  C I fine-structure excitation along 89 sight')
    P(f'  lines, STIS echelle.  Mass-weighted lognormal, their eq. (3):')
    P(f'    mean log(p/k)                     = {JT11_LOGP_MEAN:.2f} dex')
    P(f'    rms dispersion                    = {JT11_LOGP_SIG:.3f} dex '
      f'(a LOWER limit, their word)')
    P(f'    median p/k                        = {p_med:.1f} K cm^-3')
    P(f'    +/- 1 sigma range                 = '
      f'{10**(JT11_LOGP_MEAN-JT11_LOGP_SIG):.0f} to '
      f'{10**(JT11_LOGP_MEAN+JT11_LOGP_SIG):.0f} K cm^-3')
    P('')
    P('  CONFIRMED.  The measured centre lies inside the predicted window.')
    P(f'    predicted window  [{W03_PMIN:.0f}, {W03_PMAX:.0f}] K cm^-3, '
      f'geometric mean {W03_PAVE:.0f}')
    P(f'    measured median                   = {p_med:.1f} K cm^-3')
    P(f'    PUNCHLINE ratio median/P_ave      = {p_med/W03_PAVE:.3f}')
    P(f'    position in the window, in dex    = '
      f'{(JT11_LOGP_MEAN-np.log10(W03_PMIN))/(np.log10(W03_PMAX)-np.log10(W03_PMIN)):.3f} '
      f'of the way from P_min to P_max')
    P('    Neither edge of the window was fitted to a pressure value.')
    P('    Wolfire et al. computed them from grain photoelectric heating,')
    P('    [C II] and [O I] cooling, and gas-phase carbon and oxygen')
    P('    abundances fixed by independent HST absorption studies, with a')
    P('    PAH abundance fixed by ISO emission data.  One heating')
    P('    parameter, phi_PAH = 0.5, was calibrated to an observed')
    P('    C I/C II column-density ratio, which Wolfire\'s own working')
    P('    (ms.tex:2608-2611) takes from Welty & Hobbs (2001).  The')
    P('    prediction that a factor-2.5 window exists AT ALL, and sits')
    P('    where it does, is the content of the confirmation.')
    jt01 = 2240.0      # Jenkins & Tripp (2001) mean pressure, K cm^-3
    P('    Wolfire et al. also compared their predicted average against')
    P('    Jenkins & Tripp (2001), AFTER THE FACT and without adjusting')
    P('    any parameter:')
    P(f'      W03 P_ave/k = {W03_PAVE:.0f} against JT01 {jt01:.0f} K cm^-3, '
      f'a factor {W03_PAVE/jt01:.2f}')
    P(f'      that is {np.log10(W03_PAVE/jt01):.2f} dex, and the 2011 median '
      f'{10**JT11_LOGP_MEAN:.1f} is')
    P(f'      {(JT11_LOGP_MEAN - np.log10(jt01)):.2f} dex above the same 2001 value.')
    P('')
    P('    HOW FAR THE CONFIRMATION SURVIVES ITS OWN PARAMETERS.')
    P('    Wolfire et al. Table 4 gives five model variants.  Ask each one')
    P('    whether it still contains the measured median:')
    P(f'      {"model":<14}{"phi_PAH":>8} {"P_min/k":>8} {"P_max/k":>8} '
      f'{"P_ave/k":>8}  {"inside?":>7} {"med/P_max":>9} {"med/P_ave":>9}'
      f'   {"Wolfire":<15}')
    for lab, phi, pmn, pmx, pav, how in W03_TABLE4:
        inside = 'YES' if pmn <= p_med <= pmx else 'NO'
        P(f'      {lab:<14}{phi:>8.2f} {pmn:>8.1f} {pmx:>8.1f} {pav:>8.1f}'
          f'  {inside:>7} {p_med/pmx:>9.3f} {p_med/pav:>9.3f}   {how:<15}')
    n_in = sum(1 for r in W03_TABLE4 if r[2] <= p_med <= r[3])
    P(f'    The median is inside {n_in} of the {len(W03_TABLE4)} windows.  Read the')
    P('    med/P_max column: in two of those it is inside only narrowly,')
    P(f'    at {p_med/W03_TABLE4[3][3]:.3f} and {p_med/W03_TABLE4[4][3]:.3f} of P_max -- margins of only')
    P(f'    {W03_TABLE4[3][3]-p_med:.0f} and {W03_TABLE4[4][3]-p_med:.0f} K cm^-3.')
    P('    PUNCHLINE the confirmation is NOT robust across the variants')
    P(f'    its own authors tested.  In "Low phi_PAH" P_max = {W03_TABLE4[1][3]:.0f} and')
    P(f'    the measured median {p_med:.1f} lies ABOVE it, by a factor')
    P(f'    {p_med/W03_TABLE4[1][3]:.3f}.  Say this, and then say what mitigates it.')
    P('    Wolfire et al. disfavour EVERY non-standard row, on evidence')
    P('    that is not a pressure.  Their four-item enumeration at')
    P('    ms.tex:2622-2633 reads, in their own order: (1) "Low phi_PAH"')
    P('    poorly matches the C I*/C_tot ratio and C+ cooling rate; (2)')
    P('    "High phi_PAH" gives temperatures and C I/C II ratios higher')
    P('    than observed; (3) "Low PAH" -- Table 4\'s "Low n_PAH/n" -- gives')
    P('    low C I*/C_tot ratios and C+ cooling rate; (4) "Low G0" gives')
    P('    low C I*/C_tot and high C I/C II.  Separately, at')
    P('    ms.tex:2619-2621, only "High phi_PAH" and "Low G0" "can be')
    P('    safely ruled out by the required C I/C II ratio".')
    P('    SO THE MITIGATION IS STRONGER THAN ONE ROW.  The only variant')
    P('    Wolfire does not argue against is the standard one, and the')
    P('    standard one contains the measured median.  Two rows are ruled')
    P('    out in those words; two more, including the one that breaks the')
    P('    check, are called a worse fit on two independent diagnostics')
    P('    without being ruled out.  Print that distinction; do not')
    P('    flatten it, and do not write "ruled out" for "Low phi_PAH".')
    ra = [p_med/r[4] for r in W03_TABLE4]
    P('    One number IS stable across all five variants: the measured')
    P(f'    median exceeds every predicted AVERAGE pressure, from {min(ra):.3f}')
    P(f'    times the "High phi_PAH" value to {max(ra):.3f} times the "Low')
    P('    phi_PAH" one.  The measurement runs high against the central')
    P('    model value whatever the parameters; only the WINDOW verdict')
    P('    moves.')
    P('    NOTE ON WOLFIRE\'S OWN WORD.  At ms.tex:1638-1660 they call the')
    P('    phases "very robust against variations in the PAH physical and')
    P('    chemical characteristics", in the same paragraph as their own')
    P('    "P_max decreases by ~35%" for phi_PAH = 0.25.  Print the 35 per')
    P('    cent and the five rows.  Do not print the adjective.')
    P('    AND ASK THE SAME OF THE REFUTATION, which rests on P_min.')
    P('    Only the FITTED fraction can be re-evaluated at another P_min;')
    P('    the measured 29% is tied to 1960 K cm^-3, the value Jenkins &')
    P('    Tripp themselves quote, and cannot be moved without their data.')
    for lab, phi, pmn, pmx, pav, how in W03_TABLE4:
        P(f'      {lab:<14} P_min = {pmn:>6.0f}: fitted lognormal below it '
          f'= {100*jt11_fraction(0.0, pmn):.1f}%')
    fr = [jt11_fraction(0.0, r[2]) for r in W03_TABLE4]
    P(f'    The fitted fraction runs {100*min(fr):.1f} to {100*max(fr):.1f} per cent across all')
    P(f'    {len(W03_TABLE4)} variants, against the 0 per cent a static two-phase medium')
    P('    allows.  STATE THE LIMIT WITH IT.  Only the fit-against-static')
    P('    half of the refutation was re-evaluated here.  The measured')
    P('    excess over the fit, 29% against 5.0%, exists only at the')
    P('    standard P_min, because 29% is Jenkins & Tripp\'s own reading')
    P('    at 1960 K cm^-3.')
    P('    AND ONE MORE LIMIT.  Jenkins & Tripp say their lognormal')
    P('    understates the observed material outside')
    n_ex = sum(1 for r in W03_TABLE4 if r[2] < 10**3.2)
    P(f'    3.2 < log(p/k) < 4.0, that is below {10**3.2:.0f} K cm^-3.  {n_ex} of the')
    P(f'    {len(W03_TABLE4)} variants have P_min below that:')
    for lab, phi, pmn, pmx, pav, how in W03_TABLE4:
        if pmn < 10**3.2:
            P(f'      {lab:<14} P_min = {pmn:>6.0f}: the {100*jt11_fraction(0.0, pmn):.1f}% is an '
              f'EXTRAPOLATION')
    P('    of a fit its own authors say runs low there, so the true')
    P('    fraction is larger.  The direction favours the refutation, but')
    P('    label those rows extrapolated.')
    P('    So: the fitted fraction exceeds the static 0 per cent in every')
    P('    variant; the CONFIRMATION fails in one.  Report both, in that')
    P('    order.')
    P('')
    f_in = jt11_fraction(W03_PMIN, W03_PMAX)
    f_below = jt11_fraction(None, W03_PMIN)
    f_above = jt11_fraction(W03_PMAX, None)
    f_in_ki = jt11_fraction(tp['Pmin'], tp['Pmax'])
    P('  REFUTED.  The strict two-phase picture says a static CNM CANNOT')
    P('  exist below P_min.  It does.')
    P(f'    fraction of CNM mass inside the window, from their own fit  = '
      f'{100*f_in:.1f}%')
    P(f'    fraction BELOW P_min, from their own fit                    = '
      f'{100*f_below:.1f}%')
    P(f'    fraction ABOVE P_max, from their own fit                    = '
      f'{100*f_above:.1f}%')
    P(f'    fraction BELOW P_min, MEASURED (their section 10.1.2)       = '
      f'{100*JT11_FRAC_BELOW_PMIN:.0f}%')
    P(f'    PUNCHLINE excess over the fitted lognormal  = '
      f'{JT11_FRAC_BELOW_PMIN/f_below:.1f} times')
    P(f'    low-starlight subsample, measured below P_min               = '
      f'{100*JT11_FRAC_BELOW_LOWI:.0f}%')
    P(f'    fraction at log(p/k) > {JT11_LOGP_EXTREME}, measured               '
      f'            = {100*JT11_FRAC_EXTREME:.3f}%')
    P('    Read the three numbers in order.  A static two-phase medium')
    P(f'    allows 0% below P_min.  The fitted lognormal already gives '
      f'{100*f_below:.1f}%.')
    P(f'    The measurement gives {100*JT11_FRAC_BELOW_PMIN:.0f}%.  The '
      f'prediction fails twice over: the')
    P('    fit itself violates it, and the data violate the fit by a')
    P(f'    further factor of {JT11_FRAC_BELOW_PMIN/f_below:.1f}.  Jenkins & Tripp state the excess')
    P(f'    tails explicitly, for log(p/k) < {JT11_FIT_LO} and > {JT11_FIT_HI}.')
    P('    Note carefully what is NOT refuted.  Gas ABOVE P_max is allowed:')
    P('    only the WARM phase is forbidden there, and this survey measures')
    P(f'    the cold phase, so the {100*f_above:.0f}% above P_max is not a violation of')
    P('    anything and is not counted.  The refutation rests on the low')
    P('    side alone, where a static CNM is genuinely impossible.')
    P('')
    P('    WHAT FAILS, precisely: the word STATIC, not the criterion.')
    P('    Jenkins & Tripp offer two readings, and their own preference is')
    P('    the second: either the Wolfire curve does not apply to the gas')
    P('    they see, or "rarefactions caused by turbulence create momentary')
    P('    excursions below the curve".  Their dispersion of')
    P(f'    {JT11_LOGP_SIG} dex is itself read as turbulence of Mach '
      f'{JT11_MACH_LO:.0f}-{JT11_MACH_HI:.0f}.')
    P('    So the thermal-equilibrium curve is an attractor that the gas is')
    P('    pushed off faster than it relaxes back.  PROBLEM 8 makes that')
    P('    quantitative by comparing the cooling time with the crossing')
    P('    time of a turbulent eddy.')
    P('')
    P('  THE SAME FAILURE SEEN FROM THE WARM SIDE.')
    P(f'    Heiles & Troland (2003), 21-cm absorption, find at least '
      f'{100*HT03_F_UNSTABLE:.0f}% of')
    P(f'    the WNM by mass at {HT03_T_UNST_LO:.0f}-{HT03_T_UNST_HI:.0f} K, '
      f'inside the thermally unstable')
    P('    band.  A strict two-phase medium allows only the small fraction')
    P('    in transit between phases.  Their section 9.2.1 makes the point')
    P('    against the McKee-Ostriker model directly.  Their other')
    P(f'    numbers: WNM is {100*HT03_F_WNM:.0f}% of the H I column at |b| > 10 deg;')
    P(f'    the CNM spin-temperature histogram peaks at {HT03_TS_PEAK:.0f} K with a')
    P(f'    column-weighted median of {HT03_TS_MEDIAN:.0f} K.')
    P(f'    Compare the model: Wolfire et al. give a CNM temperature of')
    P(f'    {W03_T_CNM_AVE:.0f} K at P_ave, a ratio of '
      f'{W03_T_CNM_AVE/HT03_TS_MEDIAN:.2f} to the measured median.')
    P('    The mean state is right; the spread around it is not there.')
    P('')
    P(f'  (For reference, against the KI02-fit window [{tp["Pmin"]:.0f}, '
      f'{tp["Pmax"]:.0f}] the same')
    P(f'  lognormal puts {100*f_in_ki:.1f}% of the mass inside.)')

    # ---------------------------------------------------------------- H
    P('')
    P('PART H.  NUMBERS FOR THE PROBLEM SET')
    P('-'*74)

    P('')
    P('  PROBLEM 1.  Is the Earth\'s troposphere convective?')
    lapse_dry = g_earth/(gamma_air*kB/((gamma_air-1.0)*mu_air*mu_u))
    # grad of the ISA, from the polytropic relation T ~ P^(1/(n+1))
    n_isa = mu_air*mu_u*g_earth/(kB*ISA_LAPSE) - 1.0
    grad_isa = 1.0/(n_isa + 1.0)
    P(f'    ISA lapse rate (definitional)     = {ISA_LAPSE*1e5:.2f} K/km')
    P(f'    dry adiabatic lapse g/c_p         = {lapse_dry*1e5:.3f} K/km')
    P(f'    ratio                             = {ISA_LAPSE/lapse_dry:.4f}')
    P(f'    implied polytropic index n        = {n_isa:.4f}')
    P(f'    grad = 1/(n+1)                    = {grad_isa:.5f}')
    P(f'    grad_ad = 2/7                     = {ga_di:.5f}')
    P(f'    grad/grad_ad                      = {grad_isa/ga_di:.4f}')
    P('    grad < grad_ad, so the standard troposphere is STABLE by')
    P('    Schwarzschild, by a margin of 33%.  Yet it convects daily.  The')
    P('    resolution is latent heat: a saturated parcel releases about')
    P('    2.5e10 erg/g on condensation, which warms it as it rises and')
    P('    makes its effective lapse rate about 5-6 K/km, below the')
    P('    ambient 6.5.  Moist convection is unstable where dry convection')
    P('    is not.  The Sun has no such term, which is why the solar')
    P('    criterion is the clean one.')

    P('')
    P('  PROBLEM 2.  The buoyancy frequency of the Earth\'s stratosphere.')
    cp_air = gamma_air*kB/((gamma_air-1.0)*mu_air*mu_u)
    N2_strat = g_earth*g_earth/(cp_air*ISA_T_TROP)
    N_strat = np.sqrt(N2_strat)
    N2_trop = (g_earth/ISA_T0)*(-ISA_LAPSE + g_earth/cp_air)
    P(f'    c_p of dry air                    = {cp_air:.4e} erg/(g K) '
      f'= {cp_air/1e4:.1f} J/(kg K)')
    P('    For a plane-parallel ideal-gas atmosphere,')
    P('      N^2 = (g/T)(dT/dz + g/c_p).')
    P(f'    Isothermal lower stratosphere at T = {ISA_T_TROP:.2f} K, dT/dz = 0:')
    P(f'      N^2                             = {N2_strat:.4e} s^-2')
    P(f'      N                               = {N_strat:.5f} rad/s')
    P(f'      period 2 pi/N                   = {2.0*np.pi/N_strat/60.0:.2f} min')
    P(f'    Troposphere at the ISA lapse rate:')
    P(f'      N^2                             = {N2_trop:.4e} s^-2')
    P(f'      N                               = {np.sqrt(N2_trop):.5f} rad/s')
    P(f'      period                          = '
      f'{2.0*np.pi/np.sqrt(N2_trop)/60.0:.2f} min')
    P('    Both are positive, both are of order ten minutes, and both are')
    P('    the periods of the lee waves that make wave clouds downwind of')
    P('    a mountain ridge.')

    P('')
    P('  PROBLEM 3.  Cooling time against sound crossing in a cluster.')
    T_icm, n_icm, mu_icm = 1.0e8, 1.0e-3, 0.6
    lam_brems = 2.1e-27*np.sqrt(T_icm)
    # n_e = 1.2 n_H, n_tot = 2.3 n_H for a fully ionised cosmic mix
    n_H = n_icm
    n_e, n_tot = 1.2*n_H, 2.3*n_H
    u_th = 1.5*n_tot*kB*T_icm
    rate = n_e*n_H*lam_brems
    t_cool = u_th/rate
    cs_icm = np.sqrt(5.0/3.0*kB*T_icm/(mu_icm*mu_u))
    R_cl = 1e3*kpc
    t_sound = R_cl/cs_icm
    kap = spitzer_kappa(T_icm)
    lam_F = np.sqrt(kap*T_icm/(n_e*n_H*lam_brems))
    P(f'    T = {T_icm:.0e} K, n_H = {n_icm:.0e} cm^-3, mu = {mu_icm}')
    P(f'    Lambda = 2.1e-27 sqrt(T)          = {lam_brems:.4e} erg cm^3/s')
    P(f'    thermal energy (3/2) n_tot k T    = {u_th:.4e} erg/cm^3')
    P(f'    radiated power n_e n_H Lambda     = {rate:.4e} erg/cm^3/s')
    P(f'    t_cool                            = {t_cool:.4e} s '
      f'= {t_cool/yr/1e9:.2f} Gyr')
    P(f'    sound speed                       = {cs_icm/1e5:.0f} km/s')
    P(f'    t_sound across 1 Mpc              = {t_sound:.4e} s '
      f'= {t_sound/yr/1e9:.3f} Gyr')
    P(f'    PUNCHLINE t_cool/t_sound          = {t_cool/t_sound:.1f}')
    P(f'    Spitzer kappa at 1e8 K, ln L = {LN_LAMBDA_ICM}  = {kap:.4e} '
      f'erg/(s cm K)')
    P(f'    Field length sqrt(kappa T/(n_e n_H Lambda)) = {lam_F/kpc:.0f} kpc')
    P(f'    ratio to the cluster radius       = {lam_F/R_cl:.2f}')
    P('    The Field length exceeds the cluster.  Conduction smooths any')
    P('    thermally unstable mode before it can grow, and the cooling')
    P(f'    time is {t_cool/t_sound:.0f} times the crossing time anyway.  A cluster at')
    P('    this density is thermally stable on both counts.')
    P('    Now the cooling-flow core, and watch the scalings.  At fixed T,')
    P('    t_cool ~ 1/n and lambda_F ~ 1/n, so BOTH shrink together and the')
    P('    ratio lambda_F/(c_s t_cool) does not change with density at all.')
    P('    What changes is the size of the region:')
    for nn, TT, RR, lab in ((1.0e-3, 1.0e8, 1e3*kpc, 'outskirts, 1 Mpc'),
                            (1.0e-2, 3.0e7, 50.0*kpc, 'cool core, 50 kpc')):
        lam2 = 2.1e-27*np.sqrt(TT)
        ne2, nt2 = 1.2*nn, 2.3*nn
        tc2 = 1.5*nt2*kB*TT/(ne2*nn*lam2)
        cs2 = np.sqrt(5.0/3.0*kB*TT/(mu_icm*mu_u))
        lF2 = np.sqrt(spitzer_kappa(TT)*TT/(ne2*nn*lam2))
        P(f'      {lab:<18} n_H = {nn:.0e}, T = {TT:.0e} K:')
        P(f'        t_cool = {tc2/yr/1e9:7.2f} Gyr   '
          f'lambda_F = {lF2/kpc:8.1f} kpc   '
          f'lambda_F/R = {lF2/RR:6.2f}   '
          f't_cool/t_sound = {tc2/(RR/cs2):6.1f}')
    P('    The core cools in about a Gyr, comfortably inside a Hubble time,')
    P('    and its Field length is a sizeable fraction of its radius rather')
    P('    than several times it.  Thermal instability is a cool-core')
    P('    phenomenon, and the reason is geometry, not a change in the')
    P('    microphysics.')

    P('')
    P('  PROBLEM 4.  Ledoux against Schwarzschild in a helium gradient.')
    grad_test = 0.45
    for dmu in (0.0, 0.02, 0.05, 0.10):
        stable_s = grad_test < ga_mono
        term = ga_mono - grad_test + dmu
        P(f'    grad = {grad_test}, grad_mu = {dmu:.2f}: '
          f'Schwarzschild says {"stable" if stable_s else "UNSTABLE"}, '
          f'Ledoux term {term:+.3f} -> '
          f'{"stable" if term > 0 else "UNSTABLE"}')
    dmu_crit = grad_test - ga_mono
    P(f'    The composition gradient that just holds this layer together is')
    P(f'    grad_mu = grad - grad_ad          = {dmu_crit:.3f}')
    P('    A layer with Schwarzschild-unstable temperature structure but a')
    P('    stabilising mu gradient is SEMICONVECTIVE: it mixes slowly on a')
    P('    thermal, not a dynamical, timescale.')
    P('    The Sun does not show this, and the reason is NOT that its')
    P('    grad_mu is small everywhere -- at 0.10 R it reaches')
    P(f'    {st["grad_mu"][int(np.argmin(abs(r-0.10)))]:.3f}, seven times the {dmu_crit:.3f} needed above.  It is that')
    P('    the Sun\'s large grad_mu and its near-neutral layer are in')
    P('    different places.  Where grad_mu is large (inside 0.2 R),')
    P(f'    grad_ad - grad is about {ga_mono - st["grad"][int(np.argmin(abs(r-0.15)))]:.2f}, so the layer is stable by a')
    P('    wide margin with or without Ledoux.  Where the criterion is')
    P(f'    delicate (0.72-0.75 R), |grad_mu| <= '
      f'{np.nanmax(np.abs(st["grad_mu"][(r>0.72)&(r<0.75)])):.4f}.  A star with a')
    P('    receding convective core puts the two in the SAME place, and')
    P('    then the choice of criterion changes the star\'s lifetime.')

    P('')
    P('  PROBLEM 5.  Where the hydrogen ionisation zone sits in the Sun.')
    P(f'    grad_ad minimum at photospheric pressure = {gag[j]:.5f} '
      f'at T = {Tg[j]:.0f} K')
    for PP in (1e4, 1e5, 1.2e5, 1e6, 1e7):
        gg = np.array([grad_ad_ionising(t, PP)[0] for t in Tg])
        jj = int(np.argmin(gg))
        P(f'    P = {PP:.1e} dyn/cm^2: min grad_ad = {gg[jj]:.5f} '
          f'at T = {Tg[jj]:.0f} K')
    P('    The zone moves to higher temperature as the pressure rises,')
    P('    because Saha equilibrium needs a hotter gas to ionise a denser')
    P('    one.  That is why the base of the solar convection zone is deep:')
    P('    the ionisation zone is not a surface skin.')

    P('')
    P('  PROBLEM 6.  Convective turnover deep in the solar envelope.')
    for x in (0.75, 0.85, 0.90, 0.95):
        d = rows[x]
        P(f'    r = {d["rfrac"]:.3f} R: l = {d["l"]:.3e} cm = '
          f'{d["l"]/1e5:.0f} km, v_c = {d["v"]/1e5:.3f} km/s, '
          f'l/v_c = {d["tau"]/86400.0:.2f} d')
    d983 = rows[0.9831]
    P(f'    r = {d983["rfrac"]:.4f} R (last tabulated row): l = '
      f'{d983["l"]/1e5:.0f} km, v_c = {d983["v"]/1e5:.3f} km/s, '
      f'l/v_c = {d983["tau"]/3600.0:.2f} h')
    P(f'    photosphere (tau = 2/3): l = {ph["l"]/1e5:.0f} km, '
      f'v_c = {ph["v"]/1e5:.2f} km/s, l/v_c = {ph["tau"]/60.0:.2f} min')
    P(f'    The turnover time runs from {rows[0.75]["tau"]/86400.0:.0f} days at the base of the')
    P(f'    zone to {d983["tau"]/3600.0:.1f} hours at the last tabulated row and '
      f'{ph["tau"]/60.0:.1f} minutes at')
    P(f'    the photosphere, a factor {rows[0.75]["tau"]/ph["tau"]:.0e} between the two ends.')
    P('    That range is the dynamo\'s problem: the same fluid carries')
    P('    eddies whose turnover times differ by four orders of magnitude,')
    P('    and no single mixing length describes both.')

    P('')
    P('  PROBLEM 7.  The unstable band in the ISM, in three variables.')
    P(f'    temperature   {tp["T_pmin"]:.1f} K to {tp["T_pmax"]:.1f} K   '
      f'(factor {tp["T_pmax"]/tp["T_pmin"]:.1f})')
    P(f'    density       {tp["n_pmax"]:.3f} to {tp["n_pmin"]:.3f} cm^-3  '
      f'(factor {tp["n_pmin"]/tp["n_pmax"]:.1f})')
    P(f'    pressure      {tp["Pmin"]:.0f} to {tp["Pmax"]:.0f} K cm^-3  '
      f'(factor {tp["Pmax"]/tp["Pmin"]:.2f})')
    P('    Note the asymmetry: the pressure window is narrow, a factor of')
    P('    three, while the density contrast across it is a factor of')
    P(f'    {tp["n_pmin"]/tp["n_pmax"]:.0f}.  That is what makes the two-phase medium a USEFUL')
    P('    measurement: a pressure measured anywhere in the cold gas pins')
    P('    the state to within a factor of three, which is why Jenkins &')
    P('    Tripp\'s survey is worth doing.')

    P('')
    P('  PROBLEM 8.  How far off the equilibrium curve can turbulence hold')
    P('              the gas?  The cooling length.')
    P('    Both phases are taken on the equilibrium curve at the states')
    P('    Heiles & Troland and Wolfire et al. actually report: T = 70 K')
    P('    for the CNM (their column-weighted median spin temperature) and')
    P('    T = 6000 K for the WNM (a point on the warm branch near P_max).')
    lam_cool = {}
    for TT, lab in ((HT03_TS_MEDIAN, 'CNM'), (6000.0, 'WNM')):
        n_e_ism, _ = ki_equilibrium(TT)
        u = 1.5*n_e_ism*kB*TT
        tc = u/(n_e_ism*n_e_ism*ki_lambda(TT))
        cs_ism = np.sqrt(5.0/3.0*kB*TT/(1.27*mu_u))
        lF = field_length(TT, n_e_ism)
        lam_cool[lab] = cs_ism*tc
        P(f'    {lab}: T = {TT:.0f} K, n_eq = {n_e_ism:.3f} cm^-3, '
          f'P/k = {n_e_ism*TT:.0f} K cm^-3')
        P(f'      t_cool = (3/2) n k T/(n^2 Lambda) = {tc:.3e} s = '
          f'{tc/Myr:.3f} Myr')
        P(f'      sound speed                     = {cs_ism/1e5:.3f} km/s')
        P(f'      COOLING LENGTH c_s t_cool       = {cs_ism*tc/pc:.2f} pc')
        P(f'      Field length                    = {lF/pc:.5f} pc = '
          f'{lF/AU:.0f} au')
    P('    Read the two cooling lengths.  A disturbance smaller than')
    P('    c_s t_cool is erased by cooling before it can travel across')
    P('    itself; a disturbance larger than c_s t_cool outruns the')
    P('    cooling and carries the gas off the curve.')
    P(f'      CNM: {lam_cool["CNM"]/pc:.3f} pc.  Cold gas relaxes back onto the curve almost')
    P('      instantly on any scale a survey resolves.')
    P(f'      WNM: {lam_cool["WNM"]/pc:.0f} pc.  That is the size of a whole molecular')
    P('      cloud.  Turbulence driven on tens of parsecs can therefore hold')
    P('      warm gas off the curve over a large part of its volume.')
    P(f'    PUNCHLINE the two cooling lengths differ by a factor '
      f'{lam_cool["WNM"]/lam_cool["CNM"]:.0f}.  That')
    P('    asymmetry is the mechanism behind the two measured numbers in')
    P(f'    PART G: {100*HT03_F_UNSTABLE:.0f}% of the WARM gas is off the curve (Heiles &')
    P(f'    Troland), while only {100*JT11_FRAC_BELOW_PMIN:.0f}% of the COLD gas is (Jenkins &')
    P('    Tripp), and the cold excursions are transient rarefactions')
    P('    rather than a sustained state.')
    P('    The Field length sets, separately, the resolution a simulation')
    P('    needs.  Koyama & Inutsuka (2002) used 140 au cells for exactly')
    P('    this reason, on a 2048 x 512 grid over 1.44 x 0.36 pc.')

    P('')
    P('  PROBLEM 9.  How superadiabatic is the surface, really?')
    for a in (1.0, 1.5, 2.0, 3.0):
        q = mlt_photosphere(a)
        P(f'    alpha = {a:.1f}: grad-grad_ad = {q["excess"]:.4f}, '
          f'v_c = {q["v"]/1e5:.2f} km/s, v_c/c_s = {q["v"]/q["cs"]:.3f}, '
          f'l = {q["l"]/1e5:.0f} km')
    P('    Changing alpha by a factor of 3 changes the predicted velocity')
    P(f'    by only {mlt_photosphere(3.0)["v"]/mlt_photosphere(1.0)["v"]:.2f}, '
      f'because F ~ alpha^2 (grad-grad_ad)^(3/2) and')
    P('    v_c ~ alpha (grad-grad_ad)^(1/2), so at fixed F the velocity')
    P('    scales only as alpha^(1/3).  The disagreement in PART D cannot')
    P('    be tuned away with alpha.')


    P('')
    P('=' * 74)
    P('SOURCES')
    P('=' * 74)
    P('  Field, G. B. (1965), ApJ 142, 531, "Thermal Instability".')
    P('    Page 532, equations (1)-(4b), read from the scanned article.')
    P('    L(rho,T) is "energy losses minus energy gains, per gram of')
    P('    material per second exclusive of thermal conduction".')
    P('    (4a) (dL/dT)_rho < 0, isochoric;')
    P('    (4b) (dL/dT)_P = (dL/dT)_rho - (rho_0/T_0)(dL/drho)_T < 0,')
    P('         isobaric, and Field states that condensations are governed')
    P('         by (4b), not by Parker\'s (4a).')
    P('    Note: the form (d(L/T)/dT)_P < 0 that appears in some later')
    P('    texts coincides with (4b) only on the equilibrium curve, where')
    P('    L = 0.  This module uses (4b) as printed.')
    P('    https://articles.adsabs.harvard.edu/pdf/1965ApJ...142..531F')
    P('  Wolfire, M. G., McKee, C. F., Hollenbach, D. & Tielens, A. G. G. M.')
    P('    (2003), ApJ 587, 278-311, "Neutral Atomic Phases of the ISM in')
    P('    the Galaxy".  arXiv:astro-ph/0207098.  Table 3, row R = 8.5 kpc,')
    P('    N_cl = 1e19 cm^-2: P_min/k = 1960, P_max/k = 4810,')
    P('    P_th,ave/k = 3070 K cm^-3; WNM T from 8310 to 5040 K, n from')
    P('    0.209 to 0.860 cm^-3; CNM T from 258 to 61.6 K, n from 6.91 to')
    P('    71.0 cm^-3; CNM T_ave = 85.0 K, n_ave = 32.9 cm^-3.  The same')
    P('    three pressures appear in their section 8.1 as the standard')
    P('    parameter set.  Their eq. (43): P_min = 1.1e4 exp(-R/4.9 kpc);')
    P('    eq. (44): P_th,ave/k = 1.4e4 exp(-R/5.5 kpc) K cm^-3.')
    P('  Jenkins, E. B. & Tripp, T. M. (2011), ApJ 734, 65-86, "The')
    P('    Distribution of Thermal Pressures in the Diffuse, Cold Neutral')
    P('    Medium of our Galaxy. II."  arXiv:1104.2323.  Abstract and')
    P('    eq. (3): mass-weighted lognormal, mean log(p/k) = 3.58, rms')
    P('    dispersion at least 0.175 dex, normalisation 2.30e23 cm^-2 per')
    P('    dex; outside 3.2 < log(p/k) < 4.0 the fit understates the')
    P('    observed material.  Section 10.1.2: "A substantial fraction of')
    P('    the material (29%) ... is detected at pressures below those')
    P('    permissible for a static CNM, (p/k)_min = 1960 cm^-3 K, as')
    P('    defined by the standard model ... presented by Wolfire et al.')
    P('    (2003)", and they read it as turbulent rarefaction.  Abstract:')
    P('    23% for the low-intensity subsample; ~0.05% above log(p/k)=5.5;')
    P('    turbulent Mach number 1 < M < 4.')
    P('  Heiles, C. & Troland, T. H. (2003), ApJ 586, 1067-1093, "The')
    P('    Millennium Arecibo 21-cm Absorption Line Survey. II."')
    P('    arXiv:astro-ph/0207105.  Sections 2.3.2 and 9.2.1 and the')
    P('    abstract: at least 48% of the WNM by column density lies in the')
    P('    thermally unstable range 500-5000 K; 61% of H I is WNM at')
    P('    |b| > 10 deg; the CNM spin-temperature histogram peaks at 40 K')
    P('    with a column-weighted median of 70 K.')
    P('  Koyama, H. & Inutsuka, S. (2002), ApJ 564, L97, "An Origin of')
    P('    Supersonic Motions in Interstellar Clouds".  arXiv:astro-ph/')
    P('    0112420.  Equations (4) and (5): the analytic cooling fit and')
    P('    Gamma = 2e-26 erg/s.  AS PRINTED, eq. (4) has two typographical')
    P('    errors.  The corrected form is used here.')
    P('  Vazquez-Semadeni, E., Gomez, G. C., Jappsen, A. K.,')
    P('    Ballesteros-Paredes, J., Gonzalez, R. F. & Klessen, R. S. (2007),')
    P('    ApJ 657, 870-883, "Molecular Cloud Evolution II".')
    P('    arXiv:astro-ph/0608375.  Their equations (3) and (4) print the')
    P('    corrected Koyama-Inutsuka function, and footnote 5 reads: "Note')
    P('    that eq. (4) in Koyama & Inutsuka (2002) contains two')
    P('    typographical errors.  The form used here incorporates the')
    P('    necesary corrections, kindly provided by H. Koyama."')
    P('  Oba, T., Iida, Y. & Shimizu, T. (2017), ApJ 836, 40, "Height-')
    P('    dependent velocity structure of photospheric convection in')
    P('    granules and intergranular lanes with Hinode/SOT".')
    P('    arXiv:1612.06175.  Abstract and section 4.4: upward speed falls')
    P('    from 0.65 to 0.40 km/s with height, downward speed rises from')
    P('    0.30 to 0.50 km/s with depth; rms filtered convective velocity')
    P('    0.6 km/s at I/I0 = 0.75 to 0.3 km/s at I/I0 = 0.40; stated')
    P('    velocity error 0.18 km/s.  Their Table 1 puts I/I0 = 0.75 at')
    P('    h = 40 km, tau_500 = 0.55 and I/I0 = 0.40 at h = 163 km,')
    P('    tau_500 = 0.10.')
    P('  Abramenko, V. I., Yurchyshyn, V. B., Goode, P. R., Kitiashvili,')
    P('    I. N. & Kosovichev, A. G. (2012), ApJ 756, L27, "Detection of')
    P('    Small-Scale Granular Structures in the Quiet Sun with the New')
    P('    Solar Telescope".  arXiv:1208.4337.  Their section 3: the')
    P('    regular granules are Gaussian with d0 = 1050 +/- 22 km and')
    P('    sigma = 480 +/- 11 km; the mini-granules below 600 km are a')
    P('    power law of index -1.82 +/- 0.12; the area-contribution')
    P('    function gives a dominant scale of 1080-1300 km.')
    P('  Bahcall, J. N., Serenelli, A. M. & Basu, S. (2005), ApJ 621,')
    P('    L85-L88.  The tabulated model BS2005-AGS,OP at')
    P('    afd/data/bs05_agsop.dat, used here only as a stratification.')
    P('  Kippenhahn, R. & Weigert, A. (1990), "Stellar Structure and')
    P('    Evolution", sections 6.1, 7.2 and 14.3: the Schwarzschild and')
    P('    Ledoux criteria, the mixing-length flux and velocity in the')
    P('    efficient limit, and grad_ad for a partially ionised gas.')
    P('  Electron conductivity kappa = 1.84e-5 T^(5/2)/ln Lambda, read')
    P('    from Sarazin (1988) eq. (5.37), which attributes it to Spitzer,')
    P('    "Physics of Fully Ionized Gases" (1956).  The book was not')
    P('    opened here; 1956 and 1962 are its first and second editions.')
    P('  Parker, E. N. (1953): neutral-gas conductivity K = 2.5e3 T^(1/2),')
    P('    as adopted by Koyama & Inutsuka (2002) below their eq. (3).')
    P('  Sarazin, C. L. (1988), section 5.4: ln Lambda = 37.8 for the ICM,')
    P('    carried over from Module 1.')
    P('  ISO 2533:1975 / US Standard Atmosphere 1976; IAU 2015 Res. B3.')


if __name__ == '__main__':
    main()
