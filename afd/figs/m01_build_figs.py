"""Build the computed SVG figures for Module 1.

Writes m01_fig_phase.svg (the (n,T) plane with Coulomb mean-free-path
contours) and m01_fig_ladder.svg (the Knudsen ladder).  Geometry is
computed, never eyeballed; every plotted point is a value printed by
m01_numbers.py.
"""
import numpy as np
from m01_numbers import (kB, e, pc, kpc, AU, lam_coulomb, lnLambda_e,
                         lam_neutral, Rsun, SPITZER_C)

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"


def fmt_pow(x):
    """Unicode 10^k label."""
    sup = str.maketrans("-0123456789", "⁻⁰¹²³"
                        "⁴⁵⁶⁷⁸⁹")
    return "10" + str(int(round(x))).translate(sup)


def fmt_kn(kn):
    """Format a Knudsen number as a Unicode mantissa x 10^exp string."""
    if kn >= 0.1:
        return f"{kn:.2g}"
    ex = int(np.floor(np.log10(kn)))
    man = kn/10.0**ex
    mant = f"{man:.0f}" if abs(man-round(man)) < 0.05 else f"{man:.1f}"
    return f"{mant}×{fmt_pow(ex)}"


# ===================================================================
# Figure A -- the (n, T) plane
# ===================================================================
LN0, LN1 = -5.0, 27.0        # log10 n_e / cm^-3
LT0, LT1 = 3.4, 9.0          # log10 T / K
X0, X1, Y0, Y1 = 78.0, 700.0, 46.0, 350.0


def px(ln):
    return X0 + (ln-LN0)/(LN1-LN0)*(X1-X0)


def py(lt):
    return Y1 - (lt-LT0)/(LT1-LT0)*(Y1-Y0)


def n_for_lambda(T, lam_target):
    """Solve lambda_coulomb(n, T) = lam_target for n by fixed-point
    iteration on the weak ln Lambda(n) dependence."""
    n = 1.0
    for _ in range(80):
        lnL = lnLambda_e(n, T)
        if lnL <= 1.0:
            lnL = 1.0
        n_new = SPITZER_C*(kB*T)**2/(e**4*lnL*lam_target)
        n = np.exp(0.5*(np.log(n)+np.log(n_new)))
    return n


# Contour spacing is set by readability, not by taste. Adjacent decades
# of lambda sit 19.4 px apart on this x-axis, so a 3-decade step (1 pc,
# 1 kpc, 1 Mpc) leaves a 58 px corridor — narrower than any system label.
# Keeping every third-decade contour therefore makes the ICM labels
# unplaceable. These five leave corridors of 103 px and wider.
CONTOURS = [(1.0e-8, "1 Å"), (1.0, "1 cm"), (AU, "1 AU"),
            (pc, "1 pc"), (1.0e3*kpc, "1 Mpc")]

SYSTEMS = [
    # label, n_e cm^-3, T K, L cm, label dx, dy, anchor
    ("solar centre", 1.0e26, 1.5e7, Rsun, -8, -8, "end"),
    ("AGN inner disc", 1.0e15, 1.0e5, 3.0e13, -8, 14, "end"),
    ("solar corona", 3.0e8, 2.0e6, 7.0e9, -8, -8, "end"),
    ("solar wind, 1 AU", 5.0, 1.2e5, AU, 9, 4, "start"),
    ("warm ionised ISM", 0.1, 8.0e3, 100*pc, 9, 12, "start"),
    ("hot ISM", 3.0e-3, 1.0e6, 100*pc, 9, -8, "start"),
    ("ICM core", 1.0e-2, 3.0e7, 100*kpc, 9, 14, "start"),
    ("ICM outskirts", 1.0e-4, 1.0e8, 2000*kpc, 9, -8, "start"),
]


def _box_curve_clearance(box, pts):
    """Smallest distance from an axis-aligned box to any sampled contour
    point. Zero if a point lies inside the box. `pts` is one (N, 2)
    array of every contour sample, stacked once by the caller: the
    search evaluates hundreds of candidate boxes, so this has to be a
    vector operation rather than a Python loop."""
    x0, y0, x1, y1 = box
    dx = np.maximum.reduce([x0-pts[:, 0], np.zeros(len(pts)),
                            pts[:, 0]-x1])
    dy = np.maximum.reduce([y0-pts[:, 1], np.zeros(len(pts)),
                            pts[:, 1]-y1])
    return float(np.min(np.hypot(dx, dy)))


