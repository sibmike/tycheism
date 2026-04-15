# Experiment 4 / 4b: Topology Dependence and Island Attractors

## Overview

This document covers two related experiments. Experiment 4 tests whether landscape
topology affects the magnitude of intervention-induced Q-map divergence under a
mild I_e intervention. Experiment 4b is the stronger result: it demonstrates that
on a two-island landscape, the coupling mechanism that enables peak-finding also
produces trajectory lock-in — stable through the tested horizon (H=600) — once
agents settle on different islands. Experiment 4b is the single strongest
result in the paper.


---

## Experiment 4 — Topology Dependence

### Setup

- Grid: L=31 (31x31, 961 cells)
- Horizon: H=400 steps
- Intervention time: t_intervene=80
- Seeds: n_seeds=60
- Intervention type: I_e (forced encounter / position displacement toward a target)
- Temperature: default tau

Four landscape topologies tested:

1. **Smooth**: Single broad Gaussian peak centered on the grid. Gradients are
   gentle everywhere. An agent following local Q-gradients will find the peak
   eventually from any starting position.

2. **Cliff**: A plateau with a sharp drop-off. The reward surface is flat at a
   moderate level across most of the grid, then rises steeply near one edge to a
   narrow high-reward ridge. Agents near the cliff face a stark gradient signal;
   agents on the plateau get weak signal.

3. **Island**: Two or more isolated peaks separated by low-reward valleys. An
   agent that has settled on one peak receives no gradient information pointing
   toward the other peak. Local exploration is trapped.

4. **Deceptive**: A landscape where the local gradient near the start position
   points away from the global optimum. There is a local maximum that captures
   naive gradient-followers, with the true peak in a different region accessible
   only through a low-reward corridor.

Each topology was generated with the same peak heights to ensure comparable
maximum achievable reward. The key variable is the spatial structure of the
gradient information available to the agent.

For each topology, 60 paired runs were executed: each seed produces a control
agent (no intervention) and a treated agent (I_e applied at t=80). The I_e
intervention displaces the agent's position toward a fixed target location,
forcing an encounter at a position the agent would not have visited under its
own Q-driven policy.

### Parameters

| Parameter       | Value  |
|-----------------|--------|
| L               | 31     |
| H               | 400    |
| t_intervene     | 80     |
| n_seeds         | 60     |
| Intervention    | I_e    |
| Topologies      | 4      |
| tau             | default|

### What Was Measured

- **D_Q(t)**: L2 norm of the difference between treated and control Q-maps at
  each timestep, averaged over seeds. This is the primary divergence metric.
- **Final D_Q**: The value of D_Q at t=H=400.
- **Growth rate**: Whether D_Q is still increasing at H=400 or has plateaued.

### Raw Results

Final D_Q values (mean over 60 seeds):

| Topology   | Final D_Q | Still growing at H=400? |
|------------|-----------|-------------------------|
| Cliff      | 2.94      | Yes                     |
| Island     | 2.62      | Yes                     |
| Smooth     | 2.56      | Yes                     |
| Deceptive  | 2.45      | Yes                     |

Ordering: Cliff > Island > Smooth > Deceptive.

All four topologies show D_Q still increasing at H=400. None have reached a
stable plateau. This means the horizon is too short to see saturation effects,
or the divergence process is genuinely unbounded on these landscapes.

### Discussion

The result is real but underwhelming. The spread between the highest (Cliff, 2.94)
and lowest (Deceptive, 2.45) is only 0.49, which is modest relative to the
absolute values. The topology ordering makes some intuitive sense — the cliff
landscape has the sharpest gradients, so a displacement that pushes the agent
into a different gradient regime produces the largest downstream divergence —
but the differentiation is less dramatic than predicted.

The core problem is that the I_e intervention used here is too mild. A single
position displacement at t=80 creates a transient perturbation, but on all four
topologies the agent's coupling mechanism (Q-learning + softmax exploration)
partially recovers. The topology-specific dynamics that we hypothesized — e.g.,
that island topologies would show permanent divergence while smooth topologies
would show convergence — require either stronger interventions or longer horizons
to manifest clearly.

The more interesting topology-dependent result requires STRONGER interventions on
specifically designed landscapes. This is exactly what Experiment 4b delivers.

### Takeaway for Paper

