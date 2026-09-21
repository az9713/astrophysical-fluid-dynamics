"""Apply the paragraph-level textbook prose pass to the twelve revised copies.

The script never reads from or writes to afd/module*.html.  It operates only on
codex-audit-2026-09-20/revised-modules/module*.html.
"""
from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
import hashlib
import json
import re

AUDIT = Path(__file__).resolve().parent
DEST = AUDIT / "revised-modules"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fragment(markup: str) -> list:
    return [n for n in BeautifulSoup(markup, "html.parser").contents
            if not isinstance(n, NavigableString) or str(n).strip()]


def replace_tag(tag: Tag, markup: str) -> None:
    nodes = fragment(markup)
    first = nodes.pop(0)
    tag.replace_with(first)
    cursor = first
    for node in nodes:
        cursor.insert_after(node)
        cursor = node


def set_inner(tag: Tag, markup: str) -> None:
    tag.clear()
    for node in fragment(markup):
        tag.append(node)


def replace_block(soup: BeautifulSoup, needle: str, markup: str,
                  names=("p", "li", "figcaption", "div", "span")) -> bool:
    candidates = []
    for tag in soup.find_all(names):
        if needle in tag.get_text(" ", strip=True):
            candidates.append(tag)
    shallow = [t for t in candidates if not any(
        needle in c.get_text(" ", strip=True) for c in t.find_all(recursive=False)
    )]
    if not candidates:
        return False
    pool = shallow or candidates
    # Prefer the narrowest matching block.  An outer .section or .problem div can
    # contain the same words as its paragraph; replacing that container would
    # remove unrelated headings and anchors.
    target = min(pool, key=lambda t: len(t.get_text(" ", strip=True)))
    replace_tag(target, markup)
    return True


def clean_mechanics(soup: BeautifulSoup) -> None:
    """Repair punctuation introduced by HTML boundaries and split safe clauses."""
    for node in list(soup.find_all(string=True)):
        if node.parent and node.parent.name in {"script", "style", "code", "pre"}:
            continue
        text = str(node)
        text = re.sub(r"\s+([,;:.!?])", r"\1", text)
        text = re.sub(r"\s+([)\]])", r"\1", text)
        text = re.sub(r"([(\[])\s+", r"\1", text)
        # Semicolons joining full explanatory clauses are a recurring source of
        # overloaded sentences.  These patterns are safe because the following
        # words begin an independent clause.
        def split_semicolon(m):
            word = m.group(1)
            return ". " + word[0].upper() + word[1:]
        text = re.sub(r";\s+(this|that|these|those|the|it|they|we|he|she)\b",
                      split_semicolon, text, flags=re.I)
        text = re.sub(r"\s+—\s+but\s+", ". However, ", text)
        text = re.sub(r"\s+—\s+and\s+(this|that|these|those|it|they)\b",
                      lambda m: ". " + m.group(1).capitalize(), text, flags=re.I)
        if text != str(node):
            node.replace_with(NavigableString(text))


def sentence_lengths(text: str) -> list[int]:
    return [len(s.split()) for s in re.split(r"(?<=[.!?])\s+(?=[A-Z‘’“\"<])", text)]


def split_overloaded_clauses(soup: BeautifulSoup) -> int:
    """Split independent clauses in blocks that still contain 50-word sentences.

    This operates on the serialized inner HTML, so links, emphasis and MathJax
    delimiters survive.  Only strong clause boundaries are changed.
    """
    changed = 0
    for tag in soup.find_all(["p", "li", "figcaption"]):
        if tag.find_parent(["script", "style", "code", "pre"]):
            continue
        if max(sentence_lengths(tag.get_text(" ", strip=True)) or [0]) <= 50:
            continue
        raw = tag.decode_contents()
        revised = raw
        revised = re.sub(r"[.;]?\s+p\.\s*(\d+)(?=\s*[:.,])", r". Page \1", revised)
        revised = re.sub(r";\s+(?=(?:<[^>]+>)*[A-Za-z])", ". ", revised)
        revised = re.sub(r",\s+but\s+", ". However, ", revised, flags=re.I)
        revised = re.sub(
            r",\s+and\s+(this|that|these|those|the|it|they|we)\b",
            lambda m: ". " + m.group(1).capitalize(), revised, flags=re.I,
        )
        revised = re.sub(r"\.\s+and\s+", ". ", revised, flags=re.I)
        revised = re.sub(r"\.\s+but\s+", ". However, ", revised, flags=re.I)
        revised = re.sub(r"\.\s+although\s+", ". However, ", revised, flags=re.I)
        revised = re.sub(r"(?<=\.\s)([a-z])", lambda m: m.group(1).upper(), revised)
        if revised != raw:
            set_inner(tag, revised)
            changed += 1
    return changed


def rewrite_shared(soup: BeautifulSoup, module: int) -> list[str]:
    edits: list[str] = []
    # Remove self-conscious production language from the teaching narrative.
    phrase_map = {
        "That sentence is the point of the table.": "The table shows that these modelling choices are smaller than the observed year-to-year variation.",
        "and that is the answer": "which determines the result",
        "the last column is where the answer lives": "the last column gives the required comparison",
        "this module exists to explain": "this module explains",
        "the problem this module exists to solve": "the central problem for accretion-disc theory",
        "a shipped module of this book already asked for": "have already arisen in earlier modules",
        "before the table was read": "independently of the tabulated solar model",
        "Neither was read from a solar model": "Neither value was inferred from a solar model",
    }
    for node in list(soup.find_all(string=True)):
        if node.parent and node.parent.name in {"script", "style", "code", "pre"}:
            continue
        text = str(node)
        changed = text
        for old, new in phrase_map.items():
            changed = changed.replace(old, new)
        if changed != text:
            node.replace_with(NavigableString(changed))
            edits.append("production-language cleanup")
    return edits