def _boxes_overlap(a, b):
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


# Candidate label placements, as (dx, dy, anchor). The search prefers
# earlier entries, so a label only moves far when it has to.
_CANDS = []
for _r in range(10, 171, 6):
    for _ddy in range(-84, 85, 6):
        _CANDS.append((_r, _ddy, "start"))
        _CANDS.append((-_r, _ddy, "end"))


def best_label_spot(x, y, w, curves, placed, bounds):
    """Pick a label position near (x, y) that clears every contour and
    every box already claimed, and stays inside `bounds`. Returns
    (text_x, baseline_y, anchor, label_box). Falls back to the least-bad
    candidate rather than failing."""
    bx0, by0, bx1, by1 = bounds
    best, best_score, best_box = None, -1e9, None
    for dx, dy, anc in _CANDS:
        tx, ty = x+dx, y+dy
        x0 = tx if anc == "start" else tx-w
        box = (x0-3, ty-12, x0+w+3, ty+18)
        if box[0] < bx0 or box[2] > bx1 or box[1] < by0 or box[3] > by1:
            continue
        if any(_boxes_overlap(box, p) for p in placed):
            continue
        clear = _box_curve_clearance(box, curves)
        score = min(clear, 16.0)*20.0 - (abs(dx)+abs(dy))*0.35
        if score > best_score:
            best, best_score, best_box = (tx, ty, anc), score, box
    if best is None:
        tx, ty = x+10, y+5
        return tx, ty, "start", (tx-3, ty-12, tx+w+3, ty+18)
    return best[0], best[1], best[2], best_box


