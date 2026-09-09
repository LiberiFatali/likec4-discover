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

Verify install:

```bash
ls ~/.agents/skills/likec4-discover/scripts/discover.sh
# or: ls <your-project>/.agents/skills/likec4-discover/scripts/discover.sh
```

## Use

### Via agent (recommended)

After install, just ask your agent — no paths or flags needed. It auto-loads the skill when you ask for an architecture diagram, C4 model, likec4, code-to-diagram, or codebase overview, and runs the scripts itself.

```text
Generate a LikeC4 diagram
```

Defaults the agent applies unless you override: root = current repo (`.`), out = `./generated`, system = current directory name. Override only what you need:

```text
Generate a LikeC4 diagram for ./src as system 'shop' into ./docs/arch
Scan this repo so I can curate labels, then emit as system 'shop'
```

The agent follows `skills/likec4-discover/SKILL.md`: `scan -> label (you + agent) -> emit -> validate`. Scripts do the deterministic work; the agent only assigns names, grouping, and titles — it never hand-writes `.c4` syntax.

Note: full DSL reference comes from the `likec4-dsl` skill (`npx skills add https://likec4.dev/`). This skill is write-path only; use `@likec4/mcp` for read-path queries.

### Manually (no agent / CI)

Same scripts the agent runs. Defaults: scans current repo (`.`), outputs to `./generated`. Replace `<skill-dir>` with your installed path, e.g. `~/.agents/skills/likec4-discover`.

```bash
<skill-dir>/scripts/discover.sh scan --root . --out /tmp/ir.json
# label /tmp/ir.json -> /tmp/ir.labeled.json (see skills/likec4-discover/references/ir-schema.md)
<skill-dir>/scripts/discover.sh emit --in /tmp/ir.labeled.json --out ./generated
```

Preview either result:

```bash
npx -y likec4@1.59.3 start ./generated   # http://localhost:5173/
```

Stuck? See `skills/likec4-discover/references/troubleshooting.md`.
