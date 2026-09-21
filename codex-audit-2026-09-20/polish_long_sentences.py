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
        matches = [str(t) for t in soup.find_all(["p", "li", "div", "span", "td", "figcaption"])
                   if norm(t.get_text(" ", strip=True)).startswith(prefix)]
        if len(matches) != 1 or matches[0] not in html:
            raise RuntimeError((number, prefix, len(matches)))
        html = html.replace(matches[0], replacement, 1)
    path.write_text(html, encoding="utf-8")
    print(number, len(replacements))


apply(1, [
    (
        "Definition 2 (fluid, or continuum, description).",
        '<div class="def"><b>Definition 2 (fluid, or continuum, description).</b> A gas admits a fluid description when five local fields determine its distribution to the required accuracy. These fields are the number density, $$ n(\\mathbf{x},t)=\\int f\\,d^3v, $$ the three components of the bulk velocity, $$ \\mathbf{u}(\\mathbf{x},t)=\\frac{1}{n}\\int\\mathbf{v}f\\,d^3v, $$ and the temperature, defined by $$ \\frac32k_BT(\\mathbf{x},t)=\\frac1n\\int\\tfrac12m|\\mathbf{v}-\\mathbf{u}|^2f\\,d^3v. $$ The leading distribution is the local Maxwellian built from these five quantities, $$ f_M(\\mathbf{v})=n\\left(\\frac{m}{2\\pi k_BT}\\right)^{3/2}\\exp\\!\\left[-\\frac{m|\\mathbf{v}-\\mathbf{u}|^2}{2k_BT}\\right].\\tag{2.2}$$ Section 3 makes precise the requirement that the correction to $f_M$ remain small.</div>',
    ),
    (
        "Solar wind values are representative",
        '<span class="prov">The solar-wind row represents typical slow-wind conditions at 1 au. Published averages span approximately $1.9$–$8.8\\ \\mathrm{cm^{-3}}$ in proton density and $4.8\\times10^4$–$3.0\\times10^5$ K in proton temperature. The resulting Knudsen number should therefore be interpreted as order unity rather than as a two-digit measurement.</span>',
    ),
])

apply(5, [
    (
        "Proposition 6 (the isothermal sphere).",
        '<div class="prop"><b>Proposition 6 (the isothermal sphere).</b> Under Definition 3, hydrostatic equilibrium and Poisson\'s equation reduce to $$ \\frac{1}{\\xi^2}\\frac{d}{d\\xi}\\left(\\xi^2\\frac{d\\psi}{d\\xi}\\right)=e^{-\\psi},\\qquad \\psi(0)=\\psi\'(0)=0.\\tag{5.2}$$ Near the centre, $\\psi=\\xi^2/6-\\xi^4/120+O(\\xi^6)$. The mass inside $\\xi$ is $M(\\xi)=4\\pi\\rho_c\\alpha^3\\xi^2\\psi\'(\\xi)$, equivalently $M=(c_s^2r/G)\\xi\\psi\'(\\xi)$. The equation also has the singular solution $\\psi=\\ln(\\xi^2/2)$, or $\\rho=c_s^2/(2\\pi Gr^2)$. Its regular solution has $\\rho>0$ at every finite $\\xi$, so an untruncated isothermal sphere has no surface.</div>',
    ),
])

apply(6, [
    (
        "Proposition 6 (Field's criteria",
        '<div class="prop"><b>Proposition 6 (Field\'s criteria).</b> Perturb a parcel in thermal equilibrium by $\\delta T$. At fixed density, thermal runaway occurs when $$\\left(\\frac{\\partial\\mathcal L}{\\partial T}\\right)_\\rho<0.\\tag{8.1}$$ This is Field\'s isochoric criterion. A slowly evolving parcel can instead remain in pressure balance with its surroundings. At fixed pressure, runaway then requires $$\\left(\\frac{\\partial\\mathcal L}{\\partial T}\\right)_P=\\left(\\frac{\\partial\\mathcal L}{\\partial T}\\right)_\\rho-\\frac{\\rho_0}{T_0}\\left(\\frac{\\partial\\mathcal L}{\\partial\\rho}\\right)_T<0.\\tag{8.2}$$ Cooling normally increases with density, so $(\\partial\\mathcal L/\\partial\\rho)_T>0$. The isobaric condition is therefore satisfied over a wider range of states than the isochoric condition.</div>',
    ),
    (
        "Both $29$ per cent and $23$ per cent",
        '<span class="prov">The observed histograms give $29$ per cent for the complete sample and $23$ per cent for the low-starlight subsample. These are different populations, not two estimates of one quantity. Integrating the authors\' lognormal below $P_{\\min}$ gives only $5.0$ per cent, while their polynomial gives $17.4$ per cent. Neither fitted form reproduces the complete-sample fraction.</span>',
    ),
    (
        "From the turning points of Proposition 8",
        '<div class="keyresult"><b>The equilibrium pressure range is much narrower than the temperature or density range.</b> The corrected fit gives $184.0$–$5039.4$ K in temperature, a factor of $27.4$. Density spans $0.994$–$8.682\\ \\mathrm{cm^{-3}}$, a factor of $8.7$. Pressure spans only $1597$–$5007\\ \\mathrm{K\\,cm^{-3}}$, a factor of $3.13$. Along the equilibrium curve, density and temperature vary in opposite directions, so their product changes relatively little. Pressure is therefore the most discriminating observable for the static two-phase model. The measurement in Section 10 places $29$ per cent of the mass outside this interval.</div>',
    ),
])

