"""Verify every number quoted in the Module 2 problem solutions.

Two arithmetic errors were caught this way in Module 1. Each assertion
below reproduces one figure written out in module02.html and fails loudly
if the prose and the arithmetic disagree. Run before shipping solutions.
"""
import numpy as np
from m02_numbers import (kB, mp, AU, Msun, yr, kpc, v_th, lam_coulomb,
                         VB18, HELIOS_RMIN, HELIOS_RMAX, mdot,
                         continuity_residual)

OK = []


def check(label, got, want, tol, unit=""):
    """Assert that a computed value matches the figure quoted in the prose."""
    rel = abs(got-want)/abs(want) if want else abs(got)
    status = "ok " if rel <= tol else "FAIL"
    OK.append(rel <= tol)
    print(f"  [{status}] {label:<52s} {got:>11.4g} vs {want:>11.4g} {unit}"
          f"   ({rel*100:.2f}% off, tol {tol*100:g}%)")


print("="*78)
print("K1 -- mass-flux drift across the Helios range")
print("="*78)
alpha_a, beta_a = 2.010, 0.049
resid_a = 2.0-alpha_a+beta_a
check("residual exponent, mean fits", resid_a, 0.039, 2e-2)
span = HELIOS_RMAX/HELIOS_RMIN
check("radial span 0.98/0.29", span, 3.379, 1e-3)
check("ln of the span", np.log(span), 1.2176, 1e-3)
check("exponent times ln span", resid_a*np.log(span), 0.04749, 3e-2)
check("flux factor, mean fits", span**resid_a, 1.0486, 1e-3)
check("flux drift, mean fits", (span**resid_a-1)*100, 4.9, 2e-2, "%")
alpha_m, beta_m = 2.093, 0.058
resid_m = 2.0-alpha_m+beta_m
check("residual exponent, median fits", resid_m, -0.035, 2e-2)
check("flux factor, median fits", span**resid_m, 0.958, 2e-3)
check("flux drift, median fits", (span**resid_m-1)*100, -4.2, 2e-2, "%")

print("="*78)
print("K2 -- the solar mass loss rate")
print("="*78)
n_med, v_med = 5.61, 410.7
rho = n_med*mp
check("rho = n m_p", rho, 9.383e-24, 1e-3, "g/cm^3")
check("4 pi r^2 at 1 AU", 4*np.pi*AU**2, 2.812e27, 1e-3, "cm^2")
check("v in cm/s", v_med*1e5, 4.107e7, 1e-6, "cm/s")
M = mdot(n_med, v_med)
check("Mdot", M, 1.084e12, 2e-3, "g/s")
check("Mdot in Msun/yr", M*yr/Msun, 1.72e-14, 3e-3, "Msun/yr")
check("mass lost in 4.6 Gyr", M*yr/Msun*4.6e9, 7.9e-5, 5e-3, "Msun")
check("  as a percentage of Msun", M*yr/Msun*4.6e9*100, 0.0079, 5e-3, "%")
check("ratio to the published 1e12 g/s", M/1e12, 1.08, 5e-3)
check("Mdot including 4% helium", mdot(n_med, v_med, helium=True),
      1.26e12, 3e-3, "g/s")

print("="*78)
print("K3 -- Knudsen, Mach and Reynolds numbers of the cluster core")
print("="*78)
n_icm, T_icm = 1e-2, 3e7
lam = lam_coulomb(n_icm, T_icm)
check("Coulomb mfp from Module 1", lam/kpc, 0.22, 2e-2, "kpc")
L_icm = 100*kpc
check("Kn = lambda / L", lam/L_icm, 2.2e-3, 2e-2)
vt = v_th(T_icm)
check("proton thermal speed", vt, 7.04e7, 2e-3, "cm/s")
u_icm = 3e7
check("Ma_th = u / v_th", u_icm/vt, 0.426, 3e-3)
Re = 3.0*(u_icm/vt)/(lam/L_icm)
check("Re = 3 Ma_th / Kn", Re, 5.8e2, 2e-2)
check("stated as a factor of about 600", Re, 600.0, 5e-2)

