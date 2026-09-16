"""Build the computed SVG figure for Module 2.

Writes m02_fig_flux.svg, in two panels:

  upper  the measured exponent difference alpha - beta, with its formal
         and yearly-variation error bars, against the value 2 that steady
         spherically symmetric continuity demands exactly;
  lower  the mass flux 4 pi r^2 rho v that the same fits imply, divided by
         its value at 1 au, against the flat line continuity demands.

The upper panel was originally drawn as n(r) and v(r) profiles. It was
replaced: alpha is so close to 2 that the fitted density curve, the median
density curve and the exact inverse square lie within two pixels of each
other over the whole range, so the panel showed agreement by making three
curves invisible rather than by measuring the residual.

Geometry is computed, never eyeballed. Every number drawn comes from the
Venzmer & Bothmer (2018) Table 3 coefficients held in m02_numbers.py, and
every percentage matches a line printed by m02_numbers.py.
"""
import numpy as np
from m02_numbers import VB18, HELIOS_RMIN, HELIOS_RMAX, continuity_residual

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"

W, H = 760, 470

# --- panel A: the exponent difference ------------------------------------
AX0, AX1 = 150.0, 694.0
AY0, AY1 = 58.0, 196.0
AD0, AD1 = 1.845, 2.175                 # domain of alpha - beta
AROWS = [("mean fits", "avg", 106.0), ("median fits", "med", 156.0)]
ATICKS = [1.85, 1.90, 1.95, 2.00, 2.05, 2.10, 2.15]

# --- panel B: the mass flux ----------------------------------------------
BX0, BX1 = 92.0, 694.0
BY0, BY1 = 262.0, 392.0
RL0, RL1 = np.log10(0.275), np.log10(1.04)      # log10 r / au
BV0, BV1 = 0.925, 1.075                         # linear, flux / flux(1 au)
RTICKS = [0.3, 0.4, 0.5, 0.6, 0.8, 1.0]

R = np.linspace(HELIOS_RMIN, HELIOS_RMAX, 240)


def adx(d):
    return AX0 + (d-AD0)/(AD1-AD0)*(AX1-AX0)


def rx(r):
    return BX0 + (np.log10(r)-RL0)/(RL1-RL0)*(BX1-BX0)