apply(7, [
    (
        "Proposition 7 (the self-similar mixing law).",
        '<div class="prop"><b>Proposition 7 (self-similar mixing law).</b> Assume a narrowband multimode perturbation and a constant acceleration $g$. Let the front obey the buoyancy–drag balance (8.2), with constant drag and added-mass coefficients. Finally, assume that the layer has forgotten its initial condition, so its dominant wavelength is proportional to its width. Then $$h_B=\\alpha_BAgt^2.\\tag{8.1}$$ The coefficient $\\alpha_B$ depends on the density ratio, the wavelength-to-width ratio, and the drag and added-mass coefficients. It is independent of $g$, $t$, and the initial amplitude within this self-similar regime.</div>',
    ),
    (
        "Say the weakness first",
        '<span class="warn"><b>Uncertainty of the coronal inputs.</b> The source quotes each input to one significant figure and gives no statistical uncertainty. The wavelength is approximately $7000$ km, the interface spans one to three pixels, and the growth time is about 14 minutes. The driving shear is approximately $20\\ \\mathrm{km\\,s^{-1}}$ and is explicitly an upper limit. No standard deviation can therefore be assigned; the comparisons below are accurate only to factors of order two. A separate observation with quoted uncertainties was not available for direct inspection.</span>',
    ),
])

apply(8, [
    (
        "Proposition 6 (the similarity solution",
        '<div class="prop"><b>Proposition 6 (similarity solution and $\\xi_0$).</b> Define $\\lambda=r/R(t)$ and write $$v=\\frac{r}{t}u(\\lambda),\\qquad \\rho=\\rho_0g(\\lambda),\\qquad p=\\rho_0\\frac{r^2}{t^2}\\Pi(\\lambda).\\tag{4.2}$$ The spherical Euler equations then reduce to three ordinary differential equations in $\\ln\\lambda$. The strong-shock boundary values at $\\lambda=1$ are $$u(1)=\\frac{4}{5(\\gamma+1)},\\qquad g(1)=\\frac{\\gamma+1}{\\gamma-1},\\qquad \\Pi(1)=\\frac{8}{25(\\gamma+1)}.\\tag{4.3}$$ Energy conservation fixes the remaining constant through $$1=4\\pi\\xi_0^5J,\\qquad J=\\int_0^1\\lambda^4\\left[\\tfrac12gu^2+\\frac{\\Pi}{\\gamma-1}\\right]d\\lambda.\\tag{4.4}$$ Numerically, $\\xi_0=1.151666$ for $\\gamma=5/3$ and $1.032777$ for $\\gamma=7/5$.</div>',
    ),
])

apply(9, [
    (
        "Carry the condition with the number.",
        '<div class="warn"><b>The Faraday upper bound depends strongly on magnetic geometry.</b> Marrone et al. assume a largely radial, ordered field near equipartition and state that this cannot be justified observationally. Their scaling raises the accretion-rate limit as $\\epsilon^{-2/3}$ when the field strength is a fraction $\\epsilon$ of equipartition. Thus $\\epsilon=1$, $0.10$, and $0.03$ give Bondi-to-limit ratios of approximately $40$, $9$, and $4$. A nearly reversing field with little net bias can remove the upper bound altogether. The factor of 40 must therefore be quoted with the equipartition-field assumption.</div>',
    ),
    (
        "radiative efficiency $L/\\dot Mc^2$",
        'radiative efficiency $L/\\dot Mc^2$, and the field-strength fraction used by Marrone et al. The efficiency is always written $\\eta_{\\rm rad}$ because bare $\\eta$ denotes dynamic viscosity elsewhere in the book. The symbol $\\epsilon$ is restricted to the magnetic-field scaling in Section 8.2.',
    ),
])

