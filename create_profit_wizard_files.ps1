# Set your base path for the wizard
$basePath = "docs\profit_wizard"

# Make the directory if it doesn’t exist
if (-Not (Test-Path $basePath)) {
    New-Item -ItemType Directory -Path $basePath -Force | Out-Null
}

# List of file names to generate
$files = @(
    "1a_bank_stock_access.md",
    "1b_bank_stock_understanding.md",
    "2_level.md",
    "3_suitcase.md",
    "4_bank_usage.md",
    "5_merits.md",
    "6_faction.md",
    "7_five_star_company.md",
    "8_market_access.md"
)

# Create each file with front matter and header
foreach ($file in $files) {
    $fullPath = Join-Path $basePath $file
    $stepNum = $files.IndexOf($file) + 1
    $titleText = ($file -replace '^\d+[a-z]?_', '') -replace '-', ' '
    $prettyTitle = ($titleText -replace '\.md$', '') -replace '\b\w', { $_.Value.ToUpper() }

    $frontMatter = @"
---
title: Step $stepNum — $prettyTitle
---
"@

    $body = @"
# 💸 Profit Wizard: Step $stepNum of $($files.Count)

🧠 **Your Answers So Far:**  
_None yet_

---

## _Coming soon — this step will ask about **$prettyTitle**._
"@

    $content = $frontMatter + "`n" + $body
    Set-Content -Path $fullPath -Value $content -Encoding UTF8
    Write-Host "✅ Created: $file"
}
