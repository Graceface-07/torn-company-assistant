# 🧠 Torn Company Recommender (Full Wizard)

This assistant will guide you through a series of tailored questions to recommend the ideal 10★ companies based on your stats, goals, habits, and ambitions.

---

<div id="wizard" style="margin-top: 20px;">
  <!-- Step Container -->
  <div id="step-container"></div>
  <button id="nextBtn" style="margin-top:20px; display:none;" onclick="nextStep()">Next</button>

  <!-- Final Recommendations -->
  <div id="result" style="display:none; margin-top:30px; background:#f9f9f9; padding:15px; border:1px solid #ccc;">
    <h3>🏁 Final Recommendations</h3>
    <ul id="recommendations"></ul>
    <button onclick="location.reload()">🔁 Start Over</button>
  </div>
</div>

<script>
const query = new URLSearchParams(location.search);
const statVals = {
  manual: parseInt(query.get('manual') || '0'),
  intelligence: parseInt(query.get('intelligence') || '0'),
  endurance: parseInt(query.get('endurance') || '0')
};
const primaryStat = Object.entries(statVals).sort((a, b) => b[1] - a[1])[0][0];

let stepIndex = 0;
let answers = {};
let stepContainer = null;
let nextBtn = null;

const steps = [
  {
    title: "1️⃣ What are your top goals?",
    name: "goals",
    options: [
      ["income", "💰 Passive Income"],
      ["training", "🏋️ Stat Growth"],
      ["perks", "🎁 Special Perks"],
      ["leadership", "🧠 Company Ownership"],
      ["progression", "🔺 Fast Promotions"]
    ]
  },
  {
    title: "2️⃣ How would you describe your playstyle?",
    name: "playstyle",
    options: [
      ["active", "⚔️ Very Active"],
      ["daily", "💼 Daily Login"],
      ["casual", "😴 Casual / Passive"]
    ]
  },
  {
    title: "3️⃣ Are you interested in Job Specials?",
    name: "jobSpecials",
    options: [
      ["yes", "✅ Yes — I want them unlocked quickly"],
      ["no", "❌ No — don't care about specials"]
    ]
  },
  {
    title: "4️⃣ Which trade-off are you willing to make?",
    name: "tradeoff",
    options: [
      ["money", "💰 Money over Stats"],
      ["stats", "🏋️ Stats over Money"],
      ["balanced", "⚖️ Balanced"]
    ]
  },
  {
    title: "5️⃣ Do you use drugs/boosts often?",
    name: "drugUser",
    options: [
      ["frequent", "💊 Yes — I chain, refill, boost often"],
      ["seldom", "📉 Not really — I’m efficient"],
      ["never", "🚫 Never — clean & casual"]
    ]
  },
  {
    title: "6️⃣ Are you aiming to own or lead a company?",
    name: "lead",
    options: [
      ["yes", "🏢 Yes — leadership & management"],
      ["no", "👤 No — I want perks and freedom"]
    ]
  },
  {
    title: "7️⃣ What size of company team appeals to you?",
    name: "teamSize",
    options: [
      ["solo", "👤 Solo or small team (1–5)"],
      ["medium", "👥 Medium crew (5–10)"],
      ["large", "🏛️ Large active group (10+)"]
    ]
  }
];

window.onload = () => {
  stepContainer = document.getElementById("step-container");
  nextBtn = document.getElementById("nextBtn");
  renderStep();
};

function renderStep() {
  const step = steps[stepIndex];
  stepContainer.innerHTML = `<h3>${step.title}</h3>` + step.options.map(([value, label]) =>
    `<label><input type="checkbox" name="${step.name}" value="${value}"> ${label}</label><br>`
  ).join("");
  nextBtn.style.display = "inline-block";
}

function nextStep() {
  const step = steps[stepIndex];
  const selected = Array.from(document.querySelectorAll(`input[name='${step.name}']:checked`)).map(i => i.value);
  if (selected.length === 0) return alert("Please select at least one option.");
  answers[step.name] = selected;
  stepIndex++;
  if (stepIndex >= steps.length) return showRecommendations();
  renderStep();
}

