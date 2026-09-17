"""Build the computed SVG figures for Module 5.

Writes three files:

  m05_fig_disp.svg    the dispersion relation.  Left panel omega^2 against
                      k^2, which is a STRAIGHT LINE of slope c_s^2 and
                      intercept -4 pi G rho_0, with the unstable half plane
                      shaded.  Right panel the growth rate and the wave
                      frequency either side of k_J, both divided by
                      sqrt(4 pi G rho_0), carrying the k -> 0 plateau and
                      the free-fall rate so that the exact factor
                      pi sqrt(3/8) between them is visible rather than
                      asserted.

  m05_fig_be.svg      the Bonnor-Ebert sphere.  Upper panel the density
                      profile on log-log axes against the singular
                      isothermal sphere it oscillates about.  Lower panel
                      the dimensionless mass m(xi), whose MAXIMUM is the
                      whole criterion, with the critical point marked and
                      Barnard 68 placed on the unstable branch with its
                      error bar.

  m05_fig_check.svg   THE CHECK FIGURE.  Upper panel the fitted xi_max of
                      every row of Kandori et al. (2005) Table 4, each with
                      its quoted error bar, against the computed
                      xi_crit = 6.4508.  Lower panel the anchor: the two
                      stability criteria this module derives, each divided
                      by its own critical value so that 1 is the boundary
                      for both, applied to the same cloud.  They land on
                      opposite sides.

Geometry is computed, never eyeballed.  Every number drawn is produced by
m05_numbers.py, so a figure cannot drift away from the prose.

The Module 1, 2 and 3 lessons are applied here.  Labels are placed by
arithmetic and kept inside the plot box, because check_overlap reads
geometry rather than pixels and a label that strays hits the tick text.
Where agreement or disagreement is the thing being shown, the panel shows
the residual against the boundary rather than the raw quantity: the whole
content of the lower panel of m05_fig_check.svg is that 0.7068 and 1.0696
sit on opposite sides of 1.

One placement note kept for the next module.  xi_crit = 6.4508 and Barnard
68's xi_max = 6.9 differ by 0.7 per cent, which is five pixels on a
full-range logarithmic axis.  Two labels cannot share that corridor, so the
upper panel of m05_fig_be.svg marks only xi_crit and the B68 marker is
moved to the lower panel, where the axis is linear and the two are nine
pixels apart with the label carried out to the right on a leader.
"""
import re

import numpy as np

import m05_numbers as M

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


_TEXT = re.compile(r"(<text\b[^>]*>)(.*?)(</text>)", re.S)
_SUB = re.compile(r"_([A-Za-z]+)")


def subscripts(svg):
    """Turn every x_sub inside <text> content into a real subscript.

    Labels are written with underscores because they read cleanly in the
    source, but check_svg rejects a literal underscore in a rendered label.
    Only text CONTENT is rewritten, never attributes, and the tspan closes
    after the subscript so the rest of the label returns to the baseline.
    """
    def fix(m):
        body = _SUB.sub(r'<tspan baseline-shift="sub" font-size="75%">\1</tspan>',
                        m.group(2))
        return m.group(1) + body + m.group(3)
    return _TEXT.sub(fix, svg)


# =========================================================================
# Figure: the dispersion relation
# =========================================================================

