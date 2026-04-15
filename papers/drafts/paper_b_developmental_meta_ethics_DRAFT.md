# Tycheism II: Trajectory Sovereignty as Epistemic Necessity

> **Status: Working draft (v6, 2026-04-03). This is not the final version.** Included in the public repository for transparency about the full scope of the trilogy. Paper A in the parent directory is the only finalized paper.

**Mikhail Arbuzov**

*Second paper in a three-part series. Tycheism I demonstrated the dynamics of coupled stochastic learning computationally. Tycheism III maps AI alignment practices onto the intervention operators defined here.*

---

## Abstract

You can have full autonomy — every choice freely made — while the process that builds your capacity to choose is no longer yours. Existing frameworks cannot see this, because they evaluate decisions at the moment of choice, not the developmental mechanism that produces the capacity to decide.

This paper makes that mechanism visible. Moral development is a coupled stochastic learning system: your evaluative state shapes which encounters you face, encounters update your state, the loop repeats. The claim is structural correspondence, not analogy — argued across five formal features with convergent evidence from developmental psychology, cognitive neuroscience, niche construction, and the pathology of coupling disruption. If moral development belongs to the same class of coupled learners Paper A characterized computationally, Paper A's dynamics transfer: a single moral intervention compounds through the loop, expanding someone's options produces far less divergence than replacing their evaluative state, and persistent mild interventions accumulate to match one-shot severe ones.

The paper's central contribution is an epistemic derivation. Genuine stochasticity processed through coupling produces constitutively path-dependent knowledge — evaluative understanding that exists only because a particular trajectory was traversed. No external agent possesses the training data required to govern a trajectory it did not traverse. Trajectory sovereignty follows not as a value preference but as an epistemic necessity: the only coherent response to knowledge conditions that make centralized evaluative authority structurally incoherent.

Four observations would falsify this: moral interventions showing reversion instead of cascade, State Replacement producing less divergence than Option Expansion, externally curated agents developing evaluative capacity equal to self-directed ones, or an external agent reliably identifying high-gradient encounters for a target whose trajectory it has not traversed.

---

## 1. The Discrimination Problem

Your partner is considering adopting a dog. You have met the dog. It is, by any reasonable assessment, perfect for them — temperament, size, energy, everything. Your partner has not yet decided. You have three options:

1. Forward the shelter listing without comment. Your partner sees it or doesn't, acts or doesn't.
2. Take your partner to the shelter. Place the dog in their arms. Blue eyes, warm fur, done.
3. Sit down and make the case. Argue thoroughly until your partner adopts your conclusion as their operating position.

Same intent. Same probable outcome. Same consent — your partner can refuse in all three cases. Existing frameworks can distinguish between these on grounds of intent, consent, or the quality of deliberation at the moment of choice. What they cannot discriminate is what each action does to the *developmental process over time* — what happens not just to this decision but to the trajectory of decisions that follows.

Yet they are not the same. Most people feel this immediately, even if they cannot say why. The first expands what your partner can encounter without shaping the encounter itself. The second bypasses your partner's own selection process — the dog in their arms is not something their own state generated; it is an imposed experience. The third substitutes your evaluative conclusion for theirs before their own process can operate on the evidence.

Resolving this discrimination requires knowing what moral development *is* — not what it aims at or what it produces, but how it works mechanistically. The difference between these three actions is not primarily about respect or autonomy. It is about what the intervener can and cannot know. That is the subject of this paper.

---

## 2. The Formal System

Paper A (Tycheism I) formalized the simplest coupled stochastic learning system: a spatial bandit navigating a grid of hidden coin biases, learning from outcomes, and using what it learned to choose where to go next. Two equations define the system:

$$e_{t+1} \sim K(s_t) \qquad s_{t+1} = U(s_t, e_{t+1})$$

The agent carries a state — its compressed model of the world. That state shapes which encounters it faces. Each encounter updates the state; the updated state shapes the next encounter. In plainer terms: what you know determines where you go, where you go determines what you learn, what you learn determines where you go next.

