# Define root docs path
$root = "docs"
$gearDir = Join-Path $root "gear"
$weaponsDir = Join-Path $gearDir "weapons"
$armourDir = Join-Path $gearDir "armour"

# Create required directories
$paths = @($gearDir, $weaponsDir, $armourDir)
foreach ($path in $paths) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
    }
}

# Define placeholder files and titles
$files = @(
    @{ Path = "$gearDir/overview.md";               Title = "Weapons & Armour Overview" },
    @{ Path = "$weaponsDir/melee.md";               Title = "Melee Weapons" },
    @{ Path = "$weaponsDir/pistols.md";             Title = "Pistols" },
    @{ Path = "$weaponsDir/smgs.md";                Title = "Submachine Guns (SMGs)" },
    @{ Path = "$weaponsDir/rifles.md";              Title = "Rifles" },
    @{ Path = "$weaponsDir/heavy.md";               Title = "Heavy Weapons" },
    @{ Path = "$armourDir/light.md";                Title = "Light Armour" },
    @{ Path = "$armourDir/medium.md";               Title = "Medium Armour" },
    @{ Path = "$armourDir/heavy.md";                Title = "Heavy Armour" }
)

# Write placeholder content
foreach ($file in $files) {
    $title = $file.Title
    $path = $file.Path
    $content = "# $title`n`nThis page is under construction.`n`n> Tactical data and SWOT analysis coming soon."
    Set-Content -Path $path -Value $content -Encoding UTF8
    Write-Host ("Created: " + $path)
}

Write-Host "`nAll gear module files and folders generated successfully."