def build_phase():
    s = [f'<svg class="setupfig" viewBox="0 0 760 430" width="100%" '
         f'role="img" aria-label="density-temperature plane with contours '
         f'of constant Coulomb mean free path">']
    s.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" '
             f'fill="#0b1324" stroke="{RULE}" stroke-width="1"/>')
    # grid
    for ln in range(-4, 28, 4):
        s.append(f'<line x1="{px(ln):.1f}" y1="{Y0}" x2="{px(ln):.1f}" '
                 f'y2="{Y1}" stroke="{RULE}" stroke-width=".6"/>')
        s.append(f'<text x="{px(ln):.1f}" y="{Y1+16:.0f}" font-size="11" '
                 f'text-anchor="middle" fill="{MUT}">{fmt_pow(ln)}</text>')
    for lt in range(4, 10):
        s.append(f'<line x1="{X0}" y1="{py(lt):.1f}" x2="{X1}" '
                 f'y2="{py(lt):.1f}" stroke="{RULE}" stroke-width=".6"/>')
        s.append(f'<text x="{X0-8:.0f}" y="{py(lt)+4:.1f}" font-size="11" '
                 f'text-anchor="end" fill="{MUT}">{fmt_pow(lt)}</text>')
    # Contours. Points are clipped to the plot box HERE rather than left
    # to the SVG clip-path: a clip-path hides ink but the polyline still
    # occupies those coordinates, and an overlap check that reads
    # geometry rather than pixels will report a hit outside the frame.
    s.append('<g>')
    curves, reserved = [], []
    Tg = np.logspace(LT0, LT1, 900)
    for lam_t, lab in CONTOURS:
        pts = []
        for T in Tg:
            xx, yy = px(np.log10(n_for_lambda(T, lam_t))), py(np.log10(T))
            if X0 <= xx <= X1 and Y0 <= yy <= Y1:
                pts.append((xx, yy))
        if len(pts) < 2:
            continue
        # Clearance is tested against the FULL sample list: decimating
        # first leaves gaps between points that the test walks straight
        # through, and a label then lands on a segment it never saw.
        curves.extend(pts)
        draw = pts[::16] + [pts[-1]]         # decimate only what is drawn
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in draw)
        s.append(f'<polyline points="{d}" fill="none" stroke="{ACC2}" '
                 f'stroke-width="1.3" stroke-opacity=".75" '
                 f'stroke-dasharray="5 4"/>')
        # Label where the contour leaves the box, top edge or right edge;
        # both strips are free of system points.
        lx, ly = pts[-1]
        if ly < Y0+26:
            tx, ty, anc = lx+5, Y0+14, "start"
            cbox = (tx-3, ty-11, tx+len(lab)*6.0+3, ty+4)
        else:
            tx, ty, anc = X1-5, ly-6, "end"
            cbox = (tx-len(lab)*6.0-3, ty-11, tx+3, ty+4)
        reserved.append(cbox)
        s.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="10.5" '
                 f'text-anchor="{anc}" fill="{ACC2}">{lab}</text>')
    s.append('</g>')
    allpts = np.array(curves)
    # System points. The label offset is SEARCHED, not chosen by eye: the
    # contours are steep and closely spaced near the points, so a fixed
    # offset puts most labels on top of a dashed line. Labels are confined
    # to the plot box, because outside it they collide with the tick
    # labels and the axis titles, and a leader line is drawn whenever the
    # search had to move a label far enough to break the association.
    bounds = (X0+4, Y0+4, X1-4, Y1-4)
    for lab, n, T, L, _dx, _dy, _anc in SYSTEMS:
        x, y = px(np.log10(n)), py(np.log10(T))
        kn = lam_coulomb(n, T)/L
        kn_txt = f"Kn ≈ {fmt_kn(kn)}"
        w = max(len(lab)*6.1, len(kn_txt)*5.6)
        bx, by, anc, box = best_label_spot(
            x, y, w, allpts, reserved, bounds)
        reserved.append(box)
        ax = box[0] if bx > x else box[2]
        ay = (box[1]+box[3])/2.0
        if np.hypot(ax-x, ay-y) > 17.0:
            s.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{ax:.1f}" '
                     f'y2="{ay:.1f}" stroke="{ACC}" stroke-width=".9" '
                     f'stroke-opacity=".65"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{ACC}" '
                 f'stroke="{BG}" stroke-width="1.2"/>')
        s.append(f'<text x="{bx:.1f}" y="{by:.1f}" font-size="11.5" '
                 f'text-anchor="{anc}" fill="#f8fafc">{lab}</text>')
        s.append(f'<text x="{bx:.1f}" y="{by+13:.1f}" font-size="10" '
                 f'text-anchor="{anc}" fill="{MUT}">{kn_txt}</text>')
    # axis titles
    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+38:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">electron number density '
             f'<tspan font-style="italic">n</tspan>'
             f'<tspan baseline-shift="sub" font-size="9">e</tspan>'
             f' / cm<tspan baseline-shift="super" font-size="9">−3'
             f'</tspan></text>')
    s.append(f'<text x="22" y="{(Y0+Y1)/2:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}" transform="rotate(-90 22 '
             f'{(Y0+Y1)/2:.0f})">temperature <tspan font-style="italic">T'
             f'</tspan> / K</text>')
    s.append(f'<text x="{X0}" y="{Y1+62:.0f}" font-size="11" fill="{ACC2}">'
             f'dashed: contours of constant Coulomb mean free path '
             f'λ</text>')
    s.append(f'<text x="{X0}" y="{Y1+78:.0f}" font-size="11" fill="{ACC}">'
             f'dots: ionised astrophysical plasmas, annotated with their '
             f'Knudsen number Kn = λ/L</text>')
    s.append('</svg>')
    return "\n".join(s)


# ===================================================================
# Figure B -- the Knudsen ladder
# ===================================================================
LK0, LK1 = -14.0, 2.0
LX0, LX1, LY = 60.0, 700.0, 150.0


def kx(lk):
    return LX0 + (lk-LK0)/(LK1-LK0)*(LX1-LX0)


LADDER = [
    ("solar photosphere", "λ = 66 µm, L = 150 km",
     lam_neutral(1.2e5/(kB*5772.0), 1e-15)/1.5e7, -1),
    ("room air", "λ = 68 nm, L = 3 m", 6.8e-6/300.0, 1),
    ("warm neutral ISM", "λ = 134 AU, L = 100 pc",
     lam_neutral(0.5, 1e-15)/(100*pc), -1),
    ("intracluster medium, core", "λ = 0.2 kpc, L = 100 kpc",
     lam_coulomb(1e-2, 3e7)/(100*kpc), 1),
    ("intracluster medium, outskirts", "λ = 222 kpc, L = 2 Mpc",
     lam_coulomb(1e-4, 1e8)/(2000*kpc), -1),
    ("solar wind at 1 AU", "λ = 1.9 AU, L = 1 AU",
     lam_coulomb(5.0, 1.2e5)/AU, 1),
]

