"""Module 14 figures.  Five SVGs, computed with m14_solvers.py and
m14_numbers.py's own constants so that a figure and the prose cannot
diverge.

    m14_fig_courant.svg   max |G| against C for upwind and FTCS: CHECK 1
    m14_fig_sod.svg       density at t = 0.2, exact, Godunov, SPH
    m14_fig_order.svg     L1 error by region against N: CHECK 2, the anchor
    m14_fig_sedov.svg     the Sedov density at t = 1 against Module 8's
                          exact profile: CHECK 3
    m14_fig_blip.svg      SPH pressure at the contact, alpha_u = 0 and 1:
                          CHECK 4

m14_fig_sedov.svg reads m14_sedov_profiles.npz, which m14_numbers.py writes
(the n = 400 run takes four minutes and is not repeated here).

FIGURE RULES CARRIED FROM MODULES 9 TO 13: no literal "_" or "^" inside a
<text>; every legend entry carries a line swatch; shoot the CHECK figures
and look at them.
"""
import os

import numpy as np

import m14_numbers as M
import m14_solvers as S

HERE = os.path.dirname(os.path.abspath(__file__))

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"
RED = "#f87171"

SUB = '<tspan baseline-shift="sub" font-size="8">{0}</tspan>'
SUP = '<tspan baseline-shift="super" font-size="8">{0}</tspan>'


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def frame(s, X0, Y0, X1, Y1):
    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')


def text(s, x, y, body, size=11, col=FG, anchor="start"):
    s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
             f'text-anchor="{anchor}" fill="{col}">{body}</text>')


def tick(s, x0, y0, x1, y1):
    s.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" '
             f'y2="{y1:.1f}" stroke="{RULE}" stroke-width="1"/>')


def swatch(s, x, y, col, dash=None, dot=False):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    if dot:
        s.append(f'<circle cx="{x+11:.1f}" cy="{y-4:.1f}" r="3" '
                 f'fill="{col}"/>')
    else:
        s.append(f'<line x1="{x:.1f}" y1="{y-4:.1f}" x2="{x+22:.1f}" '
                 f'y2="{y-4:.1f}" stroke="{col}" stroke-width="2.2"{d}/>')


def head(W, H, label):
    return [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
            f'role="img" aria-label="{label}">']


def write(name, s):
    s.append('</svg>')
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write("\n".join(s))


def sod_grid(N):
    dx = 1.0/N
    x = (np.arange(N) + 0.5)*dx
    r0 = np.where(x < 0.5, M.SOD_L[0], M.SOD_R[0])
    p0 = np.where(x < 0.5, M.SOD_L[2], M.SOD_R[2])
    r, u, p = S.godunov_planar(r0, 0*x, p0, dx, M.SOD_T, M.GAMMA_SOD)
    return x, r, u, p


# =========================================================================
# Fig. 1.  CHECK 1.  max |G| over theta against C.
# =========================================================================

