from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).parent/"textbook-edition-20-rule"/"module09.html"
def sh(t,h):
 f=BeautifulSoup(h,"html.parser");t.clear()
 for c in list(f.contents):t.append(c)
s=BeautifulSoup(P.read_text(encoding="utf8"),"html.parser")
def rep(p,h):
 m=[x for x in s.find_all(["p","li"]) if x.get_text(" ",strip=True).startswith(p)]
 if len(m)!=1:raise RuntimeError((p,len(m)))
 sh(m[0],h)
R={
"Baganoff et al. Compute":r"Baganoff et al. calculate $R_B\approx0.05$ pc and adopt 0.06 pc using $M=2.6\times10^6M_\odot$. At fixed sound speed, $R_B/r_S=c^2/c_\infty^2$ is independent of mass and equals $1.97\times10^5$. Their quoted $2\times10^5r_S$ therefore corresponds to the calculated 0.05 pc. Comparisons in parsecs require mass rescaling, whereas comparisons in gravitational radii do not.",
"The ratios are":r"For relative speeds $0$, $0.5$, $1$, $2$, and $5$ times $c_\infty$, the accretion-rate ratios are $1.0000$, $0.7155$, $0.3536$, $0.0894$, and $0.0075$. At $5c_\infty$, motion suppresses the rate by a factor 133 because $(v^2+c_\infty^2)^{-3/2}$ replaces $c_\infty^{-3}$.",
"What kind of result":r"Bondi presents the moving-accretor formula as an order-of-magnitude interpolation, not a spherical derivation. It connects his solved velocity-dominated and temperature-dominated limits. The moving flow is not spherical, so Propositions 2–6 do not apply directly.",
"With $\\dot M = 9.843":r"For $\dot M=9.843\times10^{11}\ \mathrm{g\,s^{-1}}$ and $v=435.6\ \mathrm{km\,s^{-1}}$, the kinetic power is $9.34\times10^{26}\ \mathrm{erg\,s^{-1}}$. Lifting the wind from the solar potential requires $1.88\times10^{27}\ \mathrm{erg\,s^{-1}}$. Their sum matches the approximate Ulysses energy flux, while enthalpy contributes another 1.3 per cent and conductive flux is not calculated.",
"All three are":r"The kinetic, gravitational, and observed wind powers are all within a factor of three and near $10^{-6}L_\odot$. This energy is negligible for the solar luminosity but decisive for heliospheric structure. Its small fraction does not distinguish among possible coronal-heating mechanisms.",
"Taking the cloud":r"For fully ionised $10^4$ K gas with $\mu=0.6$, $c_\infty=9.81\ \mathrm{km\,s^{-1}}$ and $v/c_\infty=2.65$. Including helium gives $\rho=4.683\times10^{-25}\ \mathrm{g\,cm^{-3}}$. The moving-accretor estimate then gives $R_B=2.3$ au and $\dot M=8.59\times10^{-17}M_\odot\,\mathrm{yr^{-1}}$.",
"Against the outward":r"The solar wind removes mass 182 times faster than this interstellar accretion estimate supplies it. Accretion is therefore negligible in the present solar mass budget.",
"What it implies":r"The molecular-cloud example predicts a rate about three thousand times Eddington. Radiation pressure would then invalidate the assumption of dynamically negligible radiation. The spherical Bondi model is therefore self-inconsistent in this regime and must be replaced by radiation hydrodynamics.",
"The pattern is":r"For Sgr A*, the Bondi supply is about $10^{-4}$ of Eddington while luminosity is about $10^{-12}$ of Eddington. The outer supply and Faraday-rotation rate differ by a factor 40; the remaining luminosity deficit requires radiative efficiency near $4\times10^{-9}$ if that upper rate applies. The data allow mass loss, inefficient radiation, or both.",
"The anchor. M. S.":r"Venzmer, M. S. &amp; Bothmer, V. (2018), <i>A&amp;A</i> <b>611</b>, A36, arXiv:1711.07534. Table 3 gives the Helios radial power-law fits used in §7, and Fig. 9 gives their yearly scatter. Their near-Sun temperature range of 2–3 MK is itself a secondary citation.",
"The solar-wind mass":r"Verscharen, D., Bale, S. D. &amp; Velli, M. (2021), <i>MNRAS</i> <b>506</b>, 4993, arXiv:2107.06540. Section 3.1 provides polar and equatorial mass fluxes and an approximate polar energy flux. Table 3 gives Alfvén radii. Its sonic-radius estimate is a lower bound, so §7.5 does not treat it as a direct measurement.",
"The Galactic Centre":r"Baganoff, F. K. et al. (2003), <i>ApJ</i> <b>591</b>, 891, arXiv:astro-ph/0102151. Near Sgr A*, they report $n_e\approx130\ \mathrm{cm^{-3}}$, $kT_e\approx2$ keV, and $c_s\approx670\ \mathrm{km\,s^{-1}}$. Using their assumed black-hole mass, they obtain $R_B\approx0.05$ pc and $\dot M_B\approx3\times10^{-6}M_\odot\,\mathrm{yr^{-1}}$.",
"The bound on":r"Marrone, D. P. et al. (2007), <i>ApJL</i> <b>654</b>, L57, arXiv:astro-ph/0611791. The measured Faraday rotation is $(-5.6\pm0.7)\times10^5\ \mathrm{rad\,m^{-2}}$. Equipartition, ordered, mainly radial fields imply $\dot M\lt2\times10^{-7}M_\odot\,\mathrm{yr^{-1}}$. Weaker or reversing fields relax this upper bound.",
"The coronal base":r"Allen, C. W. (1947), <i>MNRAS</i> <b>107</b>, 426. The two-term electron-density law is fitted over $1.2$–$2.6R_\odot$. Section 2.1 extrapolates it to $1.03R_\odot$, where the steep $r^{-16}$ term dominates, so the base density carries substantial model uncertainty.",
"The wind. E.":r"Parker, E. N. (1958), <i>ApJ</i> <b>128</b>, 664. Section II shows that a conductive corona retains an asymptotic pressure far above the adopted interstellar value. The paper derives the transonic solar-wind solution but does not use the later six-family Roman-numeral classification.",
"The accretion flow":r"Bondi, H. (1952), <i>MNRAS</i> <b>112</b>, 195. Equation (18) gives the critical eigenvalue and equation (19) the maximum steady spherical rate. Table I provides the standard values for several $\gamma$. Section 8 proposes the moving-accretor interpolation as an order-of-magnitude conjecture.",
"Every number in":r"The module’s numerical script generates its tables, and the figure script imports those results to prevent drift. A separate problem-checking script recomputes the exercises from their stated assumptions without importing the production calculations.",
}
for p,h in R.items():rep(p,h)
P.write_text(str(s),encoding="utf8");print("rewrote",len(R),"blocks")
