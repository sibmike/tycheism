"""
Divergence metrics for the Tychism spatial bandit model.

Measures the difference between paired agents (endogenous vs intervened)
across three dimensions: position, Q-map (world model), and cumulative outcome.
"""

import numpy as np

try:
    from ..core.landscape import toroidal_distance
except ImportError:
    from core.landscape import toroidal_distance


def position_distance(pos_a, pos_b, L):
    """Toroidal Euclidean distance between two positions.

    Parameters
    ----------
    pos_a, pos_b : array-like, shape (2,)
    L : int
        Grid side length.

    Returns
    -------
    float
    """
    return toroidal_distance(pos_a, pos_b, L)


def qmap_divergence(Q_a, Q_b):
    """L2 norm of Q-map difference.

    Measures how much the two agents' models of the world differ.

    Parameters
    ----------
    Q_a, Q_b : ndarray[L, L]

    Returns
    -------
    float
    """
    return np.sqrt(np.sum((Q_a - Q_b) ** 2))


def qmap_difference_map(Q_a, Q_b):
    """Pointwise absolute difference between Q-maps.

    For visualization: shows WHERE the agents' world models diverge.

    Returns
    -------
    ndarray[L, L]
    """
    return np.abs(Q_a - Q_b)


def outcome_divergence(o_a, o_b):
    """Absolute difference in cumulative outcomes."""
    return abs(o_a - o_b)


def divergence_timeseries(result, L, t_intervene=0):
    """Compute all divergence metrics over time for a paired run.

    Parameters
    ----------
    result : dict
        Output of run_paired.
    L : int
        Grid side length.
    t_intervene : int
        Timestep of intervention (divergence is meaningful after this).

    Returns
    -------
    dict with keys:
        'timesteps': ndarray[T]
        'position_dist': ndarray[T] — toroidal distance at each t
        'outcome_div': ndarray[T] — cumulative outcome divergence at each t
    """
    pos_a = result['positions_a']
    pos_b = result['positions_b']
    T = len(pos_a)

    timesteps = np.arange(T)
    pos_dist = np.array([
        position_distance(pos_a[t], pos_b[t], L) for t in range(T)
    ])

    # Cumulative outcome divergence
    enc_a = result['agent_a'].get_encounter_history()
    enc_b = result['agent_b'].get_encounter_history()
    cum_a = np.cumsum(enc_a)
    cum_b = np.cumsum(enc_b)
    outcome_div = np.abs(cum_a - cum_b)

    return {
        'timesteps': timesteps,
        'position_dist': pos_dist,
        'outcome_div': outcome_div,
    }


def batch_divergence_timeseries(results, L, t_intervene=0):
    """Compute divergence timeseries for a batch of paired runs.

    Returns mean and std across seeds for each metric.

    Parameters
    ----------
    results : list of dict
        Output of run_paired_batch.
    L : int
    t_intervene : int

    Returns
    -------
    dict with keys:
        'timesteps': ndarray[T]
        'position_dist_mean': ndarray[T]
        'position_dist_std': ndarray[T]
        'outcome_div_mean': ndarray[T]
        'outcome_div_std': ndarray[T]
    """
    all_series = [divergence_timeseries(r, L, t_intervene) for r in results]
    T = len(all_series[0]['timesteps'])

    pos_dists = np.array([s['position_dist'] for s in all_series])
    outcome_divs = np.array([s['outcome_div'] for s in all_series])

    return {
        'timesteps': all_series[0]['timesteps'],
        'position_dist_mean': pos_dists.mean(axis=0),
        'position_dist_std': pos_dists.std(axis=0),
        'outcome_div_mean': outcome_divs.mean(axis=0),
        'outcome_div_std': outcome_divs.std(axis=0),
    }
