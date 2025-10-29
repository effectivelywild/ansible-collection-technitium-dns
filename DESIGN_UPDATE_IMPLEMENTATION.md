# Design: Implementing Update Support for technitium_dns_record

## Overview

The Technitium DNS API provides three distinct endpoints for record management:
- `/api/zones/records/add` - Creates new records
- `/api/zones/records/update` - Updates existing records (atomic operation)
- `/api/zones/records/delete` - Deletes records

Currently, our POC only uses add and delete. This document outlines how to properly implement update support.

## API Update Endpoint Analysis

### Key Characteristics

The `/api/zones/records/update` endpoint uses a **"current value" + "new value"** pattern:

```
For A record update:
- ipAddress: "127.0.0.1"      # Current value (identifies the record)
- newIpAddress: "127.0.0.2"   # New value (what to change it to)
- ttl: 3600                   # Can be updated directly
```

### Pattern for Different Record Types

Each record type has:
1. **Identifying parameters** (current values) - Required to find the specific record
2. **Update parameters** (new* prefixed) - Optional, used to change values
3. **Common parameters** (ttl, comments, disable, expiryTtl) - Updated directly

### Examples

**A/AAAA Record:**
```
Current: ipAddress=192.0.2.1
New: newIpAddress=192.0.2.2
Plus: ttl, comments, ptr, createPtrZone, updateSvcbHints
```

**MX Record:**
```
Current: exchange=mail.example.com, preference=10
New: newExchange=mail2.example.com, newPreference=20
Plus: ttl, comments
```

**TXT Record:**
```
Current: text="v=spf1 mx -all", splitText=false
New: newText="v=spf1 mx include:_spf.google.com -all", newSplitText=false
Plus: ttl, comments
```

## Implementation Strategy

### 1. Update Flow in _ensure_present()

```python
def _ensure_present(self, record_type, params):
    """Ensure the record exists with the specified parameters"""

    # Step 1: Check if record exists
    exists, current_record = self._check_record_exists(record_type, params)

    if not exists:
        # Record doesn't exist - CREATE it
        if self.check_mode:
            self.exit_json(changed=True, msg="Record would be created (check mode).")

        self._create_record(record_type, params)
        self.exit_json(changed=True, msg="DNS record created.")

    # Step 2: Record exists - check if it needs updating
    needs_update, differences = self._record_needs_update(current_record, params)

    if not needs_update:
        # Perfect match - nothing to do (idempotent)
        if self.check_mode:
            self.exit_json(changed=False, msg="Record already matches desired state (check mode).")
        else:
            self.exit_json(changed=False, msg="Record already matches desired state.")

    # Step 3: Record needs update
    if self.check_mode:
        diff_msg = ", ".join([f"{k}: {v['current']} → {v['new']}" for k, v in differences.items()])
        self.exit_json(changed=True, msg=f"Record would be updated: {diff_msg} (check mode).")

    self._update_record(record_type, current_record, params, differences)
    self.exit_json(changed=True, msg="DNS record updated.")
```

### 2. New Method: _record_needs_update()

```python
def _record_needs_update(self, current_record, desired_params):
    """
    Compare current record with desired parameters.

    Returns:
        tuple: (needs_update: bool, differences: dict)

    Example differences dict:
    {
        'ipAddress': {'current': '192.0.2.1', 'new': '192.0.2.2'},
        'ttl': {'current': 3600, 'new': 7200}
    }
    """
    differences = {}
    record_type = desired_params['type'].upper()

    # Get mappings for this record type
    param_mappings = self._get_update_param_mappings(record_type)

    # Check each parameter that can be updated
    for param_name, rdata_field in param_mappings.items():
        desired_value = desired_params.get(param_name)

        # Skip if user didn't specify this parameter
        if desired_value is None:
            continue

        # Extract current value from record
        if rdata_field:
            current_value = current_record.get('rData', {}).get(rdata_field)
        else:
            current_value = current_record.get(param_name)

        # Compare values (handle type conversions, case sensitivity, etc.)
        if not self._values_match(current_value, desired_value, param_name):
            differences[param_name] = {
                'current': current_value,
                'new': desired_value
            }

    # Check common parameters (ttl, comments)
    for common_param in ['ttl', 'comments', 'expiryTtl']:
        if common_param in desired_params:
            desired_value = desired_params[common_param]
            current_value = current_record.get(common_param)

            if not self._values_match(current_value, desired_value, common_param):
                differences[common_param] = {
                    'current': current_value,
                    'new': desired_value
                }

    needs_update = len(differences) > 0
    return needs_update, differences
```

