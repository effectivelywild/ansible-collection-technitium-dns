# Ansible Collection - technetium.dns

Documentation for the collection.

## DNS Record Update Parameters

The `technitium_dns_update_record` module uses special naming conventions to specify the updated values for existing DNS records. Unfortunately not all record parameters follow the same convention based on the API. Below is the complete list of parameters that require you provide updated values with special naming when updating.

### Update Parameter Patterns

Most parameters follow the `new<parameter>` pattern, but NAPTR records use `naptrNew<parameter>` instead:
- **Standard pattern**: `new<Parameter>` (e.g., `newIpAddress`, `newText`)  
- **NAPTR pattern**: `naptrNew<Parameter>` (e.g., `naptrNewFlags`, `naptrNewOrder`)

### Complete List of Update Parameters

The following parameters use special naming conventions in `technitium_dns_update_record`:

| Parameter | Record Types | Description |
|-----------|--------------|-------------|
| `naptrNewFlags` | NAPTR | New flags value |
| `naptrNewOrder` | NAPTR | New order value |
| `naptrNewPreference` | NAPTR | New preference value |
| `naptrNewRegexp` | NAPTR | New regular expression |
| `naptrNewReplacement` | NAPTR | New replacement string |
| `naptrNewServices` | NAPTR | New services value |
| `newAName` | ANAME | New ANAME domain name |
| `newAlgorithm` | DS | New algorithm for DS record |
| `newDigest` | DS | New digest for DS record |
| `newDigestType` | DS | New digest type for DS record |
| `newDomain` | All | New domain name (for renaming records) |
| `newExchange` | MX | New exchange domain name |
| `newFlags` | CAA | New flags value |
| `newForwarder` | FWD | New forwarder address |
| `newIpAddress` | A, AAAA | New IP address |
| `newKeyTag` | DS | New key tag for DS record |
| `newMailbox` | RP | New email address value |
| `newNameServer` | NS | New name server domain name |
| `newPreference` | MX | New preference value |
| `newPriority` | SRV | New priority value |
| `newProtocol` | FWD | New protocol value |
| `newPtrName` | PTR | New PTR domain name |
| `newRData` | UNKNOWN | New record data for unknown record types |
| `newSplitText` | TXT | New split text value |
| `newSrvPort` | SRV | New port value |
| `newSshfpAlgorithm` | SSHFP | New SSHFP algorithm |
| `newSshfpFingerprint` | SSHFP | New SSHFP fingerprint |
| `newSshfpFingerprintType` | SSHFP | New SSHFP fingerprint type |
| `newSvcParams` | SVCB, HTTPS | New service parameters |
| `newSvcPriority` | SVCB, HTTPS | New service priority |
| `newSvcTargetName` | SVCB, HTTPS | New service target name |
| `newTag` | CAA | New tag value |
| `newTarget` | SRV | New target value |
| `newText` | TXT | New text value |
| `newTlsaCertificateAssociationData` | TLSA | New TLSA certificate association data |
| `newTlsaCertificateUsage` | TLSA | New TLSA certificate usage |
| `newTlsaMatchingType` | TLSA | New TLSA matching type |
| `newTlsaSelector` | TLSA | New TLSA selector |
| `newTxtDomain` | RP | New TXT record domain name |
| `newUri` | URI | New URI value |
| `newUriPriority` | URI | New URI priority |
| `newUriWeight` | URI | New URI weight |
| `newValue` | CAA | New CAA record value |
| `newWeight` | SRV | New weight value |

### Usage Example

```yaml
- name: Update A record IP address
  technitium_dns_update_record:
    api_url: "http://localhost"
    api_token: "your_api_token"
    name: "www.example.com"
    type: "A"
    ipAddress: "192.168.1.100"      # Current IP (for identification)
    newIpAddress: "192.168.1.101"   # New IP (target value)

- name: Update MX record
  technitium_dns_update_record:
    api_url: "http://localhost"
    api_token: "your_api_token"
    name: "example.com"
    type: "MX"
    preference: 10                   # Current preference
    exchange: "old-mail.example.com" # Current exchange
    newPreference: 20                # New preference
    newExchange: "new-mail.example.com" # New exchange

- name: Update NAPTR record (note the different naming pattern)
  technitium_dns_update_record:
    api_url: "http://localhost"
    api_token: "your_api_token"
    name: "example.com"
    type: "NAPTR"
    naptrOrder: 100                  # Current order
    naptrPreference: 10              # Current preference
    naptrFlags: "u"                  # Current flags
    naptrServices: "E2U+sip"         # Current services
    naptrNewOrder: 200               # New order (uses naptrNew prefix)
    naptrNewPreference: 20           # New preference (uses naptrNew prefix)
    naptrNewFlags: "s"               # New flags (uses naptrNew prefix)
    naptrNewServices: "E2U+tel"      # New services (uses naptrNew prefix)
```

### Important Notes

1. **Identification vs. Update**: The non-prefixed parameters (e.g., `ipAddress`) are used to identify the existing record, while the `new` prefixed parameters (e.g., `newIpAddress`) specify what the record should be updated to.

2. **Record Matching**: The module uses the current parameters to find the exact record to update, which is particularly important when multiple records of the same type exist for the same domain.

3. **Idempotency**: If the current record already matches the desired `new` values, no update will be performed, maintaining Ansible's idempotent behavior.

4. **Parameter Requirements**: Not all parameters require both current and new values. Refer to the individual module documentation for specific parameter requirements per record type.
