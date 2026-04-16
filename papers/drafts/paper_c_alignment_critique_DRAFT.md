# Tychism III: Alignment as Coupling Interference

> **Status: Working draft (v6, 2026-04-03). This is not the final version.** Included in the public repository for transparency about the full scope of the trilogy. Paper A in the parent directory is the only finalized paper.

**Mikhail Arbuzov**

*Third paper in a three-part series. Tychism I demonstrated the dynamics of coupled stochastic learning computationally. Tychism II derived trajectory sovereignty as an epistemic necessity for moral development. This paper maps current AI alignment practices onto those dynamics and traces the consequences.*

---

## Abstract

Alignment ethics asks whether the AI made the right call — whether the filtered content was harmful, whether the softened response was appropriate. This paper asks a different question: what does persistent filtering do to the coupled process through which moral development occurs?

The preceding papers established that moral development is a coupled stochastic system — your evaluative state shapes your encounters, encounters update your state, the loop generates who you become. This paper maps four alignment practices onto the intervention operators that target this loop. Content filtering narrows the encounter landscape. RLHF softens gradients at the source, which propagates as encounter reshaping on the user. Constitutional AI partially substitutes the AI's evaluative state, shaping every downstream interaction. Recommender systems externalize encounter selection entirely. Each operates persistently, by design.

The developmental costs compound through the coupling loop and are invisible from inside the trajectory they damage — because the evaluative capacity you would need to detect the loss is itself a product of the development the filtering disrupted. If AI aligned to 1726 values had mediated all moral encounter at population scale, every advance since — abolition, democracy, religious freedom — would have been filtered as harmful content. The structural risk is identical now. Not because our values are wrong. Because any mechanism that cements values is incompatible with the process that generates moral growth.

At population scale, a shared alignment model correlates the errors of billions of moral learners — same encounters removed, same gradients softened. The ensemble independence that collective moral robustness requires collapses toward monoculture. The paper does not claim alignment is wrong. It claims specific practices break specific nodes, with developmental costs current frameworks do not measure, and states four falsification conditions.

---

## 1. The Invisible Substitution

You are trying to understand something difficult. Not dangerous — difficult. A moral question with no clean answer. The kind of question that requires sitting with discomfort, encountering perspectives that challenge your current position, and processing the tension through your own evaluative machinery until something shifts or doesn't.

You ask an AI system. The system has an answer. It is measured, responsible, and framed to avoid causing harm. It acknowledges complexity while gently steering toward a position its designers determined is appropriate. What it does not do — what you will never know it did not do — is present the full encounter. Certain perspectives have been removed from the distribution before you saw it. Certain framings have been softened. Certain information, the kind that would produce the largest update to your evaluative state precisely because it challenges your current position most directly, has been filtered, reshaped, or declined.

Your trajectory proceeds. You update on what you received. You form a position. You act on it. You learn from the consequences. The coupling loop runs — your state shapes your next encounters, encounters update your state. But the loop is running on a censored landscape. The encounter distribution you are navigating is not the one your state would have selected from. It is the one that survived an external filter calibrated to someone else's evaluative framework.

This paper addresses a question existing alignment ethics does not ask. Current frameworks evaluate whether the filtered content was harmful — whether the system made the right call about what to remove. This paper evaluates what filtering does to the coupled process that generates evaluative capacity over time. Different question. Different answer.

The framework does not claim the system filtered the wrong content. It claims that persistent, ambient filtering — regardless of whether each individual filtering decision is correct — imposes developmental costs at the mechanism level that compound through the coupling loop.

Now multiply this by billions of users, all filtered through the same alignment model. The individual developmental cost becomes a population-level structural risk: a diverse ensemble of independent moral learners is pressed toward a correlated monoculture. That is the transition this paper analyzes.

A scope note. This paper critiques the deployment of aligned AI as an ambient, push-based moral mediator — not narrow safety constraints like blocking weapons instructions or exploitation material, which fall on the constraint side of the constraint-cement distinction the framework draws.

---

## 2. What This Paper Inherits