apply(10, [
    (
        "Proposition 1 ( Module 2",
        '<div class="prop"><b>Proposition 1 (relation among Reynolds, Mach, and Knudsen numbers).</b> With $\\mu\\simeq\\tfrac13\\rho\\bar v\\lambda$, $$\\mathrm{Re}=\\frac{\\rho UL}{\\tfrac13\\rho\\bar v\\lambda}=3\\frac{U}{\\bar v}\\frac{L}{\\lambda}=\\frac{3\\,\\mathrm{Ma_{th}}}{\\mathrm{Kn}},\\qquad \\mathrm{Ma_{th}}=\\frac{U}{\\bar v},\\quad \\mathrm{Kn}=\\frac{\\lambda}{L}.\\tag{1.2}$$ The relation holds for any thermal-speed convention if the same $\\bar v$ appears in both viscosity and Mach number. Changing that convention changes $\\mathrm{Ma_{th}}$ but leaves the resulting Reynolds number unchanged.</div>',
    ),
    (
        "Proposition 3 (the Kolmogorov microscales).",
        '<div class="prop"><b>Proposition 3 (Kolmogorov microscales).</b> The viscosity $\\nu$ and energy flux $\\varepsilon$ define one length, speed, and time: $$\\eta=\\left(\\frac{\\nu^3}{\\varepsilon}\\right)^{1/4},\\qquad u_\\eta=(\\nu\\varepsilon)^{1/4},\\qquad \\tau_\\eta=\\left(\\frac{\\nu}{\\varepsilon}\\right)^{1/2}.\\tag{3.1}$$ They satisfy $$\\frac{u_\\eta\\eta}{\\nu}=1.\\tag{3.2}$$ Thus the Reynolds number of the smallest eddy is unity, marking the scale where viscosity becomes important.</div>',
    ),
    (
        "the Kolmogorov dissipation scale.",
        'the Kolmogorov dissipation scale introduced in Proposition 3. Elsewhere, bare $\\eta$ can denote dynamic viscosity or a module-local quantity. Braginskii\'s dynamic viscosities therefore retain the explicit labels $\\eta_0^{\\rm B}$ and $\\eta_1^{\\rm B}$. All other transport calculations here use the kinematic viscosity $\\nu$.',
    ),
])

apply(11, [
    (
        "The result that sets up the rest",
        '<div class="keyresult"><b>A Keplerian disc is stable to local axisymmetric centrifugal displacements.</b> It has $\\kappa_{\\rm ep}^2=\\Omega^2>0$ at every radius, whereas instability requires $q>2$. A point-mass potential gives $q=3/2$. Within the pressure-free, inviscid, non-magnetic model of this section, neighbouring rings therefore cannot exchange angular momentum through this axisymmetric mode. Other hydrodynamic routes require separate analysis; the later mechanism considered here is magnetic.</div>',
    ),
    (
        "Proof. Mass conservation for an annulus",
        '<div class="proof"><b>Proof.</b> Mass conservation for an annulus is $$R\\frac{\\partial\\Sigma}{\\partial t}+\\frac{\\partial}{\\partial R}(R\\Sigma v_R)=0.$$ Angular-momentum conservation for the same annulus is $$R\\frac{\\partial}{\\partial t}(\\Sigma R^2\\Omega)+\\frac{\\partial}{\\partial R}(R\\Sigma v_RR^2\\Omega)=\\frac{1}{2\\pi}\\frac{\\partial G}{\\partial R}.$$ Eliminating $\\partial\\Sigma/\\partial t$ gives $$R\\Sigma v_R\\frac{\\partial}{\\partial R}(R^2\\Omega)=\\frac{1}{2\\pi}\\frac{\\partial G}{\\partial R}.$$ For Keplerian rotation, $R^2\\Omega=\\sqrt{GM}R^{1/2}$ and $G=-3\\pi\\sqrt{GM}\\nu\\Sigma R^{1/2}$. Substitution yields $$\\Sigma v_R=-\\frac{3}{R^{1/2}}\\frac{\\partial}{\\partial R}(\\nu\\Sigma R^{1/2}).$$ Inserting this expression into mass conservation gives equation (5.1). <span class="qed">∎</span></div>',
    ),
    (
        "CHECK 4 — Disagreement",
        '<div class="keyresult"><b>Check 4: $\\alpha$ is not universal.</b> Fully ionised discs require $\\alpha=0.1$–$0.4$, compared with about $0.01$ for T Tauri discs. The classes differ by factors of $10$–$40$. FU Orionis estimates of $0.001$–$0.003$ widen the protostellar comparison to factors of $33$–$400$. Ionisation provides a plausible physical reason for this class dependence. For fully ionised discs alone, observations exceed the simulation bound $\\alpha\\le0.02$ by at least a factor of five.</div>',
    ),
    (
        "the disc viscosity parameter of (6.1).",
        'the disc viscosity parameter in equation (6.1). Other modules use $\\alpha$ for a length scale, a mixing-length parameter, a pressure ratio, and fitted exponents. None of those meanings occurs in this module. Shakura and Sunyaev\'s original definition is discussed in Section 6.',
    ),
])
