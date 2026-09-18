"""Build the computed SVG figures for Module 7.

Writes three files:

  m07_fig_growth.svg  the two growth-rate curves the module derives.  Upper
                      panel Rayleigh-Taylor for water held above air, with
                      and without interfacial tension, marking the cutoff
                      wavelength and the fastest-growing wavelength.  Lower
                      panel Kelvin-Helmholtz on the solar interface of
                      PART G, with and without gravity acting ACROSS the
                      interface, marking the two-layer cutoff and the
                      observed wavelength.  The point of the lower panel is
                      that the observed mode sits on the wrong side of a
                      cutoff that the geometry removes.

  m07_fig_check.svg   THE CHECK FIGURE, in residual style.  Upper panel the
                      measured alpha_B with its error bar against the
                      candidate values, in units of the measurement's own
                      sigma: the one panel in this module where a sigma
                      exists.  Lower panel the observed vortex propagation
                      band with BOTH predictions drawn on it, the
                      density-weighted phase speed and the equal-density
                      value, so the reader sees for himself that the band
                      cannot separate them.  Drawing the check that fails
                      to discriminate is the honest thing to draw.

  m07_fig_field.svg   THE SHARP RESULT.  Upper panel the growth rate as a
                      fraction of its field-free value against the field
                      component along the wavevector, which reaches zero at
                      0.0675 gauss.  Lower panel the same bound turned into
                      an angle: how close to perpendicular the wavevector
                      must lie, against the total field strength.

Geometry is computed, never eyeballed.  Every number drawn is produced by
m07_numbers.py, so a figure cannot drift away from the prose.

The Module 1, 2 and 3 lessons are applied.  Labels are placed by arithmetic
and kept inside the plot box, because check_overlap reads geometry rather
than pixels and a label that strays hits the tick text.  And where
agreement is the thing being shown, the panel shows the residual: the upper
panel of m07_fig_check.svg is drawn in units of sigma, not in units of
alpha, because alpha_B = 0.038 against 0.050 means nothing until it is
divided by 0.008.
"""
import re

import numpy as np

import m07_numbers as M

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def axis_box(x0, x1, y0, y1):
    return (f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1-x0:.0f}" '
            f'height="{y1-y0:.0f}" fill="none" stroke="{RULE}" '
            f'stroke-width="1"/>')


# =========================================================================
# Figure 1: the two growth-rate curves
# =========================================================================