### 3. New Method: _update_record()

```python
def _update_record(self, record_type, current_record, desired_params, differences):
    """
    Update an existing record using the /api/zones/records/update endpoint.

    Args:
        record_type: The DNS record type (A, MX, etc.)
        current_record: The current record data from API
        desired_params: The desired parameters from user
        differences: Dict of parameters that need updating
    """
    query = {
        'token': self.api_token,
        'domain': desired_params['name'],
        'type': record_type
    }

    if desired_params.get('zone'):
        query['zone'] = desired_params['zone']

    # Add current values (required to identify the record)
    current_values = self._build_current_values_for_update(record_type, current_record)
    query.update(current_values)

    # Add new values (what we're changing)
    new_values = self._build_new_values_for_update(record_type, desired_params, differences)
    query.update(new_values)

    # Add common parameters that are updated directly
    for param in ['ttl', 'comments', 'expiryTtl', 'disable']:
        if param in desired_params and desired_params[param] is not None:
            val = desired_params[param]
            if isinstance(val, bool):
                val = str(val).lower()
            query[param] = val

    # Make the update API call
    data = self.request('/api/zones/records/update', params=query, method='POST')

    if data.get('status') != 'ok':
        error_msg = data.get('errorMessage') or "Unknown error"
        self.fail_json(msg=f"Failed to update record: {error_msg}", api_response=data)

    return data
```

### 4. New Method: _build_current_values_for_update()

```python
def _build_current_values_for_update(self, record_type, current_record):
    """
    Build the 'current value' parameters needed by the update API.
    These identify which specific record to update.

    Returns dict with parameters like:
    - A record: {'ipAddress': '192.0.2.1'}
    - MX record: {'exchange': 'mail.example.com', 'preference': 10}
    """
    current_values = {}
    rdata = current_record.get('rData', {})

    # Record-type specific mappings
    mappings = {
        'A': {'ipAddress': 'ipAddress'},
        'AAAA': {'ipAddress': 'ipAddress'},
        'CNAME': {'cname': 'cname'},
        'MX': {'exchange': 'exchange', 'preference': 'preference'},
        'TXT': {'text': 'text', 'splitText': 'splitText'},
        'NS': {'nameServer': 'nameServer'},
        'PTR': {'ptrName': 'ptrName'},
        'SRV': {'priority': 'priority', 'weight': 'weight', 'port': 'port', 'target': 'target'},
        'CAA': {'flags': 'flags', 'tag': 'tag', 'value': 'value'},
        'ANAME': {'aname': 'aname'},
        # Add all other record types...
    }

    if record_type in mappings:
        for param_name, rdata_field in mappings[record_type].items():
            value = rdata.get(rdata_field)
            if value is not None:
                # Handle special case: srv_port -> port
                if param_name == 'srv_port':
                    current_values['port'] = value
                else:
                    current_values[param_name] = value

    return current_values
```

### 5. New Method: _build_new_values_for_update()

