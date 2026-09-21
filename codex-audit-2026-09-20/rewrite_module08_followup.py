from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).parent/"textbook-edition-20-rule"/"module08.html"
def sh(t,h):
 f=BeautifulSoup(h,"html.parser");t.clear()
 for c in list(f.contents):t.append(c)
s=BeautifulSoup(P.read_text(encoding="utf8"),"html.parser")
def rep(p,h):
 m=[x for x in s.find_all(["p","li"]) if x.get_text(" ",strip=True).startswith(p)]
 if len(m)!=1:raise RuntimeError((p,len(m)))
 sh(m[0],h)
R={
"By the exact ratio":r"The exact jump gives $T_2=2.087\times10^6$ K. The strong-shock approximation gives $2.201\times10^6$ K, about 5 per cent higher. At $M_1=8$, the finite terms neglected in the asymptotic pressure and density ratios remain measurable. Problem D1 determines when the approximation becomes accurate.",
"Below $M_1 = 1$":r"For $M_1\lt1$, the algebraic branch has decreasing density and pressure and negative entropy change. At $M_1=0.9$, $\Delta s/k_B=-0.00159$; at 0.7 it is $-0.07970$; and at 0.5 it is $-1.21225$. The entropy condition excludes every member of this rarefaction-shock branch.",
"The termination shock. The measured":r"The measured termination-shock width is $10^{10}$–$3\times10^{10}$ cm. For $n\approx2\times10^{-3}\ \mathrm{cm^{-3}}$, $T\approx10^5$ K, and $\ln\Lambda=25$, the proton Coulomb mean free path is $2.28\times10^{16}$ cm, or 1524 au.",
"The layer is therefore":r"The shock is roughly $8\times10^5$–$2\times10^6$ times thinner than a collisional mean free path. Electromagnetic collective processes, rather than binary collisions, mediate the transition. Conservation laws still balance the fluxes, but collisions cannot impose a common ion temperature.",
"The anchor. Sir Geoffrey":r"Taylor, G. I. (1950), “The formation of a blast wave by a very intense explosion. II”, <i>Proc. R. Soc. A</i> <b>201</b>, 175–186. Table 1 supplies 25 Trinity radius–time pairs and their photographic-source labels. Equations (1) and (3) give normalizations that differ by 1.36 per cent. Taylor adopts $\rho_0=1.25\times10^{-3}\ \mathrm{g\,cm^{-3}}$ and derives yields for several $\gamma$. The present module transcribes the table in <code>afd/data/taylor1950_trinity.dat</code>.",
"The modern yield":r"Selby, H. D. et al. (2021), “A new assessment statement for the Trinity nuclear test”, LA-UR-21-20675, arXiv:2103.06258. Modern radiochemical measurements and simulations give $24.8\pm2$ kt TNT equivalent. The uncertainty overlaps a conservatively assigned $21\pm2$ kt interval for the earlier DOE value.",
"The Sedov constant":r"Independent similarity checks use Tang &amp; Chevalier (2017) and Kamm &amp; Timmes (2007). The former gives the spherical $\gamma=5/3$ constant 2.026 in the fifth-power convention. The latter specifies a $\gamma=1.4$ standard problem whose shock reaches 1 cm at 1 s. Both agree with the constants computed here.",
"The astrophysical check":r"Richardson, J. D. et al. (2008), “Cool heliosheath plasma and deceleration of the upstream solar wind at the termination shock”, <i>Nature</i> <b>454</b>, 63–66. Voyager 2 crossed at 84 au in 2007. The paper reports $10^5$ K thermal ions where a one-fluid conversion predicts $10^6$ K, with about 80 per cent of flow energy transferred to pickup ions. Its fitted shock parameters are not used as an independent jump-condition test.",
"Tycho, and the":r"Warren, J. S. et al. (2005), <i>ApJ</i> <b>634</b>, 376, arXiv:astro-ph/0507478. Chandra images give blast-wave, contact-discontinuity, and reverse-shock radius ratios $1:0.93:0.70$ after projection correction. The observed contact lies farther out than adiabatic hydrodynamic models predict, even with Rayleigh–Taylor mixing. The paper also reports clumps and distinct fluctuation spectra at the two boundaries.",
"The simulation the":r"Wang, C.-Y. &amp; Chevalier, R. A. (2001), <i>ApJ</i> <b>549</b>, 1119, arXiv:astro-ph/0005105. Their Type Ia remnant simulation places unstable ejecta inside 85 per cent of the remnant radius near Tycho’s age. Drag limits finger growth, and strong initial clumping is required to approach the blast wave.",
"The expansion index":r"Katsuda, S. et al. (2010), <i>ApJ</i> <b>709</b>, 1387, arXiv:1001.2484. Tycho’s forward-shock expansion index varies substantially with azimuth, with an average near 0.5. Reverse-shocked ejecta give indices approximately 0.43–0.64.",
"Quoted from Module 7":r"Shimony, A. et al. (2022), arXiv:2210.06631v1. Module 7 verifies the reported bubble coefficient $\alpha_B=0.038\pm0.008$ and the theoretical comparison near 0.05. No spike coefficient is assigned because the cited source does not provide one.",
}
for p,h in R.items():rep(p,h)
P.write_text(str(s),encoding="utf8");print("rewrote",len(R),"blocks")
