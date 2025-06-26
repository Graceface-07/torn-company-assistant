# ðŸ"Š Enter Your Working Stats

Before we begin the company recommender, tell us your current working stats.

---

<div style="padding: 1em; background: #f9f9f9; border: 1px solid #ddd; max-width: 400px; border-radius: 8px;">

  <label for="manual">ðŸ› ï¸ Manual:</label><br>
  <input type="number" id="manual" placeholder="e.g. 1500" style="width:100%;"><br><br>

  <label for="intelligence">ðŸ§  Intelligence:</label><br>
  <input type="number" id="intelligence" placeholder="e.g. 1200" style="width:100%;"><br><br>

  <label for="endurance">ðŸ'ª Endurance:</label><br>
  <input type="number" id="endurance" placeholder="e.g. 1800" style="width:100%;"><br><br>

  <button onclick="goToWizard()" style="padding: 0.5em 1em; font-weight: bold;">âž¡ï¸ Start Recommender</button>

</div>

<script>
function goToWizard() {
  const m = document.getElementById('manual').value || 0;
  const i = document.getElementById('intelligence').value || 0;
  const e = document.getElementById('endurance').value || 0;

  const params = new URLSearchParams({
    manual: m,
    intelligence: i,
    endurance: e
  });

  // ✅ Use correct routed path for MkDocs — no .md extension
window.location.href = '/decision_flow/company_recommender_workingstats/?' + params.toString();
}
</script>
