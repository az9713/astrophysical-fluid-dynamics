"""Module 14 numbers: numerical methods.  The Courant condition derived
rather than borrowed, the numerical viscosity every grid code carries,
the exact Riemann solver that Godunov's method is built on, three codes
run against closed forms this book already owns, and one-dimensional
smoothed-particle hydrodynamics run against the same problem as the grid.

Every number quoted in module14.html is produced here, so the prose can be
checked against a run rather than against memory.  The codes themselves are
in m14_solvers.py.  Units: the test problems are dimensionless, as their
authors set them; the astrophysical numbers of PART G are CGS.

WHAT THIS MODULE OWES, AND TO WHOM (.ignore/m14-promises.md):
  module10.html:257  Proposition 4 USES the Courant condition.  PART A
                     derives it, and prices the step an explicit
                     compressible code takes against the step Module 10
                     assumed.
  module10.html:285  "every astrophysical code therefore solves a
                     different problem".  PART B says which: Euler plus a
                     numerical viscosity D_num = a dx (1 - C)/2.
  module05.html:767  "Module 14 (numerics) for how collapse is followed."
                     PART G: the Jeans condition.
  charter            which results of Modules 1-13 came from a simulation:
                     .ignore/m14-census-*.md, not computed here.

NOTATION INSIDE THIS FILE.  C is the Courant number (C_CFL in the page),
h the SPH smoothing length, D_num the numerical diffusivity, N a cell or
particle count.
"""

import sys
import numpy as np

import m14_solvers as S

OUT = []


def P(s=''):
    OUT.append(s)
    print(s, flush=True)


# --- constants (CODATA 2018 / IAU 2015), CGS, copied from m13_numbers.py --
kB = 1.380649e-16
mu_u = 1.66053906660e-24
G = 6.67430e-8
pc = 3.0856775814913673e18
AU = 1.495978707e13
yr = 3.15576e7
GMsun = 1.3271244e26
Msun = GMsun/G

GAMMA_SOD = 1.4
SOD_L = (1.0, 0.0, 1.0)          # rho, u, p
SOD_R = (0.125, 0.0, 0.1)
SOD_T = 0.2

# --- what the book already prints (targets, read off the files) ---------
M10_MA_TH_LAB = 0.0218           # module10.html:148, U/vbar, lab air
M10_RE_LAB = 1.0e6               # module10.html:285, "a large wind tunnel"
M10_RE_CLOUD = 8.1e7             # module10.html:285
M10_CLOUD_POINTS = 6.24e17       # module10.html:285, :918
M08_XI0_14 = 1.032777            # module08.html:360
KT_E = 0.851072                  # module08.html:381, Kamm & Timmes
M05_LAMJ_PC = 0.19479            # module05.html:170, 10 K, n(H2) = 1e4
M05_RHO0 = 4.6495e-20            # module05.html:170
M05_MJ = 2.6584                  # module05.html:170, Msun

# --- published values, filled in from .ignore/m14-sources-*.md ---------
TRUELOVE_J = 0.25                # Truelove et al. (1997): J <= 1/4


