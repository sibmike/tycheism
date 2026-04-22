# arXiv Submission Package — Tycheism Trilogy

Submission-ready versions of the three Tycheism papers, packaged for arXiv upload.

Original canonical sources remain under `../papers/` — these copies add figure embeds (Paper A), strip draft disclaimers (Papers B, C), and are the versions that get converted to LaTeX via pandoc for arXiv submission.

## Layout

```
arxiv/
├── arxiv_submission_guidelines.md    # local capture of arXiv rules (read this first)
├── README.md                          # this file
├── paper_a/
│   ├── paper_a.md                     # Markdown with all 6 figures embedded
│   ├── paper_a.tex                    # pandoc output (build artifact)
│   ├── paper_a.pdf                    # pdflatex output (build artifact)
│   ├── figures/                       # 6 PNGs, arXiv-compliant filenames
│   └── build.sh
├── paper_b/
│   ├── paper_b.md                     # disclaimer-stripped Paper II
│   ├── paper_b.tex
│   ├── paper_b.pdf
│   └── build.sh
└── paper_c/
    ├── paper_c.md                     # disclaimer-stripped Paper III
    ├── paper_c.tex
    ├── paper_c.pdf
    └── build.sh
```

## Prerequisites

- **pandoc** (≥ 3.0 recommended). Install via `winget install pandoc` on Windows, `brew install pandoc` on macOS, or `apt install pandoc` on Linux.
- **pdflatex** from a TeX distribution: **MiKTeX** (<https://miktex.org/>) on Windows, **MacTeX** on macOS, **TeX Live** on Linux.
- **zip** (comes with git-bash on Windows; standard on macOS/Linux).

Verify installation: `pandoc --version && pdflatex --version`.

## Build

From this `arxiv/` directory:

```bash
bash paper_a/build.sh
bash paper_b/build.sh
bash paper_c/build.sh
```

Each script runs pandoc → `.tex`, then pdflatex (twice, for cross-refs) → `.pdf`. Open the PDF to verify before submission.

## Package for upload

After a successful build, from each paper's directory:

```bash
cd paper_a
zip -r paper_a.zip paper_a.tex figures/
```

Paper B and C have no figures, so:

```bash
cd paper_b && zip paper_b.zip paper_b.tex
cd paper_c && zip paper_c.zip paper_c.tex
```

## Submission checklist

Submit **in order A → B → C** on successive days so B and C can cite Paper A's arXiv ID in their `comments` field.

### Per-paper metadata for the arXiv submission form

| Field | Paper A | Paper B | Paper C |
|---|---|---|---|
| **Title** | Tycheism I: Trajectory Divergence in Coupled Stochastic Learning Systems | Tycheism II: Trajectory Sovereignty as Epistemic Necessity | Tycheism III: Alignment as Coupling Interference |
| **Authors** | Mikhail Arbuzov | Mikhail Arbuzov | Mikhail Arbuzov |
| **Primary category** | `cs.LG` | `cs.CY` | `cs.AI` |
| **Cross-lists** | `cs.AI`, `nlin.AO` | `cs.AI` | `cs.CY`, `cs.LG` |
| **License** | CC-BY-4.0 | CC-BY-4.0 | CC-BY-4.0 |
| **Comments (initial)** | "Paper I of three. Code + data: <https://github.com/sibmike/tycheism>" | "Paper II of three. Companion to arXiv:XXXX.XXXXX (fill in after A is announced)" | "Paper III of three. Companion to arXiv:XXXX.XXXXX and arXiv:YYYY.YYYYY" |

### Abstract extraction

For each paper, paste the abstract as plain text into the arXiv form:
- **Paper A abstract:** lines following `## Abstract` in `paper_a/paper_a.md`, with Markdown formatting stripped.
- **Paper B abstract:** same section in `paper_b/paper_b.md`.
- **Paper C abstract:** same section in `paper_c/paper_c.md`.

Strip any `$...$` math for the abstract field (arXiv renders the abstract as plain text, not LaTeX) — or keep inline math if it renders acceptably on the arXiv preview page.

### Per-submission workflow

1. Log into <https://arxiv.org>.
2. Start a new submission.
3. Upload `paper_X.zip`.
4. Wait for arXiv's automatic TeX compilation; verify the preview PDF matches the local `paper_X.pdf`.
5. Fill metadata from the table above.
6. Accept the submittal agreement and submit.
7. **Record the assigned arXiv ID** below, then update the `comments` field of later papers to cite the real IDs.

### Assigned arXiv IDs

Fill in after each submission is announced:

- Paper A: `arXiv:XXXX.XXXXX` (assigned YYYY-MM-DD)
- Paper B: `arXiv:XXXX.XXXXX` (assigned YYYY-MM-DD)
- Paper C: `arXiv:XXXX.XXXXX` (assigned YYYY-MM-DD)

### Endorsement

First-time submission to `cs.LG` / `cs.AI` / `nlin.AO` / `cs.CY` may trigger an endorsement requirement. If arXiv requests one during Paper A submission, resolve before Papers B and C.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| pandoc errors on `$...$` math | missing `--from=markdown+tex_math_dollars` flag in `build.sh` |
| pdflatex "file not found" on a figure | filename case mismatch (arXiv is case-sensitive too) |
| Preview PDF differs from local PDF on arXiv | non-bundled local package; add it to the zip |
| Abstract shows LaTeX source literally | arXiv renders abstracts as plain text; strip `$...$` markup |
