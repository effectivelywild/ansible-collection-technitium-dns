#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_create_group
short_description: Create a group in Technitium DNS server
version_added: "0.4.0"
description:
    - Create a new group in Technitium DNS server using its API.
    - This will not update existing groups; it only creates new ones.
    - Requires Administration: Modify permissions.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_groups
    description: List all groups from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_delete_group
    description: Delete a group from Technitium DNS server
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
            - The name of the group to create
        required: true
        type: str
    description:
        description:
            - The description text for the group
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Create a group
  technitium_dns_create_group:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "Test Group"
    description: "Test group for development"

- name: Create group without description
  technitium_dns_create_group:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "Simple Group"

- name: Create group in check mode
  technitium_dns_create_group:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "Check Group"
    description: "Check mode group"
  check_mode: true
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The core data payload from the API
            type: dict
            returned: always
            contains:
                name:
                    description: Name of the created group
                    type: str
                    returned: always
                    sample: "Test Group"
                description:
                    description: Description of the created group
                    type: str
                    returned: always
                    sample: "Test group for development"
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to create a new group
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to complete the group creation
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the group creation result
    type: str
    returned: always
    sample: "Group 'Test Group' created."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class CreateGroupModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        group=dict(type='str', required=True),
        description=dict(type='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        group_name = params['group']
        description = params.get('description')

        # Check for existing group to ensure idempotent behavior
        # If group already exists, return success without changes
        group_exists, existing_group = self.check_group_exists(group_name)
        if group_exists:
            self.exit_json(
                changed=False,
                msg=f"Group '{group_name}' already exists.",
                group=existing_group
            )

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Group '{group_name}' would be created (check mode).",
                api_response={"status": "ok", "check_mode": True, "group": group_name}
            )

        # Build API query parameters from module arguments
        query = {
            'group': group_name
        }

        # Add optional description if provided
        if description is not None:
            query['description'] = description

        # Create the group via the Technitium API
        data = self.request('/api/admin/groups/create', params=query, method='POST')
        self.validate_api_response(data)

        # Return success - group was created
        self.exit_json(
            changed=True, msg=f"Group '{group_name}' created.", api_response=data)


if __name__ == '__main__':
    module = CreateGroupModule()
    module.run()
