# GitHub Workflows

I have 4 workflows that are easy to understand:

## 1. `test.yml` - Main Testing
**Runs automatically when you:**
- Push code to GitHub
- Create a pull request  
- Click "Run workflow" button manually

**What it does:**
1. Downloads your code
2. Sets up Python and Ansible
3. Builds your collection 
4. Starts 2 Technitium DNS containers for testing
5. Runs ALL your integration tests
6. Cleans up containers when done

## 2. `test-single-module.yml` - Test One Module  
**Only runs when you manually trigger it**

**What it does:**
- Same setup as main test
- But only tests the ONE module you choose from a dropdown
- Useful for debugging specific modules

## 3. `publish.yml` - Publish to Ansible Galaxy
**Only runs when you create a GitHub release**

**What it does:**
1. Updates version in galaxy.yml to match your release tag
2. Builds the collection 
3. Publishes to Ansible Galaxy (if you have API key set up)
4. Saves collection file as GitHub artifact

## 4. `docs.yml` - Generate Documentation
**Runs automatically when you push to main or create PRs**

**What it does:**
1. Builds your collection
2. Uses antsibull-docs to generate professional module documentation  
3. Deploys to GitHub Pages (on main branch)
4. Creates documentation preview for PRs

## How to Use

### View Documentation
Your documentation will be available at:
`https://[your-username].github.io/[your-repo-name]/`

### Enable GitHub Pages
1. Go to your repository → Settings → Pages
2. Source: "GitHub Actions"  
3. That's it! The workflow will handle the rest.

### Documentation Features
- **Auto-generated**: Module docs from your docstrings
- **Professional**: Uses the same tools as official Ansible docs
- **Preview**: See docs for PRs before merging
- **Searchable**: Full-text search functionality

## Setup for Publishing

To enable publishing to Ansible Galaxy:

1. **Get your API key**:
   - Go to https://galaxy.ansible.com/me/preferences
   - Copy your API key

2. **Add it to GitHub**:
   - Go to your repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"  
   - Name: `GALAXY_API_KEY`
   - Value: paste your API key
   - Click "Add secret"

3. **That's it!** Now when you create releases, they'll automatically publish to Galaxy.
