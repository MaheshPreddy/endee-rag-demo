# PowerShell Script to initialize and push to GitHub
# Usage: .\setup_git.ps1

param(
    [string]$GitHubUsername = "",
    [string]$CommitMessage = "Initial commit: Endee RAG demo with FastAPI and semantic search"
)

# Prompt for GitHub username if not provided
if (-not $GitHubUsername) {
    $GitHubUsername = Read-Host "Enter your GitHub username"
}

$repoUrl = "https://github.com/$GitHubUsername/endee-rag-demo.git"

Write-Host "=" * 70
Write-Host "GitHub Setup for Endee RAG Demo"
Write-Host "=" * 70
Write-Host ""
Write-Host "GitHub Username: $GitHubUsername"
Write-Host "Repository URL:  $repoUrl"
Write-Host ""

# Confirm before proceeding
$confirm = Read-Host "Proceed with git setup? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Cancelled."
    exit 1
}

Write-Host ""
Write-Host "Step 1: Initializing git repository..."
git init
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to initialize git repository"
    exit 1
}

Write-Host "Step 2: Staging all files..."
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to stage files"
    exit 1
}

Write-Host "Step 3: Creating initial commit..."
git commit -m $CommitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to create commit"
    exit 1
}

Write-Host "Step 4: Setting main branch..."
git branch -M main
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to rename branch"
    exit 1
}

Write-Host "Step 5: Adding remote origin..."
git remote add origin $repoUrl
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to add remote"
    exit 1
}

Write-Host "Step 6: Pushing to GitHub..."
Write-Host "A browser window may open to authenticate. Please complete the authentication."
Write-Host ""
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" * 70
    Write-Host "SUCCESS! ✓"
    Write-Host "=" * 70
    Write-Host ""
    Write-Host "Your project is now on GitHub!"
    Write-Host "Repository: $repoUrl"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1. Visit your repository on GitHub"
    Write-Host "2. Check the Actions tab to see CI/CD running"
    Write-Host "3. Update README.md with your fork URLs (if needed)"
    Write-Host "4. Share your repository links in your submission"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERROR: Failed to push to GitHub"
    Write-Host "Please check your authentication and try again."
    exit 1
}
