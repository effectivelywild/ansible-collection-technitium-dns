
# Integration Tests for technitium_dns_sign_zone

This directory contains the integration tests for the `technitium_dns_sign_zone` Ansible module, which manages the signing of Primary DNS zones in Technitium DNS.

## Overview

These tests ensure that DNS zones can be signed with an array of options and asserts those options are configured as expected.

Check mode is tested when signing and the idempotency test.

## What Is Tested

1. **Load Configuration**: Load `zone_test_data.yml`, `config.yml` and cleanup any existing zones.
2. **Create Zones**: Creates all zones in the `dnssec_test_matrix` dictionary list.
3. **Signs Zones**: Signs all zones using parameters in `dnssec_test_matrix`. 
4. **Verification**: Verifies all signing parameters match expected values.
5. **Idempotency test**: Attempts to sign the zone again, also tests check_mode. 
6. **Failure Tests**: Attempts invalid operations and asserts proper failure.

## Running the Tests

To run all integration tests:

```bash
ansible-test integration technitium_dns_sign_zone
```

Or run the orchestrator playbook directly (can add vars using --extra-vars if required):

```bash
ansible-playbook roles/test_utils/playbooks/run_dns_sign_zone_integration_test.yml
```

## Required Variables

- `technitium_api_url`: API URL (default: http://localhost)
- `technitium_api_token`: API authentication token
- `technitium_api_port`: API port (default: 5380)
- `dnssec_test_matrix`: Dictionary key containing zones to create
- `test_suffix`: Name of the parent zone

## Test Environment

Requires at least one Technitium DNS server with a valid API token.

## Debug Mode

Set `debug: true` to enable detailed output during test execution.