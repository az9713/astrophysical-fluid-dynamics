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
        matches = [str(t) for t in soup.find_all(["p", "li", "div", "span", "td", "h2", "h3"])
                   if norm(t.get_text(" ", strip=True)).startswith(prefix)]
        if len(matches) != 1 or matches[0] not in html:
            raise RuntimeError((number, prefix, len(matches)))
        html = html.replace(matches[0], replacement, 1)
    path.write_text(html, encoding="utf-8")
    print(f"module {number:02d}: rewrote {len(replacements)} blocks")


apply(8, [
    (
        "The three fluxes are stated here",
        '<span class="prov"><b>Domain of the jump conditions.</b> Proposition 1 applies to a non-magnetic gas. A magnetised shock requires additional jump conditions for the normal and tangential magnetic-field components, and magnetic terms enter the momentum flux. Section 6 compares only quantities that remain meaningful under the gas-dynamic approximation and identifies where an oblique-MHD treatment is required.</span>',
    ),
    (
        "Proposition 1 is three equations",
        '<p>Proposition 1 supplies three equations for the downstream density, velocity, and pressure. Solving this system gives the compression, temperature, and entropy changes in terms of the upstream Mach number.</p>',
    ),
    (
        "The two behaviours in Proposition 2",
        '<p>Compression and heating behave differently at large Mach number. Pressure behind the front limits the density jump to $(\\gamma+1)/(\\gamma-1)$, so compression remains finite. The temperature has no corresponding ceiling because additional kinetic energy becomes internal energy. Strong shocks therefore produce extremely hot gas without requiring an equally large density increase, as observed in X-ray-emitting supernova remnants.</p>',
    ),
    (
        "5.1 Check 1:",
        '<h3 id="confirm">5.1 Check 1: the blast-wave exponent</h3>',
    ),
    (
        "The data file is checked",
        '<p><b>Transcription check.</b> Taylor prints $\\log_{10}t$, $\\log_{10}R$, and $\\tfrac52\\log_{10}R$ beside the dimensional columns. All twenty-five transcribed radii reproduce his logarithms to the printed precision. Two ambiguous times were recovered from the corresponding logarithms and the monotonic sequence. The mean intercept is $11.9159$, compared with Taylor\'s $11.915$. These checks establish the data transcription; they do not test the blast-wave model.</p>',
    ),
    (
        "5.2 Check 2:",
        '<h3 id="refute">5.2 Check 2: residual structure in the similarity fit</h3>',
    ),
    (
        "Check 2, Disagreement with the prediction.",
        '<div class="keyresult"><b>The fitted exponent does not remove systematic residuals.</b> The point-explosion model predicts the correct approximate $2/5$ scaling, but the residuals drift from $+0.0150$ through $-0.0043$ to $-0.0339$. The first row is also $0.32$ below the mean of rows 2–14, sixteen times that block\'s internal scatter. An instrument change could contribute to the $7.3\\sigma$ step between outer blocks, but the broader monotonic pattern remains inconsistent with a single exact similarity solution.</div>',
    ),
    (
        "Check 3, Disagreement with the prediction.",
        '<div class="keyresult"><b>The blast-wave energy is smaller than the device yield.</b> The inferred energy is $0.822$ of the DOE value and $0.696$ of Selby\'s estimate, a $3.8\\sigma$ difference using Selby\'s quoted uncertainty alone. The similarity solution measures energy coupled to the expanding gas after the early radiative and ionisation losses. Pairwise fits span $14.33$–$19.50$ kt, revealing a 36 per cent systematic spread that the quoted $3.8\\sigma$ does not include.</div>',
    ),
    (
        "An inconsistency inside the source",
        '<span class="prov"><b>Internal numerical inconsistency in Taylor (1950).</b> His fitted intercept $11.915$ implies $R^5t^{-2}=6.7608\\times10^{23}$, whereas equation (3) prints $6.67\\times10^{23}$. The two values differ by $1.36$ per cent. The energy calculation follows the printed equation (3), so this discrepancy propagates into the quoted yield.</span>',
    ),
    (
        "6.1 CONFIRMED:",
        '<h3 id="neptune">6.1 The strong-shock compression ceiling at Neptune</h3>',
    ),
    (
        "Fig. 4 draws all five comparisons",
        '<p>Figure 4 places all five comparisons on a common logarithmic axis as measured divided by predicted. Ratios near unity indicate agreement, while their distance from unity displays the magnitude and direction of each discrepancy.</p>',
    ),
    (
        "6.2 REFUTED:",
        '<h3 id="tsclosure">6.2 Failure of the one-temperature closure</h3>',
    ),
    (
        "One frame caveat",
        '<span class="prov"><b>Reference-frame dependence.</b> The quoted $300\\ \\mathrm{km\\,s^{-1}}$ speed is measured in the spacecraft frame, while equation (7.1) requires the upstream speed in the shock frame. Subtracting the measured $94.0\\pm3.4\\ \\mathrm{km\\,s^{-1}}$ shock speed gives $206\\ \\mathrm{km\\,s^{-1}}$ and $T_2=4.8\\times10^5$ K. The observed $10^5$ K remains lower by a factor of $4.8$, compared with a factor of ten in the spacecraft-frame calculation.</span>',
    ),
    (
        "Second, it is the wrong formula.",
        '<p>The shock is also quasi-perpendicular: the measured angle between its normal and the magnetic field is $82.8^\\circ\\pm3.9^\\circ$. Equation (3.1) is gas-dynamic and omits magnetic pressure and tension. A quantitative Voyager comparison therefore requires the oblique-MHD jump conditions, which lie beyond the theory developed here.</p>',
    ),
    (
        "The second branch of (7.2)",
        '<div class="warn"><b>Bremsstrahlung alone is not an adequate cooling law.</b> Omitting line cooling delays the transition to $3.32\\times10^5$ yr, a factor of eight. Line emission dominates below $10^7$ K, where the remnant spends most of its evolution. The simplified cooling law therefore changes the phase structure, not merely a small numerical correction.</div>',
    ),
    (
        "A one-line criterion is not a simulation",
        '<p>The transition criterion is an order-of-magnitude estimate rather than a hydrodynamic model. Cioffi, McKee, and Bertschinger (1988) calculated the radiative transition numerically. For solar abundance and $E_{51}=n_0=1$, their equations (3.33a) and (3.33b) give</p>',
    ),
    (
        "Check 6, a calibration",
        '<div class="keyresult"><b>Calibration against a radiative-hydrodynamic model.</b> The simple criterion gives $R_{\\rm rad}/R_{\\rm PDS}=1.573$ and $t_{\\rm rad}/t_{\\rm PDS}=3.081$. The radius is more accurate because $R\\propto t^{2/5}$ compresses a factor of $3.08$ in time to a factor of $1.57$ in radius. These ratios quantify the accuracy that should be assigned to the one-line estimate.</div>',
    ),
    (
        "Module 7 closed by recording",
        '<p>Module 7 derived the history-dependent Rayleigh–Taylor width but lacked an astronomical comparison. Tycho\'s supernova remnant supplies one because its forward and reverse shock radii constrain the deceleration history. The comparison tests the shell model rather than the laboratory coefficient alone.</p>',
    ),
    (
        "One fluid, one temperature.",
        '<li><b>One fluid and one temperature.</b> The termination-shock measurement is inconsistent with this closure. Electrons, thermal ions, and pickup ions need not equilibrate, and pickup ions carry about 80 per cent of the measured energy. A multi-population shock model is required.</li>',
    ),
    (
        "One thing this module does not miss",
        '<p>The Trinity comparison uses a directly recorded radius-time table, and the Voyager comparison uses in-situ measurements. Neither test is circular in the sense discussed in Module 3. Their principal limitation is the sparse uncertainty information, especially for the Trinity images. Selby\'s quoted standard deviation is therefore only one component of the yield uncertainty.</p>',
    ),
    (
        "That spread is the refutation",
        '<p>The pairwise energy spread provides another view of the systematic residuals in Section 5.2. An exact similarity solution would return the same energy from every row. A single-point estimate hides this structure, whereas the residual plot exposes the $7.3\\sigma$ change between data blocks.</p>',
    ),
])