def main():
    P('=' * 72)
    P('MODULE 14 NUMBERS -- numerical methods')
    P('=' * 72)

    # ------------------------------------------------------------------
    P('')
    P('PART A.  The Courant condition')
    P('-' * 72)
    th = np.linspace(0.0, np.pi, 100001)
    for C in (0.5, 0.9, 1.0, 1.1):
        Gmax = np.max(np.abs(S.amplification_upwind(th, C)))
        P(f'  upwind  C = {C:.1f}   max |G(theta)| = {Gmax:.6f}'
          f'   |1 - 2C| = {abs(1 - 2*C):.6f}')
    for C in (0.5, 1.0):
        Gmax = np.max(np.abs(S.amplification_ftcs(th, C)))
        P(f'  FTCS    C = {C:.1f}   max |G(theta)| = {Gmax:.6f}'
          f'   sqrt(1 + C^2) = {np.sqrt(1 + C*C):.6f}')
        assert abs(Gmax - np.sqrt(1 + C*C)) < 1e-9
    # the sawtooth (-1)^j is the theta = pi eigenmode of the upwind scheme
    n = 64
    saw = (-1.0)**np.arange(n)
    for C in (0.9, 1.1):
        u = saw*1e-10
        for _ in range(100):
            u = S.upwind_step(u, C)
        rate = (np.max(np.abs(u))/1e-10)**(1/100)
        P(f'  sawtooth after 100 steps at C = {C}: growth per step = '
          f'{rate:.6f}  (predicted |1 - 2C| = {abs(1 - 2*C):.6f})')
        assert abs(rate - abs(1 - 2*C)) < 1e-9
    # random data at C = 1.1: the blow-up comes from rounding
    rng = np.random.default_rng(1)
    x = (np.arange(200) + 0.5)/200
    u = np.exp(-((x - 0.5)/0.1)**2)
    for step in range(1, 2001):
        u = S.upwind_step(u, 1.1)
        if np.max(np.abs(u)) > 1e3:
            break
    P(f'  smooth Gaussian, 200 cells, C = 1.1: |u| exceeds 1e3 after '
      f'{step} steps')
    del rng
    # Module 10's step against an explicit compressible code's step
    Ma_to_M = np.sqrt(np.pi*1.4/8.0)     # c_s/vbar for gamma = 1.4
    M_lab = M10_MA_TH_LAB/Ma_to_M
    P(f'  Module 10 lab air: Ma_th = {M10_MA_TH_LAB}; c_s/vbar = '
      f'sqrt(pi gamma/8) = {Ma_to_M:.4f} at gamma = 1.4')
    P(f'    Mach number U/c_s = {M_lab:.4f}')
    P(f'    PUNCHLINE steps of a compressible explicit code per step '
      f'assumed in module10 Prop. 4 = 1 + 1/M = {1 + 1/M_lab:.2f}')
    cs_mc = np.sqrt(5/3*kB*10.0/(2.33*mu_u))
    M_mc = 2.64e5/cs_mc
    P(f'  Module 10 cloud: U = 2.64 km/s, c_s(10 K, mu 2.33, 5/3) = '
      f'{cs_mc/1e5:.4f} km/s, M = {M_mc:.3f}, 1 + 1/M = {1 + 1/M_mc:.4f}')

    # ------------------------------------------------------------------
    P('')
    P('PART B.  The numerical viscosity of the upwind scheme')
    P('-' * 72)
    n = 400
    dx = 1.0/n
    x = (np.arange(n) + 0.5)*dx
    for C in (0.25, 0.5, 0.9):
        u = np.exp(-((x - 0.3)/0.02)**2)
        m0 = u.sum()
        var0 = np.sum(u*(x - np.sum(u*x)/m0)**2)/m0
        steps = 200
        for _ in range(steps):
            u = S.upwind_step(u, C)
        var1 = np.sum(u*(x - np.sum(u*x)/m0)**2)/m0
        pred = steps*C*(1 - C)*dx*dx
        P(f'  C = {C:.2f}: variance growth {var1 - var0:.6e}, predicted '
          f'n C(1-C) dx^2 = {pred:.6e}, ratio {(var1 - var0)/pred:.9f}')
        assert abs((var1 - var0)/pred - 1) < 1e-6
    for N in (256, 1024, 4096):
        for C in (0.5, 0.9):
            P(f'  Re_num = 2N/(1-C): N = {N:5d}, C = {C}: '
              f'{2*N/(1 - C):.4g}')
    for N in (1024, 4096, 10048):
        P(f'  best-case Re with the dissipation scale at one cell, '
          f'N^(4/3), N = {N}: {N**(4/3):.4g}')
    P(f'  cells per side for Re = 1e6 (Module 10): Re^(3/4) = '
      f'{M10_RE_LAB**0.75:.4g}')

    # ------------------------------------------------------------------
    P('')
    P('PART C.  The exact Riemann solver, Sod\'s problem, gamma = 1.4')
    P('-' * 72)
    w = S.riemann_waves(*SOD_L, *SOD_R, GAMMA_SOD)
    for k in ('p_star', 'u_star', 'rho_starL', 'rho_starR', 'S_R', 'S_HL',
              'S_TL'):
        P(f'  {k:10s} = {float(w[k]):.6f}')
    # consistency: the Rankine-Hugoniot conditions across the right shock
    r1, u1, p1 = SOD_R
    r2, u2, p2 = w['rho_starR'], w['u_star'], w['p_star']
    s = w['S_R']
    mass = r2*(u2 - s) - r1*(u1 - s)
    mom = r2*(u2 - s)**2 + p2 - r1*(u1 - s)**2 - p1
    P(f'  R-H residuals across the shock: mass {mass:.2e}, momentum '
      f'{mom:.2e}')
    assert abs(mass) < 1e-12 and abs(mom) < 1e-12
    # isentropic across the fan: p/rho^gamma
    P(f'  p/rho^gamma: left state {SOD_L[2]/SOD_L[0]**1.4:.6f}, star-left '
      f'{w["p_star"]/w["rho_starL"]**1.4:.6f}')

    # ------------------------------------------------------------------
    P('')
    P('PART D.  CHECK 2, THE ANCHOR.  Godunov on Sod, against PART C')
    P('-' * 72)
    t = SOD_T
    xc = 0.5 + w['u_star']*t
    xs = 0.5 + w['S_R']*t
    xt = 0.5 + w['S_TL']*t
    b1, b2 = 0.5*(xt + xc), 0.5*(xc + xs)
    drc = w['rho_starL'] - w['rho_starR']
    P(f'  t = {t}; contact at {xc:.6f}, shock at {xs:.6f}, fan tail at '
      f'{xt:.6f}; regions split at {b1:.6f} and {b2:.6f}')
    P(f'  density jump at the contact = {drc:.6f}')
    Ns = (100, 200, 400, 800, 1600, 3200, 6400)
    rows = []
    for N in Ns:
        dx = 1.0/N
        x = (np.arange(N) + 0.5)*dx
        r0 = np.where(x < 0.5, SOD_L[0], SOD_R[0])
        p0 = np.where(x < 0.5, SOD_L[2], SOD_R[2])
        r, u, p, dts = S.godunov_planar(r0, 0*x, p0, dx, t, GAMMA_SOD,
                                        C=0.9, record_dt=True)
        re, ue, pe, _, _ = S.riemann_sample((x - 0.5)/t, *SOD_L, *SOD_R,
                                            GAMMA_SOD)
        e = np.abs(r - re)*dx
        E = (e.sum(), e[x < b1].sum(), e[(x >= b1) & (x < b2)].sum(),
             e[x >= b2].sum())
        Cc = w['u_star']*dts/dx
        sig = np.sqrt(np.sum(Cc*(1 - Cc)))*dx
        pred = drc*sig*np.sqrt(2/np.pi)
        rows.append((N, *E, pred, Cc.mean(), len(dts)))
        P(f'  N = {N:5d}  L1 total {E[0]:.4e}  fan {E[1]:.4e}  contact '
          f'{E[2]:.4e}  shock {E[3]:.4e}  | predicted contact {pred:.4e}'
          f'  ratio {E[2]/pred:.4f}  <C_c> {Cc.mean():.4f}  steps '
          f'{len(dts)}')
    rows = np.array(rows)
    names = ('total', 'fan', 'contact', 'shock')
    for k, name in enumerate(names, start=1):
        o = np.log(rows[0, k]/rows[-1, k])/np.log(rows[-1, 0]/rows[0, 0])
        o2 = np.log(rows[-2, k]/rows[-1, k])/np.log(2.0)
        P(f'  PUNCHLINE order of the {name:7s} error, N = 100 -> 6400: '
          f'{o:.3f}   (last doubling {o2:.3f})')
    P(f'  PUNCHLINE contact measured/predicted: N = 100 {rows[0, 3]/rows[0, 5]:.4f},'
      f' N = 6400 {rows[-1, 3]/rows[-1, 5]:.4f}')

    # ------------------------------------------------------------------
    P('')
    P('PART F.  CHECK 4.  One-dimensional SPH on Sod')
    P('-' * 72)
    ps = w['p_star']
    uL_ex = ps/((GAMMA_SOD - 1)*w['rho_starL'])
    uR_ex = ps/((GAMMA_SOD - 1)*w['rho_starR'])
    P(f'  exact thermal energy either side of the contact: {uL_ex:.4f}, '
      f'{uR_ex:.4f}')
    for au in (0.0, 1.0):
        for nl in (200, 400, 800):
            x, rho, v, Pp, uth, m = S.sph_shock_tube(
                nl, SOD_L[0], SOD_L[2], SOD_R[0], SOD_R[2], GAMMA_SOD, t,
                alpha_u=au)
            near = np.abs(x - xc) < 0.05
            plateau = (x > xt + 0.05) & (x < xc - 0.05)
            re, _, _, _, _ = S.riemann_sample((x - 0.5)/t, *SOD_L, *SOD_R,
                                              GAMMA_SOD)
            inb = (x > 0) & (x < 1)
            P(f'  alpha_u = {au:.0f}, {nl:4d}/unit length ({inb.sum()} in '
              f'[0,1]): contact max|P-p*|/p* = '
              f'{np.max(np.abs(Pp[near] - ps))/ps:.4f}; plateau '
              f'{np.max(np.abs(Pp[plateau] - ps))/ps:.4f}; u max '
              f'{uth[near].max():.4f}; mean|rho-exact| '
              f'{np.mean(np.abs(rho[inb] - re[inb])):.4e}')

    # ------------------------------------------------------------------
    P('')
    P('PART G.  Following a collapse: the Jeans condition')
    P('-' * 72)
    for n_H2 in (1e4, 1e6, 1e8, 1e10):
        lam = M05_LAMJ_PC*(n_H2/1e4)**-0.5
        MJ = M05_MJ*(n_H2/1e4)**-0.5
        dxmax = TRUELOVE_J*lam
        P(f'  n(H2) = {n_H2:.0e}: lambda_J = {lam:.5g} pc = '
          f'{lam*pc/AU:.5g} AU, M_J = {MJ:.4g} Msun, dx <= '
          f'{dxmax*pc/AU:.4g} AU')
    box = 4*M05_LAMJ_PC
    cells = box/(TRUELOVE_J*M05_LAMJ_PC*1e-3)
    P(f'  a box of 4 lambda_J(1e4) = {box:.5f} pc at the 1e10 resolution: '
      f'{cells:.4g} cells per side, {cells**3:.4g} in 3D')
    P(f'  refinement levels of factor 2 for a factor 1e3 in lambda_J: '
      f'{np.log2(1e3):.3f}')

    P('')
    P('=' * 72)
    P('END OF RUN.  All asserts passed.')
    P('=' * 72)


if __name__ == '__main__':
    main()
    sys.exit(0)
