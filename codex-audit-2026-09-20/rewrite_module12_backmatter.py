from pathlib import Path
from bs4 import BeautifulSoup


PATH = Path(__file__).parent / "textbook-edition-20-rule" / "module12.html"


def set_html(tag, html):
    fragment = BeautifulSoup(html, "html.parser")
    tag.clear()
    for child in list(fragment.contents):
        tag.append(child)


soup = BeautifulSoup(PATH.read_text(encoding="utf-8"), "html.parser")

intro = soup.find(id="problems").find_next("p")
set_html(intro, "Each problem states the assumptions and numerical inputs needed for its solution. The exercises distinguish measured quantities from illustrative census values and modelling choices. The independent script <code>afd/figs/m12_problems_check.py</code> reproduces all nine solutions without importing results from the module’s numerical build script.")

prompts = [
    r'''<b>C1.</b> An active-region corona has $n=10^{9}\ \mathrm{cm^{-3}}$, $T=10^{6}$ K, and $B=10$ G. The field strength is the illustrative value used in <a href="module07.html">Module 7 §9.5</a>. Take $\mu=0.61$ and $\gamma=5/3$. Calculate $p_{\rm gas}$, $p_{\rm mag}$, $\beta$, $v_{\rm A}$, and $c_s$. Obtain $v_{\rm A}/c_s$ both from the two speeds and from equation (1.2). Explain why the results must agree exactly.''',
    r'''<b>C2.</b> A coronal loop has length $L=100$ Mm, density $n=10^{9}\ \mathrm{cm^{-3}}$, temperature $T=10^{6}$ K, and field-aligned flow speed $U=10\ \mathrm{km\,s^{-1}}$. Use Braginskii’s $\sigma_\parallel=1.96\,ne^2\tau_{\rm e}/m_{\rm e}$, his equation (2.5e) for $\tau_{\rm e}$, and $\ln\Lambda=18.66$. Find $\eta_{\rm m}$, $\mathrm{R_m}$, the ohmic decay time $L^2/\eta_{\rm m}$, and the dynamical time $L/U$. Compute the ratio of the two times and interpret it.''',
    r'''<b>C3.</b> Adopt the sidereal rotation period $25.38$ d, source-surface radius $r_0=2.5\,R_\odot$, colatitude $\theta=90^\circ$, and constant wind speed $v=435.6\ \mathrm{km\,s^{-1}}$. The rotation period is the NSSDC value at $16^\circ$ latitude; the speed is the Venzmer and Bothmer mean fit at 1 au. Use equation (5.1) to calculate $-B_\phi/B_r$, the spiral angle, and the local index from equation (5.2) at 1 and 5 au. Determine the effect of neglecting $r_0$ at 1 au.''',
    r'''<b>D1.</b> A spherical cloud has diameter $10$ pc, total particle density $n_{\rm tot}=100\ \mathrm{cm^{-3}}$, mean molecular weight $\mu=2.33$, and field strength $B=10\ \mu$G. The field is an illustrative order-of-magnitude value. Calculate the cloud mass $M$. Then use both geometries in equation (7.2) to find $M_\Phi$ and $\lambda_\Phi$. Explain which conclusion is independent of the assumed geometry.''',
    r'''<b>D2.</b> At 1 au, take $n=7.57\ \mathrm{cm^{-3}}$, $|\mathbf B|=6.05$ nT, and $v=435.6\ \mathrm{km\,s^{-1}}$ from the Venzmer and Bothmer mean fits. Assume a proton plasma, $-B_\phi/B_r=0.9726$, constant $v$, $B_r\propto r^{-2}$, and $\rho\propto r^{-2}v^{-1}$. Find $B_r$, the radial Alfvén speed, and $r_{\rm A}$. Repeat the calculation with $|\mathbf B|$ and explain why that substitution is inconsistent.''',
    r'''<b>D3.</b> An intracluster plasma has $n=10^{-3}\ \mathrm{cm^{-3}}$, $T=10^{8}$ K, and $B=1\ \mu$G. Use Braginskii’s electron collision time, including its factor $4\sqrt{2\pi}$, and the derived electron Coulomb logarithm $\ln\Lambda=37.08$. For $Z=1$, calculate $\omega_{\rm e}\tau_{\rm e}$ and $\kappa_\perp/\kappa_\parallel$. Explain why this local conductivity ratio cannot be compared directly with Zhuravleva et al.’s effective-viscosity constraint.''',
    r'''<b>K1.</b> A protoplanetary disc at $R=1$ au around a solar-mass star has $B=1$ G, $n=10^{14}\ \mathrm{cm^{-3}}$, $T=300$ K, and $\mu=2.33$. Assume Keplerian shear, $q=3/2$. Calculate $\Omega_{\rm K}$, $\gamma_{\max}$, the e-folds per orbit, $v_{\rm A}$, $c_s$, $H=c_s/\Omega$, and $\lambda_{\rm marg}=2\pi v_{\rm A}/(\sqrt3\,\Omega)$. Determine whether an unstable wavelength fits within one scale height. Explain why the e-folds per orbit do not depend on $B$, $n$, or $T$.''',
    r'''<b>K2.</b> <a href="module07.html">Module 7 §9.1</a> gives $\rho_h=5.8607\times10^{-16}$ and $\rho_l=2.6210\times10^{-16}\ \mathrm{g\,cm^{-3}}$ for a coronal-mass-ejection flank. It treats the measured shear $\Delta U=20\ \mathrm{km\,s^{-1}}$ as an upper limit. Use equation (4.2) to bound $B\cos\theta$ for equal fields and for a one-sided field. For $B=1$ G and $10$ G, express the allowed direction as a departure from perpendicular to $\mathbf B$. Identify the required inverse trigonometric function.''',
    r'''<b>K3.</b> For the intracluster plasma in Problem D3, calculate ion magnetisation in two ways. First evaluate $\lambda/r_g$ using Module 1’s Coulomb mean free path at $\ln\Lambda=37.8$ and $r_g=v_\perp/\omega_{\rm c}$ with $v_\perp=\sqrt{2k_{\rm B}T/m_{\rm p}}$. Then evaluate $\omega_i\tau_i$ using Braginskii’s $\tau_i$ at $\ln\Lambda=37.081$. Derive the ratio between the results and state which convention belongs in Braginskii’s factor $(\omega_{\rm c}\tau)^{-2}$.''',
]

