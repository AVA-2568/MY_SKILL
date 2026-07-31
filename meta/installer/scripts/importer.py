#!/usr/bin/env python3
"""Skill importer — pull skills from GitHub repos or local paths into MY_SKILL.

Usage:
    python importer.py owner/repo                          # scan repo for SKILL.md
    python importer.py owner/repo/path/to/skill            # specific path in repo
    python importer.py --local /path/to/skill              # from local directory
    python importer.py owner/repo --category decision      # override category
    python importer.py owner/repo --ref develop            # use non-default branch

Pulls SKILL.md, normalizes frontmatter (ensures name/description/category/
risk_level/user-invocable all exist), copies to domain/<category>/<name>/,
and registers in INDEX.yaml. Source-agnostic: works with any repo that
follows the SKILL.md convention (obra/superpowers, mattpocock/skills, etc.).
"""

import sys, os, json, re, argparse, urllib.request, urllib.error, yaml
from pathlib import Path
from datetime import date

# MY_SKILL repo root: .../meta/installer/scripts/ → up 4 levels
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INDEX_PATH = REPO_ROOT / "meta" / "distributor" / "INDEX.yaml"
DOMAIN_ROOT = REPO_ROOT / "domain"

GITHUB_API = "https://api.github.com"
GITHUB_RAW = "https://raw.githubusercontent.com"


# ── GitHub fetch helpers ──────────────────────────────────────────────

def github_list_contents(owner, repo, path="", ref="main"):
    """List contents of a GitHub repo path via the contents API."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={ref}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "my-skill-importer",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"ERROR: path '{path}' not found in {owner}/{repo}@{ref}", file=sys.stderr)
        elif e.code == 403:
            print(f"ERROR: GitHub API rate limit hit. Wait or authenticate.", file=sys.stderr)
        else:
            print(f"ERROR: GitHub API {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)


def github_get_file(owner, repo, path, ref="main"):
    """Fetch raw file content from GitHub."""
    url = f"{GITHUB_RAW}/{owner}/{repo}/{ref}/{path}"
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"ERROR: cannot fetch {url}: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)


def find_skills_in_repo(owner, repo, subpath="", ref="main"):
    """Recursively find all SKILL.md files under a GitHub repo path."""
    results = []
    items = github_list_contents(owner, repo, subpath, ref)
    for item in items:
        if item["type"] == "file" and item["name"] == "SKILL.md":
            results.append(item["path"])
        elif item["type"] == "dir":
            results.extend(find_skills_in_repo(owner, repo, item["path"], ref))
    return results


# ── Frontmatter parsing + normalization ───────────────────────────────

def parse_frontmatter(text):
    """Parse YAML frontmatter from SKILL.md. Returns (frontmatter_dict, body_str)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
    return fm, body


def normalize_frontmatter(fm, override_category=None, override_name=None):
    """Ensure all required fields exist with sensible defaults."""
    fm.setdefault("name", override_name or "unnamed")
    fm.setdefault("description", "")
    fm.setdefault("category", override_category or "generation")
    fm.setdefault("risk_level", "low")
    fm.setdefault("user-invocable", True)
    if override_name:
        fm["name"] = override_name
    if override_category:
        fm["category"] = override_category
    return fm


# ── Install + register ────────────────────────────────────────────────

def install_skill(name, fm, body, category, source):
    """Write SKILL.md to domain/<category>/<name>/; return INDEX.yaml entry."""
    skill_dir = DOMAIN_ROOT / category / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_md = skill_dir / "SKILL.md"

    fm_text = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    content = f"---\n{fm_text}---\n\n{body}"
    skill_md.write_text(content, encoding="utf-8")

    entry = {
        "name": name,
        "category": category,
        "risk_level": fm.get("risk_level", "low"),
        "user-invocable": fm.get("user-invocable", True),
        "path": f"domain/{category}/{name}",
        "status": "imported",
        "source": source,
        "last_reviewed": str(date.today()),
    }
    return entry


