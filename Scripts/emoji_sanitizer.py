import os
from pathlib import Path
import re

DOCS = Path(__file__).parent.parent / "docs"

# Common mojibake replacements
REPLACEMENTS = {
    "â†‘": "↑",
    "â†“": "↓",
    "â†’": "→",
    "â€“": "–",
    "â€”": "—",
    "â€˜": "‘",
    "â€™": "’",
    "â€œ": "“",
    "â€": "”",
    "â€¢": "•",
    "â€" : "-",   # hyphen fallback
    "âŒ": "✖",
    "âœ¨": "✨",
    "ðŸŽ¯": "🎯",
    "ðŸ§ ": "🧠",
    "ðŸ”": "🔍",
    "ðŸ'¡": "💡",
    "ðŸ""": "🎯",  # malformed again
    "ðŸŽ'": "📊",
    "ðŸ¢": "🏢",
    "ðŸ§'â€ðŸ¤â€ðŸ§'": "👨‍💼‍🤝‍👨",
    "ðŸ"ˆ": "📈",
    "ðŸ"—": "🛠",
    "ðŸ": "🏁",
}

def clean_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    for wrong, right in REPLACEMENTS.items():
        content = content.replace(wrong, right)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Cleaned: {path.relative_to(DOCS)}")

def run():
    for f in DOCS.rglob("*.md"):
        clean_file(f)

if __name__ == "__main__":
    print("🧼 Sweeping encoding issues across docs/")
    run()
    print("✨ Done! Markdown files now clean and readable.")
