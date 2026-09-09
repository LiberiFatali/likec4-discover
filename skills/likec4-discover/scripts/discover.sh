#!/usr/bin/env bash
# discover.sh — one entry point for likec4-discover.
#   discover.sh scan --root <repo> --out /tmp/ir.json [--exclude docs ...]
#   discover.sh emit --in /tmp/ir.labeled.json --out ./generated --system <name>
#   discover.sh quick --root <repo> --out ./generated --system <name> [--exclude ...]
#     one-liner: scan -> best-effort auto-label -> emit -> validate.
#     Titles are raw and all proposals are promoted; for curated diagrams,
#     run scan/emit separately with manual labeling in between.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SKILL="$(cd "$HERE/.." && pwd)"

cmd="${1:-}"; shift || true
case "$cmd" in
  scan)
    node "$SKILL/scripts/scan.mjs" "$@"
    ;;
  emit)
    IN=""; OUT=""; SYSTEM="cloud"; REST=()
    while [ $# -gt 0 ]; do
      case "$1" in
        --in) IN="$2"; shift 2;;
        --out) OUT="$2"; shift 2;;
        --system) SYSTEM="$2"; shift 2;;
        *) REST+=("$1"); shift;;
      esac
    done
    node "$SKILL/scripts/emit.mjs" --in "$IN" --out "$OUT" --system "$SYSTEM" --check "${REST[@]}"
    if command -v likec4 >/dev/null 2>&1 || command -v npx >/dev/null 2>&1; then
      npx -y likec4@1.59.3 validate --no-layout --json "$OUT" | tee "$OUT/.validate.json" | \
        node -e "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{const r=JSON.parse(s);if(!r.valid||r.stats.filteredErrors!==0){console.error('VALIDATION FAILED');process.exit(1)}console.log('validate: OK (filteredErrors=0)')})"
    else
      echo "discover.sh: likec4 CLI not found, skipping validate (emit self-check only)" >&2
    fi
    ;;
  -h|--help|help|"")
    sed -n '2,9p' "$0"
    ;;
  quick)
    ROOT=""; OUT=""; SYSTEM="cloud"; REST=()
    while [ $# -gt 0 ]; do
      case "$1" in
        --root) ROOT="$2"; shift 2;;
        --out) OUT="$2"; shift 2;;
        --system) SYSTEM="$2"; shift 2;;
        *) REST+=("$1"); shift;;
      esac
    done
    if [ -z "$ROOT" ] || [ -z "$OUT" ]; then echo "quick: --root and --out required" >&2; exit 2; fi
    TMP_IR="$(mktemp /tmp/discover-ir.XXXXXX.json)"
    TMP_LABELED="$(mktemp /tmp/discover-labeled.XXXXXX.json)"
    trap 'rm -f "$TMP_IR" "$TMP_LABELED"' EXIT
    node "$SKILL/scripts/scan.mjs" --root "$ROOT" --out "$TMP_IR" "${REST[@]}"
    node "$SKILL/scripts/auto-label.mjs" --in "$TMP_IR" --out "$TMP_LABELED" --system "$SYSTEM"
    "$0" emit --in "$TMP_LABELED" --out "$OUT" --system "$SYSTEM"
    ;;
  *)
    echo "unknown command: $cmd (try: scan, emit, quick)" >&2; exit 2;;
esac
