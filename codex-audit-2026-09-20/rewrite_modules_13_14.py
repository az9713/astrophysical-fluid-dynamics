"""Build the separate Codex textbook editions of Modules 13 and 14."""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "afd"
DEST = ROOT / "textbook-edition-20-rule"


def replace_inner(tag, html: str) -> None:
    fragment = BeautifulSoup(html, "html.parser")
    tag.clear()
    for child in list(fragment.contents):
        tag.append(child)


def blocks(soup):
    result = []
    section = ""
    for tag in soup.body.find_all(recursive=False):
        if tag.name == "h2":
            section = tag.get("id", "")
        if section in {"problems", "notation", "sources"}:
            continue
        if tag.name not in {"p", "div"}:
            continue
        if tag.name == "div" and "toc" in tag.get("class", []):
            continue
        if len(tag.get_text(" ", strip=True)) > 60:
            result.append(tag)
    return result


R13 = {
    0: r"Radiation transports energy and momentum through an astrophysical fluid. We derive radiative diffusion, examine the solar photosphere, and find the luminosity at which radiative force balances gravity.",
    1: r"Radiation changes a fluid in two ways. It carries heat down a temperature gradient and transfers momentum when it is absorbed or scattered. The first effect modifies stellar oscillations; the second can oppose gravity near a luminous source. We begin with the angular distribution of light, then derive the transfer and diffusion laws needed to quantify both effects.",
    2: r"The <a class='secref' href='#eddington'>Eddington limit in §9</a> follows from a simple force balance. Its opacity and flux must first be defined carefully. The <a class='secref' href='#anchor'>solar-atmosphere example in §6</a> then shows why electron scattering cannot be assumed to describe every gas.",
    3: r"The photospheric opacity used below comes from an ATLAS9 model atmosphere. We do not derive the atomic opacity of H⁻ here. That distinction matters: a model opacity is a physical input, whereas the column-mean calculation in §6 is an inference from it.",
    4: r"A photon of energy $E$ carries momentum $E/c$. A beam with energy flux $F$ therefore delivers momentum flux $F/c$ to a perfectly absorbing surface. In a star, radiation arrives from many directions, so a single beam is insufficient. We describe its directional distribution with the specific intensity.",
    6: r"We denote the second angular moment by $P_\nu$, emphasizing its interpretation as radiation pressure. The notation also avoids confusion with the polytropic constant $K$ used in <a href='module03.html#whypoly'>Module 3</a>.",
    9: r"The radiation constant is $a_{\rm rad}=7.565733\times10^{-15}\ \mathrm{erg\,cm^{-3}\,K^{-4}}$. The factor $1/3$ in isotropic radiation pressure is geometric. A beam directed along $z$, by contrast, has $P_\nu=u_\nu$ because every photon carries its full axial momentum across the surface. A uniformly illuminated hemisphere still gives $P_\nu=u_\nu/3$, although its net flux is nonzero. These limits show why pressure and flux are distinct moments.",
    10: r"Here $\nu$ denotes photon frequency, measured in hertz. Earlier modules also use $\nu$ for kinematic viscosity, but viscosity does not enter this chapter. Subscripts such as $I_\nu$ and $\kappa_\nu$ always refer to frequency.",
    12: r"We write $\kappa_\nu$ for monochromatic opacity, $\kappa_{\rm R}$ for its Rosseland mean, $\kappa_{\rm es}$ for electron scattering, and $\kappa_{\rm F}$ for a flux mean. Keeping these quantities distinct prevents a column-averaged opacity from being mistaken for a local scattering coefficient.",
    15: r"For a constant source function, equation (2.2) becomes $I_\nu=I_\nu(0)e^{-\tau_\nu}+S_\nu(1-e^{-\tau_\nu})$. An optically thin slab barely changes the incident ray. An optically thick slab instead emits with its own source function, losing memory of the incident intensity. When scattering contributes to $S_\nu$, the source depends on the radiation field itself, and the formal solution becomes an integral equation.",
    17: r"Optical depth measures the expected number of interactions along a path. With no emission, equation (2.2) gives an unscattered survival fraction $e^{-\tau}$. The mean distance to the next interaction is the local mean free path $\lambda_{\rm ph}$. In the ATLAS9 solar atmosphere, that path is about $84.2$ km at Rosseland optical depth $2/3$.",
    20: r"A photon must take many random steps to cross an optically thick layer. For thickness $L=\tau\lambda_{\rm ph}$, the typical number is $N\sim\tau^2$. Its total path is then $N\lambda_{\rm ph}\sim\tau L$, much longer than a straight crossing. This delay leads naturally to a diffusion description in the stellar interior.",
    21: r"Deep inside a star, the radiation field is nearly isotropic. A temperature gradient introduces a small anisotropy, allowing energy to flow from hotter layers to cooler ones. This is the diffusion limit of the transfer equation. It requires a photon mean free path short compared with the temperature scale length.",
    25: r"An isothermal region gives $F=0$ in equation (4.2), whatever its opacity. A temperature gradient alone does not guarantee that diffusion applies, however. Near a free surface the radiation field becomes strongly one-sided, and the optically thick closure fails. Section 5 treats that boundary with a grey-atmosphere approximation.",
    28: r"The factor $1/3$ in the photon diffusivity comes from averaging directions in an almost isotropic field. The gas thermal diffusivity $\chi$ is different: it divides radiative conductivity by the gas heat capacity per unit volume. We therefore use $D$ for photon energy diffusion and $\chi$ for the rate at which gas-temperature perturbations relax.",
    29: r"The gas diffusivity $\chi$ enters the adiabatic-wave criterion introduced in <a href='module04.html'>Module 4</a>. Section 7 evaluates that criterion for two layers of a solar model atmosphere.",
    30: r"Radiative diffusion cannot describe the stellar surface, where photons escape and the field is no longer nearly isotropic. A grey atmosphere connects the deep diffusive region to the surface by taking opacity to be independent of frequency. Its familiar temperature law also requires radiative equilibrium and a boundary closure.",
    33: r"Far below the surface, the grey temperature law approaches the diffusion result. Differentiating equation (5.1) gives the same constant flux as equation (4.2). At the surface, the constant $2/3$ comes from the Eddington boundary approximation, not from local diffusion. The two regimes meet only within the assumptions of the grey model.",
    34: r"A more accurate grey-transfer solution replaces the constant $2/3$ with a depth-dependent Hopf function. Its values are $0.57730$ at the surface and $0.68876$ at $\tau_{\rm R}=2/3$ in the calculation used here. The resulting temperature change is small for this comparison, but it exposes the boundary approximation in equation (5.1).",
    35: r"The ATLAS9 comparison uses $T_{\rm eff}=5777$ K because that is the effective temperature of the tabulated atmosphere. Elsewhere this book uses the IAU nominal value $5772$ K. Keeping the model's own temperature avoids introducing a mismatch unrelated to the grey approximation.",
    37: r"Figure 1 compares the grey temperature profile with seven levels from the ATLAS9 atmosphere. The residual panel shows where the grey assumptions account for most of the difference.",
    38: r"At $\tau_{\rm R}=2/3$, the grey law gives $T=T_{\rm eff}=5777$ K by construction. ATLAS9 gives $5910.1$ K there, a difference of $133.1$ K. The grey profile also differs at other depths, with the largest tabulated temperature difference near the surface. This comparison measures the combined effects of non-grey opacity, convection, and the approximate boundary condition; it does not isolate any one cause.",
    39: r"The ATLAS9 atmosphere is a numerical model, not an observation. The comparison therefore tests how well a simple grey atmosphere reproduces a more detailed model. Its seven depths do not establish an observational error bar.",
    40: r"A photospheric scale-height estimate can constrain the mean opacity of a column. <a href='module06.html'>Module 6</a> used $H=142.9$ km and $\rho=3.0631\times10^{-7}\ \mathrm{g\,cm^{-3}}$ at a representative solar layer. Combined with optical depth $2/3$, these numbers imply a column-averaged Rosseland opacity. They do not determine the opacity at the layer's base.",
    41: r"Let $m$ be the mass per unit area above a layer. The optical depth is $\tau_{\rm R}=\int_0^m\kappa_{\rm R}\,\mathrm{d}m'$. Thus $\tau_{\rm R}/m$ is a column mean even when local opacity changes with depth. Approximating $m$ by $\rho H$ yields equation (6.1), whose meaning remains a column average.",
    42: r"The estimate gives $\bar\kappa_{\rm R}=0.15231\ \mathrm{cm^2\,g^{-1}}$ from the rounded $\rho H$ values. Using hydrostatic $m=P/g$ gives $0.15233\ \mathrm{cm^2\,g^{-1}}$. Their small difference is rounding. Neither calculation measures the local $\kappa_{\rm R}$ at optical depth $2/3$.",
    43: r"Castelli's ATLAS9 solar atmosphere tabulates pressure, column mass, and local Rosseland opacity as functions of depth. Integrating the model opacity yields a column mean at each comparison layer. We compare like with like: the value inferred from $\rho H$ against that integrated mean, and separately against the local opacity to show why the distinction matters.",
    45: r"No tolerance was specified before this opacity comparison. The ratios in CHECK 2 therefore describe agreement with the ATLAS9 column means; they are not a pass or fail criterion. Most of the difference at $\tau_{\rm R}=2/3$ follows from the pressure adopted in Module 6, which exceeds the ATLAS9 pressure at that layer.",
    46: r"Equation (6.1) averages opacity over the material above the chosen layer. In ATLAS9, local $\kappa_{\rm R}$ rises from $0.0424$ at $\tau_{\rm R}=0.01$ to $0.4447\ \mathrm{cm^2\,g^{-1}}$ at $2/3$. A mean over that column cannot be substituted for the local coefficient at its base. Figure 2 shows the difference across the atmosphere.",
    47: r"ATLAS9 supplies a model atmosphere with specified abundances, opacities, and convection. Its output is useful for testing a simplified calculation, but it is not a direct measurement of the Sun's opacity. The comparison should be read at the level of those model assumptions.",
    48: r"Free electrons scatter low-energy photons with the Thomson cross-section $\sigma_{\rm T}$. For fully ionised hydrogen–helium gas, this gives the electron-scattering opacity in equation (6.2). The approximation requires free, non-relativistic electrons and photon energies $h\nu\ll m_{\rm e}c^2$. At higher photon energies the Klein–Nishina cross-section depends on energy and falls below $\sigma_{\rm T}$.",
    49: r"For pure ionised hydrogen, equation (6.2) gives $\kappa_{\rm es}=0.39773\ \mathrm{cm^2\,g^{-1}}$. With the adopted present solar-surface hydrogen fraction $X=0.7583$, it gives $0.34966\ \mathrm{cm^2\,g^{-1}}$. These values describe fully ionised gas in the Thomson regime, not the largely neutral photosphere.",
    50: r"Solar photospheric hydrogen is mostly neutral at these temperatures, so scattering by free electrons is weak. The ATLAS9 electron density at $\tau_{\rm R}=2/3$ is far below the density implied by complete ionisation. Its Rosseland opacity is instead controlled largely by atomic and ionic processes, including H⁻. Comparing the local Rosseland value with the fully ionised electron-scattering formula would mix different physical states.",
    51: r"The lower bound $\kappa_{\rm R}\ge\kappa_{\rm es}$ applies only if the gas is fully ionised and the scattering opacity stays in the Thomson limit throughout the column. Neither condition holds throughout the solar photosphere, so that bound must not be applied to the ATLAS9 column.",
}

