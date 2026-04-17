# Tycheism

**A developmental meta-ethics framework: if moral growth is a coupled stochastic process, preserving the coupling is a precondition for moral agency.**

Tycheism builds ethics from Charles Sanders Peirce's 1892 claim that chance is ontologically real. The core move: if moral development is a coupled stochastic process — your state shapes your encounters, your encounters update your state — then interventions that break that coupling don't impose wrong values. They destroy the mechanism by which values form at all.

This is **developmental meta-ethics**, not a moral theory. It does not say what is good. It says what must remain intact for agents to develop the capacity to figure out what is good.

---

## The Coupled System

Two equations define the dynamics every paper in this repository builds on:

```
e_{t+1} ~ K(s_t)              # encounter drawn from a state-dependent kernel
s_{t+1} = U(s_t, e_{t+1})     # state updated by the realized encounter
```

- `s_t` — agent state (compressed accumulated experience)
- `K(s_t)` — encounter kernel (state-dependent distribution over possible encounters)
- `e_{t+1}` — realized encounter (a single draw from `K`)
- `U` — state update function

Six intervention operators target different nodes of this loop: `I_K+` (expand options), `I_K-` (truncate options), `I_Kw` (reshape weights), `I_e` (determine encounter), `I_s` (substitute state), `I_U` (reshape learning). They differ in **sovereignty cost** — how much they replace what the coupled loop would have generated on its own.

---

## Four Levels of Claim

The framework is explicit about which level any given argument operates at. Conflating levels is the most common error.

| Level | Type | Content |
|---|---|---|
| **0** | Formal substrate (descriptive) | The coupled dynamical system. No ethics. Math only. |
| **1** | Empirical claim | Moral development is an instance of Level 0. The load-bearing wall. |
| **2** | Normative constraint | If Level 1 holds, coupling-preservation is a precondition for moral agency. |
| **3** | Applied ethics | Trajectory sovereignty, autonomy harm, alignment critique. Requires additional normative premises stated explicitly. |

---

## Papers

The trilogy:

| Paper | Levels | Status | Location |
|---|---|---|---|
| **Tycheism I — Trajectory Divergence in Coupled Stochastic Learning Systems** | L0 only | **Final** | [`papers/paper_a_trajectory_divergence.md`](papers/paper_a_trajectory_divergence.md) |
| **Tycheism II — Trajectory Sovereignty as Epistemic Necessity** | L1 → L2 | Working draft (v6) | [`papers/drafts/paper_b_developmental_meta_ethics_DRAFT.md`](papers/drafts/paper_b_developmental_meta_ethics_DRAFT.md) |
| **Tycheism III — Alignment as Coupling Interference** | L2 → L3 | Working draft (v6) | [`papers/drafts/paper_c_alignment_critique_DRAFT.md`](papers/drafts/paper_c_alignment_critique_DRAFT.md) |

Paper I is the only finalized paper. Papers II and III are included as working drafts so the full scope of the trilogy is visible. Drafts will be replaced as they are completed.

---

## Reproducing the Results

All Paper I results are produced by a spatial bandit simulation in [`simulation/`](simulation/). Results (`.npz`) and figures (`.png`) are committed for direct inspection; the experiment scripts regenerate them from scratch.

```bash
cd simulation
pip install -r requirements.txt
python -m experiments.exp2_intervention_cascade   # any experiment
python generate_figures.py                        # rebuild all figures
```

See [`simulation/README.md`](simulation/README.md) for the full experiment list and per-experiment details.

---

## Acknowledged Limitations

The framework has known weaknesses, stated up front:

- **Level 1 is underargued.** The claim that moral development instantiates the coupled-learner class is argued, not proven. Paper II carries this burden and is still in draft.
- **Sovereignty-cost thresholds are intuitive, not derived.** The ranking of intervention operators is qualitative.
- **Trajectory divergence is now quantitative for the toy model only.** Paper I's spatial bandit demonstrates the dynamics in a fully-controlled environment; the leap from there to moral development is the work of Paper II.
- **Ensemble independence imports ML results into ethics** without fully justifying the analogy.

These are acknowledged, not resolved.

---

## Citation

If you use or reference this work, please cite using [`CITATION.cff`](CITATION.cff). A short form:

> Arbuzov, M. (2026). *Tycheism I: Trajectory Divergence in Coupled Stochastic Learning Systems*. https://github.com/sibmike/tycheism

---

## License

- **Prose (everything in `papers/` and this README):** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-TEXT).
- **Code (everything in `simulation/`):** [MIT License](LICENSE).

Reuse is welcome with attribution.
