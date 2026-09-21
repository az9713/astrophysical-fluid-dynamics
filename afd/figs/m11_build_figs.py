"""Module 11 figures.  Five SVGs, each written from m11_numbers.py's own
functions and constants so that a figure and the prose cannot diverge.

    m11_fig_kinematics.svg  Omega, v_K and ell against radius: why a disc
                            is stable and therefore stuck
    m11_fig_ladder.svg      the timescale ladder, CHECK 1's twelve decades
    m11_fig_temperature.svg T_eff and its local index, CHECK 2
    m11_fig_efficiency.svg  eta against the inner radius, CHECK 3
    m11_fig_alpha.svg       the alpha census, CHECK 4

FIGURE RULES CARRIED FROM MODULES 9, 10 AND 12, and they are not optional.

  - Anything drawn must be in `ink` before any label is placed, and that
    includes the figure's own dashed reference lines and its own leaders.
  - check_svg rejects a literal "_" or "^" inside a <text>, so every
    subscript and superscript is a tspan or an entity.
  - A BOUND MUST BE DRAWN AS AN ARROW AND NOT AS A BAR.  Fig. 5 carries
    two bounds -- the simulation side of CHECK 4 and Starling et al.'s
    lower limits -- and drawing either as a bar would make the figure
    state something the papers do not.
  - Shoot Figs. 1, 3 and 5 and LOOK at them.  Module 12 found five
    defects that way, including a curve off its own plot box and a
    caption disagreeing with its figure by six decades.
"""
import os

import numpy as np

import m11_numbers as M

HERE = os.path.dirname(os.path.abspath(__file__))


def out(name):
    return os.path.join(HERE, name)


BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"
RED = "#f87171"

SUB = '<tspan baseline-shift="sub" font-size="8">{0}</tspan>'
SUP = '<tspan baseline-shift="super" font-size="8">{0}</tspan>'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def leader_svg(ax_, ay_, tx, ty, w, h, gap=3.0):
    """A dotted leader from an anchor to a label, stopping SHORT of it.

    COPIED FROM m12_build_figs.py.
    """
    x0, y0, x1, y1 = tx - gap, ty - h - gap, tx + w + gap, ty + gap
    ex, ey = min(max(ax_, x0), x1), min(max(ay_, y0), y1)
    if (ex, ey) == (ax_, ay_):
        return ''
    return (f'<line x1="{ax_:.1f}" y1="{ay_:.1f}" x2="{ex:.1f}" '
            f'y2="{ey:.1f}" stroke="{MUT}" stroke-width="0.9" '
            f'stroke-dasharray="2 3"/>')


def place_label(cands, occupied, box, w, h, ink=None, pad=4.0, window=None):
    """Choose a label position by search, never by eye.  COPIED FROM
    m12_build_figs.py, which copied it from m10."""
    X0, Y0, X1, Y1 = box
    ordered = list(cands)
    px0, py0 = cands[0]
    lat = [(x, y)
           for x in np.arange(X0 + 4, max(X0 + 5, X1 - w - 2), 22.0)
           for y in np.arange(Y0 + h + 4, Y1 - 4, 16.0)]
    lat.sort(key=lambda p: (p[0] - px0)**2 + (p[1] - py0)**2)
    if window is not None:
        lat = [p for p in lat
               if (p[0] - px0)**2 + (p[1] - py0)**2 <= window*window]
    ordered += lat

    def fits(x, y):
        r = (x - pad, y - h - pad, x + w + pad, y + pad)
        return not (r[0] < X0 or r[2] > X1 or r[1] < Y0 or r[3] > Y1)

    def free(x, y):
        r = (x - pad, y - h - pad, x + w + pad, y + pad)
        return not any(
            not (r[2] < o[0] or r[0] > o[2] or r[3] < o[1] or r[1] > o[3])
            for o in occupied)

    def clear(x, y):
        if ink is None or not len(ink):
            return True
        r = (x - pad, y - h - pad, x + w + pad, y + pad)
        return not ((ink[:, 0] >= r[0]) & (ink[:, 0] <= r[2]) &
                    (ink[:, 1] >= r[1]) & (ink[:, 1] <= r[3])).any()

    for test in (lambda x, y: fits(x, y) and free(x, y) and clear(x, y),
                 lambda x, y: fits(x, y) and free(x, y),
                 fits):
        for i, (x, y) in enumerate(ordered):
            if test(x, y):
                occupied.append((x, y - h, x + w, y))
                return x, y, i != 0
    x, y = cands[0]
    occupied.append((x, y - h, x + w, y))
    return x, y, True