def build_courant():
    W, H = 640, 380
    X0, X1, Y0, Y1 = 70.0, 600.0, 24.0, 320.0
    CLO, CHI, GLO, GHI = 0.0, 1.5, 0.0, 2.2

    def px(v):
        return X0 + (v - CLO)/(CHI - CLO)*(X1 - X0)

    def py(v):
        return Y1 - (v - GLO)/(GHI - GLO)*(Y1 - Y0)

    th = np.linspace(0.0, np.pi, 2001)
    Cs = np.linspace(0.0, 1.5, 301)
    gu = np.array([np.max(np.abs(S.amplification_upwind(th, C)))
                   for C in Cs])
    gf = np.array([np.max(np.abs(S.amplification_ftcs(th, C)))
                   for C in Cs])
    s = head(W, H, 'Largest amplification factor over all Fourier modes '
             'against the Courant number from 0 to 1.5. The upwind curve '
             'equals 1 from 0 to 1 and rises as 2C minus 1 beyond 1. The '
             'forward-time centred-space curve is the square root of 1 '
             'plus C squared and lies above 1 for every C greater than 0. '
             'Two dots on the upwind curve at C 0.9 and 1.1 mark the '
             'measured growth per step of the sawtooth mode, 0.8 in '
             'magnitude below and 1.2 above.')
    frame(s, X0, Y0, X1, Y1)
    s.append(f'<rect x="{px(0):.1f}" y="{Y0:.1f}" width="{px(1)-px(0):.1f}"'
             f' height="{Y1-Y0:.1f}" fill="{ACC2}" opacity="0.07"/>')
    s.append(f'<line x1="{X0:.1f}" y1="{py(1):.1f}" x2="{X1:.1f}" '
             f'y2="{py(1):.1f}" stroke="{MUT}" stroke-width="1" '
             f'stroke-dasharray="4 4"/>')
    s.append(f'<line x1="{px(1):.1f}" y1="{Y0:.1f}" x2="{px(1):.1f}" '
             f'y2="{Y1:.1f}" stroke="{VIO}" stroke-width="1" '
             f'stroke-dasharray="3 3"/>')
    for v in (0, 0.5, 1.0, 1.5):
        tick(s, px(v), Y1, px(v), Y1 + 5)
        text(s, px(v), Y1 + 18, f'{v:g}', 10.5, MUT, "middle")
    for v in (0, 0.5, 1.0, 1.5, 2.0):
        tick(s, X0 - 5, py(v), X0, py(v))
        text(s, X0 - 8, py(v) + 4, f'{v:g}', 10.5, MUT, "end")
    s.append(f'<path d="{path(px(Cs), py(gu))}" fill="none" stroke="{ACC}" '
             f'stroke-width="2.4"/>')
    s.append(f'<path d="{path(px(Cs), py(gf))}" fill="none" stroke="{RED}" '
             f'stroke-width="2.2" stroke-dasharray="7 4"/>')
    for C, g in ((0.9, 0.8), (1.1, 1.2)):
        s.append(f'<circle cx="{px(C):.1f}" cy="{py(g):.1f}" r="4.2" '
                 f'fill="{YEL}"/>')
    text(s, px(0.9) - 8, py(0.8) + 5, 'sawtooth, |G| = 0.8', 10.5, YEL, "end")
    text(s, px(1.1) + 9, py(1.2) + 12, 'sawtooth, |G| = 1.2', 10.5, YEL)
    text(s, px(1.0) + 6, Y0 + 14, 'C = 1', 10.5, VIO)
    text(s, px(0.08), py(0.35), 'stable for upwind', 10.5, ACC2)
    swatch(s, px(0.08), py(2.05), ACC)
    text(s, px(0.08) + 28, py(2.05), 'upwind: max |G| = max(1, 2C &#8722; 1)',
         11, ACC)
    swatch(s, px(0.08), py(1.85), RED, "7 4")
    text(s, px(0.08) + 28, py(1.85), 'FTCS: max |G| = (1 + C' + SUP.format(2)
         + ')' + SUP.format('1/2'), 11, RED)
    text(s, (X0 + X1)/2, Y1 + 40, 'Courant number C', 11.5, FG, "middle")
    text(s, 20, (Y0 + Y1)/2, '|G|', 11.5, FG, "middle")
    write('m14_fig_courant.svg', s)


# =========================================================================
# Fig. 2.  The Sod density profile at t = 0.2.
# =========================================================================

