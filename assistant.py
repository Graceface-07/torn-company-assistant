import os
import subprocess
import sys

ROOT = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.join(ROOT, "scripts")

# 📘 Known script descriptions
SCRIPT_DESCRIPTIONS = {
    "link_check.py": "Fix or validate markdown links and section anchors across all docs",
    "nav_builder.py": "Generate a flat or grouped nav block, with optional injection into mkdocs.yml",
}

def list_scripts():
    return sorted(
        [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".py") and not f.startswith("_")]
    )

def run_script(script_name):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n⚠️  Error running {script_name}:\n{e}")

def normalize_markdown_encoding():
    cmd = (
        r'powershell -Command "Get-ChildItem -Recurse -Filter *.md | '
        r'ForEach-Object { (Get-Content $_.FullName) | '
        r'Set-Content -Encoding utf8 $_.FullName }"'
    )
    subprocess.run(cmd, shell=True)
    print("✅ All Markdown files normalized to UTF-8.")

def show_menu(scripts):
    print("\n🧭 Torn Assistant Control Panel")
    print("-" * 45)
    for i, script in enumerate(scripts, 1):
        desc = SCRIPT_DESCRIPTIONS.get(script, "No description available.")
        print(f"{i}. 🛠️  {script.ljust(25)} → {desc}")
    print(f"{len(scripts) + 1}. 🖥️  Serve documentation (mkdocs serve)")
    print(f"{len(scripts) + 2}. 🚀 Deploy to GitHub Pages")
    print(f"{len(scripts) + 3}. 💾 Commit & push to Git")
    print(f"{len(scripts) + 4}. 🧼 Normalize all Markdown files to UTF-8")
    print(f"{len(scripts) + 5}. ❌ Exit")

def main():
    while True:
        scripts = list_scripts()
        show_menu(scripts)

        try:
            choice = int(input("\nChoose an option: "))
        except ValueError:
            print("❌ Invalid input.")
            continue

        if 1 <= choice <= len(scripts):
            run_script(scripts[choice - 1])
        elif choice == len(scripts) + 1:
            subprocess.run("mkdocs serve", shell=True)
        elif choice == len(scripts) + 2:
            subprocess.run("mkdocs gh-deploy", shell=True)
        elif choice == len(scripts) + 3:
            msg = input("📝 Git commit message: ")
            subprocess.run("git add .", shell=True)
            subprocess.run(f'git commit -m "{msg}"', shell=True)
            subprocess.run("git push", shell=True)
        elif choice == len(scripts) + 4:
            normalize_markdown_encoding()
        elif choice == len(scripts) + 5:
            print("👋 Goodbye.")
            sys.exit()
        else:
            print("❌ Please pick a valid number.")

if __name__ == "__main__":
    main()
