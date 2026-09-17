"""Verify every number quoted in the Module 4 problem solutions.

Run from afd/figs.  Each block prints the values the solution quotes and
asserts the ones that must hold exactly.
"""
import numpy as np

import m04_numbers as M

g_sun = M.GMsun/M.RSUN_TAB**2
ssm = M.load_ssm()
mu_n = M.mu_neutral(ssm['X'][-1], ssm['Y'][-1])

print('C1  adiabatic versus isothermal in air')
cL = M.c_adiabatic(M.T_AIR, M.MU_AIR, M.GAMMA_AIR)
nu_eq = cL**2/(2*np.pi*M.CHI_AIR)
print(f'    chi = {M.CHI_AIR:.4f} cm^2/s; omega chi/c^2 at 1 kHz = '
      f'{2*np.pi*1e3*M.CHI_AIR/cL**2:.3e}')
print(f'    equality at {nu_eq:.3e} Hz, wavelength {cL/nu_eq*1e7:.0f} nm, '
      f'{cL/nu_eq/M.LAM_AIR:.2f} mean free paths')
print(f'    Kn at that wavelength (lambda_mfp / (wavelength/2pi)) = '
      f'{M.LAM_AIR/(cL/nu_eq/(2*np.pi)):.2f}')

print('C2 / K3  the 5-minute modes above the photosphere')
nu_ac, c, H = M.nu_cutoff(M.TEFF_SUN, mu_n, 5/3, g_sun)
for nu in (M.NUMAX_MEAS, 2000e-6):
    kap = np.sqrt((2*np.pi*nu_ac)**2 - (2*np.pi*nu)**2)/c
    print(f'    nu = {nu*1e6:.0f} microHz: kappa = {kap*1e8:.3f} /Mm, '
          f'energy e-fold 1/(2 kappa) = {1/(2*kap)/1e5:.1f} km = '
          f'{1/(2*kap)/H:.3f} H; velocity exponent 1/(2H) - kappa = '
          f'{(1/(2*H) - kap)*1e8:.3f} /Mm')
print(f'    H = {H/1e5:.1f} km, 1/(2H) = {1/(2*H)*1e8:.3f} /Mm')

print('D1  amplitude growth above the cutoff')
for dz in (500e5, 1000e5):
    print(f'    over {dz/1e5:.0f} km: velocity factor exp(dz/2H) = '
          f'{np.exp(dz/(2*H)):.1f}, density factor exp(-dz/H) = '
          f'{np.exp(-dz/H):.3e}')

print('D2  cutoff scaling nu_ac = Gamma_1 g / (4 pi c)')
nu_alt = 5/3*g_sun/(4*np.pi*c)
print(f'    Gamma_1 g/(4 pi c) = {nu_alt*1e6:.1f} microHz, '
      f'c/(4 pi H) = {nu_ac*1e6:.1f} microHz')
assert abs(nu_alt/nu_ac - 1) < 1e-12

print('D3  large separation and mean density')
M_sun = M.GMsun/M.G
rhobar = 3*M_sun/(4*np.pi*M.RSUN_TAB**3)
k = M.DNU_MEAS/np.sqrt(M.G*rhobar)
print(f'    rhobar (table radius) = {rhobar:.4f} g/cm^3, sqrt(G rhobar) = '
      f'{np.sqrt(M.G*rhobar):.4e} /s, Delta nu / sqrt(G rhobar) = {k:.4f}')
dnu_as = (1 + M.ZETA_SUN)*M.DNU_MEAS
print(f'    with the asymptotic value: {dnu_as/np.sqrt(M.G*rhobar):.4f}')
rho_rg = 1.2*M_sun/(4/3*np.pi*(10*M.RSUN_TAB)**3)
print(f'    red giant 1.2 Msun, 10 Rsun: rhobar = {rho_rg:.4e}, '
      f'Delta nu = {M.DNU_MEAS*np.sqrt(rho_rg/rhobar)*1e6:.2f} microHz')

print('K1  sound in helium at 0 C')
MU_HE = 4.002602
cHe = M.c_adiabatic(M.T_AIR, MU_HE, 5/3)
cHeN = M.c_isothermal(M.T_AIR, MU_HE)
print(f'    Laplace {cHe/100:.2f} m/s, Newton {cHeN/100:.2f} m/s, '
      f'ratio {cHe/cHeN:.4f} = sqrt(5/3) {np.sqrt(5/3):.4f}')
print(f'    helium / air (Laplace) = {cHe/cL:.4f}')
print(f'    check: sqrt((5/3)/1.4 * 28.9647/4.002602) = '
      f'{np.sqrt((5/3)/1.4*M.MU_AIR/MU_HE):.4f}')

print('K2  a red giant')
g_rg = 1.2*M.GMsun/(10*M.RSUN_TAB)**2
nu_rg, c_rg, H_rg = M.nu_cutoff(4800.0, mu_n, 5/3, g_rg)
print(f'    g = {g_rg:.1f} cm/s^2, c = {c_rg/1e5:.3f} km/s, H = '
      f'{H_rg/1e5:.0f} km, nu_ac = {nu_rg*1e6:.1f} microHz')
print(f'    ratio to solar {nu_rg/nu_ac:.5f}; check g ratio * sqrt(T ratio) = '
      f'{(g_rg/g_sun)*np.sqrt(M.TEFF_SUN/4800):.5f}')
numax_rg = M.NUMAX_MEAS*nu_rg/nu_ac
print(f'    nu_max by proportion = {numax_rg*1e6:.1f} microHz, period '
      f'{1/numax_rg/3600:.2f} h')
