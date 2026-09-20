"""Module 12 figures.  Five SVGs, each written from m12_numbers.py's own
functions and constants so that a figure and the prose cannot diverge.

    m12_fig_census.svg     the two pressures, and the beta = 1 diagonal
    m12_fig_spiral.svg     the Parker spiral, and the field index it makes
    m12_fig_alfven.svg     the wind crossing its own radial Alfven speed
    m12_fig_transport.svg  the transport ladder, over thirty decades
    m12_fig_mri.svg        the magnetorotational growth rate

FIGURE RULES CARRIED FROM MODULES 9 AND 10, and they are not optional.

  - Anything drawn must be in `ink` before any label is placed, and that
    includes the figure's own dashed reference lines and its own leaders.
    Module 10 step 4 found three separate check_overlap failures and only
    one of them was a label-placement problem.
  - ink=None is sometimes right.  A label beside its own point crossing a
    grey identity line is correct; a label in clear space beside somebody
    else's point is wrong.
  - check_svg rejects a literal "_" or "^" inside a <text>, so every
    subscript and superscript is a tspan.
  - Shoot Figs. 1, 3 and 5 and LOOK at them.  check_overlap reads
    geometry; only a rendered look finds a semantically wrong label.
"""
import os

import numpy as np

import m12_numbers as M

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
    """A dotted leader from an anchor to a label, stopping SHORT of it."""
    x0, y0, x1, y1 = tx - gap, ty - h - gap, tx + w + gap, ty + gap
    ex, ey = min(max(ax_, x0), x1), min(max(ay_, y0), y1)
    if (ex, ey) == (ax_, ay_):
        return ''
    return (f'<line x1="{ax_:.1f}" y1="{ay_:.1f}" x2="{ex:.1f}" '
            f'y2="{ey:.1f}" stroke="{MUT}" stroke-width="0.9" '
            f'stroke-dasharray="2 3"/>')


def place_label(cands, occupied, box, w, h, ink=None, pad=4.0, window=None):
    """Choose a label position by search, never by eye.  From m10."""
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


# =========================================================================
# Figure 1.  The two pressures, and the beta = 1 diagonal.
#
# THE JOB: beta is a RATIO, and the same ratio occurs at pressures
# eighteen decades apart.  The active-region corona and the molecular
# cloud have IDENTICAL beta -- 0.0347 on both rows of PART A -- and
# therefore sit on the same diagonal, eighteen decades apart in absolute
# pressure.  A figure that plotted beta alone would hide that; this one
# cannot.
# =========================================================================

def build_census():
    W, H = 720, 470
    X0, X1, Y0, Y1 = 92.0, 620.0, 40.0, 350.0
    # decades of p_gas and p_mag to cover
    GX0, GX1 = -14.0, 6.0
    GY0, GY1 = -15.0, 5.0

    def px(v):
        return X0 + (v - GX0)/(GX1 - GX0)*(X1 - X0)

    def py(v):
        return Y1 - (v - GY0)/(GY1 - GY0)*(Y1 - Y0)

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Magnetic pressure plotted against gas '
         'pressure, both on logarithmic axes spanning twenty decades. A '
         'dashed diagonal marks equal pressures, plasma beta of one. Five '
         'labelled points lie on the plane: the solar photosphere far '
         'below the diagonal, the intracluster medium below it, the solar '
         'wind almost on it, and the solar corona and the molecular cloud '
         'both the same distance above it but separated along the '
         'diagonal by eighteen decades of pressure." >' % (W, H)]

    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')

    ink = []
    # axis ticks, every four decades
    for gx in np.arange(GX0, GX1 + 0.1, 4.0):
        x = px(gx)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">10{SUP.format(int(gx))}'
                 f'</text>')
    for gy in np.arange(GY0, GY1 + 0.1, 4.0):
        y = py(gy)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">10{SUP.format(int(gy))}'
                 f'</text>')

    # the beta = 1 diagonal, and two guide diagonals one hundred-fold away
    for off, col, dash, lab in ((0.0, FG, "6 4", "&#946; = 1"),
                                (-2.0, RULE, "2 5", "&#946; = 100"),
                                (+2.0, RULE, "2 5", "&#946; = 0.01")):
        xs, ys = [], []
        for gx in np.linspace(GX0, GX1, 60):
            gy = gx + off
            if GY0 <= gy <= GY1:
                xs.append(px(gx))
                ys.append(py(gy))
        if len(xs) < 2:
            continue
        s.append(f'<path d="{path(xs, ys)}" fill="none" stroke="{col}" '
                 f'stroke-width="{1.3 if off == 0 else 0.9}" '
                 f'stroke-dasharray="{dash}"/>')
        ink += list(zip(xs, ys))
        s.append(f'<text x="{xs[-1]-6:.1f}" y="{ys[-1]-7:.1f}" '
                 f'font-size="10.5" text-anchor="end" fill="{col}">'
                 f'{lab}</text>')
        ink.append((xs[-1] - 30, ys[-1] - 10))

    rows = []
    for name, n, T, B, mu in M.A_ROWS:
        pg = n*M.kB*T
        pm = M.magnetic_pressure(B)
        rows.append((name, np.log10(pg), np.log10(pm),
                     M.plasma_beta(n, T, B)))

    inka = np.array(ink) if ink else None
    occupied = []
    body = []
    for name, gx, gy, beta in rows:
        x, y = px(gx), py(gy)
        col = ACC if beta < 1.0 else ACC2
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" '
                    f'fill="{col}"/>')
        lab = f'{name} (&#946; = {beta:.3g})'
        w, h = 6.2*len(name) + 66.0, 12.0
        cands = [(x + 10, y - 8), (x - w - 10, y - 8),
                 (x + 10, y + 16), (x - w - 10, y + 16)]
        lx, ly, moved = place_label(cands, occupied, (X0, Y0, X1, Y1),
                                    w, h, ink=inka, window=320.0)
        if moved:
            body.append(leader_svg(x, y, lx, ly, w, h))
        body.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="10.5" '
                    f'fill="{col}">{lab}</text>')
    s += body

    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+40:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">gas pressure '
             f'<tspan font-style="italic">nk</tspan>'
             f'{SUB.format("B")}<tspan font-style="italic">T</tspan>'
             f' / dyn cm{SUP.format(-2)}</text>')
    s.append(f'<text x="{X0-58:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-58:.0f} {(Y0+Y1)/2:.0f})">'
             f'magnetic pressure <tspan font-style="italic">B</tspan>'
             f'{SUP.format(2)}/8&#960; / dyn cm{SUP.format(-2)}</text>')

    cor = [r for r in rows if r[0] == 'solar corona'][0]
    mc = [r for r in rows if r[0] == 'molecular cloud'][0]
    gap = cor[1] - mc[1]
    s.append(f'<text x="{X0:.0f}" y="{Y1+62:.0f}" font-size="11" '
             f'fill="{MUT}">The corona and the cloud have the SAME '
             f'&#946; = {cor[3]:.4f} and lie {gap:.1f} decades apart in '
             f'pressure.</text>')
    sw = [r for r in rows if r[0] == 'solar wind, 1 au'][0]
    sw_dec = abs(np.log10(sw[3]))
    s.append(f'<text x="{X0:.0f}" y="{Y1+80:.0f}" font-size="11" '
             f'fill="{MUT}">Orange: the field wins. Teal: the gas wins. '
             f'The solar wind sits {sw_dec:.3f} of a decade from '
             f'&#946; = 1.</text>')
    s.append('</svg>')
    open(out("m12_fig_census.svg"), "w", encoding="utf-8").write("\n".join(s))
    return rows


