#!/usr/bin/env bash
# Build Tycheism III for arXiv: Markdown -> LaTeX -> PDF
#
# Requires: pandoc, pdflatex (MiKTeX or TeX Live)
# Produces: paper_c.tex, paper_c.pdf
# Zip for arXiv upload after build succeeds:
#   cd arxiv/paper_c && zip paper_c.zip paper_c.tex

set -euo pipefail
cd "$(dirname "$0")"

# Windows install locations (harmless if not present on macOS/Linux)
export PATH="$PATH:/c/Users/${USER:-${USERNAME:-}}/AppData/Local/Pandoc:/c/Users/${USER:-${USERNAME:-}}/AppData/Local/Programs/MiKTeX/miktex/bin/x64:/c/Program Files/Pandoc:/c/Program Files/MiKTeX/miktex/bin/x64"

command -v pandoc  > /dev/null || { echo "ERROR: pandoc not found. Install: winget install JohnMacFarlane.Pandoc" >&2; exit 1; }
command -v xelatex > /dev/null || { echo "ERROR: xelatex not found. Install MiKTeX: winget install MiKTeX.MiKTeX" >&2; exit 1; }

TITLE="Tycheism III: Alignment as Coupling Interference"
AUTHOR="Mikhail Arbuzov"

# XeLaTeX is used because the trilogy uses Greek Unicode (Τύχη).

echo "[1/3] pandoc: paper_c.md -> paper_c.tex"
pandoc paper_c.md \
  --from=markdown+tex_math_dollars+implicit_figures+pipe_tables+yaml_metadata_block \
  --to=latex \
  --standalone \
  --pdf-engine=xelatex \
  --metadata title="$TITLE" \
  --metadata author="$AUTHOR" \
  -V geometry:margin=1in \
  --output=paper_c.tex

echo "[2/3] xelatex pass 1"
xelatex -interaction=nonstopmode -halt-on-error paper_c.tex > /dev/null

echo "[3/3] xelatex pass 2 (for cross-refs)"
xelatex -interaction=nonstopmode -halt-on-error paper_c.tex > /dev/null

echo "Build complete: paper_c.pdf"
ls -la paper_c.pdf
