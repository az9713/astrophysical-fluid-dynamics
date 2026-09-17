"""Verify every number quoted in the Module 5 problem solutions.

Run from afd/figs.  Each block prints the values the solution quotes and
asserts the ones that must hold exactly.
"""
import numpy as np

import m05_numbers as M

yr, AU, pc, Msun, G = M.yr, M.AU, M.pc, M.Msun, M.G

print('C1  isothermal against adiabatic Jeans mass')
T, rho = 8000.0, M.rho_from_nH(0.5)
mj_iso = M.mass_jeans(M.sound_speed(T, M.MU_HI), rho)
mj_ad = M.mass_jeans(M.sound_speed_ad(T, M.MU_HI), rho)
print(f'    M_J iso = {mj_iso/Msun:.3e}, adiabatic = {mj_ad/Msun:.3e}, '
      f'ratio {mj_ad/mj_iso:.4f}, (5/3)^1.5 = {(5/3)**1.5:.4f}')
assert abs(mj_ad/mj_iso - (5/3)**1.5) < 1e-12
rho1 = M.rho_from_nH2(1e4)
cs1 = M.sound_speed(10.0, M.MU_MOL)
print(f'    10 K core: M_J = {M.mass_jeans(cs1, rho1)/Msun:.4f}, adiabatic '
      f'{M.mass_jeans(M.sound_speed_ad(10.0, M.MU_MOL), rho1)/Msun:.4f}')

print('C2  two spheres of nearly equal mass')
for x in (6.0, 7.0):
    print(f'    xi = {x}: m = {M.be_m(x):.5f}, contrast = {M.be_contrast(x):.3f}')
print(f'    mass difference {(M.be_m(6.0)/M.be_m(7.0)-1)*100:.3f} per cent, '
      f'contrast ratio {M.be_contrast(7.0)/M.be_contrast(6.0):.4f}')
xc, mc, cc = M.be_critical()
print(f'    xi_crit {xc:.4f}, contrast {cc:.4f}')

print('C3  the swindle ratio in two media')
for T_, mu, r_ in ((10.0, M.MU_MOL, rho1), (8000.0, M.MU_HI, rho)):
    cs = M.sound_speed(T_, mu)
    g, t = M.swindle_residual(r_, M.lambda_jeans(cs, r_))
    print(f'    g = {g:.4e}, crossing {t/yr:.4e} yr, t_grow '
          f'{M.t_grow(r_)/yr:.4e} yr, ratio {t/M.t_grow(r_):.4f}')
    assert abs(t/M.t_grow(r_) - np.sqrt(3.0)) < 1e-10

print('D1  free fall')
r = M.tff_over_tgrow()
print(f'    pi sqrt(3/8) = {np.pi*np.sqrt(3/8):.6f}; script {r:.6f}')
assert abs(r - np.pi*np.sqrt(3/8)) < 1e-12
print(f'    10 K core: t_ff = {M.t_freefall(rho1)/yr:.4e} yr, '
      f't_grow = {M.t_grow(rho1)/yr:.4e} yr')

print('D2  the isothermal sheet')
H = cs1/np.sqrt(8*np.pi*G*rho1)
Sig = 4*rho1*H
kc = 2*np.pi*G*Sig/cs1**2
print(f'    H = {H/AU:.1f} AU, Sigma = {Sig:.4e} g/cm^2 = '
      f'{Sig*pc**2/Msun:.1f} Msun/pc^2')
print(f'    k_crit H = {kc*H:.6f}; lambda_crit = {2*np.pi/kc/pc:.5f} pc = '
      f'{2*np.pi/kc/AU:.0f} AU; 2 pi H = {2*np.pi*H/AU:.0f} AU')
assert abs(kc*H - 1.0) < 1e-12
smax = np.pi*G*Sig/cs1
print(f'    fastest lambda = {4*np.pi/kc/pc:.5f} pc, s_max = {smax:.4e} /s, '
      f'1/s_max = {1/smax/yr:.4e} yr, ratio to t_grow '
      f'{1/smax/M.t_grow(rho1):.4f} = sqrt(2) {np.sqrt(2):.4f}')
