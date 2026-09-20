"""Build the computed SVG figures for Module 10.

Writes four files:

  m10_fig_cascade.svg   The energy spectrum on log-log axes.  A -5/3 line
                        over a four-decade inertial band, cut off by an
                        exponential at the dissipation scale, with a -2
                        line anchored at the same point so that the two
                        exponents can be compared by eye.  SCHEMATIC in
                        its normalisation: no measured spectrum is plotted
                        anywhere in this module, and the caption says so.

  m10_fig_domain.svg    THE FIGURE THAT EARNS SECTION 6.  The (Kn, Re)
                        plane with Module 2's identity Re = 3 Ma_th/Kn
                        drawn as a family of straight lines, the four
                        fluids of PART D plotted as points, and the band
                        Kn > 1/3 shaded as the region where the
                        Chapman-Enskog expansion of Module 1 is failing.
                        Two of the four points sit inside that band, which
                        is the whole of the argument that their Reynolds
                        numbers are formulae outside their own domain.

  m10_fig_podesta.svg   THE ANCHOR FIGURE.  Podesta, Roberts & Goldstein
                        (2007) Table 2: four magnetic and four velocity
                        spectral indices with their 99 per cent confidence
                        limits, against horizontal lines at 5/3 and 3/2.
                        The magnetic mean sits on 5/3 with real scatter;
                        all four velocity points sit below it, on the same
                        side.  Error bars are 99 per cent limits and the
                        caption says how to convert them to sigma.

  m10_fig_pdf.svg       The log-normal density PDF at M = 10 for b = 1/3
                        and b = 1.  Upper panel linear, so the widths can
                        be compared; lower panel logarithmic, because the
                        consequence is in the tail and a linear axis hides
                        it.  The rho > 100 <rho> tail is shaded in both.

Geometry is computed, never eyeballed.  Every physical number drawn is
produced by m10_numbers.py's own functions, so a figure cannot drift away
from the prose.

Lessons carried in from Modules 1 and 9:

  * check_overlap reads geometry, not pixels, so curves are truncated by
    their POINT LISTS and never by an SVG clip-path, and label clearance
    is tested against the full sample list.
  * place_label searches, and its `window` caps how far a fallback may
    travel: a label whose only clear seat is on the far side of the plot
    lands among a different family and says the wrong thing.
  * A colour key belongs to the whole figure.  m10_fig_pdf's two panels
    carry the SAME key, b = 1/3 teal and b = 1 orange, in both.
"""
import os

import numpy as np

import m10_numbers as M

# Write beside THIS file, whatever the working directory is.  Running
# `python figs/m10_build_figs.py` from afd/ once dropped four stray
# SVGs into afd/ that splice.py never reads, because splice.py
# resolves its own directory and this script did not.
HERE = os.path.dirname(os.path.abspath(__file__))


def out(name):
    return os.path.join(HERE, name)


BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"
RED = "#f87171"

# check_svg rejects a literal "_" or "^" inside a <text>, so every
# subscript and superscript below is a tspan, as in m08 and m09.
SUB = '<tspan baseline-shift="sub" font-size="8">{0}</tspan>'
SUP = '<tspan baseline-shift="super" font-size="8">{0}</tspan>'

# The measured kinematic viscosity of sea-level air, mirroring
# m10_numbers.py PART D(a): TWO significant figures, NO primary source.
# It is the one number in this module that no paper was read for, and the
# domain figure marks the point it produces with an open marker.
NU_AIR_MEAS = 0.15      # cm^2 s^-1


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
    """Choose a label position by search, never by eye.  See m09_build_figs.

    Three passes, each weaker than the last, so the label always ends up
    inside the plot box.  `window` caps the distance a fallback may travel
    from the preferred spot -- the fix Module 9's editor pass earned.
    Returns (x, y, moved).
    """
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
# The four fluids, rebuilt here from m10_numbers.py's own functions so
# that the figure and the prose cannot diverge.  PART D of the prep run
# prints every one of these numbers.
# =========================================================================