# =========================================================================
# Figure 2.  The Parker spiral, and the field index it makes.
#
# THE JOB: the winding is exactly what bends -2 into something near -1.6,
# and -1.76 and -1.66 are NOT distinguishable by eye over the 0.29-0.98 au
# window.  That is the visual form of "not resolved".
# =========================================================================

def build_spiral():
    W, H = 720, 400
    # --- left panel: the spiral in the ecliptic plane
    AX, AY, AR = 178.0, 190.0, 138.0     # centre and radius of the disc
    om = 2.0*np.pi/(M.CARRINGTON_SIDEREAL_DAYS*M.day)
    r0 = M.R_SOURCE_SURFACE*M.Rsun
    v_mean = M.VB18_MEAN['velocity'][0]*1e5
    rmax = 1.0*M.AU

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Left panel: one magnetic field line '
         'spiralling outward from the Sun to one astronomical unit, with '
         'the tangent at one astronomical unit drawn and its angle to the '
         'radius marked at forty-four degrees. Right panel: the total '
         'field strength against radius on logarithmic axes over the '
         'Helios range, showing the Parker curve, a straight line of '
         'slope minus two for an unwound field, and the measured '
         'power law with a shaded band for its year-to-year scatter. The '
         'Parker curve and the measured band overlap over most of the '
         'range." >' % (W, H)]

    # the Sun
    s.append(f'<circle cx="{AX:.1f}" cy="{AY:.1f}" r="7" fill="{YEL}"/>')
    s.append(f'<circle cx="{AX:.1f}" cy="{AY:.1f}" r="{AR:.1f}" '
             f'fill="none" stroke="{RULE}" stroke-width="1" '
             f'stroke-dasharray="3 4"/>')
    s.append(f'<text x="{AX:.1f}" y="{AY+AR+16:.1f}" font-size="10.5" '
             f'text-anchor="middle" fill="{MUT}">1 au</text>')

    # four field lines, launched 90 degrees apart
    for phi0 in (0.0, np.pi/2, np.pi, 3*np.pi/2):
        xs, ys = [], []
        for r in np.linspace(r0, rmax, 240):
            phi = phi0 - om*(r - r0)/v_mean
            rr = AR*r/rmax
            xs.append(AX + rr*np.cos(phi))
            ys.append(AY - rr*np.sin(phi))
        # The companions were drawn in RULE at width 1 and were
        # invisible in a render: a reader saw ONE spiral, not a
        # field.  MUT at 1.2 reads as background without vanishing.
        col = ACC if phi0 == 0.0 else MUT
        s.append(f'<path d="{path(xs, ys)}" fill="none" stroke="{col}" '
                 f'stroke-width="{2.2 if phi0 == 0.0 else 1.2}" '
                 f'opacity="{1.0 if phi0 == 0.0 else 0.75}"/>')

    # the tangent at 1 au on the highlighted line, and the angle
    phi_end = -om*(rmax - r0)/v_mean
    ex, ey = AX + AR*np.cos(phi_end), AY - AR*np.sin(phi_end)
    ang = M.spiral_angle(rmax, v_mean, om, r0=r0)
    # radial direction at that point, and the tangent rotated by `ang`
    ur = np.array([np.cos(phi_end), -np.sin(phi_end)])
    th = np.radians(ang)
    # the spiral trails BEHIND the rotation, so the tangent is rotated
    # from the radius toward +phi, which on this screen is clockwise.
    ut = np.array([ur[0]*np.cos(th) - ur[1]*np.sin(th),
                   ur[0]*np.sin(th) + ur[1]*np.cos(th)])
    s.append(f'<line x1="{ex-ur[0]*42:.1f}" y1="{ey-ur[1]*42:.1f}" '
             f'x2="{ex+ur[0]*30:.1f}" y2="{ey+ur[1]*30:.1f}" '
             f'stroke="{MUT}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="{ex-ut[0]*42:.1f}" y1="{ey-ut[1]*42:.1f}" '
             f'x2="{ex+ut[0]*30:.1f}" y2="{ey+ut[1]*30:.1f}" '
             f'stroke="{ACC2}" stroke-width="1.6"/>')
    s.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.6" fill="{ACC}"/>')
    s.append(f'<text x="{AX-AR-6:.1f}" y="{AY-AR+4:.1f}" font-size="11" '
             f'fill="{ACC2}">spiral angle {ang:.2f}&#176;</text>')
    s.append(f'<text x="{AX-AR-6:.1f}" y="{AY-AR+20:.1f}" font-size="10.5" '
             f'fill="{MUT}">at 1 au, &#937; = 2&#960;/'
             f'{M.CARRINGTON_SIDEREAL_DAYS} d</text>')
    s.append(f'<text x="{AX-AR-6:.1f}" y="{AY-AR+36:.1f}" font-size="10.5" '
             f'fill="{MUT}">v = {v_mean/1e5:.1f} km s{SUP.format(-1)}'
             f'</text>')

    # --- right panel: |B|(r) over the Helios window
    X0, X1, Y0, Y1 = 400.0, 672.0, 52.0, 300.0
    rlo, rhi = M.VB18_R_LO_AU, M.VB18_R_HI_AU
    gx0, gx1 = np.log10(rlo), np.log10(rhi)

    B1, aB = M.VB18_MEAN['field'][0], M.VB18_MEAN['field'][2]
    sc = M.VB18_SCATTER['field']
    # 400 points, the SAME grid PART E fits on.  At 120 the fitted
    # index comes out -1.7750 against PART E's -1.7751, and a figure
    # that disagrees with the prose in the fourth decimal is a figure
    # a reader has to reconcile.
    ra = np.logspace(gx0, gx1, 400)
    # the Parker prediction, normalised at 1 au to the measured 1-au value
    # parker_field's SECOND argument is the WIND SPEED, not the field.
    # The first draft of this figure passed B1 there and got a fitted
    # index of -1.03 against PART E's -1.7751; the self-check in main()
    # is what found it.  It returns a SHAPE normalised to 1 at r1.
    v1_mean = M.VB18_MEAN['velocity'][0]*1e5
    av_mean = M.VB18_MEAN['velocity'][2]
    par = B1*M.parker_field(ra*M.AU, v1_mean, om, M.AU, r0=r0,
                            alpha_v=av_mean)
    meas = B1*ra**aB
    unw = B1*ra**(-2.0)
    allv = np.concatenate([par, meas, unw,
                           B1*ra**(aB + sc), B1*ra**(aB - sc)])
    gy0, gy1 = np.log10(allv.min())*1.0, np.log10(allv.max())*1.0
    gy0, gy1 = gy0 - 0.05, gy1 + 0.05

    def px(v):
        return X0 + (np.log10(v) - gx0)/(gx1 - gx0)*(X1 - X0)

    def py(v):
        return Y1 - (np.log10(v) - gy0)/(gy1 - gy0)*(Y1 - Y0)

    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for rv in (0.3, 0.5, 0.7, 1.0):
        if not (rlo <= rv <= rhi):
            continue
        x = px(rv)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{rv:g}</text>')
    for bv in (5, 10, 20, 50):
        if not (10**gy0 <= bv <= 10**gy1):
            continue
        y = py(bv)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-8:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{bv}</text>')

    # the measured scatter band, drawn FIRST so the curves sit on it
    up = B1*ra**(aB - sc)
    dn = B1*ra**(aB + sc)
    poly = (" ".join(f"{px(r):.1f},{py(b):.1f}" for r, b in zip(ra, up)) +
            " " +
            " ".join(f"{px(r):.1f},{py(b):.1f}"
                     for r, b in zip(ra[::-1], dn[::-1])))
    s.append(f'<polygon points="{poly}" fill="{ACC2}" opacity="0.16"/>')

    for arr, col, wdt, dash in ((meas, ACC2, 2.0, ""),
                                (par, ACC, 2.0, ""),
                                (unw, MUT, 1.4, '6 4')):
        d = path([px(r) for r in ra], [py(b) for b in arr])
        da = f' stroke-dasharray="{dash}"' if dash else ''
        s.append(f'<path d="{d}" fill="none" stroke="{col}" '
                 f'stroke-width="{wdt}"{da}/>')

    fit_idx = M.loglog_fit_index(ra, par)
    s.append(f'<text x="{X0+6:.0f}" y="{Y0+16:.0f}" font-size="10.5" '
             f'fill="{ACC}">Parker, fitted index {fit_idx:.4f}</text>')
    s.append(f'<text x="{X0+6:.0f}" y="{Y0+32:.0f}" font-size="10.5" '
             f'fill="{ACC2}">measured {aB:.4f} &#177; {sc:.3f}</text>')
    s.append(f'<text x="{X0+6:.0f}" y="{Y0+48:.0f}" font-size="10.5" '
             f'fill="{MUT}">unwound radial field, &#8722;2</text>')
    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">heliocentric distance '
             f'/ au</text>')
    s.append(f'<text x="{X0-46:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-46:.0f} {(Y0+Y1)/2:.0f})">'
             f'|<tspan font-style="italic">B</tspan>| / nT</text>')
    s.append(f'<text x="{20:.0f}" y="{Y1+62:.0f}" font-size="11" '
             f'fill="{MUT}">Mean fits. The band is the YEAR-TO-YEAR '
             f'scatter {sc:.3f},</text>')
    s.append(f'<text x="{20:.0f}" y="{Y1+78:.0f}" font-size="11" '
             f'fill="{MUT}">not the formal fit error '
             f'{M.VB18_MEAN["field"][3]:.3f}.</text>')
    s.append('</svg>')
    open(out("m12_fig_spiral.svg"), "w", encoding="utf-8").write("\n".join(s))
    return fit_idx


