---
name: dynamo-skill-writer
description: Author and maintain agent skills for DynamoDS repositories. Use this skill when creating a new skill, updating an existing skill, or ensuring skill content is consistent and well-structured across DynamoDS repos.
---

# Dynamo Skill Writer

## When to use

- Creating a new skill in a DynamoDS repository.
- Updating an existing skill and ensuring tool surfaces remain aligned.
- Auditing skills for quality, broken links, or outdated content.
- Adding skills to the shared `DynamoDS/skills` repository.

## When not to use

- Writing product code, tests, or architecture docs unrelated to agent skills.
- One-off prompt output where no canonical skill should be created.

## Inputs expected

A request to add/update a skill, or a request to sync skill surfaces across Copilot/Cursor/Claude.

## Output format

A concrete set of file edits and validation steps that:
- Create or update canonical skill content in the appropriate `skills/` directory
- Update documentation references in `README.md` or equivalent index files
- Pass `skill-validator check --strict` validation

---

## Workflow

1. Determine whether this is a **new skill** or an **update to an existing skill**.
2. For shared/org-level skills: author or update content in `DynamoDS/skills` repo under `skills/<skill-name>/SKILL.md`.
3. For repo-specific skills: author or update content in `.agents/skills/<skill-name>/SKILL.md` within the target repo.
4. Validate with `skill-validator check --strict <skill-path>`.
5. Update discovery docs when the skill inventory changes (e.g., `README.md` index tables).
6. If Copilot agent wrappers exist, regenerate them after updating canonical skills.

## Rules

- The canonical `skills/` directory (whether in `DynamoDS/skills` or a repo's `.agents/skills/`) is the source of truth for skill logic.
- Generated wrappers (e.g., in `.github/agents/`) must not be hand-edited.
- Skill metadata (`name`/`description`) should be concise and stable.
- If mirrors conflict with canonical files, canonical files win.
- Keep changes deterministic so CI validation stays reliable.

## New Skill Checklist

- [ ] Created `skills/<skill-name>/SKILL.md` with frontmatter (`name`, `description`)
- [ ] Added skill to `README.md` inventory table
- [ ] Validated with `skill-validator check --strict skills/<skill-name>/`
- [ ] Updated any Copilot wrapper maps if the skill is surfaced through Copilot agents
- [ ] Regenerated Copilot agent wrappers if applicable

## Naming guidance

- Canonical skill id: kebab-case (example: `dynamo-skill-writer`)
- Copilot wrapper agent name: title case (example: `Dynamo Skill Writer`)

## Skill Structure

Each skill lives in its own folder:

```
skills/
└── my-skill/
    ├── SKILL.md          ← required, contains frontmatter + instructions
    ├── assets/           ← optional, templates and supporting content
    │   └── template.md
    └── references/       ← optional, reference docs (quality guides, checklists)
        └── guide.md
```

## Frontmatter format

```yaml
---
name: skill-name
description: One or two sentences. First sentence is the core trigger phrase. Second sentence lists alternate trigger phrases starting with "Also use when…"
---
```

## Validation

Install the skill validator:
```bash
go install github.com/agent-ecosystem/skill-validator/cmd/skill-validator@latest
```

Run checks:
```bash
# Validate a single skill
skill-validator check --strict skills/my-skill/

# Validate all skills in the repo
skill-validator check --strict skills/
```

---

**Related Skills:**
dynamo-jira-ticket • dynamo-pr-description
