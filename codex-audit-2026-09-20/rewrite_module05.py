from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).parent/"textbook-edition-20-rule"/"module05.html"
def sh(t,h):
 f=BeautifulSoup(h,"html.parser");t.clear()
 for c in list(f.contents):t.append(c)
s=BeautifulSoup(P.read_text(encoding="utf8"),"html.parser")
def rep(p,h):
 m=[x for x in s.find_all(["p","li","figcaption"]) if x.get_text(" ",strip=True).startswith(p)]
 if len(m)!=1:raise RuntimeError((p,len(m)))
 sh(m[0],h)
R={
"Gravity against pressure":r"This module compares gravitational collapse with pressure support. It derives the Jeans and Bonnor–Ebert criteria and explains the background assumptions behind each. Applied to Barnard 68, the two criteria classify the fitted core differently. Its observed outer density profile also departs from every static isothermal sphere.",
"The system needs a closure":r"The perturbation equations require a pressure closure. For the cold clouds considered here, we assume isothermal gas, $P=c_s^2\rho$. This approximation requires radiative heating and cooling to restore the ambient temperature faster than the compression changes it.",
"The numerical solution":r"A fourth-order Runge–Kutta scheme integrates equation (5.2) from the central series. The two agree to $4\times10^{-6}$ at $\xi=0.05$ and $2\times10^{-7}$ at $\xi=0.2$. At large radius, the regular solution oscillates around the singular isothermal sphere with decreasing amplitude. Its logarithmic slope reaches a universal maximum $\xi\psi'=2.5176$ at $\xi=8.993$ before approaching 2 through damped oscillations. Section 7.3 uses this upper bound.",
"Write $S =":r"Define $S=\xi_{\max}\psi'(\xi_{\max})$. Proposition 7 gives $M=c_s^2RS/G$. Substituting this relation and $\bar\rho=3M/(4\pi R^3)$ into equation (3.3) cancels every dimensional factor. The result depends only on $S^{-3/2}$. Its minimum follows from the numerical maximum $S=2.5176$ at $\xi=8.993$. ∎",
"Proposition 9 explains":r"The two consistent entries in Table 5 have the same $\xi_{\max}$ and nearly equal $M_J/M$: $1.4149$ and $1.3972$. Their $1.25$ per cent difference reflects rounding in the tabulated masses and radii. The alternative value $0.7522$ combines a temperature and mass that violate the Bonnor–Ebert scaling $M\propto Td$ at fixed $\xi_{\max}$, so it does not represent the fitted sphere.",
"A comparison at matched":r"The observed profile is $n_{\rm H}(r)=\Delta n/[1+(r/r_0)^2]^{\eta/2}+n_{\rm out}$, with $r_0=35''$, $\eta=4.0$, $n_0=3.4\times10^5\ \mathrm{cm^{-3}}$, and $n_{\rm out}=4\times10^2\ \mathrm{cm^{-3}}$. The fitted Bonnor–Ebert model has $\xi_{\max}=6.9$ at $100''$. Comparing logarithmic slopes at equal angular radius eliminates the uncertain distance. Beyond $46.2''$, the observed slope exceeds the isothermal-sphere maximum. At $100''$, it is $3.2428$, compared with $2.4660$ for the fitted sphere.",
"What is refuted":r"The slope comparison excludes the combined assumptions of a static, spherical, isothermal, self-gravitating outer envelope. It does not identify which assumption fails. An outward temperature rise can support a steeper density profile, while asymmetry or motion offer other explanations. Because $\xi_{\max}=6.9$ comes from the same isothermal fit, the $2.25\sigma$ result of Check 1 is conditional on a model that fails over the outer $53.8$ per cent of the fitted radius.",
}
for p,h in R.items():rep(p,h)
P.write_text(str(s),encoding="utf8");print("rewrote",len(R),"blocks")