def rewrite_module12(soup: BeautifulSoup) -> list[str]:
    edits: list[str] = []
    replacements = [
        (
            "One extra term in the momentum equation",
            r'''<p class="sub">Magnetohydrodynamics adds the Lorentz force and an induction equation to ordinary fluid dynamics. These additions describe Alfvén waves, the Parker spiral, magnetic support, anisotropic transport and the magnetorotational instability.</p>''',
            "subtitle",
        ),
        (
            "Ten modules of this book have written the same sentence",
            r'''<p>Magnetic fields have appeared repeatedly in the preceding modules. They confine weakly collisional plasmas, influence the stability of interfaces and clouds, and alter transport in the solar wind and intracluster medium. We now include the magnetic field explicitly. The resulting theory combines the fluid equations of <a href="module02.html">Module 2</a> with Maxwell's equations.</p>''',
            "opening paragraph",
        ),
        (
            "What it costs is small, and that is the surprise",
            r'''<p>The extension requires two ingredients. The momentum equation gains the Lorentz force, while Faraday's law and Ohm's law provide an evolution equation for $\mathbf B$. The kinetic derivation in <a href="module02.html#transfer">Module 2 §4</a> already permits the Lorentz acceleration because $\nabla_{\mathbf v}\!\cdot\mathbf a=0$ for $\mathbf a=(q/mc)\,\mathbf v\times\mathbf B$. The moment hierarchy therefore remains valid.</p>''',
            "opening mechanics",
        ),
        (
            '"Magnetised" is not one question',
            r'''<p>The word <em>magnetised</em> describes two distinct comparisons. The plasma beta $\beta$ compares gas pressure with magnetic pressure and measures the field's dynamical importance. The product $\omega_{\rm c}\tau$ compares the gyrofrequency with the collision rate and measures whether a particle completes significant gyromotion between collisions. A plasma can satisfy one criterion without satisfying the other.</p>''',
            "magnetisation distinction",
        ),
        (
            "This is why $\\beta$ is the census variable",
            r'''<p>Plasma beta is convenient for the census because it does not require an assumed mean particle mass. The Alfvén speed does. The table gives both quantities and checks the identity $v_{\rm A}^2/c_s^2=2/(\gamma\beta)$. This redundant calculation also exposes any inconsistent change in composition.</p>''',
            "beta census",
        ),
        (
            "Two things in that figure are worth stating in words",
            r'''<p>Plasma beta is a pressure ratio, not a measure of field strength alone. The adopted corona and molecular cloud have the same $\beta$ even though their fields differ by six orders of magnitude. Four census environments lie well away from $\beta=1$. The solar wind crosses between magnetically dominated and flow-dominated regimes as it moves outward; <a class="secref" href="#alfvenradius">§6</a> locates that transition.</p>''',
            "figure interpretation",
        ),
        (
            "A one-dimensional quantity compared with a three-dimensional one",
            r'''<p>Thermal-speed conventions must be kept explicit. A one-dimensional thermal speed, a perpendicular rms speed and a three-dimensional rms speed differ by fixed numerical factors. The table below states each convention before it is used. This distinction accounts for the factor $\sqrt{3/2}$ derived in <a class="secref" href="#twotimes">§8.1</a>.</p>''',
            "speed conventions",
        ),
        (
            "The field obeys Maxwell's equations",
            r'''<p>Maxwell's equations govern the magnetic field, while the equations of <a href="module02.html">Module 2</a> govern the gas. Ohm's law couples the two systems. Combining it with Faraday's law yields an induction equation containing advection and magnetic diffusion.</p>''',
            "induction introduction",
        ),
        (
            "The result of Proposition 4 is Alfvén's",
            r'''<p>Proposition 4 is the flux-freezing theorem associated with Alfvén (1942). The derivation above is self-contained. The original paper is cited for historical attribution; its bibliographic details have been verified, but its argument is not used here.</p>''',
            "Alfven attribution",
        ),
        (
            "The field acts on the gas through the Lorentz force",
            r'''<p>The current carried by the plasma couples the magnetic field to the gas through the Lorentz force. Decomposing this force reveals two effects: a magnetic-pressure gradient perpendicular to the field and a tension force along curved field lines.</p>''',
            "Lorentz introduction",
        ),
        (
            "And here is the gap this module cannot fill",
            r'''<p>The following calculation reproduces the magnetic bound obtained in <a href="module07.html">Module 7</a>; it is an internal consistency check rather than a laboratory test. The later comparisons use astronomical measurements. A complete experimental treatment would also compare the theory with controlled measurements of Alfvén waves or laboratory MHD flows, which are outside the present source set.</p>''',
            "evidence limitation",
        ),
        (
            "Module 9 built a wind that leaves the Sun radially",
            r'''<p>The solar wind flows outward while the Sun rotates beneath it. In ideal MHD the field is frozen into the plasma, so a field line remains attached to a rotating footpoint while the wind carries its outer part radially away. The result is the Parker spiral. Its shape is fixed by the rotation rate and wind speed; no additional fitting parameter is required.</p>''',
            "Parker introduction",
        ),
        (
            "Venzmer & Bothmer (2018) fitted power laws",
            r'''<p>Venzmer and Bothmer (2018) fitted power laws $x(r)=d\,r^e$ to Helios 1 and 2 measurements over $0.29$–$0.98$ au. They reported separate mean and median fits with uncertainties. The comparison below evaluates each fit set consistently, without combining coefficients from different rows of their table.</p>''',
            "fit-set explanation",
        ),
        (
            "The control is what makes this a measurement",
            r'''<p>The density profile provides a control on the comparison. Steady spherical mass conservation predicts $\rho\propto r^{-2-\alpha_v}$, where $\alpha_v$ is the measured velocity exponent. The predicted density indices are $-2.0580$ for the median fits and $-2.0490$ for the mean fits. The measured values, $-2.093\pm0.046$ and $-2.010\pm0.038$, differ by only $0.49$ and $0.54$ of their year-to-year scatter. The same data therefore recover the expected density scaling while showing that the magnetic field falls more slowly than $r^{-2}$.</p>''',
            "Parker control",
        ),
        (
            "Close to the Sun the field is strong",
            r'''<p>Near the Sun, $v<v_{\rm A}$: magnetic stresses influence the flow, enforce partial corotation and carry angular momentum. Farther out, $v>v_{\rm A}$ and the wind advects the field. The Alfvén surface is the locus $v=v_{\rm A}$ separating these regimes.</p>''',
            "Alfven surface",
        ),
        (
            "Fig. 3 shows why the bracket is a result",
            r'''<p>All eight model variants place the crossing between $15.76$ and $19.35\,R_\odot$, a range narrower than the separation between the two published estimates. The main extrapolation concerns the wind speed: a fit obtained over $0.29$–$0.98$ au is extended inward to about $0.08$ au. Replacing the fitted power law with a constant speed changes $r_{\rm A}$ by $6.9$ per cent. More realistic inner-wind acceleration would reduce the inferred radius, consistent with the lower value obtained by Verscharen, Bale and Velli.</p>''',
            "Alfven bracket",
        ),
        (
            "Module 2 §9 put two problems together",
            r'''<p>Classical transport creates two difficulties in the intracluster medium. An isotropic collisional viscosity gives a Reynolds number too small for the observed turbulent motions, while classical conduction would also redistribute heat efficiently along unrestricted particle trajectories. A magnetic field makes transport anisotropic. Braginskii's coefficients quantify the local parallel and perpendicular components, but observations constrain an effective transport coefficient on much larger scales.</p>''',
            "transport introduction",
        ),
        (
            "The intracluster medium yields two different numbers",
            r'''<p>Two collision-time conventions produce slightly different numerical values for the ion magnetisation. They describe the same strongly magnetised plasma. The difference can be traced to the thermal-speed convention and to the value adopted for the Coulomb logarithm.</p>''',
            "collision conventions",
        ),
        (
            "That is the return, and it is all of it",
            r'''<p>The single-fluid MHD equations derived here assume an isotropic scalar pressure. They therefore exclude pressure-anisotropy instabilities. Such instabilities may regulate transport in weakly collisional plasmas, but their thresholds require a kinetic or double-adiabatic treatment beyond this module.</p>''',
            "anisotropy limitation",
        ),
        (
            "Every published value this module compares against, with what was read and how",
            r'''<p class="small">The following notes identify the sources of the numerical values and the limits of their use. “Verified” means that the stated equation, table or passage was checked in the cited source. Items listed for historical context are not used as numerical evidence.</p>''',
            "sources introduction",
        ),
    ]
    for needle, markup, label in replacements:
        if replace_block(soup, needle, markup):
            edits.append(label)

    # Rewrite the census provenance that exposed the failure of the earlier pass.
    if replace_block(
        soup,
        "The field column is an order-of-magnitude census",
        r'''<div class="prov"><p>The adopted photospheric field strength is $5$ G, representative of the quiet Sun. This value is an order-of-magnitude estimate rather than a measured global mean. The NASA Sun Fact Sheet reports fields of $1$–$2$ G near the poles, about $25$ G in the bright network, $200$ G in plages and up to $3000$ G in sunspots.</p><p>The remaining field strengths are also census values. The coronal value of $10$ G comes from the active-region example in <a href="module07.html">Module 7</a>. The solar-wind value is the $5$ nT reference used in <a href="module01.html">Module 1</a> and <a href="module10.html">Module 10</a>. The intracluster value is the $1\,\mu$G reference used in Module 10. The molecular-cloud value of $10\,\mu$G is illustrative; Troland and Crutcher (2008) report a mean $|\mathbf B|=16.4\,\mu$G for denser gas. None of the conclusions in this section depends on a factor-of-two change in these illustrative fields.</p></div>''',
    ):
        edits.append("field-census provenance")
    return edits


