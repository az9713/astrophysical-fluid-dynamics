"""Build the computed SVG figures for Module 4.

Writes two files:

  m04_fig_disp.svg   the dispersion diagram of vertical sound waves in an
                     isothermal atmosphere at T_eff.  Right half: the
                     propagating branch nu = sqrt(nu_ac^2 + (c k/2 pi)^2)
                     against the uniform-gas line nu = c k/2 pi.  Left half:
                     the evanescent branch, plotted against the decay rate
                     kappa.  The solar nu_max sits on the evanescent branch.

  m04_fig_tau.svg    THE ANCHOR FIGURE.  Left panel: the acoustic radius
                     tau accumulated from the centre, plotted against depth
                     below the surface on a log axis, so that the outer
                     1.7 per cent of the radius, which holds a fifth of tau,
                     is visible.  Right panel: the residual, Delta nu for
                     each closure against the measured and asymptotic
                     values.

Every number drawn comes from m04_numbers.py.  The Module 2 lesson applies:
the agreement or disagreement is a few microhertz, so the right panel plots
Delta nu on a narrow axis rather than tau on a full one.
"""
import numpy as np

import m04_numbers as M

BG, FG, MUT, RULE = "#0f172a", "#cbd5e1", "#94a3b8", "#334155"
ACC, ACC2, VIO, YEL = "#fb923c", "#2dd4bf", "#a78bfa", "#facc15"
BLU, PNK = "#60a5fa", "#f472b6"


def path(xs, ys):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def sub(s):
    return f'<tspan baseline-shift="sub" font-size="8">{s}</tspan>'


# =========================================================================
# Figure: dispersion diagram of the isothermal atmosphere
# =========================================================================

