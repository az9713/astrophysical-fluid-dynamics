"""Build the computed SVG figures for Module 8.

Writes four files:

  m08_fig_jumps.svg   the Rankine-Hugoniot jumps.  Left panel the density
                      ratio rho2/rho1 against upstream Mach number M1 for
                      gamma = 5/3 and 7/5, saturating at the ceilings 4
                      and 6, with the isothermal law M^2, which has no
                      ceiling.  Right panel the entropy jump Delta s/k
                      against M1: zero at M1 = 1, positive above, negative
                      below, which is the whole argument against
                      rarefaction shocks.

  m08_fig_sedov.svg   THE ANCHOR FIGURE.  Upper left the Sedov similarity
                      profiles rho/rho2, v/v2, p/p2 against r/R for both
                      gammas.  Upper right Taylor's 25 Trinity points in
                      the (log t, (5/2) log R) plane with the slope-1 line
                      that R ~ t^(2/5) predicts.  Bottom the residual from
                      that line, by photographic source, with the band
                      means drawn: the confirmation is the upper right
                      panel, and the refutation is the bottom one.

  m08_fig_check.svg   the Voyager 2 check in residual style: measured over
                      predicted for each comparison, on a logarithmic axis
                      centred on 1, the Neptune bow shock and the solar-
                      wind termination shock side by side.

  m08_fig_tycho.svg   the debt from Module 7, paid.  Four Rayleigh-Taylor
                      mixing widths on one radial axis, every one measured
                      outward from the same place, the one-dimensional
                      contact discontinuity at 0.77 of the blast-wave
                      radius.  The width that Module 7's mixing law
                      predicts is drawn at the same scale as the three
                      observed ones, so the factor of eleven is a hairline
                      beside three long bars rather than a claim in a
                      caption.

Geometry is computed, never eyeballed.  Every number drawn is produced by
m08_numbers.py, so a figure cannot drift away from the prose.

The Module 2 lesson is applied twice.  The Trinity agreement is shown as a
residual, because on the log-log panel all 25 points sit within a
point-width of the line and the structure that refutes the model is
invisible there.  And the Voyager comparison is drawn as a ratio to the
prediction, so that 1.00 and 0.10 are the same kind of mark on the same
axis.  Labels are placed by arithmetic inside each plot box, and curves
that would leave a box are truncated in the generator rather than clipped
with clip-path, because check_overlap reads geometry, not pixels.
"""
import numpy as np

import m08_numbers as M

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def box(s, x0, x1, y0, y1):
    s.append(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1-x0:.0f}" '
             f'height="{y1-y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')


def xtick(s, x, y1, label):
    s.append(f'<line x1="{x:.1f}" y1="{y1:.0f}" x2="{x:.1f}" '
             f'y2="{y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
    s.append(f'<text x="{x:.1f}" y="{y1+18:.0f}" font-size="10.5" '
             f'text-anchor="middle" fill="{MUT}">{label}</text>')


def ytick(s, x0, y, label):
    s.append(f'<line x1="{x0-5:.0f}" y1="{y:.1f}" x2="{x0:.0f}" '
             f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
    s.append(f'<text x="{x0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{MUT}">{label}</text>')


def text(s, x, y, body, fill=FG, size=10.5, anchor="start"):
    s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
             f'text-anchor="{anchor}" fill="{fill}">{body}</text>')


def ylabel(s, x, y, body):
    s.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {x:.0f} {y:.0f})">{body}</text>')


# =========================================================================
# Figure: the Rankine-Hugoniot jumps
# =========================================================================

