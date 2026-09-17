"""Build the computed SVG figures for Module 3.

Writes three files:

  m03_fig_atmos.svg   the terrestrial troposphere as a polytrope.  Two
                      panels, T(z) and P(z)/P0, each carrying three curves:
                      isothermal (n infinite), the International Standard
                      Atmosphere (n = 4.256), and the dry adiabat (n = 2.5).
                      The point of the figure is the GAP between the middle
                      curve and the dry adiabat, which is latent heat.

  m03_fig_lane.svg    the Lane-Emden solutions.  Upper panel theta(xi) for
                      n = 0, 1, 3/2, 3, 4, 5, showing the surface running
                      out to infinity as n approaches 5.  Lower panel the
                      density profiles rho/rho_c against r/R for n = 3/2
                      and n = 3, drawn against the tabulated solar profile,
                      which is the factor-of-two failure made visible.

  m03_fig_index.svg   THE ANCHOR FIGURE.  Upper panel the effective
                      polytropic index n_eff(r) read off the standard solar
                      model, against the two predicted values 3/2 and 3.
                      Lower panel a zoom on the convection-zone base in the
                      variable that locates it, grad = d ln T / d ln P,
                      carrying the model's boundary and the helioseismic
                      measurement with its error bar.

Geometry is computed, never eyeballed.  Every number drawn is produced by
m03_numbers.py, so a figure cannot drift away from the prose.

Two Module 1 and Module 2 lessons are applied here.  Labels are placed by
arithmetic and kept inside the plot box, because check_overlap reads
geometry rather than pixels and a label that strays hits the tick text.
And where agreement is the thing being shown, the panel shows the
residual or a zoom, not the raw quantity: the whole content of the lower
panel of m03_fig_index.svg is a gap of 0.015 in r/R, which is invisible on
a full-radius axis.
"""
import numpy as np

import m03_numbers as M

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"
BLU, PNK = "#60a5fa", "#f472b6"


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# =========================================================================
# Figure: the terrestrial troposphere as a polytrope
# =========================================================================

