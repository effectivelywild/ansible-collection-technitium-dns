#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_set_group_details
short_description: Set group details in Technitium DNS server
version_added: "0.4.0"
description:
    - Change group details in Technitium DNS server.
    - Allows modifying description, renaming groups, and setting group members.
    - Requires Administration: Modify permissions.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_group
    description: Create a group in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_delete_group
    description: Delete a group from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_get_group_details
    description: Get group details from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_list_groups
    description: List all groups from Technitium DNS server
options:
    api_port:
        description:
            - Port for the Technitium DNS API. Defaults to 5380
        required: false
        type: int
        default: 5380
    api_token:
        description:
            - API token for authenticating with the Technitium DNS API
        required: true
        type: str
    api_url:
        description:
            - Base URL for the Technitium DNS API
        required: true
        type: str
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests
        required: false
        type: bool
        default: true
    group:
        description:
            - The name of the group to modify
        required: true
        type: str
    newGroup:
        description:
            - A new group name to rename the group
        required: false
        type: str
    description:
        description:
            - A new group description
        required: false
        type: str
    members:
        description:
            - A list of usernames to set as the group's members
        required: false
        type: list
        elements: str
'''

EXAMPLES = r'''
- name: Update group description
  technitium_dns_set_group_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "testgroup"
    description: "Updated test group description"

- name: Rename group
  technitium_dns_set_group_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "oldname"
    newGroup: "newname"

- name: Set group members
  technitium_dns_set_group_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "testgroup"
    members:
      - "user1"
      - "user2"

- name: Update multiple properties
  technitium_dns_set_group_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "testgroup"
    description: "New description"
    members:
      - "admin"

- name: Check what would change (check mode)
  technitium_dns_set_group_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "testgroup"
    description: "New description"
  check_mode: true
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: Updated group details from the API
            type: dict
            returned: always
            contains:
                name:
                    description: Name of the group
                    type: str
                    returned: always
                    sample: "testgroup"
                description:
                    description: Description of the group
                    type: str
                    returned: always
                    sample: "Updated test group description"
                members:
                    description: List of usernames that are members of this group
                    type: list
                    returned: always
                    elements: str
                    sample: ["admin"]
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes
    type: bool
    returned: always
    sample: true
diff:
    description: Dictionary showing what changed, with current and desired values
    type: dict
    returned: when changes are made
    sample: {
        "description": {
            "current": "Old description",
            "desired": "New description"
        },
        "members": {
            "current": ["user1"],
            "desired": ["user1", "user2"]
        }
    }
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
msg:
    description: Human readable message describing the result
    type: str
    returned: always
    sample: "Group details updated successfully."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class SetGroupDetailsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        group=dict(type='str', required=True),
        newGroup=dict(type='str', required=False),
        description=dict(type='str', required=False),
        members=dict(type='list', elements='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _normalize_value(self, key, value):
        """Normalize values for consistent comparison"""
        if key == 'members':
            if not isinstance(value, list):
                return []
            return sorted(value)

        return value

    def run(self):
        params = self.params
        group_name = params['group']

        # Check if this is a built-in group that cannot be renamed
        if self.check_builtin_group(group_name) and params.get('newGroup') is not None:
            self.fail_json(msg=f"Cannot rename built-in group '{group_name}'")

        # Check if group exists by listing all groups (avoids stack trace on non-existent group)
        group_exists, existing_group = self.check_group_exists(group_name)
        if not group_exists:
            self.fail_json(msg=f"Group '{group_name}' does not exist")

        # Fetch detailed group information including users
        current_data = self.request('/api/admin/groups/get', params={'group': group_name, 'includeUsers': 'true'})
        self.validate_api_response(current_data, "Failed to get current group details")

        current = current_data.get('response', {})

        # Build desired state dict from provided parameters
        desired = {}
        for key in ['newGroup', 'description', 'members']:
            value = params.get(key)
            if value is not None:
                # Validate input types
                if key == 'members':
                    if not isinstance(value, list):
                        self.fail_json(msg=f"Parameter '{key}' must be a list, got {type(value).__name__}")

                desired[key] = value

        # Compare current vs desired for idempotency
        diff = {}
        checkable_fields = {
            'newGroup': 'name',  # newGroup becomes name in response
            'description': 'description',
            'members': 'members'
        }

        for param_key, response_key in checkable_fields.items():
            if param_key in desired:
                current_val = current.get(response_key)
                desired_val = desired[param_key]

                normalized_current = self._normalize_value(param_key, current_val)
                normalized_desired = self._normalize_value(param_key, desired_val)

                if normalized_current != normalized_desired:
                    diff[param_key] = {
                        'current': normalized_current,
                        'desired': normalized_desired
                    }

        # If no changes needed, exit early
        if not diff:
            self.exit_json(changed=False, msg="Group details already match desired state.")

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="(check mode) Group details would be updated.",
                diff=diff,
                api_response={"status": "ok", "check_mode": True, "group": group_name}
            )

        # Set group details via the Technitium API
        set_query = {'group': group_name}

        # Map parameters to API parameter names
        param_mapping = {
            'newGroup': 'newGroup',
            'description': 'description',
            'members': 'members'
        }

        for param_key, api_key in param_mapping.items():
            if param_key in desired:
                value = desired[param_key]
                if param_key == 'members' and isinstance(value, list):
                    # Convert list to comma-separated string for API
                    set_query[api_key] = ",".join(value)
                else:
                    set_query[api_key] = value

        # Make the API call to set group details
        data = self.request('/api/admin/groups/set', params=set_query, method='POST')
        self.validate_api_response(data)

        # Return success with changes made
        self.exit_json(
            changed=True,
            msg="Group details updated successfully.",
            diff=diff,
            api_response=data
        )


if __name__ == '__main__':
    module = SetGroupDetailsModule()
    module.run()