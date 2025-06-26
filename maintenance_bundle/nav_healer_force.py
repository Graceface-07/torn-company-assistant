import yaml
from pathlib import Path
import shutil
import sys

# Fix for Windows consoles with limited encoding support
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass  # For older Python versions

def run():
    root = Path(__file__).parent.parent
    yml_path = root / "mkdocs.yml"
    backup_path = root / "mkdocs.bak.yml"

    print("[*] Running nav_healer_force.py (No Prompts)")

    with open(yml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("❌ mkdocs.yml is invalid — top-level structure must be a dictionary.")

    shutil.copy(yml_path, backup_path)

    nav = config.get("nav", [])
    if not isinstance(nav, list):
        raise ValueError("❌ 'nav' section is malformed — expected a list.")

    # ✨ Healing logic would go here
    # For now, we'll just confirm the structure is valid
    print(f"✅ Parsed {len(nav)} top-level nav blocks.")
    print("✅ No changes made (skeleton only).")

if __name__ == "__main__":
    run()
