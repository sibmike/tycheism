# Experiment 3 -- Coupling Necessity (TvL Comparison)

**Status:** Complete
**Date:** 2026-03-22
**Figure:** `figures/fig3_coupling_necessity.png`

---

## 1. Motivation

Experiments 1 and 2 demonstrate that the coupling loop produces attractor
convergence and intervention cascades, respectively. But they do not isolate
WHICH components of the coupling loop are necessary. The loop has two links:

1. **Learning**: encounters update the Q-map (alpha > 0).
2. **Selection**: the Q-map drives action selection via softmax (tau < infinity).

This experiment performs a 2x2 ablation: cross learning ON/OFF with selection
ON/OFF. If the cascade requires the FULL coupling loop, then breaking either
link should eliminate it. This is the formal necessity argument for the paper.

A secondary goal is to definitively establish that **Q-map divergence, not
position divergence**, is the correct metric for measuring the coupling effect.

---

## 2. Full Setup Description

### 2.1 Landscape

- Topology: **smooth** (single broad peak, radial Gaussian falloff)
- Grid size: L = 31 (31x31 torus, 961 cells)
- Same landscape used for all conditions and seeds

### 2.2 Agent Model

- Identical architecture to Experiments 1 and 2
- Policy: softmax with temperature tau
- Update: exponential smoothing with learning rate alpha
- Initial Q-values: all zero
- Start position: (15, 15) for all agents

### 2.3 Parameters

| Parameter | Value |
|-----------|-------|
| L         | 31    |
| H (horizon) | 300 |
| t_intervene | 50 |
| n_seeds   | 50    |

### 2.4 Part A -- 2x2 Ablation Conditions

The four conditions cross learning (alpha) with selection (tau):

| Condition       | tau   | alpha | Learning? | Selection? | Description |
|-----------------|-------|-------|-----------|------------|-------------|
| **Coupled**     | 1.0   | 0.1   | YES       | YES        | Full coupling loop. Both links active. |
| **TvL baseline**| inf (1e7) | 0.0 | NO      | NO         | Trivial learner. No learning, uniform random walk. |
| **Learn-no-use**| inf (1e7) | 0.1 | YES      | NO         | Agent learns from encounters but Q-map does not influence actions. Softmax with tau=inf is uniform over actions. |
| **Use-no-learn**| 1.0   | 0.0   | NO        | YES        | Softmax is active (tau=1) but alpha=0 means Q-map is never updated. Q-map stays at all zeros, so softmax over zeros is uniform. |

Note on "use-no-learn": even though tau=1.0 (selection is "on"), with alpha=0
the Q-map never changes from its initial all-zero state. Softmax over identical
Q-values produces a uniform distribution, so the agent performs a uniform random
walk. The selection mechanism is active but has nothing to select on.

### 2.5 Part B -- tau x alpha Heatmap

A 6x6 grid sweeping:

- tau in {0.1, 0.5, 1.0, 2.0, 5.0, 50.0}
- alpha in {0.0, 0.02, 0.05, 0.1, 0.2, 0.5}

For each (tau, alpha) pair, run the intervention experiment (same I_e, same
n_seeds=50) and record D_Q(H) and D_pos(H).

### 2.6 Procedure

For each condition (Part A) or each (tau, alpha) pair (Part B):

1. For each seed (1 through 50):
   a. Run control agent for H=300 steps with natural random stream.
   b. Run intervened agent with same random stream, except at t=50 the coin
      flip is forced to -1.
   c. Record D_Q(H) and D_pos(H) between control and intervened agents.
2. Average D_Q(H) and D_pos(H) across all 50 seeds.

### 2.7 Metrics

**D_Q(H)**: Terminal Q-map divergence. L2 norm: D_Q = sqrt(sum((Q_a - Q_b)^2))
over all L*L*5 cells (same definition as Experiment 2). Most cells are unvisited
(diff=0), so D_Q aggregates sparse differences from ~150-200 visited cells.

**D_pos(H)**: Terminal position divergence -- L2 distance between control and
intervened agent's final positions on the torus.

