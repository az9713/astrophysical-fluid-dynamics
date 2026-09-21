"""Module 13 figures.  Five SVGs, each written from m13_numbers.py's own
functions and constants so that a figure and the prose cannot diverge.

    m13_fig_grey.svg       T(tau_R): ATLAS9 against the grey atmosphere,
                           with the residual panel that IS CHECK 4
    m13_fig_opacity.svg    ATLAS9's kappa_R(tau_R) against the inferred
                           opacity and fully ionised electron scattering:
                           CHECK 2, the anchor
    m13_fig_criterion.svg  omega chi/c_s^2 at three levels: CHECK 3
    m13_fig_eddratio.svg   L/L_Edd on one log axis, section 10
    m13_fig_regimes.svg    the (rho, T) plane and the P_rad = P_gas line,
                           section 11

The CSS counter numbers figures in document order, so the regimes figure,
which Gate D calls Fig. 1, renders as Fig. 5 because it sits in section 11;
the other four render as Figs. 1 to 4.

FIGURE RULES CARRIED FROM MODULES 9 TO 12.
  - check_svg rejects a literal "_" or "^" inside a <text>, so every
    subscript and superscript is a tspan or an entity.
  - A superseded value is drawn HOLLOW and labelled superseded.
  - Shoot the CHECK figures and LOOK at them.
"""
import os

import numpy as np

import m13_numbers as M

HERE = os.path.dirname(os.path.abspath(__file__))


def out(name):
    return os.path.join(HERE, name)


BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"
RED = "#f87171"

SUB = '<tspan baseline-shift="sub" font-size="8">{0}</tspan>'
SUP = '<tspan baseline-shift="super" font-size="8">{0}</tspan>'
TAU_R = '&#964;' + SUB.format('R')
KAP_R = '&#954;' + SUB.format('R')


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def frame(s, X0, Y0, X1, Y1):
    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')


def text(s, x, y, body, size=11, col=FG, anchor="start", cls=None):
    c = f' class="{cls}"' if cls else ''
    s.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
             f'text-anchor="{anchor}" fill="{col}"{c}>{body}</text>')


def xticks_log(s, lo, hi, px, Y1, labels=None):
    for e in range(int(np.ceil(lo)), int(np.floor(hi)) + 1):
        x = px(e)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        lab = labels(e) if labels else f'10{SUP.format(e)}'
        text(s, x, Y1 + 18, lab, 10.5, MUT, "middle")


def yticks_log(s, lo, hi, py, X0, step=1):
    for e in range(int(np.ceil(lo)), int(np.floor(hi)) + 1, step):
        y = py(e)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, X0 - 8, y + 4, f'10{SUP.format(e)}', 10.5, MUT, "end")


def tau_labels(e):
    return {-2: '0.01', -1: '0.1', 0: '1'}.get(e, f'10{SUP.format(e)}')


def write(name, s):
    s.append('</svg>')
    open(out(name), 'w', encoding='utf-8').write("\n".join(s))


# =========================================================================
# Fig. 1 (renders first, section 5).  CHECK 4.  T(tau_R) from ATLAS9 and
# from the grey atmosphere at the file's own Teff = 5777 K, and a residual
# panel carrying the 3.1 per cent band.  THE RESIDUAL PANEL IS THE CHECK.
# =========================================================================

