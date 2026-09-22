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

import os
import sys
import numpy as np
from scipy.integrate import solve_ivp

import m14_solvers as S

OUT = []
HERE = os.path.dirname(os.path.abspath(__file__))


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


# =========================================================================
# COPIED VERBATIM from m08_numbers.py (the Sedov similarity solution), not
# retyped, so that CHECK 3 compares the code with Module 8's own xi_0.
# =========================================================================

# Write  lambda = r/R(t)  with  R ~ t^(2/5), and
#
#     v(r,t) = (r/t) u(lambda)
#     rho(r,t) = rho_0 g(lambda)
#     p(r,t) = rho_0 (r/t)^2 h(lambda)
#
# Substituting into the spherical Euler equations of Module 2 and using
# d lambda/dt = -(2/5) lambda/t, d lambda/dr = lambda/r turns the three
# partial differential equations into three ordinary ones in ln lambda.
# Writing ' for d/d(ln lambda) and a = u - 2/5:
#
#     continuity  a g'/g + 3u + u' = 0
#     momentum    a u' + u^2 - u + (h/g)(2 + h'/h) = 0
#     entropy     a (h'/h - gamma g'/g) + 2(u - 1) = 0
#
# Eliminating g'/g and h'/h from the momentum equation gives u' explicitly.
# The derivation is set out in module08.html; the algebra is reproduced in
# sedov_rhs below so that the code and the prose cannot drift apart.

def sedov_rhs(s, y, gamma):
    """Right-hand side of the similarity system, in the variable s = ln lambda.

    State vector is (u, ln g, ln h).  Logarithms are integrated because g
    falls to zero and h rises without bound at the centre; both do so as
    pure powers of lambda, so their logarithms are linear in s and the
    integration stays well conditioned all the way in.
    """
    u, lg, lh = y
    w = np.exp(lh - lg)             # h/g = p/(rho (r/t)^2) = c^2/(gamma (r/t)^2)
    a = u - 0.4
    den = a*a - gamma*w             # vanishes only at a sonic point
    du = (a*(-u*u + u - 2.0*w) + w*((3.0*gamma + 2.0)*u - 2.0))/den
    dlg = -(3.0*u + du)/a
    dlh = gamma*dlg - 2.0*(u - 1.0)/a
    return [du, dlg, dlh]


def sedov_profile(gamma, s_min=-7.0, n_sample=200001):
    """Integrate the similarity system inward from the shock.

    The boundary values at lambda = 1 are the STRONG-SHOCK Rankine-Hugoniot
    conditions of PART A, evaluated with the shock speed D = dR/dt =
    (2/5) R/t that the similarity form itself supplies:

        rho2 = rho_0 (gamma+1)/(gamma-1)   ->  g(1) = (gamma+1)/(gamma-1)
        v2   = 2D/(gamma+1)                ->  u(1) = 4/(5(gamma+1))
        p2   = 2 rho_0 D^2/(gamma+1)       ->  h(1) = 8/(25(gamma+1))

    So PART B is not a new physical input.  It is PART A plus similarity.
    Returns (lambda, u, g, h) sampled from the shock inward.

    The integration stops at lambda = exp(s_min) = 9.1e-4 rather than at
    the centre, and the reason is not laziness.  As lambda -> 0 the system
    has the fixed point u = (2/5)/gamma with du/d(ln lambda) = -3(u - u*),
    so a perturbation grows as lambda^-3 going inward: the physical
    solution is the unstable one and rounding error overwhelms it below
    about lambda = 1e-4.  Nothing is lost.  The energy integrand carries a
    factor lambda^5, so everything inside lambda = 1e-3 contributes less
    than 1e-15 of the total, and xi_0 is unchanged in its eighth digit
    whether the integration stops at lambda = 6.7e-3 or at 3.4e-4.
    """
    u1 = 4.0/(5.0*(gamma + 1.0))
    g1 = (gamma + 1.0)/(gamma - 1.0)
    h1 = 8.0/(25.0*(gamma + 1.0))
    sol = solve_ivp(sedov_rhs, [0.0, s_min], [u1, np.log(g1), np.log(h1)],
                    args=(gamma,), rtol=1e-12, atol=1e-14,
                    dense_output=True, max_step=0.01)
    s = np.linspace(0.0, s_min, n_sample)
    u, lg, lh = sol.sol(s)
    return np.exp(s), u, np.exp(lg), np.exp(lh)