# =========================================================================
# Figure 3.  The wind crossing its own radial Alfven speed.
#
# THE JOB: make "bracketed, matches neither" visible in one look, and make
# it visible that the BAND of eight model variants is narrower than the
# gap between the two published values.
# =========================================================================

def alfven_variants():
    """The eight r_A of PART F, rebuilt from the same calls PART F makes."""
    om = 2.0*np.pi/(M.CARRINGTON_SIDEREAL_DAYS*M.day)
    r0 = M.R_SOURCE_SURFACE*M.Rsun
    outv = []
    for label, fits in (('mean', M.VB18_MEAN), ('median', M.VB18_MEDIAN)):
        n1 = fits['density'][0]
        v1 = fits['velocity'][0]*1e5
        av = fits['velocity'][2]
        B_tot = fits['field'][0]*1e-5
        x1 = M.parker_ratio(M.AU, v1, om, r0)
        B1 = B_tot/np.sqrt(1.0 + x1*x1)
        for tag, rho in (('protons', n1*M.mp), ('4% He', n1*M.mp*1.16)):
            vA1 = M.alfven_speed(B1, rho)
            outv.append((f'{label}, {tag}, const v', v1, vA1,
                         M.alfven_radius_constant_v(M.AU, v1, vA1)))
            outv.append((f'{label}, {tag}, v ~ r^{av:+.3f}', v1, vA1,
                         M.alfven_radius_power_law(M.AU, v1, vA1, av)))
    return outv


