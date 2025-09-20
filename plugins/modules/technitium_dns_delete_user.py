#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_user
short_description: Delete a user account from Technitium DNS server
version_added: "0.4.0"
description:
    - Delete a user account from Technitium DNS server using its API.
    - Requires Administration: Delete permissions.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_user
    description: Create a user account in Technitium DNS server
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
            - The username for the user account to delete
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Delete a user account
  technitium_dns_delete_user:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"

- name: Delete user in check mode
  technitium_dns_delete_user:
    api_url: "http://localhost"
    api_token: "myapitoken"
    username: "testuser"
  check_mode: true
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The core data payload from the API (empty for delete operations)
            type: dict
            returned: always
            sample: {}
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to delete the user
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to complete the user deletion
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the user deletion result
    type: str
    returned: always
    sample: "User 'testuser' deleted."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteUserModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        username=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        username = self.params['username']

        # Check if the user exists to ensure idempotent behavior
        # Idempotent delete: if user doesn't exist, report no changes made
        user_exists, existing_user = self.check_user_exists(username)

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            if user_exists:
                self.exit_json(changed=True, msg=f"User '{username}' would be deleted (check mode)", api_response={})
            else:
                self.exit_json(changed=False, msg=f"User '{username}' does not exist (check mode)", api_response={})

        # Implement idempotent delete behavior
        # If user doesn't exist, return success without changes (already deleted)
        if not user_exists:
            self.exit_json(
                changed=False,
                msg=f"User '{username}' does not exist.",
                api_response={'status': 'ok', 'msg': f"User '{username}' does not exist."}
            )

        # Delete the user via the Technitium API
        data = self.request('/api/admin/users/delete', params={'user': username}, method='POST')
        self.validate_api_response(data)

        # Return success - user was deleted
        self.exit_json(changed=True, msg=f"User '{username}' deleted.", api_response=data)


if __name__ == '__main__':
    module = DeleteUserModule()
    module.run()