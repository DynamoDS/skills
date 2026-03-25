# Contributing

## Skill format

Skills follow the [Agent Skills specification](https://agentskills.io/specification). A skill is a directory containing at minimum a `SKILL.md` file:

```
skills/
  dynamo-my-skill/
    SKILL.md
    scripts/       # optional: executable code
    references/    # optional: additional docs loaded on demand
    assets/        # optional: templates, data files
    ...            # Any additional files or directories
```

### `SKILL.md` frontmatter

| Field           | Required | Notes |
|-----------------|----------|-------|
| `name`          | Yes      | Lowercase letters, numbers, hyphens only. Max 64 chars. Must match the folder name. |
| `description`   | Yes      | What the skill does and when to use it. Max 1024 chars. Be specific — agents use this to decide when to activate the skill. |
| `metadata`      | No       | Arbitrary key-value map. We use `version: "YYYY.MM.DD"`. |
| `license`       | No       | License name or reference to a bundled license file. |
| `compatibility` | No       | Environment requirements (OS packages, network access, etc.). Omit if not needed. |
| `allowed-tools` | No       | Space-delimited list of pre-approved tools (experimental). |

Minimal example:

```markdown
---
name: dynamo-my-skill
description: One or two sentences describing what this skill does and when to use it.
metadata:
  version: "2026.03.20"
---

# My Skill Title

## When to use
...
```

### Body content

There are no format restrictions on the body. Recommended sections:

- **When to use / When not to use** — helps agents decide when to activate the skill
- **Step-by-step instructions**
- **Examples** of inputs and outputs
- **Edge cases**

Keep `SKILL.md` under 500 lines. Move detailed reference material to `references/` — those files are only loaded on demand.

## Validating skills

Skills are validated automatically on pull requests. To run validation locally, install the validator and run it against your skill directory:

```sh
go install github.com/agent-ecosystem/skill-validator/cmd/skill-validator@latest
skill-validator check --strict skills/dynamo-my-skill/
```

## Updating the marketplace manifest

`.claude-plugin/marketplace.json` is synced automatically on push, but you can also run it locally:

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python scripts/update_claude_manifest.py
```

Add keywords in [marketplace.json](.claude-plugin/marketplace.json) manually.

The script reads each `skills/*/SKILL.md` and updates `name`, `source`, `version`, and `description` in the manifest. Existing `category` and `keywords` values are preserved. Skills no longer present in `skills/` are removed.

## Building the doc site

The site at `docs/index.html` is generated from `.claude-plugin/marketplace.json`. Run both scripts in order:

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python scripts/update_claude_manifest.py
python scripts/build_site.py
```

Open `docs/index.html` in a browser to preview. Both scripts run automatically on push via the `Build site` GitHub Actions workflow whenever `skills/**/SKILL.md` or `scripts/build_site.py` changes, and any updates to `docs/index.html` and `.claude-plugin/marketplace.json` are committed back automatically.

## Pull request checklist

- [ ] Skill added to the inventory table in `README.md`
- [ ] Skill folder name matches the `name` field in `SKILL.md`
- [ ] `name` uses only lowercase letters, numbers, and hyphens (no consecutive hyphens)
- [ ] `description` clearly states what the skill does and when to use it
- [ ] `metadata.version` is set and up to date
- [ ] `skill-validator check --strict` passes locally
- [ ] `update_claude_manifest.py` run locally to update (or let CI handle it on merge)
- [ ] `build_site.py` run locally (or let CI handle it on merge)