apply(9, [
    (
        "The astrophysical application is Sagittarius A*",
        '<p>The accretion example is Sagittarius A* in <a class="secref" href="#sgr">§8</a>. The Bondi rate inferred from the outer gas exceeds a conditional Faraday-rotation upper bound by about $40$, or by about $4$ under a different magnetic-field assumption. Published lower bounds remain compatible with the Bondi estimate. Because the X-ray luminosity is band-limited and produced far inside the Bondi radius, it cannot alone determine the radiative efficiency of the outer supply.</p>',
    ),
    (
        "Check 1 — a consistency check",
        '<div class="keyresult"><b>Reproduction of Parker\'s static-corona argument.</b> The present pressure ratio is $2.358\\times10^8$, compared with Parker\'s $4.3\\times10^7$. Parker includes outward conduction and cooling and adopts an interstellar pressure ten times smaller, accounting for the factor $5.5$ difference. Both calculations reach the same physical conclusion: a static million-degree corona cannot match the external pressure. This is a consistency check of the argument, not an independent solar measurement.</div>',
    ),
    (
        "A note on the names.",
        '<p class="small"><b>Terminology.</b> Later textbooks often number the six Parker solution families I–VI, but Parker (1958) does not use that enumeration. This module therefore names the branches by their physical behaviour rather than assigning historical numbers.</p>',
    ),
    (
        "Check 2 — against the primary source.",
        '<div class="keyresult"><b>Bondi coefficient check.</b> The legible entries in Bondi\'s Table I give $\\lambda_c=1.12$ at $\\gamma=1$, $0.625$ at $1.4$, $0.500$ at $1.5$, and $0.250$ at $5/3$. All match the values derived above to the printed precision. The $\\gamma=1.2$ entry is illegible in the available scan, so the tabulated value $0.871158$ is derived here without an independent transcription check.</div>',
    ),
    (
        "Module 2 used the density",
        '<p>Module 2 tested steady continuity using the independently fitted density and velocity exponents. Their differences, $1.961$ and $2.035$, bracket the required value 2. The same data exclude the adiabatic temperature law: the predicted exponent is $-1.340$, compared with $-0.792\\pm0.028$, a $19.6\\sigma$ discrepancy.</p>',
    ),
    (
        "7.4 Check 5",
        '<h3 id="floor">7.4 Check 5: limits of the isothermal wind</h3>',
    ),
    (
        "Check 5(ii) — REFUTED",
        '<div class="keyresult"><b>No admissible isothermal temperature matches the measured density exponent.</b> Requiring the corona to remain subsonic at its base yields a minimum predicted exponent of $0.1119$. The measured value is $0.049\\pm0.010$, a difference of $6.3\\sigma$ using the formal error and $5.2\\sigma$ using year-to-year scatter. Proposition 8 establishes the bound over the entire allowed temperature range.</div>',
    ),
    (
        "The 2–3 MK coronal temperature",
        '<span class="prov"><b>Source note.</b> Venzmer and Bothmer quote a coronal temperature of 2–3 MK from earlier measurements that were not available for direct inspection. The following discrepancy would remain even if that range shifted by a factor of $1.5$, so the conclusion does not depend sensitively on this secondary citation.</span>',
    ),
    (
        "Check 6 — REFUTED",
        '<div class="keyresult"><b>A single polytropic index cannot describe the whole wind.</b> The corona is nearly isothermal where heat is deposited, while the Helios data beyond $0.3$ au give an effective index near $1.4$. The fitted $\\gamma_{\\rm eff}$ averages across a region in which the thermodynamic response changes. The failure therefore concerns the assumption of one constant index, not the usefulness of local polytropic descriptions.</div>',
    ),
    (
        "Check 8 — a weak test",
        '<div class="keyresult"><b>The mass flux weakly constrains the fitted temperature.</b> Equation (6.1) gives $d\\ln\\dot M/d\\ln T_0\\approx13.2$ at $0.947$ MK. A factor-of-three uncertainty in $\\dot M$ corresponds to only an $8.7$ per cent range in $T_0$. Agreement within a factor of a few therefore shows that the exponential was evaluated near the appropriate temperature; it does not validate the full wind model.</div>',
    ),
    (
        "Check 9 — a numerical procedure",
        '<div class="keyresult"><b>Reproduction of the published Bondi-rate calculation.</b> The present value $8.15$ agrees with Baganoff et al.\'s $8.02$ in the same units, a ratio of $1.016$. Because both use the same formula and input profiles, this verifies the arithmetic and conventions. The physical comparison begins in the next subsection.</div>',
    ),
    (
        "Their local plasma estimate",
        '<p>Baganoff et al. use $kT\\approx1.3$ keV and $n_e\\approx26\\ \\mathrm{cm^{-3}}$ to obtain a rate near $10^{-6}M_\\odot\\,\\mathrm{yr^{-1}}$. Equation (6.1), evaluated at their adopted black-hole mass, gives $1.13\\times10^{-6}M_\\odot\\,\\mathrm{yr^{-1}}$. The 13 per cent difference is consistent with rounding and input conventions.</p>',
    ),
    (
        "The lower limits and the X-ray luminosity",
        '<p>The Faraday lower limits and the X-ray luminosity constrain different aspects of the flow. Neither independently excludes the field-free Bondi supply estimate.</p>',
    ),
    (
        "Check 11 — a low X-ray luminosity",
        '<div class="keyresult"><b>The X-ray luminosity is extremely small relative to the outer supply power.</b> The ratio $L_{2-10\\,{\\rm keV}}/(\\dot M_{\\rm B}c^2)$ is approximately $4\\times10^{-9}$. This is a band-limited luminosity divided by the rest-mass power associated with the Bondi estimate, not a bolometric efficiency. Interpreting it requires both a bolometric correction and an estimate of how much supplied mass reaches the emitting region.</div>',
    ),
    (
        "Not the algebra.",
        '<p>The discrepancy does not arise from equation (5.3). Section 5.1 reproduces the critical-point construction and every legible entry in Bondi\'s table. Bondi proves only $\\lambda\\le\\lambda_c$, so even exact algebra does not determine the accretion coefficient without additional boundary conditions and dynamics.</p>',
    ),
    (
        "§7.4 refutes the isothermal wind",
        'Section 7.4 excludes the isothermal wind but does not identify the coronal heating mechanism. Section 7.6 measures the remaining force or energy shortfall without specifying its source.',
    ),
    (
        "A mixture that must be declared.",
        '<p>The energy estimate combines the polar mass flux of Verscharen et al. with the ecliptic speed fit of Venzmer and Bothmer. These measurements sample different wind streams and latitudes. They differ by less than a factor of two in the relevant quantities, so the combination supports an order-of-magnitude budget but not a three-digit measurement.</p>',
    ),
    (
        "And the accretion does not happen",
        '<p>A second argument prevents solar Bondi accretion. The Bondi radius, $2.3$ au, lies far inside the heliopause near $120$ au, so the solar wind deflects interstellar gas before it reaches the capture region. The pressure argument and the heliospheric barrier independently lead to the same conclusion.</p>',
    ),
])
