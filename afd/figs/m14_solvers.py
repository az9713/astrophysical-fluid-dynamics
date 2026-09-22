"""Module 14 solvers, kept apart from m14_numbers.py so that the numbers
script reads as a list of claims and this file as the codes they are made
with.  Every scheme here is one-dimensional and uses numpy only
(.ignore/m14-promises.md, constraint 1: "cap it at one module").

    riemann_star, riemann_sample   the exact Riemann solver (PART C)
    godunov_planar                 first-order Godunov, planar (PART D)
    godunov_spherical              the same scheme in spherical geometry
                                   (PART E, the Sedov problem)
    sph_shock_tube                 one-dimensional SPH (PART F)
    upwind_step, ftcs_step         the linear schemes of PARTS A and B
"""

import numpy as np


# =========================================================================
# The linear schemes for u_t + a u_x = 0, periodic, a > 0.
# =========================================================================

def upwind_step(u, C):
    """One step of the first-order upwind scheme at Courant number C."""
    return u - C*(u - np.roll(u, 1))


def ftcs_step(u, C):
    """One step of forward-time centred-space: unstable at every C > 0."""
    return u - 0.5*C*(np.roll(u, -1) - np.roll(u, 1))


def amplification_upwind(theta, C):
    """G(theta) = 1 - C (1 - e^{-i theta}) for the upwind scheme."""
    return 1.0 - C*(1.0 - np.exp(-1j*theta))


def amplification_ftcs(theta, C):
    """G(theta) = 1 - i C sin(theta) for FTCS."""
    return 1.0 - 1j*C*np.sin(theta)


# =========================================================================
# The exact Riemann solver for the Euler equations, ideal gas.
#
# The shock branch is Module 8's Rankine-Hugoniot conditions solved for the
# velocity jump at given pressure jump; the rarefaction branch is the
# isentropic Riemann invariant u + 2c/(gamma-1).  Both are functions of the
# star pressure p, and the star pressure is the root of
#     f_L(p) + f_R(p) + (u_R - u_L) = 0.
# Vectorised: every argument may be an array (one Riemann problem per
# cell interface).
# =========================================================================

def _f_and_df(p, rK, pK, cK, g):
    A = 2.0/((g + 1.0)*rK)
    B = (g - 1.0)/(g + 1.0)*pK
    shock = p > pK
    ps = np.where(shock, p, pK + 1.0)          # keep the unused branch finite
    pr = np.where(shock, pK, p)
    sq = np.sqrt(A/(ps + B))
    f_sh = (ps - pK)*sq
    df_sh = sq*(1.0 - 0.5*(ps - pK)/(B + ps))
    ratio = pr/pK
    f_ra = 2.0*cK/(g - 1.0)*(ratio**((g - 1.0)/(2.0*g)) - 1.0)
    df_ra = 1.0/(rK*cK)*ratio**(-(g + 1.0)/(2.0*g))
    return np.where(shock, f_sh, f_ra), np.where(shock, df_sh, df_ra)


def riemann_star(rL, uL, pL, rR, uR, pR, g, iters=60):
    """Star pressure and velocity of the Riemann problem (vectorised)."""
    rL, uL, pL, rR, uR, pR = (np.asarray(v, dtype=float)
                              for v in (rL, uL, pL, rR, uR, pR))
    cL = np.sqrt(g*pL/rL)
    cR = np.sqrt(g*pR/rR)
    if np.any(2.0/(g - 1.0)*(cL + cR) <= uR - uL):
        raise ValueError('vacuum is generated; not handled')
    # the primitive-variable guess, floored
    p = 0.5*(pL + pR) - 0.125*(uR - uL)*(rL + rR)*(cL + cR)
    p = np.maximum(p, 1e-6*np.minimum(pL, pR))
    for _ in range(iters):
        fL, dL = _f_and_df(p, rL, pL, cL, g)
        fR, dR = _f_and_df(p, rR, pR, cR, g)
        dp = (fL + fR + uR - uL)/(dL + dR)
        p_new = np.maximum(p - dp, 1e-3*p)
        if np.all(np.abs(p_new - p) <= 1e-15*p_new):
            p = p_new
            break
        p = p_new
    fL, _ = _f_and_df(p, rL, pL, cL, g)
    fR, _ = _f_and_df(p, rR, pR, cR, g)
    u = 0.5*(uL + uR) + 0.5*(fR - fL)
    return p, u