def build_jumps():
    W, H = 760, 380
    AX0, AX1, AY0, AY1 = 70.0, 360.0, 44.0, 300.0
    BX0, BX1, BY0, BY1 = 450.0, 740.0, 44.0, 300.0

    # panel A: log M1 from 1 to 100, rho2/rho1 from 1 to 7
    LM0, LM1, RY0, RY1 = 0.0, 2.0, 1.0, 7.0

    def ax(m):
        return AX0 + (np.log10(m) - LM0)/(LM1 - LM0)*(AX1 - AX0)

    def ay(r):
        return AY1 - (r - RY0)/(RY1 - RY0)*(AY1 - AY0)

    # panel B: linear M1 from 0.45 to 4, ds/k from -1.4 to 2.2
    BM0, BM1, SY0, SY1 = 0.45, 4.0, -1.4, 2.2

    def bx(m):
        return BX0 + (m - BM0)/(BM1 - BM0)*(BX1 - BX0)

    def by(v):
        return BY1 - (v - SY0)/(SY1 - SY0)*(BY1 - BY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Left panel: the density ratio across a '
         f'normal shock against upstream Mach number from 1 to 100, for '
         f'gamma 5/3 and 7/5. Both curves rise and level off, at 4 and at '
         f'6. A dashed isothermal curve, equal to Mach number squared, '
         f'leaves the top of the panel before Mach 3. Right panel: the '
         f'entropy jump per particle against Mach number. It is zero at '
         f'Mach 1, positive above and negative below, and the region below '
         f'Mach 1 is marked forbidden.">']

    # ---------------- panel A ----------------
    text(s, (AX0+AX1)/2, AY0-18, 'Compression has a ceiling', FG, 12.5,
         'middle')
    box(s, AX0, AX1, AY0, AY1)
    for m, lbl in ((1, '1'), (2, '2'), (3, '3'), (5, '5'), (10, '10'),
                   (20, '20'), (50, '50'), (100, '100')):
        xtick(s, ax(m), AY1, lbl)
    for r in range(1, 8):
        ytick(s, AX0, ay(r), str(r))
    text(s, (AX0+AX1)/2, AY1+36, 'upstream Mach number M₁', FG, 11.5,
         'middle')
    ylabel(s, AX0-36, (AY0+AY1)/2, 'ρ₂ / ρ₁')

    m = np.logspace(0.0, 2.0, 300)
    for g, col, cap in ((M.GAM_DIAT, ACC2, 6.0), (M.GAM_MONO, ACC, 4.0)):
        s.append(f'<line x1="{AX0:.0f}" y1="{ay(cap):.1f}" x2="{AX1:.0f}" '
                 f'y2="{ay(cap):.1f}" stroke="{col}" stroke-width="1" '
                 f'stroke-dasharray="3 3" opacity="0.7"/>')
        r = M.rh_jumps(m, g)[0]
        s.append(f'<path d="{path(ax(m), ay(r))}" fill="none" '
                 f'stroke="{col}" stroke-width="2.4"/>')
    # isothermal M^2, truncated at the top of the box in the generator
    mi = np.logspace(0.0, np.log10(np.sqrt(RY1)), 120)
    s.append(f'<path d="{path(ax(mi), ay(mi*mi))}" fill="none" '
             f'stroke="{MUT}" stroke-width="1.8" stroke-dasharray="5 3"/>')

    # Labels.  The ceilings are labelled at the right end, above their
    # dashed lines, where each curve has already reached 97% of its
    # ceiling and sits within 6 px of it: the label goes ABOVE both.
    text(s, AX1-8, ay(6.0)-7, 'γ = 7/5: ceiling 6', ACC2, 10.5, 'end')
    text(s, AX1-8, ay(4.0)-7, 'γ = 5/3: ceiling 4', ACC, 10.5, 'end')
    # The isothermal curve leaves the top edge at M = sqrt(7) = 2.65,
    # x = ax(2.65) = 193; its label sits left of it, under the top edge.
    text(s, AX0+10, AY0+16, 'isothermal: M₁²,', MUT, 10.5)
    text(s, AX0+10, AY0+30, 'no ceiling', MUT, 10.5)

    # ---------------- panel B ----------------
    text(s, (BX0+BX1)/2, BY0-18, 'The second law picks the sign', FG, 12.5,
         'middle')
    # forbidden region M1 < 1, drawn first so everything sits on top
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" '
             f'width="{bx(1.0)-BX0:.1f}" height="{BY1-BY0:.0f}" '
             f'fill="{RULE}" opacity="0.35"/>')
    box(s, BX0, BX1, BY0, BY1)
    for mm in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
        xtick(s, bx(mm), BY1, f'{mm:g}')
    for v in (-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0):
        ytick(s, BX0, by(v), f'{v:g}')
    s.append(f'<line x1="{BX0:.0f}" y1="{by(0):.1f}" x2="{BX1:.0f}" '
             f'y2="{by(0):.1f}" stroke="{MUT}" stroke-width="1"/>')
    text(s, (BX0+BX1)/2, BY1+36, 'upstream Mach number M₁', FG, 11.5,
         'middle')
    ylabel(s, BX0-40, (BY0+BY1)/2, 'entropy jump Δs / k per particle')

    # The jump formula gives p2/p1 < 0 below M1 = sqrt((gamma-1)/(2 gamma)),
    # 0.447 for 5/3.  The panel starts at 0.45 but the 5/3 curve falls
    # below -1.4 before that, so each curve is truncated in the generator
    # at the lower edge of the box.
    for g, col in ((M.GAM_DIAT, ACC2), (M.GAM_MONO, ACC)):
        mm = np.linspace(BM0, BM1, 600)
        ds = M.entropy_jump(mm, g)
        ok = np.isfinite(ds) & (ds >= SY0) & (ds <= SY1)
        s.append(f'<path d="{path(bx(mm[ok]), by(ds[ok]))}" fill="none" '
                 f'stroke="{col}" stroke-width="2.4"/>')

    # Labels by arithmetic.  At M1 = 3 the curves are at 0.850 (5/3) and
    # 1.114 (7/5), y = 229 and 210: 19 px apart.  The labels go to the
    # right of M1 = 3.3, 7/5 above its curve and 5/3 below its curve.
    m_lab = 3.25
    y75 = by(float(M.entropy_jump(m_lab, M.GAM_DIAT)))
    y53 = by(float(M.entropy_jump(m_lab, M.GAM_MONO)))
    text(s, bx(m_lab)-4, y75-12, 'γ = 7/5', ACC2, 10.5, 'end')
    text(s, bx(m_lab)+6, y53+22, 'γ = 5/3', ACC, 10.5)
    # forbidden-region caption, in the empty upper part of the grey band
    text(s, (BX0+bx(1.0))/2, BY0+18, 'M₁ &lt; 1', FG, 10.5, 'middle')
    text(s, (BX0+bx(1.0))/2, BY0+32, 'Δs &lt; 0', FG, 10.5, 'middle')
    text(s, (BX0+bx(1.0))/2, BY0+46, 'forbidden', FG, 10.5, 'middle')
    # the M = 3 value quoted in the problem set, marked on the 5/3 curve
    ds3 = float(M.entropy_jump(3.0, M.GAM_MONO))
    s.append(f'<circle cx="{bx(3.0):.1f}" cy="{by(ds3):.1f}" r="3.5" '
             f'fill="{ACC}"/>')

    text(s, AX0-36, H-12,
         f'Both panels are the three conservation laws of Module 2 '
         f'integrated across the layer; nothing inside it is modelled.',
         MUT, 10.5)
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure: Sedov profiles, Trinity, and the Trinity residual
# =========================================================================