def build_grey():
    W, H = 720, 520
    X0, X1 = 86.0, 640.0
    TY0, TY1 = 30.0, 250.0          # upper panel
    RY0, RY1 = 300.0, 450.0         # residual panel
    LO, HI = -2.0, np.log10(3.0)
    TLO, THI = 4500.0, 7700.0
    RLO, RHI = -4.5, 4.5            # per cent
    TEFF = 5777.0

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    def pyT(v):
        return TY1 - (v - TLO)/(THI - TLO)*(TY1 - TY0)

    def pyR(v):
        return RY1 - (v - RLO)/(RHI - RLO)*(RY1 - RY0)

    lt = np.linspace(LO, HI, 300)
    tau_p, T_p = M.atlas9_profile()[:2]
    T_a9 = np.interp(lt*np.log(10.0), np.log(tau_p), T_p)
    T_gr = M.grey_eddington_T(10.0**lt, TEFF)
    res = 100.0*(T_gr/T_a9 - 1.0)
    assert res.max() < 3.1 and res.min() > -3.1, 'residual left the band'

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="Two stacked panels against Rosseland '
         'optical depth from 0.01 to 3 on a logarithmic axis. The upper '
         'panel shows temperature from the ATLAS9 solar model and from '
         'the grey Eddington atmosphere; the two curves cross near 0.05 '
         'and the grey curve lies below the model deeper in. The lower '
         'panel shows the grey temperature divided by the model '
         'temperature minus one, in per cent, inside a shaded band of '
         'plus and minus 3.1 per cent; the largest excursion is plus 3.0 '
         'per cent at the top." >' % (W, H)]
    frame(s, X0, TY0, X1, TY1)
    frame(s, X0, RY0, X1, RY1)
    # the band first, so everything drawn later sits on it
    s.append(f'<rect x="{X0:.1f}" y="{pyR(3.1):.1f}" width="{X1-X0:.1f}" '
             f'height="{pyR(-3.1)-pyR(3.1):.1f}" fill="{ACC2}" '
             f'opacity="0.12"/>')
    for v in (3.1, -3.1):
        s.append(f'<line x1="{X0:.1f}" y1="{pyR(v):.1f}" x2="{X1:.1f}" '
                 f'y2="{pyR(v):.1f}" stroke="{ACC2}" stroke-width="1" '
                 f'stroke-dasharray="5 4"/>')
    s.append(f'<line x1="{X0:.1f}" y1="{pyR(0):.1f}" x2="{X1:.1f}" '
             f'y2="{pyR(0):.1f}" stroke="{RULE}" stroke-width="1"/>')
    # tau = 2/3, both panels
    x23 = px(np.log10(2.0/3.0))
    for a, b in ((TY0, TY1), (RY0, RY1)):
        s.append(f'<line x1="{x23:.1f}" y1="{a:.0f}" x2="{x23:.1f}" '
                 f'y2="{b:.0f}" stroke="{VIO}" stroke-width="1" '
                 f'stroke-dasharray="3 3"/>')
    xticks_log(s, LO, HI, px, RY1, tau_labels)
    for e in range(-2, 1):
        x = px(e)
        s.append(f'<line x1="{x:.1f}" y1="{TY1:.0f}" x2="{x:.1f}" '
                 f'y2="{TY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
    for v in range(5000, 7700, 500):
        y = pyT(v)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, X0 - 8, y + 4, f'{v}', 10.5, MUT, "end")
    for v in (-3, 0, 3):
        y = pyR(v)
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, X0 - 8, y + 4, f'{v:+d}' if v else '0', 10.5, MUT, "end")

    s.append(f'<path d="{path(px(lt), pyT(T_a9))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.2"/>')
    s.append(f'<path d="{path(px(lt), pyT(T_gr))}" fill="none" '
             f'stroke="{ACC2}" stroke-width="2.2" stroke-dasharray="7 4"/>')
    s.append(f'<path d="{path(px(lt), pyR(res))}" fill="none" '
             f'stroke="{YEL}" stroke-width="2"/>')
    # the seven tabulated levels of the run, as dots on the residual
    for tv in (0.01, 0.1, 0.3, 2.0/3.0, 1.0, 2.0, 3.0):
        r = 100.0*(M.grey_eddington_T(tv, TEFF)
                   / M.atlas9_photosphere(tv)[0] - 1.0)
        s.append(f'<circle cx="{px(np.log10(tv)):.1f}" cy="{pyR(r):.1f}" '
                 f'r="3.4" fill="{YEL}"/>')
    Ta23 = M.atlas9_photosphere(2.0/3.0)[0]
    s.append(f'<circle cx="{x23:.1f}" cy="{pyT(Ta23):.1f}" r="4.2" '
             f'fill="{ACC}"/>')
    s.append(f'<circle cx="{x23:.1f}" cy="{pyT(TEFF):.1f}" r="4.2" '
             f'fill="{ACC2}"/>')

    text(s, px(-1.55), pyT(6900), 'ATLAS9 model, T(' + TAU_R + ')', 11.5,
         ACC)
    text(s, px(-1.55), pyT(6650), 'grey Eddington atmosphere, '
         'T' + SUB.format('eff') + ' = 5777 K', 11.5, ACC2)
    text(s, x23 - 8, pyT(Ta23) - 12,
         f'{Ta23:.1f} K', 10.5, ACC, "end")
    text(s, x23 + 8, pyT(TEFF) + 16, 'T = T' + SUB.format('eff'), 10.5,
         ACC2)
    text(s, x23 - 6, TY0 + 14, TAU_R + ' = 2/3', 10.5, VIO, "end")
    text(s, px(-1.0), pyR(3.1) + 15, '&#177;3.1 per cent band', 10.5,
         ACC2)
    text(s, px(-1.92), pyR(-3.95), 'grey/ATLAS9 &#8722; 1, per cent',
         10.5, YEL)
    text(s, 22, (TY0 + TY1)/2, 'T (K)', 11.5, FG, "middle")
    text(s, (X0 + X1)/2, RY1 + 40, 'Rosseland optical depth ' + TAU_R,
         11.5, FG, "middle")
    write('m13_fig_grey.svg', s)


