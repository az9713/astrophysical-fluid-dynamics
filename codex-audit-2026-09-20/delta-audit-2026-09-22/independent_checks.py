from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
FIGS = ROOT / "afd" / "figs"
sys.path.insert(0, str(FIGS))

import m14_solvers as solvers  # noqa: E402


def klein_nishina_ratio(x: float) -> float:
    """Total Klein-Nishina cross-section divided by Thomson; x = h nu / m_e c^2."""
    term1 = ((1.0 + x) / x**3) * (
        (2.0 * x * (1.0 + x) / (1.0 + 2.0 * x)) - math.log(1.0 + 2.0 * x)
    )
    term2 = math.log(1.0 + 2.0 * x) / (2.0 * x)
    term3 = -(1.0 + 3.0 * x) / (1.0 + 2.0 * x) ** 2
    return 0.75 * (term1 + term2 + term3)


def module13_checks() -> dict[str, object]:
    kappa = 0.4447
    rho = 2.6721e-7
    wavelength_cm = 2615.2e5
    mean_free_path = 1.0 / (kappa * rho)
    return {
        "photosphere_mean_free_path_km": mean_free_path / 1e5,
        "acoustic_wavelength_km": wavelength_cm / 1e5,
        "optical_depth_across_wavelength": wavelength_cm / mean_free_path,
        "optical_depth_to_surface_at_evaluation_point": 2.0 / 3.0,
        "kn_cross_section_over_thomson": {
            "10_keV": klein_nishina_ratio(10.0 / 511.0),
            "100_keV": klein_nishina_ratio(100.0 / 511.0),
            "511_keV": klein_nishina_ratio(1.0),
        },
    }


def module14_sph_norms() -> list[dict[str, float]]:
    gamma = 1.4
    time = 0.2
    p_star, u_star = solvers.riemann_star(1.0, 0.0, 1.0, 0.125, 0.0, 0.1, gamma)
    contact = 0.5 + float(u_star) * time
    rows: list[dict[str, float]] = []
    for n_left in (200, 400, 800):
        x, rho, velocity, pressure, thermal, mass = solvers.sph_shock_tube(
            n_left, 1.0, 1.0, 0.125, 0.1, gamma, time, alpha_u=0.0
        )
        near = np.abs(x - contact) < 0.05
        volume = mass / rho
        abs_error = np.abs(pressure - p_star)
        weighted_l1 = float(np.sum(abs_error[near] * volume[near]))
        covered_length = float(np.sum(volume[near]))
        rows.append(
            {
                "particles_per_unit_length": float(n_left),
                "max_relative_pressure_error": float(np.max(abs_error[near]) / p_star),
                "volume_weighted_relative_L1_near_contact": weighted_l1 / (p_star * covered_length),
                "covered_length": covered_length,
            }
        )
    return rows


def main() -> None:
    data = {
        "module13": module13_checks(),
        "module14": {
            "sph_contact_norms": module14_sph_norms(),
            "reported_sedov_shock_location_errors": [0.02764, 0.01365, 0.00663],
            "note": (
                "A persistent maximum error does not by itself rule out L1 convergence; "
                "convergence claims must name the norm."
            ),
        },
    }
    output = Path(__file__).with_name("independent-checks.json")
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