def build_sod(sph):
    W, H = 680, 400
    X0, X1, Y0, Y1 = 70.0, 640.0, 24.0, 340.0
    XLO, XHI, RLO, RHI = 0.0, 1.0, 0.0, 1.1

    def px(v):
        return X0 + (v - XLO)/(XHI - XLO)*(X1 - X0)

    def py(v):
        return Y1 - (v - RLO)/(RHI - RLO)*(Y1 - Y0)

    xe = np.linspace(0.0, 1.0, 4001)
    re = S.riemann_sample((xe - 0.5)/M.SOD_T, *M.SOD_L, *M.SOD_R,
                          M.GAMMA_SOD)[0]
    x1, r1, _, _ = sod_grid(100)
    x8, r8, _, _ = sod_grid(800)
    xs, rs = sph
    sel = (xs > 0) & (xs < 1)
    s = head(W, H, 'Density against position at time 0.2 in Sod\'s shock '
             'tube. The exact solution is a rarefaction fan from 0.26 to '
             '0.49, a flat region, a contact discontinuity at 0.685 where '
             'the density falls from 0.426 to 0.266, and a shock at 0.850. '
             'Godunov at 100 cells rounds every corner and smears the '
             'contact over about ten cells; at 800 cells the smearing is '
             'narrower. SPH particles at 400 per unit length follow the '
             'exact curve with a wider shock.')
    frame(s, X0, Y0, X1, Y1)
    for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        tick(s, px(v), Y1, px(v), Y1 + 5)
        text(s, px(v), Y1 + 18, f'{v:g}', 10.5, MUT, "middle")
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        tick(s, X0 - 5, py(v), X0, py(v))
        text(s, X0 - 8, py(v) + 4, f'{v:g}', 10.5, MUT, "end")
    s.append(f'<path d="{path(px(xe), py(re))}" fill="none" stroke="{FG}" '
             f'stroke-width="1.6"/>')
    s.append(f'<path d="{path(px(x1), py(r1))}" fill="none" stroke="{ACC}" '
             f'stroke-width="2" stroke-dasharray="6 3"/>')
    s.append(f'<path d="{path(px(x8), py(r8))}" fill="none" stroke="{ACC2}" '
             f'stroke-width="1.8"/>')
    for xv, rv in zip(xs[sel][::2], rs[sel][::2]):
        s.append(f'<circle cx="{px(xv):.1f}" cy="{py(rv):.1f}" r="1.8" '
                 f'fill="{VIO}"/>')
    lx = px(0.60)
    for i, (col, dash, dot, lab) in enumerate((
            (FG, None, False, 'exact (Riemann solution)'),
            (ACC, "6 3", False, 'Godunov, 100 cells'),
            (ACC2, None, False, 'Godunov, 800 cells'),
            (VIO, None, True, 'SPH, 400 particles per unit length'))):
        y = py(1.02) + 18*i
        swatch(s, lx, y, col, dash, dot)
        text(s, lx + 28, y, lab, 11, col)
    text(s, px(0.685), py(0.2), 'contact', 10.5, MUT, "middle")
    text(s, px(0.850), py(0.05), 'shock', 10.5, MUT, "middle")
    text(s, px(0.21), py(0.55), 'rarefaction fan', 10.5, MUT, "middle")
    text(s, (X0 + X1)/2, Y1 + 40, 'x', 11.5, FG, "middle")
    text(s, 22, (Y0 + Y1)/2, '&#961;', 12, FG, "middle")
    write('m14_fig_sod.svg', s)


# =========================================================================
# Fig. 3.  CHECK 2, the anchor.  L1 error by region against N.
# =========================================================================

def build_order():
    W, H = 680, 420
    X0, X1, Y0, Y1 = 80.0, 640.0, 24.0, 360.0
    NLO, NHI, ELO, EHI = 2.0 - 0.1, np.log10(6400) + 0.1, -5.0, -1.6

    def px(v):
        return X0 + (v - NLO)/(NHI - NLO)*(X1 - X0)

    def py(v):
        return Y1 - (v - ELO)/(EHI - ELO)*(Y1 - Y0)

    w = S.riemann_waves(*M.SOD_L, *M.SOD_R, M.GAMMA_SOD)
    t = M.SOD_T
    xc, xs, xt = (0.5 + w['u_star']*t, 0.5 + w['S_R']*t,
                  0.5 + w['S_TL']*t)
    b1, b2 = 0.5*(xt + xc), 0.5*(xc + xs)
    drc = w['rho_starL'] - w['rho_starR']
    Ns = np.array([100, 200, 400, 800, 1600, 3200, 6400])
    E = np.zeros((Ns.size, 4))
    pred = np.zeros(Ns.size)
    for k, N in enumerate(Ns):
        dx = 1.0/N
        x = (np.arange(N) + 0.5)*dx
        r0 = np.where(x < 0.5, M.SOD_L[0], M.SOD_R[0])
        p0 = np.where(x < 0.5, M.SOD_L[2], M.SOD_R[2])
        r, u, p, dts = S.godunov_planar(r0, 0*x, p0, dx, t, M.GAMMA_SOD,
                                        record_dt=True)
        re = S.riemann_sample((x - 0.5)/t, *M.SOD_L, *M.SOD_R,
                              M.GAMMA_SOD)[0]
        e = np.abs(r - re)*dx
        E[k] = (e.sum(), e[x < b1].sum(), e[(x >= b1) & (x < b2)].sum(),
                e[x >= b2].sum())
        Cc = w['u_star']*dts/dx
        pred[k] = drc*np.sqrt(np.sum(Cc*(1 - Cc)))*dx*np.sqrt(2/np.pi)
    lN = np.log10(Ns)
    s = head(W, H, 'L1 error of density against the number of cells from '
             '100 to 6400, both axes logarithmic, for the whole domain and '
             'for three regions. The shock error falls with slope 1, the '
             'contact error with slope one half, the rarefaction error '
             'between them, and the total error with slope 0.646. A dashed '
             'line is the contact error predicted from the scheme\'s '
             'numerical diffusion with no fitted parameter; the measured '
             'contact points lie just above it and approach it.')
    frame(s, X0, Y0, X1, Y1)
    for N in Ns:
        tick(s, px(np.log10(N)), Y1, px(np.log10(N)), Y1 + 5)
        text(s, px(np.log10(N)), Y1 + 18, f'{N}', 10.5, MUT, "middle")
    for e in range(-5, -1):
        tick(s, X0 - 5, py(e), X0, py(e))
        text(s, X0 - 8, py(e) + 4, '10' + SUP.format(f'&#8722;{-e}'), 10.5,
             MUT, "end")
    s.append(f'<path d="{path(px(lN), py(np.log10(pred)))}" fill="none" '
             f'stroke="{ACC2}" stroke-width="1.6" stroke-dasharray="6 4"/>')
    cols = (FG, VIO, ACC2, ACC)
    labs = ('total, order 0.646', 'rarefaction fan, 0.752',
            'contact, 0.511', 'shock, 1.013')
    for k in range(4):
        s.append(f'<path d="{path(px(lN), py(np.log10(E[:, k])))}" '
                 f'fill="none" stroke="{cols[k]}" stroke-width="1.8"/>')
        for a, b in zip(lN, np.log10(E[:, k])):
            s.append(f'<circle cx="{px(a):.1f}" cy="{py(b):.1f}" r="3.2" '
                     f'fill="{cols[k]}"/>')
    lx = px(3.05)
    for i in range(4):
        y = py(-1.75) + 17*i
        swatch(s, lx, y, cols[i])
        text(s, lx + 28, y, labs[i], 11, cols[i])
    y = py(-1.75) + 68
    swatch(s, lx, y, ACC2, "6 4")
    text(s, lx + 28, y, 'contact predicted by (5.1), no fit', 11, ACC2)
    text(s, (X0 + X1)/2, Y1 + 40, 'cells N', 11.5, FG, "middle")
    text(s, 22, (Y0 + Y1)/2, 'L1', 11.5, FG, "middle")
    write('m14_fig_order.svg', s)
    return E, pred