def fluid_rows():
    """(label, Kn, Re, Ma_th, colour, open_marker) for the four fluids."""
    rows = []

    # (a) laboratory air at 1 m.  The ONLY row whose Re uses a MEASURED
    # viscosity rather than lam v/3, so it is the only row that does not
    # sit on its own Re = 3 Ma_th/Kn line.  The gap is exactly the 0.69 of
    # PART D(a), and the open marker is how the figure says so.
    T_air, mu_air = 288.15, 28.9647
    v_air = M.v_thermal(T_air, mu_air)
    U_air, L_air = 1.0e3, 1.0e2          # 10 m/s over 1 m
    Kn_air = M.LAM_AIR/L_air
    Ma_air = U_air/v_air
    Re_air = M.reynolds(U_air, L_air, NU_AIR_MEAS)
    rows.append(("laboratory air, 1 m", Kn_air, Re_air, Ma_air, YEL, True))

    # (b) molecular cloud, 10 pc.  Larson's THREE-dimensional sigma is the
    # outer-scale speed; PART D(b) and the speed table of section 6 both
    # say so.
    T_mc, mu_mc, n_mc = 10.0, 2.33, 1.0e2
    lam_mc = 1.0/(n_mc*M.SIGMA_H)
    v_mc = M.v_thermal(T_mc, mu_mc)
    nu_mc = M.nu_kinetic(lam_mc, v_mc)
    L_mc = 10.0*M.pc
    # 2.64e5 cm/s, not larson_sigma(10.0)*1e5 = 2.6389e5: PART D(b) of the
    # prep rounds Larson's sigma to the 2.64 km/s the prose quotes, and the
    # figure uses the SAME number so that the two cannot drift apart.
    U_mc = 2.64e5
    rows.append(("molecular cloud, 10 pc", lam_mc/L_mc,
                 M.reynolds(U_mc, L_mc, nu_mc), U_mc/v_mc, ACC2, False))

    # (c) intracluster medium at Hitomi's 60 kpc.
    n_icm, T_icm, lnL_icm = 1.0e-3, 1.0e8, 37.8
    lam_icm = M.lam_coulomb(n_icm, T_icm, lnL_icm)
    v_icm = M.v_thermal(T_icm, M.MU_H)
    nu_icm = M.nu_kinetic(lam_icm, v_icm)
    L_icm, U_icm = 60.0*M.kpc, M.HITOMI_SIGMA_V
    rows.append(("intracluster medium, 60 kpc", lam_icm/L_icm,
                 M.reynolds(U_icm, L_icm, nu_icm), U_icm/v_icm, ACC, False))

    # (d) solar wind at 1 au, on MODULE 1's census values.
    n_sw, T_sw, U_sw = 5.0, 1.2e5, 4.0e7
    lnL_sw = M.lnLambda_e(n_sw, T_sw)
    lam_sw = M.lam_coulomb(n_sw, T_sw, lnL_sw)
    v_sw = M.v_thermal(T_sw, M.MU_H)
    nu_sw = M.nu_kinetic(lam_sw, v_sw)
    rows.append(("solar wind, 1 au", lam_sw/M.AU,
                 M.reynolds(U_sw, M.AU, nu_sw), U_sw/v_sw, VIO, False))
    return rows


# =========================================================================
# Figure 1: the cascade, and two exponents compared by eye
# =========================================================================

