#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_session
short_description: Delete a user session from Technitium DNS server
version_added: "0.5.0"
description:
    - Delete a specified user session from Technitium DNS server using its API.
    - This module is idempotent and will not fail if the session does not exist.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_sessions
    description: List active user sessions from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_create_token
    description: Create an API token for a user in Technitium DNS server
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
    partialToken:
        description:
            - The partial token of the session to delete that was returned by the list of sessions
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Delete a user session
  technitium_dns_delete_session:
    api_url: "http://localhost"
    api_token: "myapitoken"
    partialToken: "ddfaecb8e9325e77"

- name: Delete session in check mode
  technitium_dns_delete_session:
    api_url: "http://localhost"
    api_token: "myapitoken"
    partialToken: "ddfaecb8e9325e77"
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
    description: Whether the module made changes to delete the session
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to complete the session deletion
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the session deletion result
    type: str
    returned: always
    sample: "Session with partial token 'ddfaecb8e9325e77' deleted."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteSessionModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        partialToken=dict(type='str', required=True, no_log=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        partial_token = self.params['partialToken']

        # Check if the session exists to ensure idempotent behavior
        # Idempotent delete: if session doesn't exist, report no changes made
        session_exists, existing_session = self.check_session_exists_by_partial_token(partial_token)

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            if session_exists:
                username = existing_session.get('username', 'unknown')
                session_type = existing_session.get('type', 'unknown')
                self.exit_json(
                    changed=True,
                    msg=f"Session with partial token '{partial_token}' (user: {username}, type: {session_type}) would be deleted (check mode)",
                    api_response={"status": "ok", "check_mode": True}
                )
            else:
                self.exit_json(
                    changed=False,
                    msg=f"Session with partial token '{partial_token}' does not exist (check mode)",
                    api_response={"status": "ok", "check_mode": True}
                )

        # Implement idempotent delete behavior
        # If session doesn't exist, return success without changes (already deleted)
        if not session_exists:
            self.exit_json(
                changed=False,
                msg=f"Session with partial token '{partial_token}' does not exist.",
                api_response={'status': 'ok', 'msg': f"Session with partial token '{partial_token}' does not exist."}
            )

        # Delete the session via the Technitium API
        data = self.request('/api/admin/sessions/delete', params={'partialToken': partial_token}, method='POST')
        self.validate_api_response(data)

        # Extract session info for better messaging
        username = existing_session.get('username', 'unknown')
        session_type = existing_session.get('type', 'unknown')

        # Return success - session was deleted
        self.exit_json(
            changed=True,
            msg=f"Session with partial token '{partial_token}' (user: {username}, type: {session_type}) deleted.",
            api_response=data
        )


if __name__ == '__main__':
    module = DeleteSessionModule()
    module.run()
