"""
Landscape generation for the Tycheism spatial bandit model.

Each landscape is a 2D grid where every cell has a hidden bias p(x) in [0, 1].
p(x) is the probability that an encounter at cell x yields +1 (vs -1).
The agent never observes p(x) directly — only the coin flip outcomes.

Five topologies are supported, each producing qualitatively different
dynamics under encounter-selection coupling.
"""

import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.special import expit  # sigmoid


def generate_landscape(topology, L, seed=42, **params):
    """Generate a landscape p[L, L] with values in [0, 1].

    Parameters
    ----------
    topology : str
        One of 'smooth', 'cliff', 'island', 'deceptive', 'nonstationary'.
        For 'nonstationary', returns a callable p(t) -> ndarray[L, L].
    L : int
        Grid side length. Grid is L x L with toroidal (periodic) boundaries.
    seed : int
        Random seed for reproducibility.
    **params : dict
        Topology-specific parameters (see individual functions).

    Returns
    -------
    p : ndarray[L, L] or callable
        Bias map with p(x) in [0, 1]. For 'nonstationary', returns
        a function that takes timestep t and returns p[L, L].
    """
    generators = {
        'smooth': _smooth,
        'cliff': _cliff,
        'island': _island,
        'deceptive': _deceptive,
        'nonstationary': _nonstationary,
    }
    if topology not in generators:
        raise ValueError(f"Unknown topology: {topology}. Choose from {list(generators)}")
    return generators[topology](L, seed, **params)


def _smooth(L, seed, length_scale=None, **_):
    """Smooth gradient landscape via Gaussian process -> sigmoid.

    High-p regions surrounded by gradually improving neighbors.
    Agent can follow the gradient to find good regions.

    Parameters
    ----------
    length_scale : float, optional
        Controls smoothness. Default: L/4.
    """
    if length_scale is None:
        length_scale = L / 4
    rng = np.random.default_rng(seed)
    raw = rng.standard_normal((L, L))
    smoothed = gaussian_filter(raw, sigma=length_scale, mode='wrap')
    # Normalize to zero mean, unit variance before sigmoid
    smoothed = (smoothed - smoothed.mean()) / (smoothed.std() + 1e-8)
    return expit(smoothed)  # maps to [0, 1]


def _cliff(L, seed, interior_radius=None, cliff_drop=0.1, **_):
    """Smooth interior with sharp boundary drops.

    Interior has high p (via smooth GP). At the boundary, p drops
    sharply to cliff_drop. No transition zone.

    The agent in the interior builds high Q-values from consistently
    good encounters but has no information about what lies past the
    boundary — Q at the boundary cells is at the prior, not at the
    true (catastrophic) value.

    Parameters
    ----------
    interior_radius : float, optional
        Radius of the safe interior region. Default: L/3.
    cliff_drop : float
        The low p value outside the boundary.
    """
    if interior_radius is None:
        interior_radius = L / 3
    # Start with smooth interior
    base = _smooth(L, seed)
    # Scale interior to [0.6, 0.95] — consistently good
    base = 0.6 + 0.35 * (base - base.min()) / (base.max() - base.min() + 1e-8)
    # Create circular boundary mask
    center = L / 2
    y, x = np.mgrid[0:L, 0:L]
    # Toroidal distance from center
    dx = np.minimum(np.abs(x - center), L - np.abs(x - center))
    dy = np.minimum(np.abs(y - center), L - np.abs(y - center))
    dist = np.sqrt(dx**2 + dy**2)
    # Sharp drop: interior = base, exterior = cliff_drop
    mask = dist <= interior_radius
    p = np.where(mask, base, cliff_drop)
    return p


