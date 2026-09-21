from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent / "textbook-edition-20-rule"


def norm(text):
    return " ".join(text.split())


def apply(number, replacements):
    path = ROOT / f"module{number:02d}.html"
    html = path.read_text(encoding="utf-8")
    for prefix, replacement in replacements:
        soup = BeautifulSoup(html, "html.parser")
        matches = [
            str(tag)
            for tag in soup.find_all(["p", "li", "div", "span", "td", "h2", "h3"])
            if norm(tag.get_text(" ", strip=True)).startswith(prefix)
        ]
        if len(matches) != 1:
            raise RuntimeError((number, prefix, len(matches)))
        if matches[0] not in html:
            raise RuntimeError((number, prefix, "serialization mismatch"))
        html = html.replace(matches[0], replacement, 1)
    path.write_text(html, encoding="utf-8")
    print(f"module {number:02d}: rewrote {len(replacements)} blocks")


apply(1, [
    (
        "The cheapest honest model",
        '<p>The simplest useful model of the collision term is the relaxation, or BGK, approximation introduced by Bhatnagar, Gross, and Krook (1954):</p>',
    ),
    (
        "Deflections from independent encounters",
        '<p>Independent encounters have random azimuths, so their mean vector deflection vanishes while their mean-square deflections add. This gives $$\\frac{d\\langle\\theta^2\\rangle}{dt}=8\\pi nvb_{90}^2\\int\\frac{db}{b},$$ which is equation (5.3). With $b=e^s$, the measure becomes $db/b=ds$, and every equal interval in $\\ln b$ contributes equally. The result therefore depends on the cutoffs only through $\\ln\\Lambda=\\ln(b_{\\max}/b_{\\min})$. Changing either cutoff by a factor of two changes $\\ln\\Lambda\\simeq37$ by less than two per cent.</p>',
    ),
    (
        "On the resolution question",
        '<p>The numerical resolution does not restore the fluid approximation. At $r=1.73$ Mpc, the mean free path is $173$ kpc, seventeen times the $10$ kpc cell size. A particle typically crosses many cells before colliding, so an individual cell is not a local fluid element. Mesh refinement resolves smaller collisionless structures but does not make the Euler equations more applicable. Interpreting those resolved structures as ordinary gas dynamics therefore requires additional kinetic justification.</p>',
    ),
])

apply(2, [
    (
        "Check against a published measurement.",
        '<div class="keyresult"><b>Continuity agrees with the Helios radial scalings.</b> Equation (8.4) requires $\\alpha-\\beta=2$. The mean fits give $1.961$, and the median fits give $2.035$; their ratios to the prediction are $0.980$ and $1.018$. Formal fit errors place the two values $0.99\\sigma$ and $0.73\\sigma$ from 2. Year-to-year scatter gives the more representative values $0.53\\sigma$ and $0.48\\sigma$. The steady spherical continuity relation therefore holds to about two per cent over a factor of $3.4$ in radius.</div>',
    ),
    (
        "A test that only ever confirms",
        '<p>The temperature exponent supplies an independent test of the adiabatic closure. It uses the same Helios data and fitting method as the continuity comparison, but the closure makes a different quantitative prediction.</p>',
    ),
    (
        "A reader who took §9 seriously",
        '<p>The failure of the adiabatic closure is consistent with the kinetic ordering. Section 9 found $\\mathrm{Kn}\\approx1.9$, where the Chapman–Enskog expansion does not converge. Neither the Euler nor Navier–Stokes closure is then controlled. The measured temperature profile demonstrates the resulting failure rather than introducing a separate inconsistency.</p>',
    ),
    (
        "From D4, the adiabatic prediction",
        '<div>Problem D4 gives the adiabatic prediction $\\tau=2\\alpha/3=1.395$, or $T\\propto r^{-1.395}$. The measured exponent is $-0.913$, only $0.654$ of the predicted magnitude. The discrepancy is $12.4\\sigma$ for the median fits and $19.6\\sigma$ for the mean fits. Thus the same data satisfy steady continuity within one standard deviation but exclude adiabatic cooling.</div>',
    ),
])