def build_growth():
    W, H = 760, 664
    AX0, AX1, AY0, AY1 = 84.0, 706.0, 58.0, 282.0
    BX0, BX1, BY0, BY1 = 84.0, 706.0, 396.0, 566.0

    # ---- upper panel: RT, water over air, with and without tension -------
    drho = M.RHO_WATER - M.RHO_AIR
    lam_c = M.rt_lambda_cut(M.SIGMA_WATER, M.g_earth, drho)
    lam_m = M.rt_lambda_max(M.SIGMA_WATER, M.g_earth, drho)
    Aw = M.atwood(M.RHO_WATER, M.RHO_AIR)
    sig_m = np.sqrt(M.sigma_squared(2*np.pi/lam_m, M.RHO_WATER, M.RHO_AIR,
                                    g=M.g_earth, T=M.SIGMA_WATER))

    LAM_LO, LAM_HI = 0.30, 40.0            # cm
    SMAX = 70.0                            # s^-1

    def ax(lam):
        return (AX0 + (np.log10(lam) - np.log10(LAM_LO))
                / (np.log10(LAM_HI) - np.log10(LAM_LO))*(AX1 - AX0))

    def ay(s):
        return AY1 - s/SMAX*(AY1 - AY0)

    lam = np.logspace(np.log10(LAM_LO), np.log10(LAM_HI), 700)
    k = 2*np.pi/lam
    s_free = np.sqrt(Aw*M.g_earth*k)
    s2_cap = M.sigma_squared(k, M.RHO_WATER, M.RHO_AIR, g=M.g_earth,
                             T=M.SIGMA_WATER)
    s_cap = np.where(s2_cap > 0.0, np.sqrt(np.maximum(s2_cap, 0.0)), 0.0)

    # ---- lower panel: KH on the solar interface --------------------------
    mu_e = M.mu_electron()
    rho_h = mu_e*M.NE_CORONA*M.mu_u
    rho_l = rho_h/np.sqrt(M.OT_EMIS)
    g_surf = M.GMsun/M.Rsun**2
    k_cut = M.kh_k_gravity_cutoff(g_surf, rho_l, rho_h, M.OT_DU)
    lam_cut = 2*np.pi/k_cut

    KLO, KHI = 2.0e8, 3.0e9                # cm, i.e. 2000 to 30000 km
    GMAX = 32.0                            # units of 1e-3 s^-1

    def bx(lm):
        return (BX0 + (np.log10(lm) - np.log10(KLO))
                / (np.log10(KHI) - np.log10(KLO))*(BX1 - BX0))

    def by(s):
        return BY1 - s/GMAX*(BY1 - BY0)

    lm = np.logspace(np.log10(KLO), np.log10(KHI), 700)
    kk = 2*np.pi/lm
    f_dens = np.sqrt(rho_h*rho_l)/(rho_h + rho_l)
    s_nog = kk*f_dens*M.OT_DU*1e3                      # in 1e-3 s^-1
    s2_g = M.sigma_squared(kk, rho_l, rho_h, dU=M.OT_DU, g=g_surf)
    s_g = np.where(s2_g > 0.0, np.sqrt(np.maximum(s2_g, 0.0))*1e3, 0.0)
    sig_obs = 2*np.pi/M.OT_LAMBDA*f_dens*M.OT_DU*1e3

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper panel: Rayleigh-Taylor growth rate '
         f'against wavelength for water held above air, drawn twice, once '
         f'with interfacial tension and once without. Without tension the '
         f'rate rises without limit as the wavelength shortens. With '
         f'tension it peaks at about three centimetres and falls to zero at '
         f'1.71 centimetres. Lower panel: Kelvin-Helmholtz growth rate '
         f'against wavelength for the solar interface of the anchor '
         f'observation, drawn twice, once with gravity acting across the '
         f'interface and once without. Without gravity the rate rises '
         f'steadily as the wavelength shortens; with gravity it falls to '
         f'zero at about five thousand kilometres, which is shorter than '
         f'the seven thousand kilometre wavelength that was observed.">']

    # ================= panel A =================
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-30:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Rayleigh–Taylor: water held '
             f'above air, with and without surface tension</text>')
    s.append(axis_box(AX0, AX1, AY0, AY1))
    for t in (0.3, 1.0, 3.0, 10.0, 30.0):
        x = ax(t)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        lab = f'{t:g}'
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{lab}</text>')
    for v in (0, 20, 40, 60):
        y = ay(v)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{y:.1f}" x2="{AX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{AX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">wavelength λ / cm</text>')
    s.append(f'<text x="{AX0-46:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {AX0-46:.0f} {(AY0+AY1)/2:.0f})">'
             f'σ / s⁻¹</text>')

    keep = s_free <= SMAX
    s.append(f'<path d="{path(ax(lam[keep]), ay(s_free[keep]))}" fill="none" '
             f'stroke="{MUT}" stroke-width="1.8" stroke-dasharray="5 3"/>')
    s.append(f'<path d="{path(ax(lam), ay(s_cap))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.6"/>')

    # the two marked wavelengths, drawn as verticals inside the box
    xc, xm = ax(lam_c), ax(lam_m)
    s.append(f'<line x1="{xc:.1f}" y1="{ay(0.0):.1f}" x2="{xc:.1f}" '
             f'y2="{AY0:.0f}" stroke="{ACC2}" stroke-width="1.6" '
             f'stroke-dasharray="4 3"/>')
    s.append(f'<line x1="{xm:.1f}" y1="{ay(0.0):.1f}" x2="{xm:.1f}" '
             f'y2="{ay(sig_m):.1f}" stroke="{YEL}" stroke-width="1.6" '
             f'stroke-dasharray="4 3"/>')
    s.append(f'<circle cx="{xm:.1f}" cy="{ay(sig_m):.1f}" r="4.2" '
             f'fill="{YEL}"/>')
    # Labels, placed by arithmetic.  Two regions of panel A hold no curve.
    # (i) The bottom-left: left of lambda_c the tension curve is identically
    # zero and the free curve is above sigma = 64, so everything below
    # sigma = 20 and left of x = ax(lambda_c) is empty.  The lambda_c
    # caption goes there.
    s.append(f'<text x="{xc-8:.1f}" y="{ay(16.0):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC2}">λ_c = {lam_c:.2f} cm</text>')
    s.append(f'<text x="{xc-8:.1f}" y="{ay(9.0):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC2}">nothing shorter grows</text>')
    # (ii) The top-right: the tension curve peaks at sigma = 37.2 and the
    # free curve has fallen to sigma = 34.4 by x = 446, so the block of
    # four right-anchored rows between sigma = 45 and sigma = 66 clears
    # both curves everywhere it is drawn.
    for row, (col, txt) in enumerate((
            (MUT, 'σ = √(Agk), no tension'),
            (ACC, 'σ = √(Agk − T_s k³/(ρ_t+ρ_b))'),
            (YEL, f'λ_max = {lam_m:.2f} cm, σ = {sig_m:.1f} s⁻¹ '
                  f'({1e3/sig_m:.0f} ms)'),
            (FG, f'A = {Aw:.4f}, T_s = {M.SIGMA_WATER:g} dyn/cm, 20 °C'))):
        s.append(f'<text x="{AX1-10:.0f}" y="{ay(66.0 - 7.0*row):.1f}" '
                 f'font-size="10.5" text-anchor="end" fill="{col}">'
                 f'{txt}</text>')

    # ================= panel B =================
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-30:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Kelvin–Helmholtz on the CME '
             f'flank: what gravity would do if it acted across the '
             f'interface</text>')
    s.append(axis_box(BX0, BX1, BY0, BY1))
    for t in (2e8, 5e8, 1e9, 2e9):
        x = bx(t)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t/1e5:.0f}</text>')
    for v in (0, 10, 20, 30):
        y = by(v)
        s.append(f'<line x1="{BX0-5:.0f}" y1="{y:.1f}" x2="{BX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{BX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">wavelength λ / km</text>')
    s.append(f'<text x="{BX0-48:.0f}" y="{(BY0+BY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {BX0-48:.0f} {(BY0+BY1)/2:.0f})">'
             f'σ / 10⁻³ s⁻¹</text>')

    keep = s_nog <= GMAX
    s.append(f'<path d="{path(bx(lm[keep]), by(s_nog[keep]))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.6"/>')
    # Draw the stabilised curve only where it is positive, so it does not
    # lie along the axis and give check_overlap a phantom horizontal line.
    pos = s_g > 0.0
    s.append(f'<path d="{path(bx(lm[pos]), by(s_g[pos]))}" fill="none" '
             f'stroke="{ACC2}" stroke-width="2.4" stroke-dasharray="6 3"/>')

    xcut = bx(lam_cut)
    s.append(f'<line x1="{xcut:.1f}" y1="{BY1:.0f}" x2="{xcut:.1f}" '
             f'y2="{BY0:.0f}" stroke="{ACC2}" stroke-width="1.6"/>')
    xobs = bx(M.OT_LAMBDA)
    s.append(f'<line x1="{xobs:.1f}" y1="{BY1:.0f}" x2="{xobs:.1f}" '
             f'y2="{BY0:.0f}" stroke="{VIO}" stroke-width="2"/>')
    s.append(f'<circle cx="{xobs:.1f}" cy="{by(sig_obs):.1f}" r="4.2" '
             f'fill="{VIO}"/>')
    # the gap between cutoff and observation, drawn as a measured bar
    ygap = by(GMAX) + 22.0
    s.append(f'<line x1="{xcut:.1f}" y1="{ygap:.1f}" x2="{xobs:.1f}" '
             f'y2="{ygap:.1f}" stroke="{FG}" stroke-width="1.6"/>')
    s.append(f'<text x="{(xcut+xobs)/2:.1f}" y="{ygap-8:.1f}" font-size="11" '
             f'text-anchor="middle" fill="{FG}">factor '
             f'{M.OT_LAMBDA/lam_cut:.2f}</text>')
    # Label block.  Both curves are steeply falling, so the only region of
    # panel B free of ink over a wide span of x is the upper right: at
    # x = 460 the no-gravity curve is already down to sigma = 5.7 and the
    # stabilised curve has ended, so four right-anchored rows placed
    # between sigma = 24 and sigma = 15 clear everything, and they sit
    # below the measured bar at sigma = 32 + 22 px.
    for row, (col, txt) in enumerate((
            (ACC, 'no gravity across the interface'),
            (ACC2, f'gravity across it: cut off at {lam_cut/1e5:.0f} km'),
            (VIO, f'observed λ = {M.OT_LAMBDA/1e5:.0f} km, '
                  f'σ = {sig_obs:.2f}×10⁻³ s⁻¹'),
            (MUT, f'ΔU = {M.OT_DU/1e5:.0f} km/s, ρ ratio '
                  f'{np.sqrt(M.OT_EMIS):.2f}, n_e = 3×10⁸ cm⁻³'))):
        s.append(f'<text x="{BX1-10:.0f}" y="{by(24.0) + 15.0*row:.1f}" '
                 f'font-size="10.5" text-anchor="end" fill="{col}">'
                 f'{txt}</text>')

    s.append(f'<text x="{BX0-48:.0f}" y="{H-12:.0f}" font-size="10.5" '
             f'fill="{MUT}">Solar inputs: Ofman &amp; Thompson (2011), ApJ '
             f'734, L11. The coronal density is carried from Module 1 and is '
             f'an input, not a measurement; the cutoff moves as n_e⁰.</text>')
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure 2: the check figure, in residual style
# =========================================================================

