# Clean spacing and formatting across all markdown files in /docs/
$root = "docs"
$mdFiles = Get-ChildItem -Path $root -Recurse -Filter *.md

foreach ($file in $mdFiles) {
    $lines = Get-Content $file.FullName
    $output = @()
    $blankCount = 0

    foreach ($line in $lines) {
        $t = $line.TrimEnd()

        # Collapse multiple blank lines into one
        if ($t -eq "") {
            $blankCount++
            if ($blankCount -le 1) { $output += "" }
        }
        else {
            $blankCount = 0

            # Optional: compress wizard headings
            if ($t -match "^#\s?💸 Profit Wizard: Step (\d+) of \d+" ) {
                $output += "## 💸 Step $($matches[1])"
                continue
            }

            # Optional: tighten "Your Answers So Far" block
            if ($t -match "^\*\*Your Answers So Far") {
                $output += "🧠 $t"
                continue
            }

            $output += $t
        }
    }

    # Save cleaned content back to file
    Set-Content -Path $file.FullName -Value $output -Encoding UTF8
    Write-Host "✅ Cleaned: $($file.FullName)"
}