BANDS = [(-14.0, -2.0, "Euler: ideal fluid", ACC2),
         (-2.0, -1.0, "Navier–Stokes: first-order transport", VIO),
         (-1.0, 1.0, "transition: no closed fluid closure", YEL),
         (1.0, 2.0, "free molecular", "#f87171")]


def build_ladder():
    """All regime bands sit ABOVE the axis, all system callouts BELOW it,
    so band labels and callout labels can never collide.  Band names go in
    a legend row, because three of the four bands are one decade wide and
    too narrow to letter in place."""
    s = ['<svg class="setupfig" viewBox="0 0 760 352" width="100%" '
         'role="img" aria-label="logarithmic Knudsen number axis with '
         'astrophysical systems and fluid-model validity regimes">']
    # regime strip above the axis
    for a, b, lab, col in BANDS:
        xa, xb = kx(a), kx(b)
        s.append(f'<rect x="{xa:.1f}" y="{LY-40:.0f}" width="{xb-xa:.1f}" '
                 f'height="32" fill="{col}" fill-opacity="0.22" '
                 f'stroke="{col}" stroke-opacity="0.55" stroke-width="1"/>')
    s.append(f'<text x="{kx(-8):.0f}" y="{LY-19:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{ACC2}">Euler: ideal fluid</text>')
    # legend for the three narrow bands
    lx, ly0 = LX0, 40
    for k, (a, b, lab, col) in enumerate(BANDS[1:]):
        yy = ly0 + 17*k
        s.append(f'<rect x="{lx:.0f}" y="{yy-9:.0f}" width="16" height="11" '
                 f'fill="{col}" fill-opacity="0.35" stroke="{col}" '
                 f'stroke-opacity="0.7" stroke-width="1"/>')
        rng = (f'Kn = {fmt_pow(a)}–{fmt_pow(b)}' if b < 2
               else f'Kn ≥ {fmt_pow(a)}')
        s.append(f'<text x="{lx+22:.0f}" y="{yy:.0f}" font-size="11" '
                 f'fill="{col}">{lab}   <tspan fill="{MUT}">({rng})'
                 f'</tspan></text>')
    # the axis
    s.append(f'<line x1="{LX0}" y1="{LY}" x2="{LX1}" y2="{LY}" '
             f'stroke="{MUT}" stroke-width="1.6"/>')
    for lk in range(-14, 3, 2):
        x = kx(lk)
        s.append(f'<line x1="{x:.1f}" y1="{LY-5:.0f}" x2="{x:.1f}" '
                 f'y2="{LY+5:.0f}" stroke="{MUT}" stroke-width="1.2"/>')
        s.append(f'<text x="{x:.1f}" y="{LY+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{fmt_pow(lk)}</text>')
    # Callouts all sit below the axis, sorted by ascending Kn, and every
    # label is RIGHT-anchored so its text runs leftward from its own
    # leader. Leaders further left belong to earlier (shallower) rows, so
    # no label can ever cross a leader. Left-anchoring would cross.
    rows = sorted(LADDER, key=lambda r: r[2])
    for k, (lab, sub, kn, _side) in enumerate(rows):
        x = kx(np.log10(kn))
        ytip = LY + 44 + 24*k
        s.append(f'<line x1="{x:.1f}" y1="{LY+8:.0f}" x2="{x:.1f}" '
                 f'y2="{ytip:.1f}" stroke="{ACC}" stroke-width="1.1" '
                 f'stroke-opacity="0.8"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{LY:.0f}" r="4" fill="{ACC}" '
                 f'stroke="{BG}" stroke-width="1"/>')
        s.append(f'<text x="{x-7:.1f}" y="{ytip+4:.1f}" font-size="11.5" '
                 f'text-anchor="end" fill="#f8fafc">{lab}  '
                 f'<tspan font-size="9.5" fill="{MUT}">{sub}</tspan></text>')
    s.append(f'<text x="{(LX0+LX1)/2:.0f}" y="340" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Knudsen number '
             f'Kn = λ / L</text>')
    s.append('</svg>')
    return "\n".join(s)


