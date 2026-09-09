# likec4-discover

[![ci](https://github.com/LiberiFatali/likec4-discover/actions/workflows/ci.yml/badge.svg)](https://github.com/LiberiFatali/likec4-discover/actions)

Agent Skill that scans a repo (TypeScript/JavaScript or Python) and generates a validated LikeC4 architecture model (`specification` + `model` + `views`). Deterministic scripts do the scanning and emitting; the agent only assigns names, grouping, and titles — it never writes DSL directly.

## Install

Global (all your projects):
```bash
mkdir -p ~/.agents/skills ~/.claude/skills
cp -r skills/likec4-discover ~/.agents/skills/
cp -r skills/likec4-discover ~/.claude/skills/
```

One project
```bash
cp -r skills/likec4-discover <your-project>/.agents/skills/   # OpenCode, Cursor, Antigravity, Codex, Copilot, VS Code
cp -r skills/likec4-discover <your-project>/.claude/skills/   # Claude Code
# or: npx skills add <this-repo-url>
```

Prereqs: `node >= 20` for TS/JS repos, `python3` for Python repos (stdlib only). For validate/preview: `npx -y likec4@1.59.3`.

## Use

One-liner (best-effort auto-labeling — raw titles, all proposals promoted):

```bash
<skill>/scripts/discover.sh quick --root <target-repo> --out ./generated --system <name>
```

Curated (label names, relationships, and proposals yourself between scan and emit):

```bash
<skill>/scripts/discover.sh scan --root <target-repo> --out /tmp/ir.json
# ...label /tmp/ir.json (see skills/likec4-discover/references/ir-schema.md)
<skill>/scripts/discover.sh emit --in /tmp/ir.labeled.json --out ./generated --system <name>  # emits + validates
```

Preview either result:

```bash
npx -y likec4@1.59.3 start ./generated   # http://localhost:5173/
```

Stuck? See `skills/likec4-discover/references/troubleshooting.md`.
