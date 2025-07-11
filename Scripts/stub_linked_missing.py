import re
from pathlib import Path
import os

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((?!http)([^)#]+)(#[^\)]*)?\)")

def find_markdown_files():
    return list(DOCS.rglob("*.md"))

def extract_links(md_path):
    links = set()
    with md_path.open("r", encoding="utf-8") as f:
        for line in f:
            for match in LINK_PATTERN.finditer(line):
                href = match[2].strip().split("#")[0]
                if href.endswith(".md"):
                    links.add(href)
    return links

def resolve_target(link, src_path):
    target_path = (src_path.parent / link).resolve()
    try:
        return target_path.relative_to(DOCS)
    except ValueError:
        return None

def stub_file(rel_path):
    abs_path = DOCS / rel_path
    os.makedirs(abs_path.parent, exist_ok=True)
    title = abs_path.stem.replace("_", " ").title()
    content = f"# {title}\n\n_This page was autogenerated to resolve a broken link._\n\n- Content coming soon\n- Placeholder for context\n"
    abs_path.write_text(content, encoding="utf-8")
    print(f"🧩 Stub created: {rel_path}")

def run():
    print("🔎 Scanning for broken internal links and stubbing missing targets...\n")
    existing = {f.relative_to(DOCS).as_posix() for f in find_markdown_files()}
    all_targets = set()

    for md in find_markdown_files():
        rel_src = md.relative_to(DOCS)
        links = extract_links(md)
        for link in links:
            resolved = resolve_target(link, md)
            if resolved:
                rel_posix = resolved.as_posix()
                all_targets.add(rel_posix)

    missing = sorted(set(all_targets) - existing)

    if missing:
        print(f"⚠️ Found {len(missing)} missing target files. Creating stubs...\n")
        for rel in missing:
            stub_file(Path(rel))
    else:
        print("✅ No missing internal links detected.")

if __name__ == "__main__":
    run()
