import sys
import io
import yaml

# Ensure UTF-8 output for emoji compatibility
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

COMPANIES_FILE = 'data/companies.yaml'

def load_companies():
    with open(COMPANIES_FILE, encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_company_anchor(name):
    return name.lower().replace(' ', '-')

def generate_company_link(company):
    name = company['name']
    emoji = company.get('emoji', '🏢')
    anchor = generate_company_anchor(name)
    return f"✅ [{emoji} {name}](../company_profiles/index.md#{anchor})"

def recommend_by_goal(companies, goal_tag):
    return sorted(
        [c for c in companies if goal_tag in c.get('tags', [])],
        key=lambda c: c['name']
    )

def main():
    companies = load_companies()

    print("# 🎯 Company Recommendations by Goal\n")

    goals = {
        'Profit-Focused': 'profit_friendly',
        'Stat-Gain Focused': 'gym_synergy',
        'Energy-Hungry Builds': 'energy_gain',
        'Brainy / Hacker Builds': 'edu_synergy',
        'Passive Income': 'passive_friendly'
    }

    for goal_name, tag in goals.items():
        print(f"\n## 🔹 {goal_name}\n")
        matched = recommend_by_goal(companies, tag)

        if not matched:
            print("_No companies matched this goal yet._")
        else:
            for company in matched:
                print(generate_company_link(company))

if __name__ == '__main__':
    main()
