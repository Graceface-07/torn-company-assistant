# 📋 Job Picker Wizard

<div id="jobWizard" style="margin-top: 20px;">
  <p id="wizard-intro">Use this guided assistant to find the best city job for your stats, playstyle, and goals.</p>
  <div id="job-step-container"></div>
  <button id="jobNextBtn" style="margin-top:20px; display:none;" onclick="nextJobStep()">Next</button>
</div>

<div id="job-result" style="display:none; margin-top:20px; background:#f9f9f9; padding:15px; border:1px solid #ccc;">
  <h3>🏁 Recommended Jobs</h3>
  <ul id="job-recommendations" style="margin-bottom:10px;"></ul>
  <div id="job-comparison-table"></div>
  <div style="margin-top:10px; display:flex; gap:10px;">
    <button onclick="location.reload()">🔁 Start Over</button>
    <button onclick="window.location.href='/'">🏠 Home</button>
  </div>
</div>

<style>
  #job-result ul li {
    margin-bottom: 6px;
  }
  #job-comparison-table hr {
    margin-top: 10px;
    margin-bottom: 10px;
  }
</style>

<script>
let jobStepIndex = 0;
let jobAnswers = {};
let jobStepContainer = null;
let jobNextBtn = null;

const jobSteps = [
  {
    title: "1️⃣ What are your main job goals?",
    name: "jobGoals",
    options: [
      ["income", "💰 Make Good Money"],
      ["stats", "📈 Increase Stats Over Time"],
      ["specials", "🎁 Unlock Job Specials Fast"],
      ["perks", "📦 Benefit from Passive Bonuses"]
    ]
  },
  {
    title: "2️⃣ What is your current playstyle?",
    name: "playstyle",
    options: [
      ["active", "⚔️ Very Active"],
      ["daily", "💼 Daily Login"],
      ["casual", "😴 Casual or Infrequent"]
    ]
  },
  {
    title: "3️⃣ Do you use drugs/boosts regularly?",
    name: "drugUsage",
    options: [
      ["frequent", "💊 Frequently (chains, refills, boosting)"],
      ["occasional", "📉 Occasionally"],
      ["never", "🚫 Never — clean play"]
    ]
  },
  {
    title: "4️⃣ What’s your strongest stat focus right now?",
    name: "statFocus",
    options: [
      ["manual", "🛠️ Manual"],
      ["intelligence", "🧠 Intelligence"],
      ["endurance", "💪 Endurance"]
    ]
  },
  {
    title: "5️⃣ Which do you prefer long-term?",
    name: "preference",
    options: [
      ["money", "💰 Income over Stat Gains"],
      ["growth", "📈 Stat Growth over Money"],
      ["balanced", "⚖️ Balanced Mix"]
    ]
  }
];

const jobMap = {
  "Medical": {
    label: "🏥 Medical",
    focus: "Manual",
    perks: "Energy Refills, Gym Boosters",
    specials: "Recover Energy, First Aid Refill, Gym Cost Discount",
    idealFor: ["manual", "frequent", "stats", "perks"],
    link: "/company_profiles/medical/"
  },
  "Army": {
    label: "🎖️ Army",
    focus: "Endurance",
    perks: "Strength & Defense Multipliers",
    specials: "Stat Boosters, Chain Perks, Discipline Track",
    idealFor: ["endurance", "active", "stats"],
    link: "/company_profiles/army/"
  },
  "Fire Department": {
    label: "🚒 Fire Department",
    focus: "Endurance",
    perks: "All-Round Boosts, Energy Bonuses",
    specials: "Refill Boost, Gym Multiplier, Team Bonuses",
    idealFor: ["balanced", "endurance", "perks"],
    link: "/company_profiles/fire_department/"
  },
  "Casino": {
    label: "🎰 Casino",
    focus: "Balanced",
    perks: "Morale Boosts, Fun Perks",
    specials: "",
    idealFor: ["casual", "income", "perks"],
    link: "/company_profiles/casino/"
  }
};

document.addEventListener("DOMContentLoaded", function () {
  jobStepContainer = document.getElementById("job-step-container");
  jobNextBtn = document.getElementById("jobNextBtn");
  renderJobStep();
});

function renderJobStep() {
  const step = jobSteps[jobStepIndex];
  jobStepContainer.innerHTML = `<h3>${step.title}</h3>` + step.options.map(([val, label]) =>
    `<label><input type="checkbox" name="${step.name}" value="${val}"> ${label}</label><br>`
  ).join("");
  jobNextBtn.style.display = "inline-block";
}

function nextJobStep() {
  const step = jobSteps[jobStepIndex];
  const selected = Array.from(document.querySelectorAll(`input[name='${step.name}']:checked`)).map(x => x.value);
  if (selected.length === 0) {
    alert("Please select at least one option.");
    return;
  }
  jobAnswers[step.name] = selected;
  jobStepIndex++;
  if (jobStepIndex >= jobSteps.length) return showJobResults();
  renderJobStep();
}

function showJobResults() {
  document.getElementById("jobWizard").style.display = "none";
  document.getElementById("job-result").style.display = "block";

  const ul = document.getElementById("job-recommendations");
  ul.innerHTML = "";

  const pickedTraits = Object.values(jobAnswers).flat();

  const scoredJobs = Object.entries(jobMap).map(([key, job]) => {
    const score = job.idealFor.reduce((acc, trait) => pickedTraits.includes(trait) ? acc + 1 : acc, 0);
    return { ...job, score };
  }).sort((a, b) => b.score - a.score);

  scoredJobs.slice(0, 3).forEach(job => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div style="display:flex; align-items:center; justify-content:space-between; max-width:600px;">
        <div><strong>${job.label}</strong><br>🔹 ${job.perks}</div>
        <div style="display:flex; gap:10px;">
          <a href="${job.link}" target="_blank"><button>Learn More</button></a>
          <button onclick="alert('✅ ${job.label} selected!')">🎯 Select</button>
        </div>
      </div>`;
    ul.appendChild(li);
  });

  if (scoredJobs.length >= 2) {
    const top = scoredJobs.slice(0, 3);
    const table = document.createElement("table");
    table.style.marginTop = "10px";
    table.style.borderCollapse = "collapse";
    table.style.width = "100%";

    const headerRow = `<tr>${top.map(() => `<th style="padding:6px; border:1px solid #ccc;"></th>`).join("")}</tr>`;

    const row = (label, key, isSpecial = false) => `
      <tr>
        ${top.map(job => {
          let val = job[key] || "";
          if (isSpecial && !val.trim()) val = "<em>No Job Specials</em>";
          return `<td style="padding:6px; border:1px solid #ccc;"><strong>${label}:</strong><br>${val}</td>`;
        }).join("")}
      </tr>`;

    table.innerHTML = `
      ${headerRow}
      ${row("Stat Focus", "focus")}
      ${row("Perks", "perks")}
      ${row("Job Specials", "specials", true)}
    `;

    document.getElementById("job-comparison-table").appendChild(document.createElement("hr"));
    document.getElementById("job-comparison-table").appendChild(table);
  }
}
</script>