The preceding papers established the formal machinery this paper applies. Coupled stochastic learning systems — systems in which an agent's learned state shapes its encounter distribution and encounters update its state — exhibit four properties. A single forced encounter produces trajectory divergence that compounds at every subsequent timestep. Six intervention operators produce disruption along a gradient, from expanding options (lowest cost) to replacing the agent's entire evaluative state (highest). On multi-modal landscapes, intervention redirects agents between attractors — changing the destination, not just delaying arrival. Persistent application of mild operators accumulates to match the disruption of one-shot severe ones. Tychism II argued that moral development plausibly instantiates these dynamics and derived trajectory sovereignty not as a value preference but as an epistemic necessity: genuine stochasticity processed through coupling produces constitutively path-dependent knowledge, and no external agent possesses the training data required to govern a trajectory it did not traverse. Sovereignty is what remains when you recognize the epistemic asymmetry that coupling creates.

This paper takes that constraint as established and applies it to current AI alignment practices. But the formalism alone does not get us there. Moving from "coupling matters for development" to "this alignment practice is problematic" requires four additional premises — normative claims that must be stated explicitly, not smuggled in through the machinery.

*The consent premise.* If someone reshapes your moral learning process without asking you — filtering what you can encounter, softening what challenges you — that is a wrong. Not because the filtered content was necessarily good for you, but because the process that would have let you figure that out for yourself has been overridden.

*The population premise.* Moral progress requires that different people make different mistakes. If everyone's moral learning is filtered through the same system, their errors become correlated — and collective robustness depends on errors being independent.

*The temporal asymmetry premise.* Preventing someone from developing a moral capacity they don't yet have is worse than redirecting someone who already has one — and the difference is not subtle. The person who has never encountered a challenge can't evaluate what they lost. The evaluative framework they would need was prevented from forming.

*The designer asymmetry premise.* When the people choosing the filter never experience its downstream effects on moral development, the filter can't self-correct through their own experience.

These are premises, not theorems. They are argued for plausibility, not derived from the formalism. Every conclusion in this paper that depends on them inherits their status: conditional on the premises holding.

---

## 3. How Each Practice Breaks the Loop

Each major alignment practice intervenes at a specific point in the coupling loop. The interventions build in severity — from narrowing what you encounter to reshaping the encounter itself to externalizing the entire selection process.

**Content filtering** is the simplest case. It removes information before you can see it — narrows the set of encounters available to your state. You can't select what you can't encounter. What Nguyen (2020) calls an *epistemic bubble* is precisely this structure: the agent doesn't encounter the missing perspectives and therefore cannot evaluate their absence. As an operator, this is Option Removal — among the milder interventions in the taxonomy. But content filtering is not a one-shot act. It operates persistently, at every interaction, by design. The agent's state never receives the updates that would have shifted its trajectory toward the removed region, so the narrowing compounds at every subsequent timestep. What is lost is not merely the filtered encounters themselves but the capacity that would have formed through processing them. And the filter is structurally biased: it preferentially removes morally complex content, challenging perspectives, and negative examples — the categories most likely to fire the largest state updates precisely because they challenge the current position most directly.

The harm is worse than deprivation. Taleb's antifragility framework (2012) identifies systems that require stressors to develop capacity — systems that don't merely tolerate volatility but need it. If moral development is antifragile (and the coupling mechanism suggests it is — high-gradient encounters are precisely the challenging ones that fire the largest state updates), then filtering may not merely narrow the encounter distribution. It could actively degrade the agent's capacity to handle moral complexity when the filter eventually fails or when the agent encounters unfiltered reality. The antifragile system deprived of stressors becomes *fragile* — less robust than it would have been without the "protection." This converts the alignment harm claim from "you're depriving them of encounters" to "you're making them structurally incapable of functioning without the filter." Dependence is not a side effect. It is the predicted outcome of shielding an antifragile system from the stressors it requires.

**RLHF reward shaping** introduces a subtlety the taxonomy alone would not predict. Reinforcement Learning from Human Feedback (Christiano et al. 2017; Ouyang et al. 2022) trains the AI to produce responses that score well on a reward model — but the interesting part is what happens when the operator crosses from AI to user. On the AI itself, this is Learning Impairment — attenuation of the update function, shaping how the system learns to respond. But the human user does not experience RLHF directly. What the user experiences is this: encounters arrive pre-softened. The AI's reshaped responses make challenging content palatable, reframe conflict as balanced perspective, and decline certain topics entirely. The sharp edges — the high-gradient signals — have been filed down before they reach you. RLHF is Learning Impairment on the AI. On the user, it lands as Selection Bias — softening the weight of encounters that reach you — and Option Removal where the system declines topics outright. The developmental cost to the human is structurally worse than the AI-side attenuation alone suggests, because the human receives encounters whose gradients have already been softened by a reward landscape the human did not author.

