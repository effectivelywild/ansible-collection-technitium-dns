#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_get_group_details
short_description: Get group details from Technitium DNS server
version_added: "0.4.0"
description:
    - Retrieve detailed information about a group from Technitium DNS server.
    - Returns group name, description, and user membership information.
    - Users information is always included in the response.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_group
    description: Create a group in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_delete_group
    description: Delete a group from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_list_groups
    description: List all groups from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_set_group_details
    description: Set group details in Technitium DNS server
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
            - The name of the group to get details for
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Get Administrators group details
  technitium_dns_get_group_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "Administrators"
  register: result

- debug:
    var: result.group_details

- name: Get details for a custom group
  technitium_dns_get_group_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "Custom Group"
  register: result

- debug:
    var: result.group_details
'''

RETURN = r'''
changed:
    description: Whether the module made changes (always false for get operations)
    type: bool
    returned: always
    sample: false
group_details:
    description: Complete group details and membership information
    type: dict
    returned: always
    contains:
        name:
            description: Name of the group
            type: str
            returned: always
            sample: "Administrators"
        description:
            description: Description of the group
            type: str
            returned: always
            sample: "Super administrators"
        members:
            description: List of usernames that are members of this group
            type: list
            returned: always
            elements: str
            sample: ["admin"]
        users:
            description: List of all usernames that have access to this group
            type: list
            returned: always
            elements: str
            sample: ["admin", "user1"]
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class GetGroupDetailsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        group=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        group_name = self.params['group']

        # Check if group exists by listing all groups (avoids stack trace on non-existent group)
        group_exists, existing_group = self.check_group_exists(group_name)
        if not group_exists:
            self.fail_json(msg=f"Group '{group_name}' does not exist")

        # Build API parameters for group details request
        params = {
            'group': group_name,
            'includeUsers': 'true'
        }

        # Fetch group details from the Technitium API
        data = self.request('/api/admin/groups/get', params=params)

        # Check API response status and handle errors
        self.validate_api_response(data)

        # Extract group details from API response
        group_details = data.get('response', {})

        # Return the group details (read-only operation, never changed=True)
        self.exit_json(changed=False, group_details=group_details)


if __name__ == '__main__':
    module = GetGroupDetailsModule()
    module.run()