def build_disp():
    W, H = 760, 420
    X0, X1, Y0, Y1 = 90.0, 730.0, 40.0, 340.0
    KMIN, KMAX = -4.0, 6.0          # Mm^-1; negative side is kappa
    NUMAX_AX = 9000.0               # microHz

    g = M.GMsun/M.RSUN_TAB**2
    ssm = M.load_ssm()
    mu = M.mu_neutral(ssm['X'][-1], ssm['Y'][-1])
    nu_ac, c, Hs = M.nu_cutoff(M.TEFF_SUN, mu, 5/3, g)
    kac = 2*np.pi*nu_ac/c*1e8       # Mm^-1, where kappa reaches omega_ac/c

    def x(k):
        return X0 + (k-KMIN)/(KMAX-KMIN)*(X1-X0)

    def y(nu):
        return Y1 - nu/NUMAX_AX*(Y1-Y0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Frequency against vertical wavenumber for '
         f'sound in an isothermal atmosphere at the solar effective '
         f'temperature. To the right of zero the propagating branch lies '
         f'above the straight line of a uniform gas and meets zero '
         f'wavenumber at the cutoff frequency. To the left of zero the '
         f'evanescent branch falls from the cutoff to zero frequency. The '
         f'solar frequency of maximum power lies on the evanescent branch.">']
    s.append(f'<rect x="{X0:.0f}" y="{Y0:.0f}" width="{X1-X0:.0f}" '
             f'height="{Y1-Y0:.0f}" fill="none" stroke="{RULE}"/>')
    # evanescent region below the cutoff
    s.append(f'<rect x="{X0:.0f}" y="{y(nu_ac*1e6):.1f}" '
             f'width="{X1-X0:.0f}" height="{Y1-y(nu_ac*1e6):.1f}" '
             f'fill="{VIO}" fill-opacity="0.08"/>')
    for k in range(-4, 7, 2):
        xx = x(k)
        s.append(f'<line x1="{xx:.1f}" y1="{Y1:.0f}" x2="{xx:.1f}" '
                 f'y2="{Y1+5:.0f}" stroke="{RULE}"/>')
        s.append(f'<text x="{xx:.1f}" y="{Y1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{abs(k)}</text>')
    for nu in range(0, 9001, 1500):
        yy = y(nu)
        s.append(f'<line x1="{X0-5:.0f}" y1="{yy:.1f}" x2="{X0:.0f}" '
                 f'y2="{yy:.1f}" stroke="{RULE}"/>')
        s.append(f'<text x="{X0-9:.0f}" y="{yy+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{nu}</text>')
    s.append(f'<line x1="{x(0):.1f}" y1="{Y0:.0f}" x2="{x(0):.1f}" '
             f'y2="{Y1:.0f}" stroke="{RULE}" stroke-width="1.2"/>')
    s.append(f'<text x="{(x(KMIN)+x(0))/2:.0f}" y="{Y1+38:.0f}" '
             f'font-size="11.5" text-anchor="middle" fill="{FG}">'
             f'decay rate κ / Mm⁻¹ (evanescent)</text>')
    s.append(f'<text x="{(x(0)+x(KMAX))/2:.0f}" y="{Y1+38:.0f}" '
             f'font-size="11.5" text-anchor="middle" fill="{FG}">'
             f'vertical wavenumber k / Mm⁻¹ (propagating)</text>')
    s.append(f'<text x="{X0-58:.0f}" y="{(Y0+Y1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" transform="rotate(-90 '
             f'{X0-58:.0f} {(Y0+Y1)/2:.0f})">frequency ν / μHz</text>')

    # uniform gas line
    kk = np.linspace(0, KMAX, 100)
    nu_u = c*kk*1e-8/(2*np.pi)*1e6
    keep = nu_u <= NUMAX_AX
    s.append(f'<path d="{path(x(kk[keep]), y(nu_u[keep]))}" fill="none" '
             f'stroke="{MUT}" stroke-width="1.8" stroke-dasharray="5 4"/>')
    # propagating branch
    nu_p = np.sqrt((nu_ac*1e6)**2 + nu_u**2)
    keep = nu_p <= NUMAX_AX
    s.append(f'<path d="{path(x(kk[keep]), y(nu_p[keep]))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.6"/>')
    # evanescent branch, kappa from 0 to kac
    ka = np.linspace(0, kac, 120)
    nu_e = np.sqrt(np.clip((nu_ac*1e6)**2 - (c*ka*1e-8/(2*np.pi)*1e6)**2,
                           0, None))
    s.append(f'<path d="{path(x(-ka), y(nu_e))}" fill="none" '
             f'stroke="{ACC2}" stroke-width="2.6"/>')
    # cutoff line
    yc = y(nu_ac*1e6)
    s.append(f'<line x1="{X0:.0f}" y1="{yc:.1f}" x2="{X1:.0f}" '
             f'y2="{yc:.1f}" stroke="{VIO}" stroke-width="1.4" '
             f'stroke-dasharray="3 3"/>')
    s.append(f'<text x="{X1-8:.0f}" y="{yc+16:.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{VIO}">ν{sub("ac")} = c/(4πH) = '
             f'{nu_ac*1e6:.0f} μHz at T{sub("eff")}</text>')
    # nu_max on the evanescent branch
    om = 2*np.pi*M.NUMAX_MEAS
    kap = np.sqrt((2*np.pi*nu_ac)**2 - om**2)/c*1e8
    xm, ym = x(-kap), y(M.NUMAX_MEAS*1e6)
    s.append(f'<circle cx="{xm:.1f}" cy="{ym:.1f}" r="5" fill="{YEL}"/>')
    s.append(f'<line x1="{X0:.0f}" y1="{ym:.1f}" x2="{xm-7:.1f}" '
             f'y2="{ym:.1f}" stroke="{YEL}" stroke-width="1" '
             f'stroke-dasharray="2 3"/>')
    s.append(f'<text x="{X0+8:.0f}" y="{ym+18:.1f}" font-size="10.5" '
             f'fill="{YEL}">ν{sub("max")} = 3090 μHz, κ = {kap:.2f} Mm⁻¹'
             f'</text>')
    s.append(f'<text x="{X0+8:.0f}" y="{ym+33:.1f}" font-size="10.5" '
             f'fill="{YEL}">(the 5-minute modes)</text>')
    # labels for the branches
    s.append(f'<text x="{x(3.2):.1f}" y="{y(8200):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{ACC}">stratified gas</text>')
    s.append(f'<text x="{x(5.9):.1f}" y="{y(5600):.1f}" font-size="10.5" '
             f'text-anchor="end" fill="{MUT}">uniform gas, ν = ck/2π</text>')
    s.append(f'<text x="{x(-2.3):.1f}" y="{y(6000):.1f}" font-size="10.5" '
             f'text-anchor="middle" fill="{ACC2}">evanescent branch</text>')
    s.append(f'<text x="{X0+8:.0f}" y="{H-16:.0f}" font-size="10.5" '
             f'fill="{MUT}">c = {c/1e5:.3f} km/s, H = {Hs/1e5:.1f} km, '
             f'Γ{sub("1")} = 5/3, μ = {mu:.3f} (neutral surface mixture)'
             f'</text>')
    s.append('</svg>')
    return "\n".join(s)


