#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_sessions
short_description: List active user sessions from Technitium DNS server
version_added: "0.5.0"
description:
    - Retrieve a list of all active user sessions from a Technitium DNS server.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_delete_session
    description: Delete active user sessions from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_create_token
    description: Create an API token for a user in Technitium DNS server
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
            - Whether to validate SSL certificates when making API requests.
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: List all active sessions from Technitium DNS
  technitium_dns_list_sessions:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.sessions
'''

RETURN = r'''
sessions:
    description: List of active sessions from the Technitium DNS server
    type: list
    returned: always
    elements: dict
    contains:
        username:
            description: Username for the session
            type: str
            returned: always
            sample: "admin"
        isCurrentSession:
            description: Whether this is the current session
            type: bool
            returned: always
            sample: true
        partialToken:
            description: Partial token for the session
            type: str
            returned: always
            sample: "272f4890427b9ab5"
        type:
            description: Type of session (Standard or ApiToken)
            type: str
            returned: always
            sample: "Standard"
        tokenName:
            description: Name of the API token (null for standard sessions)
            type: str
            returned: always
            sample: "MyToken1"
        lastSeen:
            description: Timestamp of last activity (ISO 8601 format)
            type: str
            returned: always
            sample: "2022-09-17T13:23:44.9972772Z"
        lastSeenRemoteAddress:
            description: Remote IP address of last activity
            type: str
            returned: always
            sample: "127.0.0.1"
        lastSeenUserAgent:
            description: User agent string of last activity
            type: str
            returned: always
            sample: "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
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


class ListSessionsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Fetch all sessions from the API
        data = self.request('/api/admin/sessions/list')
        self.validate_api_response(data)

        sessions = data.get('response', {}).get('sessions', [])
        self.exit_json(changed=False, sessions=sessions)


if __name__ == '__main__':
    module = ListSessionsModule()
    module.run()
