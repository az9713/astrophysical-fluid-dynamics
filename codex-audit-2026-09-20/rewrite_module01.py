from pathlib import Path
from bs4 import BeautifulSoup

PATH = Path(__file__).parent / "textbook-edition-20-rule" / "module01.html"


def set_html(tag, html):
    fragment = BeautifulSoup(html, "html.parser")
    tag.clear()
    for child in list(fragment.contents):
        tag.append(child)


soup = BeautifulSoup(PATH.read_text(encoding="utf-8"), "html.parser")

titles = {
    "origin": "1. Why can an extremely dilute gas behave as a fluid?",
    "claim": "2. What a fluid description retains",
    "lte": "3. Collisions and local thermodynamic equilibrium",
    "neutral": "4. Mean free path in a neutral gas",
    "phot": "4.1 Worked example: the solar photosphere",
    "coulomb": "5. Mean free path in an ionised gas",
    "b90": "5.1 Coulomb deflection and the impact parameter",
    "lnlam": "5.2 The origin of the Coulomb logarithm",
    "lamC": "5.3 The Coulomb mean free path",
    "knudsen": "6. The Knudsen number and the fluid hierarchy",
    "census": "7. Astrophysical regimes",
    "fails": "8. Failure of the collisional fluid approximation",
    "solarwind": "8.1 Magnetic confinement in the solar wind",
    "nostars": "8.2 Collisionless stars and dark matter",
    "limits": "9. Scope and limitations",
    "lab": "9.1 Reproducing the numerical results",
}
for ident, title in titles.items():
    node = soup.find(id=ident)
    if node is None:
        raise RuntimeError(f"missing heading #{ident}")
    node.string = title


def replace(prefix, html):
    matches = [x for x in soup.find_all(["p", "li", "figcaption"]) if x.get_text(" ", strip=True).startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"{prefix!r} matched {len(matches)} blocks")
    set_html(matches[0], html)


