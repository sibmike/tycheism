# Paper A Experiment Results — Holistic Synthesis

## What We Set Out To Do

Paper A exists to answer one question: does the formal machinery of coupled stochastic learning systems actually produce the dynamics the framework claims? Specifically: does encounter-selection coupling cause single interventions to cascade into compounding trajectory divergence?

The review identified this as the framework's most urgent weakness: "trajectory divergence is qualitative, not quantitative." Six experiments were designed to convert qualitative claims into demonstrated results using a spatial bandit model with Bernoulli coin-flip encounters.

## The Model

An agent navigates an L×L toroidal grid. Each cell has a hidden coin bias p(x) ∈ [0,1]. At each timestep:

1. **Select arm** via softmax over Q-values of neighboring cells: π(a) ∝ exp(Q(target(a,x)) / τ)
2. **Move** to the target cell
3. **Flip the coin**: encounter e = +1 with probability p(x), -1 otherwise
4. **Update Q**: Q(x) ← (1-α)Q(x) + α·e

The coupling loop: Q → softmax → arm → position → coin flip → Q update.

The coin flip is genuine ontological chance — aligned with Peirce's tycheism. The agent never observes p(x) directly; it only learns through experience.

## Primary Metric: D_Q

D_Q is the L2 norm of the difference between two agents' Q-maps:
D_Q = sqrt(sum((Q_a(x) - Q_b(x))^2)) over all L*L cells. It is NOT a
per-entry average or normalized by number of entries. Most cells are unvisited
by one or both agents (diff = 0 for those cells), so D_Q aggregates sparse
but potentially large differences. Per-entry |diff| max is ~0.57, well within
the [-1, 1] bounds of the Q-value range. D_Q is zero under TvL (no coupling),
compounds under coupling, and differentiates between operators.

## What We Found: The Five Core Results

### Result 1: The Cascade Is Real (Experiment 2)

**Finding:** A single forced coin flip at time t₀ produces Q-map divergence that compounds from 0.44 (10 steps post-intervention) to 2.66 (350 steps post-intervention). Under the TvL baseline (no coupling), Q-map divergence is exactly zero.

**Why it matters:** This is the headline result. The framework's central claim — that a single intervention on a coupled learning system cascades through all downstream encounters — is quantitatively confirmed. The cascade is not a metaphor. It is a measurable, compounding divergence in the agent's learned model of the world.

**The magnitude independence finding:** Whether you force 1 encounter or 20, the final Q-map divergence is approximately the same (~2.5). The coupling loop does all the amplification. The intervention is a seed; the coupling is the amplifier. This is stronger than the original "superlinear" prediction — it shows that intervention magnitude is largely irrelevant to final divergence. One forced coin flip is sufficient.

### Result 2: Two Types of Cascade — Representational and Behavioral (Experiment 3)

**Finding:** The coupling loop decomposes into two independently testable links.
Four conditions tested:

| Condition | Q-map divergence | Behavioral divergence | Why |
|-----------|-----------------|----------------------|-----|
| Coupled (learn + use) | 2.28 | Yes | Full loop: Q learns, Q drives selection |
| TvL (no learn, no use) | 0.00 | No | No loop: nothing connects intervention to future |
| Learn, don't use (Q updates but policy ignores Q) | 2.24 | No | Q diverges but behavior doesn't cascade |
| Use, don't learn (policy uses Q but Q is frozen) | 0.00 | No | No learning means no Q divergence to cascade |

**Why it matters:** This decomposition reveals two distinct cascades:

- **The representational cascade** (Q-map divergence): Learning (alpha > 0) is
  necessary and sufficient. The "learn, don't use" condition produces Q-map
  divergence (2.24) nearly equal to the fully coupled case (2.28), because
  the agent still updates Q from its encounters even though Q doesn't drive
  action selection.

- **The behavioral cascade** (attractor divergence): Selection (tau < infinity)
  is additionally necessary. The "learn, don't use" condition has divergent
  Q-maps but identical behavior — the Q divergence goes nowhere because the
  agent ignores its own Q-values. The behavioral cascade, demonstrated most
  dramatically in Exp 4b's island lock-in, requires the full coupling loop:
  the agent must both learn from encounters AND use what it learned to select
  future encounters.

The full coupling loop combines both effects: representational divergence
feeds back through selection to produce behavioral divergence, which generates
new encounters that further amplify representational divergence.

### Result 3: Different Operators Produce Different Cascades (Experiment 6)

**Finding:** Seven operator variants ranked by final Q-map divergence fall into
three natural clusters:

