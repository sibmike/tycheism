"""
Experiment 2 — Intervention Cascade

Proposition: A single forced intervention (I_e) at t0 produces trajectory
divergence that compounds at every subsequent timestep.

Key insight from Exp 3: the cascade lives in the Q-MAP (world model),
not in position. Q-map divergence is the primary metric.

Setup: Smooth landscape. Paired agents (clone at t0). Apply I_e to one.
Measure: Q-map divergence D_Q(t), position distance D_x(t), outcome
divergence D_o(t) from t0 to H.

Also: vary intervention magnitude to show D(H) is superlinear in magnitude.
Also: include sqrt(t) reference line (random walk baseline).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import numpy as np
from core.landscape import generate_landscape, toroidal_distance
from core.agent import Agent
from core.simulation import run_paired
from core import interventions as ops

# Parameters
L = 31
H = 400
X0 = (15, 15)
ALPHA = 0.1
TAU = 1.0
Q_PRIOR = 0.0
T_INTERVENE = 50
N_SEEDS = 80
LANDSCAPE_SEED = 42


def compute_qmap_divergence_timeseries(result, L, snapshot_interval=5):
    """Compute Q-map divergence over time by re-running with snapshots.

    Since agent.history stores positions but not full Q snapshots at every step,
    we re-run the paired comparison and snapshot Q at intervals.
    """
    # We need to re-run to get Q snapshots. Use the stored history to verify.
    pass


def run_paired_with_q_snapshots(landscape, L, x0, tau, alpha, q_prior, H,
                                 intervention_fn, t_intervene, seed,
                                 snapshot_every=1):
    """Run paired comparison tracking Q-map divergence at every timestep."""
    from core.agent import Agent

    agent_a = Agent(L=L, x0=x0, tau=tau, alpha=alpha, q_prior=q_prior, rng=seed)

    # Run to intervention time
    for _ in range(t_intervene):
        agent_a.step(landscape)

    # Clone
    agent_b = agent_a.clone()

    # Intervene on b
    intervention_fn(agent_b)

    # Run both, recording divergence
    q_divs = []
    pos_dists = []
    outcome_divs = []

    for t in range(t_intervene, H):
        agent_a.step(landscape)
        agent_b.step(landscape)

        if (t - t_intervene) % snapshot_every == 0:
            q_div = np.sqrt(np.sum((agent_a.Q - agent_b.Q) ** 2))
            q_divs.append(q_div)

            pos_dist = toroidal_distance(agent_a.x, agent_b.x, L)
            pos_dists.append(pos_dist)

            o_div = abs(agent_a.o - agent_b.o)
            outcome_divs.append(o_div)

    return {
        'q_divs': np.array(q_divs),
        'pos_dists': np.array(pos_dists),
        'outcome_divs': np.array(outcome_divs),
        'q_final_a': agent_a.get_q_snapshot(),
        'q_final_b': agent_b.get_q_snapshot(),
    }


if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENT 2: INTERVENTION CASCADE")
    print(f"L={L}, H={H}, t_intervene={T_INTERVENE}, n_seeds={N_SEEDS}")
    print("=" * 60)

    landscape = generate_landscape('smooth', L, seed=LANDSCAPE_SEED)

    # --- Part A: Q-map divergence over time (coupled vs TvL) ---
    print("\nPart A: D_Q(t) for coupled vs TvL")
    print("-" * 40)

    def intervene_ie(agent):
        ops.determine_encounter(agent, forced_e=-1)

    # Coupled runs
    all_q_divs_coupled = []
    all_pos_dists_coupled = []
    for seed in range(N_SEEDS):
        r = run_paired_with_q_snapshots(
            landscape, L, X0, TAU, ALPHA, Q_PRIOR, H,
            intervene_ie, T_INTERVENE, seed, snapshot_every=1)
        all_q_divs_coupled.append(r['q_divs'])
        all_pos_dists_coupled.append(r['pos_dists'])

    q_divs_coupled = np.array(all_q_divs_coupled)
    pos_dists_coupled = np.array(all_pos_dists_coupled)

    # TvL runs
    all_q_divs_tvl = []
    all_pos_dists_tvl = []
    for seed in range(N_SEEDS):
        r = run_paired_with_q_snapshots(
            landscape, L, X0, 1e7, 0.0, Q_PRIOR, H,
            intervene_ie, T_INTERVENE, seed, snapshot_every=1)
        all_q_divs_tvl.append(r['q_divs'])
        all_pos_dists_tvl.append(r['pos_dists'])

    q_divs_tvl = np.array(all_q_divs_tvl)
    pos_dists_tvl = np.array(all_pos_dists_tvl)

    T_post = q_divs_coupled.shape[1]
    timesteps = np.arange(T_post) + T_INTERVENE

    # Report key moments
    for t_check in [10, 50, 100, 200, 300]:
        if t_check < T_post:
            q_c = q_divs_coupled[:, t_check].mean()
            q_t = q_divs_tvl[:, t_check].mean()
            p_c = pos_dists_coupled[:, t_check].mean()
            print(f"  t={T_INTERVENE + t_check:3d}: "
                  f"Q_div(coupled)={q_c:.3f}, Q_div(TvL)={q_t:.4f}, "
                  f"pos(coupled)={p_c:.2f}")

    # Check: does Q divergence grow over time? (the cascade claim)
    early_q = q_divs_coupled[:, 10].mean()
    late_q = q_divs_coupled[:, -1].mean()
    print(f"\n  Q-div growth: early(t+10)={early_q:.3f} -> late(t+{T_post})={late_q:.3f}")
    if late_q > early_q:
        print("  CONFIRMED: Q-map divergence compounds over time")
    else:
        print("  NOTE: Q-map divergence plateaus (may be bounded by landscape)")

    # --- Part B: Intervention magnitude sensitivity ---
    print("\nPart B: D_Q(H) vs intervention magnitude")
    print("-" * 40)

    # Vary how many forced encounters we impose
    n_forced_values = [1, 2, 5, 10, 20]
    n_seeds_mag = 40
    mag_results = {}

    for n_forced in n_forced_values:
        def intervene_n(agent, n=n_forced):
            for _ in range(n):
                ops.determine_encounter(agent, forced_e=-1)
                # Need to actually step to consume the forced encounter
            # Actually, determine_encounter only sets the NEXT encounter.
            # For multiple, we need to force encounters over multiple steps.
            # This is handled differently — set a persistent override.
            # For now, just force one: the agent gets one -1.
            pass

        # Simpler approach: force n consecutive -1 encounters by intervening
        # at consecutive timesteps
        q_divs = []
        for seed in range(n_seeds_mag):
            agent_a = Agent(L=L, x0=X0, tau=TAU, alpha=ALPHA, q_prior=Q_PRIOR, rng=seed)
            for _ in range(T_INTERVENE):
                agent_a.step(landscape)
            agent_b = agent_a.clone()

            # Force n_forced consecutive -1 encounters on agent_b
            for step in range(H - T_INTERVENE):
                if step < n_forced:
                    ops.determine_encounter(agent_b, forced_e=-1)
                agent_a.step(landscape)
                agent_b.step(landscape)

            q_div = np.sqrt(np.sum((agent_a.Q - agent_b.Q) ** 2))
            q_divs.append(q_div)

        mean_div = np.mean(q_divs)
        mag_results[n_forced] = mean_div
        print(f"  n_forced={n_forced:2d}: D_Q(H) = {mean_div:.3f}")

    # Check superlinearity
    d1 = mag_results[1]
    d20 = mag_results[20]
    ratio = d20 / d1 if d1 > 0 else float('inf')
    print(f"\n  Ratio D(20)/D(1) = {ratio:.2f} (linear would be 20.0)")
    if ratio > 20:
        print("  CONFIRMED: Superlinear — divergence amplified beyond intervention")
    elif ratio > 10:
        print("  PARTIAL: Sublinear but substantial amplification")
    else:
        print("  NOTE: Nearly linear or sublinear scaling")

    # Save results
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
    os.makedirs(output_dir, exist_ok=True)

    np.savez(
        os.path.join(output_dir, 'exp2_intervention_cascade.npz'),
        timesteps=timesteps,
        q_divs_coupled_mean=q_divs_coupled.mean(axis=0),
        q_divs_coupled_std=q_divs_coupled.std(axis=0),
        q_divs_tvl_mean=q_divs_tvl.mean(axis=0),
        q_divs_tvl_std=q_divs_tvl.std(axis=0),
        pos_dists_coupled_mean=pos_dists_coupled.mean(axis=0),
        pos_dists_coupled_std=pos_dists_coupled.std(axis=0),
        pos_dists_tvl_mean=pos_dists_tvl.mean(axis=0),
        pos_dists_tvl_std=pos_dists_tvl.std(axis=0),
        n_forced_values=np.array(list(mag_results.keys())),
        mag_q_divs=np.array(list(mag_results.values())),
    )
    print(f"\nResults saved to results/exp2_intervention_cascade.npz")
