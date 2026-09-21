from pathlib import Path
from bs4 import BeautifulSoup


PATH = Path(__file__).parent / "textbook-edition-20-rule" / "module12.html"


def set_html(tag, html):
    fragment = BeautifulSoup(html, "html.parser")
    tag.clear()
    for child in list(fragment.contents):
        tag.append(child)


soup = BeautifulSoup(PATH.read_text(encoding="utf-8"), "html.parser")
heading = soup.find(id="sources")
intro = heading.find_next("p")
set_html(intro, "These notes identify the origin of numerical values and delimit how each source is used. A verified equation, table, or passage was checked in the cited source. Historical citations provide attribution but do not supply numerical evidence unless stated explicitly.")

entries = [
    r'''Venzmer, M. S. &amp; Bothmer, V. (2018), “Solar-wind predictions for the Parker Solar Probe orbit”, <i>A&amp;A</i> <b>611</b>, A36, arXiv:1711.07534. Equation (10) and Table 3 provide the power-law fits used in §5. Figure 9 provides the year-to-year scatter of the exponents. The mean and median rows are kept separate throughout the comparison.''',
    r'''Verscharen, D., Bale, S. D. &amp; Velli, M. (2021), “Flow deflections and Alfvén radii in the solar wind”, <i>MNRAS</i> <b>506</b>, 4993–5004. Table 3 gives $r_{\rm A}=12.080\pm0.236\,R_\odot$ for the first fast-latitude scan and $9.504\pm0.221\,R_\odot$ for the third. Their sonic radius refers to a different surface and is not used as an Alfvén-radius estimate.''',
    r'''Kasper, J. C. et al. (2021), “Parker Solar Probe enters the magnetically dominated solar corona”, <i>Phys. Rev. Lett.</i> <b>127</b>, 255101. Table I lists three sub-Alfvénic intervals during encounter 8, with median Alfvén Mach numbers $0.79$, $0.49$, and $0.88$. The paper places these intervals between $16$ and $20\,R_\odot$. Its event-specific PFSS model adopts a source surface at $2.0\,R_\odot$.''',
    r'''Braginskii, S. I. (1965), “Transport processes in a plasma”, <i>Reviews of Plasma Physics</i> <b>1</b>, 205–311. Equations (2.5e) and (2.5i) define the electron and ion collision times. Equations (2.7), (2.8), (2.12), (2.13), (2.15), and (2.16) provide the conductivity and thermal-transport coefficients used here. The quoted coefficients apply to $Z=1$; Table 1 gives their charge dependence.''',
    r'''Zhuravleva, I. et al. (2019), “Suppressed effective viscosity in the bulk intergalactic plasma”, <i>Nature Astronomy</i> <b>3</b>, 832–837, arXiv:1906.06346. The paper constrains the effective viscosity of the Coma intracluster medium. Its result is a one-sided bound rather than a measurement of local perpendicular transport. Section 8.2 retains that distinction.''',
    r'''Mouschovias, T. Ch. &amp; Spitzer, L. (1976), “Note on the collapse of magnetic interstellar clouds”, <i>ApJ</i> <b>210</b>, 326–327. Equations (2) and (4) give the coefficient used for the spherical-cloud threshold. The paper prints $c_1=0.53$. Its coefficient $c_2=0.60$ concerns maximum external pressure and should not be substituted for the critical mass at fixed flux.''',
    r'''Nakano, T. &amp; Nakamura, T. (1978), “Gravitational instability of magnetized gaseous disks”, <i>PASJ</i> <b>30</b>, 671–679. The abstract gives the stability condition $\sigma_0/B_0\lt(4\pi^2G)^{-1/2}=1/(2\pi\sqrt G)$. This surface-density-to-field ratio supplies the flattened-cloud coefficient in equation (7.2).''',
    r'''Troland, T. H. &amp; Crutcher, R. M. (2008), “Magnetic fields in dark cloud cores: Arecibo OH Zeeman observations”, <i>ApJ</i> <b>680</b>, 457–465, arXiv:0802.2253. The survey covers 34 cores observed for about 500 hours. Section 3.2 and equation (2) define $\lambda$ relative to the Nakano–Nakamura critical value. The geometry-corrected ranges are $\lambda_c=1.4$–$2.1$ and $\lambda_{1/2,c}=1.7$–$2.6$.''',
    r'''Goldreich, P. &amp; Sridhar, S. (1995), “Toward a theory of interstellar turbulence. II. Strong Alfvénic turbulence”, <i>ApJ</i> <b>438</b>, 763–775. The abstract states $k_z\approx k_\perp^{2/3}L^{-1/3}$ and a one-dimensional perpendicular spectrum proportional to $k_\perp^{-5/3}$. Their symmetric model excludes direct application to the imbalanced solar wind, so §10 uses it as a theoretical scaling rather than a fitted solar-wind prediction.''',
    r'''Parker, E. N. (1958), “Dynamics of the interplanetary gas and magnetic fields”, <i>ApJ</i> <b>128</b>, 664–676. Equations (24), (26), and (27) in Section II give the spiral geometry. Equation (26) contains $(r-b)$; §5 retains the corresponding finite source radius as $(r-r_0)$.''',
    r'''Snodgrass, H. B. &amp; Ulrich, R. K. (1990), “Rotation of Doppler features in the solar photosphere”, <i>ApJ</i> <b>351</b>, 309–316. Their sidereal law is $\omega(\theta)=14.71-2.39\sin^2\theta-1.78\sin^4\theta$ degrees per day. It gives a $24.47$ d period for the tracer used in §5.2. The authors note that this rate is about 2 per cent faster than the magnetic-feature rate.''',
    r'''NASA NSSDC Sun Fact Sheet. The adopted sidereal rotation period is $609.12$ hours, or $25.380$ d. The latitude-dependent law $14.37-2.33\sin^2L-1.56\sin^4L$ degrees per day reproduces this value at $L=16^\circ$. The fact sheet also provides the photospheric field ranges quoted in §1.''',
    r'''Alfvén, H. (1942), “Existence of electromagnetic–hydrodynamic waves”, <i>Nature</i> <b>150</b>, 405–406. This paper supplies historical attribution for flux freezing and Alfvénic dynamics. Proposition 4 is derived independently in the present module, so no numerical or logical step depends on the historical citation.''',
    r'''Balbus, S. A. &amp; Hawley, J. F. (1991), “A powerful local shear instability in weakly magnetized disks. I”, <i>ApJ</i> <b>376</b>, 214–222. The paper supplies historical attribution for the local MRI result. Proposition 11 and the numerical examples are derived within this module.''',
    r'''Crutcher, R. M. (2012), “Magnetic fields in molecular clouds”, <i>ARA&amp;A</i> <b>50</b>, 29–63. This review is listed as a guide to the broader Zeeman literature. The numerical argument in §7 relies instead on the accessible primary survey of Troland and Crutcher (2008).''',
    r'''Podesta, J. J., Roberts, D. A. &amp; Goldstein, M. L. (2007), <i>ApJ</i> <b>664</b>, 543–548. Table 2 provides the solar-wind spectral indices introduced in Module 10 and restated in §10. The present module does not use those measurements as an independent test of critical-balance theory.''',
]

source_items = []
for node in heading.find_all_next("li"):
    source_items.append(node)
if len(source_items) != len(entries):
    raise RuntimeError(f"expected {len(entries)} source entries, found {len(source_items)}")
for item, html in zip(source_items, entries):
    set_html(item, html)

PATH.write_text(str(soup), encoding="utf-8")
print(f"rewrote {len(entries)} source notes")
