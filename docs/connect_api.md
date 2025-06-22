# Connect Your Torn API Key

Enter your API key below so the assistant can personalize its recommendations.

> 💡 Your key is only stored in your browser and never shared.

<form id="api-form">
  <label for="apikey"><strong>API Key:</strong></label><br>
  <input type="text" id="apikey" name="apikey" size="50" /><br><br>
  <button type="submit">Save API Key</button>
</form>

---

## Preview Your Torn Profile

<div id="torn-info"></div>

<script>
  document.getElementById("api-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const key = document.getElementById("apikey").value;
    localStorage.setItem("torn_api_key", key);
    alert("API Key saved locally!");
    loadProfile();
  });

  function loadProfile() {
    const key = localStorage.getItem("torn_api_key");
    if (!key) return;

    fetch(`https://api.torn.com/user/?selections=basic&key=${key}`)
      .then(res => res.json())
      .then(data => {
        const infoBox = document.getElementById("torn-info");
        if (data.error) {
          infoBox.innerHTML = `<p style="color:red;">Error: ${data.error.error}</p>`;
        } else {
          infoBox.innerHTML = `<p><strong>Welcome, ${data.name} (#${data.player_id})!</strong></p>`;
        }
      });
  }

  window.onload = loadProfile;
</script>
<h2>🔑 Test Your API Key</h2>
<p>Click below to check if your key is valid and has the right permissions.</p>
<button onclick="testApiKey()">✅ Test My Key</button>
<div id="key-test-result" style="margin-top:10px;"></div>

<script>
function testApiKey() {
  const key = localStorage.getItem("torn_api_key");
  const resultDiv = document.getElementById("key-test-result");

  if (!key) {
    resultDiv.innerHTML = "<p style='color:red;'>❌ No API key found. Please enter one first.</p>";
    return;
  }

  fetch(`https://api.torn.com/user/?selections=basic&key=${key}`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        resultDiv.innerHTML = `<p style='color:red;'>❌ Invalid API key: ${data.error.error}</p>`;
      } else {
        resultDiv.innerHTML = `<p style='color:green;'>✅ Key works! Welcome, ${data.name} (Level ${data.level})</p>`;
      }
    })
    .catch(err => {
      resultDiv.innerHTML = `<p style='color:red;'>❌ Something went wrong: ${err.message}</p>`;
    });
}
</script>