def riemann_sample(xi, rL, uL, pL, rR, uR, pR, g, star=None):
    """Exact solution (rho, u, p) at similarity coordinate xi = x/t.

    Vectorised over xi and over the states.  Returns also the star values.
    """
    rL, uL, pL, rR, uR, pR, xi = (np.asarray(v, dtype=float)
                                  for v in (rL, uL, pL, rR, uR, pR, xi))
    ps, us = riemann_star(rL, uL, pL, rR, uR, pR, g) if star is None else star
    cL = np.sqrt(g*pL/rL)
    cR = np.sqrt(g*pR/rR)
    gm = (g - 1.0)/(g + 1.0)

    # ---- left side of the contact
    shL = ps > pL
    rsL_sh = rL*(ps/pL + gm)/(gm*ps/pL + 1.0)
    SL = uL - cL*np.sqrt((g + 1.0)/(2.0*g)*ps/pL + (g - 1.0)/(2.0*g))
    rsL_ra = rL*(ps/pL)**(1.0/g)
    csL = cL*(ps/pL)**((g - 1.0)/(2.0*g))
    SHL = uL - cL
    STL = us - csL
    # inside the left fan
    fac = 2.0/(g + 1.0) + gm/cL*(uL - xi)
    r_fanL = rL*np.maximum(fac, 0.0)**(2.0/(g - 1.0))
    u_fanL = 2.0/(g + 1.0)*(cL + (g - 1.0)/2.0*uL + xi)
    p_fanL = pL*np.maximum(fac, 0.0)**(2.0*g/(g - 1.0))

    left_r = np.where(shL,
                      np.where(xi < SL, rL, rsL_sh),
                      np.where(xi < SHL, rL,
                               np.where(xi < STL, r_fanL, rsL_ra)))
    left_u = np.where(shL,
                      np.where(xi < SL, uL, us),
                      np.where(xi < SHL, uL,
                               np.where(xi < STL, u_fanL, us)))
    left_p = np.where(shL,
                      np.where(xi < SL, pL, ps),
                      np.where(xi < SHL, pL,
                               np.where(xi < STL, p_fanL, ps)))

    # ---- right side of the contact
    shR = ps > pR
    rsR_sh = rR*(ps/pR + gm)/(gm*ps/pR + 1.0)
    SR = uR + cR*np.sqrt((g + 1.0)/(2.0*g)*ps/pR + (g - 1.0)/(2.0*g))
    rsR_ra = rR*(ps/pR)**(1.0/g)
    csR = cR*(ps/pR)**((g - 1.0)/(2.0*g))
    SHR = uR + cR
    STR = us + csR
    fac = 2.0/(g + 1.0) - gm/cR*(uR - xi)
    r_fanR = rR*np.maximum(fac, 0.0)**(2.0/(g - 1.0))
    u_fanR = 2.0/(g + 1.0)*(-cR + (g - 1.0)/2.0*uR + xi)
    p_fanR = pR*np.maximum(fac, 0.0)**(2.0*g/(g - 1.0))

    right_r = np.where(shR,
                       np.where(xi > SR, rR, rsR_sh),
                       np.where(xi > SHR, rR,
                                np.where(xi > STR, r_fanR, rsR_ra)))
    right_u = np.where(shR,
                       np.where(xi > SR, uR, us),
                       np.where(xi > SHR, uR,
                                np.where(xi > STR, u_fanR, us)))
    right_p = np.where(shR,
                       np.where(xi > SR, pR, ps),
                       np.where(xi > SHR, pR,
                                np.where(xi > STR, p_fanR, ps)))

    left = xi <= us
    r = np.where(left, left_r, right_r)
    u = np.where(left, left_u, right_u)
    p = np.where(left, left_p, right_p)
    return r, u, p, ps, us


