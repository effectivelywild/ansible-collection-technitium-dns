
# Integration Tests for technitium_dns_zone_create

This directory contains the integration tests for the `technitium_dns_zone_create` Ansible module, which manages the creation of DNS zones in Technitium DNS.

## Overview

These tests ensure that all supported DNS zones can be created correctly, and that the module behaves as expected in various scenarios, including idempotency, negative tests, and verification of zone creation.

## Test Structure

- Zone information is loaded from `vars/zone_test_data.yml` and passed to `roles/test_utils/zone_creation.yml` for creation
- Zones are created and verified 

## What Is Tested

For each record type, the following phases are covered:

1. **Load Configuration**: Load `zone_test_data.yml` and `config.yml` and cleanup any existing zones.
2. **Check mode**: Creates zones with `check_mode: true` to verify zones would be created and asserts creation.
3. **Create Zones**: Creates all zones in the `zones_to_create` dictionary list and asserts creation.
4. **Verify Zone Parameters**: Uses `technitium_dns_get_zone_info`,`technitium_dns_get_zone_options` and `technitium_dns_get_record` to get zone info and asserts parameters of created zones match `zones_to_create`.
5. **Idempotecy Testing**: Add records again, assert no change, also tests check_mode.
6. **Negative tests**: Attempts invalid operations and asserts proper failure.

## Zone Types Covered

- Primary, Primary (DNSSEC), Forwarder, Catalog, Seconday, Stub, SecondaryForwarder, SecondaryCatalog

## Running the Tests

To run all integration tests:

```bash
ansible-test integration technitium_dns_create_zone
```

Or run the orchestrator playbook directly (can add vars using --extra-vars if required):

```bash
ansible-playbook roles/test_utils/playbooks/run_dns_create_zone_integration_test.yml
```

## Required Variables

- `technitium_api_url`: API URL (default: http://localhost)
- `technitium_api_token`: API authentication token
- `technitium_api_port`: API port (default: 5380)
- `zones_to_create`: Dictionary key containing zones to create
- `test_suffix`: Name of the parent zone

## Test Environment

Requires at least one Technitium DNS server with a valid API token and a second server that the `Secondary` and `Stub` zones can complete zone transfer with.

## Debug Mode

Set `debug: true` to enable detailed output during test execution.
