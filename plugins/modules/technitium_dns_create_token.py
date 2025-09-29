#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_create_token
short_description: Create an API token for a user in Technitium DNS server
version_added: "0.5.0"
description:
    - Create a non-expiring API token for a user in Technitium DNS server using its API.
    - The token allows access to API calls with the same privileges as that of the user.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_sessions
    description: List active user sessions from Technitium DNS server
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
    user:
        description:
            - The username for the user account for which to generate the API token
        required: true
        type: str
    tokenName:
        description:
            - The name of the created token to identify its session
        required: true
        type: str
    return_token:
        description:
            - Whether to return the actual API token value in the response
            - 'WARNING: Setting this to true will expose the sensitive API token in Ansible logs, fact cache, and console output'
            - 'Only use this for testing or when you specifically need the token value for subsequent tasks'
            - 'For production use, keep this false (default) for security'
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Create an API token for a user
  technitium_dns_create_token:
    api_url: "http://localhost"
    api_token: "myapitoken"
    user: "testuser"
    tokenName: "MyToken1"

- name: Create API token and return the actual token value (for testing)
  technitium_dns_create_token:
    api_url: "http://localhost"
    api_token: "myapitoken"
    user: "testuser"
    tokenName: "MyToken1"
    return_token: true
  register: token_result
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
                username:
                    description: Username for which the token was created
                    type: str
                    returned: always
                    sample: "admin"
                tokenName:
                    description: Name of the created token
                    type: str
                    returned: always
                    sample: "MyToken1"
                token:
                    description: The generated API token (sensitive information) or '[NEW_TOKEN_HIDDEN]' if return_token is false
                    type: str
                    returned: always
                    sample: "ddfaecb8e9325e77865ee7e100f89596a65d3eae0e6dddcb33172355b95a64af"
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to create a new token
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to complete the token creation
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the token creation result
    type: str
    returned: always
    sample: "API token 'MyToken1' created for user 'admin'."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class CreateTokenModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        user=dict(type='str', required=True),
        tokenName=dict(type='str', required=True, no_log=False),
        return_token=dict(type='bool', required=False, default=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        username = params['user']
        token_name = params['tokenName']
        return_token = params.get('return_token', False)

        # Check if user exists before attempting to create token
        user_exists, existing_user = self.check_user_exists(username)
        if not user_exists:
            self.fail_json(msg=f"User '{username}' does not exist. Cannot create token for non-existent user.")

        # Check for existing token to ensure idempotent behavior
        token_exists, existing_token = self.check_token_session_exists(username, token_name)
        if token_exists:
            self.exit_json(
                changed=False,
                msg=f"API token '{token_name}' already exists for user '{username}'.",
                api_response={
                    "status": "ok",
                    "response": {
                        "username": existing_token.get('username'),
                        "tokenName": existing_token.get('tokenName'),
                        "token": "[EXISTING_TOKEN_HIDDEN]"
                    }
                }
            )

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"API token '{token_name}' would be created for user '{username}' (check mode).",
                api_response={"status": "ok", "check_mode": True, "username": username, "tokenName": token_name}
            )

        # Build API query parameters from module arguments
        query = {
            'user': username,
            'tokenName': token_name
        }

        # Create the token via the Technitium API
        data = self.request('/api/admin/sessions/createToken', params=query, method='POST')
        self.validate_api_response(data)

        # Sanitize the response to hide the sensitive token before exiting (unless return_token is True)
        if return_token:
            # User explicitly requested the token value - return it as-is with warning in logs
            response_data = data
        else:
            # Default secure behavior - sanitize the token
            response_data = data.copy()
            if 'response' in response_data and 'token' in response_data['response']:
                response_data['response']['token'] = '[NEW_TOKEN_HIDDEN]'

        # Return success - token was created
        self.exit_json(
            changed=True,
            msg=f"API token '{token_name}' created for user '{username}'.",
            api_response=response_data
        )


if __name__ == '__main__':
    module = CreateTokenModule()
    module.run()
