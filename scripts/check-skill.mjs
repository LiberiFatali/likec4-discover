#!/usr/bin/env node
// check-skill.mjs — Agent Skills spec compliance + load-readiness for likec4-discover.
// Stdlib only. Usage: node scripts/check-skill.mjs [--skill <dir>]
// Covers the automatable part of the §9 test matrix (OpenCode host):
// frontmatter validity, layout, budgets, script UX, trigger keywords.
// Client-specific checks (Antigravity skill list, Claude/Cursor trigger,
// `npx skills add` discovery) remain manual — see README "Test matrix".
import { readFileSync, existsSync, statSync } from "node:fs";
import { join, basename, resolve } from "node:path";

const skillDir = resolve(process.argv.includes("--skill") ? process.argv[process.argv.indexOf("--skill") + 1] : "skills/likec4-discover");
const failures = [];
const check = (cond, msg) => { console.log(`${cond ? "ok" : "FAIL"}  ${msg}`); if (!cond) failures.push(msg); };
const mustExist = (p) => check(existsSync(join(skillDir, p)), `exists: ${p}`);

const name = basename(skillDir);
const skillMd = join(skillDir, "SKILL.md");
check(existsSync(skillMd), "exists: SKILL.md");
const body = readFileSync(skillMd, "utf8");
const fm = /^---\n([\s\S]*?)\n---\n/.exec(body);
check(!!fm, "SKILL.md has YAML frontmatter");

// --- frontmatter fields (agentskills.io: name ≤64, lowercase/digits/hyphens, matches dir) ---
const get = (k) => (new RegExp(`^${k}:\\s*(.+)$`, "m").exec(fm?.[1] || "") || [])[1]?.trim() || "";
const fname = get("name"), desc = get("description");
check(fname === name, `name matches directory (${fname || "<missing>"})`);
check(fname.length >= 1 && fname.length <= 64 && /^[a-z0-9-]+$/.test(fname) && !/^-|-$|--/.test(fname), "name charset/length valid");
check(desc.length >= 1 && desc.length <= 1024, `description 1-1024 chars (got ${desc.length})`);
for (const kw of ["architecture diagram", "C4", "likec4", "code-to-diagram", "codebase overview"]) {
  check(desc.toLowerCase().includes(kw.toLowerCase()), `trigger keyword in description: "${kw}"`);
}
check(get("license").length > 0, "license field present");
check(existsSync("LICENSE"), "LICENSE file present (matches license: MIT)");

// --- budgets: plan bar <350 lines; spec guidance <500 lines / <5000 tokens ---
const lines = body.split("\n").length;
const tokens = Math.ceil(body.length / 4); // ~4 chars/token heuristic
check(lines < 350, `SKILL.md ${lines} lines < 350`);
check(tokens < 5000, `SKILL.md ~${tokens} tokens < 5000`);

// --- layout ---
for (const p of ["scripts/scan.mjs", "scripts/scan.py", "scripts/emit.mjs", "scripts/discover.sh",
  "references/ir-schema.md", "references/dsl-min.md", "references/validation.md",
  "references/troubleshooting.md", "assets/templates/spec.c4", "assets/templates/model.c4",
  "assets/templates/views.c4"]) mustExist(p);
for (const p of ["scripts/scan.mjs", "scripts/scan.py", "scripts/emit.mjs", "scripts/discover.sh"]) {
  try { check((statSync(join(skillDir, p)).mode & 0o111) !== 0, `executable: ${p}`); }
  catch { check(false, `executable: ${p}`); }
}

if (failures.length) { console.error(`\ncheck-skill: ${failures.length} FAILURE(S)`); process.exit(1); }
console.log("\ncheck-skill: all local matrix checks passed");
console.log("manual (per plan §9): Antigravity skill list, Claude/Cursor trigger phrase, `npx skills add <repo>`");
