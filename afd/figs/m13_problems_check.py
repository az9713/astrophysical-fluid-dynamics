"""Independent check of every number Module 13's problems print.

IT IMPORTS NOTHING FROM m13_numbers.py.  Its constants are retyped from
CODATA and IAU, its formulas are written from the propositions in
module13.html, every input is the number the problem STATEMENT prints, and
the expected column is PARSED OUT OF THE SAVED RUN, .ignore/m13_prep_run.txt.
Reusing the generator's input would reproduce the generator's bug.

It also reads module13.html and checks that every number with three or
more decimals that a SOLUTION prints is a number the run printed, so a
typo in a solution fails here.

Usage:  python m13_problems_check.py
Exit 0 and "0 failures" is the only passing result.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, '..', '..', '.ignore', 'm13_prep_run.txt')
HTML = os.path.join(HERE, '..', 'module13.html')

# --- constants, retyped rather than imported -----------------------------
mp = 1.67262192369e-24
c = 2.99792458e10
G = 6.67430e-8
sigma_SB = 5.670374419e-5
sigma_T = 6.6524587321e-25
yr = 3.15576e7
a_rad = 4.0*sigma_SB/c

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


def grab(text, label, occurrence=1):
    """The first number AFTER `label` on the nth line containing it."""
    hits = [ln for ln in text.splitlines() if label in ln]
    if len(hits) < occurrence:
        return None
    ln = hits[occurrence - 1]
    tail = ln[ln.index(label) + len(label):].lstrip().lstrip('=').lstrip()
    m = re.match(r'(-?\d+\.?\d*(?:[eE][+-]?\d+)?)', tail)
    return float(m.group(1)) if m else None


# --- the formulas, written from the propositions -------------------------

def kappa_es(X):                       # (6.2)
    return sigma_T*(1.0 + X)/(2.0*mp)


def l_edd(M, kap):                     # (9.1)
    return 4.0*math.pi*G*M*c/kap


def grey_T(tau, Teff):                 # (5.1)
    return Teff*(0.75*(tau + 2.0/3.0))**0.25


def gamma1(beta, gg=5.0/3.0):          # (8.1)
    return beta + (4.0 - 3.0*beta)**2*(gg - 1.0)/(
        beta + 12.0*(gg - 1.0)*(1.0 - beta))


def dlnT(beta, gg=5.0/3.0):            # proof of Proposition 8
    return (4.0 - 3.0*beta)*(gg - 1.0)/(beta + 12.0*(gg - 1.0)*(1.0 - beta))


def chi_rad(kap, rho, T, cP):          # (4.4)
    return 16.0*sigma_SB*T**3/(3.0*kap*rho*rho*cP)


def main():
    txt = open(RUN, encoding='utf-8').read()
    html = open(HTML, encoding='utf-8').read()

    # ================================================= C1
    n = 200000
    mus = [-1.0 + (i + 0.5)*2.0/n for i in range(n)]
    iso = sum(m*m for m in mus)/n
    hemi = sum(m*m for m in mus if m > 0)/(n/2)
    chk('C1 isotropic', iso, grab(txt, 'C1 isotropic field, P_rad/u_rad'),
        rtol=1e-6)
    chk('C1 hemisphere', hemi,
        grab(txt, 'C1 one open hemisphere, P_rad/u_rad'), rtol=1e-6)
    chk('C1 beam', 1.0, grab(txt, 'C1 parallel beam, P_rad/u_rad'))

    # ================================================= C2
    Msun_stmt = 1.9884e33
    M_ns = 1.4*Msun_stmt
    LH = l_edd(M_ns, kappa_es(1.0))
    Li = l_edd(M_ns, kappa_es(0.7261))
    chk('C2 mass', M_ns, grab(txt, 'C2 neutron-star mass, g'))
    chk('C2 L_Edd X=1', LH, grab(txt, 'C2 L_Edd, pure hydrogen, erg/s'))
    chk('C2 L_Edd X=0.7261', Li, grab(txt, 'C2 L_Edd, protosolar X, erg/s'))
    chk('C2 Mdot X=1', LH/(0.1*c*c),
        grab(txt, 'C2 Mdot_Edd, pure hydrogen, g/s'))
    chk('C2 Mdot X=0.7261', Li/(0.1*c*c),
        grab(txt, 'C2 Mdot_Edd, protosolar X, g/s'))
    chk('C2 ratio', Li/LH, grab(txt, 'C2 ratio of the two limits'))
    chk('C2 ratio is 2/(1+X)', Li/LH, 2.0/1.7261, rtol=1e-12)

    # ================================================= C3
    for lab, tv in (('surface', 0.0), ('two-thirds', 2.0/3.0),
                    ('depth two', 2.0)):
        chk(f'C3 T at {lab}', grey_T(tv, 5772.0),
            grab(txt, f'C3 grey T at the {lab}, K'))
    chk('C3 surface ratio', grey_T(0.0, 5772.0)/5772.0,
        grab(txt, 'C3 surface T over Teff'), rtol=1e-6)
    chk('C3 surface ratio is 2^-1/4', grey_T(0.0, 1.0), 2.0**-0.25,
        rtol=1e-12)

    # ================================================= D1
    chk('D1 pure gas', gamma1(1.0), grab(txt, 'D1 Gamma_one, pure gas'),
        rtol=1e-6)
    chk('D1 pure radiation', gamma1(0.0),
        grab(txt, 'D1 Gamma_one, pure radiation'), rtol=1e-6)
    chk('D1 half and half', gamma1(0.5),
        grab(txt, 'D1 Gamma_one, half and half'), rtol=1e-6)
    chk('D1 dlnT pure gas', dlnT(1.0),
        grab(txt, 'D1 dlnT/dlnrho, pure gas'), rtol=1e-6)
    chk('D1 dlnT pure radiation', dlnT(0.0),
        grab(txt, 'D1 dlnT/dlnrho, pure radiation'), rtol=2e-6)
    chk('D1 limit 5/3', gamma1(1.0), 5.0/3.0, rtol=1e-12)
    chk('D1 limit 4/3', gamma1(0.0), 4.0/3.0, rtol=1e-12)
    chk('D1 Chandrasekhar Table 1 at 0.5', gamma1(0.5), 1.426, rtol=4e-4)

    # ================================================= D2
    Teff = 5772.0
    dT4 = grey_T(101.0, Teff)**4 - grey_T(100.0, Teff)**4
    chk('D2 deep flux ratio', (c*a_rad/3.0)*dT4/(sigma_SB*Teff**4),
        grab(txt, 'D2 deep flux from the diffusion law over sigma Teff^4'),
        rtol=1e-6)

    # ================================================= D3
    Lsun, GMsun = 3.828e33, 1.3271244e26
    bound = 4.0*math.pi*c*GMsun/Lsun
    chk('D3 bound', bound,
        grab(txt, 'D3 Eddington opacity bound for the Sun, cm^2/g'))
    chk('D3 kappa_es/bound', kappa_es(0.7583)/bound,
        grab(txt, 'D3 kappa_es over that bound'))
    chk('D3 equals L/L_Edd', kappa_es(0.7583)/bound,
        grab(txt, 'D3 L_sun/L_Edd from the limit'))

    # ================================================= K1
    t_sal = 0.1*(sigma_T/mp)*c/(4.0*math.pi*G)
    t_e = t_sal/(1.0 - 0.1)
    nf = math.log(1.0e9/10.0)
    chk('K1 t_e (yr)', t_e/yr,
        grab(txt, 'K1 e-folding time with the kept fraction, yr'))
    chk('K1 e-folds', nf, grab(txt, 'K1 number of e-folds'), rtol=1e-7)
    chk('K1 time (yr)', nf*t_e/yr,
        grab(txt, 'K1 growth time with the kept fraction, yr'))
    chk('K1 time without (yr)', nf*t_sal/yr,
        grab(txt, 'K1 growth time if all the inflow were kept, yr'))
    chk('K1 Salpeter time (yr)', t_sal/yr,
        grab(txt, 'Salpeter time at eta = 0.10, kappa = sigma_T/m_p:'))

    # ================================================= K2
    Mdot = 5.124e22
    M10 = 10.0*Msun_stmt
    L = 0.1*Mdot*c*c
    LE = 4.0*math.pi*G*M10*mp*c/sigma_T         # (9.2)
    chk('K2 L', L, grab(txt, 'K2 luminosity at the book efficiency, erg/s'))
    chk('K2 L/L_Edd', L/LE, grab(txt, 'K2 that luminosity over L_Edd'))
    chk('K2 eta at L_Edd', LE/(Mdot*c*c),
        grab(txt, 'K2 efficiency that would sit at L_Edd'))

    # ================================================= K3
    chi = chi_rad(0.4447, 2.6721e-7, 5910.1, 1.6968e8)
    par = 2.0*math.pi*4497.0e-6*chi/(8.081e5**2)
    chk('K3 chi', chi, grab(txt, 'K3 chi from the stated inputs, cm^2/s'))
    chk('K3 parameter', par,
        grab(txt, 'K3 adiabaticity parameter at the cutoff'))
    chk('K3 periods', 2.0*math.pi/par,
        grab(txt, 'K3 diffusion time over period at the cutoff'))
    chk('K3 ratio to nu_max', 4497.0/3090.0,
        grab(txt, 'K3 against the same level at nu_max, ratio'))
    # P7 as an identity, from the statement's inputs
    lam = 8.081e5/4497.0e-6
    chk('K3 P7 identity', 2.0*math.pi/((lam*lam/chi)*4497.0e-6), par,
        rtol=1e-12)

    # ================================ the SOLUTIONS in the HTML
    probs = html.split('<div class="prob">')[1:]
    probs = [p.split('<h2')[0] for p in probs]
    sols = [p.split('<details', 1)[-1] for p in probs]
    if len(probs) != 9:
        FAIL.append(f'HTML: found {len(probs)} problems, expected 9')
    else:
        PASS.append('HTML: nine problems found')
    runnums = set()
    for tok in re.findall(r'\d[\d.]*(?:e[+-]?\d+)?', txt.replace(',', '')):
        runnums.add(tok)
        runnums.add(tok.split('e')[0])
        runnums.add(tok.split('e')[0].rstrip('0').rstrip('.'))
    for i, sol in enumerate(sols, 1):
        body = re.sub(r'<[^>]+>', '', sol)
        for tok in re.findall(r'(?<![\w.])\d+\.\d{3,}', body):
            here = tok in runnums or tok.rstrip('0').rstrip('.') in runnums
            (PASS if here else FAIL).append(
                f'HTML problem {i}: {tok} '
                + ('is in the run' if here else 'IS NOT IN THE RUN'))

    for line in FAIL:
        print('FAIL  ' + line)
    print(f'{len(PASS) + len(FAIL)} checks, {len(FAIL)} failures')
    return 1 if FAIL else 0


if __name__ == '__main__':
    sys.exit(main())
