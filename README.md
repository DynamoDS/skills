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

## How to use these skills

### In VS Code (GitHub Copilot)

Copy the skill directories you need into your repo's `.agents/skills/` or `.github/skills/` folder (or any path configured in `chat.agentSkillsLocations`):

```bash
cp -r skills/dynamo-jira-ticket .agents/skills/
cp -r skills/dynamo-pr-description .agents/skills/
cp -r skills/dynamo-skill-writer .agents/skills/
```

Or add a custom location in `.vscode/settings.json`:

```json
{
  "chat.agentSkillsLocations": ["path/to/skills"]
}
```

Type `/skills` in Copilot chat to browse and enable installed skills. See the [VS Code skills docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills) for full details.

### In Cursor

Copy the skill directories you need into your repo's `.agents/skills/` or `.cursor/skills/` folder:

```bash
cp -r skills/dynamo-jira-ticket .agents/skills/
cp -r skills/dynamo-pr-description .agents/skills/
cp -r skills/dynamo-skill-writer .agents/skills/
```

Or go to **Settings → Rules → Add Rule → Remote Rule (GitHub)** and paste the repository URL:

```
https://github.com/DynamoDS/skills.git
```

Cursor will fetch the skills automatically. Once added, invoke a skill by typing `/` followed by its name in the Agent chat (e.g. `/dynamo-jira-ticket`). See the [Cursor skills docs](https://cursor.com/docs/skills) for full details.

### In Claude Code

This repository is registered as a Claude plugin marketplace. You can browse and install skills directly from Claude Code.

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

Or browse interactively:

```
/plugin marketplace browse dynamo-skills
```

**3. Use a skill:**

Once installed, skills are available automatically based on context. You can also invoke them explicitly:

> "Use the dynamo-jira-ticket skill to file a bug for this error"

**Updating skills:**

```text
/plugin update dynamo-jira-ticket
```

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

1. Create a new skill directory under `skills/` with a `SKILL.md` containing the required frontmatter (`name`, `description`). Refer to the [Agent Skills specification](https://agentskills.io/specification) for all supported fields.
2. Run `skill-validator check --strict skills/<skill-name>/` to validate.
3. Add the skill to the inventory table in this README.
4. Open a pull request — the CI workflow will validate your skill automatically.
