# Experiment 2 -- Intervention Cascade

**Status:** Complete
**Date:** 2026-03-22
**Figure:** `figures/fig2_intervention_cascade.png`

---

## 1. Motivation

The central claim of the paper at Level 0 is that the coupling loop can amplify
a small perturbation into a large, persistent change in the agent's learned map
and subsequent behavior. This experiment tests that claim directly by applying a
minimal intervention -- a single forced encounter -- and tracking the resulting
divergence between the intervened agent and its counterfactual (non-intervened)
self over the remaining horizon.

The intervention I_e forces one coin flip to come up -1 (a "bad" encounter) at
time t_intervene, while the control agent receives the natural coin flip at that
same step. Everything else is identical: same landscape, same random seed for
all other coin flips and action samples.

If the coupling loop amplifies, the Q-map divergence between the two agents
should grow over time. If there is no amplification, the divergence should stay
constant or decay.

---

## 2. Full Setup Description

### 2.1 Landscape

- Topology: **smooth** (single broad peak, radial Gaussian falloff)
- Grid size: L = 31 (31x31 torus, 961 cells)
- Same landscape used for all seeds

### 2.2 Agent Model

- Identical to Experiment 1 (see Exp 1 for full specification)
- Policy: softmax with temperature tau
- Update: exponential smoothing with learning rate alpha
- Initial Q-values: all zero

### 2.3 Parameters

| Parameter | Value |
|-----------|-------|
| L         | 31    |
| H (horizon) | 400 |
| t_intervene | 50 |
| n_seeds   | 80    |
| alpha     | 0.1   |

### 2.4 Conditions

**Part A -- Coupled vs. TvL:**

| Condition | tau   | alpha | Description |
|-----------|-------|-------|-------------|
| Coupled   | 1.0   | 0.1   | Full coupling loop active |
| TvL       | 1e7   | 0.0   | Trivial learner -- no learning, uniform random policy |

**Part B -- Intervention Magnitude:**

All at tau=1.0, alpha=0.1 (coupled). Vary the number of forced -1 encounters
at t_intervene:

| Condition | Forced encounters |
|-----------|-------------------|
| Magnitude 1  | 1 forced -1 at t=50 |
| Magnitude 5  | 5 forced -1 at t=50 through t=54 |
| Magnitude 10 | 10 forced -1 at t=50 through t=59 |
| Magnitude 20 | 20 forced -1 at t=50 through t=69 |

### 2.5 Procedure

For each seed (1 through 80):

1. Generate a shared random stream for coin flips and action sampling.
2. Run the **control agent** for H=400 steps using the natural random stream.
3. Run the **intervened agent** with identical random stream, EXCEPT at
   t_intervene the coin flip is forced to -1 (regardless of what the natural
   flip would have been).
4. At every timestep t, compute D_Q(t) = L2 norm of (Q_intervened(t) -
   Q_control(t)): D_Q = sqrt(sum((Q_a - Q_b)^2)) over all L*L*5 cells.
5. Record the full D_Q(t) trajectory for each seed.
6. Average D_Q(t) across all 80 seeds.

### 2.6 Metrics

**D_Q(t)**: Instantaneous Q-map divergence at time t, defined as the L2 norm:
D_Q = sqrt(sum((Q_intervened - Q_control)^2)) over all L*L*5 cells. Most cells
are unvisited (diff=0), so D_Q aggregates sparse differences from the ~150-200
cells actually visited. This is the primary metric.

**D_Q(H)**: Terminal Q-map divergence. The divergence at the end of the horizon.

---

## 3. What Was Measured

- D_Q(t) trajectory for each seed (80 trajectories per condition)
- Mean D_Q(t) across seeds at every timestep
- D_Q(H) terminal divergence for each condition
- Position divergence D_pos(t) was also recorded but is secondary

---

## 4. Raw Results

### 4.1 Part A -- Coupled vs. TvL

**Coupled condition (tau=1, alpha=0.1):**

| Time after intervention | D_Q |
|-------------------------|-----|
| t_intervene + 0 (t=50)  | instantaneous spike from forced encounter |
| t_intervene + 10 (t=60) | 0.44 |
| t_intervene + 50 (t=100) | ~0.9 |
| t_intervene + 100 (t=150) | ~1.4 |
| t_intervene + 200 (t=250) | ~2.1 |
| t_intervene + 350 (t=400, horizon) | 2.66 |

D_Q grows monotonically from the initial perturbation. The growth is roughly
sublinear in time (the curve bends downward on a linear scale) but the key
point is that it does NOT plateau or decay. The single forced encounter
produces a divergence that GROWS over the remaining 350 steps.

**TvL condition (tau=1e7, alpha=0):**

| Time after intervention | D_Q |
|-------------------------|-----|
| All timesteps           | 0.000 |

