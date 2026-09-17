"""Verify every number quoted in the Module 3 problem solutions.

Run from afd/figs.  Each block prints the quantities that appear in one
solution, in the order the solution quotes them.  Nothing in
afd/module03.html Section 12 may state a number this script does not
print.  Two arithmetic errors were caught this way in Module 1.

Constants and helpers come from m03_numbers.py, so a problem cannot
drift away from the body of the module.
"""
import numpy as np

import m03_numbers as M

P = print
P('=' * 74)
P('MODULE 3 PROBLEM-SET CHECK')
P('=' * 74)

# ---------------------------------------------------------------- C1
P('')
P('C1.  What the virial ratio can and cannot confirm')
P('-'*74)
ssm0 = M.load_ssm()
lhs, rhs, vr = M.virial_check(ssm0, M.Msun)
P(f'  3 int P dV                         = {lhs:.4e} erg')
P(f'  -Omega                             = {rhs:.4e} erg')
P(f'  ratio                              = {vr:.5f}')

# ---------------------------------------------------------------- C3
P('')
P('C3.  Where the plane-parallel scale height stops meaning anything')
P('-'*74)
T_icm, mu_icm = 1e8, 0.6
M_cl, r_cl = 5e14*M.Msun, 1e3*M.kpc
H_icm = M.scale_height_self_grav(T_icm, mu_icm, M_cl, r_cl)
P(f'  ICM H                              = {H_icm/M.kpc:.0f} kpc '
  f'= {H_icm/r_cl:.2f} r')
P(f'  g(r+H)/g(r) for a point mass       = {(r_cl/(r_cl+H_icm))**2:.3f}')
g_sun = M.GMsun/M.Rsun**2
H_ph = M.scale_height(5772.0, 1.30, g_sun)
P(f'  photosphere H/R                    = {H_ph/M.Rsun:.2e}')
P(f'  g(R+H)/g(R) at the photosphere     = '
  f'{(M.Rsun/(M.Rsun+H_ph))**2:.6f}')

# ---------------------------------------------------------------- C2
P('')
P('C2.  Why T_c survives when rho_c and P_c do not')
P('-'*74)
ssm = M.load_ssm()
rhoc, Pc, Tc = ssm['rho'][0], ssm['P'][0], ssm['T'][0]
rhobar = 3.0*M.Msun/(4.0*np.pi*M.RSUN_TAB**3)
c3 = M.polytrope_constants(3.0)
rho_pred = c3['D']*rhobar
P_pred = c3['W']*M.G*M.Msun**2/M.RSUN_TAB**4
P(f'  rho ratio                          = {rho_pred/rhoc:.4f}')
P(f'  P ratio                            = {P_pred/Pc:.4f}')
P(f'  T ratio, being P ratio / rho ratio = '
  f'{(P_pred/Pc)/(rho_pred/rhoc):.4f}')
P(f'  the module quotes                  = 1.0486')
P('  READ: the T ratio is the quotient of the other two.  The two')
P('  errors are in the same direction, so most of each cancels.')

# ---------------------------------------------------------------- D1
P('')
P('D1.  The mass-radius relation of a polytrope')
P('-'*74)
P('  R ~ M^((1-n)/(3-n)) for n != 3.  Exponents:')
for n in (0.0, 1.0, 1.5, 2.0, 2.5, 4.0):
    P(f'    n = {n:.1f}   exponent = {(1.0-n)/(3.0-n):+.4f}')
P('  n = 1:  exponent 0, so R does not depend on M at all.')
P('  n = 3:  the exponent is singular.  M drops out of the radius')
P('          relation instead: M is fixed by K alone.')
P('  n = 3/2 (a non-relativistic white dwarf): exponent '
  f'{(1.0-1.5)/(3.0-1.5):+.4f} = -1/3, the classical R ~ M^(-1/3).')

# ---------------------------------------------------------------- D2
P('')
P('D2.  Chandrasekhar\'s bound for a white dwarf')
P('-'*74)
M_wd, R_wd = 0.6*M.Msun, 0.013*M.RSUN_TAB
bound_wd = M.G*M_wd**2/(8.0*np.pi*R_wd**4)
bound_sun = M.G*M.Msun**2/(8.0*np.pi*M.RSUN_TAB**4)
P(f'  M = 0.6 Msun                       = {M_wd:.4e} g')
P(f'  R = 0.013 Rsun                     = {R_wd:.4e} cm = '
  f'{R_wd/1e5:.0f} km')