```python
def _build_new_values_for_update(self, record_type, desired_params, differences):
    """
    Build the 'new value' parameters for the update API.
    Only include parameters that are changing.

    Returns dict with 'new*' prefixed parameters like:
    - A record: {'newIpAddress': '192.0.2.2'}
    - MX record: {'newExchange': 'mail2.example.com', 'newPreference': 20}
    """
    new_values = {}

    # Mapping of parameter names to their 'new*' equivalents
    new_param_mapping = {
        'ipAddress': 'newIpAddress',
        'nameServer': 'newNameServer',
        'cname': 'cname',  # CNAME doesn't use 'new' prefix
        'ptrName': 'newPtrName',
        'exchange': 'newExchange',
        'preference': 'newPreference',
        'text': 'newText',
        'splitText': 'newSplitText',
        'priority': 'newPriority',
        'weight': 'newWeight',
        'srv_port': 'newPort',
        'target': 'newTarget',
        'flags': 'newFlags',
        'tag': 'newTag',
        'value': 'newValue',
        'aname': 'newAName',
        # Add all other record types...
    }

    # Only add 'new*' parameters for values that are actually changing
    for param_name, new_param_name in new_param_mapping.items():
        if param_name in differences:
            new_value = desired_params.get(param_name)
            if new_value is not None:
                if isinstance(new_value, bool):
                    new_value = str(new_value).lower()
                new_values[new_param_name] = new_value

    # Special handling for record-specific parameters
    if record_type in ['A', 'AAAA']:
        # Add ptr, createPtrZone, updateSvcbHints if specified
        for param in ['ptr', 'createPtrZone', 'updateSvcbHints']:
            if param in desired_params and desired_params[param] is not None:
                val = desired_params[param]
                if isinstance(val, bool):
                    val = str(val).lower()
                new_values[param] = val

    return new_values
```

### 6. Helper Method: _values_match()

```python
def _values_match(self, current_value, desired_value, param_name):
    """
    Compare current and desired values, handling type conversions.

    Handles:
    - Type mismatches (int vs string)
    - Case sensitivity (for certain fields)
    - None/null handling
    """
    # Both None/null = match
    if current_value is None and desired_value is None:
        return True

    # One is None = no match
    if current_value is None or desired_value is None:
        return False

    # Numeric comparison (handle string vs int)
    if isinstance(current_value, (int, float)) or isinstance(desired_value, (int, float)):
        try:
            return int(current_value) == int(desired_value)
        except (ValueError, TypeError):
            pass

    # String comparison
    if isinstance(current_value, str) and isinstance(desired_value, str):
        # Case-insensitive for certain parameters
        case_insensitive_params = ['sshfpFingerprint', 'tlsaCertificateAssociationData', 'digest']
        if param_name in case_insensitive_params:
            return current_value.lower() == desired_value.lower()
        return current_value == desired_value

    # Default: direct comparison
    return current_value == desired_value
```

## Complete Parameter Mappings

### Record Type to Current/New Parameter Mappings

