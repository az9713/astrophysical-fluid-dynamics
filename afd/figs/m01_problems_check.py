"""Verify every number that appears in a Module 1 problem solution.

Nothing in the solutions is done by hand; the values printed here are the
values that must appear in module01.html.
"""
import numpy as np
from m01_numbers import kB, e, kpc, AU, lam_coulomb, SPITZER_C


def show(label, value, unit=""):
    print(f"  {label:<50s} {value:>12.4g} {unit}")


print("="*72)
print("D3 -- conduction time over sound-crossing time = 3/Kn")
print("="*72)
for name, kn in [("ICM cool core, Kn = 2.2e-3", 2.20e-3),
                 ("ICM outskirts, Kn = 1.11e-1", 1.11e-1)]:
    show(name + "  ->  3/Kn", 3.0/kn)
print()

print("="*72)
print("K1 -- where the solar wind reaches Kn = 1")
print("="*72)
lam1 = lam_coulomb(5.0, 1.2e5, lnL=26.0)/AU
show("lambda at 1 AU (ln Lambda = 26)", lam1, "AU")
print("  n ~ r^-2 and T ~ r^-4/3  =>  lambda ~ T^2/n ~ r^(-8/3+2) = r^-2/3")
print("  Kn(r) = lambda(1) r^-2/3 / r = lambda(1) r^-5/3")
show("r where Kn = 1", lam1**0.6, "AU")
show("same, if lambda(1) were doubled", (2*lam1)**0.6, "AU")
print()

print("="*72)
print("K2 -- beta-model cluster: n_e = 1e-2 [1+(r/100 kpc)^2]^-1")
print("="*72)
T_k2, lnL_k2 = 5.0e7, 37.0
lam0 = lam_coulomb(1.0e-2, T_k2, lnL=lnL_k2)/kpc
show("lambda at n_e = 1e-2 (cluster centre)", lam0, "kpc")


def kn_k2(r):
    """r in kpc; L = r."""
    return lam0*(1.0 + (r/100.0)**2)/r


for r in (100, 300, 500, 1000, 1500, 1740, 2000):
    show(f"Kn at r = {r} kpc", kn_k2(r))
# solve Kn = 0.1
rs = np.linspace(200, 4000, 400000)
k = lam0*(1.0+(rs/100.0)**2)/rs
r_cross = rs[np.argmin(np.abs(k-0.1))]
show("radius where Kn = 0.1", r_cross, "kpc")
show("  lambda there", lam0*(1.0+(r_cross/100.0)**2), "kpc")
print("  <-- PUNCHLINE: is that mean free path above or below a 10 kpc cell?")
print()

print("="*72)
print("K3 -- maximum core temperature for t_cond/t_s >= 100")
print("="*72)
L_k3, n_k3, lnL_k3 = 50.0*kpc, 2.0e-2, 36.0
kn_max = 3.0/100.0
lam_max = kn_max*L_k3
show("Kn ceiling", kn_max)
show("lambda ceiling", lam_max/kpc, "kpc")
T_max = np.sqrt(lam_max*n_k3*e**4*lnL_k3/(SPITZER_C*kB**2))
show("T ceiling", T_max, "K")
show("  check: lambda at that T", lam_coulomb(n_k3, T_max, lnL=lnL_k3)/kpc,
     "kpc")
print()

print("="*72)
print("C1 -- warm neutral ISM interface scale")
print("="*72)
show("lambda, warm neutral ISM", 1.0/(0.5*1e-15)/AU, "AU")