def build_atmos():
    W, H = 760, 400
    # panel A, temperature; panel B, pressure
    AX0, AX1, AY0, AY1 = 78.0, 360.0, 52.0, 300.0
    BX0, BX1, BY0, BY1 = 452.0, 734.0, 52.0, 300.0
    ZMAX = 11.0                                  # km
    T0, TMIN = M.ISA_T0, 175.0
    PMIN, PMAX = 0.15, 1.0

    n_isa = M.polytrope_index_from_lapse(M.ISA_LAPSE, M.mu_air, M.g_earth)
    lapse_dry = M.lapse_adiabatic(1.4, M.mu_air, M.g_earth)
    n_dry = M.polytrope_index_from_lapse(lapse_dry, M.mu_air, M.g_earth)
    Hiso = M.scale_height(T0, M.mu_air, M.g_earth)/1e5      # km

    z = np.linspace(0.0, ZMAX, 200)
    T_iso = np.full_like(z, T0)
    T_isa = T0 - M.ISA_LAPSE*1e5*z
    T_dry = T0 - lapse_dry*1e5*z
    P_iso = np.exp(-z/Hiso)
    P_isa = (T_isa/T0)**(n_isa + 1.0)
    P_dry = (T_dry/T0)**(n_dry + 1.0)

    def ax(t):
        return AX0 + (t-TMIN)/(T0+4.0-TMIN)*(AX1-AX0)

    def ay(zz):
        return AY1 - zz/ZMAX*(AY1-AY0)

    def bx(p):
        return BX0 + (p-PMIN)/(PMAX-PMIN)*(BX1-BX0)

    def by(zz):
        return BY1 - zz/ZMAX*(BY1-BY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Left panel: temperature against altitude '
         f'from sea level to 11 kilometres for three hydrostatic '
         f'atmospheres, an isothermal one, the International Standard '
         f'Atmosphere, and a dry adiabat. Right panel: the pressure of the '
         f'same three atmospheres divided by its sea-level value. The '
         f'standard atmosphere lies between the other two, and the gap '
         f'between it and the dry adiabat is the effect of latent heat.">']

    # ---------------- panel A ----------------
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-24:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Temperature</text>')
    s.append(f'<rect x="{AX0:.0f}" y="{AY0:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for t in (180, 200, 220, 240, 260, 280):
        x = ax(t)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t}</text>')
    for zz in (0, 2, 4, 6, 8, 10):
        y = ay(zz)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{y:.1f}" x2="{AX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{AX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{zz}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">T / K</text>')
    s.append(f'<text x="{AX0-46:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {AX0-46:.0f} {(AY0+AY1)/2:.0f})">'
             f'altitude z / km</text>')

    s.append(f'<path d="{path(ax(T_iso), ay(z))}" fill="none" '
             f'stroke="{MUT}" stroke-width="1.8" stroke-dasharray="4 3"/>')
    s.append(f'<path d="{path(ax(T_dry), ay(z))}" fill="none" '
             f'stroke="{ACC2}" stroke-width="2.2"/>')
    s.append(f'<path d="{path(ax(T_isa), ay(z))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.6"/>')
    # the gap between standard atmosphere and dry adiabat, at 11 km
    s.append(f'<line x1="{ax(T_dry[-1]):.1f}" y1="{ay(ZMAX)+1:.1f}" '
             f'x2="{ax(T_isa[-1]):.1f}" y2="{ay(ZMAX)+1:.1f}" '
             f'stroke="{YEL}" stroke-width="2.5"/>')
    s.append(f'<text x="{(ax(T_dry[-1])+ax(T_isa[-1]))/2:.1f}" '
             f'y="{ay(ZMAX)+18:.1f}" font-size="10.5" text-anchor="middle" '
             f'fill="{YEL}">{T_isa[-1]-T_dry[-1]:.0f} K</text>')

    # The legend goes in the bottom-left corner of the box.  Every curve
    # runs towards T(0) at z = 0, so the cold, low-altitude corner is the
    # only region of panel A no curve enters: at z = 1.9 km the coldest
    # curve, the dry adiabat, is still at 270 K, which is x = 306.
    # Page CSS sets the fill of every figure label, so colour alone cannot
    # key the legend; each entry carries a line swatch in its curve's style.
    for k, (col, dash, lab) in enumerate((
            (MUT, ' stroke-dasharray="4 3"', 'isothermal, n → ∞'),
            (ACC, '', f'standard atmosphere, n = {n_isa:.2f}'),
            (ACC2, '', f'dry adiabat, n = {n_dry:.2f}'))):
        y = AY1 - 42 + 16*k
        s.append(f'<line x1="{AX0+10:.0f}" y1="{y-4:.0f}" '
                 f'x2="{AX0+36:.0f}" y2="{y-4:.0f}" stroke="{col}" '
                 f'stroke-width="2.4"{dash}/>')
        s.append(f'<text x="{AX0+44:.0f}" y="{y:.0f}" font-size="10.5" '
                 f'fill="{col}">{lab}</text>')

    # ---------------- panel B ----------------
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-24:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Pressure</text>')
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" width="{BX1-BX0:.0f}" '
             f'height="{BY1-BY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for p in (0.2, 0.4, 0.6, 0.8, 1.0):
        x = bx(p)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{p:.1f}</text>')
    for zz in (0, 2, 4, 6, 8, 10):
        y = by(zz)
        s.append(f'<line x1="{BX0-5:.0f}" y1="{y:.1f}" x2="{BX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{BX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{zz}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">P / P(0)</text>')

    s.append(f'<path d="{path(bx(P_iso), by(z))}" fill="none" '
             f'stroke="{MUT}" stroke-width="1.8" stroke-dasharray="4 3"/>')
    s.append(f'<path d="{path(bx(P_dry), by(z))}" fill="none" '
             f'stroke="{ACC2}" stroke-width="2.2"/>')
    s.append(f'<path d="{path(bx(P_isa), by(z))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.6"/>')
    # mark the tabulated tropopause point, which the n = 4.256 curve must hit
    xt, yt = bx(M.ISA_P_TROP/M.ISA_P0), by(11.0)
    s.append(f'<circle cx="{xt:.1f}" cy="{yt:.1f}" r="4.5" fill="none" '
             f'stroke="{YEL}" stroke-width="2"/>')
    # All three curves crowd the top-left of panel B, so the annotations sit
    # against the right edge, where the rightmost curve at this height is
    # the isothermal one at x = 502, clear of text that starts at 629.
    # An L-shaped leader, down then across.  A straight one from the circle
    # to the label passes through the "polytropic curves" row above it.
    s.append(f'<path d="M {xt:.1f},{yt+7:.1f} L {xt:.1f},{BY0+32:.0f} '
             f'L {BX1-112:.1f},{BY0+32:.0f}" fill="none" stroke="{YEL}" '
             f'stroke-width="1"/>')
    s.append(f'<text x="{BX1-10:.0f}" y="{BY0+36:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{YEL}">tabulated: '
             f'{M.ISA_P_TROP/1e3:.0f} hPa</text>')
    s.append(f'<text x="{BX1-10:.0f}" y="{BY0+18:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{MUT}">polytropic curves: '
             f'P = P(0) (T/T(0))ⁿ⁺¹</text>')

    s.append(f'<text x="{AX0-46:.0f}" y="{H-12:.0f}" font-size="10.5" '
             f'fill="{MUT}">Standard atmosphere: ISO 2533 / US Standard '
             f'Atmosphere 1976, defined by T(0) = {M.ISA_T0} K, '
             f'P(0) = {M.ISA_P0/1e6:.5f} bar and a lapse rate of '
             f'{M.ISA_LAPSE*1e5:.1f} K/km.</text>')
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure: the Lane-Emden solutions and the solar density profile
# =========================================================================

def build_lane():
    W, H = 760, 660
    AX0, AX1, AY0, AY1 = 78.0, 700.0, 54.0, 270.0     # theta(xi)
    BX0, BX1, BY0, BY1 = 78.0, 700.0, 374.0, 570.0    # rho/rho_c vs r/R
    XIMAX = 15.5

    def ax(xi):
        return AX0 + xi/XIMAX*(AX1-AX0)

    def ay(th):
        return AY1 - th*(AY1-AY0)

    def bx(r):
        return BX0 + r*(BX1-BX0)

    def by(v):
        # log10 of rho/rho_c, from 0 down to -5
        return BY0 + (0.0 - v)/5.0*(BY1-BY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper panel: the Lane-Emden function '
         f'theta against the dimensionless radius xi for polytropic indices '
         f'0, 1, one and a half, 3, 4 and 5. The first zero moves outward as '
         f'the index rises and runs to infinity at index 5. Lower panel: '
         f'density divided by central density against fractional radius, on '
         f'a logarithmic scale, for the index three-halves and index three '
         f'polytropes and for the tabulated standard solar model. The solar '
         f'profile falls faster than either polytrope.">']

    # ---------------- panel A ----------------
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-26:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Solutions of the Lane–Emden '
             f'equation θ″ + (2/ξ)θ′ + θⁿ = 0</text>')
    s.append(f'<rect x="{AX0:.0f}" y="{AY0:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    s.append(f'<line x1="{AX0:.0f}" y1="{ay(0.0):.1f}" x2="{AX1:.0f}" '
             f'y2="{ay(0.0):.1f}" stroke="{RULE}" stroke-width="1"/>')
    for t in (0, 2, 4, 6, 8, 10, 12, 14):
        x = ax(t)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t}</text>')
    for v in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = ay(v)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{y:.1f}" x2="{AX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{AX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.2f}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">ξ</text>')
    s.append(f'<text x="{AX0-44:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {AX0-44:.0f} {(AY0+AY1)/2:.0f})">'
             f'θ(ξ)</text>')

    # Curves.  The six solutions crowd together at small xi — at theta =
    # 0.25 the n = 0, 1 and 3/2 curves are 14 px apart, narrower than any
    # label — so inline labels are impossible here and the figure carries a
    # legend instead.  That forces one colour per index: n = 3/2 and n = 3
    # keep the colours they have in panel B, and the other four take
    # distinct ones.  The legend block sits in the upper right, where the
    # highest curve at x = 452 is the n = 5 tail at y = 230, eighty pixels
    # below the lowest legend row.
    curves = [(0.0, BLU), (1.0, PNK), (1.5, ACC2),
              (3.0, ACC), (4.0, VIO), (5.0, MUT)]
    for n, col in curves:
        xi, th, _unused = M.lane_emden(n, xi_max=XIMAX)
        keep = th > 0.0
        xi, th = xi[keep], th[keep]
        # decimate for drawing only; the full array set the geometry above
        step = max(1, len(xi)//400)
        w = 2.6 if n in (1.5, 3.0) else 1.8
        dash = ' stroke-dasharray="5 3"' if n == 5.0 else ''
        s.append(f'<path d="{path(ax(xi[::step]), ay(th[::step]))}" '
                 f'fill="none" stroke="{col}" stroke-width="{w}"{dash}/>')
        # marker at the surface, where there is one
        if th[-1] < 5e-3 and n < 5.0:
            s.append(f'<circle cx="{ax(xi[-1]):.1f}" cy="{ay(0.0):.1f}" '
                     f'r="3.4" fill="{col}"/>')

    c3 = M.polytrope_constants(3.0)
    c15 = M.polytrope_constants(1.5)
    LGX = 452.0
    for k, (n, col) in enumerate(curves):
        y = AY0 + 16.0 + 16.0*k
        dash = ' stroke-dasharray="5 3"' if n == 5.0 else ''
        s.append(f'<line x1="{LGX:.0f}" y1="{y-4:.0f}" x2="{LGX+26:.0f}" '
                 f'y2="{y-4:.0f}" stroke="{col}" stroke-width="2.4"{dash}/>')
        name = "n = 3/2" if n == 1.5 else f"n = {n:g}"
        tail = ("no surface" if n == 5.0
                else f'ξ₁ = {M.polytrope_constants(n)["xi1"]:.3f}')
        s.append(f'<text x="{LGX+34:.0f}" y="{y:.0f}" font-size="10.5" '
                 f'fill="{col}">{name}, {tail}</text>')
    s.append(f'<text x="{AX1-10:.0f}" y="{AY0+126:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{MUT}">filled dot: the surface ξ₁, '
             f'the first zero of θ</text>')
    s.append(f'<text x="{AX1-10:.0f}" y="{AY0+142:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{MUT}">n = 5 has none: finite mass, '
             f'infinite radius</text>')

    # ---------------- panel B ----------------
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-26:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The same solutions as '
             f'density profiles, against the Sun</text>')
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" width="{BX1-BX0:.0f}" '
             f'height="{BY1-BY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        x = bx(t)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t:.1f}</text>')
    for v in (0, -1, -2, -3, -4, -5):
        y = by(v)
        s.append(f'<line x1="{BX0-5:.0f}" y1="{y:.1f}" x2="{BX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        lab = "1" if v == 0 else f"10{'⁻' + '¹²³⁴⁵'[abs(v)-1]}"
        s.append(f'<text x="{BX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{lab}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">r / R</text>')
    s.append(f'<text x="{BX0-44:.0f}" y="{(BY0+BY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {BX0-44:.0f} {(BY0+BY1)/2:.0f})">'
             f'ρ / ρ<tspan baseline-shift="sub" font-size="8">c</tspan></text>')

    # The axis floor is rho/rho_c = 1e-5.  Clip the POINT LISTS there rather
    # than clipping the drawing: check_overlap reads geometry, so a path that
    # leaves the box still occupies the coordinates it was given.
    FLOOR = 1e-5
    for n, col, lab in ((1.5, ACC2, "n = 3/2"), (3.0, ACC, "n = 3")):
        xi, th, _ = M.lane_emden(n)
        cc = M.polytrope_constants(n)
        pos = th > 0.0
        xi, th = xi[pos], th[pos]
        keep = th**n >= FLOOR
        rr, dd = xi[keep]/cc["xi1"], th[keep]**n
        step = max(1, len(rr)//400)
        idx = np.r_[np.arange(0, len(rr), step), len(rr)-1]
        s.append(f'<path d="{path(bx(rr[idx]), by(np.log10(dd[idx])))}" '
                 f'fill="none" stroke="{col}" stroke-width="2.4"/>')

    ssm = M.load_ssm()
    keep = ssm["rho"]/ssm["rho"][0] >= FLOOR
    rr = ssm["rfrac"][keep]
    dd = np.log10(ssm["rho"][keep]/ssm["rho"][0])
    step = max(1, len(rr)//500)
    s.append(f'<path d="{path(bx(rr[::step]), by(dd[::step]))}" fill="none" '
             f'stroke="{YEL}" stroke-width="2.8"/>')

    # The Sun and the n = 3 polytrope run within six pixels of each other
    # from r = 0.3 to r = 0.75 — which is the point of the panel — so no
    # inline label can be attached to either without ambiguity, and all
    # three curves are too steep for a horizontal label to stay clear of
    # them.  A legend goes in the region under the curves and above the
    # two note lines, where the lowest curve at x = 250 is still at y = 410.
    LGX, LGY = BX0 + 10.0, BY0 + 96.0
    for k, (col, lab) in enumerate(((ACC2, "n = 3/2 polytrope"),
                                    (ACC, "n = 3 polytrope"),
                                    (YEL, "tabulated solar model"))):
        y = LGY + 16.0*k
        s.append(f'<line x1="{LGX:.0f}" y1="{y-4:.0f}" x2="{LGX+26:.0f}" '
                 f'y2="{y-4:.0f}" stroke="{col}" stroke-width="2.4"/>')
        s.append(f'<text x="{LGX+34:.0f}" y="{y:.0f}" font-size="10.5" '
                 f'fill="{col}">{lab}</text>')

    rhobar = 3.0*M.Msun/(4.0*np.pi*M.RSUN_TAB**3)
    s.append(f'<text x="{BX0+10:.0f}" y="{BY1-30:.0f}" font-size="10.5" '
             f'fill="{FG}">ρ<tspan baseline-shift="sub" font-size="8">c</tspan>/ρ̄ : {ssm["rho"][0]/rhobar:.1f} tabulated, '
             f'{c3["D"]:.1f} for n = 3, {c15["D"]:.1f} for n = 3/2</text>')
    s.append(f'<text x="{BX0+10:.0f}" y="{BY1-14:.0f}" font-size="10.5" '
             f'fill="{MUT}">the Sun is more centrally condensed than either '
             f'polytrope, by a factor {(ssm["rho"][0]/rhobar)/c3["D"]:.2f} '
             f'on n = 3</text>')

    # Two lines: on one it overran the 760-unit viewBox and was cut off, and
    # it sat on the "r / R" axis title at BY1 + 36.
    s.append(f'<text x="{BX0-44:.0f}" y="{H-28:.0f}" font-size="10.5" '
             f'fill="{MUT}">Solar profile: BS2005-AGS,OP, Bahcall, Serenelli '
             f'&amp; Basu (2005), ApJ 621, L85.</text>')
    s.append(f'<text x="{BX0-44:.0f}" y="{H-12:.0f}" font-size="10.5" '
             f'fill="{MUT}">Polytropes integrated numerically and '
             f'checked against the exact n = 0, 1 and 5 solutions.</text>')
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure: the effective polytropic index, and the convection-zone base
# =========================================================================

def build_index():
    W, H = 760, 660
    AX0, AX1, AY0, AY1 = 84.0, 700.0, 56.0, 288.0
    BX0, BX1, BY0, BY1 = 84.0, 700.0, 392.0, 566.0

    ssm = M.load_ssm()
    grad, neff = M.effective_polytropic_index(ssm, half=25)
    rb, plateau, n_plateau = M.convection_zone_base(ssm, grad)
    r = ssm["rfrac"]

    NLO, NHI = 1.0, 4.6
    # The zoom window is centred on the two boundaries rather than started
    # at one of them: with RLO = 0.700 the measured value sat 22% across the
    # panel and its label ran off the left edge into the tick numbers.
    RLO, RHI = 0.695, 0.745
    GLO, GHI = 0.26, 0.42

    def ax(x):
        return AX0 + x*(AX1-AX0)

    def ay(v):
        return AY1 - (v-NLO)/(NHI-NLO)*(AY1-AY0)

    def bx(x):
        return BX0 + (x-RLO)/(RHI-RLO)*(BX1-BX0)

    def by(v):
        return BY1 - (v-GLO)/(GHI-GLO)*(BY1-BY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper panel: the effective polytropic '
         f'index read off a standard solar model, against fractional '
         f'radius. It sits near two in the burning core, rises to a maximum '
         f'above four near the middle of the radiative interior, then drops '
         f'to a flat plateau at one and a half through the convection zone. '
         f'Horizontal lines mark the predicted values three-halves and '
         f'three. Lower panel: a zoom on the convection-zone base in the '
         f'logarithmic temperature gradient, showing the model boundary at '
         f'0.728 of the solar radius and the helioseismic measurement at '
         f'0.7133 with an error bar far smaller than the gap between '
         f'them.">']

    # ---------------- panel A ----------------
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-28:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The polytropic index the Sun '
             f'actually has</text>')
    s.append(f'<rect x="{AX0:.0f}" y="{AY0:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    # the convective envelope, shaded
    s.append(f'<rect x="{ax(rb):.1f}" y="{AY0:.0f}" '
             f'width="{AX1-ax(rb):.1f}" height="{AY1-AY0:.0f}" '
             f'fill="{ACC2}" fill-opacity="0.08"/>')
    for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        x = ax(t)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t:.1f}</text>')
    for v in (1, 2, 3, 4):
        y = ay(v)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{y:.1f}" x2="{AX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{AX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">r / R</text>')
    s.append(f'<text x="{AX0-46:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {AX0-46:.0f} {(AY0+AY1)/2:.0f})">'
             f'effective index n</text>')

    # the two predicted values
    for v, col, lab in ((1.5, ACC2, "n = 3/2, adiabatic convection"),
                        (3.0, ACC, "n = 3, Eddington's standard model")):
        y = ay(v)
        s.append(f'<line x1="{AX0:.0f}" y1="{y:.1f}" x2="{AX1:.0f}" '
                 f'y2="{y:.1f}" stroke="{col}" stroke-width="1.6" '
                 f'stroke-dasharray="6 4"/>')
    # Both labels are anchored at r = 0.62 and run leftwards.  The curve
    # crosses n = 3 at r = 0.217, so a label starting at the left edge is
    # struck through; over 0.33 < r < 0.62 the curve stays above n = 3.5,
    # nineteen pixels clear of the higher label and far above the lower one.
    s.append(f'<text x="{ax(0.62):.1f}" y="{ay(3.0)-8:.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC}">n = 3, Eddington\'s standard '
             f'model</text>')
    s.append(f'<text x="{ax(0.62):.1f}" y="{ay(1.5)-8:.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC2}">n = 3/2, adiabatic '
             f'convection</text>')

    ok = np.isfinite(neff) & (r > 0.015) & (r < 0.965)
    rr, nn = r[ok], np.clip(neff[ok], NLO, NHI)
    step = max(1, len(rr)//600)
    s.append(f'<path d="{path(ax(rr[::step]), ay(nn[::step]))}" fill="none" '
             f'stroke="{YEL}" stroke-width="2.6"/>')

    # annotate the three regions, inside the box
    imax = int(np.argmax(nn))
    s.append(f'<text x="{ax(rr[imax]):.1f}" y="{ay(nn[imax])-10:.1f}" '
             f'font-size="10.5" text-anchor="middle" fill="{YEL}">'
             f'max {nn[imax]:.2f} at r = {rr[imax]:.2f} R</text>')
    s.append(f'<text x="{ax(0.06):.1f}" y="{ay(2.08)+18:.1f}" '
             f'font-size="10.5" fill="{MUT}">burning core</text>')
    s.append(f'<text x="{ax(0.86):.1f}" y="{ay(1.5)+20:.1f}" '
             f'font-size="10.5" text-anchor="middle" fill="{FG}">'
             f'measured plateau {n_plateau:.3f}</text>')

    # ---------------- panel B ----------------
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-28:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Zoom on the base of the '
             f'convection zone, where that index changes</text>')
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" width="{BX1-BX0:.0f}" '
             f'height="{BY1-BY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for t in (0.70, 0.71, 0.72, 0.73, 0.74):
        x = bx(t)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t:.2f}</text>')
    for v in (0.28, 0.32, 0.36, 0.40):
        y = by(v)
        s.append(f'<line x1="{BX0-5:.0f}" y1="{y:.1f}" x2="{BX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{BX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.2f}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">r / R</text>')
    s.append(f'<text x="{BX0-48:.0f}" y="{(BY0+BY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {BX0-48:.0f} {(BY0+BY1)/2:.0f})">'
             f'∇ = d ln T / d ln P</text>')

    # the adiabatic plateau
    yp = by(plateau)
    s.append(f'<line x1="{BX0:.0f}" y1="{yp:.1f}" x2="{BX1:.0f}" '
             f'y2="{yp:.1f}" stroke="{ACC2}" stroke-width="1.6" '
             f'stroke-dasharray="6 4"/>')
    s.append(f'<text x="{BX1-10:.0f}" y="{yp-8:.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC2}">adiabatic plateau, '
             f'∇ = {plateau:.4f}</text>')

    sel = (r >= RLO) & (r <= RHI) & np.isfinite(grad)
    s.append(f'<path d="{path(bx(r[sel]), by(np.clip(grad[sel], GLO, GHI)))}" '
             f'fill="none" stroke="{YEL}" stroke-width="2.6"/>')

    # the model's own boundary
    xm = bx(M.RCZ_MODEL_PUBLISHED)
    s.append(f'<line x1="{xm:.1f}" y1="{BY0:.0f}" x2="{xm:.1f}" '
             f'y2="{BY1:.0f}" stroke="{ACC}" stroke-width="2"/>')
    # Rows at BY0 + 50 and + 65, not + 20 and + 35: the second line used to
    # straddle the adiabatic-plateau dash at y = 418.  Below the plateau the
    # curve is flat at y = 418 for r > 0.7269, so these rows are clear.
    s.append(f'<text x="{xm+8:.1f}" y="{BY0+50:.0f}" font-size="10.5" '
             f'fill="{ACC}">model: {M.RCZ_MODEL_PUBLISHED:.4f}</text>')
    s.append(f'<text x="{xm+8:.1f}" y="{BY0+65:.0f}" font-size="10.5" '
             f'fill="{ACC}">this script recovers {rb:.4f}</text>')

    # the measurement, with its error bar
    xs = bx(M.RCZ_MEAS)
    s.append(f'<line x1="{xs:.1f}" y1="{BY0:.0f}" x2="{xs:.1f}" '
             f'y2="{BY1:.0f}" stroke="{VIO}" stroke-width="2"/>')
    # the +/- 1 sigma interval as a full-height band, so it reads as an
    # interval on r rather than as a marker at one value of grad
    s.append(f'<rect x="{bx(M.RCZ_MEAS-M.RCZ_MEAS_ERR):.1f}" '
             f'y="{BY0:.0f}" '
             f'width="{bx(M.RCZ_MEAS+M.RCZ_MEAS_ERR)-bx(M.RCZ_MEAS-M.RCZ_MEAS_ERR):.1f}" '
             f'height="{BY1-BY0:.0f}" fill="{VIO}" fill-opacity="0.22"/>')
    s.append(f'<text x="{xs-8:.1f}" y="{BY0+50:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{VIO}">measured: '
             f'{M.RCZ_MEAS:.4f} ± {M.RCZ_MEAS_ERR:.4f}</text>')
    s.append(f'<text x="{xs-8:.1f}" y="{BY0+65:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{VIO}">Basu &amp; Antia (2004)</text>')

    # the gap, drawn as a measured bar between the two verticals
    ygap = BY1 - 52.0
    s.append(f'<line x1="{xs:.1f}" y1="{ygap:.1f}" x2="{xm:.1f}" '
             f'y2="{ygap:.1f}" stroke="{FG}" stroke-width="1.6"/>')
    sig = (M.RCZ_MODEL_PUBLISHED - M.RCZ_MEAS)/M.RCZ_MEAS_ERR
    s.append(f'<text x="{(xs+xm)/2:.1f}" y="{ygap-9:.1f}" font-size="11" '
             f'text-anchor="middle" fill="{FG}">'
             f'{M.RCZ_MODEL_PUBLISHED-M.RCZ_MEAS:.4f} R, or {sig:.0f}σ</text>')

    s.append(f'<text x="{BX0-48:.0f}" y="{H-28:.0f}" font-size="10.5" '
             f'fill="{MUT}">Model: BS2005-AGS,OP. Measurement: Basu &amp; '
             f'Antia (2004), ApJ 606, L85, r<tspan baseline-shift="sub" font-size="8">b</tspan> = (0.7133 ± 0.0005) R from '
             f'GONG p-mode frequencies.</text>')
    s.append(f'<text x="{BX0-48:.0f}" y="{H-12:.0f}" font-size="10.5" '
             f'fill="{MUT}">What the gap indicts is the model\'s composition '
             f'and opacity, not hydrostatic equilibrium.</text>')
    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    for name, body in (("m03_fig_atmos.svg", build_atmos()),
                       ("m03_fig_lane.svg", build_lane()),
                       ("m03_fig_index.svg", build_index())):
        with open(name, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"wrote {name} ({len(body)} bytes)")
