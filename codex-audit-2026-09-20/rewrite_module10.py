from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).parent/"textbook-edition-20-rule"/"module10.html"
def sh(t,h):
 f=BeautifulSoup(h,"html.parser");t.clear()
 for c in list(f.contents):t.append(c)
s=BeautifulSoup(P.read_text(encoding="utf8"),"html.parser")
def rep(p,h):
 m=[x for x in s.find_all(["p","li","figcaption"]) if x.get_text(" ",strip=True).startswith(p)]
 if len(m)!=1:raise RuntimeError((p,len(m)))
 sh(m[0],h)
R={
"The units line":r"The exponent depends on defining $E(k)$ as energy per unit wavenumber. Its units are $\mathrm{cm^3\,s^{-2}}$, not those of energy itself. Dimensional analysis then gives $k^{-5/3}$. Changing the spectral definition changes the exponent and the physical quantity being described.",
"What dimensional":r"Dimensional analysis leaves the Kolmogorov constant $C$ undetermined. If local isotropic cascade physics is universal, different flows should yield the same value. Section 5 tests this claim with laboratory measurements before the constant is used astrophysically.",
"The inertial range is a band":r"Energy enters at the stirring scale $L$ and leaves near the dissipation scale $\eta$. Between them, K41 predicts $E(k)\propto k^{-5/3}$. A shock spectrum proportional to $k^{-2}$ falls faster, differing by a factor $2.15$ after one decade and $21.5$ after four. The plotted cutoff is schematic; its shape is not derived here.",
"The inertial range of":r"The same scaling that determines the inertial-range spectrum also fixes the dissipation scale. Resolving that scale throughout a three-dimensional domain sets the minimum cost of direct numerical simulation. For astrophysical Reynolds numbers, that cost is prohibitive.",
"The snapshot column":r"The storage estimate assigns three eight-byte velocity components to each grid point. It excludes density, pressure, magnetic fields, and additional time-integration arrays. The quoted memory is therefore a strict lower bound.",
"Proposition 2 predicts":r"K41 predicts the spectral exponent but leaves the Kolmogorov constant to experiment. Laboratory measurements test whether that constant is universal. This calibration precedes its use for solar-wind and molecular-cloud spectra.",
"One entry of":r"Grant, Stewart, and Moilliet (1962) measured tidal-channel spectra at $R_\lambda=3000$–$18000$. Their three-dimensional constant is $1.436\pm0.061$, only $1.09$ population standard deviations below the compiled mean. It is therefore typical of the laboratory sample.",
"Definition 1 needs":r"Estimating Reynolds number from $\nu\simeq\lambda\bar v/3$ is justified only when $\mathrm{Kn}\ll1$. This expression is the first Chapman–Enskog correction. Two of the four astrophysical examples lie outside that regime, so their collisional Reynolds numbers cannot be interpreted as valid transport predictions.",
"And the bound":r"Zhuravleva et al. (2019) compare deep Chandra observations of the Coma cluster with viscous simulations. They find no Coulomb-viscous cutoff and infer that effective viscosity is suppressed by at least a factor 10–1000 for $\mathrm{Pr}\le1$. The classical value $\mathrm{Re}=0.90$ is therefore only a lower bound.",
"Equation (6.8) is":r"Equation (6.8) reconciles two viscosity normalizations through velocity averaging. Both speeds are three-dimensional; one is $\langle v\rangle$ and the other $\sqrt{\langle v^2\rangle}$. The coefficients $0.96$ and $1.042$ therefore do not represent competing physical viscosities.",
"The conclusion does":r"Both solar-wind parameter sets have $\mathrm{Kn}$ of order unity, so collisional viscosity is invalid in either case. Their numerical mean free paths differ because the thermodynamic inputs differ. The Coulomb logarithm should also use electron rather than proton temperature, adding another reason not to combine the two data sets.",
"A one-dimensional quantity":r"The module lists every thermal speed, velocity dispersion, and spectral width with its component convention. This prevents comparisons between one-dimensional and three-dimensional quantities unless the conversion is explicit.",
"Eight fitted exponents":r"Solar-wind magnetic and velocity spectra are compared with the $5/3$ Kolmogorov and $3/2$ Iroshnikov–Kraichnan indices. Error bars show 99 per cent confidence intervals. Magnetic indices scatter around $5/3$, whereas all four velocity indices lie below it. The pattern is visible without combining the intervals.",
"Read the velocity":r"Each of the four velocity indices lies below $5/3$ by 3.8–8.3 times its 99 per cent half-width. All four deviations have the same sign across eight years. The data therefore reject a $5/3$ velocity spectrum far beyond the formal fit uncertainty.",
"The magnetic column":r"The magnetic indices are $1.66$, $1.72$, $1.66$, and $1.58$. Their mean lies near $5/3$, but individual intervals show real scatter larger than their fit errors. Only two agree with $5/3$ within their own intervals. The evidence supports a mean relation, not interval-by-interval equality.",
"Everything so far":r"K41 and the exact $4/5$ law assume incompressibility. This is reasonable for the intracluster example, where $\mathcal M_{3D}=0.273$. Molecular-cloud turbulence has Mach number near ten, so density fluctuations and shocks change the cascade phenomenology.",
"The last check":r"The final comparison asks whether molecular-cloud linewidths follow the Kolmogorov exponent $h=1/3$. They do not. Connecting observed linewidths to a spectral index requires the statistical relation derived in the following proposition.",
"The statistical case":r"Solomon et al. report that formal fit error is smaller than their systematic envelope, so the envelope provides the conservative uncertainty. They explicitly conclude that their data rule out the earlier Kolmogorov interpretation.",
"Why Solomon":r"Larson’s exponent $0.38$ came from an eye fit to heterogeneous literature data and has no parameter uncertainty. Solomon et al. fit 273 clouds from one survey and report an uncertainty envelope, obtaining $0.50$. Larson motivated the question; the homogeneous Solomon sample provides the stronger test.",
"An order-of-magnitude":r"Using $\sigma_v(1\,\mathrm{pc})=1.0\ \mathrm{km\,s^{-1}}$ in the uniform-sphere virial estimate gives $\Sigma=222M_\odot\,\mathrm{pc^{-2}}$, compared with the reported 170. The ratio 1.31 is acceptable only as an order-of-magnitude check because the adopted virial coefficient differs from Solomon et al.’s.",
"Solomon et al. also":r"Without the authors’ $2\ \mathrm{km\,s^{-1}}$ velocity extrapolation, the linewidth normalization falls from 1.0 to 0.83. Every derived Mach number decreases by 17 per cent, while the fitted exponent and its rejection of $1/3$ remain unchanged.",
}
for p,h in R.items():rep(p,h)
P.write_text(str(s),encoding="utf8");print("rewrote",len(R),"blocks")