def build_cascade():
    W, H = 720, 400
    X0, X1, Y0, Y1 = 82.0, 660.0, 44.0, 330.0

    DEC = 4.0                       # decades of inertial range drawn
    RE_DRAWN = (10.0**DEC)**(4.0/3.0)   # the Re that band implies

    LX0, LX1 = -0.6, 5.6            # log10(k L)
    LY0, LY1 = -9.6, 1.4            # log10(E), arbitrary normalisation

    def px(lx):
        return X0 + (lx - LX0)/(LX1 - LX0)*(X1 - X0)

    def py(ly):
        return Y1 - (ly - LY0)/(LY1 - LY0)*(Y1 - Y0)

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="A log-log plot of the energy spectrum E '
         'of k against wavenumber k times the outer scale L. A straight '
         'line of slope minus five thirds runs across four decades of '
         'wavenumber, from the stirring scale on the left to the '
         'dissipation scale on the right, where an exponential cut-off '
         'bends it sharply downward. A dashed line of slope minus two '
         'starts at the same point on the left and falls below the first '
         'line, ending about twenty-one times lower after four decades. '
         'Vertical dashed lines mark the stirring scale and the '
         'dissipation scale, and the band between them is shaded and '
         'labelled the inertial range." >' % (W, H)]

    # the inertial band, shaded
    s.append(f'<rect x="{px(0.0):.1f}" y="{Y0:.0f}" '
             f'width="{px(DEC)-px(0.0):.1f}" height="{Y1-Y0:.0f}" '
             f'fill="#1e293b" opacity="0.9"/>')
    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')

    for d in range(0, 6):
        x = px(float(d))
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">10{SUP.format(d)}</text>')
    for d in range(-9, 2, 2):
        y = py(float(d))
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">'
                 f'10{SUP.format(d)}</text>')
    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">'
             f'<tspan font-style="italic">k</tspan> '
             f'<tspan font-style="italic">L</tspan>, '
             f'wavenumber in units of the outer scale</text>')
    s.append(f'<text x="{X0-46:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-46:.0f} {(Y0+Y1)/2:.0f})">'
             f'<tspan font-style="italic">E</tspan>('
             f'<tspan font-style="italic">k</tspan>), arbitrary units</text>')

    # The two exponents, anchored at the SAME point at k L = 1 so that the
    # comparison is of slopes and of nothing else.
    lx = np.linspace(0.0, DEC + 1.3, 600)
    cut = np.exp(-(10.0**(lx - DEC)))          # exponential at k eta ~ 1
    ly53 = -(5.0/3.0)*lx + np.log10(cut)
    ly2 = -2.0*lx
    m53 = ly53 > LY0
    m2 = (ly2 > LY0) & (lx <= DEC)
    s.append(f'<path d="{path(px(lx[m2]), py(ly2[m2]))}" fill="none" '
             f'stroke="{VIO}" stroke-width="2" stroke-dasharray="6 4"/>')
    s.append(f'<path d="{path(px(lx[m53]), py(ly53[m53]))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.4"/>')

    # the two bounding scales
    for lxv, col, lab, dy in ((0.0, ACC2, "stirring scale L", 0),
                              (DEC, ACC2, "dissipation scale", 0)):
        s.append(f'<line x1="{px(lxv):.1f}" y1="{Y0:.0f}" '
                 f'x2="{px(lxv):.1f}" y2="{Y1:.0f}" stroke="{ACC2}" '
                 f'stroke-width="1.2" stroke-dasharray="4 4"/>')
    s.append(f'<text x="{px(0.0)+6:.1f}" y="{Y0+16:.0f}" font-size="11" '
             f'fill="{ACC2}">energy in at '
             f'<tspan font-style="italic">L</tspan></text>')
    s.append(f'<text x="{px(DEC)-6:.1f}" y="{Y0+16:.0f}" font-size="11" '
             f'text-anchor="end" fill="{ACC2}">energy out at '
             f'<tspan font-style="italic">&#951;</tspan></text>')
    s.append(f'<text x="{(px(0.0)+px(DEC))/2:.1f}" y="{Y0+36:.0f}" '
             f'font-size="12" text-anchor="middle" fill="{FG}">'
             f'inertial range: {DEC:.0f} decades</text>')

    # Slope labels, placed by search against the drawn ink -- WHICH
    # INCLUDES THE TWO VERTICAL DASHED LINES.  Leaving them out was the
    # whole of the first failure here: the Burgers label sat on the
    # dissipation-scale line at k L = 10^4 and place_label had no way to
    # know, because that line was not in the array it tests against.
    vert = np.linspace(Y0, Y1, 120)
    ink = np.column_stack([
        np.concatenate([px(lx[m53]), px(lx[m2]),
                        np.full(len(vert), px(0.0)),
                        np.full(len(vert), px(DEC))]),
        np.concatenate([py(ly53[m53]), py(ly2[m2]), vert, vert])])
    occupied = []
    box = (X0 + 2, Y0 + 2, X1 - 2, Y1 - 2)
    leaders = []
    # The widths below are the RENDERED widths, 5.2 units per VISIBLE
    # character at font-size 11.5 -- not len() of the source string, which
    # counts "&#8733;" as seven characters and overstated the Burgers label
    # by half.  An overstated width makes every clear seat look occupied,
    # so the search falls through to a weaker pass and lands on a curve,
    # which is exactly what check_overlap then reports.
    # The preferred seat of each label is COMPUTED, not eyeballed: one sits
    # above the upper curve and one below the lower one, in the two regions
    # the power laws leave empty, and place_label still searches from
    # there.  The leader is drawn unconditionally, because both labels
    # stand off their curves by design; leader_svg returns '' when the
    # anchor is already inside the label box.
    #
    # Why not a bare search from each curve: a searched label's LEADER is
    # in neither `ink` nor `occupied`, so the second label's dotted leader
    # ran straight through the first label, and check_overlap reported the
    # first label as sitting on a dashed element.  Fixing the two seats
    # removes the interaction instead of chasing it.
    for lxv, ly, col, txt, wd, dx, dy in (
            (2.2, -(5.0/3.0)*2.2, ACC, "E &#8733; k^-5/3, Kolmogorov",
             109.0, 12.0, -12.0),
            (3.2, -2.0*3.2, VIO, "E &#8733; k^-2, Burgers",
             83.0, -95.0, 26.0)):
        ax_, ay_ = px(lxv), py(ly)
        x, y, _ = place_label([(ax_ + dx, ay_ + dy)], occupied, box,
                              wd, 13.0, ink=ink, window=None)
        label = txt.replace("^-5/3", SUP.format("&#8722;5/3")) \
                   .replace("^-2", SUP.format("&#8722;2"))
        s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="11.5" '
                 f'fill="{col}">{label}</text>')
        leaders.append(leader_svg(ax_, ay_, x, y, wd, 13.0))

    # the separation after one decade and after the whole band
    sep1 = 10.0**(2.0 - 5.0/3.0)
    sepd = 10.0**((2.0 - 5.0/3.0)*DEC)
    xd = px(DEC)
    s.append(f'<line x1="{xd:.1f}" y1="{py(-(5.0/3.0)*DEC):.1f}" '
             f'x2="{xd:.1f}" y2="{py(-2.0*DEC):.1f}" stroke="{FG}" '
             f'stroke-width="1.1"/>')
    # BELOW the foot of the separation bar, not beside its middle: beside
    # its middle is where the Burgers label's computed seat is, and two
    # texts on one another is a defect check_overlap cannot see, because
    # it tests labels against curves and not against each other.
    s.append(f'<text x="{xd-8:.1f}" y="{py(-2.0*DEC) + 16:.1f}" '
             f'font-size="11" text-anchor="end" fill="{FG}">'
             f'&#215;{sepd:.1f} here, &#215;{sep1:.2f} after one '
             f'decade</text>')
    s.extend(leaders)

    s.append('</svg>')
    open(out("m10_fig_cascade.svg"), "w", encoding="utf-8").write("\n".join(s))
    return RE_DRAWN, sep1, sepd


