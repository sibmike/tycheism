# arXiv Submission Guidelines — Local Reference

Captured from <https://info.arxiv.org/help/submit/index.html> on 2026-04-22 for the Tycheism trilogy submission effort. This file is a local snapshot of the rules that matter for our submissions. Re-check the upstream page before each submission cycle — arXiv policy occasionally shifts.

## 1. Accepted source formats (in arXiv's preferred order)

1. **(La)TeX / AMSLaTeX / PDFLaTeX source** — strongly preferred. arXiv's stated rationale: "store articles in formats that are highly portable and stable over time."
2. **PDF** — accepted, but second-class. PDFs produced from LaTeX should be submitted as the LaTeX source, not the compiled PDF.
3. **HTML with raster images** — accepted for conference proceedings only.

**Not accepted:** DVI, PostScript, scanned documents, Markdown. Anything submitted as a PDF produced from TeX/LaTeX source will be flagged.

Our path: Markdown → (pandoc) → LaTeX source + figure PNGs → ZIP → arXiv.

## 2. Figure / image requirements

| Compiler | Accepted figure formats |
|---|---|
| Plain LaTeX | PS, EPS only |
| PDFLaTeX | PNG, JPG, GIF, PDF |

- arXiv does **not** auto-convert figure formats — pre-convert before upload.
- Filenames are **case-sensitive** and must match `\includegraphics{}` references exactly.
- Filenames may contain only: `a-z A-Z 0-9 _ + - . , =`. No spaces, no special chars.
- Use the `graphicx` package (not legacy `graphics`) for figure inclusion.
- "arXiv does not accept submissions with omitted figures, even if you provide links." All figures must be bundled in the upload.

## 3. File packaging

- Upload as **ZIP** or **TAR.GZ** preserving relative paths, or as individual files.
- arXiv auto-detects the top-level `.tex` file (the one containing `\documentclass`).
- Use relative paths in `\includegraphics` — `figures/figure3.png`, never absolute paths.

## 4. File size limits

Not explicitly stated on the main submit page; arXiv maintains a separate "Oversized Submissions" help page. Our papers are text-heavy with <10 figures each and well under typical limits (~10 MB).

## 5. Required metadata

Mandatory fields during submission:
- **Title** (plain text)
- **Abstract** (plain text; no LaTeX markup, bullet points, or headings — arXiv renders it verbatim)
- **Authors and affiliations**
- **Primary category** from the arXiv taxonomy
- **License selection**
- Acceptance of the Submittal Agreement, code of conduct, moderation policy, privacy policy

Optional fields:
- **Cross-list categories** (additional topical categories)
- **Comments** (free-text; typical uses: page count, "companion paper to arXiv:xxxx.xxxxx", code repository link)
- **Journal reference** and **DOI** (add later, post-publication)

## 6. License options

arXiv offers at submission time:
- arXiv non-exclusive license (most permissive for arXiv, restrictive for readers — avoid)
- CC-BY-4.0
- CC-BY-SA-4.0
- CC-BY-NC-SA-4.0
- CC0 (public domain dedication)

**Tycheism trilogy uses CC-BY-4.0** (matches repo `LICENSE` and `CITATION.cff`).

## 7. Endorsement

First-time submitters to a category may need an **endorsement** from an existing author in that category. This is a common first-submission friction point:
- Register at arXiv.org with an institutional or established email.
- Attempt submission; arXiv will tell you if endorsement is required.
- If required, email colleagues already publishing in that category and request endorsement through arXiv's endorsement flow.
- Endorsement is per-category, so `cs.LG` endorsement does not automatically grant `cs.AI` or `nlin.AO`.

Plan: Paper A will be our first submission; if endorsement is required, resolve before Papers B and C.

## 8. Categories relevant to the Tycheism trilogy

Full taxonomy: <https://arxiv.org/category_taxonomy>.

| Paper | Primary | Cross-lists | Rationale |
|---|---|---|---|
| Paper A — Trajectory Divergence | `cs.LG` | `cs.AI`, `nlin.AO` | Coupled stochastic learning simulation; ML methodology primary, adaptation/self-organization cross |
| Paper B — Trajectory Sovereignty | `cs.CY` | `cs.AI` | Meta-ethics / epistemic argument; arXiv has no philosophy category, `cs.CY` (Computers & Society) is the closest fit |
| Paper C — Alignment as Coupling Interference | `cs.AI` | `cs.CY`, `cs.LG` | AI alignment critique; AI primary, computers-and-society + ML cross |

## 9. Common rejection / processing causes

1. **Missing figures** — figures referenced but not bundled.
2. **Filename case mismatch** — e.g. `Figure1.PDF` referenced but file is `figure1.pdf`.
3. **Spaces or special characters in filenames**.
4. **Absolute paths** in `\includegraphics` — always relative.
5. **Mixed figure formats** — don't mix PS/EPS and PNG/PDF in one submission; use one compiler (PDFLaTeX → PNG/PDF).
6. **Missing custom style files** — bundle all non-standard `.sty` files.
7. **Hyperref package conflicts** — check the compilation log past the first hyperref error for root causes.

## 10. Announcement timing

- Submissions received by **14:00 US Eastern** are announced at **20:00 same day**.
- Edits before 14:00 do not delay announcement.
- Check <http://arxiv.org/localtime> before submitting.

For the trilogy, submit in order A → B → C on successive days so later papers can reference the earlier arXiv IDs in their text and `comments` field.

## 11. Replacements vs new submissions

- **Corrections after announcement:** use the "replace" flow on the original arXiv ID. Do NOT make a new submission.
- **Pre-announcement corrections:** use the "Unsubmit" button on the user page to return the article to incomplete status; note that resubmission time becomes the new effective submission time.
- arXiv tracks all versions (v1, v2, v3, …); earlier versions remain accessible.

## 12. Series linkage

arXiv has **no formal "series" or "trilogy" metadata**. Linking between papers is done through:
- The `comments` field (e.g. "Paper II of three; companion to arXiv:xxxx.xxxxx")
- In-text references to arXiv IDs once assigned
- Optional: cross-references on the authors' personal or institutional pages

## 13. Self-submission requirement

- "Authors are expected to self-submit." Third-party submission is possible only under narrow conditions.
- Register at <https://arxiv.org/user/register> before attempting first submission.

## 14. Submission workflow summary (what we actually do)

1. Build `paper_X.tex` and `figures/` via `build.sh` (pandoc + pdflatex).
2. Verify `paper_X.pdf` renders correctly (figures in place, math typeset, tables clean).
3. From `arxiv/paper_X/`, run: `zip -r paper_X.zip paper_X.tex figures/`.
4. Log into arxiv.org, click "Start New Submission".
5. Upload `paper_X.zip`.
6. Wait for arXiv's automatic TeX compilation (shows preview PDF).
7. If preview matches local PDF → fill metadata (title, abstract, authors, categories, license, comments).
8. Submit.
9. Record the assigned arXiv ID in `arxiv/README.md` so later papers can cite it.
