# likec4-discover

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

```bash
# 1. Scan the target repo -> IR
node <skill>/scripts/scan.mjs --root <target-repo> --out /tmp/ir.json

# 2. Label: assign FQNs, titles, wire relationships, promote/drop proposals
#    (see skills/likec4-discover/references/ir-schema.md) -> /tmp/ir.labeled.json

# 3. Emit the model
node <skill>/scripts/emit.mjs --in /tmp/ir.labeled.json --out ./generated --system <name>

# 4. Validate (gate: valid == true, filteredErrors == 0)
npx -y likec4@1.59.3 validate --no-layout --json ./generated

# 5. Preview at http://localhost:5173/
npx -y likec4@1.59.3 start ./generated
```

Stuck? See `skills/likec4-discover/references/troubleshooting.md`.