| Cluster | Operators | D_Q(H) | Notes |
|---------|-----------|--------|-------|
| **Low** | I_K+ (expand options) | 0.518 | Coupling fully preserved, one-shot |
| **Mid** | I_U (attenuate learning) | 1.862 | Broken (e→s link) |
|         | I_s partial (replace local Q) | 2.195 | Broken, one-shot |
|         | I_K- (remove option) | 2.531 | Preserving, persistent |
|         | I_Kw (bias selection) | 2.544 | Preserving, persistent |
|         | I_e (force encounter) | 2.561 | Broken, one-shot |
| **Extreme** | I_s full (replace entire Q) | 8.915 | Complete state substitution |

**Why it matters:** The framework's predicted ranking by coupling status holds
at the extremes: I_K+ (0.518) vs I_s full (8.915) is a 17x difference. But
the mid cluster (range 1.86 to 2.56) reveals that **duration matters as much
as operator type**: persistent I_Kw/I_K- (applied every step) produce
divergence comparable to one-shot I_e. I_U is classified as coupling-breaking
(it modifies the learning rule, breaking coupling at the e→s link). The
sovereignty cost table needs a duration dimension: *type x magnitude x
duration*, not type alone.

### Result 4: Interventions Redirect to Different Attractors — Stable Through the Tested Horizon (Experiment 4b)

**Finding:** On a two-island landscape:
- I_s local (favorable tip — set Q-values near peak B to true reward rates): 2% switch (95% CI [0.0%, 8.9%])
- I_s (replace Q-map to favor the other island): 37% switch (95% CI [25%, 50%])
- I_e (force movement toward the other island): 43% switch (95% CI [31%, 56%])

Once agents land on different islands, Q-map divergence is **stable in the final quarter**: mean = 18.51 +/- 0.008 (std). No switching was observed by H=600. This is consistent with permanent lock-in but has not been demonstrated over arbitrarily long horizons.

**Why it matters:** This is the most visually and conceptually compelling result. The same agent, with the same history up to the intervention point, ends up on a fundamentally different attractor — stable through the tested horizon. The coupling that originally helped the agent find a good peak now *locks it onto whichever peak it was pushed to*. The agent isn't "wrong" on either island — both are valid local maxima. The intervention redirected the entire downstream trajectory.

The I_s local result (2% switching) is even more striking than it first appears: this operator directly writes Q-values into the agent's state (it is technically I_s applied locally, not I_K+ which would add an arm without overwriting Q). Even direct Q-value injection barely causes switching when the agent has strong prior beliefs. Both I_s (37%) and I_e (43%) produced substantially higher switching rates than I_s local (2%); the difference between I_s and I_e was not statistically significant at n=60. Mechanism override redirects trajectories; local state injection does not. This is the framework's central ethical discrimination rendered as a measurable outcome.

### Result 5: Coupling Produces Convergence, Not Divergence (Experiment 1)

**Finding:** Strong coupling (low τ) makes independently seeded agents *converge* to the same attractor, not diverge from each other. At τ=0.1, agents are closer together (11.22) than at τ=50 (11.78).

**Why it matters:** The original proposition — "divergence grows with coupling strength" — was wrong for smooth landscapes. The correct statement: coupling produces *path-dependent convergence to attractors*. On smooth landscapes with a single global optimum, all coupled agents find the same peak. The interesting path dependence appears on multi-modal landscapes (Experiment 4b), where different early encounters lead to convergence on *different* local optima.

This reframing actually strengthens the paper's argument. Coupling is a mechanism for efficient learning — it drives the agent toward good outcomes. The problem arises not because coupling is bad, but because *intervening on a coupled system redirects the convergence target*, and the same mechanism that produces efficient convergence also produces efficient lock-in.

### Supplementary Result: Nonstationary Landscapes (Experiment 5)

**Finding:** Modest effect. At high drift, fast learners (high alpha) adapt better. At zero drift, fast learners also have lower regret (faster convergence to the optimum dominates any noise penalty on this smooth landscape).

**Assessment:** The simulation effect is too weak at these parameters to anchor a major claim. The conceptual argument — that an imposed Q-map is inherently "nonstationary" because it was calibrated to a different agent's local patch — should be argued textually in the paper rather than demonstrated empirically. Include as brief discussion or supplementary material.

## What the Simulation Reveals About the Framework

### The cascade mechanism is not where we expected it

The Core Note claims divergence requires "nonlinear U." The spatial bandit has *linear* U (exponential smoothing). The nonlinearity that drives the cascade comes from two other sources:

1. **The softmax policy** — a nonlinear mapping from Q-values to arm selection probabilities. Small Q differences are amplified into large behavioral differences, especially at low τ.
2. **The Bernoulli coin flip** — discrete {+1, -1} outcomes. Two agents at the same cell can get opposite results purely by chance, triggering different Q updates.