R14 = {
    0: r"Numerical methods approximate fluid equations on a finite grid or with particles. This chapter derives their stability and truncation limits, then tests both approaches against shock-tube and blast-wave solutions.",
    1: r"A simulation result depends on the equations, the discretisation, and the resolution. A method may conserve mass and energy while smearing a contact or shock. We first ask what conservation guarantees, then examine how a finite time step and grid spacing alter the computed solution. The Sod and Sedov problems provide quantitative tests.",
    2: r"The chapter also distinguishes calculations from observations. Its final census identifies results in earlier modules that came from simulations, numerical models, or numerical integration. That provenance changes what a comparison can establish.",
    3: r"The examples here use one-dimensional grid and particle methods, with a spherical-grid Sedov calculation. They illustrate stability, convergence, and resolution requirements. Higher-order reconstruction, multidimensional flow, gravity, magnetic fields, and radiation require additional numerical techniques.",
    4: r"The Euler equations conserve mass, momentum, and energy. A finite-volume method applies those balances to cells rather than point values. Its update is determined by fluxes through cell faces, so neighbouring cells exchange equal and opposite amounts. This construction matters most when the solution contains a shock.",
    8: r"Conservation is necessary for a numerical shock to approach the correct weak solution. It does not guarantee convergence, stability, or small error on a finite grid. The Lax–Wendroff theorem identifies the weak solution if a consistent conservative scheme converges under its stated conditions; it does not prove that a chosen scheme will converge.",
    9: r"""Constant-speed advection isolates the time-step question. Its exact solution translates the initial profile by $at$, where $a>0$. The upwind and centred schemes below use the same neighbouring cells but behave differently. The upwind update is
$$ u_i^{n+1} = u_i^n - C\,(u_i^n - u_{i-1}^n), \qquad C = \frac{a\Delta t}{\Delta x}. \tag{2.1}$$
Comparing the methods separates the necessary domain-of-dependence condition from stability of a particular update.""",
    12: r"Courant, Friedrichs, and Lewy showed that the numerical domain of dependence must contain the physical one for convergence. For the local stencil in Proposition 2 this requires $a\Delta t/\Delta x\le1$. The condition is necessary, not sufficient: a scheme may satisfy it and still amplify numerical disturbances.",
    15: r"At $C=1$, upwinding shifts every value exactly one cell per step and reproduces constant-speed advection on the grid. At $C=0$, no time elapses. For $0<C<1$, the scheme is stable but spreads a sharp profile. The centred FTCS scheme instead amplifies nonconstant Fourier modes for every positive $C$.",
    16: r"<b>CHECK 1 — stability in a numerical example.</b> For a sawtooth mode, the upwind amplification factor is $|1-2C|$: it is $0.8$ at $C=0.9$ and $1.2$ at $C=1.1$. A sampled Gaussian at $C=1.1$ exceeds amplitude $10^3$ after 210 steps. These runs illustrate the stability calculation in Proposition 3. They do not provide an independent empirical test of the scheme.",
    17: r"An explicit compressible-flow code must resolve its fastest characteristic speed, approximately $|u|+c_{\rm s}$. Module 10 estimated a step from the flow speed $U$ alone. For its laboratory-air example, the compressible Courant step is smaller by a factor $1+1/M=35.01$, where $M=U/c_{\rm s}=0.0294$. In its supersonic cloud example the factor is only $1.0924$. This distinction changes computational cost without changing the physical Reynolds number.",
    18: r"Stability does not mean that a grid reproduces the original differential equation exactly. A Taylor expansion of the upwind update reveals an additional diffusion term. This modified equation explains why a stable first-order scheme broadens smooth profiles and discontinuities.",
    21: r"At $C=1$, the numerical diffusivity vanishes because the update is an exact cell shift. As $C$ decreases, the diffusion coefficient $a\Delta x(1-C)/2$ increases, although the physical time advanced per step also decreases. The coefficient describes the leading error for a smooth solution; the next proposition gives an exact variance result for the discrete update.",
    24: r"""A Gaussian advected for 200 steps shows the predicted increase in variance at $C=0.25$, $0.5$, and $0.9$. The measured-to-predicted ratios are $1.000000000$ to the displayed precision. This agreement checks the implementation of the discrete update. For $N$ cells across length $L$, the effective numerical Reynolds number is
$$ \mathrm{Re}_{\rm num} \;=\; \frac{UL}{D_{\rm num}} \;=\; \frac{2N}{1 - C}. \tag{3.3}$$
It depends on $N$ and $C$ rather than on the simulated fluid. At $N=1024$, it is $4096$ for $C=0.5$ and $2.048\times10^4$ for $C=0.9$.""",
    25: r"A scalar has one propagation speed, so upwinding selects a single side of each face. The Euler equations have three characteristic speeds: $u-c_{\rm s}$, $u$, and $u+c_{\rm s}$. A face can therefore receive information from both directions. A Riemann solver determines the flux from the local left and right states.",
    30: r"Identical left and right states remain unchanged: the Riemann solution has $P^*=P_{\rm L}$ and $u^*=u_{\rm L}$. When the star pressure approaches zero, the two rarefactions can separate and create a vacuum; equation (4.2) states the corresponding limit. These cases check the solver beyond the standard shock-tube example.",
    31: r"The Sod shock tube starts from two stationary ideal gases separated by a diaphragm. With $\gamma=1.4$, the left state has $(\rho,P)=(1,1)$ and the right state $(0.125,0.1)$. Removing the diaphragm produces a left-moving rarefaction, a contact, and a right-moving shock. The exact Riemann solution provides a reference for measuring numerical error.",
    33: r"We use the exact solution to measure density error separately in the fan, at the contact, and at the shock. First-order Godunov runs cover $N=100$ through $6400$ cells with Courant coefficient $0.9$. These regions converge at different rates because their solution profiles have different regularity.",
    36: r"The fan has a measured density-error order of $0.752$ over the sampled resolutions. Its head and tail are continuous corners where derivatives jump, so smooth-solution truncation estimates need not describe them. Equation (5.1) predicts only the contact contribution. Its remaining discrepancy with the measured contact error decreases as resolution rises.",
    37: r"The Sedov–Taylor blast provides a second test with a known shock trajectory. For $\gamma=1.4$, $\rho_0=1$, and explosion energy $E=0.851072$, the similarity solution puts the shock at $r=1$ when $t=1$. We compare that radius and the strong-shock density jump with a spherical Godunov calculation.",
    38: r"The spherical update uses cell volumes $(r_+^3-r_-^3)/3$ per steradian and face areas $r^2$. A geometric pressure source preserves a uniform-pressure state. Energy begins in the innermost cell, and the ambient pressure is $10^{-6}$. The grid spans $0\le r\le1.2$ with 100, 200, or 400 cells at Courant coefficient $0.5$.",
    41: r"A grid fixes spatial cells and moves fluid through them. Smoothed particle hydrodynamics (SPH) instead follows particles of fixed mass. Fields are reconstructed from neighbouring particles using a smoothing kernel. The method follows a collapsing concentration without adding grid cells, but fixed particle mass still limits the smallest resolved gravitating mass.",
    43: r"The smoothing length $h$ sets the kernel's spatial support. It differs from the mixing-layer width $h$ used in Module 8. With $h=1.2\Delta x$, the chosen cubic-spline kernel extends $2.4$ particle spacings to either side.",
    47: r"The Sod contact tests how the particle method handles a jump in density at nearly uniform pressure. Equal-mass particles are eight times farther apart on the low-density side. We run 200, 400, and 800 left-side particles per unit length, then compare pressure near the moving contact at $t=0.2$ with the exact $P^*=0.303130$.",
    51: r"Gravity introduces a physical instability scale. Module 5 derived the Jeans length $\lambda_{\rm J}=(\pi c_{\rm s}^2/G\rho_0)^{1/2}$: perturbations longer than this scale can collapse. If a numerical grid represents that length with too few cells, it may produce fragmentation driven by discretisation rather than by the fluid equations.",
    56: r"Resolving turbulence and resolving a contact impose different computational costs. The first depends on the smallest dissipative scale represented by the method. The second depends on how rapidly error decreases as a discontinuity is refined. Both estimates require a specified numerical representation and accuracy criterion.",
    59: r"A number produced by a computer need not be a simulation result. We distinguish hydrodynamic simulations, tabulated numerical models, and numerical integration of reduced equations. The table classifies representative inputs and comparisons from Modules 1–13 by that origin. Each category answers a different evidential question.",
    60: r"Some results used throughout the book have analytic forms, including the shock jump conditions, the Sedov exponent $2/5$, and the Eddington force balance. Numerical quadrature of a reduced ordinary differential equation is another category. Its integration error can be controlled independently, whereas errors in a full simulation or atmosphere model depend on its physical and numerical assumptions.",
    61: r"Several earlier pages describe numerical-model or simulation outputs as measurements. The following table identifies those cases and gives the appropriate evidence category. It is an editorial provenance record, separate from the derivations in this chapter.",
    62: r"A match to a simulation shows agreement between two calculations. A match to an observation tests a prediction against data from nature. The distinction does not make model comparisons useless, but it limits the inference drawn from them. Where a cited primary source was not checked, the classification remains provisional.",
    63: r"This chapter has derived the Courant condition, the leading numerical diffusivity of upwinding, and resolution tests for grid and particle methods. It has also shown how shocks and contacts can converge at different rates. Multidimensional turbulence, magnetic fields, radiation, and self-gravity require further numerical machinery beyond these examples.",
    64: r"The practical lesson is to state what was solved and how its error was measured. A conservative update supports the correct jump conditions if it converges, but conservation alone does not guarantee a resolved feature. Stability, convergence, and provenance must each be established for the quantity used in a physical claim.",
}