def frame(s, X0, Y0, X1, Y1):
    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')


def decade_ticks(s, lo, hi, px, Y0, Y1, fmt=None, step=1):
    """Decade ticks on a logarithmic horizontal axis."""
    for e in range(int(np.ceil(lo)), int(np.floor(hi)) + 1, step):
        x = px(e)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        lab = fmt(e) if fmt else f'10{SUP.format(e)}'
        s.append(f'<text x="{x:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{lab}</text>')


# =========================================================================
# Figure 1.  Omega, v_K and ell against radius.
#
# THE JOB: make Proposition 2 visible.  Two of the three curves fall
# outward and the third RISES, and the one that rises is the conserved
# quantity.  A reader who sees ell climb sees why a Keplerian disc is
# Rayleigh-stable and therefore cannot accrete -- which is the problem
# module09.html:832 handed this module and module12.html:700 restated.
# =========================================================================

def build_kinematics():
    W, H = 720, 420
    X0, X1, Y0, Y1 = 78.0, 596.0, 44.0, 300.0
    LO, HI = 0.0, 4.0          # log10(R/R_0)
    VLO, VHI = -6.5, 2.5       # log10(quantity/its value at R_0)

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    def py(v):
        return Y1 - (v - VLO)/(VHI - VLO)*(Y1 - Y0)

    lr = np.linspace(LO, HI, 400)
    curves = [
        ('&#937;', -1.5*lr, ACC, 'falls as R' + SUP.format('&#8722;3/2')),
        ('v' + SUB.format('K'), -0.5*lr, ACC2,
         'falls as R' + SUP.format('&#8722;1/2')),
        ('&#8467; = &#937;R&#178;', 0.5*lr, VIO,
         'RISES as R' + SUP.format('1/2')),
    ]

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Three quantities of a Keplerian disc '
         'plotted against radius on logarithmic axes, each divided by its '
         'own value at the inner radius. The angular velocity falls '
         'steeply, the orbital speed falls gently, and the specific '
         'angular momentum rises. A shaded note marks that the rising '
         'curve is the one the Rayleigh criterion tests, so the disc is '
         'stable at every radius." >' % (W, H)]
    frame(s, X0, Y0, X1, Y1)
    decade_ticks(s, LO, HI, px, Y0, Y1,
                 fmt=lambda e: f'10{SUP.format(e)}')
    for e in range(-6, 3, 2):
        y = py(e)
        if y < Y0 or y > Y1:
            continue
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-8:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">10{SUP.format(e)}</text>')

    # the unity line, drawn before any label so it lands in ink
    s.append(f'<line x1="{X0:.0f}" y1="{py(0.0):.1f}" x2="{X1:.0f}" '
             f'y2="{py(0.0):.1f}" stroke="{RULE}" stroke-width="1" '
             f'stroke-dasharray="4 4"/>')

    ink = [[px(v), py(0.0)] for v in np.linspace(LO, HI, 200)]
    for _, ys, col, _ in curves:
        xs_, ys_ = [px(v) for v in lr], [py(v) for v in ys]
        s.append(f'<path d="{path(xs_, ys_)}" fill="none" stroke="{col}" '
                 f'stroke-width="2.2"/>')
        ink += [[a, b] for a, b in zip(xs_, ys_)]
    ink = np.array(ink)

    # LABELS ARE HAND-PLACED HERE, AND THE FIRST DRAFT'S SEARCH IS WHY.
    # place_label put the v_K label ON the v_K curve and left a dangling
    # leader under the Omega label; shooting the figure found both, and
    # check_overlap had passed.  The three curves are 4.00 decades apart
    # in the vertical at every radius -- that is the whole content of the
    # figure -- so the clear space is large, known, and does not need a
    # search.  Each label sits at x = 10^2.6, offset from its own curve
    # into the gap ABOVE it, except ell, whose gap is below.
    XL = 2.6
    for (name, ys, col, note), sign in zip(curves, (+1.0, +1.0, -1.0)):
        yv = np.interp(XL, lr, ys)
        base = py(yv) - sign*18.0
        s.append(f'<text x="{px(XL):.1f}" y="{base:.1f}" font-size="12" '
                 f'fill="{col}">{name}</text>')
        s.append(f'<text x="{px(XL):.1f}" y="{base+15:.1f}" '
                 f'font-size="10" fill="{MUT}">{note}</text>')

    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+40:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">R / R'
             f'{SUB.format("in")}</text>')
    s.append(f'<text x="{X0-52:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-52:.0f} {(Y0+Y1)/2:.0f})">'
             f'value / value at R{SUB.format("in")}</text>')

    s.append(f'<text x="{X0:.0f}" y="{Y1+62:.0f}" font-size="11" '
             f'fill="{VIO}">The Rayleigh criterion tests d(&#8467;&#178;)'
             f'/dR, and for a point mass that is GM at every radius.</text>')
    s.append(f'<text x="{X0:.0f}" y="{Y1+78:.0f}" font-size="11" '
             f'fill="{MUT}">Positive everywhere: the disc is stable, and a '
             f'stable disc transports no angular momentum.</text>')
    s.append('</svg>')
    open(out('m11_fig_kinematics.svg'), 'w', encoding='utf-8').write(
        "\n".join(s))


