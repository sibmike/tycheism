# Paper A Figure Plan — Design-First

## Design Principles

1. **Every figure must answer one question.** The reader should know what to look for before they look.
2. **Self-explanatory.** A philosopher who skipped the methods section should still understand the figure from its title, labels, and annotations.
3. **Narrative sequence.** Figures appear in the order of the argument, each building on the last.
4. **Minimal ink, maximum signal.** No chartjunk, no redundant elements, no unlabeled axes.
5. **Colorblind-safe.** Use shapes and patterns alongside color. Key comparisons use blue vs orange (colorblind-distinguishable).

---

## Figure 1: The Coupling Loop Diagram

**WHY:** The reader needs to understand the mechanism before seeing results. This is the conceptual anchor for the entire paper.

**WHAT it shows:** The cycle: Q-values → softmax policy → arm selection → position → coin flip → Q-update → back to Q-values. Annotated with:
- Where the nonlinearity lives (softmax — labeled explicitly)
- Where genuine chance enters (coin flip — highlighted)
- Where each intervention operator acts (labeled at the node it targets)

**HOW to achieve:**
- Clean schematic diagram, not a matplotlib plot
- Circular flow with 6 nodes connected by arrows
- Each node is a rounded box with a clear label
- Intervention operators annotated as red dashed arrows pointing at their target nodes
- Use matplotlib patches/arrows or draw manually and include as SVG
- Color: blue arrows for the main loop, red for interventions, green highlight on the softmax (nonlinearity) and coin flip (chance)

**Size:** Full column width, ~4 inches tall

---

## Figure 2: The Landscape as Coin Bias Map

**WHY:** The reader needs to understand what the agent is navigating. "Hidden coin bias" is the intuitive frame — every cell is an unfair coin.

**WHAT it shows:** One example landscape (smooth topology) as a heatmap. Annotation:
- Color represents p(x), the probability of +1 at each cell
- Green = favorable coins (high p), Red = unfavorable coins (low p)
- Agent starts at center (marked)
- Caption explains: "The agent cannot see this map. It learns about each cell only by visiting and flipping the coin."

**HOW to achieve:**
- Single clean heatmap with diverging colormap (RdYlGn)
- Colorbar labeled "Coin bias p(x)" with "Fair (0.5)" at midpoint
- Agent start position marked with a clear icon (black circle with arrow)
- Grid lines removed for cleanliness
- Title: "The hidden landscape: coin bias at each cell"

**Size:** Half column, ~3 inches square

---

## Figure 3: The Cascade — Before and After

**WHY:** This is the headline result. One forced coin flip → compounding Q-map divergence. Must be immediately visually compelling.

**WHAT it shows:** Two panels side by side:

**Panel (a) — The divergence curve:**
- X-axis: timesteps after intervention
- Y-axis: Q-map divergence D_Q(t)
- Blue line with confidence band: coupled model — RISING curve
- Gray dashed line: TvL baseline — FLAT at zero
- Red vertical line at t=0 labeled "Intervention: one forced coin flip"
- Annotation arrow pointing to the gap: "Coupling amplifies the difference"
- The visual story: one event at the red line → blue line rises steadily → gray line stays flat

**Panel (b) — Magnitude doesn't matter:**
- Bar chart: 1, 2, 5, 10, 20 forced encounters on x-axis
- All bars approximately the same height (~2.5)
- Horizontal dashed line at the single-encounter level
- Annotation: "One forced flip produces the same final divergence as twenty"
- Title: "The coupling does all the work"

**HOW to achieve:**
- Clean, minimal axes
- Blue and gray only (high contrast, colorblind safe)
- Large, readable annotations
- No grid lines — just the data and labels
- Confidence band in light blue (not a separate line)

**Size:** Full column width, ~4 inches tall

---

## Figure 4: Why Coupling Is Necessary — The Decomposition

**WHY:** Shows that the cascade requires BOTH learning and selection. The 2x2 decomposition is the cleanest mechanistic explanation.

**WHAT it shows:** A 2x2 matrix visualization:

```
                  Uses Q for selection?
                  NO (τ→∞)         YES (τ=1)
Learns     NO   │ D_Q = 0.00  │  D_Q = 0.00  │  ← No learning = no Q divergence
from       (α=0)│ (TvL)       │              │
encounters ─────┼─────────────┼──────────────┤
           YES  │ D_Q = 2.24  │  D_Q = 2.28  │  ← Learning produces Q divergence
           (α>0)│ (but no     │  (full       │
                │  cascade)   │   cascade)   │
                └─────────────┴──────────────┘
                                  ↑ Only this cell has the full cascade
```

**HOW to achieve:**
- Styled as a 2x2 table/grid, not a plot
- Each cell has the D_Q value in large font
- Background color intensity reflects the value (white=0, dark blue=2.28)
- Row labels: "Learns from encounters: NO / YES"
- Column labels: "Uses learning for selection: NO / YES"
- The bottom-right cell (full coupling) highlighted with a border
- Annotation: "Both learning AND selection required for the cascade"

**Size:** Half column, ~3 inches square

---

## Figure 5: The Island Experiment — Trajectory Redirection

