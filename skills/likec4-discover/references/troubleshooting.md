# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `1api` / `a.pi` rejected | identifier starts with digit / contains dot | sanitize to `_1api` / nest as `a.pi` FQN levels |
| duplicate FQN error from `emit.mjs` | two files map to same `<system>.<area>.<Name>` | rename title or split areas; emit dedupes with `_2` suffix + warning |
| `order` (or style/keyword) rejected as identifier | LikeC4 reserved word in identifier position | `emit.mjs` auto-renames to `order_`; keep the rename, don't fight it |
| `kind X not defined` | invented kind | declare in `spec.c4` or map to actor/system/container/component |
| parent-child `->` error | `cloud -> cloud.api` | remove; hierarchy already expresses containment |
| `include *` shows only top level | expected for unscoped views | add scoped `view of <system>` (emitted by default) |
| `scan.py failed` in scan output | bad Python syntax / missing python3 | fix file or install `python3`; TS/JS side still completes |
| over budget (>200 elements) | large repo | narrow `--include`, add `--exclude`, or confirm raising the cap |
| `valid: false` with layout errors | layout drift, not semantic | re-run with `--no-layout` for the semantic gate |