def update_index(entry):
    """Add or replace a skill entry in INDEX.yaml (idempotent by name)."""
    with open(INDEX_PATH, encoding="utf-8") as f:
        index = yaml.safe_load(f)

    skills = index.get("skills", [])
    for i, s in enumerate(skills):
        if s["name"] == entry["name"]:
            skills[i] = entry
            break
    else:
        skills.append(entry)

    index["skills"] = skills
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        yaml.dump(index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ── Import entry points ───────────────────────────────────────────────

def import_from_github(spec, category=None, name=None, ref="main"):
    """Import skill(s) from 'owner/repo' or 'owner/repo/path/to/skill'."""
    parts = spec.strip("/").split("/", 2)
    owner, repo = parts[0], parts[1]
    subpath = parts[2] if len(parts) > 2 else ""
    source = f"github:{owner}/{repo}" + (f"/{subpath}" if subpath else "")

    skill_paths = find_skills_in_repo(owner, repo, subpath, ref)
    if not skill_paths:
        print(f"No SKILL.md found in {owner}/{repo}/{subpath}@{ref}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(skill_paths)} skill(s) in {owner}/{repo}:")
    for sp in skill_paths:
        print(f"  - {sp}")

    for sp in skill_paths:
        text = github_get_file(owner, repo, sp, ref)
        fm, body = parse_frontmatter(text)
        skill_name = name or fm.get("name") or Path(sp).parent.name
        fm = normalize_frontmatter(fm, category, skill_name)
        cat = fm["category"]
        entry = install_skill(skill_name, fm, body, cat, source)
        update_index(entry)
        print(f"  Imported: {skill_name} → domain/{cat}/{skill_name}/ (source: {source})")


def import_from_local(local_path, category=None, name=None):
    """Import skill(s) from a local directory."""
    p = Path(local_path).resolve()
    if not p.exists():
        print(f"ERROR: path not found: {p}", file=sys.stderr)
        sys.exit(1)

    if (p / "SKILL.md").exists():
        skill_files = [p / "SKILL.md"]
    else:
        skill_files = list(p.rglob("SKILL.md"))

    if not skill_files:
        print(f"No SKILL.md found under {p}", file=sys.stderr)
        sys.exit(1)

    source = f"local:{p}"
    print(f"Found {len(skill_files)} skill(s) locally:")
    for sf in skill_files:
        print(f"  - {sf}")

    for sf in skill_files:
        text = sf.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        skill_name = name or fm.get("name") or sf.parent.name
        fm = normalize_frontmatter(fm, category, skill_name)
        cat = fm["category"]
        entry = install_skill(skill_name, fm, body, cat, source)
        update_index(entry)
        print(f"  Imported: {skill_name} → domain/{cat}/{skill_name}/ (source: {source})")


# ── CLI ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Skill importer — pull skills from GitHub repos or local paths.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python importer.py owner/repo                  # scan repo for SKILL.md
  python importer.py owner/repo/path/to/skill    # specific path in repo
  python importer.py --local /path/to/skill      # from local directory
""",
    )
    parser.add_argument("spec", nargs="?", default=None,
                        help="GitHub spec: owner/repo or owner/repo/path/to/skill")
    parser.add_argument("--local", default=None,
                        help="Import from local directory instead of GitHub")
    parser.add_argument("--category", default=None,
                        help="Override skill category (default: from frontmatter)")
    parser.add_argument("--name", default=None,
                        help="Override skill name (default: from frontmatter)")
    parser.add_argument("--ref", default="main",
                        help="GitHub branch/tag (default: main)")
    args = parser.parse_args()

    if args.local:
        import_from_local(args.local, args.category, args.name)
    elif args.spec:
        import_from_github(args.spec, args.category, args.name, args.ref)
    else:
        parser.error("provide a GitHub spec (owner/repo) or --local <path>")


if __name__ == "__main__":
    main()
