"""Build the computed SVG figures for Module 6.

Writes three files:

  m06_fig_brunt.svg   convection in the Sun.  Upper panel the Brunt-Vaisala
                      frequency N(r) read off the BS2005-AGS,OP table, with
                      and without the Ledoux composition term, the maximum
                      marked, and the convection zone shaded where N^2 is
                      zero to the table's precision.  Lower panel the
                      mixing-length superadiabatic excess grad - grad_ad on
                      a log axis, from 1e-7 at the base of the zone to order
                      unity at the photosphere, with the photospheric point
                      computed two ways (all of L, and the measured
                      convective flux of PART D A3).

  m06_fig_phase.svg   the thermal-equilibrium curve P(n) of the neutral ISM
                      from the corrected Koyama-Inutsuka cooling function,
                      the thermally unstable branch (dP/dn < 0, Field's
                      isobaric criterion) drawn separately, P_min and P_max
                      marked, the two-phase window of Wolfire et al. (2003)
                      as a band, and the measured CNM pressures of Jenkins &
                      Tripp (2011) as a bar.

  m06_fig_check.svg   THE ANCHOR, in the residual style of m02_fig_flux.svg.
                      Upper panel the predicted window against the measured
                      pressure distribution on one log axis.  Lower panel
                      the fraction of cold gas below P_min: the static
                      prediction, the fitted lognormal, and the measurements.

Geometry is computed, never eyeballed, and every number drawn is produced
by m06_numbers.py.  Label clearance is TESTED, not assumed: every text
element is registered with an estimated bounding box, and check_labels()
measures its distance to every drawn curve sample (at full resolution, not
the decimated drawing) and to every other label, then prints the result.
A figure with a collision is reported, not silently written.
"""
import numpy as np

import m06_numbers as N

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"

CHAR_W = 0.56          # average glyph advance as a fraction of font size
CLEAR_PX = 4.0         # minimum label-to-curve clearance


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


class Fig:
    """An SVG under construction, with a registry for the clearance test."""

    def __init__(self, name, W, H, aria):
        self.name, self.W, self.H = name, W, H
        self.s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" '
                  f'width="100%" role="img" aria-label="{aria}">']
        self.labels = []          # (x0, y0, x1, y1, text, check_curves)
        self.curves = []          # arrays of (x, y) pixel samples

    def add(self, el):
        self.s.append(el)

    def curve(self, xs, ys):
        self.curves.append(np.column_stack([xs, ys]))

    def text(self, x, y, txt, size=10.5, anchor="start", fill=MUT,
             check=True, extra=""):
        w = len(txt)*size*CHAR_W
        if "rotate(-90" in extra:
            # a middle-anchored title rotated about (x, y): it runs
            # vertically, centred on y, one glyph height to the left of x
            self.labels.append((x - 0.78*size, y - w/2, x + 0.22*size,
                                y + w/2, txt, check))
        else:
            x0 = {"start": x, "middle": x - w/2, "end": x - w}[anchor]
            self.labels.append((x0, y - 0.78*size, x0 + w, y + 0.22*size,
                                txt, check))
        t = (txt.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;"))
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
                 f'text-anchor="{anchor}" fill="{fill}"{extra}>{t}</text>')

    def check_labels(self):
        bad = 0
        for i, (x0, y0, x1, y1, txt, chk) in enumerate(self.labels):
            if x0 < 0 or x1 > self.W or y0 < 0 or y1 > self.H:
                print(f"  [{self.name}] OUTSIDE viewBox: {txt!r}")
                bad += 1
            if chk:
                for c in self.curves:
                    dx = np.maximum(np.maximum(x0 - c[:, 0], 0.0),
                                    c[:, 0] - x1)
                    dy = np.maximum(np.maximum(y0 - c[:, 1], 0.0),
                                    c[:, 1] - y1)
                    d = float(np.min(np.hypot(dx, dy)))
                    if d < CLEAR_PX:
                        print(f"  [{self.name}] label {txt!r} is {d:.1f} px "
                              f"from a curve")
                        bad += 1
            for (a0, b0, a1, b1, t2, _) in self.labels[i+1:]:
                if x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
                    print(f"  [{self.name}] labels overlap: {txt!r} / {t2!r}")
                    bad += 1
        print(f"  [{self.name}] {len(self.labels)} labels, "
              f"{len(self.curves)} curves, {bad} clearance problems")
        return bad

    def svg(self):
        return "\n".join(self.s + ["</svg>"])


