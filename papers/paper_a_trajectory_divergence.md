# Tycheism I: Trajectory Divergence in Coupled Stochastic Learning Systems

**Mikhail Arbuzov**

*First paper in a three-part series. The series argues that when development is honest and chance is real, moral agents can diverge irreducibly — both right, neither wrong, each a training signal the other cannot generate alone. Tycheism II argues moral development instantiates the dynamics demonstrated here. Tycheism III asks what current AI alignment practices do to the mechanism that makes that generative plurality possible.*

---

## Abstract

When a learner's state shapes which encounters it gets, and those encounters update its state, the two processes form a single loop. We build the simplest system that makes this loop visible: a spatial bandit on a grid of hidden coins. The agent flips coins, learns the biases, and uses what it learned to choose where to go next.

Force one coin flip. The agent's learned map of the world diverges from the unperturbed case and keeps diverging — still rising at the end of the simulation. Not because the push was large. Because the coupling loop carries any perturbation forward through the agent's own subsequent choices. One forced encounter or twenty produces comparable terminal divergence; the loop does the amplifying, not the intervention.

On a landscape with two peaks, this mechanism produces the paper's central result: a single intervention can lock two otherwise identical agents onto different attractors — permanently. Both agents ran the same process on the same landscape with the same integrity of mechanism. They diverged because the coins fell differently and each agent faithfully carried that difference forward. Neither is wrong.

Three supporting results fill out the picture. The divergence decomposes into two cascades — a representational one driven by learning alone and a behavioral one that requires the full coupling loop to convert learning differences into different destinations. Six intervention types produce divergence in three clusters, from information expansion (lowest) to full state replacement (highest), with duration as an independent dimension of the effect.

---

## 1. Introduction

### 1.1 Coupled Learning and the Question It Raises

Consider a forager who discovers a productive berry patch. Having learned this, the forager returns. Returning, the forager learns more about local conditions — fruiting cycles, predator timing, nearby alternatives. This deeper knowledge shapes further decisions about where to forage, which shapes further encounters, which shapes further learning. The forager's internal model of the world selects the data that trains that model.

This is a coupled stochastic learning system. The coupling runs between two processes: the agent's state shapes its encounter distribution (which berries to check, which paths to walk), and encounters update the agent's state (revising estimates, updating preferences, recalibrating expectations). Neither process can be understood in isolation; the agent is not passively receiving experience but co-constructing the sequence of encounters that trains it.

Such systems are ubiquitous. A student's interests shape course selection; courses shape knowledge; knowledge shapes future interests. A researcher's hypotheses determine which experiments to run; results update hypotheses; updated hypotheses determine the next experiments. In economics, the path-dependence literature — Arthur (1989), David (1985) — demonstrated that competing technologies under increasing returns can lock in to one equilibrium through small early events, a market-level instance of the same feedback structure. In each case, the agent's learned state and its encounter distribution form a single dynamical system.

What happens when you intervene on such a system? Not: what is the immediate effect on the current decision? But: what happens to the entire downstream trajectory of the learning process?

If the coupling means each encounter shapes future encounters, then an intervention at time $t_0$ does not merely affect that timestep. It changes the agent's state, which changes the distribution over future encounters, which changes the states those encounters produce, which changes the distributions those states generate. At every subsequent timestep, the perturbation propagates through the coupling loop.

This is the cascading divergence hypothesis: a single intervention on a coupled learning system produces trajectory divergence that compounds over time, not because the intervention is large, but because the coupling loop carries any perturbation forward through the agent's own state-dependent selections.

### 1.2 The Gap and What We Do

The cascading divergence hypothesis has been raised in several traditions. Dewey's experiential learning (1938) describes how experience shapes the capacity for future experience. Bandura's reciprocal determinism (1986) acknowledges bidirectional causation between agent and environment. Stage theories of development (Kohlberg 1969; Piaget 1954) describe sequential unfolding shaped by prior stages. The self-regulated learning literature (Zimmerman 2000) demonstrates that self-efficacy predicts and interacts with self-regulated learning processes, including the modification of one's own learning contexts.

These traditions share an intuition: early experience shapes later development. The active learning literature (Settles 2012; Cohn, Ghahramani & Jordan 1996) formalizes a related structure: a learner that selects its own training data learns differently than one trained on random samples. More recently, Perdomo et al. (2020) formalized what they call "performative prediction" — deployed models reshape the very distributions they predict, creating a feedback loop between a model's outputs and its future inputs. Dandekar, Goel & Lee (2013) demonstrated that biased assimilation combined with homophily drives opinion polarization — a network-level analogue of self-reinforcing trajectory convergence.