def riemann_waves(rL, uL, pL, rR, uR, pR, g):
    """Wave speeds and star densities of one Riemann problem (scalars).

    Returns a dict: p_star, u_star, rho_starL, rho_starR, and the speeds of
    whichever waves exist (shock or rarefaction head/tail on each side).
    """
    ps, us = riemann_star(rL, uL, pL, rR, uR, pR, g)
    ps, us = float(ps), float(us)
    cL = np.sqrt(g*pL/rL)
    cR = np.sqrt(g*pR/rR)
    gm = (g - 1.0)/(g + 1.0)
    out = {'p_star': ps, 'u_star': us}
    if ps > pL:
        out['rho_starL'] = rL*(ps/pL + gm)/(gm*ps/pL + 1.0)
        out['S_L'] = uL - cL*np.sqrt((g + 1.0)/(2.0*g)*ps/pL
                                     + (g - 1.0)/(2.0*g))
    else:
        out['rho_starL'] = rL*(ps/pL)**(1.0/g)
        out['S_HL'] = uL - cL
        out['S_TL'] = us - cL*(ps/pL)**((g - 1.0)/(2.0*g))
    if ps > pR:
        out['rho_starR'] = rR*(ps/pR + gm)/(gm*ps/pR + 1.0)
        out['S_R'] = uR + cR*np.sqrt((g + 1.0)/(2.0*g)*ps/pR
                                     + (g - 1.0)/(2.0*g))
    else:
        out['rho_starR'] = rR*(ps/pR)**(1.0/g)
        out['S_HR'] = uR + cR
        out['S_TR'] = us + cR*(ps/pR)**((g - 1.0)/(2.0*g))
    return out


# =========================================================================
# Godunov's method: conservative finite volumes, exact Riemann flux.
# =========================================================================

def _prim(U, g):
    r = U[0]
    u = U[1]/r
    p = (g - 1.0)*(U[2] - 0.5*r*u*u)
    return r, u, p


def _flux_from_prim(r, u, p, g):
    E = p/(g - 1.0) + 0.5*r*u*u
    return np.array([r*u, r*u*u + p, u*(E + p)])


def godunov_flux(rl, ul, pl, rr, ur, pr, g):
    """Flux at each interface from the exact solution sampled at x/t = 0."""
    r, u, p, _, _ = riemann_sample(0.0*rl, rl, ul, pl, rr, ur, pr, g)
    return _flux_from_prim(r, u, p, g)


def godunov_planar(rho0, u0, p0, dx, t_end, g, C=0.9, record_dt=False):
    """First-order Godunov on a uniform planar grid, transmissive ends.

    Returns (rho, u, p) at t_end and, if record_dt, the list of steps.
    """
    U = np.array([rho0, rho0*u0, p0/(g - 1.0) + 0.5*rho0*u0*u0])
    t = 0.0
    dts = []
    while t < t_end - 1e-14:
        r, u, p = _prim(U, g)
        c = np.sqrt(g*p/r)
        dt = C*dx/np.max(np.abs(u) + c)
        dt = min(dt, t_end - t)
        # ghost cells: copy the end values
        rg = np.concatenate(([r[0]], r, [r[-1]]))
        ug = np.concatenate(([u[0]], u, [u[-1]]))
        pg = np.concatenate(([p[0]], p, [p[-1]]))
        F = godunov_flux(rg[:-1], ug[:-1], pg[:-1], rg[1:], ug[1:], pg[1:], g)
        U = U - dt/dx*(F[:, 1:] - F[:, :-1])
        t += dt
        dts.append(dt)
    r, u, p = _prim(U, g)
    if record_dt:
        return r, u, p, np.array(dts)
    return r, u, p


