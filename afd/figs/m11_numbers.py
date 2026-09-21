"""Module 11 numbers: accretion discs.  Keplerian shear and the Rayleigh
criterion, the timescale gap that molecular viscosity cannot close, the
Shakura-Sunyaev alpha prescription, vertical structure and the thin-disc
condition, the steady disc and its temperature profile, the radiative
efficiency, the Toomre criterion, centrifugal support, and the link to
the magnetorotational instability that Module 12 already derived.

Every physical number quoted in module11.html is produced here, so the prose
can be checked against a run rather than against memory.
Units: CGS-Gaussian throughout (cm, g, s, erg, K, statcoulomb, gauss).

STEP 1 OF SIX.  NO CONSTANT IN THIS FILE IS VERIFIED YET.  Every published
value carries the tag NOT YET VERIFIED and the paper it must be read from.
Step 2 fetches those papers, reads the page, and replaces the tag.  Nothing
here may be quoted in prose until it does.

WHAT THIS MODULE OWES, AND TO WHOM.  The eighteen debts eleven shipped pages
have already printed against Module 11 are listed, each with the file and
line it was read from, in .ignore/m11-promises.md.  The four that drive the
design:

  module12.html:700   Module 12 SS9 already prints the problem in one line.
                      A Keplerian disc has Omega ~ R^-3/2, so its specific
                      angular momentum ell = Omega R^2 ~ R^1/2 INCREASES
                      outward, the Rayleigh criterion calls that stable, and
                      a stable disc does not accrete.  PART B derives it.
  module12.html:782   The Keplerian q = 3/2 is ASSUMED there and not
                      derived.  PART B derives it from a point mass.
  module12.html:940   A shipped page has already fixed this module's alpha
                      as the disc viscosity parameter.  Not a Gate D choice.
  module09.html:757   A shipped REFUTED verdict rests on "a geometrically
                      thin accretion disc radiates with eta_rad ~ 0.1",
                      which Module 9 asserts and does not derive.  PART G
                      derives it and says what happens to Module 9's factor.

THE FOUR CHECKS, WITH THE VERDICTS NOT YET FIXED -- Gate D fixes them.

  CHECK 1  THE TIMESCALE GAP.  REFUTES molecular viscosity, and it is the
           reason the rest of the module exists.  index.html:78 has already
           promised this number in print: "the timescale gap that forces
           it".  Module 1 SS6 supplies the transport coefficients, which
           module01.html:623 says in print is what Module 11 needs them for.

  CHECK 2  THE TEMPERATURE PROFILE, T_eff ~ R^-3/4.  STEP 2 REPLACED THE
           CHECK THAT STOOD HERE.  Step 1 proposed inferring alpha from a
           dwarf-nova outburst timescale and comparing it to King, Pringle
           & Livio's range.  Reading their section 2.1 killed it: their own
           eq. (2) is t_visc ~ R^2/nu, the SAME relation, so the comparison
           tests arithmetic and not physics.  The arithmetic is kept in
           PART D and is labelled in print as not a check.
           What replaces it is viscosity-INDEPENDENT: the exponent -3/4
           follows from energy conservation alone, with nu, alpha and Sigma
           all cancelled, and their section 1 says it "is in reasonable
           accord with both continuum spectra and eclipse mapping of
           cataclysmic variables".  THE OBSERVATIONAL SIDE HAS NO ERROR
           BAR in that review, so this confirms a shape and not a digit.

  CHECK 3  THE RADIATIVE EFFICIENCY.  Three numbers, not one: the Newtonian
           thin disc at the Schwarzschild innermost stable circular orbit
           gives exactly 1/12; the relativistic Schwarzschild value is
           1 - sqrt(8/9); and the Soltan-argument mean over the quasar
           population is near 0.1.  Module 9's 0.1 sits above both zero-spin
           values, which is a statement about spin.

  CHECK 4  ALPHA IS NOT A CONSTANT OF NATURE.  REFUTES the prescription read
           as a law.  Two gaps, both from ONE review: a factor 10 to 40
           between fully-ionised and protostellar discs, and AT LEAST a
           factor 5 between what observations of ionised discs need and
           what MHD simulations of the Module 12 SS9 instability produce.
           King, Pringle & Livio's title asks exactly this question.

A NOTATION WARNING, FROM .ignore/m11-promises.md.  The glyph ell already
carries three meanings in this book: Module 6's mixing length alpha H,
Module 10's separation inside the inertial range, and -- undeclared in any
notation table -- the specific angular momentum Omega R^2 at
module12.html:700.  In THIS file ell is the specific angular momentum and
nothing else.  The mixing length does not occur here.
"""

import numpy as np

# --- constants (CODATA 2018 / IAU 2015 nominal), CGS-Gaussian -------------
# Copied verbatim from m12_numbers.py rather than imported, so that each
# module's numbers script reads on its own.
kB = 1.380649e-16       # erg/K          (exact, SI definition)
e = 4.80320471e-10      # esu            (elementary charge)
me = 9.1093837015e-28   # g
mp = 1.67262192369e-24  # g
mu_u = 1.66053906660e-24  # g            (unified atomic mass unit)
hbar = 1.054571817e-27  # erg s
c = 2.99792458e10       # cm/s
G = 6.67430e-8          # cm^3 g^-1 s^-2
sigma_SB = 5.670374419e-5   # erg cm^-2 s^-1 K^-4  (exact, SI definition)
sigma_T = 6.6524587321e-25  # cm^2      (Thomson cross-section)
pc = 3.0856775814913673e18   # cm
kpc = 1e3*pc
AU = 1.495978707e13     # cm
yr = 3.15576e7          # s
day = 86400.0           # s

GMsun = 1.3271244e26    # cm^3/s^2       (IAU 2015 nominal)
Rsun = 6.957e10         # cm             (IAU 2015 nominal)
Msun = GMsun/G          # g

# Module 1's inputs, reused unchanged so the modules cannot diverge.
SPITZER_C = 3.0**1.5/(4.0*np.sqrt(np.pi))   # = 0.7329, Sarazin eq. 5.32
MU_IONISED_H = 0.6      # mean molecular weight, fully ionised H + He
MU_MOLECULAR = 2.34     # mean molecular weight, H2 + He, protoplanetary
SIGMA_NEUTRAL = 1.0e-15    # cm^2, Module 1's order-of-magnitude
# neutral cross-section, copied from m12_numbers.py's SIGMA_H.
MU_H_ION = mp/mu_u      # = 1.00728, a proton measured against m_u.
# THE VISCOSITY CARRIER, not the mixture.  Module 1's convention, and
# Module 12's MU_H is the same quantity under the same name.

# =========================================================================
# PUBLISHED VALUES COMPARED AGAINST.  Each block names the paper, the table
# or equation, and what the quoted error means.  AT STEP 1 NOT ONE OF THEM
# HAS BEEN READ.  The tag is the instruction to step 2.
# =========================================================================

# --- Shakura & Sunyaev (1973), A&A 24, 337-355. -------------------------
# VERIFIED at step 2 from the ADS scan, bibcode 1973A&A....24..337S.  The
# scan has NO TEXT LAYER -- 398 characters, all of it the bibcode
# watermark -- so pages 338 and 339 were rendered at 190 dpi and read as
# images.  The ADS gateway returned 504 on the first request and worked
# on the second.
#
# STEP 1 DESCRIBED THEIR ALPHA WRONGLY.  It said "t_r,phi = alpha P, a
# stress proportional to the pressure".  That is the later standard
# restatement.  Their p. 338, right column, prints
#
#       alpha = v_t/v_s + H^2/(4 pi rho v_s^2)
#
# with, in the same sentence, rho v_s^2/2 = (3/2) rho kT/m_p + eps_r as
# "the thermal energy density of the matter", eps_r the radiation energy
# density, v_s the sound velocity and v_t the turbulent velocity.
#
# THREE CONSEQUENCES, ALL OF WHICH THIS MODULE MUST CARRY.
#  (1) Their alpha is a SUM of a turbulent Mach number and a
#      magnetic-to-thermal-energy ratio, not one stress coefficient.
#  (2) THEIR H IS THE MAGNETIC FIELD, in the old convention where H
#      denotes B.  This book's H is the scale height.  The two symbols
#      collide inside the founding paper of the subject, and the module
#      says so where it first writes nu = alpha c_T H.
#  (3) THEIR v_s IS NOT THIS BOOK'S c_T.  With radiation neglected their
#      own definition gives v_s^2 = 3kT/m_p, the rms thermal speed,
#      larger than c_T = sqrt(kT/(mu m_u)) by sqrt(3 mu m_u/m_p) = 1.34
#      at mu = 0.6.  Writing nu = alpha c_T H is a CONVENTION of this
#      book and alpha absorbs the factor.
#
# Their bound, same column: "In part II below we show that alpha <~ 1."
# The printed relation is <~ and not <=.
SS73_ALPHA_MAX = 1.0            # their bound, alpha <~ 1      VERIFIED
# Their footnote 3, p. 338: alpha "is assumed to be constant along the
# disk in our calculations", and "the observational appearance of the
# disk (spectrum of its radiation and the effective temperature of the
# surface) DO NOT STRONGLY DEPEND on the chosen value of alpha".  That
# footnote is CHECK 4's context: the founding paper says the easiest
# observable is the one least able to measure alpha.
#
# Their p. 339, left column, inside the parenthesis defining L_cr:
#   "(eta is the efficiency of gravitational energy release, in the case
#    of Schwarzschild's metric eta ~= 0.06, in a Kerr black hole eta can
#    attain 40%)"
# THE FOUNDING PAPER PRINTS BOTH ENDS OF CHECK 3's RANGE.
SS73_ETA_SCHWARZSCHILD = 0.06   # their p. 339                 VERIFIED
SS73_ETA_KERR_MAX = 0.40        # their p. 339, "40%"          VERIFIED
# Recorded from the same page and NOT used: L_cr = 1e38 (M/M_sun) erg/s
# and Mdot_cr = 3e-8 (0.06/eta)(M/M_sun) M_sun/yr.

# --- King, Pringle & Livio (2007), MNRAS 376, 1740-1746. ----------------
# VERIFIED at step 2 from arXiv:astro-ph/0701803, fetched and read with
# PyMuPDF.  Their abstract, verbatim:
#   "We consider observational and theoretical estimates of the accretion
#    disc viscosity parameter alpha.  We find that in THIN, FULLY-IONIZED
#    DISCS, the best observational evidence suggests a typical range
#    alpha ~ 0.1 - 0.4, whereas the relevant NUMERICAL SIMULATIONS tend to
#    derive estimates for alpha which are AN ORDER OF MAGNITUDE SMALLER.
#    We discuss possible reasons for this apparent discrepancy."
# STEP 1 LABELLED 0.1-0.4 "outburst, dwarf novae".  IT IS WIDER THAN THAT:
# "thin, fully-ionized discs".  Relabelled here.
KPL07_ALPHA_LO = 0.1            # thin fully-ionised discs     VERIFIED
KPL07_ALPHA_HI = 0.4            # thin fully-ionised discs     VERIFIED
# Their section 2.1, DWARF NOVAE SPECIFICALLY, which is a narrower
# figure than the abstract's and is the one CHECK 2's arithmetic meets:
# "All of these papers agree that alpha must lie in a fairly narrow
# range alpha ~= 0.1 - 0.3", citing Schreiber et al. (2003, 2004) on SS
# Cyg and VW Hyi, Cannizzo (2001a, 2001b) on VW Hyi, U Gem, SS Cyg and
# WZ Sge, and Buat-Menard et al. (2001) on Z Cam.
KPL07_DN_ALPHA_LO = 0.1         # their section 2.1            VERIFIED
KPL07_DN_ALPHA_HI = 0.3         # their section 2.1            VERIFIED
# STEP 2's FIRST PASS PICKED ITS OWN ENDPOINTS FOR THE SIMULATIONS,
# 0.004 to 0.02.  THE AUTHORS STATE THE RANGE THEMSELVES, in their
# section 5: "a large discrepancy between the values ... required to
# model observations of fully ionized, time-dependent accretion discs
# (Section 2: alpha ~ 0.1 - 0.4) and those which are generally obtained
# from numerical MHD simulations WITHOUT INCLUDING A SUPERIMPOSED
# MAGNETIC FIELD (Section 3: ALPHA <= 0.02)."
# IT IS A BOUND AND IT POINTS DOWN.  Their section 4 adds that the
# limitations of the simulations "would indeed tend to lead to
# UNDERESTIMATING the value of alpha", so the true simulated alpha may
# be larger and the gap smaller.  The module states the bound and the
# direction, and never a midpoint.
KPL07_SIM_MAX = 0.02            # their section 5, a BOUND     VERIFIED
# Their section 2.3.2: "Estimates for alpha in protostellar (T Tauri)
# discs, based on evolutionary lifetimes, are given by Hartmann et al.
# (1998).  They give estimates of alpha ~= 0.01 at disc radii
# R ~ 10 - 100 AU."  HARTMANN ET AL. WAS NOT READ; this module quotes it
# through the review and names the route in print.
# THIS MODULE'S CENSUS SITS AT 10 au, INSIDE THAT RANGE.
KPL07_ALPHA_PROTOSTELLAR = 0.01     # Hartmann et al. (1998)   VERIFIED
KPL07_PROTO_R_LO_AU = 10.0          # their stated range       VERIFIED
KPL07_PROTO_R_HI_AU = 100.0         # their stated range       VERIFIED
# STEP 1 INVENTED A CONSTANT.  It carried KPL07_ALPHA_QUIESCENT = 0.01
# as a "quiescent dwarf-nova" value.  The 0.01 in this paper is the
# PROTOSTELLAR value above, and the two are different physics.  Removed.
# Their section 2.3.1, Starling et al. (2004), AGN optical variability
# read through the thermal time: 0.01 <= alpha <= 0.03, and Starling et
# al. "note that these values of alpha are really LOWER LIMITS because
# data sampling means that they might miss shorter timescales".  A BOUND
# HAS A DIRECTION and this one points UP.  Recorded, not used in a check.
KPL07_AGN_ALPHA_LO = 0.01       # a lower limit, not a value   VERIFIED
KPL07_AGN_ALPHA_HI = 0.03       # a lower limit, not a value   VERIFIED
# Their section 1, and PART F's observational anchor: the radial run of
# effective temperature across a steady disc, T ~ R^-3/4, "is independent
# of the viscosity, being just a statement of energy conservation, and is
# in reasonable accord with both continuum spectra and eclipse mapping of
# cataclysmic variables".

