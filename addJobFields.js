const fs = require("fs");
const path = require("path");

const dir = "./docs/company_profiles";
const fieldTemplate = (jobSlug, focus = "Manual", perks = "TBD") => 
  `**Stat Focus:** ${focus}  
**Perks:** ${perks}  
**Leadership Friendly:** N/A  

**Job Specials:**  
- TBD  
---

`;

fs.readdirSync(dir).forEach(file => {
  if (!file.endsWith(".md")) return;
  const fullPath = path.join(dir, file);
  const content = fs.readFileSync(fullPath, "utf8");

  // Skip if already contains Stat Focus field
  if (content.includes("**Stat Focus:**")) return;

  const slug = file.replace(".md", "").toLowerCase().replace(/[^a-z0-9]/g, "_");
  const newFields = fieldTemplate(slug);

  // Add fields after the title (first line)
  const lines = content.split("\n");
  const titleLine = lines[0];
  const rest = lines.slice(1).join("\n");
  const newContent = `${titleLine}\n\n${newFields}${rest}`;

  fs.writeFileSync(fullPath, newContent, "utf8");
  console.log(`✅ Updated ${file}`);
});
