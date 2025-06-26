$basePath = "docs\profit"
New-Item -ItemType Directory -Force -Path $basePath | Out-Null

$files = @{
    "index.md" = "# Profit Paths`n`nChoose your earning style."
    "trading.md" = "# Trading`n`nFlip goods, snipe deals, arbitrage."
    "dump-hunting.md" = "# Dump Hunting`n`nScour the dump for resaleables."
    "job-cans.md" = "# Job Cans`n`nTurn job points into energy cans."
    "slutting.md" = '# Slutting and Loss Selling`n`nGet paid to take losses.'
    "drug-running.md" = "# Drug Running`n`nImport/export profit game."
    "blood-farming.md" = "# Blood Farming`n`nSell rare blood types for markup."
    "morphine-sales.md" = "# Morphine Sales`n`nSell meds to hospital players."
    "passive-income.md" = "# Passive Income`n`nEarn through dividends and stocks."
    "faction-income.md" = "# Faction Income`n`nShared perks and earnings."
    "investment-tips.md" = "# Investment Tips`n`nLong-term growth strategies."
}

foreach ($entry in $files.GetEnumerator()) {
    $fullPath = Join-Path $basePath $entry.Key
    $entry.Value | Set-Content -Path $fullPath -Encoding UTF8
}

Write-Host "✅ Profit module initialized at $basePath"
