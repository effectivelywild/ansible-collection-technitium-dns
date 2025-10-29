# Design Analysis: How Should state=present Handle Updates?

## The Question

When a DNS record already exists and you run the module with `state=present` but with **different parameter values** (e.g., different TTL, different IP address, different MX preference), should the module:

**Option A**: Update the existing record to match the new parameters (reports `changed=true`)
**Option B**: Leave the existing record unchanged if it exists (reports `changed=false`)

## Ansible Best Practices Research

### Official Ansible Documentation

From [Ansible Module Development Best Practices](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html):

> **Implement declarative operations (not CRUD)** so the user can ignore existing state and focus on final state. For example, use `started/stopped`, `present/absent`.

> **Strive for a consistent final state (aka idempotency).** If running your module twice in a row against the same system would result in two different states, see if you can redesign or rewrite to achieve consistent final state.

**Key Takeaway**: Modules should be **declarative** - they should ensure the resource matches the desired state, regardless of its current state.

## Real-World Examples from Core and Community Modules

### 1. amazon.aws.ec2_instance (AWS)

**Behavior**: `state=present` **DOES UPDATE** existing instances

- If instance type differs: "the instance will be stopped and the instance type will be updated"
- For tags: Uses `purge_tags` parameter to control whether to update tags
- **Design Philosophy**: Declarative - ensures instance matches desired configuration

**Example**:
```yaml
- name: Update instance type
  amazon.aws.ec2_instance:
    instance_ids: "i-123456"
    instance_type: "t3.medium"  # Different from current
    state: present
  # Result: Updates the instance type (reports changed=true)
```

### 2. azure.azcollection.azure_rm_dnsrecordset (Azure DNS)

**Behavior**: `state=present` **DOES UPDATE** existing DNS records

- Explicitly documented as "Create, delete and **update** DNS record sets"
- Running with different values replaces the entire record set
- **Design Philosophy**: Declarative - record set converges to specified state

**Example**:
```yaml
- name: Update DNS record
  azure.azcollection.azure_rm_dnsrecordset:
    relative_name: www
    zone_name: example.com
    record_type: A
    records:
      - entry: 192.168.100.101  # Different from current
    state: present
  # Result: Updates the A record (reports changed=true)
```

### 3. community.general.nsupdate (DNS Updates)

**Behavior**: `state=present` **DOES UPDATE** existing DNS records

- Task examples explicitly say "Add or **modify** ansible.example.org"
- Idempotent - detects when value differs and updates
- **Design Philosophy**: Declarative - ensures record matches specified value

**Example**:
```yaml
- name: Update DNS record
  community.general.nsupdate:
    record: "ansible"
    value: "192.168.1.2"  # Different from current 192.168.1.1
    state: present
  # Result: Updates the record (reports changed=true)
```

### 4. ansible.builtin.user (User Management)

**Behavior**: `state=present` **DOES UPDATE** existing users

- Can update uid, shell, home directory, etc. on existing users
- Idempotent - only changes what differs
- **Design Philosophy**: Declarative - user account matches desired state

**Example**:
```yaml
- name: Update user shell
  ansible.builtin.user:
    name: johndoe
    shell: /bin/zsh  # Different from current /bin/bash
    state: present
  # Result: Updates the shell (reports changed=true)
```

## The Pattern: Declarative State Management

All major Ansible modules follow the same pattern:

1. **state=present means "ensure this exact configuration exists"**
2. **If resource doesn't exist**: Create it (changed=true)
3. **If resource exists but differs**: Update it (changed=true)
4. **If resource exists and matches**: Do nothing (changed=false)

This is the **declarative approach** - you declare what you want, and the module makes it happen.

## Current Implementation Issue

Our current POC implementation follows **Option B** (no updates):

```python
def _ensure_present(self, record_type, params):
    exists, matching_record = self._check_record_exists(record_type, params)

    if exists and not params.get('overwrite', False):
        # Current behavior: Does nothing if record exists
        self.exit_json(changed=False, msg="Record already exists...")
```

**Problem**: This violates Ansible best practices and user expectations.

### Example of the Issue:

```yaml
# Initial run - creates record with TTL 3600
- name: Ensure DNS record
  technitium_dns_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.1
    ttl: 3600
    state: present
  # Result: changed=true (record created)

# Second run - try to update TTL to 7200
- name: Ensure DNS record
  technitium_dns_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.1
    ttl: 7200  # Different TTL!
    state: present
  # Current behavior: changed=false (does nothing!)
  # Expected behavior: changed=true (updates TTL)
```

## Recommended Implementation: Option A (Update on Difference)

### Design