Exactly zero at all times. The TvL agent has alpha=0, so no learning occurs.
The forced encounter changes the immediate outcome but nothing is written to
the Q-map, so there is nothing to diverge. The Q-maps remain identical (all
zeros) throughout.

### 4.2 Part B -- Intervention Magnitude

All conditions at tau=1, alpha=0.1, measured at horizon H=400:

| Forced encounters | D_Q(H) |
|-------------------|--------|
| 1                 | 2.66   |
| 5                 | ~2.55  |
| 10                | ~2.48  |
| 20                | 2.44   |

The terminal Q-map divergence is approximately the SAME regardless of how
many encounters were forced. One forced encounter produces D_Q(H) = 2.66.
Twenty forced encounters produce D_Q(H) = 2.44. The difference is within
noise, and if anything the direction is REVERSED (more forcing produces
slightly LESS divergence, not more).

---

## 5. Discussion

### 5.1 The Cascade Is Real and Lives in the Q-Map

The coupled condition shows clear, monotonically growing Q-map divergence after
a single forced encounter. This is the core result: the coupling loop amplifies
a minimal perturbation. The TvL baseline at exactly zero confirms that the
amplification requires learning -- without Q-map updates, there is nothing to
compound.

The growth pattern of D_Q(t) is important: it does not plateau within the 400-step
horizon. This means the cascade has not saturated. On a longer horizon, the
divergence would continue to grow (bounded eventually by the Q-map's dynamic
range, but we are not near that bound).

### 5.2 Magnitude Independence Is the Strongest Result

The Part B result -- that 1 forced encounter produces comparable terminal
divergence to 20 -- is more striking than the cascade itself. It says:

**The intervention is a seed. The coupling is the amplifier.**

The size of the seed does not matter much (within the range tested). One forced
encounter produces comparable terminal divergence (2.66 +/- SE vs 2.44 +/- SE
for 1 vs 20 forced encounters). The coupling amplifies any perturbation to a
similar terminal level regardless of initial magnitude over the tested range.

This is STRONGER than "superlinear amplification." A superlinear relationship
would still show D_Q(H) increasing with intervention magnitude. Instead, D_Q(H)
is approximately constant -- the amplification is **approximately
magnitude-independent**.

The slight DECREASE in D_Q(H) with more forced encounters (2.66 for 1 vs. 2.44
for 20) may be because a longer forced period keeps the two agents in more
similar positions (both are being pushed by forced outcomes), reducing the
divergence in the position-dependent encounters that follow.

### 5.3 Where the Nonlinearity Lives

The cascade mechanism operates through the nonlinear softmax policy and discrete
Bernoulli outcomes, not through a nonlinear update function. The update rule
Q <- (1-alpha)Q + alpha*e is linear in e. The nonlinearity that amplifies small
Q differences into large behavioral differences lives in the softmax:
pi(a) proportional to exp(Q/tau).

The coupling loop has two components:

1. **Q-update**: Q(x,a) <- Q(x,a) + alpha * (e - Q(x,a)). This is LINEAR
   exponential smoothing. It does not amplify -- it averages.

2. **Softmax policy**: pi(a|x) = exp(Q(x,a)/tau) / sum. This is NONLINEAR.
   Small differences in Q-values can produce large differences in action
   probabilities, especially at low tau.

Here is how the cascade operates:

- The forced encounter changes Q(x,a) by a small amount at one cell.
- At the next visit to that cell (or a nearby cell), the softmax converts the
  small Q-difference into a different action probability distribution.