# --- Yu & Tremaine (2002), MNRAS 335, 965-976. --------------------------
# VERIFIED at step 2 from arXiv:astro-ph/0203082, fetched and read with
# PyMuPDF.  IT IS NOT A MEASUREMENT WITH AN ERROR BAR.  Their abstract:
#   "The local BH mass density is CONSISTENT WITH the density accreted
#    during optically bright QSO phases IF QSOs have a mass-to-energy
#    conversion efficiency eps ~= 0.1."
# and further on, "luminous QSOs ... have a high efficiency (e.g.
# eps ~ 0.2, WHICH IS POSSIBLE FOR THIN-DISK ACCRETION ONTO A KERR BH)",
# and "less luminous QSOs must accrete with a low efficiency < 0.1".
# Their local density carries an h_0.65 scaling:
# rho_bh(z=0) = (2.5 +/- 0.4) x 10^5 h_0.65^2 M_sun Mpc^-3.
# CHECK 3 must say "the efficiency that makes the accounting close", not
# "the measured efficiency".
YT02_EFFICIENCY = 0.1           # closes the Soltan argument   VERIFIED
YT02_EFFICIENCY_KERR = 0.2      # their luminous-QSO case      VERIFIED

# --- Toomre (1964), ApJ 139, 1217-1238. ---------------------------------
# VERIFIED at step 2 from the ADS scan, bibcode 1964ApJ...139.1217T.
#
# THE PAPER DOES NOT CONTAIN THE CRITERION FOR A GAS DISC, AND STEP 1
# CITED IT FOR ONE.  His p. 1217: "it seemed a legitimate first
# approximation TO IGNORE THE INTERSTELLAR GAS AND DUST, and to
# concentrate here on the stability of a thin disk composed ONLY OF
# STARS.  A discussion of the gravitational stability of a thin layer of
# GASEOUS material imbedded within an otherwise stable galaxy WILL BE
# PRESENTED IN A LATER PAPER (Toomre 1964)."
#
# His own result is his eq. (65), and his abstract states the same:
#   sigma_u,min = (0.2857)^(1/2) kappa/alpha_crit = 3.36 G mu/kappa,
# with mu the projected STELLAR density.  The 3.36 is his.  The pi is not.
TOOMRE_STELLAR_COEFF = 3.36     # his eq. (65), STARS          VERIFIED
# THE GAS COEFFICIENT IS DERIVED IN PART H, NOT CITED.  See
# toomre_gas_coefficient() below, which obtains pi from the rotating
# isothermal sheet's own dispersion relation.  Safronov (1960), Ann.
# d'Ap. 23, 979 -- which Toomre's own reference list carries -- is the
# gas-disc precedent and WAS NOT READ; it is named for the precedent
# only, exactly as Module 12 cited Balbus & Hawley (1991).

# --- Bardeen, Press & Teukolsky (1972), ApJ 178, 347-369. ---------------
# VERIFIED at step 2 from the ADS scan, bibcode 1972ApJ...178..347B.
# Their eq. (2.21): r_ms = 6M for a = 0, the Schwarzschild innermost
# stable circular orbit.  Their eq. (2.12), the energy per unit rest mass
# of an equatorial circular orbit:
#   E/mu = (r^3/2 - 2 M r^1/2 +/- a M^1/2)
#          / (r^3/4 (r^3/2 - 3 M r^1/2 +/- 2 a M^1/2)^1/2).
# THEY PRINT NO EFFICIENCY.  The strings "8/9", "0.057" and "0.42" do not
# occur in the paper.  ETA_SCHWARZSCHILD below is COMPUTED from their
# formula by bpt_orbit_energy(), not retyped, and the assert checks it
# against the closed form 4/(3 sqrt 2).
ISCO_SCHWARZSCHILD_RG = 6.0     # their eq. (2.21), a = 0      VERIFIED

# --- Module 9's numbers, READ FROM ITS OWN RUN. -------------------------
# Not retyped off module09.html.  `python m09_numbers.py` prints:
#   L_X (2-10 keV, Baganoff)     = 2.0e+33 erg/s
#   Mdot_Bondi c^2               = 4.543e+41 erg/s
#   implied radiative efficiency = 4e-09
#   a thin disc would give ~0.1, a factor 2e+07 larger
# and module09.html:672 gives the mass: "the GRAVITY Collaboration's,
# from the orbits of individual stars: M = 4.30x10^6 M_sun to about
# +/-0.25 per cent, that is 8.5502x10^39 g".
M09_LX = 2.0e33                 # erg/s, from its run          VERIFIED
M09_MDOT_C2 = 4.543e41          # erg/s, from its run          VERIFIED
M09_ETA_RAD = M09_LX/M09_MDOT_C2    # = 4.402e-9, not retyped
M09_PRINTED_FACTOR = 2.0e7      # what module09.html:757 says  VERIFIED
M09_ASSERTED_ETA = 0.1          # module09.html:757, asserted  VERIFIED
M09_BH_MASS_MSUN = 4.30e6       # module09.html:672, GRAVITY   VERIFIED
M09_BH_MASS_G = 8.5502e39       # module09.html:672            VERIFIED

# =========================================================================
# TWO NUMBERS THIS FILE DERIVES RATHER THAN QUOTES.  Both were cited to a
# paper at step 1 and step 2 found that neither paper prints them.
# =========================================================================


def bpt_orbit_energy(r_over_M, a_over_M=0.0, direct=True):
    """E/mu for an equatorial circular orbit, Bardeen, Press & Teukolsky
    (1972) eq. (2.12), in geometrised units with M = 1.

        E/mu = (r^3/2 - 2 r^1/2 +/- a)
               / (r^3/4 (r^3/2 - 3 r^1/2 +/- 2a)^1/2)

    THEY PRINT NO EFFICIENCY.  This function evaluates the formula they
    do print.  At a = 0, r = 6 the value is 4/(3 sqrt 2) = sqrt(8/9)
    exactly, and the assert in _self_check() requires it.
    """
    r = float(r_over_M)
    a = float(a_over_M) if direct else -float(a_over_M)
    num = r**1.5 - 2.0*np.sqrt(r) + a
    den = r**0.75*np.sqrt(r**1.5 - 3.0*np.sqrt(r) + 2.0*a)
    return num/den


def toomre_gas_coefficient():
    """The pi in Q = c_T kappa_ep/(pi G Sigma), DERIVED and not cited.

    STEP 1 CITED TOOMRE (1964) FOR THIS AND HE DOES NOT PRINT IT: his
    p. 1217 says he ignores the gas and treats a disc "composed only of
    stars", and sends the gaseous case to a later paper.  His own
    coefficient, eq. (65), is 3.36 and is for stars.

    The derivation, which costs nothing.  A rotating isothermal sheet has

        omega^2 = c_T^2 k^2 - 2 pi G Sigma k + kappa_ep^2,

    which is Module 5's Jeans dispersion relation with the rotation term
    added.  The minimum over k is at k* = pi G Sigma/c_T^2, where

        omega^2(k*) = kappa_ep^2 - (pi G Sigma)^2/c_T^2,

    so marginal stability is exactly c_T kappa_ep/(pi G Sigma) = 1.  The
    function below finds the coefficient numerically from that dispersion
    relation, so it is the algebra and not a literal that supplies the pi.
    """
    # Work in units where c_T = Sigma = kappa_ep = G = 1 and solve for the
    # coefficient C such that marginal stability is kappa_ep = C G Sigma/c_T.
    k = np.linspace(1e-6, 20.0, 4000001)
    # omega^2 = k^2 - 2 pi k + kappa^2; marginal when min over k is zero.
    # min of (k^2 - 2 pi k) is at k = pi, value -pi^2, so kappa^2 = pi^2.
    kappa_sq = -np.min(k*k - 2.0*np.pi*k)
    return np.sqrt(kappa_sq)


def bpt_orbit_energy_extreme_kerr(r_over_M, direct=True):
    """E/mu for a = M, Bardeen, Press & Teukolsky (1972) eq. (2.14).

        E/mu = (r +/- M^1/2 r^1/2 - M)/(r^3/4 (r^1/2 + 2 M^1/2)^1/2)

    A SEPARATE FUNCTION IS NECESSARY AND THE PAPER SAYS WHY.  Their
    general eq. (2.12) has r^3/2 - 3 M r^1/2 + 2 a M^1/2 under the root,
    which at a = M and r = M is 1 - 3 + 2 = 0 exactly: evaluating the
    general formula at the extreme-Kerr innermost stable orbit divides by
    zero.  The first draft of this file did precisely that and got NaN.
    Their own text warns of it -- "Appearances are deceptive!  ... The
    confusion is due to the subtle nature of the Boyer-Lindquist
    coordinates at r = M for a = M" -- and their eq. (2.14) is the
    simplification to use.  At r = M it gives 1/sqrt(3).
    """
    r = float(r_over_M)
    s = 1.0 if direct else -1.0
    return (r + s*np.sqrt(r) - 1.0)/(r**0.75*np.sqrt(np.sqrt(r) + 2.0))


ETA_SCHWARZSCHILD = 1.0 - bpt_orbit_energy(ISCO_SCHWARZSCHILD_RG, 0.0)
# Their eq. (2.21) gives r_ms = M for a = M, direct orbits.
ETA_KERR_EXTREME = 1.0 - bpt_orbit_energy_extreme_kerr(1.0)
TOOMRE_GAS_COEFF = toomre_gas_coefficient()     # = pi, derived above

# --- predictions, held as named constants so no magic number appears ----
KEPLER_Q = 1.5          # q = -d ln Omega/d ln R for a point mass
RAYLEIGH_Q_CRIT = 2.0   # kappa_ep^2 > 0 iff q < 2
MRI_GROWTH_FACTOR = 0.75        # gamma_max = (q/2) Omega, Module 12 SS9
MRI_KMAX_FACTOR = np.sqrt(15.0)/4.0     # (k v_A)_max = sqrt(15)/4 Omega
THIN_DISC_TEFF_INDEX = -0.75    # T_eff ~ R^-3/4 far from the inner edge


# =========================================================================
# PART A.  The three discs, and the one question that separates them
# =========================================================================

def kepler_omega(M, R):
    """Omega_K = sqrt(G M/R^3).

    COPIED FROM m12_numbers.py PART I, where it was written for the MRI
    and is the same function.  Retyping it is the mistake the Module 12
    editor pass named.
    """
    return np.sqrt(G*M/R**3)


def kepler_speed(M, R):
    """v_K = Omega_K R = sqrt(G M/R)."""
    return np.sqrt(G*M/R)


def specific_angular_momentum(M, R):
    """ell = Omega R^2 = sqrt(G M R).

    THE GLYPH ell MEANS THIS AND NOTHING ELSE IN THIS FILE.  See the
    notation warning in the module docstring.  module12.html:700 already
    prints ell = Omega R^2 and Module 12 carries no notation row for it.
    """
    return np.sqrt(G*M*R)


def isothermal_sound_speed(T, mu):
    """c_T = sqrt(k T/(mu m_u)), Module 9's isothermal speed.

    THE ISOTHERMAL SPEED, not the adiabatic one.  The vertical structure
    of a thin disc is set by the pressure the gas actually has at its own
    temperature, and the disc is cooled by radiation on a timescale short
    against the viscous one, so the isothermal speed is the right one.
    Module 9 wrote c_T for exactly this quantity; the book does not need a
    second symbol for it.
    """
    return np.sqrt(kB*T/(mu*mu_u))