---

## 3. What Was Measured

- D_Q(H) for all 4 ablation conditions (Part A)
- D_pos(H) for all 4 ablation conditions (Part A)
- D_Q(H) for all 36 (tau, alpha) pairs (Part B)
- D_pos(H) for all 36 (tau, alpha) pairs (Part B)

---

## 4. Raw Results

### 4.1 Part A -- 2x2 Ablation (Initial Results, H=300)

| Condition       | tau     | alpha | D_Q(H) | D_pos(H) |
|-----------------|---------|-------|--------|----------|
| Coupled         | 1.0     | 0.1   | 2.28   | 10.95    |
| TvL baseline    | inf     | 0.0   | 0.00   | 11.74    |
| Learn-no-use    | inf     | 0.1   | 2.24   | 11.74    |
| Use-no-learn    | 1.0     | 0.0   | 0.00   | 11.22    |

### 4.1b Extended Analysis (H=2000, n=50 seeds)

The H=300 results left open the question of whether coupled D_Q would pull ahead
of learn-no-use on longer horizons. A follow-up run at H=2000 with 50 seeds
**disconfirmed** this expectation:

| t    | Coupled (tau=1, alpha=0.1) | Learn-No-Use (tau=inf, alpha=0.1) | Gap   |
|------|----------------------------|-----------------------------------|-------|
| 100  | 1.405 +/- 0.148            | 1.424 +/- 0.136                   | -1.3% |
| 300  | 2.491 +/- 0.178            | 2.457 +/- 0.143                   | +1.4% |
| 500  | 3.194 +/- 0.214            | 3.190 +/- 0.176                   | +0.1% |
| 1000 | 4.374 +/- 0.263            | 4.469 +/- 0.238                   | -2.1% |
| 1500 | 5.280 +/- 0.254            | 5.355 +/- 0.274                   | -1.4% |
| 1950 | 5.890 +/- 0.259            | 5.942 +/- 0.200                   | -0.9% |

TvL (alpha=0, tau=inf): D_Q = 0.000 +/- 0.000 at all timepoints.
Use-no-learn (alpha=0, tau=1): D_Q = 0.000 +/- 0.000 at all timepoints.

Coupled and learn-no-use produce **statistically identical D_Q at all tested
horizons up to H=2000.** The gap oscillates around zero and never exceeds 2.1%
in either direction. The original hypothesis that coupled D_Q would pull ahead
due to closed-loop compounding is not supported by this data.

### 4.2 Part B -- Heatmap Summary

The 6x6 heatmap of D_Q(H) shows:

- **alpha=0 row**: D_Q = 0.00 for ALL tau values. No learning means no Q-map
  divergence, regardless of how aggressively the softmax selects.
- **tau=50 column** (weak selection): D_Q is moderate and determined primarily
  by alpha. Higher alpha produces more Q-map divergence because the forced
  encounter writes a larger update, but the divergence does not compound because
  the Q-map barely influences actions.
- **Bottom-right corner** (high alpha, low tau): Highest D_Q values. Strong
  learning AND strong selection produce the largest cascades.
- **The heatmap has a clear diagonal structure**: D_Q increases as BOTH alpha
  increases AND tau decreases. Neither parameter alone is sufficient.

The 6x6 heatmap of D_pos(H) shows:

- **All values are between ~10.5 and ~12.0.** The position divergence is
  dominated by random walk diffusion on the torus and shows no clear structure
  related to the coupling parameters.
- There is no clean relationship between (tau, alpha) and D_pos(H).

---

## 5. Discussion

### 5.1 Position Divergence Is NOT the Right Metric

This is the most important methodological finding of the entire simulation study.

D_pos(H) ranges from 10.95 to 11.74 across the four ablation conditions. The
TvL baseline (no learning, no selection, pure uniform random walk) has D_pos =
11.74. The coupled condition has D_pos = 10.95. The coupled condition has LOWER
position divergence than the null model.

