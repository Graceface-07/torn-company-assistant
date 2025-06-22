import yaml

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def filter_companies(companies, filters):
    return [
        c for c in companies
        if all(tag in c['tags'] for tag in filters)
    ]

if __name__ == "__main__":
    answers = {
        'budget': 'Under $100 million',
        'motivation': 'Boosting my gym stats',
        'activity': 'Somewhat involved',
        'perks': 'Gym/stat boosts',
        'job_special': 'Yes — must match my perk'
    }

    # Load filter mappings
    tag_map = load_yaml('filters.yml')
    selected_tags = [
        tag_map[q][a]
        for q, a in answers.items()
    ]

    companies = load_yaml('companies.yaml')
    matched = filter_companies(companies, selected_tags)

    for c in matched:
        print(f"✅ {c['name']} — {c.get('job_special') or 'No job special'}")