def scale_height(T, mu, M, R):
    """H = c_T/Omega_K, from vertical hydrostatic balance.

    PART E proves it.
    """
    return isothermal_sound_speed(T, mu)/kepler_omega(M, R)


def midplane_density(Sigma, H):
    """rho_0 = Sigma/(sqrt(2 pi) H), for a Gaussian vertical profile.

    PART E derives rho(z) = rho_0 exp(-z^2/2H^2), whose integral over all
    z is sqrt(2 pi) rho_0 H.  The factor is sqrt(2 pi) = 2.5066 and NOT 2:
    writing Sigma = 2 rho_0 H would be the constant-density slab and would
    put the density 25.3 per cent high.
    """
    return Sigma/(np.sqrt(2.0*np.pi)*H)


# =========================================================================
# PART B.  Keplerian shear, and why a disc does not accrete
# =========================================================================

def shear_parameter(M, R, dR_rel=1.0e-6):
    """q = -d ln Omega/d ln R, computed numerically from Omega_K.

    NOT RETURNED AS 3/2.  module12.html:782 says in print that the 3/2 is
    ASSUMED there and that deriving it needs a disc model, so this module
    must produce it rather than name it.  The derivative is taken on the
    function, so if kepler_omega were wrong this would be wrong too and
    the assert below would fire.
    """
    lnR1 = np.log(R*(1.0 - dR_rel))
    lnR2 = np.log(R*(1.0 + dR_rel))
    lnO1 = np.log(kepler_omega(M, np.exp(lnR1)))
    lnO2 = np.log(kepler_omega(M, np.exp(lnR2)))
    return -(lnO2 - lnO1)/(lnR2 - lnR1)


def epicyclic_frequency(Omega, q):
    """kappa_ep^2 = 2 Omega^2 (2 - q), for Omega ~ R^-q.

    THE SYMBOL IS kappa_ep AND NOT kappa.  notation_table.md:74 reserved it
    in Module 12 against the thermal conductivity, and said it did so
    "because a reader who knows that literature will look for it".  This
    module inherits the reservation.

    At q = 3/2 this gives kappa_ep = Omega exactly, which is the degeneracy
    that makes a Keplerian orbit close.
    """
    return Omega*np.sqrt(2.0*(2.0 - q))


def rayleigh_discriminant(M, R, dR_rel=1.0e-6):
    """d(ell^2)/dR, the Rayleigh discriminant.  Positive means STABLE.

    ell^2 = G M R for a point mass, so d(ell^2)/dR = G M > 0 everywhere:
    a Keplerian disc is hydrodynamically stable at every radius, and that
    is the problem, not the answer.  module12.html:700 states it in prose.
    """
    R1, R2 = R*(1.0 - dR_rel), R*(1.0 + dR_rel)
    l1 = specific_angular_momentum(M, R1)
    l2 = specific_angular_momentum(M, R2)
    return (l2**2 - l1**2)/(R2 - R1)


# =========================================================================
# PART C.  The timescale gap.  CHECK 1
# =========================================================================

def debye(n, T):
    """Debye length sqrt(k T/(4 pi n e^2)).  COPIED FROM m12_numbers.py."""
    return np.sqrt(kB*T/(4.0*np.pi*n*e**2))


def b_min_e(T):
    """Classical/quantum turning point for an electron.

    COPIED FROM m12_numbers.py PART B.  The larger of the classical
    distance of closest approach and the thermal de Broglie wavelength.
    """
    b_cl = e**2/(3.0*kB*T)
    b_qm = hbar/np.sqrt(3.0*me*kB*T)
    return max(b_cl, b_qm)


def lnLambda_e(n, T):
    """Coulomb logarithm, ln(lambda_D/b_min).  COPIED FROM m12_numbers.py."""
    return np.log(debye(n, T)/b_min_e(T))


def lam_coulomb(n, T, lnL, coef=SPITZER_C):
    """Thermal Coulomb mean free path, Module 1's equation and coefficient.

        lambda = coef (k T)^2/(n e^4 ln Lambda),  coef = 3^(3/2)/(4 sqrt(pi))

    COPIED FROM m12_numbers.py, which copied it from m10_numbers.py.
    Retyping it once already put a spurious pi in the denominator.
    """
    return coef*(kB*T)**2/(n*e**4*lnL)


def v_thermal(T, mu):
    """Mean thermal speed sqrt(8 k T/(pi mu m_u)).  Module 1's definition."""
    return np.sqrt(8.0*kB*T/(np.pi*mu*mu_u))


def molecular_viscosity(n, T, lnL, mu_carrier=None):
    """nu_mol = mu_dyn/rho = (1/3) v_th lambda, MODULE 1's OWN FORMULA.

    module01.html:363 is Module 1 Proposition 4, eq. (6.2):

        mu ~= (1/3) rho v_th lambda,   kappa ~= (1/3) n k_B v_th lambda,

    so the KINEMATIC viscosity is nu = mu/rho = (1/3) v_th lambda and the
    density cancels.  The coefficient 1/3 is NOT a choice made here: it
    is the book's, from the shipped page that module01.html:623 promises
    this module.

    THE THERMAL SPEED IS THE ION'S, NOT THE MIXTURE'S, and the first
    draft used the mixture.  Viscosity in a hydrogen plasma is carried by
    the ions: at equal temperature and comparable mean free path,
    mu_i/mu_e = (rho_i/rho_e)(v_i/v_e) = (m_p/m_e) sqrt(m_e/m_p)
              = sqrt(m_p/m_e) = 42.9,
    so the electron contribution is 2.3 per cent and the momentum is
    carried by protons.  Using mu = 0.6, the mean molecular weight of the
    MIXTURE, overstates v_th by sqrt(1.00728/0.6) = 1.296 and nu with it.
    """
    if mu_carrier is None:
        mu_carrier = MU_H_ION
    return lam_coulomb(n, T, lnL)*v_thermal(T, mu_carrier)/3.0


def viscous_time(R, nu):
    """t_nu = R^2/nu.  The time for the viscous diffusion of PART D to
    move material across a distance R."""
    return R*R/nu


def dynamical_time(Omega):
    """t_dyn = 1/Omega.  One radian of orbit, not one orbit."""
    return 1.0/Omega


# =========================================================================
# PART D.  The alpha prescription, and the three timescales
# =========================================================================

def alpha_viscosity(alpha, c_T, H):
    """nu = alpha c_T H.  Shakura & Sunyaev (1973).

    THIS IS NOT A DERIVATION AND THE MODULE MUST NOT PRETEND IT IS.  It is
    a dimensional parametrisation with one bound behind it: the turbulent
    eddy cannot be larger than H or faster than c_T without shocking, so
    alpha <= 1.  What supplies the stress is the magnetorotational
    instability of Module 12 SS9; what alpha's VALUE is, neither module
    derives.  module12.html:940 already fixes this symbol for this meaning.
    """
    return alpha*c_T*H


def alpha_from_viscous_time(R, t_nu, c_T, H):
    """Invert nu = alpha c_T H against a measured t_nu = R^2/nu."""
    return R*R/(t_nu*c_T*H)


def thermal_time(alpha, Omega):
    """t_th = 1/(alpha Omega).  The time to radiate the heat alpha supplies."""
    return 1.0/(alpha*Omega)


def viscous_time_alpha(alpha, Omega, H, R):
    """t_nu = (1/alpha)(R/H)^2 (1/Omega), the alpha-disc viscous time.

    The identity worth printing: with nu = alpha c_T H and H = c_T/Omega,
        t_nu = R^2/nu = R^2/(alpha c_T H) = R^2/(alpha Omega H^2)
             = (1/alpha)(R/H)^2 t_dyn.
    So the three timescales are ordered
        t_dyn : t_th : t_nu  =  1 : 1/alpha : (1/alpha)(R/H)^2,
    and for a thin disc (H/R << 1) with alpha < 1 that ordering is strict.
    """
    return (R/H)**2/(alpha*Omega)


# =========================================================================
# PART E.  Vertical structure and the thin-disc condition
# =========================================================================

def vertical_gravity(M, R, z):
    """g_z = G M z/(R^2 + z^2)^(3/2), the vertical pull of the central mass.

    For z << R this is Omega_K^2 z, which is what makes the vertical
    profile a Gaussian.  The function keeps the exact form so that PART E
    can price the error of the approximation rather than assume it.
    """
    return G*M*z/(R*R + z*z)**1.5


def vertical_gravity_thin(M, R, z):
    """Omega_K^2 z, the thin-disc approximation to vertical_gravity."""
    return kepler_omega(M, R)**2*z


def density_profile(rho0, z, H):
    """rho(z) = rho_0 exp(-z^2/2H^2), isothermal vertical hydrostatic."""
    return rho0*np.exp(-0.5*(z/H)**2)


def aspect_ratio(T, mu, M, R):
    """H/R = c_T/v_K.  The thin-disc condition is that this is small."""
    return isothermal_sound_speed(T, mu)/kepler_speed(M, R)


# =========================================================================
# PART F.  The steady thin disc
# =========================================================================

def nu_sigma_steady(Mdot, R, R_in):
    """nu Sigma = (Mdot/3 pi)[1 - sqrt(R_in/R)].

    The steady solution of the diffusion equation with a zero-torque inner
    boundary.  The bracket is what makes the disc radiate MORE than the
    local release rate at large R: a factor of three at R >> R_in, because
    the inner disc's angular momentum has to go somewhere.
    """
    return (Mdot/(3.0*np.pi))*(1.0 - np.sqrt(R_in/R))


def dissipation_per_area(Mdot, M, R, R_in):
    """D(R) = (3 G M Mdot/8 pi R^3)[1 - sqrt(R_in/R)], per unit area PER SIDE.

    PER SIDE.  The disc has two faces and radiates from both, so the
    quantity that equals sigma T_eff^4 is half the total dissipation per
    unit area of disc.  Getting this factor wrong moves T_eff by 2^(1/4)
    = 19 per cent.
    """
    return (3.0*G*M*Mdot/(8.0*np.pi*R**3))*(1.0 - np.sqrt(R_in/R))


def t_effective(Mdot, M, R, R_in):
    """T_eff = (D(R)/sigma_SB)^(1/4)."""
    return (dissipation_per_area(Mdot, M, R, R_in)/sigma_SB)**0.25


def t_eff_index(Mdot, M, R, R_in, dR_rel=1.0e-6):
    """d ln T_eff/d ln R, computed numerically.  Tends to -3/4 far out."""
    R1, R2 = R*(1.0 - dR_rel), R*(1.0 + dR_rel)
    t1 = t_effective(Mdot, M, R1, R_in)
    t2 = t_effective(Mdot, M, R2, R_in)
    return (np.log(t2) - np.log(t1))/(np.log(R2) - np.log(R1))


def disc_luminosity(Mdot, M, R_in):
    """L = G M Mdot/(2 R_in), the integral of 2 D(R) over the whole disc.

    HALF the binding energy at R_in, not all of it.  The other half is the
    kinetic energy of the orbit at R_in, which the disc has not radiated.
    """
    return G*M*Mdot/(2.0*R_in)


# =========================================================================
# PART G.  The radiative efficiency.  CHECK 3
# =========================================================================

def gravitational_radius(M):
    """R_g = G M/c^2."""
    return G*M/c**2


def efficiency_newtonian(R_in_over_Rg):
    """eta = L/(Mdot c^2) = 1/(2 x), with x = R_in/R_g.

    From PART F:  L = G M Mdot/(2 R_in), so
        eta = G M/(2 R_in c^2) = R_g/(2 R_in) = 1/(2 x).
    At the Schwarzschild innermost stable circular orbit, x = 6, this is
    EXACTLY 1/12.  The assert below is the trivial-limit check the Module
    12 editor pass asked every later module to copy.
    """
    return 1.0/(2.0*R_in_over_Rg)


def eddington_luminosity(M):
    """L_Edd = 4 pi G M m_p c/sigma_T.

    Module 9 states this and does not derive it; module09.html:944 sends
    the derivation to Module 13 and this module does NOT take it up.  It
    is used here only to set a scale for Mdot.
    """
    return 4.0*np.pi*G*M*mp*c/sigma_T


def eddington_rate(M, eta):
    """Mdot_Edd = L_Edd/(eta c^2).  Depends on the efficiency assumed."""
    return eddington_luminosity(M)/(eta*c*c)


# =========================================================================
# PART H.  Self-gravity: the Toomre criterion
# =========================================================================

def toomre_q(c_T, kappa_ep, Sigma, coeff=TOOMRE_GAS_COEFF):
    """Q = c_T kappa_ep/(coeff G Sigma).  Stable to axisymmetric
    modes if Q > 1.

    THE COEFFICIENT IS pi FOR A GAS DISC AND 3.36 FOR A STELLAR ONE, and
    the module must not average them.  Module 5 built the Jeans criterion
    for a non-rotating gas; this is the same competition with rotation
    added, which is the promise module05.html:764 printed.
    """
    return c_T*kappa_ep/(coeff*G*Sigma)


