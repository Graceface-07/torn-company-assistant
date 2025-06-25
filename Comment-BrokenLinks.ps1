# Path to your docs directory
$docsPath = "docs"
$targetFile = Join-Path $docsPath "main_menu.md"
$backupFile = "$targetFile.bak"

# Backup the original file
Copy-Item $targetFile $backupFile

# Read and process each line
$lines = Get-Content $targetFile
$processed = @()

foreach ($line in $lines) {
    if ($line -match "

\[[^\]

]+\]

\(([^)]+\.md)\)") {
        $linkPath = $matches[1]
        $fullPath = Join-Path $docsPath $linkPath
        if (-Not (Test-Path $fullPath)) {
            $processed += "<!-- $line -->"
        } else {
            $processed += $line
        }
    } else {
        $processed += $line
    }
}

# Write output back to the file
$processed | Set-Content $targetFile

Write-Host "✅ Done. Broken links in 'main_menu.md' have been commented out."
Write-Host "🗂️ Backup saved as: $backupFile"