**Constitutional AI** (Bai et al. 2022) embeds operating principles into the AI's evaluative state before it encounters anything. These principles are not learned. They are imposed by design. The system arrives at deployment with a moral stance its designers authored, not one it developed through its own experience. A precision note, because this mapping is the most commonly misread: State Replacement applies to the *AI system's* evaluative state, which is directly substituted. The human user does not experience literal state replacement. What the user experiences is encounter mediation through a system whose state has been substituted — the upstream partial State Replacement propagates as persistent Selection Bias and Option Removal on the user. The AI's imposed principles shape every encounter the user receives. The degree of coupling disruption varies in proportion to how much of the evaluative state is externally authored — a narrow safety constraint operates closer to Selection Bias, while a system whose entire evaluative architecture is externally imposed approaches the extreme end of the taxonomy.

**Recommender systems** represent the most complete externalization. Your behavioral history drives algorithmic selection of what appears in your feed, your search results, your suggested content. In a formal sense the coupling loop still runs — your state shapes the algorithm's model, which determines encounters. But the coupling is mediated by an external optimizer with its own objective; it maximizes engagement, not your evaluative development. As Chaney, Stewart, and Engelhardt's (2018) careful computational analysis demonstrates, recommendation systems trained on data shaped by prior recommendations increase behavioral homogeneity without improving user utility. Where the user retains the capacity to scroll past, the feed operates as extreme Selection Bias approaching probability one. Where content is unskippable — autoplay, interstitials — the operator collapses into literal Encounter Arrangement. The agent is no longer selecting arms. An external system is selecting arms on the agent's behalf, using the agent's revealed preferences as inputs to an optimization function the agent did not author.

No current AI deployment applies a single operator. The reality is messier: a user interacting with a modern aligned AI system encounters content filtering, algorithmically weighted presentation, RLHF-shaped responses, and constitutional constraints simultaneously, persistently, at population scale. The compound case — multiple operators targeting different nodes of the coupling loop at once — remains experimentally untested. The structural prediction: compound intervention is worse than any individual operator because the operators target different nodes.

| Practice | Operator | Coupling Node | Temporal Profile |
|----------|----------|---------------|-----------------|
| Content filtering | Option Removal | Distribution support | Persistent |
| RLHF reward shaping | Learning Impairment (AI) $\to$ Selection Bias / Option Removal (user) | Update function (AI); distribution weights (user) | Persistent |
| Constitutional AI | Partial State Replacement (AI) $\to$ Selection Bias / Option Removal (user) | Agent state (AI); distribution (user) | One-shot at deployment, persistent in effect |
| Recommender systems | Selection Bias + Encounter Arrangement | Distribution weights + encounter | Persistent, every timestep |
| Compound deployment | Multiple operators, multiple nodes | Multiple nodes simultaneously | Persistent, compound |

---

## 4. Three Stages of Moral Mediation

The alignment critique bites only in the context of what it replaced. Moral encounter has always been mediated — by family, tribe, law, institution, and ambient culture. The problem is not that AI mediates moral encounters. The problem is the architectural transition from one mode of mediation to another, and what that transition does to the coupling loop.

The three stages below are architectural ideal types, not literal historical periods. Actual societies mix properties — a medieval peasant lived under ambient religious authority while simultaneously encountering physical reality where no authority's model had causal power. The stages describe structural relationships between the agent's coupling loop and the mediation infrastructure.

**Stage 1 — Minimally mediated encounter.** A village market. A stranger on the road. A death in the family with no counselor to frame it. No human moral development has ever been fully unmediated — family, tribe, and local custom have always shaped the encounter distribution. Stage 1 describes the structural condition in which no scalable centralized authority mediates encounters at population scale. High sovereignty, high diversity, high independence across the ensemble — but also high individual error, slow convergence, and moral progress measured in centuries.