def build_alfven():
    W, H = 720, 440
    X0, X1, Y0, Y1 = 92.0, 600.0, 46.0, 312.0
    var = alfven_variants()
    rA = np.array([v[3] for v in var])/M.Rsun
    lo, hi = rA.min(), rA.max()

    gx0, gx1 = np.log10(5.0), np.log10(240.0)     # R_sun
    gy0, gy1 = np.log10(20.0), np.log10(900.0)    # km/s

    def px(v):
        return X0 + (np.log10(v) - gx0)/(gx1 - gx0)*(X1 - X0)

    def py(v):
        return Y1 - (np.log10(v) - gy0)/(gy1 - gy0)*(Y1 - Y0)

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Wind speed and radial Alfven speed '
         'against heliocentric distance on logarithmic axes. The wind '
         'speed is nearly flat; the Alfven speed falls as one over '
         'radius and crosses it. A narrow shaded band marks the eight '
         'model crossing radii between about sixteen and nineteen solar '
         'radii. Two measured values are marked: Verscharen and '
         'colleagues at twelve solar radii, to the left of the band, and '
         'the Parker Solar Probe lower bound at nineteen point eight '
         'solar radii, at its right-hand edge." >' % (W, H)]

    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for rv in (5, 10, 20, 50, 100, 200):
        x = px(rv)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{rv}</text>')
    for vv in (20, 50, 100, 200, 500):
        y = py(vv)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-8:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{vv}</text>')

    # the model band of crossing radii
    s.append(f'<rect x="{px(lo):.1f}" y="{Y0:.0f}" '
             f'width="{px(hi)-px(lo):.1f}" height="{Y1-Y0:.0f}" '
             f'fill="{ACC}" opacity="0.18"/>')

    # curves: v(r) constant, and v_A(r) ~ 1/r, on the MEAN fits with
    # protons only -- the row PART L's D2 works by hand.
    om = 2.0*np.pi/(M.CARRINGTON_SIDEREAL_DAYS*M.day)
    r0 = M.R_SOURCE_SURFACE*M.Rsun
    v1 = M.VB18_MEAN['velocity'][0]*1e5
    n1 = M.VB18_MEAN['density'][0]
    x1 = M.parker_ratio(M.AU, v1, om, r0)
    B1 = M.VB18_MEAN['field'][0]*1e-5/np.sqrt(1.0 + x1*x1)
    vA1 = M.alfven_speed(B1, n1*M.mp)
    rr = np.logspace(gx0, gx1, 400)*M.Rsun
    d_wind = path([px(r/M.Rsun) for r in rr], [py(v1/1e5)]*len(rr))
    s.append(f'<path d="{d_wind}" fill="none" stroke="{ACC2}" '
             f'stroke-width="2"/>')
    vA_of_r = vA1*(M.AU/rr)
    # CLIP TO THE PLOT BOX.  The first draft drew the whole range and the
    # Alfven speed ran off the top of the frame at 5 R_sun, where it is
    # 1478 km/s against a y-axis that stops at 900.  check_frame measures
    # TEXT extents and check_overlap measures labels, so neither saw it;
    # a rendered look did.
    keep = [(px(r/M.Rsun), py(v/1e5))
            for r, v in zip(rr, vA_of_r) if 10.0**gy0 <= v/1e5 <= 10.0**gy1]
    d_alf = path([q[0] for q in keep], [q[1] for q in keep])
    s.append(f'<path d="{d_alf}" fill="none" stroke="{ACC}" '
             f'stroke-width="2"/>')
    # and MARK the crossing, which is what the whole figure is about
    r_cross = M.AU*vA1/v1
    s.append(f'<circle cx="{px(r_cross/M.Rsun):.1f}" '
             f'cy="{py(v1/1e5):.1f}" r="5" fill="none" stroke="{FG}" '
             f'stroke-width="1.6"/>')

    # the two published values
    for val, err, col, lab, dy in (
            (M.VBV21_RA_FLS1, M.VBV21_RA_FLS1_ERR, VIO,
             'Verscharen FLS1', 0.0),
            (M.KASPER21_RA_OUTERMOST, None, YEL,
             'PSP I1, a LOWER bound', 18.0)):
        x = px(val)
        s.append(f'<line x1="{x:.1f}" y1="{Y0:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1:.0f}" stroke="{col}" stroke-width="1.4" '
                 f'stroke-dasharray="5 4"/>')
        if err:
            s.append(f'<rect x="{px(val-err):.1f}" y="{Y0:.0f}" '
                     f'width="{px(val+err)-px(val-err):.1f}" '
                     f'height="{Y1-Y0:.0f}" fill="{col}" opacity="0.22"/>')
        # The label goes BELOW the axis, in the legend row.  Inside
        # the box it would cross the other measurement's dashed line --
        # check_overlap found exactly that, twice.
        rel = '&#8805; ' if lab.startswith('PSP') else ''
        s.append(f'<text x="{X0:.0f}" y="{Y1+62+dy:.0f}" font-size="10.5" '
                 f'fill="{col}">{lab} {rel}{val:g} '
                 f'R{SUB.format("&#9737;")}</text>')
        # The bound's direction is written as a relation, not drawn as
        # a free-floating arrow that a reader must interpret.

    s.append(f'<rect x="{X0:.0f}" y="{Y1+92:.0f}" width="12" '
             f'height="10" fill="{ACC}" opacity="0.30"/>')
    s.append(f'<text x="{X0+18:.0f}" y="{Y1+101:.0f}" font-size="10.5" '
             f'fill="{ACC}">eight model variants, '
             f'{lo:.2f}&#8211;{hi:.2f} R{SUB.format("&#9737;")}</text>')
    s.append(f'<text x="{px(120):.0f}" y="{py(v1/1e5)-9:.0f}" '
             f'font-size="10.5" fill="{ACC2}">wind speed '
             f'{v1/1e5:.1f} km s{SUP.format(-1)}</text>')
    # BELOW the curve and to the left, in the empty wedge.  Beside the
    # curve at 120 R_sun the label sat ON it; a rendered look found that.
    s.append(f'<text x="{px(26):.0f}" y="{Y1-22:.0f}" '
             f'font-size="10.5" fill="{ACC}">radial Alfv&#233;n speed, '
             f'&#8733; 1/r</text>')

    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+40:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">heliocentric distance '
             f'/ R{SUB.format("&#9737;")}</text>')
    s.append(f'<text x="{X0-52:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-52:.0f} {(Y0+Y1)/2:.0f})">'
             f'speed / km s{SUP.format(-1)}</text>')
    s.append(f'<text x="{X0+250:.0f}" y="{Y1+62:.0f}" font-size="10.5" '
             f'fill="{MUT}">the two differ by '
             f'{M.KASPER21_RA_OUTERMOST/M.VBV21_RA_FLS1:.2f}, and are not '
             f'the same quantity</text>')
    s.append(f'<text x="{X0+250:.0f}" y="{Y1+80:.0f}" font-size="10.5" '
             f'fill="{MUT}">every variant exceeds the first by '
             f'{lo/M.VBV21_RA_FLS1:.3f}&#8211;{hi/M.VBV21_RA_FLS1:.3f}'
             f'</text>')
    s.append(f'<text x="{X0+250:.0f}" y="{Y1+98:.0f}" font-size="10.5" '
             f'fill="{MUT}">and falls short of the second by '
             f'{M.KASPER21_RA_OUTERMOST/hi:.3f}&#8211;'
             f'{M.KASPER21_RA_OUTERMOST/lo:.3f}</text>')
    s.append('</svg>')
    open(out("m12_fig_alfven.svg"), "w", encoding="utf-8").write("\n".join(s))
    return lo, hi