```python
UPDATE_PARAM_MAPPINGS = {
    'A': {
        'current': ['ipAddress'],
        'new': ['newIpAddress'],
        'direct': ['ptr', 'createPtrZone', 'updateSvcbHints']
    },
    'AAAA': {
        'current': ['ipAddress'],
        'new': ['newIpAddress'],
        'direct': ['ptr', 'createPtrZone', 'updateSvcbHints']
    },
    'MX': {
        'current': ['exchange', 'preference'],
        'new': ['newExchange', 'newPreference'],
        'direct': []
    },
    'TXT': {
        'current': ['text', 'splitText'],
        'new': ['newText', 'newSplitText'],
        'direct': []
    },
    'CNAME': {
        'current': ['cname'],
        'new': ['cname'],  # CNAME doesn't use 'new' prefix!
        'direct': []
    },
    'NS': {
        'current': ['nameServer'],
        'new': ['newNameServer'],
        'direct': ['glue']
    },
    'PTR': {
        'current': ['ptrName'],
        'new': ['newPtrName'],
        'direct': []
    },
    'SRV': {
        'current': ['priority', 'weight', 'port', 'target'],
        'new': ['newPriority', 'newWeight', 'newPort', 'newTarget'],
        'direct': []
    },
    'CAA': {
        'current': ['flags', 'tag', 'value'],
        'new': ['newFlags', 'newTag', 'newValue'],
        'direct': []
    },
    'ANAME': {
        'current': ['aname'],
        'new': ['newAName'],
        'direct': []
    },
    'DS': {
        'current': ['keyTag', 'algorithm', 'digestType', 'digest'],
        'new': ['newKeyTag', 'newAlgorithm', 'newDigestType', 'newDigest'],
        'direct': []
    },
    'SSHFP': {
        'current': ['sshfpAlgorithm', 'sshfpFingerprintType', 'sshfpFingerprint'],
        'new': ['newSshfpAlgorithm', 'newSshfpFingerprintType', 'newSshfpFingerprint'],
        'direct': []
    },
    'TLSA': {
        'current': ['tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData'],
        'new': ['newTlsaCertificateUsage', 'newTlsaSelector', 'newTlsaMatchingType', 'newTlsaCertificateAssociationData'],
        'direct': []
    },
    'SVCB': {
        'current': ['svcPriority', 'svcTargetName', 'svcParams'],
        'new': ['newSvcPriority', 'newSvcTargetName', 'newSvcParams'],
        'direct': ['autoIpv4Hint', 'autoIpv6Hint']
    },
    'HTTPS': {
        'current': ['svcPriority', 'svcTargetName', 'svcParams'],
        'new': ['newSvcPriority', 'newSvcTargetName', 'newSvcParams'],
        'direct': ['autoIpv4Hint', 'autoIpv6Hint']
    },
    'URI': {
        'current': ['uriPriority', 'uriWeight', 'uri'],
        'new': ['newUriPriority', 'newUriWeight', 'newUri'],
        'direct': []
    },
    'NAPTR': {
        'current': ['naptrOrder', 'naptrPreference', 'naptrFlags', 'naptrServices', 'naptrRegexp', 'naptrReplacement'],
        'new': ['naptrNewOrder', 'naptrNewPreference', 'naptrNewFlags', 'naptrNewServices', 'naptrNewRegexp', 'naptrNewReplacement'],
        'direct': []
    },
    'FWD': {
        'current': ['protocol', 'forwarder', 'forwarderPriority'],
        'new': ['newProtocol', 'newForwarder'],
        'direct': ['dnssecValidation', 'proxyType', 'proxyAddress', 'proxyPort', 'proxyUsername', 'proxyPassword']
    },
    'DNAME': {
        'current': ['dname'],
        'new': ['dname'],  # DNAME doesn't use 'new' prefix (similar to CNAME)
        'direct': []
    },
    'APP': {
        'current': ['appName', 'classPath', 'recordData'],
        'new': [],  # APP updates all values in place
        'direct': ['recordData']
    },
    'UNKNOWN': {
        'current': ['rdata'],
        'new': ['newRData'],
        'direct': []
    }
}

# Parameters that are always updated directly (not prefixed with 'new')
COMMON_UPDATE_PARAMS = ['ttl', 'comments', 'disable', 'expiryTtl']
```

## Testing Strategy

### Unit Tests for Update Detection

```python
def test_record_needs_update_ttl_change():
    """Test detecting TTL change"""
    current = {'name': 'test.example.com', 'type': 'A', 'ttl': 3600, 'rData': {'ipAddress': '192.0.2.1'}}
    desired = {'name': 'test.example.com', 'type': 'A', 'ttl': 7200, 'ipAddress': '192.0.2.1'}
    needs_update, diffs = _record_needs_update(current, desired)
    assert needs_update == True
    assert 'ttl' in diffs
    assert diffs['ttl']['current'] == 3600
    assert diffs['ttl']['new'] == 7200

def test_record_needs_update_no_change():
    """Test no update needed when values match"""
    current = {'name': 'test.example.com', 'type': 'A', 'ttl': 3600, 'rData': {'ipAddress': '192.0.2.1'}}
    desired = {'name': 'test.example.com', 'type': 'A', 'ttl': 3600, 'ipAddress': '192.0.2.1'}
    needs_update, diffs = _record_needs_update(current, desired)
    assert needs_update == False
    assert len(diffs) == 0
```