P(f'  bound P_c >= G M^2/(8 pi R^4)      = {bound_wd:.4e} dyn/cm^2')
P(f'  the Sun\'s bound, for comparison    = {bound_sun:.4e} dyn/cm^2')
P(f'  ratio of the two bounds            = {bound_wd/bound_sun:.4e}')
P(f'  check: (0.6)^2/(0.013)^4           = '
  f'{0.6**2/0.013**4:.4e}')
P(f'  the Sun\'s tabulated P_c            = {Pc:.4e} dyn/cm^2')
P(f'  the Sun exceeds its own bound by   = {Pc/bound_sun:.1f}')

# ---------------------------------------------------------------- D3
P('')
P('D3.  The Sun with the pressure switched off')
P('-'*74)
tff = M.t_freefall(rhobar)
P(f'  mean density rhobar                = {rhobar:.4f} g/cm^3')
P(f'  t_ff = sqrt(3 pi/(32 G rhobar))    = {tff:.1f} s = {tff/60:.1f} min')
P(f'  the coefficient sqrt(3 pi/32)      = {np.sqrt(3*np.pi/32):.4f}')
P(f'  the naive R/sqrt(GM/R^2) estimate  = '
  f'{np.sqrt(M.RSUN_TAB**3/M.GMsun):.1f} s')
P(f'  ratio of the exact result to it    = '
  f'{tff/np.sqrt(M.RSUN_TAB**3/M.GMsun):.4f}')
P(f'  exact ratio pi/(2 sqrt 2)          = {np.pi/(2*np.sqrt(2)):.4f}')

# ---------------------------------------------------------------- K1
P('')
P('K1.  Scale heights of Mars and Venus')
P('-'*74)
cases = [('Earth', M.ISA_T0, M.mu_air, M.g_earth),
         ('Mars', 210.0, 43.34, 371.0),
         ('Venus', 737.0, 43.45, 887.0)]
H = {}
for name, T, mu, g in cases:
    H[name] = M.scale_height(T, mu, g)
    P(f'  {name:6s} T = {T:6.2f} K  mu = {mu:7.4f}  g = {g:7.3f} cm/s^2'
      f'   H = {H[name]/1e5:7.3f} km')
P(f'  Mars  / Earth                      = {H["Mars"]/H["Earth"]:.4f}')
P(f'  Venus / Earth                      = {H["Venus"]/H["Earth"]:.4f}')
P(f'  Venus / Mars                       = {H["Venus"]/H["Mars"]:.4f}')
P('  READ: Mars and Venus have mu within 0.25 per cent, so T/g sets')
P('  the ratio of their scale heights and mu corrects it slightly.')
P(f'  T ratio {737.0/210.0:.4f} divided by g ratio {887.0/371.0:.4f} = '
  f'{(737.0/210.0)/(887.0/371.0):.4f}')
P(f'  mu ratio Venus/Mars                = {43.45/43.34:.5f}')
P(f'  (T/g ratio) / (mu ratio)           = '
  f'{(737.0/210.0)/(887.0/371.0)/(43.45/43.34):.4f}')

# ---------------------------------------------------------------- K2
P('')
P('K2.  The n = 1 polytrope as a neutron-star toy')
P('-'*74)
c1 = M.polytrope_constants(1.0)
M_ns, R_ns = 1.4*M.Msun, 12.0e5
# n = 1: a^2 = K/(2 pi G) and R = pi a, so K = 2 G R^2/pi.
K_ns = 2.0*M.G*R_ns**2/np.pi
rhoc_ns = np.pi*M_ns/(4.0*R_ns**3)
rhobar_ns = 3.0*M_ns/(4.0*np.pi*R_ns**3)
P(f'  M = 1.4 Msun                       = {M_ns:.4e} g')
P(f'  R = 12 km                          = {R_ns:.4e} cm')
P(f'  xi_1 for n = 1                     = {c1["xi1"]:.6f}  (exact pi = '
  f'{np.pi:.6f})')