# =========================================================================
# Fig. 2 (renders second, section 6).  CHECK 2, THE ANCHOR.  kappa_R must
# be seen to DOUBLE across the column the one-scale-height inference
# averages.
# =========================================================================

def build_opacity():
    W, H = 720, 420
    X0, X1, Y0, Y1 = 86.0, 640.0, 44.0, 344.0
    LO, HI = -2.0, np.log10(3.0)
    KLO, KHI = -1.6, 0.9

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    def py(v):
        return Y1 - (v - KLO)/(KHI - KLO)*(Y1 - Y0)

    tau_p, _, _, _, kR = M.atlas9_profile()[:5]
    lt = np.linspace(LO, HI, 300)
    lk = np.interp(lt*np.log(10.0), np.log(tau_p), np.log10(kR))
    k_inf = M.opacity_from_optical_depth(M.M6_PHOT_TAU, M.M6_PHOT_RHO,
                                         M.M6_PHOT_H)
    k_es = M.kappa_electron_scattering(M.X_H)
    Tb, _, _, kb, taub = M.atlas9_photosphere(T_target=M.M6_TEFF)[:5]
    k23 = M.atlas9_photosphere(2.0/3.0)[3]
    k1 = M.atlas9_photosphere(1.0)[3]

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="The Rosseland mean opacity of the ATLAS9 '
         'solar model against Rosseland optical depth, both axes '
         'logarithmic. The curve rises by about two decades from optical '
         'depth 0.01 to 3. Two horizontal dashed lines mark the opacity '
         'inferred from one scale height, 0.152, and the fully ionised '
         'electron-scattering opacity, 0.350. A shaded band between '
         'optical depth 0.543 and 1 shows the model opacity doubling '
         'across the layer the inference averages." >' % (W, H)]
    frame(s, X0, Y0, X1, Y1)
    xa, xb = px(np.log10(taub)), px(0.0)
    s.append(f'<rect x="{xa:.1f}" y="{Y0:.0f}" width="{xb-xa:.1f}" '
             f'height="{Y1-Y0:.0f}" fill="{VIO}" opacity="0.13"/>')
    xticks_log(s, LO, HI, px, Y1, tau_labels)
    for v, lab in ((0.03, '0.03'), (0.1, '0.1'), (0.3, '0.3'), (1, '1'),
                   (3, '3')):
        y = py(np.log10(v))
        s.append(f'<line x1="{X0-5:.0f}" y1="{y:.1f}" x2="{X0:.0f}" '
                 f'y2="{y:.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, X0 - 8, y + 4, lab, 10.5, MUT, "end")
    for kv, col in ((k_inf, ACC2), (k_es, RED)):
        y = py(np.log10(kv))
        s.append(f'<line x1="{X0:.0f}" y1="{y:.1f}" x2="{X1:.0f}" '
                 f'y2="{y:.1f}" stroke="{col}" stroke-width="1.4" '
                 f'stroke-dasharray="6 4"/>')
    s.append(f'<path d="{path(px(lt), py(lk))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.4"/>')
    for tv, kv in ((taub, kb), (2.0/3.0, k23), (1.0, k1)):
        s.append(f'<circle cx="{px(np.log10(tv)):.1f}" '
                 f'cy="{py(np.log10(kv)):.1f}" r="4" fill="{ACC}"/>')

    text(s, px(-1.95), py(np.log10(k_inf)) + 16,
         f'inferred from one scale height, {k_inf:.5f}', 10.5, ACC2)
    text(s, px(-1.95), py(np.log10(k_es)) - 7,
         f'fully ionised electron scattering, X = {M.X_H:.4f}: '
         f'{k_es:.5f}', 10.5, RED)
    text(s, px(-1.9), py(0.3), 'ATLAS9 ' + KAP_R + '(' + TAU_R + ')',
         11.5, ACC)
    text(s, xa + 6, py(np.log10(kb)) + 20, f'{kb:.4f} at T = 5772 K',
         10, ACC)
    text(s, xb + 7, py(np.log10(k1)) + 4, f'{k1:.4f} at ' + TAU_R + ' = 1',
         10, ACC)
    text(s, (xa + xb)/2, Y0 + 14, 'the layer', 10, VIO, "middle")
    text(s, (xa + xb)/2, Y0 + 27, f'&#215;{k1/kb:.2f}', 10, VIO, "middle")
    text(s, X0, Y0 - 12, KAP_R + ' (cm' + SUP.format('2')
         + ' g' + SUP.format('&#8722;1') + ')', 11.5, FG, "middle")
    text(s, (X0 + X1)/2, Y1 + 40, 'Rosseland optical depth ' + TAU_R,
         11.5, FG, "middle")
    write('m13_fig_opacity.svg', s)


# =========================================================================
# Fig. 3 (renders third, section 7).  CHECK 3.  omega chi/c_s^2 at three
# levels, the line at 1, and a shaded << 1 band whose edge is a convention.
# The superseded value is hollow and says so.
# =========================================================================

def build_criterion():
    W, H = 720, 330
    X0, X1, Y0, Y1 = 250.0, 680.0, 30.0, 250.0
    LO, HI = 0.0, 1.2

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    omega = 2.0*np.pi*M.M4_NU_MAX
    k_inf = M.opacity_from_optical_depth(M.M6_PHOT_TAU, M.M6_PHOT_RHO,
                                         M.M6_PHOT_H)
    chi0 = M.radiative_diffusivity(k_inf, M.M6_PHOT_RHO, M.M6_TEFF,
                                   M.M6_PHOT_CP)
    p0 = M.adiabaticity_parameter(omega, chi0, M.M4_SOUND_SPEED)
    Tb, _, rb, kb = M.atlas9_photosphere(T_target=M.M6_TEFF)[:4]
    Ta, _, ra, ka = M.atlas9_photosphere(2.0/3.0)[:4]
    vals = []
    for Tl, rl, kl in ((Tb, rb, kb), (Ta, ra, ka)):
        chi = M.radiative_diffusivity(kl, rl, Tl, M.M6_PHOT_CP)
        vals.append(M.adiabaticity_parameter(omega, chi, M.M4_SOUND_SPEED))
    rows = [('inferred opacity, 0.15231', 'SUPERSEDED by CHECK 2', p0,
             True),
            ('ATLAS9, T = 5772 K', KAP_R + ' = %.4f' % kb, vals[0], False),
            ('ATLAS9, ' + TAU_R + ' = 2/3', KAP_R + ' = %.4f' % ka, vals[1],
             False)]

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="A horizontal axis from 0 to 1.2 of the '
         'adiabaticity parameter at the solar frequency of maximum power. '
         'A shaded strip from 0 to 0.1 marks much less than one, and a '
         'vertical line marks 1. Three rows: a hollow marker at 0.713 '
         'labelled superseded, from the refuted inferred opacity, and '
         'two filled markers at 0.447 and 0.345 from the ATLAS9 model. '
         'None lies in the shaded strip." >' % (W, H)]
    frame(s, X0, Y0, X1, Y1)
    s.append(f'<rect x="{px(0):.1f}" y="{Y0:.0f}" '
             f'width="{px(0.1)-px(0):.1f}" height="{Y1-Y0:.0f}" '
             f'fill="{ACC2}" opacity="0.18"/>')
    s.append(f'<line x1="{px(1):.1f}" y1="{Y0:.0f}" x2="{px(1):.1f}" '
             f'y2="{Y1:.0f}" stroke="{RED}" stroke-width="1.6" '
             f'stroke-dasharray="6 4"/>')
    for v in np.arange(0.0, 1.21, 0.2):
        x = px(v)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, x, Y1 + 18, f'{v:.1f}', 10.5, MUT, "middle")
    for i, (name, note, v, old) in enumerate(rows):
        y = Y0 + 50.0 + i*62.0
        s.append(f'<line x1="{px(0):.1f}" y1="{y:.1f}" x2="{px(v):.1f}" '
                 f'y2="{y:.1f}" stroke="{MUT if old else ACC}" '
                 f'stroke-width="1.2" stroke-dasharray="2 3"/>')
        if old:
            s.append(f'<circle cx="{px(v):.1f}" cy="{y:.1f}" r="6.5" '
                     f'fill="none" stroke="{MUT}" stroke-width="2"/>')
        else:
            s.append(f'<circle cx="{px(v):.1f}" cy="{y:.1f}" r="6.5" '
                     f'fill="{ACC}"/>')
        text(s, px(v) + 11, y - 9, f'{v:.4f}', 11, MUT if old else ACC)
        text(s, X0 - 10, y - 2, name, 11.5, MUT if old else FG, "end")
        text(s, X0 - 10, y + 13, note, 9.5, RED if old else MUT, "end")
    text(s, px(0.05), Y0 - 8, '&#8810; 1', 10.5, ACC2, "middle")
    text(s, px(1) - 6, Y0 - 8, 'the boundary, 1', 10.5, RED, "end")
    text(s, (X0 + X1)/2, Y1 + 42, '&#969;&#967;/c' + SUB.format('s')
         + SUP.format('2') + ' at &#957;' + SUB.format('max')
         + ' = 3090 &#956;Hz', 11.5, FG, "middle")
    text(s, X0 - 230, Y1 + 66, 'The shaded strip ends at 0.1 by '
         'convention: the criterion says much less than one and names '
         'no edge.', 10.5, MUT)
    write('m13_fig_criterion.svg', s)


