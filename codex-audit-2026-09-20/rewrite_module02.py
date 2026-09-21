from pathlib import Path
from bs4 import BeautifulSoup

PATH = Path(__file__).parent / "textbook-edition-20-rule" / "module02.html"


def set_html(tag, html):
    frag = BeautifulSoup(html, "html.parser")
    tag.clear()
    for child in list(frag.contents):
        tag.append(child)


soup = BeautifulSoup(PATH.read_text(encoding="utf-8"), "html.parser")

titles = {
    "problem": "1. From a kinetic distribution to five fluid fields",
    "moments": "2. Moments of the distribution function",
    "invariants": "3. The five collision invariants",
    "transfer": "4. The moment hierarchy and the closure problem",
    "continuity": "5. Conservation of mass",
    "lagrange": "6. The material derivative",
    "momentum": "7. Momentum conservation",
    "euler": "7.1 The Euler equation",
    "ns": "7.2 The Navier–Stokes equation",
    "energy": "8. Conservation of energy",
    "closure": "9. Closure and the Reynolds number",
    "solarwind": "10. Comparison with the solar wind",
    "prediction": "10.1 The prediction from steady spherical continuity",
    "helios": "10.2 Helios measurements",
    "verdict": "10.3 Comparison of prediction and measurement",
    "mdot": "10.4 Solar mass-loss rate",
    "broken": "10.5 Failure of the adiabatic energy closure",
    "limits": "11. Scope and limitations",
    "lab": "11.1 Reproducing the numerical results",
}
for ident, title in titles.items():
    soup.find(id=ident).string = title


def replace(prefix, html):
    matches = [x for x in soup.find_all(["p", "li", "figcaption"]) if x.get_text(" ", strip=True).startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"{prefix!r} matched {len(matches)} blocks")
    set_html(matches[0], html)


