"""Build the computed SVG figures for Module 9.

Writes three files:

  m09_fig_topology.svg  The (r/r_c, v/c_T) plane of the isothermal steady
                        spherical flow.  Every curve is a level set of
                        u^2 - 2 ln u - 4 ln x - 4/x = C.  The two transonic
                        solutions (C = -3) cross at the critical point; the
                        breezes sit below them, the supersonic-everywhere
                        solutions above, and the double-valued families
                        (C < -3) stop at a forbidden band around x = 1.
                        The whole classification is drawn, not asserted.

  m09_fig_parker.svg    THE ANCHOR FIGURE.  Upper panel: the isothermal
                        wind speed against radius for three coronal
                        temperatures, with the Helios range shaded and the
                        Venzmer & Bothmer (2018) mean fit drawn over it.
                        Lower panel: the RESIDUAL that the upper panel
                        cannot show -- the logarithmic slope dln v/dln r
                        over 0.29-0.98 au, predicted five ways, against the
                        measured value drawn as a sixth bar and as a band.
                        This is the Module 2
                        lesson applied: plot the residual, not the
                        quantity, when the disagreement is what matters.

  m09_fig_sgra.svg      The Sgr A* accretion-rate ladder on a log axis:
                        the Bondi rate computed here, Baganoff et al.'s own
                        value at their own black-hole mass, and Marrone et
                        al.'s Faraday-rotation upper and lower limits.  The
                        gap is annotated with the measured factor.

Geometry is computed, never eyeballed.  Every number drawn is produced by
m09_numbers.py, so a figure cannot drift away from the prose.

Lessons from Modules 1-3 that are applied here:

  * check_overlap reads geometry, not pixels, so the contours in the
    topology panel are CLIPPED BY TRUNCATING THEIR POINT LISTS, never by
    an SVG clip-path, and label clearance is tested against the full
    sample list before anything is decimated for drawing.
  * Label positions are searched over a candidate grid and confined to the
    plot box; a leader line is drawn wherever the search moves a label
    away from its curve.
  * Contour spacing sets label feasibility, so the topology panel carries
    five labelled families and no more.
  * Where agreement (or its absence) is the point, the panel plots the
    residual.  m09_fig_parker's lower panel exists because on a v(r) axis
    running from 0 to 900 km/s a slope of 0.049 against 0.19 is a
    difference of a few pixels.
"""
import numpy as np

import m09_numbers as M

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"
RED = "#f87171"


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def leader_svg(ax_, ay_, tx, ty, w, h, gap=3.0):
    """A dotted leader from a curve point to a label, stopping SHORT of it.

    The label box is (tx, ty-h) to (tx+w, ty).  The leader ends at the
    point of that box, inflated by `gap`, nearest to the anchor.  Ending it
    inside the box -- the first version did -- draws a dashed line through
    the text, and check_overlap rightly reports every such label.  Returns
    '' when the anchor already sits inside the inflated box.
    """
    x0, y0, x1, y1 = tx - gap, ty - h - gap, tx + w + gap, ty + gap
    ex, ey = min(max(ax_, x0), x1), min(max(ay_, y0), y1)
    if (ex, ey) == (ax_, ay_):
        return ''
    return (f'<line x1="{ax_:.1f}" y1="{ay_:.1f}" x2="{ex:.1f}" '
            f'y2="{ey:.1f}" stroke="{MUT}" stroke-width="0.9" '
            f'stroke-dasharray="2 3"/>')


def place_label(cands, occupied, box, w, h, ink=None, pad=4.0):
    """Choose a position for a label by search, never by eye.

    cands    list of (x, y) text anchors in preference order.  The search
             does not stop there: it falls back to a lattice over the whole
             plot box, ordered by distance from the first candidate.
    occupied list of (x0, y0, x1, y1) rectangles already taken
    box      (X0, Y0, X1, Y1) the plot box the label must stay inside
    w, h     the label's width and height in user units
    ink      an (N, 2) array of every drawn curve point, at FULL sampling
             density.  Testing against a decimated list leaves gaps the
             clearance test walks straight through -- the Module 1 lesson.
    pad      clearance demanded around the label box, in user units

    Three passes, each weaker than the last, so that the label always ends
    up INSIDE the box.  Pass 1 demands clearance from other labels and from
    every drawn curve; pass 2 drops the curve test; pass 3 only keeps the
    label in the box.  Returns (x, y, moved), with moved true whenever the
    first candidate was not the one taken, which is the caller's cue to
    draw a leader line.
    """
    X0, Y0, X1, Y1 = box
    ordered = list(cands)
    # A lattice over the box, ordered by distance from the preferred spot.
    px0, py0 = cands[0]
    lat = [(x, y)
           for x in np.arange(X0 + 4, X1 - w - 2, 26.0)
           for y in np.arange(Y0 + h + 4, Y1 - 4, 18.0)]
    lat.sort(key=lambda p: (p[0] - px0)**2 + (p[1] - py0)**2)
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
# Figure 1: the isothermal solution topology
# =========================================================================

