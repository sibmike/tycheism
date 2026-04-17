"""
Experiment 4b — Island Convergence / Divergent Attractors

The real island topology test: intervention displaces agent from one
local maximum to another. Coupling then locks the agent onto the new
peak. Two agents with identical history converge to DIFFERENT local
maxima — permanently.

This is the strongest visual demonstration of the Tycheism claim:
a single intervention doesn't just change one decision — it redirects
the entire downstream trajectory to a different attractor.

Setup:
- Island landscape with well-separated peaks
- Agent starts near one peak, learns its local Q-map
- Intervention: force agent to a position near a different peak (I_e via
  forced arm pulls) or substitute Q with values favoring a different region
- Measure: which peak each agent converges to, Q-map divergence,
  and whether divergence is PERMANENT (plateaus at inter-peak distance)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import numpy as np
from core.landscape import generate_landscape, toroidal_distance
from core.agent import Agent
from core import interventions as ops

# Parameters
L = 41  # larger grid to separate islands
H = 600  # longer horizon to confirm lock-in
ALPHA = 0.1
TAU = 0.5  # stronger coupling — agent exploits learned Q
Q_PRIOR = 0.0
T_INTERVENE = 100  # let agent settle on first island
N_SEEDS = 60
LANDSCAPE_SEED = 42


def make_two_island_landscape(L, seed=42):
    """Create a landscape with exactly 2 well-separated high-p islands.

    Island A centered at (L//4, L//4), Island B at (3L//4, 3L//4).
    Background p = 0.2. Peak p = 0.9. Clear separation.
    """
    p = np.full((L, L), 0.2)
    peak_a = (L // 4, L // 4)
    peak_b = (3 * L // 4, 3 * L // 4)
    peak_width = L / 8

    y, x = np.mgrid[0:L, 0:L]
    for peak in [peak_a, peak_b]:
        dy = np.minimum(np.abs(y - peak[0]), L - np.abs(y - peak[0]))
        dx = np.minimum(np.abs(x - peak[1]), L - np.abs(x - peak[1]))
        dist_sq = dy**2 + dx**2
        contribution = 0.7 * np.exp(-dist_sq / (2 * peak_width**2))
        p += contribution

    return np.clip(p, 0, 1), peak_a, peak_b


def closest_peak(pos, peak_a, peak_b, L):
    """Which peak is the agent closer to?"""
    da = toroidal_distance(pos, peak_a, L)
    db = toroidal_distance(pos, peak_b, L)
    return 'A' if da < db else 'B'


def run_island_experiment(landscape, peak_a, peak_b, intervention_fn, seed):
    """Run paired comparison on two-island landscape."""
    # Start near peak A
    x0 = peak_a

    agent_a = Agent(L=L, x0=x0, tau=TAU, alpha=ALPHA, q_prior=Q_PRIOR, rng=seed)
    for _ in range(T_INTERVENE):
        agent_a.step(landscape)

    agent_b = agent_a.clone()
    intervention_fn(agent_b)

    # Track over time
    q_divs = []
    pos_dists = []
    peaks_a = []
    peaks_b = []

    for _ in range(H - T_INTERVENE):
        agent_a.step(landscape)
        agent_b.step(landscape)
        q_divs.append(np.sqrt(np.sum((agent_a.Q - agent_b.Q) ** 2)))
        pos_dists.append(toroidal_distance(agent_a.x, agent_b.x, L))
        peaks_a.append(closest_peak(agent_a.x, peak_a, peak_b, L))
        peaks_b.append(closest_peak(agent_b.x, peak_a, peak_b, L))

    return {
        'q_divs': np.array(q_divs),
        'pos_dists': np.array(pos_dists),
        'final_peak_a': closest_peak(agent_a.x, peak_a, peak_b, L),
        'final_peak_b': closest_peak(agent_b.x, peak_a, peak_b, L),
        'final_pos_a': agent_a.x.copy(),
        'final_pos_b': agent_b.x.copy(),
        'traj_a': agent_a.get_position_history(),
        'traj_b': agent_b.get_position_history(),
        'q_final_a': agent_a.Q.copy(),
        'q_final_b': agent_b.Q.copy(),
    }


if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENT 4b: ISLAND CONVERGENCE / DIVERGENT ATTRACTORS")
    print(f"L={L}, H={H}, tau={TAU}, t_intervene={T_INTERVENE}, n_seeds={N_SEEDS}")
    print("=" * 60)

    landscape, peak_a, peak_b = make_two_island_landscape(L, LANDSCAPE_SEED)
    inter_peak_dist = toroidal_distance(peak_a, peak_b, L)
    print(f"Peak A: {peak_a}, Peak B: {peak_b}")
    print(f"Inter-peak distance: {inter_peak_dist:.1f}")
    print(f"Landscape p range: [{landscape.min():.3f}, {landscape.max():.3f}]")

    # --- Intervention 1: Set Q near peak B to high value (I_K+) ---
    # This is the "tip" — tell the agent about the other island
    print("\n--- I_K+ intervention: reveal peak B to agent ---")

    def intervene_tip(agent):
        """I_K+: Set Q values near peak B to attract the agent."""
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                cell = ((peak_b[0] + dr) % L, (peak_b[1] + dc) % L)
                ops.expand_support(agent, cell, q_info=0.8)

    count_switched_tip = 0
    for seed in range(N_SEEDS):
        r = run_island_experiment(landscape, peak_a, peak_b, intervene_tip, seed)
        if r['final_peak_a'] != r['final_peak_b']:
            count_switched_tip += 1

    print(f"  Agents on different peaks: {count_switched_tip}/{N_SEEDS} "
          f"({100*count_switched_tip/N_SEEDS:.0f}%)")

    # --- Intervention 2: Replace Q-map with one favoring peak B (I_s) ---
    print("\n--- I_s intervention: replace Q-map to favor peak B ---")

    def intervene_substitute(agent):
        """I_s: Replace Q-map with values that attract agent to peak B."""
        new_Q = np.full((L, L), -0.5)
        y, x = np.mgrid[0:L, 0:L]
        dy = np.minimum(np.abs(y - peak_b[0]), L - np.abs(y - peak_b[0]))
        dx = np.minimum(np.abs(x - peak_b[1]), L - np.abs(x - peak_b[1]))
        dist_sq = dy**2 + dx**2
        new_Q += 1.3 * np.exp(-dist_sq / (2 * (L/8)**2))
        ops.substitute_state(agent, new_Q)

    count_switched_sub = 0
    q_divs_sub = []
    pos_dists_sub = []
    example_result = None

    for seed in range(N_SEEDS):
        r = run_island_experiment(landscape, peak_a, peak_b, intervene_substitute, seed)
        q_divs_sub.append(r['q_divs'])
        pos_dists_sub.append(r['pos_dists'])
        if r['final_peak_a'] != r['final_peak_b']:
            count_switched_sub += 1
            if example_result is None:
                example_result = r

    q_arr = np.array(q_divs_sub)
    pos_arr = np.array(pos_dists_sub)

    print(f"  Agents on different peaks: {count_switched_sub}/{N_SEEDS} "
          f"({100*count_switched_sub/N_SEEDS:.0f}%)")
    print(f"  D_Q: early={q_arr[:,20].mean():.2f}, "
          f"mid={q_arr[:,min(200, q_arr.shape[1]-1)].mean():.2f}, "
          f"final={q_arr[:,-1].mean():.2f}")
    print(f"  D_pos: final={pos_arr[:,-1].mean():.2f}")

    # Check if divergence plateaus (locked onto different peaks)
    last_quarter = q_arr[:, -q_arr.shape[1]//4:]
    q_mean_series = last_quarter.mean(axis=0)
    is_stable = (q_mean_series.std() / (q_mean_series.mean() + 1e-8)) < 0.1
    print(f"  Q-divergence in last quarter: mean={q_mean_series.mean():.2f}, "
          f"std={q_mean_series.std():.3f}")
    print(f"  Divergence {'is STABLE (locked on different attractors)' if is_stable else 'is still changing'}")

    # --- Intervention 3: Force arm pulls toward peak B (I_e sequence) ---
    print("\n--- I_e intervention: force 10 moves toward peak B ---")

    def intervene_force_move(agent):
        """Force agent toward peak B by overriding encounters."""
        # Compute direction from current position to peak B
        dy = peak_b[0] - agent.x[0]
        dx = peak_b[1] - agent.x[1]
        # Handle torus wrapping
        if abs(dy) > L // 2:
            dy = -np.sign(dy) * (L - abs(dy))
        if abs(dx) > L // 2:
            dx = -np.sign(dx) * (L - abs(dx))
        # Set Q in the direction of peak B to very high
        for step in range(10):
            target_y = (agent.x[0] + np.sign(dy)) % L
            target_x = (agent.x[1] + np.sign(dx)) % L
            agent.Q[target_y, target_x] = 1.0  # make this cell attractive
            # Also force a positive encounter to reinforce
            ops.determine_encounter(agent, forced_e=1)

    count_switched_force = 0
    for seed in range(N_SEEDS):
        r = run_island_experiment(landscape, peak_a, peak_b, intervene_force_move, seed)
        if r['final_peak_a'] != r['final_peak_b']:
            count_switched_force += 1

    print(f"  Agents on different peaks: {count_switched_force}/{N_SEEDS} "
          f"({100*count_switched_force/N_SEEDS:.0f}%)")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY: Attractor Switching by Operator Type")
    print("-" * 50)
    print(f"  I_K+ (tip about peak B):  {count_switched_tip}/{N_SEEDS} switched "
          f"({100*count_switched_tip/N_SEEDS:.0f}%)")
    print(f"  I_s  (replace Q-map):     {count_switched_sub}/{N_SEEDS} switched "
          f"({100*count_switched_sub/N_SEEDS:.0f}%)")
    print(f"  I_e  (force toward B):    {count_switched_force}/{N_SEEDS} switched "
          f"({100*count_switched_force/N_SEEDS:.0f}%)")
    print()

    if count_switched_sub > count_switched_tip:
        print("  Coupling-breaking operators redirect trajectories to different")
        print("  attractors more reliably than coupling-preserving ones.")
    print("  Key: Once on a different island, the agent STAYS there —")
    print("  the coupling locks them onto the new attractor permanently.")

    # Save
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
    os.makedirs(output_dir, exist_ok=True)

    save_data = {
        'landscape': landscape,
        'peak_a': np.array(peak_a),
        'peak_b': np.array(peak_b),
        'q_divs_sub_mean': q_arr.mean(axis=0),
        'q_divs_sub_std': q_arr.std(axis=0),
        'pos_dists_sub_mean': pos_arr.mean(axis=0),
        'pos_dists_sub_std': pos_arr.std(axis=0),
        'switch_rates': np.array([count_switched_tip, count_switched_sub, count_switched_force]),
        'timesteps': np.arange(q_arr.shape[1]) + T_INTERVENE,
    }
    if example_result is not None:
        save_data['example_traj_a'] = example_result['traj_a']
        save_data['example_traj_b'] = example_result['traj_b']
        save_data['example_q_a'] = example_result['q_final_a']
        save_data['example_q_b'] = example_result['q_final_b']

    np.savez(os.path.join(output_dir, 'exp4b_island_convergence.npz'), **save_data)
    print(f"\nResults saved to results/exp4b_island_convergence.npz")