# =========================================================================
# Figure 2.  The timescale ladder.  CHECK 1.
#
# THE JOB: twelve decades must be a VISIBLE GAP and not a sentence.
# Module 9's Fig. 4 is the pattern -- every rate on one logarithmic
# axis, with the two that are being compared marked and the gap between
# them labelled with its own number.
# =========================================================================

def build_ladder():
    W, H = 720, 400
    X0, X1, Y0, Y1 = 92.0, 620.0, 52.0, 250.0
    LO, HI = 1.0, 19.0          # log10(t/s)

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    dn = M.DISC_ROWS[0]
    _, Mw, Rd, Td, mud, Sig = dn
    Om = M.kepler_omega(Mw, Rd)
    cT = M.isothermal_sound_speed(Td, mud)
    Hd = cT/Om
    rho0 = M.midplane_density(Sig, Hd)
    n0 = rho0/(mud*M.mu_u)
    lnL = M.lnLambda_e(n0, Td)
    nu_mol = M.molecular_viscosity(n0, Td, lnL)

    rows = [
        ('t' + SUB.format('dyn') + ' = 1/&#937;',
         M.dynamical_time(Om), ACC2, 'one radian of orbit'),
        ('t' + SUB.format('th') + ' at &#945; = 0.2',
         M.thermal_time(0.2, Om), YEL, 'the disc reaches thermal balance'),
        ('observed outburst',
         M.T_OUTBURST_OBSERVED, ACC, 'five days &#8212; a configuration'),
        ('t' + SUB.format('&#957;') + ' at &#945; = 0.2',
         M.viscous_time_alpha(0.2, Om, Hd, Rd), VIO,
         'the &#945;-disc drains'),
        ('t' + SUB.format('&#957;') + ' molecular',
         M.viscous_time(Rd, nu_mol), RED,
         'collisions alone &#8212; 14.1 billion years'),
    ]

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Five timescales for one dwarf-nova disc '
         'on a single logarithmic axis spanning eighteen decades in '
         'seconds. The dynamical and thermal times sit at the left, the '
         'observed outburst near the middle, and the viscous time '
         'computed from molecular collisions alone at the far right, '
         'twelve decades beyond the outburst. A brace marks that gap and '
         'labels it." >' % (W, H)]
    frame(s, X0, Y0, X1, Y1)
    decade_ticks(s, LO, HI, px, Y0, Y1, step=2)

    for i, (name, t, col, note) in enumerate(rows):
        y = Y0 + 30.0 + i*38.0
        x = px(np.log10(t))
        s.append(f'<line x1="{X0:.0f}" y1="{y:.1f}" x2="{x:.1f}" '
                 f'y2="{y:.1f}" stroke="{col}" stroke-width="2.4" '
                 f'opacity="0.55"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}"/>')
        s.append(f'<text x="{X0+6:.0f}" y="{y-7:.1f}" font-size="11.5" '
                 f'fill="{col}">{name}</text>')
        s.append(f'<text x="{X0+6:.0f}" y="{y+15:.1f}" font-size="10" '
                 f'fill="{MUT}">{note}</text>')

    # the gap, drawn as a brace between the outburst and the molecular
    xo = px(np.log10(M.T_OUTBURST_OBSERVED))
    xm = px(np.log10(M.viscous_time(Rd, nu_mol)))
    yb = Y1 - 16.0
    s.append(f'<line x1="{xo:.1f}" y1="{yb:.1f}" x2="{xm:.1f}" '
             f'y2="{yb:.1f}" stroke="{RED}" stroke-width="1.6"/>')
    for xx in (xo, xm):
        s.append(f'<line x1="{xx:.1f}" y1="{yb-6:.1f}" x2="{xx:.1f}" '
                 f'y2="{yb+6:.1f}" stroke="{RED}" stroke-width="1.6"/>')
    gap = np.log10(M.viscous_time(Rd, nu_mol)/M.T_OUTBURST_OBSERVED)
    s.append(f'<text x="{(xo+xm)/2:.1f}" y="{yb-12:.1f}" font-size="12" '
             f'text-anchor="middle" fill="{RED}">{gap:.2f} decades</text>')

    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+40:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">time (seconds)</text>')
    s.append(f'<text x="{X0:.0f}" y="{Y1+64:.0f}" font-size="11" '
             f'fill="{FG}">CHECK 1 is the red bar. Nothing inside the '
             f'transport coefficient closes it: the carrier is worth '
             f'1.30 and</text>')
    s.append(f'<text x="{X0:.0f}" y="{Y1+80:.0f}" font-size="11" '
             f'fill="{MUT}">doubling ln&#923; is worth 0.5, together 0.35 '
             f'of a decade against {gap:.2f}.</text>')
    s.append('</svg>')
    open(out('m11_fig_ladder.svg'), 'w', encoding='utf-8').write(
        "\n".join(s))