R13.update({
    71: r"""<b>Proposition 10 (the Eddington luminosity).</b> Let gas at radius $r$ have flux-mean opacity $\kappa_{\rm F}\equiv(1/F)\int\kappa_\nu F_\nu\,\mathrm d\nu$. Suppose a central mass $M$ radiates luminosity $L$ isotropically. Outward radiative acceleration is smaller than inward gravitational acceleration when
$$ L \;\lt\; L_{\rm Edd} \;\equiv\; \frac{4\pi GMc}{\kappa_{\rm F}}, \tag{9.1}$$
provided the stated opacity describes momentum transfer by the radiation field. For fully ionised hydrogen–helium gas in the low-energy Thomson limit, $\kappa_{\rm es}=\sigma_{\rm T}(1+X)/(2m_{\rm p})$. Taking electron scattering as the relevant flux-mean opacity gives, for pure hydrogen $(X=1)$,
$$ L_{\rm Edd} \;=\; \frac{4\pi GMm_{\rm p}c}{\sigma_{\rm T}}, \tag{9.2}$$
the form used in Module 9. Additional opacity lowers this force-balance luminosity. At photon energies approaching $m_ec^2$, the scattering cross-section decreases and the Thomson value cannot serve as a spectrum-independent floor.""",
    72: r"""At radius $r$, isotropic luminosity produces flux $F=L/(4\pi r^2)$. Gas with flux-mean momentum opacity $\kappa_{\rm F}$ experiences outward acceleration $\kappa_{\rm F}F/c$. Gravity supplies inward acceleration $GM/r^2$. The first is smaller when
$$ \frac{\kappa_{\rm F}L}{4\pi r^{2}c} \;\lt\; \frac{GM}{r^{2}}, $$
and cancelling $r^2$ gives equation (9.1). In the Thomson regime, scattering is effectively independent of photon frequency for free, non-relativistic electrons. If it dominates momentum coupling, $\kappa_{\rm F}=\kappa_{\rm es}$ and equation (6.2) gives the composition dependence. For $X=1$, equation (9.2) follows. Electrostatic coupling makes the electrons and ions respond together, so the force balance is written per unit mass of plasma. <span class='qed'>∎</span>""",
    5: r"""<b>Definition 1 (specific intensity and its moments).</b> The specific intensity $I_\nu(\mathbf r,\mathbf n,t)$ gives radiation energy per unit time, area normal to direction $\mathbf n$, solid angle, and frequency. Its units are $\mathrm{erg\,s^{-1}\,cm^{-2}\,sr^{-1}\,Hz^{-1}}$. Let $\theta$ be the angle from a chosen $z$ axis and $\mathrm d\Omega$ an element of solid angle. Three angular moments are
$$ u_\nu = \frac{1}{c}\oint I_\nu\,\mathrm{d}\Omega, \qquad F_\nu = \oint I_\nu\cos\theta\,\mathrm{d}\Omega, \qquad P_\nu = \frac{1}{c}\oint I_\nu\cos^{2}\theta\,\mathrm{d}\Omega, \tag{1.1}$$
They are energy density, axial energy flux, and axial momentum flux per unit frequency. The last is radiation pressure. Mean intensity is $J_\nu=(1/4\pi)\oint I_\nu\,\mathrm d\Omega=c u_\nu/(4\pi)$. Frequency-integrated quantities omit the subscript: $u_{\rm rad}=\int u_\nu\,\mathrm d\nu$, $F=\int F_\nu\,\mathrm d\nu$, and $P_{\rm rad}=\int P_\nu\,\mathrm d\nu$.""",
    23: r"""<b>Proposition 4 (radiative diffusion).</b> Consider a static, plane-parallel medium whose optical depth is large across a temperature scale height. Its frequency-integrated flux along $z$ is
$$ F \;=\; -\,\frac{c}{3\kappa_{\rm R}\rho}\,\frac{\mathrm{d}}{\mathrm{d}z}\!\left(a_{\rm rad}T^{4}\right) \;=\; -\,\frac{16\sigma_{\rm SB}T^{3}}{3\kappa_{\rm R}\rho}\,\frac{\mathrm{d}T}{\mathrm{d}z}. \tag{4.2}$$
The derivation uses the Eddington closure $P_\nu=u_\nu/3$. Proposition 1 proved that relation for an isotropic field; here it is an approximation for a nearly isotropic field.""",
    77: r"""<b>Proposition 11 (Eddington's opacity bound).</b> Consider a hydrostatic star of total luminosity $L$ and mass $M$. Suppose gas pressure $p_{\rm G}$ increases inward. Also suppose the interior ratio $L_r/M_r$ is at least its surface value $L/M$. The flux-mean opacity $k$ then obeys
$$ k \;\lt\; \frac{4\pi cGM}{L}. \tag{9.3}$$
For specified $L$ and $M$, this is a bound on opacity under the stated conditions.""",
    44: r"<b>CHECK 2 — a column-mean opacity comparison.</b> Equation (6.1) gives $\bar\kappa_{\rm R}=0.15231\ \mathrm{cm^2\,g^{-1}}$. The ATLAS9 column means are $0.15470$ at the layer with $T=5772$ K and $0.17487$ at $\tau_{\rm R}=2/3$. The model-to-estimate ratios are $1.0157$ and $1.1482$. No acceptance tolerance was fixed in advance, so these numbers describe agreement rather than validate a prediction. As a <em>local</em> opacity, equation (6.1) is low by factors of $2.36$–$2.92$. It must not be used as the coefficient at the base of the column.",
    52: r"<a href='module04.html'>Module 4</a> used an adiabatic approximation for solar acoustic waves. It identified $\omega\chi/c_{\rm s}^2\ll1$ as the condition for negligible thermal leakage, but did not evaluate the gas diffusivity $\chi$. We now estimate it from an ATLAS9 atmosphere. The estimate is informative near the photosphere, where radiative escape is important, yet the diffusion closure becomes unreliable at the free surface.",
    55: r"The dimensionless ratio compares thermal diffusion with wave motion. If $\omega\chi/c_{\rm s}^2\ll1$, a wave retains most of its compressional heat during an oscillation and behaves approximately adiabatically. A ratio near unity signals potentially important leakage. It does not by itself give a damping rate, because that requires a wave calculation with the radiative boundary condition.",
    56: r"We use $\nu_{\rm max}=3090\ \mu$Hz, $\omega=1.941504\times10^{-2}\ \mathrm{s^{-1}}$, and the photospheric sound speed $c_{\rm s}=8.0810\times10^5\ \mathrm{cm\,s^{-1}}$. Local temperature, density, and Rosseland opacity come from two ATLAS9 layers. Using local rather than column-mean opacity is essential because $\chi$ is a local transport coefficient.",
    58: r"Substituting the column mean $0.15231\ \mathrm{cm^2\,g^{-1}}$ for the local opacity would increase the estimated diffusivity and change the wave criterion. That substitution is physically inconsistent: the column mean averages over a range of densities and temperatures. The local ATLAS9 Rosseland opacity belongs in equation (4.3). Even with that correction, the calculation remains a diffusion estimate near an optically thin boundary.",
    59: r"These ratios suggest that radiative leakage cannot safely be ignored in the selected photospheric layers. They do not establish a mode damping rate or frequency shift. Quantitative results require non-adiabatic oscillation equations coupled to radiative transfer and a surface boundary condition. The local mean free path is shorter than the acoustic wavelength, but the outward optical depth at $\tau_{\rm R}=2/3$ is only $2/3$.",
    60: r"Radiation also alters the equation of state. A gas–radiation mixture has pressure from particles and photons, and both components respond to compression. Its adiabatic index therefore depends on the local fraction of total pressure supplied by gas.",
    61: r"Write $P=P_{\rm gas}+P_{\rm rad}$, with $P_{\rm gas}=\rho k_BT/(\mu m_u)$ and $P_{\rm rad}=a_{\rm rad}T^4/3$. Define $\beta=P_{\rm gas}/P$. This is the gas-pressure fraction used in <a href='module03.html'>Module 3</a>, not the plasma beta of Module 12. The next proposition computes the first adiabatic index at fixed entropy.",
    64: r"Equation (8.1) is Chandrasekhar's gas–radiation expression for $\Gamma_1$. It approaches $5/3$ when gas pressure dominates and $4/3$ when radiation pressure dominates. Those limits provide checks on the algebra. Between them, the local value depends on $\beta$ and cannot be replaced by a universal constant.",
    65: r"Two statements about $\Gamma_1$ must be kept separate. Equation (8.1) gives the local response of a gas–radiation mixture. A stellar model may also use an effective polytropic exponent to describe an extended structure. That structural parameter need not equal the local thermodynamic derivative. A claim about one cannot be transferred to the other without the model assumptions.",
    66: r"At the solar centre, the tabulated model used in Module 3 gives $1-\beta_c=6.1940\times10^{-4}$. Substitution into equation (8.1) therefore leaves $\Gamma_1$ close to the gas-dominated value $5/3$. Radiation pressure is present but is a small correction to the local compressional response in this example.",
    69: r"For $\mu=0.832$, equation (8.2) gives $\rho_{\rm eq}=2.5236\times10^{-5}\ \mathrm{g\,cm^{-3}}$ at $10^6$ K and $25.236\ \mathrm{g\,cm^{-3}}$ at $10^8$ K. The crossover density rises as $T^3$. Above it gas pressure dominates; below it radiation pressure dominates, within the assumed ideal-gas and equilibrium-radiation model.",
    70: r"The radiative force on surrounding gas competes with gravity. For a source of mass $M$ and isotropic luminosity $L$, both forces per unit mass decrease as $r^{-2}$. Their ratio is therefore independent of radius if the flux-mean opacity stays fixed. Setting that ratio to one defines the Eddington luminosity.",
    73: r"If opacity tends to zero, radiation transfers negligible momentum and the force-balance luminosity tends to infinity. Conversely, increasing opacity lowers the luminosity at which the outward radiative acceleration matches gravity. This is a local force balance, not a guarantee that gas above the limit escapes or that gas below it accretes steadily.",
    75: r"The familiar $m_p$ form of the Eddington luminosity assumes one free electron per proton, as in fully ionised pure hydrogen. A fully ionised hydrogen–helium mixture has fewer electrons per unit mass when $X<1$. Its electron-scattering opacity is $\sigma_{\rm T}(1+X)/(2m_p)$, so its Thomson-limit Eddington luminosity scales as $2/(1+X)$. The appropriate $X$ depends on the accreted gas; protosolar composition is an example, not a universal choice.",
    76: r"Eddington's original argument set an upper bound on opacity in a hydrostatic star with an inward-increasing gas pressure. It did not derive the electron-scattering luminosity used in modern accretion examples. The following proposition states his result in the notation used here, so its historical scope remains clear.",
    79: r"The historical bound depends on the radial distributions of luminosity and enclosed mass. It applies where gas pressure rises inward and the assumptions of hydrostatic balance hold. The simple Eddington luminosity in equation (9.1) instead compares gravity with radiative acceleration for a specified flux-mean opacity. The two arguments are related but not identical.",
    80: r"Equation (9.1) assumes spherical, isotropic radiation and a specified opacity. A disc or beam has a direction-dependent flux. Dust, bound–free absorption, and spectral changes can alter $\kappa_{\rm F}$; high-energy photons leave the Thomson regime. Gas dynamics, geometry, and time dependence can also permit inflow or outflow in situations where a spherical static balance would suggest otherwise.",
    81: r"For accretion at mass rate $\dot M$, define radiative efficiency by $L=\eta_{\rm rad}\dot Mc^2$. The Eddington accretion rate is then $\dot M_{\rm Edd}=L_{\rm Edd}/(\eta_{\rm rad}c^2)$. This convention depends on the chosen efficiency as well as the opacity. We retain $\eta_{\rm rad}=0.1$ for numerical comparisons with Module 9.",
    84: r"With $\eta_{\rm rad}=0.1$ and pure-hydrogen Thomson opacity, $M/\dot M_{\rm Edd}=4.5049\times10^7$ yr. The black-hole mass grows on a longer e-folding time because a fraction $\eta_{\rm rad}$ of the supplied rest mass leaves as radiation. Proposition 12 includes that factor explicitly.",
    85: r"A mass divided by a supply rate is a characteristic supply time, not automatically a black-hole doubling time. The Bondi example in Module 9 gives $M/\dot M=1.2297\times10^4$ yr for its outer supply estimate. Interpreting this as growth requires knowing what fraction reaches the horizon and what fraction of that mass-energy is radiated.",
    86: r"Changing $\eta_{\rm rad}$ changes the numerical value of $\dot M_{\rm Edd}$ by definition. Module 11 derives a Newtonian thin-disc efficiency of $1/12$ for one inner-boundary model. We retain the book's $0.1$ convention in the comparison table and state any alternative efficiency beside the number it changes.",
    87: r"The adopted $\eta_{\rm rad}=0.1$ keeps the earlier numerical Eddington accretion rates directly comparable. It is a normalization, not a measured efficiency for every black hole. Any physical application must specify the emitting flow and its energy losses.",
    88: r"The Bondi supply in Module 9 exceeds its adopted Eddington accretion rate by a factor of $3664$. This compares an outer, idealised supply calculation with an inner luminosity scale. It does not prove that a steady flow reaches the black hole at that rate. Feedback, angular momentum, and mass loss may change the inflow before it reaches the radiating region.",
    89: r"For Sagittarius A*, the adopted $2$–$10$ keV luminosity is $3.70\times10^{-12}L_{\rm Edd}$, while the Bondi supply estimate is $8.405\times10^{-5}\dot M_{\rm Edd}$. Their ratio, $4.40\times10^{-9}$, divides a band-limited luminosity by the rest-mass power of an outer supply rate. It is not the bolometric radiative efficiency of gas reaching the black hole. That inference would require a bolometric correction and a model for mass lost between the Bondi radius and the emitting flow. Module 11's disc example instead runs at $0.100002\dot M_{\rm Edd}$ under the adopted normalization.",
    90: r"The equality $P_{\rm rad}=P_{\rm gas}$ defines a line $\rho_{\rm eq}\propto T^3$ in the density–temperature plane. Figure 5 places the examples considered here relative to that line. It is a local pressure comparison, separate from the luminosity-based Eddington ratio.",
    91: r"The solar centre lies well above the equal-pressure density at its temperature, so gas pressure dominates there. Hotter or more dilute environments can approach radiation-pressure dominance. The plotted values depend on the adopted mean molecular weight and on whether local thermal equilibrium is justified.",
    92: r"For the Sun, the global ratio $L_\odot/L_{\rm Edd}$ is $2.6772\times10^{-5}$ under the stated electron-scattering convention. This does not mean that radiative force is equally small at every layer: local flux, opacity, and enclosed mass matter. In the solar photosphere, electron scattering is not the dominant opacity. Use the ratio as an illustrative global scale, not a local force measurement.",
    93: r"Radiation can also remove heat behind a shock. The molecular-gas example in <a href='module08.html'>Module 8</a> reaches a much larger compression when cooling is efficient than an adiabatic jump permits. That effect involves radiative energy loss, whereas the Eddington balance concerns radiative momentum transfer. A full radiation-hydrodynamics calculation couples both.",
    94: r"The chapter now supplies three useful limits: optically thick diffusion for heat transport, a grey atmosphere for the surface temperature profile, and a force balance for the Eddington luminosity. None describes arbitrary spectra, time-dependent transfer, or multidimensional accretion. Applying them outside their assumptions requires solving the radiation field together with the fluid equations.",
    95: r"A reader can now calculate radiation pressure from intensity moments, estimate a local thermal diffusivity, and determine the opacity dependence of the Eddington scale. The photospheric example also shows why a column mean, a local Rosseland mean, and a flux mean answer different questions. Their distinctions must survive any cross-module use of the numerical results.",
})