```python
def _ensure_present(self, record_type, params):
    """Ensure the record exists with the specified parameters"""

    # Check current state
    exists, current_record = self._check_record_exists(record_type, params)

    if exists:
        # Record exists - check if it matches desired state
        needs_update = self._record_needs_update(current_record, params)

        if not needs_update:
            # Perfect match - idempotent
            if self.check_mode:
                self.exit_json(changed=False, msg="Record already matches desired state (check mode).")
            else:
                self.exit_json(changed=False, msg="Record already matches desired state.")

        # Record exists but differs - need to update
        if self.check_mode:
            self.exit_json(changed=True, msg="Record would be updated (check mode).")

        # Perform update (delete + recreate or use overwrite)
        self._update_record(record_type, params)
        self.exit_json(changed=True, msg="DNS record updated.")

    else:
        # Record doesn't exist - create it
        if self.check_mode:
            self.exit_json(changed=True, msg="Record would be created (check mode).")

        self._create_record(record_type, params)
        self.exit_json(changed=True, msg="DNS record created.")
```

### New Helper Method Needed

```python
def _record_needs_update(self, current_record, desired_params):
    """
    Check if current record differs from desired state.
    Returns True if any parameter needs updating.
    """
    required_params = self._get_required_params(record_type)
    optional_params = ['ttl', 'comments']  # Add all optional params

    for param in required_params + optional_params:
        current_value = self._extract_value_from_record(current_record, param)
        desired_value = desired_params.get(param)

        if desired_value is not None:  # Only check specified params
            if not self._values_match(current_value, desired_value):
                return True

    return False
```

## What About the `overwrite` Parameter?

With the new approach, the `overwrite` parameter serves a different purpose:

### Current Understanding (from add_record module):
- `overwrite=false` (default): Add to existing record set
- `overwrite=true`: Replace entire record set

### For State-Based Module:

**Option 1: Keep overwrite for record sets**
```yaml
# Multiple A records for www.example.com exist: 192.0.2.1, 192.0.2.2
- name: Add another A record
  technitium_dns_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.3
    overwrite: false  # Add to set (now have 3 A records)
    state: present

- name: Replace all A records
  technitium_dns_record:
    name: www.example.com
    type: A
    ipAddress: 192.0.2.10
    overwrite: true  # Remove others, only have this one
    state: present
```

**Option 2: Remove overwrite, always update**
- Simpler mental model
- More predictable behavior
- Follows Azure DNS module pattern

**Recommendation**: Go with Option 2 - remove `overwrite` parameter for simpler, more predictable behavior.

## Impact on Technitium API

The Technitium API has:
- `/api/zones/records/add` - Adds or updates records
- `/api/zones/records/delete` - Deletes records

**For updates**: The API's add endpoint with `overwrite=true` replaces the record set, which is exactly what we want for declarative state management.

## Comparison Table

| Scenario | Current Behavior | Recommended Behavior | AWS ec2_instance | Azure DNS | nsupdate |
|----------|------------------|---------------------|------------------|-----------|----------|
| Record doesn't exist | Create (changed=true) | Create (changed=true) | ✓ | ✓ | ✓ |
| Record exists, matches | No change (changed=false) | No change (changed=false) | ✓ | ✓ | ✓ |
| Record exists, differs | No change (changed=false) ❌ | Update (changed=true) ✓ | ✓ | ✓ | ✓ |

## Conclusion

**Recommendation: Implement Option A (Update on Difference)**

### Reasons:

1. ✅ **Follows Ansible Best Practices**: Declarative, idempotent state management
2. ✅ **Matches User Expectations**: Consistent with all major Ansible modules
3. ✅ **More Intuitive**: "state=present" means "make it look like this"
4. ✅ **Eliminates Confusion**: Users don't need to delete-then-create to update
5. ✅ **Better DX**: Simpler playbooks, fewer tasks needed

### Implementation Checklist:

- [ ] Modify `_ensure_present()` to detect differences
- [ ] Add `_record_needs_update()` method
- [ ] Add `_values_match()` for comparing current vs desired
- [ ] Update API calls to use `overwrite=true` for updates
- [ ] Update tests to verify update behavior
- [ ] Update documentation with examples of updates
- [ ] Consider removing `overwrite` parameter for simplicity

### Documentation Note:

Add to module documentation:
> **Note on Updates**: When `state=present` is used, the module ensures the record matches the specified parameters. If a record already exists but has different values (e.g., different TTL, IP address), it will be updated to match. This provides declarative, idempotent behavior consistent with Ansible best practices.

## Questions for Discussion

1. Should we keep the `overwrite` parameter for multi-value record sets, or remove it for simplicity?
2. Should updates be atomic (delete + recreate) or use the API's update capability?
3. How should we handle partial parameter specifications (e.g., only specifying TTL without other params)?