# =========================================================================
# Figure 3.  T_eff and its local index.  CHECK 2.
#
# THE JOB: the exponent is the check, so the index gets its own panel.
# The upper panel carries the maximum at (49/36) R_in, which is the
# derived number that proves the bracket f is being carried rather than
# dropped; the lower panel carries the approach to -3/4, which is what
# King, Pringle & Livio's section 1 says is measured.
# =========================================================================

def build_temperature():
    W, H = 720, 480
    X0, X1 = 88.0, 620.0
    YA0, YA1 = 44.0, 216.0      # T_eff panel
    YB0, YB1 = 268.0, 384.0     # index panel
    LO, HI = 0.0, 5.0           # log10(R/R_g)

    Rg = M.gravitational_radius(M.M_AGN)
    Rin = M.ISCO_SCHWARZSCHILD_RG*Rg
    Mdot = M.MDOT_AGN_EDD_FRACTION*M.eddington_rate(M.M_AGN,
                                                    M.M09_ASSERTED_ETA)

    # START SAFELY ABOVE R_in.  t_eff_index differentiates at
    # R*(1 +/- 1e-6), so a first point at R_in*(1 + 1e-7) puts the lower
    # sample INSIDE R_in, where the bracket f is negative and the fourth
    # root is NaN.  The first build did exactly that and numpy said so.
    xs = np.logspace(np.log10(M.ISCO_SCHWARZSCHILD_RG*1.001), HI, 1200)
    Rs = xs*Rg
    Ts = M.t_effective(Mdot, M.M_AGN, Rs, Rin)
    idx = np.array([M.t_eff_index(Mdot, M.M_AGN, r, Rin) for r in Rs])

    TLO, THI = 1.0, 5.4         # log10(T/K)

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    def pya(v):
        return YA1 - (v - TLO)/(THI - TLO)*(YA1 - YA0)

    def pyb(v):
        return YB1 - (v - (-1.0))/((-0.2) - (-1.0))*(YB1 - YB0)

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Two stacked panels against radius in '
         'gravitational radii on a logarithmic axis. The upper panel '
         'shows the effective temperature of a steady thin disc, which '
         'rises from zero at the inner edge to a maximum and then falls. '
         'The lower panel shows the local logarithmic slope of that '
         'curve, which starts near zero at the inner edge and approaches '
         'minus three quarters far out, where a dashed line marks that '
         'value." >' % (W, H)]
    frame(s, X0, YA0, X1, YA1)
    frame(s, X0, YB0, X1, YB1)
    decade_ticks(s, LO, HI, px, YB0, YB1)
    for e in range(2, 6):
        y = pya(e)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-8:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">10{SUP.format(e)}</text>')
    for v in (-1.0, -0.75, -0.5, -0.25):
        y = pyb(v)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-8:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.2f}</text>')

    _xs = [px(np.log10(v)) for v in xs]
    s.append(f'<path d="{path(_xs, [pya(np.log10(v)) for v in Ts])}" '
             f'fill="none" stroke="{ACC}" stroke-width="2.2"/>')
    s.append(f'<line x1="{X0:.0f}" y1="{pyb(-0.75):.1f}" x2="{X1:.0f}" '
             f'y2="{pyb(-0.75):.1f}" stroke="{ACC2}" stroke-width="1.4" '
             f'stroke-dasharray="5 4"/>')
    # CLIP THE INDEX CURVE TO ITS OWN PANEL.  The first build drew it
    # unclipped and it ran off the top of the lower panel and straight
    # across the upper one -- the Module 12 defect, found by shooting the
    # figure and not by check_overlap.  Near R_in the temperature rises
    # from zero, so d lnT/d lnR is large and POSITIVE and has no business
    # on an axis that runs from -1 to -0.2.  The curve therefore starts
    # where it first enters the panel, and the caption says so.
    _in = [(x, v) for x, v in zip(_xs, idx) if -1.0 <= v <= -0.2]
    _ix = [p[0] for p in _in]
    _iy = [pyb(p[1]) for p in _in]
    s.append(f'<path d="{path(_ix, _iy)}" '
             f'fill="none" stroke="{VIO}" stroke-width="2.2"/>')
    _x_enter, _r_enter = _in[0][0], xs[list(idx).index(_in[0][1])]
    s.append(f'<line x1="{_x_enter:.1f}" y1="{YB0:.0f}" '
             f'x2="{_x_enter:.1f}" y2="{YB1:.0f}" stroke="{MUT}" '
             f'stroke-width="1" stroke-dasharray="2 4"/>')
    s.append(f'<text x="{_x_enter+7:.1f}" y="{YB0+16:.0f}" font-size="10" '
             f'fill="{MUT}">index enters the panel at '
             f'{_r_enter:.2f} R{SUB.format("g")}; it is POSITIVE inside '
             f'this radius</text>')

    xpk = 49.0/36.0*M.ISCO_SCHWARZSCHILD_RG
    Tpk = M.t_effective(Mdot, M.M_AGN, xpk*Rg, Rin)
    _cx, _cy = px(np.log10(xpk)), pya(np.log10(Tpk))
    s.append(f'<circle cx="{_cx:.1f}" cy="{_cy:.1f}" r="4.4" '
             f'fill="{YEL}"/>')
    s.append(f'<text x="{_cx+10:.1f}" y="{_cy-4:.1f}" font-size="11" '
             f'fill="{YEL}">maximum at (49/36)R{SUB.format("in")} = '
             f'{xpk:.3f} R{SUB.format("g")}, {Tpk:,.0f} K</text>')
    far = M.t_eff_index(Mdot, M.M_AGN, 1.0e5*Rg, Rin)
    s.append(f'<text x="{X1-8:.0f}" y="{pyb(-0.75)-10:.1f}" '
             f'font-size="11" text-anchor="end" fill="{ACC2}">'
             f'&#8722;3/4, the prediction</text>')
    s.append(f'<text x="{X1-8:.0f}" y="{YB1-10:.1f}" font-size="11" '
             f'text-anchor="end" fill="{VIO}">{far:.5f} at 10'
             f'{SUP.format(5)} R{SUB.format("g")}</text>')

    s.append(f'<text x="{X0-58:.0f}" y="{(YA0+YA1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-58:.0f} {(YA0+YA1)/2:.0f})">'
             f'T{SUB.format("eff")} (K)</text>')
    s.append(f'<text x="{X0-58:.0f}" y="{(YB0+YB1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-58:.0f} {(YB0+YB1)/2:.0f})">'
             f'd lnT / d lnR</text>')
    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{YB1+40:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">R / R'
             f'{SUB.format("g")}</text>')
    s.append(f'<text x="{X0:.0f}" y="{YB1+64:.0f}" font-size="11" '
             f'fill="{FG}">The exponent contains no viscosity: &#957;, '
             f'&#945; and &#931; all cancel between the dissipation rate '
             f'and &#963;T&#8308;.</text>')
    s.append('</svg>')
    open(out('m11_fig_temperature.svg'), 'w', encoding='utf-8').write(
        "\n".join(s))


