$docsDir = "docs"
$mdFiles = Get-ChildItem -Path $docsDir -Filter "*.md" -Recurse

foreach ($file in $mdFiles) {
    $fullPath = $file.FullName
    $backupPath = "$fullPath.bak"

    # Backup the file
    Copy-Item $fullPath $backupPath -Force

    $lines = Get-Content $fullPath
    $processed = @()

    foreach ($line in $lines) {
        if ($line -match "

\[.*?\]

\(([^)]+\.md)\)") {
            $target = $matches[1]
            $absolutePath = Join-Path $file.Directory.Parent.FullName $target

            if (-not (Test-Path $absolutePath)) {
                $processed += "<!-- $line -->"
                Write-Host "❌ Commented out link: $target"
            } else {
                $processed += $line
            }
        } else {
            $processed += $line
        }
    }

    $processed | Set-Content $fullPath
}

Write-Host "`n✅ Done! Broken .md links commented. Backups saved with .bak extension."