z = np.linspace(-10*H, 10*H, 20001)
prof = rho1/np.cosh(z/(2*H))**2
lnr = np.log(prof)
d2 = np.gradient(np.gradient(lnr, z), z)
res = np.max(np.abs(cs1**2*d2[5:-5] + 4*np.pi*G*prof[5:-5]))/(4*np.pi*G*rho1)
print(f'    residual of c^2 (ln rho)" + 4 pi G rho, relative: {res:.2e}')

print('D3  radius at fixed mass')
xR, sl = M.be_max_slope()
csb = M.sound_speed(M.B68_T_BE, M.MU_MOL)
Mb = M.B68_M*Msun
Rmin = G*Mb/(sl*csb**2)
Rc = G*Mb/(M.be_slope(xc)*csb**2)
print(f'    max xi psi\' = {sl:.4f} at xi = {xR:.3f}')
print(f'    B68 (2.10 Msun, 16 K): R_min = {Rmin/AU:.0f} AU, R at xi_crit = '
      f'{Rc/AU:.0f} AU, R at xi = 6.9 = '
      f'{G*Mb/(M.be_slope(6.9)*csb**2)/AU:.0f} AU; published 12500 AU, '
      f'{(1-12500*AU/Rmin)*100:.2f} per cent below R_min')

print('K1  three regimes')
for label, cs, r_ in (('core', cs1, rho1),
                      ('WNM', M.sound_speed(8000.0, M.MU_HI), rho)):
    lj = M.lambda_jeans(cs, r_)
    print(f'    {label}: lambda_J = {lj/AU:.0f} AU = {lj/pc:.4f} pc, '
          f'M_J = {M.mass_jeans(cs, r_)/Msun:.4e}, cube/sphere '
          f'{r_*lj**3/M.mass_jeans(cs, r_):.4f}')
rho_b0 = 3*(M.PLANCK_H0*1e5/M.Mpc)**2/(8*np.pi*G)*M.PLANCK_OMBH2 \
    / (M.PLANCK_H0/100)**2
rho_z = rho_b0*(1 + M.PLANCK_ZSTAR)**3
csr = M.sound_speed(3000.0, M.MU_PRIM)
print(f'    recombination: rho = {rho_z:.4e}, lambda_J = '
      f'{M.lambda_jeans(csr, rho_z)/pc:.2f} pc, M_J = '
      f'{M.mass_jeans(csr, rho_z)/Msun:.4e}')

print('K2  a Bonnor-Ebert core at P/k = 1e5, 10 K')
P = 1e5*M.kB
mbe = mc*cs1**4/(G**1.5*np.sqrt(P))
rhoc = P/cs1**2*cc
alpha = cs1/np.sqrt(4*np.pi*G*rhoc)
print(f'    M_BE = {mbe/Msun:.4f} Msun, R = {xc*alpha/AU:.0f} AU, '
      f'rho_c = {rhoc:.4e}, M_J(rho_c) = {M.mass_jeans(cs1, rhoc)/Msun:.4f}, '
      f'M_J(rho_edge) = {M.mass_jeans(cs1, rhoc/cc)/Msun:.4f}')
Mcheck = 4*np.pi*rhoc*alpha**3*xc**2*M.be_state(xc)[1]
assert abs(Mcheck/mbe - 1) < 1e-6

print('K3  inverting a contrast, and the degeneracy')
for c_ in (30.0, 10.0):
    x = M.be_xi_from_contrast(c_)
    print(f'    contrast {c_}: xi_max = {x:.4f}, {(x/xc-1)*100:+.1f} per cent '
          f'from critical')
for T_, R_au, M_ in ((16.0, 1.25e4, 2.10), (10.0, 0.85e4, 0.90)):
    R_ = R_au*AU
    rb = 3*M_*Msun/(4*np.pi*R_**3)
    mj = M.mass_jeans(M.sound_speed(T_, M.MU_MOL), rb)
    print(f'    {T_} K, {R_au:.2e} AU, {M_} Msun: rhobar {rb:.4e}, '
          f'M_J {mj/Msun:.4f}, M_J/M {mj/(M_*Msun):.4f}')
print(f'    mass ratio {2.10/0.90:.4f}; M_J/M ratio {1.3972/1.4149:.4f}')