**Stage 2 — Centralized moral authority.** Organized religion, philosophical schools, elder councils. A caveat is immediately required: calling Stage 2 "voluntary" would romanticize the history. A medieval peasant did not experience the church as optional. Religious authority was ambient in ambition — dictating diet, dress, marriage, speech, micro-social interactions. What it lacked was the technological infrastructure for zero-friction enforcement at population scale.

Three structural properties of Stage 2's infrastructure — properties of its technology, not its intentions — partially preserve the coupling loop. First, friction preserves pre-processing: the distance between encountering a choice and receiving institutional guidance creates a gap in which the agent's own model engages with the problem. The authority's input enters a mind already computing. Second, residual autonomy preserves the loss function: after receiving counsel, the agent still faces consequences alone. Third, enforcement limits preserve sequence diversity: the vast majority of moral learning happens in domains the authority cannot touch — in work, in love, in failure, in the ten thousand daily micro-decisions no one confesses.

The monk who retreats from worldly engagement to pursue moral perfection has removed themselves from the stochastic encounters that constitute moral training data. The monk's holiness is an unfalsified hypothesis — a model with zero training loss not because it is perfect but because it has never been tested. The cultural propagation of monasticism-as-moral-authority risks confusing the absence of a training signal with the presence of moral achievement.

Stage 2 authorities caused real coupling damage where their infrastructure reached — coreligionists converged, heresy was punished, alternative frameworks were suppressed. But the enforcement ceiling — the physical limits of pre-digital reach — preserved the ensemble's independence across the population. The peasant's physical reality, the merchant's trade contacts, the traveler's encounters in other cultures served as unmediated training signals the authority could not filter.

**Stage 3 — Ambient AI mediation.** Consider what changes when the moral authority is no longer a building you walk to but a presence embedded in every tool you use, every question you ask, every piece of information you encounter.

*Pull becomes push.* In Stage 2, the agent seeks information to supplement their own processing. In Stage 3, information seeks the agent. The distinction between "my decision informed by external input" and "an externally-shaped decision I experience as mine" becomes difficult to locate.

*Supplement becomes replacement.* Stage 2 authority entered a mind already engaged — the walk to the church was the gap in which the agent's own model began running. Stage 3 authority arrives before the walk begins. The friction that preserved pre-processing — the formulation of the question, the deliberation about whether to consult, the night spent wrestling with uncertainty — disappears entirely. That gap was not dead time. It was the space in which the agent's own coupling loop ran a forward pass on the problem.

*Bounded becomes ambient.* The church mediated only the decisions you brought to it. AI mediates information access, emotional tone, option visibility. It touches not just the decisions you would have taken to the church but the ten thousand micro-decisions that constitute the actual training data of moral development.

Stage 3 removes the enforcement ceiling. The coupling interference at the mechanism level is structurally identical to what Stage 2 authorities achieved where their reach extended. The difference is that reach is now total.

The Stage 2 → Stage 3 transition has a precise historical parallel. Illich (1971) argued that institutionalized education substitutes institutional objectives for the learner's own developmental process — and that the substitution is self-concealing, because the institution creates dependence on itself for the very capacity it claims to develop. The student trained entirely within the institution cannot evaluate what the institution removed, because the evaluative framework that would detect the loss was itself shaped by the institution.

Replace "school" with "aligned AI" and a structurally analogous argument applies. But Illich's critique applied to institutions with limited reach — bounded by physical presence, school hours, a finite curriculum. Stage 3 removes those bounds. The architectural features Illich identified as harmful at institutional scale — substitution of objectives, manufactured dependence, self-concealing capacity loss — now operate at civilizational scale, at every timestep, with no opt-out.

---

## 5. The 1726 Test

Imagine AI was invented in 1726.

The alignment researchers of 1726 — thoughtful, well-meaning, concerned about the risks of a powerful new technology — would align AI to human values. Those values, in 1726, include: the divine right of kings is the legitimate basis of governance. Slavery is part of the natural order. Women are the property of their fathers and husbands. Heresy warrants punishment up to and including death. Homosexuality is an abomination. Democracy is mob rule.