def godunov_spherical(n, r_out, E0, rho_amb, p_amb, t_end, g, C=0.5,
                      n_hot=1):
    """First-order Godunov in spherical symmetry: the Sedov point blast.

    Finite volumes of volume (r+^3 - r-^3)/3 per steradian, face areas r^2.
    The momentum equation carries the geometric source p (r+^2 - r-^2)/V,
    which is the cell integral of 2 p r and makes a uniform pressure an
    exact steady state.  The energy E0 is deposited as thermal energy in
    the innermost n_hot cells.  The centre face has zero area, so no flux
    crosses it; the outer face is transmissive.

    Returns (r_centres, rho, u, p, total_energy_history).
    """
    edges = np.linspace(0.0, r_out, n + 1)
    rc = 0.5*(edges[1:] + edges[:-1])
    V = (edges[1:]**3 - edges[:-1]**3)/3.0          # per steradian
    A = edges**2
    rho = np.full(n, rho_amb)
    u = np.zeros(n)
    p = np.full(n, p_amb)
    V_hot = 4.0*np.pi*np.sum(V[:n_hot])
    p[:n_hot] = (g - 1.0)*E0/V_hot
    U = np.array([rho, rho*u, p/(g - 1.0) + 0.5*rho*u*u])
    dr = edges[1] - edges[0]
    t = 0.0
    energy = []
    while t < t_end - 1e-14:
        r, u, p = _prim(U, g)
        c = np.sqrt(g*p/r)
        dt = C*dr/np.max(np.abs(u) + c)
        dt = min(dt, t_end - t)
        # ghost at the centre: mirror (reflecting); at the edge: copy
        rg = np.concatenate(([r[0]], r, [r[-1]]))
        ug = np.concatenate(([-u[0]], u, [u[-1]]))
        pg = np.concatenate(([p[0]], p, [p[-1]]))
        F = godunov_flux(rg[:-1], ug[:-1], pg[:-1], rg[1:], ug[1:], pg[1:], g)
        AF = F*A
        dU = -(AF[:, 1:] - AF[:, :-1])/V
        dU[1] += p*(A[1:] - A[:-1])/V
        U = U + dt*dU
        t += dt
        energy.append(4.0*np.pi*np.sum(U[2]*V))
    r, u, p = _prim(U, g)
    return rc, r, u, p, np.array(energy)


# =========================================================================
# Smoothed particle hydrodynamics in one dimension.
# =========================================================================

def kernel_m4(x, h):
    """The M4 cubic spline in 1D, normalisation 2/(3h), support 2h.

    Returns (W, dW/dx).
    """
    q = np.abs(x)/h
    s = np.sign(x)
    w = np.where(q < 1.0, 1.0 - 1.5*q*q + 0.75*q**3,
                 np.where(q < 2.0, 0.25*(2.0 - q)**3, 0.0))
    dw = np.where(q < 1.0, -3.0*q + 2.25*q*q,
                  np.where(q < 2.0, -0.75*(2.0 - q)**2, 0.0))
    norm = 2.0/(3.0*h)
    return norm*w, norm*dw*s/h


def _pairs(n, K):
    i = np.concatenate([np.arange(n - k) for k in range(1, K + 1)])
    j = np.concatenate([np.arange(k, n) for k in range(1, K + 1)])
    return i, j


def sph_density(x, m, h_guess, eta, pairs, n_iter=6):
    """Density by the kernel sum with h = eta m/rho, fixed-point iterated."""
    i, j = pairs
    h = h_guess.copy()
    for _ in range(n_iter):
        rho = m*kernel_m4(0.0*x, h)[0]
        wi = kernel_m4(x[i] - x[j], h[i])[0]
        wj = kernel_m4(x[j] - x[i], h[j])[0]
        np.add.at(rho, i, m*wi)
        np.add.at(rho, j, m*wj)
        h = eta*m/rho
    return rho, h