def build_sedov():
    W, H = 760, 660
    AX0, AX1, AY0, AY1 = 70.0, 360.0, 44.0, 290.0
    BX0, BX1, BY0, BY1 = 450.0, 740.0, 44.0, 290.0
    CX0, CX1, CY0, CY1 = 70.0, 740.0, 382.0, 598.0

    # ---- data ----
    t, R, auth = M.load_trinity()
    n_i = M.taylor_intercept(t, R)
    n_fixed = float(np.mean(n_i[1:]))
    resid = n_i - n_fixed
    lt = np.log10(t)
    y52 = 2.5*np.log10(R)

    # ---- panel A scales: r/R from 0 to 1, value from 0 to 1.05 ----
    def ax(x):
        return AX0 + x*(AX1 - AX0)

    def ay(v):
        return AY1 - v/1.05*(AY1 - AY0)

    # ---- panel B scales: log t from -4.2 to -1.0, (5/2) log R ----
    LT0, LT1 = -4.2, -1.0
    YB0, YB1 = 7.4, 10.9

    def bx(x):
        return BX0 + (x - LT0)/(LT1 - LT0)*(BX1 - BX0)

    def by(v):
        return BY1 - (v - YB0)/(YB1 - YB0)*(BY1 - BY0)

    # ---- panel C scales: same log t, residual from -0.07 to +0.05 ----
    RC0, RC1 = -0.07, 0.05

    def cx(x):
        return CX0 + (x - LT0)/(LT1 - LT0)*(CX1 - CX0)

    def cy(v):
        return CY1 - (v - RC0)/(RC1 - RC0)*(CY1 - CY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper left: the Sedov-Taylor profiles of '
         f'density, velocity and pressure against radius for gamma 5/3 and '
         f'7/5. Density is piled into a thin shell behind the shock, and '
         f'pressure levels off at about a third of its post-shock value in '
         f'the interior. Upper right: Taylor\'s 25 Trinity points, five '
         f'halves log radius against log time, lying along a line of slope '
         f'one. Bottom: the residual of each point from that line. The '
         f'first point, at 0.10 milliseconds, is far below the scale. The '
         f'rest fall in three bands whose means decrease with time.">']

    # ---------------- panel A ----------------
    text(s, (AX0+AX1)/2, AY0-18, 'Inside the blast wave', FG, 12.5, 'middle')
    box(s, AX0, AX1, AY0, AY1)
    for x in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        xtick(s, ax(x), AY1, f'{x:.1f}')
    for v in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        ytick(s, AX0, ay(v), f'{v:.1f}')
    text(s, (AX0+AX1)/2, AY1+36, 'r / R', FG, 11.5, 'middle')
    ylabel(s, AX0-38, (AY0+AY1)/2, 'value / value just behind shock')

    cols = {'rho': ACC, 'v': ACC2, 'p': VIO}
    prof = {}
    for g, dash in ((M.GAM_MONO, None), (M.GAM_DIAT, "5 3")):
        lam, u, gg, hh = M.sedov_profile(g, n_sample=20001)
        u1 = 4.0/(5.0*(g + 1.0))
        g1 = (g + 1.0)/(g - 1.0)
        h1 = 8.0/(25.0*(g + 1.0))
        sel = lam >= 0.002
        lam, u, gg, hh = lam[sel], u[sel], gg[sel], hh[sel]
        curves = {'rho': gg/g1, 'v': lam*u/u1, 'p': hh*lam*lam/h1}
        prof[g] = (lam, curves)
        # decimate for drawing only
        idx = np.unique(np.concatenate([
            np.searchsorted(-lam, -np.linspace(1.0, 0.002, 400))]))
        idx = idx[idx < len(lam)]
        for key in ('p', 'v', 'rho'):
            d = f' stroke-dasharray="{dash}"' if dash else ''
            s.append(f'<path d="{path(ax(lam[idx]), ay(curves[key][idx]))}" '
                     f'fill="none" stroke="{cols[key]}" '
                     f'stroke-width="{2.4 if dash is None else 1.8}"{d}/>')

    # Labels by arithmetic.  At r/R = 0.25 the velocity curves are near
    # 0.20, the pressure curves near 0.31-0.37 and density below 0.01.
    # Labels sit in the empty upper-left region, each with a short leader.
    lam53, c53 = prof[M.GAM_MONO]
    # Pressure label: no leader.  For r/R < 0.30 the velocity curves are
    # below 0.21 and the pressure plateaus sit at 0.306 and 0.365, so the
    # band 0.43-0.50 above them is empty.
    text(s, ax(0.03), ay(0.43), 'pressure p/p₂ (plateau)', VIO)
    j = int(np.argmin(abs(lam53 - 0.55)))
    text(s, ax(0.04), ay(0.84), 'velocity v/v₂', ACC2)
    s.append(f'<line x1="{ax(0.24):.1f}" y1="{ay(0.81):.1f}" '
             f'x2="{ax(0.55):.1f}" y2="{ay(c53["v"][j])-4:.1f}" '
             f'stroke="{ACC2}" stroke-width="1"/>')
    j = int(np.argmin(abs(lam53 - 0.88)))
    text(s, ax(0.40), ay(0.10), 'density ρ/ρ₂', ACC)
    s.append(f'<line x1="{ax(0.62):.1f}" y1="{ay(0.13):.1f}" '
             f'x2="{ax(0.88)-3:.1f}" y2="{ay(c53["rho"][j]):.1f}" '
             f'stroke="{ACC}" stroke-width="1"/>')
    text(s, ax(0.04), ay(1.00), 'solid γ = 5/3, dashed γ = 7/5', MUT)

    # ---------------- panel B ----------------
    text(s, (BX0+BX1)/2, BY0-18, 'Trinity: R ∝ t²ᐟ⁵ confirmed', FG, 12.5,
         'middle')
    box(s, BX0, BX1, BY0, BY1)
    for x in (-4, -3, -2, -1):
        xtick(s, bx(x), BY1, f'10<tspan dy="-5" font-size="8">{x}</tspan>')
    for v in (8, 9, 10):
        ytick(s, BX0, by(v), f'{v}')
    text(s, (BX0+BX1)/2, BY1+36, 't / s', FG, 11.5, 'middle')
    ylabel(s, BX0-34, (BY0+BY1)/2, '(5/2) log₁₀(R / cm)')
    xl = np.array([LT0, LT1])
    s.append(f'<path d="{path(bx(xl), by(xl + n_fixed))}" fill="none" '
             f'stroke="{MUT}" stroke-width="1.4" stroke-dasharray="5 3"/>')
    acol = {'A': ACC, 'B': ACC2, 'C': VIO, 'D': YEL}
    for xi, yi, ai in zip(lt, y52, auth):
        s.append(f'<circle cx="{bx(xi):.1f}" cy="{by(yi):.1f}" r="3.2" '
                 f'fill="{acol[ai]}"/>')
    # The line runs from bottom-left to top-right, so the top-left and
    # bottom-right corners are empty: the equation goes top left.
    text(s, BX0+10, BY0+18, 'slope 1 ⇔ R ∝ t²ᐟ⁵', MUT)
    text(s, BX0+10, BY0+32, f'intercept {n_fixed:.3f} (Taylor: 11.915)',
         MUT)
    text(s, BX1-10, BY1-40, '25 rows, Taylor (1950)', MUT, 10.5, 'end')
    text(s, BX1-10, BY1-26, 'Table 1: 0.10–62 ms,', MUT, 10.5, 'end')
    text(s, BX1-10, BY1-12, '11.1–185 m', MUT, 10.5, 'end')

    # ---------------- panel C ----------------
    text(s, (CX0+CX1)/2, CY0-18,
         'The residual from that line: the model behind it refuted', FG,
         12.5, 'middle')
    box(s, CX0, CX1, CY0, CY1)
    for x in (-4, -3, -2, -1):
        xtick(s, cx(x), CY1, f'10<tspan dy="-5" font-size="8">{x}</tspan>')
    for v in (-0.06, -0.04, -0.02, 0.0, 0.02, 0.04):
        ytick(s, CX0, cy(v), f'{v:+.2f}' if v else '0')
    text(s, (CX0+CX1)/2, CY1+36, 't / s', FG, 11.5, 'middle')
    ylabel(s, CX0-44, (CY0+CY1)/2, 'residual in (5/2) log₁₀ R')
    s.append(f'<line x1="{CX0:.0f}" y1="{cy(0):.1f}" x2="{CX1:.0f}" '
             f'y2="{cy(0):.1f}" stroke="{MUT}" stroke-width="1" '
             f'stroke-dasharray="5 3"/>')

    # band means as horizontal bars over each band's time span
    for lo, hi in ((1, 14), (14, 20), (20, 25)):
        mval = float(np.mean(resid[lo:hi]))
        xa, xb = cx(lt[lo]) - 8, cx(lt[hi-1]) + 8
        s.append(f'<line x1="{xa:.1f}" y1="{cy(mval):.1f}" x2="{xb:.1f}" '
                 f'y2="{cy(mval):.1f}" stroke="{FG}" stroke-width="2"/>')
    # the points
    for xi, ri, ai in zip(lt[1:], resid[1:], auth[1:]):
        s.append(f'<circle cx="{cx(xi):.1f}" cy="{cy(ri):.1f}" r="3.4" '
                 f'fill="{acol[ai]}"/>')
    # row 1 is off scale: a triangle pointing down at the lower edge
    x1p = cx(lt[0])
    yb = CY1 - 4
    s.append(f'<polygon points="{x1p-6:.1f},{yb-10:.1f} {x1p+6:.1f},'
             f'{yb-10:.1f} {x1p:.1f},{yb:.1f}" fill="{ACC}"/>')
    text(s, x1p+12, yb-22, f'0.10 ms: {resid[0]:+.3f}', ACC)
    text(s, x1p+12, yb-8, 'off scale below', ACC)

    # band-mean labels, placed by arithmetic above or below each bar,
    # in the clear vertical space away from that band's points
    b1 = float(np.mean(resid[1:14]))
    b2 = float(np.mean(resid[14:20]))
    b3 = float(np.mean(resid[20:25]))
    text(s, cx(lt[1]), cy(0.043), f'band mean {b1:+.4f}', FG)
    text(s, (cx(lt[14])+cx(lt[19]))/2, cy(-0.030),
         f'{b2:+.4f}', FG, 10.5, 'middle')
    # below the lowest point of the last band (-0.044), clear of the legend
    text(s, (cx(lt[20])+cx(lt[24]))/2, cy(-0.060),
         f'{b3:+.4f}', FG, 10.5, 'middle')

    # legend for photographic source, top right corner of panel C: the
    # rows plotted there (t > 15 ms) all lie below -0.02, clear of it.
    lx, ly = CX1-220, CY0+16
    for k, (a, lbl) in enumerate((('A', 'MDDC-221 small images'),
                                  ('B', 'Ministry of Supply strip'),
                                  ('C', 'MDDC-221 small images'),
                                  ('D', 'MDDC-221 large photographs'))):
        s.append(f'<circle cx="{lx:.1f}" cy="{ly+k*14-4:.1f}" r="3.4" '
                 f'fill="{acol[a]}"/>')
        text(s, lx+10, ly+k*14, f'{a}: {lbl}', MUT)

    text(s, CX0-44, H-28,
         f'Residuals are from the fixed-slope line through rows 2–25. The '
         f'band means fall from {b1:+.3f} to {b2:+.3f} to {b3:+.3f};',
         MUT, 10.5)
    text(s, CX0-44, H-12,
         'the step between the outer bands is 7.3 times their combined '
         'standard error. Bands coincide with photographic sources.',
         MUT, 10.5)
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure: Voyager 2, measured over predicted
# =========================================================================

