#!/usr/bin/env python3
"""Sync .claude-plugin/marketplace.json from skills/ directory.

For each skill directory containing a SKILL.md, updates the marketplace entry
with name, source, version, and description read from frontmatter. Existing
category and keywords are preserved; new entries default to empty strings/lists.
Skills removed from the skills/ directory are removed from the manifest.
"""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}


def main():
    manifest = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    existing = {p["name"]: p for p in manifest.get("plugins", [])}

    updated = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        fm = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        if not fm:
            print(f"warning: no frontmatter in {skill_file}, skipping", file=sys.stderr)
            continue

        name = fm.get("name", skill_dir.name)
        version = str((fm.get("metadata") or {}).get("version", ""))
        description = fm.get("description", "")
        prev = existing.get(name, {})

        updated.append({
            "name": name,
            "source": f"./skills/{skill_dir.name}",
            "version": version,
            "description": description,
            "category": prev.get("category", ""),
            "keywords": prev.get("keywords", []),
        })

    removed = set(existing) - {p["name"] for p in updated}
    for name in removed:
        print(f"removed: {name}")

    manifest["plugins"] = updated
    MARKETPLACE.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"updated {MARKETPLACE} with {len(updated)} plugin(s): {[p['name'] for p in updated]}")


if __name__ == "__main__":
    main()
