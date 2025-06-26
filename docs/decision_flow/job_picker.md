---
hide:
  - toc
---

# 🎯 Torn Job Picker Wizard  
> _Find the best City Job based on your stats, style, and Torn goals._

This assistant will guide you through a series of tailored questions to recommend your ideal job path.

---

<div id="wizard" style="margin-top:20px;">
  <div id="step-container"></div>
  <button id="nextBtn" style="margin-top:20px; display:none;" onclick="nextStep()">Next</button>

  <div id="result" style="display:none; margin-top:30px; background:#f9f9f9; padding:15px; border:1px solid #ccc;">
    <h3>🏁 Final Job Suggestions</h3>
    <ul id="recommendations"></ul>
    <button onclick="location.reload()">🔁 Start Over</button>
  </div>
</div>

<script>
// State
let stepIndex = 0;
const answers = {};
const steps = [
  {
    title: "1️⃣ What’s your strongest working stat?",
    name:  "stat",
    options: [
      ["manual",       "💪 Manual Labor"],
      ["intelligence", "🧠 Intelligence"],
      ["endurance",    "❤️ Endurance"]
    ]
  },
  {
    title: "2️⃣ What do you want from your job?",
    name:  "preference",
    options: [
      ["scaling", "📈 Stat Scaling & Progression"],
      ["profit",  "💰 Profit & Tradeables"],
      ["utility", "🔋 Utility & Energy Boosts"]
    ]
  }
];

// Map of jobs
const jobMap = {
  "Grocer":           { label:"Grocer",           link:"/company_profiles/grocery_store/",   desc:"Job Cans + passive income" },
  "Fire Department":  { label:"Fire Department",  link:"/company_profiles/fire_department/",desc:"FHCs, meds & XP" },
  "Casino":           { label:"Casino",           link:"/company_profiles/casino/",          desc:"Job Points → FHCs & Morphine" },
  "Education":        { label:"Education",        link:"/company_profiles/education/",       desc:"Fast-track degrees + INT boosts" },
  "Law":              { label:"Law Firm",         link:"/company_profiles/law_firm/",        desc:"Convert Job Points into Energy" },
  "Army":             { label:"Army",             link:"/company_profiles/army/",            desc:"Military gyms + END bonuses" },
  "Medical":          { label:"Medical",          link:"/company_profiles/medical/",         desc:"Revives & medical perks" }
};

// Boot
window.onload = () => renderStep();

// Render current step
function renderStep() {
  const step = steps[stepIndex];
  const container = document.getElementById("step-container");
  container.innerHTML = `<h3>${step.title}</h3>` + step.options.map(
    ([value,label]) =>
      `<label><input type="checkbox" name="${step.name}" value="${value}"> ${label}</label><br>`
  ).join("");
  document.getElementById("nextBtn").style.display = "inline-block";
}

// Advance or finish
function nextStep() {
  const step = steps[stepIndex];
  const selected = Array.from(
    document.querySelectorAll(`input[name='${step.name}']:checked`)
  ).map(i=>i.value);

  if (!selected.length) {
    return alert("Please select at least one option.");
  }
  answers[step.name] = selected;
  stepIndex++;
  if (stepIndex >= steps.length) {
    return showRecommendations();
  }
  renderStep();
}

// Build and display results
function showRecommendations() {
  document.getElementById("step-container").style.display = "none";
  document.getElementById("nextBtn").style.display       = "none";

  const picks = new Set();
  const stat = answers.stat[0];
  const pref = answers.preference[0];

  // Stat-based paths
  if (stat === "manual")       ["Grocer","Fire Department","Casino"].forEach(j=>picks.add(j));
  if (stat === "intelligence") ["Education","Law","Casino"].forEach(j=>picks.add(j));
  if (stat === "endurance")    ["Army","Medical","Fire Department"].forEach(j=>picks.add(j));

  // Preference-based paths
  if (pref === "scaling") ["Education","Army","Medical"].forEach(j=>picks.add(j));
  if (pref === "profit")  ["Casino","Grocer","Fire Department"].forEach(j=>picks.add(j));
  if (pref === "utility") ["Law","Casino","Education"].forEach(j=>picks.add(j));

  // Render
  const ul = document.getElementById("recommendations");
  if (!picks.size) {
    ul.innerHTML = "<li>📝 No suitable job found.</li>";
  } else {
    ul.innerHTML = "";
    picks.forEach(key => {
      const job = jobMap[key];
      if (job) {
        ul.innerHTML += `<li><a href="${job.link}" target="_blank">${job.label}</a> — ${job.desc}</li>`;
      }
    });
  }

  document.getElementById("result").style.display = "block";
}
</script>