# ===================================================================
# Figure C -- a magnetised particle: bounded across B, free along it
# ===================================================================
def build_gyro():
    """The projection of a helix onto the page. The transverse amplitude
    is the gyroradius; the axial extent is set only by how long you
    watch. Drawn from sampled points, not from hand-placed arcs, so the
    animation path and the drawn path are the same object."""
    gx0, gx1, gy = 92.0, 690.0, 118.0
    amp, wl = 34.0, 82.0
    pts = []
    for k in range(361):
        x = gx0 + (gx1-gx0)*k/360.0
        y = gy + amp*np.sin(2.0*np.pi*(x-gx0)/wl)
        pts.append((x, y))
    d = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    s = ['<svg class="setupfig" viewBox="-10 -10 772 248" width="100%" '
         'role="img" aria-label="a charged particle spiralling along a '
         'magnetic field line, bounded across the field and free along '
         'it">']
    s.append('<defs><marker id="m1gB" markerWidth="9" markerHeight="9" '
             'refX="7" refY="3" orient="auto">'
             f'<path d="M0,0 L7,3 L0,6 Z" fill="{MUT}"/></marker>'
             '<marker id="m1gR" markerWidth="8" markerHeight="8" refX="6" '
             f'refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" '
             f'fill="{ACC2}"/></marker>'
             '<marker id="m1gRb" markerWidth="8" markerHeight="8" refX="6" '
             f'refY="3" orient="auto"><path d="M6,0 L0,3 L6,6 Z" '
             f'fill="{ACC2}"/></marker></defs>')
    # the field line
    s.append(f'<line x1="40" y1="{gy}" x2="722" y2="{gy}" stroke="{MUT}" '
             f'stroke-width="1.6" marker-end="url(#m1gB)"/>')
    s.append(f'<text x="46" y="{gy-10:.0f}" font-size="13" class="vb" '
             f'fill="{MUT}">B</text>')
    # the orbit
    s.append(f'<path id="m1gpath" d="{d}" fill="none" stroke="{ACC}" '
             f'stroke-width="1.9" stroke-opacity="0.85"/>')
    s.append(f'<circle r="5.5" fill="{ACC}" stroke="{BG}" stroke-width="1">'
             '<animateMotion dur="6s" repeatCount="indefinite" '
             'rotate="auto"><mpath href="#m1gpath"/></animateMotion>'
             '</circle>')
    # transverse extent = 2 r_g
    xr = gx0 + 0.25*wl          # first crest
    s.append(f'<line x1="{xr:.1f}" y1="{gy-amp:.1f}" x2="{xr:.1f}" '
             f'y2="{gy+amp:.1f}" stroke="{ACC2}" stroke-width="1.2" '
             f'marker-start="url(#m1gRb)" marker-end="url(#m1gR)"/>')
    s.append(f'<text x="{xr-8:.1f}" y="{gy-amp-8:.1f}" font-size="12" '
             f'text-anchor="middle" fill="{ACC2}">2<tspan font-style='
             f'"italic">r</tspan><tspan baseline-shift="sub" '
             f'font-size="9">g</tspan></text>')
    s.append(f'<line x1="40" y1="{gy-amp:.1f}" x2="700" y2="{gy-amp:.1f}" '
             f'stroke="{ACC2}" stroke-width=".8" stroke-dasharray="4 5" '
             f'stroke-opacity=".5"/>')
    s.append(f'<line x1="40" y1="{gy+amp:.1f}" x2="700" y2="{gy+amp:.1f}" '
             f'stroke="{ACC2}" stroke-width=".8" stroke-dasharray="4 5" '
             f'stroke-opacity=".5"/>')
    # the two captions
    s.append(f'<text x="40" y="34" font-size="12.5" fill="{ACC2}">'
             f'across the field: bounded forever by <tspan '
             f'font-style="italic">r</tspan><tspan baseline-shift="sub" '
             f'font-size="9">g</tspan> = 93 km, with or without '
             f'collisions</text>')
    s.append(f'<text x="40" y="206" font-size="12.5" fill="{ACC}">'
             f'along the field: nothing bounds the motion — the '
             f'particle free-streams a mean free path, 1.9 AU, which is '
             f'3.1×10⁶ gyroradii</text>')
    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    for name, body in (("m01_fig_phase.svg", build_phase()),
                       ("m01_fig_ladder.svg", build_ladder()),
                       ("m01_fig_gyro.svg", build_gyro())):
        with open(name, "w", encoding="utf-8") as f:
            f.write(body)
        print("wrote", name, len(body), "bytes")
    print("\nPUNCHLINE CHECK -- the ladder must span Euler to collisionless:")
    for lab, sub, kn, _ in LADDER:
        print(f"  {lab:<34s} Kn = {kn:9.2e}  log10 = {np.log10(kn):6.2f}")
