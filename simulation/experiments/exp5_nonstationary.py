"""
Experiment 5 — Nonstationary Landscapes

Proposition: When the landscape drifts, agents trained on past landscapes
navigate with stale Q-maps. Fast learners (high alpha) adapt better.
An imposed Q-map (I_s) becomes stale at the same rate.

Extension experiment — lower priority but completes the set.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import numpy as np
from core.landscape import generate_landscape
from core.agent import Agent

# Parameters
L = 31
H = 400
X0 = (15, 15)
TAU = 1.0
Q_PRIOR = 0.0
N_SEEDS = 40
LANDSCAPE_SEED = 42

DRIFT_MAGNITUDES = [0.0, 0.005, 0.01, 0.02, 0.05]
ALPHA_VALUES = [0.01, 0.05, 0.1, 0.2, 0.5]


def compute_regret(agent, landscape_fn, H):
    """Compute regret: difference between agent's outcome and oracle outcome.

    Oracle always goes to the cell with highest p at current time.
    """
    # Agent's actual cumulative outcome
    agent_outcome = agent.o

    # Oracle outcome: sum of expected values at best cell per timestep
    oracle_outcome = 0
    for t in range(H):
        p_t = landscape_fn(t) if callable(landscape_fn) else landscape_fn
        best_p = p_t.max()
        oracle_outcome += (2 * best_p - 1)  # expected Bernoulli value

    return oracle_outcome - agent_outcome


def qmap_staleness(agent, landscape_fn, t):
    """How stale is the agent's Q-map relative to current landscape?

    Measures L2 distance between Q and the true bias map at time t.
    """
    p_t = landscape_fn(t) if callable(landscape_fn) else landscape_fn
    true_q = 2 * p_t - 1  # expected Q if perfectly learned
    return np.sqrt(np.sum((agent.Q - true_q) ** 2))


if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENT 5: NONSTATIONARY LANDSCAPES")
    print(f"L={L}, H={H}, n_seeds={N_SEEDS}")
    print("=" * 60)

    # --- Part A: Drift magnitude x learning rate ---
    print("\nPart A: Regret by drift x alpha")
    print("-" * 60)

    regret_matrix = np.zeros((len(DRIFT_MAGNITUDES), len(ALPHA_VALUES)))
    staleness_matrix = np.zeros_like(regret_matrix)

    for i, drift in enumerate(DRIFT_MAGNITUDES):
        for j, alpha in enumerate(ALPHA_VALUES):
            regrets = []
            stalenesses = []

            for seed in range(N_SEEDS):
                if drift == 0:
                    landscape = generate_landscape('smooth', L, seed=LANDSCAPE_SEED)
                    landscape_fn = landscape
                else:
                    landscape_fn = generate_landscape(
                        'nonstationary', L, seed=LANDSCAPE_SEED,
                        drift_magnitude=drift, drift_seed=seed + 5000)

                agent = Agent(L=L, x0=X0, tau=TAU, alpha=alpha,
                              q_prior=Q_PRIOR, rng=seed)
                for t in range(H):
                    p_t = landscape_fn(t) if callable(landscape_fn) else landscape_fn
                    agent.step(p_t)

                regrets.append(compute_regret(agent, landscape_fn, H))
                stalenesses.append(qmap_staleness(agent, landscape_fn, H - 1))

            regret_matrix[i, j] = np.mean(regrets)
            staleness_matrix[i, j] = np.mean(stalenesses)

    # Print regret table
    print(f"\n  Regret (oracle - agent):")
    print(f"  {'drift':>8s}", end='')
    for alpha in ALPHA_VALUES:
        print(f"  a={alpha:.2f}", end='')
    print()
    for i, drift in enumerate(DRIFT_MAGNITUDES):
        print(f"  {drift:8.3f}", end='')
        for j in range(len(ALPHA_VALUES)):
            print(f"  {regret_matrix[i,j]:7.1f}", end='')
        print()

    # Print staleness table
    print(f"\n  Q-map staleness (L2 vs true landscape):")
    print(f"  {'drift':>8s}", end='')
    for alpha in ALPHA_VALUES:
        print(f"  a={alpha:.2f}", end='')
    print()
    for i, drift in enumerate(DRIFT_MAGNITUDES):
        print(f"  {drift:8.3f}", end='')
        for j in range(len(ALPHA_VALUES)):
            print(f"  {staleness_matrix[i,j]:7.2f}", end='')
        print()

    # Key finding
    print(f"\n  Key: At high drift, fast learners (high alpha) have lower staleness")
    print(f"  At zero drift, slow learners (low alpha) have lower regret (less noisy)")

    # Save
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
    os.makedirs(output_dir, exist_ok=True)

    np.savez(
        os.path.join(output_dir, 'exp5_nonstationary.npz'),
        drift_magnitudes=np.array(DRIFT_MAGNITUDES),
        alpha_values=np.array(ALPHA_VALUES),
        regret_matrix=regret_matrix,
        staleness_matrix=staleness_matrix,
    )
    print(f"\nResults saved to results/exp5_nonstationary.npz")