# =========================================================================
# Fig. 4.  CHECK 3.  Sedov density at t = 1.
# =========================================================================

def build_sedov():
    d = np.load(os.path.join(HERE, 'm14_sedov_profiles.npz'))
    W, H = 680, 400
    X0, X1, Y0, Y1 = 70.0, 640.0, 24.0, 340.0
    XLO, XHI, RLO, RHI = 0.0, 1.2, 0.0, 6.5

    def px(v):
        return X0 + (v - XLO)/(XHI - XLO)*(X1 - X0)

    def py(v):
        return Y1 - (v - RLO)/(RHI - RLO)*(Y1 - Y0)

    lam, g = d['lam'], d['g']
    R = M.M08_XI0_14*M.KT_E**0.2
    xs = np.concatenate((lam[::-1]*R, [R, R, 1.2]))
    ys = np.concatenate((g[::-1], [6.0, 1.0, 1.0]))
    s = head(W, H, 'Density against radius at time 1 for the Sedov point '
             'blast of Kamm and Timmes. The exact profile rises steeply to '
             '6 at radius 1 and drops to 1 outside. The Godunov profiles '
             'at 100, 200 and 400 cells peak at 3.06, 3.76 and 4.40, just '
             'inside radius 1, and their outer edges approach radius 1 as '
             'the cells shrink.')
    frame(s, X0, Y0, X1, Y1)
    for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2):
        tick(s, px(v), Y1, px(v), Y1 + 5)
        text(s, px(v), Y1 + 18, f'{v:g}', 10.5, MUT, "middle")
    for v in range(0, 7):
        tick(s, X0 - 5, py(v), X0, py(v))
        text(s, X0 - 8, py(v) + 4, f'{v}', 10.5, MUT, "end")
    s.append(f'<path d="{path(px(xs), py(ys))}" fill="none" stroke="{FG}" '
             f'stroke-width="1.8"/>')
    cols = {100: VIO, 200: ACC2, 400: ACC}
    for n, col in cols.items():
        s.append(f'<path d="{path(px(d[f"r{n}"]), py(d[f"rho{n}"]))}" '
                 f'fill="none" stroke="{col}" stroke-width="1.8"/>')
    lx = px(0.08)
    rows = ((FG, 'exact (Module 8, &#958;' + SUB.format('0') + ' = 1.032777)'),
            (VIO, 'Godunov, 100 cells: peak 3.06'),
            (ACC2, 'Godunov, 200 cells: peak 3.76'),
            (ACC, 'Godunov, 400 cells: peak 4.40'))
    for i, (col, lab) in enumerate(rows):
        y = py(6.1) + 18*i
        swatch(s, lx, y, col)
        text(s, lx + 28, y, lab, 11, col)
    text(s, px(1.0) + 6, py(6.0) + 4, 'jump ceiling 6', 10.5, MUT)
    text(s, (X0 + X1)/2, Y1 + 40, 'r', 11.5, FG, "middle")
    text(s, 22, (Y0 + Y1)/2, '&#961;', 12, FG, "middle")
    write('m14_fig_sedov.svg', s)


