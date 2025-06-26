import yaml
from pathlib import Path
import shutil

RESTORE_ITEMS = [
    {"Profit Wizard Overview": "profit_wizard/index.md"},
    {"Bank": "company_profiles/bank.md"},
    {"Cruise Line": "company_profiles/cruise_line.md"},
    {"Grocery Store": "company_profiles/grocery_store.md"},
    {"Law Firm": "company_profiles/law_firm.md"},
    {"Sweet Shop": "company_profiles/sweet_shop.md"},
    {"Tech Company": "company_profiles/tech_company.md"},
    {"TV Station": "company_profiles/tv_station.md"},
    {"Company Info Index": "company_info/index.md"},
    {"Decision Flow Index": "decision_flow/index.md"},
    {"Stat Entry": "decision_flow/stat_entry.md"},
    {"Budget Advice": "decision_flow/budget_advice.md"},
    {"Performance Review": "decision_flow/performance_review.md"},
    {"Goal Strategy": "decision_flow/goal_strategy.md"},
    {"Goal - Profit": "decision_flow/goal_profit.md"},
    {"Goal - Social": "decision_flow/goal_social.md"},
    {"Goal - Stats": "decision_flow/goal_stats.md"},
    {"Respec Tool": "decision_flow/respec_tool.md"},
    {"Armour Loadouts": "gear/armour/index.md"},
    {"Weapon Loadouts": "gear/weapons/index.md"},
    {"Changelog": "changelog.md"},
    {"Connect API": "connect_api.md"},
]

def run():
    root = Path(__file__).parent.parent
    yml_path = root / "mkdocs.yml"
    backup_path = root / "mkdocs.bak.yml"

    with open(yml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    shutil.copy(yml_path, backup_path)
    print(f"[BACKUP] Backup created at: {backup_path}")


    nav = config.get("nav", [])

    # Append restored items to appropriate sections
    section_map = {
        "Making Money": [],
        "Company Guide": [],
        "Decision Flow": [],
        "Gear": [],
        "Docs": [],
        "Utilities": []
    }

    for item in RESTORE_ITEMS:
        title, path = next(iter(item.items()))
        if path.startswith("profit_wizard/"):
            section_map["Making Money"].append(item)
        elif path.startswith("company_profiles/") or path.startswith("company_info/"):
            section_map["Company Guide"].append(item)
        elif path.startswith("decision_flow/"):
            section_map["Decision Flow"].append(item)
        elif path.startswith("gear/"):
            section_map["Gear"].append(item)
        elif path.startswith("utils/") or "connect_api" in path:
            section_map["Utilities"].append(item)
        else:
            section_map["Docs"].append(item)

    # Extend each section in nav
    for title, new_links in section_map.items():
        for block in nav:
            if isinstance(block, dict) and title in block:
                block[title].extend(new_links)
                break
        else:
            nav.append({title: new_links})

    # Remove Review & Reinstate if it exists
    nav = [block for block in nav if not (isinstance(block, dict) and "📂 Review & Reinstate" in block)]

    config["nav"] = nav

    with open(yml_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, sort_keys=False)

    print("✅ Restored content integrated and mkdocs.yml updated.")

if __name__ == "__main__":
    run()