### Integration Tests

Add to existing test file:

```yaml
# Phase: Test updates
- name: "Update A record TTL"
  effectivelywild.technitium_dns.technitium_dns_record:
    name: "state-a-1.{{ primary_zone_name }}"
    zone: "{{ primary_zone_name }}"
    type: A
    ipAddress: 192.0.2.100
    ttl: 7200  # Changed from 3600
    state: present
  register: update_ttl_result

- name: "Assert update reported changed"
  assert:
    that:
      - update_ttl_result.changed == true
      - "'updated' in update_ttl_result.msg.lower()"

- name: "Verify TTL was updated"
  technitium_dns_get_record:
    name: "state-a-1.{{ primary_zone_name }}"
  register: verify_update

- name: "Assert TTL is new value"
  assert:
    that:
      - verify_update.records[0].ttl == 7200

- name: "Re-run update (idempotency check)"
  effectivelywild.technitium_dns.technitium_dns_record:
    name: "state-a-1.{{ primary_zone_name }}"
    zone: "{{ primary_zone_name }}"
    type: A
    ipAddress: 192.0.2.100
    ttl: 7200
    state: present
  register: update_idempotent

- name: "Assert no change on re-run"
  assert:
    that:
      - update_idempotent.changed == false
```

## Edge Cases and Considerations

### 1. Partial Updates

**Question**: What if user only specifies TTL but not other parameters?

```yaml
- name: Update only TTL
  technitium_dns_record:
    name: www.example.com
    type: A
    ttl: 7200  # Only TTL specified, no ipAddress!
    state: present
```

**Answer**: This should **fail** with a clear error message. Required parameters for the record type must always be specified to properly identify which record to update.

### 2. Multiple Records of Same Type

If multiple A records exist for www.example.com:
- 192.0.2.1
- 192.0.2.2

User wants to update the first one to 192.0.2.10:

```yaml
- technitium_dns_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.10  # This is ambiguous!
    state: present
```

**Solution**: The `ipAddress` parameter serves dual purpose:
1. To identify which record to update (current value)
2. To specify the new value

For updates, we need the current value. The user would need to:
```yaml
# This won't work as desired - it creates/updates based on the final state
# The user must delete the old record and create the new one
# OR we need a way to specify "current" vs "new" values
```

**Decision**: Keep it simple - for A records, the `ipAddress` is both identifier and value. If you want to change an IP, you delete the old record and create a new one. Updates are for TTL, comments, etc.

### 3. Record Type Constraints

Some parameters can't be updated (they're part of the record's identity):
- Record type itself
- Record name (use newDomain parameter for that)
- Zone

These should remain immutable. Changing them requires delete + recreate.

## Implementation Phases

### Phase 1: Basic Update Support (A, MX, TXT, CNAME)
- Implement core update logic
- Support most common record types
- Complete integration tests

### Phase 2: Extended Record Types
- Add support for all remaining record types
- Edge case handling
- Performance optimization

### Phase 3: Advanced Features
- Diff output showing what changed
- Batch updates
- Rollback capability

## Summary

The update implementation provides:
- ✅ Proper declarative state management
- ✅ Atomic updates (no delete+recreate)
- ✅ Clear diff reporting
- ✅ Full idempotency
- ✅ Follows Ansible best practices
- ✅ Uses Technitium's native update API

This approach is significantly better than delete+recreate because:
1. **Atomic**: No downtime during update
2. **Safer**: Less chance of errors
3. **Faster**: Single API call instead of two
4. **Cleaner**: Preserves record metadata
