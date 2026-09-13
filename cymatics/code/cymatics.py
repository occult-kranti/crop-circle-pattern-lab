#!/usr/bin/env python3
"""cymatics.py — forward cymatic simulators (physics spec §1–§4).

Two reference resonators, matching the master spec:

* circular membrane (drumhead):  f_{n,m} = z_{n,m}·c/(2πR)
      z_{n,m} = m-th positive zero of J_n; nodal set =
      {n diameters} ∪ {m−1 interior circles + boundary}
* square plate (thin membrane model): f_{p,q} = (c/2L)·√(p²+q²)
      (an actual thin plate is biharmonic — §1b plate option retained)

Every pattern renderer returns a dict with the displacement field `u`,
the nodal-line mask, and the physical metadata needed downstream
(amplitude normalisation ε·max|u| from physics spec §4.5).
"""

import numpy as np
from scipy.special import jn, jn_zeros

# ---------------------------------------------------------------- zeros

def bessel_zero(n, m):
    """m-th positive zero of J_n (physics spec §1a table, computed).

    scipy.special.jn_zeros covers n ≤ 100, m ≤ 20 comfortably; that is the
    practical decoding range (formations with n > 100 do not occur).  Only
    beyond scipy's range do we fall back to the asymptotic formula — the
    printed §1a table itself (n ≤ 8) is well inside jn_zeros territory, so
    the exact zeros are used everywhere that matters.  (Earlier versions
    used the asymptotic for n > 8, which mis-decoded pattern 9: at (10,1)
    the asymptotic zero errs by +2.35 % — see test_cymatics.py regression.)
    """
    n, m = int(n), int(m)
    if n < 0 or m < 1:
        raise ValueError("need n ≥ 0, m ≥ 1")
    if n <= 100 and m <= 20:
        return float(jn_zeros(n, m)[m - 1])
    return asymptotic_zero(n, m)


def asymptotic_zero(n, m):
    """McMahon asymptotic expansion of z_{n,m} (physics spec §4.8).

    Relative error < 1e-3 for m ≥ 6 (all n), and decent for m ≥ 2.
    μ = 4n²;  β = (m + n/2 − 1/4)π
    z ≈ β − (μ−1)/(8β) − 4(μ−1)(7μ−31)/(3(8β)³)
    """
    n, m = int(n), int(m)
    if n < 0 or m < 1:
        raise ValueError("need n ≥ 0, m ≥ 1")
    mu = 4.0 * n * n
    beta = (m + n / 2.0 - 0.25) * np.pi
    z = (beta - (mu - 1) / (8 * beta)
         - 4 * (mu - 1) * (7 * mu - 31) / (3 * (8 * beta) ** 3))
    return float(z)


# ------------------------------------------------- membrane (drumhead)

def frequency_membrane(n, m, R, c):
    """f_{n,m} = z_{n,m}·c/(2πR)  [Hz].  R in metres, c in m/s."""
    if R <= 0 or c <= 0:
        raise ValueError("R and c must be positive")
    return bessel_zero(n, m) * c / (2.0 * np.pi * R)


def frequency_ratio_membrane(n, m):
    """f_{n,m}/f_{0,1} = z_{n,m}/z_{0,1} (resonator-independent)."""
    return bessel_zero(n, m) / bessel_zero(0, 1)


def membrane_pattern(n, m, R=1.0, res=512, phase=0.0, eps=0.05):
    """Standing-wave pattern u(r,θ) = J_n(z_{n,m} r/R)·cos(nθ+φ).

    phase φ is physically present but unobservable from a nodal photo
    (physics spec §4.6: rotation invariance); default 0.
    Nodal mask: |u| ≤ eps·max|u| inside the membrane (§4.5).
    Returns dict(u, nodal, x, y, r, th, n, m, z, inside, amplitude).
    """
    n, m = int(n), int(m)
    if n < 0 or m < 1:
        raise ValueError("need n ≥ 0, m ≥ 1")
    if eps <= 0:
        raise ValueError("eps must be positive")
    z = bessel_zero(n, m)
    ax = np.linspace(-R, R, res)
    x, y = np.meshgrid(ax, ax)
    r = np.hypot(x, y)
    th = np.arctan2(y, x)
    inside = r <= R
    rr = np.clip(r / R, 0.0, 1.0)
    u = np.zeros_like(r)
    u[inside] = jn(n, z * rr[inside]) * np.cos(n * th[inside] + phase)
    amp = np.abs(u)[inside].max() if inside.any() else 0.0
    nodal = inside & (np.abs(u) <= eps * amp)
    return dict(u=u, nodal=nodal, x=x, y=y, r=r, th=th, n=n, m=m, z=z,
                inside=inside, amplitude=amp)


