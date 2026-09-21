from pathlib import Path
from bs4 import BeautifulSoup


PATH = Path(__file__).resolve().parent / "textbook-edition-20-rule" / "module12.html"


def norm(text: str) -> str:
    return " ".join(text.split())


def replace_blocks(html: str, replacements: list[tuple[str, str]]) -> str:
    for prefix, replacement in replacements:
        soup = BeautifulSoup(html, "html.parser")
        matches = []
        for tag in soup.find_all(["p", "li", "div", "span", "td", "h2", "h3"]):
            if norm(tag.get_text(" ", strip=True)).startswith(prefix):
                matches.append(str(tag))
        if len(matches) != 1:
            raise RuntimeError((prefix, len(matches)))
        html = html.replace(matches[0], replacement, 1)
    return html


html = PATH.read_text(encoding="utf-8")
replacements = [
    (
        "8. Transport across a field",
        '<li><b>8.</b> <a href="#transport">Transport across a magnetic field</a></li>',
    ),
    (
        "10. Anisotropy, critical balance",
        '<li><b>10.</b> <a href="#balance">Anisotropy and critical balance</a></li>',
    ),
    (
        "This module has no terrestrial measurement",
        '<div class="warn"><b>Scope of the empirical comparisons.</b> The four tests in this module use astronomical data. Section 4 instead reproduces a calculation from Module 7 to verify cross-module consistency. That reproduction checks the algebra and conventions; it is not an independent measurement.</div>',
    ),
    (
        "Definition 2 (the magnetisation).",
        '<div class="def"><b>Definition 2 (magnetisation).</b> The dimensionless product $\\omega_{\\rm c}\\tau$ measures the gyro-phase accumulated between collisions. Here $\\omega_{\\rm c}=ZeB/mc$, and $\\tau$ is Braginskii\'s collision time for electrons or ions. For the intracluster medium in <a class="secref" href="#transport">§8</a>, $\\omega_i\\tau_i=4.3\\times10^{12}$. This large value leads to the strong suppression of perpendicular classical transport. Section 8.1 compares Braginskii\'s convention with the alternative mean-free-path convention used elsewhere in the book.</div>',
    ),
    (
        "Dropping the displacement current",
        '<div class="warn"><b>Non-relativistic ordering.</b> With $E\\sim UB/c$, the displacement current is smaller than $\\nabla\\times\\mathbf B$ by a factor of order $(U/c)^2$. The fastest flow considered here is the solar wind at $435.6\\ \\mathrm{km\\,s^{-1}}$, for which this factor is $2.1\\times10^{-6}$. The approximation therefore applies to the present examples. It fails for relativistic jets and pulsar magnetospheres.</div>',
    ),
    (
        "The molecular cloud row is wrong",
        '<div class="warn"><b>Limit of the Spitzer-resistivity estimate.</b> A $10$ K molecular cloud is only weakly ionised, so electron–ion collisions do not determine its resistivity. Ion–neutral drift and ambipolar diffusion control the magnetic-flux evolution instead. The Spitzer value $\\mathrm{R_m}=4.653\\times10^{13}$ is therefore shown only to demonstrate the failure of that approximation; it is not used in an empirical comparison. The same limitation applies to the protoplanetary-disc example in <a class="secref" href="#mri">§9</a>. Ambipolar diffusion also provides a mechanism by which a magnetically subcritical cloud can lose flux and become supercritical.</div>',
    ),
    (
        "Flux freezing is a measurement",
        '<div class="keyresult"><b>Ohmic diffusion is extremely slow in the fully ionised examples.</b> The smallest valid magnetic Reynolds number in the table is $1.024\\times10^{12}$ for the solar corona. Equation (2.4) then gives an ohmic-decay time of approximately $10^{12}$ dynamical times. Flux freezing is therefore an excellent approximation on the dynamical scales considered here, although it does not preclude reconnection in thin current sheets.</div>',
    ),
    (
        "A validation of the machinery",
        '<div class="keyresult"><b>Cross-module consistency check.</b> Using $\\rho_h=5.8607\\times10^{-16}$, $\\rho_l=2.6210\\times10^{-16}\\ \\mathrm{g\\,cm^{-3}}$, and $\\Delta U=20\\ \\mathrm{km\\,s^{-1}}$, equation (4.2) gives $0.06747$ G. Module 7 reports $0.0675$ G for the same inputs, a ratio of $0.9995$. The one-sided case similarly gives $0.09541$ G against $0.0954$ G. The complete angle table also agrees, showing that the two modules use the same geometry and numerical conventions.</div>',
    ),
    (
        "The angle is measured from perpendicular",
        '<div class="warn"><b>Angle convention.</b> Equation (4.2) constrains $B\\cos\\theta$, where $\\theta$ is measured from the magnetic field. At fixed $B$, the permitted departure from a perpendicular field is therefore $\\arcsin(\\cos\\theta)$. This convention gives $3.87^\\circ$ for the first row of the table; using $\\arccos$ would instead report the complementary angle.</div>',
    ),
    (
        "Parker's $(r-r_0)$ is carried",
        '<div class="warn"><b>Finite source-surface radius.</b> Parker\'s equation (26) contains $(r-r_0)$, whereas the familiar $\\Omega r\\sin\\theta/v$ form assumes $r\\gg r_0$. At 1 au with $r_0=2.5\\,R_\\odot$, retaining $r_0$ lowers $-B_\\phi/B_r$ from $0.9840$ to $0.9726$, or by $1.16$ per cent. The symbol $r_0$ denotes the source-surface radius throughout this module.</div>',
    ),
    (
        "The rotation rate is two choices",
        '<div class="warn"><b>Solar rotation rate.</b> The NASA NSSDC sidereal period is $25.38$ d at $16^\\circ$ latitude. Snodgrass and Ulrich (1990) obtain $24.47$ d from Doppler tracking of the supergranulation network. The $3.71$ per cent difference combines a tracer dependence of $2.36$ per cent with a latitude dependence of $1.32$ per cent. Both choices are retained below to show their effect on the inferred Alfvén radius.</div>',
    ),
    (
        "The Alfvén speed in (6.1)",
        '<div class="warn"><b>Radial field in the Alfvén-radius estimate.</b> Equation (6.1) uses $B_r$, because the Weber–Davis Alfvén radius is defined from the radial flow and radial field. The extrapolation also requires $B_r\\propto r^{-2}$, which follows from $\\nabla\\!\\cdot\\mathbf B=0$. The total field $|\\mathbf B|$ does not obey this scaling once the Parker spiral develops. Substituting $|\\mathbf B|$ would increase the inferred radii by a factor near $1.40$.</div>',
    ),
    (
        "Check 1 — CONFIRMED",
        '<div class="keyresult"><b>Comparison with the measured radial-field index.</b> For both fit sets, the Parker-spiral prediction lies closer to the measured index than the $r^{-2}$ radial-field prediction. The improvement factor is $3.43$ for the median fits and $1.98$ for the mean fits. Neither prediction lies within the formal fit error, so the data support field winding without determining its strength precisely.</div>',
    ),
    (
        "The PSP number is a bound",
        '<div class="warn"><b>Parker Solar Probe gives a lower bound.</b> Kasper et al. report three sub-Alfvénic intervals between $16.0$ and $19.8\\,R_\\odot$, all with Alfvén Mach number below unity. The spacecraft was already inside the Alfvén surface during each interval. The outermost point, $19.8\\,R_\\odot$, is therefore a lower bound on the local surface radius along that trajectory. The quoted range combines different longitudes and days and should not be interpreted as a single spherical surface.</div>',
    ),
    (
        "A cross-module number, settled here.",
        '<span class="prov"><b>Comparison of two Alfvén-surface estimates.</b> Module 9 quotes a Weber–Davis estimate near $12\\,R_\\odot$ from Ulysses fast-wind data. Parker Solar Probe instead observed local sub-Alfvénic intervals near $16$–$20\\,R_\\odot$. These values use different methods and describe different aspects of a non-spherical, time-dependent surface; they are not duplicate estimates of one radius.</span>',
    ),
    (
        "Check 2 — BRACKETED",
        '<div class="keyresult"><b>Comparison of the Alfvén-radius estimates.</b> All eight spherical extrapolations lie above the Ulysses Weber–Davis estimate and below the Parker Solar Probe lower bound. The two observations differ by a factor of $1.639$ and do not measure the same quantity. Their disagreement shows that a single spherical radius cannot represent the structured, time-dependent Alfvén surface.</div>',
    ),
    (
        "This module never prints $0.13$.",
        '<div class="warn"><b>Critical mass-to-flux coefficient.</b> Mouschovias and Spitzer report $c_1=0.53$, which gives $0.125745/\\sqrt G$ in equation (7.2). The frequently quoted rounded value $0.13/\\sqrt G$ is $3.38$ per cent larger. Their coefficient $c_2=0.60$ applies to the maximum external pressure, not to the critical mass. Their notation also distinguishes the critical mass at fixed flux from that at fixed initial density; interchanging these quantities introduces a cubic error.</div>',
    ),
    (
        "Check 3 — CONFIRMED",
        '<div class="keyresult"><b>Mass-to-flux coefficient and geometry.</b> Equation (7.3), evaluated with $c_\\Phi=1/(2\\pi)$ and $\\mu=2.8$ per $\\mathrm{H_2}$ molecule, gives $7.6022\\times10^{-21}$ and rounds to the published $7.6\\times10^{-21}$. The geometry-corrected observations give $\\lambda_c=1.4$–$2.1$ and $\\lambda_{1/2,c}=1.7$–$2.6$, indicating mildly supercritical cores. Geometry remains quantitatively important: the spherical and sheet coefficients differ by a factor of $1.2657$. A reported $\\lambda_\\Phi$ is therefore incomplete unless it specifies the assumed geometry.</div>',
    ),
    (
        "This is not a check on this module's cloud",
        '<div class="warn"><b>Density range of the comparison.</b> Troland and Crutcher study cores with densities of a few $10^3\\ \\mathrm{cm^{-3}}$. The illustrative cloud used here has $n_{\\rm tot}=100\\ \\mathrm{cm^{-3}}$, about thirty times smaller. Their observations test the critical coefficient and the sign of the mass-to-flux conclusion, but not the numerical value for this illustrative cloud.</div>',
    ),
    (
        "Two mass conventions",
        '<div class="warn"><b>Mass conventions.</b> Troland and Crutcher use $\\mu=2.8$ per $\\mathrm{H_2}$ molecule, whereas this module uses $\\mu=2.33$ per particle. Both describe the same helium-corrected mass density. For He/H $=0.1$ by number, $\\rho/(n_{\\rm H_2}m_{\\rm H})=2.8$ and $\\rho/(n_{\\rm tot}m_{\\rm H})=2.333$. Thus $n_{\\rm tot}=100\\ \\mathrm{cm^{-3}}$ corresponds to $n(\\mathrm{H_2})=83.3\\ \\mathrm{cm^{-3}}$.</div>',
    ),
    (
        "Crutcher (2012), ARA&A",
        '<span class="prov"><b>Source note.</b> Crutcher (2012) is cited as a review of Zeeman measurements but is not used for any numerical result here. The quantitative comparison uses the primary survey of Troland and Crutcher (2008), which states both the measured ratios and the critical normalisation.</span>',
    ),
    (
        "Every Braginskii coefficient",
        '<span class="prov"><b>Charge-state dependence.</b> The calculations use Braginskii\'s $Z=1$ coefficients, appropriate for the hydrogenic plasmas considered here. His Table 1 gives $\\kappa_\\parallel^{\\rm e}=3.16,4.9,6.1,6.9,12.5$ for $Z=1,2,3,4,\\infty$. The corresponding perpendicular coefficients are $4.66,4.0,3.7,3.6,3.2$. For $Z=1$, the ion-density factors in his collision times equal the electron density by charge neutrality.</span>',
    ),
    (
        "Check 4 — strong particle magnetisation",
        '<div class="keyresult"><b>Strong particle magnetisation does not determine the effective viscosity.</b> The large value of $\\omega_i\\tau_i$ places the ions in the strongly magnetised regime and strongly suppresses Braginskii\'s local perpendicular viscosity. Zhuravleva et al. infer only an upper bound on an effective cluster viscosity. Comparing that bound with a local anisotropic coefficient requires a model of field geometry and velocity structure. Without such a model, the observation neither measures nor excludes the classical perpendicular coefficient.</div>',
    ),
    (
        "What the effective transport is",
        '<div class="warn"><b>Effective transport remains uncertain.</b> Zhuravleva et al. give a bound that depends on the unknown Prandtl number. They also note that present observations do not establish whether the measured density fluctuations arise from turbulence. The local Braginskii coefficients therefore cannot be converted into a measured cluster-scale transport coefficient without additional assumptions.</div>',
    ),
    (
        "These two discs are a configuration",
        '<span class="prov"><b>Status of the disc examples.</b> The two rows are illustrative configurations used to evaluate equation (9.2); they are not models fitted to particular observed discs. Their Keplerian shear parameter $q=3/2$ follows from the disc dynamics derived in Module 11. Proposition 11 reproduces the local ideal-MHD result associated with Balbus and Hawley (1991), while the derivation and numerical evaluations are given explicitly here.</span>',
    ),
    (
        "And the condition this book cannot check",
        '<div class="warn"><b>Ionisation limits the ideal-MHD calculation.</b> The MRI requires magnetic coupling between the field and the gas. A $300$ K protoplanetary disc at $n=10^{14}\\ \\mathrm{cm^{-3}}$ is nearly neutral, so non-ideal terms may suppress the instability. The condition $\\lambda_{\\rm marg}<H$ therefore applies only where the ionisation is high enough for ideal MHD. Weakly ionised regions can form magnetically inactive dead zones.</div>',
    ),
    (
        "The exponent is not the discriminant.",
        '<div class="keyresult"><b>The spectral exponent alone does not distinguish the two cascades.</b> K41 and critical balance both predict a $-5/3$ spectrum, but they predict different geometry. K41 assumes isotropic eddies, whereas critical balance gives $k_\\parallel\\propto k_\\perp^{2/3}$. Module 10 reports solar-wind indices with a mean of $1.6550$, close to $5/3$. An anisotropy measurement is required to decide which physical mechanism applies.</div>',
    ),
    (
        "Goldreich & Sridhar's own restriction",
        '<div class="warn"><b>Domain of the critical-balance result.</b> Goldreich and Sridhar restrict their derivation to oppositely directed Alfvén-wave fluxes of equal strength. The solar wind generally has a larger outward than inward flux, so their symmetric result cannot be applied to it without modification. Agreement with a $-5/3$ solar-wind spectrum is therefore suggestive but does not by itself test the published symmetric theory.</div>',
    ),
    (
        "Returned to, not derived.",
        'Pressure anisotropy lies outside the scalar-pressure closure used here. Section 11.1 explains why separate $p_\\parallel$ and $p_\\perp$ are needed, but it does not derive the firehose or mirror thresholds. A kinetic or CGL treatment is required for those instabilities.',
    ),
    (
        "Nobody in this book. Named once",
        'Ambipolar diffusion and Hall drift are identified as missing non-ideal terms. Their governing equations and characteristic scales lie beyond the present treatment.',
    ),
    (
        "Nobody. What the effective transport",
        'The effective cluster-scale transport coefficient remains undetermined. Inferring it requires a model of magnetic geometry and turbulent motions.',
    ),
    (
        "Nobody in this book. §10",
        'Section 10 identifies anisotropy as the discriminating observable. No anisotropy measurement is analysed here.',
    ),
    (
        "Nobody. No existing module",
        'Magnetic reconnection is not developed in this volume. A treatment requires non-ideal structure at current-sheet scales.',
    ),
]

html = replace_blocks(html, replacements)
PATH.write_text(html, encoding="utf-8")
print(f"rewrote {len(replacements)} Module 12 blocks")