# =========================================================================
# Fig. 4 (renders fourth, section 10).  L/L_Edd on one log axis.  TWO
# KINDS OF POINT: a measured luminosity over L_Edd, and an accretion rate
# over Mdot_Edd, which is L/L_Edd only if the gas radiates at 0.1.
# =========================================================================

def build_eddratio():
    W, H = 720, 330
    X0, X1, Y0, Y1 = 40.0, 680.0, 40.0, 230.0
    LO, HI = -13.0, 5.0

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    sun = M.eddington_ratio_of_a_star(M.Msun, M.Lsun,
                                      M.kappa_electron_scattering(M.X_H))
    agn = M.eddington_ratio(M.M11_AGN_MDOT, M.M11_AGN_M, M.M9_ETA_ASSUMED)
    bondi = M.M9_K2_MDOT_BONDI/M.eddington_accretion_rate(
        M.M9_K2_M, M.M9_ETA_ASSUMED)
    # (name, value, printed value, is it a rate read at eta_rad = 0.1?)
    pts = [('Sgr A*, X-ray', M.M9_K3_LX_OVER_LEDD,
            '3.70&#215;10' + SUP.format('&#8722;12'), False),
           ('the Sun', sun,
            '%.4f&#215;10' % (sun*1e5) + SUP.format('&#8722;5'), False),
           ('AGN disc, Module 11', agn, '%.6f' % agn, True),
           ('Bondi hole, Module 9', bondi, '%.1f' % bondi, True)]

    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="One logarithmic axis of luminosity over '
         'the Eddington luminosity, from ten to the minus thirteen to ten '
         'to the five. A vertical line marks 1, the limit. Filled circles '
         'mark two measured luminosities, Sagittarius A star at 3.7 times '
         'ten to the minus twelve and the Sun at 2.7 times ten to the '
         'minus five. Open diamonds mark two accretion rates read as '
         'luminosities at efficiency 0.1: the Module 11 disc at 0.1 and '
         'the Module 9 Bondi hole at 3664, above the limit." >' % (W, H)]
    frame(s, X0, Y0, X1, Y1)
    s.append(f'<rect x="{px(0):.1f}" y="{Y0:.0f}" '
             f'width="{X1-px(0):.1f}" height="{Y1-Y0:.0f}" fill="{RED}" '
             f'opacity="0.10"/>')
    s.append(f'<line x1="{px(0):.1f}" y1="{Y0:.0f}" x2="{px(0):.1f}" '
             f'y2="{Y1:.0f}" stroke="{RED}" stroke-width="1.8"/>')
    for e in range(-12, 5, 2):
        x = px(e)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, x, Y1 + 18, f'10{SUP.format(e)}', 10.5, MUT, "middle")
    yc = (Y0 + Y1)/2 + 10
    s.append(f'<line x1="{X0:.0f}" y1="{yc:.1f}" x2="{X1:.0f}" '
             f'y2="{yc:.1f}" stroke="{RULE}" stroke-width="1"/>')
    for i, (name, v, lab, rate) in enumerate(pts):
        x = px(np.log10(v))
        if rate:
            s.append(f'<path d="M {x:.1f},{yc-8:.1f} L {x+8:.1f},{yc:.1f} '
                     f'L {x:.1f},{yc+8:.1f} L {x-8:.1f},{yc:.1f} Z" '
                     f'fill="{BG}" stroke="{ACC2}" stroke-width="2"/>')
        else:
            s.append(f'<circle cx="{x:.1f}" cy="{yc:.1f}" r="7" '
                     f'fill="{ACC}"/>')
        up = i % 2 == 0
        yl = yc - 44 if up else yc + 34
        col = ACC2 if rate else ACC
        anc = "end" if i in (2, 3) else "middle"
        xl = x + (10 if i == 3 else 12 if i == 2 else 0)
        text(s, xl, yl, name, 11, col, anc)
        text(s, xl, yl + 14, lab, 10.5, MUT, anc)
    text(s, px(0) + 6, Y0 + 16, 'L = L' + SUB.format('Edd'), 11, RED)
    text(s, px(0) + 6, Y0 + 30, 'above: no', 10, RED)
    text(s, px(0) + 6, Y0 + 43, 'steady state', 10, RED)
    text(s, (X0 + X1)/2, Y1 + 40, 'L/L' + SUB.format('Edd')
         + ' (filled circle: a measured luminosity; open diamond: '
         + '&#7744;/&#7744;' + SUB.format('Edd') + ' read at '
         + '&#951;' + SUB.format('rad') + ' = 0.1)', 11, FG, "middle")
    write('m13_fig_eddratio.svg', s)