def membrane_superposition(terms, R=1.0, res=512, eps=0.05):
    """Σ aᵢ·J_{nᵢ}(z_{nᵢ,mᵢ} r/R)·cos(nᵢθ+φᵢ) — spec §7 superposition.

    terms: iterable of (n, m, amplitude, phase).  Used by the decoder's
    honesty path (V12): superpositions must yield *multiple* candidates.
    """
    terms = list(terms)
    if not terms:
        raise ValueError("empty superposition")
    ax = np.linspace(-R, R, res)
    x, y = np.meshgrid(ax, ax)
    r = np.hypot(x, y)
    th = np.arctan2(y, x)
    inside = r <= R
    u = np.zeros_like(r)
    for (n, m, a, phi) in terms:
        z = bessel_zero(n, m)
        rr = np.clip(r / R, 0.0, 1.0)
        u[inside] += a * jn(int(n), z * rr[inside]) * np.cos(int(n) * th[inside] + phi)
    amp = np.abs(u)[inside].max() if inside.any() else 0.0
    nodal = inside & (np.abs(u) <= eps * amp)
    return dict(u=u, nodal=nodal, x=x, y=y, r=r, th=th, inside=inside,
                amplitude=amp, terms=terms)


# ------------------------------------------------------ square plate

def frequency_square(p, q, L, c, dispersion="membrane"):
    """f_{p,q} for the L×L square.

    dispersion='membrane':  f = (c/2L)·√(p²+q²)     (physics spec §1b main)
    dispersion='plate':     f ∝ (p²+q²) (biharmonic thin plate; normalised
                            so that (1,1) matches (c/2L)·√2 — option kept
                            because Chladni plates are really biharmonic).
    """
    p, q = int(p), int(q)
    if p < 1 or q < 1:
        raise ValueError("need p, q ≥ 1 (no n=0 on a clamped square)")
    if L <= 0 or c <= 0:
        raise ValueError("L and c must be positive")
    base = c / (2.0 * L)
    if dispersion == "membrane":
        return base * np.hypot(p, q)
    if dispersion == "plate":
        return base * (p * p + q * q) / np.sqrt(2.0)
    raise ValueError(f"unknown dispersion {dispersion!r}")


def square_pattern(p, q, L=1.0, res=512, sign=+1, eps=0.05):
    """u(x,y) = sin(pπx/L)sin(qπy/L) + sign·sin(qπx/L)sin(pπy/L).

    Degenerate (p,q)/(q,p) superpositions change the nodal topology
    (physics spec §4.3): (1,2)+(2,1) is nodal on the anti-diagonal x+y=L,
    (1,2)−(2,1) on the diagonal x=y.  sign is ignored when p == q.
    """
    p, q = int(p), int(q)
    if p < 1 or q < 1:
        raise ValueError("need p, q ≥ 1")
    if eps <= 0:
        raise ValueError("eps must be positive")
    ax = np.linspace(0.0, L, res)
    x, y = np.meshgrid(ax, ax)
    u = np.sin(p * np.pi * x / L) * np.sin(q * np.pi * y / L)
    if p != q:
        u = u + np.sign(sign) * np.sin(q * np.pi * x / L) * np.sin(p * np.pi * y / L)
    amp = np.abs(u).max()
    inside = np.ones_like(u, dtype=bool)
    nodal = np.abs(u) <= eps * amp
    return dict(u=u, nodal=nodal, x=x, y=y, p=p, q=q, sign=int(np.sign(sign)),
                inside=inside, amplitude=amp)


# --------------------------------------------------------- Chladni helper

def nodal_density(pattern, n_rings=8, n_wedges=32):
    """Azimuthal/radial nodal-density profiles used by the decoder.

    Returns (wedge_profile, ring_profile): nodal-pixel counts per angular
    wedge and per radial ring — the rotation-invariant fingerprint of a
    membrane figure (decoder spec §2.1).
    """
    nodal = pattern["nodal"]
    r, th, inside = pattern["r"], pattern["th"], pattern["inside"]
    R = r[inside].max() if inside.any() else 1.0
    wedges = np.zeros(n_wedges)
    rings = np.zeros(n_rings)
    widx = ((th + np.pi) / (2 * np.pi) * n_wedges).astype(int) % n_wedges
    ridx = np.clip((r / (R + 1e-12) * n_rings).astype(int), 0, n_rings - 1)
    for i in range(n_wedges):
        wedges[i] = (nodal & inside & (widx == i)).sum()
    for i in range(n_rings):
        rings[i] = (nodal & inside & (ridx == i)).sum()
    return wedges, rings