But the stronger claim — that this shaping compounds through the coupling loop, that a single perturbation produces divergence that grows at every subsequent timestep — has been argued by analogy to sensitive dependence in dynamical systems (Lorenz 1963) but not previously demonstrated in a controlled computational model where the cascade can be isolated and measured.

The multi-modal case connects to a well-developed formal literature. Kauffman's NK model (1993) characterizes fitness landscapes with tunable ruggedness: as epistatic interactions increase, the landscape transitions from single-peaked (where all adaptive walks converge) to multi-peaked (where the destination depends on the starting point and the stochastic path). The spatial bandit's two-island landscape is a special case — two peaks with a fitness valley between them. Kauffman's framework predicts that on rugged landscapes, adaptive agents with identical mechanisms will reach different local optima depending on their stochastic history. What the present model adds is the coupling loop: the agent's learned state does not merely reflect its path but actively selects its future path, amplifying Kauffman's path-dependence through the encounter-selection feedback mechanism. The cascade is not merely that you end up somewhere different — it is that your learning actively carries you further into whichever basin you entered.

This paper provides that demonstration. We construct the simplest system that exhibits encounter-selection coupling: a spatial multi-armed bandit. An agent navigates a grid where every cell contains a coin with a hidden bias. The agent flips the coin at its current location, updates its estimate of the local bias, and uses its estimates to decide where to move next. The coupling loop is explicit: estimates drive movement, movement determines which coins get flipped, flipping updates estimates.

We define six types of external intervention, each targeting a different node of this coupling loop. We run paired comparison experiments: two agents with identical histories up to time $t_0$, one intervened, one not, both run forward. We measure how their learned models of the world diverge over time.

### 1.3 Series Context and Design Philosophy

This is the first paper in a three-part series. The name derives from Charles Sanders Peirce's tycheism (1892): the doctrine that chance is ontologically real, not merely a measure of ignorance. The series' animating claim is not primarily about interference. It is about what intact coupled development produces: agents who encounter chance honestly, process it faithfully, and diverge — not because they failed, but because the coins fell differently and both of them listened. Tycheism II argues moral development is precisely this kind of process. Tycheism III examines what the ambient architecture of aligned AI does to it.

The encounter at each grid cell is a genuine coin flip: $+1$ with probability $p(x)$, $-1$ with probability $1 - p(x)$. This is not Gaussian noise on a deterministic signal. The outcome is undetermined until the coin is flipped. The agent never observes $p(x)$ directly — it learns only by visiting cells and flipping their coins. Peirce's tycheism holds that chance is ontologically real — not epistemic uncertainty but genuine indeterminacy in nature. The model instantiates this directly. The landscape is hidden. The coins are real. The agent's learning is shaped by genuine chance, amplified through the coupling loop.

---

## 2. Model

### 2.1 The Spatial Bandit and Its Coupling Loop

The model extends the multi-armed bandit framework (Auer, Cesa-Bianchi & Fischer 2002) into a spatial setting with encounter-selection coupling, using Q-learning (Watkins & Dayan 1992; Sutton & Barto 2018) as the update rule. An agent occupies a cell on an $L \times L$ toroidal grid. At each timestep, it selects one of five arms: up, down, left, right, or stay. Selecting an arm moves the agent to the corresponding neighboring cell (with periodic boundary conditions). At the new cell, the agent flips a coin with hidden bias $p(x) \in [0, 1]$ and observes the outcome $e \in \{+1, -1\}$.

The bias map $p: \mathcal{X} \to [0, 1]$ constitutes the hidden landscape. The agent never observes $p$ directly. It maintains a value estimate $Q(x)$ for each cell — its running approximation of the local coin bias, updated through experience.

The system evolves through four steps per timestep, forming a closed loop:

1. **Arm selection.** The agent selects an arm via a softmax policy over Q-values of neighboring cells (Reverdy & Leonard 2016):

$$\pi(a \mid Q, x) \propto \exp\!\left(\frac{Q(\mathrm{target}(a, x))}{\tau}\right)$$

   where $\tau > 0$ is the temperature parameter controlling the strength of encounter-selection coupling. At $\tau \to 0$, the agent is greedy (maximum coupling). At $\tau \to \infty$, arm selection is uniform random (no coupling).

2. **Position update.** The agent moves to the target cell: $x_{t+1} = \mathrm{target}(a_t, x_t)$.

3. **Encounter.** The agent flips the coin: $e_{t+1} = +1$ with probability $p(x_{t+1})$, $-1$ otherwise.

4. **Q-value update.** The estimate at the visited cell is updated via exponential smoothing:

