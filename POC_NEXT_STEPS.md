# POC Next Steps: State-Based Record Management

## Current Status

✅ **Completed:**
- POC module `technitium_dns_record` with state=present/absent
- Basic integration tests (45 tasks, all passing)
- Documentation and examples

❌ **Missing - Critical for Production:**
- Update support for existing records (state=present with different parameters)
- This violates Ansible best practices and user expectations

## Key Decision Made

### Should state=present Update Existing Records?

**Answer: YES - Absolutely Required**

Based on comprehensive research:
1. **Ansible Best Practices**: Modules should be declarative and ensure final state
2. **User Expectations**: All major Ansible modules (AWS, Azure, DNS) update on state=present
3. **Real-World Examples**:
   - `amazon.aws.ec2_instance` - Updates instance type, tags
   - `azure.azcollection.azure_rm_dnsrecordset` - Updates DNS records
   - `community.general.nsupdate` - "Add or **modify**" records

### Current Behavior vs Expected Behavior

| Scenario | Current POC | Should Be |
|----------|-------------|-----------|
| Record doesn't exist | Create (✓) | Create (✓) |
| Record exists, matches | No change (✓) | No change (✓) |
| Record exists, differs | **No change (❌)** | **Update (✓)** |

## Implementation Requirements

### 1. Use Technitium's Update API

The API provides `/api/zones/records/update` which:
- Updates records atomically (no delete+recreate)
- Uses "current value" + "new value" pattern
- Safer and faster than delete+recreate

Example:
```
/api/zones/records/update?
  domain=www.example.com&
  type=A&
  ipAddress=192.0.2.1&        # Current value
  newIpAddress=192.0.2.2&     # New value
  ttl=7200                    # Updated directly
```

### 2. Key Methods to Implement

```python
# Detect if update is needed
_record_needs_update(current_record, desired_params)
  → Returns: (needs_update: bool, differences: dict)

# Perform the update
_update_record(record_type, current_record, desired_params, differences)
  → Calls /api/zones/records/update endpoint

# Build API parameters
_build_current_values_for_update(record_type, current_record)
  → Returns: {'ipAddress': '192.0.2.1', ...}

_build_new_values_for_update(record_type, desired_params, differences)
  → Returns: {'newIpAddress': '192.0.2.2', ...}

# Value comparison
_values_match(current_value, desired_value, param_name)
  → Handles type conversions, case sensitivity
```

### 3. Parameter Mapping Complexity

Each record type has different patterns:

**Simple (A record):**
- Current: `ipAddress`
- New: `newIpAddress`

**Complex (MX record):**
- Current: `exchange`, `preference`
- New: `newExchange`, `newPreference`

**Special Cases:**
- CNAME: No "new" prefix (just `cname`)
- Common params: `ttl`, `comments` updated directly (no prefix)

**Full mapping needed for 20+ record types.**

## Work Estimate

### Phase 1: Core Update Logic (8-12 hours)
- [ ] Implement `_record_needs_update()`
- [ ] Implement `_update_record()`
- [ ] Implement helper methods for parameter mapping
- [ ] Support 4-5 common record types (A, AAAA, MX, TXT, CNAME)
- [ ] Add basic update tests

### Phase 2: All Record Types (8-12 hours)
- [ ] Add mappings for all 20+ record types
- [ ] Handle special cases (SVCB, HTTPS, NAPTR, etc.)
- [ ] Comprehensive testing for each type

### Phase 3: Edge Cases & Polish (4-6 hours)
- [ ] Handle partial parameter updates
- [ ] Better error messages
- [ ] Diff output in check mode
- [ ] Performance optimization

**Total Estimate: 20-30 hours**

## Design Decisions Needed

### 1. Partial Parameter Updates

**Scenario:**
```yaml
# Record exists with: ipAddress=192.0.2.1, ttl=3600, comments="Old"
- technitium_dns_record:
    name: www.example.com
    type: A
    ttl: 7200  # Only TTL specified!
    state: present
```

**Options:**
- **A**: Fail - require all identifying parameters (ipAddress for A records)
- **B**: Fetch current record, update only specified params
- **C**: Allow but warn about potential issues

**Recommendation**: Option A (fail with clear error)
- Safer and more explicit
- Prevents accidental updates to wrong records
- Users must specify enough to identify the record

### 2. The `overwrite` Parameter

**Current POC has:** `overwrite: true/false`

**Question**: Keep it, modify it, or remove it?

**Options:**
- **A**: Remove it - always update matching record
- **B**: Keep it - use for multi-value record sets
- **C**: Rename to `replace_all` - clearer intent