R14.update({
    52: r"<b>Proposition 8 (the Jeans resolution condition).</b> Truelove and colleagues (1997) define $J=\Delta x/\lambda_{\rm J}$ and report that $J\le0.25$ avoided artificial fragmentation in their tested isothermal collapse. This is an empirical resolution criterion, not a general convergence theorem. Since $\lambda_{\rm J}\propto\rho^{-1/2}$ at fixed temperature, following collapse from $\rho_0$ to $\rho$ requires cell width to shrink by $(\rho/\rho_0)^{1/2}$ to maintain the same $J$.",
    6: r"<b>Proposition 1 (conservation and the weak solution).</b> (a) Update (1.1) conserves $\sum_iU_i\Delta x$ apart from flux through the grid ends. (b) If a consistent conservative scheme converges boundedly and almost everywhere as $\Delta x,\Delta t\to0$, its limit is a weak solution of the conservation law. Its shocks therefore satisfy the <a href='module08.html#jump'>jump conditions of Module 8</a>. We derive (a) below and state (b), the Lax–Wendroff theorem, with its convergence hypothesis explicit.",
    32: r"<b>CHECK 2(a) — the exact Sod solution.</b> Proposition 6 gives $P^*=0.303130$, $u^*=0.927453$, $\rho^*_{\rm L}=0.426319$, $\rho^*_{\rm R}=0.265574$, and shock speed $1.752156$. The five values agree with Marzouk (2020), Table 2, to its printed precision. The computed shock satisfies the mass and momentum jump conditions, while the rarefaction follows the isentropic branch. This checks the implementation of both branches of the Riemann solver against known reference values.",
    34: r"""The contact is a particularly useful test because pressure and velocity are constant across it while density jumps. Godunov's mass flux there reduces to the upwind flux $\rho_i u^*$. The contact therefore obeys the scalar update (2.1) with $C_{\rm c}=u^*\Delta t/\Delta x$. At $N=6400$, the time-averaged contact Courant number is $0.3810$.

To predict its width, apply Proposition 5 to density differences $d_i=\rho_{i-1}-\rho_i$. Initially only one $d_i$ is nonzero. Upwinding replaces each difference by $(1-C_{\rm c})d_i+C_{\rm c}d_{i-1}$, so its total remains $\Delta\rho_{\rm c}$ and its variance grows by $C_{\rm c}(1-C_{\rm c})\Delta x^2$ per step. Summing over steps gives $\sigma^2=\sum_n C_{\rm c}(1-C_{\rm c})\Delta x^2$. With $\Delta t\propto\Delta x$, there are $O(1/\Delta x)$ steps at fixed physical time. Consequently $\sigma\propto\Delta x^{1/2}$.

For many steps, the distribution of differences approaches a Gaussian. Integrating the difference between the resulting smoothed step and the exact step gives
$$ E_{\rm c} \;=\; \Delta\rho_{\rm c}\,\sigma\left(\frac{2}{\pi}\right)^{1/2}, \qquad \sigma \propto \Delta x^{1/2}. \tag{5.1}$$
Here $\Delta\rho_{\rm c}=0.160746$; no width parameter is fitted. A shock behaves differently because characteristics converge toward it, keeping its numerical width to a few cells as the grid is refined.""",
    35: r"<b>CHECK 2(b) — different convergence rates within one flow.</b> From $N=100$ to $6400$, the measured density $L_1$ error falls with order $1.013$ at the shock, $0.511$ at the contact, $0.752$ in the fan, and $0.646$ overall. The contact error is $1.1293$ times equation (5.1) at $N=100$ and $1.0659$ times at $N=6400$. Its measured rate is consistent with the predicted $\Delta x^{1/2}$ scaling. The method's formal first-order estimate assumes smooth solutions; the discontinuous contact changes the observed global rate in this norm. These results do not invalidate the formal order under its stated regularity assumptions.",
    39: r"<b>CHECK 3 — convergence in the Sedov blast.</b> At 100, 200, and 400 cells, the half-height estimates of the shock radius are $1.02764$, $1.01365$, and $1.00663$. Their errors relative to the exact radius 1 roughly halve with each doubling of resolution. Peak densities are $3.0559$, $3.7619$, and $4.4010$, below the exact strong-shock jump value 6 because the shock is spread over several cells. The update conserves total energy to the reported roundoff level. Conservation supports convergence to the correct weak solution; it does not make the shock position exact on a finite grid.",
    40: r"The Sedov solution concentrates swept-up mass in a thin shell behind the shock. A first-order calculation spreads that shell across cells, reducing its peak density. The chosen half-height radius also lies outside the exact radius at finite resolution, but approaches it as the grid is refined. The peak and position therefore measure different aspects of error; neither should be reported as exact merely because the discrete update conserves energy.",
    46: r"Shocks require dissipation in the SPH equations. Here the pairwise artificial-viscosity term uses Monaghan's form with $\alpha=1$ and $\beta=2$ for approaching particles. The thermal-energy update is paired with the momentum equation so that pairwise exchanges conserve total energy. Time integration uses kick–drift–kick with a step based on $0.2h/(c_{\rm s}+|v|)$. These choices define the particular SPH calculation tested below; other formulations may behave differently.",
    48: r"<b>CHECK 4 — pressure error at an SPH contact.</b> For standard SPH, the maximum relative pressure error within $0.05$ of the contact is $0.0893$, $0.0938$, and $0.0942$ at 200, 400, and 800 particles per unit length. These runs show no decrease in that maximum-norm error. The corresponding volume-weighted relative $L_1$ errors are $0.0511$, $0.0241$, and $0.0129$, so integrated error does decrease. With Price's artificial conductivity, the maximum error falls to $0.0371$, $0.0310$, and $0.0216$. The added term improves this test; no norm-independent convergence claim follows from three resolutions.",
    49: r"Price (2008) identifies a pressure blip at an SPH contact and traces it in part to a thermal-energy overshoot. The present run also has such an overshoot: near the contact, specific thermal energy reaches $3.0943$ rather than the exact hot-side value $2.8535$. Since $P=(\gamma-1)\rho u$, that error affects pressure. Price's published shock tube uses $\gamma=5/3$; this Sod test uses $\gamma=1.4$. Their numerical values should therefore not be identified, even though they illustrate the same mechanism.",
    50: r"A spurious pressure gradient at an entropy contrast can resist interpenetration of two fluids. Price relates this effect to artificial surface tension at shearing contacts and shows how conductivity reduces it. Agertz and colleagues found that a standard SPH calculation suppressed Kelvin–Helmholtz rolls that developed in a grid calculation. Their two-dimensional result is consistent with this contact mechanism, but the one-dimensional Sod runs here do not reproduce the full instability test.",
    54: r"For the 10 K core used in Module 5, $\lambda_{\rm J}=0.19479$ pc at $n(\mathrm{H_2})=10^4\ \mathrm{cm^{-3}}$. The Truelove condition requires cells no wider than about $10^4$ AU initially. If the gas remains isothermal up to $10^{10}\ \mathrm{cm^{-3}}$, the limit falls to $10.04$ AU. A uniform box four initial Jeans lengths across would then need about $1.6\times10^4$ cells per side, or $4.096\times10^{12}$ cells in three dimensions. Adaptive refinement places the required cells only where the density rises. The isothermal estimate ceases to apply when cooling can no longer hold the gas at 10 K.",
    55: r"SPH has a corresponding mass-resolution condition. Bate and Burkert (1997) require the Jeans mass to exceed roughly $2N_{\rm neigh}m$, where $m$ is particle mass and $N_{\rm neigh}=50$ in their example. At $10^{10}\ \mathrm{cm^{-3}}$, the core's quoted Jeans mass is $0.002658\,M_\odot$, giving $m\lesssim2.66\times10^{-5}\,M_\odot$. Particles move closer during collapse, improving spatial resolution, but their individual masses do not shrink. A fixed-mass SPH run must therefore choose its particle mass for the highest density it intends to resolve.",
    57: r"<b>A grid-scale estimate.</b> Suppose a local discretisation has one characteristic spatial scale $\Delta x=L/N$ and requires the Kolmogorov scale $\eta$ to be no smaller than $\Delta x$. Since $L/\eta=\mathrm{Re}^{3/4}$, this gives the necessary estimate $\mathrm{Re}\lesssim N^{4/3}$. It yields $1.032\times10^4$ for $N=1024$ and $6.554\times10^4$ for $N=4096$. This is not a universal accuracy bound. Practical methods need several effective degrees of freedom across a relevant structure, and higher-order or subcell representations do not fit the literal one-scale assumption.",
    58: r"<b>The cost of a contact.</b> Over the last measured refinement, the contact error decreases with fitted order $0.5209$. Extrapolating that rate from $N=6400$ to an error of $10^{-4}$ gives about $1.864\times10^5$ cells in one dimension. For a uniform three-dimensional explicit grid, work scales approximately as $N^4$: $N^3$ cells times $N$ Courant-limited steps. The projected work is therefore about $7.19\times10^5$ times greater. This is an extrapolation for this method and error measure, not a universal cost law.",
})

