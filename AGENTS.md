# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A single Claude Code plugin (`dynamo-skills`) containing shared agent skills for the DynamoDS org. Each skill is a self-contained folder under `skills/` with a `SKILL.md` file following the [Agent Skills spec](https://agentskills.io/specification).

## Common commands

```sh
# Build the docs site (run from repo root)
pip install -r requirements.txt
python scripts/build_site.py

# Validate a skill locally
go install github.com/agent-ecosystem/skill-validator/cmd/skill-validator@latest
skill-validator check --strict skills/<skill-name>/
```

## Architecture

### Plugin structure

- `.claude-plugin/plugin.json` — single plugin metadata; version is maintained manually here
- `.claude-plugin/marketplace.json` — one entry with `source: "./"` pointing to this repo root; no per-skill entries
- `skills/` — individual skill folders, each with a `SKILL.md`

### `scripts/build_site.py`

Reads `skills/*/SKILL.md` directly (not `marketplace.json`) and generates `docs/index.html`. Skills are the source of truth — name, description, and h1 title all come from the SKILL.md file. Run from the repo root.

### CI

- `build_site.yml` — triggers on push to master when `skills/**` or `scripts/build_site.py` changes; rebuilds `docs/index.html` and commits it back
- `validate_skills.yml` — triggers on PRs touching `skills/**`; runs `skill-validator` against only the changed skills via `.github/scripts/validate_skills.sh`

### SKILL.md frontmatter

Required: `name`, `description`. Optional: `metadata` (arbitrary map). No `keywords` or per-skill versioning — those were removed in favor of the single plugin version in `plugin.json`.