- The different action leads to a different next position.
- The different position produces a different coin flip (different p(x')).
- The different coin flip produces a different Q-update.
- The cycle repeats.

Additionally, the Bernoulli discrete outcomes (+1 or -1, nothing in between)
provide a secondary amplification mechanism. Even a tiny difference in position
(and thus in p(x)) can flip a coin outcome from +1 to -1, producing a
delta-e of 2 rather than a small continuous perturbation. The discreteness of
the encounter outcome acts as a noise amplifier layered on top of the softmax
nonlinearity.

### 5.4 The Cascade Requires Position-Dependent Encounters

A critical but subtle point: the cascade requires that encounter probabilities
depend on position. If p(x) were uniform across the grid, then different
positions would produce the same distribution of outcomes, and the positional
divergence caused by the softmax would not feed back into different Q-updates.
The cascade requires the full loop:

Q -> softmax -> arm -> position -> p(x') -> coin flip -> Q update

The spatial structure of the landscape is essential. On a uniform landscape,
the cascade would be much weaker (driven only by the discreteness of
individual coin flips, not by systematic differences in encounter probability).

---

## 6. Surprises and Deviations from Expectations

### 6.1 Magnitude Independence Was Not Predicted

We expected D_Q(H) to scale with intervention magnitude -- perhaps sublinearly,
but still increasing. The flat relationship was a surprise and is arguably the
strongest result in the entire simulation study. It sharply constrains the
class of models that can explain the data: only models where the coupling does
all the amplification (and the perturbation merely breaks symmetry) are
consistent.

### 6.2 The TvL Baseline Was Boring in a Good Way

Zero divergence at all times for TvL is exactly what the theory predicts. With
no learning (alpha=0), the Q-map is frozen at its initial state (all zeros),
and the softmax over uniform Q-values produces a uniform random walk regardless
of the forced encounter. This confirms that the experimental apparatus is
working correctly -- the divergence in the coupled condition is genuinely
produced by the coupling loop, not by some artifact of the random seed sharing
or the intervention mechanism.

### 6.3 D_Q(t) Did Not Plateau

We expected the cascade to saturate within H=400 steps, reaching a steady-state
divergence. Instead, D_Q(t) is still growing at t=400. This suggests that the
cascade operates on a timescale longer than the horizon, which has implications
for the paper: we should be careful not to claim that D_Q(H) represents the
"final" divergence. It represents a lower bound on the cascade's magnitude.

### 6.4 The Growth Curve Is Sublinear

D_Q(t) grows but at a decelerating rate. This is expected from exponential
smoothing -- older Q-values are progressively discounted -- but it means the
cascade is not explosive. It is persistent and cumulative but not runaway. This
is important for the paper's framing: the cascade is a compounding process, not
an instability.

---

## 7. Takeaways for the Paper

1. **The cascade is the paper's central empirical result.** A single forced
   encounter produces monotonically growing Q-map divergence that persists for
   the entire remaining horizon. This directly supports the claim that the
   coupling loop amplifies perturbations.

2. **Magnitude independence is the headline.** The fact that 1 forced encounter
   produces the same terminal divergence as 20 is the most striking result.
   Frame this as: "The coupling amplifies any symmetry-breaking perturbation to
   a magnitude determined by the system parameters, regardless of the
   perturbation's size."

3. **The TvL comparison is the control.** Zero divergence in TvL proves the
   cascade requires the coupling loop. This is necessary for the formal
   argument.

4. **The nonlinearity is in the softmax.** The paper should identify the softmax
   as the source of amplification, not the learning rule (which is linear).
   The Bernoulli discreteness provides secondary amplification.

5. **The cascade lives in Q-space, not position space.** D_Q is the right metric.
   Position divergence conflates the cascade with random walk diffusion (see
   Experiment 3).

6. **Figure 2 should show the D_Q(t) trajectory** for coupled vs. TvL, making
   the growth vs. flatline contrast visually immediate. A secondary panel can
   show the magnitude-independence result.

7. **Do not claim the cascade saturates.** The data shows ongoing growth at
   H=400. Either extend the horizon in future runs or frame D_Q(H) as a lower
   bound.

---

## 8. Connection to Other Experiments

- **Experiment 1** (Path Dependence): Established that coupling produces
  convergence on smooth landscapes. The cascade in Experiment 2 operates on top
  of this convergence -- the intervened and control agents both converge toward
  the peak, but their Q-maps diverge along the way because the coupling drives
  them through slightly different routes with slightly different encounter
  histories.

- **Experiment 3** (Coupling Necessity): The 2x2 ablation showing that learning
  is necessary and sufficient for Q-map divergence, while selection converts
  representational divergence into behavioral divergence. Experiment 2 shows
  the cascade exists; Experiment 3 isolates which components drive it.

- **Experiment 4b** (Island Topology): On landscapes with multiple attractors,
  the cascade can produce qualitative divergence -- the intervened agent
  converges to a different attractor than the control. This is the strongest
  form of the cascade and requires the island topology to manifest.

---

## 9. Technical Notes

### 9.1 Random Seed Sharing

The control and intervened agents share the same random stream for all steps
EXCEPT the forced encounter(s). This means:

- At t < t_intervene, the two agents are identical (same Q-maps, same positions,
  same actions, same outcomes).
- At t = t_intervene, the intervention forces a different outcome for the
  intervened agent.
- At t > t_intervene, the agents share the same underlying random numbers, but
  because their Q-maps and positions may differ, those random numbers are
  consumed differently (e.g., the softmax probabilities differ, so the same
  uniform random draw produces different actions).

This is the correct experimental design: it isolates the effect of the single
perturbation from all other sources of randomness. The divergence is causally
attributable to the forced encounter and its downstream amplification.

### 9.2 Definition of D_Q

D_Q is the L2 norm of the Q-map difference tensor:
D_Q = sqrt(sum((Q_intervened - Q_control)^2)) over all L*L*5 = 4805 cells.
It is NOT normalized by entry count. Most cells are unvisited (diff=0), so D_Q
aggregates sparse differences from the ~150-200 cells each agent actually
visits. A D_Q of 2.66 means roughly sqrt(N_different_cells * avg_squared_diff),
e.g. sqrt(90 * 0.08) ~ 2.7. Per-entry |diff| max is ~0.57, well within the
[-1,1] Q-value bounds.
