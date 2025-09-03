
# Integration Tests for technitium_dns_delete_record

This directory contains the integration tests for the `technitium_dns_delete_record` Ansible module, which manages the deletion of DNS records in Technitium DNS.

## Overview

These tests ensure that all supported DNS record types can be deleted correctly, and that the module behaves as expected in various scenarios, including idempotency, negative tests, and verification of record deletion.

## Test Structure

- All test playbooks are in `tasks/`, one per record type (e.g. `test_delete_a_records.yml`, `test_delete_mx_records.yml`, etc).
- The main orchestrator is `tasks/main.yml`, which sets up/tears down zones and includes all record-type tests.
- Each test file is self-contained and defines its own test records inline (no external vars required).

## What Is Tested

For each record type, the following phases are covered:

1. **Create Records**: Creates records to be deleted.
2. **Check mode**: Deletes the records with `check_mode: true` to verify records would be deleted.
3. **Delete records**: Deletes the created records.
4. **Check mode**: Deletes the records with `check_mode: true` to confirm no change.
5. **Verify deletion**: Use `technitium_dns_get_record` to verify the record has been deleted.
6. **Idempotency**: Delete the records again and verify no change.
7. **Negative tests**: Attempts invalid operations and asserts proper failure.

## Record Types Covered

- A, AAAA, ANAME, APP, CAA, CNAME, DNAME, DS, FWD, HTTPS, MX, NS, PTR, SRV, SSHFP, SVCB, TLSA, TXT, UNKNOWN, URI

## Running the Tests

To run all integration tests:

```bash
ansible-test integration technitium_dns_delete_record
```

Or run the orchestrator playbook directly (can add vars using --extra-vars if required):

```bash
ansible-playbook roles/test_utils/playbooks/run_dns_delete_record_integration_test.yml
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
