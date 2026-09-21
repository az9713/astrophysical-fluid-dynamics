from pathlib import Path
from bs4 import BeautifulSoup

PATH=Path(__file__).parent/"textbook-edition-20-rule"/"module04.html"
def set_html(tag,html):
 f=BeautifulSoup(html,"html.parser");tag.clear()
 for c in list(f.contents):tag.append(c)
s=BeautifulSoup(PATH.read_text(encoding="utf8"),"html.parser")
def rep(prefix,html):
 ms=[x for x in s.find_all(["p","li","figcaption"]) if x.get_text(" ",strip=True).startswith(prefix)]
 if len(ms)!=1:raise RuntimeError(f"{prefix!r}: {len(ms)}")
 set_html(ms[0],html)
R={
"Perturbing the equilibrium":r"This module perturbs the hydrostatic equilibrium developed in Module 3. It derives the acoustic wave equation, distinguishes isothermal and adiabatic sound speeds, and obtains the cutoff frequency of a stratified atmosphere. The measured solar large separation then tests these approximations and isolates the contribution of the outermost layers.",
"A star is not uniform":r"A star is stratified by gravity. Module 3 derived an isothermal plane-parallel atmosphere with $P,\rho\propto e^{-z/H}$ and $H=k_BT/(\mu m_ug)$. Perturbing that equilibrium introduces an acoustic cutoff. Waves below the cutoff frequency cannot propagate upward through the atmosphere.",
"Evaluate (4.6)":r"Evaluate equation (4.6) at the photosphere. The nominal solar $GM$ and the radius of the §6 model give $g_\odot=2.7398\times10^4\ \mathrm{cm\,s^{-2}}$. Its surface abundances are $X=0.7583$, $Y=0.22905$, and $Z=0.01265$. Treating the gas as neutral and assigning mass 16 per heavy-element particle gives",
"The bound (5.3a)":r"Equation (5.3a) shows that the departure from $n/(2\tau)$ decreases as $1/\nu_n$, consistent with the second-order correction in equation (5.4). A spherical star adds a regularity condition at the centre and an upper turning point set by the acoustic cutoff. Tassoul’s asymptotic analysis gives the corresponding spectrum for radial order $n$ and angular degree $\ell$.",
"Simpson's rule":r"Simpson’s rule gives $2963.15$ s, while the trapezoidal rule gives $2963.16$ s. Halving the number of rows changes the result to $2963.20$ s, so numerical quadrature contributes less than $0.1$ s. The isothermal-to-adiabatic ratio is $3825.4/2963.2=1.2910=\sqrt{5/3}$, as required by the constant sound-speed factor.",
"A positive remainder":r"A positive outer-layer remainder is only a weak constraint. Any closure with an interior crossing time below the measured total would satisfy it. The relevant question is whether a physically motivated outer-layer model supplies the required $644$ s; §7.3 evaluates one such model.",
"The adiabatic assumption":r"Adiabatic propagation also requires radiative diffusion to be slow, $\omega\chi/c^2\ll1$. This module does not evaluate that ratio through the solar envelope. It should hold in the deep interior and fail near the radiating photosphere, but Module 13 must quantify the transition.",
"To ask whether":r"To estimate the missing $644$ s, model the untabulated outer layer between depth $D=11{,}776$ km, where $T=81{,}200$ K, and the photosphere, where $T=5772$ K. Assume that temperature varies linearly with depth. This form follows from a polytropic layer with constant $\mu$ and $g$. With uniform $\Gamma_1$ and $\mu$, the sound speed obeys $c^2=\Gamma_1k_BT/(\mu m_u)$, allowing the crossing time to be integrated analytically.",
"The slope of the linear":r"The adopted linear profile has slope $6.41\ \mathrm{K\,km^{-1}}$. A fully ionised $n=3/2$ adiabat gives $7.78\ \mathrm{K\,km^{-1}}$, whereas a neutral adiabat gives $16.15\ \mathrm{K\,km^{-1}}$. The tabulated endpoint is therefore closer to the ionised case. The actual Sun contains a thin superadiabatic region, so the linear profile remains an approximation whose crossing-time bias is not determined here.",
"The model's effective":r"The model’s effective molecular weight rises by $11.6$ per cent toward its outermost row. Recombination provides the standard physical interpretation because it reduces the number of free particles per unit mass. The table alone does not separate ionisation from non-ideal pressure corrections, which could produce a similar inferred $\mu$. Both ionisation and the associated reduction in $\Gamma_1$ occur mainly in the untabulated surface layers.",
"One limitation belongs":r"Checks 2–4 combine an observed frequency spacing with pressure and density from a solar model, so they test closures conditional on that model structure. Module 3 shows that the same model misplaces the convection-zone base by $0.0147R$. Reversing the isothermal exclusion would require a structural correction of at least $3.25$ per cent in the crossing time. This module does not calculate whether the model error has the required magnitude or sign.",
}
for p,h in R.items():rep(p,h)
PATH.write_text(str(s),encoding="utf8");print("rewrote",len(R),"blocks")
