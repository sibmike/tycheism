"""
Experiment 3 — Coupling Necessity (TvL Comparison)

Proposition: Under zero coupling (tau->inf, alpha=0), intervention-induced
divergence does not compound. The same intervention on the same landscape
produces bounded, non-cascading effects. Coupling is necessary for the cascade.

Setup: Same landscape, same I_e intervention.
Compare: coupled (tau=1, alpha=0.1) vs TvL baseline (tau=1e7, alpha=0).
Also test partial coupling: (tau=inf, alpha>0) and (tau<inf, alpha=0).
Enhancement: 2D heatmap of tau x alpha -> D(H).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import numpy as np
from core.landscape import generate_landscape, toroidal_distance
from core.agent import Agent
from core.simulation import run_paired
from core import interventions as ops
from analysis.metrics import divergence_timeseries, batch_divergence_timeseries

# Parameters
L = 31
H = 300
X0 = (15, 15)
Q_PRIOR = 0.0
T_INTERVENE = 50
N_SEEDS = 50
LANDSCAPE_SEED = 42


def intervention_fn(agent):
    """Force a negative encounter (I_e)."""
    ops.determine_encounter(agent, forced_e=-1)


if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENT 3: COUPLING NECESSITY (TvL COMPARISON)")
    print(f"L={L}, H={H}, t_intervene={T_INTERVENE}, n_seeds={N_SEEDS}")
    print("=" * 60)

    landscape = generate_landscape('smooth', L, seed=LANDSCAPE_SEED)

    # --- Part A: Coupled vs TvL head-to-head ---
    print("\nPart A: Coupled vs TvL baseline")
    print("-" * 40)

    conditions = {
        'coupled':        {'tau': 1.0,  'alpha': 0.1},
        'tvl_baseline':   {'tau': 1e7,  'alpha': 0.0},
        'learn_no_use':   {'tau': 1e7,  'alpha': 0.1},  # learns but doesn't use Q
        'use_no_learn':   {'tau': 1.0,  'alpha': 0.0},  # uses Q but Q is frozen
    }

    condition_results = {}
    for name, params in conditions.items():
        results = []
        for seed in range(N_SEEDS):
            r = run_paired(
                landscape, L=L, x0=X0,
                tau=params['tau'], alpha=params['alpha'],
                q_prior=Q_PRIOR, H=H,
                intervention_fn=intervention_fn,
                t_intervene=T_INTERVENE, seed=seed,
            )
            results.append(r)

        batch_div = batch_divergence_timeseries(results, L, T_INTERVENE)
        final_pos_div = batch_div['position_dist_mean'][-1]
        final_out_div = batch_div['outcome_div_mean'][-1]

        # Q-map divergence at final step
        qmap_divs = [np.sqrt(np.sum((r['q_final_a'] - r['q_final_b'])**2))
                     for r in results]
        qmap_div_mean = np.mean(qmap_divs)

        condition_results[name] = {
            'batch_div': batch_div,
            'qmap_div_mean': qmap_div_mean,
            'results': results,
        }

        print(f"  {name:15s}: pos_div={final_pos_div:7.3f}, "
              f"qmap_div={qmap_div_mean:7.3f}, outcome_div={final_out_div:7.1f}")

    # Check the key result
    coupled_div = condition_results['coupled']['batch_div']['position_dist_mean'][-1]
    tvl_div = condition_results['tvl_baseline']['batch_div']['position_dist_mean'][-1]
    print(f"\n  Coupling gap: {coupled_div:.3f} (coupled) vs {tvl_div:.3f} (TvL)")
    if coupled_div > tvl_div * 1.5:
        print("  CONFIRMED: Coupling produces compounding divergence that TvL does not")
    else:
        print("  WARNING: Coupling gap smaller than expected")

    # --- Part B: tau x alpha heatmap ---
    print("\nPart B: tau x alpha heatmap")
    print("-" * 40)

    tau_grid = [0.5, 1.0, 2.0, 5.0, 20.0, 1e7]
    alpha_grid = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]
    n_seeds_heatmap = 20  # fewer seeds for the grid

    heatmap = np.zeros((len(alpha_grid), len(tau_grid)))

    for i, alpha in enumerate(alpha_grid):
        for j, tau in enumerate(tau_grid):
            divs = []
            for seed in range(n_seeds_heatmap):
                r = run_paired(
                    landscape, L=L, x0=X0,
                    tau=tau, alpha=alpha,
                    q_prior=Q_PRIOR, H=H,
                    intervention_fn=intervention_fn,
                    t_intervene=T_INTERVENE, seed=seed,
                )
                d = divergence_timeseries(r, L, T_INTERVENE)
                divs.append(d['position_dist'][-1])
            heatmap[i, j] = np.mean(divs)

    print("\n  Heatmap: D(H) = mean final position divergence")
    print(f"  {'':>8s}", end='')
    for tau in tau_grid:
        print(f"  tau={tau:>6.0f}" if tau < 100 else f"  tau=inf ", end='')
    print()
    for i, alpha in enumerate(alpha_grid):
        print(f"  a={alpha:.2f}", end='')
        for j in range(len(tau_grid)):
            print(f"  {heatmap[i, j]:8.3f}", end='')
        print()

    # Save results
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
    os.makedirs(output_dir, exist_ok=True)

    # Save timeseries for the 4 conditions
    save_data = {
        'tau_grid': np.array(tau_grid),
        'alpha_grid': np.array(alpha_grid),
        'heatmap': heatmap,
    }
    for name, cr in condition_results.items():
        bd = cr['batch_div']
        save_data[f'{name}_pos_mean'] = bd['position_dist_mean']
        save_data[f'{name}_pos_std'] = bd['position_dist_std']
        save_data[f'{name}_out_mean'] = bd['outcome_div_mean']
        save_data[f'{name}_out_std'] = bd['outcome_div_std']
    save_data['timesteps'] = condition_results['coupled']['batch_div']['timesteps']

    np.savez(os.path.join(output_dir, 'exp3_coupling_necessity.npz'), **save_data)
    print(f"\nResults saved to results/exp3_coupling_necessity.npz")
