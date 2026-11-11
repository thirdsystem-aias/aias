#!/bin/zsh
# Offline mock test of Code.gs on a packets_all.csv (r2, 2026-11-11). Usage: mock_run.sh <out_dir>
# <out_dir> is a make_packets_v1_11_paperB.py output folder. Uses macOS JavaScriptCore (jsc); no network.
set -e
HERE="${0:A:h}"
OUT="${1:A}"
TMP="$(mktemp -d)"
python3 - "$OUT/packets/packets_all.csv" "$TMP/items.json" <<'EOF'
import csv, json, sys
csv.field_size_limit(sys.maxsize)
rows = list(csv.reader(open(sys.argv[1], newline="", encoding="utf-8")))
json.dump(rows, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
print("items rows", len(rows) - 1)
EOF
{ echo "var ITEMS_JSON = '$TMP/items.json';"; cat "$HERE/mock_test.js" "$HERE/Code.gs" "$HERE/mock_driver.js"; } > "$TMP/all.js"
/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc "$TMP/all.js"
rm -rf "$TMP"