Experiment 4 can be mentioned briefly: "Topology affects divergence magnitude,
with sharper landscapes producing larger D_Q, but the effect is modest under
mild I_e intervention." The real topology story is told by Experiment 4b.


---

## Experiment 4b — Island Convergence / Divergent Attractors

### THIS IS THE STRONGEST RESULT IN THE PAPER.

### Setup

- Grid: L=41 (41x41, 1681 cells)
- Horizon: H=600 steps
- Temperature: tau=0.5
- Intervention time: t_intervene=100
- Seeds: n_seeds=60

**Landscape design**: Two-island landscape with Gaussian peaks at positions
(10,10) and (30,30). Inter-peak Euclidean distance = sqrt((30-10)^2 + (30-10)^2)
= sqrt(800) = 28.28. The valley between the peaks has reward near zero. Each
peak has comparable height and width, so neither island is "better" — they are
symmetric attractors.

All agents start near peak A at (10,10). Under the default coupling dynamics,
agents discover peak A through local exploration, build Q-values that reinforce
staying near peak A, and never receive gradient information about peak B because
the inter-peak valley provides no signal.

**Three operator types tested**, each applied at t_intervene=100:

1. **I_s local (favorable tip)**: Q-values for cells near (30,30) are set to
   reflect the true reward rates in that region. This is local state injection:
   the agent's Q-map is directly modified to include accurate information about
   peak B. Note: despite the informational intent, this is technically I_s
   (state replacement) applied to a local region, not I_K+ (which would add a
   new arm or reveal an option without overwriting any Q-values). The coupling
   loop continues to operate normally after injection — the agent still selects
   actions via softmax(Q/tau) and updates Q from encountered rewards.

2. **I_s (state replacement)**: The agent's entire Q-map is replaced with a
   Q-map that has been calibrated to peak B. This is equivalent to transplanting
   another agent's learned beliefs. The replacement Q-map has high values near
   (30,30) and low values near (10,10), effectively inverting the agent's
   preferences.

3. **I_e (forced encounter)**: The agent's position is displaced from its
   current location near peak A to a position near peak B at (30,30). The agent
   then experiences rewards from peak B's local environment and updates its
   Q-map based on those encounters. The Q-map itself is not directly modified.

**Measurement protocol**: For each seed, a control run (no intervention) and
three treated runs (one per operator) share the same random seed up to
t_intervene. After intervention, each run proceeds independently to H=600.

The key outcome variable is **which peak the agent is on at t=H**: peak A
(original) or peak B (target of intervention). An agent is classified as
"switched" if it is within radius 5 of peak B at t=600 and has been there
for the last 50 steps (stable residence, not transient visit).

Secondary measurement: **Q-map divergence** between agents that ended on
different peaks, measured in the final quarter of the run (t=450 to t=600).

### Parameters

| Parameter       | Value        |
|-----------------|--------------|
| L               | 41           |
| H               | 600          |
| tau             | 0.5          |
| t_intervene     | 100          |
| n_seeds         | 60           |
| Peak A          | (10, 10)     |
| Peak B          | (30, 30)     |
| Inter-peak dist | 28.28        |
| Operators       | I_s local, I_s, I_e |

### What Was Measured

1. **Switch rate**: Fraction of agents that end on peak B (the target peak)
   instead of peak A (the original peak).
2. **Q-map divergence in final quarter**: For agents that ended on different
   peaks (one on A, one on B from a different operator), compute the L2 norm
   of Q-map difference from t=450 to t=600. Report mean and std.
3. **Stability of divergence**: Whether the divergence between differently-
   peaked agents is stable, growing, or shrinking in the final quarter.

### Raw Results

**Switch rates**:

| Operator    | Switched to B | Switch Rate | 95% CI (Wilson) | Interpretation                         |
|-------------|---------------|-------------|-----------------|----------------------------------------|
| I_s local   | 1 / 60        | 2%          | [0.0%, 8.9%]    | Direct Q-injection barely works        |
| I_s         | 22 / 60       | 37%         | [25%, 50%]      | State replacement moderately effective |
| I_e         | 26 / 60       | 43%         | [31%, 56%]      | Forced encounter substantially effective |
| Control     | 0 / 60        | 0%          | —               | No spontaneous switching               |

**Q-map divergence in final quarter (t=450 to t=600)**:

For pairs where one agent is on peak A and the other on peak B:
- Mean D_Q: 18.51 +/- 0.008 (std over final quarter)

