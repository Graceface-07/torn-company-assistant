# 🕵️ Analyze My Company

This tool uses your saved Torn API key to evaluate your current company, its type, and staff setup.

> ⚠️ Your API key is never shared or stored online—it stays in your browser.

---

## 🧰 Company Snapshot

<div id="company-info">
  <p>Loading your company profile...</p>
</div>

---

<script>
async function fetchCompanyProfile() {
  const key = localStorage.getItem("torn_api_key");
  const infoDiv = document.getElementById("company-info");

  if (!key) {
    infoDiv.innerHTML = "<p style='color:red;'>No API key found. Please <a href='connect_api.html'>connect your key</a> first.</p>";
    return;
  }

  const url = `https://api.torn.com/company/?selections=profile,basic&key=${key}`;

  try {
    const res = await fetch(url);
    const data = await res.json();

    if (data.error) {
      infoDiv.innerHTML = `<p style='color:red;'>Error: ${data.error.error}. Check your API key and try again.</p>`;
      return;
    }

    const company = data.company_profile;
    const staff = Object.keys(data.company_employees || {}).length;
    const loyaltyList = Object.values(data.company_employees || {}).map(e => e.days_in_company);
    const avgLoyalty = loyaltyList.length ? (loyaltyList.reduce((a,b) => a + b) / loyaltyList.length).toFixed(1) : 0;

    infoDiv.innerHTML = `
      <p><strong>📛 Company:</strong> ${company.name} (${company.type})</p>
      <p><strong>📊 Tier:</strong> ${company.upgrade}</p>
      <p><strong>👥 Staff:</strong> ${staff}</p>
      <p><strong>❤️ Avg Loyalty:</strong> ${avgLoyalty} days</p>
      <p><strong>💡 Analysis:</strong> ${getInsight(company.type, avgLoyalty)}</p>
    `;
  } catch (err) {
    infoDiv.innerHTML = `<p style='color:red;'>Unexpected error: ${err.message}</p>`;
  }
}

function getInsight(type, loyalty) {
  const l = parseFloat(loyalty);
  const tips = {
    "Sweet Shop": l >= 30 ? "✅ Candy drops likely active—maintain staff." : "⏳ Build loyalty toward 30+ days to unlock candy drops.",
    "Music Store": l >= 35 ? "🎵 Bonus drops should be live. Keep staff active!" : "📈 Push staff to 35+ days for consistent bonuses.",
    "Farm": l >= 40 ? "🌾 Energy & happiness boosts are unlocked—consider expansion." : "🧪 Scale slow—boost loyalty to activate passive perks.",
    "Software Corporation": l >= 50 ? "💻 Cooldowns and regen in full effect." : "👷 Hire long-term INT staff to unlock peak value."
  };
  return tips[type] || "🛠 No custom insight yet—consider submitting this company type to improve the assistant!";
}

window.onload = fetchCompanyProfile;
</script>
