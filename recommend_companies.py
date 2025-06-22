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
    # Step 1: User answers (you can replace this with dynamic inputs later)
    answers = {
        'budget': 'Under $100 million',
        'motivation': 'Boosting my gym stats',
        'activity': 'Somewhat involved',
        'perks': 'Gym/stat boosts',
        'job_special': 'Yes — must match my perk'
    }

    # Step 2: Map answers to tag filters
    tag_map = load_yaml('data/filters.yml')
    selected_tags = [
        tag_map[q][a]
        for q, a in answers.items()
    ]

    # Step 3: Load company data
    companies = load_yaml('data/companies.yaml')

    # Step 4: Filter and output
    matched = filter_companies(companies, selected_tags)

    if not matched:
        print("❌ No companies matched all selected preferences.")
    else:
        print("✅ Recommended Companies:\n")
        for c in matched:
            print(f"- {c['name']}: {c.get('job_special') or 'No job special'}")