def rewrite_other_modules(soup: BeautifulSoup, module: int) -> list[str]:
    """Rebuild each module's narrative spine in a consistent textbook register."""
    data = {
        1: [
            ("Everything in this book rests on four equations", r'''<p>The fluid equations describe conservation of mass, momentum and energy, supplemented by an equation of state. Later modules use them to model stellar structure, interstellar collapse, blast waves and accretion. Before using those equations, however, we must establish when a dilute gas can be treated as a continuum.</p>'''),
            ("A continuum has a density at every point", r'''<p>A continuum assigns a density and velocity to every point in space. A real gas consists of discrete particles separated by empty space. The continuum description is therefore an approximation, and its validity is especially important in the low densities common in astrophysics.</p>'''),
            ("So the object we are about to call a fluid", r'''<p>The interstellar medium can be much more rarefied than the best laboratory vacua and still behave as a fluid on sufficiently large scales. The controlling quantity is the Knudsen number, the ratio of the mean free path to the macroscopic scale of interest. This module derives that ratio and identifies the regimes in which a fluid model fails.</p>'''),
            ("The logic runs in one direction", r'''<p>We begin with the particle distribution function and the information discarded by a fluid description. Collisions drive the local distribution toward equilibrium and define a mean free path. Comparing that path with the resolved macroscopic scale gives the Knudsen number, which determines whether continuum equations are appropriate.</p>'''),
        ],
        2: [
            ("Module 1 ended by licensing the fluid description", r'''<p><a href="module01.html">Module 1</a> established when collisions maintain a nearly Maxwellian local velocity distribution. We now derive the continuum equations by taking velocity moments of the Boltzmann equation. This procedure yields exact conservation laws, together with a hierarchy that must be closed by additional physical assumptions.</p>'''),
            ("This is a complete description and it is almost useless", r'''<p>The distribution function depends on three position coordinates, three velocity coordinates and time. Its collision term also contains high-dimensional velocity integrals. Solving this kinetic equation directly is unnecessary for many macroscopic flows, but reducing it to fluid variables requires a controlled approximation.</p>'''),
            ("What we want instead is a description in terms of quantities", r'''<p>A fluid description uses five local scalar fields: mass density, three components of bulk velocity and temperature. These fields depend only on position and time. The reduction from a seven-variable distribution function is substantial, but the resulting moment equations do not close automatically.</p>'''),
            ("The route is as follows", r'''<p>Sections 2–4 define velocity moments, identify the five collision invariants and derive the general moment equation. Sections 5–8 obtain the conservation laws for mass, momentum and energy. Section 9 introduces the closures leading to the Euler and Navier–Stokes equations. Section 10 then tests mass conservation against solar-wind measurements.</p>'''),
        ],
        3: [
            ("Module 2 derived the Euler equation", r'''<p><a href="module02.html">Module 2</a> derived the Euler equation and showed that viscosity is negligible in stellar interiors. We now apply that equation to a stationary, self-gravitating gas. The resulting balance between pressure and gravity determines the structure of stars and atmospheres.</p>'''),
            ("The Sun does not collapse in 29.5 minutes", r'''<p>The Sun has survived for about $4.6$ Gyr, or $8.2\times10^{13}$ free-fall times. A pressure gradient must therefore oppose gravity with high accuracy. Hydrostatic equilibrium describes this leading balance and constrains the radial profiles of pressure and density.</p>'''),
            ("is the time in which a star of luminosity", r'''<p>The Kelvin–Helmholtz time is the time required for a star of luminosity $L$ to radiate an energy comparable to its gravitational binding energy. For the Sun it is $31.4$ Myr, more than $5\times10^{11}$ free-fall times. Secular evolution is therefore slow compared with dynamical adjustment, allowing the Sun to remain close to hydrostatic equilibrium as it evolves.</p>'''),
            ("The module follows the three-part shape", r'''<p>Sections 3 and 4 apply hydrostatic balance to the terrestrial atmosphere. Sections 5–8 extend the calculation to self-gravitating polytropes and derive the Lane–Emden equation. Sections 9 and 10 compare the resulting profiles with a standard solar model and with helioseismic measurements.</p>'''),
        ],
        4: [
            ("Module 3 set the velocity to zero", r'''<p><a href="module03.html">Module 3</a> described a gas in hydrostatic equilibrium. We now perturb that equilibrium and retain only terms linear in the disturbance. The calculation produces acoustic waves and introduces the perturbative method used for the instabilities in Modules 5–7.</p>'''),
            ("The Sun supplies the astrophysical half", r'''<p>The Sun supports standing acoustic modes with periods near five minutes. Their frequencies are measured with high precision. Modes of fixed angular degree and consecutive radial order are separated by the large frequency separation, which is controlled mainly by the acoustic travel time across the star.</p>'''),
            ("The module follows the three-part shape", r'''<p>Sections 2 and 3 derive the acoustic wave equation and compare isothermal and adiabatic sound speeds with measurements in air. Sections 4 and 5 introduce gravitational stratification and standing modes. Sections 6 and 7 use the solar frequency separation to test the sound-speed profile and its thermodynamic closure.</p>'''),
        ],
        5: [
            ("The question has a concrete astronomical form", r'''<p>Barnard 68 provides a concrete test case. It is a small, isolated molecular cloud with a fitted mass of $2.10\,M_\odot$, radius $1.25\times10^4$ au and temperature $16$ K at the adopted distance of $125$ pc. These values imply a mean density of $1.5245\times10^{-19}\ \mathrm{g\,cm^{-3}}$.</p>'''),
            ("Two stability criteria are derived", r'''<p>Two commonly used criteria give different answers for Barnard 68. The Jeans criterion treats the cloud as part of a uniform medium and predicts a critical mass of $2.97\,M_\odot$, classifying the cloud as stable. The Bonnor–Ebert criterion treats it as a pressure-confined isothermal sphere. Its fitted dimensionless radius, $\xi_{\max}=6.9\pm0.2$, exceeds the critical value $6.4508$ and therefore indicates instability.</p>'''),
            ("Both criteria come from the same fluid equations", r'''<p>The disagreement arises from the background states used in the two derivations. The standard Jeans calculation perturbs a uniform static medium that is not a self-consistent finite equilibrium. The Bonnor–Ebert calculation perturbs a pressure-confined equilibrium sphere. Sections 3–5 derive both approaches, while Sections 6 and 7 compare them with Barnard 68 and other Bok globules.</p>'''),
        ],
        6: [
            ("Module 3 solved the hydrostatic equation", r'''<p>Hydrostatic balance does not guarantee stability. A stratified fluid can satisfy force balance at every point and still amplify a displaced parcel. This module studies two such failures: buoyant convection and radiative thermal instability.</p>'''),
            ("The first is buoyancy", r'''<p>Consider a parcel displaced upward into a region of lower pressure. It expands as it moves. If it remains denser than its new surroundings, buoyancy restores it; if it becomes lighter, it continues to rise. Sections 2–5 express this comparison through the Schwarzschild and Ledoux criteria and examine the effect of partial ionisation. Sections 6 and 7 then estimate the convective heat flux and compare it with solar observations.</p>'''),
            ("The second is cooling", r'''<p>Thermal instability follows a different feedback. A compressed parcel that loses heat faster than its surroundings cools and contracts further at nearly constant pressure. Sections 8 and 9 derive Field's criterion and the resulting two-phase equilibrium. Section 10 compares the predicted pressure range with measurements along 89 interstellar sight lines.</p>'''),
        ],
        7: [
            ("Modules 5 and 6 asked whether", r'''<p>Modules 5 and 6 studied perturbations of smoothly varying fluids. We now consider a sharp interface separating two fluids. Perturbations on both sides must satisfy common boundary conditions, producing the Rayleigh–Taylor and Kelvin–Helmholtz instabilities as limits of one dispersion relation.</p>'''),
            ("Rayleigh–Taylor. Put the heavy fluid on top", r'''<p><b>Rayleigh–Taylor instability.</b> When a dense fluid lies above a lighter one in a gravitational field, an interchange lowers the gravitational potential energy. Dense spikes descend while light bubbles rise. Surface tension can stabilise sufficiently short wavelengths in laboratory fluids; an interface between plasmas requires magnetic or finite-thickness effects instead.</p>'''),
            ("Kelvin–Helmholtz. Now let the two fluids", r'''<p><b>Kelvin–Helmholtz instability.</b> A velocity difference parallel to an interface can amplify a ripple through its associated pressure perturbation. Gravity, when directed across the interface, stabilises sufficiently long wavelengths. Surface tension or magnetic tension can stabilise short wavelengths.</p>'''),
            ("The two halves of the module are tested differently", r'''<p>The two applications have different evidential strength. A laser-driven Rayleigh–Taylor experiment reports a mixing coefficient with a standard deviation. The solar Kelvin–Helmholtz observation gives approximate inputs without a full uncertainty budget. It therefore constrains a magnetic-field component but does not provide a precise measurement of it.</p>'''),
        ],
        8: [
            ("Write out the equations of Module 2", r'''<p>The inviscid equations contain no microscopic length scale. Viscosity and thermal conduction, which would set the internal thickness of a shock, were neglected in <a href="module02.html">Module 2</a>. The resulting equations can therefore admit discontinuities whose thickness is unresolved but whose jumps are fixed by conservation laws.</p>'''),
            ("The gain from the idealisation", r'''<p>Integrating the conservation laws across a thin shock relates the upstream and downstream states without resolving the internal layer. These Rankine–Hugoniot conditions determine the density, pressure and temperature jumps from the upstream Mach number and the equation of state.</p>'''),
            ("A second absence of length drives", r'''<p>A point explosion in a uniform medium also begins without an intrinsic length scale. Dimensional analysis of the explosion energy $E$, ambient density $\rho_0$ and time $t$ gives $R\propto(Et^2/\rho_0)^{1/5}$. The exponent $2/5$ follows before the internal similarity solution is calculated.</p>'''),
            ("Four years later the argument met a test", r'''<p>The Trinity photographs provide a direct test of this scaling. Taylor tabulated 25 fireball radii and times and compared them with the similarity prediction published during the war. Section 5 repeats the fit. The exponent agrees closely with $2/5$, while structured residuals reveal limitations of the simplest model.</p>'''),
            ("The module then leaves the laboratory twice", r'''<p>Section 6 applies the jump conditions to Voyager 2 measurements of the solar-wind termination shock, using Neptune's bow shock as a control. Section 7 follows the evolution of a supernova remnant into its radiative phase. Section 8 discusses the Rayleigh–Taylor structure of Tycho's remnant and explains why a constant-acceleration planar mixing law cannot be transferred directly to an expanding shell.</p>'''),
            ("The direction of the remaining error is known", r'''<p>The ambient density used by Taylor is another source of systematic uncertainty. The Trinity site lies above sea level, so its air density was lower than the adopted $1.25\times10^{-3}\ \mathrm{g\,cm^{-3}}$. Because the inferred energy is proportional to $\rho_0$, a lower density would reduce the recovered energy and increase the discrepancy with the comparison yield. The available sources do not provide a site-specific density, so only the direction of this correction is used.</p>'''),
        ],
        9: [
            ("The module in one picture", r'''<figcaption>A central mass drives a steady spherical flow. The dashed circle marks the critical radius, where a regular solution can pass between subsonic and supersonic branches. Reversing the velocity changes a Parker wind into Bondi accretion while leaving the stationary differential equation unchanged; the boundary conditions select different branches.</figcaption>'''),
            ("The singular point is the reason", r'''<p>At the critical radius, the coefficient of $\mathrm{d}v/\mathrm{d}r$ vanishes. A regular solution requires the remaining numerator to vanish there as well. This condition selects a transonic branch from a continuum of formal solutions. For a wind, the selected branch begins subsonically and becomes supersonic; the usual accretion branch has the opposite ordering.</p>'''),
            ("The module then does what this book always does", r'''<p>The theory is tested in two regimes. Solar-wind measurements probe the velocity and pressure gradients of an outflow. Measurements around Sagittarius A* test how a spherical outer supply estimate relates to conditional bounds and radiation from the inner accretion flow.</p>'''),
            ("The anchor is the solar wind", r'''<p>Venzmer and Bothmer (2018) fitted density, temperature, magnetic-field and velocity power laws to Helios data over $0.29$–$0.98$ au. These independently fitted exponents test the solution family and the radial momentum equation. They also permit comparison with the mass-conservation and energy-equation tests in <a href="module02.html">Module 2</a>.</p>'''),
            ("The steady equations alone do not uniquely", r'''<p>The steady equations bound the accretion rate but do not, by themselves, prove that nature selects the transonic solution. Bondi supplied an additional physical selection argument. We therefore distinguish consequences of the differential equation from conclusions that depend on this choice of branch.</p>'''),
        ],
        10: [
            ("Module 2 derived the Navier–Stokes equation", r'''<p><a href="module02.html">Module 2</a> derived the Navier–Stokes equation and showed that viscosity is small in many astrophysical flows. A small viscous term does not mean that viscosity is irrelevant. In a turbulent flow, nonlinear advection transfers kinetic energy to small scales, where even a small viscosity can dissipate it.</p>'''),
            ('"Large enough" is not a number', r'''<p>No universal Reynolds number marks the onset of turbulence. Pipe flow becomes turbulent near $\mathrm{Re}\approx2300$, whereas a flat-plate boundary layer may remain laminar to about $5\times10^5$. Geometry and disturbances affect the transition. Astrophysical Reynolds numbers often exceed either value by many orders of magnitude, so the precise threshold is not important here.</p>'''),
            ("This module's choice, stated once", r'''<p>Throughout this module, $\bar v=\sqrt{8k_{\rm B}T/(\pi m)}$ denotes the mean thermal speed used in the kinetic-theory viscosity $\nu=\lambda\bar v/3$. Module 2 instead used $v_{\rm th}=\sqrt{2k_{\rm B}T/m}$. The two conventions differ by a factor $\sqrt{4/\pi}=1.1284$, which is included explicitly in the cross-module comparisons of <a class="secref" href="#fluids">§6</a>.</p>'''),
            ("A Reynolds number of $10^{9}$", r'''<p>The visible solar surface has a Reynolds number of order $10^9$, already larger than laboratory values and smaller than many other astrophysical examples. Direct calculation of all dynamically active scales is therefore impractical. Statistical scaling arguments can nevertheless predict spectra and scale relations without resolving every eddy.</p>'''),
        ],
        11: [
            ("Module 9 built spherical accretion", r'''<p>Spherical accretion neglects angular momentum. Gas approaching Sagittarius A* is expected to circularise near $100\,r_S$, roughly $2{,}000$ times inside the quoted Bondi radius. Once a disc forms, further accretion requires angular momentum to move outward while mass moves inward.</p>'''),
            ("The plan of this module is one problem", r'''<p>A Keplerian disc is stable to axisymmetric centrifugal disturbances, yet molecular viscosity transports angular momentum far too slowly. The central problem is therefore to identify an effective stress large enough to drive the observed accretion. The $\alpha$ prescription parameterises that stress, while later sections compare the required values with observations and simulations.</p>'''),
            ("Two worked discs carry the rest", r'''<p>Two representative disc configurations are used throughout the module. Their parameters are round values characteristic of their respective classes rather than measurements of named systems. This distinction matters when numerical examples are compared with observations.</p>'''),
        ],
    }
    edits: list[str] = []
    for needle, markup in data.get(module, []):
        if replace_block(soup, needle, markup):
            edits.append("narrative-spine paragraph")
    return edits


