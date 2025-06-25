import requests

API_KEY = "JfyNVufOHgrzgKE7"
USER_ID = "2702970"

def fetch_stats():
    url = f"https://api.torn.com/user/{USER_ID}?selections=basic,battlestats&key={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def recommend_company(stats):
    bs = stats.get("battlestats")
    if not bs:
        print("⚠️ 'battlestats' not found in API response. Make sure your key includes that permission.")
        return

    strength = bs.get("strength", 0)
    speed = bs.get("speed", 0)
    dexterity = bs.get("dexterity", 0)
    defense = bs.get("defense", 0)

    total_stats = strength + speed + dexterity + defense

    print("\n📊 Torn Stats Summary")
    print(f"- Strength:  {strength:,.0f}")
    print(f"- Speed:     {speed:,.0f}")
    print(f"- Dexterity: {dexterity:,.0f}")
    print(f"- Defense:   {defense:,.0f}")
    print(f"- Total:     {total_stats:,.0f}\n")

    print("🏢 Company Recommendations\n")

    if total_stats < 10_000_000:
        print("✅ 1. 10★ Sports Science")
        print("   Great for early training boosts while building stats.\n")
        print("✅ 2. 10★ Cruise Line")
        print("   Helps with energy and drug refill efficiency — perfect for Xanax users.\n")

    elif total_stats < 100_000_000:
        print("✅ 1. 10★ Medical Company")
        print("   Offers refill bonuses and passive perks to help you grind longer.\n")
        print("✅ 2. 10★ Tech Company")
        print("   Boosts combat effectiveness and pairs well with aggressive builds.\n")

    else:
        print("✅ 1. 10★ Music Studio")
        print("   Easy passive income with low management — good for high stat players.\n")
        print("✅ 2. 10★ Law Firm")
        print("   Provides stealth, accuracy, and weapon bonuses for elite PvP or chaining.\n")

def run():
    data = fetch_stats()
    if data:
        recommend_company(data)

if __name__ == "__main__":
    run()
