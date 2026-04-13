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
│       └── template.md
├── dynamo-pr-description/
│   └── SKILL.md
└── dynamo-skill-writer/
    └── SKILL.md
```

## Usage

### Claude Code

This repository is a single Claude plugin (`dynamo-skills`) containing all skills. One install brings everything in.

**1. Add the marketplace (one-time setup):**

```
/plugin marketplace add DynamoDS/skills
```

**2. Install the plugin:**

```
/plugin install dynamo-skills
```

**3. Use a skill:**

Skills are available automatically based on context. You can also invoke them explicitly with a slash command:

```
/dynamo-jira-ticket
/dynamo-pr-description
/dynamo-skill-writer
```

**Updating:**

```
/plugin update dynamo-skills
```

See the [Claude skills docs](https://claude.com/docs/skills/how-to) for full details.

### GitHub Copilot

Copy individual skill folders into `.github/skills/`, `.agents/skills/`, or `.claude/skills/` for project-level access, or `~/.copilot/skills/` for personal skills shared across all projects. Copilot discovers them automatically.

In the CLI, use `/skill-name` to invoke a skill explicitly, or `/skills list` to see what's available.

See the [GitHub Copilot agent skills docs](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) for full details.

### VS Code

Copy individual skill folders directly into `.github/skills/`, `.agents/skills/`, or `.claude/skills/` — VS Code discovers those paths automatically, no settings required.

Alternatively, add this repo as a git submodule and point `chat.skillsLocations` at the `skills/` subfolder in `.vscode/settings.json`:

```bash
git submodule add https://github.com/DynamoDS/skills.git .agents/dynamo-skills
```

```json
{
  "chat.skillsLocations": [".agents/dynamo-skills/skills"]
}
```

See the [VS Code shared skills docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills#_use-shared-skills) for full details.

### Cursor

Copy individual skill folders into `.cursor/skills/` in your project, or `~/.cursor/skills/` for global (user-wide) access:

Cursor discovers skills in those paths automatically. See the [Cursor skills docs](https://cursor.com/docs/skills) for full details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