# =========================================================================
# Figure 4.  The transport ladder, over thirty decades.
#
# THE JOB: show the 22.8-to-24.8 decade gap AS A GAP.  Zhuravleva's bound
# is ONE-SIDED, so its band is drawn OPEN at the bottom.
# =========================================================================

def build_transport():
    W, H = 720, 366
    X0, X1, Y0, Y1 = 96.0, 620.0, 60.0, 190.0
    GLO, GHI = -30.0, 1.0

    def px(g):
        return X0 + (g - GLO)/(GHI - GLO)*(X1 - X0)

    lnL = M.lnLambda_e(M.n_icm, M.T_icm)
    wt_i = M.gyrofrequency(M.B_icm)*M.tau_ion(M.n_icm, M.T_icm, lnL)
    wt_e = M.gyrofrequency(M.B_icm, m=M.me)*M.tau_electron(
        M.n_icm, M.T_icm, lnL)
    nu_sup = M.viscosity_suppression(wt_i)
    kap_sup = M.conduction_suppression(wt_e)
    z_lo = 1.0/M.ZHURAVLEVA_SUPPRESSION_HI
    z_hi = 1.0/M.ZHURAVLEVA_SUPPRESSION_LO

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="One horizontal logarithmic axis running '
         'from ten to the minus thirty up to one, the ratio of '
         'perpendicular to parallel transport. Unsuppressed transport sits '
         'at one on the right. A shaded band open at its left-hand end '
         'marks the measured suppression of the Coma cluster viscosity, '
         'between ten to the minus three and ten to the minus one. Far to '
         'the left, two narrow marks give Braginskii classical '
         'perpendicular viscosity and conduction near ten to the minus '
         'twenty-six and ten to the minus twenty-nine. A labelled arrow '
         'spans the gap of about twenty-three decades between the '
         'measured band and the classical marks." >' % (W, H)]

    s.append(f'<line x1="{X0:.0f}" y1="{Y1:.0f}" x2="{X1:.0f}" '
             f'y2="{Y1:.0f}" stroke="{RULE}" stroke-width="1.4"/>')
    for g in range(-30, 2, 5):
        x = px(g)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+6:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Y1+20:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">10{SUP.format(g)}'
                 f'</text>')

    # Zhuravleva's band, OPEN at its lower end
    s.append(f'<rect x="{px(np.log10(z_lo)):.1f}" y="{Y0:.0f}" '
             f'width="{px(np.log10(z_hi))-px(np.log10(z_lo)):.1f}" '
             f'height="{Y1-Y0:.0f}" fill="{ACC2}" opacity="0.22"/>')
    s.append(f'<line x1="{px(np.log10(z_hi)):.1f}" y1="{Y0:.0f}" '
             f'x2="{px(np.log10(z_hi)):.1f}" y2="{Y1:.0f}" '
             f'stroke="{ACC2}" stroke-width="1.6"/>')
    s.append(f'<path d="M {px(np.log10(z_lo)):.1f},{Y0+14:.0f} l -26,0 '
             f'l 6,-5 m -6,5 l 6,5" fill="none" stroke="{ACC2}" '
             f'stroke-width="1.3"/>')
    s.append(f'<rect x="{X0:.0f}" y="{Y1+56:.0f}" width="12" '
             f'height="10" fill="{ACC2}" opacity="0.30"/>')
    s.append(f'<text x="{X0+18:.0f}" y="{Y1+65:.0f}" '
             f'font-size="10.5" fill="{ACC2}">Zhuravleva et al. (2019): '
             f'suppressed by {M.ZHURAVLEVA_SUPPRESSION_LO:.0f}&#8211;'
             f'{M.ZHURAVLEVA_SUPPRESSION_HI:.0f}, a ONE-SIDED bound'
             f'</text>')

    # the unsuppressed value
    s.append(f'<line x1="{px(0.0):.1f}" y1="{Y0:.0f}" x2="{px(0.0):.1f}" '
             f'y2="{Y1:.0f}" stroke="{FG}" stroke-width="1.4" '
             f'stroke-dasharray="5 4"/>')
    s.append(f'<text x="{px(0.0):.1f}" y="{Y0-8:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{FG}">unsuppressed</text>')

    # the two classical values
    for val, col, lab, dy in ((nu_sup, ACC, '&#957;&#8869;/&#957;&#8741;',
                               0.0),
                              (kap_sup, VIO,
                               '&#954;&#8869;/&#954;&#8741;', 20.0)):
        x = px(np.log10(val))
        s.append(f'<line x1="{x:.1f}" y1="{Y0:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1:.0f}" stroke="{col}" stroke-width="2"/>')
        # BELOW the axis title, in the legend rows.  At Y1+9 the two
        # labels landed on the "10^-10" and "10^-5" tick labels; a
        # rendered look found it, check_overlap does not test text on
        # text.
        s.append(f'<rect x="{X0:.0f}" y="{Y1+84+dy:.0f}" width="12" '
                 f'height="3" fill="{col}"/>')
        s.append(f'<text x="{X0+18:.0f}" y="{Y1+89+dy:.0f}" '
                 f'font-size="10.5" fill="{col}">Braginskii {lab} = '
                 f'{val:.2e}</text>')

    # the gap, drawn as an arrow between the nu mark and the band
    gy = Y1 - 18.0
    xa, xb = px(np.log10(nu_sup)), px(np.log10(z_lo))
    s.append(f'<line x1="{xa:.1f}" y1="{gy:.0f}" x2="{xb:.1f}" '
             f'y2="{gy:.0f}" stroke="{YEL}" stroke-width="1.3"/>')
    for xx, dirn in ((xa, +1), (xb, -1)):
        s.append(f'<path d="M {xx:.1f},{gy:.0f} l {6*dirn},-4 m {-6*dirn},4 '
                 f'l {6*dirn},4" fill="none" stroke="{YEL}" '
                 f'stroke-width="1.3"/>')
    d_lo = np.log10(1.0/nu_sup/M.ZHURAVLEVA_SUPPRESSION_HI)
    d_hi = np.log10(1.0/nu_sup/M.ZHURAVLEVA_SUPPRESSION_LO)
    s.append(f'<text x="{(xa+xb)/2:.1f}" y="{gy-8:.0f}" font-size="11" '
             f'text-anchor="middle" fill="{YEL}">{d_lo:.1f} to {d_hi:.1f} '
             f'decades</text>')

    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+44:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">ratio of perpendicular to '
             f'parallel transport</text>')
    s.append(f'<text x="{20:.0f}" y="{Y1+132:.0f}" font-size="11" '
             f'fill="{MUT}">The measurement lies far nearer the '
             f'UNSUPPRESSED value than the classical one,</text>')
    s.append(f'<text x="{20:.0f}" y="{Y1+150:.0f}" font-size="11" '
             f'fill="{MUT}">so the step is not the gyroradius. What it '
             f'IS, this book does not compute.</text>')
    s.append('</svg>')
    open(out("m12_fig_transport.svg"), "w",
         encoding="utf-8").write("\n".join(s))
    return nu_sup, kap_sup


