"""cymatics.py — forward models for the Reverse Cymatic Decoder.

Implements the Physics Specification §1 (forward models) and §2.2 (scaling law):

  * Circular membrane (physics spec §1a):
        u_{n,m}(r, θ) = J_n(z_{n,m} · r / R) · cos(nθ + φ)
        f_{n,m}       = z_{n,m} · c / (2πR)
  * Square plate / Chladni approximation (physics spec §1b):
        u_{p,q}(x, y) = sin(pπx/L)·sin(qπy/L)
        f_{p,q}       = (c/2L)·√(p²+q²)               [membrane dispersion]
        f_{p,q}       = (c_flex/L²)·(p²+q²)           [biharmonic plate option]
  * Amplitude rendering / nodal-line extraction (physics spec §1c):
        nodal set = { (x,y) : |A(x,y)| ≤ eps · max|A| }

Bessel zeros z_{n,m} come from scipy.special.jn_zeros throughout its practical
range (n = 0..100, m = 1..20) and from the asymptotic expansion of physics
spec §1a only beyond that (n > 100 or m > 20).  The asymptotic is accurate
only for m ≥ 5, so it must NOT be used for low m at high n (e.g. z_{10,1}
has a +2.4 % error asymptotically).

Only numpy/scipy are used.  SI units throughout; K = c/(2πR) is in Hz.
"""

from __future__ import annotations

import numpy as np
from scipy.special import jn, jn_zeros

#: Practical range of scipy.special.jn_zeros, used for ALL zeros inside it
#: (the physics spec §1a printed table stops at n = 8, m = 6, but jn_zeros
#: is exact far beyond that; the asymptotic expansion is kept only as the
#: true fallback outside this range — it is adequate only for m ≥ 5).
N_MAX_SCIPY = 100
M_MAX_SCIPY = 20

#: Default nodal threshold |A| ≤ eps·max|A| (physics spec §1c: 0.05–0.15).
DEFAULT_EPS = 0.08

_ZERO_CACHE: dict[tuple[int, int], np.ndarray] = {}


def asymptotic_zero(n: int, m: int) -> float:
    """Asymptotic Bessel zero z_{n,m} (physics spec §1a).

        z ≈ β − (μ−1)/(8β) − 4(μ−1)(7μ−31)/(3(8β)³),
        β = π(m + n/2 − 1/4),  μ = 4n²

    Error O(β⁻⁵); adequate for m ≥ 5 at any n.  Used ONLY as the fallback
    beyond scipy's practical range (n > 100 or m > 20); inside that range
    scipy.special.jn_zeros is exact and always preferred.
    """
    n = int(n)
    m = int(m)
    if n < 0 or m < 1:
        raise ValueError("asymptotic_zero: require n ≥ 0 and m ≥ 1")
    beta = np.pi * (m + n / 2.0 - 0.25)
    mu = 4.0 * n * n
    return float(beta - (mu - 1.0) / (8.0 * beta)
                 - 4.0 * (mu - 1.0) * (7.0 * mu - 31.0) / (3.0 * (8.0 * beta) ** 3))


def bessel_zeros(n_max: int = 8, m_max: int = 6) -> np.ndarray:
    """Table Z[n, m-1] = z_{n,m} for n = 0..n_max, m = 1..m_max.

    Uses scipy.special.jn_zeros inside its practical range
    (n ≤ 100, m ≤ 20) and the asymptotic expansion as true fallback beyond
    it (physics spec §1a / §3.2).  Rows are enforced strictly increasing
    in m so the interlacing property z_{n,m} < z_{n,m+1} is preserved at
    the seam.
    """
    n_max = int(n_max)
    m_max = int(m_max)
    if n_max < 0 or m_max < 1:
        raise ValueError("bessel_zeros: require n_max ≥ 0, m_max ≥ 1")
    key = (n_max, m_max)
    if key in _ZERO_CACHE:
        return _ZERO_CACHE[key]
    table = np.zeros((n_max + 1, m_max))
    for n in range(n_max + 1):
        if n <= N_MAX_SCIPY:
            n_exact = min(m_max, M_MAX_SCIPY)
            row = list(jn_zeros(n, n_exact))
            for m in range(M_MAX_SCIPY + 1, m_max + 1):
                row.append(asymptotic_zero(n, m))
        else:
            row = [asymptotic_zero(n, m) for m in range(1, m_max + 1)]
        # Enforce strict monotonicity in m (interlacing, physics spec §1a).
        for m in range(1, m_max):
            if row[m] <= row[m - 1]:
                row[m] = np.nextafter(row[m - 1], np.inf)
        table[n, :] = row
    _ZERO_CACHE[key] = table
    return table


