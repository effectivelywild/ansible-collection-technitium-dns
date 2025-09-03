
# Integration Tests for technitium_dns_add_record

This directory contains the integration tests for the `technitium_dns_add_record` Ansible module, which manages the creation of DNS records in Technitium DNS.

## Overview

These tests ensure that all supported DNS record types can be created correctly, and that the module behaves as expected in various scenarios, including idempotency, negative tests, and verification of record creation.

## Test Structure

- All test playbooks are in `tasks/`, one per record type (e.g. `test_add_a_records.yml`, `test_add_mx_records.yml`, etc).
- The main orchestrator is `tasks/main.yml`, which sets up/tears down zones and includes all record-type tests.
- Each test file is self-contained and defines its own test records inline (no external vars required).

## What Is Tested

For each record type, the following phases are covered:

1. **Check mode plan**: Ensures the module reports changes when records would be added.
2. **Verify absence**: Uses `technitium_dns_get_record` to confirm records do not exist before creation.
3. **Create records**: Adds records and asserts they are created.
4. **Verify presence**: Confirms records exist and match parameters.
5. **Re-plan**: Ensures re-adding is idempotent (no changes).
6. **Overwrite**: (where supported) Overwrites an existing record and verifies the update.
7. **Negative tests**: Attempts invalid operations and asserts proper failure.

## Record Types Covered

- A, AAAA, ANAME, APP, CAA, CNAME, DNAME, DS, FWD, HTTPS, MX, NS, PTR, SRV, SSHFP, SVCB, TLSA, TXT, UNKNOWN, URI

## Running the Tests

To run all integration tests:

```bash
ansible-test integration technitium_dns_add_record
```

Or run the orchestrator playbook directly (can add vars using --extra-vars if required):

```bash
ansible-playbook roles/test_utils/playbooks/run_dns_add_record_integration_test.yml
```

## Required Variables

- `technitium_api_url`: API URL (default: http://localhost)
- `technitium_api_token`: API authentication token
- `technitium_api_port`: API port (default: 5380)
- `zones_to_create`: Dictionary key containing zones to create
- `primary_zone_name`: Name of the primary zone used in testing
- `primary_sec_zone_name`: Name of the DNSSEC signed zone used in testing
- `forwarder_zone_name`: Name of the forwarder zone used in testing

## Test Environment

Requires at least one Technitium DNS server with a valid API token.

The test suite creates and cleans up its own zones:

- Primary zone: `test-primary.example.com`
- Secondary zone: `test-secondary.example.com`
- Forwarder zone: `test-forwarder.example.com`

## Debug Mode

Set `debug: true` to enable detailed output during test execution.
