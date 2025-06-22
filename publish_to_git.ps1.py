# Prompt for a commit message
$commitMessage = Read-Host "Enter commit message"

# Show current Git status
git status

# Add all changes
git add .

# Commit
git commit -m "$commitMessage"

# Push to origin
git push origin main

Write-Host "🚀 Changes pushed to GitHub!"