def toomre_q_steady(alpha, c_T, Mdot, R, R_in):
    """Q for a steady alpha-disc, in closed form.

    Substituting Sigma = nu_sigma_steady/nu with nu = alpha c_T H and
    H = c_T/Omega, and kappa_ep = Omega for a Keplerian disc:

        Sigma = (Mdot/3 pi) f Omega/(alpha c_T^2),   f = 1 - sqrt(R_in/R)
        Q = c_T Omega/(pi G Sigma) = 3 alpha c_T^3/(G Mdot f).

    OMEGA AND R HAVE BOTH CANCELLED.  Q depends on the LOCAL TEMPERATURE
    only, through c_T^3, and on two global numbers.  That is why the
    self-gravity radius of a disc is a statement about its temperature
    profile and not about its mass.
    """
    f = 1.0 - np.sqrt(R_in/R)
    return 3.0*alpha*c_T**3/(G*Mdot*f)


# =========================================================================
# PART I.  Centrifugal support, the promise of module03.html:792
# =========================================================================

def centrifugal_flattening(Omega, M, R):
    """Omega^2 R^3/(G M), the ratio of centrifugal to gravitational pull.

    module03.html:792 printed "Excludes centrifugal flattening and the
    rotational support of discs" and sent it here.  For a Keplerian disc
    this ratio is exactly 1 in the plane -- the disc is entirely
    centrifugally supported radially -- and the assert below checks it.
    A hydrostatic star has this ratio near zero; that is the whole
    difference between Module 3's object and this one.
    """
    return Omega**2*R**3/(G*M)


def circularisation_radius(M, ell):
    """R_circ = ell^2/(G M).  Where gas of specific angular momentum ell
    stops falling and starts orbiting.

    module09.html:832 printed that Sgr A*'s gas circularises near 100 r_S
    and that transporting its angular momentum outward "is Module 11's
    subject".  This is the function that makes that sentence a number.
    """
    return ell*ell/(G*M)


# =========================================================================
# PART J.  The link to the magnetorotational instability
# =========================================================================

def mri_growth_rate(omega, q=KEPLER_Q):
    """gamma_max = (q/2) Omega.  COPIED FROM m12_numbers.py PART I.

    Module 12 SS9 derived this with q ASSUMED.  PART B of this file derives
    the q.  The instability itself is NOT re-derived here:
    module08.html:728 lists it among what Module 12 builds, and deriving it
    twice would make one of the two modules redundant in print.
    """
    return 0.5*q*omega


def mri_wavelength_max(vA, omega):
    """2 pi v_A/(sqrt(15)/4 Omega).  COPIED FROM m12_numbers.py PART I."""
    return 2.0*np.pi*vA/(MRI_KMAX_FACTOR*omega)


def alfven_speed(B, rho):
    """v_A = B/sqrt(4 pi rho).  COPIED FROM m12_numbers.py PART A."""
    return B/np.sqrt(4.0*np.pi*rho)


def mri_containment_ratio(alpha):
    """lambda_max/(2H) = 4 pi sqrt(alpha)/sqrt(15), a PURE NUMBER.

    THE FIRST DRAFT OF THIS FILE PRINTED THIS AS A TWO-ROW TABLE OVER THE
    CENSUS AND BOTH ROWS CAME OUT 1.0260.  They had to.  Putting
    B = sqrt(4 pi alpha rho c_T^2) into v_A = B/sqrt(4 pi rho) gives
    v_A = c_T sqrt(alpha), and H = c_T/Omega, so

        lambda_max = 2 pi v_A/((sqrt(15)/4) Omega)
                   = (8 pi/sqrt(15)) sqrt(alpha) H

    and every disc property cancels.  A table of identical rows pretends
    to be a census result and is not one.  The real content is the bound
    below.
    """
    return 4.0*np.pi*np.sqrt(alpha)/np.sqrt(15.0)


def alpha_max_for_containment():
    """The largest alpha for which lambda_max < 2H: alpha < 15/(16 pi^2).

    A DERIVED BOUND, not a fitted one.  Setting mri_containment_ratio to
    1 and squaring gives alpha = 15/(16 pi^2) = 0.094993.  Above it the
    fastest-growing MRI mode is longer than the disc is thick, so the
    equipartition identification B^2 ~ 4 pi alpha P cannot be the whole
    story for the alpha that CHECK 2 infers.
    """
    return 15.0/(16.0*np.pi**2)


def field_for_alpha(alpha, rho, c_T):
    """The field whose Maxwell stress supplies a given alpha.

    The MRI's saturated stress is of order B_R B_phi/4 pi, and the alpha
    prescription writes that stress as alpha rho c_T^2.  Taking
    B_R B_phi ~ B^2 gives B ~ sqrt(4 pi alpha rho c_T^2) = sqrt(4 pi alpha
    P).  THIS IS AN ORDER-OF-MAGNITUDE IDENTIFICATION AND NOT A RESULT:
    simulations put B_R B_phi/B^2 near 0.3, and the module says so rather
    than printing a number to three figures.
    """
    return np.sqrt(4.0*np.pi*alpha*rho*c_T**2)


# =========================================================================
# THE CENSUS, AT MODULE SCOPE.  m11_build_figs.py imports these, so the
# figures and the prose cannot diverge -- m10_build_figs.py's rule.
#
# THESE THREE DISCS ARE A CONFIGURATION AND NOT AN OBJECT, in the sense
# module07.html:453 and module12.html:782 use the phrase, EXCEPT for the
# dwarf nova, which CHECK 1 and CHECK 2 do compare against measurement.
# Every entry is a round choice inside the range its class occupies.
# =========================================================================

# Dwarf nova in outburst.  A short-period cataclysmic variable: a white
# dwarf accreting from a Roche-lobe-filling companion.  NOT YET VERIFIED:
# step 2 must source the white-dwarf mass, the outer disc radius, the
# outburst temperature and the surface density, and must find a named
# system rather than a class average if CHECK 2 is to be a measurement.
M_WD = 0.6*Msun                 # g                      NOT YET VERIFIED
R_DN = 1.0e10                   # cm, outer disc         NOT YET VERIFIED
T_DN = 3.0e4                    # K, outburst            NOT YET VERIFIED
SIGMA_DN = 1.0e2                # g cm^-2, outburst      NOT YET VERIFIED
T_OUTBURST_OBSERVED = 5.0*day   # s, outburst duration   NOT YET VERIFIED

# Protoplanetary disc around a T Tauri star, at 10 au.
M_TT = 1.0*Msun                 # g                      NOT YET VERIFIED
R_TT = 10.0*AU                  # cm                     NOT YET VERIFIED
T_TT = 50.0                     # K                      NOT YET VERIFIED
SIGMA_TT = 10.0                 # g cm^-2                NOT YET VERIFIED

# The inner disc of a 10^8 M_sun active galactic nucleus, at 100 R_g.
M_AGN = 1.0e8*Msun              # g
R_AGN_RG = 100.0                # in units of R_g
MDOT_AGN_EDD_FRACTION = 0.1     # of the Eddington rate at eta = 0.1

DISC_ROWS = [
    # name, M, R, T, mu, Sigma
    ('dwarf nova, outburst', M_WD, R_DN, T_DN, MU_IONISED_H, SIGMA_DN),
    ('protoplanetary, 10 au', M_TT, R_TT, T_TT, MU_MOLECULAR, SIGMA_TT),
]


# =========================================================================
# ASSERTS.  Each one fails if a formula above is wrong, and each was
# written before the run rather than fitted to it.
# =========================================================================

def _self_check():
    """Every check here is a limit whose answer is known in advance."""
    # q = 3/2 for a point mass, to the accuracy of the numerical derivative.
    q = shear_parameter(M_WD, R_DN)
    assert abs(q - KEPLER_Q) < 1e-6, f'shear parameter is {q}, not 3/2'

    # kappa_ep = Omega exactly at q = 3/2.  The Keplerian degeneracy.
    Om = kepler_omega(M_WD, R_DN)
    assert abs(epicyclic_frequency(Om, KEPLER_Q)/Om - 1.0) < 1e-12

    # The Rayleigh discriminant is G M at every radius, and positive.
    d = rayleigh_discriminant(M_WD, R_DN)
    assert abs(d/(G*M_WD) - 1.0) < 1e-5, f'discriminant/GM = {d/(G*M_WD)}'
    assert d > 0.0, 'a Keplerian disc must come out Rayleigh-stable'

    # A Keplerian disc is exactly centrifugally supported in its plane.
    cf = centrifugal_flattening(Om, M_WD, R_DN)
    assert abs(cf - 1.0) < 1e-12, f'centrifugal ratio is {cf}, not 1'

    # THE TRIVIAL LIMIT OF CHECK 3.  At the Schwarzschild ISCO the
    # Newtonian efficiency is exactly 1/12.  If this ever fails, PART F's
    # factor of two in disc_luminosity is wrong.
    eta = efficiency_newtonian(ISCO_SCHWARZSCHILD_RG)
    assert abs(eta - 1.0/12.0) < 1e-15, f'eta is {eta}, not 1/12'

    # BPT's eq. (2.12) at a = 0, r = 6 must give 4/(3 sqrt 2) = sqrt(8/9)
    # EXACTLY.  This is the assert that makes ETA_SCHWARZSCHILD a
    # computation from their formula rather than a retyped literal.
    assert abs(bpt_orbit_energy(6.0, 0.0) - 4.0/(3.0*np.sqrt(2.0))) < 1e-14
    assert abs(bpt_orbit_energy(6.0, 0.0) - np.sqrt(8.0/9.0)) < 1e-14
    # And their eq. (2.14) at r = M, a = M must give 1/sqrt(3).
    assert abs(bpt_orbit_energy_extreme_kerr(1.0)
               - 1.0/np.sqrt(3.0)) < 1e-14
    # The general formula DIVIDES BY ZERO there, which is why a second
    # function exists.  If this ever stops being nan, the note is stale.
    assert not np.isfinite(bpt_orbit_energy(1.0, 1.0))
    # Both derived efficiencies must land on Shakura & Sunyaev's own
    # printed values to the one figure they printed them with.
    assert abs(ETA_SCHWARZSCHILD - SS73_ETA_SCHWARZSCHILD) < 0.005
    assert abs(ETA_KERR_EXTREME - SS73_ETA_KERR_MAX) < 0.03

    # The gas coefficient must come out of the dispersion relation as pi.
    assert abs(TOOMRE_GAS_COEFF - np.pi) < 1e-9, \
        f'gas coefficient is {TOOMRE_GAS_COEFF}, not pi'
    # It must NOT be Toomre's own 3.36, which is the STELLAR value.
    assert abs(TOOMRE_GAS_COEFF - TOOMRE_STELLAR_COEFF) > 0.2

    # Module 9's efficiency must be what its own run prints, and the
    # factor its HTML prints must follow from it to one figure.
    assert abs(M09_ETA_RAD - 4.402e-9) < 1e-11, f'{M09_ETA_RAD}'
    assert abs(np.log10(M09_ASSERTED_ETA/M09_ETA_RAD)
               - np.log10(M09_PRINTED_FACTOR)) < 0.06

    # The efficiency must also equal the luminosity route, which uses
    # disc_luminosity and gravitational_radius and shares no line of code.
    R_in = ISCO_SCHWARZSCHILD_RG*gravitational_radius(M_AGN)
    Mdot = 1.0                  # 1 g/s, so L/(Mdot c^2) is eta directly
    assert abs(disc_luminosity(Mdot, M_AGN, R_in)/(Mdot*c*c)
               - 1.0/12.0) < 1e-12

    # T_eff -> R^-3/4 far from the inner edge.
    idx = t_eff_index(1.0e18, M_AGN, 1.0e6*gravitational_radius(M_AGN),
                      ISCO_SCHWARZSCHILD_RG*gravitational_radius(M_AGN))
    assert abs(idx - THIN_DISC_TEFF_INDEX) < 1e-3, f'T_eff index {idx}'

    # The closed-form Toomre Q must equal the long route.
    alpha, Mdot2 = 0.1, 1.0e25
    M, R = M_AGN, 1.0e4*gravitational_radius(M_AGN)
    R_in2 = ISCO_SCHWARZSCHILD_RG*gravitational_radius(M_AGN)
    Om2 = kepler_omega(M, R)
    T = t_effective(Mdot2, M, R, R_in2)
    cT = isothermal_sound_speed(T, MU_IONISED_H)
    H = cT/Om2
    nu = alpha_viscosity(alpha, cT, H)
    Sig = nu_sigma_steady(Mdot2, R, R_in2)/nu
    q_long = toomre_q(cT, epicyclic_frequency(Om2, KEPLER_Q), Sig)
    q_short = toomre_q_steady(alpha, cT, Mdot2, R, R_in2)
    assert abs(q_long/q_short - 1.0) < 1e-10, f'{q_long} vs {q_short}'

    # The MRI containment ratio must be the identity, on BOTH census
    # rows and for the closed form.  This is the assert that would have
    # caught the decorative two-row table on the first run.
    for _n, _M, _R, _T, _mu, _S in DISC_ROWS:
        _Om = kepler_omega(_M, _R)
        _cT = isothermal_sound_speed(_T, _mu)
        _H = _cT/_Om
        _rho = midplane_density(_S, _H)
        _B = field_for_alpha(0.1, _rho, _cT)
        _lam = mri_wavelength_max(alfven_speed(_B, _rho), _Om)
        assert abs(_lam/(2.0*_H)/mri_containment_ratio(0.1) - 1.0) < 1e-12
    assert abs(mri_containment_ratio(alpha_max_for_containment())
               - 1.0) < 1e-12

    # PART L's own limits, each known in advance.
    # C1: a rigid rotator has kappa_ep = 2 Omega, and kappa_ep vanishes
    # exactly at the Rayleigh boundary q = 2.
    assert abs(epicyclic_frequency(1.0, 0.0) - 2.0) < 1e-14
    assert abs(epicyclic_frequency(1.0, RAYLEIGH_Q_CRIT)) < 1e-14
    # C3: the steady disc's temperature maximum is at 49/36 of R_in, a
    # number that depends on nothing at all.
    _Rin = ISCO_SCHWARZSCHILD_RG*gravitational_radius(M_AGN)
    _g = np.linspace(1.0001*_Rin, 4.0*_Rin, 400001)
    _i = int(np.argmax(t_effective(1.0e25, M_AGN, _g, _Rin)))
    assert abs(_g[_i]/_Rin - 49.0/36.0) < 1e-4
    # D2: the dissipation is exactly the local release at R = 9/4 R_in,
    # because 3(1 - sqrt(R_in/R)) = 1 there, and tends to 3 far out.
    _R94 = 2.25*_Rin
    _loc = G*M_AGN*1.0e25/(8.0*np.pi*_R94**3)
    assert abs(dissipation_per_area(1.0e25, M_AGN, _R94, _Rin)/_loc
               - 1.0) < 1e-9
    _Rfar = 1.0e9*_Rin
    _locf = G*M_AGN*1.0e25/(8.0*np.pi*_Rfar**3)
    assert abs(dissipation_per_area(1.0e25, M_AGN, _Rfar, _Rin)/_locf
               - 3.0) < 1e-4
    # K2: the luminosity route and the efficiency route must give the
    # same eta, and it must be 1/12.
    _Ms = M09_BH_MASS_G
    _Rins = ISCO_SCHWARZSCHILD_RG*gravitational_radius(_Ms)
    _Md = M09_MDOT_C2/(c*c)
    assert abs(disc_luminosity(_Md, _Ms, _Rins)/(_Md*c*c)
               - 1.0/12.0) < 1e-12
    # and K2's decades must match PART G's factor for the same eta.
    assert abs(np.log10(disc_luminosity(_Md, _Ms, _Rins)/M09_LX)
               - np.log10((1.0/12.0)/M09_ETA_RAD)) < 1e-9

    # The three timescales must be ordered for a thin disc.
    cT_dn = isothermal_sound_speed(T_DN, MU_IONISED_H)
    H_dn = cT_dn/Om
    t1 = dynamical_time(Om)
    t2 = thermal_time(0.2, Om)
    t3 = viscous_time_alpha(0.2, Om, H_dn, R_DN)
    assert t1 < t2 < t3, f'timescales out of order: {t1} {t2} {t3}'

    # viscous_time_alpha and viscous_time must agree.
    nu_dn = alpha_viscosity(0.2, cT_dn, H_dn)
    assert abs(viscous_time(R_DN, nu_dn)/t3 - 1.0) < 1e-12

    # The Gaussian column must integrate to Sigma.
    z = np.linspace(-20.0*H_dn, 20.0*H_dn, 200001)
    rho0 = midplane_density(SIGMA_DN, H_dn)
    col = np.trapezoid(density_profile(rho0, z, H_dn), z)
    assert abs(col/SIGMA_DN - 1.0) < 1e-6, f'column is {col/SIGMA_DN} Sigma'

    # The thin-disc vertical gravity must approach the exact one.
    zt = 0.01*R_DN
    assert abs(vertical_gravity_thin(M_WD, R_DN, zt)
               / vertical_gravity(M_WD, R_DN, zt) - 1.0) < 2e-4


