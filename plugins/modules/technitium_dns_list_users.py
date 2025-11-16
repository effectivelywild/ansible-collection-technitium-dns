#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_users
short_description: List all users
version_added: "0.4.0"
description:
    - Retrieve a list of all users.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_user
    description: Create a user account
  - module: effectivelywild.technitium_dns.technitium_dns_delete_user
    description: Delete a user account
  - module: effectivelywild.technitium_dns.technitium_dns_get_user_details
    description: Get user account details
  - module: effectivelywild.technitium_dns.technitium_dns_set_user_details
    description: Set user account details
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
    node:
        description:
            - The node domain name for which this API call is intended
            - When unspecified, the current node is used
            - This parameter can be used only when Clustering is initialized
        required: false
        type: str
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests.
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: List all users from Technitium DNS
  technitium_dns_list_users:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.users

- name: List users on a specific cluster node
  technitium_dns_list_users:
    api_url: "http://localhost"
    api_token: "myapitoken"
    node: "node1.cluster.example.com"
  register: result

- name: Check if a specific user exists
  technitium_dns_list_users:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: users_result

- name: Verify admin user exists
  assert:
    that:
      - users_result.users | selectattr('username', 'equalto', 'admin') | list | length > 0
    fail_msg: "Admin user not found"
'''

RETURN = r'''
users:
    description: List of users from the Technitium DNS server
    type: list
    returned: always
    elements: dict
    contains:
        displayName:
            description: Display name of the user
            type: str
            returned: always
            sample: "Administrator"
        username:
            description: Username for the user account
            type: str
            returned: always
            sample: "admin"
        disabled:
            description: Whether the user account is disabled
            type: bool
            returned: always
            sample: false
        previousSessionLoggedOn:
            description: Timestamp of previous session login (ISO 8601 format)
            type: str
            returned: always
            sample: "2022-09-17T13:20:32.7933783Z"
        previousSessionRemoteAddress:
            description: Remote IP address of previous session
            type: str
            returned: always
            sample: "127.0.0.1"
        recentSessionLoggedOn:
            description: Timestamp of most recent session login (ISO 8601 format)
            type: str
            returned: always
            sample: "2022-09-17T13:22:45.671081Z"
        recentSessionRemoteAddress:
            description: Remote IP address of most recent session
            type: str
            returned: always
            sample: "127.0.0.1"
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


class ListUsersModule(TechnitiumModule):
    argument_spec = dict(
        node=dict(type='str', required=False),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Build API request parameters
        params = {}
        if self.params.get('node'):
            params['node'] = self.params['node']

        # Fetch all users from the API
        data = self.request('/api/admin/users/list', params=params)
        self.validate_api_response(data)

        users = data.get('response', {}).get('users', [])
        self.exit_json(changed=False, users=users)


if __name__ == '__main__':
    module = ListUsersModule()
    module.run()
