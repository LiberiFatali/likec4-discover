# DSL minimum (LikeC4 v1.59.3, condensed — full ref is `likec4-dsl` skill)

- Top-level blocks: `specification {}`, `model {}`, `views {}` (each file needs ≥1; all sources merge).
- `specification` declares every kind/tag used: `element <id>`, `relationship <id>`, `tag <id>` (no `#` in declaration; `#id` at use).
- Element identifier: letters/digits/`-`/`_`, must not start with digit, no dots. Dots separate FQN nesting only.
- Element: `<name> = <kind> '<Title>' { #tag technology '...' description '...' }`. Nested blocks create FQN `a.b.c`. Arbitrary nesting depth allowed.
- Relationships: `a -> b` or typed `a -[kind]-> b 'label'` with optional kind/label. Never parent-child (`cloud -> cloud.api` is invalid).
- Evidence comments (`// evidence: file:line`) are plain comments, always safe.
- Views: `view <id> { include * }`, scoped `view <id> of <fqn> { include * }`. `index` is the default view. Rules apply in order; `exclude` only removes already-included items.
- This skill emits: `spec.c4` (person/system/container/component/database + http/kafka/s3/promql/inproc/calls/imports/inherits), `model.c4` (nested system→container→file→symbols with `// evidence:` comments, typed edges), `views.c4` (`index` + one per system, titled, `autoLayout LeftRight`). Provenance is a file header comment, never element tags.