def main():
    _self_check()
    P = print
    P('=' * 74)
    P('MODULE 11 NUMBERS: accretion discs')
    P('=' * 74)
    P('STEPS 1 AND 2 OF SIX.  Every published constant is now marked')
    P('VERIFIED with the page it was read from, EXCEPT the dwarf-nova')
    P('parameters, which are STILL UNSOURCED -- see the end of this run.')
    P('Five papers were fetched; one, Shakura & Sunyaev (1973), is an')
    P('image-only scan and was rendered at 190 dpi and read as images.')
    P('The four checks have no verdicts yet: Gate D fixes them in')
    P('advance, as Modules 7 to 12 did.')

    # ---------------------------------------------------------------- B
    P('')
    P('PART B.  Keplerian shear, and why a disc does not accrete')
    P('-'*74)
    P('  module12.html:700 prints the argument and module12.html:782 says')
    P('  the q = 3/2 behind it is ASSUMED.  Here it is derived.')
    P('')
    q = shear_parameter(M_WD, R_DN)
    Om_dn = kepler_omega(M_WD, R_DN)
    kap = epicyclic_frequency(Om_dn, q)
    P(f'  q = -d ln Omega/d ln R, differentiated numerically = {q:.10f}')
    P(f'  exactly 3/2 to {abs(q - KEPLER_Q):.2e}, and the assert requires it')
    P(f'  kappa_ep/Omega at q = 3/2                          = '
      f'{kap/Om_dn:.10f}')
    P('  so the epicyclic and orbital frequencies are EQUAL, which is why')
    P('  a Keplerian orbit closes on itself and does not precess.')
    P('')
    P('  THE RAYLEIGH CRITERION.  A rotating flow is stable to')
    P('  axisymmetric displacements where d(ell^2)/dR > 0.  For a point')
    P('  mass ell^2 = G M R, so')
    d = rayleigh_discriminant(M_WD, R_DN)
    P(f'    d(ell^2)/dR             = {d:.6e} cm^3 s^-2')
    P(f'    G M                     = {G*M_WD:.6e} cm^3 s^-2')
    P(f'    ratio                   = {d/(G*M_WD):.10f}')
    P('  POSITIVE AT EVERY RADIUS, and independent of radius.  The disc')
    P('  is stable, and a stable disc transports no angular momentum and')
    P('  therefore does not accrete.  THAT IS THE PROBLEM OF THIS MODULE.')
    P(f'  Instability would need q > {RAYLEIGH_Q_CRIT:.1f}, and a point')
    P('  mass gives 3/2 and can give nothing else.')

    # ---------------------------------------------------------------- A
    P('')
    P('PART A.  The census.  TWO rows here, and a third at PART F')
    P('-'*74)
    P('  THESE ARE CONFIGURATIONS AND NOT OBJECTS, except that CHECK 1')
    P('  and CHECK 2 do compare the dwarf-nova row against measurement.')
    P('  Every entry is NOT YET VERIFIED.  The active-galactic-nucleus')
    P('  disc is NOT in this table: it has no independent temperature,')
    P('  because PART F computes T_eff for it from the accretion rate.')
    P('  Putting it here would have meant inventing a temperature.')
    P('')
    P(f'  {"disc":<24} {"T (K)":>8} {"Omega (s^-1)":>13} {"c_T (km/s)":>11} '
      f'{"H/R":>10} {"n (cm^-3)":>11}')
    census = {}
    for name, M, R, T, mu, Sigma in DISC_ROWS:
        Om = kepler_omega(M, R)
        cT = isothermal_sound_speed(T, mu)
        H = cT/Om
        rho0 = midplane_density(Sigma, H)
        n0 = rho0/(mu*mu_u)
        census[name] = dict(M=M, R=R, T=T, mu=mu, Sigma=Sigma, Om=Om,
                            cT=cT, H=H, rho0=rho0, n0=n0)
        P(f'  {name:<24} {T:>8.3g} {Om:>13.4e} {cT/1e5:>11.4g} '
          f'{H/R:>10.5f} {n0:>11.4g}')
    P('')
    P('  BOTH ARE THIN: H/R is a few per cent, so the thin-disc')
    P('  approximation of PART E is self-consistent in both rows.')

    # ---------------------------------------------------------------- C
    P('')
    P('PART C.  CHECK 1.  The timescale gap')
    P('-'*74)
    P('  index.html:78 has already promised this number in print.')
    P('  module01.html:623 says Module 1 SS6 supplies the coefficients')
    P('  and that Module 11 needs them for accretion discs.  Here they')
    P('  are used.')
    P('')
    dn = census['dwarf nova, outburst']
    lnL = lnLambda_e(dn['n0'], dn['T'])
    lam = lam_coulomb(dn['n0'], dn['T'], lnL)
    vth = v_thermal(dn['T'], MU_H_ION)
    nu_mol = molecular_viscosity(dn['n0'], dn['T'], lnL)
    nu_mol_mixture = molecular_viscosity(dn['n0'], dn['T'], lnL, dn['mu'])
    t_nu_mol = viscous_time(dn['R'], nu_mol)
    t_dyn = dynamical_time(dn['Om'])
    P(f'  dwarf-nova disc at R      = {dn["R"]:.3e} cm')
    P(f'    midplane n              = {dn["n0"]:.4e} cm^-3')
    P(f'    ln Lambda               = {lnL:.4f}')
    P(f'    Coulomb mean free path  = {lam:.4e} cm')
    P(f'      lambda/H              = {lam/dn["H"]:.4e}')
    P(f'    mean thermal speed, IONS= {vth/1e5:.4f} km/s')
    P(f'    nu_mol = v_th lambda/3  = {nu_mol:.4f} cm^2 s^-1')
    P(f'      module01.html:363 eq. (6.2) is mu ~= (1/3) rho v_th lambda,')
    P(f'      so nu = mu/rho = (1/3) v_th lambda and rho cancels.  The')
    P(f'      1/3 is MODULE 1\'s coefficient and not a choice made here.')
    P(f'      With the MIXTURE mu = {dn["mu"]} instead of the ion, nu would')
    P(f'      be {nu_mol_mixture:.4f}, larger by '
      f'{nu_mol_mixture/nu_mol:.4f}.  Viscosity is carried')
    P(f'      by the ions: mu_i/mu_e = sqrt(m_p/m_e) = '
      f'{np.sqrt(mp/me):.1f}.')
    P('')
    P(f'    t_dyn = 1/Omega         = {t_dyn:.4e} s '
      f'= {t_dyn/day:.4f} d')
    P(f'    t_nu = R^2/nu_mol       = {t_nu_mol:.4e} s '
      f'= {t_nu_mol/yr:.4e} yr')
    P(f'    observed outburst       = {T_OUTBURST_OBSERVED:.4e} s '
      f'= {T_OUTBURST_OBSERVED/day:.1f} d   NOT YET VERIFIED')
    P('')
    P('  PUNCHLINE CHECK 1, AND THE VERDICT IS NOT FIXED AT STEP 1.')
    gap = t_nu_mol/T_OUTBURST_OBSERVED
    P(f'    t_nu(molecular)/t_observed = {gap:.4e}')
    P(f'    that is {np.log10(gap):.2f} DECADES.')
    P('    Molecular viscosity is not slow by a factor.  It is slow by')
    P(f'    {np.log10(gap):.2f} decades, and nothing inside the transport')
    P('    coefficient closes a gap of that size.  The two quantities')
    P('    that could be argued about are priced here, not waved at:')
    P(f'      using the mixture and not the ion          x '
      f'{nu_mol_mixture/nu_mol:.4f}')
    P(f'      doubling ln Lambda from {lnL:.2f} to {2*lnL:.2f}      x '
      f'{0.5:.4f}')
    P('    Together they are worth 0.35 of a decade against 12.01.')
    P('    SOMETHING OTHER THAN COLLISIONS MOVES THE ANGULAR MOMENTUM.')
    alpha_needed = nu_mol/(dn['cT']*dn['H'])
    P(f'    alpha_equivalent of nu_mol = {alpha_needed:.4e}')
    P(f'    against the measured {KPL07_ALPHA_LO}-{KPL07_ALPHA_HI}: short')
    P(f'    by {np.log10(KPL07_ALPHA_LO/alpha_needed):.2f} to '
      f'{np.log10(KPL07_ALPHA_HI/alpha_needed):.2f} decades.')

    # ---------------------------------------------------------------- D
    P('')
    P('PART D.  alpha from an outburst.  THIS IS NOT A CHECK')
    P('-'*74)
    alpha_inferred = alpha_from_viscous_time(
        dn['R'], T_OUTBURST_OBSERVED, dn['cT'], dn['H'])
    P('  STEP 2 KILLED THIS AS A CHECK, AND THE PAPER IS WHY.  King,')
    P('  Pringle & Livio section 2.1 writes their own eq. (2) as')
    P('    t_visc ~ R^2/nu,')
    P('  which is the SAME RELATION this file inverts, and they say in')
    P('  the same paragraph that "the disc sizes are known from the')
    P('  system properties", that the temperatures "are known from the')
    P('  spectra thus determining H/R", and that "observation of the')
    P('  evolution timescale of the outbursts gives a reasonably')
    P('  well-determined estimate of the viscous timescale and hence of')
    P('  alpha".  Running their method on a configuration and comparing')
    P('  the answer to their answer tests ARITHMETIC, not physics.')
    P('')
    P('  What it does show is that the module reproduces their method:')
    P(f'    alpha from t_nu = R^2/(alpha c_T H)  = {alpha_inferred:.4f}')
    P(f'    their section 2.1, dwarf novae       = '
      f'{KPL07_DN_ALPHA_LO}-{KPL07_DN_ALPHA_HI}      VERIFIED')
    P(f'    their abstract, all ionised discs    = '
      f'{KPL07_ALPHA_LO}-{KPL07_ALPHA_HI}      VERIFIED')
    if alpha_inferred > KPL07_DN_ALPHA_HI:
        P(f'    above the top of their 2.1 range by  = '
          f'{alpha_inferred/KPL07_DN_ALPHA_HI:.4f}')
    elif alpha_inferred < KPL07_DN_ALPHA_LO:
        P(f'    below the bottom of their 2.1 range  = '
          f'{alpha_inferred/KPL07_DN_ALPHA_LO:.4f}')
    else:
        P('    inside their section 2.1 range')
    P('  AND THE INPUTS ARE A CONFIGURATION.  No named dwarf nova was')
    P('  fetched, so R, T, Sigma and the 5-day timescale are round')
    P('  choices, and the agreement above is worth exactly what a round')
    P('  choice is worth.  CHECK 2 IS NOW THE TEMPERATURE PROFILE OF')
    P('  PART F, which is viscosity-INDEPENDENT and therefore tests')
    P('  something this module does not put in by hand.')
    P('')
    P('  THE THREE TIMESCALES, at alpha = 0.2 and the dwarf-nova row:')
    a0 = 0.2
    tt = thermal_time(a0, dn['Om'])
    tv = viscous_time_alpha(a0, dn['Om'], dn['H'], dn['R'])
    P(f'    t_dyn                   = {t_dyn:.4e} s')
    P(f'    t_th  = t_dyn/alpha     = {tt:.4e} s   '
      f'ratio {tt/t_dyn:.2f}')
    P(f'    t_nu  = t_th (R/H)^2    = {tv:.4e} s   '
      f'ratio {tv/t_dyn:.4e}')
    P(f'    (R/H)^2                 = {(dn["R"]/dn["H"])**2:.4e}')
    P('    The ordering t_dyn < t_th < t_nu is what makes a thin disc a')
    P('    well-posed object: it can be treated as hydrostatic vertically')
    P('    and in thermal balance locally while it evolves radially.')

    # ---------------------------------------------------------------- E
    P('')
    P('PART E.  Vertical structure, and the price of the thin approximation')
    P('-'*74)
    z_test = 2.0*dn['H']
    exact = vertical_gravity(dn['M'], dn['R'], z_test)
    thin = vertical_gravity_thin(dn['M'], dn['R'], z_test)
    P(f'  At z = 2H = {z_test:.4e} cm, z/R = {z_test/dn["R"]:.5f}:')
    P(f'    exact g_z               = {exact:.6e} cm s^-2')
    P(f'    thin-disc Omega^2 z     = {thin:.6e} cm s^-2')
    P(f'    error                   = {100*(thin/exact - 1.0):.4f} per cent')
    P('  0.31 PER CENT AT TWO SCALE HEIGHTS, and 95.45 per cent of a')
    P('  Gaussian column lies inside 2H.  The error grows as (z/R)^2, so')
    P('  it is the ASPECT RATIO and not the height that prices it: at')
    P(f'  H/R = {dn["H"]/dn["R"]:.5f} the disc is thin enough that the')
    P('  approximation costs less than half a per cent where the mass is.')
    rho0 = dn['rho0']
    P(f'    rho_0 = Sigma/(sqrt(2 pi) H) = {rho0:.4e} g cm^-3')
    P('    The factor is sqrt(2 pi) = 2.5066 and not 2; a constant-density')
    P('    slab would put rho_0 25.3 per cent high.')

    # ---------------------------------------------------------------- F
    P('')
    P('PART F.  The steady thin disc')
    P('-'*74)
    Rg_agn = gravitational_radius(M_AGN)
    R_in_agn = ISCO_SCHWARZSCHILD_RG*Rg_agn
    eta_assumed = M09_ASSERTED_ETA
    Mdot_agn = MDOT_AGN_EDD_FRACTION*eddington_rate(M_AGN, eta_assumed)
    P(f'  A 10^8 M_sun black hole, R_g = {Rg_agn:.4e} cm')
    P(f'    R_in = 6 R_g            = {R_in_agn:.4e} cm')
    P(f'    L_Edd                   = {eddington_luminosity(M_AGN):.4e} erg/s')
    P(f'    Mdot at 0.1 Edd, eta=0.1= {Mdot_agn:.4e} g/s '
      f'= {Mdot_agn*yr/Msun:.4f} M_sun/yr')
    P('')
    P(f'  {"R/R_g":>10} {"T_eff (K)":>12} {"d ln T/d ln R":>15}')
    for x in [10.0, 30.0, 1.0e2, 1.0e3, 1.0e4, 1.0e5]:
        R = x*Rg_agn
        if R <= R_in_agn:
            continue
        P(f'  {x:>10.4g} {t_effective(Mdot_agn, M_AGN, R, R_in_agn):>12.4f} '
          f'{t_eff_index(Mdot_agn, M_AGN, R, R_in_agn):>15.5f}')
    P('')
    P('')
    P('  PUNCHLINE CHECK 2, AND THE VERDICT IS NOT FIXED AT STEP 2.')
    P('  THE EXPONENT -3/4 CONTAINS NO VISCOSITY.  It comes from')
    P('  D(R) = (3 G M Mdot/8 pi R^3) f and sigma T^4 = D, and nu,')
    P('  alpha and Sigma have all cancelled.  King, Pringle & Livio')
    P('  section 1 say exactly that, and say what it is measured')
    P('  against:')
    P('    "the radial distribution of effective temperature across a')
    P('     steady disc (T(R) ~ R^-3/4) IS INDEPENDENT OF THE VISCOSITY,')
    P('     being just a statement of energy conservation, and is in')
    P('     reasonable accord with both continuum spectra and eclipse')
    P('     mapping of cataclysmic variables"')
    idx_far = t_eff_index(Mdot_agn, M_AGN, 1.0e5*Rg_agn, R_in_agn)
    P(f'    this module far from the edge        = {idx_far:.5f}')
    P(f'    the prediction                       = '
      f'{THIN_DISC_TEFF_INDEX:.5f}')
    P(f'    difference                           = '
      f'{abs(idx_far - THIN_DISC_TEFF_INDEX):.5f}')
    P('  THE COMPARISON IS QUALITATIVE ON THE OBSERVATIONAL SIDE.  The')
    P('  review says "in reasonable accord" and prints no exponent and')
    P('  no error bar, so this CONFIRMS a shape and not a digit.  The')
    P('  module must say so; a check whose data has no error bar cannot')
    P('  be scored like Module 10\'s Podesta indices.')
    P('')
    P('  The index tends to -3/4 outward and is NOT -3/4 near the inner')
    P('  edge, where the bracket [1 - sqrt(R_in/R)] still bites.  The')
    P('  temperature has a MAXIMUM at R = (49/36) R_in, which is a')
    P('  derived number and not a fitted one:')
    R_peak = (49.0/36.0)*R_in_agn
    P(f'    R_max = (49/36) R_in    = {R_peak/Rg_agn:.6f} R_g')
    P(f'    T_eff there             = '
      f'{t_effective(Mdot_agn, M_AGN, R_peak, R_in_agn):.4f} K')
    grid = np.linspace(1.0001*R_in_agn, 4.0*R_in_agn, 200001)
    num_peak = grid[np.argmax(t_effective(Mdot_agn, M_AGN, grid, R_in_agn))]
    P(f'    numerical maximum       = {num_peak/R_in_agn:.6f} R_in '
      f'against 49/36 = {49.0/36.0:.6f}')

    # ---------------------------------------------------------------- G
    P('')
    P('PART G.  CHECK 3.  The radiative efficiency, and Module 9\'s 0.1')
    P('-'*74)
    eta_newt = efficiency_newtonian(ISCO_SCHWARZSCHILD_RG)
    P('  EIGHT NUMBERS IN THREE CLUSTERS: zero spin, maximal spin,')
    P('  and the value the quasar accounting needs.')
    P(f'    Newtonian thin disc at R_in = 6 R_g, DERIVED in PART F:')
    P(f'      eta = R_g/(2 R_in) = 1/12        = {eta_newt:.6f}')
    P(f'    Schwarzschild, COMPUTED from Bardeen, Press & Teukolsky')
    P(f'    (1972) eq. (2.12) at a = 0 and their eq. (2.21) r_ms = 6M:')
    P(f'      eta = 1 - E/mu = 1 - sqrt(8/9)   = '
      f'{ETA_SCHWARZSCHILD:.6f}')
    P(f'    Extreme Kerr, their eq. (2.14) at r_ms = M:')
    P(f'      eta = 1 - 1/sqrt(3)              = {ETA_KERR_EXTREME:.6f}')
    P(f'    Shakura & Sunyaev (1973) p. 339, printed by them:')
    P(f'      Schwarzschild                    = '
      f'{SS73_ETA_SCHWARZSCHILD:.6f}')
    P(f'      Kerr, "can attain 40%"           = '
      f'{SS73_ETA_KERR_MAX:.6f}')
    P(f'    Yu & Tremaine (2002), the value that CLOSES the Soltan')
    P(f'    accounting -- not a measurement with an error bar:')
    P(f'      eps                              = {YT02_EFFICIENCY:.6f}')
    P(f'      their luminous-QSO case, "possible for thin-disk')
    P(f'      accretion onto a Kerr BH"        = '
      f'{YT02_EFFICIENCY_KERR:.6f}')
    P(f'    module09.html:757, asserted in a SHIPPED page:')
    P(f'      eta_rad                          ~ {M09_ASSERTED_ETA:.6f}')
    P('')
    P('  TWO INDEPENDENT ROUTES AGREE, WHICH IS THE CHECK.')
    P(f'    derived Schwarzschild / their 0.06 = '
      f'{ETA_SCHWARZSCHILD/SS73_ETA_SCHWARZSCHILD:.4f}')
    P(f'    derived Kerr / their 40 per cent   = '
      f'{ETA_KERR_EXTREME/SS73_ETA_KERR_MAX:.4f}')
    P('    A 1972 orbit formula evaluated here and a 1973 sentence about')
    P('    the same two metrics agree to 5 per cent at both ends.')
    P('')
    P('  PUNCHLINE CHECK 3, AND THE VERDICT IS NOT FIXED AT STEP 2.')
    P(f'    The NEWTONIAN thin disc overstates the Schwarzschild value:')
    P(f'      (1/12)/(1 - sqrt(8/9))           = '
      f'{eta_newt/ETA_SCHWARZSCHILD:.4f}')
    P('    THIS BOOK IS NEWTONIAN, and that ratio is the price.  A')
    P('    Newtonian calculation at a radius six gravitational radii')
    P(f'    from a black hole gets the efficiency '
      f'{100*(eta_newt/ETA_SCHWARZSCHILD - 1.0):.1f} per cent too')
    P('    high, because')
    P('    it has no gravitational redshift and no relativistic binding')
    P('    energy.  Naming the number is the only honest way to use it.')
    P('')
    P(f'    Module 9\'s round 0.1 against the two zero-spin values:')
    P(f'      0.1/(1/12)                       = '
      f'{M09_ASSERTED_ETA/eta_newt:.4f}')
    P(f'      0.1/(1 - sqrt(8/9))              = '
      f'{M09_ASSERTED_ETA/ETA_SCHWARZSCHILD:.4f}')
    P('    0.1 is not a Schwarzschild thin-disc number.  Yu & Tremaine')
    P('    say so themselves: their 0.2 is "possible for thin-disk')
    P('    accretion onto a Kerr BH".  The population that closes the')
    P('    Soltan accounting at 0.1 contains spinning holes.')
    P('')
    P('  GATE D QUESTION 1, ANSWERED WITH MODULE 9\'S OWN RUN.')
    P(f'    m09_numbers.py prints L_X = {M09_LX:.1e} erg/s and')
    P(f'    Mdot c^2 = {M09_MDOT_C2:.3e} erg/s, so its eta is')
    P(f'    {M09_ETA_RAD:.4e}, which it prints as 4e-09.')
    P(f'    {"efficiency":<24} {"factor":>12} {"1 sig. fig.":>14}')
    for label, val in (('0.1, as shipped', M09_ASSERTED_ETA),
                       ('1/12, Newtonian', eta_newt),
                       ('1 - sqrt(8/9)', ETA_SCHWARZSCHILD),
                       ('0.06, S&S p. 339', SS73_ETA_SCHWARZSCHILD)):
        f = val/M09_ETA_RAD
        P(f'    {label:<24} {f:>12.4e} {f"{f:.0e}":>14}')
    P('    THE NEWTONIAN VALUE LEAVES module09.html:757 TRUE at one')
    P('    significant figure; the relativistic one would make it read')
    P('    1e7 and not 2e7.  No number in Module 9 depends on the factor')
    P('    -- it is the size of a refutation that stays a refutation --')
    P('    so the edit, if Gate D wants it, is one HTML cell and')
    P('    170c4da is the precedent.')

    # ---------------------------------------------------------------- H
    P('')
    P('PART H.  Self-gravity: the Toomre criterion')
    P('-'*74)
    P('  module05.html:764 printed "Omits the stabilisation of long')
    P('  wavelengths by rotation in a disc" and sent it here.  Module 5')
    P('  built the Jeans criterion without rotation; this is the same')
    P('  competition with rotation added.')
    P('')
    P('  For a steady alpha-disc the closed form of PART H gives')
    P('    Q = 3 alpha c_T^3/(G Mdot [1 - sqrt(R_in/R)]),')
    P('  in which Omega and R have both CANCELLED.  Q depends on the')
    P('  local temperature and on two global numbers, and on nothing')
    P('  else.')
    P('')
    P(f'  {"R/R_g":>10} {"T_eff (K)":>12} {"Sigma (g/cm^2)":>16} {"Q":>12}')
    alpha_agn = 0.1
    for x in [1.0e2, 1.0e3, 1.0e4, 1.0e5]:
        R = x*Rg_agn
        T = t_effective(Mdot_agn, M_AGN, R, R_in_agn)
        cT = isothermal_sound_speed(T, MU_IONISED_H)
        Om = kepler_omega(M_AGN, R)
        H = cT/Om
        nu = alpha_viscosity(alpha_agn, cT, H)
        Sig = nu_sigma_steady(Mdot_agn, R, R_in_agn)/nu
        Q = toomre_q_steady(alpha_agn, cT, Mdot_agn, R, R_in_agn)
        P(f'  {x:>10.4g} {T:>12.4f} {Sig:>16.4e} {Q:>12.4e}')
    P('')
    xs = np.logspace(2.0, 5.0, 300001)
    Rs = xs*Rg_agn
    Ts = t_effective(Mdot_agn, M_AGN, Rs, R_in_agn)
    Qs = toomre_q_steady(alpha_agn, isothermal_sound_speed(Ts, MU_IONISED_H),
                         Mdot_agn, Rs, R_in_agn)
    j = int(np.argmin(np.abs(np.log(Qs))))
    x_sg, R_sg = xs[j], Rs[j]
    P('')
    P(f'  Q = 1 at R = {x_sg:.1f} R_g = {R_sg:.4e} cm = '
      f'{R_sg/pc:.3e} pc')
    P(f'    Q there = {Qs[j]:.6f}, found on a 3e5-point log grid.')
    P('')
    P('  Q FALLS OUTWARD AND PASSES THROUGH 1.  Beyond that radius the')
    P('  disc is unstable to its own gravity and the thin steady solution')
    P('  of PART F does not describe it.')
    P('  THE MIDPLANE TEMPERATURE IS NOT T_eff.  An optically thick disc')
    P('  has T_mid^4 = (3 tau/4) T_eff^4 with tau = kappa Sigma/2, so the')
    P('  true c_T is LARGER and the true Q is LARGER, and the radius at')
    P('  which Q = 1 moves OUTWARD.  Using T_eff therefore gives a LOWER')
    P('  BOUND on that radius, and the module must print it as a bound.')
    P('  [NUMBER NOT YET COMPUTED: the optically thick correction.  Gate')
    P('  D decides whether this module carries it or states the bound.]')
    P('')
    P('  The protoplanetary row, where self-gravity is the physics of a')
    P('  real object rather than a caveat:')
    tt_row = census['protoplanetary, 10 au']
    kap_tt = epicyclic_frequency(tt_row['Om'], KEPLER_Q)
    Q_tt = toomre_q(tt_row['cT'], kap_tt, tt_row['Sigma'])
    q_tt_stellar = toomre_q(tt_row['cT'], kap_tt, tt_row['Sigma'],
                            TOOMRE_STELLAR_COEFF)
    P(f'    Q (gas, coefficient pi) = {Q_tt:.4f}')
    P(f'    Q (stellar, 3.36)       = '
      f'{q_tt_stellar:.4f}')
    P('    The two coefficients differ by 7 per cent and the module must')
    P('    not average them; the gas value is the one that applies.')
    Sigma_crit = tt_row['cT']*kap_tt/(TOOMRE_GAS_COEFF*G)
    P(f'    Sigma at which Q = 1    = {Sigma_crit:.4f} g cm^-2')
    P(f'    against the row\'s       = {tt_row["Sigma"]:.4f} g cm^-2')

    # ---------------------------------------------------------------- I
    P('')
    P('PART I.  Centrifugal support, and where gas circularises')
    P('-'*74)
    P('  module03.html:792 printed "Excludes centrifugal flattening and')
    P('  the rotational support of discs" and sent it here.')
    P(f'    Omega^2 R^3/(G M) for a Keplerian disc = '
      f'{centrifugal_flattening(Om_dn, M_WD, R_DN):.12f}')
    P('    EXACTLY ONE, at every radius, by construction.  A disc is not')
    P('    partly rotationally supported; radially it is supported by')
    P('    rotation and by nothing else.  Module 3\'s hydrostatic star has')
    P('    this ratio near zero, and that single number is the whole')
    P('    difference between the two objects.')
    P('')
    P('  module09.html:832 printed that Sgr A*\'s gas circularises near')
    P('  100 r_S.  As a number:')
    M_SGRA = 4.3e6*Msun         # NOT YET VERIFIED: Module 9 owns this mass
    r_S = 2.0*gravitational_radius(M_SGRA)
    R_circ = 100.0*r_S
    ell_needed = np.sqrt(G*M_SGRA*R_circ)
    P(f'    M (Module 9\'s value)    = {M_SGRA/Msun:.3e} M_sun'
      f'   NOT YET VERIFIED')
    P(f'    r_S = 2 G M/c^2         = {r_S:.4e} cm')
    P(f'    R_circ = 100 r_S        = {R_circ:.4e} cm')
    P(f'    ell required            = {ell_needed:.4e} cm^2 s^-1')
    P(f'    back through R = ell^2/GM = '
      f'{circularisation_radius(M_SGRA, ell_needed)/r_S:.6f} r_S')
    P('    STEP 2 MUST READ MODULE 9\'S MASS off module09.html rather than')
    P('    retyping 4.3e6 here.  Grep the other file before citing it.')

    # ---------------------------------------------------------------- J
    P('')
    P('PART J.  What supplies the stress: the link to Module 12 SS9')
    P('-'*74)
    P('  THE MRI IS NOT RE-DERIVED HERE.  module08.html:728 lists it')
    P('  among what Module 12 builds and module12.html:698 builds it.')
    P('  What this module owes Module 12 is the q that section assumed,')
    P('  and PART B has now supplied it.')
    P('')
    P(f'    gamma_max = (q/2) Omega, q from PART B = '
      f'{mri_growth_rate(Om_dn, q)/Om_dn:.10f} Omega')
    P(f'    Module 12 SS9\'s assumed value          = '
      f'{MRI_GROWTH_FACTOR:.10f} Omega')
    P(f'    difference                             = '
      f'{abs(mri_growth_rate(Om_dn, q)/Om_dn - MRI_GROWTH_FACTOR):.2e}')
    P('')
    P('  DOES THE UNSTABLE WAVELENGTH FIT INSIDE THE DISC?  The MRI needs')
    P('  lambda_max < 2H or the mode has nowhere to grow.  The field that')
    P('  supplies a given alpha is B ~ sqrt(4 pi alpha rho c_T^2), an')
    P('  ORDER-OF-MAGNITUDE identification and not a result.')
    P('')
    P('  THE CENSUS CANNOT ANSWER THIS, AND THE FIRST DRAFT PRETENDED IT')
    P('  COULD.  Every disc property cancels:')
    P('    lambda_max/(2H) = 4 pi sqrt(alpha)/sqrt(15),  a pure number.')
    for name in census:
        row = census[name]
        B = field_for_alpha(0.1, row['rho0'], row['cT'])
        vA = alfven_speed(B, row['rho0'])
        lam_mri = mri_wavelength_max(vA, row['Om'])
        P(f'    {name:<24} B = {B:.4e} G  ratio = '
          f'{lam_mri/(2.0*row["H"]):.6f}')
    P(f'    the identity                                  ratio = '
      f'{mri_containment_ratio(0.1):.6f}')
    _ns = [census[k]['n0'] for k in census]
    P(f'    Two discs {np.log10(max(_ns)/min(_ns)):.2f} decades apart in '
      f'midplane density give the')
    P('    SAME ratio to six figures.  That is the identity and not a')
    P('    coincidence, and a table of it would be decoration.')
    P('')
    P('  WHAT THE IDENTITY DOES SAY IS A BOUND.')
    a_max = alpha_max_for_containment()
    P(f'    lambda_max < 2H  requires  alpha < 15/(16 pi^2) = '
      f'{a_max:.6f}')
    P(f'    CHECK 2 inferred alpha      = {alpha_inferred:.4f}, which is '
      f'{alpha_inferred/a_max:.2f} times the bound.')
    P(f'    King, Pringle & Livio range {KPL07_ALPHA_LO}-'
      f'{KPL07_ALPHA_HI} lies ENTIRELY ABOVE it,')
    P(f'    by factors {KPL07_ALPHA_LO/a_max:.2f} to '
      f'{KPL07_ALPHA_HI/a_max:.2f}.')
    P('    So the equipartition identification B^2 ~ 4 pi alpha P is')
    P('    marginal exactly where the measured alpha lives.  THIS IS NOT')
    P('    A REFUTATION OF ANYTHING: it says the crude identification is')
    P('    at its limit, which is what an order-of-magnitude argument is')
    P('    entitled to be.  Gate D decides whether the module prints it.')

    # ---------------------------------------------------------------- K
    P('')
    P('PART K.  CHECK 4.  alpha is not a constant of nature')
    P('-'*74)
    P('  King, Pringle & Livio titled their paper with this question, and')
    P('  EVERY NUMBER BELOW IS FROM THAT ONE REVIEW.  A single-source')
    P('  comparison cannot be a disagreement between two papers.')
    P('')
    P(f'    {"system":<34} {"alpha":>14} {"kind":>14}')
    P(f'    {"thin, fully-ionised discs":<34} '
      f'{f"{KPL07_ALPHA_LO}-{KPL07_ALPHA_HI}":>14} {"a range":>14}')
    P(f'    {"soft X-ray transients (Dubus+01)":<34} '
      f'{"0.2-0.4":>14} {"a range":>14}')
    P(f'    {"T Tauri, 10-100 au (Hartmann+98)":<34} '
      f'{KPL07_ALPHA_PROTOSTELLAR:>14} {"a value":>14}')
    P(f'    {"AGN variability (Starling+04)":<34} '
      f'{f"{KPL07_AGN_ALPHA_LO}-{KPL07_AGN_ALPHA_HI}":>14} '
      f'{"LOWER LIMITS":>14}')
    P(f'    {"dwarf novae (their 2.1)":<34} '
      f'{f"{KPL07_DN_ALPHA_LO}-{KPL07_DN_ALPHA_HI}":>14} {"a range":>14}')
    P(f'    {"MHD simulations, no imposed field":<34} '
      f'{f"<= {KPL07_SIM_MAX}":>14} {"A BOUND":>14}')
    P('')
    P('  PUNCHLINE CHECK 4, AND THE VERDICT IS NOT FIXED AT STEP 2.')
    P('  TWO GAPS, AND THE SECOND IS THE ONE THE PAPER IS ABOUT.')
    lo = np.log10(KPL07_ALPHA_LO/KPL07_ALPHA_PROTOSTELLAR)
    hi = np.log10(KPL07_ALPHA_HI/KPL07_ALPHA_PROTOSTELLAR)
    P(f'    (a) ACROSS DISC CLASSES.  Fully-ionised over protostellar =')
    P(f'        {KPL07_ALPHA_LO/KPL07_ALPHA_PROTOSTELLAR:.0f} to '
      f'{KPL07_ALPHA_HI/KPL07_ALPHA_PROTOSTELLAR:.0f}, that is '
      f'{lo:.2f} to {hi:.2f} decades.')
    P('        The two classes differ in ionisation, so this gap has a')
    P('        candidate physical cause and is not a contradiction.')
    P(f'    (b) OBSERVATION AGAINST SIMULATION, on the SAME class of')
    P(f'        disc.  {KPL07_ALPHA_LO}-{KPL07_ALPHA_HI} observed against '
      f'a simulated alpha <= {KPL07_SIM_MAX}:')
    P(f'        AT LEAST {KPL07_ALPHA_LO/KPL07_SIM_MAX:.0f} and at least '
      f'{np.log10(KPL07_ALPHA_LO/KPL07_SIM_MAX):.2f} decades, ONE-SIDED,')
    P('        because their section 5 states the simulation side as a')
    P('        BOUND and not a value.  Their own abstract calls it "an')
    P('        order of magnitude smaller".')
    P('        THE DIRECTION CUTS BOTH WAYS AND THE PAPER SAYS SO: their')
    P('        section 4 notes that the limitations of the simulations')
    P('        "would indeed tend to lead to UNDERESTIMATING the value of')
    P('        alpha", so the gap is an upper estimate of a lower bound.')
    P('        THE SIMULATIONS ARE OF THE MAGNETOROTATIONAL INSTABILITY')
    P('        OF MODULE 12 SS9.  So the mechanism this book derives does')
    P('        not, in the simulations that solve it, reach the alpha the')
    P('        observations need -- and the same authors say the')
    P('        simulations are the side more likely to be wrong.')
    P('')
    P('    A BOUND HAS A DIRECTION.  Starling et al.\'s AGN row is a set')
    P('    of LOWER limits, so it cannot be read as an alpha near 0.02;')
    P('    it says only that alpha is at least that.  It is recorded and')
    P('    is used in no check.')
    P('    WHAT IS REFUTED is not the prescription -- nu = alpha c_T H')
    P('    remains a definition of alpha -- but the reading of alpha as a')
    P('    constant of nature.  Shakura & Sunyaev never claimed it was')
    P(f'    one: their bound is alpha <~ {SS73_ALPHA_MAX:.0f}, and their')
    P('    own footnote 3 says the disc\'s observational appearance "do')
    P('    not strongly depend on the chosen value of alpha".')

    # ---------------------------------------------------------------- L
    P('')
    P('PART L.  The nine problems')
    P('-'*74)
    P('  Every number a solution prints is produced here.  The slots and')
    P('  the modelling inputs are fixed by .ignore/m11-gate-d.md.')

    P('')
    P('  C1.  The epicyclic frequency, and the Rayleigh boundary')
    for qq in (0.0, 1.0, KEPLER_Q, 1.9, RAYLEIGH_Q_CRIT):
        P(f'    q = {qq:<4} kappa_ep/Omega = '
          f'{epicyclic_frequency(1.0, qq):.6f}')
    P(f'    kappa_ep^2 = 2 Omega^2 (2 - q) vanishes at q = '
      f'{RAYLEIGH_Q_CRIT:.1f}, so a disc')
    P('    is Rayleigh-unstable only for q > 2, which a point mass cannot')
    P('    produce.  A rigidly rotating fluid has q = 0 and')
    P(f'    kappa_ep = 2 Omega; Keplerian q = 3/2 gives exactly Omega.')

    P('')
    P('  C2.  The protoplanetary row at alpha = 0.01')
    tt = census['protoplanetary, 10 au']
    a_c2 = KPL07_ALPHA_PROTOSTELLAR
    nu_c2 = alpha_viscosity(a_c2, tt['cT'], tt['H'])
    tnu_c2 = viscous_time(tt['R'], nu_c2)
    P(f'    c_T                     = {tt["cT"]/1e5:.6f} km/s')
    P(f'    Omega                   = {tt["Om"]:.6e} s^-1')
    P(f'    H                       = {tt["H"]:.6e} cm '
      f'= {tt["H"]/AU:.6f} au')
    P(f'    H/R                     = {tt["H"]/tt["R"]:.6f}')
    P(f'    rho_0                   = {tt["rho0"]:.6e} g cm^-3')
    P(f'    nu = alpha c_T H        = {nu_c2:.6e} cm^2 s^-1')
    P(f'    t_nu = R^2/nu           = {tnu_c2:.6e} s '
      f'= {tnu_c2/yr:.6e} yr')
    P(f'    alpha is Hartmann et al. (1998) through King, Pringle &')
    P(f'    Livio section 2.3.2, at 10-100 au.  This row is at 10 au.')

    P('')
    P('  C3.  Where the steady disc is hottest')
    P(f'    R_max/R_in              = {49.0/36.0:.6f}  (= 49/36)')
    P(f'    R_max                   = {R_peak/Rg_agn:.6f} R_g '
      f'= {R_peak:.6e} cm')
    T_peak = t_effective(Mdot_agn, M_AGN, R_peak, R_in_agn)
    P(f'    T_eff(R_max)            = {T_peak:.4f} K')
    P(f'    T_eff at R_in           = 0 exactly, because f vanishes there')
    P(f'    numerical maximum       = {num_peak/R_in_agn:.6f} R_in')

    P('')
    P('  D2.  Three times the local release')
    P('    The specific orbital energy is -G M/2R, so matter moving in')
    P('    releases G M Mdot/(2R^2) dR over an annulus, and the annulus')
    P('    has area 2 x 2 pi R dR.  Per unit area PER SIDE that is')
    P('      G M Mdot/(8 pi R^3),')
    P('    against a dissipation of (3 G M Mdot/8 pi R^3) f.')
    P(f'    {"R/R_in":>10} {"ratio D/(local release)":>26}')
    for x in (1.5, 2.0, 10.0, 1.0e2, 1.0e4):
        R = x*R_in_agn
        local = G*M_AGN*Mdot_agn/(8.0*np.pi*R**3)
        P(f'  {x:>12.4g} '
          f'{dissipation_per_area(Mdot_agn, M_AGN, R, R_in_agn)/local:>26.6f}')
    P('    The limit is 3.  ONE of those three units is the energy')
    P('    released locally; the other TWO are carried out to this radius')
    P('    by the viscous torque of P3, from material further in.  Energy')
    P('    is not conserved annulus by annulus, and that is the whole')
    P('    content of the bracket f.')
    P('    Below R = 9/4 R_in exactly -- set 3(1 - sqrt(R_in/R)) = 1 --')
    P('    the ratio is LESS than 1: those annuli')
    P('    radiate less than they release, because they are exporting')
    P('    energy outward rather than importing it.')

    P('')
    P('  K1.  The protoplanetary disc is MOLECULAR, so the plasma')
    P('       formula does not apply')
    sigma_H2 = SIGMA_NEUTRAL
    lam_k1 = 1.0/(tt['n0']*sigma_H2)
    vth_k1 = v_thermal(tt['T'], tt['mu'])
    nu_k1 = lam_k1*vth_k1/3.0
    tnu_k1 = viscous_time(tt['R'], nu_k1)
    P(f'    n                       = {tt["n0"]:.6e} cm^-3')
    P(f'    sigma (neutral, Module 1)= {sigma_H2:.1e} cm^2')
    P(f'    lambda = 1/(n sigma)    = {lam_k1:.6e} cm')
    P(f'    v_th at 50 K, mu = 2.34 = {vth_k1/1e5:.6f} km/s')
    P(f'    nu_mol = v_th lambda/3  = {nu_k1:.6e} cm^2 s^-1')
    P(f'    t_nu = R^2/nu_mol       = {tnu_k1:.6e} s '
      f'= {tnu_k1/yr:.6e} yr')
    P(f'    against C2 at alpha = {a_c2}: a factor '
      f'{tnu_k1/tnu_c2:.6e},')
    P(f'    that is {np.log10(tnu_k1/tnu_c2):.2f} decades.')
    P('    AND THE TRAP: lam_coulomb is a PLASMA formula.  Using it at')
    P('    50 K in a molecular gas is meaningless, because there are no')
    P('    free charges to deflect.  The neutral cross-section above is')
    P('    Module 1\'s order-of-magnitude value and the problem says so.')

    P('')
    P('  K2.  A thin disc at Sgr A*, on Module 9\'s own accretion rate')
    Mdot_sgra = M09_MDOT_C2/(c*c)
    M_sgra = M09_BH_MASS_G
    Rin_sgra = ISCO_SCHWARZSCHILD_RG*gravitational_radius(M_sgra)
    L_thin = disc_luminosity(Mdot_sgra, M_sgra, Rin_sgra)
    P(f'    M (module09.html:672)   = {M_sgra:.4e} g '
      f'= {M_sgra/Msun:.4e} M_sun')
    P(f'    Mdot = (Mdot c^2)/c^2   = {Mdot_sgra:.6e} g/s')
    P(f'    R_in = 6 R_g            = {Rin_sgra:.6e} cm')
    P(f'    L = G M Mdot/(2 R_in)   = {L_thin:.6e} erg/s')
    P(f'    eta implied             = {L_thin/(Mdot_sgra*c*c):.6f} '
      f'(= 1/12 = {1.0/12.0:.6f})')
    P(f'    observed L_X            = {M09_LX:.4e} erg/s')
    P(f'    ratio L_thin/L_X        = {L_thin/M09_LX:.6e}')
    P(f'    that is {np.log10(L_thin/M09_LX):.2f} decades.  Module 9')
    P(f'    prints the same refutation as a factor of '
      f'{M09_PRINTED_FACTOR:.0e}, from')
    P('    the efficiency rather than the luminosity; the two routes are')
    P('    the same arithmetic and must agree.')

    P('')
    P('  K3.  The alpha at which the MRI outgrows the disc')
    P(f'    lambda_max/(2H) = 4 pi sqrt(alpha)/sqrt(15) = 1 at')
    P(f'      alpha = 15/(16 pi^2)  = {a_max:.6f}')
    P(f'    dwarf novae (KPL07 2.1) = {KPL07_DN_ALPHA_LO}-'
      f'{KPL07_DN_ALPHA_HI}')
    P(f'      ratios to the bound   = {KPL07_DN_ALPHA_LO/a_max:.4f} to '
      f'{KPL07_DN_ALPHA_HI/a_max:.4f}')
    P(f'    protostellar            = {KPL07_ALPHA_PROTOSTELLAR}')
    P(f'      ratio to the bound    = '
      f'{KPL07_ALPHA_PROTOSTELLAR/a_max:.4f}, INSIDE it')
    P('    So the crude equipartition identification is self-consistent')
    P('    in protostellar discs and marginal in ionised ones, which is')
    P('    the same split CHECK 4 measures -- and the module must not')
    P('    claim that is more than a coincidence of two crude numbers.')

    P('')
    P('=' * 74)
    P('END OF STEP 2.  FIVE PAPERS FETCHED AND READ; THREE FINDINGS')
    P('CHANGED WHAT THIS MODULE MAY PRINT.')
    P('  1. Shakura & Sunyaev\'s alpha is v_t/v_s + H^2/(4 pi rho v_s^2),')
    P('     a SUM of two terms, and THEIR H IS THE MAGNETIC FIELD.  Step')
    P('     1 described it as a stress proportional to the pressure,')
    P('     which is the later restatement and not their equation.')
    P('  2. TOOMRE (1964) DOES NOT CONTAIN THE GAS CRITERION.  His')
    P('     p. 1217 says he ignores the gas and treats a disc "composed')
    P('     only of stars"; his 3.36 is eq. (65) and is for stars.  The')
    P('     pi is now DERIVED from the dispersion relation instead.')
    P('  3. Bardeen, Press & Teukolsky print NO efficiency.  The')
    P('     Schwarzschild value is computed from their eq. (2.12), and')
    P('     their general formula divides by zero at extreme Kerr, which')
    P('     is why eq. (2.14) has its own function.')
    P('')
    P('AND ONE CONSTANT STEP 1 INVENTED: KPL07_ALPHA_QUIESCENT = 0.01,')
    P('called a quiescent dwarf-nova value.  The 0.01 in that paper is')
    P('the PROTOSTELLAR value of Hartmann et al.  Removed.')
    P('Flaherty et al. (2018) was not fetched and is not needed: King,')
    P('Pringle & Livio supply the protostellar number themselves, so')
    P('CHECK 4 is a SINGLE-SOURCE comparison.')
    P('')
    P('WHAT IS STILL UNSOURCED, AND GATE D MUST RULE ON IT:')
    P('  The dwarf-nova parameters -- 0.6 M_sun, 1e10 cm, 3e4 K,')
    P('  100 g/cm^2, a 5-day outburst.  NO NAMED SYSTEM WAS FETCHED, so')
    P('  CHECK 2 is a class CONFIGURATION in the sense')
    P('  module07.html:453 uses the phrase, and its alpha may not be')
    P('  called a measurement.  Gate D sources a named dwarf nova or')
    P('  says this in print.')
    P('  The full record is .ignore/m11-source-verification.md.')
    P('=' * 74)


if __name__ == '__main__':
    main()
