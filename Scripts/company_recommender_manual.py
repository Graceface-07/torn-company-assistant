def get_player_input():
    print("📊 Enter your battle stats:")

    try:
        strength = float(input("Strength: ").replace(",", ""))
        speed = float(input("Speed: ").replace(",", ""))
        dexterity = float(input("Dexterity: ").replace(",", ""))
        defense = float(input("Defense: ").replace(",", ""))
    except ValueError:
        print("❌ Please enter numeric values only.")
        return None

    print("\n🎯 What do you want most from a company?")
    print("1. Stat gains (training boosts)")
    print("2. Drug or refill efficiency")
    print("3. Combat bonuses")
    print("4. Passive income")
    print("5. Unique travel/support perks")

    goal = input("Select option 1–5: ").strip()
    return strength, speed, dexterity, defense, goal

def recommend(strength, speed, dexterity, defense, goal):
    total = strength + speed + dexterity + defense
    print(f"\n🧠 Total Battle Stats: {int(total):,}\n")

    recs = []

    if total < 10_000_000:
        if goal == "1":
            recs = ["10★ Sports Science", "10★ Gym"]
        elif goal == "2":
            recs = ["10★ Cruise Line", "10★ Medical"]
        elif goal == "3":
            recs = ["10★ Law Firm", "10★ Tech Company"]
        elif goal == "4":
            recs = ["10★ Music Studio", "10★ TV Station"]
        else:
            recs = ["10★ Cruise Line", "10★ Oil Rig"]

    elif total < 100_000_000:
        if goal == "1":
            recs = ["10★ Sports Science", "10★ Medical"]
        elif goal == "2":
            recs = ["10★ Cruise Line", "10★ Farm"]
        elif goal == "3":
            recs = ["10★ Tech Company", "10★ Law Firm"]
        elif goal == "4":
            recs = ["10★ TV Station", "10★ Music Studio"]
        else:
            recs = ["10★ Cruise Line", "10★ Oil Rig"]

    else:
        if goal == "1":
            recs = ["10★ Gym", "10★ Sports Science"]
        elif goal == "2":
            recs = ["10★ Medical", "10★ Cruise Line"]
        elif goal == "3":
            recs = ["10★ Law Firm", "10★ Tech Company"]
        elif goal == "4":
            recs = ["10★ Music Studio", "10★ TV Station"]
        else:
            recs = ["10★ Oil Rig", "10★ Private Security"]

    print("📦 Recommended Companies:\n")
    for i, company in enumerate(recs, start=1):
        print(f"✅ {i}. {company}")
    print()

def run():
    data = get_player_input()
    if data:
        recommend(*data)

if __name__ == "__main__":
    run()
