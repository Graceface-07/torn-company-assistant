# -*- coding: utf-8 -*-
import os
from pathlib import Path

# Handle stdout encoding on Windows
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Map of bad characters to replacements
sanitizers = {
    "â€œ": "\"",
    "â€": "\"",
    "â€˜": "'",
    "â€™": "'",
    "â€“": "-",
    "â€”": "—",
    "â€¦": "...",
    "â€": '"',
    "ðŸ‘‰": "→",
    "ðŸ”ˆ": "📈",
    "Ã—": "×",
}

def sanitize_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content
    for bad, good in sanitizers.items():
        content = content.replace(bad, good)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[CLEANED] {path.relative_to(ROOT)}")

def run():
    print("[*] Scanning markdown files for encoding issues...\n")
    for file in DOCS.rglob("*.md"):
        sanitize_file(file)
    print("\n✅ Emoji and encoding cleanup complete.")

if __name__ == "__main__":
    run()