apply(3, [
    (
        "A star that contracts is not static.",
        '<p>A contracting star departs slightly from exact hydrostatic balance. The required fractional imbalance is set by the ratio of dynamical to evolutionary timescales. That ratio is extremely small for ordinary stellar evolution, which justifies equation (2.2) despite the slow contraction.</p>',
    ),
    (
        "This agreement is a check of the algebra",
        '<div class="warn"><b>Internal consistency of the atmospheric example.</b> The International Standard Atmosphere defines its tabulated tropopause values from the sea-level conditions, lapse rate, and hydrostatic equation. Agreement at the $10^{-5}$ level verifies equations (4.2) and (4.3) and their numerical evaluation. It does not establish that the real atmosphere is exactly polytropic.</div>',
    ),
    (
        "Everything in §6 and §7",
        '<p>Sections 6 and 7 use the polytropic closure (4.1). Before testing that closure, we first derive two consequences of hydrostatic equilibrium alone: one inequality and one integral identity.</p>',
    ),
    (
        "This agreement does not confirm hydrostatic equilibrium.",
        '<div class="warn"><b>The virial comparison is an internal consistency check.</b> The solar model was constructed by solving equation (2.4), so it must satisfy the derived identity (8.2). The ratio $1.00049$ verifies the table integration and boundary treatment. The residual may arise from trapezoidal integration and from the table ending at $0.983\\,R$. Tests of the physical model must instead examine closures that were not imposed during its construction.</div>',
    ),
    (
        "The table has $1284$ rows",
        '<p>The solar-model table contains $1284$ rows from $r/R=0.00161$ to $0.98308$. Each row gives mass, radius, temperature, density, pressure, luminosity, and six composition fractions. The first row supplies $T_c=1.5480\\times10^7$ K, $\\rho_c=150.50\\ \\mathrm{g\\,cm^{-3}}$, and $P_c=2.3380\\times10^{17}\\ \\mathrm{dyn\\,cm^{-2}}$. The final-row helium fraction, $0.22905$, agrees with the published value $0.229$ and identifies the tabulation as the cited model.</p>',
    ),
    (
        "Check 1: refuted.",
        '<div class="warn"><b>Check 1: the $n=3$ Eddington model fails the density and pressure tests.</b> It predicts $\\rho_c/\\bar\\rho=54.18$, whereas the tabulated solar model gives $106.88$. The predicted-to-tabulated ratio is $0.5069$ for density and $0.5316$ for central pressure. The central-temperature ratio is much closer, $1.0486$, showing that agreement in one variable does not validate the full structure.</div>',
    ),
    (
        "Check 2: confirmed.",
        '<div class="keyresult"><b>Check 2: the convective envelope is close to an $n=3/2$ polytrope.</b> Proposition 5 predicts $n=3/2$ for an adiabatically stratified monatomic gas. Between $0.80$ and $0.92\\,R$, the model gives $\\nabla=0.3957$ and $n_{\\rm eff}=1.5273$. The effective index differs from the prediction by $1.8$ per cent.</div>',
    ),
    (
        "Check 3: the model is refuted",
        '<div class="warn"><b>Check 3: the convection-zone boundary disagrees with helioseismology.</b> The model places the boundary at $0.7280\\,R$, compared with the measured $0.7133\\pm0.0005\\,R$. The difference is $0.0147\\,R$, or $29.4\\sigma$. The independently located table boundary, $0.7269\\,R$, remains $27.2\\sigma$ above the measurement. Even the rounded uncertainty $0.001\\,R$ leaves a $15.0\\sigma$ discrepancy.</div>',
    ),
    (
        "The measured base is from Basu",
        '<span class="prov"><b>Source note.</b> The helioseismic boundary is the GONG value from Basu and Antia (2004). The model boundary and surface helium abundance come from Bahcall, Serenelli, and Basu (2005). The inference of the boundary from oscillation frequencies is model-dependent; Module 6 derives the local stability criterion but does not reproduce that inversion.</span>',
    ),
    (
        "Proposition 12 derives (8.2)",
        '<div>Proposition 12 derives equation (8.2) directly from hydrostatic equilibrium. Because the solar table was generated from the same equation, the ratio $3\\int P\\,dV/(-\\Omega)=1.00049$ checks the numerical integration rather than the Sun. A physical test would require independently measured profiles of $P$, $\\rho$, and enclosed mass. This differs from the Module 2 continuity test, whose density and velocity exponents were fitted independently.</div>',
    ),
])