# =========================================================================
# Figure 5.  The magnetorotational growth rate.
#
# THE JOB: show that the instability has a BAND of unstable wavenumbers
# with a hard upper edge, and that the field kills it from above -- which
# is the whole content of the lambda(marginal) < H condition.
# =========================================================================

def mri_sigma(x, q=M.KEPLER_Q):
    """gamma/Omega against k v_A/Omega, from the local dispersion relation.

    With kappa^2 = 2(2 - q) Omega^2 the axisymmetric vertical-field
    dispersion relation is

        sigma^4 + sigma^2 (kappa^2/Omega^2 + 2 x^2)
                 + x^2 (x^2 - 4 + kappa^2/Omega^2) = 0,

    whose growing root is the positive square root of the larger
    solution for sigma^2.  At q = 3/2 this gives sigma = 3/4 at
    x = sqrt(15)/4 and sigma = 0 at x = sqrt(3), both of which the
    caller checks.
    """
    k2 = 2.0*(2.0 - q)
    b = k2 + 2.0*x*x
    cc = x*x*(x*x - 4.0 + k2)
    disc = b*b - 4.0*cc
    s2 = 0.5*(-b + np.sqrt(np.maximum(disc, 0.0)))
    return np.sqrt(np.maximum(s2, 0.0))


