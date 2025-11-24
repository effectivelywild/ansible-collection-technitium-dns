#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_get_user_details
short_description: Get user account profile details
version_added: "0.4.0"
description:
    - Retrieve detailed information about a user account.
    - Returns user profile, session information, and group memberships.
    - Groups information is always included in the response.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_user
    description: Create a user account
  - module: effectivelywild.technitium_dns.technitium_dns_delete_user
    description: Delete a user
  - module: effectivelywild.technitium_dns.technitium_dns_list_users
    description: List all users
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
            - Whether to validate SSL certificates when making API requests
        required: false
        type: bool
        default: true
    username:
        description:
            - The username for the user account to get details for
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Get admin user details
  technitium_dns_get_user_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "admin"
  register: result

- debug:
    var: result.user_details

- name: Get user details for a specific user
  technitium_dns_get_user_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"
  register: result

- debug:
    var: result.user_details

- name: Get user details on a specific cluster node
  technitium_dns_get_user_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"
    node: "node1.cluster.example.com"
  register: result
'''

RETURN = r'''
changed:
    description: Whether the module made changes (always false for get operations)
    type: bool
    returned: always
    sample: false
user_details:
    description: Complete user account details and profile information
    type: dict
    returned: always
    contains:
        displayName:
            description: Display name of the user
            type: str
            returned: always
            sample: "Administrator"
        username:
            description: Username of the user account
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
            sample: "2022-09-16T13:22:45.671Z"
        previousSessionRemoteAddress:
            description: Remote IP address of previous session
            type: str
            returned: always
            sample: "127.0.0.1"
        recentSessionLoggedOn:
            description: Timestamp of most recent session login (ISO 8601 format)
            type: str
            returned: always
            sample: "2022-09-18T09:55:26.9800695Z"
        recentSessionRemoteAddress:
            description: Remote IP address of most recent session
            type: str
            returned: always
            sample: "127.0.0.1"
        sessionTimeoutSeconds:
            description: Session timeout in seconds
            type: int
            returned: always
            sample: 1800
        memberOfGroups:
            description: List of groups the user is a member of
            type: list
            returned: always
            elements: str
            sample: ["Administrators"]
        sessions:
            description: List of active user sessions
            type: list
            returned: always
            elements: dict
            contains:
                username:
                    description: Username of the session
                    type: str
                    returned: always
                isCurrentSession:
                    description: Whether this is the current session
                    type: bool
                    returned: always
                partialToken:
                    description: Partial token identifier
                    type: str
                    returned: always
                type:
                    description: Session type (Standard or ApiToken)
                    type: str
                    returned: always
                tokenName:
                    description: Name of the API token (if applicable)
                    type: str
                    returned: when type is ApiToken
                lastSeen:
                    description: Last seen timestamp (ISO 8601 format)
                    type: str
                    returned: always
                lastSeenRemoteAddress:
                    description: Last seen remote IP address
                    type: str
                    returned: always
                lastSeenUserAgent:
                    description: Last seen user agent string
                    type: str
                    returned: always
        groups:
            description: Available groups list
            type: list
            returned: always
            elements: str
            sample: ["Administrators", "DHCP Administrators", "DNS Administrators"]
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class GetUserDetailsModule(TechnitiumModule):
    argument_spec = dict(
        node=dict(type='str', required=False),
        **TechnitiumModule.get_common_argument_spec(),
        username=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        username = self.params['username']

        # Check if user exists by listing all users (avoids stack trace on non-existent user)
        user_exists, existing_user = self.check_user_exists(username)
        if not user_exists:
            self.fail_json(msg=f"User '{username}' does not exist")

        # Build API parameters for user details request
        params = {
            'user': username,
            'includeGroups': 'true'
        }
        if self.params.get('node'):
            params['node'] = self.params['node']

        # Fetch user details from the Technitium API
        data = self.request('/api/admin/users/get', params=params)

        # Check API response status and handle errors
        self.validate_api_response(data)

        # Extract user details from API response
        user_details = data.get('response', {})

        # Return the user details (read-only operation, never changed=True)
        self.exit_json(changed=False, user_details=user_details)


if __name__ == '__main__':
    module = GetUserDetailsModule()
    module.run()