R = {
    "The continuum condition": r"A quantitative test of the continuum approximation: mean free paths, Knudsen numbers, and the astrophysical systems for which ordinary fluid dynamics fails.",
    "Start with the complete description": r"A kinetic description resolves the full particle velocity distribution. A fluid description retains only a small set of velocity moments, such as density, bulk velocity, and thermal energy. We begin with the kinetic equation to identify the information lost in this reduction.",
    "The saving is enormous": r"Replacing a six-dimensional distribution function by five fields of three spatial variables greatly reduces the computational problem. This reduction is justified only when collisions keep the local velocity distribution close to a Maxwellian.",
    "Boltzmann's H": r"Boltzmann’s H-theorem identifies the Maxwellian in equation (2.2) as the unique equilibrium of the collision operator. Here the central issue is the relaxation rate. A local Maxwellian forms only when collisions act faster than macroscopic transport changes the gas.",
    "where $\\tau$ is": r"Here $\tau$ is the mean time between collisions experienced by one particle. The BGK model replaces the full collision integral by exponential relaxation toward the local Maxwellian. Although it cannot reproduce every kinetic detail, it retains the timescale needed to derive the continuum criterion.",
    "Proposition 1 is": r"Proposition 1 gives the physical origin of the continuum criterion. A particle arriving at a point last collided roughly one mean free path away. If macroscopic conditions vary substantially across that distance, particles arriving from different directions carry incompatible local distributions. Their mixture is not the Maxwellian associated with the arrival point. When $\lambda/L\ll1$, those source regions are effectively identical, and local thermodynamic equilibrium becomes an accurate approximation.",
    "Everything now reduces": r"The remaining task is to calculate the mean free path $\lambda$. Neutral particles collide through short-range interactions, whereas charged particles accumulate many long-range Coulomb deflections. The two cases therefore require different calculations.",
    "The photosphere is": r"The solar photosphere is conventionally located near visible optical depth $\tau=2/3$. Its gas pressure is approximately $1.2\times10^{5}\ \mathrm{dyn\,cm^{-2}}$, and its temperature is close to $T_{\rm eff}=5772$ K. In a grey Eddington atmosphere, $T^4(\tau)=\tfrac34T_{\rm eff}^4(\tau+\tfrac23)$, so $T=T_{\rm eff}$ at this optical depth. The ideal-gas law then determines the particle density without an independent density measurement.",
    "The length $b_{90}$ is": r"The scale $b_{90}$ is the impact parameter that produces a $90^\circ$ deflection. For identical particles with charge $e$ and mass $m$, the reduced mass is $\mu=m/2$. Two independent Maxwellian velocities satisfy $\langle v_{\rm rel}^2\rangle=2\langle v^2\rangle=6k_BT/m$. Consequently, $\mu\langle v_{\rm rel}^2\rangle=3k_BT$.",
    "One step there deserves": r"Equation (5.1) defines $b_{90}$ for a pair with a specified relative speed. Equation (5.2) substitutes the distribution’s mean-square relative speed. Because $b_{90}\propto v_{\rm rel}^{-2}$, this substitution is an approximation: the average of a reciprocal is not the reciprocal of an average. It preserves the scaling but misses the properly averaged numerical coefficient by a factor of $2.05$. Section 5.3 therefore uses the coefficient obtained from the full velocity average.",
    "A test charge": r"A test charge passes a field charge at impact parameter $b$ and is deflected through $\theta\approx2b_{90}/b$. Equal logarithmic intervals in $b$ make equal contributions between the lower cutoff $b_{\min}$ and Debye length $\lambda_D$. Their ratio defines the Coulomb logarithm. For intracluster electrons, the quantum cutoff exceeds $b_{90}$ by a factor of 31. The drawing is schematic: the physical ratio $\lambda_D/b_{\min}$ is $1.3\times10^{16}$.",
    "The integral is": r"The integral equals $\ln(b_{\max}/b_{\min})$. Every logarithmic interval of impact parameter contributes equally because the increasing number of distant encounters offsets their decreasing strength. The Coulomb collision rate therefore depends on many weak deflections rather than only on rare close encounters. Screening and quantum or large-angle physics supply the two cutoffs.",
    "The mass-independence": r"At fixed temperature and charge, the Coulomb mean free path is independent of particle mass because $b_{90}=e^2/(3k_BT)$. Electrons and protons therefore travel comparable distances between cumulative large-angle deflections. Electrons traverse that distance $\sqrt{m_p/m_e}=42.9$ times faster, so their collision time is shorter by the same factor. For ions of charge $Ze$, the mean free path decreases as $Z^{-4}$.",
    "The second half of that definition": r"The Knudsen number depends on both the gas and the macroscopic scale being studied. The photospheric mean free path is about $66\,\mu$m. Relative to the solar radius, $\mathrm{Kn}=9.6\times10^{-14}$; relative to a 150 km pressure scale height, $\mathrm{Kn}=4.4\times10^{-10}$. Both values securely justify a continuum description, although they differ by more than four orders of magnitude.",
    "The thresholds in the last column": r"The regime boundaries in the table are accuracy conventions rather than measured constants. Truncating the Chapman–Enskog series after order $\mathrm{Kn}^k$ leaves errors of order $\mathrm{Kn}^{k+1}$. Requiring roughly one per cent accuracy suggests $\mathrm{Kn}\lesssim10^{-2}$ for Euler flow and $\mathrm{Kn}\lesssim10^{-1}$ for Navier–Stokes flow. Rarefied-gas engineering uses similar boundaries and identifies a free-molecular regime above $\mathrm{Kn}\sim10$.",
    "Two consequences are": r"Two consequences follow from the transport scalings. First, dilute-gas viscosity is nearly independent of density because a lower particle density is offset by a longer mean free path. Second, plasma thermal conductivity grows approximately as $T^{5/2}$. Raising the temperature from $10^6$ to $10^8$ K increases $\kappa$ by about $8.8\times10^4$ after the Coulomb logarithm is included. Efficient parallel conduction can therefore erase temperature gradients in hot cluster plasma unless magnetic geometry or kinetic effects suppresses the effective transport.",
    "The same particle, seen": r"The same particle behaves differently along and across the magnetic field. Across $\mathbf B$, its orbit is confined to a gyroradius of 93 km at 1 au. Along $\mathbf B$, it can stream for a mean free path of 1.9 au, or $3.1\times10^6$ gyroradii. Magnetic confinement therefore produces strongly anisotropic transport rather than restoring an ordinary isotropic fluid.",
    "The $N/\\ln N$ carries": r"The factor $N/\ln N$ has the same mathematical origin as the Coulomb logarithm. Gravity is long-ranged, so the cumulative effect of many weak encounters dominates. Integrating those encounters over impact parameter produces the logarithm.",
    "Dark matter. Here": r"For dark matter, the interaction cross-section is constrained observationally rather than assumed. In the Bullet Cluster, X-ray gas shocks and lags behind, while galaxies and lensing mass continue through the collision. Randall et al. (2008) infer $\sigma/m\lt0.7\ \mathrm{cm^2\,g^{-1}}$ at 68 per cent confidence. A $10^{15}\,M_\odot$ cluster within 1 Mpc has mean density $1.6\times10^{-26}\ \mathrm{g\,cm^{-3}}$, which we round to $2\times10^{-26}\ \mathrm{g\,cm^{-3}}$. Since $\lambda=1/[\rho(\sigma/m)]$, even the maximum allowed cross-section implies a very large mean free path.",
    "so $\\mathrm{Kn}\\ge23$": r"The mean-density estimate gives $\mathrm{Kn}\ge23$ on a 1 Mpc scale. A core density of $10^{-25}\ \mathrm{g\,cm^{-3}}$ instead gives $\lambda\ge4.6$ Mpc and $\mathrm{Kn}\ge4.6$. The core value is smaller but remains above unity where interactions would be most likely. The observations therefore support a collisionless description on cluster scales.",
    "The first row deserves": r"Electron and proton temperatures need not equilibrate rapidly in intracluster plasma. Sarazin (1988) gives electron–electron, proton–proton, and proton–electron equilibration times in the ratio $1:43:1870$. The latter two factors are close to $\sqrt{m_p/m_e}$ and $m_p/m_e$. At $T\sim10^8$ K and $n_e\sim10^{-3}\ \mathrm{cm^{-3}}$, proton–electron equilibration takes about $6\times10^8$ yr. This is comparable to a cluster-merger timescale, so post-shock ions can remain hotter than the electrons measured by X-ray spectroscopy.",
    "If $\\lambda_D$ were infinite": r"Without Debye screening, the integral in equation (5.3) would diverge at large impact parameter and predict an unphysical zero mean free path. The collective plasma response makes the collision rate finite. Consequently, $\ln\Lambda$ cannot be obtained from two-body Rutherford scattering alone.",
    "It measures a Knudsen number": r"The Bullet Cluster constrains a Knudsen number, or equivalently a lower bound on the dark-matter mean free path. Gas with $\mathrm{Kn}\ll1$ shocks and loses bulk kinetic energy, so it remains between the subclusters. Galaxies and lensing mass with $\mathrm{Kn}\gg1$ pass through with little interaction. Their spatial separation yields $\sigma/m\lt0.7\ \mathrm{cm^2\,g^{-1}}$, corresponding to $\lambda\ge23$ Mpc and $\mathrm{Kn}\ge23$ for the adopted mean density.",
    "A cool core has": r"A cool core has relatively high density, low temperature, and small size; cluster outskirts have the opposite properties. The §7 values give $t_{\rm cond}/t_s=3/\mathrm{Kn}\approx1.4\times10^3$ in the core and $27$ in the outskirts. Conduction is therefore negligible over a core sound-crossing time but approaches dynamical relevance in the outskirts.",
    "Two readings. First": r"This illustrative radial model makes $\mathrm{Kn}$ decrease outward and places the crossing near 1.5 au. That behaviour follows from choosing the system scale $L=r$, which grows faster than the mean free path decreases. A fixed structure, such as a 0.01 au interaction region, remains collisionless throughout. The shallow $-5/3$ exponent also makes the crossing radius insensitive to moderate changes in the 1 au mean free path. The precise radius is model-dependent because the observed wind cools more slowly than the assumed adiabatic law.",
    "Since real cool cores": r"Observed cool-core temperatures of $2$–$4\times10^7$ K satisfy this bound, so unsuppressed conduction is slow compared with sound crossing. The cooling-flow problem requires a different comparison: conduction must be tested against the radiative cooling time, which is much longer than $t_s$ in a dense core. The physical conclusion therefore depends on the chosen macroscopic timescale.",
    "The H -theorem": r"The H-theorem is invoked in §3 but not proved here. Boltzmann (1872) introduced the result. Chapman and Cowling, <i>The Mathematical Theory of Non-uniform Gases</i>, 3rd ed. (1970), provide a modern treatment and the standard development of the Chapman–Enskog expansion used in §6.",
    "Values used as inputs": r"Input values are identified where they enter the calculation. These include the laboratory vacuum pressures in §1, the photospheric pressure and neutral-hydrogen cross-section in §4.1, and the representative solar-wind parameters in §7. The cluster density in equation (8.4) is derived directly from $10^{15}\,M_\odot$ within 1 Mpc.",
}

for prefix, html in R.items():
    replace(prefix, html)

PATH.write_text(str(soup), encoding="utf-8")
print(f"rewrote {len(R)} complete prose blocks and {len(titles)} headings")
