#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_set_user_details
short_description: Set user account profile details in Technitium DNS server
version_added: "0.4.0"
description:
    - Change user account profile details in Technitium DNS server.
    - Allows modifying display name, username, password, enabled/disabled status, session timeout, and group memberships.
    - Requires Administration: Modify permissions.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_user
    description: Create a user account in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_delete_user
    description: Delete a user from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_get_user_details
    description: Get user account details from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_list_users
    description: List all users from Technitium DNS server
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
            - The username for the user account to modify
        required: true
        type: str
    displayName:
        description:
            - The display name for the user account
        required: false
        type: str
    newUsername:
        description:
            - A new username for renaming the user account
        required: false
        type: str
    disabled:
        description:
            - Set true to disable the user account and delete all its active sessions
        required: false
        type: bool
    sessionTimeoutSeconds:
        description:
            - A session timeout value in seconds for the user account
        required: false
        type: int
    newPassword:
        description:
            - A new password to reset the user account password
        required: false
        type: str
        no_log: true
    iterations:
        description:
            - The number of iterations for PBKDF2 SHA256 password hashing. Only used with newPassword option.
        required: false
        type: int
    memberOfGroups:
        description:
            - A list of group names that the user must be set as a member
        required: false
        type: list
        elements: str
'''

EXAMPLES = r'''
- name: Update user display name
  technitium_dns_set_user_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"
    displayName: "Updated Test User"

- name: Disable user account
  technitium_dns_set_user_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"
    disabled: true

- name: Change user groups and session timeout
  technitium_dns_set_user_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"
    memberOfGroups:
      - "DNS Administrators"
      - "DHCP Administrators"
    sessionTimeoutSeconds: 3600

- name: Reset user password
  technitium_dns_set_user_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"
    newPassword: "NewSecurePassword123!"
    iterations: 100000

- name: Rename user account
  technitium_dns_set_user_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "oldusername"
    newUsername: "newusername"

- name: Check what would change (check mode)
  technitium_dns_set_user_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"
    displayName: "New Display Name"
    disabled: false
  check_mode: true
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: Updated user details from the API
            type: dict
            returned: always
            contains:
                displayName:
                    description: Display name of the user
                    type: str
                    returned: always
                    sample: "Updated Test User"
                username:
                    description: Username of the user account
                    type: str
                    returned: always
                    sample: "testuser"
                disabled:
                    description: Whether the user account is disabled
                    type: bool
                    returned: always
                    sample: false
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
        "displayName": {
            "current": "Old Name",
            "desired": "New Name"
        },
        "memberOfGroups": {
            "current": ["Administrators"],
            "desired": ["DNS Administrators", "DHCP Administrators"]
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
    sample: "User details updated successfully."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class SetUserDetailsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        username=dict(type='str', required=True),
        displayName=dict(type='str', required=False),
        newUsername=dict(type='str', required=False),
        disabled=dict(type='bool', required=False),
        sessionTimeoutSeconds=dict(type='int', required=False),
        newPassword=dict(type='str', required=False, no_log=True),
        iterations=dict(type='int', required=False),
        memberOfGroups=dict(type='list', elements='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _normalize_value(self, key, value):
        """Normalize values for consistent comparison"""
        if key == 'memberOfGroups':
            if not isinstance(value, list):
                return []
            return sorted(value)

        return value

    def run(self):
        params = self.params
        username = params['username']

        # Check if user exists by listing all users (avoids stack trace on non-existent user)
        users_data = self.request('/api/admin/users/list')
        if users_data.get('status') != 'ok':
            error_msg = users_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check existing users: {error_msg}", api_response=users_data)

        users = users_data.get('response', {}).get('users', [])
        existing_user = next((u for u in users if u.get('username') == username), None)
        if existing_user is None:
            self.fail_json(msg=f"User '{username}' does not exist")

        # Fetch detailed user information including groups
        current_data = self.request('/api/admin/users/get', params={'user': username, 'includeGroups': 'true'})
        if current_data.get('status') != 'ok':
            error_msg = current_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to get current user details: {error_msg}", api_response=current_data)

        current = current_data.get('response', {})

        # Build desired state dict from provided parameters
        desired = {}
        for key in ['displayName', 'newUsername', 'disabled', 'sessionTimeoutSeconds', 'newPassword', 'iterations', 'memberOfGroups']:
            value = params.get(key)
            if value is not None:
                # Validate input types
                if key == 'memberOfGroups':
                    if not isinstance(value, list):
                        self.fail_json(msg=f"Parameter '{key}' must be a list, got {type(value).__name__}")
                if key == 'sessionTimeoutSeconds':
                    if not isinstance(value, int) or value <= 0:
                        self.fail_json(msg=f"Parameter '{key}' must be a positive integer, got {value}")
                if key == 'iterations':
                    if not isinstance(value, int) or value <= 0:
                        self.fail_json(msg=f"Parameter '{key}' must be a positive integer, got {value}")

                desired[key] = value

        # Compare current vs desired for idempotency (excluding password fields)
        # We can't check password/iterations since they're not returned by the API
        diff = {}
        checkable_fields = {
            'displayName': 'displayName',
            'newUsername': 'username',  # newUsername becomes username in response
            'disabled': 'disabled',
            'sessionTimeoutSeconds': 'sessionTimeoutSeconds',
            'memberOfGroups': 'memberOfGroups'
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

        # Always consider password changes as requiring updates if provided
        if 'newPassword' in desired:
            diff['newPassword'] = {
                'current': '[HIDDEN]',
                'desired': '[HIDDEN]'
            }

        # If no changes needed, exit early
        if not diff:
            self.exit_json(changed=False, msg="User details already match desired state.")

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="(check mode) User details would be updated.",
                diff=diff,
                api_response={"status": "ok", "check_mode": True, "username": username}
            )

        # Set user details via the Technitium API
        set_query = {'user': username}

        # Map parameters to API parameter names
        param_mapping = {
            'displayName': 'displayName',
            'newUsername': 'newUser',
            'disabled': 'disabled',
            'sessionTimeoutSeconds': 'sessionTimeoutSeconds',
            'newPassword': 'newPass',
            'iterations': 'iterations',
            'memberOfGroups': 'memberOfGroups'
        }

        for param_key, api_key in param_mapping.items():
            if param_key in desired:
                value = desired[param_key]
                if param_key == 'memberOfGroups' and isinstance(value, list):
                    # Convert list to comma-separated string for API
                    set_query[api_key] = ",".join(value)
                elif param_key == 'disabled' and isinstance(value, bool):
                    # Convert boolean to lowercase string for API
                    set_query[api_key] = str(value).lower()
                else:
                    set_query[api_key] = value

        # Make the API call to set user details
        data = self.request('/api/admin/users/set', params=set_query, method='POST')
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        # Return success with changes made
        self.exit_json(
            changed=True,
            msg="User details updated successfully.",
            diff=diff,
            api_response=data
        )


if __name__ == '__main__':
    module = SetUserDetailsModule()
    module.run()