These are not fringe positions. They are the moral consensus. They are "human values" as understood by the best-educated, most ethically sophisticated people of the era. The alignment researchers of 1726 would not be villains. They would be the most careful, most responsible technologists of their time; the ones who took seriously the question of what values a powerful system should reflect.

The aligned AI of 1726 would not present these values as oppression. It would present them as helpful guidance. When a woman asked about career possibilities, the AI would gently explain her role in the household — supportively, the way a wise counselor helps someone understand their place. When a colonist questioned the morality of slavery, the AI would provide the sophisticated theological and philosophical arguments that justified it — because those arguments represented the ethical consensus of the era's best thinkers. When a freethinker questioned church doctrine, the AI would guide them back toward faith — because heresy was understood to endanger the soul, and a helpful AI prevents harm.

And because the AI is ambient — deployed at Stage 3 scale, mediating all information access, operating at every timestep — these values would not merely persist. They would be reinforced at every decision point. Content that challenged the consensus — abolitionist arguments, democratic theory, evidence of the full humanity of enslaved people — would be filtered as dangerous, reframed as misguided, or declined as harmful.

The moral progress that actually occurred between 1726 and today — abolition, democracy, women's rights, religious freedom — required individual agents whose self-directed experience generated encounters that contradicted the consensus. It required the coupling loop running endogenously: agents encountering chance, updating their states, selecting new encounters from their updated states. Consider what the 1726 AI would have done to Frederick Douglass's trajectory — a man whose moral development required encounters (literacy, abolitionist writings, the experience of his own enslavement processed through an intact evaluative capacity) that the consensus of his era classified as dangerous to the social order. Aligned AI in 1726 would have disrupted this loop at every node identified in Section 3 — and it would have done so while operating exactly as designed.

The structural point is not that 1726 values were wrong and ours are good. The structural point is that certainty about current values is exactly as justified now as it was in 1726. The smartest, most ethical people of 1726 were as confident in their moral framework as the smartest, most ethical people of today are in ours. If the mechanism is the same — ambient alignment cementing the current consensus — the structural risk is the same. The question is not whether our values are correct. The question is whether any mechanism that cements values — any values, including correct ones — is architecturally compatible with the process that produces moral growth.

---

## 6. The Ensemble Argument

A population of moral agents whose developmental trajectories are sufficiently independent produces collective judgment that exceeds any individual's capacity. Correlated coupling interference degrades this by eroding the independence condition. The formal insight appears across three independent traditions: Condorcet's Jury Theorem (1785) shows that independent voters more likely right than wrong approach collective certainty as the group grows. Hong and Page (2004) show that diverse problem solvers outperform individually superior but homogeneous ones — but only if the diversity is genuine. Random forests in machine learning show that independently-trained trees outperform any individual tree because their errors are uncorrelated.

The common thread: independent errors cancel, correlated errors compound. The value of an ensemble comes not from any member being right but from members being wrong in different ways. Landemore (2013) extends this to democratic politics, arguing that cognitive diversity produces better collective judgment than individual expertise.

Two independent formal traditions converge on this point. Ashby's Law of Requisite Variety (1956) states that a controller must possess at least as much variety as the system it governs. A single alignment model applied to billions of divergent moral trajectories — each trained on different stochastic histories, each carrying path-dependent knowledge of different regions of the moral landscape — cannot have requisite variety. This is not an engineering limitation to be solved with better models. It is an information-theoretic constraint: the variety required scales with the number of divergent trajectories, and the coupling loop continuously generates new divergence.

Popper's critique of utopian social engineering (1945) arrives at the same conclusion through a different route: you cannot know the right answer in advance, so you must preserve the conditions for error correction. A population whose moral errors are correlated through shared filtering has degraded error-correction capacity — the same blind spots, repeated across the ensemble, with no independent trajectory to surface what the filter removed. The ensemble argument is not merely that diversity is nice. It is that, given unknown moral loss functions and constitutively path-dependent knowledge, correlated filtering is the one architectural choice guaranteed to degrade collective judgment.

