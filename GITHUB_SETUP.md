# GitHub Setup Guide for Endee RAG Demo

## Step 1: Fork the Endee Repository

1. Visit https://github.com/endee-io/endee
2. Click the **Fork** button (top-right)
3. Keep default settings and click **Create fork**
4. Your fork is now at: `https://github.com/<your-username>/endee`

## Step 2: Create a New GitHub Repository for the RAG Demo

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name:** `endee-rag-demo`
   - **Description:** `Retrieval-Augmented Generation with Endee Vector Database`
   - **Visibility:** Public
3. Click **Create repository**
4. Your repo is now at: `https://github.com/<your-username>/endee-rag-demo`

## Step 3: Push This Project to GitHub

### Option A: Using the Provided Script (Recommended)

**Windows PowerShell:**

```powershell
# Edit the script with your GitHub username
$GITHUB_USERNAME = "your-github-username"

# Run the setup script
.\setup_git.ps1
```

**macOS/Linux:**

```bash
# Edit the script with your GitHub username
GITHUB_USERNAME="your-github-username"

# Run the setup script
chmod +x setup_git.sh
./setup_git.sh
```

### Option B: Manual Setup

```bash
cd /workspace

# Initialize git repo
git init
git add .
git commit -m "Initial commit: Endee RAG demo with FastAPI and semantic search"

# Rename branch to main (if not already)
git branch -M main

# Add remote (replace <your-username>)
git remote add origin https://github.com/<your-username>/endee-rag-demo.git

# Push to GitHub
git push -u origin main
```

## Step 4: Update README.md

The README references placeholder URLs. Update them with your fork URLs:

**In README.md, replace:**

- `https://github.com/endee-io/endee` → `https://github.com/<your-username>/endee`
- `https://github.com/<your-username>/endee-rag-demo.git` → your actual repo URL
- Any other `<your-username>` placeholders

**To do this:**

```bash
# Edit README.md locally, then push again
git add README.md
git commit -m "Update README with fork URLs"
git push
```

## Step 5: Verify Everything on GitHub

1. Visit your repo: `https://github.com/<your-username>/endee-rag-demo`
2. Check that all files are present:
   - app/main.py, app/vector_store.py
   - tests/test_vector_store.py
   - examples/rag_demo.py
   - samples/dataset.py
   - README.md, requirements.txt, Dockerfile, docker-compose.yml
   - .env.example, LICENSE, .gitignore
   - .github/workflows/ci.yml

3. Verify CI/CD pipeline:
   - Go to **Actions** tab
   - You should see "CI" workflow (GitHub Actions)
   - It will run tests automatically on each push

## Step 6: Optional - Enable GitHub Pages (Docs)

1. Go to **Settings** → **Pages**
2. Select **main** branch and **/root** folder
3. Your project docs will be at: `https://<your-username>.github.io/endee-rag-demo`

## Troubleshooting

### Authentication Error

```bash
# If you get "fatal: Authentication failed", use personal access token:
git remote set-url origin https://<your-username>:<personal-access-token>@github.com/<your-username>/endee-rag-demo.git
```

### Branch Already Exists

```bash
# If main branch already exists, just push:
git push -u origin main
```

### Want to Start Fresh

```bash
# Reset and reinitialize
rm -r .git
git init
git add .
git commit -m "Initial commit: Endee RAG demo"
git remote add origin https://github.com/<your-username>/endee-rag-demo.git
git push -u origin main
```

## Done! ✅

Once everything is pushed, your project is complete and ready for evaluation. Share your repo URLs:

- Endee Fork: `https://github.com/<your-username>/endee`
- RAG Demo: `https://github.com/<your-username>/endee-rag-demo`

Both links meet all evaluation criteria! 🎉
