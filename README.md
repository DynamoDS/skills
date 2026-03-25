# DynamoDS Shared Skills

Shared agent skills for the DynamoDS organization. These skills are the **canonical source of truth** for org-level AI-assisted development workflows that apply across multiple DynamoDS repositories.

## What are skills?

Skills are structured markdown files that guide AI coding agents (GitHub Copilot, Cursor, Claude Code, etc.) through specific tasks. Each skill lives in its own folder with a `SKILL.md` file and optional supporting assets. See the [Agent Skills specification](https://agentskills.io/specification) for the full schema.

## Skill Inventory

| Skill | Description | When to use |
|-------|-------------|-------------|
| [dynamo-jira-ticket](skills/dynamo-jira-ticket/SKILL.md) | Create structured Jira tickets | Filing bugs, feature requests, or triage |
| [dynamo-pr-description](skills/dynamo-pr-description/SKILL.md) | Generate PR descriptions | Writing or cleaning up pull request bodies |
| [dynamo-skill-writer](skills/dynamo-skill-writer/SKILL.md) | Author and maintain skills | Creating or updating skills across DynamoDS repos |

## Folder Structure

```
skills/
├── dynamo-jira-ticket/
│   ├── SKILL.md
│   └── assets/
│       └── template.md       ← Jira ticket template
├── dynamo-pr-description/
│   └── SKILL.md
└── dynamo-skill-writer/
    └── SKILL.md
```

## Usage

### Claude Code

This repository is configured as a Claude plugin marketplace. Install skills directly from Claude Code.

**Option A — Via marketplace:**

**1. Add the marketplace (one-time setup):**

```
/plugin marketplace add DynamoDS/skills
```

**2. Install individual skills:**

```
/plugin install dynamo-jira-ticket@dynamo-skills
/plugin install dynamo-pr-description@dynamo-skills
/plugin install dynamo-skill-writer@dynamo-skills
```

**3. Use a skill:**

Once installed, skills are available automatically based on context. You can also invoke them explicitly:

> "Use the dynamo-jira-ticket skill to file a bug for this error"

**Option B — Directly as a plugin** (using `.claude-plugin/plugin.json`, loads all skills without going through the marketplace):

```bash
claude --plugin-dir /path/to/dynamo/skills
```

**Updating skills:**

If installed via the marketplace:

```text
/plugin update dynamo-jira-ticket
/plugin update dynamo-pr-description
/plugin update dynamo-skill-writer
```

If loaded via `--plugin-dir` with a git submodule, pull the latest from the submodule:

```bash
git submodule update --remote /path/to/dynamo/skills
```

If loaded via `--plugin-dir` with a symlink, pull in the source repo:

```bash
cd /path/to/dynamo/skills && git pull
```

### VS Code

Choose the integration method that fits your workflow:

**Option A — Git submodule:**

```bash
git submodule add https://github.com/DynamoDS/skills.git .agents/dynamo-skills
```

Then add the submodule path to `chat.agentSkillsLocations` in `.vscode/settings.json`:

```json
{
  "chat.agentSkillsLocations": [
    ".agents/skills",
    ".agents/dynamo-skills/skills"
  ]
}
```

This appends to any existing skill locations rather than replacing them. Everyone who clones the repo gets the skills after running `git submodule update --init`.

**Option B — Symlink:**

```bash
mkdir -p .agents/skills
ln -s /path/to/dynamo-skills/skills .agents/skills
```

Changes in the source repo are reflected immediately without any sync step.

**Option C — Copy files:**

```bash
cp -r skills/dynamo-jira-ticket .agents/skills/
cp -r skills/dynamo-pr-description .agents/skills/
cp -r skills/dynamo-skill-writer .agents/skills/
```

Type `/skills` in Copilot chat to browse and enable installed skills. See the [VS Code skills docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills) for full details.

### Cursor

Choose the integration method that fits your workflow:

**Option A — Git submodule:**

```bash
git submodule add https://github.com/DynamoDS/skills.git .cursor/dynamo-skills
ln -s "$(pwd)/.cursor/dynamo-skills/skills" .cursor/skills
```

Cursor scans `.cursor/skills/` automatically — the symlink points it at the submodule contents.

**Option B — Symlink:**

```bash
ln -s /path/to/dynamo-skills/skills .cursor/skills
```

**Option C — Remote rule:**

Go to **Settings → Rules → Add Rule → Remote Rule (GitHub)** and paste:

```txt
https://github.com/DynamoDS/skills.git
```

Cursor will fetch the skills automatically. Once added, invoke a skill by typing `/` followed by its name in the Agent chat (e.g. `/dynamo-jira-ticket`). See the [Cursor skills docs](https://cursor.com/docs/skills) for full details.

## Repo-specific variants

The skills in this repository are **org-level shared skills**. Individual DynamoDS repositories may maintain their own repo-specific variants in `.agents/skills/` to tailor content to that repo's architecture, templates, and tooling.

When a repo-specific variant exists, use it. Fall back to these shared skills when no repo-specific version is available.

## Validation

Skills are validated on every pull request using [`skill-validator`](https://github.com/agent-ecosystem/skill-validator).

To validate locally:

```bash
# Install the validator
go install github.com/agent-ecosystem/skill-validator/cmd/skill-validator@latest

# Validate a single skill
skill-validator check --strict skills/dynamo-jira-ticket/

# Validate all skills
skill-validator check --strict skills/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