def build_disp():
    W, H = 760, 380
    AX0, AX1, AY0, AY1 = 84.0, 360.0, 60.0, 302.0
    BX0, BX1, BY0, BY1 = 456.0, 734.0, 60.0, 302.0

    # Panel A domain: x = (k/k_J)^2, y = omega^2/(4 pi G rho_0) = x - 1.
    AXD0, AXD1 = 0.0, 2.6
    AYD0, AYD1 = -1.15, 1.6
    # Panel B domain: x = k/k_J, y = |omega|/sqrt(4 pi G rho_0).
    BXD0, BXD1 = 0.0, 2.0
    BYD0, BYD1 = 0.0, 1.3

    ratio = M.tff_over_tgrow()          # pi sqrt(3/8) = 1.9238
    ff_rate = 1.0/ratio                 # the free-fall rate in these units

    # The concrete cloud the figcaption quotes, from m05_numbers.py.
    rho_core = M.rho_from_nH2(1.0e4)
    cs_core = M.sound_speed(10.0, M.MU_MOL)
    lam_core = M.lambda_jeans(cs_core, rho_core)
    MJ_core = M.mass_jeans(cs_core, rho_core)
    tg_core = M.t_grow(rho_core)

    def ax(v):
        return AX0 + (v - AXD0)/(AXD1 - AXD0)*(AX1 - AX0)

    def ay(v):
        return AY1 - (v - AYD0)/(AYD1 - AYD0)*(AY1 - AY0)

    def bx(v):
        return BX0 + (v - BXD0)/(BXD1 - BXD0)*(BX1 - BX0)

    def by(v):
        return BY1 - (v - BYD0)/(BYD1 - BYD0)*(BY1 - BY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Left panel: the square of the frequency '
         f'against the square of the wavenumber for a uniform '
         f'self-gravitating medium. It is a straight line of slope the '
         f'sound speed squared, crossing zero at the Jeans wavenumber, and '
         f'the region below zero is shaded as unstable. Right panel: the '
         f'growth rate below the Jeans wavenumber and the wave frequency '
         f'above it, both divided by the square root of four pi G rho. The '
         f'growth rate rises to a plateau of one as the wavenumber goes to '
         f'zero, and the free-fall rate is drawn as a second horizontal '
         f'line about half as high.">']

    # ---------------- panel A ----------------
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-30:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The dispersion relation is a '
             f'straight line</text>')
    # the unstable half: y < 0, which is x < 1
    s.append(f'<rect x="{ax(0.0):.1f}" y="{ay(0.0):.1f}" '
             f'width="{ax(1.0)-ax(0.0):.1f}" height="{AY1-ay(0.0):.1f}" '
             f'fill="{ACC}" fill-opacity="0.10"/>')
    s.append(f'<rect x="{AX0:.0f}" y="{AY0:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    # zero line
    s.append(f'<line x1="{AX0:.0f}" y1="{ay(0.0):.1f}" x2="{AX1:.0f}" '
             f'y2="{ay(0.0):.1f}" stroke="{RULE}" stroke-width="1"/>')
    for t in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5):
        x = ax(t)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t:.1f}</text>')
    for v in (-1.0, -0.5, 0.0, 0.5, 1.0, 1.5):
        y = ay(v)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{y:.1f}" x2="{AX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{AX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.1f}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">(k / k_J)²</text>')
    s.append(f'<text x="{AX0-50:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {AX0-50:.0f} {(AY0+AY1)/2:.0f})">'
             f'ω² / 4πGρ₀</text>')

    xs = np.array([AXD0, AXD1])
    s.append(f'<path d="{path(ax(xs), ay(xs - 1.0))}" fill="none" '
             f'stroke="{YEL}" stroke-width="2.8"/>')
    s.append(f'<circle cx="{ax(1.0):.1f}" cy="{ay(0.0):.1f}" r="4.5" '
             f'fill="{YEL}"/>')
    # Inside the box, below-right of the crossing: the shaded rectangle
    # stops at x = 1 and the line is above y = 0 for x > 1.
    s.append(f'<text x="{ax(1.06):.1f}" y="{ay(-0.20):.1f}" font-size="10.5" '
             f'fill="{YEL}">k = k_J</text>')

    # Annotations.  The line passes through (0,-1) and (2.6,1.6), so the
    # upper-left corner of the box is empty: at x = 1.1 the line is at
    # y = 0.1, far below the y = 1.42 and y = 1.20 used here.
    s.append(f'<text x="{ax(0.06):.1f}" y="{ay(1.42):.1f}" font-size="10.5" '
             f'fill="{FG}">ω² = c_s²k² − 4πGρ₀</text>')
    s.append(f'<text x="{ax(0.06):.1f}" y="{ay(1.16):.1f}" font-size="10.5" '
             f'fill="{MUT}">slope c_s², intercept −4πGρ₀</text>')
    # The "unstable" caption sits BELOW the line everywhere it extends: the
    # line reaches y = -1.02 only at x = -0.02, outside the box.
    s.append(f'<text x="{ax(0.60):.1f}" y="{ay(-1.02):.1f}" font-size="10.5" '
             f'text-anchor="middle" fill="{ACC}">unstable: ω² &lt; 0</text>')

    # ---------------- panel B ----------------
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-30:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Growth rate, and the two '
             f'timescales</text>')
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" width="{BX1-BX0:.0f}" '
             f'height="{BY1-BY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for t in (0.0, 0.5, 1.0, 1.5, 2.0):
        x = bx(t)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t:.1f}</text>')
    for v in (0.0, 0.25, 0.5, 0.75, 1.0, 1.25):
        y = by(v)
        s.append(f'<line x1="{BX0-5:.0f}" y1="{y:.1f}" x2="{BX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{BX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.2f}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">k / k_J</text>')
    s.append(f'<text x="{BX0-50:.0f}" y="{(BY0+BY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {BX0-50:.0f} {(BY0+BY1)/2:.0f})">'
             f'rate / √(4πGρ₀)</text>')

    # the two horizontal references
    s.append(f'<line x1="{BX0:.0f}" y1="{by(1.0):.1f}" x2="{BX1:.0f}" '
             f'y2="{by(1.0):.1f}" stroke="{MUT}" stroke-width="1.4" '
             f'stroke-dasharray="5 3"/>')
    s.append(f'<line x1="{BX0:.0f}" y1="{by(ff_rate):.1f}" x2="{BX1:.0f}" '
             f'y2="{by(ff_rate):.1f}" stroke="{VIO}" stroke-width="1.4" '
             f'stroke-dasharray="5 3"/>')
    # Both captions sit just above their own line.  The growth curve never
    # exceeds 1, so nothing can reach above the y = 1 line; and over the x
    # range these two labels occupy the growth curve is above 0.84, well
    # clear of the 0.52 line.
    s.append(f'<text x="{BX0+8:.0f}" y="{by(1.0)-7:.1f}" font-size="10.5" '
             f'fill="{MUT}">1 / t_grow, the k → 0 limit</text>')
    s.append(f'<text x="{BX0+8:.0f}" y="{by(ff_rate)-7:.1f}" '
             f'font-size="10.5" fill="{VIO}">1 / t_ff = '
             f'{ff_rate:.4f}</text>')

    kk = np.linspace(0.0, 1.0, 400)
    s.append(f'<path d="{path(bx(kk), by(np.sqrt(1.0 - kk*kk)))}" '
             f'fill="none" stroke="{ACC}" stroke-width="2.8"/>')
    # The wave branch leaves the box at |omega| = 1.3, i.e. k/k_J = 1.6401;
    # it is clipped there by construction rather than by a clip-path,
    # because check_overlap reads coordinates and not ink.
    k_exit = np.sqrt(1.0 + BYD1*BYD1)
    kw = np.linspace(1.0, min(k_exit, BXD1), 400)
    s.append(f'<path d="{path(bx(kw), by(np.sqrt(kw*kw - 1.0)))}" '
             f'fill="none" stroke="{ACC2}" stroke-width="2.8"/>')
    s.append(f'<line x1="{bx(1.0):.1f}" y1="{BY0:.0f}" x2="{bx(1.0):.1f}" '
             f'y2="{BY1:.0f}" stroke="{YEL}" stroke-width="1.6"/>')
    # Inside the box, left of the vertical near the top: the growth curve
    # is below 0.6 for k > 0.8, far under y = 1.22.
    s.append(f'<text x="{bx(1.0)-6:.1f}" y="{by(1.20):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{YEL}">k = k_J</text>')
    # Curve captions.  The growth curve is below 0.44 for k > 0.9 and the
    # wave curve is below 0.44 for k < 1.09, so y = 0.20 and y = 0.34 near
    # the outer edges of each half are clear of both.
    s.append(f'<text x="{bx(0.10):.1f}" y="{by(0.20):.1f}" font-size="10.5" '
             f'fill="{ACC}">growth, λ &gt; λ_J</text>')
    s.append(f'<text x="{bx(1.96):.1f}" y="{by(0.20):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC2}">sound waves, λ &lt; λ_J</text>')

    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure: the Bonnor-Ebert sphere