def build_mri():
    W, H = 720, 430
    X0, X1, Y0, Y1 = 92.0, 596.0, 46.0, 296.0
    XMAX, YMAX = 2.1, 0.90

    def px(v):
        return X0 + v/XMAX*(X1 - X0)

    def py(v):
        return Y1 - v/YMAX*(Y1 - Y0)

    xs = np.linspace(0.0, XMAX, 400)
    sig = mri_sigma(xs)

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Magnetorotational growth rate divided by '
         'the orbital angular velocity, plotted against the wavenumber '
         'times the Alfven speed divided by the same angular velocity. '
         'The curve rises from zero, peaks at three quarters, and falls '
         'to zero at the square root of three, beyond which there is no '
         'growth. Two vertical dotted lines mark, for two worked discs, '
         'the wavenumber whose wavelength equals one scale height; both '
         'lie inside the unstable band." >' % (W, H)]

    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for v in np.arange(0.0, XMAX + 0.01, 0.5):
        x = px(v)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{v:.1f}</text>')
    for v in np.arange(0.0, YMAX + 0.01, 0.25):
        y = py(v)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-8:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.2f}</text>')

    # the unstable band
    xc = np.sqrt(3.0)
    s.append(f'<rect x="{px(0.0):.1f}" y="{Y0:.0f}" '
             f'width="{px(xc)-px(0.0):.1f}" height="{Y1-Y0:.0f}" '
             f'fill="{ACC}" opacity="0.10"/>')

    s.append(f'<path d="{path([px(v) for v in xs], [py(v) for v in sig])}" '
             f'fill="none" stroke="{ACC}" stroke-width="2.2"/>')

    xm, sm = np.sqrt(15.0)/4.0, 0.75
    s.append(f'<line x1="{px(xm):.1f}" y1="{py(sm):.1f}" '
             f'x2="{px(xm):.1f}" y2="{Y1:.0f}" stroke="{ACC}" '
             f'stroke-width="1" stroke-dasharray="3 4"/>')
    s.append(f'<circle cx="{px(xm):.1f}" cy="{py(sm):.1f}" r="4.2" '
             f'fill="{ACC}"/>')
    s.append(f'<text x="{px(xm)+8:.1f}" y="{py(sm)-6:.1f}" font-size="11" '
             f'fill="{ACC}">&#8730;15/4 = {xm:.5f}, &#947; = '
             f'{sm:.2f}&#937;</text>')
    s.append(f'<line x1="{px(xc):.1f}" y1="{Y0:.0f}" x2="{px(xc):.1f}" '
             f'y2="{Y1:.0f}" stroke="{RED}" stroke-width="1.5" '
             f'stroke-dasharray="5 4"/>')
    s.append(f'<text x="{px(xc)+8:.1f}" y="{Y0+16:.0f}" font-size="11" '
             f'fill="{RED}">marginal, &#8730;3 = {xc:.5f}</text>')
    s.append(f'<text x="{px(xc)+8:.1f}" y="{Y0+32:.0f}" font-size="10.5" '
             f'fill="{MUT}">no growth beyond here</text>')

    # the two worked discs: the wavenumber whose wavelength is H
    for (R_au, B, n, T), col, dy in ((((1.0, 1.0, 1.0e14, 300.0)), ACC2, 0.0),
                                     (((10.0, 1.0e-2, 1.0e12, 50.0)), VIO,
                                      18.0)):
        om = M.kepler_omega(M.Msun, R_au*M.AU)
        vA = M.alfven_speed(B, n*2.33*M.mu_u)
        cs = M.sound_speed(T, 2.33)
        xH = 2.0*np.pi*vA/cs        # k v_A/Omega at lambda = H
        s.append(f'<line x1="{px(xH):.1f}" y1="{Y0:.0f}" '
                 f'x2="{px(xH):.1f}" y2="{Y1:.0f}" stroke="{col}" '
                 f'stroke-width="1.2" stroke-dasharray="2 4"/>')
        s.append(f'<line x1="{X0:.0f}" y1="{Y1+58+dy:.0f}" '
                 f'x2="{X0+14:.0f}" y2="{Y1+58+dy:.0f}" stroke="{col}" '
                 f'stroke-width="1.2" stroke-dasharray="2 4"/>')
        s.append(f'<text x="{X0+20:.0f}" y="{Y1+62+dy:.0f}" '
                 f'font-size="10.5" fill="{col}">&#955; = H at '
                 f'{R_au:g} au, where &#946; = '
                 f'{M.plasma_beta(n, T, B):.3g}</text>')

    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+40:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">'
             f'<tspan font-style="italic">k</tspan>'
             f'<tspan font-style="italic">v</tspan>{SUB.format("A")}/'
             f'&#937;</text>')
    s.append(f'<text x="{X0-46:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-46:.0f} {(Y0+Y1)/2:.0f})">'
             f'&#947;/&#937;</text>')
    s.append(f'<text x="{20:.0f}" y="{Y1+98:.0f}" font-size="11" '
             f'fill="{MUT}">The peak height is q/2 and the marginal '
             f'wavenumber is &#8730;3 for EVERY Keplerian disc.</text>')
    s.append(f'<text x="{20:.0f}" y="{Y1+116:.0f}" font-size="11" '
             f'fill="{MUT}">A disc is stabilised when its dashed line '
             f'passes to the RIGHT of &#8730;3.</text>')
    s.append('</svg>')
    open(out("m12_fig_mri.svg"), "w", encoding="utf-8").write("\n".join(s))
    return xm, xc


