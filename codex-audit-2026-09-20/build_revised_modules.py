"""Build Codex's revised copies of Modules 01-12 without editing afd/module*.html.

Run one module at a time:
    python build_revised_modules.py 1
"""
from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
AUDIT = Path(__file__).resolve().parent
DEST = AUDIT / "revised-modules"
DATA = json.loads((AUDIT / "findings.json").read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_nodes(markup: str) -> list:
    return list(BeautifulSoup(markup, "html.parser").contents)


def best_target(soup: BeautifulSoup, quote: str) -> Tag:
    candidates = []
    for tag in soup.find_all(["p", "div", "figcaption", "th", "td", "h1", "h2", "h3", "h4", "li"]):
        if quote in tag.get_text(" ", strip=True):
            candidates.append(tag)
    shallow = [
        tag for tag in candidates
        if not any(quote in child.get_text(" ", strip=True)
                   for child in tag.find_all(recursive=False))
    ]
    if shallow:
        return shallow[0]
    if candidates:
        return candidates[-1]
    raise RuntimeError(f"Could not locate quote: {quote!r}")


def replace_tag(tag: Tag, markup: str) -> None:
    nodes = parse_nodes(markup)
    first = True
    for node in nodes:
        if isinstance(node, NavigableString) and not str(node).strip():
            continue
        if first:
            tag.replace_with(node)
            first = False
        else:
            previous = node.previous_sibling
            if previous is not None:
                previous.insert_after(node)
    if first:
        tag.decompose()


def set_inner(tag: Tag, markup: str) -> None:
    tag.clear()
    fragment = BeautifulSoup(markup, "html.parser")
    wrapper = fragment.find(["p", "div"])
    nodes = list(wrapper.contents) if wrapper else list(fragment.contents)
    for node in nodes:
        tag.append(node)


def replace_text_once(soup: BeautifulSoup, old: str, new: str) -> bool:
    for node in soup.find_all(string=True):
        if old in str(node):
            node.replace_with(NavigableString(str(node).replace(old, new, 1)))
            return True
    return False


def replace_contiguous(start: Tag, stop: Tag, markup: str) -> None:
    cursor = start
    while cursor is not stop:
        nxt = cursor.next_sibling
        cursor.extract()
        cursor = nxt
    for node in parse_nodes(markup):
        if isinstance(node, NavigableString) and not str(node).strip():
            continue
        stop.insert_before(node)


def repair_navigation(soup: BeautifulSoup) -> None:
    """Keep the twelve-module edition free of dead local links."""
    for a in list(soup.find_all("a", href=True)):
        href = a["href"]
        if href in {"module13.html", "module14.html"}:
            a.name = "span"
            del a["href"]
            a["title"] = "Planned module; not present in this twelve-module edition"
        elif href == "module02.html#boltzmann":
            a["href"] = "module02.html#transfer"


def add_revision_notice(soup: BeautifulSoup, module: int, source_hash: str) -> None:
    title = soup.title
    if title:
        title.string = f"Codex revised copy — {title.get_text()}"
    head = soup.head
    meta = soup.new_tag("meta")
    meta["name"] = "author"
    meta["content"] = "Codex — OpenAI"
    head.append(meta)
    style = soup.new_tag("style")
    style.string = """
  .codex-revision{background:#102a2b;border:1px solid #2dd4bf;border-left:5px solid #2dd4bf;
    color:#d5fffa;padding:.75rem 1rem;margin:1rem 0 1.5rem;border-radius:5px;font: .9rem/1.55
    ui-sans-serif,system-ui,sans-serif}
  .codex-revision b{color:#5eead4}.codex-revision a{color:#fde68a}
"""
    head.append(style)
    h1 = soup.find("h1")
    notice = BeautifulSoup(
        f'<aside class="codex-revision"><b>Codex revised copy.</b> '
        f'Scientific and prose corrections from the independent audit have been applied to this copy. '
        f'The original <a href="../../afd/module{module:02}.html">module{module:02}.html</a> is unchanged. '
        f'Source SHA-256: <code>{source_hash[:16]}…</code>. '
        f'<a href="../AUDIT_REPORT.html">Read the signed audit.</a></aside>',
        "html.parser",
    ).aside
    if h1:
        sub = h1.find_next_sibling("p", class_="sub")
        (sub or h1).insert_after(notice)


def apply_style_edits(soup: BeautifulSoup, module: int) -> tuple[list[str], list[str]]:
    applied, superseded = [], []
    # Several audit quotations are identifying fragments rather than complete
    # sentences.  Replace the complete source wording so that the revision does
    # not leave a duplicated clause or stranded punctuation behind.
    full = {
        "P02": ("The Coulomb force has no range: two charges interact at any separation, so there is no distance $d$ inside which a collision happens and outside which it does not.", "The unscreened Coulomb force has no finite cutoff: two charges interact at every separation."),
        "P03": (r"Sixty-six micrometres, in an object $6.957\times10^{10}\ \mathrm{cm}$ across.", "The mean free path is about 66 micrometres, whereas the solar radius is $6.957\\times10^{10}\\ \\mathrm{cm}$. Their ratio measures the separation between microscopic and stellar scales."),
        "P04": ("The figure supports the claim that the magnetic rescue is one-dimensional: it makes the plasma fluid-like in two directions out of three.", "Gyromotion restricts motion across a locally uniform field, while particles remain free to stream along it. These two directions therefore require different transport descriptions."),
        "P05": ("There are five, so there are five: one scalar mass equation, three components of a momentum equation, and one energy equation.", "The five independent collision invariants yield five scalar conservation equations: one for mass, three for momentum and one for energy."),
        "P06": ("The second is advection — the gas at this point is not changing, but a denser parcel has arrived from upstream.", "The second is advection: a moving parcel experiences change as it crosses a spatial density gradient, even if the density at a fixed point is steady."),
        "P07": ("The subscript is not decoration.", "Here $\\mu$ denotes dynamic viscosity and $\\mu_{\\rm m}$ denotes mean molecular weight."),
        "P10": ("Hold that number.", "This pressure fraction tests the assumption that gas pressure dominates at the solar centre."),
        "P11": ("The difference is the latent heat released when water vapour condenses in rising air, which warms the parcel as it rises.", "Latent heat can reduce the cooling rate of a saturated rising parcel. The standard atmospheric lapse rate, however, is a reference profile rather than the result of this parcel calculation alone."),
        "P13": (r"So (1.2) tests the closure inside the Sun, as the $331.45\ \mathrm{m\,s^{-1}}$ tests it in air.", "The solar frequency spacing tests the interior sound-speed profile, just as the measured speed of sound in air tests the thermodynamic closure for air."),
        "P14": ("That is the whole of the disagreement between Newton and Laplace.", "The two predictions differ because one uses an isothermal pressure response and the other an adiabatic response."),
        "P21": ("where the premise is therefore spent.", "so pressure equilibration is less well separated from the parcel's motion and the approximation requires closer examination."),
        "P22": ("No single mixing length describes both.", "The local turnover time varies strongly with depth. This is compatible with a mixing length proportional to the local pressure scale height."),
        "P23": (r"The isochoric runaway fires nowhere in this table: $\Lambda$ increases with $T$ throughout, so $d\Lambda/dT\gt 0$ everywhere and (8.1) is never met.", r"The isochoric instability criterion is not satisfied anywhere in this table: $\Lambda$ increases with $T$ throughout, so $d\Lambda/dT\gt 0$ and (8.1) is never met."),
        "P24": ("This module takes two predictions to that measurement, in the shape Module 2 used: one confirmed and one refuted, from the same source table.", "We compare two predictions with the same source table, stating the assumptions and uncertainties for each comparison."),
        "P25": (r"Their $k$-dependences are all different — $k^2$, $k$, $k^3$, $k^2$ — and that is the whole story of which wavelengths grow:", r"The contributions scale as $k$, $k^2$ or $k^3$. Their signs and coefficients determine which wavelengths are unstable:"),
        "P26": ("Gravity charges by volume and the shear pays by area, so the longer the wave, the worse the bargain. Long waves have too much heavy fluid to lift.", r"For this interface, the stabilising gravity term is proportional to $k$, whereas the destabilising shear term is proportional to $k^2$. Gravity therefore dominates at sufficiently small $k$."),
        "P27": (r"The jet crosses $1$ kpc in $4.069\times10^{5}$ yr, so the incompressible theory says the interface has $0.99$ e-folding times in which to roll up over that length — marginal, and just interesting enough to believe.", r"The jet crosses $1$ kpc in $4.069\times10^{5}$ yr, so the predicted growth is about one e-folding over the crossing time. The interface may amplify a disturbance, but this estimate does not establish nonlinear roll-up."),
        "P33": ("This module does the thing neither of them did: it takes the steady spherical flow seriously as an equation to be solved, discovers that the equation has a singular point, and finds that almost everything worth knowing about stellar winds and about accretion onto compact objects follows from the behaviour of solutions near that point.", "We solve the steady spherical-flow equations and examine how regular passage through a critical point constrains the solution."),
        "P34": ("The corona must move. The question is how, and the answer is more constrained than it has any right to be.", "The corona must move. Regularity at the sonic point restricts the allowed flow profiles."),
        "P35": ("One thing must be said at the outset, because the module's first draft got it wrong and the correction is instructive.", "The steady equations alone do not uniquely select the accretion rate; the transonic solution also requires a physical selection argument."),
        "P36": ("asks whether it is quantitatively right, and the last column is where the answer lives.", "asks whether it is quantitatively right; the last column compares the predicted speed with the measured value."),
        "P37": ("There is exactly one result in the theory of turbulence that is exact, that follows from the Navier–Stokes equation rather than from counting units, and that has no adjustable constant at all.", "The four-fifths law is an exact relation derived from the Navier–Stokes equations under specified assumptions; its coefficient is not obtained from dimensional analysis."),
        "P38": ("Supersonic turbulence has nothing else: shocks compress gas, and the distribution of densities they produce is what makes stars.", "Supersonic turbulence also develops large density fluctuations, whose distribution is important for star formation."),
        "P40": ("Solomon, Rivolo, Barrett & Yahil (1987) did the measurement properly, with one survey, one distance scale and one cloud-finding algorithm applied to $273$ Galactic molecular clouds:", "Solomon and colleagues used one survey, one distance scale and one cloud-identification method for their sample of 273 Galactic molecular clouds:"),
        "P41": ("five decades inside the Bondi radius", "about 2,000 times smaller than the quoted Bondi radius"),
        "P43": ("No number in Module 9 depends on the factor — it is the size of a refutation that stays a refutation on any row of that table — so Module 9 is left as it stands, and the repayment is this paragraph rather than an edit to a shipped page.", "The comparison must use a bolometric luminosity and the mass flux reaching the emitting region before it can be interpreted as a radiative efficiency."),
        "P45": ("Twenty such promises are on the record, each with the file and line it was printed at, and this module exists to pay them.", "This module develops the magnetic stresses and induction equation, then applies them to waves, gravitational support, transport and disc instability."),
    }
    for item in [x for x in DATA["prose"] if x["module"] == module]:
        old, new = full.get(item["id"], (item["quote"], item["rewrite"]))
        if replace_text_once(soup, old, new):
            applied.append(item["id"])
        else:
            superseded.append(item["id"])

    # Two examples span inline links, and one is a complete explanatory note.
    if module == 4:
        for p in soup.find_all("p"):
            if "The last sentence of Definition 1 is quoted" in p.get_text(" ", strip=True):
                replace_tag(p, r'''<p>Equation (2.4) follows from (2.3) by the chain rule along a parcel's path, since $s$ is constant along that path. Module 2's condition $D(P/\rho^\gamma)/Dt = 0$ is (2.4) with $\Gamma_1=\gamma$ constant. We postpone the thermodynamics of partial ionisation to <a href="module06.html">Module 6</a>. Here it identifies one limitation of the constant-$\gamma$ closure and is used in <a class="secref" href="#check4">§7.3</a> only as a candidate explanation of a measured shortfall.</p>''')
                if "P16" not in applied: applied.append("P16")
                if "P16" in superseded: superseded.remove("P16")
                break
    if module == 11:
        for p in soup.find_all("p"):
            if "a Keplerian disc threaded by" in p.get_text(" ", strip=True) and "magnetorotational" in p.get_text(" ", strip=True):
                replace_tag(p, r'''<p>Definition 2 named and bounded the stress but did not identify the physical process that supplies it. <a href="module12.html">Module 12 §9</a> supplies one answer: in ideal MHD, a sufficiently weak field can destabilise differential rotation when an unstable wavelength fits within the disc. Non-ideal effects can alter this conclusion. For a Keplerian disc the maximum ideal-MHD growth rate is $\gamma_{\max}=(q/2)\Omega$.</p>''')
                if "P44" not in applied: applied.append("P44")
                if "P44" in superseded: superseded.remove("P44")
                break
    if module == 12:
        for p in soup.find_all("p", class_="small"):
            if "photosphere's" in p.get_text(" ", strip=True) and "0.41" in p.get_text(" ", strip=True):
                replace_tag(p, r'''<p class="small">The last column is $1/\beta$ by construction and carries no new information; it is printed so that the two pressures can be compared directly. For the adopted $5$ G photospheric field, $p_{\rm mag}\approx1\ \mathrm{dyn\,cm^{-2}}$, much smaller than the adopted gas pressure.</p>''')
                if "P46" not in applied: applied.append("P46")
                if "P46" in superseded: superseded.remove("P46")
                break
    return applied, superseded


def apply_content_edits(soup: BeautifulSoup, module: int) -> list[str]:
    items = [x for x in DATA["content"] if x["module"] == module]
    targets = {x["id"]: best_target(soup, x["quote"]) for x in items}
    applied = []
    inner_ids = {"C11", "C16", "C23", "C26", "C27", "C30", "C33"}
    special_ids = {"C03", "C07", "C08"}
    for item in items:
        cid, target = item["id"], targets[item["id"]]
        if cid in special_ids:
            continue
        if cid in inner_ids:
            if cid == "C11":
                target.clear()
                target.append(NavigableString(r"median $\rho/\langle\rho\rangle$"))
                table = target.find_parent("table")
                table.insert_before(BeautifulSoup(item["replacement"], "html.parser"))
                replace_text_once(
                    soup,
                    "the most probable density is below the mean density, and by an amount fixed entirely by the width.",
                    r"$e^{s_0}$ is the median density ratio and is below the mean; the mode of the density PDF is $e^{s_0-\sigma_s^2}$.",
                )
            elif cid == "C30":
                target.clear()
                target.append(NavigableString("Venzmer & Bothmer mean fits (Module 9)"))
            else:
                set_inner(target, item["replacement"])
        else:
            replace_tag(target, item["replacement"])
        applied.append(cid)

    # C07: retain the proposition and proof; correct their physical interpretation.
    if module == 2:
        c = next(x for x in items if x["id"] == "C07")
        prop = targets["C07"]
        replace_text_once(
            prop,
            "The density cancels, so the Reynolds number of a gas depends on its temperature, speed and size but not on how much of it there is.",
            "The explicit density factor cancels, but density still enters through the mean free path.",
        )
        prop.insert_after(BeautifulSoup(c["replacement"], "html.parser"))
        replace_text_once(
            soup,
            "the factor $\\rho$ cancelling between numerator and denominator. The cancellation is the density-independence of viscosity established in Module 1: $\\lambda\\propto 1/n$ falls exactly as fast as the number of momentum carriers $n$ rises.",
            "the explicit factor $\\rho$ cancelling between numerator and denominator. This algebra does not remove the density dependence contained in $\\lambda$; for neutral hard spheres, $\\lambda\\propto1/n$ and hence $\\mathrm{Re}\\propto n$ at fixed $u$, $L$, $T$ and cross-section.",
        )
        applied.append("C07")

    # C08: remove the incorrect spatial integral as well as its probabilistic interpretation.
    if module == 1:
        c = next(x for x in items if x["id"] == "C08")
        target = targets["C08"]
        prev = target.previous_sibling
        while prev is not None and isinstance(prev, NavigableString) and not str(prev).strip():
            old = prev
            prev = prev.previous_sibling
            old.extract()
        if isinstance(prev, NavigableString) and "\\int_0^{1}" in str(prev):
            prev.extract()
        replace_tag(target, c["replacement"])
        applied.append("C08")

    # C03: replace the entire invalid Tycho bound and its dependent verdict.
    if module == 8:
        start = soup.find("h3", id="tychosetup")
        stop = soup.find("h2", id="limits")
        replacement = r'''
<h3 id="tychosetup">8.1 Why the acceleration history matters</h3>
<p>The planar relation $h=\alpha Agt^2$ used in Module 7 assumes constant acceleration. A self-similar shell with $R=Ct^m$ has $g(t)=m(1-m)Ct^{m-2}$, so substituting the instantaneous value of $g$ into the constant-acceleration formula does not give a bound on the accumulated width.</p>
<p>For comparison, the history-dependent Read prescription quoted in Module 7 gives</p>
$$ \frac{h}{R}=\frac{4\alpha A(1-m)}{m}\left[1-\left(\frac{t_0}{t}\right)^{m/2}\right]^2,\qquad 0<m<1, $$
<p>when the integration begins at $t_0$. This result differs from $\alpha A m(1-m)$ and depends on the onset time. At $m=1/2$ and $t_0=0$, the two expressions differ by a factor of 16. The calculation demonstrates why an acceleration history is required; it is not a validated model of a curved, expanding supernova shell.</p>
<h3 id="tychoresult">8.2 What the Tycho comparison can establish</h3>
<p>The published radii remain informative. A one-dimensional hydrodynamic calculation places the contact discontinuity near $0.77R_{\rm BW}$, a two-dimensional calculation places Rayleigh–Taylor fingers near $0.85R_{\rm BW}$, and the reported mean contact discontinuity in Tycho is near $0.93R_{\rm BW}$. These positions show that the real or simulated shell contains structure absent from the smooth one-dimensional profile.</p>
<div class="keyresult"><b>Check 7 — no quantitative transfer test is established.</b> The constant-acceleration plane-interface law cannot be converted into a shell-width upper bound by inserting the shell's instantaneous deceleration. The observed widths therefore cannot be used here to reject that law by a factor of eleven. A quantitative comparison requires an expanding-shell model that specifies the acceleration history, curvature, density evolution, bubble-versus-spike coefficient and onset time.</div>
<h3 id="tychowhy">8.3 Physical complications that a shell model must include</h3>
<p>Several effects can change the interface position or apparent width: dense ejecta clumps retain information about the initial conditions; spikes and bubbles need not share one coefficient at large Atwood number; projection and threshold choices alter the inferred radii; and cosmic-ray acceleration can move the blast wave relative to the contact discontinuity. These effects explain why a planar coefficient cannot be transferred without a dynamical shell calculation. They do not, by themselves, identify a unique corrected coefficient.</p>
<span class="prov">The quoted radii and caveats are retained from Wang &amp; Chevalier (2001) and Warren et al. (2005). The former comparison is descriptive. No significance or factor-of-eleven rejection is assigned.</span>
'''
        replace_contiguous(start, stop, replacement)
        applied.append("C03")
    return applied


def repair_dependencies(soup: BeautifulSoup, module: int) -> list[str]:
    notes = []
    def r(old, new, label):
        if replace_text_once(soup, old, new):
            notes.append(label)

    if module == 4:
        r(
            r"as the $331.45\ \mathrm{m\,s^{-1}}$ excluded it in air",
            "just as the measured speed of sound excluded it for dry air under the stated conditions",
            "sound-speed comparison wording",
        )

    if module == 3:
        r(
            "If the Sun contracted on its Kelvin–Helmholtz time of $31.4$ Myr, gravity and the pressure gradient would still have to balance to $2.587\\times10^{-24}$ of the surface gravity, by (2.5). On the nuclear timescale of $1.036\\times10^{10}$ yr, on which the Sun actually evolves, the fraction is $2.379\\times10^{-29}$.",
            "For a deliberately slow, approximately homologous contraction on the Kelvin–Helmholtz time, equation (2.5) gives a characteristic secular acceleration $2.587\\times10^{-24}$ times the surface gravity. This is a scale estimate for that assumed evolution, not an observational upper bound on oscillatory, convective or other local accelerations.",
            "hydrostatic result box",
        )
    if module == 6:
        r(
            "Locating the base of the convection zone again with $\\nabla_{\\rm ad}+\\nabla_\\mu$ in place of $\\nabla_{\\rm ad}$, using the same locator, moves it from $0.7269\\,R$ to $0.7306\\,R$: a shift of $0.0037\\,R$, or $0.37$ per cent of the solar radius. And that is an upper bound, because the $\\nabla_\\mu$ the table gives near the base is partly the effective-$\\mu$ artefact described next.",
            "If the table's effective $\\mu$ is inserted as though it were a conserved composition variable, the locator moves from $0.7269\\,R$ to $0.7306\\,R$. Because that substitution is not thermodynamically consistent near the ionisation zone, the displacement is only a diagnostic of the approximation and is not an upper bound on the physical boundary shift.",
            "effective-mu boundary claim",
        )
    if module == 7:
        for li in list(soup.find_all("li")):
            text = li.get_text(" ", strip=True)
            if "reader should know the verdict before going there" in text:
                replace_tag(li, r'''<li><b>The Rayleigh–Taylor half of this module is not tested here against an astronomical measurement.</b> Section 8 checks the nonlinear plane-interface law against a laser experiment. <a href="module08.html#tycho">Module 8 §8</a> compares published shell radii for Tycho's supernova remnant, but it also shows why inserting a shell's instantaneous deceleration into a constant-acceleration mixing law does not produce a valid accumulated width. That comparison is descriptive until an expanding-shell model specifies the acceleration history, curvature, density evolution and onset time.</li>''')
                notes.append("Module 8 Tycho dependency")
            elif "refutes the transfer of (8.1)" in text:
                replace_tag(li, r'''<li><b>Sought and not readable.</b> C. Foullon et al., <em>ApJL</em> <b>729</b>, L8 (2011), and J. J. Hester et al., <em>ApJ</em> <b>456</b>, 225 (1996), were not readable in full from the project sources, so no numerical claim is taken from them. <a href="module08.html#tycho">Module 8 §8</a> discusses Tycho using Warren et al. (2005) and Wang &amp; Chevalier (2001), but does not claim a quantitative test of the planar constant-acceleration law.</li>''')
                notes.append("Module 8 source-note dependency")
    if module == 8:
        for caption in soup.find_all("figcaption"):
            if "isothermal law of Proposition 4" in caption.get_text(" ", strip=True):
                replace_tag(caption, r'''<figcaption>Left: the density ratio across a normal shock against upstream Mach number, for $\gamma=5/3$ and $\gamma=7/5$, with the isothermal law of Proposition 4 dashed for contrast at the <em>same speed</em>. On this axis it is $\rho_2/\rho_1=\mathcal{M}^2=\gamma M_1^2$. Both adiabatic curves approach finite ceilings, 4 and 6; the isothermal curve does not. Right: the entropy jump of Proposition 3 is zero at $M_1=1$, positive above it and negative below it, with the forbidden branch marked.</figcaption>''')
                notes.append("shock-figure TeX and prose")
                break
        for li in list(soup.find_all("li")):
            if "mixing law transferred from a plane interface" in li.get_text(" ", strip=True):
                replace_tag(li, r'''<li><b>The plane-interface mixing law.</b> Section 8 shows that the attempted instantaneous-acceleration substitution is invalid. No quantitative transfer test is established for an expanding supernova shell.</li>''')
                notes.append("Tycho limits dependency")
                break
    if module == 9:
        for p in soup.find_all("p"):
            if "largest ratio in the book so far" in p.get_text(" ", strip=True):
                replace_tag(p, r'''<p><b>The astrophysical application is Sagittarius A*</b>, <a class="secref" href="#sgra">§8</a>. The Bondi rate computed from the measured outer gas exceeds a conditional Faraday-rotation upper limit by a factor of about $40$, or about $4$ under a different field assumption. The published lower limits are satisfied by the Bondi estimate and therefore do not refute it. The X-ray luminosity is band-limited and arises far inside the radius at which the outer supply is estimated, so it cannot by itself be converted into a radiative efficiency for the Bondi rate.</p>''')
                notes.append("Sgr A* opening summary")
                break
        r(
            "Two further comparisons do not depend on the field at all, and the refutation rests on them.",
            "The lower limits and the X-ray luminosity provide different information, but neither is an independent field-free refutation of the Bondi supply estimate.",
            "Sgr A* transition",
        )
        p = soup.find("p")
        for candidate in soup.find_all("p"):
            if candidate.get_text(" ", strip=True).startswith("The lower limits."):
                replace_tag(candidate, r'''<p><b>The lower limits.</b> Marrone et al. require the accretion rate to exceed $1$–$2\times10^{-8}\,M_\odot\,\mathrm{yr^{-1}}$ or $2$–$4\times10^{-9}\,M_\odot\,\mathrm{yr^{-1}}$, depending on the assumed inner radius. The Bondi estimate is larger and therefore satisfies both lower-limit inequalities. These bounds exclude sufficiently small rates; they do not reject the larger Bondi value.</p>''')
                notes.append("lower-limit paragraph")
                break
        fig = soup.find("figure", id="fig-sgra")
        if fig and fig.figcaption:
            set_inner(fig.figcaption, r'''<p>The rates and limits in this section on one logarithmic axis. The upper limits depend on magnetic-field assumptions and can constrain the Bondi estimate only while those assumptions are retained. The lower limits point in the opposite logical direction: the Bondi estimate satisfies them. The plot therefore displays conditional constraints at different radii rather than a field-independent rejection.</p>''')
            notes.append("Sgr A* figure caption")
        for caption in soup.find_all("figcaption"):
            if "Bondi rate is computed from gas measured at" in caption.get_text(" ", strip=True):
                replace_tag(caption, r'''<figcaption>The comparisons refer to different radii. The Bondi rate is inferred from gas near $R_B$. Marrone et al.'s Faraday-rotation limits depend on whether the rotating medium extends inward to $30$–$100\,r_S$ or $3$–$10\,r_S$. The gas is expected to circularise near $100\,r_S$, roughly $2{,}000$ times inside the quoted Bondi radius. The steady spherical calculation does not model the intervening disc, outflow or radial change in mass flux.</figcaption>''')
                notes.append("Sgr A* radial-scale caption")
                break
        h = soup.find("h3", id="what-fails")
        if h:
            h.string = "8.3 Which Bondi assumptions require further physics"
        r(
            "What fails are the three physical premises of Proposition 5, each of which Sgr A* violates in a way that is separately documented:",
            "Three assumptions of the spherical model require additional physics before it can be applied across the full radial range of Sgr A*:",
            "Bondi premise introduction",
        )
        r(
            "(8.2) shows the flow radiates $2\\times10^{7}$ times less efficiently than a thin disc. That is the defining property of a radiatively inefficient accretion flow, and the literature Baganoff et al. review in their Sect. 11 exists because of it.",
            "The observed 2–10 keV luminosity is small relative to the rest-mass power associated with the outer Bondi supply. Interpreting that ratio requires a bolometric correction and an estimate of the mass flux reaching the emitting region.",
            "Bondi premise 3",
        )
        r(
            "Each premise, on its own, would reduce the rate. All three act in the same direction, and together they span the factor of 40 — or 4, or 401, depending on which leg is being used — without difficulty. The value of the calculation is not that it predicts the rate. It is that it predicts a rate which is definitely wrong, by a definite amount, in a definite direction, and the size of the discrepancy is the measure of how much physics the spherical picture omits.",
            "Angular momentum, outflows and thermodynamics can all alter the connection between the outer gas supply and the inner flow. The comparisons above show where the spherical model needs extension, but the present bounds and band-limited luminosity do not determine a unique reduction factor.",
            "Bondi conclusion",
        )
        r(
            "Sgr A* is faint mainly because the gas that does arrive radiates almost nothing, not because little gas arrives.",
            "The Eddington-scaled quantities show that Sgr A* is faint relative to the outer Bondi supply. They do not by themselves determine whether the difference is dominated by mass loss, inefficient radiation, or both.",
            "Sgr A* exercise conclusion",
        )
        for li in list(soup.find_all("li")):
            if "It circularises near" in li.get_text(" ", strip=True) and "five decades" in li.get_text(" ", strip=True):
                html = str(li).replace("five decades inside $R_B$", "roughly $2{,}000$ times inside $R_B$")
                replace_tag(li, html)
                notes.append("Bondi-to-circularisation scale")
                break
        for p in list(soup.find_all("p")):
            if "smallest ratio in it is" in p.get_text(" ", strip=True) and "largest" in p.get_text(" ", strip=True):
                replace_tag(p, r'''<p>One limitation belongs to the comparisons rather than to the equations. The Helios fits average a structured solar wind, and the Chandra measurement characterises gas near the Bondi radius while the inner flow may contain a disc and outflows. Section 7.1 states the self-similarity condition used for the first comparison. For Sagittarius A*, the available bounds are conditional and apply at different radii; they identify missing physics but do not determine one model-independent discrepancy factor.</p>''')
                notes.append("Sgr A* limitations summary")
                break
    if module == 10:
        for div in soup.find_all("div", class_="warn"):
            if "Which solar wind is this" in div.get_text(" ", strip=True):
                html = str(div).replace("Table 3 median fits", "Table 3 mean fits")
                replace_tag(div, html)
                notes.append("Venzmer fit-set dependency")
                break
        for caption in soup.find_all("figcaption"):
            if "why the most probable density" in caption.get_text(" ", strip=True):
                replace_tag(caption, r'''<figcaption><b>A width ratio of $1.36$ becomes a tail ratio of $6.1$.</b> The probability density of $s=\ln(\rho/\langle\rho\rangle)$ at $\mathcal{M}=10$, for solenoidal forcing ($b=1/3$, teal) and compressive forcing ($b=1$, orange). The Gaussian in $s$ is centred at the median density ratio $e^{s_0}<1$; the mode of the density PDF lies lower still, at $e^{s_0-\sigma_s^2}$. The upper panel shows the widths on a linear scale. The lower panel plots the same curves logarithmically so that the shaded region $\rho>100\langle\rho\rangle$ is visible.</figcaption>''')
                notes.append("log-density figure caption")
                break
    if module == 11:
        r(
            "There is therefore a radius at which the two balance and the infall stops:",
            "The radius of the circular orbit with this specific angular momentum is",
            "circularisation setup",
        )
        start = next((h for h in soup.find_all("h3") if "What this does to Module 9" in h.get_text(" ", strip=True)), None)
        stop = soup.find("h2", id="selfgravity")
        if start and stop:
            replace_contiguous(start, stop, r'''<h3>Why the Sagittarius A* comparison needs two additional quantities</h3>
<p>A Newtonian thin disc with an inner edge at $6R_g$ has efficiency $1/12$, while relativistic efficiencies depend on black-hole spin. Those efficiencies refer to bolometric luminosity divided by the mass flux through the radiating disc.</p>
<p><a href="module09.html">Module 9</a> instead quotes a 2–10 keV luminosity and an accretion rate inferred at the Bondi radius. Dividing those quantities produces a small number, but not a measured disc radiative efficiency: a bolometric correction and the fraction of the outer supply that reaches the emitting region are both required. The comparison motivates radiatively inefficient, mass-losing flow models without selecting between them.</p>''')
            notes.append("disc-efficiency subsection")
        for div in list(soup.find_all("div", class_="prob")):
            if div.get_text(" ", strip=True).startswith("K2.") and "Sagittarius A*" in div.get_text(" ", strip=True):
                replace_tag(div, r'''<div class="prob"><b>K2.</b> Using Module 9's outer Bondi supply and black-hole mass for Sagittarius A*, compute the bolometric luminosity a Newtonian thin disc would produce if the entire supply reached an inner edge at $6R_g$. Compare that illustrative luminosity with the quoted 2–10 keV luminosity, and explain why their ratio is not a measured radiative efficiency.<br/><br/><b>Solution.</b> With $\dot M c^2=4.543\times10^{41}\ \mathrm{erg\,s^{-1}}$, Proposition 10 gives $L=(1/12)\dot Mc^2=3.786\times10^{40}\ \mathrm{erg\,s^{-1}}$. This is about $1.9\times10^7$ times the quoted 2–10 keV luminosity. The arithmetic illustrates how faint the source is relative to that idealised thin-disc prediction. It does not measure the efficiency because the observed value is band-limited and the mass flux through the inner radiating flow need not equal the supply inferred near the Bondi radius.</div>''')
                notes.append("K2 interpretation")
                break
    if module == 12:
        fig = soup.find("figure", id="fig-transport")
        if fig:
            fig.replace_with(BeautifulSoup(
                r'''<div class="warn"><b>The transport comparison is one-sided.</b> The classical coefficients in the table are local components relative to a magnetic field. Zhuravleva et al. infer an effective cluster viscosity and, for the cases discussed, require it to be suppressed by at least a stated factor. Their result does not supply a lower bound that would exclude a still smaller perpendicular coefficient, and it cannot be compared directly without a model connecting the local tensor to the cluster-scale effective transport.</div>''',
                "html.parser",
            ))
            notes.append("removed misleading transport ladder")
        h = soup.find("h3", id="check4")
        if h:
            h.string = "8.2 Check 4 — strong magnetisation; effective transport unresolved"
        for candidate in soup.find_all(["p", "div"]):
            text = candidate.get_text(" ", strip=True)
            if text.startswith("The direction of the failure is the physical content"):
                replace_tag(candidate, r'''<p>The large value of $\omega_i\tau_i$ establishes strong particle magnetisation. It does not determine the effective transport of a tangled, weakly collisional cluster plasma. Field-line geometry, pressure-anisotropy instabilities and the relation between local and coarse-grained stresses must be modelled before the classical tensor coefficients can be compared with the observed fluctuation spectrum.</p>''')
                notes.append("transport interpretation")
                break
        for candidate in list(soup.find_all("p")):
            text = candidate.get_text(" ", strip=True)
            if text.startswith("That answer must be checked before it is quoted"):
                replace_tag(candidate, r'''<p>The classical perpendicular conductivity is extremely small relative to the parallel value. This calculation establishes anisotropy of the classical transport tensor; it does not predict the effective cross-field transport of a tangled cluster field.</p>''')
                notes.append("D3 conductivity solution")
            elif text.startswith("And the comparison must be made on the right quantity"):
                replace_tag(candidate, r'''<p>Zhuravleva et al. constrain an effective viscosity rather than thermal conductivity. Even for viscosity, their one-sided result does not exclude a smaller local perpendicular coefficient. A quantitative comparison requires a model relating Braginskii's anisotropic tensor to the effective viscosity inferred from cluster-scale fluctuations.</p>''')
                notes.append("D3 viscosity solution")
            elif "a proton turns $10^{12.71}$ gyro-orbits" in text:
                replace_text_once(
                    candidate,
                    "a proton turns $10^{12.71}$ gyro-orbits between collisions.",
                    r"the corresponding gyro-phase is $10^{12.71}$ radians, or about $8.2\times10^{11}$ complete turns.",
                )
                notes.append("K3 complete-turn count")
        r(
            "the number of gyro-orbits a proton completes between collisions",
            "the gyro-phase in radians accumulated between collisions; divide by $2\\pi$ for complete turns",
            "transport table orbit count",
        )
        for div in list(soup.find_all("div", class_="keyresult")):
            if "intracluster proton completes" in div.get_text(" ", strip=True):
                replace_tag(div, r'''<div class="keyresult"><b>The module's $\omega_{\rm c}\tau$ uses Braginskii's collision time because his transport coefficients are defined with that convention.</b> The alternative ratio $\lambda/r_g=5.1767\times10^{12}$ is a gyro-phase in radians when compatible speed conventions are used. It corresponds to about $8.24\times10^{11}$ complete turns after division by $2\pi$. Either convention establishes very strong particle magnetisation.</div>''')
                notes.append("gyro-phase result box")
                break
    return notes


def build(module: int) -> dict:
    if not 1 <= module <= 12:
        raise SystemExit("module must be between 1 and 12")
    source = ROOT / "afd" / f"module{module:02}.html"
    source_hash = sha(source)
    soup = BeautifulSoup(source.read_text(encoding="utf-8"), "html.parser")
    content_applied = apply_content_edits(soup, module)
    # Content replacements run first because several prose examples quote the
    # same defective paragraph. In those cases the stronger scientific rewrite
    # deliberately supersedes the narrower line edit.
    prose_applied, prose_missing = apply_style_edits(soup, module)
    dependencies = repair_dependencies(soup, module)
    repair_navigation(soup)
    add_revision_notice(soup, module, source_hash)
    DEST.mkdir(parents=True, exist_ok=True)
    target = DEST / source.name
    target.write_text("<!DOCTYPE html>\n" + str(soup).replace("<!DOCTYPE html>\n", "", 1), encoding="utf-8")
    return {
        "module": module,
        "source": str(source.relative_to(ROOT)).replace("\\", "/"),
        "destination": str(target.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": source_hash,
        "revised_sha256": sha(target),
        "content_findings_applied": content_applied,
        "prose_edits_applied_before_content_replacements": prose_applied,
        "prose_edits_not_found_or_superseded": prose_missing,
        "dependent_repairs": dependencies,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python build_revised_modules.py MODULE_NUMBER")
    result = build(int(sys.argv[1]))
    manifest_path = DEST / "build-manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {"edition": "Codex revised copies", "modules": []}
    manifest["modules"] = [x for x in manifest["modules"] if x["module"] != result["module"]]
    manifest["modules"].append(result)
    manifest["modules"].sort(key=lambda x: x["module"])
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