# =========================================================================
# Figure 2: the (Kn, Re) plane, and the domain the formula has left
# =========================================================================

def build_domain():
    W, H = 720, 430
    X0, X1, Y0, Y1 = 84.0, 636.0, 44.0, 344.0

    # LKN1 was 1.2, which put the solar-wind point 54 units from the
    # right edge and left its label nowhere to go but across the
    # Kn = 1/3 line.  2.2 gives it a seat beside its own point.
    LKN0, LKN1 = -8.0, 2.2          # log10 Kn
    LRE0, LRE1 = -1.2, 9.2          # log10 Re
    KN_FAIL = 1.0/3.0               # Chapman-Enskog failing beyond this

    def px(lk):
        return X0 + (lk - LKN0)/(LKN1 - LKN0)*(X1 - X0)

    def py(lr):
        return Y1 - (lr - LRE0)/(LRE1 - LRE0)*(Y1 - Y0)

    rows = fluid_rows()

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="A log-log plot of Reynolds number against '
         'Knudsen number. Four straight lines of slope minus one run from '
         'upper left to lower right, one for each value of the thermal '
         'Mach number, drawing Module 2 identity Reynolds number equals '
         'three times thermal Mach number divided by Knudsen number. The '
         'right-hand band, where the Knudsen number exceeds one third, is '
         'shaded red and labelled as the region where the Chapman-Enskog '
         'expansion is failing. Four points are plotted: laboratory air '
         'and a molecular cloud lie far to the left at high Reynolds '
         'number, well inside the valid region, while the intracluster '
         'medium and the solar wind lie inside the shaded band at '
         'Reynolds numbers of order one and ten." >' % (W, H)]

    # the region where the expansion is failing
    s.append(f'<rect x="{px(np.log10(KN_FAIL)):.1f}" y="{Y0:.0f}" '
             f'width="{X1-px(np.log10(KN_FAIL)):.1f}" height="{Y1-Y0:.0f}" '
             f'fill="#2a1414" opacity="0.85"/>')
    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    # The dashed boundary starts BELOW the two annotation lines at the
    # top: a dashed reference line running through its own caption is what
    # check_overlap reports, and rightly.
    s.append(f'<line x1="{px(np.log10(KN_FAIL)):.1f}" y1="{Y0+44:.0f}" '
             f'x2="{px(np.log10(KN_FAIL)):.1f}" y2="{Y1:.0f}" '
             f'stroke="{RED}" stroke-width="1.4" stroke-dasharray="5 4"/>')

    for d in range(-8, 3, 2):
        x = px(float(d))
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">'
                 f'10{SUP.format(d)}</text>')
    for d in range(0, 10, 2):
        y = py(float(d))
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">'
                 f'10{SUP.format(d)}</text>')
    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">Knudsen number '
             f'Kn = <tspan font-style="italic">&#955;</tspan>/'
             f'<tspan font-style="italic">L</tspan></text>')
    s.append(f'<text x="{X0-48:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-48:.0f} {(Y0+Y1)/2:.0f})">'
             f'Reynolds number Re</text>')

    ink = []
    occupied = []
    box = (X0 + 2, Y0 + 2, X1 - 2, Y1 - 2)
    leaders = []

    # Module 2's identity, as a family of lines of slope -1
    lk = np.linspace(LKN0, LKN1, 400)
    # Each line carries its label at its OWN x, spread left to right, so
    # the four read as a ladder instead of stacking in one corner.  The
    # first version anchored them all at the same Re and produced the
    # order 1, 0.1, 10, 0.01 down the left-hand edge, which invites the
    # reader to match the wrong label to the wrong line.
    FAMILY = ((0.01, "0.01", -7.0), (0.1, "0.1", -5.2),
              (1.0, "1", -3.4), (10.0, "10", -1.6))
    for Ma, lab, lk_lab in FAMILY:
        lr = np.log10(3.0*Ma) - lk
        m = (lr >= LRE0) & (lr <= LRE1)
        if not m.any():
            continue
        s.append(f'<path d="{path(px(lk[m]), py(lr[m]))}" fill="none" '
                 f'stroke="{RULE}" stroke-width="1.1"/>')
        ink.append(np.column_stack([px(lk[m]), py(lr[m])]))

    inkarr = np.vstack(ink) if ink else None   # kept for check_overlap parity

    # THE FOUR FLUIDS ARE DRAWN AND RESERVED FIRST.  The identity labels
    # are furniture; the points are the figure, and a point label pushed
    # aside by a piece of furniture is the Module 9 defect again.
    for lab, Kn, Re, Ma, col, hollow in rows:
        x, y = px(np.log10(Kn)), py(np.log10(Re))
        fill = BG if hollow else col
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.6" fill="{fill}" '
                 f'stroke="{col}" stroke-width="2"/>')
        occupied.append((x - 9, y - 9, x + 9, y + 9))

    for lab, Kn, Re, Ma, col, hollow in rows:
        ax_, ay_ = px(np.log10(Kn)), py(np.log10(Re))
        wd = 8.0 + 5.9*len(lab)
        # ink=None DELIBERATELY.  The identity lines are thin grey
        # furniture and the stylesheet puts a dark halo behind every
        # in-plot label, so demanding clearance from them pushed the air
        # label 150 px away -- on top of the CLOUD point, which is the
        # Module 9 defect exactly.  A label that sits beside its own point
        # and crosses a grey line is right; one that sits in clear space
        # beside somebody else's point is wrong.
        x, y, moved = place_label([(ax_ + 10, ay_ - 9), (ax_ + 10, ay_ + 20),
                                   (ax_ - wd - 10, ay_ - 9),
                                   (ax_ - wd - 10, ay_ + 20)],
                                  occupied, box, wd, 13.0, ink=None,
                                  window=60.0)
        s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="11.5" '
                 f'fill="{col}">{esc(lab)}</text>')
        if moved:
            leaders.append(leader_svg(ax_, ay_, x, y, wd, 13.0))

    # now the identity labels, in whatever room the points have left
    for Ma, lab, lk_lab in FAMILY:
        lr_lab = np.log10(3.0*Ma) - lk_lab
        if not (LRE0 <= lr_lab <= LRE1):
            continue
        ax_, ay_ = px(lk_lab), py(lr_lab)
        txt = f'Ma~T~ = {lab}'
        wd = 8.0 + 6.2*len(txt)
        x, y, moved = place_label([(ax_ + 6, ay_ - 6), (ax_ - wd - 6, ay_ + 15)],
                                  occupied, box, wd, 13.0, ink=None,
                                  window=70.0)
        s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="10.5" '
                 f'fill="{MUT}">'
                 f'{txt.replace("~T~", SUB.format("th"))}</text>')
        if moved:
            leaders.append(leader_svg(ax_, ay_, x, y, wd, 13.0))

    s.append(f'<text x="{X0+8:.0f}" y="{Y1-34:.0f}" font-size="11" '
             f'fill="{MUT}">grey lines: Module 2&#8217;s identity '
             f'Re = 3&#8201;Ma{SUB.format("th")}/Kn</text>')
    s.append(f'<text x="{X1-8:.0f}" y="{Y0+18:.0f}" font-size="11.5" '
             f'text-anchor="end" fill="{RED}">Kn &#8805; 1/3: no '
             f'Navier&#8211;Stokes viscosity exists</text>')
    s.append(f'<text x="{X1-8:.0f}" y="{Y0+34:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{MUT}">the Chapman&#8211;Enskog '
             f'expansion of Module 1 is failing here</text>')

    # the open-marker key, reserved as occupied so no label lands on it
    kx, ky = X0 + 10, Y1 - 14
    s.append(f'<circle cx="{kx+6:.0f}" cy="{ky-4:.0f}" r="5.6" fill="{BG}" '
             f'stroke="{YEL}" stroke-width="2"/>')
    s.append(f'<text x="{kx+18:.0f}" y="{ky:.0f}" font-size="10.5" '
             f'fill="{MUT}">open marker: Re from the MEASURED '
             f'<tspan font-style="italic">&#957;</tspan>, not from '
             f'<tspan font-style="italic">&#955;</tspan>'
             f'<tspan font-style="italic">v&#772;</tspan>/3</text>')
    s.extend(leaders)

    s.append('</svg>')
    open(out("m10_fig_domain.svg"), "w", encoding="utf-8").write("\n".join(s))
    return rows