def build_topology():
    W, H = 760, 486
    X0, X1, Y0, Y1 = 78.0, 700.0, 46.0, 372.0
    XMIN, XMAX = 0.12, 6.0          # r/r_c
    UMIN, UMAX = 0.0, 3.4           # v/c_T

    def px(x):
        return X0 + (np.log(x) - np.log(XMIN))/(np.log(XMAX) - np.log(XMIN)) \
            * (X1 - X0)

    def py(u):
        return Y1 - (u - UMIN)/(UMAX - UMIN)*(Y1 - Y0)

    def branch(C, which, xs):
        """u(x) on one branch of the level set, with nan where none exists."""
        out = np.full(len(xs), np.nan)
        for i, x in enumerate(xs):
            out[i] = M.solve_h(4.0*np.log(x) + 4.0/x + C, which)
        return out

    xs = np.exp(np.linspace(np.log(XMIN), np.log(XMAX), 720))
    ink = []          # every drawn point, at full density, for clearance

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="The plane of radius divided by the sonic '
         f'radius against flow speed divided by the sound speed, for steady '
         f'spherical isothermal flow. Two curves cross at the critical '
         f'point at coordinates one, one: the accelerating wind and the '
         f'accretion solution. Below them lie the breeze solutions, which '
         f'stay subsonic and decay; above them the solutions that are '
         f'supersonic everywhere; and to the sides two double-valued '
         f'families that turn back before reaching the sonic radius and so '
         f'cannot connect the base to infinity.">']

    # frame
    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for xt, lab in ((0.125, "1/8"), (0.25, "1/4"), (0.5, "1/2"), (1.0, "1"),
                    (2.0, "2"), (4.0, "4")):
        x = px(xt)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{lab}</text>')
    for ut in (0, 1, 2, 3):
        y = py(ut)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{ut}</text>')
    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">r / r_c</text>')
    s.append(f'<text x="{X0-42:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-42:.0f} {(Y0+Y1)/2:.0f})">'
             f'v / c_T</text>')

    # the sonic line u = 1 and the sonic radius x = 1, drawn first so the
    # solution curves sit on top of them
    s.append(f'<line x1="{X0:.0f}" y1="{py(1.0):.1f}" x2="{X1:.0f}" '
             f'y2="{py(1.0):.1f}" stroke="{RULE}" stroke-width="1" '
             f'stroke-dasharray="3 4"/>')
    s.append(f'<line x1="{px(1.0):.1f}" y1="{Y0:.0f}" x2="{px(1.0):.1f}" '
             f'y2="{Y1:.0f}" stroke="{RULE}" stroke-width="1" '
             f'stroke-dasharray="3 4"/>')

    # The "sonic radius" annotation is written last but reserved first, so
    # the label search below treats it as taken rather than drawing over it.
    SONIC_X, SONIC_Y, SONIC_W = px(1.0) + 8, Y0 + 16.0, 152.0
    occupied = [(SONIC_X, SONIC_Y - 13, SONIC_X + SONIC_W, SONIC_Y)]
    box = (X0 + 2, Y0 + 2, X1 - 2, Y1 - 2)
    leaders = []

    def draw(C, which, colour, width, dash=None, xlo=XMIN, xhi=XMAX):
        """Draw one branch, truncating the POINT LIST to the plot box.

        Nothing is hidden with a clip-path: check_overlap reads coordinates,
        so a clipped polyline would still occupy the space it was clipped
        out of.  Points outside the box, and points where no root exists,
        are dropped before the path is written, and the path is broken into
        separate <path> elements wherever a gap appears.
        """
        m = (xs >= xlo) & (xs <= xhi)
        xv, uv = xs[m], branch(C, which, xs[m])
        keep = np.isfinite(uv) & (uv >= UMIN) & (uv <= UMAX)
        segs, cur = [], []
        for i in range(len(xv)):
            if keep[i]:
                cur.append((px(xv[i]), py(uv[i])))
            elif cur:
                segs.append(cur)
                cur = []
        if cur:
            segs.append(cur)
        d = '' if dash is None else f' stroke-dasharray="{dash}"'
        for seg in segs:
            if len(seg) < 2:
                continue
            # The FULL point list goes into the clearance set; only what is
            # DRAWN is decimated, and the endpoints are always kept so the
            # decimated path still reaches the edge of the box.
            ink.extend(seg)
            thin = seg[::3]
            if thin[-1] != seg[-1]:
                thin.append(seg[-1])
            dd = path([p[0] for p in thin], [p[1] for p in thin])
            s.append(f'<path d="{dd}" fill="none" stroke="{colour}" '
                     f'stroke-width="{width}"{d}/>')
        return xv, uv, keep

    # --- the two transonic solutions, C = -3 -----------------------------
    # The wind: subsonic branch inside x = 1, supersonic branch outside.
    draw(-3.0, 'sub', ACC, 2.8, xhi=1.0)
    draw(-3.0, 'sup', ACC, 2.8, xlo=1.0)
    # The accretion solution: the mirror image through u = 1.
    draw(-3.0, 'sup', ACC2, 2.8, xhi=1.0)
    draw(-3.0, 'sub', ACC2, 2.8, xlo=1.0)

    # --- breezes and supersonic-everywhere solutions, C > -3 -------------
    for C in (-2.2, -1.2, 0.2):
        draw(C, 'sub', VIO, 1.5, dash="5 4")
        draw(C, 'sup', YEL, 1.5, dash="5 4")

    # --- the double-valued families, C < -3 ------------------------------
    # R(x) = 4 ln x + 4/x + C dips below 1 in a band about x = 1, so no
    # solution exists there at all; the curve turns back on itself at the
    # edges of that band.  Drawing both branches of the same C shows the
    # turning point without any annotation.
    for C in (-4.2,):
        draw(C, 'sub', RED, 1.5, dash="2 3")
        draw(C, 'sup', RED, 1.5, dash="2 3")

    # --- the critical point ----------------------------------------------
    s.append(f'<circle cx="{px(1.0):.1f}" cy="{py(1.0):.1f}" r="5" '
             f'fill="{BG}" stroke="{FG}" stroke-width="2"/>')

    # --- labels, placed by search ----------------------------------------
    # The search runs over a grid of candidates and rejects any that lands
    # on a drawn curve.  Nothing here is positioned by eye; where the search
    # has to move a label off its own curve, a leader line is drawn.
    ink = np.array(ink) if ink else np.zeros((0, 2))

    def grid(x_pref, y_pref, wide):
        """Candidates: the preferred spot first, then a ring around it."""
        out = [(x_pref, y_pref)]
        for dyy in (0, -18, 18, -34, 34, -52, 52):
            for dxx in (0, -wide - 16, 22, -wide - 40, 46, -wide - 70, 78):
                if dxx == 0 and dyy == 0:
                    continue
                out.append((x_pref + dxx, y_pref + dyy))
        return out

    def label(text, colour, anchor_x, anchor_y, x_pref, y_pref, wide):
        x, y, fell = place_label(grid(x_pref, y_pref, wide), occupied, box,
                                 wide, 13.0, ink=ink)
        s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="11" '
                 f'fill="{colour}">{esc(text)}</text>')
        if fell or abs(x - anchor_x) > 34 or abs(y - anchor_y) > 26:
            leaders.append((anchor_x, anchor_y, x, y, wide))

    # wind: anchor on the supersonic branch at x = 3
    ax_, ay_ = px(3.0), py(M.parker_u(3.0, 'sup'))
    label("transonic WIND", ACC, ax_, ay_, ax_ - 130, ay_ - 10, 122)
    # accretion: anchor on the supersonic branch inside x = 1
    ax_, ay_ = px(0.35), py(M.parker_u(0.35, 'sup'))
    label("transonic ACCRETION", ACC2, ax_, ay_, ax_ + 12, ay_ - 6, 148)
    # breeze: anchor on the topmost breeze curve at its peak
    ax_, ay_ = px(1.0), py(M.solve_h(4.0 - 1.2, 'sub'))
    label("breeze, v ~ r⁻²", VIO, ax_, ay_,
          px(1.3), py(0.72), 118)
    # supersonic everywhere
    ax_, ay_ = px(0.6), py(M.solve_h(4*np.log(0.6) + 4/0.6 - 1.2, 'sup'))
    label("supersonic everywhere", YEL, ax_, ay_, ax_ + 12, ay_ - 8, 156)
    # double-valued
    ax_, ay_ = px(0.28), py(M.solve_h(4*np.log(0.28) + 4/0.28 - 4.2, 'sub'))
    label("double-valued", RED, ax_, ay_, ax_ + 10, ay_ + 20, 126)

    for lx, ly, tx, ty, tw in leaders:
        s.append(leader_svg(lx, ly, tx, ty, tw, 13.0))

    s.append(f'<text x="{SONIC_X:.1f}" y="{SONIC_Y:.0f}" font-size="10.5" '
             f'fill="{MUT}">sonic radius r_c = GM/(2a²)</text>')

    # --- caption ---------------------------------------------------------
    cap = [
        "Level sets of u² − 2 ln u − 4 ln x − 4/x = C, with u = v/c_T and "
        "x = r/r_c. Both sides of the equation have a single minimum, at",
        "u = 1 and at x = 1, so a curve reaches u = 1 only when C = −3, and "
        "then only at x = 1. C = −3 therefore gives exactly two",
        "solutions that connect a subsonic base to a supersonic infinity "
        "(II) or the reverse (I); C > −3 gives curves that never cross the",
        "sonic line; C < −3 gives curves that stop before reaching it. Only "
        "II leaves the Sun with v > 0 at infinity.",
    ]
    for i, line in enumerate(cap):
        s.append(f'<text x="{X0-48:.0f}" y="{Y1+56+i*15:.0f}" '
                 f'font-size="10.5" fill="{MUT}">{esc(line)}</text>')
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure 2: the Parker wind against Helios -- THE ANCHOR
# =========================================================================

