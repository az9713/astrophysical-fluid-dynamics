"""Independent check of Module 14's problem answers and headline numbers.

Imports nothing from m14_numbers.py or m14_solvers.py.  Every expected
value is PARSED from the saved run, .ignore/m14_prep_run.txt, and every
computed value is rebuilt here from the problem statement, with its own
Riemann solver (bisection, not Newton) and its own arithmetic.  A check
that reused the generator's code would reproduce the generator's bugs.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, '..', '..', '.ignore', 'm14_prep_run.txt')
HTML = os.path.join(HERE, '..', 'module14.html')
run = open(RUN, encoding='utf-8').read()
html = open(HTML, encoding='utf-8').read()
n_ok = 0


class Printed(float):
    """A number read off the run, carrying the half-unit of its last digit."""


def grab(pattern):
    m = re.search(pattern, run)
    if not m:
        sys.exit('pattern not in run: ' + pattern)
    txt = m.group(1)
    v = Printed(float(txt))
    mant, _, ex = txt.lower().partition('e')
    dec = len(mant.split('.')[1]) if '.' in mant else 0
    v.half = 0.5*10.0**(-dec + (int(ex) if ex else 0))
    return v


def check(name, got, want, rel=None):
    """Tolerance: half a unit in the last digit the run printed, or rel."""
    global n_ok
    tol = getattr(want, 'half', None) if rel is None else rel*abs(want)
    if tol is None:
        tol = 5e-4*abs(want)
    if abs(got - want) > tol*1.0000001:
        sys.exit(f'FAIL {name}: computed {got!r}, run says {want!r}')
    n_ok += 1
    print(f'ok  {name:44s} {got:.6g}')


def in_html(s):
    global n_ok
    if s not in html:
        sys.exit('FAIL: not printed in module14.html: ' + s)
    n_ok += 1


# --- an independent exact Riemann solver: bisection on the star pressure
def fK(p, r, pk, g):
    c = math.sqrt(g*pk/r)
    if p > pk:
        A, B = 2/((g + 1)*r), (g - 1)/(g + 1)*pk
        return (p - pk)*math.sqrt(A/(p + B))
    return 2*c/(g - 1)*((p/pk)**((g - 1)/(2*g)) - 1)


def star(rl, ul, pl, rr, ur, pr, g):
    lo, hi = 1e-12, 100.0
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if fK(mid, rl, pl, g) + fK(mid, rr, pr, g) + ur - ul > 0:
            hi = mid
        else:
            lo = mid
    p = 0.5*(lo + hi)
    u = 0.5*(ul + ur) + 0.5*(fK(p, rr, pr, g) - fK(p, rl, pl, g))
    return p, u


def rho_star(r, pk, p, g):
    if p > pk:
        b = (g - 1)/(g + 1)
        return r*(p/pk + b)/(b*p/pk + 1)
    return r*(p/pk)**(1/g)


g = 1.4
ps, us = star(1, 0, 1, 0.125, 0, 0.1, g)
check('Sod p*', ps, grab(r'p_star\s+=\s+([\d.]+)'))
check('Sod u*', us, grab(r'u_star\s+=\s+([\d.]+)'))
check('Sod rho*L', rho_star(1, 1, ps, g), grab(r'rho_starL\s+=\s+([\d.]+)'))
check('Sod rho*R', rho_star(0.125, 0.1, ps, g),
      grab(r'rho_starR\s+=\s+([\d.]+)'))
cR = math.sqrt(g*0.1/0.125)
SR = cR*math.sqrt((g + 1)/(2*g)*ps/0.1 + (g - 1)/(2*g))
check('Sod shock speed', SR, grab(r'S_R\s+=\s+([\d.]+)'))
for v in ('0.30313', '0.92745', '0.42632', '0.26557', '1.75216'):
    in_html(v)

# C1
G = math.sqrt(1 + 0.25)
check('C1 FTCS max |G|', G, grab(r'C1  FTCS at C = 0.5: max \|G\| = ([\d.]+)'))
check('C1 steps to 1e3', math.log(1e3)/math.log(G),
      grab(r'steps to grow 1e3 = ([\d.]+)'))
# C2
cL = math.sqrt(1.4)
check('C2 c_L', cL, grab(r'c_L = ([\d.]+)'))
check('C2 dt', 0.9/400/cL, grab(r'dt = 0.9 \(1/400\)/S_max = ([\d.e+-]+)'))
check('C2 steps at that dt', 0.2/(0.9/400/cL),
      grab(r'steps to t = 0.2 at that dt = ([\d.]+)'))
cs_post = math.sqrt(1.4*ps/rho_star(0.125, 0.1, ps, g))
check('C2 post-shock c_s', cs_post, 1.264, rel=5e-4)
# C3
check('C3 Re_num', 2*512/0.2, grab(r'Re_num\(N = 512, C = 0.8\) = ([\d.]+)'))
check('C3 N^(4/3)', 512**(4/3), grab(r'N\^\(4/3\) = ([\d.]+)'))
# K1
p1, u1 = star(1, -2, 0.4, 1, 2, 0.4, g)
check('K1 p*', p1, grab(r'K1  123 problem: p\* = ([\d.]+)'))
check('K1 rho*', rho_star(1, 0.4, p1, g), grab(r'rho\* = ([\d.]+)'))
check('K1 no-vacuum lhs', 5*2*math.sqrt(1.4*0.4), 7.483, rel=1e-4)
# K2
lam8 = 0.19479*1e-2
cells = 4*0.19479/(0.25*lam8)
check('K2 cells per side', cells, grab(r'cells per side = ([\d.]+);'))
check('K2 cells 3D', cells**3, grab(r'3D = ([\d.e+]+)\n'))
# K3, from the contact errors printed in PART D
E32 = grab(r'N =  3200  L1 total [\d.e-]+  fan [\d.e-]+  contact ([\d.e-]+)')
E64 = grab(r'N =  6400  L1 total [\d.e-]+  fan [\d.e-]+  contact ([\d.e-]+)')
o = math.log(E32/E64)/math.log(2)
check('K3 order', o, grab(r'contact order over the last doubling = ([\d.]+)'))
Nt = 6400*(E64/1e-4)**(1/o)
check('K3 N', Nt, grab(r'N for L1 = 1e-4: ([\d.e+]+)'))
check('K3 work ratio', (Nt/6400)**4, grab(r'3D work ratio \(N/6400\)\^4 = '
                                          r'([\d.e+]+)'))
check('K3 first-order ratio', (E64/1e-4)**4, 1.12e3, rel=5e-3)
# headline arithmetic printed in the prose
E100 = grab(r'N =   100  L1 total ([\d.e-]+)')
C100 = grab(r'N =   100  L1 total [\d.e-]+  fan [\d.e-]+  contact ([\d.e-]+)')
T64 = grab(r'N =  6400  L1 total ([\d.e-]+)')
check('contact share N=100', 100*C100/E100, 35.0, rel=2e-3)
check('contact share N=6400', 100*E64/T64, 61.3, rel=2e-3)
check('Sedov peak shortfall', 100*(6 - grab(r'n = 400: peak rho ([\d.]+)'))/6,
      26.6, rel=2e-3)
M = 0.0218/math.sqrt(math.pi*1.4/8)
check('Module 10 Mach', M, grab(r'Mach number U/c_s = ([\d.]+)'))
check('Module 10 step factor', 1 + 1/M, grab(r'= 1 \+ 1/M = ([\d.]+)'))
csmc = math.sqrt(5/3*1.380649e-16*10/(2.33*1.66053906660e-24))
check('cloud factor', 1 + csmc/2.64e5, grab(r'1 \+ 1/M = (1\.0\d+)'))
check('Re_num N=1024 C=0.5', 2*1024/0.5,
      grab(r'N =  1024, C = 0.5: ([\d.]+)'))
check('Re bound N=1024', 1024**(4/3), grab(r'N = 1024: ([\d.e+]+)'))
check('cells for Re=1e6', 1e6**0.75, grab(r'Re\^\(3/4\) = ([\d.e+]+)'))
for v in ('35.01', '1.0924', '0.646', '0.511', '1.013', '0.752', '1.1293',
          '1.0659', '0.0893', '0.0938', '0.0942', '0.0371', '0.0310',
          '0.0216', '3.0559', '3.7619', '4.4010', '1.02764', '1.01365',
          '1.00663', '9.966', '4.096\\times10^{12}', '1.864\\times10^{5}',
          '7.19\\times10^{5}'):
    in_html(v)
print(f'{n_ok} checks passed')