def by(v):
    return BY1 - (v-BV0)/(BV1-BV0)*(BY1-BY0)


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def build_flux():
    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Upper panel: the difference between the '
         f'fitted radial exponents of solar wind density and speed, for the '
         f'mean and median Helios fits, each with a formal and a '
         f'yearly-variation error bar, compared with the value 2 that '
         f'continuity requires exactly. Lower panel: the mass flux those '
         f'fits imply, divided by its value at 1 au, against the constant '
         f'value continuity requires.">']

    # =============== panel A ===============
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-16:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Measured exponent difference '
             f'α − β, against the exact prediction</text>')
    s.append(f'<rect x="{AX0:.0f}" y="{AY0:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')

    # the prediction: a bright vertical line at exactly 2
    xp = adx(2.0)
    s.append(f'<line x1="{xp:.1f}" y1="{AY0:.0f}" x2="{xp:.1f}" '
             f'y2="{AY1:.0f}" stroke="{YEL}" stroke-width="2"/>')
    s.append(f'<text x="{xp+9:.1f}" y="{AY1-12:.0f}" font-size="11" '
             f'fill="{YEL}">continuity demands exactly 2</text>')

    for t in ATICKS:
        x = adx(t)
        s.append(f'<line x1="{x:.1f}" y1="{AY1:.0f}" x2="{x:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{AY1+18:.0f}" font-size="11" '
                 f'text-anchor="middle" fill="{MUT}">{t:.2f}</text>')

    for label, which, yy in AROWS:
        d, formal, yearly = continuity_residual(which)
        xc = adx(d)
        # yearly-variation bar, thin and long
        s.append(f'<line x1="{adx(d-yearly):.1f}" y1="{yy:.0f}" '
                 f'x2="{adx(d+yearly):.1f}" y2="{yy:.0f}" stroke="{ACC}" '
                 f'stroke-opacity="0.45" stroke-width="2"/>')
        for e in (-yearly, yearly):
            s.append(f'<line x1="{adx(d+e):.1f}" y1="{yy-6:.0f}" '
                     f'x2="{adx(d+e):.1f}" y2="{yy+6:.0f}" stroke="{ACC}" '
                     f'stroke-opacity="0.45" stroke-width="2"/>')
        # formal fit bar, thick and short
        s.append(f'<line x1="{adx(d-formal):.1f}" y1="{yy:.0f}" '
                 f'x2="{adx(d+formal):.1f}" y2="{yy:.0f}" stroke="{ACC}" '
                 f'stroke-width="4"/>')
        s.append(f'<circle cx="{xc:.1f}" cy="{yy:.0f}" r="4.5" '
                 f'fill="{ACC}"/>')
        s.append(f'<text x="{AX0-10:.0f}" y="{yy+4:.0f}" font-size="11.5" '
                 f'text-anchor="end" fill="{FG}">{label}</text>')
        s.append(f'<text x="{AX0-10:.0f}" y="{yy+18:.0f}" font-size="10" '
                 f'text-anchor="end" fill="{MUT}">{d:.3f} '
                 f'({abs(d-2.0)/yearly:.2f}σ)</text>')

    s.append(f'<text x="{AX0+8:.0f}" y="{AY0+18:.0f}" font-size="10" '
             f'fill="{MUT}">thick bar: formal fit σ  ·  pale bar: '
             f'year-to-year σ of the exponents</text>')

    # =============== panel B ===============
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-16:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Mass flux 4πr²ρv implied by '
             f'those fits, divided by its value at 1 au</text>')
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" width="{BX1-BX0:.0f}" '
             f'height="{BY1-BY0:.0f}" fill="none" stroke="{RULE}" '
             f'stroke-width="1"/>')
    s.append(f'<rect x="{BX0:.0f}" y="{by(1.05):.1f}" width="{BX1-BX0:.0f}" '
             f'height="{by(0.95)-by(1.05):.1f}" fill="{ACC2}" '
             f'fill-opacity="0.10"/>')
    for v in (0.95, 1.00, 1.05):
        y = by(v)
        col = YEL if v == 1.0 else RULE
        w = 2.0 if v == 1.0 else 1.0
        s.append(f'<line x1="{BX0:.0f}" y1="{y:.1f}" x2="{BX1:.0f}" '
                 f'y2="{y:.1f}" stroke="{col}" stroke-width="{w}"/>')
        s.append(f'<text x="{BX0-9:.0f}" y="{y+4:.1f}" font-size="11" '
                 f'text-anchor="end" fill="{MUT}">{v:.2f}</text>')
    for r in RTICKS:
        x = rx(r)
        s.append(f'<line x1="{x:.1f}" y1="{BY1:.0f}" x2="{x:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{BY1+18:.0f}" font-size="11" '
                 f'text-anchor="middle" fill="{MUT}">{r:.1f}</text>')

    d_avg, sf_avg, _ = continuity_residual("avg")
    d_med, _, _ = continuity_residual("med")
    hi, lo = R**(2.0-d_avg+sf_avg), R**(2.0-d_avg-sf_avg)
    s.append(f'<path d="{path(rx(R), by(hi))} L '
             + " L ".join(f"{x:.1f},{y:.1f}"
                          for x, y in zip(rx(R[::-1]), by(lo[::-1])))
             + f' Z" fill="{ACC}" fill-opacity="0.13" stroke="none"/>')
    s.append(f'<path d="{path(rx(R), by(R**(2.0-d_avg)))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.2"/>')
    s.append(f'<path d="{path(rx(R), by(R**(2.0-d_med)))}" fill="none" '
             f'stroke="{ACC}" stroke-width="1.6" stroke-dasharray="5 3"/>')

    def pct(x):
        """Signed percentage with a typographic minus, not a hyphen."""
        return f"{x*100:+.1f}".replace("-", "−")

    drift_avg = (HELIOS_RMAX/HELIOS_RMIN)**(2.0-d_avg) - 1.0
    drift_med = (HELIOS_RMAX/HELIOS_RMIN)**(2.0-d_med) - 1.0
    # labels are placed at the right-hand end, where the two curves have
    # converged on 1 and the left-hand end of the panel is left clear
    s.append(f'<text x="{rx(0.33):.1f}" y="{by(R[0]**(2.0-d_avg))+17:.1f}" '
             f'font-size="10.5" fill="{ACC}">mean fit, '
             f'{pct(drift_avg)}% across the range</text>')
    s.append(f'<text x="{rx(0.33):.1f}" y="{by(R[0]**(2.0-d_med))-9:.1f}" '
             f'font-size="10.5" fill="{ACC}">median fit, '
             f'{pct(drift_med)}%</text>')
    s.append(f'<text x="{BX1-8:.0f}" y="{by(1.0)-8:.1f}" font-size="11" '
             f'text-anchor="end" fill="{YEL}">continuity: exactly '
             f'constant</text>')
    s.append(f'<text x="{BX1-8:.0f}" y="{BY0+16:.0f}" font-size="10" '
             f'text-anchor="end" fill="{MUT}">shading: ±1σ on the mean-fit '
             f'exponent  ·  pale band: ±5%</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+40:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">heliocentric distance '
             f'r / au</text>')

    s.append(f'<text x="{BX0-58:.0f}" y="{H-14:.0f}" font-size="10.5" '
             f'fill="{MUT}">Fits: Venzmer &amp; Bothmer (2018), A&amp;A 611, '
             f'A36, Table 3, Helios 1 + 2 over 0.29–0.98 au. Drawn from the '
             f'published power laws, not from the underlying points.</text>')

    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    for name, body in (("m02_fig_flux.svg", build_flux()),):
        with open(name, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"wrote {name} ({len(body)} bytes)")
