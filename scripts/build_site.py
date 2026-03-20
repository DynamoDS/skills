#!/usr/bin/env python3
"""
Build docs/index.html from skills/*/SKILL.md frontmatter.
Run from the repository root.
"""

import re
import yaml
from pathlib import Path

ICONS = {
    "jira":  '<i class="fa-brands fa-jira"></i>',
    "pr":    '<i class="fa-solid fa-code-pull-request"></i>',
    "skill": '<i class="fa-solid fa-wand-magic-sparkles"></i>',
}
DEFAULT_ICON = '<i class="fa-solid fa-circle-info"></i>'

SKILL_CARD_TEMPLATE = """\
<div class="skill-card">
  <div class="skill-card-body">
    <div class="skill-icon">__SKILL_ICON__</div>
    <div class="skill-name">__SKILL_SLUG__</div>
    <h3>__SKILL_TITLE__</h3>
    <div class="skill-version">v__SKILL_VERSION__</div>
    <p>__SKILL_DESC__</p>
  </div>
  <div class="code-wrap">
    <div class="code-block">/plugin install __SKILL_SLUG__@dynamo-skills</div>
    <button class="copy-btn" aria-label="Copy"><i class="fa-regular fa-copy"></i></button>
  </div>
</div>
"""

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>DynamoDS Shared Skills</title>
  <link rel="icon" type="image/png" href="images/logo_32.png" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0d0d0d;
      --surface: #141414;
      --border: #222;
      --text: #e8e8e8;
      --muted: #888;
      --accent: #4c9bff;
      --accent-dim: rgba(76, 155, 255, 0.12);
      --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --mono: "SF Mono", "Fira Code", "Cascadia Code", Menlo, monospace;
    }

    body {
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
    }

    nav {
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(13, 13, 13, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 0 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 56px;
    }

    .nav-logo {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: var(--text);
      font-size: 0.9rem;
      font-weight: 500;
    }

    .nav-logo img { width: 24px; height: 24px; }

    nav a.gh-link {
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--muted);
      text-decoration: none;
      font-size: 0.85rem;
      transition: color 0.15s;
    }

    nav a.gh-link:hover { color: var(--text); }
    nav a.gh-link i { font-size: 18px; }

    .hero {
      max-width: 960px;
      margin: 0 auto;
      padding: 48px 2rem 40px;
      text-align: center;
    }

    .hero img {
      width: 48px;
      height: 48px;
      margin-bottom: 16px;
      opacity: 0.95;
    }

    .hero h1 {
      font-size: clamp(1.5rem, 3vw, 2rem);
      font-weight: 600;
      letter-spacing: -0.02em;
      line-height: 1.2;
      margin-bottom: 20px;
    }

    .hero h1 span { color: var(--accent); }

    .badge-row {
      display: flex;
      gap: 8px;
      justify-content: center;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 0.75rem;
      border: 1px solid var(--border);
      color: var(--muted);
      background: var(--surface);
    }

    .cta-row {
      display: flex;
      gap: 12px;
      justify-content: center;
      flex-wrap: wrap;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 10px 20px;
      border-radius: 8px;
      font-size: 0.875rem;
      font-weight: 500;
      text-decoration: none;
      transition: all 0.15s;
      border: none;
    }

    .btn-primary { background: var(--accent); color: #fff; }
    .btn-primary:hover { background: #6aadff; }
    .btn-secondary { background: var(--surface); color: var(--text); border: 1px solid var(--border); }
    .btn-secondary:hover { border-color: #444; background: #1c1c1c; }

    section {
      max-width: 1100px;
      margin: 0 auto;
      padding: 0 2rem 80px;
    }

    .section-label {
      font-size: 0.7rem;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 10px;
    }

    section h2 {
      font-size: 1.5rem;
      font-weight: 600;
      letter-spacing: -0.01em;
      margin-bottom: 8px;
    }

    section > p {
      color: var(--muted);
      font-size: 0.95rem;
      margin-bottom: 32px;
    }

    .skills-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 16px;
    }

    .skill-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      transition: border-color 0.15s;
      display: flex;
      flex-direction: column;
    }

    .skill-card:hover { border-color: #333; }

    .skill-card-body { flex: 1; }

    .skill-icon {
      width: 38px;
      height: 38px;
      border-radius: 8px;
      background: var(--accent-dim);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 14px;
    }

    .skill-icon i { font-size: 18px; color: var(--accent); }

    .skill-name {
      font-size: 0.8rem;
      font-family: var(--mono);
      color: var(--accent);
      margin-bottom: 6px;
    }

    .skill-card h3 {
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 8px;
    }

    .skill-version {
      font-size: 0.72rem;
      font-family: var(--mono);
      color: var(--muted);
      margin-bottom: 8px;
    }

    .skill-card p {
      font-size: 0.875rem;
      color: var(--muted);
      line-height: 1.55;
      margin-bottom: 16px;
    }

    .code-block {
      background: #0a0a0a;
      border: 1px solid #1e1e1e;
      border-radius: 8px;
      padding: 12px 14px;
      font-family: var(--mono);
      font-size: 0.8rem;
      color: #cdd6f4;
      overflow-x: auto;
      white-space: pre;
    }

    .skill-card .code-block {
      white-space: pre-wrap;
      word-break: break-all;
      overflow-x: hidden;
    }

    .other-ides {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(460px, 1fr));
      gap: 16px;
    }

    .ide-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px 24px;
    }

    .ide-card h3 {
      font-size: 0.9rem;
      font-weight: 600;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .ide-card h3 i { color: var(--muted); }

    .ide-card p {
      font-size: 0.875rem;
      color: var(--muted);
      line-height: 1.55;
      margin-bottom: 12px;
    }

    .ide-card p:last-child { margin-bottom: 0; }

    hr { border: none; border-top: 1px solid var(--border); margin: 0 2rem; }

    footer {
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 2rem 48px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }

    footer p { font-size: 0.82rem; color: var(--muted); }
    footer a { color: var(--muted); text-decoration: none; }
    footer a:hover { color: var(--text); }

    .code-wrap { position: relative; }
    .copy-btn {
      position: absolute; top: 8px; right: 8px;
      background: transparent; border: 1px solid #2e2e2e;
      border-radius: 6px; padding: 4px 6px;
      cursor: pointer; color: var(--muted); transition: all 0.15s;
      line-height: 0;
    }
    .copy-btn:hover { color: var(--text); border-color: #444; }
    .copy-btn i { font-size: 13px; }
    .copy-btn.copied { color: #3fb950; border-color: #3fb950; }

    @media (max-width: 600px) {
      .hero { padding: 32px 1.25rem 28px; }
      section { padding: 0 1.25rem 60px; }
      nav { padding: 0 1.25rem; }
      footer { padding: 28px 1.25rem 40px; }
      hr { margin: 0 1.25rem; }
    }
  </style>
</head>
<body>

<nav>
  <a class="nav-logo" href="#">
    <img src="images/logo_32.png" alt="Dynamo" />
    DynamoDS / skills
  </a>
  <a class="gh-link" href="https://github.com/DynamoDS/skills" target="_blank" rel="noopener">
    <i class="fa-brands fa-github"></i>
    GitHub
  </a>
</nav>

<div class="hero">
  <img src="images/logo.png" alt="Dynamo logo" />
  <h1>Shared <span>Agent Skills</span> for DynamoDS</h1>
  <div class="badge-row">
    <span class="badge">__SKILL_COUNT__ Skills</span>
  </div>
  <div class="cta-row">
    <a class="btn btn-primary" href="https://github.com/DynamoDS/skills" target="_blank" rel="noopener">
      <i class="fa-brands fa-github"></i>
      View on GitHub
    </a>
    <a class="btn btn-secondary" href="https://github.com/DynamoDS/skills/tree/master/skills" target="_blank" rel="noopener">
      Browse Skills
    </a>
  </div>
</div>

<hr />

<section style="padding-top: 64px;">
  <div class="section-label">Skills</div>
  <h2>Introduction</h2>
  <p>Agent Skills are a simple, open format for giving agents new capabilities and expertise. Each skill is a self-contained folder of instructions and resources that agents can discover and use — write once, use everywhere. <a href="https://agentskills.io/home" target="_blank" rel="noopener" style="color: var(--accent); text-decoration: none;">Learn more →</a></p>
  <div style="margin-bottom: 32px;">
    <div class="section-label">Get started</div>
    <h2 style="font-size: 1.2rem; margin-bottom: 8px;">Install as a Claude plugin</h2>
    <p style="color: var(--muted); font-size: 0.95rem; margin-bottom: 16px;">Register the DynamoDS skills repo once, then install any skill on demand.</p>
    <div class="code-wrap">
      <div class="code-block">/plugin add dynamo-skills https://github.com/DynamoDS/skills</div>
      <button class="copy-btn" aria-label="Copy"><i class="fa-regular fa-copy"></i></button>
    </div>
  </div>
  <div class="skills-grid">
__SKILL_CARDS__
  </div>
  <div style="margin-top: 32px;">
    <h2 style="font-size: 1.2rem; margin-bottom: 8px;">Other IDEs</h2>
    <p style="color: var(--muted); font-size: 0.95rem; margin-bottom: 16px;">Skills follow the <a href="https://agentskills.io/specification" target="_blank" rel="noopener" style="color: var(--accent); text-decoration: none;">agentskills.io</a> open spec and work with any agent-aware IDE.</p>
    <div class="other-ides">
      <div class="ide-card">
        <h3><i class="fa-brands fa-microsoft"></i> VS Code + Copilot</h3>
        <p>Copy any skill folder into your workspace:</p>
        <div class="code-wrap">
          <div class="code-block">cp -r skills/&lt;skill-name&gt; .github/agents/skills/</div>
          <button class="copy-btn" aria-label="Copy"><i class="fa-regular fa-copy"></i></button>
        </div>
        <p style="margin-top: 10px;">Copilot will pick up the skill automatically when you open an agent session. <a href="https://code.visualstudio.com/docs/copilot/customization/agent-skills" target="_blank" rel="noopener" style="color: var(--accent); text-decoration: none;">Learn more →</a></p>
      </div>
      <div class="ide-card">
        <h3><i class="fa-solid fa-arrow-pointer"></i> Cursor</h3>
        <p>Add as a remote rule in <strong>Cursor Settings → Rules for AI</strong>:</p>
        <div class="code-wrap">
          <div class="code-block">https://github.com/DynamoDS/skills.git</div>
          <button class="copy-btn" aria-label="Copy"><i class="fa-regular fa-copy"></i></button>
        </div>
        <p style="margin-top: 10px;"><a href="https://cursor.com/docs/skills" target="_blank" rel="noopener" style="color: var(--accent); text-decoration: none;">Learn more →</a></p>
      </div>
    </div>
  </div>
</section>

<hr />

<footer>
  <p>Built by <a href="https://github.com/DynamoDS" target="_blank" rel="noopener">DynamoDS</a></p>
</footer>

<script>
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const text = btn.closest('.code-wrap').querySelector('.code-block').textContent.trim();
    navigator.clipboard.writeText(text).then(() => {
      btn.classList.add('copied');
      btn.innerHTML = '<i class="fa-solid fa-check"></i>';
      setTimeout(() => {
        btn.classList.remove('copied');
        btn.innerHTML = '<i class="fa-regular fa-copy"></i>';
      }, 2000);
    });
  });
});
</script>
</body>
</html>
"""


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\s*(.*)", text, re.DOTALL)
    if not m:
        return {}, None
    fm = yaml.safe_load(m.group(1)) or {}
    h1 = re.search(r"^# (.+)", m.group(2), re.MULTILINE)
    return fm, h1.group(1).strip() if h1 else None


def human_name(slug):
    return " ".join(p.capitalize() for p in slug.split("-"))


def pick_icon(name):
    name_lower = name.lower()
    for key in ICONS:
        if key in name_lower:
            return key
    return "default"


def short_desc(description, limit=130):
    first = description.split(".")[0]
    return (first + ".") if len(first) <= limit else description[:limit].rstrip() + "\u2026"


def skill_card(skill):
    icon = ICONS.get(skill["icon_key"], DEFAULT_ICON)
    return (
        SKILL_CARD_TEMPLATE
        .replace("__SKILL_ICON__", icon)
        .replace("__SKILL_SLUG__", skill["slug"])
        .replace("__SKILL_TITLE__", skill["title"])
        .replace("__SKILL_VERSION__", skill["version"])
        .replace("__SKILL_DESC__", skill["description"])
    )


def build_html(skills):
    skill_cards_html = "\n".join(skill_card(s) for s in skills)
    skill_count = len(skills)
    return (
        TEMPLATE
        .replace("__SKILL_COUNT__", str(skill_count))
        .replace("__SKILL_CARDS__", skill_cards_html)
    )


skills = []
for skill_dir in sorted(Path("skills").iterdir()):
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        continue
    fm, h1 = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
    if not fm:
        continue
    slug = fm.get("name", skill_dir.name)
    skills.append({
        "slug": slug,
        "title": h1 or human_name(slug),
        "description": short_desc(fm.get("description", "")),
        "version": str((fm.get("metadata") or {}).get("version", "")),
        "icon_key": pick_icon(slug),
    })

out = Path("docs/index.html")
out.parent.mkdir(exist_ok=True)
out.write_text(build_html(skills), encoding="utf-8")
print(f"Built {out} with {len(skills)} skill(s): {[s['slug'] for s in skills]}")
