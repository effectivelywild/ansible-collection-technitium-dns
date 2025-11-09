#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_login
short_description: Authenticate and get a session token
version_added: "1.0.0"
description:
    - Authenticates with the Technitium DNS server using username and password.
    - Generates a session token that can be used for subsequent API calls.
    - Session tokens expire based on user's session expiry timeout (default 30 minutes from last API call).
    - Useful when API tokens have been invalidated, such as after joining a cluster.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
notes:
    - This operation requires no permissions (it's the authentication endpoint).
    - The session token returned expires after the configured session timeout.
    - It is recommended to change default passwords on first use.
options:
    api_port:
        description:
            - Port for the Technitium DNS API. Defaults to 5380
        required: false
        type: int
        default: 5380
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
    username:
        description:
            - The username for the user account.
            - The built-in administrator username is 'admin'.
        required: true
        type: str
    password:
        description:
            - The password for the user account.
            - The default password for admin user is 'admin'.
        required: true
        type: str
    totp:
        description:
            - The time-based one-time password if 2FA is enabled for the user account.
        required: false
        type: str
    include_info:
        description:
            - Include basic user info and permissions in the response.
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: Login and get session token
  effectivelywild.technitium_dns.technitium_dns_login:
    api_url: "http://localhost"
    username: "admin"
    password: "admin"
  register: login_result

- name: Display session token
  debug:
    var: login_result.token

- name: Login with 2FA
  effectivelywild.technitium_dns.technitium_dns_login:
    api_url: "http://localhost"
    username: "admin"
    password: "mypassword"
    totp: "123456"
  register: login_result

- name: Login and get user info
  effectivelywild.technitium_dns.technitium_dns_login:
    api_url: "http://localhost"
    username: "admin"
    password: "admin"
    include_info: true
  register: login_result

- name: Use session token in subsequent calls
  effectivelywild.technitium_dns.technitium_dns_get_cluster_state:
    api_url: "http://localhost"
    api_token: "{{ login_result.token }}"
  register: cluster_state
'''

RETURN = r'''
token:
    description: Session token to use for subsequent API calls
    type: str
    returned: always
    sample: "932b2a3495852c15af01598f62563ae534460388b6a370bfbbb8bb6094b698e9"
display_name:
    description: Display name of the authenticated user
    type: str
    returned: always
    sample: "Administrator"
username:
    description: Username of the authenticated user
    type: str
    returned: always
    sample: "admin"
totp_enabled:
    description: Whether 2FA is enabled for this user
    type: bool
    returned: always
    sample: false
info:
    description: User information and permissions (when include_info is true)
    type: dict
    returned: when include_info is true
    contains:
        version:
            description: Technitium DNS Server version
            type: str
            sample: "14.0"
        dnsServerDomain:
            description: DNS server domain name
            type: str
            sample: "server1"
        defaultRecordTtl:
            description: Default TTL for records
            type: int
            sample: 3600
        permissions:
            description: User permissions for various sections
            type: dict
changed:
    description: Whether the module made changes (always false for login)
    type: bool
    returned: always
    sample: false
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
msg:
    description: Status message
    type: str
    returned: always
    sample: "Login successful"
'''

import json
from urllib.parse import urlencode
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_url=dict(type='str', required=True),
            api_port=dict(type='int', required=False, default=5380),
            validate_certs=dict(type='bool', required=False, default=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            totp=dict(type='str', required=False, no_log=True),
            include_info=dict(type='bool', required=False, default=True)
        ),
        supports_check_mode=True
    )

    api_url = module.params['api_url'].rstrip('/')
    api_port = module.params.get('api_port', 5380)
    validate_certs = module.params.get('validate_certs', True)
    username = module.params['username']
    password = module.params['password']
    totp = module.params.get('totp')
    include_info = module.params.get('include_info', True)

    # In check mode, we can't actually login
    if module.check_mode:
        module.exit_json(
            changed=False,
            msg="Would attempt to login (check mode)"
        )

    # Build login parameters
    login_params = {
        'user': username,
        'pass': password,
        'includeInfo': 'true' if include_info else 'false'
    }

    if totp:
        login_params['totp'] = totp

    # Make login request
    url = f"{api_url}:{api_port}/api/user/login"
    url_with_params = url + '?' + urlencode(login_params)

    try:
        resp, info = fetch_url(
            module,
            url_with_params,
            method='GET',
            headers={'Accept': 'application/json'},
            timeout=10
        )

        # Check if response is None (connection/transport failed)
        if resp is None:
            error_msg = "Login request failed - no response received"
            if 'msg' in info:
                error_msg += f": {info['msg']}"
            module.fail_json(msg=error_msg)

        # Check if the request failed with HTTP error status
        if info['status'] >= 400:
            error_msg = f"Login request failed with status {info['status']}"
            if 'msg' in info:
                error_msg += f": {info['msg']}"
            module.fail_json(msg=error_msg)

        data = json.loads(resp.read().decode('utf-8'))

        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Login failed"
            module.fail_json(msg=error_msg, api_response=data)

        # Extract response data
        result = {
            'changed': False,
            'token': data.get('token'),
            'display_name': data.get('displayName'),
            'username': data.get('username'),
            'totp_enabled': data.get('totpEnabled', False),
            'msg': 'Login successful'
        }

        if include_info and 'info' in data:
            result['info'] = data['info']

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Login request failed: {e}")


if __name__ == '__main__':
    main()