**Recommendation**: Option A (remove it)
- Simpler mental model
- Consistent with Azure DNS module behavior
- If multiple records exist, update the matching one

### 3. Update vs Delete+Create

**When should we use each?**

**Use Update API for:**
- Changing TTL
- Changing comments
- Changing IP address (A/AAAA)
- Changing target values (MX, CNAME, etc.)
- = Anything the API's "new*" parameters support

**Use Delete+Create for:**
- Changing record type (A → CNAME)
- Changing record name
- = Things that change record identity

**Implementation**: Try update first, fall back to delete+create if needed

## Testing Requirements

### Unit Tests
```python
test_record_needs_update_ttl_change()
test_record_needs_update_ip_change()
test_record_needs_update_no_change()
test_values_match_case_insensitive()
test_values_match_type_conversion()
test_build_update_params_a_record()
test_build_update_params_mx_record()
# ... one test per record type
```

### Integration Tests
```yaml
- Phase: Create record
- Phase: Update TTL (verify changed=true)
- Phase: Update again (verify changed=false, idempotent)
- Phase: Update multiple params at once
- Phase: Update different record types
- Phase: Check mode for updates
```

## Documentation Updates

### Module Documentation
Add section:
```markdown
## Update Behavior

When `state=present` is used, the module ensures the record matches
ALL specified parameters. If a record already exists but has different
values (e.g., different TTL, IP address, or other attributes), it will
be updated to match the desired state.

This provides declarative, idempotent behavior consistent with Ansible
best practices. Running the module multiple times with the same
parameters will not cause unnecessary changes.

### Examples

# Create a record
- technitium_dns_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.1
    ttl: 3600
    state: present
  # Result: changed=true (record created)

# Update the TTL
- technitium_dns_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.1
    ttl: 7200  # Different!
    state: present
  # Result: changed=true (record updated)

# Run again (idempotent)
- technitium_dns_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.1
    ttl: 7200  # Same as current
    state: present
  # Result: changed=false (no changes needed)
```

### Migration Guide

Create guide for users migrating from old modules:
```markdown
## Migrating from technitium_dns_add_record

The new `technitium_dns_record` module is a drop-in replacement
with `state=present` for most use cases:

# Old way
- technitium_dns_add_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.1

# New way
- technitium_dns_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.1
    state: present  # explicit is better

Bonus: Now handles updates automatically!
```

## Risk Assessment

### High Risk Areas

1. **Parameter Mapping Errors**: 20+ record types with complex mappings
   - Mitigation: Comprehensive tests for each type
   - Automated testing against live Technitium instance

2. **Breaking Changes**: Existing users expect current behavior
   - Mitigation: This is a new module, old ones still work
   - Clear documentation about differences

3. **API Edge Cases**: Technitium API quirks
   - Mitigation: Extensive real-world testing
   - Fallback to delete+create if update fails

### Low Risk Areas

- Core logic is sound (based on proven patterns)
- Tests are comprehensive
- Can be released alongside existing modules

## Success Criteria

### Must Have
- ✅ Updates work for all record types
- ✅ Idempotency is perfect
- ✅ Check mode works correctly
- ✅ All integration tests pass
- ✅ Documentation is complete

### Nice to Have
- ⭐ Diff output showing what changed
- ⭐ Performance benchmarks
- ⭐ Example playbooks for common scenarios
- ⭐ Video demo/tutorial

## Recommendation

**Proceed with implementation** using the design outlined in [DESIGN_UPDATE_IMPLEMENTATION.md](DESIGN_UPDATE_IMPLEMENTATION.md).

### Suggested Approach

1. **Week 1**: Implement core update logic + 5 common record types
2. **Week 2**: Add remaining record types + comprehensive tests
3. **Week 3**: Edge cases, documentation, polish
4. **Week 4**: Beta testing with real users

### Alternative: Minimal Viable Product (MVP)

If time is constrained:
1. Implement update for **A, AAAA, MX, TXT, CNAME only** (covers 80% of use cases)
2. For other types, fall back to delete+create
3. Add message: "Update support for {type} records coming soon"
4. Expand support in future releases

This allows shipping the core feature faster while maintaining quality.

## Questions?

Before proceeding, consider:

1. **Timeline**: When does this need to ship?
2. **Scope**: All record types or MVP approach?
3. **Testing**: Do we have access to Technitium test instance?
4. **Resources**: Who will implement and review?
5. **Release**: New major version (2.0) or minor (1.x)?
