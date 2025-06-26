<h2>🏢 Analyze My Company</h2>
<button onclick="analyzeCompany()" style="padding:6px 12px;">🔍 Analyze</button>
<div id="company-result" style="margin-top:15px; font-family: sans-serif;"></div>

<script>
function analyzeCompany() {
  const key = localStorage.getItem("torn_api_key");
  const div = document.getElementById("company-result");
  if (!key) {
    div.innerHTML = "<p style='color:red;'>❌ No API key found. Please enter or save one first.</p>";
    return;
  }

  fetch(`https://api.torn.com/company/?key=${key}`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        div.innerHTML = `<p style='color:red;'>❌ API Error: ${data.error.error}</p>`;
        return;
      }

      if (!data.company || !data.company.name) {
        div.innerHTML = `<p style='color:orange;'>❓ Key is valid, but no company data returned.<br>Make sure you're in a company and your API key has <strong>Company</strong> permission.</p>`;
        return;
      }

      const c = data.company;
      const revenuePer = Math.round(c.weekly_income / c.employees_hired || 1).toLocaleString();

      let html = `
        <p style="color:green; font-weight:bold;">✅ Loaded: ${c.name}</p>
        <ul>
          <li>🏢 ID: ${c.ID}</li>
          <li>🏷️ Type: ${c.company_type}</li>
          <li>⭐ Rating: ${c.rating} stars</li>
          <li>👥 Staffed: ${c.employees_hired} / ${c.employees_capacity}</li>
          <li>📈 Weekly Income: \$${c.weekly_income.toLocaleString()} (${revenuePer} per employee)</li>
          <li>📅 Days Old: ${c.days_old}</li>
        </ul>
      `;

      html += `<h3>👤 Employees (${Object.keys(c.employees).length})</h3>`;
      html += `<table border="1" cellpadding="6" style="border-collapse: collapse;">
        <tr><th>Name</th><th>Role</th><th>Days</th><th>Status</th></tr>`;

      for (const id in c.employees) {
        const e = c.employees[id];
        const status = e.status.state === "Hospital" || e.status.state === "Traveling"
          ? `<span style="color:orange;">${e.status.description}</span>`
          : `<span style="color:green;">${e.status.description}</span>`;

        html += `<tr>
          <td>${e.name}</td>
          <td>${e.position}</td>
          <td>${e.days_in_company}</td>
          <td>${status}</td>
        </tr>`;
      }

      html += `</table><br>`;

      // Quick suggestion logic based on roles
      const roles = Object.values(c.employees).map(e => e.position);
      const totalDrivers = roles.filter(r => r.toLowerCase().includes("driver")).length;
      const totalManagers = roles.filter(r => r.toLowerCase().includes("manager")).length;

      html += `<h4>🧠 Suggestions</h4><ul>`;
      if (totalDrivers < 3) html += `<li>🚛 Consider hiring more Drivers to optimize transport speed.</li>`;
      if (totalManagers < 2) html += `<li>📊 Add a second manager to keep efficiency high.</li>`;
      if (c.employees_hired === c.employees_capacity) html += `<li>👥 Your staff capacity is maxed—consider upgrading for growth.</li>`;
      html += `</ul>`;

      div.innerHTML = html;
    })
    .catch(err => {
      div.innerHTML = `<p style="color:red;">❌ Fetch error: ${err.message}</p>`;
    });
}
</script>