def build_parker():
    W, H = 760, 672
    # Panel A: v(r).  Panel B: the slope residual.  The 96 px between
    # AY1 and BY0 has to carry panel A's tick labels and axis title AND
    # panel B's two-line heading; at 60 px they collided.
    AX0, AX1, AY0, AY1 = 78.0, 700.0, 44.0, 296.0
    BX0, BX1, BY0, BY1 = 232.0, 700.0, 392.0, 554.0

    RMIN, RMAX = 1.03*M.Rsun/M.AU, 1.6        # au
    VMAX = 950.0                              # km/s

    def ax(r):
        return AX0 + (np.log(r) - np.log(RMIN))/(np.log(RMAX) - np.log(RMIN)) \
            * (AX1 - AX0)

    def ay(v):
        return AY1 - v/VMAX*(AY1 - AY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper panel: the speed of the isothermal '
         f'Parker wind against heliocentric distance on a logarithmic axis, '
         f'for coronal temperatures of one, one and a half, and two million '
         f'kelvin, with the sonic point marked on each and the Helios '
         f'measurement range from 0.29 to 0.98 astronomical units shaded. '
         f'Lower panel: the logarithmic slope of velocity against radius '
         f'over that same range, predicted five different ways, each with '
         f'its own bar, against the measured value of '
         f'{M.vb("velocity", "avg")[2]:.3f} plus or minus '
         f'{M.vb("velocity", "avg")[3]:.3f}, which is drawn both as a sixth '
         f'bar and as a vertical band. Every prediction misses the '
         f'band, the isothermal ones from above and the momentum-equation '
         f'one from below.">']

    # ---------------- panel A ----------------
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-22:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The isothermal Parker wind, '
             f'and what Helios measured</text>')

    # the Helios band, drawn before the frame so the frame sits on top
    hx0, hx1 = ax(M.HELIOS_RMIN), ax(M.HELIOS_RMAX)
    s.append(f'<rect x="{hx0:.1f}" y="{AY0:.0f}" width="{hx1-hx0:.1f}" '
             f'height="{AY1-AY0:.0f}" fill="{ACC}" fill-opacity="0.09"/>')

    s.append(f'<rect x="{AX0:.0f}" y="{AY0:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for rt, lab in ((0.005, "0.005"), (0.01, "0.01"), (0.03, "0.03"),
                    (0.1, "0.1"), (0.29, "0.29"), (0.98, "0.98")):
        x = ax(rt)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{lab}</text>')
    for vt in (0, 200, 400, 600, 800):
        y = ay(vt)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{y:.1f}" x2="{AX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{AX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{vt}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">r / au</text>')
    s.append(f'<text x="{AX0-46:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {AX0-46:.0f} {(AY0+AY1)/2:.0f})">'
             f'v / km s⁻¹</text>')
    s.append(f'<text x="{(hx0+hx1)/2:.1f}" y="{AY0+15:.0f}" font-size="10.5" '
             f'text-anchor="middle" fill="{ACC}">Helios 1+2, 0.29–0.98 au'
             f'</text>')

    rgrid = np.exp(np.linspace(np.log(RMIN), np.log(RMAX), 260))*M.AU
    occupied, leaders = [], []
    boxA = (AX0 + 2, AY0 + 2, AX1 - 2, AY1 - 2)
    for T0, col in ((1.0e6, ACC2), (1.5e6, YEL), (2.0e6, VIO)):
        v, a, rc = M.parker_wind(rgrid, T0)
        s.append(f'<path d="{path(ax(rgrid/M.AU), ay(v/1e5))}" fill="none" '
                 f'stroke="{col}" stroke-width="2.2"/>')
        # the sonic point
        s.append(f'<circle cx="{ax(rc/M.AU):.1f}" cy="{ay(a/1e5):.1f}" r="4" '
                 f'fill="{BG}" stroke="{col}" stroke-width="2"/>')
        # label at the right-hand end of the curve, searched into the box
        lx, ly = ax(RMAX) - 8, ay(v[-1]/1e5)
        txt = f'T₀ = {T0/1e6:.1f} MK'
        x, y, fell = place_label(
            [(lx - 86, ly - 6), (lx - 86, ly + 20), (lx - 86, ly - 26)],
            occupied, boxA, 84, 13)
        s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="11" '
                 f'fill="{col}">{esc(txt)}</text>')
        if fell:
            leaders.append((lx, ly, x, y, 84.0))

    # the measured fit, drawn only over the range it was fitted on
    d_v, _, e_v, _, _ = M.vb('velocity', 'avg')
    rfit = np.exp(np.linspace(np.log(M.HELIOS_RMIN), np.log(M.HELIOS_RMAX),
                              60))
    s.append(f'<path d="{path(ax(rfit), ay(d_v*rfit**e_v))}" fill="none" '
             f'stroke="{ACC}" stroke-width="3.4"/>')
    fx, fy = ax(M.HELIOS_RMIN), ay(d_v*M.HELIOS_RMIN**e_v)
    x, y, fell = place_label([(fx + 6, fy + 34), (fx + 6, fy + 52)],
                             occupied, boxA, 190, 13)
    s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="11" fill="{ACC}">'
             f'{esc(f"measured: {d_v:.1f} r^+{e_v:.3f} km/s")}</text>')
    leaders.append((fx + 40, ay(d_v*0.4**e_v), x, y, 190.0))
    s.append(f'<text x="{x:.1f}" y="{y+14:.1f}" font-size="10" '
             f'fill="{MUT}">Venzmer &amp; Bothmer (2018), Table 3, mean fit'
             f'</text>')
    s.append(f'<text x="{AX0+8:.0f}" y="{AY0+15:.0f}" font-size="10.5" '
             f'fill="{MUT}">○ sonic point</text>')
    for lx, ly, tx, ty, tw in leaders:
        s.append(leader_svg(lx, ly, tx, ty, tw, 13.0))

    # ---------------- panel B: the residual ----------------
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-38:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The residual: '
             f'd ln v / d ln r over 0.29–0.98 au</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-22:.0f}" font-size="10.5" '
             f'text-anchor="middle" fill="{MUT}">On the axis above, a slope '
             f'of 0.049 and a slope of 0.19 differ by a few pixels. Here '
             f'they do not.</text>')

    rows = []
    for T0 in (1.0e6, 1.5e6, 2.0e6):
        rows.append((f'isothermal, T₀ = {T0/1e6:.1f} MK',
                     M.parker_slope_chord(T0), 0.0, YEL))
    Ts = np.linspace(M.T_SCAN_LO, M.T_BASE_SONIC, 121)
    chords = np.array([M.parker_slope_chord(T) for T in Ts])
    imin = int(np.argmin(chords))
    rows.append((f'isothermal, best of 0.5–{M.T_BASE_SONIC/1e6:.2f} MK',
                 chords[imin], 0.0, VIO))
    s_pred, s_err = M.euler_slope_from_fits('avg')
    rows.append(('steady Euler, measured ∇P', s_pred, s_err, ACC2))
    rows.append(('measured (VB18 mean fit)', e_v,
                 M.vb('velocity', 'avg')[3], ACC))

    SMAX = 0.28
    n = len(rows)
    dy = (BY1 - BY0)/n

    def bx(v):
        return BX0 + v/SMAX*(BX1 - BX0)

    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" width="{BX1-BX0:.0f}" '
             f'height="{BY1-BY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for st in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25):
        x = bx(st)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{st:.2f}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">d ln v / d ln r</text>')

    # the measured band, drawn behind the bars
    mlo, mhi = e_v - M.vb('velocity', 'avg')[3], e_v + M.vb('velocity',
                                                            'avg')[3]
    s.append(f'<rect x="{bx(mlo):.1f}" y="{BY0:.0f}" '
             f'width="{bx(mhi)-bx(mlo):.1f}" height="{BY1-BY0:.0f}" '
             f'fill="{ACC}" fill-opacity="0.22"/>')
    s.append(f'<line x1="{bx(e_v):.1f}" y1="{BY0:.0f}" x2="{bx(e_v):.1f}" '
             f'y2="{BY1:.0f}" stroke="{ACC}" stroke-width="1.4"/>')

    for i, (lab, val, err, col) in enumerate(rows):
        yc = BY0 + (i + 0.5)*dy
        s.append(f'<text x="{BX0-10:.0f}" y="{yc+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{FG}">{esc(lab)}</text>')
        s.append(f'<rect x="{bx(0.0):.1f}" y="{yc-6:.1f}" '
                 f'width="{max(bx(val)-bx(0.0), 1.0):.1f}" height="12" '
                 f'fill="{col}" fill-opacity="0.55"/>')
        if err > 0.0:
            s.append(f'<line x1="{bx(val-err):.1f}" y1="{yc:.1f}" '
                     f'x2="{bx(val+err):.1f}" y2="{yc:.1f}" stroke="{col}" '
                     f'stroke-width="2"/>')
            for e2 in (val - err, val + err):
                s.append(f'<line x1="{bx(e2):.1f}" y1="{yc-5:.1f}" '
                         f'x2="{bx(e2):.1f}" y2="{yc+5:.1f}" '
                         f'stroke="{col}" stroke-width="2"/>')
        # the value, placed just right of the bar and kept inside the box
        tx = min(bx(val) + 8 + (18 if err > 0 else 0), BX1 - 46)
        s.append(f'<text x="{tx:.1f}" y="{yc+4:.1f}" font-size="10.5" '
                 f'fill="{col}">{val:.3f}</text>')

    # --- caption ---------------------------------------------------------
    cap = [
        "Upper: the transonic isothermal solution v(r) for three coronal "
        "temperatures, each with its own sonic radius r_c = GM/(2a²). Raising",
        "T₀ moves r_c inward and the whole curve up. Lower: the same three "
        "models reduced to the one number Helios measured, the logarithmic",
        "slope over 0.29–0.98 au. No isothermal temperature between 0.5 and "
        "5 MK gets below "
        f"{chords[imin]:.3f}. Steady Euler fed the MEASURED pressure",
        "gradient goes the other way and predicts "
        f"{s_pred:.4f}. Thermal proton pressure accounts for about one third "
        "of the measured acceleration.",
    ]
    for i, line in enumerate(cap):
        s.append(f'<text x="{AX0-48:.0f}" y="{BY1+54+i*15:.0f}" '
                 f'font-size="10.5" fill="{MUT}">{esc(line)}</text>')
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure 3: the Sgr A* accretion-rate ladder
# =========================================================================

