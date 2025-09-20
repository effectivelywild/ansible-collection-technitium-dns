#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_create_user
short_description: Create a user account in Technitium DNS server
version_added: "0.4.0"
description:
    - Create a new user account in Technitium DNS server using its API.
    - This will not update existing users; it only creates new ones (see technitium_dns_set_user_details).
    - Note that the password is passed in plaintext to the API and could be logged depending on your setup.
    - Requires Administration: Modify permissions.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_users
    description: List all users from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_delete_user
    description: Delete a user from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_get_user_details
    description: Get user account details from Technitium DNS server
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
    username:
        description:
            - A unique username for the user account
        required: true
        type: str
    password:
        description:
            - A password for the user account
        required: true
        type: str
        no_log: true
    displayName:
        description:
            - The display name for the user account
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Create a user account
  technitium_dns_create_user:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"
    password: "securepassword"
    displayName: "Test User"

- name: Create user in check mode
  technitium_dns_create_user:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "checkuser"
    password: "testpass"
    displayName: "Check Mode User"
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
                displayName:
                    description: Display name of the created user
                    type: str
                    returned: always
                    sample: "Test User"
                username:
                    description: Username of the created user
                    type: str
                    returned: always
                    sample: "testuser"
                disabled:
                    description: Whether the user account is disabled
                    type: bool
                    returned: always
                    sample: false
                previousSessionLoggedOn:
                    description: Timestamp of previous session login
                    type: str
                    returned: always
                    sample: "0001-01-01T00:00:00"
                previousSessionRemoteAddress:
                    description: Remote IP address of previous session
                    type: str
                    returned: always
                    sample: "0.0.0.0"
                recentSessionLoggedOn:
                    description: Timestamp of most recent session login
                    type: str
                    returned: always
                    sample: "0001-01-01T00:00:00"
                recentSessionRemoteAddress:
                    description: Remote IP address of most recent session
                    type: str
                    returned: always
                    sample: "0.0.0.0"
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to create a new user
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to complete the user creation
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the user creation result
    type: str
    returned: always
    sample: "User 'testuser' created."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class CreateUserModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        displayName=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        username = params['username']
        password = params['password']
        display_name = params.get('displayName')

        # Check for existing user to ensure idempotent behavior
        # If user already exists, return success without changes
        users_data = self.request('/api/admin/users/list')
        if users_data.get('status') != 'ok':
            error_msg = users_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check existing users: {error_msg}", api_response=users_data)

        users = users_data.get('response', {}).get('users', [])
        existing_user = next((u for u in users if u.get('username') == username), None)
        if existing_user:
            self.exit_json(
                changed=False,
                msg=f"User '{username}' already exists.",
                user=existing_user,
                api_response=users_data
            )

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"User '{username}' would be created (check mode).",
                api_response={"status": "ok", "check_mode": True, "username": username}
            )

        # Build API query parameters from module arguments
        query = {
            'user': username,
            'pass': password
        }

        # Add optional displayName if provided
        if display_name is not None:
            query['displayName'] = display_name

        # Create the user via the Technitium API
        data = self.request('/api/admin/users/create', params=query, method='POST')
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Technitium API error: {error_msg}", api_response=data)

        # Return success - user was created
        self.exit_json(
            changed=True, msg=f"User '{username}' created.", api_response=data)


if __name__ == '__main__':
    module = CreateUserModule()
    module.run()
