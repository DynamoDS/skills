---
name: dynamo-pr-description
description: Generate PR descriptions for DynamoDS repositories that align with the team template. Use this skill whenever writing a pull request description, cleaning up a PR body, or generating a review-ready summary from a diff in a DynamoDS repo. Also use when the user says "write a PR", "PR description", or "prep this for review."
metadata:
  version: "2026.03.20"
---

# Dynamo PR Description

## When to use

- Writing a PR description from a diff in a DynamoDS repository.
- Cleaning up or reformatting an existing PR body to match the team template.
- Producing review-ready summaries quickly.

## When not to use

- Jira ticket triage -- use the `dynamo-jira-ticket` skill instead.

## Inputs expected

A git diff, commit log, or description of the changes. Optionally a Jira key.

## Output format

A complete PR body matching the repository's PR template (`.github/PULL_REQUEST_TEMPLATE.md`), ready to paste.

---

## Workflow

1. Read the diff (staged changes, commit history, or user-provided summary).
2. Identify the *why* -- what problem does this solve?
3. Fill the repository's `.github/PULL_REQUEST_TEMPLATE.md` from the diff and context.
4. For each declaration checkbox, only check it if you've verified it's true.
5. Write the release note from the user's perspective (one sentence, or `N/A`).
6. Leave `(FILL ME IN)` placeholders for anything you can't determine from the diff.

## Rules

- Mirror section names and heading order from the template exactly.
- Keep facts verifiable from the diff. Do not invent Jira keys, reviewers, or test results.
- Call out breaking changes or migration steps explicitly in Purpose.
- If the PR changes public API, mention the affected types and whether the API surface file was updated.
- Release Notes is a **mandatory** section -- always include it, even if just `N/A`.
- If the user provides explicit checklist bullets or section content, treat those as source of truth and override the defaults below.

## PR Title

Format: `DYN-1234: concise change summary` (include Jira key when known).

## Template

Read `.github/PULL_REQUEST_TEMPLATE.md` in the target repository for the exact template structure. Follow its sections in order.

Content guidance within those sections:
- In Purpose, include a concise **"Key changes:"** bullet list when it helps readability.
- For Release Notes, write one concise sentence from the user's perspective, or `N/A` when not user-facing.

---

**Example: PR adding a new feature**

```markdown
### Purpose

DYN-5678: Add `String.Interpolate` node for string formatting with placeholders.

Key changes:
- New `StringInterpolate` method in the string utilities library
- Added to API surface file
- NUnit tests covering the new method
- Help files: `.dyn`, `.md`, `.jpg` added

### Declarations

- [x] Is documented according to the standards
- [x] The level of testing this PR includes is appropriate
- [x] Changes to the API follow Semantic Versioning and are documented in the API Changes document.

### Release Notes

Added String.Interpolate node for formatting strings with named placeholders.

### Reviewers

(FILL ME IN) Reviewer 1

### FYIs

(FILL ME IN, Optional)
```

---

**Related Skills:**
dynamo-jira-ticket
