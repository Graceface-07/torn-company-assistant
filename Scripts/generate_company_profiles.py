import os
import yaml

INPUT_FILE = 'data/companies.yaml'
OUTPUT_FILE = 'docs/company_profiles/index.md'

CATEGORY_MAP = {
    'Passive-Friendly': ['passive_friendly', 'staff_light', 'no_job_special'],
    'Energy or Stat-Focused': ['energy_gain', 'gym_synergy', 'stat_boost'],
    'Strategic / Perk-Based': ['hacking_ready', 'edu_synergy', 'crime_helper', 'job_special_supports_perk']
}

def load_data():
    with open(INPUT_FILE, encoding='utf-8') as f:
        return yaml.safe_load(f)

def sort_companies(companies):
    return sorted(companies, key=lambda c: c['name'].lower())

def generate_anchor(name):
    return name.lower().replace(' ', '-')

def categorize(companies):
    categories = {k: [] for k in CATEGORY_MAP}
    for c in companies:
        for cat, tags in CATEGORY_MAP.items():
            if any(tag in c.get('tags', []) for tag in tags):
                categories[cat].append(c['name'])
                break
    return categories

def write_profiles(companies, categories):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🏢 Company Profiles (A–Z)\n\n")
        f.write("Welcome! Explore every company currently supported by the Torn Assistant.\n\n")

        # A–Z Jump List
        f.write("## 📚 Browse Alphabetically\n\n")
        for c in companies:
            emoji = c.get('emoji', '🏢')
            f.write(f"- [{emoji} {c['name']}](#{generate_anchor(c['name'])})\n")
        f.write("\n---\n\n")

        # Category Groupings
        f.write("## 🗂 Browse by Category\n\n")
        for cat, names in categories.items():
            f.write(f"### {cat}\n")
            for name in names:
                company = next((cmp for cmp in companies if cmp['name'] == name), {})
                emoji = company.get('emoji', '🏢')
                f.write(f"- {emoji} {name}\n")
            f.write("\n")

        f.write("---\n\n## 🔽 Company Details\n\n")
        for c in companies:
            name = c['name']
            emoji = c.get('emoji', '🏢')
            anchor = generate_anchor(name)
            f.write(f"### {emoji} {name} <a name=\"{anchor}\"></a>\n")
            f.write("<details>\n<summary>View Profile</summary>\n\n")
            f.write(f"**Budget Tier**: {c.get('budget', 'Unknown')}\n")
            f.write(f"  \n**Tags**: {', '.join(c.get('tags', [])) or 'None'}\n")
            f.write(f"  \n**Job Special**: {c.get('job_special', 'None')}\n")
            f.write(f"  \n**Best For**: {c.get('best_for', 'TBD')}\n\n")
            f.write("**Pros**:\n- " + '\n- '.join(c.get('pros', ['TBD'])) + "\n\n")
            f.write("**Cons**:\n- " + '\n- '.join(c.get('cons', ['TBD'])) + "\n\n")
            f.write("</details>\n\n---\n\n")

    print(f"✅ Company index generated at: {OUTPUT_FILE}")

if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    companies = load_data()
    sorted_companies = sort_companies(companies)
    categories = categorize(sorted_companies)
    write_profiles(sorted_companies, categories)