def tighten_long_prose(soup: BeautifulSoup, module: int) -> list[str]:
    """Rewrite the remaining long expository sentences outside source notes."""
    data = {
        1: [
            ("below which the notion of a classical impact parameter", r'''<p>The lower cutoff is the larger of two scales. The classical scale $b_{90}$ marks the failure of the small-angle approximation. The reduced de Broglie length $\hbar/(mv)$ marks the failure of a classical impact parameter because the transverse position cannot be specified more accurately. This reduced wavelength differs from the thermal de Broglie wavelength $h/\sqrt{2\pi m k_BT}$.</p>'''),
            ("The evidence this figure supports is that $\\lambda$ alone decides nothing", r'''<figcaption>A mean free path becomes meaningful only after comparison with a macroscopic scale. The solar corona and hot interstellar medium differ in density by eleven orders of magnitude, yet their Knudsen numbers differ by only a factor of $2.8$. Their system sizes compensate for much of the difference in mean free path.</figcaption>'''),
            ("The evidence this figure supports is the central claim", r'''<figcaption>Most entries lie well inside the Euler regime even though their densities are extremely low, because their macroscopic scales are correspondingly large. The solar wind is the exception in this census: its mean free path is not small compared with the scale being resolved.</figcaption>'''),
        ],
        5: [
            ("A perturbation that starts growing at $z_*", r'''<p>For the growing mode, a perturbation beginning at $z_*=1089.92$ grows in proportion to the scale factor. The available growth factor is therefore $1+z_*=1090.92$, rather than an exponential of elapsed time divided by $t_{\rm grow}$. Initial data with $\dot\delta=0$ place $3/5$ of the amplitude in this growing mode.</p>'''),
            ("The rate is $(G\\rho_c)^{1/2}$ times a function", r'''<p>The instability rate has the form $(G\rho_c)^{1/2}f(\xi_{\max})$. The function $f$ vanishes at $\xi_{\rm crit}$, where the equilibrium sequence changes stability. Barnard 68 lies only $6.96$ per cent above this threshold, so its departure from equilibrium can be much slower than the free-fall time of $1.70\times10^5$ yr computed from its mean density.</p>'''),
        ],
        6: [
            ("$N$ is computed twice on the right", r'''<p>Table 1 lists the buoyancy frequency, and the upper panel of Fig. 2 plots it. The right-hand columns use two adiabatic gradients: the ideal monatomic value $0.4$ and the model plateau $0.3957$. The latter includes the equation-of-state corrections from Coulomb interactions and radiation pressure.</p>'''),
            ("The BS2005-AGS,OP table stops", r'''<p>The BS2005-AGS,OP table ends at $r=0.98308\,R$, below the photosphere. The surface estimate therefore uses independent inputs: $T=5772$ K, $P=1.2\times10^5\ \mathrm{dyn\,cm^{-2}}$ at $\tau=2/3$, and $\mu=1.2250$ from the surface hydrogen and helium fractions.</p>'''),
            ("Note also that $(\\partial\\mathcal{L}/\\partial\\rho)_T", r'''<p>Here $(\partial\mathcal L/\partial\rho)_T=\Lambda/m_{\rm H}^2>0$. The isochoric condition, $d\ln\Lambda/d\ln T<0$, is therefore stricter than the isobaric condition, $d\ln\Lambda/d\ln T<1$. Every isochorically unstable state on this equilibrium curve is also isobarically unstable, but the converse does not hold. ∎</p>'''),
            ("One property of the source has to be said", r'''<p>Wolfire's quoted $P_{\rm th,ave}$ is the geometric mean $\sqrt{P_{\min}P_{\max}}$ in all five variants of Table 6. The calculated values are $3070.4$, $2216.8$, $3681.3$, $2488.7$ and $2410.6\ \mathrm{K\,cm^{-3}}$, consistent with the rounded table entries.</p>'''),
            ("Across the five variants of Table 6", r'''<p>The fitted lognormal assigns between $0.9$ and $10.0$ per cent of the gas to pressures below $P_{\min}$ across the five model variants. A static two-phase model permits none there. The observed low-pressure tail therefore persists under every parameter choice in the table.</p>'''),
            ("Problem D3 makes that quantitative", r'''<p>Problem D3 compares each cooling time with the crossing time of a turbulent eddy. The warm and cold phases differ in cooling length by a factor of $794$. A cold excursion below $P_{\min}$ is therefore short-lived, whereas a warm departure can persist over a much larger distance.</p>'''),
        ],
        7: [
            ("Water over air at $20", r'''<p>For water over air at $20\ ^\circ$C, $\rho_t=0.998207\ \mathrm{g\,cm^{-3}}$, $\rho_b=1.2041\times10^{-3}\ \mathrm{g\,cm^{-3}}$ and $T_s=72.75\ \mathrm{dyn\,cm^{-1}}$. These values give $A=0.997590$. The air's inertia is therefore negligible in the usual hand calculation.</p>'''),
            ("Its axis annotations name three quantities", r'''<figcaption>The annotations use three inputs introduced later. The measured shear is $\Delta U=20\ \mathrm{km\,s^{-1}}$, and the density ratio across the coronal-mass-ejection flank is $2.24$. The electron density $n_e=3\times10^8\ \mathrm{cm^{-3}}$ is a reference value from <a href="module01.html">Module 1</a>, not a measurement of this event.</figcaption>'''),
            ("Second, the e-folding counts", r'''<p>The predicted amplification ranges from $3$ to $12$ e-foldings over the plotted decade in wavelength. A young remnant is therefore many growth times old on scales between $0.01R$ and $0.1R$. Linear theory can diagnose the instability, but it cannot describe the nonlinear structures seen in an image.</p>'''),
        ],
        8: [
            ("The whole difference is one closure", r'''<p>The distinction is whether the shocked layer retains its heat or radiates it away. At $10$ K the rotational states of molecular hydrogen are largely frozen out because their characteristic temperature is about $85$ K. The gas then has three active translational degrees of freedom, so $\gamma=5/3$ is the appropriate ideal-gas value.</p>'''),
            ("The three later blocks are chosen", r'''<p>The later fitting blocks follow Taylor's authority labels with two adjustments. The first authority-A row is isolated because the model is expected to fail at the earliest time. Authorities C and D are combined because category D contains only two rows.</p>'''),
            ("That the density jump and the speed drop", r'''<p>Equation (2.2) requires the density jump to equal the inverse velocity jump in the shock frame. The measured ratios agree within the quoted precision. A planetary bow shock is nearly stationary in the frame used for these spacecraft measurements, so the observed speeds provide the required shock-frame comparison.</p>'''),
        ],
        9: [
            ("A decade in $T_0$ costs", r'''<p>Increasing $T_0$ by a decade reduces the logarithmic slope by $52$ per cent from $0.5$ to $5$ MK, $46$ per cent from $1$ to $10$ MK, $41$ per cent from $2$ to $20$ MK and $36$ per cent from $5$ to $50$ MK. The declining fractional change follows the expected $1/(2\ln x)$ dependence.</p>'''),
            ("Redoing (7.3) for a pure proton plasma", r'''<p>For a pure proton plasma, $\rho=n_{\rm p}m_{\rm p}$ and $n_{\rm tot}=2n_{\rm p}$, giving $\mu=m_{\rm p}/(2m_{\rm u})=0.50364$. This raises $c_T^2$ by a factor $1.1163$ to $1.5964\times10^{13}\ \mathrm{cm^2\,s^{-2}}$. The predicted acceleration becomes $0.01890\pm0.00068$, reducing the observed-to-predicted ratio from $2.98$ to $2.59$ and the shortfall from $3.2\sigma$ to $3.0\sigma$.</p>'''),
            ("Both lie comfortably inside the equatorial range", r'''<p>Both mass-flux estimates lie within the measured equatorial range, so the adopted helium fraction does not control the conclusion. <a href="module02.html">Module 2</a> used a different row of the same table, with lower density and speed. Its smaller mass flux follows from those inputs rather than from the helium convention.</p>'''),
        ],
        10: [
            ("The air point is drawn open", r'''<figcaption>The air point uses the measured viscosity rather than the kinetic-theory estimate $\lambda\bar v/3$, so it does not lie on its grey reference line. Its Reynolds number is lower by a factor $1.44$, the reciprocal of the viscosity ratio $0.69$ discussed above.</figcaption>'''),
            ("intracluster outskirts row", r'''<p>In the intracluster-outskirts entry of <a href="module01.html">Module 1</a>, $n=10^{-4}\ \mathrm{cm^{-3}}$, $T=10^8$ K and $L=2$ Mpc. The resulting $\lambda=222$ kpc and $\mathrm{Kn}=0.11$ are ten times the core mean free path, partly offset by a system size twice as large.</p>'''),
            ("intracluster row is not comparable", r'''<p>The intracluster example in <a href="module02.html">Module 2</a> uses $n=10^{-2}\ \mathrm{cm^{-3}}$, $T=3\times10^7$ K, $L=100$ kpc and $u=300\ \mathrm{km\,s^{-1}}$. It represents a different radius and thermodynamic state from the core model used here, so the two Reynolds numbers should not be interpreted as estimates for the same gas.</p>'''),
            ("Goldstein (2007) took Wind spacecraft data", r'''<p>Podesta, Roberts and Goldstein (2007) fitted magnetic, velocity, kinetic-energy and total-energy spectra from Wind measurements at 1 au. Their four intervals sample solar minimum, maximum, and the ascending and descending phases of the cycle. Each interval spans 54–81 days.</p>'''),
            ("Two exponents are now in play", r'''<p>Two candidate exponents are relevant: $5/3$ for a Kolmogorov-like cascade and $2$ for a shock-dominated field. They differ by a factor $2.15$ in power per decade of wavenumber. Section 10 tests which scaling better describes a molecular cloud.</p>'''),
        ],
        12: [
            ("Module 10 §7.2 confirmed Kolmogorov's", r'''<p><a href="module10.html">Module 10 §7.2</a> found a magnetic-spectrum exponent close to $-5/3$ in the solar wind. Its hydrodynamic dimensional argument does not explain why a magnetised plasma should share that value. Magnetised-turbulence theory supplies a separate route to the same perpendicular spectral exponent.</p>'''),
        ],
    }
    edits: list[str] = []
    for needle, markup in data.get(module, []):
        if replace_block(soup, needle, markup):
            edits.append("long-sentence rewrite")
    return edits