P(f'  K = 2 G R^2/pi                     = {K_ns:.4e} cgs')
P(f'  rho_c = pi M/(4 R^3)               = {rhoc_ns:.4e} g/cm^3')
P(f'  rhobar = 3M/(4 pi R^3)             = {rhobar_ns:.4e} g/cm^3')
P(f'  rho_c/rhobar                       = {rhoc_ns/rhobar_ns:.4f}')
P(f'  the table\'s D for n = 1            = {c1["D"]:.4f}')
P(f'  exact pi^2/3                       = {np.pi**2/3.0:.4f}')
rho_sat = 0.16e39*M.mu_u     # 0.16 nucleons per fm^3
P(f'  nuclear saturation density         = {rho_sat:.3e} g/cm^3')
P(f'  rho_c in units of it               = {rhoc_ns/rho_sat:.2f}')
P(f'  P_c = K rho_c^2                    = {K_ns*rhoc_ns**2:.4e} dyn/cm^2')
P(f'  Chandrasekhar bound G M^2/(8 pi R^4) = '
  f'{M.G*M_ns**2/(8*np.pi*R_ns**4):.4e} dyn/cm^2')
P(f'  P_c / bound                        = '
  f'{K_ns*rhoc_ns**2/(M.G*M_ns**2/(8*np.pi*R_ns**4)):.2f}')
P(f'  the table\'s W for n = 1            = {c1["W"]:.5f}')
P(f'  W x 8 pi, which must equal P_c/bound = {c1["W"]*8*np.pi:.2f}')

# ---------------------------------------------------------------- K3
P('')
P('K3.  Eddington\'s quartic: how 1 - beta depends on mass')
P('-'*74)
P('  For n = 3, M = 4 pi (K/(pi G))^(3/2) (-xi_1^2 theta_1\'), so K is')
P('  fixed by M alone, and Eddington\'s K fixes beta:')
P('    K = [(3/a) (1-beta)/beta^4]^(1/3) (k/(mu m_u))^(4/3)')


def beta_of_mass(Msolar, mu):
    """Solve Eddington's quartic for beta at a given mass."""
    Mtot = Msolar*M.Msun
    K = np.pi*M.G*(Mtot/(4.0*np.pi*c3["mu1"]))**(2.0/3.0)
    # (1-beta)/beta^4 = (a/3) K^3 (mu m_u/k)^4
    rhs = (M.a_rad/3.0)*K**3*(mu*M.mu_u/M.kB)**4
    lo, hi = 1e-12, 1.0 - 1e-15
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if (1.0 - mid)/mid**4 > rhs:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo + hi), K, rhs


MU_STAR = 0.8320
P(f'  -xi_1^2 theta_1\' for n = 3         = {c3["mu1"]:.5f}')
P(f'  mu taken as the Sun\'s central value = {MU_STAR}')
for Msolar in (1.0, 10.0, 50.0):
    b, K, rhs = beta_of_mass(Msolar, MU_STAR)
    P(f'  M = {Msolar:5.1f} Msun   K = {K:.4e}   (1-beta)/beta^4 = '
      f'{rhs:.4e}')
    P(f'                   beta = {b:.6f}   1 - beta = {1.0-b:.4e}')
b1 = beta_of_mass(1.0, MU_STAR)[0]
b10 = beta_of_mass(10.0, MU_STAR)[0]
b50 = beta_of_mass(50.0, MU_STAR)[0]
P(f'  (1-beta) at 10 Msun / at 1 Msun    = '
  f'{(1.0-b10)/(1.0-b1):.1f}')
P(f'  the table\'s central 1 - beta for the Sun = 6.194e-04')
P(f'  Eddington\'s 1 - beta at 1 Msun     = {1.0-b1:.4e}')
P(f'  ratio                              = {(1.0-b1)/6.194e-4:.2f}')
P('  READ: n = 3 needs beta constant, not large.  At 1 Msun the')
P(f'  quartic gives {100*(1.0-b1):.2f} per cent, at 10 Msun '
  f'{100*(1.0-b10):.1f} per cent, at 50 Msun '
  f'{100*(1.0-b50):.0f} per cent.')

P('')
P('=' * 74)
P('All problem-set numbers above.  Section 12 quotes no other.')
P('=' * 74)
