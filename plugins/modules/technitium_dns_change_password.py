#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_change_password
short_description: Change password for the currently logged in user in Technitium DNS server
version_added: "0.5.0"
description:
    - Change the password for the current logged in user account.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_set_user_details
    description: Set user account details in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_get_user_details
    description: Get user account details in Technitium DNS server
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
    pass:
        description:
            - The new password for the currently logged in user
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Change admin password
  technitium_dns_change_password:
    api_url: "http://localhost"
    api_token: "myapitoken"
    pass: "NewSecurePassword123!"

- name: Change password in check mode
  technitium_dns_change_password:
    api_url: "http://localhost"
    api_token: "myapitoken"
    pass: "NewSecurePassword123!"
  check_mode: true
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
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
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
msg:
    description: Human readable message describing the result
    type: str
    returned: always
    sample: "Password changed successfully."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class ChangePasswordModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        **{'pass': dict(type='str', required=True, no_log=True)}
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        new_password = params['pass']

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="(check mode) Password would be changed.",
                api_response={"status": "ok", "check_mode": True}
            )

        # Make the API call to change password
        data = self.request('/api/user/changePassword', params={'pass': new_password}, method='POST')
        self.validate_api_response(data)

        # Return success
        self.exit_json(
            changed=True,
            msg="Password changed successfully.",
            api_response=data
        )


if __name__ == '__main__':
    module = ChangePasswordModule()
    module.run()