def build_check():
    W, H = 760, 576
    AX0, AX1, AY0, AY1 = 96.0, 700.0, 74.0, 250.0
    BX0, BX1, BY0, BY1 = 96.0, 700.0, 372.0, 492.0

    # ---- upper panel: alpha_B, drawn in units of its own sigma -----------
    SLO, SHI = -3.5, 3.5                  # sigma
    # Only values PRINTED in Shimony et al. appear here.  The 0.060 and
    # 0.077 that an earlier draft of this figure carried are in no paper
    # this folder holds, and were cut with the prose that used them.
    cands = [(M.ALPHA_SIM, "3D simulations, inferred 0.05/2", ACC2),
             (M.ALPHA_FIT_LO, "their λ=30 µm data", MUT),
             (M.ALPHA_THEORY_3D, "3D immiscible model", VIO)]

    def ax(sg):
        return AX0 + (sg - SLO)/(SHI - SLO)*(AX1 - AX0)

    # ---- lower panel: the phase speed ------------------------------------
    mu_e = M.mu_electron()
    rho_h = mu_e*M.NE_CORONA*M.mu_u
    rho_l = rho_h/np.sqrt(M.OT_EMIS)
    c_ph = M.phase_speed(rho_h, rho_l, 0.0, M.OT_DU)/1e5
    c_a = M.phase_speed(rho_h, rho_h/np.sqrt(M.OT_EMIS_LO), 0.0, M.OT_DU)/1e5
    c_b = M.phase_speed(rho_h, rho_h/np.sqrt(M.OT_EMIS_HI), 0.0, M.OT_DU)/1e5
    c_lo, c_hi = min(c_a, c_b), max(c_a, c_b)
    c_eq = M.OT_DU/2e5
    VLO, VHI = 0.0, 17.0                  # km/s

    def bx(v):
        return BX0 + (v - VLO)/(VHI - VLO)*(BX1 - BX0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper panel: the measured Rayleigh-Taylor '
         f'mixing constant alpha B, drawn with its error bar on an axis '
         f'marked in units of that error bar. Three candidate values are '
         f'marked. The two ends of the factor-of-two discrepancy this '
         f'measurement was meant to close, 0.025 and 0.05, both lie within '
         f'two sigma of it, so it closes neither. Lower '
         f'panel: the observed vortex propagation speed band, from six to '
         f'fourteen kilometres per second, with two predictions drawn on '
         f'it. Both fall inside the band, so the observation cannot '
         f'separate them.">']

    # ================= panel A =================
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-40:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The one place in this module '
             f'where a σ exists: the mixing constant α_B</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-24:.0f}" font-size="10.5" '
             f'text-anchor="middle" fill="{MUT}">measured '
             f'{M.ALPHA_B:.3f} ± {M.ALPHA_B_ERR:.3f}; the axis is the '
             f'distance from that measurement, in its own σ</text>')
    # The span the paper's abstract claims to have closed, drawn as one
    # bracket so the reader sees the measurement reaching both of its ends.
    sg_sim = (M.ALPHA_SIM - M.ALPHA_B)/M.ALPHA_B_ERR
    sg_thy = (M.ALPHA_THEORY_3D - M.ALPHA_B)/M.ALPHA_B_ERR
    s.append(axis_box(AX0, AX1, AY0, AY1))
    # the +/- 1 and 2 sigma bands, drawn from the axis mapping
    s.append(f'<rect x="{ax(-2.0):.1f}" y="{AY0:.0f}" '
             f'width="{ax(2.0)-ax(-2.0):.1f}" height="{AY1-AY0:.0f}" '
             f'fill="{ACC2}" fill-opacity="0.07"/>')
    s.append(f'<rect x="{ax(-1.0):.1f}" y="{AY0:.0f}" '
             f'width="{ax(1.0)-ax(-1.0):.1f}" height="{AY1-AY0:.0f}" '
             f'fill="{ACC2}" fill-opacity="0.10"/>')
    for sg in (-3, -2, -1, 0, 1, 2, 3):
        x = ax(sg)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{sg:+d}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">(candidate α_B − '
             f'{M.ALPHA_B:.3f}) / {M.ALPHA_B_ERR:.3f}</text>')
    # the measurement itself, at zero
    x0 = ax(0.0)
    ymid = AY0 + 30.0
    s.append(f'<line x1="{ax(-1.0):.1f}" y1="{ymid:.1f}" '
             f'x2="{ax(1.0):.1f}" y2="{ymid:.1f}" stroke="{YEL}" '
             f'stroke-width="3"/>')
    for e in (-1.0, 1.0):
        s.append(f'<line x1="{ax(e):.1f}" y1="{ymid-7:.1f}" '
                 f'x2="{ax(e):.1f}" y2="{ymid+7:.1f}" stroke="{YEL}" '
                 f'stroke-width="2"/>')
    s.append(f'<circle cx="{x0:.1f}" cy="{ymid:.1f}" r="5" fill="{YEL}"/>')
    s.append(f'<text x="{ax(1.0)+10:.1f}" y="{ymid+4:.1f}" font-size="10.5" '
             f'fill="{YEL}">α_B = {M.ALPHA_B:.3f} ± {M.ALPHA_B_ERR:.3f}, '
             f'Shimony et al. (2022)</text>')
    # The two-sigma line, drawn ONLY as two short stubs at the top and
    # bottom edges of the box.  A full-height rule crosses every candidate
    # label, and the shaded band already carries the same information.
    x2 = ax(2.0)
    for ya, yb in ((AY0, AY0 + 10.0), (AY1 - 10.0, AY1)):
        s.append(f'<line x1="{x2:.1f}" y1="{ya:.1f}" x2="{x2:.1f}" '
                 f'y2="{yb:.1f}" stroke="{FG}" stroke-width="1.6"/>')
    # candidates, stacked downward on rows computed from the panel height
    # Rows stop 22 px above the axis so the bottom two-sigma stub, which
    # occupies the last 10 px of the box, cannot reach the lowest label.
    ybr = AY1 - 30.0
    s.append(f'<line x1="{ax(sg_sim):.1f}" y1="{ybr:.1f}" '
             f'x2="{ax(sg_thy):.1f}" y2="{ybr:.1f}" stroke="{FG}" '
             f'stroke-width="1.3" stroke-dasharray="4 3"/>')
    for e in (sg_sim, sg_thy):
        s.append(f'<line x1="{ax(e):.1f}" y1="{ybr-4:.1f}" '
                 f'x2="{ax(e):.1f}" y2="{ybr+4:.1f}" stroke="{FG}" '
                 f'stroke-width="1.3"/>')
    s.append(f'<text x="{(ax(sg_sim)+ax(sg_thy))/2:.1f}" y="{ybr+14:.1f}" '
             f'font-size="10" text-anchor="middle" fill="{FG}">the factor 2 '
             f'the abstract says this measurement resolved</text>')
    rows = np.linspace(ymid + 28.0, AY1 - 54.0, len(cands))
    for (val, lab, col), yy in zip(cands, rows):
        sg = (val - M.ALPHA_B)/M.ALPHA_B_ERR
        x = ax(sg)
        s.append(f'<line x1="{x:.1f}" y1="{yy-6:.1f}" x2="{x:.1f}" '
                 f'y2="{yy+6:.1f}" stroke="{col}" stroke-width="2.2"/>')
        verdict = "excluded" if abs(sg) > 2.0 else "not excluded"
        # Put the text on whichever side of the mark has room: the panel is
        # 604 px wide and the longest string is ~230 px, so anything left of
        # x = AX1 - 240 is labelled to the right, the rest to the left.
        if x < AX1 - 246.0:
            s.append(f'<text x="{x+8:.1f}" y="{yy+4:.1f}" font-size="10.5" '
                     f'fill="{col}">{lab} {val:.3f} — {abs(sg):.1f}σ, '
                     f'{verdict}</text>')
        else:
            s.append(f'<text x="{x-8:.1f}" y="{yy+4:.1f}" font-size="10.5" '
                     f'text-anchor="end" fill="{col}">{lab} {val:.3f} — '
                     f'{abs(sg):.1f}σ, {verdict}</text>')

    # ================= panel B =================
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-40:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">A check that does NOT '
             f'discriminate, drawn so that you can see it does not</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-24:.0f}" font-size="10.5" '
             f'text-anchor="middle" fill="{MUT}">the phase speed of the '
             f'vortices: two predictions, one observed band</text>')
    s.append(axis_box(BX0, BX1, BY0, BY1))
    s.append(f'<rect x="{bx(M.OT_VPROP_LO/1e5):.1f}" y="{BY0:.0f}" '
             f'width="{bx(M.OT_VPROP_HI/1e5)-bx(M.OT_VPROP_LO/1e5):.1f}" '
             f'height="{BY1-BY0:.0f}" fill="{VIO}" fill-opacity="0.16"/>')
    for v in (0, 2, 4, 6, 8, 10, 12, 14, 16):
        x = bx(v)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{v}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">propagation speed / '
             f'km s⁻¹</text>')
    # the observed band, labelled inside the shading
    s.append(f'<text x="{(bx(M.OT_VPROP_LO/1e5)+bx(M.OT_VPROP_HI/1e5))/2:.1f}"'
             f' y="{BY0+18:.0f}" font-size="10.5" text-anchor="middle" '
             f'fill="{VIO}">observed, {M.OT_VPROP_LO/1e5:.0f}–'
             f'{M.OT_VPROP_HI/1e5:.0f} km/s</text>')
    # prediction 1: the density-weighted phase speed, with its spread
    yr1 = BY0 + 46.0
    s.append(f'<line x1="{bx(c_lo):.1f}" y1="{yr1:.1f}" x2="{bx(c_hi):.1f}" '
             f'y2="{yr1:.1f}" stroke="{ACC2}" stroke-width="3"/>')
    for e in (c_lo, c_hi):
        s.append(f'<line x1="{bx(e):.1f}" y1="{yr1-6:.1f}" '
                 f'x2="{bx(e):.1f}" y2="{yr1+6:.1f}" stroke="{ACC2}" '
                 f'stroke-width="2"/>')
    s.append(f'<circle cx="{bx(c_ph):.1f}" cy="{yr1:.1f}" r="4.6" '
             f'fill="{ACC2}"/>')
    s.append(f'<text x="{bx(c_hi)+10:.1f}" y="{yr1+4:.1f}" font-size="10.5" '
             f'fill="{ACC2}">ΔU/(1+ρ_h/ρ_l) = {c_ph:.2f} km/s</text>')
    # prediction 2: the equal-density value
    yr2 = BY0 + 76.0
    s.append(f'<circle cx="{bx(c_eq):.1f}" cy="{yr2:.1f}" r="4.6" '
             f'fill="{ACC}"/>')
    s.append(f'<line x1="{bx(c_eq):.1f}" y1="{yr2-7:.1f}" '
             f'x2="{bx(c_eq):.1f}" y2="{yr2+7:.1f}" stroke="{ACC}" '
             f'stroke-width="2"/>')
    s.append(f'<text x="{bx(c_eq)+10:.1f}" y="{yr2+4:.1f}" font-size="10.5" '
             f'fill="{ACC}">equal densities, ΔU/2 = {c_eq:.0f} km/s</text>')
    s.append(f'<text x="{BX0+10:.0f}" y="{BY1-12:.0f}" font-size="10.5" '
             f'fill="{FG}">both land in the band; a band a factor '
             f'{M.OT_VPROP_HI/M.OT_VPROP_LO:.1f} wide cannot separate '
             f'predictions a factor {c_eq/c_ph:.2f} apart</text>')

    s.append(f'<text x="{BX0-88:.0f}" y="{H-28:.0f}" font-size="10.5" '
             f'fill="{MUT}">Upper: Shimony et al. (2022), arXiv:2210.06631 '
             f'(preprint; no journal reference). Lower: Ofman &amp; Thompson '
             f'(2011), ApJ 734, L11,</text>')
    s.append(f'<text x="{BX0-88:.0f}" y="{H-12:.0f}" font-size="10.5" '
             f'fill="{MUT}">whose numbers carry one significant figure and no '
             f'uncertainties, so the lower panel has no σ to draw.</text>')
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure 3: the magnetic bound, which is the sharp result
# =========================================================================

