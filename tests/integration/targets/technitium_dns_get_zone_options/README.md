
# Integration Tests for technitium_dns_get_zone_info

This directory contains the integration tests for the `technitium_dns_zone_delete` Ansible module, which manages the deletion of DNS zones in Technitium DNS.

## Overview

These tests ensure that info can be retrieved for all supported zones, and that the module behaves as expected in various scenarios, negative tests, and verification of zone info.

## What Is Tested

For each record type, the following phases are covered:

1. **Load Configuration**: Load `zone_test_data.yml`, `config.yml` and cleanup any existing zones.
2. **Create Zones**: Creates all zones in the `zones_to_create` dictionary list.
3. **Info Verification**: Test data returned from `technitium_dns_zone_delete` matches created zones. Test that the `zone_type` parameter returns specific zone types. Verify DNSSEC realted info is returned correctly.
6. **Negative tests**: Attempts invalid operations and asserts proper failure.

## Zone Types Covered

- Primary, Primary (DNSSEC), Forwarder, Catalog, Seconday, Stub, SecondaryForwarder, SecondaryCatalog

## Running the Tests

To run all integration tests:

```bash
ansible-test integration technitium_dns_get_zone_info
```

Or run the orchestrator playbook directly (can add vars using --extra-vars if required):

```bash
ansible-playbook roles/test_utils/playbooks/run_dns_get_zone_info_integration_test.yml
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