def main():
    rows = build_census()
    fit = build_spiral()
    lo, hi = build_alfven()
    nu_sup, kap_sup = build_transport()
    xm, xc = build_mri()

    # --- self-checks.  A figure builder that cannot fail is not a check.
    beta_cor = [r[3] for r in rows if r[0] == 'solar corona'][0]
    beta_mc = [r[3] for r in rows if r[0] == 'molecular cloud'][0]
    assert abs(beta_cor/beta_mc - 1.0) < 1e-12, (beta_cor, beta_mc)
    assert abs(mri_sigma(np.array([xm]))[0] - 0.75) < 1e-9
    assert mri_sigma(np.array([xc + 1e-6]))[0] == 0.0
    assert 15.0 < lo < hi < 20.0, (lo, hi)
    assert -1.80 < fit < -1.70, fit
    assert nu_sup > kap_sup > 0.0

    print('m12_build_figs: 5 SVGs written')
    print(f'  census      corona and cloud share beta = {beta_cor:.4f}')
    print(f'  spiral      fitted Parker index {fit:.4f}')
    print(f'  alfven      band {lo:.2f} to {hi:.2f} R_sun')
    print(f'  transport   nu_perp/nu_par {nu_sup:.3e}, '
          f'kappa {kap_sup:.3e}')
    print(f'  mri         peak at {xm:.5f}, marginal at {xc:.5f}')


if __name__ == '__main__':
    main()