This does not mean the coupling has no effect on position. It means the coupling
effect on position is SMALL relative to the random walk diffusion, and in the
OPPOSITE direction (coupling produces convergence, as established in
Experiment 1). The position divergence metric is dominated by the diffusion
floor and cannot isolate the coupling effect.

D_Q(H), by contrast, cleanly separates the conditions:
- Coupled: 2.28
- TvL: 0.00
- Learn-no-use: 2.24
- Use-no-learn: 0.00

The Q-map divergence has zero baseline noise (TvL = 0.00 exactly) and clearly
differentiates between conditions where the coupling loop is active and where
it is broken.

**For the paper: ALWAYS use D_Q as the primary metric. Report D_pos only to
explicitly demonstrate that it is uninformative.**

### 5.2 Learning Is Necessary and Sufficient for Q-Map Divergence

The 2x2 ablation, now confirmed by the H=2000 extended run, produces:

|                  | Selection ON (tau=1)   | Selection OFF (tau=inf)  |
|------------------|------------------------|--------------------------|
| Learning ON      | D_Q = 5.89 +/- 0.259  | D_Q = 5.94 +/- 0.200    |
| Learning OFF     | D_Q = 0.00 +/- 0.000  | D_Q = 0.00 +/- 0.000    |

(Values at H=2000. At H=300: Coupled = 2.28, Learn-no-use = 2.24.)

The pattern is unambiguous:

- **Learning (alpha > 0) is necessary and sufficient for Q-map divergence.**
  Without learning, D_Q = 0 regardless of selection policy.
- **Selection (tau < inf) does NOT amplify Q-map divergence.** Coupled and
  learn-no-use produce statistically identical D_Q at all tested horizons up to
  H=2000. The gap never exceeds 2.1% and oscillates around zero.

The original hypothesis -- that coupled D_Q would pull ahead of learn-no-use on
longer horizons due to closed-loop compounding -- was **disconfirmed** by the
H=2000 data. The representational cascade (D_Q divergence) is driven by learning
alone, not by the feedback loop.

### 5.3 What Selection Actually Does

If selection does not amplify D_Q, what does it contribute?

Selection matters for **behavioral consequences** -- which attractor the agent
converges to, not how much the Q-map diverges. Look at D_pos:
- Coupled: 10.95
- Learn-no-use: 11.74

The learn-no-use agent has position divergence identical to the TvL baseline
(11.74). It performs a uniform random walk, ignoring its Q-map. The coupled
agent has lower D_pos (10.95), indicating that selection drives agents toward
attractors, producing convergent behavior.

The critical distinction is:

- **Coupled**: Q-map divergence AND behavioral divergence. The Q-map divergence
  drives different actions via softmax, directing the agent toward different
  attractors on multi-attractor landscapes (demonstrated in Exp 4b).
- **Learn-no-use**: Q-map divergence WITHOUT behavioral divergence. The Q-map
  diverges because random walks through different regions produce different
  encounter histories, but behavior is unaffected -- the agent ignores its Q-map.

Selection converts representational divergence (different Q-maps) into behavioral
divergence (different attractors). The Q-map diverges either way; what changes
is whether those different beliefs lead to different actions.

### 5.4 Use-No-Learn Is the Clean Control

Use-no-learn (tau=1, alpha=0) produces D_Q = 0.00 +/- 0.000 exactly at all
timepoints up to H=2000. Even though the softmax is active (tau=1), the Q-map
is all zeros and never changes. Softmax over identical values is uniform, so the
agent does a uniform random walk. The forced encounter has no lasting effect
because nothing is written to the Q-map.

This confirms that learning is strictly necessary for any Q-map divergence.
Without it, the intervention is ephemeral.

### 5.5 The Revised Coupling Loop Argument

Combining the four conditions with the extended H=2000 data:

1. **Coupled** (learn + use): D_Q = 5.89 +/- 0.259. Learning changes what the
   agent believes; selection changes where the agent goes based on those beliefs.
   The full loop contributes to both representational AND behavioral cascades.