def build_check():
    W, H = 760, 350
    X0, X1, Y0, Y1 = 330.0, 740.0, 40.0, 262.0
    L0, L1 = np.log10(0.05), np.log10(2.0)

    def x(v):
        return X0 + (np.log10(v) - L0)/(L1 - L0)*(X1 - X0)

    r_ts2_pred = float(M.rh_jumps(M.V2_TS2_MACH_FAST_UP, M.GAM_MONO)[0])
    M_T = M._mach_from_Tratio(M.V2_NEPTUNE_TEMP_JUMP, M.GAM_MONO)
    r_from_T = float(M.rh_jumps(M_T, M.GAM_MONO)[0])
    rows = [
        ('Neptune bow shock', 'density jump / 4',
         M.V2_NEPTUNE_DENSITY_JUMP/4.0, None, ACC, True),
        ('Neptune bow shock', 'speed drop / 4',
         M.V2_NEPTUNE_SPEED_DROP/4.0, None, ACC, True),
        ('Neptune bow shock', f'ρ₂/ρ₁ from T-jump Mach {M_T:.1f} / 4',
         r_from_T/M.V2_NEPTUNE_DENSITY_JUMP, None, ACC, True),
        ('termination shock', 'T observed / T predicted',
         M.V2_TS_T_OBSERVED/M.V2_TS_T_PREDICTED, None, ACC2, True),
        ('termination shock', f'TS-2 ρ₂/ρ₁ / gas-dynamic {r_ts2_pred:.2f}',
         M.V2_TS2_COMPRESSION/r_ts2_pred,
         M.V2_TS2_COMPRESSION_ERR/r_ts2_pred, MUT, False),
    ]
    dy = (Y1 - Y0)/len(rows)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Measured value divided by the '
         f'Rankine-Hugoniot prediction, on a logarithmic axis from 0.05 to '
         f'2, for five comparisons from Voyager 2. Three comparisons at '
         f'Neptune\'s bow shock sit at 1. The termination-shock temperature '
         f'sits at 0.1. A fifth, grey, termination-shock compression ratio '
         f'sits at 0.67 and is marked as partly circular.">']
    text(s, (X0+X1)/2, Y0-18, 'Voyager 2: measured ÷ Rankine–Hugoniot '
         'prediction', FG, 12.5, 'middle')
    box(s, X0, X1, Y0, Y1)
    for v in (0.05, 0.1, 0.2, 0.5, 1.0, 2.0):
        xtick(s, x(v), Y1, f'{v:g}')
    text(s, (X0+X1)/2, Y1+36, 'ratio, logarithmic', FG, 11.5, 'middle')
    s.append(f'<line x1="{x(1.0):.1f}" y1="{Y0:.0f}" x2="{x(1.0):.1f}" '
             f'y2="{Y1:.0f}" stroke="{MUT}" stroke-width="1" '
             f'stroke-dasharray="5 3"/>')
    for k, (grp, lbl, val, err, col, used) in enumerate(rows):
        yc = Y0 + dy*(k + 0.5)
        s.append(f'<line x1="{X0:.0f}" y1="{yc:.1f}" x2="{X1:.0f}" '
                 f'y2="{yc:.1f}" stroke="{RULE}" stroke-width="0.6"/>')
        text(s, X0-12, yc-2, grp, col if used else MUT, 10.5, 'end')
        text(s, X0-12, yc+12, lbl, MUT, 10.5, 'end')
        if err is not None:
            s.append(f'<line x1="{x(val-err):.1f}" y1="{yc:.1f}" '
                     f'x2="{x(val+err):.1f}" y2="{yc:.1f}" stroke="{col}" '
                     f'stroke-width="2"/>')
        if used:
            s.append(f'<circle cx="{x(val):.1f}" cy="{yc:.1f}" r="5" '
                     f'fill="{col}"/>')
        else:
            s.append(f'<circle cx="{x(val):.1f}" cy="{yc:.1f}" r="5" '
                     f'fill="{BG}" stroke="{col}" stroke-width="1.6"/>')
        # value label: right of the mark if the mark is left of 1, else left
        if val < 0.8:
            text(s, x(val)+12 + (x(val+err)-x(val) if err else 0),
                 yc-6, f'{val:.2f}', col)
        else:
            text(s, x(val)-12, yc-6, f'{val:.2f}', col, 10.5, 'end')
    # verdict tags in the left, empty part of the box (ratios below 0.08
    # are absent from every row)
    text(s, x(0.052), Y0+dy*1.5-8, 'CONFIRMED', ACC, 10.5)
    text(s, x(0.052), Y0+dy*3.5-8, 'REFUTED', ACC2, 10.5)
    text(s, x(0.052), Y0+dy*4.5-22, 'not used:', MUT, 10.5)
    text(s, x(0.052), Y0+dy*4.5-8, 'partly circular', MUT, 10.5)

    text(s, 20, H-28,
         'Richardson et al. (2008), Nature 454, 63–66. Neptune values read '
         'from their Fig. 5 caption, which gives no uncertainty; '
         'T values from p. 65.', MUT, 10.5)
    text(s, 20, H-12,
         'Grey row: compression ratio and Mach number come from one '
         'Rankine–Hugoniot fit (their Table 1), so it tests the fit.',
         MUT, 10.5)
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure: the Rayleigh-Taylor debt from Module 7, paid at Tycho
# =========================================================================

