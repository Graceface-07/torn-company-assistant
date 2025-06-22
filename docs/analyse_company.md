# 🕵️ Analyze My Company (Live API Key)

This tool connects directly to Torn’s API using your company-enabled key to provide real-time analysis.

> 🛡️ Your API key is embedded directly. Only use this for personal/private versions of your site.

---

## 🧰 Company Snapshot

<div id="company-info">
  <p>Fetching company details...</p>
</div>

<script>
  const API_KEY = "NVMCjgpq86wpcPCF"; // ✅ Your validated key with company access

  fetch(`https://api.torn.com/company/?selections=profile,basic&key=${API_KEY}`)
    .then(res => res.json())
    .then(data => {
      if (!data.company_profile) {
        document.getElementById("company-info").innerHTML =
          "<p style='color:red;'>❌ Key is valid, but company data is unavailable. Double-check Torn access settings.</p>";
        return;
      }

      const company = data.company_profile;
      const staffList = Object.values(data.company_employees || {});
      const staffCount = staffList.length;
      const avgLoyalty = staffCount
        ? (staffList.reduce((sum, e) => sum + e.days_in_company, 0) / staffCount).toFixed(1)
        : 0;

      document.getElementById("company-info").innerHTML = `
        <p><strong>📛 Name:</strong> ${company.name}</p>
        <p><strong>🏢 Type:</strong> ${company.type}</p>
        <p><strong>📈 Tier:</strong> ${company.upgrade}</p>
        <p><strong>👥 Staff Count:</strong> ${staffCount}</p>
        <p><strong>📅 Avg Loyalty:</strong> ${avgLoyalty} days</p>
        <p><strong>💡 Insight:</strong> ${generateInsight(company.type, avgLoyalty)}</p>
      `;
    })
    .catch(err => {
      document.getElementById("company-info").innerHTML =
        `<p style='color:red;'>❌ Error fetching data: ${err.message}</p>`;
    });

  function generateInsight(type, loyaltyStr) {
    const loyalty = parseFloat(loyaltyStr);
    const tips = {
      "Sweet Shop": loyalty >= 30
        ? "✅ Candy drops likely active—maintain staff loyalty to keep them flowing."
        : "🍬 Boost loyalty past 30 days to activate candy perks.",
      "Farm": loyalty >= 40
        ? "🌾 Happiness and energy bonuses active—expand if needed."
        : "🌱 Build to 40+ day loyalty for steady passive perks.",
      "Music Store": loyalty >= 35
        ? "🎶 Item drops probably online—check your item log."
        : "📈 Push loyalty over 35 days to trigger perks.",
      "Software Corporation": loyalty >= 50
        ? "💻 Energy regen and cooldown perks should now be live."
        : "👷 Steady loyalty growth unlocks passive scaling.",
      "TV Station": loyalty >= 45
        ? "📺 Crime XP likely enabled—perfect for faction synergy."
        : "📰 Loyalty grind → top-tier XP and regen boosts."
    };
    return tips[type] || "🛠 No tailored insight for this company type yet—want to help me add it?";
  }
</script>
