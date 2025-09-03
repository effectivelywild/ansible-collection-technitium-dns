# Technitium DNS Update Record Integration Test Coverage

## Overview
The `technitium_dns_update_record` integration tests provide extensive coverage of all supported DNS record types and parameters, matching the thoroughness of the `add_record` tests.

## Test Coverage

### Complete Coverage
- **Record Types**: 21 types (all supported types)
- **Test Scenarios**: 50+ detailed scenarios  
- **Parameter Coverage**: All parameters for all record types

## Record Types Tested

### Basic Record Types
1. **A Records** - IPv4 addresses with comments, TTL variations
2. **AAAA Records** - IPv6 addresses (short and full format)
3. **NS Records** - Name server delegation
4. **CNAME Records** - Canonical name aliases
5. **PTR Records** - Reverse DNS lookups

### Mail and Communication Records
6. **MX Records** - Mail exchange with multiple priorities
7. **TXT Records** - Text records (SPF, DMARC, custom)
8. **SRV Records** - Service location (SIP, XMPP, etc.)

### Security and Certificate Records
9. **CAA Records** - Certificate Authority Authorization (issue, issuewild, iodef)
10. **SSHFP Records** - SSH key fingerprints (RSA, ECDSA, Ed25519)
11. **TLSA Records** - TLS Association (DANE)
12. **DS Records** - DNSSEC Delegation Signer

### Modern/Advanced Record Types
13. **NAPTR Records** - Name Authority Pointer (ENUM)
14. **DNAME Records** - Delegation name (domain aliasing)
15. **SVCB Records** - Service Binding
16. **HTTPS Records** - HTTPS Service Binding
17. **URI Records** - Uniform Resource Identifier
18. **ANAME Records** - Address Name (CNAME-like for apex)
19. **FWD Records** - DNS Forwarder configuration
20. **APP Records** - Application-specific records
21. **UNKNOWN Records** - Generic record support

## Test Phases
- **Record Creation**: All 21 record types with realistic parameters
- **Parameter Updates**: Test all parameter combinations for each record type
- **Value Verification**: Ensure updated values are correctly applied
- **Idempotency Testing**: Verify no changes when values match current state
- **Edge Case Testing**: TTL limits, long domain names, special characters
- **Negative Testing**: Invalid parameters, missing required fields, unsupported combinations

## Parameter Coverage Examples

### A Records
- Basic IP updates: `192.168.1.10` → `192.168.1.11`
- TTL changes: `3600` → `7200`
- Comments: `"Original"` → `"Updated with émojis ✓"`

### SRV Records
- Priority/Weight: `10/60` → `5/100`
- Port changes: `5060` → `5061`
- Target updates: `server1` → `server2`

### CAA Records
- Flags: `0` → `128`
- Tag changes: `"issue"` → `"issuewild"`
- Value updates: `"letsencrypt.org"` → `";"`

### SSHFP Records
- Algorithm upgrades: `RSA` → `Ed25519`
- Fingerprint type: `SHA1` → `SHA256`
- Key rotations with new fingerprints

## Special Test Scenarios

### Parameter Variations
- **TTL Edge Cases**: Min (1) to Max (2^31-1)
- **Long Domain Names**: 63+ character subdomains
- **International Domains**: Punycode (xn--) support
- **Special Characters**: Unicode in comments and values

### Idempotency Scenarios
- Same value updates (should return `changed: false`)
- Multiple record types in same zone
- Complex parameter combinations

### Negative Test Coverage
- **Missing Required Parameters**: Each record type's required fields
- **Invalid Values**: Malformed IPs, negative TTLs, invalid choices
- **Unsupported Parameters**: Wrong parameters for record types
- **Empty Values**: Blank domains, empty targets
- **Authentication**: Invalid API tokens

## Usage

### Run Tests
```bash
ansible-test integration technitium_dns_update_record
```

### Test Data File
The test data is located in:
```bash
tests/integration/targets/technitium_dns_update_record/vars/test_data.yml
```

## Test Data Structure

### Test Records
```yaml
test_records:
  - domain: "example.zone.com"
    type: "A"
    ipAddress: "192.168.1.10"      # Current value
    newIpAddress: "192.168.1.11"   # Update value
    ttl: 3600
    newTtl: 7200
    test_scenario: "descriptive_name"
```

### Parameter Variations
```yaml
parameter_variation_tests:
  - domain: "edge-case.zone.com"
    # Tests edge cases, limits, special values
```

### Negative Tests
```yaml
negative_tests:
  - domain: "invalid-test.zone.com"
    type: "A"
    newTtl: -1  # Invalid value
    expected_error: "invalid"
```

## Benefits

1. **Complete Coverage**: All DNS record types and parameters tested
2. **Real-world Scenarios**: Practical use cases for each record type
3. **Regression Prevention**: Catches parameter type issues (like the CAA flags bug)
4. **Idempotency Verification**: Ensures proper change detection
5. **Error Handling**: Comprehensive negative test coverage
6. **Documentation**: Tests serve as usage examples

## Maintenance

- **Adding New Record Types**: Add to `comprehensive_test_data.yml`
- **New Parameters**: Include in test scenarios with valid/invalid cases
- **API Changes**: Update test data to match new API requirements
- **Performance**: Tests can be selectively enabled/disabled via variables