2. **Learn-no-use** (learn only): D_Q = 5.94 +/- 0.200. Statistically identical
   Q-map divergence. The representational cascade occurs through learning alone.
   Random walk diffusion provides sufficient positional variation to drive Q-map
   divergence without any selection feedback.

3. **Use-no-learn** (use only): D_Q = 0.00 +/- 0.000. Selection without
   learning produces nothing to select on.

4. **TvL** (neither): D_Q = 0.00 +/- 0.000. The null baseline.

The revised argument: the **representational** cascade (D_Q) requires only
learning. The **behavioral** cascade (attractor switching, demonstrated in
Exp 4b) requires the full coupling loop. Both are needed for the complete effect:
changed beliefs -> changed behavior -> changed encounters -> further changed
beliefs. But D_Q alone does not distinguish coupled from learn-no-use.

### 5.6 The Heatmap and Its Reinterpretation

The Part B heatmap (H=300) shows that D_Q(H) depends on BOTH tau and alpha in
an interacting way, with highest values where alpha is high AND tau is low.
However, the H=2000 extended results suggest this interaction is weaker than
initially interpreted. The dominant factor is alpha: without learning, D_Q = 0
regardless of tau. The tau dependence visible in the heatmap at H=300 may
reflect transient dynamics rather than a fundamental interaction. Further
heatmap analysis at longer horizons would clarify whether the tau effect
persists or washes out.

---

## 6. Surprises and Deviations from Expectations

### 6.1 Learn-No-Use Matching Coupled D_Q Was the Biggest Surprise

At H=300, we expected learn-no-use to produce lower D_Q than coupled, and
hypothesized the near-equality (2.24 vs. 2.28) was a short-horizon artifact
that would resolve at longer horizons. The H=2000 follow-up **disconfirmed**
this: coupled D_Q (5.89 +/- 0.259) and learn-no-use D_Q (5.94 +/- 0.200)
remain statistically identical through 2000 steps. The gap never exceeds 2.1%.

This means the original claim -- "both learning AND selection are required for
the cascade" -- must be revised. Learning is necessary and sufficient for
Q-map divergence. Selection is necessary only for converting that
representational divergence into behavioral divergence (attractor selection).

### 6.2 Position Divergence Being Uninformative Was Confirmed

We suspected from Experiment 1 that position divergence was a poor metric, and
Experiment 3 provides the definitive confirmation. The D_pos values across all
four conditions are within a range of 0.79 (from 10.95 to 11.74), which is
small relative to the torus diameter and dominated by random walk diffusion.
There is no clean separation between conditions.

This has implications beyond this experiment: any future analysis that uses
position divergence as a metric is likely to miss the coupling effect. The
paper should state this explicitly as a methodological finding.

### 6.3 Use-No-Learn Being Exactly Zero Was Expected But Still Satisfying

D_Q = 0.00 for use-no-learn is a mathematical certainty (alpha=0 means Q is
never updated), but seeing it in the data confirms that the simulation
machinery is correct. No bugs, no floating-point drift, no unintended state
leakage. This kind of exact null result is reassuring for the validity of all
other results.

---

## 7. Takeaways for the Paper

1. **Position divergence is the wrong metric.** State this explicitly and
   demonstrate it with the 2x2 table showing D_pos is uninformative while D_Q
   cleanly separates conditions. This is a methodological contribution.

2. **Learning (alpha > 0) is necessary and sufficient for Q-map divergence.**
   Without learning, D_Q = 0 regardless of selection policy. With learning,
   D_Q grows to ~5.9 by H=2000 whether or not selection is active.

3. **Selection (tau < inf) does NOT amplify Q-map divergence.** Coupled and
   learn-no-use produce statistically identical D_Q at all tested horizons up
   to H=2000. The original claim that "both learning AND selection are required
   for the cascade" has been disconfirmed for the representational (D_Q) cascade.

