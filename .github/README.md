# GitHub Workflows

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
