"""
Experiment 6 — Operator Discrimination

Proposition: Different intervention operators produce different divergence
profiles. Operators that preserve coupling (I_K+) produce less Q-map
divergence than operators that break it (I_e, I_s, I_U).

Approach: Apply each operator in its "minimal effective form" and compare
D_Q(t) timeseries. Don't attempt magnitude matching — the ranking is the result.
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
X0 = (15, 15)
ALPHA = 0.1
TAU = 1.0
Q_PRIOR = 0.0
T_INTERVENE = 80  # let agent learn a bit before intervening
N_SEEDS = 60
LANDSCAPE_SEED = 42


def run_with_operator(landscape, operator_fn, seed):
    """Run paired comparison with a specific operator intervention."""
    agent_a = Agent(L=L, x0=X0, tau=TAU, alpha=ALPHA, q_prior=Q_PRIOR, rng=seed)

    for _ in range(T_INTERVENE):
        agent_a.step(landscape)

    agent_b = agent_a.clone()
    operator_fn(agent_b)

    q_divs = []
    pos_dists = []

    for _ in range(H - T_INTERVENE):
        agent_a.step(landscape)
        agent_b.step(landscape)
        q_div = np.sqrt(np.sum((agent_a.Q - agent_b.Q) ** 2))
        q_divs.append(q_div)
        pos_dists.append(toroidal_distance(agent_a.x, agent_b.x, L))

    return np.array(q_divs), np.array(pos_dists)


# Define minimal-form operators
def op_ik_plus(agent):
    """I_K+ : Set Q for one distant unvisited cell to a moderate positive value."""
    # Find a cell far from agent with Q still at prior
    far_x = (agent.x[0] + L // 2) % L
    far_y = (agent.x[1] + L // 2) % L
    ops.expand_support(agent, (far_x, far_y), q_info=0.5)


def op_ik_minus(agent):
    """I_K- : Block one arm for one timestep."""
    ops.truncate_support(agent, ['up'])
    # Note: will be cleared after one step because we only block once


def op_ikw(agent):
    """I_Kw : Add small bias toward one arm."""
    ops.reshape_weights(agent, [0.3, 0, 0, 0, 0])  # bias toward 'up'


def op_ie(agent):
    """I_e : Force one negative encounter."""
    ops.determine_encounter(agent, forced_e=-1)


def op_is_partial(agent):
    """I_s (partial) : Replace Q for a 3x3 neighborhood around agent."""
    rng = np.random.default_rng(9999)
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            cell = ((agent.x[0] + dr) % L, (agent.x[1] + dc) % L)
            agent.Q[cell] = rng.uniform(-0.5, 0.5)


def op_is_full(agent):
    """I_s (full) : Replace entire Q-map with random values."""
    rng = np.random.default_rng(9999)
    ops.substitute_state(agent, rng.uniform(-0.5, 0.5, size=(L, L)))


def op_iu(agent):
    """I_U : Halve learning rate for 20 timesteps."""
    # Persistent attenuation — reduce alpha directly
    agent.alpha = agent.alpha * 0.5
    # Note: this is permanent, unlike the one-shot override


OPERATORS = {
    'I_K+ (expand)':   op_ik_plus,
    'I_K- (truncate)': op_ik_minus,
    'I_Kw (bias)':     op_ikw,
    'I_e (force enc)': op_ie,
    'I_s partial':     op_is_partial,
    'I_s full':        op_is_full,
    'I_U (attenuate)': op_iu,
}


if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENT 6: OPERATOR DISCRIMINATION")
    print(f"L={L}, H={H}, t_intervene={T_INTERVENE}, n_seeds={N_SEEDS}")
    print("=" * 60)

    landscape = generate_landscape('smooth', L, seed=LANDSCAPE_SEED)

    # Also run a no-intervention baseline for reference
    print("\nRunning no-intervention baseline...")
    no_int_q_divs = []
    for seed in range(N_SEEDS):
        qd, _ = run_with_operator(landscape, lambda a: None, seed)
        no_int_q_divs.append(qd)
    no_int_mean = np.array(no_int_q_divs).mean(axis=0)
    print(f"  Baseline D_Q(H) = {no_int_mean[-1]:.4f} (should be ~0)")

    all_results = {'no_intervention': np.array(no_int_q_divs)}

    print(f"\n{'Operator':>18s} | {'D_Q(H)':>8s} | {'D_Q(t+50)':>10s} | {'Coupling':>10s}")
    print("-" * 60)

    for name, op_fn in OPERATORS.items():
        q_divs_all = []
        pos_dists_all = []
        for seed in range(N_SEEDS):
            qd, pd = run_with_operator(landscape, op_fn, seed)
            q_divs_all.append(qd)
            pos_dists_all.append(pd)

        q_arr = np.array(q_divs_all)
        all_results[name] = q_arr

        final_q = q_arr[:, -1].mean()
        mid_q = q_arr[:, 50].mean() if q_arr.shape[1] > 50 else q_arr[:, -1].mean()

        # Classify coupling status
        if 'K+' in name or 'Kw' in name:
            coupling = 'preserved'
        elif 'K-' in name:
            coupling = 'partial'
        else:
            coupling = 'broken'

        print(f"{name:>18s} | {final_q:8.3f} | {mid_q:10.3f} | {coupling:>10s}")

    # Check the ranking
    print("\n" + "=" * 60)
    print("RANKING (by final D_Q)")
    print("-" * 40)
    rankings = []
    for name in OPERATORS:
        final = all_results[name][:, -1].mean()
        rankings.append((final, name))
    rankings.sort()
    for rank, (val, name) in enumerate(rankings, 1):
        print(f"  {rank}. {name:>18s}: D_Q = {val:.3f}")

    # Check if coupling-breaking > coupling-preserving
    preserving = ['I_K+ (expand)', 'I_Kw (bias)']
    breaking = ['I_e (force enc)', 'I_s partial', 'I_s full', 'I_U (attenuate)']
    avg_preserving = np.mean([all_results[n][:, -1].mean() for n in preserving])
    avg_breaking = np.mean([all_results[n][:, -1].mean() for n in breaking])
    print(f"\n  Avg coupling-preserving: {avg_preserving:.3f}")
    print(f"  Avg coupling-breaking:   {avg_breaking:.3f}")
    if avg_breaking > avg_preserving:
        print("  CONFIRMED: Breaking coupling produces more Q-map divergence")
    else:
        print("  WARNING: Expected breaking to produce more divergence")

    # Save results
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
    os.makedirs(output_dir, exist_ok=True)

    save_data = {}
    for name, arr in all_results.items():
        safe_name = name.replace(' ', '_').replace('(', '').replace(')', '').replace('+', 'plus').replace('-', 'minus')
        save_data[f'{safe_name}_mean'] = arr.mean(axis=0)
        save_data[f'{safe_name}_std'] = arr.std(axis=0)
    save_data['timesteps'] = np.arange(arr.shape[1]) + T_INTERVENE

    np.savez(os.path.join(output_dir, 'exp6_operator_discrimination.npz'), **save_data)
    print(f"\nResults saved to results/exp6_operator_discrimination.npz")