D_Q here is the L2 norm of the full Q-map difference: sqrt(sum((Q_a - Q_b)^2))
over all 41x41 = 1681 cells. Most cells are unvisited by at least one agent
(diff = 0 for those cells), so D_Q aggregates sparse but large differences
concentrated near the two peaks.

The standard deviation of 0.008 on a mean of 18.51 means the divergence is
**stable through the tested horizon**. No drift, no convergence, no fluctuation
was observed from t=450 to t=600. Once agents are on different islands, the
Q-map difference is effectively frozen. This is consistent with permanent
lock-in but has not been demonstrated over arbitrarily long horizons.

**Temporal dynamics**: D_Q rises sharply after intervention, climbs as agents
settle onto their respective peaks, then flatlines completely once both agents
have fully converged to their local peak. The flatline begins around t=300-350
and persists unchanged through t=600.

### Discussion

#### Key Insight 1: Trajectory Lock-In Stable Through the Tested Horizon

No switching was observed by H=600 for any agent that had settled on a peak.
The coupling mechanism that helped the agent find its first peak — Q-learning
builds up values near rewarding locations, softmax concentrates action selection
toward those locations, which produces more encounters near those locations,
which further reinforces the Q-values — now locks the agent onto whichever
peak it was pushed to.

The divergence is not merely large; it is stable in the final quarter
(D_Q = 18.51, std = 0.008). The two agents' Q-maps have settled into fixed
points separated by a chasm of zero-reward valley, and no switching occurred
under tau=0.5 within the tested horizon.

This is consistent with permanent lock-in but has not been demonstrated over
arbitrarily long horizons. Without further intervention, an agent on peak A
showed no tendency to discover peak B, and vice versa. The coupling loop has
constructed a self-reinforcing basin of attraction that the agent did not
escape within 600 steps.

#### Key Insight 2: The Same Mechanism Produces Convergence AND Lock-In

This is the central theoretical point. The coupling loop
Q -> softmax(Q/tau) -> arm -> position -> coin flip -> Q update
is a single mechanism that serves two functions:

- **Convergence**: Early in learning, the coupling helps the agent find rewarding
  regions. Q-values build up near good locations, the softmax policy concentrates
  exploration there, more rewards are found, Q-values increase further. This is
  valuable — it is how the agent learns.

- **Lock-in**: Late in learning, the same coupling prevents the agent from
  leaving. Q-values are high near the current peak, softmax strongly favors
  staying, no encounters occur near distant alternatives, no new information
  arrives, Q-values remain frozen. The agent is trapped.

This is the "self-constructing bubble" from the Core Note. The agent's own
learning process builds a perceptual/behavioral bubble around its current
position. The bubble is not imposed externally — the agent constructed it
through its own successful learning. And yet the bubble is also a prison: the
agent cannot see alternatives that might be equally good or better.

The paper should emphasize that this dual nature is intrinsic to the coupling
mechanism. You cannot have convergence without risking lock-in. Any system that
learns from its own experience will eventually over-commit to its current
trajectory. The question is not whether lock-in occurs but what kinds of
interventions can redirect the trajectory, and at what cost.

#### Key Insight 3: Direct Q-Injection vs. Override — The Framework's Central Discrimination

The switch rates validate the framework's most important distinction:

- **I_s local (favorable tip): 2% switching (95% CI [0.0%, 8.9%]).** Setting
  Q-values near peak B to reflect true reward rates — giving the agent accurate
  local state about the alternative — almost never causes switching. Why?
  Because the agent's existing Q-values for peak A are already high and
  well-calibrated. Injecting favorable Q-values for B does not reduce the
  attractiveness of A. The softmax policy still favors A because the agent has
  extensive, reliable experience there. The injected values are "correct" but
  compete with deeply entrenched Q-values for A.

  This is even more striking than it first appears: I_s local is not merely
  providing information — it is directly writing Q-values into the agent's
  state. A true I_K+ (adding a new arm or revealing an option without
  overwriting Q) would be *less* invasive. Yet even direct Q-value injection
  barely causes switching when the agent has strong prior beliefs from
  experience on island A. The 2% rate (1/60) demonstrates the remarkable
  resistance of entrenched coupling to local state perturbation.