def main() -> None:
    manifest = {"edition": "Human-written prose pass", "modules": []}
    for module in range(1, 13):
        path = DEST / f"module{module:02}.html"
        before = digest(path)
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        edits = rewrite_shared(soup, module)
        if module == 12:
            edits.extend(rewrite_module12(soup))
        else:
            edits.extend(rewrite_other_modules(soup, module))
        edits.extend(tighten_long_prose(soup, module))
        clean_mechanics(soup)
        clause_splits = split_overloaded_clauses(soup)
        # Mark the edition without adding process narration to the teaching text.
        notice = soup.select_one(".codex-revision")
        if notice:
            notice.clear()
            notice.append(BeautifulSoup(
                '<b>Codex textbook rewrite.</b> This separate edition incorporates the scientific audit and a paragraph-level prose revision. '
                f'The original <a href="../../afd/module{module:02}.html">source module</a> remains unchanged. '
                '<a href="../AUDIT_REPORT.html">Editorial record.</a>',
                "html.parser",
            ))
        path.write_text("<!DOCTYPE html>\n" + str(soup).replace("<!DOCTYPE html>\n", "", 1), encoding="utf-8")
        manifest["modules"].append({
            "module": module,
            "pre_rewrite_sha256": before,
            "post_rewrite_sha256": digest(path),
            "explicit_rewrites": edits,
            "overloaded_blocks_split": clause_splits,
        })
    build_path = DEST / "build-manifest.json"
    if build_path.exists():
        build = json.loads(build_path.read_text(encoding="utf-8"))
        for record in build.get("modules", []):
            record["revised_sha256"] = digest(DEST / f"module{record['module']:02}.html")
        build["prose_rewrite"] = "paragraph-level pass; see prose-rewrite-manifest.json"
        build_path.write_text(json.dumps(build, indent=2, ensure_ascii=False), encoding="utf-8")
    (DEST / "prose-rewrite-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