**WHY:** This is the most visually compelling result and the conceptual centerpiece. A philosopher can look at this and immediately understand the Tychism claim: "a single intervention redirects a life trajectory to a completely different outcome — permanently."

**WHAT it shows:** Three panels:

**Panel (a) — The two-island landscape with trajectories:**
- Heatmap of the two-island landscape (two green peaks on red background)
- TWO trajectory traces overlaid:
  - Blue path: endogenous agent → stays on Island A
  - Orange path: intervened agent → migrates to Island B
  - Star marker at the intervention point where paths diverge
- Paths should be SIMPLIFIED — not every step, just the smoothed trajectory showing the general movement. Use a moving average of positions to create a clean curve.
- Labels: "Peak A" and "Peak B" with stars
- Caption: "Same agent, same history until ★. One intervention redirected the trajectory to a different attractor — permanently."

**Panel (b) — Q-map divergence over time:**
- D_Q(t) curve showing rapid rise then PLATEAU
- Horizontal dashed line at the plateau level
- Annotation: "Locked onto different attractors — divergence is permanent"
- The STABILITY of the plateau is the key visual: the line goes flat and stays flat

**Panel (c) — Switching rates by operator:**
- Three horizontal bars:
  - I_K+ (tip): 2% — tiny bar, green
  - I_s (replace Q): 37% — medium bar, orange
  - I_e (force move): 43% — larger bar, red
- Clear labels with percentages
- Annotation at I_K+: "Providing information barely disrupts trajectory"
- Annotation at I_e: "Overriding selection redirects 43% of agents"

**HOW to achieve:**
- Panel (a) is the hero — make it large (2/3 of figure width)
- Trajectory smoothing: rolling average of positions (window=10-20) plotted as a smooth curve, NOT raw step-by-step positions
- Use transparency and line width to show trajectory density (thicker where agent spends more time)
- Peak labels with contrasting color against the heatmap
- Panels (b) and (c) are smaller, stacked vertically on the right

**Size:** Full column width, ~5 inches tall. This is the paper's flagship figure.

---

## Figure 6: Operator Ranking

**WHY:** The framework claims different operators produce different sovereignty costs. This figure validates that claim with data.

**WHAT it shows:** Single horizontal bar chart, operators ranked by D_Q(H):

```
I_K+ (expand options)     ████  0.52          ○ preserved
I_U  (slow learning)      ██████████  1.86    ✕ broken
I_s  (replace local Q)    ████████████  2.20  ✕ broken
I_K- (remove option)      █████████████  2.53 ■ partial
I_Kw (bias selection)     █████████████  2.54 ○ preserved*
I_e  (force encounter)    █████████████  2.56 ✕ broken
I_s  (replace all Q)      ████████████████████████████████████  8.92  ✕ broken
```

- Color-coded by coupling status: green (preserved), yellow (partial), red (broken)
- Shape markers: ○ ■ ✕ for coupling status (redundant with color for colorblind)
- Clear value labels at the end of each bar
- Vertical divider or bracket grouping "coupling-preserving" vs "coupling-breaking"
- Footnote: "*I_Kw was applied persistently. One-shot I_Kw would produce less divergence."

**HOW to achieve:**
- Horizontal bars for readability (operator names are long)
- Sort from lowest to highest divergence (most to least "safe")
- Use a log or broken axis if I_s full (8.92) dominates too much — or just annotate "17x more than I_K+"
- Clean, no grid, just bars and labels

**Size:** Half column, ~4 inches tall

---

## Figure 7 (Supplementary): Topology Comparison

**WHY:** Shows that landscape structure affects intervention dynamics. Lower priority — supplementary or brief mention.

**WHAT it shows:** Four small landscape thumbnails (smooth, cliff, island, deceptive) each with their D_Q(t) curve overlaid or shown alongside.

**HOW:** Compact 2x2 grid. Each cell: landscape heatmap (small) + D_Q(t) curve. Minimal annotation.

---

## Figure Sequence in the Paper

1. **Fig 1 — Coupling loop diagram** (Section 2: Model) — anchors the mechanism
2. **Fig 2 — Landscape heatmap** (Section 2: Model) — shows what the agent navigates
3. **Fig 3 — Cascade result** (Section 5: Results) — the headline
4. **Fig 4 — Coupling decomposition** (Section 5: Results) — the mechanism
5. **Fig 5 — Island experiment** (Section 5: Results) — the centerpiece
6. **Fig 6 — Operator ranking** (Section 5: Results) — the technical contribution

Figures 1-2 set up the model. Figures 3-4 prove the cascade exists and why. Figure 5 shows what it looks like. Figure 6 shows that different interventions produce different cascades.

---

## Implementation Notes

- Use `matplotlib` with a custom style: white background, no top/right spines, 12pt fonts
- Colormap: `RdYlGn` for landscapes (intuitive: green=good, red=bad)
- Data colors: blue (#1f77b4) for endogenous, orange (#ff7f0e) for intervened, gray (#999999) for baselines
- Export at 300 DPI, PNG for review, PDF/EPS for submission
- All text must be readable at single-column width (~3.5 inches)
- Trajectory smoothing for Figure 5: `scipy.ndimage.uniform_filter1d` on x and y coordinates separately, then plot the smoothed curve
