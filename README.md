# DynamoDS Shared Skills

Shared agent skills for the DynamoDS organization. These skills are the **canonical source of truth** for org-level AI-assisted development workflows that apply across multiple DynamoDS repositories.

## What are skills?

Skills are structured markdown files that guide AI coding agents (GitHub Copilot, Cursor, Claude Code, etc.) through specific tasks. Each skill lives in its own folder with a `SKILL.md` file and optional supporting assets.

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

### In GitHub Copilot

Reference a skill in your agent prompt by pointing to it in this repository, or create a thin wrapper in your repo's `.github/agents/` directory that delegates to the canonical skill here.

### In Cursor

Reference skills using `@`-file mentions, e.g.:
```
@skills/dynamo-jira-ticket/SKILL.md
```

### In Claude Code

Add a reference in your repo's `CLAUDE.md` file pointing to the canonical skills in this repository.

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

1. Create a new skill directory under `skills/` with a `SKILL.md` containing the required frontmatter (`name`, `description`).
2. Run `skill-validator check --strict skills/<skill-name>/` to validate.
3. Add the skill to the inventory table in this README.
4. Open a pull request — the CI workflow will validate your skill automatically.