def build_sgra():
    W, H = 760, 400
    X0, X1, Y0, Y1 = 250.0, 700.0, 56.0, 268.0
    LMIN, LMAX = -9.6, -4.6         # log10 Mdot / (M_sun/yr)

    def lx(v):
        return X0 + (np.log10(v) - LMIN)/(LMAX - LMIN)*(X1 - X0)

    # --- the numbers, all from m09_numbers -------------------------------
    M_sgra = M.SGRA_M_MSUN*M.Msun
    kT = M.BAG_KT_KEV*M.keV
    cs = np.sqrt(M.BAG_GAMMA*kT/(M.BAG_MU*M.mp))
    rho = M.BAG_NE*M.BAG_MU*M.mp
    mdot = M.bondi_rate(M_sgra, rho, cs, M.BAG_GAMMA)*M.yr/M.Msun
    M_implied = M.BAG_RB_PAPER_PC*M.pc*M.BAG_CS_PAPER**2/(2.0*M.G)/M.Msun

    rows = [
        (f'Bondi rate, M = {M.SGRA_M_MSUN/1e6:.2f}×10⁶ M☉', mdot, 'point',
         ACC, 'this module, GRAVITY (2022) mass'),
        (f'Bondi rate, M = {M_implied/1e6:.1f}×10⁶ M☉', M.BAG_MDOT_PAPER,
         'point', YEL, 'Baganoff et al. (2003), their Sect. 11.1.2, their own mass'),
        ('upper limit, r_in ≈ 30 r_S', M.MAR_UPPER_HEAD, 'upper', ACC2,
         'Marrone et al. (2007), Faraday rotation'),
        ('upper limit, r_in ≈ 100 r_S', M.MAR_UPPER_TIGHT, 'upper', ACC2,
         'Marrone et al. (2007), their Sect. 4'),
        ('lower limit, r_in ≈ 10 r_S', M.MAR_LOWER_10RS, 'lower', VIO,
         'Marrone et al. (2007), their Sect. 4, 1–2×10⁻⁸'),
        ('lower limit, r_in ≈ 3 r_S', M.MAR_LOWER_3RS, 'lower', VIO,
         'Marrone et al. (2007), their Sect. 4, 2–4×10⁻⁹'),
    ]

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="A logarithmic axis of accretion rate onto '
         f'Sagittarius A star in solar masses per year, from ten to the '
         f'minus nine and a half to ten to the minus four and a half. Six '
         f'rungs. The two highest are the Bondi rate computed from the '
         f'measured gas density and temperature, at eight times ten to the '
         f'minus six and three times ten to the minus six. Below them, four '
         f'limits from Faraday rotation: two upper limits at two times ten '
         f'to the minus seven and five times ten to the minus eight, and '
         f'two lower limits at one and a half times ten to the minus eight '
         f'and three times ten to the minus nine. The gap between the Bondi '
         f'rate and the highest upper limit is a factor of forty, but that '
         f'upper limit assumes a magnetic field near equipartition strength; '
         f'at three per cent of equipartition the same rotation measure '
         f'allows a rate ten times higher and the gap is a factor of four. '
         f'The two lower limits carry no such condition.">']

    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y0-30:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">What Bondi accretion '
             f'predicts for Sgr A*, and what is measured</text>')
    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for e in range(-9, -4):
        x = lx(10.0**e)
        s.append(f'<line x1="{x:.1f}" y1="{Y0:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1:.0f}" stroke="{RULE}" stroke-width="0.7" '
                 f'stroke-dasharray="2 4"/>')
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">10{esc(_sup(e))}</text>')
    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">'
             f'Ṁ / (M☉ yr⁻¹)</text>')

    dy = (Y1 - Y0)/len(rows)
    for i, (lab, val, kind, col, note) in enumerate(rows):
        yc = Y0 + (i + 0.5)*dy
        s.append(f'<text x="{X0-10:.0f}" y="{yc+1:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{FG}">{esc(lab)}</text>')
        s.append(f'<text x="{X0-10:.0f}" y="{yc+13:.1f}" font-size="9" '
                 f'text-anchor="end" fill="{MUT}">{esc(note)}</text>')
        x = lx(val)
        if kind == 'point':
            s.append(f'<circle cx="{x:.1f}" cy="{yc:.1f}" r="5.5" '
                     f'fill="{col}"/>')
        else:
            # an arrow running in the permitted direction
            x2 = lx(10.0**LMIN) + 6 if kind == 'upper' else lx(10.0**LMAX) - 6
            s.append(f'<line x1="{x:.1f}" y1="{yc:.1f}" x2="{x2:.1f}" '
                     f'y2="{yc:.1f}" stroke="{col}" stroke-width="2"/>')
            s.append(f'<line x1="{x:.1f}" y1="{yc-7:.1f}" x2="{x:.1f}" '
                     f'y2="{yc+7:.1f}" stroke="{col}" stroke-width="2.6"/>')
            hx = 1.0 if kind == 'lower' else -1.0
            s.append(f'<path d="M {x2:.1f},{yc:.1f} L {x2-hx*9:.1f},'
                     f'{yc-5:.1f} L {x2-hx*9:.1f},{yc+5:.1f} Z" '
                     f'fill="{col}"/>')
        # The value, kept inside the plot box on both axes.  The first row
        # sits only dy/2 below the top edge, so a label at yc-10 escaped it.
        # Point rungs are labelled to the LEFT of the dot: the bracket's
        # dashed stub runs down the right-hand side from the top rung.
        end = kind in ('upper', 'point') or (x > X1 - 66)
        tvx = min(max(x + (-9 if end else 9), X0 + (66 if end else 4)),
                  X1 - (4 if end else 66))
        tvy = min(max(yc - 10.0, Y0 + 12.0), Y1 - 4.0)
        s.append(f'<text x="{tvx:.1f}" y="{tvy:.1f}" font-size="10" '
                 f'text-anchor="{"end" if end else "start"}" '
                 f'fill="{col}">{esc(_sci(val))}</text>')

    # The annotated gap between the Bondi rate (row 0) and the headline
    # bound (row 2).  The horizontal bar sits between them, and a stub
    # runs from each end up or down to the rung it belongs to, so the
    # bracket cannot be misread as belonging to row 1.
    xa, xb = lx(mdot), lx(M.MAR_UPPER_HEAD)
    y_bondi, y_bound = Y0 + 0.5*dy, Y0 + 2.5*dy
    ygap = Y0 + 1.96*dy
    s.append(f'<line x1="{xb:.1f}" y1="{ygap:.1f}" x2="{xa:.1f}" '
             f'y2="{ygap:.1f}" stroke="{FG}" stroke-width="1.6"/>')
    s.append(f'<line x1="{xa:.1f}" y1="{y_bondi+8:.1f}" x2="{xa:.1f}" '
             f'y2="{ygap:.1f}" stroke="{FG}" stroke-width="1.2" '
             f'stroke-dasharray="3 3"/>')
    s.append(f'<line x1="{xb:.1f}" y1="{ygap:.1f}" x2="{xb:.1f}" '
             f'y2="{y_bound-8:.1f}" stroke="{FG}" stroke-width="1.2" '
             f'stroke-dasharray="3 3"/>')
    for xx in (xa, xb):
        s.append(f'<line x1="{xx:.1f}" y1="{ygap-5:.1f}" x2="{xx:.1f}" '
                 f'y2="{ygap+5:.1f}" stroke="{FG}" stroke-width="1.6"/>')
    s.append(f'<text x="{(xa+xb)/2:.1f}" y="{ygap-9:.1f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">factor '
             f'{mdot/M.MAR_UPPER_HEAD:.0f}</text>')
    # The upper limit assumes a near-equipartition field.  Marrone et al.
    # (2007), their Sect. 4: a fraction epsilon of equipartition raises the
    # limit by epsilon^(-2/3), a factor of 10 at 3 per cent.  Print the
    # condition next to the number, or the figure overclaims what the text
    # beside it already qualifies.
    s.append(f'<text x="{(xa+xb)/2:.1f}" y="{ygap+16:.1f}" font-size="9.5" '
             f'text-anchor="middle" fill="{MUT}">equipartition field; '
             f'{mdot/(M.MAR_UPPER_HEAD*0.03**(-2.0/3.0)):.0f} at 3% of it'
             f'</text>')

    cap = [
        "The Bondi arithmetic is not in doubt: m09_numbers.py rebuilds "
        "λ(γ) from the sonic point to eight figures, and the top two rungs",
        "agree once Baganoff et al.'s 2.6×10⁶ M☉ is rescaled to the GRAVITY "
        "mass by M². Bondi himself, though, proves only that λ ≤ λ_c; the",
        "transonic choice is his physical argument. What the gap indicts is "
        "the three premises — no angular momentum, no outflow, adiabatic and",
        "radiatively unimportant — every one of which Sgr A* violates. The "
        "lower limits are a measurement too, and unlike the upper ones they",
        "carry no assumption about the field: the flow is not switched off, "
        "it is throttled somewhere between the Bondi radius and the horizon.",
    ]
    for i, line in enumerate(cap):
        s.append(f'<text x="{X0-220:.0f}" y="{Y1+56+i*15:.0f}" '
                 f'font-size="10.5" fill="{MUT}">{esc(line)}</text>')
    s.append('</svg>')
    return "\n".join(s)


def _sup(e):
    """Unicode superscript for a small negative integer exponent."""
    digits = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    sign = "⁻" if e < 0 else ""
    return sign + "".join(digits[int(d)] for d in str(abs(e)))


def _sci(v):
    """'8.0×10⁻⁶' for an axis annotation."""
    e = int(np.floor(np.log10(v)))
    m = v/10.0**e
    return f'{m:.1f}×10{_sup(e)}'


if __name__ == "__main__":
    for name, body in (("m09_fig_topology.svg", build_topology()),
                       ("m09_fig_parker.svg", build_parker()),
                       ("m09_fig_sgra.svg", build_sgra())):
        with open(name, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"wrote {name} ({len(body)} bytes)")