def frame(f, x0, y0, x1, y1):
    f.add(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1-x0:.0f}" '
          f'height="{y1-y0:.0f}" fill="none" stroke="{RULE}" '
          f'stroke-width="1"/>')


def xtick(f, x, y1, lab):
    f.add(f'<line x1="{x:.1f}" y1="{y1:.0f}" x2="{x:.1f}" y2="{y1+5:.0f}" '
          f'stroke="{RULE}" stroke-width="1"/>')
    f.text(x, y1 + 18, lab, anchor="middle", check=False)


def ytick(f, x0, y, lab):
    f.add(f'<line x1="{x0-5:.0f}" y1="{y:.1f}" x2="{x0:.0f}" y2="{y:.1f}" '
          f'stroke="{RULE}" stroke-width="1"/>')
    f.text(x0 - 9, y + 4, lab, anchor="end", check=False)


SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def pow10(k):
    return "1" if k == 0 else ("10" if k == 1 else f"10{str(k).translate(SUP)}")


# =========================================================================
# Figure 1: the Brunt-Vaisala frequency and the superadiabatic excess
# =========================================================================

def build_brunt():
    W, H = 760, 640
    AX0, AX1, AY0, AY1 = 84.0, 700.0, 56.0, 276.0
    BX0, BX1, BY0, BY1 = 84.0, 700.0, 376.0, 576.0
    NMAX = 520.0                       # uHz
    RLO, RHI = 0.70, 1.005
    ELO, EHI = -7.3, 0.6               # log10 excess

    ssm = N.load_ssm()
    st = N.structure(ssm)
    r = st["rfrac"]
    rb = N.convection_zone_base(st)
    N2 = N.brunt_vaisala_sq(st["g"], st["HP"], st["plateau"], st["grad"])
    N2L = N.brunt_vaisala_sq(st["g"], st["HP"], st["plateau"], st["grad"],
                             grad_mu=st["grad_mu"])

    def ax(x):
        return AX0 + x*(AX1 - AX0)

    def ay(v):
        return AY1 - v/NMAX*(AY1 - AY0)

    def bx(x):
        return BX0 + (x - RLO)/(RHI - RLO)*(BX1 - BX0)

    def by(v):
        return BY1 - (v - ELO)/(EHI - ELO)*(BY1 - BY0)

    f = Fig("m06_fig_brunt", W, H,
            "Upper panel: the buoyancy frequency N against fractional radius "
            "in a standard solar model. It rises from the centre to a "
            "maximum of 430 microhertz at 0.27 of the solar radius and falls "
            "to the base of the convection zone at 0.727, beyond which it is "
            "zero to the precision of the table. A dashed curve adds the "
            "composition term, which roughly doubles N inside 0.1 of the "
            "radius and makes no difference outside 0.3. Lower panel: the "
            "superadiabatic excess needed to carry the solar luminosity by "
            "mixing-length convection, on a logarithmic axis, rising from "
            "about one part in ten million at the base of the convection zone "
            "to order unity at the photosphere.")

    # ---------------- panel A ----------------
    f.text((AX0+AX1)/2, AY0-28, "Buoyancy frequency through the Sun",
           size=12.5, anchor="middle", fill=FG, check=False)
    f.add(f'<rect x="{ax(rb):.1f}" y="{AY0:.0f}" '
          f'width="{ax(r[-1])-ax(rb):.1f}" height="{AY1-AY0:.0f}" '
          f'fill="{ACC2}" fill-opacity="0.08"/>')
    frame(f, AX0, AY0, AX1, AY1)
    for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        xtick(f, ax(t), AY1, f"{t:.1f}")
    for v in (0, 100, 200, 300, 400, 500):
        ytick(f, AX0, ay(v), f"{v}")
    f.text((AX0+AX1)/2, AY1+36, "r / R", size=11.5, anchor="middle",
           fill=FG, check=False)
    f.text(AX0-50, (AY0+AY1)/2, "N / 2π  (µHz)", size=11.5, anchor="middle",
           fill=FG, check=False,
           extra=f' transform="rotate(-90 {AX0-50:.0f} {(AY0+AY1)/2:.0f})"')

    uhz = 1e6/(2.0*np.pi)
    sel = (r > 0.03) & (r < rb) & np.isfinite(N2) & (N2 > 0)
    xs, ys = ax(r[sel]), ay(np.sqrt(N2[sel])*uhz)
    selL = sel & np.isfinite(N2L) & (N2L > 0) & (r < 0.40)
    xl, yl = ax(r[selL]), ay(np.sqrt(N2L[selL])*uhz)
    f.curve(xs, ys)
    f.curve(xl, yl)
    step = max(1, len(xs)//500)
    f.add(f'<path d="{path(xl[::step], yl[::step])}" fill="none" '
          f'stroke="{ACC2}" stroke-width="1.8" stroke-dasharray="5 3"/>')
    f.add(f'<path d="{path(xs[::step], ys[::step])}" fill="none" '
          f'stroke="{YEL}" stroke-width="2.6"/>')

    rad = (r > 0.05) & (r < 0.65) & np.isfinite(N2)
    idx = np.where(rad)[0]
    imax = idx[int(np.argmax(N2[idx]))]
    Nmax = np.sqrt(N2[imax])
    xm, ym = ax(r[imax]), ay(Nmax*uhz)
    f.add(f'<circle cx="{xm:.1f}" cy="{ym:.1f}" r="4" fill="{YEL}"/>')
    lx, ly = ax(0.28), ay(150.0)
    f.add(f'<line x1="{xm:.1f}" y1="{ym+6:.1f}" x2="{lx+20:.1f}" '
          f'y2="{ly-12:.1f}" stroke="{YEL}" stroke-width="1"/>')
    f.text(lx, ly, f"maximum {Nmax*uhz:.0f} µHz at {r[imax]:.2f} R", fill=YEL)
    f.text(lx, ly + 15,
           f"so every g mode has period > {2*np.pi/Nmax/60:.1f} min",
           fill=MUT)
    f.text(AX0 + 8, AY0 + 16, "with the Ledoux composition term", fill=ACC2)

    f.text(ax(rb) + 8, AY0 + 16, "convection zone", fill=ACC2)
    f.text(ax(rb) + 8, AY1 - 26, "N² = 0 to the", fill=MUT)
    f.text(ax(rb) + 8, AY1 - 11, "table's precision", fill=MUT)
    f.text(ax(rb) - 8, AY1 - 11, f"base {rb:.3f} R", anchor="end", fill=FG)

    # ---------------- panel B ----------------
    f.text((BX0+BX1)/2, BY0-28, "How superadiabatic the convection zone "
           "must be to carry the Sun's luminosity", size=12.5,
           anchor="middle", fill=FG, check=False)
    frame(f, BX0, BY0, BX1, BY1)
    for t in (0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00):
        xtick(f, bx(t), BY1, f"{t:.2f}")
    for k in (-7, -6, -5, -4, -3, -2, -1, 0):
        ytick(f, BX0, by(k), pow10(k))
    f.text((BX0+BX1)/2, BY1+36, "r / R", size=11.5, anchor="middle",
           fill=FG, check=False)
    f.text(BX0-52, (BY0+BY1)/2, "∇ − ∇_ad", size=11.5, anchor="middle",
           fill=FG, check=False,
           extra=f' transform="rotate(-90 {BX0-52:.0f} {(BY0+BY1)/2:.0f})"')

    rows = np.where((r >= rb) & (r <= r[-1]))[0]
    ex = []
    for i in rows:
        d = N.mlt_at(st, r[i], 2.0)
        ex.append(d["excess"])
    ex = np.array(ex)
    xe, ye = bx(r[rows]), by(np.log10(ex))
    f.curve(xe, ye)
    f.add(f'<path d="{path(xe, ye)}" fill="none" stroke="{ACC}" '
          f'stroke-width="2.6"/>')

    d90 = N.mlt_at(st, 0.90, 2.0)
    x9, y9 = bx(d90["rfrac"]), by(np.log10(d90["excess"]))
    f.add(f'<circle cx="{x9:.1f}" cy="{y9:.1f}" r="4" fill="{ACC}"/>')
    mant, expo = f"{d90['excess']:.1e}".split("e")
    f.text(x9 - 10, y9 - 30, f"{mant}×10{str(int(expo)).translate(SUP)} "
           f"at 0.90 R:", anchor="end", fill=ACC)
    f.text(x9 - 10, y9 - 15, "adiabatic to one part in "
           f"{1/d90['excess']/1e5:.0f}×10⁵", anchor="end", fill=MUT)

    xt = bx(r[-1])
    f.add(f'<line x1="{xt:.1f}" y1="{BY0:.0f}" x2="{xt:.1f}" y2="{BY1:.0f}" '
          f'stroke="{RULE}" stroke-width="1" stroke-dasharray="3 3"/>')
    f.text(xt - 6, BY1 - 10, f"table ends {r[-1]:.3f} R", anchor="end",
           fill=MUT)

    ph = N.mlt_photosphere(2.0)
    xp = bx(1.0)
    yp_all = by(np.log10(ph["excess"]))
    x_pl = N.h_pl*N.c/(N.GRAN_LAMBDA*N.kB*N.T_PHOT)
    dlnB = x_pl*np.exp(x_pl)/(np.exp(x_pl) - 1.0)
    dT = N.GRAN_CONTRAST/dlnB*N.T_PHOT
    F_meas = ph["rho"]*N.OBA_UP_LO*ph["cP"]*dT
    ex_meas = N.mlt_excess(ph["rho"], ph["cP"], N.T_PHOT, ph["g"], ph["HP"],
                           2.0, F_meas)
    yp_meas = by(np.log10(ex_meas))
    f.add(f'<circle cx="{xp:.1f}" cy="{yp_all:.1f}" r="4.5" fill="none" '
          f'stroke="{VIO}" stroke-width="2"/>')
    f.add(f'<circle cx="{xp:.1f}" cy="{yp_meas:.1f}" r="4.5" '
          f'fill="{YEL}"/>')
    f.add(f'<line x1="{xp:.1f}" y1="{yp_all+6:.1f}" x2="{xp:.1f}" '
          f'y2="{yp_meas-6:.1f}" stroke="{MUT}" stroke-width="1"/>')
    f.text(xp - 12, yp_all + 4, f"photosphere, carrying all of L: "
           f"{ph['excess']:.2f}", anchor="end", fill=VIO)
    f.text(xp - 12, yp_meas + 4, f"carrying the measured "
           f"{100*F_meas/ph['F']:.1f}% of L: {ex_meas:.3f}", anchor="end",
           fill=YEL)

    f.text(BX0 + 8, BY0 + 16, f"mixing-length theory, α = 2, "
           f"L(r) from the table", fill=ACC)

    f.text(BX0-52, H-12, "Stratification: BS2005-AGS,OP (Bahcall, "
           "Serenelli & Basu 2005). N² uses the measured adiabatic plateau "
           f"∇ = {st['plateau']:.4f}, not 0.4.", fill=MUT, check=False)
    f.check_labels()
    return f.svg()


# =========================================================================
# Figure 2: the thermal-equilibrium curve of the neutral ISM
# =========================================================================

def build_phase():
    W, H = 760, 520
    AX0, AX1, AY0, AY1 = 90.0, 700.0, 56.0, 440.0
    LN0, LN1 = -2.0, 3.3
    LP0, LP1 = 2.4, 4.6

    def ax(ln):
        return AX0 + (ln - LN0)/(LN1 - LN0)*(AX1 - AX0)

    def ay(lp):
        return AY1 - (lp - LP0)/(LP1 - LP0)*(AY1 - AY0)

    tp = N.two_phase_window()
    ln, lp = np.log10(tp["n"]), np.log10(tp["P"])
    inside = (ln >= LN0) & (ln <= LN1) & (lp >= LP0) & (lp <= LP1)
    i_min, i_max = tp["turning"][0], tp["turning"][1]
    idx = np.arange(len(ln))
    unst = inside & (idx >= i_min) & (idx <= i_max)
    cold = inside & (idx <= i_min)
    warm = inside & (idx >= i_max)

    f = Fig("m06_fig_phase", W, H,
            "Thermal-equilibrium pressure against density for neutral "
            "interstellar gas heated by grain photoelectric emission and "
            "cooled by carbon and hydrogen line emission. Pressure rises "
            "along the warm branch to a maximum of about 5000, falls along a "
            "thermally unstable branch, reaches a minimum of about 1600, and "
            "rises again along the cold branch. A horizontal band marks the "
            "two-phase pressure window computed by Wolfire and collaborators, "
            "1960 to 4810. A vertical bar marks the measured cold-gas "
            "pressures of Jenkins and Tripp, centred on 3802 with a spread of "
            "0.175 dex, inside the window.")

    f.text((AX0+AX1)/2, AY0-28, "Thermal equilibrium of neutral "
           "interstellar gas, and where the cold gas is measured",
           size=12.5, anchor="middle", fill=FG, check=False)

    # the Wolfire window, as a band
    yb0, yb1 = ay(np.log10(N.W03_PMAX)), ay(np.log10(N.W03_PMIN))
    f.add(f'<rect x="{AX0:.0f}" y="{yb0:.1f}" width="{AX1-AX0:.0f}" '
          f'height="{yb1-yb0:.1f}" fill="{ACC2}" fill-opacity="0.13"/>')
    frame(f, AX0, AY0, AX1, AY1)
    for k in (-2, -1, 0, 1, 2, 3):
        xtick(f, ax(k), AY1, pow10(k))
    for v in (300, 1000, 3000, 10000, 30000):
        ytick(f, AX0, ay(np.log10(v)), f"{v}")
    f.text((AX0+AX1)/2, AY1+36, "hydrogen density n  (cm⁻³)", size=11.5,
           anchor="middle", fill=FG, check=False)
    f.text(AX0-54, (AY0+AY1)/2, "P / k  (K cm⁻³)", size=11.5,
           anchor="middle", fill=FG, check=False,
           extra=f' transform="rotate(-90 {AX0-54:.0f} {(AY0+AY1)/2:.0f})"')

    for m, col, dash, w in ((warm, ACC, "", 2.6), (cold, ACC, "", 2.6),
                            (unst, VIO, ' stroke-dasharray="6 4"', 2.4)):
        xs, ys = ax(ln[m]), ay(lp[m])
        f.curve(xs, ys)
        step = max(1, len(xs)//600)
        xd = np.append(xs[::step], xs[-1])
        yd = np.append(ys[::step], ys[-1])
        f.add(f'<path d="{path(xd, yd)}" fill="none" stroke="{col}" '
              f'stroke-width="{w}"{dash}/>')

    # turning points
    for lab, nn, pp, dy, anchor, dx in (
            ("P_max", tp["n_pmax"], tp["Pmax"], -12, "end", -8),
            ("P_min", tp["n_pmin"], tp["Pmin"], 20, "start", 8)):
        x, y = ax(np.log10(nn)), ay(np.log10(pp))
        f.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{YEL}"/>')
        f.text(x + dx, y + dy, f"{lab} = {pp:.0f}", anchor=anchor, fill=YEL)

    # branch labels, positioned from the curve itself
    def on_curve(T_target):
        j = int(np.argmin(abs(tp["T"] - T_target)))
        return ax(ln[j]), ay(lp[j])

    xw, yw = on_curve(7400.0)
    f.text(xw + 14, yw + 16, "warm neutral medium", fill=ACC)
    xc, yc = on_curve(33.0)
    f.text(xc - 14, yc, "cold neutral medium", anchor="end", fill=ACC)
    xu, yu = on_curve(1200.0)
    ux, uy = ax(0.30), ay(2.93)
    f.add(f'<line x1="{xu:.1f}" y1="{yu+6:.1f}" x2="{ux+40:.1f}" '
          f'y2="{uy-13:.1f}" stroke="{VIO}" stroke-width="1"/>')
    f.text(ux, uy, "thermally unstable branch:", fill=VIO)
    f.text(ux, uy + 15, "dP/dn < 0, Field (1965) eq. 4b", fill=VIO)

    f.text(AX0 + 8, yb0 + 16, "two-phase window,", fill=ACC2)
    f.text(AX0 + 8, yb0 + 31, "Wolfire et al. (2003)", fill=ACC2)
    f.text(AX0 + 8, yb0 + 46, f"{N.W03_PMIN:.0f} to {N.W03_PMAX:.0f}",
           fill=ACC2)

    # Jenkins & Tripp measured distribution, as a bar in its own column
    xj = ax(2.85)
    lm = N.JT11_LOGP_MEAN
    ls = N.JT11_LOGP_SIG
    yj0, yj1, yjm = ay(lm + ls), ay(lm - ls), ay(lm)
    f.add(f'<line x1="{xj:.1f}" y1="{yj0:.1f}" x2="{xj:.1f}" y2="{yj1:.1f}" '
          f'stroke="{YEL}" stroke-width="3"/>')
    for yy in (yj0, yj1):
        f.add(f'<line x1="{xj-7:.1f}" y1="{yy:.1f}" x2="{xj+7:.1f}" '
              f'y2="{yy:.1f}" stroke="{YEL}" stroke-width="2"/>')
    f.add(f'<circle cx="{xj:.1f}" cy="{yjm:.1f}" r="5" fill="{YEL}"/>')
    f.text(xj - 12, yj1 + 20, "measured CNM pressure,", anchor="end",
           fill=YEL)
    f.text(xj - 12, yj1 + 35, f"median {10**lm:.0f} ± {ls} dex", anchor="end",
           fill=YEL)
    f.text(xj - 12, yj1 + 50, "Jenkins & Tripp (2011)", anchor="end",
           fill=YEL)

    # The source note that used to sit here as two <text> lines is a caption,
    # not a plot annotation, so it lives in the module's <figcaption>.  The
    # exact text, kept here so it survives a fresh session (it is also quoted
    # in .ignore/m06-prep-review.md section 4):
    #
    #   Curve: Koyama & Inutsuka (2002) eq. 4 with the two typographical
    #   corrections printed by Vazquez-Semadeni et al. (2007),
    #   Lambda/Gamma = 10^7 exp(-1.184e5/(T+1000)) + 1.4e-2 sqrt(T)
    #   exp(-92/T) cm^3, Gamma = 2e-26 erg s^-1, equilibrium n = Gamma/Lambda(T).
    f.check_labels()
    return f.svg()


# =========================================================================
# Figure 3: the anchor check, in the residual style
# =========================================================================

def build_check():
    W, H = 760, 590
    AX0, AX1, AY0, AY1 = 250.0, 700.0, 58.0, 218.0
    BX0, BX1, BY0, BY1 = 250.0, 700.0, 306.0, 486.0
    LP0, LP1 = 2.95, 4.25
    FMAX = 40.0

    def ax(lp):
        return AX0 + (lp - LP0)/(LP1 - LP0)*(AX1 - AX0)

    def bx(pc):
        return BX0 + pc/FMAX*(BX1 - BX0)

    tp = N.two_phase_window()
    f = Fig("m06_fig_check", W, H,
            "Upper panel: on a logarithmic pressure axis, the two-phase "
            "window predicted by Wolfire and collaborators from 1960 to 4810 "
            "with its geometric mean 3070, the window from the analytic "
            "cooling fit from 1597 to 5007, and the measured cold-gas "
            "pressure of Jenkins and Tripp at 3802 with a spread of 0.175 dex. "
            "The measurement lies inside both windows. Lower panel: the "
            "fraction of cold gas below the minimum pressure. A static "
            "two-phase medium allows none, the fitted lognormal gives 5 per "
            "cent, and the measurement gives 29 per cent for all sight lines "
            "and 23 per cent for the low-starlight subsample.")

    # ---------------- panel A ----------------
    f.text((AX0+AX1)/2, AY0-18, "CONFIRMED: the measured centre lies inside "
           "the predicted window", size=12.5, anchor="middle", fill=FG,
           check=False)
    frame(f, AX0, AY0, AX1, AY1)
    for v in (1000, 2000, 3000, 5000, 10000, 15000):
        xtick(f, ax(np.log10(v)), AY1, f"{v}")
    f.text((AX0+AX1)/2, AY1+36, "P / k  (K cm⁻³), logarithmic", size=11.5,
           anchor="middle", fill=FG, check=False)

    lm, ls = N.JT11_LOGP_MEAN, N.JT11_LOGP_SIG
    xmed = ax(lm)
    f.add(f'<line x1="{xmed:.1f}" y1="{AY0:.0f}" x2="{xmed:.1f}" '
          f'y2="{AY1:.0f}" stroke="{YEL}" stroke-width="1.2" '
          f'stroke-opacity="0.5"/>')

    rows = [("Wolfire et al. (2003)", "predicted window", 92.0,
             N.W03_PMIN, N.W03_PMAX, ACC2),
            ("Koyama–Inutsuka fit", "window, this module", 138.0,
             tp["Pmin"], tp["Pmax"], ACC)]
    for lab, sub, yy, p0, p1, col in rows:
        x0, x1 = ax(np.log10(p0)), ax(np.log10(p1))
        f.add(f'<line x1="{x0:.1f}" y1="{yy:.0f}" x2="{x1:.1f}" y2="{yy:.0f}" '
              f'stroke="{col}" stroke-width="6" stroke-opacity="0.75"/>')
        for xx in (x0, x1):
            f.add(f'<line x1="{xx:.1f}" y1="{yy-9:.0f}" x2="{xx:.1f}" '
                  f'y2="{yy+9:.0f}" stroke="{col}" stroke-width="2"/>')
        xg = ax(0.5*(np.log10(p0) + np.log10(p1)))
        f.add(f'<line x1="{xg:.1f}" y1="{yy-6:.0f}" x2="{xg:.1f}" '
              f'y2="{yy+6:.0f}" stroke="{BG}" stroke-width="2"/>')
        f.text(AX0-10, yy+4, lab, anchor="end", fill=FG, check=False)
        f.text(AX0-10, yy+18, f"{sub}: {p0:.0f}–{p1:.0f}", anchor="end",
               fill=MUT, check=False)

    yj = 188.0
    f.add(f'<line x1="{ax(lm-ls):.1f}" y1="{yj:.0f}" x2="{ax(lm+ls):.1f}" '
          f'y2="{yj:.0f}" stroke="{YEL}" stroke-width="3"/>')
    for e in (-ls, ls):
        f.add(f'<line x1="{ax(lm+e):.1f}" y1="{yj-7:.0f}" '
              f'x2="{ax(lm+e):.1f}" y2="{yj+7:.0f}" stroke="{YEL}" '
              f'stroke-width="2"/>')
    f.add(f'<circle cx="{xmed:.1f}" cy="{yj:.0f}" r="5" fill="{YEL}"/>')
    f.text(AX0-10, yj+4, "Jenkins & Tripp (2011)", anchor="end", fill=FG,
           check=False)
    f.text(AX0-10, yj+18, f"measured: {10**lm:.0f}, ±{ls} dex", anchor="end",
           fill=MUT, check=False)

    f.text(AX1-8, AY0+16, f"median / predicted mean = {10**lm:.0f} / "
           f"{N.W03_PAVE:.0f} = {10**lm/N.W03_PAVE:.3f}", anchor="end",
           fill=YEL)
    f.text(AX0+8, AY0+16, "notch = geometric mean", fill=MUT)

    # ---------------- panel B ----------------
    f.text((BX0+BX1)/2, BY0-18, "REFUTED: cold gas below P_min, which a "
           "static medium forbids", size=12.5, anchor="middle", fill=FG,
           check=False)
    frame(f, BX0, BY0, BX1, BY1)
    for v in (0, 5, 10, 15, 20, 25, 30, 35, 40):
        xtick(f, bx(v), BY1, f"{v}")
    f.text((BX0+BX1)/2, BY1+36, "per cent of CNM mass below P_min = 1960 "
           "K cm⁻³", size=11.5, anchor="middle", fill=FG, check=False)

    f_below = 100.0*N.jt11_fraction(None, N.W03_PMIN)
    bars = [("static two-phase medium", "prediction", 0.0, MUT),
            ("lognormal fit, their eq. 3", "same survey, fitted", f_below,
             ACC),
            ("measured, all sight lines", "Jenkins & Tripp §10.1.2",
             100.0*N.JT11_FRAC_BELOW_PMIN, YEL),
            ("measured, low starlight", "their abstract",
             100.0*N.JT11_FRAC_BELOW_LOWI, YEL)]
    for k, (lab, sub, val, col) in enumerate(bars):
        yy = BY0 + 30 + k*42
        if val > 0:
            f.add(f'<rect x="{BX0:.0f}" y="{yy-8:.0f}" '
                  f'width="{bx(val)-BX0:.1f}" height="16" fill="{col}" '
                  f'fill-opacity="0.8"/>')
        else:
            f.add(f'<line x1="{BX0:.0f}" y1="{yy-8:.0f}" x2="{BX0:.0f}" '
                  f'y2="{yy+8:.0f}" stroke="{col}" stroke-width="3"/>')
        f.text(AX0-10, yy+1, lab, anchor="end", fill=FG, check=False)
        f.text(AX0-10, yy+15, sub, anchor="end", fill=MUT, check=False)
        f.text(bx(val) + 8, yy + 4, f"{val:.1f}%" if val < 10 else
               f"{val:.0f}%", fill=col)
    ym = BY0 + 30 + 2*42
    f.text(bx(100.0*N.JT11_FRAC_BELOW_PMIN) + 44, ym + 4,
           f"{N.JT11_FRAC_BELOW_PMIN/(f_below/100):.1f} × the fit", fill=FG)

    f.text(20, H-28, "What fails is the word static: Jenkins & Tripp read "
           "the excess as turbulent rarefaction, Mach 1–4. Gas above P_max "
           "is allowed", fill=MUT, check=False)
    f.text(20, H-12, "for the cold phase and is not counted. Window: "
           "Wolfire et al. (2003) Table 3, R = 8.5 kpc, N_cl = 10¹⁹ cm⁻².",
           fill=MUT, check=False)
    f.check_labels()
    return f.svg()


if __name__ == "__main__":
    for name, fn in (("m06_fig_brunt.svg", build_brunt),
                     ("m06_fig_phase.svg", build_phase),
                     ("m06_fig_check.svg", build_check)):
        body = fn()
        with open(name, "w", encoding="utf-8") as fh:
            fh.write(body)
        print(f"wrote {name} ({len(body)} bytes)")
