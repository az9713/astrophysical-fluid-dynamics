from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).parent/"textbook-edition-20-rule"/"module10.html"
def sh(t,h):
 f=BeautifulSoup(h,"html.parser");t.clear()
 for c in list(f.contents):t.append(c)
s=BeautifulSoup(P.read_text(encoding="utf8"),"html.parser")
def rep(p,h):
 m=[x for x in s.find_all(["p","li"]) if x.get_text(" ",strip=True).startswith(p)]
 if len(m)!=1:raise RuntimeError((p,len(m)))
 sh(m[0],h)
R={
"The ratio is":r"The exact-to-dimensional velocity ratio is $(4/5)^{1/3}=0.9283$. Both expressions contain the same product $\varepsilon\ell$ and differ only by the exact coefficient. The dimensional estimate is therefore accurate to about eight per cent for this quantity.",
"The minus sign says":r"The negative third-order moment means longitudinal increments are skewed toward approaching motions, consistent with a forward cascade. Evaluating it with $\varepsilon=U^3/L$ still imports the outer-scale K41 estimate, even though the $4/5$ coefficient itself is exact.",
"Check the licence":r"Here $\mathrm{Kn}=3.2\times10^{-7}$, safely inside the Chapman–Enskog regime. The Reynolds-number estimate is therefore meaningful, unlike the collisionless example in D1. Because the adopted cross-section is uncertain by about a factor of two, one significant figure is sufficient.",
"Read it as a":r"The measured three-dimensional Kolmogorov constant spans approximately $1.53$–$1.62$. This gives $E(k)=7.1$–$7.5\times10^{28}\ \mathrm{cm^3\,s^{-2}}$ for the stated inputs. Reporting the range reflects the uncertainty in the constant and preserves the spectral-density units.",
"(a) Unmagnetised":r"The unmagnetised formula gives $\mathrm{Re}=0.90$ at $\mathrm{Kn}=0.375$. Since this Knudsen number lies outside the Chapman–Enskog regime, the result does not establish laminar flow. It only shows that the collisional viscosity formula is being extrapolated beyond its domain.",
"Every symbol used":r"The notation table defines each symbol and its units. It also distinguishes reused symbols such as $\eta$, $\nu$, $b$, $L$, $E$, and $\alpha$ from their meanings in earlier modules.",
"The anchor. J.":r"Podesta, J. J., Roberts, D. A. &amp; Goldstein, M. L. (2007), <i>ApJ</i> <b>664</b>, 543–548. Tables 1 and 2 provide four Wind intervals and their magnetic, velocity, and energy spectral exponents at 99 per cent confidence. Endpoint sensitivity is smaller than the tabulated fit errors.",
"The Kolmogorov constant":r"Sreenivasan, K. R. (1995), <i>Physics of Fluids</i> <b>7</b>, 2778–2784. The compilation gives one-dimensional $C_K=0.53\pm0.055$ over more than 100 spectra and discusses a revision near 0.50. Isotropy factors convert these values to the three-dimensional constants used here.",
"The cluster. Hitomi":r"Hitomi Collaboration (2016), <i>Nature</i> <b>535</b>, 117–121, arXiv:1607.04487. The line-of-sight velocity dispersion is $164\pm10\ \mathrm{km\,s^{-1}}$ at 30–60 kpc, with 90 per cent confidence. The gas temperature is $4.1\pm0.1$ keV, and turbulent pressure support is at most about four per cent without large-scale shear.",
"The size–linewidth relation, properly":r"Solomon, P. M. et al. (1987), <i>ApJ</i> <b>319</b>, 730–741. Their 273-cloud fit gives $\sigma_v=(1.0\pm0.1)S^{0.5\pm0.05}\ \mathrm{km\,s^{-1}}$. The exponent uncertainty is a systematic envelope from alternative cloud definitions. The authors explicitly reject the earlier Kolmogorov interpretation.",
"The contested intracluster":r"Zhuravleva, I. et al. (2019), <i>Nature Astronomy</i> <b>3</b>, 832–837, arXiv:1906.06346. Coma fluctuation spectra compared with simulations require effective viscosity to be suppressed by roughly 10–1000 for $\mathrm{Pr}\le1$. The result rules out a purely Coulomb-collision-dominated transport model for that region.",
"The Coulomb mean free path. C.":r"Sarazin, C. L., <i>X-ray Emission from Clusters of Galaxies</i> (1988), §5.4. The Coulomb logarithm $37.8$ and mean free path near 23 kpc are the values already used and checked in Module 1.",
"The check script":r"The independent problem checker reconstructs each answer from the inputs printed in the exercise. It does not import numerical-production code, so it can expose assumptions that otherwise exist only in a generator.",
}
for p,h in R.items():rep(p,h)
P.write_text(str(s),encoding="utf8");print("rewrote",len(R),"blocks")
