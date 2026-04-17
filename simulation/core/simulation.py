"""
Simulation runner for the Tycheism spatial bandit model.

Provides paired comparison experiments: run two identical agents on the
same landscape, intervene on one at time t_intervene, measure trajectory
divergence from t_intervene to horizon H.

The paired design isolates the effect of intervention from baseline
stochastic variation.
"""

import numpy as np
from .agent import Agent
from . import interventions as ops


def run_single(landscape, L, x0, tau, alpha, q_prior, H, seed):
    """Run a single agent for H timesteps.

    Returns
    -------
    agent : Agent
        The agent after H steps, with full history.
    """
    agent = Agent(L=L, x0=x0, tau=tau, alpha=alpha, q_prior=q_prior, rng=seed)
    for _ in range(H):
        agent.step(landscape)
    return agent


def run_paired(landscape, L, x0, tau, alpha, q_prior, H,
               intervention_fn, t_intervene, seed):
    """Run a paired comparison: two identical agents, intervene on one.

    Both agents start with the same state and RNG. They run identically
    until t_intervene. At t_intervene, intervention_fn is applied to
    agent_b (the intervened agent). Both continue to H.

    Parameters
    ----------
    landscape : ndarray[L, L] or callable
        Bias map p(x).
    L : int
        Grid size.
    x0 : tuple of int
        Starting position.
    tau, alpha, q_prior : float
        Agent parameters.
    H : int
        Total simulation horizon.
    intervention_fn : callable
        Function(agent) -> None. Applied to agent_b at t_intervene.
    t_intervene : int
        Timestep at which to intervene.
    seed : int
        Random seed.

    Returns
    -------
    dict with keys:
        'agent_a': Agent (endogenous, no intervention)
        'agent_b': Agent (intervened)
        'positions_a': ndarray[H, 2]
        'positions_b': ndarray[H, 2]
        'q_final_a': ndarray[L, L]
        'q_final_b': ndarray[L, L]
    """
    agent_a = Agent(L=L, x0=x0, tau=tau, alpha=alpha, q_prior=q_prior, rng=seed)

    # Run agent_a up to t_intervene
    for _ in range(t_intervene):
        agent_a.step(landscape)

    # Clone to create agent_b with identical state
    agent_b = agent_a.clone()

    # Apply intervention to agent_b
    intervention_fn(agent_b)

    # Run both from t_intervene to H
    for _ in range(t_intervene, H):
        agent_a.step(landscape)
        agent_b.step(landscape)

    return {
        'agent_a': agent_a,
        'agent_b': agent_b,
        'positions_a': agent_a.get_position_history(),
        'positions_b': agent_b.get_position_history(),
        'q_final_a': agent_a.get_q_snapshot(),
        'q_final_b': agent_b.get_q_snapshot(),
    }


def run_paired_batch(landscape, L, x0, tau, alpha, q_prior, H,
                     intervention_fn, t_intervene, n_seeds, base_seed=0):
    """Run multiple paired comparisons with different random seeds.

    Parameters
    ----------
    n_seeds : int
        Number of independent runs.
    base_seed : int
        Seeds used are base_seed, base_seed+1, ..., base_seed+n_seeds-1.

    Returns
    -------
    list of dict
        One result dict per seed (same format as run_paired).
    """
    results = []
    for i in range(n_seeds):
        result = run_paired(
            landscape=landscape, L=L, x0=x0, tau=tau, alpha=alpha,
            q_prior=q_prior, H=H, intervention_fn=intervention_fn,
            t_intervene=t_intervene, seed=base_seed + i,
        )
        results.append(result)
    return results


def run_sweep(landscape, L, x0, q_prior, H, intervention_fn, t_intervene,
              param_name, param_values, n_seeds=20, base_seed=0, **defaults):
    """Sweep one parameter while holding others at defaults.

    Parameters
    ----------
    param_name : str
        'tau' or 'alpha'.
    param_values : list
        Values to sweep over.
    defaults : dict
        Default values for non-swept parameters.
        Must include 'tau' and 'alpha'.

    Returns
    -------
    dict mapping param_value -> list of result dicts
    """
    sweep_results = {}
    for val in param_values:
        params = dict(defaults)
        params[param_name] = val
        results = run_paired_batch(
            landscape=landscape, L=L, x0=x0,
            tau=params['tau'], alpha=params['alpha'],
            q_prior=q_prior, H=H,
            intervention_fn=intervention_fn,
            t_intervene=t_intervene,
            n_seeds=n_seeds, base_seed=base_seed,
        )
        sweep_results[val] = results
    return sweep_results