The paper must state this explicitly: the cascade mechanism is softmax + discrete chance + spatial navigation, not nonlinear U. If a reviewer catches this discrepancy before the paper addresses it, the paper looks like it doesn't understand its own model.

### Q-map divergence is the right metric, not position

Position divergence on a torus saturates quickly and is dominated by random walk diffusion. Q-map divergence isolates the coupling effect: it's zero under TvL, compounds under coupling, and differentiates between operators. Every claim in the paper should be grounded in Q-map divergence as the primary metric, with position and outcome divergence as secondary.

### The sovereignty cost ranking needs a duration dimension

The simulation shows three clusters rather than a simple two-group split:
I_K+ (low, 0.518), a mid cluster (I_U, I_s partial, I_K-, I_Kw, I_e; range
1.86–2.56), and I_s full (extreme, 8.915). Persistent application of
coupling-preserving operators (I_Kw, I_K-) produces divergence comparable to
one-shot coupling-breaking operators (I_e). The paper should present the
ranking as: *type x magnitude x duration*, not type alone.

### Coupling is both the benefit and the danger

Coupling produces:
- Efficient learning (convergence to high-p regions)
- Valuable specialization (agents develop expertise in their local patch)
- Dangerous lock-in (inability to leave a local maximum)
- Amplification of intervention effects (small perturbations cascade)

The same mechanism that makes the agent good at navigating its world makes it vulnerable to trajectory redirection. The paper should not present coupling as inherently good and intervention as inherently bad. Instead: coupling is a powerful learning mechanism, and interventions that break coupling damage the mechanism, while interventions that preserve coupling (I_K+) leave it intact.

## What Goes Into the Paper

### Main results (Sections 5-6):
1. **Cascade is real and magnitude-independent** (Exp 2) — the headline
2. **Two types of cascade: representational vs behavioral** (Exp 3) — learning
   is necessary and sufficient for Q-map divergence; selection is additionally
   necessary for behavioral divergence / attractor lock-in
3. **Operators discriminate in three clusters** (Exp 6) — the sharpest
   technical contribution; three-cluster analysis replaces the two-group
   comparison
4. **Attractor lock-in** (Exp 4b) — the most visually compelling demonstration;
   I_s local (not I_K+) vs I_s/I_e contrast

### Discussion points (Section 7):
- Nonlinearity lives in the policy, not in U — explicit correction of Core Note's phrasing
- Q-map divergence as the right metric — why position divergence misleads
- Duration dimension in the operator ranking (three clusters, not two groups)
- Coupling as both benefit and danger

### Supplementary:
- Experiment 1 (attractor convergence) — reframed as motivation for why coupling matters
- Experiment 4 (topology comparison) — brief, less differentiation than expected
- Experiment 5 (nonstationary) — conceptual argument stronger than simulation

### Figures:
1. Landscape gallery (fig1) — shows the experimental terrain
2. Intervention cascade D_Q(t) + magnitude independence (fig2) — headline result
3. Coupling decomposition: 2x2 showing representational vs behavioral cascade (fig3) — reframed to show two cascade types
4. Island attractor switching: trajectories + Q-map diff + switching rates with CIs (fig4) — centerpiece; uses I_s local label (not I_K+)
5. Operator discrimination: D_Q(t) timeseries + three-cluster bar chart (fig5) — replaces two-group overlay
6. Topology comparison D_Q(t) (fig6) — supplementary
7. Nonstationary heatmaps (fig7) — supplementary

## Connection to Paper B

Paper A establishes that coupled stochastic learning systems have these properties as *formal/computational facts*. Paper B will argue that human moral development is an instance of these dynamics (Level 1), and that trajectory sovereignty — the degree to which an agent's trajectory is generated by its own coupling — is a structural precondition for moral agency (Level 2).

The bridge: if Paper B's Level 1 claim holds, then every result in Paper A applies to moral development. The cascade (Exp 2) means a single intervention on someone's moral learning compounds through their entire subsequent trajectory. The coupling decomposition (Exp 3) means the cascade has two components: a representational cascade (requiring learning) and a behavioral cascade (requiring selection) — moral development involves both. The operator discrimination (Exp 6) means that expanding options (I_K+) is fundamentally different from overriding someone's learning process (I_s, I_U) — the first preserves the mechanism, the second disrupts it. The attractor lock-in (Exp 4b) means that once someone is redirected to a different "island" of moral development, the coupling holds them there — stable through the tested horizon, with even direct Q-value injection (I_s local) failing to redirect entrenched trajectories.

Paper A does not make these claims. Paper A establishes the dynamics. Paper B makes the bridge.