def sedov_xi0(gamma):
    """The Sedov constant xi_0 in R = xi_0 (E t^2/rho_0)^(1/5).

    The total energy inside the shock is

        E = int_0^R [rho v^2/2 + p/(gamma-1)] 4 pi r^2 dr
          = 4 pi rho_0 (R^5/t^2) J,
        J = int_0^1 lambda^4 [g u^2/2 + h/(gamma-1)] d lambda.

    But R^5/t^2 = xi_0^5 E/rho_0 by the definition of xi_0, so the E on
    both sides cancels and 1 = 4 pi xi_0^5 J.  The energy integral does not
    determine the energy; it determines the CONSTANT.  Returns
    (xi_0, J, K) with K = 1/xi_0^5 = 4 pi J, which is Taylor's K.
    """
    lam, u, g, h = sedov_profile(gamma)
    s = np.log(lam)
    integrand = lam**5*(g*u*u/2.0 + h/(gamma - 1.0))
    J = -np.trapezoid(integrand, s)      # s runs from 0 downward
    xi0 = (4.0*np.pi*J)**-0.2
    return xi0, J, 4.0*np.pi*J


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
    # a smooth Gaussian at C = 1.1.  The blow-up is NOT seeded by rounding:
    # the Gaussian is not periodic on [0, 1] (its end cells hold 1.8e-11),
    # and the sampled profile itself carries a small amplitude at the high
    # wavenumbers, which grow by (2.3).  Checked below by repeating the
    # same steps in exact rational arithmetic on the stored samples, and
    # in 60-digit decimal arithmetic on samples computed to 60 digits.
    x = (np.arange(200) + 0.5)/200
    u0 = np.exp(-((x - 0.5)/0.1)**2)
    u = u0.copy()
    for step in range(1, 2001):
        u = S.upwind_step(u, 1.1)
        if np.max(np.abs(u)) > 1e3:
            break
    P(f'  smooth Gaussian, 200 cells, C = 1.1: |u| exceeds 1e3 after '
      f'{step} steps')
    from fractions import Fraction
    import decimal
    umax_f = np.max(np.abs(u))
    Cq = Fraction(11, 10)
    q = [Fraction(float(a)) for a in u0]
    for _ in range(step):
        q = [q[i] - Cq*(q[i] - q[i - 1]) for i in range(200)]
    umax_q = float(max(abs(a) for a in q))
    decimal.getcontext().prec = 60
    D = decimal.Decimal
    d = [(-(((D(i) + D('0.5'))/200 - D('0.5'))/D('0.1'))**2).exp()
         for i in range(200)]
    Cd = D('1.1')
    for _ in range(step):
        d = [d[i] - Cd*(d[i] - d[i - 1]) for i in range(200)]
    umax_d = float(max(abs(a) for a in d))
    P(f'    max|u| after {step} steps: float64 {umax_f:.10f}; exact '
      f'rational steps on the stored samples {umax_q:.10f}; 60-digit '
      f'samples and steps {umax_d:.10f}')
    P(f'    relative differences from float64: exact {umax_q/umax_f - 1:.1e}'
      f', 60-digit {umax_d/umax_f - 1:.1e}')
    amp = np.abs(np.fft.fft(u0))/200
    P(f'    end-cell value of the Gaussian {u0[0]:.3e}; amplitude of the '
      f'samples at wavenumbers 91, 92, 93 of 200: {amp[91]:.2e}, '
      f'{amp[92]:.2e}, {amp[93]:.2e}')
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
    P(f'    cloud: extra steps of a compressible code, 100/M = '
      f'{100/M_mc:.2f} per cent')

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
    contact_rows = (rows[-2, 3], rows[-1, 3])
    names = ('total', 'fan', 'contact', 'shock')
    for k, name in enumerate(names, start=1):
        o = np.log(rows[0, k]/rows[-1, k])/np.log(rows[-1, 0]/rows[0, 0])
        o2 = np.log(rows[-2, k]/rows[-1, k])/np.log(2.0)
        P(f'  PUNCHLINE order of the {name:7s} error, N = 100 -> 6400: '
          f'{o:.3f}   (last doubling {o2:.3f})')
    P(f'  PUNCHLINE contact measured/predicted: N = 100 '
      f'{rows[0, 3]/rows[0, 5]:.4f}, N = 6400 {rows[-1, 3]/rows[-1, 5]:.4f}')
    P(f'  contact share of the total error: N = 100 '
      f'{100*rows[0, 3]/rows[0, 1]:.1f} per cent, N = 6400 '
      f'{100*rows[-1, 3]/rows[-1, 1]:.1f} per cent')

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
    P(f'  Bate & Burkert, N_neigh = 50: largest particle mass that resolves'
      f' M_J(1e10) = M_J/(2 N_neigh) = {M05_MJ*1e-3/100:.3g} Msun')

    # ------------------------------------------------------------------
    P('')
    P('PART E.  CHECK 3.  The Sedov problem of Kamm & Timmes, spherical')
    P('-' * 72)
    xi0, J, K = sedov_xi0(1.4)
    P(f'  xi_0(gamma = 7/5) from the copied Module 8 routine = {xi0:.6f}'
      f'  (module08.html:360 prints {M08_XI0_14})')
    assert abs(xi0 - M08_XI0_14) < 5e-7
    P(f'  K = 1/xi_0^5 = {1/xi0**5:.6f} (Kamm & Timmes E = {KT_E})')
    R_exact = xi0*(KT_E*1.0**2/1.0)**0.2
    P(f'  exact shock radius at t = 1: {R_exact:.6f}')
    lam, u_s, g_s, h_s = sedov_profile(1.4)
    save = {'lam': lam[::50], 'g': g_s[::50]}
    for n in (100, 200, 400):
        rc, r, u, p, E = S.godunov_spherical(n, 1.2, KT_E, 1.0, 1e-6, 1.0,
                                             1.4)
        k = np.argmax(r)
        half = 1.0 + 0.5*(r[k] - 1.0)
        out = np.where((rc > rc[k]) & (r < half))[0][0]
        x0, x1, y0, y1 = rc[out - 1], rc[out], r[out - 1], r[out]
        Rs = x0 + (half - y0)*(x1 - x0)/(y1 - y0)
        dE = (E[-1] - E[0])/E[0]
        P(f'  n = {n:3d}: peak rho {r[k]:.4f} at r = {rc[k]:.4f}; '
          f'half-height radius {Rs:.5f}, error {Rs - R_exact:+.5f}; '
          f'energy drift {dE:.1e}; steps {len(E)}')
        assert abs(dE) < 1e-12
        save[f'r{n}'] = rc
        save[f'rho{n}'] = r
        peak_last = r[k]
    P(f'  jump ceiling (gamma+1)/(gamma-1) = {2.4/0.4:.1f}')
    P(f'  shortfall of the n = 400 peak below the ceiling: '
      f'{100*(1 - peak_last/6.0):.2f} per cent')
    np.savez(os.path.join(HERE, 'm14_sedov_profiles.npz'), **save)

    # ------------------------------------------------------------------
    P('')
    P('PART L.  The problems')
    P('-' * 72)
    th = np.linspace(0.0, np.pi, 200001)
    Gf = np.max(np.abs(S.amplification_ftcs(th, 0.5)))
    P(f'  C1  FTCS at C = 0.5: max |G| = {Gf:.6f}; steps to grow 1e3 = '
      f'{np.log(1e3)/np.log(Gf):.2f}')
    cL = np.sqrt(1.4*SOD_L[2]/SOD_L[0])
    P(f'  C2  initial S_max = c_L = {cL:.6f}; dt = 0.9 (1/400)/S_max = '
      f'{0.9/400/cL:.6e}; steps to t = 0.2 at that dt = '
      f'{0.2/(0.9/400/cL):.2f}')
    P(f'  C2  post-shock sound speed (1.4 p*/rho*R)^(1/2) = '
      f'{np.sqrt(1.4*w["p_star"]/w["rho_starR"]):.4g}')
    P(f'  C3  Re_num(N = 512, C = 0.8) = {2*512/(1 - 0.8):.1f}; '
      f'N^(4/3) = {512**(4/3):.1f}')
    w2 = S.riemann_waves(1.0, -2.0, 0.4, 1.0, 2.0, 0.4, 1.4)
    P(f'  K1  123 problem: p* = {w2["p_star"]:.6f}, u* = '
      f'{w2["u_star"]:.6f}, rho* = {w2["rho_starL"]:.6f} (both sides '
      f'{w2["rho_starR"]:.6f})')
    c123 = np.sqrt(1.4*0.4)
    P(f'  K1  c = {c123:.6f}; c_L + c_R = {2*c123:.6f}; (4.2) left side '
      f'2(c_L + c_R)/(gamma - 1) = {2*2*c123/0.4:.4g}')
    lam8 = M05_LAMJ_PC*1e-2
    cells = 4*M05_LAMJ_PC/(TRUELOVE_J*lam8)
    P(f'  K2  lambda_J(1e8) = {lam8:.7f} pc; cells per side = {cells:.1f};'
      f' 3D = {cells**3:.4g}')
    # K3: contact law fitted on the last two rows of PART D
    N1, N2 = 3200.0, 6400.0
    E1, E2 = contact_rows
    slope = np.log(E1/E2)/np.log(N2/N1)
    Nt = N2*(E2/1e-4)**(1/slope)
    P(f'  K3  contact order over the last doubling = {slope:.4f}; N for '
      f'L1 = 1e-4: {Nt:.4g}; 3D work ratio (N/6400)^4 = '
      f'{(Nt/N2)**4:.4g}')
    P(f'  K3  error factor E(6400)/1e-4 = {E2/1e-4:.3g}; first-order work '
      f'ratio (E(6400)/1e-4)^4 = {(E2/1e-4)**4:.3g}')

    P('')
    P('=' * 72)
    P('END OF RUN.  All asserts passed.')
    P('=' * 72)


if __name__ == '__main__':
    main()
    sys.exit(0)