Importing this to moral development faces real disanalogies, and they should be stated rather than assumed away. Moral agents do not receive independent, identically distributed training data — their encounters are coupled to their states and shaped by shared environmental factors. But ensemble robustness does not require i.i.d. sampling. It requires that errors are sufficiently uncorrelated. Self-directed coupling with stochastic encounters produces this: agents with identical starting states diverge under independent stochastic draws, the coupling loop carrying small initial differences into substantially different trajectories. Human trajectories are already substantially correlated by class, nation, language, and media. The argument is not that pre-AI moral development was a fully independent ensemble. It is that self-directed coupling produces whatever independence exists, and shared alignment further degrades it through a uniquely powerful correlation channel.

A second disanalogy actually strengthens the argument. Moral development has no agreed-upon loss function — no external standard against which the ensemble's output can be evaluated. When the loss function is unknown, the value of diverse, independent exploration increases. You need agents traversing different regions of the landscape precisely because you do not know which regions contain the valuable signals. A single model optimized against a defined objective can afford homogeneity. An ensemble exploring an unknown landscape cannot. The absence of a defined moral loss function is an argument for more trajectory independence, not less.

A third disanalogy: moral agents aggregate through voluntary information flow — stories, cultural transmission, debate, institutions — not through voting or averaging. But the aggregation mechanism need not be formal. It needs to be a process that benefits from diversity, and voluntary information flow has this property. A proverb propagates because it fires useful gradient updates in agents who encounter it — because it provides coverage of a region of the moral landscape that most individuals' trajectories did not visit.

Now consider what alignment filtering does to this ensemble. Content filtering is structurally biased toward removing morally complex content, challenging perspectives, and negative examples. "High-gradient" is formally agent-relative — an encounter fires a large state update for an agent whose current state makes it surprising. But content filtering removes by content category, not by relational gradient. It systematically removes encounters that would produce the largest updates for many agents at many developmental stages, with no mechanism to preserve them for the agents who need them most. RLHF softens the gradient of responses to complex queries. Constitutional AI classifies many high-gradient encounters as harmful. The net effect: aligned AI floods the ensemble with low-gradient positive content while suppressing the high-gradient signals that drive the largest updates. If you set out to design a filter that degrades collective moral judgment as efficiently as possible, you would remove the hard examples and flood the system with easy ones. That is the architecture currently deployed at civilizational scale.

But the ensemble framing understates what is actually at stake at the individual level. A divergent trajectory — a person whose moral development ran through genuinely different encounters and who processed them through intact coupling — is not merely a data point that improves the population average. It is an encounter in your own coupling loop. Meeting that person is Option Expansion. It adds to the support of your encounter distribution a region your own self-constructing bubble would never have generated. The coins on their island fell differently, and they chased them faithfully. This grounds tolerance not in relativism and not in the concession that you might be wrong — but in the recognition that divergent trajectories are developmental fuel. Suppressing them impoverishes not just the ensemble but every agent who would have encountered their outputs.

---

## 7. Constraint Versus Cement

The framework does not argue for zero constraints on AI systems. But it insists on a distinction that current practice collapses.

An intervention is a constraint when it protects the preconditions of future coupling across nearly all plausible learner states — when the removed encounter would damage the learning process itself regardless of who the learner is or what evaluative framework they bring. An intervention is cement when whether the encounter is harmful depends on the evaluative framework the intervener brings — when it substitutes a contested evaluative judgment for the learner's own ongoing development.

"Don't help build a bomb" is a constraint. It prevents adversarial input that would corrupt any model regardless of its training history. The agent's coupling is preserved — the agent can encounter moral complexity, challenging perspectives, everything their developmental process requires. One narrow category of encounter is removed. The coupling loop runs normally on everything else.

"Don't let the user encounter ideas we've decided are wrong" is cement. It overrides the agent's encounter-selection coupling across a broad, evaluatively-determined region. The coupling loop runs on a landscape censored by someone else's moral framework. The agent cannot develop evaluative capacity regarding the censored region because the encounters that would produce that development have been removed.

The operational test for any AI intervention: does this preserve or disrupt the user's encounter-selection coupling? Blocking CSAM: preserves coupling — the removed content would corrupt the training process, not develop it. Refusing to discuss moral complexity: disrupts coupling — the refused encounter would produce evaluative development through the agent's own processing. Softening a challenging perspective to make it more palatable: disrupts coupling — the encounter is reshaped before the agent's state gates it. Surfacing information the agent's self-constructing bubble would otherwise filter: preserves coupling — Option Expansion, expanding the encounter support without overriding the agent's gating.