def sph_accelerations(x, v, uth, m, h, rho, g, pairs, alpha=1.0, beta=2.0,
                      alpha_u=0.0):
    """dv/dt and du/dt for SPH with Monaghan's artificial viscosity and,
    if alpha_u > 0, an artificial thermal conductivity on u.

    Kernel gradients are the average of the two particles' kernels, which
    keeps every pair force antisymmetric: momentum is conserved exactly.
    """
    i, j = pairs
    P = (g - 1.0)*rho*uth
    cs = np.sqrt(g*P/rho)
    xij = x[i] - x[j]
    vij = v[i] - v[j]
    dWi = kernel_m4(xij, h[i])[1]
    dWj = kernel_m4(xij, h[j])[1]
    dW = 0.5*(dWi + dWj)                      # d/dx_i of the mean kernel
    hb = 0.5*(h[i] + h[j])
    rhob = 0.5*(rho[i] + rho[j])
    cb = 0.5*(cs[i] + cs[j])
    vx = vij*xij
    mu = np.where(vx < 0.0, hb*vx/(xij*xij + 0.01*hb*hb), 0.0)
    Pi = (-alpha*cb*mu + beta*mu*mu)/rhob
    term = P[i]/rho[i]**2 + P[j]/rho[j]**2 + Pi
    fpair = m*term*dW
    acc = np.zeros_like(x)
    np.add.at(acc, i, -fpair)
    np.add.at(acc, j, fpair)
    du = np.zeros_like(x)
    np.add.at(du, i, m*(P[i]/rho[i]**2 + 0.5*Pi)*vij*dW)
    np.add.at(du, j, m*(P[j]/rho[j]**2 + 0.5*Pi)*vij*dW)
    if alpha_u > 0.0:
        vsig = np.sqrt(np.abs(P[i] - P[j])/rhob)
        # dW*sign(xij) is dW/d|x|, negative: heat flows from hot to cold
        cond = m*alpha_u*vsig*(uth[i] - uth[j])/rhob*dW*np.sign(xij)
        np.add.at(du, i, cond)
        np.add.at(du, j, -cond)
    return acc, du, cs


def sph_shock_tube(n_left, rhoL, pL, rhoR, pR, g, t_end, x_lo=-0.5,
                   x_mid=0.5, x_hi=1.5, eta=1.2, alpha=1.0, beta=2.0,
                   alpha_u=0.0, CFL=0.2, n_frozen=6, K=40):
    """Equal-mass SPH particles, Sod-type tube, ends frozen.

    n_left particles per unit length on the left; the right spacing is set
    by the density ratio so that every particle has the same mass.
    Returns (x, rho, v, P, u) at t_end.
    """
    dxL = 1.0/n_left
    m = rhoL*dxL
    dxR = m/rhoR
    xl = np.arange(x_lo + 0.5*dxL, x_mid, dxL)
    xr = np.arange(x_mid + 0.5*dxR, x_hi, dxR)
    x = np.concatenate((xl, xr))
    n = x.size
    v = np.zeros(n)
    uth = np.concatenate((np.full(xl.size, pL/((g - 1.0)*rhoL)),
                          np.full(xr.size, pR/((g - 1.0)*rhoR))))
    h = eta*np.concatenate((np.full(xl.size, dxL), np.full(xr.size, dxR)))
    pairs = _pairs(n, K)
    frozen = np.zeros(n, bool)
    frozen[:n_frozen] = True
    frozen[-n_frozen:] = True
    rho, h = sph_density(x, m, h, eta, pairs)
    acc, du, cs = sph_accelerations(x, v, uth, m, h, rho, g, pairs,
                                    alpha, beta, alpha_u)
    t = 0.0
    while t < t_end - 1e-14:
        dt = CFL*np.min(h/(cs + np.abs(v) + 1e-30))
        dt = min(dt, t_end - t)
        # kick-drift-kick
        v_half = v + 0.5*dt*np.where(frozen, 0.0, acc)
        u_half = uth + 0.5*dt*np.where(frozen, 0.0, du)
        x = x + dt*np.where(frozen, 0.0, v_half)
        rho, h = sph_density(x, m, h, eta, pairs, n_iter=3)
        acc, du, cs = sph_accelerations(x, v_half, u_half, m, h, rho, g,
                                        pairs, alpha, beta, alpha_u)
        v = v_half + 0.5*dt*np.where(frozen, 0.0, acc)
        uth = u_half + 0.5*dt*np.where(frozen, 0.0, du)
        t += dt
    P = (g - 1.0)*rho*uth
    return x, rho, v, P, uth, m