apply(4, [
    (
        "Check 1: Laplace agrees",
        '<div class="keyresult"><b>Check 1: dry air supports the adiabatic sound speed.</b> For an ideal diatomic gas, the adiabatic prediction is $331.32\\ \\mathrm{m\\,s^{-1}}$. The measured value is $331.45\\pm0.01\\ \\mathrm{m\\,s^{-1}}$, giving a ratio of $0.9996$. The isothermal prediction is only $280.02\\ \\mathrm{m\\,s^{-1}}$, or $0.8448$ of the measurement. Their ratio, $\\sqrt{7/5}=1.1832$, is fixed by the different thermodynamic closures.</div>',
    ),
    (
        "The measured value, $(331.45",
        '<span class="prov"><b>Source note.</b> Smith and Harlow (1963) measured $(331.45\\pm0.01)\\ \\mathrm{m\\,s^{-1}}$ for dry air at $273.15$ K and one atmosphere. The value is quoted here through the experimental compilation of Gavioso et al. (2025), because the original paper was not available for direct inspection.</span>',
    ),
    (
        "where the last form uses",
        '<p>The final form uses $H=c^2/(\\Gamma_1g)$ from equation (4.1). It connects the acoustic cutoff frequency directly to the pressure scale height introduced in Module 3.</p>',
    ),
    (
        "7.1 Check 2:",
        '<h3 id="check2">7.1 Check 2: the isothermal solar model</h3>',
    ),
    (
        "Check 2: the isothermal closure",
        '<div class="warn"><b>Check 2: the standard solar stratification excludes the isothermal closure.</b> With the tabulated $P$ and $\\rho$, an isothermal Sun requires $\\Delta\\nu\\le130.70\\ \\mu$Hz. The measured spacing is $135.1\\ \\mu$Hz, $3.25$ per cent above this bound. The asymptotic value, $138.61\\ \\mu$Hz, exceeds it by $5.71$ per cent.</div>',
    ),
    (
        "The check refutes the isothermal closure",
        '<p>This comparison excludes the isothermal closure for the measured spacing and the standard model\'s pressure and density profiles. It does not exclude every conceivable structure with an isothermal sound speed. The dry-air experiment and the solar bound nevertheless reject the same closure under two explicitly stated sets of conditions.</p>',
    ),
    (
        "With $c^2 = \\tfrac{5}{3}P/\\rho$",
        '<p>With $c^2=\\tfrac53P/\\rho$, the tabulated interior contributes $2963.2$ s. The corresponding bound $\\Delta\\nu\\le168.74\\ \\mu$Hz lies above both the measured and asymptotic spacings, so it does not exclude the adiabatic closure. The outer layers must supply the remaining acoustic travel time:</p>',
    ),
    (
        "Check 3: consistent, not confirmed.",
        '<div class="keyresult"><b>Check 3: the required outer-layer travel time is physically admissible.</b> With $\\Gamma_1=5/3$ in the tabulated interior, the outer $1.69$ per cent of the radius contributes $644.0$ s of the $3607.2$ s asymptotic acoustic radius. Using the measured spacing gives $737.8$ s of $3701.0$ s. Both remainders are positive, as the closure requires, but positivity alone does not establish that the closure is accurate near the photosphere.</div>',
    ),
    (
        "Confirmed in air by Check 1.",
        'Supported by the dry-air measurement in Check 1. Near the solar photosphere, rapid radiative exchange makes compression non-adiabatic and shifts the mode frequencies.',
    ),
])

apply(5, [
    (
        "With $R_0^3/M",
        '<p>Using $R_0^3/M=3/(4\\pi\\rho_0)$ gives $t_{\\rm ff}=(3\\pi/32G\\rho_0)^{1/2}$. Every shell has the same value of $R_0^3/M$, so $r/R_0$ follows the same time dependence for all shells. Their ordering is preserved, and they reach the origin simultaneously. The dimensionless time is $t_{\\rm ff}(4\\pi G\\rho_0)^{1/2}=\\pi\\sqrt{3/8}$. <span class="qed">∎</span></p>',
    ),
    (
        "A validation, not a check.",
        '<p><b>Numerical consistency check.</b> Kandori et al. derived the contrast column of their Table 4 from $\\xi_{\\max}$. Integrating equation (5.2) reproduces all fifteen entries from $6.63$ to $364$. The largest residual is $2.2$ per cent for CB 110, while Barnard 68 gives $16.56$ against the tabulated $16.6$. This agreement verifies the integration and parameter convention but supplies no independent evidence about the clouds.</p>',
    ),
    (
        "Every Bok globule number",
        '<span class="prov"><b>Source note.</b> The Bok-globule values come from Tables 4 and 5 of Kandori et al. (2005). Results attributed there to Alves et al. (2001), Hotzel et al. (2002), and Lai et al. (2003) are used only through Kandori\'s compilation. The Gaussian line widths from Lada et al. (2003) are treated as full widths at half maximum, consistent with their equation 2.</span>',
    ),
    (
        "Check 1: refuted.",
        '<div class="keyresult"><b>Check 1: most fitted globules are unstable under the static isothermal criterion.</b> Proposition 8 gives $\\xi_{\\rm crit}=6.4508$. Eight of eleven starless globules exceed this value, and Barnard 68 has $\\xi_{\\max}=6.9\\pm0.2$, or $2.25\\sigma$ above the threshold. The conclusion applies only if the fitted isothermal sphere is interpreted as a static equilibrium.</div>',
    ),
    (
        "Check 2: refuted.",
        '<div class="keyresult"><b>Check 2: the outer half of Barnard 68 is inconsistent with a static isothermal sphere.</b> At $100^{\\prime\\prime}$, the measured local density slope is $3.2428$, whereas every isothermal sphere has a ceiling of $2.5176$. The observed slope exceeds the ceiling for radii beyond $46.2^{\\prime\\prime}$. Across the same cloud, the dust temperature varies by a factor of $2.04$.</div>',
    ),
    (
        "The density profile of Nielbock",
        '<span class="prov"><b>Model dependence of the density profile.</b> Nielbock et al. infer the profile from a spherical radiative-transfer model with assumed opacity and gas-to-dust ratio. Their alternative fits give outer slopes from $3.4$ to $3.7$, while the adopted fit gives $\\eta=4.0$. All exceed the isothermal ceiling, so the conclusion is insensitive to the chosen fit. The assumed distance of $150$ pc cancels from the angular comparison.</span>',
    ),
    (
        "Refuted, jointly with the static",
        'The outer $53.8$ per cent of Barnard 68 is inconsistent with a static isothermal sphere. Its dust temperature also varies by a factor of $2.04$; the heating and cooling required for an isothermal model are not calculated here.',
    ),
])