R13.update({
    36: r"<b>CHECK 4 — grey temperature profile against ATLAS9.</b> At seven Rosseland depths, equation (5.1) differs from the model temperature by at most $3.01$ per cent. The comparison describes the size of the grey approximation's discrepancy; a success tolerance was not set before the calculation. Because radiative flux scales with $T^4$, a $3.01$ per cent temperature difference corresponds to about $12.6$ per cent in $T^4$. {table} The largest listed temperature discrepancy occurs at $\tau_{\rm R}=0.01$. Agreement in temperature does not separately validate the opacity, convection treatment, or surface boundary closure.",
    57: r"<b>CHECK 3 — a photospheric radiative-leakage estimate.</b> Using local ATLAS9 opacity and density gives $\omega\chi/c_{\rm s}^2=0.4468$ at the $T=5772$ K layer and $0.3445$ at $\tau_{\rm R}=2/3$. Neither is asymptotically small, so the adiabatic limit is not well controlled under this estimate. {table} The diffusion closure assumes an optically thick, nearly isotropic field, while the outward optical depth at the second layer is only $2/3$. These values indicate potentially important heat leakage; they do not refute a complete adiabatic-oscillation model. A quantitative damping rate requires non-adiabatic transfer with the surface boundary condition.",
    74: r"<b>CHECK 1 — Eddington scales and composition.</b> The pure-hydrogen Thomson formula reproduces the numerical examples in Modules 9 and 11 to their printed precision. {table} For fully ionised gas with hydrogen mass fraction $X$, the corresponding luminosity scales as $2/(1+X)$ relative to pure hydrogen. Taking $X=0.7261$, the initial fraction in the cited solar model, gives $1.4565\times10^{39}\ \mathrm{erg\,s^{-1}}$ for a $10\,M_\odot$ object, 15.9 per cent above the pure-hydrogen value. The choice of $X$ is an illustrative composition; it must be specified for a particular accretion flow.",
})


