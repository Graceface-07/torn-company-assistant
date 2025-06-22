import os
import yaml

# Define file paths
input_path = "data/companies.yaml"
output_dir = "docs/company_profiles"
os.makedirs(output_dir, exist_ok=True)

# Load YAML data
try:
    with open(input_path, "r", encoding="utf-8") as f:
        companies = yaml.safe_load(f)
except FileNotFoundError:
    print(f"❌ YAML file not found at: {input_path}")
    exit()
except yaml.YAMLError as e:
    print(f"❌ YAML parsing error:\n{e}")
    exit()

if not companies:
    print("⚠️  No companies found in the YAML file.")
    exit()

# Generate Markdown files for each company
for company in companies:
    filename = f"{company['name'].lower().replace(' ', '_')}.md"
    output_file = os.path.join(output_dir, filename)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# {company['name']}\n\n")
        f.write(f"**Category:** {company['category']}\n\n")

        if company.get('has_job_special'):
            f.write(f"**Job Special:** {company['job_special']}\n\n")
        else:
            f.write("**Job Special:** None ❌\n\n")

        f.write("## 🌟 Perks\n")
        for perk in company.get('perks', []):
            f.write(f"- {perk}\n")
        f.write("\n")

        f.write("## 🔗 Synergy Notes\n")
        for note in company.get('synergy_notes', []):
            f.write(f"- {note}\n")
        f.write("\n")

        f.write("## 🏷 Tags\n")
        for tag in company.get('tags', []):
            f.write(f"- `{tag}`\n")

print(f"✅ {len(companies)} company profiles generated in: {output_dir}")