def build_tycho():
    """Widths, not positions, on one radial axis.

    Every bar starts at the same place, the one-dimensional contact
    discontinuity, and its length is a mixing width.  The predicted width is
    drawn on the same axis as the observed ones and at the same scale, which
    is the only honest way to show a factor of eleven: it comes out a
    hairline beside them, and no caption has to assert it.
    """
    W, H = 760, 330
    X0, X1, Y0, Y1 = 250.0, 720.0, 52.0, 236.0
    R0, R1 = 0.74, 1.04

    def x(r):
        return X0 + (r - R0)/(R1 - R0)*(X1 - X0)

    base = M.W05_WC01_CD_1D
    h_pred = M.rt_width_fraction(M.SHIMONY_ALPHA_B, 1.0, M.K10_M_MEAN, base)
    h_hi = M.rt_width_fraction(M.SHIMONY_ALPHA_B + M.SHIMONY_ALPHA_B_ERR,
                               1.0, M.K10_M_MEAN, base)
    rows = [
        ("predicted by Module 7's mixing law", 'h = α_B A m(1−m) R, A = 1',
         h_pred, h_hi, ACC2, True),
        ('2-D simulation, pure hydro', 'Wang &amp; Chevalier (2001)',
         M.WC01_FINGER_TIPS - base, None, ACC, False),
        ('Tycho, mean CD, deprojected', 'Warren et al. (2005)',
         M.W05_CD_OVER_BW - base, None, ACC, False),
        ('Tycho, farthest ejecta clumps', 'Warren et al. (2005) §3',
         1.0 - base, None, ACC, False),
    ]
    dy = (Y1 - Y0)/len(rows)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Four Rayleigh-Taylor mixing widths drawn '
         f'on one radial axis from 0.74 to 1.04 in units of the blast-wave '
         f'radius, every one starting at the one-dimensional contact '
         f'discontinuity at 0.77. The width predicted by the plane-interface '
         f'mixing law is {100*h_pred:.2f} per cent of the blast-wave radius '
         f'and is a hairline. The two-dimensional simulation gives 8 per '
         f'cent, Tycho\'s mean contact discontinuity 16 per cent and its '
         f'farthest clumps 23 per cent.">']
    text(s, (X0+X1)/2, Y0-24, 'Rayleigh–Taylor at Tycho: one predicted width '
         'against three observed ones', FG, 12.5, 'middle')
    box(s, X0, X1, Y0, Y1)
    for v in (0.77, 0.80, 0.85, 0.90, 0.95, 1.00):
        xtick(s, x(v), Y1, f'{v:.2f}')
    text(s, (X0+X1)/2, Y1+36, 'radius ÷ blast-wave radius', FG, 11.5,
         'middle')
    # the blast wave itself, and the 1-D contact discontinuity both bars
    # start from
    s.append(f'<line x1="{x(1.0):.1f}" y1="{Y0:.0f}" x2="{x(1.0):.1f}" '
             f'y2="{Y1:.0f}" stroke="{MUT}" stroke-width="1" '
             f'stroke-dasharray="5 3"/>')
    text(s, x(1.0)-6, Y0+13, 'blast wave', MUT, 10.5, 'end')
    s.append(f'<line x1="{x(base):.1f}" y1="{Y0:.0f}" x2="{x(base):.1f}" '
             f'y2="{Y1:.0f}" stroke="{VIO}" stroke-width="1.2"/>')
    text(s, x(base)+6, Y0+13, '1-D contact discontinuity', VIO, 10.5)

    for k, (lbl, src, wid, wid_hi, col, predicted) in enumerate(rows):
        yc = Y0 + dy*(k + 0.5)
        s.append(f'<line x1="{X0:.0f}" y1="{yc:.1f}" x2="{X1:.0f}" '
                 f'y2="{yc:.1f}" stroke="{RULE}" stroke-width="0.6"/>')
        text(s, X0-12, yc-2, lbl, col, 10.5, 'end')
        text(s, X0-12, yc+12, src, MUT, 10.5, 'end')
        h = 9.0
        s.append(f'<rect x="{x(base):.1f}" y="{yc-h/2:.1f}" '
                 f'width="{max(x(base + wid) - x(base), 1.2):.1f}" '
                 f'height="{h:.0f}" fill="{col}" '
                 f'{"stroke=\'"+col+"\' stroke-width=\'1\'" if predicted else ""}/>')
        if predicted:
            # the bar is thinner than its own outline, so label it with a
            # leader line rather than beside it
            s.append(f'<line x1="{x(base + wid):.1f}" y1="{yc-h/2-3:.1f}" '
                     f'x2="{x(base + 0.055):.1f}" y2="{yc-h/2-13:.1f}" '
                     f'stroke="{col}" stroke-width="1"/>')
            text(s, x(base + 0.058), yc-h/2-11,
                 f'{100*wid:.2f}% of R (≤{100*wid_hi:.2f}% at α_B+1σ)',
                 col, 10.5)
        else:
            text(s, x(base + wid)+9, yc+4, f'{100*wid:.0f}%', col)

    text(s, 20, H-30,
         f'Predicted ÷ simulated = {h_pred/(M.WC01_FINGER_TIPS-base):.3f}. '
         f'α_B = {M.SHIMONY_ALPHA_B} ± {M.SHIMONY_ALPHA_B_ERR} is the BUBBLE '
         'coefficient; the observed quantity is a spike penetration, so the '
         'prediction is a lower bound.', MUT, 10.5)
    text(s, 20, H-14,
         'A ≤ 1 and m(1−m) ≤ ¼ are hard bounds, so no choice of Atwood '
         'number or expansion index closes the gap. Warren et al. read the '
         '0.93 as evidence of cosmic-ray compression, not of mixing.',
         MUT, 10.5)
    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    for name, body in (("m08_fig_jumps.svg", build_jumps()),
                       ("m08_fig_sedov.svg", build_sedov()),
                       ("m08_fig_check.svg", build_check()),
                       ("m08_fig_tycho.svg", build_tycho())):
        with open(name, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"wrote {name} ({len(body)} bytes)")