def build(module: int, replacements: dict[int, str]) -> None:
    source = SOURCE / f"module{module:02}.html"
    destination = DEST / source.name
    soup = BeautifulSoup(source.read_text(encoding="utf-8"), "html.parser")
    nodes = blocks(soup)
    expected = 96 if module == 13 else 65
    if len(nodes) != expected:
        raise RuntimeError(f"Module {module}: expected {expected} blocks, got {len(nodes)}")
    for index, html in replacements.items():
        old_table = nodes[index].find("table")
        if old_table is not None:
            table_html = str(old_table)
            html = html.replace("{table}", table_html)
            if table_html not in html:
                html += table_html
        if module == 14 and index == 34:
            parts = html.split("\n\n")
            replace_inner(nodes[index], parts[0])
            previous = nodes[index]
            for part in parts[1:]:
                paragraph = soup.new_tag("p")
                replace_inner(paragraph, part)
                previous.insert_after(paragraph)
                previous = paragraph
        else:
            replace_inner(nodes[index], html)

    if module == 13:
        replacements_in_cells = {
            "§7 confirms Module 4's prediction at the photosphere": "§7 estimates substantial radiative leakage near the photosphere",
            "§10 pays the debt as a bound": "§10 gives a force-balance scale",
            "The radiative heating of a wind is not computed here": "Wind heating requires frequency-dependent absorption and a dynamical wind model",
            "That needs dust opacities, which the book does not carry": "This requires dust opacities and radiative equilibrium for the grains",
            'The "tenth" itself is confirmed by CHECK 1': 'The accretion-rate normalization is reproduced in CHECK 1',
            "Paid as a bound, not as a flow": "Force-balance estimate only",
            "Refused in print, here": "Outside scope",
            "Half paid": "Partly addressed",
            "Not repaid": "Outside scope",
            "where it is repaid": "further work",
        }
    else:
        replacements_in_cells = {
            "the plan caps numerics at one module": "multidimensional methods require a separate treatment",
            "pays the debt as a resolution count": "applies the published criterion to a resolution estimate",
            "Half paid": "Partly addressed",
            "Paid as a count": "Resolution estimate supplied",
        }
    for cell in soup.find_all(["td", "th"]):
        html = cell.decode_contents()
        for before, after in replacements_in_cells.items():
            html = html.replace(before, after)
        replace_inner(cell, html)

    if module == 13:
        for row in soup.select("#limits ~ table tr"):
            cells = row.find_all("td", recursive=False)
            if not cells:
                continue
            label = cells[0].get_text(" ", strip=True)
            if "Radiative Bondi" in label:
                replace_inner(cells[1], "<a href='#accretion'>§10</a> compares outer mass supply with a radiative force-balance scale. It does not solve the radiating inflow.")
            elif "Radiative heating of the solar wind" in label:
                replace_inner(cells[1], "Wind heating requires frequency-dependent absorption coupled to the wind dynamics.")
            elif "Radiative heating of dust" in label:
                replace_inner(cells[1], "Dust heating requires grain opacities and radiative equilibrium for the grains.")
            elif "The inner AGN disc" in label:
                replace_inner(cells[1], "Its vertical structure must include radiation pressure before an inner-disc pressure ratio can be calculated.")
            elif "adiabatic criterion" in label:
                replace_inner(cells[1], r"<a href='#leak'>§7</a> estimates $\omega\chi/c_{\rm s}^2=0.3445$–$0.4468$ near the photosphere. Because diffusion is unreliable at the free boundary, this is evidence of possible leakage rather than a computed damping rate.")
            if len(cells) > 2 and "Outside scope" not in cells[2].get_text():
                value = cells[2].decode_contents()
                value = value.replace("Nowhere in this book", "Requires a fuller radiation-hydrodynamics treatment")
                replace_inner(cells[2], value)

        source_list = soup.find(id="sources").find_next("ol")
        citation = soup.new_tag("li")
        replace_inner(citation, "<b>NIST XCOM photon cross-section database.</b> <a href='https://pml.nist.gov/PhysRefData/Xcom/Text/chap2.html'>Documentation, Section 2</a>. Its Compton-scattering treatment uses the Klein–Nishina energy dependence, supporting the Thomson-limit qualification in §§6 and 9.")
        source_list.append(citation)

        for proof in soup.select("div.proof"):
            html = proof.decode_contents()
            html = html.replace("<b>The hinge is the surface condition, which fixes $C$.</b>", "The surface condition fixes the integration constant $C$.")
            html = html.replace("<b>What is stated and not derived</b> is the Stefan–Boltzmann law", "We take the Stefan–Boltzmann law")
            html = html.replace("this book does no statistical mechanics of photons", "its statistical-mechanical derivation lies outside the present fluid treatment")
            html = html.replace("this module computes $q_{\\rm H}$ numerically and does not derive it", "$q_{\\rm H}$ is evaluated numerically below")
            html = html.replace("This is an order of magnitude and is printed as one.", "This is an order-of-magnitude estimate.")
            html = html.replace("The time $R^2/D$ is an order of magnitude and is printed as one.", "The time $R^2/D$ is an order-of-magnitude estimate.")
            replace_inner(proof, html)
        for caption in soup.find_all("figcaption"):
            html = caption.decode_contents()
            html = html.replace("The Bondi hole lies above the line at $1$, which is Module 9's self-inconsistency drawn as a point.", "The Bondi supply ratio lies above one only under the assumed conversion of outer supply into an inner radiating flow; it is not a measured Eddington luminosity ratio.")
            replace_inner(caption, html)
    else:
        for row in soup.select("#limits ~ table tr"):
            for cell in row.find_all(["td", "th"], recursive=False):
                html = cell.decode_contents().replace("where it is repaid", "scope or further work")
                html = html.replace("Nowhere in this book", "Beyond this chapter")
                replace_inner(cell, html)
        for caption in soup.find_all("figcaption"):
            html = caption.decode_contents()
            html = html.replace("measured by the run", "calculated from the discrete update")
            html = html.replace("the run's own time steps", "the recorded time steps")
            html = html.replace("this module does not measure that overshoot", "the plotted overshoot is not quantified")
            replace_inner(caption, html)
        for proof in soup.select("div.proof"):
            html = proof.decode_contents().replace(
                "Part (b) is the theorem of Lax and Wendroff, read in their 1958 Los Alamos report, p. 9.",
                "Part (b) is the Lax–Wendroff theorem."
            )
            replace_inner(proof, html)

    exercise_edits = {
        13: {
            "K2.": [
                ("<b>A flow that radiates that inefficiently escapes the limit</b>: it can accrete at the Bondi rate without radiation pressure stopping it. That is the regime <a href=\"module09.html#limits\">Module 9 §9</a> puts Sgr A* in, at $\\eta_{\\rm rad} \\approx 4\\times10^{-9}$.",
                 "At that <em>assumed</em> efficiency, the luminosity equals the Thomson force-balance scale. This alone does not establish a steady inflow at the Bondi rate: the supplied gas may be lost before reaching the radiating region, and flow geometry and opacity also matter."),
            ],
            "K3.": [
                ("At the cutoff, the highest frequency the atmosphere traps, the leakage is half a radian of heat per radian of oscillation.",
                 "The local diffusion estimate is therefore not asymptotically adiabatic at this frequency. Because the layer lies near a free surface, the number is not a computed damping rate."),
            ],
        },
        14: {
            "C3.": [
                ("What Reynolds number does it run at, by (3.3), and what is the largest Reynolds number that any scheme on 512 cells can represent, by <a class=\"secref\" href=\"#price\">§10</a>?",
                 "Compute the effective numerical Reynolds number from (3.3). Compare it with the one-cell Kolmogorov-scale estimate of <a class=\"secref\" href=\"#price\">§10</a> and explain why they answer different questions."),
                ("The bound is $512^{4/3} = 4096.0$. The upwind number is above the bound, which is not a contradiction: (3.3) says the scheme's diffusion is weak enough to allow $\\mathrm{Re} = 5120$, while the bound says that no structure smaller than one cell can be represented, whatever the diffusion. The smaller of the two numbers applies, and here that is the grid.",
                 "The one-cell scale estimate is $512^{4/3}=4096.0$. The first number describes the leading diffusive error of upwind advection; the second estimates whether a Kolmogorov scale occupies at least one cell. Their numerical ordering does not define a universal resolvable Reynolds number or prove that either criterion is sufficient for accuracy."),
            ],
        },
    }
    for problem in soup.select("div.prob"):
        label = problem.find("b")
        if label is None:
            continue
        changes = exercise_edits[module].get(label.get_text(strip=True))
        if not changes:
            continue
        html = problem.decode_contents()
        for before, after in changes:
            if before not in html:
                raise RuntimeError(f"Module {module}: exercise replacement not found: {label.text}")
            html = html.replace(before, after)
        replace_inner(problem, html)

    soup.find(id="limits").string = "12. Scope and limitations"
    for link in soup.select('a[href="#limits"]'):
        link.string = "Scope and limitations"

    credit = soup.new_tag("aside", attrs={"class": "codex-revision"})
    credit["style"] = "display:block;background:#102a2b;border-left:4px solid #2dd4bf;padding:.8rem 1rem;margin:1rem 0;color:#d5fffa"
    replace_inner(credit, f"<b>Codex textbook edition.</b> This separate rewrite applies the twenty-rule prose standard and the scientific corrections documented in the <a href='../delta-audit-2026-09-22/AUDIT_REPORT.html'>independent audit</a>. The <a href='../../afd/module{module:02}.html'>original module</a> remains unchanged.")
    soup.select_one("p.sub").insert_after(credit)
    author = soup.new_tag("meta", attrs={"name": "author", "content": "Codex — OpenAI"})
    soup.head.append(author)
    output = str(soup)
    original_displays = re.findall(r"\$\$.*?\$\$", source.read_text(encoding="utf-8"), re.S)
    generated_displays = re.findall(r"\$\$.*?\$\$", output, re.S)
    if len(original_displays) != len(generated_displays):
        raise RuntimeError(f"Module {module}: displayed equation count changed")
    for old, generated in zip(original_displays, generated_displays):
        if html_lib.unescape(generated) != old:
            raise RuntimeError(f"Module {module}: displayed equation changed")
    display_iter = iter(original_displays)
    output = re.sub(r"\$\$.*?\$\$", lambda _: next(display_iter), output, flags=re.S)
    destination.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    build(13, R13)
    build(14, R14)
