import os
import yaml

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_yaml(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def generate_tags(company):
    tags = []

    # Use job_special as a hint
    js = company.get('job_special', '').lower()

    if 'gym' in js or 'strength' in js or 'dexterity' in js:
        tags.append('stat_boosts')
    if 'energy' in js:
        tags.append('energy_boost')
    if 'hacking' in js or 'intelligence' in js:
        tags.append('brainy_bonuses')
    if 'travel' in js or 'vehicle' in js:
        tags.append('travel_speed')
    if 'crime' in js or 'revive' in js:
        tags.append('crime_synergy')

    return tags if tags else ['no_tag_info']

if __name__ == "__main__":
    file_path = 'data/companies.yaml'
    companies = load_yaml(file_path)

    updated = 0
    for company in companies:
        if 'tags' not in company or not company['tags']:
            company['tags'] = generate_tags(company)
            updated += 1

    save_yaml(file_path, companies)
    print(f"✅ Fixed {updated} companies with missing tags.")
