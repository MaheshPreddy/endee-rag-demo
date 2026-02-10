#!/bin/bash
# Bash script to initialize and push to GitHub
# Usage: ./setup_git.sh

set -e  # Exit on error

GITHUB_USERNAME="${1:-}"
COMMIT_MESSAGE="Initial commit: Endee RAG demo with FastAPI and semantic search"

# Prompt for GitHub username if not provided
if [ -z "$GITHUB_USERNAME" ]; then
    read -p "Enter your GitHub username: " GITHUB_USERNAME
fi

REPO_URL="https://github.com/$GITHUB_USERNAME/endee-rag-demo.git"

echo "======================================================================="
echo "GitHub Setup for Endee RAG Demo"
echo "======================================================================="
echo ""
echo "GitHub Username: $GITHUB_USERNAME"
echo "Repository URL:  $REPO_URL"
echo ""

# Confirm before proceeding
read -p "Proceed with git setup? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "Step 1: Initializing git repository..."
git init

echo "Step 2: Staging all files..."
git add .

echo "Step 3: Creating initial commit..."
git commit -m "$COMMIT_MESSAGE"

echo "Step 4: Setting main branch..."
git branch -M main

echo "Step 5: Adding remote origin..."
git remote add origin "$REPO_URL"

echo "Step 6: Pushing to GitHub..."
echo "A browser window may open to authenticate. Please complete the authentication."
echo ""
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================="
    echo "SUCCESS! ✓"
    echo "======================================================================="
    echo ""
    echo "Your project is now on GitHub!"
    echo "Repository: $REPO_URL"
    echo ""
    echo "Next steps:"
    echo "1. Visit your repository on GitHub"
    echo "2. Check the Actions tab to see CI/CD running"
    echo "3. Update README.md with your fork URLs (if needed)"
    echo "4. Share your repository links in your submission"
    echo ""
else
    echo ""
    echo "ERROR: Failed to push to GitHub"
    echo "Please check your authentication and try again."
    exit 1
fi