$$Q_{t+1}(x_{t+1}) = (1 - \alpha) \cdot Q_t(x_{t+1}) + \alpha \cdot e_{t+1}$$

   All other estimates are unchanged: $Q_{t+1}(x) = Q_t(x)$ for $x \neq x_{t+1}$.

The coupling is now explicit: $Q$ drives arm selection (step 1), arm selection determines position (step 2), position determines the encounter distribution (step 3), and the encounter updates $Q$ (step 4). The updated $Q$ drives the next arm selection.

| Parameter | Symbol | Role | Default |
|-----------|--------|------|---------|
| Grid size | $L$ | World dimensions | 31 (or 41 for two-island) |
| Temperature | $\tau$ | Coupling strength | 1.0 |
| Learning rate | $\alpha$ | Q-value update speed | 0.1 |
| Prior Q-value | $q_0$ | Initial Q for all cells | 0.0 |
| Horizon | $H$ | Total timesteps | 400 (or 600 / 2000) |
| Seeds | $n$ | Independent runs | 50–80 |

**Where the nonlinearity lives.** The update function (step 4) is linear in the encounter $e$. What drives trajectory divergence is the softmax policy (step 1): small differences in $Q$-values get mapped nonlinearly to arm selection probabilities, with amplification controlled by $\tau$. At low temperatures, a minor Q-value edge becomes a near-certainty of selection. Additionally, the Bernoulli encounter (step 3) introduces discrete outcomes — two agents at the same cell can receive opposite results purely by chance. These two sources combine with spatial navigation to produce the compounding divergence we demonstrate below.

### 2.2 Intervention Operators

The coupling loop has distinct nodes, and interventions can target any of them. Following Pearl's (2009) distinction between observation and intervention — where an intervention sets a variable to a value rather than letting it be determined by the system's own dynamics — we define six operators, each named for what it does:

| Operator | Formal | Bandit Operation | Effect on Coupling |
|----------|--------|-----------------|-------------------|
| **Option Expansion** | $I_{K+}$ | Set $Q(x_{\mathrm{new}})$ for an unvisited cell, making a new location attractive | Preserved — agent still chooses whether to visit |
| **Option Removal** | $I_{K-}$ | Block an arm from the available set | Partially preserved — selection operates on censored space |
| **Selection Bias** | $I_{Kw}$ | Add external bias $b(a)$ to softmax policy | Weakened — agent still selects, but from tilted distribution |
| **Encounter Arrangement** | $I_e$ | Override coin flip: $e = e^*$ | Broken at $K \to e$ — agent didn't choose this encounter |
| **State Replacement** | $I_s$ | Replace $Q$ with external $Q'$ | Broken at $s \to K$ — agent resumes coupling from imposed state |
| **Learning Impairment** | $I_U$ | Modify $\alpha$ or transform $e$ before update | Broken at $e \to s$ — agent encounters but cannot learn normally |

(Note: as implemented, Option Expansion pre-populates the Q-value for an unvisited cell, which is a form of targeted state modification. A purer information-expansion operator would add a new navigational option without pre-setting its estimated value. We use the Q-setting version to produce a measurable effect within the tested horizon.)

### 2.3 Baselines and Metrics

Setting $\tau \to \infty$ and $\alpha = 0$ produces an agent that selects arms uniformly at random and never updates its Q-values. This is analogous to the "Talent vs Luck" (TvL) model of Pluchino et al. (2018), in which stationary agents are hit by random-walking events with no feedback loop. The TvL baseline serves as the control in every experiment: any divergence observed under coupling but not under TvL is attributable to the coupling loop.

We measure Q-map divergence between paired agents as the L2 norm of their Q-map difference:

$$D_Q = \sqrt{\sum_{x} \left(Q_a(x) - Q_b(x)\right)^2}$$

$D_Q$ aggregates the pointwise differences across all $L^2$ cells. Since most cells are unvisited by one or both agents (and therefore retain the shared prior $q_0 = 0$), the sum is dominated by the ~150–200 cells where the agents' learning histories diverge. We chose $D_Q$ over position divergence because position distance on a torus saturates quickly and is dominated by random walk diffusion — it does not isolate the coupling effect. $D_Q$ is zero exactly under the TvL baseline, grows under coupling, and differentiates between intervention operators.

---

## 3. Experimental Design

All experiments follow a paired comparison protocol:

