#!/bin/bash
# Third System — build_report.sh
# Renders a Markdown report to PDF using thirdsystem.tex template + xelatex

set -e

INPUT="${1:-report_v0.6_cross.md}"
OUTPUT="${INPUT%.md}.pdf"

echo "Rendering $INPUT -> $OUTPUT"

pandoc "$INPUT" \
  --template=thirdsystem.tex \
  --pdf-engine=xelatex \
  -o "$OUTPUT"

echo "Done: $OUTPUT"
