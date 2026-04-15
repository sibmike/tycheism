# Experiment 5: Nonstationary Landscapes

## Overview

This experiment tests whether nonstationarity in the reward landscape — rewards
that drift over time — interacts with the agent's learning rate to produce
detectable effects on regret and Q-map staleness. The motivation is that several
real-world interventions (particularly I_s, state replacement) effectively create
nonstationarity from the agent's perspective: the implanted Q-map was calibrated
to a different reward landscape than the one the agent is currently experiencing.

The result is a weak signal. The effects exist but are modest at the drift
magnitudes tested. This experiment is an extension, not a core result.


---

## Setup

### Landscape

Standard smooth landscape on L=31 grid (31x31, 961 cells). Single Gaussian peak
centered on the grid. The peak reward probability is ~0.9 at the center,
decaying to ~0.1 at the edges.

### Nonstationarity Mechanism

At each timestep, the reward probability at each cell is perturbed:

    p(x, t+1) = clip(p(x, t) + drift * N(0,1), 0, 1)

where `drift` is the drift magnitude parameter and N(0,1) is a standard normal
draw independent at each cell. The clip ensures probabilities stay in [0,1].

This produces a landscape where the reward structure is locally preserved (small
perturbations) but gradually wanders over time. At high drift values, the
landscape becomes effectively random within a few hundred steps. At low drift
values, the landscape structure is nearly preserved throughout the run.

Note: the drift is applied independently to each cell, so the spatial correlation
structure of the landscape is gradually destroyed. The peak may flatten, shift,
or fragment depending on the drift magnitude and duration.

### Agent

Standard spatial bandit agent:
- Q-learning update: Q(x) <- Q(x) + alpha * (r - Q(x)) where r is the Bernoulli
  coin flip outcome and x is the current position.
- Action selection: softmax(Q/tau) over neighboring cells.
- No intervention applied. This is a pure learning-rate vs. drift interaction study.

### Parameter Grid

| Parameter       | Values                          |
|-----------------|---------------------------------|
| L               | 31                              |
| H               | 400                             |
| n_seeds         | 40                              |
| drift           | {0, 0.005, 0.01, 0.02, 0.05}   |
| alpha           | {0.01, 0.05, 0.1, 0.2, 0.5}    |
| tau             | default                         |

Total configurations: 5 drift values x 5 alpha values = 25 conditions.
Total runs: 25 x 40 seeds = 1000 runs.

### What Was Measured

1. **Cumulative regret at H=400**: Sum over all timesteps of (optimal_reward(t) -
   actual_reward(t)), where optimal_reward(t) is the maximum reward probability
   available on the landscape at time t. Note that under nonstationarity, the
   optimal location may change over time.

2. **Q-map staleness**: Measured as the L2 norm between the agent's current Q-map
   and the "true" reward probability map at each timestep. This captures how
   well the agent's beliefs track the actual landscape. Reported as mean
   staleness over the last 100 timesteps (t=300 to t=400).

3. **Tracking accuracy**: Fraction of timesteps in the last 100 where the agent
   is within radius 3 of the current optimal location. This measures whether
   the agent can track a moving target.


---

## Raw Results

### Cumulative Regret at H=400

Table of mean regret (over 40 seeds) for each (drift, alpha) combination:

| drift \ alpha | 0.01  | 0.05  | 0.1   | 0.2   | 0.5   |
|---------------|-------|-------|-------|-------|-------|
| 0.000         | ~340  | ~330  | ~325  | ~322  | ~320  |
| 0.005         | ~345  | ~333  | ~328  | ~324  | ~322  |
| 0.010         | ~350  | ~338  | ~332  | ~328  | ~325  |
| 0.020         | ~358  | ~345  | ~340  | ~335  | ~330  |
| 0.050         | ~375  | ~360  | ~352  | ~340  | ~335  |

(Values are approximate, rounded from simulation output.)

Key observations:
- At drift=0, higher alpha produces slightly lower regret (320 vs 340). This is
  the standard result: faster learners converge faster.
- At drift=0.05, the spread widens: alpha=0.01 gives regret ~375 while alpha=0.5
  gives ~335. A difference of ~40 regret units.
- The drift effect is monotonic: higher drift always increases regret.
- The alpha effect is also monotonic: higher alpha always decreases regret
  (faster tracking of the changing landscape).

### Q-map Staleness (last 100 steps)

| drift \ alpha | 0.01  | 0.05  | 0.1   | 0.2   | 0.5   |
|---------------|-------|-------|-------|-------|-------|
| 0.000         | low   | low   | low   | low   | low   |
| 0.005         | slight| low   | low   | low   | low   |
| 0.010         | mod   | slight| low   | low   | low   |
| 0.020         | mod   | mod   | slight| low   | low   |
| 0.050         | high  | mod   | mod   | slight| low   |

(Qualitative labels; exact numeric values available but not highly informative
given the weak signal.)

Staleness increases with drift and decreases with alpha, as expected. Slow
learners on drifting landscapes accumulate stale Q-values because their update
rate cannot keep pace with the landscape changes.

### Tracking Accuracy (last 100 steps)