# =========================================================================
# Figure: the acoustic radius and the large separation
# =========================================================================

def build_tau():
    W, H = 760, 408
    AX0, AX1, AY0, AY1 = 72.0, 380.0, 40.0, 330.0
    BX0, BX1, BY0, BY1 = 440.0, 734.0, 40.0, 330.0
    LD0, LD1 = 0.0, -4.0             # log10 depth, centre to 1e-4 R
    TMAX = 4000.0

    ssm = M.load_ssm()
    R = ssm['r']*M.RSUN_TAB
    depth_tab = 1 - ssm['r']
    cum = {}
    for g1 in (5/3, 1.0):
        ic = 1/np.sqrt(g1*ssm['P']/ssm['rho'])
        seg = 0.5*(ic[1:]+ic[:-1])*np.diff(R)
        cum[g1] = np.concatenate([[R[0]*ic[0]], R[0]*ic[0]+np.cumsum(seg)])
    tau_ad = cum[5/3][-1]
    depth = M.RSUN_TAB*(1 - ssm['r'][-1])
    T_top = ssm['T'][-1]
    mu_i = M.mu_fully_ionised(ssm['X'][-1], ssm['Y'][-1])
    mu_n = M.mu_neutral(ssm['X'][-1], ssm['Y'][-1])
    tau_meas = 1/(2*M.DNU_MEAS)
    dnu_as = (1 + M.ZETA_SUN)*M.DNU_MEAS
    tau_as = 1/(2*dnu_as)

    def ax(ld):
        return AX0 + (ld-LD0)/(LD1-LD0)*(AX1-AX0)

    def ay(t):
        return AY1 - t/TMAX*(AY1-AY0)

    s = [f'<svg class="setupfig" viewBox="0 0 {W} {H}" width="100%" '
         f'role="img" aria-label="Left panel: acoustic radius accumulated '
         f'from the centre of the tabulated solar model against depth below '
         f'the surface on a logarithmic axis, for the adiabatic and the '
         f'isothermal sound speed, with the extension through the '
         f'untabulated outer layer for two gas models and the totals the '
         f'measurement requires. Right panel: the large separation implied '
         f'by each case against the measured and the asymptotic values.">']

    # ---------------- panel A ----------------
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY0-16:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Acoustic radius from the '
             f'centre</text>')
    s.append(f'<rect x="{AX0:.0f}" y="{AY0:.0f}" width="{AX1-AX0:.0f}" '
             f'height="{AY1-AY0:.0f}" fill="none" stroke="{RULE}"/>')
    # the untabulated layer as a band
    xl = ax(np.log10(1 - ssm['r'][-1]))
    s.append(f'<rect x="{xl:.1f}" y="{AY0:.0f}" width="{AX1-xl:.1f}" '
             f'height="{AY1-AY0:.0f}" fill="{VIO}" fill-opacity="0.10"/>')
    for ld, lab in ((0, '1'), (-1, '0.1'), (-2, '0.01'), (-3, '10⁻³'),
                    (-4, '10⁻⁴')):
        xx = ax(ld)
        s.append(f'<line x1="{xx:.1f}" y1="{AY1:.0f}" x2="{xx:.1f}" '
                 f'y2="{AY1+5:.0f}" stroke="{RULE}"/>')
        s.append(f'<text x="{xx:.1f}" y="{AY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{lab}</text>')
    for t in range(0, 4001, 1000):
        yy = ay(t)
        s.append(f'<line x1="{AX0-5:.0f}" y1="{yy:.1f}" x2="{AX0:.0f}" '
                 f'y2="{yy:.1f}" stroke="{RULE}"/>')
        s.append(f'<text x="{AX0-9:.0f}" y="{yy+4:.1f}" font-size="10.5" '
                 f'text-anchor="end" fill="{MUT}">{t}</text>')
    s.append(f'<text x="{(AX0+AX1)/2:.0f}" y="{AY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">depth below surface, '
             f'1 − r/R</text>')
    s.append(f'<text x="{AX0-46:.0f}" y="{(AY0+AY1)/2:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}" transform="rotate(-90 '
             f'{AX0-46:.0f} {(AY0+AY1)/2:.0f})">τ(r) / s</text>')

    # required totals
    for t, col, lab, dy in ((tau_meas, FG, f'measured Δν: {tau_meas:.0f} s',
                             -6),
                            (tau_as, YEL, f'asymptotic Δν: {tau_as:.0f} s',
                             15)):
        s.append(f'<line x1="{AX0:.0f}" y1="{ay(t):.1f}" x2="{AX1:.0f}" '
                 f'y2="{ay(t):.1f}" stroke="{col}" stroke-width="1" '
                 f'stroke-dasharray="4 3"/>')
        s.append(f'<text x="{AX0+8:.0f}" y="{ay(t)+dy:.1f}" '
                 f'font-size="10.5" fill="{col}">{lab}</text>')

    ld = np.log10(np.clip(depth_tab, 1e-6, None))
    ok = ld <= LD0
    s.append(f'<path d="{path(ax(ld[ok]), ay(cum[1.0][ok]))}" fill="none" '
             f'stroke="{MUT}" stroke-width="2" stroke-dasharray="5 4"/>')
    s.append(f'<path d="{path(ax(ld[ok]), ay(cum[5/3][ok]))}" fill="none" '
             f'stroke="{ACC}" stroke-width="2.6"/>')
    # extensions through the layer, T linear, for two mu
    zz = np.logspace(np.log10(depth), np.log10(1e-4*M.RSUN_TAB), 60)
    for mu, col in ((mu_i, ACC2), (mu_n, PNK)):
        t_ext = []
        for z in zz:
            # time from the top row (depth) up to depth z
            s_lin = (T_top - M.TEFF_SUN)/depth
            Tz = M.TEFF_SUN + s_lin*z
            A = 5/3*M.kB/(mu*M.mu_u)
            t_ext.append(2*(np.sqrt(T_top)-np.sqrt(Tz))/(s_lin*np.sqrt(A)))
        s.append(f'<path d="{path(ax(np.log10(zz/M.RSUN_TAB)), ay(tau_ad + np.array(t_ext)))}" '
                 f'fill="none" stroke="{col}" stroke-width="2.2"/>')
    # legend, lower left
    for k, (col, dash, lab) in enumerate((
            (MUT, ' stroke-dasharray="5 4"', 'table, isothermal c² = P/ρ'),
            (ACC, '', 'table, Γ₁ = 5/3'),
            (ACC2, '', 'layer: Γ₁ = 5/3, fully ionised μ'),
            (PNK, '', 'layer: Γ₁ = 5/3, neutral μ'))):
        yy = AY1 - 70 + 16*k
        s.append(f'<line x1="{AX0+10:.0f}" y1="{yy-4:.0f}" x2="{AX0+34:.0f}" '
                 f'y2="{yy-4:.0f}" stroke="{col}" stroke-width="2.4"{dash}/>')
        s.append(f'<text x="{AX0+40:.0f}" y="{yy:.0f}" font-size="10.5" '
                 f'fill="{FG}">{lab}</text>')
    s.append(f'<text x="{AX1-6:.0f}" y="{AY1-26:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{VIO}">untabulated</text>')
    s.append(f'<text x="{AX1-6:.0f}" y="{AY1-12:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{VIO}">outer layer</text>')

    # ---------------- panel B ----------------
    DMIN, DMAX = 126.0, 172.0

    def bx(d):
        return BX0 + (d-DMIN)/(DMAX-DMIN)*(BX1-BX0)

    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY0-16:.0f}" font-size="12.5" '
             f'text-anchor="middle" fill="{FG}">Large separation</text>')
    s.append(f'<rect x="{BX0:.0f}" y="{BY0:.0f}" width="{BX1-BX0:.0f}" '
             f'height="{BY1-BY0:.0f}" fill="none" stroke="{RULE}"/>')
    for d in range(130, 171, 10):
        xx = bx(d)
        s.append(f'<line x1="{xx:.1f}" y1="{BY1:.0f}" x2="{xx:.1f}" '
                 f'y2="{BY1+5:.0f}" stroke="{RULE}"/>')
        s.append(f'<text x="{xx:.1f}" y="{BY1+18:.0f}" font-size="10.5" '
                 f'text-anchor="middle" fill="{MUT}">{d}</text>')
    s.append(f'<text x="{(BX0+BX1)/2:.0f}" y="{BY1+36:.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="{FG}">Δν = 1/(2τ) / μHz</text>')
    # measured and asymptotic band
    xa, xb = bx(M.DNU_MEAS*1e6), bx(dnu_as*1e6)
    s.append(f'<rect x="{xa:.1f}" y="{BY0:.0f}" width="{xb-xa:.1f}" '
             f'height="{BY1-BY0:.0f}" fill="{YEL}" fill-opacity="0.16"/>')
    s.append(f'<line x1="{xa:.1f}" y1="{BY0:.0f}" x2="{xa:.1f}" '
             f'y2="{BY1:.0f}" stroke="{FG}" stroke-width="1.4"/>')
    s.append(f'<line x1="{xb:.1f}" y1="{BY0:.0f}" x2="{xb:.1f}" '
             f'y2="{BY1:.0f}" stroke="{YEL}" stroke-width="1.4"/>')
    s.append(f'<text x="{xa-4:.1f}" y="{BY1-10:.0f}" font-size="10.5" '
             f'text-anchor="end" fill="{FG}">measured 135.1</text>')
    s.append(f'<text x="{xb+4:.1f}" y="{BY1-10:.0f}" font-size="10.5" '
             f'fill="{YEL}">asymptotic {dnu_as*1e6:.1f}</text>')

    tau_iso = cum[1.0][-1]
    rows = [(1/(2*tau_iso), MUT, 'table, isothermal: bound', True),
            (1/(2*tau_ad), ACC, 'table, Γ₁ = 5/3: bound', True)]
    for mu, col, lab in ((mu_i, ACC2, '+ layer, fully ionised'),
                         (ssm['rho'][-1]*M.kB*T_top /
                          ((ssm['P'][-1]-M.a_rad*T_top**4/3)*M.mu_u), BLU,
                          '+ layer, top-row μ'),
                         (mu_n, PNK, '+ layer, neutral')):
        t = M.layer_time(T_top, M.TEFF_SUN, depth, 5/3, mu)
        rows.append((1/(2*(tau_ad+t)), col, lab, False))
    for k, (d, col, lab, bound) in enumerate(rows):
        yy = BY0 + 34 + 46*k
        xx = bx(d*1e6)
        if bound:
            s.append(f'<line x1="{xx:.1f}" y1="{yy:.1f}" x2="{xx-26:.1f}" '
                     f'y2="{yy:.1f}" stroke="{col}" stroke-width="2"/>')
            s.append(f'<path d="M {xx-26:.1f},{yy:.1f} l 7,-4 l 0,8 z" '
                     f'fill="{col}"/>')
        s.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="5" fill="{col}"/>')
        right = xx < (BX0+BX1)/2
        tx = xx + 10 if right else xx - 10
        anc = 'start' if right else 'end'
        if bound and not right:
            tx = xx - 34
        if d*1e6 < dnu_as*1e6:
            # left of the band: write the label beyond the band
            tx, anc = xb + 10, 'start'
        s.append(f'<text x="{tx:.1f}" y="{yy-10:.1f}" font-size="10.5" '
                 f'text-anchor="{anc}" fill="{FG}">{lab}</text>')
        s.append(f'<text x="{tx:.1f}" y="{yy+16:.1f}" font-size="10.5" '
                 f'text-anchor="{anc}" fill="{col}">{d*1e6:.2f}</text>')
    s.append(f'<text x="{AX0-50:.0f}" y="{H-12:.0f}" font-size="10.5" '
             f'fill="{MUT}">Model: BS2005-AGS,OP. Measured: Huber et al. '
             f'(2011). Asymptotic: × (1 + 0.026), Mosser et al. (2013). '
             f'Layer: T linear from {T_top:.0f} K to {M.TEFF_SUN:.0f} K.'
             f'</text>')
    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    for name, body in (("m04_fig_disp.svg", build_disp()),
                       ("m04_fig_tau.svg", build_tau())):
        with open(name, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"wrote {name} ({len(body)} bytes)")
