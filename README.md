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

### VS Code

Add as a git submodule and point `chat.agentSkillsLocations` at it:

```bash
git submodule add https://github.com/DynamoDS/skills.git .agents/dynamo-skills
```

`.vscode/settings.json`:

```json
{
  "chat.agentSkillsLocations": [".agents/dynamo-skills/skills"]
}
```

See the [VS Code skills docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills) for full details. Alternatively, symlink the `skills/` folder or copy individual skill folders into `.agents/skills/`.

### Cursor

Go to **Settings → Rules → Add Rule → Remote Rule (GitHub)** and paste:

```txt
https://github.com/DynamoDS/skills.git
```

Cursor will fetch the skills automatically. See the [Cursor skills docs](https://cursor.com/docs/skills) for full details. Alternatively, symlink the `skills/` folder to `.cursor/skills/`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
