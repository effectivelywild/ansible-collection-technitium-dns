# Technitium DNS Ansible Collection Documentation

This directory contains the documentation build configuration for the Technitium DNS Ansible Collection.

## What Gets Generated

The documentation includes:

- **Module Documentation**: Auto-generated from module docstrings
- **Role Documentation**: Documentation for any roles in the collection
- **Examples**: Usage examples and playbooks
- **API Reference**: Complete parameter and return value documentation

## Local Documentation Building

To build documentation locally:

```bash
# Install requirements
pip install ansible antsibull-docs sphinx-rtd-theme

# Build the collection
ansible-galaxy collection build .
ansible-galaxy collection install effectivelywild-technitium_dns-*.tar.gz

# Generate documentation
mkdir -p docs/build
antsibull-docs sphinx-init --use-current --dest-dir ./docs/build effectivelywild.technitium_dns

# Build HTML docs
cd docs/build
pip install -r requirements.txt
make html

# View docs
open _build/html/index.html
```

## GitHub Pages

The documentation is automatically built and deployed to GitHub Pages when changes are pushed to the main branch.

Access your documentation at: `https://[username].github.io/[repository-name]/`