# GitHub Workflows for Technitium DNS Ansible Collection

This directory contains GitHub Actions workflows for automated testing and release management of the Technitium DNS Ansible Collection.

## Workflows

### 1. Integration Tests (`integration-tests.yml`)
- **Triggers**: Push to main/develop, PRs to main, manual dispatch
- **Purpose**: Runs comprehensive integration tests against a live Technitium DNS server
- **Matrix Testing**: Multiple Python versions (3.9, 3.10, 3.11) and Ansible versions
- **Requirements**: Requires repository secrets for API access

### 2. Ansible Lint (`ansible-lint.yml`)
- **Triggers**: Push to main/develop, PRs to main, manual dispatch
- **Purpose**: Validates Ansible code quality and YAML syntax
- **Tools**: ansible-lint, yamllint

### 3. Unit Tests (`unit-tests.yml`)
- **Triggers**: Push to main/develop, PRs to main, manual dispatch
- **Purpose**: Validates Python syntax and basic module imports
- **Matrix Testing**: Multiple Python versions

### 4. Individual Module Tests (`module-tests.yml`)
- **Triggers**: Manual dispatch only
- **Purpose**: Test specific modules individually
- **Usage**: Select module from dropdown in GitHub Actions interface

### 5. Release (`release.yml`)
- **Triggers**: Published releases, manual dispatch
- **Purpose**: Builds and publishes collection to Ansible Galaxy
- **Requirements**: GALAXY_API_KEY secret for publishing

## Required Repository Secrets

### For Integration Tests
- `TECHNITIUM_API_URL`: Your Technitium DNS Server URL (e.g., `https://dns.example.com`)
- `TECHNITIUM_API_TOKEN`: API authentication token
- `TECHNITIUM_API_PORT`: API port (optional, defaults to 5380)
- `VALIDATE_CERTS`: Certificate validation (optional, defaults to false)
- `NOTIFY_NAME_SERVER`: Notify name server for testing (optional)
- `DEBUG`: Enable debug output (optional, defaults to false)

### For Releases
- `GALAXY_API_KEY`: Ansible Galaxy API key for publishing collections

## Setting Up Secrets

1. Go to your repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each required secret with the appropriate value

## Running Tests Locally

### Integration Tests
```bash
# Set environment variables
export TECHNITIUM_API_URL="https://your-dns-server.com"
export TECHNITIUM_API_TOKEN="your-api-token"
export TECHNITIUM_API_PORT="5380"
export VALIDATE_CERTS="false"

# Build and install collection
ansible-galaxy collection build .
ansible-galaxy collection install effectivelywild-technitium_dns-*.tar.gz

# Run all integration tests
cd ~/.ansible/collections/ansible_collections/effectivelywild/technitium_dns
ansible-playbook -i tests/integration/inventory \
  roles/test_utils/playbooks/run_all_integration_tests.yml -v
```

### Individual Module Tests
```bash
# Run specific module test (example: add_record)
ansible-playbook -i tests/integration/inventory \
  roles/test_utils/playbooks/run_dns_add_record_integration_test.yml -v
```

### Linting
```bash
# Install linting tools
pip install ansible-lint yamllint

# Run linting
ansible-lint .
yamllint -d relaxed .
```

## Workflow Status

The workflows will show status badges in your repository. You can add these to your main README:

```markdown
![Integration Tests](https://github.com/your-org/your-repo/workflows/Integration%20Tests/badge.svg)
![Ansible Lint](https://github.com/your-org/your-repo/workflows/Ansible%20Lint/badge.svg)
![Unit Tests](https://github.com/your-org/your-repo/workflows/Unit%20Tests/badge.svg)
```

## Troubleshooting

### Integration Tests Failing
1. Verify your Technitium DNS server is accessible
2. Check that API credentials are correct
3. Ensure the server has the necessary zones and permissions
4. Review the test logs for specific error messages

### Lint Failures
1. Fix any ansible-lint rule violations
2. Ensure YAML files are properly formatted
3. Check that all required metadata is present

### Module Import Errors
1. Verify Python syntax in module files
2. Check that required dependencies are available
3. Review module imports and library usage