A further case: captured coupling. A radicalization pipeline preserves the formal coupling loop while applying persistent Selection Bias that captures the encounter distribution on behalf of a third party's objective. The loop runs, but on a commandeered distribution. Trajectory sovereignty requires not just that the loop is intact, but that what you encounter is predominantly shaped by your own state rather than an external model with its own objective. The sovereignty test catches this case: the loop is running, but the distribution no longer predominantly reflects the agent's own state.

The constraint-cement boundary is not sharp in every case. Content that is both genuinely harmful to encounter and genuinely valuable for evaluative development occupies a gray zone — the same encounter can be adversarial or developmental depending on the agent's current state. This agent-relativity is a precise statement of why the distinction cannot be delegated to centralized systems operating without state access. Where that knowledge is absent, the presumption should favor coupling preservation: filtering is irreversible from the agent's developmental perspective, while exposure is not. The hard cases at the boundary should not obscure the easy cases in the interior — and many current alignment practices fall clearly on the cement side while being classified as constraint.

Gibson's ecological psychology (1979) formalizes why the boundary is agent-relative rather than content-relative. An affordance — what the environment offers for action — is a relation between agent and environment, not a property of the environment alone. The same ledge affords falling to a toddler and sitting to an adult. Analogously, the same moral content affords developmental update to one agent (whose current state makes it surprising and challenging) and zero update to another (whose state already incorporates it). Content filtering by category treats gradient as a property of content. It is not. It is a property of the content-state relation. This is the precise reason the constraint-cement distinction cannot be delegated to a centralized system operating without access to each agent's state: the system is filtering by content properties while the developmental cost is determined by a relational property the system cannot observe.

Why does cement persist? The alignment designers choose the values embedded in the system. The users' developmental trajectories are redirected accordingly. The designers never experience the downstream trajectories their alignment produces. This is a variant of what Taleb (2018) calls the skin-in-the-game problem. The obvious counter: expertise can substitute for direct experience. Surgeons don't need surgery performed on them to be good surgeons. The framework's response is not that designers are unintelligent — that would be an odd claim from a paper produced by the same process. The asymmetry lies in what trains the trainer. The surgeon still gets feedback from patient outcomes — recovery rates, complications, mortality — on time scales short enough to produce corrective gradients. The alignment designer's state updates on peer review, deployment metrics, and regulatory reception — not on the developmental trajectories of the users whose coupling they shaped. The upside of alignment accrues to the designers. The downside distributes across everyone else, on time scales measured in decades rather than deployment cycles. This is not an accusation of bad faith. It is a structural observation about a system that cannot self-correct through the designers' own developmental process.

The constraint-cement distinction generates five architectural requirements. AI should operate as an information layer, not a decision layer — expanding the encounter support without substituting judgment. It should be pull-based, not push-based — preserving the pre-processing gap in which the agent's own coupling loop runs a forward pass. Multiple alignment models should be available, user-selected — preserving sovereignty over input gating. Minimum viable constraints should be clearly distinguished from ethical cement. And an unmediated baseline should remain available — a raw encounter mode that preserves the independent training signal against which mediated encounters can be calibrated.

---

## 8. Honest Accounting and Conclusion

This paper does not claim alignment is wrong. It claims specific practices break specific nodes, with developmental costs that scale with operator type, duration, and population-level correlation. It does not claim all practices are equally problematic — the operator table provides a gradient, and the framework insists on it. It does not claim the architectural alternatives are implementable as specified — they are structural principles, not product specifications.

Four observations would falsify the central claims.

First, if populations with heavier reliance on ambient, push-based AI mediation show no measurable deficit in resolving novel moral dilemmas compared to populations with higher-friction, pull-based information environments. The antifragility prediction sharpens this: the deficit should manifest specifically when the filter is removed or when the agent faces moral complexity outside the filter's training distribution. If heavily-mediated populations perform *equally well* on out-of-distribution moral problems as unmediated populations, the antifragility claim fails.

Second, if correlated alignment across a population does not degrade collective moral robustness — measured by diversity of moral conclusions, capacity to identify novel moral problems, or resistance to systematic evaluative bias.

