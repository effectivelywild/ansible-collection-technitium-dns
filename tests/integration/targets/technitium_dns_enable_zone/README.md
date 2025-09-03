# technitium_dns_enable_zone Integration Tests

This directory contains comprehensive integration tests for the `technitium_dns_enable_zone` module.

## Test Structure

- **tasks/main.yml**: Main test playbook with comprehensive test phases
- **vars/config.yml**: Test environment configuration 
- **vars/zone_test_data.yml**: Test zone definitions and scenarios

## Test Phases

1. **Setup**: Load configuration and create test zones
2. **Preparation**: Disable zones to test enable functionality
3. **Check Mode**: Validate check mode behavior
4. **Enable Operations**: Test actual zone enabling
5. **Idempotency**: Verify idempotent behavior
6. **Negative Tests**: Test error conditions
7. **Cleanup**: Remove test zones

## Test Scenarios

The tests validate:
- Enable functionality for various zone types (Primary, Forwarder, Catalog, Secondary, Stub)
- Check mode behavior
- Idempotent operations
- Error handling for invalid inputs
- API authentication failures

## Configuration

Tests expect the following variables to be defined:
- `technitium_api_url`: Technitium DNS API base URL
- `technitium_api_token`: Valid API token
- `technitium_api_port`: API port (default: 5380)
- `validate_certs`: SSL certificate validation (default: true)