# =========================================================================
# Fig. 5 (renders fifth, section 11).  The (rho, T) plane.  THE LINE HAS
# SLOPE 3 in log rho against log T, and radiation dominates BELOW it, at
# lower density for the temperature.  The shading is on that side.
# =========================================================================

def build_regimes():
    W, H = 720, 440
    X0, X1, Y0, Y1 = 86.0, 640.0, 44.0, 374.0
    LO, HI = 3.5, 8.5           # log10 T
    RLO, RHI = -13.0, 4.0       # log10 rho

    def px(v):
        return X0 + (v - LO)/(HI - LO)*(X1 - X0)

    def py(v):
        return Y1 - (v - RLO)/(RHI - RLO)*(Y1 - Y0)

    lt = np.linspace(LO, HI, 200)
    lr = np.log10(M.prad_equals_pgas_density(10.0**lt, M.M3_MU))
    assert lr.min() > RLO and lr.max() < RHI, 'the line left the box'
    poly = ([(px(a), py(b)) for a, b in zip(lt, lr)]
            + [(X1, Y1), (X0, Y1)])
    s = ['<svg class="setupfig" viewBox="0 0 %d %d" width="100%%" '
         'role="img" aria-label="The density-temperature plane on '
         'logarithmic axes, temperature across and density up. A '
         'straight line of slope 3 marks where radiation pressure equals '
         'gas pressure; the region below it, at lower density for the '
         'temperature, is shaded and labelled radiation dominated. The '
         'Sun\'s centre sits more than three decades above the line and '
         'the photosphere about five decades above it." >' % (W, H)]
    frame(s, X0, Y0, X1, Y1)
    s.append('<path d="M ' + ' L '.join(f'{a:.1f},{b:.1f}' for a, b in poly)
             + f' Z" fill="{VIO}" opacity="0.16"/>')
    s.append(f'<path d="{path(px(lt), py(lr))}" fill="none" '
             f'stroke="{VIO}" stroke-width="2.2"/>')
    for e in range(4, 9):
        x = px(e)
        s.append(f'<line x1="{x:.1f}" y1="{Y1:.0f}" x2="{x:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, x, Y1 + 18, f'10{SUP.format(e)}', 10.5, MUT, "middle")
    yticks_log(s, RLO, RHI, py, X0, step=3)

    Tc, rc = M.M3_T_C, M.M3_RHO_C
    Ta, _, ra = M.atlas9_photosphere(2.0/3.0)[:3]
    ratio_c = rc/M.prad_equals_pgas_density(Tc, M.M3_MU_C)
    for (T, r, name, note) in (
            (Tc, rc, "the Sun's centre (tabulated)",
             f'{ratio_c:.1f} times the line\'s density'),
            (Ta, ra, 'the photosphere, ' + TAU_R + ' = 2/3',
             'P' + SUB.format('rad') + '/P = %.2f&#215;10'
             % (M.radiation_pressure(Ta)/M.atlas9_photosphere(2.0/3.0)[1]
                * 1e5) + SUP.format('&#8722;5'))):
        x, y = px(np.log10(T)), py(np.log10(r))
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" '
                 f'fill="{ACC}"/>')
        anc = "end" if T > 1e6 else "start"
        dx = -10 if T > 1e6 else 10
        text(s, x + dx, y - 4, name, 11, ACC, anc)
        text(s, x + dx, y + 11, note, 10, MUT, anc)
    text(s, px(6.1), py(-8.2), 'P' + SUB.format('rad') + ' &gt; P'
         + SUB.format('gas') + ': radiation dominates', 11.5, VIO)
    text(s, px(4.0), py(1.0), 'P' + SUB.format('gas') + ' &gt; P'
         + SUB.format('rad'), 11.5, FG)
    text(s, px(5.9), py(-2.6), 'P' + SUB.format('rad') + ' = P'
         + SUB.format('gas') + ', slope 3', 10.5, VIO, "end")
    text(s, px(5.9), py(-2.6) + 14, '&#956; = 0.832', 10.5, MUT, "end")
    text(s, X0, Y0 - 12, '&#961; (g cm' + SUP.format('&#8722;3') + ')',
         11.5, FG, "middle")
    text(s, (X0 + X1)/2, Y1 + 40, 'T (K)', 11.5, FG, "middle")
    write('m13_fig_regimes.svg', s)


def main():
    build_grey()
    build_opacity()
    build_criterion()
    build_eddratio()
    build_regimes()
    for n in ('grey', 'opacity', 'criterion', 'eddratio', 'regimes'):
        p = out(f'm13_fig_{n}.svg')
        print(f'  {os.path.basename(p):<26} {os.path.getsize(p):>7} bytes')


if __name__ == '__main__':
    main()