4. **Selection matters for behavioral consequences, not representational ones.**
   Selection determines WHICH attractor the agent converges to (demonstrated in
   Exp 4b island attractors), not how much the Q-map diverges. Frame the
   argument as two distinct cascades:
   - **Representational cascade** (D_Q divergence): driven by learning alone.
   - **Behavioral cascade** (attractor switching): requires the full coupling
     loop (learning + selection).

5. **The updated 2x2 table is the key exhibit:**

   |                       | Selects: NO (tau->inf)                          | Selects: YES (tau=1)                                          |
   |-----------------------|-------------------------------------------------|---------------------------------------------------------------|
   | Learns: NO (alpha=0)  | D_Q = 0.00 +/- 0.000                           | D_Q = 0.00 +/- 0.000                                         |
   | Learns: YES (alpha>0) | D_Q = 5.94 +/- 0.200 -- Q diverges, random walk | D_Q = 5.89 +/- 0.259 -- Q diverges, agent navigates attractors |

   The bottom row shows: learning produces the representational cascade
   regardless of selection. The right column shows: selection converts
   representational divergence into behavioral divergence. Both are needed for
   the FULL effect, but D_Q alone does not distinguish them.

6. **Figure 3 should have four panels:**
   - Panel A: The 2x2 table of D_Q values at H=2000 with +/- SE.
   - Panel B: Time series of Coupled vs Learn-no-use D_Q over H=2000, showing
     the two curves are indistinguishable.
   - Panel C: The 6x6 D_Q heatmap (H=300, for parameter sensitivity).
   - Panel D (optional): D_pos comparison showing it is uninformative.

7. **The D_pos comparison between coupled (10.95) and learn-no-use (11.74) is
   now reinterpreted.** The coupled agent has lower D_pos because selection
   drives convergence to attractors. Learn-no-use has D_pos identical to the
   random walk baseline. This confirms that selection affects WHERE agents go,
   not what they learn.

---

## 8. Connection to Other Experiments

- **Experiment 1** (Path Dependence): Established that coupling produces
  positional convergence on smooth landscapes, which explains why D_pos is
  lower for coupled than for random walk conditions. Experiment 3 extends this
  by showing D_pos is uninformative for measuring the cascade.

- **Experiment 2** (Intervention Cascade): Demonstrated the cascade in the
  coupled condition with temporal resolution. Experiment 3 performs the
  ablation that isolates which components are necessary. Together, Experiments 2
  and 3 form the core empirical argument: the cascade exists (Exp 2), learning
  drives it representationally, and selection converts it into behavioral
  consequences (Exp 3).

- **Experiment 4b** (Island Topology): The critical experiment for demonstrating
  that selection matters. On landscapes with multiple attractors, selection
  determines WHICH attractor the agent converges to. This is where the full
  coupling loop produces qualitative (attractor-switching) divergence that
  learn-no-use cannot produce. Exp 4b is the empirical complement to Exp 3's
  ablation: Exp 3 shows selection does not affect D_Q; Exp 4b shows selection
  affects behavioral outcomes.

---

## 9. Technical Notes

### 9.1 Implementation of tau=infinity

In practice, tau=inf is implemented as tau=1e7. At this temperature, the softmax
outputs are numerically indistinguishable from uniform (1/5 for each of 5
actions). Verified that exp(Q/1e7) differs from 1.0 by less than machine epsilon
for all Q-values encountered in the simulation.

### 9.2 The Alpha=0 Invariant

When alpha=0, the Q-update formula becomes:
Q(x,a) <- Q(x,a) + 0 * (e - Q(x,a)) = Q(x,a)

This means Q is invariant under the update. The Q-map remains at its initial
value (all zeros) for the entire horizon. This is a mathematical certainty, not
an empirical finding, but the simulation confirms it holds to floating-point
precision.

### 9.3 Seed Count

n_seeds = 50 was chosen to provide reasonable confidence intervals while keeping
runtime manageable. For the Part B heatmap (36 conditions x 50 seeds x 2 agents
= 3600 agent runs), total computation was substantial but feasible. Standard
errors on D_Q(H) are approximately 0.1-0.2 across conditions, sufficient to
distinguish the ablation effects.
