from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).parent/"textbook-edition-20-rule"/"module11.html"
def sh(t,h):
 f=BeautifulSoup(h,"html.parser");t.clear()
 for c in list(f.contents):t.append(c)
s=BeautifulSoup(P.read_text(encoding="utf8"),"html.parser")
def rep(p,h):
 m=[x for x in s.find_all(["p","li","figcaption"]) if x.get_text(" ",strip=True).startswith(p)]
 if len(m)!=1:raise RuntimeError((p,len(m)))
 sh(m[0],h)
R={
"Angular momentum, not":r"Angular momentum prevents orbiting gas from falling directly inward. Molecular viscosity removes it far too slowly, so accretion-disc theory introduces an effective stress parameter $\alpha$. Observations infer values that vary by factors of ten to forty between disc classes, while current MRI simulations generally produce smaller stresses.",
"Both satisfy":r"Both fiducial discs have $H/R\ll1$, validating the thin-disc geometry later quantified in §7. The active-galactic-nucleus example enters in §8, where its temperature is derived from the accretion rate rather than specified independently.",
"Two consequences are":r"In a Keplerian potential, the epicyclic and orbital frequencies are equal. This degeneracy makes radial perturbations close after one orbit and simplifies the Toomre criterion. In a general galactic potential, $\kappa_{\rm ep}$ and $\Omega$ need not coincide.",
"Module 1 §6":r"Module 1 derives the molecular transport coefficients needed here. Applying them to an accretion disc shows that ordinary collisional viscosity cannot move angular momentum on the observed timescale. This failure motivates an effective turbulent or magnetic stress.",
"Module 1's Proposition":r"Module 1 gives $\mu\simeq\rho v_{\rm th}\lambda/3$ for dynamic viscosity. Dividing by density gives the kinematic coefficient used in equation (3.1).",
"For the dwarf-nova row the":r"For the dwarf-nova model, $n=1.7524\times10^{17}\ \mathrm{cm^{-3}}$ and $\ln\Lambda=5.0355$. The Coulomb mean free path is $2.6770\times10^{-4}$ cm, only $1.17\times10^{-12}$ of a scale height. The gas is therefore securely collisional, and its ion thermal speed is $25.11\ \mathrm{km\,s^{-1}}$.",
"Their own footnote":r"Shakura and Sunyaev assume $\alpha$ constant with radius. They also note that the spectrum and surface temperature depend only weakly on its chosen value. Section 8 derives this independence, while §11 compares the observed values of $\alpha$.",
"The approximation $g_z":r"At two scale heights in the dwarf-nova model, $z/R=0.04570$. The linear approximation $g_z=\Omega^2z$ then exceeds the exact vertical gravity by only 0.3134 per cent. A Gaussian column places 95.45 per cent of its mass within this height, so the thin-disc error is controlled by $(H/R)^2$.",
"Module 3 §11":r"Equation (7.2) quantifies rotational flattening. Radially, a Keplerian disc is supported mainly by rotation; vertically, it is supported by pressure. Their ratio gives $H/R=c_T/v_K$. The fiducial dwarf-nova and protoplanetary discs have $H/R=0.02285$ and $0.044751$, respectively, far below the spherical value of order unity.",
"For the active-galactic-nucleus configuration —":r"For the active-galactic-nucleus example, take $M=10^8M_\odot$, $R_{\rm in}=6R_g=8.8598\times10^{13}$ cm, and $\dot M=0.2220M_\odot\,\mathrm{yr^{-1}}$. The rate is one tenth of Eddington for assumed radiative efficiency 0.1. These inputs determine the temperature profile below.",
"Half the binding":r"A Newtonian circular orbit has specific binding energy $GM/(2R)$ rather than $GM/R$. Half of the potential-energy release remains as orbital kinetic energy when matter reaches the inner boundary. The disc radiates only the other half under the zero-torque assumption.",
"This book is Newtonian":r"Near a black hole, relativistic efficiencies replace the Newtonian estimate. For a Schwarzschild hole, the innermost stable orbit is $6R_g$ and the efficiency is $1-\sqrt{8/9}=0.057191$. For an extreme prograde Kerr orbit at $R_g$, it is $1-1/\sqrt3=0.422650$.",
"The Newtonian efficiency":r"The figure compares $\eta=R_g/(2R_{\rm in})$ with quoted and relativistic efficiencies. At $6R_g$, Newtonian theory gives $1/12=0.08333$, while Schwarzschild relativity gives $0.05719$. At $R_g$, extreme Kerr gives $0.42265$. The plotted differences show the cost of applying Newtonian binding energy near the innermost stable orbit.",
"Because a Keplerian":r"For a Keplerian disc, $\kappa_{\rm ep}=\Omega$. Substituting $\Sigma$ from the steady-disc relation and $\nu=\alpha c_TH$ with $H=c_T/\Omega$ eliminates the explicit radius from the Toomre parameter.",
"On the protoplanetary":r"The fiducial protoplanetary disc has $Q=126.56$ with the gas coefficient and $118.34$ with Toomre’s stellar coefficient. The 7 per cent difference does not affect stability. Reaching $Q=1$ at the same sound speed and rotation would require $\Sigma=1265.6\ \mathrm{g\,cm^{-2}}$, compared with the adopted 10.",
"The thin $\\alpha$":r"The thin $\alpha$-disc converts angular-momentum loss into inward mass flow and outward energy release through a one-parameter stress closure. It predicts a useful radial temperature profile that does not depend on $\alpha$. Its principal omissions concern the origin and variability of the stress, relativistic inner boundaries, self-gravity, winds, and vertical structure.",
"Read as a whole":r"The two most consequential assumptions are a constant $\alpha$ and a zero-torque inner boundary. Neither follows from the vertically averaged conservation laws. Observed $\alpha$ varies between systems, and simulations often give $\alpha\le0.02$ where observations require $0.1$–$0.4$. That discrepancy marks the central unresolved closure problem.",
}
for p,h in R.items():rep(p,h)
P.write_text(str(s),encoding="utf8");print("rewrote",len(R),"blocks")