At drift=0, all alphas achieve >90% tracking accuracy (the peak doesn't move).
At drift=0.05, tracking drops to ~60% for alpha=0.01 and ~80% for alpha=0.5.
The effect is present but the agent never completely loses the peak, even at
the highest drift, because the drift is applied independently to each cell and
the peak structure is partially preserved stochastically.


---

## Discussion

### The Effect Is Real but Small

The drift-alpha interaction exists and behaves as predicted: faster learners
track nonstationary landscapes better, slower learners accumulate stale beliefs.
But the magnitude of the effect is modest. The worst case (drift=0.05,
alpha=0.01) produces only ~17% more regret than the best case (drift=0,
alpha=0.5): 375 vs 320.

This is not a dramatic result. It would not, on its own, justify a section in
the paper.

### Why the Signal Is Weak

Several factors contribute to the weak signal:

1. **Drift magnitudes are small relative to the landscape scale.** At drift=0.05,
   each cell's reward probability changes by ~0.05 per step in expectation. Over
   400 steps, this could accumulate to large changes, but the clip to [0,1]
   prevents unbounded drift, and the spatial averaging over the agent's
   exploration region further attenuates the effect.

2. **The smooth landscape has a broad peak.** The agent doesn't need to be
   precisely at the optimum to capture most of the available reward. Even if the
   peak drifts by a few cells, the agent's current position is still in a
   high-reward region.

3. **Independent cell drift destroys structure slowly.** Because drift is applied
   independently to each cell, the spatial correlation of the landscape degrades
   gradually. The peak doesn't "jump" — it blurs. The agent can still exploit
   the blurred peak.

4. **40 seeds may be insufficient** to detect a subtle interaction cleanly,
   especially at low drift magnitudes where the effect is buried in stochastic
   noise.

### The Interesting Connection Is Conceptual, Not Empirical

The real reason this experiment was run is the following conceptual argument:

When an I_s (state replacement) intervention implants a Q-map calibrated to a
different agent's experience, the receiving agent effectively faces a
nonstationary landscape — not because the physical landscape changed, but because
its Q-map was calibrated to a different local patch of the landscape. The
implanted Q-values are "stale" relative to the receiving agent's actual position
and local reward structure.

This argument connects nonstationarity to the intervention operator framework:
I_s creates artificial nonstationarity, and the receiving agent's alpha determines
how quickly it can recalibrate.

However, this connection is better made CONCEPTUALLY in the paper text than
demonstrated through the weak empirical signal in this experiment. The simulation
shows that alpha-drift interactions exist, but the magnitude is too small to
carry a main argument. The paper should reference this experiment as supporting
evidence for the conceptual claim, not as a standalone result.

### What Would Make This Stronger

If we wanted a strong empirical result from nonstationarity, we would need:
- Larger drift magnitudes (0.1 to 0.5 per step)
- Sharper landscapes where precise tracking matters
- Longer horizons to accumulate the effect
- Direct comparison: run I_s on a nonstationary landscape and show that alpha
  modulates the recovery time

But this is scope expansion that is probably not warranted for Paper A.


---

## Surprises / Deviations from Expectations

1. **The effect was weaker than expected.** We anticipated a more dramatic
   interaction, but the smooth landscape and moderate drift magnitudes produced
   only a gentle gradient across the parameter space.

2. **High alpha did not produce instability.** We expected that alpha=0.5 on a
   stationary landscape (drift=0) might produce oscillatory Q-values and higher
   regret due to overreaction to stochastic rewards. Instead, alpha=0.5 produced
   the lowest regret across all conditions. On this simple landscape, faster
   learning is unambiguously better.

3. **The staleness metric was not very informative.** Staleness (Q-map vs true
   landscape divergence) tracks drift and alpha monotonically, but doesn't
   reveal any nonlinear interactions or threshold effects. It confirms the
   obvious without adding insight.

4. **No qualitative transition was observed.** We hoped to see a phase transition
   where slow learners on fast-drifting landscapes would "lose" the peak entirely,
   producing a qualitative change in behavior (random walk instead of directed
   exploitation). This did not occur at any tested parameter combination. The
   agent always retained partial knowledge of the peak structure.


---

## Takeaways for the Paper

1. **Include as supplementary or brief discussion, NOT as a main result.** The
   signal is too weak to carry a section.

2. **The conceptual argument is stronger than the empirical demonstration.**
   The paper should argue that I_s creates artificial nonstationarity from the
   agent's perspective, and that alpha modulates recalibration speed. This
   argument can reference the experiment as supporting evidence but should not
   depend on it.

3. **If included, present as a 2-3 sentence summary** with the figure in
   supplementary material: "We tested drift magnitudes from 0 to 0.05 across
   five learning rates. Higher drift increases regret and Q-map staleness, with
   the effect modulated by alpha. The interaction confirms that learning rate
   determines tracking capacity in nonstationary environments, supporting the
   conceptual connection between I_s interventions and nonstationarity."

4. **Do not oversell.** The regret difference between best and worst conditions
   is ~17%. This is detectable but not dramatic.

5. **Possible paper framing**: "The nonstationary extension confirms that alpha
   governs tracking fidelity, which becomes relevant when interventions like I_s
   introduce artificial nonstationarity by implanting Q-maps calibrated to
   different environmental patches."


---

## Figure Reference

figures/fig7_nonstationary.png