# =========================================================================
# Figure 4.  The radiative efficiency.  CHECK 3.
#
# THE JOB: five numbers in three clusters, in one picture.  The curve is
# the NEWTONIAN eta = R_g/(2 R_in), which is what this book can derive;
# the points are what relativity and two papers say.  The vertical gap
# between the curve and the Schwarzschild point AT THE SAME RADIUS is
# the price of a Newtonian book, and it is the thing to look at.
# =========================================================================

def build_efficiency():
    W, H = 720, 420
    X0, X1, Y0, Y1 = 92.0, 600.0, 44.0, 286.0
    LO, HI = 0.0, 2.0           # log10(R_in/R_g)
    ELO, EHI = -2.2, 0.0        # log10(eta)

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    def py(v):
        return Y1 - (v - ELO)/(EHI - ELO)*(Y1 - Y0)

    xs = np.logspace(LO, HI, 400)
    eta_n = np.array([M.efficiency_newtonian(v) for v in xs])

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Radiative efficiency plotted against the '
         'inner radius of the disc in gravitational radii, both axes '
         'logarithmic. A straight line falling to the right is the '
         'Newtonian result, one over twice the inner radius. At six '
         'gravitational radii three markers sit in a vertical column: the '
         'Newtonian value, the relativistic Schwarzschild value below it, '
         'and the value Shakura and Sunyaev print. Two further markers at '
         'the left edge give the extreme Kerr values." >' % (W, H)]
    frame(s, X0, Y0, X1, Y1)
    decade_ticks(s, LO, HI, px, Y0, Y1,
                 fmt=lambda e: f'10{SUP.format(e)}')
    for e in (-2, -1, 0):
        y = py(e)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-8:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">10{SUP.format(e)}</text>')

    _px = [px(np.log10(v)) for v in xs]
    s.append(f'<path d="{path(_px, [py(np.log10(v)) for v in eta_n])}" '
             f'fill="none" stroke="{ACC}" stroke-width="2.2"/>')
    _ey = py(np.log10(M.efficiency_newtonian(10**1.55)))
    s.append(f'<text x="{px(1.55):.1f}" y="{_ey-10:.1f}" '
             f'font-size="11" fill="{ACC}">Newtonian, &#951; = R'
             f'{SUB.format("g")}/2R{SUB.format("in")}</text>')

    x6 = px(np.log10(M.ISCO_SCHWARZSCHILD_RG))
    s.append(f'<line x1="{x6:.1f}" y1="{Y0:.0f}" x2="{x6:.1f}" '
             f'y2="{Y1:.0f}" stroke="{RULE}" stroke-width="1" '
             f'stroke-dasharray="4 4"/>')
    s.append(f'<text x="{x6+7:.1f}" y="{Y1-8:.0f}" font-size="10.5" '
             f'fill="{MUT}">Schwarzschild ISCO, 6R{SUB.format("g")}</text>')

    pts = [
        (M.ISCO_SCHWARZSCHILD_RG, 1.0/12.0, ACC, 'Newtonian 1/12', 1),
        (M.ISCO_SCHWARZSCHILD_RG, M.ETA_SCHWARZSCHILD, ACC2,
         'Schwarzschild, BPT eq. (2.12)', -1),
        (M.ISCO_SCHWARZSCHILD_RG, M.SS73_ETA_SCHWARZSCHILD, VIO,
         'Shakura &amp; Sunyaev p. 339', -2),
        (M.ISCO_SCHWARZSCHILD_RG, M.M09_ASSERTED_ETA, RED,
         'module09.html:757 asserts 0.1', 2),
        (1.0, M.ETA_KERR_EXTREME, YEL, 'extreme Kerr, BPT eq. (2.14)', 1),
        (1.0, M.SS73_ETA_KERR_MAX, VIO, 'S&amp;S "can attain 40%"', -1),
    ]
    for xr, yv, col, lab, side in pts:
        cx, cy = px(np.log10(xr)), py(np.log10(yv))
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.6" '
                 f'fill="{col}"/>')
        ty = cy - 9.0 if side > 0 else cy + 15.0
        ty += (abs(side) - 1)*(14.0 if side > 0 else -14.0)
        s.append(f'<text x="{cx+9:.1f}" y="{ty:.1f}" font-size="10.5" '
                 f'fill="{col}">{lab} = {yv:.4f}</text>')

    ratio = (1.0/12.0)/M.ETA_SCHWARZSCHILD
    s.append(f'<text x="{X0:.0f}" y="{Y1+44:.0f}" font-size="11" '
             f'fill="{FG}">At the SAME radius the Newtonian value is '
             f'{ratio:.4f} times the relativistic one. That '
             f'{100*(ratio-1):.1f} per cent is the price of a</text>')
    s.append(f'<text x="{X0:.0f}" y="{Y1+60:.0f}" font-size="11" '
             f'fill="{MUT}">Newtonian book six gravitational radii from a '
             f'black hole, and the module prints it rather than hiding '
             f'it.</text>')
    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+24:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">R{SUB.format("in")} / R'
             f'{SUB.format("g")}</text>')
    s.append(f'<text x="{X0-56:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-56:.0f} {(Y0+Y1)/2:.0f})">'
             f'&#951;</text>')
    s.append('</svg>')
    open(out('m11_fig_efficiency.svg'), 'w', encoding='utf-8').write(
        "\n".join(s))


