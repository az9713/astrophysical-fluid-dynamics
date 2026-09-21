from pathlib import Path
from bs4 import BeautifulSoup

PATH = Path(__file__).parent / "textbook-edition-20-rule" / "module03.html"


def set_html(tag, html):
    frag = BeautifulSoup(html, "html.parser")
    tag.clear()
    for child in list(frag.contents): tag.append(child)


soup = BeautifulSoup(PATH.read_text(encoding="utf-8"), "html.parser")

def replace(prefix, html):
    ms=[x for x in soup.find_all(["p","li","figcaption"]) if x.get_text(" ",strip=True).startswith(prefix)]
    if len(ms)!=1: raise RuntimeError(f"{prefix!r} matched {len(ms)}")
    set_html(ms[0],html)

R={
"Setting the velocity":r"Hydrostatic equilibrium follows by setting the fluid velocity to zero. This module derives atmospheric scale heights, polytropes, and the Lane–Emden equation. A standard solar model then tests where these approximations succeed and where they fail.",
"A sound wave carries":r"Pressure disturbances restore hydrostatic balance at approximately the sound speed. At the solar centre, $\sqrt{P_c/\rho_c}=394.1\ \mathrm{km\,s^{-1}}$, giving a crossing time of $29.4$ minutes. This differs from the free-fall estimate by only $0.3$ per cent, partly by coincidence. Their common scale follows from the virial relation $3\int P\,dV=-\Omega$. With $\Omega\sim-GM^2/R$ and $\int P\,dV\sim(P/\rho)M$, one obtains $P/\rho\sim GM/R$ and hence $R/c_s\sim\sqrt{R^3/(GM)}$.",
"Read the last column":r"The ratio $H/R$ determines whether a plane-parallel atmosphere is adequate. It is $1/755$ for Earth and $1/5167$ at the solar photosphere, so curvature is negligible across one scale height in both cases. In the intracluster medium, $H/R=0.64$. Gravity changes substantially over that distance, requiring the spherical equation (2.4).",
"Note what the proof needs":r"Proposition 6 assumes that $\beta$ is constant and that radiation pressure is nonzero. The radiation fraction is $1-\beta=a_{\rm rad}T^4/(3P)$. Constant $\beta$ therefore requires $T^4\propto P$, or $d\ln T/d\ln P=1/4$, at every depth. Section 10 tests this gradient in the Sun and measures the central radiation fraction.",
"The case $n=0$":r"The $n=0$ polytrope requires a limiting definition because $\rho=\rho_c\theta^n$ makes the density uniform. Rewrite the length scale as $a^2=(n+1)P_c/(4\pi G\rho_c^2)$ and define $P=P_c\theta^{n+1}$. Both remain finite at $n=0$. Hydrostatic balance then gives $P=P_c-(2/3)\pi G\rho_c^2r^2$. With $r=a\xi$, the solution is $\theta=1-\xi^2/6$, which satisfies equation (6.2) with $\theta^0=1$.",
"The comparison object":r"The checks use the BS2005-AGS,OP standard solar model of Bahcall, Serenelli, and Basu (2005). This numerical stellar-evolution model is calibrated to the present solar radius and luminosity at the solar age. Its tabulated profile is stored in <code>data/bs05_agsop.dat</code>.",
"Two quantities computed":r"Section 10 uses an effective central mean molecular weight obtained from the ideal-gas relation. Inverting $P=\rho k_BT/(\mu m_u)$ gives $\mu=0.82851$. The tabulated composition instead gives $\mu=0.83195$ for a fully ionised gas, a ratio of $0.99587$. Radiation pressure explains $6\times10^{-4}$ of the $4.1\times10^{-3}$ difference; the remaining non-ideal contribution is not assigned here.",
"The reason for the failure":r"Proposition 6 fails because the solar radiation fraction is not constant. Across the sampled radiative interior, $d\ln T/d\ln P$ ranges from $0.1937$ to $0.3963$ rather than remaining at $1/4$. Radiation contributes only $6.19\times10^{-4}$ of the central pressure, so it cannot enforce a fixed $\beta$. Problem K3 shows that the radiation fraction becomes appreciable for more massive stars, reaching about 42 per cent at $50\,M_\odot$.",
"Inside $0.15":r"The effective polytropic index varies throughout the radiative interior. It is about $2.1$ inside $0.15R$, crosses $3$ at $0.217R$, reaches $4.16$ near $0.453R$, and falls through $3$ again at $0.674R$. No single polytrope describes this region. In the nuclear-burning core, composition gradients make $n_{\rm eff}$ a statement about the local temperature gradient rather than a global relation between $P$ and $\rho$. The chemically mixed convection zone does not share this ambiguity.",
"State exactly what":r"The comparison isolates a failure of the low-abundance solar model, not of hydrostatic equilibrium or the convective $n=3/2$ closure. BS2005-AGS,OP places the convection-zone base at $0.7280R$. Helioseismology gives $0.713\pm0.001R$. Opacity and heavy-element abundance determine where the radiative gradient first reaches the adiabatic value, so the discrepancy is evidence for the solar-abundance problem.",
}
for p,h in R.items():replace(p,h)
PATH.write_text(str(soup),encoding="utf-8")
print(f"rewrote {len(R)} prose blocks")
