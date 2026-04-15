"""
Experiment 4 — Topology Dependence

Proposition: Different landscape topologies produce qualitatively different
divergence dynamics and intervention recoverability.

- Smooth: gradient guides recovery, D_Q plateaus
- Cliff: intervention past boundary is irrecoverable
- Island: agents trapped on different islands, D_Q plateaus at inter-island gap
- Deceptive: coupling itself can mislead — divergence even without intervention
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import numpy as np
from core.landscape import generate_landscape, toroidal_distance
from core.agent import Agent
from core import interventions as ops

# Parameters
L = 31
H = 400
ALPHA = 0.1
TAU = 1.0
Q_PRIOR = 0.0
T_INTERVENE = 80
N_SEEDS = 60
LANDSCAPE_SEED = 42

TOPOLOGIES = ['smooth', 'cliff', 'island', 'deceptive']


def run_topology_experiment(landscape, x0, seed, do_intervene=True):
    """Run paired comparison on given landscape."""
    agent_a = Agent(L=L, x0=x0, tau=TAU, alpha=ALPHA, q_prior=Q_PRIOR, rng=seed)
    for _ in range(T_INTERVENE):
        agent_a.step(landscape)

    agent_b = agent_a.clone()

    if do_intervene:
        # Force agent to a specific arm pull (displace them)
        ops.determine_encounter(agent_b, forced_e=-1)

    q_divs = []
    pos_dists = []
    for _ in range(H - T_INTERVENE):
        agent_a.step(landscape)
        agent_b.step(landscape)
        q_divs.append(np.sqrt(np.sum((agent_a.Q - agent_b.Q) ** 2)))
        pos_dists.append(toroidal_distance(agent_a.x, agent_b.x, L))

    return {
        'q_divs': np.array(q_divs),
        'pos_dists': np.array(pos_dists),
        'final_pos_a': agent_a.x.copy(),
        'final_pos_b': agent_b.x.copy(),
        'q_final_a': agent_a.Q.copy(),
        'q_final_b': agent_b.Q.copy(),
    }


if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENT 4: TOPOLOGY DEPENDENCE")
    print(f"L={L}, H={H}, t_intervene={T_INTERVENE}, n_seeds={N_SEEDS}")
    print("=" * 60)

    all_results = {}

    for topo in TOPOLOGIES:
        print(f"\n{'=' * 40}")
        print(f"Topology: {topo}")
        print(f"{'=' * 40}")

        landscape = generate_landscape(topo, L, seed=LANDSCAPE_SEED)
        print(f"  p range: [{landscape.min():.3f}, {landscape.max():.3f}]")

        # Find a good starting position (near high-p region for cliff/island)
        if topo == 'cliff':
            x0 = (L // 2, L // 2)  # center (interior of safe region)
        elif topo == 'island':
            # Start on one of the islands
            peak_pos = np.unravel_index(landscape.argmax(), landscape.shape)
            x0 = peak_pos
        else:
            x0 = (L // 2, L // 2)

        q_divs_all = []
        pos_dists_all = []

        for seed in range(N_SEEDS):
            r = run_topology_experiment(landscape, x0, seed)
            q_divs_all.append(r['q_divs'])
            pos_dists_all.append(r['pos_dists'])

        q_arr = np.array(q_divs_all)
        pos_arr = np.array(pos_dists_all)

        all_results[topo] = {
            'q_divs_mean': q_arr.mean(axis=0),
            'q_divs_std': q_arr.std(axis=0),
            'pos_dists_mean': pos_arr.mean(axis=0),
            'pos_dists_std': pos_arr.std(axis=0),
            'landscape': landscape,
        }

        # Report
        final_q = q_arr[:, -1].mean()
        mid_q = q_arr[:, min(100, q_arr.shape[1]-1)].mean()
        early_q = q_arr[:, min(20, q_arr.shape[1]-1)].mean()

        # Check recoverability: does D_Q plateau or keep growing?
        last_quarter = q_arr[:, -q_arr.shape[1]//4:].mean(axis=0)
        is_plateauing = (last_quarter[-1] - last_quarter[0]) / (last_quarter.mean() + 1e-8) < 0.1

        print(f"  D_Q: early(t+20)={early_q:.3f}, mid(t+100)={mid_q:.3f}, final={final_q:.3f}")
        print(f"  Recoverability: {'plateauing' if is_plateauing else 'still growing'}")

    # Summary comparison
    print("\n" + "=" * 60)
    print("SUMMARY: Topology x Divergence")
    print("-" * 50)
    print(f"{'Topology':>12s} | {'D_Q(final)':>10s} | {'Recovery':>12s}")
    print("-" * 50)
    for topo in TOPOLOGIES:
        final = all_results[topo]['q_divs_mean'][-1]
        q_series = all_results[topo]['q_divs_mean']
        last_q = q_series[-q_series.shape[0]//4:]
        trend = (last_q[-1] - last_q[0]) / (last_q.mean() + 1e-8)
        recovery = 'plateauing' if abs(trend) < 0.1 else ('growing' if trend > 0 else 'recovering')
        print(f"{topo:>12s} | {final:10.3f} | {recovery:>12s}")

    # Save
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
    os.makedirs(output_dir, exist_ok=True)

    save_data = {'timesteps': np.arange(q_arr.shape[1]) + T_INTERVENE}
    for topo in TOPOLOGIES:
        save_data[f'{topo}_q_mean'] = all_results[topo]['q_divs_mean']
        save_data[f'{topo}_q_std'] = all_results[topo]['q_divs_std']
        save_data[f'{topo}_pos_mean'] = all_results[topo]['pos_dists_mean']
        save_data[f'{topo}_pos_std'] = all_results[topo]['pos_dists_std']
        save_data[f'{topo}_landscape'] = all_results[topo]['landscape']

    np.savez(os.path.join(output_dir, 'exp4_topology_dependence.npz'), **save_data)
    print(f"\nResults saved to results/exp4_topology_dependence.npz")