def bessel_zero(n: int, m: int) -> float:
    """Scalar accessor for z_{n,m} (scipy exact + asymptotic fallback)."""
    n = int(n)
    m = int(m)
    if n < 0 or m < 1:
        raise ValueError("bessel_zero: require n ≥ 0 and m ≥ 1")
    if n <= N_MAX_SCIPY and m <= M_MAX_SCIPY:
        return float(jn_zeros(n, m)[m - 1])
    return asymptotic_zero(n, m)


# --------------------------------------------------------------------------
# Circular membrane forward model (physics spec §1a, §1c)
# --------------------------------------------------------------------------

def _validate_nm(n, m):
    n = int(n)
    m = int(m)
    if n < 0:
        raise ValueError("azimuthal order n must be ≥ 0")
    if m < 1:
        raise ValueError("radial order m must be ≥ 1")
    return n, m


def _validate_geometry(R=None, L=None, c=None, eps=None):
    if R is not None and not (np.isfinite(R) and R > 0):
        raise ValueError("resonator radius R must be > 0 (guard rail, physics §3.6)")
    if L is not None and not (np.isfinite(L) and L > 0):
        raise ValueError("plate side L must be > 0 (guard rail, physics §3.6)")
    if c is not None and not (np.isfinite(c) and c > 0):
        raise ValueError("wave speed c must be > 0 (guard rail, physics §3.6)")
    if eps is not None and not (np.isfinite(eps) and eps > 0):
        raise ValueError("nodal threshold eps must be > 0 (guard rail, physics §3.10)")


def membrane_pattern(n, m, R=1.0, res=512, phase=0.0, weight=1.0,
                     eps=DEFAULT_EPS):
    """Render a single circular-membrane mode (physics spec §1a/§1c).

        u_{n,m}(r,θ) = weight · J_n(z_{n,m} r/R) · cos(nθ + phase)

    Returns a dict with keys
        u          signed amplitude (0 outside r > R)
        amplitude  |u|  (time-averaged sand-collecting field)
        nodal      bool mask, |u| ≤ eps·max|u| inside the disk
        inside     bool mask of the disk r ≤ R
        x, y       1-D coordinate axes
        n, m, R, phase, eps   echo of parameters
    """
    n, m = _validate_nm(n, m)
    _validate_geometry(R=R, eps=eps)
    res = int(res)
    if res < 8:
        raise ValueError("res too small to render a pattern")
    z = bessel_zero(n, m)
    x = np.linspace(-R, R, res)
    y = np.linspace(-R, R, res)
    X, Y = np.meshgrid(x, y)
    r = np.hypot(X, Y)
    theta = np.arctan2(Y, X)
    inside = r <= R
    rr = np.where(inside, r, 0.0)
    u = weight * jn(n, z * rr / R) * np.cos(n * theta + phase)
    u = np.where(inside, u, 0.0)
    amp = np.abs(u)
    amax = amp.max()
    nodal = inside & (amp <= eps * amax)
    return dict(u=u, amplitude=amp, nodal=nodal, inside=inside,
                x=x, y=y, n=n, m=m, R=R, phase=phase, eps=eps)


def membrane_superposition(modes, R=1.0, res=512, eps=DEFAULT_EPS):
    """Render a real superposition A(x,y) = Σ_k w_k u_k (physics spec §1c).

    modes: iterable of (n, m, weight, phase) tuples or dicts with keys
    n/m/weight/phase.  Degenerate partners (cos/sin pairs for n ≥ 1) are
    represented by the free phase φ (physics spec §1c: always include both
    members of a degenerate pair).
    """
    _validate_geometry(R=R, eps=eps)
    terms = []
    for md in modes:
        if isinstance(md, dict):
            terms.append((md["n"], md["m"], md.get("weight", 1.0),
                          md.get("phase", 0.0)))
        else:
            n, m = md[0], md[1]
            w = md[2] if len(md) > 2 else 1.0
            ph = md[3] if len(md) > 3 else 0.0
            terms.append((n, m, w, ph))
    if not terms:
        raise ValueError("membrane_superposition: empty mode list")
    acc = None
    for n, m, w, ph in terms:
        pat = membrane_pattern(n, m, R=R, res=res, phase=ph, weight=w, eps=eps)
        acc = pat["u"].copy() if acc is None else acc + pat["u"]
    amp = np.abs(acc)
    amax = amp.max()
    nodal = pat["inside"] & (amp <= eps * amax)
    return dict(u=acc, amplitude=amp, nodal=nodal, inside=pat["inside"],
                x=pat["x"], y=pat["y"], modes=terms, R=R, eps=eps)


# --------------------------------------------------------------------------
# Square plate forward model (physics spec §1b, §1c)
# --------------------------------------------------------------------------

