import subprocess

STEPS = [
    ("Nav Healer", ["python", "scripts/nav_healer_force.py"]),
    ("Archiver", ["python", "scripts/move_to_trash.py"]),
    ("Restore Nav", ["python", "scripts/nav_restore.py"]),
    ("Encoding Sweep", ["python", "scripts/emoji_sanitizer.py"]),
]

def run():
    print("🔧 Starting Torn Assistant Maintenance...\n")
    for label, command in STEPS:
        print(f"➡️  {label}...")
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(result.stdout.strip() or "✅ Done.\n")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed during {label}:")
            print(e.stderr or str(e))
            break
    else:
        print("\n🎯 All steps completed successfully.\n")

if __name__ == "__main__":
    run()