function showRecommendations() {
  stepContainer.style.display = "none";
  nextBtn.style.display = "none";
  const recList = document.getElementById("recommendations");
  const picks = new Set();

  const { goals, playstyle, jobSpecials, tradeoff, drugUser, lead, teamSize } = answers;

  if (goals.includes("income")) {
    if (primaryStat === "manual") picks.add("🎵 Music Store – ad revenue focus");
    if (primaryStat === "endurance") picks.add("🍣 Restaurant – balanced with stat perks");
    if (primaryStat === "intelligence") picks.add("📺 TV Station – passive & easy upkeep");
  }

  if (goals.includes("training")) {
    if (primaryStat === "endurance") picks.add("🥋 Sports Team – solo stat stacking");
    if (primaryStat === "manual") picks.add("🚜 Farm – Manual-heavy gym bonuses");
    if (primaryStat === "intelligence") picks.add("🔬 Law Firm – stealth & combat scaling");
  }

  if (goals.includes("perks")) {
    if (drugUser.includes("frequent")) picks.add("🛳️ Cruise Line – refill boosts & travel hacks");
    if (primaryStat === "manual" || primaryStat === "intelligence") picks.add("💾 Tech Company – accuracy, stealth & damage");
  }

  if (goals.includes("leadership") || lead.includes("yes")) {
    picks.add("🏢 Mechanic – simple ownership + passive");
    picks.add("📈 Software Corp – strong for managers + growth");
  }

  if (tradeoff.includes("money")) picks.add("🎵 Music Store");
  if (tradeoff.includes("stats")) picks.add("🥋 Sports or Farm");
  if (jobSpecials.includes("yes")) picks.add("🏋️ Any company where you meet the required stats (1500+)");

  if (teamSize.includes("solo")) picks.add("🛠️ Mechanic – great for 1–3 operators");
  if (teamSize.includes("medium")) picks.add("🍣 Restaurant – active social stats");
  if (teamSize.includes("large")) picks.add("🧠 Tech or Cruise – faction-friendly perks");

  if (picks.size === 0) picks.add("📝 Not enough data to generate a meaningful recommendation.");

  picks.forEach(p => {
    const li = document.createElement("li");
    li.innerHTML = p;
    document.getElementById("recommendations").appendChild(li);
  });

  document.getElementById("result").style.display = "block";
}
</script>
<script>
function showRecommendations() {
  document.getElementById("step-container").style.display = "none";
  document.getElementById("nextBtn").style.display = "none";

  const companyMap = {
    "🎵 Music Store": {
      label: "🎵 Music Store",
      link: "/company_profiles/music_store/",
      stat: "Manual",
      perks: "Ad revenue, passive income",
      leader: "Medium",
      specials: "Music CDs, Improve Morale, Mood Boost"
    },
    "🍣 Restaurant": {
      label: "🍣 Restaurant",
      link: "/company_profiles/restaurant/",
      stat: "Endurance",
      perks: "Income + stat perks",
      leader: "Medium",
      specials: "Job Points for Energy Refills"
    },
    "📺 TV Station": {
      label: "📺 TV Station",
      link: "/company_profiles/tv_station/",
      stat: "Intelligence",
      perks: "Ultra-passive income",
      leader: "Low",
      specials: "Extra Nerve, Drug Cooldown Reduction"
    },
    "🥋 Sports Team": {
      label: "🥋 Sports Team",
      link: "/company_profiles/sports_team/",
      stat: "Endurance",
      perks: "Gym stat boosts",
      leader: "Low",
      specials: "Strength & Defense Boosters"
    },
    "🚜 Farm": {
      label: "🚜 Farm",
      link: "/company_profiles/farm/",
      stat: "Manual",
      perks: "Manual + gym synergy",
      leader: "Medium",
      specials: "Food Production, Natural Energy Buff"
    },
    "🔬 Law Firm": {
      label: "🔬 Law Firm",
      link: "/company_profiles/law_firm/",
      stat: "Intelligence",
      perks: "Stealth & speed boosts",
      leader: "Medium",
      specials: "Legal Counsel, Reduced Jail Time"
    },
    "🛳️ Cruise Line": {
      label: "🛳️ Cruise Line",
      link: "/company_profiles/cruise_line/",
      stat: "Endurance",
      perks: "Drug refill & travel perks",
      leader: "Medium",
      specials: "Travel Vouchers, Refill Boosts"
    },
    "💾 Tech Company": {
      label: "💾 Tech Company",
      link: "/company_profiles/tech_company/",
      stat: "Intelligence",
      perks: "Combat, stealth, accuracy",
      leader: "High",
      specials: "Hacking Tools, Stealth Buffs"
    },
    "🏢 Mechanic": {
      label: "🏢 Mechanic",
      link: "/company_profiles/mechanic/",
      stat: "Manual",
      perks: "Easy ownership, passive profit",
      leader: "Very High",
      specials: "Chaining Assistance, Repair Efficiency"
    },
    "📈 Software Corp": {
      label: "📈 Software Corp",
      link: "/company_profiles/software_corporation/",
      stat: "Intelligence",
      perks: "Promotion perks, leadership track",
      leader: "High",
      specials: "Coding Projects, Intelligence Boosters"
    }
  };

  const picks = new Set();
  const { goals = [], playstyle = [], jobSpecials = [], tradeoff = [], drugUser = [], lead = [], teamSize = [] } = answers;
  const stat = primaryStat;

  if (goals.includes("income")) {
    if (stat === "manual") picks.add("🎵 Music Store");
    if (stat === "endurance") picks.add("🍣 Restaurant");
    if (stat === "intelligence") picks.add("📺 TV Station");
    if (playstyle.includes("casual")) picks.add("📺 TV Station");
  }

  if (goals.includes("training")) {
    if (stat === "endurance") picks.add("🥋 Sports Team");
    if (stat === "manual") picks.add("🚜 Farm");
    if (stat === "intelligence") picks.add("🔬 Law Firm");
  }

  if (goals.includes("perks")) {
    if (stat === "intelligence" || stat === "manual") picks.add("💾 Tech Company");
    if (stat === "endurance") picks.add("🛳️ Cruise Line");
  }

  if (goals.includes("leadership") || lead.includes("yes")) {
    picks.add("🏢 Mechanic");
    picks.add("📈 Software Corp");
  }

  if (tradeoff.includes("money")) picks.add("🎵 Music Store");
  if (tradeoff.includes("stats")) picks.add("🥋 Sports Team");
  if (jobSpecials.includes("yes")) picks.add("🔬 Law Firm");

  if (teamSize.includes("solo")) picks.add("🏢 Mechanic");
  if (teamSize.includes("medium")) picks.add("🍣 Restaurant");
  if (teamSize.includes("large")) picks.add("🛳️ Cruise Line");

  const ul = document.getElementById("recommendations");
  ul.innerHTML = "";

  if (picks.size === 0) {
    ul.innerHTML = "<li>📝 Not enough data to generate suggestions.</li>";
    document.getElementById("result").style.display = "block";
    return;
  }

  picks.forEach(key => {
    const c = companyMap[key];
    if (c) {
      const li = document.createElement("li");
      li.innerHTML = `<a href="${c.link}" target="_blank">${c.label}</a>`;
      ul.appendChild(li);
    }
  });

  // Side-by-side table
  if (picks.size >= 2) {
    const table = document.createElement("table");
    table.style.marginTop = "20px";
    table.style.borderCollapse = "collapse";
    table.style.width = "100%";

    const headers = [...picks].map(k => `<th style="padding:6px; border:1px solid #ccc;">${companyMap[k]?.label}</th>`).join("");

    const row = (label, prop, isButton = false) => `
      <tr>
        <td style="padding:6px; border:1px solid #ccc;"><strong>${label}</strong></td>
        ${[...picks].map(k => {
          const val = companyMap[k]?.[prop] || '';
          return `<td style="padding:6px; border:1px solid #ccc;">${isButton ? `<a href='${companyMap[k].link}' target='_blank'><button>See Profile</button></a>` : val}</td>`;
        }).join("")}
      </tr>`;

    table.innerHTML = `
      <tr><th></th>${headers}</tr>
      ${row("Primary Stat", "stat")}
      ${row("Perks", "perks")}
      ${row("Leadership Friendly", "leader")}
      ${row("Job Specials", "specials")}
      ${row("Profile", "link", true)}
    `;

    document.getElementById("result").appendChild(document.createElement("hr"));
    document.getElementById("result").appendChild(table);
  }

  document.getElementById("result").style.display = "block";
}
</script>