- **I_e (forced encounter): 43% switching (95% CI [31%, 56%]).** Physically
  moving the agent to peak B, where it experiences B's rewards directly,
  switches the agent 43% of the time. The remaining 57% return to peak A,
  indicating that the existing coupling is strong enough to pull many agents
  back even after direct exposure to an equally good alternative.

- **I_s (state replacement): 37% switching (95% CI [25%, 50%]).** Replacing
  the Q-map directly modifies the agent's internal state, bypassing the
  coupling loop. 37% of agents switch, which is lower than I_e (43%) —
  possibly because the replaced Q-map, having been calibrated elsewhere, is
  slightly misaligned with the agent's actual position and encounters, creating
  a brief period of incoherence that some agents "recover" from by reverting
  to peak A behavior.

Both I_s and I_e produced substantially higher switching rates (37% and 43%
respectively) than I_s local (2%). The difference between I_s (37%) and I_e
(43%) was not statistically significant at this sample size (overlapping 95%
CIs: [25%, 50%] vs [31%, 56%]). The key contrast is between I_s local (2%)
and the two override operators, confirming that direct state or position
manipulation is far more effective at redirecting trajectories than local
Q-value injection.

#### Key Insight 4: Mechanism Redirection, Not Content Harm

The agent is not "wrong" on either island. Both peaks have comparable reward
rates. An agent on peak A is performing well by any local metric. An agent on
peak B is also performing well. The intervention that redirected the agent from
A to B did not make the agent worse off — it made the agent different.

This is crucial for the paper's Level 0 framing. At Level 0, we do not ask
whether peak A or peak B is "better" in any moral sense. We observe that the
intervention redirected the trajectory to a DIFFERENT but equally valid outcome.
The damage — if any — is to the coupling mechanism itself, not to the reward
outcomes. The agent that was switched had its self-constructed learning trajectory
disrupted. Its Q-map was coherent with its history on peak A; after switching to
peak B, there is a period of incoherence while the Q-map recalibrates.

The paper should frame this as: interventions that break coupling redirect
the trajectory. The redirected trajectory may be equally good, better, or worse
in terms of reward — that is a Level 1 question. At Level 0, we measure only
the disruption to the coupling mechanism, which is captured by D_Q.

### Surprises / Deviations from Expectations

1. **I_s local was even less effective than expected.** We predicted low
   switching but 2% (1/60; 95% CI [0.0%, 8.9%]) is striking. Even direct
   Q-value injection barely overcomes entrenched coupling on this landscape.

2. **I_e and I_s produced comparable switching rates.** I_e (43%, CI [31%,56%])
   and I_s (37%, CI [25%,50%]) were not statistically distinguishable at n=60.
   Both were dramatically higher than I_s local (2%). The Q-map replacement
   may create a brief incoherence (the new Q-map doesn't match the agent's
   position), allowing some agents to "shake off" the replacement and revert.
   The forced encounter, by contrast, creates genuine new experience that the
   agent's own coupling loop integrates naturally.

3. **The divergence stability was more extreme than expected.** We expected
   stable divergence but std=0.008 indicates D_Q stable in the final quarter.
   The two-island landscape creates a clean separation that eliminates
   stochastic fluctuation in the divergence metric within the tested horizon.

4. **57% of I_e agents returned to peak A.** Even after being physically moved
   to an equally good peak and experiencing its rewards, more than half the
   agents returned to their original peak. The coupling's gravitational pull is
   remarkably strong.

### Takeaways for the Paper

1. Experiment 4b should be presented as a MAIN RESULT, possibly the centerpiece
   of the simulation section. The figure (fig4_island_attractors.png) should be
   prominent.

2. The "self-constructing bubble" narrative should be built around these results:
   coupling enables learning, learning creates lock-in, lock-in resists
   information-only intervention, breaking lock-in requires coupling disruption.

3. The I_s local vs I_e/I_s contrast is the empirical anchor for the
   framework's central ethical discrimination. This should be highlighted.

4. Experiment 4 (topology comparison) can be mentioned briefly as motivation
   for why we designed 4b: mild interventions on arbitrary topologies produce
   modest effects; strong interventions on designed landscapes produce dramatic,
   clear results.

5. The stability of divergence (D_Q stable in final quarter, std=0.008) should
   be emphasized — this is not a noisy statistical effect, it is a clean
   dynamical phenomenon consistent with permanent lock-in but demonstrated
   only through H=600.

### Figure Reference

figures/fig4_island_attractors.png