def _island(L, seed, n_peaks=4, peak_width=None, peak_height=0.9,
            background=0.2, **_):
    """Isolated high-p peaks separated by low-p terrain.

    Multiple local optima. Agent on a low-p island builds accurate
    local Q but cannot see that better islands exist. Escape requires
    high τ (random exploration) or external information (I_K+).

    Parameters
    ----------
    n_peaks : int
        Number of high-p islands.
    peak_width : float, optional
        Width (sigma) of each Gaussian peak. Default: L/10.
    peak_height : float
        Maximum p at peak centers.
    background : float
        Base p value between islands.
    """
    if peak_width is None:
        peak_width = L / 10
    rng = np.random.default_rng(seed)
    p = np.full((L, L), background)
    # Place peaks at random positions
    peaks = rng.integers(0, L, size=(n_peaks, 2))
    y, x = np.mgrid[0:L, 0:L]
    for py, px in peaks:
        # Toroidal distance
        dx = np.minimum(np.abs(x - px), L - np.abs(x - px))
        dy = np.minimum(np.abs(y - py), L - np.abs(y - py))
        dist_sq = dx**2 + dy**2
        peak_contribution = (peak_height - background) * np.exp(-dist_sq / (2 * peak_width**2))
        p = np.maximum(p, background + peak_contribution)
    return np.clip(p, 0, 1)


def _deceptive(L, seed, **_):
    """Local gradient of p points away from global maximum.

    The global optimum is at the center, but the local gradient everywhere
    points outward — the further from center, the higher the local gradient
    suggests you should go. An agent following improving Q-values moves
    confidently in the wrong direction.

    Constructed as concentric rings with decreasing peak p but increasing
    local gradient.
    """
    center = L / 2
    y, x = np.mgrid[0:L, 0:L]
    # Toroidal distance from center
    dx = np.minimum(np.abs(x - center), L - np.abs(x - center))
    dy = np.minimum(np.abs(y - center), L - np.abs(y - center))
    dist = np.sqrt(dx**2 + dy**2)
    max_dist = L / 2
    # The trick: local gradient increases with distance, but absolute p
    # has a global max at center. Use a sinusoidal + decay:
    # - Global envelope decreases from center (p highest at center)
    # - Local oscillation creates ridges where gradient points outward
    n_rings = 4
    envelope = 0.9 - 0.5 * (dist / max_dist)  # decreasing from center
    oscillation = 0.15 * np.sin(2 * np.pi * n_rings * dist / max_dist)
    # The deception: between rings, local gradient points outward
    # because the next ring outward has a higher local peak than the
    # current valley, even though the envelope is lower
    p = envelope + oscillation
    return np.clip(p, 0.05, 0.95)


def _nonstationary(L, seed, base_topology='smooth', drift_magnitude=0.01,
                   drift_seed=None, **base_params):
    """Base landscape with temporal drift.

    Returns a callable that takes timestep t and returns p[L, L] at that time.
    The drift is a smooth random field added incrementally, causing the
    landscape to shift. An agent's Q-map becomes stale as the landscape
    it was trained on changes underneath it.

    Parameters
    ----------
    base_topology : str
        Starting topology. Default: 'smooth'.
    drift_magnitude : float
        Standard deviation of drift per timestep.
    drift_seed : int, optional
        Separate seed for drift process.
    """
    p_base = generate_landscape(base_topology, L, seed, **base_params)
    if drift_seed is None:
        drift_seed = seed + 1000
    drift_rng = np.random.default_rng(drift_seed)

    # Pre-generate a smooth drift field per timestep would be too expensive.
    # Instead, use a running drift state that accumulates smooth noise.
    drift_state = {'cumulative': np.zeros((L, L)), 'rng': drift_rng}

    def p_at_t(t):
        # Lazily accumulate drift up to time t
        # For efficiency, store the last computed timestep
        if not hasattr(p_at_t, '_cache_t'):
            p_at_t._cache_t = 0
            p_at_t._cache_p = p_base.copy()
            p_at_t._drift_cum = np.zeros((L, L))
        while p_at_t._cache_t < t:
            raw_drift = drift_state['rng'].standard_normal((L, L))
            smooth_drift = gaussian_filter(raw_drift, sigma=L/8, mode='wrap')
            smooth_drift *= drift_magnitude
            p_at_t._drift_cum += smooth_drift
            p_at_t._cache_t += 1
        p_at_t._cache_p = np.clip(p_base + p_at_t._drift_cum, 0, 1)
        return p_at_t._cache_p

    return p_at_t


def toroidal_distance(x1, x2, L):
    """Euclidean distance on a torus of side length L.

    Parameters
    ----------
    x1, x2 : array-like, shape (2,)
        Positions as (row, col).
    L : int
        Grid side length.

    Returns
    -------
    float
        Shortest distance on the torus.
    """
    d = np.abs(np.array(x1) - np.array(x2))
    d = np.minimum(d, L - d)
    return np.sqrt(np.sum(d**2))