R = {
    "Taking moments of the Boltzmann": r"Taking moments of the Boltzmann equation reduces the kinetic description to fluid equations. This module derives that reduction, identifies why the hierarchy requires closure, and tests mass and energy conservation against Helios solar-wind measurements.",
    "Now read the structure": r"Equation (4.1) reveals the moment hierarchy. Its storage term contains $\langle\psi\rangle$, while its flux contains $\langle\mathbf v\psi\rangle$. Choosing $\psi=m$ introduces the bulk velocity. Choosing $\psi=m\mathbf v$ introduces the pressure tensor, and choosing kinetic energy introduces the heat flux. Each equation therefore depends on a higher velocity moment, as Fig. 1 illustrates.",
    "The moment hierarchy.": r"The moment hierarchy arises because transport multiplies the chosen weight $\psi$ by one additional power of velocity. Mass conservation requires the velocity, momentum conservation requires the pressure tensor, and energy conservation requires the heat flux. The sequence continues indefinitely, so any finite fluid system requires a closure assumption.",
    "Equation (7.2) is": r"Equation (7.2) is Newton’s second law per unit volume. The material acceleration $\rho Du_i/Dt$ is balanced by the surface force $-\partial_jP_{ij}$ and body force $\rho g_i$. The material derivative from §6 converts the motion of a fluid parcel into an Eulerian field equation.",
    "For an incompressible flow": r"For incompressible flow, Proposition 5 gives $\nabla\!\cdot\mathbf u=0$, so the third term in equation (7.5) vanishes. The remaining viscous term may still be negligible. Section 9 uses the Reynolds number to make that comparison.",
    "The Reynolds number is": r"""The Reynolds number measures the term discarded by the Euler closure. On a length scale $L$, inertia has magnitude $\rho u^2/L$ and viscosity has magnitude $\mu u/L^2$. Their ratio is
$$ \frac{|\mu\nabla^2\mathbf u|}{{|\rho(\mathbf u\!\cdot\nabla)\mathbf u|}}\sim\frac{\mu}{\rho uL}=\frac{1}{\mathrm{Re}}. \tag{9.2}$$
Equation (9.1) therefore converts the Knudsen census from Module 1 into a test of whether viscosity may be neglected. The table uses the same environmental parameters and the appropriate neutral or Coulomb mean free path.""",
    "The last two rows": r"The final two rows expose different limitations. With unsuppressed Spitzer viscosity, the intracluster medium has $\mathrm{Re}\approx600$ and would be much less turbulent than cluster observations suggest. Magnetic suppression of cross-field transport may resolve this tension, as discussed in Module 12. At 1 au the solar wind has $\mathrm{Kn}\approx1.9$, so the Chapman–Enskog expansion does not converge. Its transverse fluid behaviour instead relies on magnetic confinement at the proton gyroradius.",
    "Venzmer and Bothmer": r"Venzmer and Bothmer (2018) fit radial power laws to combined Helios 1 and 2 measurements from $0.29$ to $0.98$ au. Their equation (10) has the form $x(r)=d\,r^e$, with $r$ measured in au. Table 3 reports separate coefficients for the mean and median distributions of each plasma variable.",
    "One step in the argument": r"Proposition 13 applies to a single steady stream, whereas each radial bin contains a mixture of fast and slow wind. Density and speed are anticorrelated within that mixture. Continuity constrains $\langle nv\rangle$, but the published fits describe $\langle n\rangle$ and $\langle v\rangle$ separately. The fitted exponents obey $\alpha-\beta=2$ if the mixture is radially self-similar. This requires individual streams to share the same exponents and their relative weights to remain constant with radius.",
    "The condition is an idealisation": r"The solar-wind mixture is not exactly self-similar because fast streams overtake slow streams and exchange mass and momentum. This evolution plausibly produces the 4–5 per cent residual in Fig. 3. The residual measures departure from the single-stream assumptions rather than failure of continuity. Density–velocity anticorrelation mainly changes the flux amplitude when its covariance has the same radial scaling as the product. The mass-loss comparison in §10.4 should therefore be treated as a calibration.",
    "The continuity test.": r"Continuity test. The upper panel compares the Helios value of $\alpha-\beta$ with the exact steady-flow prediction $2$. Thick bars show formal fit errors; pale bars show the larger year-to-year scatter. Both fits agree within one standard deviation and bracket the prediction. The lower panel shows $4\pi r^2\rho v$ relative to its 1 au value. Across the observed interval, the mean fit rises by $4.9$ per cent and the median fit falls by $4.2$ per cent. These deviations quantify the wind’s departure from a steady spherical flow.",
    "This second check is": r"The mass-loss comparison is weaker than the exponent test. Equation (10.2) compares a measured exponent with an exact prediction that contains no fitted normalization. Equation (10.3) compares two estimates derived from overlapping data and can accommodate any constant $\dot M$. Agreement in equation (10.3) checks normalization and arithmetic; equation (10.2) tests the radial scaling.",
    "This is the most useful result": r"The observations distinguish exact conservation from an approximate closure. Continuity, which follows from particle-number conservation, agrees with the fitted exponents to about two per cent. The adiabatic energy equation assumes no heating or conduction and misses the temperature exponent by roughly forty per cent. The solar wind therefore conserves mass while violating the adopted thermodynamic closure.",
    "One structural limitation": r"No closure solves the moment hierarchy in every regime. Chapman–Enskog theory is an asymptotic expansion in $\mathrm{Kn}$, and higher-order truncation is not automatically more accurate or stable. When $\mathrm{Kn}\sim1$, a collisional fluid closure is unavailable and the kinetic equation must be retained. The solar wind lies in this regime along the field, although magnetic confinement supplies a much shorter transverse scale.",
    "Radial power-law fits": r"Radial solar-wind fits: Venzmer, M. S. &amp; Bothmer, V. (2018), “Solar-wind predictions for the Parker Solar Probe orbit”, <i>A&amp;A</i> <b>611</b>, A36, arXiv:1711.07534. Their equation (10) defines $x(r)=d\,r^e$. Table 3 gives the mean and median density, speed, and temperature fits over $0.29$–$0.98$ au. Figure 9 and Table 3 provide the year-to-year exponent scatters used in Fig. 3.",
}

for prefix, html in R.items():
    replace(prefix, html)

PATH.write_text(str(soup), encoding="utf-8")
print(f"rewrote {len(R)} prose blocks and {len(titles)} headings")
