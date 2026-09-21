from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).parent/"textbook-edition-20-rule"/"module07.html"
def sh(t,h):
 f=BeautifulSoup(h,"html.parser");t.clear()
 for c in list(f.contents):t.append(c)
s=BeautifulSoup(P.read_text(encoding="utf8"),"html.parser")
def rep(p,h):
 m=[x for x in s.find_all(["p","li"]) if x.get_text(" ",strip=True).startswith(p)]
 if len(m)!=1:raise RuntimeError((p,len(m)))
 sh(m[0],h)
R={
"The astrophysical anchor":r"Ofman, L. &amp; Thompson, B. J. (2011), “SDO/AIA Observation of Kelvin–Helmholtz Instability in the Solar Corona”, <i>ApJL</i> <b>734</b>, L11, arXiv:1101.4249. The paper reports vortex sizes of several to ten arcseconds, propagation speeds $6$–$14\ \mathrm{km\,s^{-1}}$, and an upper shear limit near $20\ \mathrm{km\,s^{-1}}$. The interface spans roughly 1–3 AIA pixels. The first vortex appears at 03:00:13 UT, and motion along the front begins at 03:13:53 UT. Their model uses density ratio $\sqrt5$, $V_0=5V_{A,xy}$, and no gravity. The coronal field strength is not measured.",
"The terrestrial check":r"Shimony, A. et al. (2022), “Determining the Self-Similar Stage of the Rayleigh–Taylor Instability via LLNL’s NIF Discovery Science Experiments”, arXiv:2210.06631v1. The preprint reports $\alpha_B=0.038\pm0.008$ for the $15\,\mu$m target and a similar slope near 0.03 for the $30\,\mu$m target. Its analytic comparison spans values near 0.025 and 0.05. The stated layer densities are pre-shock values, so this module does not infer an experimental Atwood number from them.",
"Quoted, not read":r"Classical references: Landau (1944), Miles (1958), and Fejer &amp; Miles (1963) for compressible vortex-sheet stability; Miles (1961) and Howard (1961) for the $\mathrm{Ri}\gt1/4$ sufficient condition; Read (1984) for the nonlinear mixing integral; and Chandrasekhar (1961) for interfacial stability. These works provide attribution. The module derives the incompressible dispersion relation and does not solve the viscous quartic.",
"Constants and standards":r"Physical constants use CODATA 2018. Nominal solar $GM$ and radius use IAU 2015 Resolution B3 and give $g_\odot=2.7420\times10^4\ \mathrm{cm\,s^{-2}}$. Standard terrestrial gravity is $980.665\ \mathrm{cm\,s^{-2}}$ by definition.",
}
for p,h in R.items():rep(p,h)
P.write_text(str(s),encoding="utf8");print("rewrote",len(R),"source blocks")