problems = soup.select("div.prob")
if len(problems) != len(prompts):
    raise RuntimeError(f"expected {len(prompts)} problems, found {len(problems)}")
for problem, prompt in zip(problems, prompts):
    details = problem.find("details", class_="sol")
    saved = details.extract()
    set_html(problem, prompt)
    problem.append(saved)


def replace_paragraph(prefix, html):
    matches = [p for p in soup.find_all("p") if p.get_text(" ", strip=True).startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"prefix {prefix!r} matched {len(matches)} paragraphs")
    set_html(matches[0], html)


replacements = {
    "The ratio of the two speeds": r'''Using unrounded values gives $v_{\rm A}/c_s=5.8807$. Equation (1.2) independently gives $\sqrt{2/(\gamma\beta)}=5.8807$. The displayed speeds are rounded, so their printed ratio differs slightly.''',
    "They must agree exactly": r'''The agreement is exact because equation (1.2) is an identity. Its derivation eliminates $\rho$, and the same mean molecular weight enters both speeds. A disagreement would therefore reveal inconsistent inputs or conventions rather than new physics.''',
    "$\\eta_{\\rm m} = c^2": r'''$\eta_{\rm m}=c^2/(4\pi\sigma_\parallel)=\mathbf{9.768\times10^{3}\ cm^2\,s^{-1}}$. This finite diffusivity is nevertheless small enough to produce an enormous magnetic Reynolds number on coronal-loop scales.''',
    "Their ratio is $1.024": r'''The ratio of the ohmic and dynamical times is $1.024\times10^{12}$, equal to $\mathrm{R_m}$. This equality follows identically from $(L^2/\eta_{\rm m})/(L/U)=UL/\eta_{\rm m}$. It also provides an internal numerical check.''',
    "And the comparison is with": r'''Flux freezing is assessed against the loop’s dynamical time, not against a cosmological age. The loop evolves in $10^4$ s, while resistive decay requires $3.244\times10^8$ yr. Magnetic diffusion is therefore negligible during the loop’s evolution.''',
    "The spiral tightens outward": r'''The spiral becomes increasingly azimuthal with distance. The local index changes from $-1.51$ at 1 au toward the asymptotic value $-1$. By 5 au, the total field decreases approximately as $r^{-1}$ rather than $r^{-2}$.''',
    "Dropping $r_0$": r'''Neglecting $r_0$ increases $-B_\phi/B_r$ at 1 au from $0.9726$ to $0.9840$, a change of $1.18$ per cent. The fractional effect is smaller at 5 au because $r_0/r$ decreases with distance.''',
    "Neither should be quoted alone": r'''Both geometries classify the cloud as supercritical, so the physical conclusion is robust: the adopted field cannot prevent collapse. The inferred $\lambda_\Phi$ differs by the coefficient ratio $1.2657$. A numerical mass-to-flux ratio must therefore be reported with its assumed geometry.''',
    "Note also what has been assumed": r'''The flux estimate $\Phi=\pi R^2B$ assumes a uniform field threading the cloud’s mid-plane. A tangled field with the same $|B|$ generally contributes less net flux, which would make the inferred cloud more supercritical.''',
    "That answer is wrong twice over": r'''Using $|\mathbf B|$ is inconsistent for two reasons. First, the extrapolation assumes an $r^{-2}$ scaling, which applies to $B_r$ rather than to the total Parker field. Second, the Weber–Davis surface is defined using radial flow and radial Alfvén speeds. Either reason requires the radial component.''',
    "A caution about which number": r'''The value $16.97\,R_\odot$ represents only one of the eight variants considered in §6.1. The full range, $15.76$–$19.35\,R_\odot$, better represents the sensitivity to fit choice, velocity model, and helium abundance.''',
    "Why the two $\\ln\\Lambda$": r'''The value $37.08$ is the electron-branch Coulomb logarithm derived for this density and temperature. Modules 1 and 10 use the census value $37.8$. Their $1.9$ per cent difference is one factor in equation (8.3), not a correction to either convention.''',
    "Why $4.712$ contains": r'''Equation (9.2) gives $\gamma_{\max}=q\Omega/2$, so a Keplerian disc undergoes $2\pi\gamma_{\max}/\Omega=3\pi/2$ e-folds per orbit. This rate depends only on the shear. The field controls the unstable wavelengths and therefore determines whether a mode fits inside the disc.''',
    "What this does not establish": r'''This ideal-MHD calculation assumes that the gas remains coupled to the field. A $300$ K disc at $n=10^{14}\ \mathrm{cm^{-3}}$ is predominantly neutral, so its coupling depends on the ionisation fraction. The calculation establishes the ideal-MHD result but does not show that this particular disc satisfies that approximation.''',
    "You need $\\arcsin$": r'''The required departure from perpendicular is $90^\circ-\theta$, whose sine equals $\cos\theta$. The appropriate inverse function is therefore $\arcsin$. Applying $\arccos$ returns $\theta$ itself, $86.13^\circ$ for the 1 G case, rather than the $3.87^\circ$ departure from perpendicular.''',
    "It is worth noticing": r'''The complementary angle $86.13^\circ$ appears numerically plausible, so dimensional or magnitude checks will not expose the mistake. Defining the angle geometrically before applying the inverse function prevents this error.''',
    "The $\\sqrt{3/2}$ is a component count": r'''The exact factor $\sqrt{3/2}$ comes from the thermal-speed convention. The mean free path uses the three-dimensional rms speed $\sqrt{3k_{\rm B}T/m}$, whereas the gyroradius uses the perpendicular rms speed $\sqrt{2k_{\rm B}T/m}$. Their ratio is $\sqrt{3/2}$. The remaining $1.9$ per cent comes from the two Coulomb logarithms.''',
    "Braginskii's belongs": r'''Braginskii’s $\omega_{\rm c}\tau$ must be used in his transport factor $(\omega_{\rm c}\tau)^{-2}$ because the numerical transport coefficients are defined with that collision time. Substituting the mean-free-path convention would introduce an artificial factor $1.2015^2=1.44$.''',
}
for prefix, html in replacements.items():
    replace_paragraph(prefix, html)

# Notation notes describe conventions directly rather than narrating editorial work.
notation = soup.find(id="notation")
notation_paragraphs = notation.find_all_next("p", limit=2)
set_html(notation_paragraphs[0], r"The table defines every symbol used in this module and records its units. It also distinguishes symbols that carry different meanings elsewhere in the book, including $\eta$, $\lambda$, $\beta$, $\sigma$, $\kappa$, $\Omega$, and $\mu$.")
set_html(notation_paragraphs[1], r"Section 8 uses the derived electron Coulomb logarithm $\ln\Lambda=37.081$. Modules 1 and 10 use the census value $37.8$. The $1.9$ per cent difference contributes one factor in equation (8.3); the thermal-speed convention contributes the other.")

PATH.write_text(str(soup), encoding="utf-8")
print(f"rewrote {len(prompts)} problem statements and {len(replacements)} solution paragraphs")