def square_pattern(p, q, L=1.0, res=512, sign=+1, eps=DEFAULT_EPS):
    """Render a square-plate mode including its degenerate partner.

        u = sin(pπx/L)sin(qπy/L) + sign · sin(qπx/L)sin(pπy/L)   (p ≠ q)
        u = sin(pπx/L)sin(qπy/L)                                  (p = q)

    Physics spec §1c: "(p,q) and (q,p) are exactly degenerate; always include
    both members of a degenerate pair."  With p≠q and sign = +1 the nodal set
    contains the anti-diagonal x + y = L; with sign = −1 the diagonal x = y
    (physics spec §4.3 sanity test 3).
    """
    p = int(p)
    q = int(q)
    if p < 1 or q < 1:
        raise ValueError("square mode numbers p, q must be ≥ 1")
    _validate_geometry(L=L, eps=eps)
    res = int(res)
    x = np.linspace(0.0, L, res)
    X, Y = np.meshgrid(x, x)
    u = np.sin(p * np.pi * X / L) * np.sin(q * np.pi * Y / L)
    if p != q and sign != 0:
        u = u + sign * np.sin(q * np.pi * X / L) * np.sin(p * np.pi * Y / L)
    amp = np.abs(u)
    amax = amp.max()
    nodal = amp <= eps * amax
    return dict(u=u, amplitude=amp, nodal=nodal, x=x, y=x,
                p=p, q=q, L=L, sign=sign, eps=eps)


def square_superposition(modes, L=1.0, res=512, eps=DEFAULT_EPS):
    """Superposition of square modes: A = Σ_k w_k sin(p_kπx/L)sin(q_kπy/L).

    modes: iterable of (p, q, weight).
    """
    _validate_geometry(L=L, eps=eps)
    acc = None
    for md in modes:
        p, q = md[0], md[1]
        w = md[2] if len(md) > 2 else 1.0
        x = np.linspace(0.0, L, int(res))
        X, Y = np.meshgrid(x, x)
        term = w * np.sin(int(p) * np.pi * X / L) * np.sin(int(q) * np.pi * Y / L)
        acc = term if acc is None else acc + term
    if acc is None:
        raise ValueError("square_superposition: empty mode list")
    amp = np.abs(acc)
    nodal = amp <= eps * amp.max()
    return dict(u=acc, amplitude=amp, nodal=nodal, x=x, y=x, L=L, eps=eps)


# --------------------------------------------------------------------------
# Frequency mapping (physics spec §2.1 step 5, §2.2 scaling law)
# --------------------------------------------------------------------------

def frequency_membrane(n, m, R, c):
    """f_{n,m} = z_{n,m} · c / (2πR)  (physics spec §1a, §2.1).

    f ∝ 1/R and f ∝ c (scaling law §2.2).  All frequency *ratios*
    f_{n,m}/f_{0,1} = z_{n,m}/z_{0,1} are resonator-independent.
    """
    n, m = _validate_nm(n, m)
    _validate_geometry(R=R, c=c)
    return bessel_zero(n, m) * c / (2.0 * np.pi * R)


def frequency_square(p, q, L, c, dispersion="membrane"):
    """Square-plate frequency (physics spec §1b, §2.1).

    dispersion='membrane' (default, model i):  f = (c/2L)·√(p²+q²),  c in m/s.
    dispersion='plate'   (model ii, biharmonic thin free plate):
        f = (c_flex/L²)·(p²+q²),  where the `c` argument is the flexural
        coefficient c_flex = C·h·√(E/(12ρ(1−ν²))) in m²/s — flexural waves
        are dispersive, so a constant wave speed is *not* used (§1b, §3.8).
        The sin·sin shapes are only an interior ansatz for model (ii).
    """
    p = int(p)
    q = int(q)
    if p < 1 or q < 1:
        raise ValueError("square mode numbers p, q must be ≥ 1")
    _validate_geometry(L=L, c=c)
    s2 = p * p + q * q
    if dispersion == "membrane":
        return (c / (2.0 * L)) * np.sqrt(s2)
    if dispersion == "plate":
        return (c / (L * L)) * float(s2)
    raise ValueError("dispersion must be 'membrane' or 'plate'")


# --------------------------------------------------------------------------
# Reference data helpers
# --------------------------------------------------------------------------

#: Interior nodal-circle radii fingerprint: r_j/R = z_{n,j}/z_{n,m}, j = 1..m−1
#: (physics spec §3.7 — far more discriminating than ring count alone).
def nodal_circle_radii(n, m):
    """Interior nodal-circle radii r_j/R for mode (n,m), j = 1..m−1."""
    n, m = _validate_nm(n, m)
    if m < 2:
        return np.array([])
    return np.array([bessel_zero(n, j) / bessel_zero(n, m)
                     for j in range(1, m)])


def frequency_ratio_membrane(n, m, n_ref=0, m_ref=1):
    """Dimensionless ratio z_{n,m}/z_{n_ref,m_ref} (the PRIMARY output)."""
    return bessel_zero(n, m) / bessel_zero(n_ref, m_ref)