# =========================================================================
# Fig. 5.  CHECK 4.  SPH pressure near the contact.
# =========================================================================

def build_blip(runs):
    W, H = 680, 380
    X0, X1, Y0, Y1 = 80.0, 640.0, 24.0, 320.0
    XLO, XHI, PLO, PHI = 0.45, 0.90, 0.26, 0.345

    def px(v):
        return X0 + (v - XLO)/(XHI - XLO)*(X1 - X0)

    def py(v):
        return Y1 - (v - PLO)/(PHI - PLO)*(Y1 - Y0)

    w = S.riemann_waves(*M.SOD_L, *M.SOD_R, M.GAMMA_SOD)
    ps = w['p_star']
    xc = 0.5 + w['u_star']*M.SOD_T
    s = head(W, H, 'Pressure against position between 0.45 and 0.9 at '
             'time 0.2, SPH with 800 particles per unit length. The exact '
             'pressure is flat at 0.30313 from the fan tail to the shock. '
             'Standard SPH shows a spike of about 9 per cent at the '
             'contact at 0.685; with artificial conductivity the spike is '
             'about 2 per cent.')
    frame(s, X0, Y0, X1, Y1)
    for v in (0.5, 0.6, 0.7, 0.8, 0.9):
        tick(s, px(v), Y1, px(v), Y1 + 5)
        text(s, px(v), Y1 + 18, f'{v:g}', 10.5, MUT, "middle")
    for v in (0.27, 0.29, 0.31, 0.33):
        tick(s, X0 - 5, py(v), X0, py(v))
        text(s, X0 - 8, py(v) + 4, f'{v:.2f}', 10.5, MUT, "end")
    s.append(f'<line x1="{X0:.1f}" y1="{py(ps):.1f}" x2="{X1:.1f}" '
             f'y2="{py(ps):.1f}" stroke="{FG}" stroke-width="1.4" '
             f'stroke-dasharray="5 4"/>')
    s.append(f'<line x1="{px(xc):.1f}" y1="{Y0:.1f}" x2="{px(xc):.1f}" '
             f'y2="{Y1:.1f}" stroke="{MUT}" stroke-width="1" '
             f'stroke-dasharray="2 3"/>')
    for (x, P), col in zip(runs, (RED, ACC2)):
        sel = (x > XLO) & (x < XHI) & (P > PLO) & (P < PHI)
        s.append(f'<path d="{path(px(x[sel]), py(P[sel]))}" fill="none" '
                 f'stroke="{col}" stroke-width="1.8"/>')
    lx = px(0.52)
    for i, (col, dash, lab) in enumerate((
            (FG, "5 4", 'exact p* = 0.30313'),
            (RED, None, 'SPH, standard: +9.4 per cent at the contact'),
            (ACC2, None, 'SPH with conductivity: 2.2 per cent'))):
        y = py(0.2765) + 17*i
        swatch(s, lx, y, col, dash)
        text(s, lx + 28, y, lab, 11, col)
    text(s, px(xc) + 5, Y1 - 8, 'contact', 10.5, MUT)
    text(s, (X0 + X1)/2, Y1 + 40, 'x', 11.5, FG, "middle")
    text(s, 22, (Y0 + Y1)/2, 'P', 11.5, FG, "middle")
    write('m14_fig_blip.svg', s)


def main():
    build_courant()
    x, rho, v, Pp, u, m = S.sph_shock_tube(400, 1.0, 1.0, 0.125, 0.1, 1.4,
                                           M.SOD_T)
    build_sod((x, rho))
    build_order()
    build_sedov()
    runs = []
    for au in (0.0, 1.0):
        x, rho, v, Pp, u, m = S.sph_shock_tube(800, 1.0, 1.0, 0.125, 0.1,
                                               1.4, M.SOD_T, alpha_u=au)
        runs.append((x, Pp))
    build_blip(runs)
    print('five figures written')


if __name__ == '__main__':
    main()