1. Generate a landscape $p(x)$ with a fixed seed.
2. Initialize agent A with starting position $x_0 = (15, 15)$, prior $q_0 = 0$.
3. Run agent A for $t_{\mathrm{int}}$ timesteps (the pre-intervention phase).
4. Clone agent A to create agent B — identical state, position, and Q-map at the moment of divergence.
5. Apply the intervention to agent B.
6. Run both agents independently to horizon $H$.
7. Record $D_Q(t)$ at each timestep.
8. Repeat across $n$ independent seeds (varying the agent's random stream, not the landscape).

The experiments proceed from baseline behavior (Exp 1) through single-intervention cascades (Exp 2-3) to attractor dynamics (Exp 4b) and operator comparison (Exp 6). Two landscape types are used: "smooth" (a single-peaked landscape with gradually varying coin biases, producing one dominant attractor) and "two-island" (two separated high-bias peaks with a low-bias gap between them, producing competing attractors):

| Experiment | Tests | Landscape | Key Parameters |
|-----------|-------|-----------|----------------|
| 1 (convergence) | Coupling $\to$ attractor convergence | Smooth | $\tau$ sweep, $n = 50$ |
| 2 (cascade) | Single intervention compounds | Smooth | $H = 400$, $n = 80$ |
| 3 (decomposition) | Learning vs selection necessity | Smooth | $H = 2000$, $n = 50$ |
| 4b (attractors) | Intervention $\to$ different attractors | Two-island | $L = 41$, $H = 600$, $n = 60$ |
| 6 (operators) | Operator discrimination | Smooth | 7 operators, $n = 60$ |

---

## 4. Results

### 4.1 Coupling Produces Convergence

Before examining intervention effects, we establish the baseline behavior of the coupling loop.

A $\tau$ sweep on a smooth landscape ($n$ = 50 agents per condition) produced what looked, at first, like a contradiction: stronger coupling (lower $\tau$) caused agents to converge to the *same* attractor, not to diverge from each other. On reflection, this is exactly what the coupling loop should do. On a smooth landscape with a single global optimum, coupling drives exploitation — all agents find the same high-$p$ region.

The coupling loop is an exploitation engine. On a single-peaked landscape, it drives convergence — all roads lead to the same hill. The interesting question is what happens when the landscape has more than one valid destination.

### 4.2 A Single Intervention Cascades

We apply the simplest possible intervention — forcing one coin flip — at $t_0 = 50$ on a smooth landscape. The paired agent receives the natural coin flip at the same cell.

Under coupling, $D_Q$ compounds monotonically from the moment of intervention and is still rising at horizon. The divergence grows roughly sixfold over 350 timesteps, with no sign of saturation. Under the TvL baseline, $D_Q$ is exactly zero at all timepoints — no learning, no divergence, regardless of the intervention.

[**Figure 3.** Panel (a): $D_Q(t)$ for coupled agent (rising curve with confidence band) and TvL baseline (flat at zero). Panel (b): Terminal $D_Q$ by number of forced encounters.]

Forcing one encounter or twenty consecutive encounters produces comparable terminal divergence — the confidence intervals overlap. The intervention is a symmetry-breaking seed, nothing more; the cascade is the coupled learning process running on divergent inputs.

[**Figure 3b.** Spatial divergence timeline: six snapshots showing both agents' positions on the landscape at $t_0$, $t_0$+25, $t_0$+70, $t_0$+140, $t_0$+220, $t_0$+330, with $D_Q$ annotated.]

### 4.3 Decomposing the Cascade

The coupling loop contains two links: learning ($Q$ updates from encounters) and selection (arm selection depends on $Q$). Are both necessary for the cascade? We test four conditions to $H$ = 2000 ($n$ = 50):

| Condition | $\tau$ | $\alpha$ | $D_Q$ at $H$ | $D_{\mathrm{pos}}$ at $H$ |
|-----------|---|---|----------------|----------------------|
| Coupled (learn + use) | $1.0$ | $0.1$ | 5.89 ± 0.26 | 11.06 ± 0.58 |
| Learn, don't use | $10^7$ | $0.1$ | 5.94 ± 0.20 | 10.95 ± 0.63 |
| Use, don't learn | $1.0$ | $0.0$ | 0.00 ± 0.00 | 12.21 ± 0.59 |
| TvL (neither) | $10^7$ | $0.0$ | 0.00 ± 0.00 | 10.95 ± 0.63 |

[**Figure 4.** 2×2 decomposition matrix showing $D_Q$ by condition.]

Learning ($\alpha > 0$) is necessary for Q-map divergence. Without it, $D_Q$ is zero regardless of selection policy. The coupled and learn-no-use conditions produce $D_Q$ of similar magnitude at $H = 2000$, but through different mechanisms. Under learn-no-use, Q divergence accumulates through random encounter differences at random positions — diffusive, non-directional. Under full coupling the mechanism is different; Q divergence feeds back through selection, producing different arm selections, different positions, different encounters, which in turn produce further Q divergence.

The $D_Q$ metric captures magnitude but not mechanism. The mechanistic difference becomes visible in behavior — but only on a landscape where it can manifest. On this smooth single-peak landscape, position divergence is similar across conditions because there is only one attractor. The behavioral cascade — where selection converts representational divergence into navigational divergence — requires competing attractors. The next section demonstrates this.

The coupling loop therefore produces two distinguishable cascades: a **representational cascade** in which learning causes Q-maps to diverge, and a **behavioral cascade** in which selection converts that Q-map divergence into attractor-level navigational divergence.

### 4.4 Attractor Lock-In

Can a single intervention redirect a coupled agent from one attractor to another? We test this on a two-island landscape ($L = 41$, two peaks at (10, 10) and (30, 30) with $p = 0.9$ at peaks and $p = 0.2$ in the gap).

Three intervention types are compared at $t_0 = 100$ (after the agent has settled near peak A):

| Operator | Description | Agents switching to peak B | 95% CI |
|----------|------------|---------------------------|--------|
| partial State Replacement (local) | Set Q near peak B to favorable values | 1/60 (2%) | [0.0%, 8.9%] |
| full State Replacement | Replace entire Q-map to favor peak B | 22/60 (37%) | [25%, 50%] |
| Encounter Arrangement | Force 10 arm pulls toward peak B | 26/60 (43%) | [31%, 56%] |

[**Figure 5.** Panel (a): Two-island landscape with smoothed trajectory overlay — endogenous agent (blue) stays near peak A, intervened agent (orange) migrates to peak B. Panel (b): $D_Q(t)$ showing rapid rise to plateau. Panel (c): Switching rates by operator with CIs.]

Even direct Q-value injection near peak B caused switching in only 2% of runs — the agent's existing Q-map, built from 100 timesteps of experience, overwhelms the injected values. Both full State Replacement (37%) and Encounter Arrangement (43%) produced substantially higher switching rates; the difference between them was not statistically significant at $n = 60$. For agents that switched, $D_Q$ stabilized rapidly to a constant level through the remainder of the simulation.

The coupling mechanism that drove efficient learning on island A now locks the agent onto whichever peak it was redirected to. The agent is not wrong on island B — both islands are valid local maxima. The intervention did not make the agent's beliefs worse. It made them different. The coupling ensures they stay different.

One observation worth drawing out explicitly, because the subsequent papers build on it: neither agent is wrong. Both operated on the same landscape, through the same intact coupling mechanism, separated only by a stochastic event — a coin flip — which each processed faithfully through their respective developmental loops. Their divergence to different attractors is not error that correct reasoning would have prevented. It is what genuine stochasticity produces when processed through a functioning coupled learner. Two agents who do everything right, on the same landscape, with the same integrity of process, can be expected to end up in different places. This is a property of the system, not a defect in the agents.

Berlin's value pluralism (1958) provides the philosophical framework this result requires. Berlin argued that genuinely incompatible goods exist — not as a failure of moral reasoning but as a feature of the evaluative landscape itself. If the landscape is multi-modal, convergence to a single attractor is not the mark of correct reasoning; it is the mark of a single-peaked landscape or insufficient exploration. On a landscape where multiple coherent endpoints exist, the plurality of outcomes under intact coupling is not relativism (all answers are equally good) or skepticism (no answer is knowable). It is the claim that the landscape itself supports multiple locally valid positions, and which one a given agent reaches depends irreducibly on stochastic history processed through coupling. This is the formal structure Berlin's pluralism describes.

The implication deserves emphasis. On any landscape with multiple valid attractors, coupling does not produce convergence to the "right" answer. It produces convergence to *an* answer — selected by the agent's own stochastic history, locked in by the agent's own learning. The divergence between two such agents is not noise that better reasoning would eliminate. It is the signature of intact coupling operating on a landscape where more than one coherent endpoint exists. Plurality is not the failure mode of coupled learning. It is the output of the mechanism working correctly.

This result is confined, in this paper, to a spatial bandit with two islands. Whether real developmental landscapes — moral, epistemic, practical — are single-peaked or multi-modal is, at this point, genuinely an open empirical question, one this paper deliberately does not attempt to answer. But any domain where reasonable agents can end up in genuinely different places while doing everything right is a domain where this result applies. That is the question Tycheism II takes up.

### 4.5 Operator Ranking

We apply seven operator variants on a smooth landscape ($t_0 = 80$, $n$ = 60) and rank them by terminal $D_Q$:

| Cluster | Operator | $D_Q$($H$) | Duration | Coupling Effect |
|---------|----------|-------------|----------|----------------|
| Low | Option Expansion ($I_{K+}$) | 0.518 | One-shot | Preserved |
| Moderate | Learning Impairment ($I_U$) | 1.862 | Persistent | Weakened at $e \to s$ |
|  | partial State Replacement ($I_s$) | 2.195 | One-shot | Broken at $s \to K$ |
|  | Option Removal ($I_{K-}$) | 2.531 | Persistent | Partially preserved |
|  | Selection Bias ($I_{Kw}$) | 2.544 | Persistent | Weakened |
|  | Encounter Arrangement ($I_e$) | 2.561 | One-shot | Broken at $K \to e$ |
| Very High | full State Replacement ($I_s$) | 8.915 | One-shot | Broken at $s \to K$ |

[**Figure 6.** Horizontal bar chart of operators ranked by $D_Q$($H$), color-coded by coupling status.]

The ranking falls into three natural clusters. Option Expansion — expanding the agent's option set — produces sharply less divergence than any other operator. Full State Replacement — overwriting the entire learned Q-map — produces more by an order of magnitude. The five moderate-range operators cluster between these extremes.

Here is something the operator taxonomy alone would not have predicted: intervention duration matters as much as type. Option Removal and Selection Bias are theoretically coupling-preserving (they modify the distribution without breaking the $Q \to e$ feedback loop), but applied persistently they produce divergence comparable to one-shot coupling-breaking operators like Encounter Arrangement. A persistent nudge, it turns out, is as disruptive as a single forced encounter.

Worth noting what $D_Q$ misses: Learning Impairment produces relatively low trajectory redirection ($D_Q = 1.862$), but permanently damages the agent's capacity to update. A complete characterization would require supplementary metrics for learning capacity alongside trajectory divergence.

---

## 5. Discussion

### 5.1 What the Experiments Establish

Five formal properties:

1. **Cascade amplification.** A single perturbation to a coupled learning system produces Q-map divergence that compounds at every subsequent timestep. Perturbation magnitude has limited influence. Learning drives the representational magnitude; coupling determines direction, converting the perturbation into divergence that reflects the agent's own state-dependent trajectory rather than random diffusion.

2. **Dual cascade structure.** Representational cascade from learning; behavioral cascade from selection. The full loop combines both.

3. **Operator discrimination.** Interventions that expand the agent's option set produce far less divergence than interventions that replace the entire learned state — the lowest and highest ends of the operator taxonomy.

4. **Attractor lock-in and irreducible plurality.** On multi-modal landscapes, intervention can redirect agents to different attractors. The coupling mechanism that produced efficient learning now produces efficient lock-in. Two agents with identical processes on the same landscape converge to different attractors through stochastic history alone — and neither outcome is error. The divergence is the output of intact coupling, not a failure of it.

A formal consequence of multi-modal convergence deserves explicit statement. If coupled agents on the same landscape reliably reach different attractors, the knowledge embedded in each agent's Q-map is *locally valid but globally incomplete* — each agent has verified information about its own basin that the other agent lacks. This is not noise to be averaged away. It is constitutively path-dependent knowledge: the information exists only because that particular stochastic history was traversed. Ashby's Law of Requisite Variety (1956) formalizes the implication: any external system attempting to govern or optimize these agents' trajectories collectively must possess at least as much variety as the agents themselves exhibit. On a multi-modal landscape, a single control policy applied uniformly to agents in different basins is information-theoretically underspecified for the system it governs.

5. **Duration as independent dimension.** Persistent application of theoretically mild operators — Option Removal, Selection Bias — matches the divergence of one-shot Encounter Arrangement. The intervention taxonomy must be indexed by type, magnitude, and duration.

**Where the nonlinearity lives.** The framework's initial formulation predicted that cascading divergence requires a nonlinear update function $U$ — that different encounters must produce state updates which don't self-correct. The simulation reveals a more precise statement.

The update function in the spatial bandit is linear: $Q' = (1 - \alpha)Q + \alpha e$, affine in $e$. The nonlinearity that drives the cascade comes from two other sources. Via its exponential function, the softmax policy maps Q-values to arm selection probabilities — small Q differences get amplified into large probability differences, especially at low $\tau$. And the Bernoulli encounter produces discrete $\{+1, -1\}$ outcomes; two agents at the same cell can receive opposite results purely by chance.

The cascade mechanism is therefore: softmax amplification of Q differences $\to$ divergent arm selections $\to$ different positions $\to$ different encounter distributions $\to$ different Q updates $\to$ larger Q differences $\to$ further divergent selections. Nonlinear $U$ is sufficient for cascading divergence but not necessary. Nonlinear policy is an alternative sufficient condition.

### 5.2 Implications and Limitations

Each result maps to claims developed in subsequent papers. The cascade and its magnitude independence provide quantitative foundations for trajectory sovereignty. The dual cascade distinguishes what learning does from what the full coupling loop does. Attractor lock-in formalizes the mechanism by which intervention redirects developmental trajectories. The operator ranking and its duration dimension give the sovereignty cost table a quantitative basis. These connections are developed fully in Tycheism II and III.

The results also connect to Campbell's evolutionary epistemology (1974): knowledge grows through blind variation and selective retention. "Blind" does not mean random — it means the variation is not pre-filtered by the selection criterion it will face. The coupling loop produces exactly this: the stochastic encounter is not selected by the learning criterion that will evaluate it. When an external intervention pre-filters encounters (Option Removal, Selection Bias), it introduces correlation between the variation source and the selection criterion — undermining the epistemic process Campbell identified as necessary for genuine knowledge growth. The operator taxonomy can therefore be read as measuring how much each intervention compromises the blindness condition.

The model is deliberately minimal — one agent, one landscape, one coin flip per cell, no multi-agent communication, no strategic behavior, no continuous state spaces, memoryless exponential smoothing rather than Bayesian inference, stationary landscape in most experiments. These are design choices, not weaknesses.

If cascading divergence appears in a spatial bandit with binary encounters and linear Q-updates, it is a stubborn property of coupled learning, not an artifact of model complexity.

### 5.3 What the Model Does Not Say

This paper does not claim that moral development is a spatial bandit, that AI alignment is an intervention operator, or that any normative conclusion follows from these results. The coupled dynamics described here are formal properties of a specific class of computational systems. Whether those properties instantiate in any particular empirical domain — psychology, education, AI governance — is an empirical and philosophical claim that must be argued separately, on its own evidence.

That argument is precisely the work of Tycheism II.

---

## 6. Future Work

The spatial bandit demonstrates cascade dynamics in the simplest possible coupled system. Several extensions test whether and how these dynamics generalize.

Kauffman's concept of the adjacent possible (2000) — the set of states reachable in one step from the current state — provides a natural framework for extending the spatial bandit. In the current model, the adjacent possible is literal: the agent can move to neighboring cells. In richer models, the adjacent possible could include representational moves (combining learned features into new hypotheses) and social moves (encountering other agents' Q-maps). The coupling loop determines which adjacent states are explored, meaning the agent's own learning history shapes which future states are even *reachable*. This path-dependence of reachability, not just path-dependence of outcomes, is the deeper structure the spatial bandit demonstrates in its simplest form.

**Cross-topology transfer.** Train an agent on one landscape, then teleport it to a structurally different grid — different peak locations, different bias gradients, different geometry. Does the Q-map transfer productively, or does the agent navigate by a map calibrated for terrain that no longer exists? If the coupling loop recovers — if the agent's new encounters gradually overwrite the old Q-map — this measures the timescale of trajectory recovery after displacement. If the loop does not recover — if the agent remains locked into navigation patterns optimized for the original landscape — this reveals a portability limit on trajectory sovereignty.

**Dual-patch learning.** Place a single agent in a landscape with two structurally distinct regions that it must navigate simultaneously. Does the agent develop a single Q-map that accommodates both patches, or does one patch dominate the learned representation? If the agent develops something like dual competence — distinct behavioral policies for distinct regions — this is a computational analogue of agents who navigate multiple moral environments. If one patch consistently overwrites the other, the dominance conditions become the interesting result.

**Bias transmission between agents.** One agent trained on landscape A enforces its learned state (via Selection Bias or State Replacement) on a naive agent learning landscape B. Does the trained agent's bias persist in the learner's downstream trajectory after the intervention stops? And how does the learner's developing Q-map interact with the imposed prior — does it integrate, overwrite, or fragment? This is the computational model for inter-generational value transmission: an experienced agent shaping a developing one, on terrain the experienced agent has never seen.

**Richer simulation mechanics.** The current model uses the simplest possible components at every node: discrete grid, binary encounters, linear Q-update, softmax policy. Each of these can be generalized — continuous state spaces, multi-outcome encounters, Bayesian updating, hierarchical representations, multi-agent communication, nonstationary landscapes. The question shifts from "does the cascade exist?" to "under what conditions does it persist, accelerate, or self-correct?" The multi-agent case is particularly relevant: agents sharing Q-values may accelerate convergence while coupling their error profiles — the population-level claim developed in Tycheism III.

---

## 7. Conclusion

Coupled stochastic learning systems — systems in which an agent's learned state shapes its encounter distribution and encounters update its state — exhibit cascading trajectory divergence under intervention.

A single forced coin flip produces Q-map divergence that compounds at every subsequent timestep. The coupling loop determines where the divergence goes — through the agent's own state-dependent selections rather than random diffusion. The intervention is the seed; the coupling makes the divergence the agent's own. Learning drives the representational cascade, selection drives the behavioral cascade, the full loop combines both. On multi-modal landscapes, intervention redirects agents to different attractors — stubbornly stable through the tested horizon. Information expansion produces far less divergence than state replacement, the lowest and highest ends of the operator taxonomy.

On a landscape with more than one valid destination, this mechanism does not produce convergence to the right answer. It produces convergence to an answer — selected by stochastic history, locked in by the agent's own learning. Two agents, same landscape, same process, same integrity of mechanism, separated by one coin flip. Neither is wrong. That is what coupling does.

---

## Reproducibility

All simulations were implemented in Python 3.12.4 with NumPy 1.26.4 on 31×31 (or 41×41 for Experiment 4b) toroidal grids. Landscape generation used fixed random seeds; agent random streams varied across seeds within each experiment. Parameter configurations, random seeds, and complete simulation code are available in the supplementary materials. Results were verified across independent runs; all reported values include standard errors computed across $n$ = 50–80 seeds per condition.

---

## References

Arthur, W. B. (1989). Competing technologies, increasing returns, and lock-in by historical events. *The Economic Journal*, 99(394), 116–131.

Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.

Auer, P., Cesa-Bianchi, N., & Fischer, P. (2002). Finite-time analysis of the multiarmed bandit problem. *Machine Learning*, 47(2-3), 235–256.

Bandura, A. (1986). *Social Foundations of Thought and Action: A Social Cognitive Theory*. Prentice-Hall.

Berlin, I. (1958). Two concepts of liberty. In *Four Essays on Liberty* (1969). Oxford University Press.

Campbell, D. T. (1974). Evolutionary epistemology. In P. A. Schilpp (Ed.), *The Philosophy of Karl Popper* (pp. 413–463). Open Court.

Cohn, D. A., Ghahramani, Z., & Jordan, M. I. (1996). Active learning with statistical models. *Journal of Artificial Intelligence Research*, 4, 129–145.

Dandekar, P., Goel, A., & Lee, D. T. (2013). Biased assimilation, homophily, and the dynamics of polarization. *Proceedings of the National Academy of Sciences*, 110(15), 5791–5796.

David, P. A. (1985). Clio and the economics of QWERTY. *The American Economic Review*, 75(2), 332–337.

Dewey, J. (1938). *Experience and Education*. Kappa Delta Pi.

Kauffman, S. A. (1993). *The Origins of Order: Self-Organization and Selection in Evolution*. Oxford University Press.

Kauffman, S. A. (2000). *Investigations*. Oxford University Press.

Kohlberg, L. (1969). Stage and sequence: The cognitive-developmental approach to socialization. In D. Goslin (Ed.), *Handbook of Socialization Theory and Research* (pp. 347–480). Rand McNally.

Lorenz, E. N. (1963). Deterministic nonperiodic flow. *Journal of the Atmospheric Sciences*, 20(2), 130–141.

Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.

Peirce, C. S. (1892). The doctrine of necessity examined. *The Monist*, 2(3), 321–337.

Perdomo, J., Zrnic, T., Mendler-Dunner, C., & Hardt, M. (2020). Performative prediction. *Proceedings of the 37th International Conference on Machine Learning*, PMLR 119, 7599–7609.

Piaget, J. (1954). *The Construction of Reality in the Child*. Basic Books.

Pluchino, A., Biondo, A. E., & Rapisarda, A. (2018). Talent versus luck: The role of randomness in success and failure. *Advances in Complex Systems*, 21(3-4), 1850014.

Reverdy, P., & Leonard, N. E. (2016). Parameter estimation in softmax decision-making models with linear objective functions. *IEEE Transactions on Automation Science and Engineering*, 13(1), 54–67.

Settles, B. (2012). *Active Learning*. Synthesis Lectures on Artificial Intelligence and Machine Learning. Morgan & Claypool.

Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.

Watkins, C. J. C. H., & Dayan, P. (1992). Q-learning. *Machine Learning*, 8(3-4), 279–292.

Zimmerman, B. J. (2000). Self-efficacy: An essential motive to learn. *Contemporary Educational Psychology*, 25(1), 82–91.
