#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_groups
short_description: List all groups from Technitium DNS server
version_added: "0.4.0"
description:
    - Retrieve a list of all groups from a Technitium DNS server.
    - Requires Administration: View permissions.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_user
    description: Create a user account in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_delete_user
    description: Delete a user account from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_get_user_details
    description: Get user account details from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_list_users
    description: List all users from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_set_user_details
    description: Set user account details on Technitium DNS server
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
            - Whether to validate SSL certificates when making API requests.
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: List all groups from Technitium DNS
  technitium_dns_list_groups:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.groups

- name: Check if default groups exist
  technitium_dns_list_groups:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: groups_result

- name: Verify administrators group exists
  assert:
    that:
      - groups_result.groups | selectattr('name', 'equalto', 'Administrators') | list | length > 0
    fail_msg: "Administrators group not found"
'''

RETURN = r'''
groups:
    description: List of groups from the Technitium DNS server
    type: list
    returned: always
    elements: dict
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
changed:
    description: Whether the module made changes (always false for list operations)
    type: bool
    returned: always
    sample: false
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class ListGroupsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Fetch all groups from the API
        data = self.request('/api/admin/groups/list')
        self.validate_api_response(data)

        groups = data.get('response', {}).get('groups', [])
        self.exit_json(changed=False, groups=groups)


if __name__ == '__main__':
    module = ListGroupsModule()
    module.run()