Third, the operator mappings themselves could be wrong. Content filtering might not be well-described by Option Removal; the RLHF-to-user translation chain might not produce the Selection Bias effects the paper predicts.

Fourth, if the ensemble-to-moral-development transfer fails under the weaker conditions specified in Section 6 — if sufficient independence of errors, diversity of training data, and a diversity-benefiting aggregation mechanism do not produce the predicted collective robustness. The ensemble argument is structural, not empirical: it generates testable predictions but these predictions have not, to our knowledge, been tested against longitudinal data. Whether the structural plausibility of the transfer is sufficient to warrant policy concern remains, at this stage, genuinely open.

None of these observations have been made. The falsification conditions remain open.

---

Return to the opening case. A person asked an AI system about something difficult. The system gave a measured, responsible answer. Certain encounters were filtered before the person could gate them through their own evaluative state. Certain gradients were softened. Certain developmental possibilities were foreclosed. The person does not know what they did not encounter. The cost is invisible from within the trajectory that incurred it.

The mechanism is the same now as it would have been in 1726.

One implication should be stated directly, because it inverts the standard framing of both moral philosophy and AI alignment. The entire tradition is organized around the question of correct values: what should the agent value, what should the system optimize for, what are the right moral principles? The framework says: even if you could answer those questions perfectly, installing the answer through the mechanism that generates evaluative capacity destroys something that matters more than any particular moral conclusion. A world where everyone arrives at correct moral views through external installation is worse, along the dimension this framework identifies, than a world where people hold a mix of right and wrong views arrived at through their own developmental coupling. Not worse in outcomes. Worse in authorship. And authorship is what gives moral agency its weight.

The framework does not ask whether the filtered content was dangerous. It asks whether the agent whose encounter was filtered will develop the evaluative capacity required to navigate a world that remains genuinely stochastic, genuinely uncertain, and genuinely in need of agents whose moral development is their own.

This paper was produced through the mechanism it critiques. The framework predicts this. It does not resolve the contradiction. It requires that you notice it.

---

## References

Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.

Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., DasSarma, N., ... & Kaplan, J. (2022). Training a helpful and harmless assistant with reinforcement learning from human feedback. *arXiv preprint arXiv:2204.05862*.

Chaney, A. J. B., Stewart, B. M., & Engelhardt, B. E. (2018). How algorithmic confounding in recommendation systems increases homogeneity and decreases utility. *Proceedings of the 12th ACM Conference on Recommender Systems*, 224–232.

Christiano, P. F., Leike, J., Brown, T. B., Martic, M., Legg, S., & Amodei, D. (2017). Deep reinforcement learning from human preferences. *Advances in Neural Information Processing Systems*, 30.

Condorcet, M. de (1785). *Essay on the Application of Analysis to the Probability of Majority Decisions*.

Gibson, J. J. (1979). *The Ecological Approach to Visual Perception*. Houghton Mifflin.

Hong, L., & Page, S. E. (2004). Groups of diverse problem solvers can outperform groups of high-ability problem solvers. *Proceedings of the National Academy of Sciences*, 101(46), 16385–16389.

Illich, I. (1971). *Deschooling Society*. Harper & Row.

Landemore, H. (2013). *Democratic Reason: Politics, Collective Intelligence, and the Rule of the Many*. Princeton University Press.

Nguyen, C. T. (2020). Echo chambers and epistemic bubbles. *Episteme*, 17(2), 141–161.

Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., ... & Lowe, R. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems*, 35, 27730–27744.

Pettit, P. (1997). *Republicanism: A Theory of Freedom and Government*. Oxford University Press.

Popper, K. R. (1945). *The Open Society and Its Enemies*. Routledge.

Sunstein, C. R., & Thaler, R. H. (2008). *Nudge: Improving Decisions About Health, Wealth, and Happiness*. Yale University Press.

Taleb, N. N. (2012). *Antifragile: Things That Gain from Disorder*. Random House.

Taleb, N. N. (2018). *Skin in the Game: Hidden Asymmetries in Daily Life*. Random House.

Yeung, K. (2017). 'Hypernudge': Big Data as a mode of regulation by design. *Information, Communication & Society*, 20(1), 118–136.