# =========================================================================

def build_be():
    W, H = 760, 640
    AX0, AX1, AY0, AY1 = 90.0, 700.0, 62.0, 296.0
    BX0, BX1, BY0, BY1 = 90.0, 700.0, 392.0, 578.0

    xi_crit, m_crit, contrast_crit = M.be_critical()
    xs_max, sl_max = M.be_max_slope()
    xi_b68, sig_b68 = M.B68_T4_XI, M.B68_T4_SIG

    # ---- upper panel domain: log10 xi, log10 rho/rho_c
    ALX0, ALX1 = -1.0, np.log10(200.0)
    ALY0, ALY1 = -5.0, 0.15
    # ---- lower panel domain: xi, m(xi)
    BXD0, BXD1 = 0.0, 26.0
    BYD0, BYD1 = 0.60, 1.26

    def ax(v):
        return AX0 + (v - ALX0)/(ALX1 - ALX0)*(AX1 - AX0)

    def ay(v):
        return AY1 - (v - ALY0)/(ALY1 - ALY0)*(AY1 - AY0)

    def bx(v):
        return BX0 + (v - BXD0)/(BXD1 - BXD0)*(BX1 - BX0)

    def by(v):
        return BY1 - (v - BYD0)/(BYD1 - BYD0)*(BY1 - BY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper panel: the density of an isothermal '
         f'self-gravitating sphere divided by its central density, against '
         f'the dimensionless radius, on logarithmic axes. It is flat in the '
         f'core and then falls, oscillating about the singular isothermal '
         f'sphere which is drawn as a dashed line of slope minus two. A '
         f'vertical line marks the critical dimensionless radius 6.4508. '
         f'Lower panel: the dimensionless mass against the dimensionless '
         f'radius. It rises to a maximum of 1.1822 at the critical radius '
         f'and falls again; the stable branch is left of the maximum and '
         f'the unstable branch right of it, and Barnard 68 is marked with '
         f'an error bar on the unstable branch.">']

    # ---------------- panel A ----------------
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-32:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The pressure-bounded '
             f'isothermal sphere has no surface of its own</text>')
    s.append(f'<rect x="{AX0:.0f}" y="{AY0:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for t, lab in ((-1.0, "0.1"), (0.0, "1"), (1.0, "10"), (2.0, "100")):
        x = ax(t)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{lab}</text>')
    for v in (0, -1, -2, -3, -4, -5):
        y = ay(v)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{y:.1f}" x2="{AX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        lab = "1" if v == 0 else "10" + "⁻" + "¹²³⁴⁵"[abs(v)-1]
        s.append(f'<text x="{AX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{lab}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">ξ = r √(4πGρ_c) / c_s</text>')
    s.append(f'<text x="{AX0-52:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {AX0-52:.0f} {(AY0+AY1)/2:.0f})">'
             f'ρ / ρ_c</text>')

    # the singular isothermal sphere, 2/xi^2, drawn only where it is in box
    lx = np.linspace(max(ALX0, np.log10(np.sqrt(2.0/10.0**ALY1))), ALX1, 200)
    s.append(f'<path d="{path(ax(lx), ay(np.log10(2.0) - 2.0*lx))}" '
             f'fill="none" stroke="{MUT}" stroke-width="1.8" '
             f'stroke-dasharray="5 3"/>')

    xi, psi, dpsi = M._XI, M._PSI, M._DPSI
    keep = xi >= 10.0**ALX0
    lxx, lyy = np.log10(xi[keep]), -psi[keep]/np.log(10.0)
    step = max(1, len(lxx)//600)
    s.append(f'<path d="{path(ax(lxx[::step]), ay(lyy[::step]))}" '
             f'fill="none" stroke="{YEL}" stroke-width="2.8"/>')

    # only ONE vertical here: xi_crit and 6.9 are 5 px apart on this axis
    xc = ax(np.log10(xi_crit))
    s.append(f'<line x1="{xc:.1f}" y1="{AY0:.0f}" x2="{xc:.1f}" '
             f'y2="{AY1:.0f}" stroke="{ACC2}" stroke-width="1.8"/>')
    s.append(f'<circle cx="{xc:.1f}" cy="{ay(-np.log10(contrast_crit)):.1f}" '
             f'r="4.5" fill="{ACC2}"/>')
    # Label carried to the right on a leader: the curve at log10 xi > 1.0 is
    # below -1.3 in log10 rho, so y = -0.35 there is empty.
    s.append(f'<line x1="{xc+5:.1f}" y1="{ay(-np.log10(contrast_crit)):.1f}" '
             f'x2="{ax(1.10):.1f}" y2="{ay(-0.45):.1f}" stroke="{ACC2}" '
             f'stroke-width="1"/>')
    s.append(f'<text x="{ax(1.14):.1f}" y="{ay(-0.42):.1f}" '
             f'font-size="10.5" fill="{ACC2}">ξ_crit = {xi_crit:.4f}, '
             f'ρ_c/ρ_R = {contrast_crit:.3f}</text>')
    s.append(f'<text x="{ax(-0.94):.1f}" y="{ay(-0.55):.1f}" '
             f'font-size="10.5" fill="{FG}">flat core</text>')
    s.append(f'<text x="{ax(2.28):.1f}" y="{ay(-4.55):.1f}" '
             f'font-size="10.5" text-anchor="end" fill="{MUT}">'
             f'ρ = c_s²/(2πGr²), slope −2</text>')
    s.append(f'<text x="{ax(2.28):.1f}" y="{ay(-4.80):.1f}" '
             f'font-size="10.5" text-anchor="end" fill="{MUT}">'
             f'steepest local slope {sl_max:.4f} at ξ = {xs_max:.2f}</text>')

    # ---------------- panel B ----------------
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-32:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The criterion is the '
             f'MAXIMUM of the mass, not the mass</text>')
    s.append(f'<rect x="{bx(xi_crit):.1f}" y="{BY0:.0f}" '
             f'width="{BX1-bx(xi_crit):.1f}" height="{BY1-BY0:.0f}" '
             f'fill="{ACC}" fill-opacity="0.08"/>')
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" width="{BX1-BX0:.0f}" '
             f'height="{BY1-BY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for t in (0, 5, 10, 15, 20, 25):
        x = bx(t)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t}</text>')
    for v in (0.7, 0.8, 0.9, 1.0, 1.1, 1.2):
        y = by(v)
        s.append(f'<line x1="{BX0-5:.0f}" y1="{y:.1f}" x2="{BX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{BX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.1f}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">ξ_max</text>')
    s.append(f'<text x="{BX0-52:.0f}" y="{(BY0+BY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {BX0-52:.0f} {(BY0+BY1)/2:.0f})">'
             f'm = M √(G³ P_ext) / c_s⁴</text>')

    xg = np.linspace(1.2, BXD1, 2000)
    mg = np.array([M.be_m(x) for x in xg])
    # Start the curve where it enters the box instead of clipping, so no
    # flat segment is drawn along the lower edge.
    inbox = mg >= BYD0
    xg, mg = xg[inbox], mg[inbox]
    stable = xg <= xi_crit
    s.append(f'<path d="{path(bx(xg[stable]), by(np.clip(mg[stable], BYD0, BYD1)))}" '
             f'fill="none" stroke="{ACC2}" stroke-width="2.8"/>')
    s.append(f'<path d="{path(bx(xg[~stable]), by(np.clip(mg[~stable], BYD0, BYD1)))}" '
             f'fill="none" stroke="{ACC}" stroke-width="2.8"/>')

    # the maximum, and a short dashed rule to the left axis only
    s.append(f'<line x1="{BX0:.0f}" y1="{by(m_crit):.1f}" '
             f'x2="{bx(13.0):.1f}" y2="{by(m_crit):.1f}" stroke="{YEL}" '
             f'stroke-width="1.4" stroke-dasharray="5 3"/>')
    s.append(f'<line x1="{bx(xi_crit):.1f}" y1="{by(m_crit):.1f}" '
             f'x2="{bx(xi_crit):.1f}" y2="{BY1:.0f}" stroke="{YEL}" '
             f'stroke-width="1.4" stroke-dasharray="5 3"/>')
    # Radius 3.5, not 4.5: the critical point and Barnard 68 are 9.4 px
    # apart on this axis, so two 4.5 px dots would touch.
    s.append(f'<circle cx="{bx(xi_crit):.1f}" cy="{by(m_crit):.1f}" r="3.5" '
             f'fill="{YEL}"/>')
    s.append(f'<text x="{BX0+10:.0f}" y="{by(m_crit)-8:.1f}" '
             f'font-size="10.5" fill="{YEL}">m_crit = {m_crit:.4f}</text>')
    s.append(f'<text x="{bx(xi_crit)+8:.1f}" y="{BY1-12:.0f}" '
             f'font-size="10.5" fill="{YEL}">ξ_crit = {xi_crit:.4f}</text>')
    s.append(f'<text x="{bx(0.5):.1f}" y="{BY1-12:.0f}" font-size="10.5" '
             f'fill="{ACC2}">stable</text>')
    s.append(f'<text x="{BX1-10:.0f}" y="{BY1-12:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC}">unstable</text>')

    # Barnard 68 on the unstable branch, with its error bar, labelled out to
    # the right: the curve between xi = 19 and 26 sits near m = 0.85, which
    # is 110 px below the y = 1.22 used for the text.
    mb = M.be_m(xi_b68)
    xb, yb = bx(xi_b68), by(mb)
    s.append(f'<line x1="{bx(xi_b68-sig_b68):.1f}" y1="{yb:.1f}" '
             f'x2="{bx(xi_b68+sig_b68):.1f}" y2="{yb:.1f}" stroke="{VIO}" '
             f'stroke-width="3.2"/>')
    for e in (-sig_b68, sig_b68):
        s.append(f'<line x1="{bx(xi_b68+e):.1f}" y1="{yb-6:.1f}" '
                 f'x2="{bx(xi_b68+e):.1f}" y2="{yb+6:.1f}" stroke="{VIO}" '
                 f'stroke-width="2"/>')
    s.append(f'<circle cx="{xb:.1f}" cy="{yb:.1f}" r="3.5" fill="{VIO}"/>')
    s.append(f'<line x1="{xb+6:.1f}" y1="{yb:.1f}" x2="{bx(18.0):.1f}" '
             f'y2="{by(1.215):.1f}" stroke="{VIO}" stroke-width="1"/>')
    s.append(f'<text x="{BX1-10:.0f}" y="{by(1.225):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{VIO}">Barnard 68: ξ_max = '
             f'{xi_b68} ± {sig_b68}, m = {mb:.4f}</text>')
    s.append(f'<text x="{BX1-10:.0f}" y="{by(1.150):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{MUT}">its mass is only '
             f'{(1.0-mb/m_crit)*100:.2f}% below the maximum</text>')

    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure: the check
# =========================================================================

def build_check():
    W, H = 760, 600
    AX0, AX1, AY0 = 196.0, 700.0, 78.0
    ROW = 17.0
    rows = M.KANDORI_T4
    AY1 = AY0 + (len(rows) - 1)*ROW + 14.0
    BX0, BX1, BY0, BY1 = 196.0, 700.0, 430.0, 530.0

    xi_crit, m_crit, contrast_crit = M.be_critical()

    # ---- upper panel: log xi from 4 to 32
    ALX0, ALX1 = np.log10(4.0), np.log10(32.0)

    def ax(v):
        return AX0 + (np.log10(v) - ALX0)/(ALX1 - ALX0)*(AX1 - AX0)

    # ---- lower panel: quantity divided by its own critical value
    BXD0, BXD1 = 0.60, 1.26

    def bx(v):
        return BX0 + (v - BXD0)/(BXD1 - BXD0)*(BX1 - BX0)

    # the two criteria, both normalised so that > 1 means unstable
    cs_b68 = M.sound_speed(M.B68_T_BE, M.MU_MOL)
    R_b68 = M.B68_R_AU*M.AU
    rhobar = 3.0*M.B68_M*M.Msun/(4.0*np.pi*R_b68**3)
    MJ = M.mass_jeans(cs_b68, rhobar)
    jeans_ratio = M.B68_M*M.Msun/MJ
    be_ratio = M.B68_T4_XI/xi_crit
    be_err = M.B68_T4_SIG/xi_crit

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper panel: the fitted dimensionless '
         f'radius of fifteen Bok globule rows, each with its error bar, '
         f'against a vertical line at the computed critical value 6.4508. '
         f'Most lie to the right of it, on the unstable side. Barnard 68 '
         f'is highlighted. Lower panel: the same cloud judged by the two '
         f'criteria of this module, each divided by its own critical '
         f'value so that one is the boundary. The Jeans criterion puts it '
         f'at 0.71, on the stable side; the Bonnor-Ebert criterion puts it '
         f'at 1.07, on the unstable side.">']

    # ---------------- panel A ----------------
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-40:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Every fitted globule, '
             f'against the stability boundary</text>')
    s.append(f'<rect x="{ax(xi_crit):.1f}" y="{AY0-22:.0f}" '
             f'width="{AX1-ax(xi_crit):.1f}" height="{AY1-AY0+22:.0f}" '
             f'fill="{ACC}" fill-opacity="0.08"/>')
    s.append(f'<rect x="{AX0:.0f}" y="{AY0-22:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0+22:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for t in (4, 5, 6, 8, 10, 15, 20, 30):
        x = ax(float(t))
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">ξ_max, fitted</text>')

    xc = ax(xi_crit)
    s.append(f'<line x1="{xc:.1f}" y1="{AY0-22:.0f}" x2="{xc:.1f}" '
             f'y2="{AY1:.0f}" stroke="{YEL}" stroke-width="2"/>')
    # the boundary caption sits in the 22 px strip above the first row
    s.append(f'<text x="{xc+7:.1f}" y="{AY0-8:.1f}" font-size="10.5" '
             f'fill="{YEL}">ξ_crit = {xi_crit:.4f}   →  unstable</text>')

    for i, (name, th, xi, sig, contrast, label, starless) in enumerate(rows):
        y = AY0 + i*ROW
        b68 = name.startswith("Barnard 68")
        col = VIO if b68 else (ACC if xi > xi_crit else ACC2)
        s.append(f'<text x="{AX0-10:.0f}" y="{y+4:.1f}" font-size="10" '
                 f'text-anchor="end" fill="{FG if b68 else MUT}">'
                 f'{esc(name)}</text>')
        if sig is not None:
            lo, hi = max(xi - sig, 4.05), min(xi + sig, 31.5)
            s.append(f'<line x1="{ax(lo):.1f}" y1="{y:.1f}" '
                     f'x2="{ax(hi):.1f}" y2="{y:.1f}" stroke="{col}" '
                     f'stroke-width="2.6"/>')
            for e in (lo, hi):
                s.append(f'<line x1="{ax(e):.1f}" y1="{y-5:.1f}" '
                         f'x2="{ax(e):.1f}" y2="{y+5:.1f}" stroke="{col}" '
                         f'stroke-width="1.8"/>')
        s.append(f'<circle cx="{ax(xi):.1f}" cy="{y:.1f}" r="4.0" '
                 f'fill="{col}"/>')

    # ---------------- panel B ----------------
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-34:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The anchor: two criteria, '
             f'one cloud, opposite verdicts</text>')
    s.append(f'<rect x="{bx(1.0):.1f}" y="{BY0:.0f}" '
             f'width="{BX1-bx(1.0):.1f}" height="{BY1-BY0:.0f}" '
             f'fill="{ACC}" fill-opacity="0.08"/>')
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" '
             f'width="{bx(1.0)-BX0:.1f}" height="{BY1-BY0:.0f}" '
             f'fill="{ACC2}" fill-opacity="0.08"/>')
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" width="{BX1-BX0:.0f}" '
             f'height="{BY1-BY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    for t in (0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2):
        x = bx(t)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t:.1f}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+38:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">measured quantity ÷ its own '
             f'critical value</text>')

    x1 = bx(1.0)
    s.append(f'<line x1="{x1:.1f}" y1="{BY0:.0f}" x2="{x1:.1f}" '
             f'y2="{BY1:.0f}" stroke="{YEL}" stroke-width="2"/>')
    s.append(f'<text x="{x1-7:.1f}" y="{BY0+15:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC2}">stable ←</text>')
    s.append(f'<text x="{x1+7:.1f}" y="{BY0+15:.0f}" font-size="10.5" '
             f'fill="{ACC}">→ unstable</text>')

    y1, y2 = BY0 + 44.0, BY0 + 78.0
    s.append(f'<text x="{BX0-10:.0f}" y="{y1+4:.0f}" font-size="11" '
             f'text-anchor="end" fill="{FG}">Jeans: M / M_J</text>')
    s.append(f'<circle cx="{bx(jeans_ratio):.1f}" cy="{y1:.0f}" r="5.5" '
             f'fill="{ACC2}"/>')
    s.append(f'<text x="{bx(jeans_ratio):.1f}" y="{y1-11:.0f}" '
             f'font-size="10.5" text-anchor="middle" fill="{ACC2}">'
             f'{jeans_ratio:.4f}</text>')

    s.append(f'<text x="{BX0-10:.0f}" y="{y2+4:.0f}" font-size="11" '
             f'text-anchor="end" fill="{FG}">Bonnor–Ebert: ξ_max / '
             f'ξ_crit</text>')
    s.append(f'<line x1="{bx(be_ratio-be_err):.1f}" y1="{y2:.0f}" '
             f'x2="{bx(be_ratio+be_err):.1f}" y2="{y2:.0f}" stroke="{ACC}" '
             f'stroke-width="3.2"/>')
    for e in (-be_err, be_err):
        s.append(f'<line x1="{bx(be_ratio+e):.1f}" y1="{y2-6:.0f}" '
                 f'x2="{bx(be_ratio+e):.1f}" y2="{y2+6:.0f}" '
                 f'stroke="{ACC}" stroke-width="2"/>')
    s.append(f'<circle cx="{bx(be_ratio):.1f}" cy="{y2:.0f}" r="5.5" '
             f'fill="{ACC}"/>')
    s.append(f'<text x="{bx(be_ratio):.1f}" y="{y2-11:.0f}" '
             f'font-size="10.5" text-anchor="middle" fill="{ACC}">'
             f'{be_ratio:.4f} ± {be_err:.4f}</text>')

    s.append('</svg>')
    return "\n".join(s)

