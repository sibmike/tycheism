# Tychism Paper I — Simulation

Spatial bandit simulation that produces every quantitative result in *Tychism I: Trajectory Divergence in Coupled Stochastic Learning Systems*.

## Install

```bash
pip install -r requirements.txt
```

Tested with Python 3.10+ and the package versions in `requirements.txt` (numpy, scipy, matplotlib, seaborn).

## The Model

An agent navigates an L×L toroidal grid. Each cell hides a coin with bias `p(x) ∈ [0,1]`. At each timestep:

1. **Select arm** via softmax over Q-values of neighbouring cells: `π(a) ∝ exp(Q(target(a,x)) / τ)`
2. **Move** to the target cell
3. **Flip the coin**: encounter `e = +1` with probability `p(x)`, `−1` otherwise
4. **Update Q**: `Q(x) ← (1−α)·Q(x) + α·e`

The coupling loop: `Q → softmax → arm → position → coin flip → Q update`. The coin flip is genuine ontological chance — Peirce's tychism. The agent never observes `p(x)` directly; it only learns through experience.

The primary divergence metric is `D_Q`, the L2 norm of the difference between two agents' Q-maps.

## Layout

```
simulation/
├── core/                  # Agent, landscape, intervention operators, simulation loop
├── analysis/              # D_Q and other metrics
├── experiments/           # Seven experiment scripts (see below)
├── docs/                  # Per-experiment write-ups + cross-experiment synthesis
├── figures/               # Generated PNG figures (committed)
├── results/               # Saved .npz result files (committed)
├── requirements.txt
└── generate_figures.py    # Rebuild all figures from results/
```

## Experiments

| Script | What it shows |
|---|---|
| `exp1_path_dependence.py` | Two identical agents on identical landscapes diverge from chance alone — establishes the baseline path-dependence. |
| `exp2_intervention_cascade.py` | A single forced encounter compounds: Q-map divergence rises from 0.44 (10 steps post-intervention) to 2.66 (350 steps). Magnitude independence: 1 forced flip ≈ 20. |
| `exp3_coupling_necessity.py` | Decomposes the loop into representational vs behavioural cascades. The full coupling loop is necessary to convert learning differences into different destinations. |
| `exp4_topology_dependence.py` | Sweeps landscape topology to test which environments amplify or dampen the cascade. |
| `exp4b_island_convergence.py` | Two-peak landscape: a single intervention can lock two otherwise-identical agents onto different attractors permanently. |
| `exp5_nonstationary.py` | Shifting reward landscapes — does the cascade survive when the environment itself changes? |
| `exp6_operator_discrimination.py` | Six intervention operators ranked by terminal divergence. Three clusters from option expansion (lowest cost) to full state replacement (highest). |

Run any experiment from the `simulation/` directory:

```bash
python -m experiments.exp2_intervention_cascade
```

Each script writes to `results/<experiment>.npz`. **Running an experiment overwrites the committed results file.** The committed `.npz` files are present so you can reproduce the figures without re-running the (slow) experiments.

## Regenerating Figures

```bash
python generate_figures.py
```

Reads everything in `results/` and writes to `figures/`. Requires `seaborn` and a working matplotlib backend; the script forces the `Agg` backend so it works on headless machines.

## Per-experiment write-ups

Detailed methodology, results tables, and analysis for each experiment live in `docs/`. The cross-experiment synthesis is `docs/synthesis_all_experiments.md`.
