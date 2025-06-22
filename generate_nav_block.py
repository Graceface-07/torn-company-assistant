import yaml

# Load companies.yaml
with open("data/companies.yaml", "r", encoding="utf-8") as file:
    companies = yaml.safe_load(file)

# Sort alphabetically by company name
companies_sorted = sorted(companies, key=lambda x: x["name"].lower())

# Build nav block
print("🔽 Copy the following into your mkdocs.yml under 'nav':\n")
print("- Companies:")

for c in companies_sorted:
    name = c["name"]
    slug = name.lower().replace(" ", "_")
    path = f"company_profiles/{slug}.md"
    print(f"    - {name}: {path}")
