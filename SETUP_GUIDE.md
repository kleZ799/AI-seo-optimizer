# 🚀 How to Run Locally & Upload to GitHub
## AI SEO Optimizer — Complete Setup Guide

---

## PART 1 — Run on Your PC

### Step 1: Install Python (if not already installed)
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12
3. **IMPORTANT:** During install, check ✅ "Add Python to PATH"
4. Verify installation — open Command Prompt and type:
   ```
   python --version
   ```
   You should see: `Python 3.11.x`

---

### Step 2: Install Git (if not already installed)
1. Go to https://git-scm.com/download/win
2. Download and run the installer (all defaults are fine)
3. Verify:
   ```
   git --version
   ```

---

### Step 3: Download / Extract the Project Files

Place all the project files into a folder, for example:
```
C:\Projects\ai-seo-optimizer\
```

Your folder should look like:
```
ai-seo-optimizer/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── modules/
    ├── __init__.py
    ├── llm_client.py
    ├── keyword_research.py
    ├── content_optimizer.py
    ├── serp_analyzer.py
    ├── site_auditor.py
    └── meta_generator.py
```

---

### Step 4: Open a Terminal in Your Project Folder

**Windows:**
- Open File Explorer
- Navigate to your project folder
- Click the address bar, type `cmd`, press Enter

**macOS / Linux:**
- Open Terminal
- Type: `cd /path/to/ai-seo-optimizer`

---

### Step 5: Create a Virtual Environment

A virtual environment keeps your project's dependencies isolated.

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

You should now see `(venv)` at the start of your terminal line.

---

### Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs: streamlit, anthropic, requests, beautifulsoup4

Wait for all packages to finish installing (~1-2 minutes).

---

### Step 7: Run the App

```bash
streamlit run app.py
```

Your browser will automatically open to:
```
http://localhost:8501
```

If the browser doesn't open, copy that URL and paste it manually.

---

### Step 8: Get an Anthropic API Key

1. Go to: https://console.anthropic.com
2. Sign up for a free account
3. Click "API Keys" in the left sidebar
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-api03-...`)
6. Paste it into the **sidebar** of the running app

You're ready to use all 5 tools! ✅

---

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `python not found` | Add Python to PATH during install or reinstall with PATH option checked |
| `pip not found` | Use `python -m pip install -r requirements.txt` instead |
| `ModuleNotFoundError` | Make sure venv is activated (you see `(venv)`) before running |
| `Port already in use` | Run `streamlit run app.py --server.port 8502` |
| Site auditor fails | Some sites block bots — try another URL |
| API error | Double-check your Anthropic API key in the sidebar |

---

---

## PART 2 — Upload to GitHub

### Step 1: Create a GitHub Account (if needed)
Go to https://github.com and sign up for free.

---

### Step 2: Create a New Repository

1. Click the **+** icon in the top-right → "New repository"
2. Fill in:
   - **Repository name:** `ai-seo-optimizer`
   - **Description:** `AI-powered SEO tool using Claude LLM — keyword research, content optimization, SERP analysis & site auditing`
   - **Visibility:** Public (so recruiters can see it)
   - **DO NOT** check "Add a README file" (we already have one)
3. Click **Create repository**

---

### Step 3: Configure Git on Your Machine (first time only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

### Step 4: Initialise Git in Your Project Folder

Make sure your terminal is in the project folder, then:

```bash
# Initialise git
git init

# Add all files
git add .

# Make the first commit
git commit -m "Initial commit: AI SEO Optimizer with Keyword Research, Content Optimizer, SERP Analyzer, Site Auditor, and Meta Tag Generator"
```

---

### Step 5: Connect to GitHub and Push

After creating the repo on GitHub, you'll see a page with setup instructions.
Copy the remote URL (looks like `https://github.com/YOUR_USERNAME/ai-seo-optimizer.git`), then:

```bash
# Set the remote origin
git remote add origin https://github.com/YOUR_USERNAME/ai-seo-optimizer.git

# Rename branch to main
git branch -M main

# Push your code
git push -u origin main
```

GitHub will ask for your username and password.
**Note:** Use a Personal Access Token instead of your password:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token, check "repo" scope
3. Use that token as your password when prompted

---

### Step 6: Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/ai-seo-optimizer`
2. You should see all your files + the README beautifully rendered ✅

---

### Step 7: Update Your Resume / LinkedIn

Use this description on your resume:

```
AI-Powered SEO Optimization Tool | Python, LLM APIs, NLP, Streamlit, REST APIs
GitHub: github.com/YOUR_USERNAME/ai-seo-optimizer               June 2025

• Developed an AI-driven SEO tool leveraging LLMs for keyword research,
  content optimization, and SERP analysis
• Automated meta tags, headings, and content suggestions to improve
  search ranking and visibility
• Built an interactive dashboard for real-time SEO insights, site audits,
  and performance tracking
• Reduced manual SEO effort by automating analysis and recommendations,
  boosting efficiency and content quality
```

---

## Future Updates — Push Changes to GitHub

Whenever you make changes:

```bash
git add .
git commit -m "Describe what you changed"
git push
```

---

*That's everything — your project is live, professional, and ready for recruiters!* 🎉