# =========================================================================
# Figure: the outer slope of Barnard 68
# =========================================================================

def build_slope():
    """Local density slope against angular radius: Nielbock et al. (2012)
    eq. (8) fit against the Alves et al. Bonnor-Ebert sphere (xi_max = 6.9
    at 100 arcsec), with the 2.5176 ceiling no isothermal sphere exceeds.
    Angles, not lengths, so neither distance enters."""
    W, H = 760, 330
    AX0, AX1, AY0, AY1 = 90.0, 700.0, 40.0, 270.0
    XD0, XD1, YD0, YD1 = 0.0, 100.0, 0.0, 3.5
    xs_max, ceil = M.be_max_slope()
    th = np.linspace(0.5, 100.0, 400)
    meas = np.array([M.nielbock_slope(t) for t in th])
    be = np.array([M.be_slope(M.B68_T4_XI*t/M.B68_THETA_R) for t in th])

    def ax(v):
        return AX0 + (v - XD0)/(XD1 - XD0)*(AX1 - AX0)

    def ay(v):
        return AY1 - (v - YD0)/(YD1 - YD0)*(AY1 - AY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Local logarithmic density slope of Barnard '
         f'68 against angular radius. The measured profile of Nielbock et al. '
         f'rises above the dashed ceiling of 2.5176 beyond about 46 arcsec and '
         f'reaches 3.24 at 100 arcsec. The Bonnor-Ebert sphere fitted by Alves '
         f'et al. stays below the ceiling everywhere and reaches 2.47 at its '
         f'edge.">']
    s.append(f'<rect x="{AX0:.0f}" y="{AY0:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0:.0f}" fill="none" stroke="{RULE}"/>')
    for t in range(0, 101, 20):
        x = ax(t)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t}</text>')
    for v in (0.0, 1.0, 2.0, 3.0):
        y = ay(v)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{y:.1f}" x2="{AX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}"/>')
        s.append(f'<text x="{AX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.0f}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+40:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">angular radius (arcsec)</text>')
    s.append(f'<text x="{AX0-42:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" transform="rotate(-90 '
             f'{AX0-42:.0f} {(AY0+AY1)/2:.0f})">− d ln n / d ln r</text>')
    yc = ay(ceil)
    s.append(f'<line x1="{AX0:.0f}" y1="{yc:.1f}" x2="{AX1:.0f}" y2="{yc:.1f}" '
             f'stroke="{YEL}" stroke-width="1.5" stroke-dasharray="6 4"/>')
    s.append(f'<polyline points="{" ".join(f"{ax(a):.1f},{ay(b):.1f}" for a, b in zip(th, meas))}" '
             f'fill="none" stroke="{ACC}" stroke-width="2.6"/>')
    s.append(f'<polyline points="{" ".join(f"{ax(a):.1f},{ay(b):.1f}" for a, b in zip(th, be))}" '
             f'fill="none" stroke="{ACC2}" stroke-width="2.6"/>')
    # labels in the empty upper-left and lower-right regions, clear of curves
    s.append(f'<text x="{ax(3):.1f}" y="{ay(3.25):.1f}" font-size="10.5" '
             f'fill="{ACC}">measured, Nielbock et al. (2012) eq. (8): '
             f'{M.nielbock_slope(100.0):.2f} at 100″</text>')
    s.append(f'<line x1="{ax(3):.1f}" y1="{ay(3.05):.1f}" x2="{ax(14):.1f}" '
             f'y2="{ay(3.05):.1f}" stroke="{ACC}" stroke-width="2.6"/>')
    s.append(f'<line x1="{ax(3):.1f}" y1="{ay(2.86):.1f}" x2="{ax(9):.1f}" '
             f'y2="{ay(2.86):.1f}" stroke="{YEL}" stroke-width="1.5" '
             f'stroke-dasharray="6 4"/>')
    s.append(f'<text x="{ax(10.5):.1f}" y="{ay(2.82):.1f}" font-size="10.5" '
             f'fill="{YEL}">ceiling of every isothermal sphere, {ceil:.4f}</text>')
    s.append(f'<text x="{ax(97):.1f}" y="{ay(0.45):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC2}">Bonnor–Ebert, ξ_max = '
             f'{M.B68_T4_XI} at 100″: {M.be_slope(M.B68_T4_XI):.2f} at the edge'
             f'</text>')
    s.append(f'<line x1="{ax(71):.1f}" y1="{ay(0.25):.1f}" x2="{ax(97):.1f}" '
             f'y2="{ay(0.25):.1f}" stroke="{ACC2}" stroke-width="2.6"/>')
    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    for name, body in (("m05_fig_disp.svg", build_disp()),
                       ("m05_fig_be.svg", build_be()),
                       ("m05_fig_check.svg", build_check()),
                       ("m05_fig_slope.svg", build_slope())):
        body = subscripts(body)
        with open(name, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"wrote {name} ({len(body)} bytes)")