# =========================================================================
# Figure 3: Podesta's eight indices, THE ANCHOR
# =========================================================================

def build_podesta():
    W, H = 720, 400
    X0, X1, Y0, Y1 = 84.0, 616.0, 46.0, 316.0
    YMIN, YMAX = 1.44, 1.80

    def py(v):
        return Y1 - (v - YMIN)/(YMAX - YMIN)*(Y1 - Y0)

    n = len(M.PODESTA)
    slot = (X1 - X0)/n

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Eight measured spectral indices plotted '
         'against interval number, one to four. For each interval an '
         'orange point shows the magnetic index and a teal point the '
         'velocity index, each with a vertical ninety-nine per cent '
         'confidence bar. A horizontal line at five thirds and another at '
         'three halves cross the plot. The four magnetic points scatter '
         'around the five thirds line, one clearly above it and one '
         'clearly below. All four velocity points lie below the five '
         'thirds line and near the three halves line." >' % (W, H)]

    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for v in (1.45, 1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80):
        y = py(v)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.2f}</text>')

    # the two predictions
    # Both prediction lines are drawn in the neutral foreground grey.
    # Orange means magnetic and teal means velocity everywhere in this
    # figure, and a prediction line in either colour would claim a
    # membership it does not have.
    # The labels are the BARE fractions.  Spelled out, "3/2,
    # Iroshnikov-Kraichnan" is 140 units wide and lands on interval 4's
    # velocity point; the names belong in the caption, where there is room
    # for them and for what each prediction assumes.
    for v, col, lab in ((5.0/3.0, FG, "5/3"), (1.5, FG, "3/2")):
        y = py(v)
        s.append(f'<line x1="{X0:.0f}" y1="{y:.1f}" x2="{X1:.0f}" '
                 f'y2="{y:.1f}" stroke="{col}" stroke-width="1.3" '
                 f'stroke-dasharray="6 4"/>')
        s.append(f'<text x="{X1-6:.0f}" y="{y-6:.1f}" font-size="11" '
                 f'text-anchor="end" fill="{col}">{lab}</text>')

    # PODESTA rows are (interval, start, days, magnetic, dB, velocity, dV,
    # kinetic, dK, total, dE, Alfven-ratio range).
    mags = [row[3] for row in M.PODESTA]
    magerr = [row[4] for row in M.PODESTA]
    vels = [row[5] for row in M.PODESTA]
    velerr = [row[6] for row in M.PODESTA]

    for i in range(n):
        xc = X0 + (i + 0.5)*slot
        s.append(f'<text x="{xc:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">interval {i+1}</text>')
        for dx, val, err, col in ((-11.0, mags[i], magerr[i], ACC),
                                  (+11.0, vels[i], velerr[i], ACC2)):
            x = xc + dx
            ylo, yhi = py(val - err), py(val + err)
            s.append(f'<line x1="{x:.1f}" y1="{ylo:.1f}" x2="{x:.1f}" '
                     f'y2="{yhi:.1f}" stroke="{col}" stroke-width="1.6"/>')
            for yy in (ylo, yhi):
                s.append(f'<line x1="{x-4:.1f}" y1="{yy:.1f}" '
                         f'x2="{x+4:.1f}" y2="{yy:.1f}" stroke="{col}" '
                         f'stroke-width="1.6"/>')
            s.append(f'<circle cx="{x:.1f}" cy="{py(val):.1f}" r="4.2" '
                     f'fill="{col}"/>')

    # the two means, drawn as short bars at the right-hand edge
    mmean, vmean = float(np.mean(mags)), float(np.mean(vels))
    for val, col, lab in ((mmean, ACC, "magnetic mean"),
                          (vmean, ACC2, "velocity mean")):
        y = py(val)
        s.append(f'<line x1="{X0+4:.0f}" y1="{y:.1f}" x2="{X1-4:.0f}" '
                 f'y2="{y:.1f}" stroke="{col}" stroke-width="0.9" '
                 f'stroke-dasharray="2 5" opacity="0.9"/>')
        # BELOW its own line: above it, the magnetic mean label sits on
        # the 5/3 line it is being compared with.
        s.append(f'<text x="{X0+8:.0f}" y="{y+13:.1f}" font-size="10.5" '
                 f'fill="{col}">{lab} {val:.4f}</text>')

    s.append(f'<text x="{X0-52:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-52:.0f} {(Y0+Y1)/2:.0f})">'
             f'spectral index of '
             f'<tspan font-style="italic">P</tspan>('
             f'<tspan font-style="italic">f</tspan>)</text>')
    s.append(f'<circle cx="{X0+120:.0f}" cy="{Y1+34:.0f}" r="4.2" '
             f'fill="{ACC}"/>')
    s.append(f'<text x="{X0+130:.0f}" y="{Y1+38:.0f}" font-size="11" '
             f'fill="{ACC}">magnetic</text>')
    s.append(f'<circle cx="{X0+220:.0f}" cy="{Y1+34:.0f}" r="4.2" '
             f'fill="{ACC2}"/>')
    s.append(f'<text x="{X0+230:.0f}" y="{Y1+38:.0f}" font-size="11" '
             f'fill="{ACC2}">velocity</text>')
    s.append(f'<text x="{X0+300:.0f}" y="{Y1+38:.0f}" font-size="10.5" '
             f'fill="{MUT}">bars are 99 per cent confidence limits; '
             f'divide by 2.576 for one &#963;</text>')

    s.append('</svg>')
    open(out("m10_fig_podesta.svg"), "w", encoding="utf-8").write("\n".join(s))
    return mmean, vmean