def build_field():
    W, H = 760, 616
    AX0, AX1, AY0, AY1 = 90.0, 700.0, 62.0, 262.0
    BX0, BX1, BY0, BY1 = 90.0, 700.0, 386.0, 536.0

    mu_e = M.mu_electron()
    rho_h = mu_e*M.NE_CORONA*M.mu_u
    rho_l = rho_h/np.sqrt(M.OT_EMIS)
    Bmax = M.b_parallel_max(rho_h, rho_l, M.OT_DU)

    BLO, BHI = 0.0, 0.085                 # gauss
    k_obs = 2*np.pi/M.OT_LAMBDA
    f_dens = np.sqrt(rho_h*rho_l)/(rho_h + rho_l)
    sig0 = k_obs*f_dens*M.OT_DU

    def ax(b):
        return AX0 + (b - BLO)/(BHI - BLO)*(AX1 - AX0)

    def ay(r):
        return AY1 - r*(AY1 - AY0)

    bb = np.linspace(0.0, Bmax, 500)
    s2 = M.sigma_squared(k_obs, rho_l, rho_h, dU=M.OT_DU, B_t=bb, B_b=bb)
    rr = np.sqrt(np.maximum(s2, 0.0))/sig0

    # lower panel: angle window against total field
    TLO, THI = 0.5, 100.0                 # gauss
    ALO, AHI = 0.0, 8.0                   # degrees

    def bx(b):
        return (BX0 + (np.log10(b) - np.log10(TLO))
                / (np.log10(THI) - np.log10(TLO))*(BX1 - BX0))

    def by(a):
        return BY1 - (a - ALO)/(AHI - ALO)*(BY1 - BY0)

    Bt = np.logspace(np.log10(TLO), np.log10(THI), 500)
    ang = np.degrees(np.arcsin(np.clip(Bmax/Bt, 0.0, 1.0)))

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper panel: the Kelvin-Helmholtz growth '
         f'rate as a fraction of its field-free value, against the magnetic '
         f'field component along the wavevector. The curve is a quarter '
         f'circle falling to zero at 0.0675 gauss. Lower panel: the same '
         f'bound expressed as an angle. For a total field of ten gauss the '
         f'wavevector must lie within four tenths of a degree of '
         f'perpendicular to the field.">']

    # ================= panel A =================
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-34:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">What the instability '
             f'measures: the field along the wavevector</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-18:.0f}" font-size="10.5" '
             f'text-anchor="middle" fill="{MUT}">the paper assumed this '
             f'component was zero; undoing the assumption turns the '
             f'observation into a bound</text>')
    s.append(axis_box(AX0, AX1, AY0, AY1))
    s.append(f'<rect x="{ax(Bmax):.1f}" y="{AY0:.0f}" '
             f'width="{AX1-ax(Bmax):.1f}" height="{AY1-AY0:.0f}" '
             f'fill="{ACC}" fill-opacity="0.09"/>')
    for t in (0.00, 0.02, 0.04, 0.06, 0.08):
        x = ax(t)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t:.2f}</text>')
    for v in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = ay(v)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{y:.1f}" x2="{AX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{AX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v:.2f}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">B cos θ, the field along '
             f'k / gauss</text>')
    s.append(f'<text x="{AX0-50:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {AX0-50:.0f} {(AY0+AY1)/2:.0f})">'
             f'σ / σ(B = 0)</text>')
    s.append(f'<path d="{path(ax(bb), ay(rr))}" fill="none" stroke="{ACC2}" '
             f'stroke-width="2.8"/>')
    xb = ax(Bmax)
    s.append(f'<line x1="{xb:.1f}" y1="{AY0:.0f}" x2="{xb:.1f}" '
             f'y2="{AY1:.0f}" stroke="{ACC}" stroke-width="2"/>')
    # Labels.  The curve is above y = ay(0.55) only for B below 0.056 G,
    # x = 492, so the upper-right corner beyond x = 500 is free ink-wise
    # except for the shading, which carries no geometry.
    s.append(f'<text x="{AX1-10:.0f}" y="{ay(0.92):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC}">STABLE: no instability '
             f'possible</text>')
    s.append(f'<text x="{AX1-10:.0f}" y="{ay(0.92)+15:.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC}">B cos θ &gt; '
             f'{Bmax:.4f} G</text>')
    s.append(f'<text x="{ax(0.004):.1f}" y="{ay(0.30):.1f}" font-size="10.5" '
             f'fill="{ACC2}">σ/σ₀ = √(1 − (B cos θ / '
             f'{Bmax:.4f} G)²)</text>')
    s.append(f'<text x="{ax(0.004):.1f}" y="{ay(0.30)+15:.1f}" '
             f'font-size="10.5" fill="{FG}">the vortices were seen, so the '
             f'Sun sits to the LEFT of the line</text>')
    s.append(f'<text x="{ax(0.004):.1f}" y="{ay(0.30)+30:.1f}" '
             f'font-size="10.5" fill="{MUT}">bound ∝ √n_e: '
             f'{Bmax*np.sqrt(1e9/M.NE_CORONA):.3f} G at n_e = 10⁹ cm⁻³</text>')

    # ================= panel B =================
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-34:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">The same bound as an angle: '
             f'how nearly perpendicular k must lie</text>')
    s.append(axis_box(BX0, BX1, BY0, BY1))
    for t in (0.5, 1, 2, 5, 10, 20, 50, 100):
        x = bx(t)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{t:g}</text>')
    for v in (0, 2, 4, 6, 8):
        y = by(v)
        s.append(f'<line x1="{BX0-5:.0f}" y1="{y:.1f}" x2="{BX0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{BX0-9:.0f}" y="{y+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{v}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">total field B / gauss</text>')
    s.append(f'<text x="{BX0-50:.0f}" y="{(BY0+BY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" '
             f'transform="rotate(-90 {BX0-50:.0f} {(BY0+BY1)/2:.0f})">'
             f'90° − θ / degrees</text>')
    keep = ang <= AHI
    s.append(f'<path d="{path(bx(Bt[keep]), by(ang[keep]))}" fill="none" '
             f'stroke="{YEL}" stroke-width="2.8"/>')
    # the 10 gauss reading, marked with a leader inside the box
    a10 = np.degrees(np.arcsin(Bmax/10.0))
    s.append(f'<circle cx="{bx(10.0):.1f}" cy="{by(a10):.1f}" r="4.4" '
             f'fill="{VIO}"/>')
    s.append(f'<line x1="{bx(10.0):.1f}" y1="{by(a10):.1f}" '
             f'x2="{bx(24.0):.1f}" y2="{by(3.0):.1f}" stroke="{VIO}" '
             f'stroke-width="1"/>')
    s.append(f'<text x="{bx(25.0):.1f}" y="{by(3.0)+4:.1f}" font-size="10.5" '
             f'fill="{VIO}">10 G: within {a10:.2f}° of perpendicular</text>')
    s.append(f'<text x="{bx(1.6):.1f}" y="{by(6.6):.1f}" font-size="10.5" '
             f'fill="{FG}">the hydrodynamic rate of Module 7 needs a '
             f'one-degree statement</text>')
    s.append(f'<text x="{bx(1.6):.1f}" y="{by(6.6)+15:.1f}" font-size="10.5" '
             f'fill="{FG}">about a field it never mentions — which is '
             f'Module 12</text>')

    s.append(f'<text x="{BX0-82:.0f}" y="{H-26:.0f}" font-size="10.5" '
             f'fill="{MUT}">Shear ΔU = {M.OT_DU/1e5:.0f} km/s and density '
             f'ratio {np.sqrt(M.OT_EMIS):.2f} from Ofman &amp; Thompson '
             f'(2011), ApJ 734, L11; the absolute density</text>')
    s.append(f'<text x="{BX0-82:.0f}" y="{H-12:.0f}" font-size="10.5" '
             f'fill="{MUT}">n_e = 3×10⁸ cm⁻³ is an input carried from '
             f'Module 1. Equal field on both sides; a one-sided field '
             f'weakens the bound by √2.</text>')
    s.append('</svg>')
    return "\n".join(s)


_TEXT = re.compile(r"(<text\b[^>]*>)(.*?)(</text>)", re.S)
_SUB = re.compile(r"_([A-Za-z]+)")


def subscripts(svg):
    """Turn every x_sub inside <text> content into a real subscript.

    Labels are written with underscores because they read cleanly in the
    source, but check_svg rejects a literal underscore in a rendered label,
    and Unicode has no subscript for most letters (there is no subscript c,
    b or B).  Only text CONTENT is rewritten, never an attribute, so the
    aria-label is untouched.  Ported from m06_build_figs.py.
    """
    def fix(m):
        body = _SUB.sub(
            r'<tspan baseline-shift="sub" font-size="75%">\1</tspan>',
            m.group(2))
        return m.group(1) + body + m.group(3)
    return _TEXT.sub(fix, svg)


if __name__ == "__main__":
    for name, body in (("m07_fig_growth.svg", build_growth()),
                       ("m07_fig_check.svg", build_check()),
                       ("m07_fig_field.svg", build_field())):
        body = subscripts(body)
        with open(name, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"wrote {name} ({len(body)} bytes)")
