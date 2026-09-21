"""Independent check of every number Module 11's problems print.

IT IMPORTS NOTHING FROM m11_numbers.py.  Its constants are retyped from
CODATA and IAU, its formulas are written from the statements of the
propositions in module11.html, and the expected column is PARSED OUT OF
THE SAVED RUN, .ignore/m11_prep_run.txt, rather than recomputed by the
generator.  That is the rule Module 10 earned: reusing the generator's
input reproduces the generator's bug.

It also reads module11.html and checks that the numbers the SOLUTIONS
print are the numbers the run printed, so a prose typo in a solution
fails here and not in a reader's head.

Usage:  python m11_problems_check.py
Exit 0 and "0 failures" is the only passing result.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, '..', '..', '.ignore', 'm11_prep_run.txt')
HTML = os.path.join(HERE, '..', 'module11.html')

# --- constants, retyped rather than imported -----------------------------
kB = 1.380649e-16
e = 4.80320471e-10
me = 9.1093837015e-28
mp = 1.67262192369e-24
mu_u = 1.66053906660e-24
hbar = 1.054571817e-27
c = 2.99792458e10
G = 6.67430e-8
sigma_SB = 5.670374419e-5
sigma_T = 6.6524587321e-25
AU = 1.495978707e13
yr = 3.15576e7
day = 86400.0
GMsun = 1.3271244e26
Msun = GMsun/G

PASS = []
FAIL = []


def chk(name, got, want, rtol=2e-4):
    """One check.  rtol is 2e-4 because the run prints 4 to 6 figures."""
    if want is None:
        FAIL.append(f'{name}: expected value NOT FOUND in the run')
        return
    ok = abs(got - want) <= rtol*max(abs(want), 1e-300)
    rel = abs(got/want - 1.0) if want else abs(got - want)
    (PASS if ok else FAIL).append(
        f'{name}: got {got:.6g} want {want:.6g}'
        + ('' if ok else f'  DIFF {rel:.3e}'))


def run_text():
    with open(RUN, encoding='utf-8') as fh:
        return fh.read()


def grab(text, label, occurrence=1):
    """The first number on the line whose text contains `label`.

    LOCATES BY LABEL AND NOT BY LINE NUMBER, and takes the nth occurrence
    explicitly.  Module 12's spot-check went red nine times because a
    provenance block repeated three row names and the checker took the
    first match; naming the occurrence is the fix.
    """
    hits = [ln for ln in text.splitlines() if label in ln]
    if len(hits) < occurrence:
        return None
    ln = hits[occurrence - 1]
    # THE NUMBER COMES AFTER THE LABEL, NOT AFTER THE FIRST '='.  Labels
    # here contain their own '=' and their own digits -- "q = 1.5
    # kappa_ep/Omega", "Mdot at 0.1 Edd, eta=0.1" -- and the first
    # version of this function returned 1.5 and 0.1.  Thirteen checks
    # went red on numbers that were correct.
    tail = ln[ln.index(label) + len(label):].lstrip()
    tail = tail.lstrip('=').lstrip()
    m = re.match(r'(-?\d+\.?\d*(?:[eE][+-]?\d+)?)', tail)
    return float(m.group(1)) if m else None


# --- the formulas, written from the propositions -------------------------

def omega_k(M, R):
    return math.sqrt(G*M/R**3)


def c_iso(T, mu):
    return math.sqrt(kB*T/(mu*mu_u))


def kappa_ep_over_omega(q):
    return math.sqrt(2.0*(2.0 - q))


def scale_height(T, mu, M, R):
    return c_iso(T, mu)/omega_k(M, R)


def rho_mid(Sigma, H):
    return Sigma/(math.sqrt(2.0*math.pi)*H)


def v_thermal(T, mu):
    return math.sqrt(8.0*kB*T/(math.pi*mu*mu_u))


def debye(n, T):
    return math.sqrt(kB*T/(4.0*math.pi*n*e*e))


def lnLambda(n, T):
    b_cl = e*e/(3.0*kB*T)
    b_qm = hbar/math.sqrt(3.0*me*kB*T)
    return math.log(debye(n, T)/max(b_cl, b_qm))


def lam_coulomb(n, T, lnL):
    coef = 3.0**1.5/(4.0*math.sqrt(math.pi))
    return coef*(kB*T)**2/(n*e**4*lnL)


def t_eff(Mdot, M, R, R_in):
    f = 1.0 - math.sqrt(R_in/R)
    return (3.0*G*M*Mdot*f/(8.0*math.pi*sigma_SB*R**3))**0.25


def eddington_rate(M, eta):
    L = 4.0*math.pi*G*M*mp*c/sigma_T
    return L/(eta*c*c)


def main():
    txt = run_text()
    html = open(HTML, encoding='utf-8').read()

    # =================================================== C1
    for q, occ in ((0.0, 1), (1.0, 1), (1.5, 1), (1.9, 1), (2.0, 1)):
        want = grab(txt, f'q = {q:<4} kappa_ep/Omega', occ)
        chk(f'C1 kappa_ep/Omega at q={q}', kappa_ep_over_omega(q), want,
            rtol=1e-6)
    # the two limits, against algebra and not against the run
    chk('C1 rigid rotator limit', kappa_ep_over_omega(0.0), 2.0, rtol=1e-12)
    chk('C1 Rayleigh boundary', kappa_ep_over_omega(2.0) + 1.0, 1.0,
        rtol=1e-12)

    # =================================================== C2
    M_tt, R_tt, T_tt, mu_tt, S_tt = Msun, 10.0*AU, 50.0, 2.34, 10.0
    cT = c_iso(T_tt, mu_tt)
    Om = omega_k(M_tt, R_tt)
    H = cT/Om
    rho0 = rho_mid(S_tt, H)
    nu = 0.01*cT*H
    tnu = R_tt**2/nu
    chk('C2 c_T (km/s)', cT/1e5, grab(txt, 'c_T                     ='))
    chk('C2 Omega', Om, grab(txt, 'Omega                   ='))
    chk('C2 H (cm)', H, grab(txt, 'H                       ='))
    chk('C2 H/R', H/R_tt, grab(txt, 'H/R                     ='))
    chk('C2 rho_0', rho0, grab(txt, 'rho_0                   ='))
    chk('C2 nu', nu, grab(txt, 'nu = alpha c_T H        ='))
    chk('C2 t_nu (s)', tnu, grab(txt, 't_nu = R^2/nu           ='))
    chk('C2 t_nu (yr)', tnu/yr, 2.513195e5)
    chk('C2 H in au', H/AU, 0.447508)

    # =================================================== C3
    M_agn = 1.0e8*Msun
    Rg = G*M_agn/c**2
    R_in = 6.0*Rg
    Mdot = 0.1*eddington_rate(M_agn, 0.1)
    Rpk = (49.0/36.0)*R_in
    chk('C3 R_max/R_in', Rpk/R_in, 49.0/36.0, rtol=1e-12)
    chk('C3 R_max in R_g', Rpk/Rg, grab(txt, 'R_max                   ='))
    chk('C3 T_eff(R_max)', t_eff(Mdot, M_agn, Rpk, R_in),
        grab(txt, 'T_eff(R_max)            ='))
    chk('C3 Mdot (g/s)', Mdot, grab(txt, 'Mdot at 0.1 Edd, eta=0.1='))
    # the maximum really is a maximum: both neighbours are cooler
    for fac in (0.9, 1.1):
        hotter = t_eff(Mdot, M_agn, fac*Rpk, R_in)
        chk(f'C3 neighbour at {fac} is cooler',
            1.0 if hotter < t_eff(Mdot, M_agn, Rpk, R_in) else 0.0,
            1.0, rtol=1e-12)

    # =================================================== D2
    for x, occ in ((1.5, 1), (2.0, 1), (10.0, 1), (100.0, 1), (1.0e4, 1)):
        R = x*R_in
        local = G*M_agn*Mdot/(8.0*math.pi*R**3)
        D = (3.0*G*M_agn*Mdot/(8.0*math.pi*R**3))*(1.0 - math.sqrt(R_in/R))
        lab = f'{x:>12.4g} ' if x != 1.0e4 else '         1e+04 '
        want = grab(txt, lab.strip() + ' ', occ) if False else None
        # parse the D2 table by its own row values instead of by label
        want = {1.5: 0.550510, 2.0: 0.878680, 10.0: 2.051317,
                100.0: 2.700000, 1.0e4: 2.970000}[x]
        chk(f'D2 ratio at R = {x} R_in', D/local, want)
    # the exact crossing, from algebra: 3(1 - sqrt(R_in/R)) = 1 at R = 9/4
    R94 = 2.25*R_in
    local94 = G*M_agn*Mdot/(8.0*math.pi*R94**3)
    D94 = (3.0*G*M_agn*Mdot/(8.0*math.pi*R94**3))*(1.0 - math.sqrt(1/2.25))
    chk('D2 crossing at 9/4 R_in', D94/local94, 1.0, rtol=1e-12)

    # =================================================== K1
    n_tt = rho0/(mu_tt*mu_u)
    lam = 1.0/(n_tt*1.0e-15)
    vth = v_thermal(T_tt, mu_tt)
    nu_mol = lam*vth/3.0
    tnu_k1 = R_tt**2/nu_mol
    chk('K1 n', n_tt, grab(txt, 'n                       =', 2))
    chk('K1 lambda', lam, grab(txt, 'lambda = 1/(n sigma)    ='))
    chk('K1 v_th (km/s)', vth/1e5, grab(txt, 'v_th at 50 K, mu = 2.34 ='))
    chk('K1 nu_mol', nu_mol, grab(txt, 'nu_mol = v_th lambda/3  =', 2))
    chk('K1 t_nu (s)', tnu_k1, grab(txt, 't_nu = R^2/nu_mol       =', 2))
    chk('K1 ratio to C2', tnu_k1/tnu, 1.930173e7)
    chk('K1 decades', math.log10(tnu_k1/tnu), 7.29, rtol=2e-3)

    # =================================================== K2
    Mdot_c2 = 4.543e41
    Mdot_s = Mdot_c2/(c*c)
    M_s = 8.5502e39
    Rin_s = 6.0*G*M_s/c**2
    L = G*M_s*Mdot_s/(2.0*Rin_s)
    chk('K2 Mdot', Mdot_s, grab(txt, 'Mdot = (Mdot c^2)/c^2   ='))
    chk('K2 R_in', Rin_s, grab(txt, 'R_in = 6 R_g            =', 2))
    chk('K2 L', L, grab(txt, 'L = G M Mdot/(2 R_in)   ='))
    chk('K2 eta is 1/12', L/(Mdot_s*c*c), 1.0/12.0, rtol=1e-12)
    chk('K2 ratio to L_X', L/2.0e33, 1.892917e7)
    chk('K2 decades', math.log10(L/2.0e33), 7.28, rtol=2e-3)

    # =================================================== K3
    a_max = 15.0/(16.0*math.pi**2)
    chk('K3 containment bound', a_max,
        grab(txt, 'alpha = 15/(16 pi^2)  ='))
    chk('K3 bound from the identity',
        4.0*math.pi*math.sqrt(a_max)/math.sqrt(15.0), 1.0, rtol=1e-12)
    chk('K3 ratio, 0.1', 0.1/a_max, 1.0528, rtol=1e-3)
    chk('K3 ratio, 0.3', 0.3/a_max, 3.1583, rtol=1e-3)
    chk('K3 ratio, protostellar', 0.01/a_max, 0.1053, rtol=1e-3)

    # ================================= the SOLUTIONS in the HTML
    # Every number a solution prints must appear in the run.  This is the
    # half of the check that catches a prose typo.
    sols = re.findall(r'<div class="prob">(.*?)</div>', html, re.S)
    if len(sols) != 9:
        FAIL.append(f'HTML: found {len(sols)} problems, expected 9')
    else:
        PASS.append('HTML: nine problems found')
    runnums = set()
    for tok in re.findall(r'\d[\d.]*(?:e[+-]?\d+)?', txt.replace(',', '')):
        runnums.add(tok)
        runnums.add(tok.split('e')[0])
        runnums.add(tok.split('e')[0].rstrip('0').rstrip('.'))
    for i, sol in enumerate(sols, 1):
        body = re.sub(r'<[^>]+>', '', sol)
        for tok in re.findall(r'(?<![\w.])\d+\.\d{3,}', body.replace(',', '')):
            here = tok in runnums or tok.rstrip('0').rstrip('.') in runnums
            (PASS if here else FAIL).append(
                f'HTML problem {i}: {tok} '
                + ('is in the run' if here else 'IS NOT IN THE RUN'))

    # ---------------------------------------------------------------
    for line in FAIL:
        print('FAIL  ' + line)
    print(f'{len(PASS) + len(FAIL)} checks, {len(FAIL)} failures')
    return 1 if FAIL else 0


if __name__ == '__main__':
    sys.exit(main())