# =========================================================================
# Figure 4: the log-normal PDF, and the tail that forcing moves
# =========================================================================

def build_pdf():
    W, H = 720, 470
    X0, X1 = 86.0, 656.0
    YA0, YA1 = 44.0, 236.0          # upper panel, linear
    YB0, YB1 = 288.0, 420.0         # lower panel, logarithmic

    MACH = 10.0
    THRESH = 100.0                  # rho/<rho>
    SMIN, SMAX = -9.0, 6.6

    cases = [(M.FED_B_SOLENOIDAL, ACC2, "b = 1/3, solenoidal"),
             (M.FED_B_COMPRESSIVE, ACC, "b = 1, compressive")]

    sg = [M.lognormal_sigma_s(b, MACH) for b, _, _ in cases]
    s0 = [M.lognormal_peak_s(v) for v in sg]
    tails = [M.volume_fraction_above(THRESH, v) for v in sg]

    ss = np.linspace(SMIN, SMAX, 900)
    pdfs = [np.exp(-(ss - m)**2/(2.0*w*w))/(w*np.sqrt(2.0*np.pi))
            for w, m in zip(sg, s0)]
    PMAX = max(p.max() for p in pdfs)*1.12
    LPMIN, LPMAX = -7.0, np.log10(PMAX)

    def px(v):
        return X0 + (v - SMIN)/(SMAX - SMIN)*(X1 - X0)

    def pya(p):
        return YA1 - p/PMAX*(YA1 - YA0)

    def pyb(p):
        lp = np.log10(np.maximum(p, 10.0**LPMIN))
        return YB1 - (lp - LPMIN)/(LPMAX - LPMIN)*(YB1 - YB0)

    xt = px(np.log(THRESH))

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Two stacked panels sharing a horizontal '
         'axis of s, the natural logarithm of density divided by mean '
         'density. The upper panel is linear and shows two bell curves, a '
         'narrow teal one for solenoidal forcing and a wider orange one '
         'for compressive forcing, both centred left of zero. The lower '
         'panel plots the same two curves on a logarithmic vertical axis, '
         'where the orange curve lies well above the teal one in the far '
         'right tail. A vertical line marks the threshold where the '
         'density is one hundred times the mean, and the area beyond it '
         'is shaded in both panels." >' % (W, H)]

    for (Y0, Y1) in ((YA0, YA1), (YB0, YB1)):
        s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
                 f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
                 f'stroke-width="1"/>')

    # the tail, shaded in both panels, before the curves are drawn
    for (Y0, Y1) in ((YA0, YA1), (YB0, YB1)):
        s.append(f'<rect x="{xt:.1f}" y="{Y0:.0f}" width="{X1-xt:.1f}" '
                 f'height="{Y1-Y0:.0f}" fill="#2a2410" opacity="0.7"/>')
        s.append(f'<line x1="{xt:.1f}" y1="{Y0:.0f}" x2="{xt:.1f}" '
                 f'y2="{Y1:.0f}" stroke="{YEL}" stroke-width="1.3" '
                 f'stroke-dasharray="5 4"/>')

    for sv in range(-8, 7, 2):
        x = px(float(sv))
        s.append(f'<line x1="{x:.1f}" y1="{YB1:.0f}" x2="{x:.1f}" '
                 f'y2="{YB1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{YB1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{sv}</text>')
    for pv in (0.0, 0.1, 0.2):
        y = pya(pv)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{pv:.1f}</text>')
    for d in (-6, -4, -2, 0):
        y = pyb(10.0**d)
        if y < YB0 or y > YB1:
            continue
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{X0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">'
                 f'10{SUP.format(d)}</text>')

    for i, (w, m, (b, col, lab)) in enumerate(zip(sg, s0, cases)):
        p = pdfs[i]
        s.append(f'<path d="{path(px(ss), pya(p))}" fill="none" '
                 f'stroke="{col}" stroke-width="2.2"/>')
        mb = p > 10.0**LPMIN
        s.append(f'<path d="{path(px(ss[mb]), pyb(p[mb]))}" fill="none" '
                 f'stroke="{col}" stroke-width="2.2"/>')

    # the key, identical in both panels because it belongs to the figure
    for i, (b, col, lab) in enumerate(cases):
        s.append(f'<text x="{X0+10:.0f}" y="{YA0+18+18*i:.0f}" '
                 f'font-size="11.5" fill="{col}">{esc(lab)}, '
                 f'&#963;~s~ = {sg[i]:.4f}'
                 .replace("~s~", SUB.format("s")) + '</text>')
    s.append(f'<text x="{X0+10:.0f}" y="{YB1-9:.0f}" font-size="11" '
             f'fill="{MUT}">same two curves, logarithmic axis: the tail '
             f'is where the difference lives</text>')

    s.append(f'<text x="{xt+6:.1f}" y="{YA0+18:.0f}" font-size="11" '
             f'fill="{YEL}">&#961; &gt; 100&#8202;&#10216;&#961;&#10217;'
             f'</text>')
    s.append(f'<text x="{xt-8:.1f}" y="{YB0+20:.0f}" font-size="11" '
             f'text-anchor="end" fill="{YEL}">volume beyond the line: '
             f'{tails[1]*1e4:.2f}&#215;10{SUP.format("&#8722;4")} against '
             f'{tails[0]*1e4:.2f}&#215;10{SUP.format("&#8722;4")}, '
             f'a factor {tails[1]/tails[0]:.1f}</text>')

    s.append(f'<text x="{(X0+X1)/2:.0f}" y="{YB1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">'
             f'<tspan font-style="italic">s</tspan> = ln('
             f'<tspan font-style="italic">&#961;</tspan>/'
             f'&#10216;<tspan font-style="italic">&#961;</tspan>&#10217;)'
             f', at Mach 10</text>')
    s.append(f'<text x="{X0-48:.0f}" y="{(YA0+YA1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-48:.0f} {(YA0+YA1)/2:.0f})">'
             f'<tspan font-style="italic">p</tspan>('
             f'<tspan font-style="italic">s</tspan>)</text>')
    s.append(f'<text x="{X0-48:.0f}" y="{(YB0+YB1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {X0-48:.0f} {(YB0+YB1)/2:.0f})">'
             f'<tspan font-style="italic">p</tspan>('
             f'<tspan font-style="italic">s</tspan>)</text>')

    s.append('</svg>')
    open(out("m10_fig_pdf.svg"), "w", encoding="utf-8").write("\n".join(s))
    return sg, s0, tails


if __name__ == '__main__':
    re_drawn, sep1, sepd = build_cascade()
    print(f"m10_fig_cascade.svg   inertial band implies Re = {re_drawn:.3g}; "
          f"5/3 against 2 separate by {sep1:.3f} per decade, {sepd:.1f} "
          f"over the band")
    rows = build_domain()
    for lab, Kn, Re, Ma, col, hollow in rows:
        print(f"m10_fig_domain.svg    {lab:<28} Kn = {Kn:.3e}  "
              f"Re = {Re:.3e}  Ma_th = {Ma:.4f}"
              f"{'   (measured nu)' if hollow else ''}")
    mmean, vmean = build_podesta()
    print(f"m10_fig_podesta.svg   magnetic mean {mmean:.4f}, "
          f"velocity mean {vmean:.4f}")
    sg, s0, tails = build_pdf()
    print(f"m10_fig_pdf.svg       sigma_s {sg[0]:.4f} and {sg[1]:.4f} "
          f"(ratio {sg[1]/sg[0]:.2f}); tails {tails[0]:.3e} and "
          f"{tails[1]:.3e} (ratio {tails[1]/tails[0]:.1f})")
