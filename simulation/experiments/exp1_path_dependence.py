"""
Experiment 1 — Path Dependence

Proposition: Under encounter-selection coupling (finite tau, alpha > 0),
agents with identical initialization but different random seeds produce
divergent trajectories. Divergence grows with coupling strength (lower tau).

Setup: Smooth landscape. N agents, same x0, same Q0. Different seeds.
Sweep: tau in {0.1, 0.5, 1.0, 2.0, 5.0, 50.0}
Measure: Pairwise position distance and Q-map divergence over time.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import numpy as np
from core.landscape import generate_landscape, toroidal_distance
from core.agent import Agent

# Parameters
L = 31
H = 300
N_AGENTS = 50  # agents per tau value
X0 = (15, 15)
ALPHA = 0.1
Q_PRIOR = 0.0
TAU_VALUES = [0.1, 0.5, 1.0, 2.0, 5.0, 50.0]
LANDSCAPE_SEED = 42

# Results storage
results = {}


def run_cohort(landscape, tau, n_agents, H):
    """Run n_agents with same init but different seeds at given tau."""
    agents = []
    for i in range(n_agents):
        agent = Agent(L=L, x0=X0, tau=tau, alpha=ALPHA, q_prior=Q_PRIOR, rng=1000 + i)
        for _ in range(H):
            agent.step(landscape)
        agents.append(agent)
    return agents


def pairwise_position_divergence(agents, L):
    """Mean pairwise toroidal distance between all agent final positions."""
    positions = [a.x for a in agents]
    n = len(positions)
    total = 0.0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += toroidal_distance(positions[i], positions[j], L)
            count += 1
    return total / count if count > 0 else 0.0


def pairwise_qmap_divergence(agents):
    """Mean pairwise L2 Q-map distance."""
    n = len(agents)
    total = 0.0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += np.sqrt(np.sum((agents[i].Q - agents[j].Q) ** 2))
            count += 1
    return total / count if count > 0 else 0.0


def trajectory_spread_over_time(agents, L):
    """Compute mean pairwise distance at each timestep."""
    H = len(agents[0].history)
    n = len(agents)
    spread = np.zeros(H)
    for t in range(H):
        total = 0.0
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                pi = agents[i].history[t]['x']
                pj = agents[j].history[t]['x']
                total += toroidal_distance(pi, pj, L)
                count += 1
            spread[t] = total / count if count > 0 else 0.0
    return spread


if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENT 1: PATH DEPENDENCE")
    print(f"L={L}, H={H}, N_agents={N_AGENTS}, alpha={ALPHA}")
    print("=" * 60)

    landscape = generate_landscape('smooth', L, seed=LANDSCAPE_SEED)
    print(f"Landscape: smooth, p range=[{landscape.min():.3f}, {landscape.max():.3f}]")

    print(f"\n{'tau':>6s} | {'pos_div':>10s} | {'qmap_div':>10s}")
    print("-" * 35)

    all_spreads = {}

    for tau in TAU_VALUES:
        agents = run_cohort(landscape, tau, N_AGENTS, H)
        pos_div = pairwise_position_divergence(agents, L)
        qmap_div = pairwise_qmap_divergence(agents)
        spread = trajectory_spread_over_time(agents, L)
        all_spreads[tau] = spread
        results[tau] = {
            'pos_divergence': pos_div,
            'qmap_divergence': qmap_div,
            'spread_timeseries': spread,
        }
        print(f"{tau:6.1f} | {pos_div:10.3f} | {qmap_div:10.3f}")

    # Verify proposition: divergence should increase as tau decreases
    pos_divs = [results[tau]['pos_divergence'] for tau in TAU_VALUES]
    # Check monotonic trend (allowing some noise)
    low_tau_div = results[0.1]['pos_divergence']
    high_tau_div = results[50.0]['pos_divergence']

    print(f"\nKey comparison:")
    print(f"  tau=0.1 (strong coupling): pos_div = {low_tau_div:.3f}")
    print(f"  tau=50  (weak coupling):   pos_div = {high_tau_div:.3f}")

    if low_tau_div > high_tau_div:
        print("  CONFIRMED: Stronger coupling -> more path dependence")
    else:
        print("  WARNING: Expected stronger coupling to produce more divergence")

    # Save results for figure generation
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
    os.makedirs(output_dir, exist_ok=True)
    np.savez(
        os.path.join(output_dir, 'exp1_path_dependence.npz'),
        tau_values=np.array(TAU_VALUES),
        pos_divergences=np.array(pos_divs),
        qmap_divergences=np.array([results[tau]['qmap_divergence'] for tau in TAU_VALUES]),
        **{f'spread_tau_{tau}': all_spreads[tau] for tau in TAU_VALUES},
    )
    print(f"\nResults saved to results/exp1_path_dependence.npz")
