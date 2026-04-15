"""
Generate all publication figures for Paper A.

Reads saved .npz results from simulation/results/ and produces
figures in simulation/figures/.

Figure list:
1. Landscape gallery — 5 topologies + two-island
2. Exp 2: Intervention cascade — D_Q(t) coupled vs TvL
3. Exp 2: Intervention magnitude independence
4. Exp 3: Coupling necessity — 4 conditions comparison
5. Exp 3: tau x alpha heatmap
6. Exp 4b: Island attractor switching — trajectory overlay on landscape
7. Exp 4b: Island Q-map divergence stability
8. Exp 6: Operator discrimination — D_Q(t) by operator
9. Exp 6: Operator ranking bar chart
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import seaborn as sns

from core.landscape import generate_landscape

# Style
sns.set_theme(style='whitegrid', font_scale=1.1)
COLORS = sns.color_palette('colorblind', 10)
FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(FIG_DIR, exist_ok=True)


def save_fig(fig, name):
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {name}")


# ============================================================
# Figure 1: Landscape Gallery
# ============================================================
def fig_landscape_gallery():
    print("Figure 1: Landscape gallery")
    L = 41

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    topos = ['smooth', 'cliff', 'island', 'deceptive']
    titles = ['(a) Smooth', '(b) Cliff', '(c) Island', '(d) Deceptive']

    for i, (topo, title) in enumerate(zip(topos, titles)):
        ax = axes[i // 3, i % 3]
        p = generate_landscape(topo, L, seed=42)
        im = ax.imshow(p, cmap='RdYlGn', vmin=0, vmax=1, origin='lower')
        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.colorbar(im, ax=ax, label='p(x)', shrink=0.8)

    # Two-island landscape
    ax = axes[1, 1]
    p_island2 = np.full((L, L), 0.2)
    peak_a, peak_b = (L//4, L//4), (3*L//4, 3*L//4)
    y, x = np.mgrid[0:L, 0:L]
    for peak in [peak_a, peak_b]:
        dy = np.minimum(np.abs(y - peak[0]), L - np.abs(y - peak[0]))
        dx = np.minimum(np.abs(x - peak[1]), L - np.abs(x - peak[1]))
        p_island2 += 0.7 * np.exp(-(dy**2 + dx**2) / (2 * (L/8)**2))
    p_island2 = np.clip(p_island2, 0, 1)
    im = ax.imshow(p_island2, cmap='RdYlGn', vmin=0, vmax=1, origin='lower')
    ax.plot(peak_a[1], peak_a[0], 'k*', markersize=15, label='Peak A')
    ax.plot(peak_b[1], peak_b[0], 'w*', markersize=15, label='Peak B')
    ax.set_title('(e) Two-Island (Exp 4b)', fontsize=13, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend(loc='upper right', fontsize=9)
    plt.colorbar(im, ax=ax, label='p(x)', shrink=0.8)

    axes[1, 2].axis('off')  # empty cell

    fig.suptitle('Landscape Topologies — Hidden Coin Bias p(x)', fontsize=15, y=1.01)
    plt.tight_layout()
    save_fig(fig, 'fig1_landscape_gallery.png')


# ============================================================
# Figure 2: Intervention Cascade — D_Q(t)
# ============================================================
def fig_intervention_cascade():
    print("Figure 2: Intervention cascade D_Q(t)")
    data = np.load(os.path.join(RESULTS_DIR, 'exp2_intervention_cascade.npz'))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Panel A: D_Q(t) coupled vs TvL
    t = data['timesteps']
    q_mean = data['q_divs_coupled_mean']
    q_std = data['q_divs_coupled_std']
    t_mean = data['q_divs_tvl_mean']

    ax1.plot(t, q_mean, color=COLORS[0], linewidth=2, label='Coupled (tau=1, alpha=0.1)')
    ax1.fill_between(t, q_mean - q_std, q_mean + q_std, color=COLORS[0], alpha=0.2)
    ax1.plot(t, t_mean, color=COLORS[1], linewidth=2, linestyle='--', label='TvL baseline (no coupling)')

    # sqrt(t) reference
    t_post = t - t[0]
    scale = q_mean[10] / np.sqrt(10) if q_mean[10] > 0 else 0.1
    ax1.plot(t, scale * np.sqrt(t_post + 1), color='gray', linewidth=1,
             linestyle=':', label=r'$\sqrt{t}$ reference')

    ax1.axvline(x=t[0], color='red', linewidth=1, linestyle='--', alpha=0.5, label='Intervention')
    ax1.set_xlabel('Timestep')
    ax1.set_ylabel(r'$D_Q(t)$ — Q-map divergence')
    ax1.set_title('(a) Q-Map Divergence After Single Intervention', fontweight='bold')
    ax1.legend(fontsize=9)

    # Panel B: Magnitude independence
    n_forced = data['n_forced_values']
    mag_divs = data['mag_q_divs']

    ax2.bar(range(len(n_forced)), mag_divs, color=COLORS[2], edgecolor='black', linewidth=0.5)
    ax2.set_xticks(range(len(n_forced)))
    ax2.set_xticklabels([str(int(n)) for n in n_forced])
    ax2.set_xlabel('Number of forced encounters')
    ax2.set_ylabel(r'$D_Q(H)$ — Final Q-map divergence')
    ax2.set_title('(b) Divergence vs Intervention Magnitude', fontweight='bold')
    # Reference line: what linear would look like
    ax2.axhline(y=mag_divs[0], color='gray', linestyle=':', linewidth=1, label='Single-encounter level')
    ax2.legend(fontsize=9)

    plt.tight_layout()
    save_fig(fig, 'fig2_intervention_cascade.png')


# ============================================================
# Figure 3: Coupling Necessity — 4 conditions + heatmap
# ============================================================
def fig_coupling_necessity():
    print("Figure 3: Coupling necessity")
    data = np.load(os.path.join(RESULTS_DIR, 'exp3_coupling_necessity.npz'))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    t = data['timesteps']

    # Panel A: 4 conditions D_Q timeseries (using outcome divergence as proxy
    # since we saved that; Q-map timeseries wasn't saved per-step in exp3)
    conditions = [
        ('coupled', 'Coupled (tau=1, alpha=0.1)', COLORS[0], '-'),
        ('tvl_baseline', 'TvL (no coupling)', COLORS[1], '--'),
        ('learn_no_use', 'Learn, no use (tau=inf, alpha=0.1)', COLORS[2], '-.'),
        ('use_no_learn', 'Use, no learn (tau=1, alpha=0)', COLORS[3], ':'),
    ]

    for name, label, color, ls in conditions:
        mean = data[f'{name}_out_mean']
        std = data[f'{name}_out_std']
        ax1.plot(t, mean, color=color, linewidth=2, linestyle=ls, label=label)
        ax1.fill_between(t, mean - std, mean + std, color=color, alpha=0.1)

    ax1.set_xlabel('Timestep')
    ax1.set_ylabel('Outcome divergence')
    ax1.set_title('(a) Divergence by Coupling Condition', fontweight='bold')
    ax1.legend(fontsize=8, loc='upper left')

    # Panel B: tau x alpha heatmap
    heatmap = data['heatmap']
    tau_grid = data['tau_grid']
    alpha_grid = data['alpha_grid']

    tau_labels = [f'{t:.0f}' if t < 100 else 'inf' for t in tau_grid]
    alpha_labels = [f'{a:.2f}' for a in alpha_grid]

    sns.heatmap(heatmap, ax=ax2, annot=True, fmt='.1f', cmap='YlOrRd',
                xticklabels=tau_labels, yticklabels=alpha_labels,
                cbar_kws={'label': r'$D_{pos}(H)$'})
    ax2.set_xlabel(r'$\tau$ (coupling strength)')
    ax2.set_ylabel(r'$\alpha$ (learning rate)')
    ax2.set_title(r'(b) Final Position Divergence: $\tau \times \alpha$', fontweight='bold')

    plt.tight_layout()
    save_fig(fig, 'fig3_coupling_necessity.png')


# ============================================================
# Figure 4: Island Attractor Switching (Exp 4b)
# ============================================================
def fig_island_attractors():
    print("Figure 4: Island attractor switching")
    data = np.load(os.path.join(RESULTS_DIR, 'exp4b_island_convergence.npz'))

    landscape = data['landscape']
    peak_a = data['peak_a']
    peak_b = data['peak_b']

    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)

    # Panel A: Landscape with example trajectories
    ax1 = fig.add_subplot(gs[0, 0:2])
    im = ax1.imshow(landscape, cmap='RdYlGn', vmin=0, vmax=1, origin='lower')
    ax1.plot(peak_a[1], peak_a[0], 'k*', markersize=18, zorder=5)
    ax1.plot(peak_b[1], peak_b[0], 'k*', markersize=18, zorder=5)
    ax1.annotate('Peak A', (peak_a[1], peak_a[0]), fontsize=11, fontweight='bold',
                 xytext=(5, 5), textcoords='offset points')
    ax1.annotate('Peak B', (peak_b[1], peak_b[0]), fontsize=11, fontweight='bold',
                 xytext=(5, 5), textcoords='offset points')

    if 'example_traj_a' in data:
        traj_a = data['example_traj_a']
        traj_b = data['example_traj_b']
        # Plot trajectories (subsample for clarity)
        step = max(1, len(traj_a) // 200)
        ax1.plot(traj_a[::step, 1], traj_a[::step, 0], '-', color=COLORS[0],
                 linewidth=1.2, alpha=0.7, label='Endogenous')
        ax1.plot(traj_b[::step, 1], traj_b[::step, 0], '-', color=COLORS[3],
                 linewidth=1.2, alpha=0.7, label='Intervened')
        # Mark intervention point
        t_int = 100  # T_INTERVENE
        if t_int < len(traj_a):
            ax1.plot(traj_a[t_int, 1], traj_a[t_int, 0], 'r*', markersize=15,
                     zorder=6, label='Intervention')

    ax1.set_title('(a) Two-Island Landscape with Trajectory Overlay', fontweight='bold')
    ax1.legend(fontsize=9, loc='lower left')
    plt.colorbar(im, ax=ax1, label='p(x)', shrink=0.7)

    # Panel B: Q-map divergence stability
    ax2 = fig.add_subplot(gs[0, 2])
    t = data['timesteps']
    q_mean = data['q_divs_sub_mean']
    q_std = data['q_divs_sub_std']
    ax2.plot(t, q_mean, color=COLORS[0], linewidth=2)
    ax2.fill_between(t, q_mean - q_std, q_mean + q_std, color=COLORS[0], alpha=0.2)
    ax2.axhline(y=q_mean[-1], color='gray', linestyle=':', linewidth=1)
    ax2.set_xlabel('Timestep')
    ax2.set_ylabel(r'$D_Q(t)$')
    ax2.set_title('(b) Q-Map Divergence\n(I_s intervention)', fontweight='bold')
    ax2.annotate(f'Stable at {q_mean[-1]:.1f}', xy=(t[-1], q_mean[-1]),
                 xytext=(-80, -30), textcoords='offset points', fontsize=10,
                 arrowprops=dict(arrowstyle='->', color='gray'))

    # Panel C: Attractor switching rates
    ax3 = fig.add_subplot(gs[1, 0])
    switch_rates = data['switch_rates']
    operators = ['I_K+\n(tip)', 'I_s\n(replace Q)', 'I_e\n(force move)']
    colors_bar = [COLORS[2], COLORS[3], COLORS[1]]
    bars = ax3.bar(operators, switch_rates / 60 * 100, color=colors_bar,
                   edgecolor='black', linewidth=0.5)
    ax3.set_ylabel('Agents switching peaks (%)')
    ax3.set_title('(c) Attractor Switching Rate', fontweight='bold')
    ax3.set_ylim(0, 60)
    for bar, rate in zip(bars, switch_rates):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{int(rate)}/60', ha='center', fontsize=10)

    # Panel D: Q-map difference heatmaps
    if 'example_q_a' in data:
        ax4 = fig.add_subplot(gs[1, 1])
        q_diff = np.abs(data['example_q_a'] - data['example_q_b'])
        im4 = ax4.imshow(q_diff, cmap='hot', origin='lower')
        ax4.set_title('(d) |Q_endo - Q_interv|\nat horizon', fontweight='bold')
        plt.colorbar(im4, ax=ax4, label='Q difference', shrink=0.7)
        ax4.plot(peak_a[1], peak_a[0], 'c*', markersize=12)
        ax4.plot(peak_b[1], peak_b[0], 'c*', markersize=12)

        # Panel E: Side-by-side Q-maps
        ax5 = fig.add_subplot(gs[1, 2])
        # Show intervened agent's Q-map
        im5 = ax5.imshow(data['example_q_b'], cmap='RdBu_r', origin='lower',
                         vmin=-1, vmax=1)
        ax5.set_title("(e) Intervened Agent's\nFinal Q-Map", fontweight='bold')
        plt.colorbar(im5, ax=ax5, label='Q value', shrink=0.7)
        ax5.plot(peak_a[1], peak_a[0], 'k*', markersize=12)
        ax5.plot(peak_b[1], peak_b[0], 'k*', markersize=12)

    save_fig(fig, 'fig4_island_attractors.png')


# ============================================================
# Figure 5: Operator Discrimination
# ============================================================
def fig_operator_discrimination():
    print("Figure 5: Operator discrimination")
    data = np.load(os.path.join(RESULTS_DIR, 'exp6_operator_discrimination.npz'))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    t = data['timesteps']

    # Panel A: D_Q(t) timeseries by operator
    operators = [
        ('I_Kplus_expand', 'I_K+ (expand)', COLORS[2], '-', 'preserved'),
        ('I_Kminus_truncate', 'I_K- (truncate)', COLORS[4], '--', 'partial'),
        ('I_Kw_bias', 'I_Kw (bias)', COLORS[5], '-.', 'preserved'),
        ('I_e_force_enc', 'I_e (force)', COLORS[1], '-', 'broken'),
        ('I_s_partial', 'I_s (partial)', COLORS[3], '--', 'broken'),
        ('I_s_full', 'I_s (full)', COLORS[6], '-', 'broken'),
        ('I_U_attenuate', 'I_U (attenuate)', COLORS[7], '-.', 'broken'),
    ]

    for key, label, color, ls, coupling in operators:
        mean_key = f'{key}_mean'
        if mean_key in data:
            mean = data[mean_key]
            ax1.plot(t[:len(mean)], mean, color=color, linewidth=1.8,
                     linestyle=ls, label=label)

    ax1.set_xlabel('Timestep')
    ax1.set_ylabel(r'$D_Q(t)$ — Q-map divergence')
    ax1.set_title('(a) Q-Map Divergence by Operator Type', fontweight='bold')
    ax1.legend(fontsize=8, loc='upper left', ncol=2)

    # Panel B: Final D_Q bar chart ranked
    rankings = []
    for key, label, color, ls, coupling in operators:
        mean_key = f'{key}_mean'
        if mean_key in data:
            final_val = data[mean_key][-1]
            rankings.append((final_val, label, color, coupling))

    rankings.sort()
    labels = [r[1] for r in rankings]
    values = [r[0] for r in rankings]
    colors_bar = [r[2] for r in rankings]
    couplings = [r[3] for r in rankings]

    bars = ax2.barh(range(len(rankings)), values, color=colors_bar,
                    edgecolor='black', linewidth=0.5)

    # Add coupling status annotation
    for i, (val, label, color, coupling) in enumerate(rankings):
        marker = {'preserved': 'o', 'partial': 's', 'broken': 'X'}[coupling]
        ax2.scatter(val + 0.3, i, marker=marker, s=80, color='black', zorder=5)

    ax2.set_yticks(range(len(rankings)))
    ax2.set_yticklabels(labels, fontsize=10)
    ax2.set_xlabel(r'$D_Q(H)$ — Final Q-map divergence')
    ax2.set_title('(b) Operator Ranking by Divergence', fontweight='bold')

    # Legend for coupling status markers
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black',
               markersize=8, label='Coupling preserved'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='black',
               markersize=8, label='Coupling partial'),
        Line2D([0], [0], marker='X', color='w', markerfacecolor='black',
               markersize=8, label='Coupling broken'),
    ]
    ax2.legend(handles=legend_elements, fontsize=9, loc='lower right')

    plt.tight_layout()
    save_fig(fig, 'fig5_operator_discrimination.png')


# ============================================================
# Figure 6: Topology Comparison
# ============================================================
def fig_topology_comparison():
    print("Figure 6: Topology comparison")
    data = np.load(os.path.join(RESULTS_DIR, 'exp4_topology_dependence.npz'))

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    t = data['timesteps']
    topos = ['smooth', 'cliff', 'island', 'deceptive']
    labels = ['Smooth', 'Cliff', 'Island', 'Deceptive']

    # Panel A: D_Q(t) by topology
    for i, (topo, label) in enumerate(zip(topos, labels)):
        mean = data[f'{topo}_q_mean']
        std = data[f'{topo}_q_std']
        axes[0].plot(t[:len(mean)], mean, color=COLORS[i], linewidth=2, label=label)
        axes[0].fill_between(t[:len(mean)], mean - std, mean + std,
                             color=COLORS[i], alpha=0.1)

    axes[0].set_xlabel('Timestep')
    axes[0].set_ylabel(r'$D_Q(t)$')
    axes[0].set_title('(a) Q-Map Divergence by Topology', fontweight='bold')
    axes[0].legend(fontsize=10)

    # Panel B: Landscape thumbnails with final D_Q annotation
    L = 31
    gs_inner = axes[1].inset_axes([0, 0, 1, 1])
    axes[1].axis('off')

    inner_fig, inner_axes = plt.subplots(2, 2, figsize=(5, 5))
    for i, (topo, label) in enumerate(zip(topos, labels)):
        ax = inner_axes[i // 2, i % 2]
        p = data[f'{topo}_landscape']
        ax.imshow(p, cmap='RdYlGn', vmin=0, vmax=1, origin='lower')
        final_q = data[f'{topo}_q_mean'][-1]
        ax.set_title(f'{label}\nD_Q={final_q:.2f}', fontsize=10, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    save_fig(inner_fig, 'fig6b_topology_thumbnails.png')

    # Save main panel
    save_fig(fig, 'fig6_topology_comparison.png')


# ============================================================
# Figure 7: Nonstationary (Exp 5)
# ============================================================
def fig_nonstationary():
    print("Figure 7: Nonstationary")
    data = np.load(os.path.join(RESULTS_DIR, 'exp5_nonstationary.npz'))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    drift_mags = data['drift_magnitudes']
    alpha_vals = data['alpha_values']
    regret = data['regret_matrix']
    staleness = data['staleness_matrix']

    # Panel A: Staleness heatmap
    sns.heatmap(staleness, ax=ax1, annot=True, fmt='.1f', cmap='YlOrRd',
                xticklabels=[f'{a:.2f}' for a in alpha_vals],
                yticklabels=[f'{d:.3f}' for d in drift_mags],
                cbar_kws={'label': 'Q-map staleness (L2)'})
    ax1.set_xlabel(r'$\alpha$ (learning rate)')
    ax1.set_ylabel('Drift magnitude')
    ax1.set_title('(a) Q-Map Staleness', fontweight='bold')

    # Panel B: Regret heatmap
    sns.heatmap(regret, ax=ax2, annot=True, fmt='.0f', cmap='YlOrRd',
                xticklabels=[f'{a:.2f}' for a in alpha_vals],
                yticklabels=[f'{d:.3f}' for d in drift_mags],
                cbar_kws={'label': 'Regret (oracle - agent)'})
    ax2.set_xlabel(r'$\alpha$ (learning rate)')
    ax2.set_ylabel('Drift magnitude')
    ax2.set_title('(b) Regret vs Oracle', fontweight='bold')

    fig.suptitle('Nonstationary Landscapes: Drift x Learning Rate', fontsize=14, y=1.02)
    plt.tight_layout()
    save_fig(fig, 'fig7_nonstationary.png')


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("GENERATING ALL FIGURES")
    print("=" * 60)

    fig_landscape_gallery()
    fig_intervention_cascade()
    fig_coupling_necessity()
    fig_island_attractors()
    fig_operator_discrimination()
    fig_topology_comparison()
    fig_nonstationary()

    print("\n" + "=" * 60)
    print(f"All figures saved to {FIG_DIR}")
    print("=" * 60)