print("="*78)
print("K4 -- the adiabatic closure, tested against the same fits")
print("="*78)
gamma = 5.0/3.0
tau_pred_m = alpha_m*(gamma-1.0)
check("adiabatic T exponent, median alpha", tau_pred_m, 1.395, 2e-3)
T_meas_m, T_sig_m = 0.913, 0.039
check("ratio measured/adiabatic, median", T_meas_m/tau_pred_m, 0.654, 2e-3)
check("shortfall, median", (1-T_meas_m/tau_pred_m)*100, 34.6, 3e-3, "%")
check("departure in sigma, median",
      abs(T_meas_m-tau_pred_m)/T_sig_m, 12.4, 5e-3, "sigma")
tau_pred_a = alpha_a*(gamma-1.0)
check("adiabatic T exponent, mean alpha", tau_pred_a, 1.340, 2e-3)
T_meas_a, T_sig_a = 0.792, 0.028
check("ratio measured/adiabatic, mean", T_meas_a/tau_pred_a, 0.591, 2e-3)
check("shortfall, mean", (1-T_meas_a/tau_pred_a)*100, 40.9, 3e-3, "%")
check("departure in sigma, mean",
      abs(T_meas_a-tau_pred_a)/T_sig_a, 19.6, 5e-3, "sigma")

print("="*78)
print("Body text -- the anchor result of section 10.3")
print("="*78)
d_a, f_a, y_a = continuity_residual("avg")
d_m, f_m, y_m = continuity_residual("med")
check("alpha - beta, mean fits", d_a, 1.961, 1e-3)
check("alpha - beta, median fits", d_m, 2.035, 1e-3)
check("ratio to 2, mean fits", d_a/2, 0.980, 1e-3)
check("ratio to 2, median fits", d_m/2, 1.018, 1e-3)
check("midpoint of the two", 0.5*(d_a+d_m), 1.998, 1e-3)
check("mean fits, formal sigma from 2", abs(d_a-2)/f_a, 0.99, 1e-2, "sigma")
check("median fits, formal sigma from 2", abs(d_m-2)/f_m, 0.73, 1e-2, "sigma")
check("mean fits, yearly sigma from 2", abs(d_a-2)/y_a, 0.53, 2e-2, "sigma")
check("median fits, yearly sigma from 2", abs(d_m-2)/y_m, 0.48, 2e-2, "sigma")

print("="*78)
print("Section 9 table -- every entry, against the prose")
print("="*78)
SIGMA_H = 1.0e-15
pc = kpc/1e3
TABLE = [
    # label, n, T, L, u, ionised, Kn, Ma, Re
    ("solar convection zone", 1e23, 2e6, 2e10, 1e4, True,
     1.6e-16, 5.5e-4, 1.0e13),
    ("warm ISM", 0.5, 8e3, 100*pc, 1e6, False, 6.5e-6, 0.87, 4.0e5),
    ("ICM cluster core", 1e-2, 3e7, 100*kpc, 3e7, True, 2.2e-3, 0.43, 580.0),
    ("solar wind at 1 AU", 5.0, 1.2e5, AU, 4.107e7, True, 1.9, 9.2, 14.0),
]
for nm, n, T, L, u, ion, kn_w, ma_w, re_w in TABLE:
    lam_s = lam_coulomb(n, T) if ion else 1.0/(n*SIGMA_H)
    kn, ma = lam_s/L, u/v_th(T)
    check(f"{nm}: Kn", kn, kn_w, 3e-2)
    check(f"{nm}: Ma_th", ma, ma_w, 3e-2)
    check(f"{nm}: Re", 3*ma/kn, re_w, 3e-2)
    check(f"{nm}: 1/Re", kn/(3*ma), 1.0/re_w, 3e-2)

print("="*78)
print(f"{sum(OK)}/{len(OK)} checks passed")
assert all(OK), "a quoted number does not match its arithmetic"
print("Every number quoted in module02.html reproduces.")