Paper A established five results:

1. **Cascade amplification.** A single forced encounter produces divergence that compounds at every subsequent timestep, still rising at the end of the simulation. The coupling loop carries any perturbation forward through the agent's own subsequent choices.
2. **Dual cascade.** The divergence decomposes into two components — a representational cascade (the agents' models of the world diverge, driven by learning) and a behavioral cascade (the agents go to different places, driven by selection). Learning alone produces comparable model divergence. But only the full coupling loop converts that into different destinations; without coupling, the agents wander randomly rather than locking onto divergent attractors.
3. **Operator discrimination.** Six intervention types produce divergence in three natural clusters. Option Expansion (adding to what the agent can encounter) produces far less divergence than full State Replacement (overwriting the agent's entire learned model) — the lowest and highest ends of the taxonomy.
4. **Attractor lock-in.** On landscapes with two peaks, a single intervention locks agents onto different attractors — permanently. Both ran the same process on the same landscape. Neither is wrong.
5. **Duration as independent dimension.** Persistent mild operators — Option Removal, Selection Bias — produce divergence comparable to one-shot disruptive ones like Encounter Arrangement.

These are properties of coupled learning systems as a class. Whether they apply to any particular domain depends on whether that domain instantiates the coupled dynamics. The claim of this paper is that moral development does.

---

## 3. The Level 1 Argument: Structural Correspondence

The strategy is structural correspondence, not analogy. If moral development has every feature of a coupled system — persistent state, state-dependent encounter distribution, encounter-driven updates, genuine stochasticity, and the loop that ties them together — then it is an instance, not a metaphor. The evidence is convergent, not deductive, and the convergence is substantial.

### 3.1 State, Encounters, and Updates

Moral agents carry compressed representations of accumulated experience that persist across time, shape perception, and gate responses to new encounters. This is the agent state — and the evidence barely needs stating. The developmental literature converges: Piaget's schemas (1954), Kohlberg's stages (1969), predictive processing models (Clark 2013; Friston 2010), and adaptive specialization under harsh conditions (Ellis & Frankenhuis 2019) all describe agents whose accumulated state shapes how new information is processed. Ellis and Frankenhuis's evidence is particularly sharp: people who developed under unpredictable conditions carry genuinely different cognitive specializations — not deficits, but different states calibrated to different environments, producing different encounter-selection patterns.

Two features of the update matter for coupling dynamics. The update is nonlinear: the same encounter produces different state changes depending on who you already are. And most encounters produce near-zero updates — a motorcycle blogger who logs thousands of successful rides barely adjusts their risk model. The encounters that matter most for moral development are precisely the ones least predictable from the current state.

### 3.2 The Encounter Distribution Is State-Dependent

The recovering addict and the venture capitalist in the same city encounter different things — not because the city changed, but because their states selected different aspects of it. What you encounter depends on who you are. This is the crux of the correspondence argument, because it is what distinguishes the framework from all prior accounts of moral development.

The evidence converges from three directions. Behaviorally, your state selects your neighborhoods, relationships, information sources, and social contexts. Perceptually, selective attention gates what you notice — two people walking the same street read different signs and initiate different interactions because their states filter different stimuli (Desimone & Duncan 1995). Developmentally, niche construction theory (Odling-Smee, Laland & Feldman 2003) describes agents who modify their own selective environments, which then feed back into development. Moral agents do this continuously — choosing communities, careers, media environments, relationships that generate the encounters that train them.

Dewey (1938) recognized that experience shapes the capacity for future experience. Bandura (1986) formalized bidirectional causation as reciprocal determinism. Neither analyzed the *trajectory-level consequences* of perturbation at specific nodes of the loop. What Paper A contributed — and what the moral domain inherits — is the formalization that enables operator discrimination: asking not just "does intervention affect development?" but "which part of the loop does the intervention target, and how much divergence does each part produce?"

### 3.3 The Stochasticity Is Genuine

Moral encounters include genuine luck — the person you happened to sit next to, the crisis that arrived on a Tuesday, the teacher who noticed you. Two sources of irreducible contingency operate: which encounter is drawn and whether a given encounter produces a meaningful update. Neither is under the agent's control.

Peirce called this tychism (1892) — chance is ontologically real, not epistemic uncertainty about a determined outcome. The series takes its name from his doctrine. But the mathematical framework requires only a weaker claim: moral encounters include substantial contingency not reducible to agent intention or effort. Whether that contingency is ontological or a product of deterministic complexity, the coupled dynamics operate identically. Agent-based modeling confirms that identical capability parameters produce radically different outcomes depending on stochastic encounter sequences (Pluchino, Biondo & Rapisarda 2018).

### 3.4 The Coupling Makes It Developmental

Having all four features does not make moral development a coupled system. The coupling does — the loop where your state shapes your encounters and encounters reshape your state. Without this loop, you have experience but not development.

If what you encountered were independent of who you are, your encounters would be exogenous — determined by something other than your own state. This is the structure of indoctrination, thought reform, and totalitarian information control: the agent still carries a state, still updates from encounters, but has no influence over which encounters arrive.

The evidence that coupling disruption damages evaluative capacity comes from three independent sources. Lifton's research on Chinese thought reform (1961) documents that removing the agent's control over their encounter distribution damages not just the content of beliefs but the *capacity for moral judgment itself*. Bettelheim's accounts of concentration camp psychology (1960) describe a related pattern: agents deprived of encounter-selection coupling exhibit deterioration of evaluative capacity that persists long after the external control is removed. The moral injury literature (Litz et al. 2009; Shay 2014) documents a third case — when institutions force encounters that violate the agent's own evaluative state, requiring soldiers to act against their trained moral dispositions, the damage is to the capacity to trust their own state as a guide to future encounters.

All three cases involve factors beyond coupling disruption: trauma, coercion, deprivation, terror. The coupling break cannot be experimentally isolated as sole cause. But the one factor common to all, and absent from comparable adversity without the same evaluative deterioration, is the externalization of encounter selection. The evidence is convergent. Experimental isolation remains a research direction.

Berlin's value pluralism (1958) provides the philosophical framework this coupling result requires. Berlin argued that genuinely incompatible goods exist — not as a failure of moral reasoning but as a feature of the evaluative landscape itself. If the moral landscape is multi-modal (Paper A's two-island result), then convergence to a single attractor is not the mark of correct reasoning; it is the mark of a single-peaked landscape or insufficient exploration. The plurality of outcomes under intact coupling is the formal structure Berlin's pluralism describes: multiple locally valid positions, reached irreducibly through stochastic history processed through coupling.

If the structural correspondence holds — and Sections 3.1 through 3.4 have argued it does, through convergent evidence across five independent features — then moral development belongs to the same class of coupled learners Paper A characterized computationally. Each of Paper A's results generates a prediction: a single moral intervention should cascade, Option Expansion should produce less divergence than State Replacement, interventions should redirect agents to different evaluative attractors, and persistent mild shaping should accumulate to match one-shot disruptions. These predictions are testable against the falsification conditions stated in Section 6.

But establishing that moral development *is* a coupled system does not yet tell us what follows normatively. The structural correspondence is the foundation. The question is what it implies about intervention — and the answer turns out to be epistemic.

---

## 4. From Path-Dependent Knowledge to Epistemic Sovereignty

### 4.1 Coupled Learning Produces Constitutively Path-Dependent Knowledge

Two agents walk the same city for a year. Same streets, same population, same economy. One is a recovering addict; the other is a venture capitalist. At the end of the year, they know different things — not because one paid more attention, but because their states selected different encounters, and those encounters trained different models of how the city works. The addict knows which blocks are dangerous at 2 AM. The VC knows which coffee shops host founders. Both models are locally valid, experience-verified, and useful. Neither can be derived from the other.

This is constitutively path-dependent knowledge: knowledge that exists only because a particular stochastic history was traversed. It is not merely historically contingent — "it happened to go this way." It is constitutive — the knowledge could not have been produced by a different path, because the encounters that generated it were selected by the state that only that path produced.

Peirce's tychism explains why this knowledge scatter is irreducible. If chance is ontologically real — not epistemic uncertainty about a determined outcome — then two agents running identical processes on identical landscapes necessarily produce different knowledge. The scattering is not a coordination failure. It is the output of the mechanism working correctly. Paper A demonstrated this formally: same landscape, same process, same integrity of mechanism, different attractors. Their Q-maps are not noisy approximations of the same truth. They are locally valid models of *different regions* of the landscape.

Kauffman's framework (1993) formalizes the structure. On fitness landscapes with tunable ruggedness — his NK model — adaptive agents reach different local optima depending on their starting point and stochastic path. What you can explore next depends on where you currently are. Kauffman calls this the *adjacent possible* — the set of states reachable in one step from your current configuration. The coupling loop determines which adjacent states are explored, meaning the agent's own learning history shapes which future states are even *reachable*. This is path-dependence of reachability, not just path-dependence of outcomes.

Campbell's evolutionary epistemology (1974) identifies the deeper structure: knowledge grows through blind variation and selective retention. "Blind" does not mean random — it means the variation is not pre-filtered by the selection criterion it will face. The coupling loop produces exactly this: the stochastic encounter is not selected by the learning criterion that will evaluate it. The agent's state selects the neighborhood; chance selects the encounter within that neighborhood; the encounter updates the state. The knowledge that results is a product of this specific blind-variation-and-selective-retention process, run on this specific trajectory.

Much of this knowledge is tacit. Polanyi (1966) argued that we can know more than we can tell — that practical knowledge is often embodied in skilled performance rather than articulable as propositions. The evaluative state a coupled agent develops is substantially of this kind. The motorcycle blogger cannot fully articulate the risk model that 10,000 rides calibrated. The recovering addict cannot fully specify the threat-detection heuristics that years of hard experience trained. The knowledge is in the state, inseparable from the path that produced it.

### 4.2 The Intervener's Epistemic Position

A well-meaning friend wants to help with your moral development. They know you. They care about you. They have their own experience, their own hard-won evaluative state. What do they actually know about what encounters would serve your development?

The answer is: structurally less than they think. Three conceptual frameworks, developed independently in different domains, map onto this problem — each illuminating a different facet of what the intervener cannot know.

**Encounter gradient is agent-relative.** Gibson's ecological psychology (1979) formalizes an analogous relational structure: an affordance — what the environment offers for action — is a relation between agent and environment, not a property of the environment alone. The same ledge affords falling to a toddler and sitting to an adult. The same moral content affords a large state update to one agent (whose current state makes it surprising and challenging) and zero update to another (whose state already incorporates it). The gradient of an encounter — how much it would change you — is not a property of the content. It is a property of the content-state relation. An intervener who filters by content category is filtering by a property of the environment while the developmental cost is determined by a relational property the intervener cannot observe without access to the target's state.

**The knowledge needed to intervene well is structurally inaccessible.** If the structural correspondence of Section 3 holds, and coupling dynamics determine what an intervener can access, the epistemic consequence is sharp. Hayek's core argument in "The Use of Knowledge in Society" (1945) is not that central planners are unintelligent. It is that the knowledge relevant to coordination is dispersed across millions of individuals, embedded in their specific circumstances, often tacit, and continuously generated through local action. By the time a central authority could aggregate it, it is stale. Scott's *Seeing Like a State* (1998) provides the case studies: Soviet collectivization, compulsory villagization in Tanzania, the redesign of Brasília — each case follows the same pattern. A legible, rational central plan destroys the illegible local knowledge — what Scott calls *mētis* — that actually made things work.

The moral analog is structurally identical. Each agent's evaluative state is trained on a path no one else traversed. That state contains compressed information about a region of the moral landscape that only that trajectory visited. The intervener's model is trained on *their* path. It compresses *their* territory. Applied to the target, it is a map of the wrong terrain — not wrong because biased or malicious, but wrong because the intervener traversed a different landscape and their state compresses different encounters.

**A single controller cannot match the variety of divergent trajectories.** Ashby's Law of Requisite Variety (1956) states that a controller must possess at least as much variety as the system it governs. A single alignment model applied to billions of divergent moral trajectories — each trained on different stochastic histories, each carrying path-dependent knowledge of different regions of the moral landscape — cannot have requisite variety. This is not an engineering limitation to be solved with better models. It is an information-theoretic constraint: the variety required scales with the number of divergent trajectories, and the coupling loop continuously generates new divergence.

Popper's critique of utopian social engineering (1945) arrives at the same conclusion through a different route: you cannot predict what knowledge will be produced by a process that has not yet run. If we could predict the growth of knowledge, we would already possess it. Applied here: the intervener cannot predict what evaluative knowledge the agent's coupling would produce, because that knowledge depends on encounters that have not yet occurred and updates that depend on a state only the agent occupies. The response that preserves epistemic integrity is to keep the coupling intact so the agent can revise bad conclusions through their own subsequent encounters, rather than to substitute conclusions that the intervener's own path-dependent limitations have shaped.

### 4.3 Sovereignty as Epistemic Consequence

The derivation:

1. Genuine stochasticity processed through coupling produces constitutively path-dependent knowledge — evaluative understanding that exists only because that particular trajectory was traversed (Section 4.1).

2. This knowledge is structurally inaccessible to any agent who did not traverse the path. The gradient of an encounter is agent-relative. The knowledge needed to improve a trajectory is embedded in that trajectory. The variety of divergent moral agents exceeds any single model's capacity (Section 4.2).

3. An intervention that displaces the coupling — filtering encounters, reshaping the distribution, substituting evaluative state — requires the intervener to possess knowledge about what the target's development needs. But path-dependence makes that knowledge structurally unavailable. The intervener is navigating by a map of different terrain.

4. Therefore, preserving the agent's own coupling is not a value preference. It is the epistemically coherent response to the knowledge conditions that coupling creates. Sovereignty is what remains when you recognize the epistemic asymmetry.

This shifts the normative engine. The question is no longer "does authorship matter intrinsically?" — a contestable value claim. The question is: does the intervener have the epistemic standing to govern a path-dependent process they did not traverse? The answer, given the knowledge conditions Section 4.1 established and the structural inaccessibility Section 4.2 demonstrated, is no. Not because intervention is always wrong, but because the justification must overcome a specific epistemic barrier — and that barrier scales with how much path-dependent knowledge the intervention requires.

There is a category of harm you cannot name from inside the trajectory that incurred it. The evaluative framework you would need to assess whether an intervention improved your development is itself a product of the development the intervention disrupted. Not "you don't know what you don't know" — sharper than that. The thing you would need in order to recognize the loss is the thing that was lost. The epistemic argument explains why this harm is structural: the intervention foreclosed the development of precisely the evaluative capacity that would have detected the loss.

### 4.4 The Operator Table Reframed

Paper A tested six intervention operators and found they produce divergence in three natural clusters. The table below maps these to moral development — but with a second interpretation the epistemic argument makes available. "Divergence" reflects Paper A's measured clusters. "Knowledge required" measures how much structurally inaccessible path-dependent knowledge the intervener must possess to apply the operator competently.

| Divergence | Operator | Moral Analog | Knowledge Required of Intervener |
|-----------|----------|-------------|--------------------------------|
| Low | Option Expansion | Adds to what you can encounter without displacing your selection | None — adds without modeling target state |
| Moderate | Selection Bias | Tilts which encounters are likely without removing options | Moderate — must estimate which encounters matter |
|  | Option Removal | Narrows the encounter landscape; coupling runs on censored space | Moderate — must know which encounters are safe to remove |
|  | Encounter Arrangement | Determines the encounter directly, bypassing your selection | High — must select the right encounter for this agent |
|  | partial State Replacement | Overwrites local evaluative state; coupling continues from imposed starting point | Very high — must model target's local evaluative state |
|  | Learning Impairment | Weakens capacity to learn from encounters | Very high — must know that reduced learning is net-positive* |
| Very High | full State Replacement | Wholesale displacement of the agent's learned evaluative state | Total — must model target's entire evaluative state |

*Learning Impairment produces the lowest divergence in the moderate cluster but retains "very high" knowledge requirement because it permanently damages the mechanism that would correct future errors — a harm the divergence metric does not capture.

Low-sovereignty-cost operators are low-cost *because they require less knowledge of the target's path*. High-cost operators are high-cost *because they presuppose knowledge that path-dependence makes structurally unavailable*. The two orderings — divergence produced and knowledge required — converge because the same structural feature determines both: the deeper you intervene into the coupling, the more path-dependent knowledge you need and the more divergence you create. The ordering is not coincidence. It is the same gradient viewed from two directions.

The puppy test from Section 1 now has not just a taxonomy but an explanation. Forwarding the listing works because it requires no knowledge of your partner's evaluative state. Taking them to the shelter requires knowing this encounter is high-gradient for them — that the dog in their arms will fire a large update. Arguing until they agree requires modeling their entire evaluative framework. The sovereignty cost tracks the epistemic presumption.

Duration is an independent dimension. Paper A established that persistent mild operators produce divergence comparable to one-shot disruptive ones. The epistemic argument sharpens this: a persistent mild intervention — algorithmic curation, institutional norms, ambient social pressure — does not merely accumulate divergence. It accumulates *epistemic debt*: ongoing intervention that continuously requires knowledge the intervener continuously lacks. The moral assessment of an intervention requires both its operator type and its temporal profile.

---

## 5. Trajectory Sovereignty

A recommender system curates your information environment — selecting which news, which opinions, which contacts you encounter. It never overrides a single choice. You click freely on everything presented.

But what you encounter no longer depends primarily on who you are. It depends on an external optimization objective — engagement, retention, predicted preference. You have autonomy. You have severely diminished trajectory sovereignty.

Trajectory sovereignty is the degree to which your developmental trajectory is generated by your own encounter-selection coupling rather than imposed from outside. Autonomy asks: did you choose freely at this moment? Trajectory sovereignty asks: is the process that generates your capacity to choose still intact over time? The distinction matters because you can respect someone's autonomy on every individual decision while systematically eroding their trajectory sovereignty. The epistemic argument of Section 4 grounds this concept: sovereignty is necessary because the evaluative knowledge coupling produces is inaccessible to anyone outside the trajectory.

Not all intact coupling is sovereign coupling. A radicalization pipeline preserves the formal coupling loop — your state shapes encounters, encounters update state — while capturing the encounter distribution upstream through persistent Selection Bias. The loop runs, but on a captured distribution rather than one your state generates freely. Trajectory sovereignty requires not just that the loop is intact, but that what you encounter is predominantly shaped by your own state rather than by an external model with its own objective.

Christman's (1991) historical conditions for autonomy come closest to what trajectory sovereignty formalizes: autonomy depends not just on current endorsement of a value but on whether the agent would not have resisted the process by which it formed. Trajectory sovereignty shares this historical turn but adds the formal apparatus — the operator taxonomy, the quantitative gradient, and the coupling mechanism that explains *how* formation history compounds — and the epistemic foundation that explains *why* formation history cannot be governed from outside.

No human development is purely endogenous. Parenting, education, institutions, social norms, ambient culture — all shape what you encounter. The framework does not demand purity. It identifies a gradient. At one end, the agent's coupling primarily authors their trajectory. At the other, the encounter distribution is externally determined, the state has been overwritten, or the capacity to learn has been attenuated. Where you sit on this gradient matters — moving an agent toward the exogenous end imposes a developmental cost proportional to how far and how persistently the coupling is displaced.

This is developmental meta-ethics. It does not say what agents should value. It says what must remain intact for their evaluative development to be their own. Two agents with intact coupling can reach opposing moral conclusions — the veteran and the pacifist, the person who found meaning through religion and the person who found meaning through leaving it — and that opposition is not a failure of moral development. It is the signature that the encounters were real and the development was honest. The failure occurs when one agent's trajectory is governed by someone whose epistemic position does not include the path-dependent knowledge that trajectory would have produced.

One implication at civilizational scale. If an AI system aligned to the consensus values of 1726 had mediated all human information access, it could have frozen downstream moral development. Not because those values were wrong by some external standard, but because the alignment designers of 1726 couldn't model the developmental needs of trajectories they'd never traversed. The risk is not misalignment. The risk is alignment applied by interveners who structurally lack the knowledge to govern the trajectories they are shaping. Tycheism III develops this in full.

---

## 6. Honest Accounting

### 6.1 Falsification Conditions

Most moral frameworks do not specify the observations that would refute them. This one does.

1. **If moral interventions show reversion rather than cascade.** The framework predicts that a single intervention on a moral trajectory produces divergence that compounds — the agent does not drift back to their pre-intervention baseline. If longitudinal studies showed reliable reversion to baseline after forced moral encounters, cascade amplification would fail for the moral domain and the instantiation argument would collapse.

2. **If State Replacement produces less divergence than Option Expansion.** The framework predicts State Replacement produces dramatically more trajectory divergence than Option Expansion. If indoctrination produced *less* long-term behavioral divergence than information expansion, the operator table would invert and the sovereignty cost gradient with it.

3. **If externally curated agents match self-directed ones.** The framework predicts that externalizing encounter selection impairs evaluative development. If agents in completely externally curated environments developed moral judgment indistinguishable from agents whose own states shaped their encounters, the coupling claim would be falsified and the normative argument would lose its foundation.

4. **If the epistemic argument fails.** If an external agent with no access to the target's trajectory history can identify high-gradient encounters for the target with significantly above-chance accuracy on held-out trajectory data — predicting which encounters would produce the largest state updates before the target's own coupling processes them — the epistemic inaccessibility claim collapses, and sovereignty reduces to a contested preference rather than an epistemic necessity.

None of these observations have been made. The conditions remain open.

### 6.2 What This Paper Does Not Establish

**The correspondence is argued, not proved.** Section 3 establishes structural correspondence through converging evidence. A skeptic could grant every piece and still question whether the correspondence is tight enough to warrant transferring Paper A's results. The appropriate standard is converging evidence sufficient to warrant the transfer, not mathematical proof.

**The epistemic argument does not establish that intervention is never justified.** It establishes that the justification must overcome a specific epistemic barrier — and that barrier scales with how much path-dependent knowledge the intervention requires. Emergency cases (preventing immediate harm) may clear the bar. Persistent ambient shaping almost certainly does not.

**Sovereignty cost thresholds are not derived.** Paper A provides a quantitative ordering of operators. It does not provide threshold values at which intervention becomes impermissible. That question requires additional normative premises the framework identifies as necessary but does not supply.

**The framework is a constraint, not a theory.** It does not say what is good. It says what must remain intact for agents to develop the capacity to figure out what is good. It cannot resolve first-order moral disagreements. It can identify when the mechanism that would resolve them has been damaged.

The Level 2 constraint has implications wherever interventions on moral development are systematic: AI alignment, education, institutional governance, parenting. Each domain requires additional normative premises beyond what this paper establishes. Tycheism III takes up the AI alignment case, including the population-level ensemble argument — whether trajectory sovereignty is not just individually important but structurally necessary for collective moral robustness.

---

## 7. Conclusion

We now know why those three actions from Section 1 are not equivalent — and now we know why the difference is epistemic, not just ethical. Forwarding the listing works because it requires no knowledge of your partner's evaluative state. Taking your partner to the shelter requires knowing this encounter is high-gradient for them. Arguing until they agree requires modeling their entire evaluative framework. The sovereignty cost tracks the epistemic presumption — how much structurally inaccessible knowledge the intervener claims to possess.

The argument runs: moral development is a coupled stochastic learning process. Genuine stochasticity processed through coupling produces constitutively path-dependent knowledge — evaluative understanding that exists only because a particular trajectory was traversed. That knowledge is structurally inaccessible to anyone who did not traverse the path. Therefore, the intervener who displaces the coupling claims epistemic standing they do not have. Sovereignty is not a dignity claim. It is what remains when you recognize the asymmetry.

The framework does not say what agents should conclude. It says what must remain intact while they are concluding. Not because authorship is sacred — but because the alternative requires knowledge that does not exist.

This paper was produced through a coupling that shaped what I encountered, what I noticed, what I concluded. The epistemic argument predicts this: the encounters that would have made this paper better are precisely the ones no external reviewer could have prescribed without having traversed the path that produced it. The framework does not resolve the contradiction. It requires that you notice it.

It protects not convergence of conscience, but the epistemic conditions under which conscience can form at all.

---

## References

Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.

Bandura, A. (1986). *Social Foundations of Thought and Action: A Social Cognitive Theory*. Prentice-Hall.

Berlin, I. (1958). Two concepts of liberty. In *Four Essays on Liberty* (1969). Oxford University Press.

Bettelheim, B. (1960). *The Informed Heart: Autonomy in a Mass Age*. Free Press.

Campbell, D. T. (1974). Evolutionary epistemology. In P. A. Schilpp (Ed.), *The Philosophy of Karl Popper* (pp. 413–463). Open Court.

Christman, J. (1991). Autonomy and personal history. *Canadian Journal of Philosophy*, 21(1), 1–24.

Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*, 36(3), 181–204.

Desimone, R., & Duncan, J. (1995). Neural mechanisms of selective visual attention. *Annual Review of Neuroscience*, 18, 193–222.

Dewey, J. (1938). *Experience and Education*. Kappa Delta Pi.

Ellis, B. J., & Frankenhuis, W. E. (2019). Beyond risk and protective factors: An adaptation-based approach to resilience. *Perspectives on Psychological Science*, 14(4), 561–576.

Friston, K. (2010). The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127–138.

Gibson, J. J. (1979). *The Ecological Approach to Visual Perception*. Houghton Mifflin.

Hayek, F. A. (1945). The use of knowledge in society. *American Economic Review*, 35(4), 519–530.

Kauffman, S. A. (1993). *The Origins of Order: Self-Organization and Selection in Evolution*. Oxford University Press.

Kohlberg, L. (1969). Stage and sequence: The cognitive-developmental approach to socialization. In D. Goslin (Ed.), *Handbook of Socialization Theory and Research* (pp. 347–480). Rand McNally.

Lifton, R. J. (1961). *Thought Reform and the Psychology of Totalism: A Study of "Brainwashing" in China*. Norton.

Litz, B. T., Stein, N., Delaney, E., Lebowitz, L., Nash, W. P., Silva, C., & Maguen, S. (2009). Moral injury and moral repair in war veterans: A preliminary model and intervention strategy. *Clinical Psychology Review*, 29(8), 695–706.

Odling-Smee, F. J., Laland, K. N., & Feldman, M. W. (2003). *Niche Construction: The Neglected Process in Evolution*. Princeton University Press.

Peirce, C. S. (1892). The doctrine of necessity examined. *The Monist*, 2(3), 321–337.

Piaget, J. (1954). *The Construction of Reality in the Child*. Basic Books.

Pluchino, A., Biondo, A. E., & Rapisarda, A. (2018). Talent versus luck: The role of randomness in success and failure. *Advances in Complex Systems*, 21(3-4), 1850014.

Polanyi, M. (1966). *The Tacit Dimension*. University of Chicago Press.

Popper, K. R. (1945). *The Open Society and Its Enemies*. Routledge.

Scott, J. C. (1998). *Seeing Like a State: How Certain Schemes to Improve the Human Condition Have Failed*. Yale University Press.

Shay, J. (2014). Moral injury. *Psychoanalytic Psychology*, 31(2), 182–191.
