# technitium_dns_unsign_zone integration tests

Integration tests for the `technitium_dns_unsign_zone` module.

## Test coverage

These tests verify:
- Basic functionality of unsigning DNSSEC zones
- Check mode support
- Idempotency (attempting to unsign already unsigned zones)
- Error handling for invalid tokens and non-existent zones

## Prerequisites

- A running Technitium DNS server
- Valid API token
- Test environment configured in `integration_config.yml`

## Test structure

1. **Setup**: Create and sign test zones
2. **Unsign zones**: Test the unsign functionality
3. **Verify**: Confirm zones are unsigned
4. **Idempotency**: Test re-running on already unsigned zones
5. **Error cases**: Test failure scenarios
6. **Cleanup**: Remove test zones