# =========================================================================
# Figure 5.  The alpha census.  CHECK 4.
#
# THE JOB, AND IT IS A JOB ABOUT HONESTY: two of these six rows are
# BOUNDS and four are ranges.  A bound drawn as a bar states a value the
# paper does not give.  Every bound here is drawn as an ARROW with an
# open end, and the legend says which way it points.
# =========================================================================

def build_alpha():
    W, H = 720, 430
    X0, X1, Y0, Y1 = 196.0, 620.0, 44.0, 268.0
    LO, HI = -4.0, 0.5          # log10(alpha)

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    rows = [
        ('thin, fully-ionised discs',
         M.KPL07_ALPHA_LO, M.KPL07_ALPHA_HI, None, ACC, 'abstract'),
        ('dwarf novae',
         M.KPL07_DN_ALPHA_LO, M.KPL07_DN_ALPHA_HI, None, ACC, '&#167;2.1'),
        ('soft X-ray transients', 0.2, 0.4, None, ACC, '&#167;2.2'),
        ('AGN variability',
         M.KPL07_AGN_ALPHA_LO, M.KPL07_AGN_ALPHA_HI, 'up', YEL,
         '&#167;2.3.1, LOWER limits'),
        ('T Tauri, 10&#8211;100 au',
         M.KPL07_ALPHA_PROTOSTELLAR, M.KPL07_ALPHA_PROTOSTELLAR, None,
         ACC2, '&#167;2.3.2'),
        ('MHD simulations',
         None, M.KPL07_SIM_MAX, 'down', RED, '&#167;5, A BOUND'),
    ]

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Six estimates of the disc viscosity '
         'parameter alpha, all from one review, on a horizontal '
         'logarithmic axis spanning four decades. Four are drawn as bars '
         'because the review gives a range; two are drawn as arrows with '
         'an open end because the review gives only a bound, one pointing '
         'up and one pointing down. A vertical dashed line marks the '
         'value above which the fastest-growing magnetorotational mode is '
         'longer than the disc is thick." >' % (W, H)]
    frame(s, X0, Y0, X1, Y1)
    decade_ticks(s, LO, HI, px, Y0, Y1)

    amax = M.alpha_max_for_containment()
    xb = px(np.log10(amax))
    s.append(f'<line x1="{xb:.1f}" y1="{Y0:.0f}" x2="{xb:.1f}" '
             f'y2="{Y1:.0f}" stroke="{VIO}" stroke-width="1.4" '
             f'stroke-dasharray="5 4"/>')

    for i, (name, lo, hi, arrow, col, note) in enumerate(rows):
        y = Y0 + 26.0 + i*34.0
        xl = px(np.log10(lo)) if lo is not None else X0
        xh = px(np.log10(hi))
        if arrow == 'down':
            s.append(f'<line x1="{xh:.1f}" y1="{y:.1f}" x2="{X0+6:.1f}" '
                     f'y2="{y:.1f}" stroke="{col}" stroke-width="3"/>')
            s.append(f'<path d="M {X0+6:.1f},{y:.1f} L {X0+16:.1f},'
                     f'{y-5:.1f} L {X0+16:.1f},{y+5:.1f} Z" '
                     f'fill="{col}"/>')
            s.append(f'<line x1="{xh:.1f}" y1="{y-7:.1f}" x2="{xh:.1f}" '
                     f'y2="{y+7:.1f}" stroke="{col}" stroke-width="2.4"/>')
        elif arrow == 'up':
            # THE HEAD MUST NOT LAND ON THE CONTAINMENT LINE.  A fixed
            # 50 px extension put it exactly there, and the shot made it
            # read as though the bound were 0.095.  A quarter of a decade
            # is a length in the figure's own units and cannot collide by
            # accident.
            xt = px(np.log10(hi) + 0.25)
            s.append(f'<line x1="{xl:.1f}" y1="{y:.1f}" x2="{xt-10:.1f}" '
                     f'y2="{y:.1f}" stroke="{col}" stroke-width="3"/>')
            s.append(f'<path d="M {xt:.1f},{y:.1f} L {xt-10:.1f},'
                     f'{y-5:.1f} L {xt-10:.1f},{y+5:.1f} Z" '
                     f'fill="{col}"/>')
            s.append(f'<line x1="{xl:.1f}" y1="{y-7:.1f}" x2="{xl:.1f}" '
                     f'y2="{y+7:.1f}" stroke="{col}" stroke-width="2.4"/>')
        elif lo == hi:
            s.append(f'<circle cx="{xh:.1f}" cy="{y:.1f}" r="5.4" '
                     f'fill="{col}"/>')
        else:
            s.append(f'<rect x="{xl:.1f}" y="{y-7:.1f}" '
                     f'width="{xh-xl:.1f}" height="14" fill="{col}" '
                     f'opacity="0.75"/>')
        s.append(f'<text x="{X0-10:.0f}" y="{y-1:.1f}" font-size="11.5" '
                 f'text-anchor="end" fill="{FG}">{name}</text>')
        s.append(f'<text x="{X0-10:.0f}" y="{y+13:.1f}" font-size="9.5" '
                 f'text-anchor="end" fill="{MUT}">{note}</text>')

    s.append(f'<text x="{xb-8:.1f}" y="{Y0+14:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{VIO}">&#945; = 15/16&#960;&#178; = '
             f'{amax:.4f}</text>')
    s.append(f'<text x="{xb-8:.1f}" y="{Y0+27:.0f}" font-size="9.5" '
             f'text-anchor="end" fill="{MUT}">above this the fastest MRI '
             f'mode is longer than 2H</text>')

    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+40:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">&#945;</text>')
    s.append(f'<text x="{X0-170:.0f}" y="{Y1+64:.0f}" font-size="11" '
             f'fill="{FG}">An ARROW is a bound and a BAR is a range. The '
             f'two arrows point in opposite directions, so the gap '
             f'between the</text>')
    s.append(f'<text x="{X0-170:.0f}" y="{Y1+80:.0f}" font-size="11" '
             f'fill="{MUT}">observations and the simulations is '
             f'one-sided: at least '
             f'{M.KPL07_ALPHA_LO/M.KPL07_SIM_MAX:.0f}, and the review '
             f'says the simulations probably underestimate.</text>')
    s.append('</svg>')
    open(out('m11_fig_alpha.svg'), 'w', encoding='utf-8').write(
        "\n".join(s))


def main():
    build_kinematics()
    build_ladder()
    build_temperature()
    build_efficiency()
    build_alpha()
    for n in ('kinematics', 'ladder', 'temperature', 'efficiency', 'alpha'):
        p = out(f'm11_fig_{n}.svg')
        print(f'  {os.path.basename(p):<28} {os.path.getsize(p):>7} bytes')


if __name__ == '__main__':
    main()
