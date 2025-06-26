import shutil
from pathlib import Path
import sys

# Attempt to reconfigure stdout for UTF-8 encoding on supported terminals
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass  # Fallback for older Python versions or non-UTF-8 environments

# Files flagged as "Archive"
FILES_TO_ARCHIVE = [
    "main_menu.md",
    "gear/index.md",
    "company_profiles/farm.md",
    "company_profiles/fire_department.md",
    "company_profiles/furniture_store.md",
    "company_profiles/game_development.md",
    "company_profiles/insurance.md",
    "company_profiles/logistics.md",
    "company_profiles/mechanic.md",
    "company_profiles/music_store.md",
    "company_profiles/restaurant.md",
    "company_profiles/software_corporation.md",
    "company_profiles/sports_team.md",
]

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TRASH = ROOT / ".trash"

def move_to_trash(file):
    src = DOCS / file
    dest = TRASH / file
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    print(f"[ARCHIVED] {file}")

def run():
    print("[*] Archiving unused files...\n")
    for f in FILES_TO_ARCHIVE:
        if (DOCS / f).exists():
            move_to_trash(f)
        else:
            print(f"[SKIPPED] {f} (not found)")
    print("\n✅ Archiving complete.")

if __name__ == "__main__":
    run()
