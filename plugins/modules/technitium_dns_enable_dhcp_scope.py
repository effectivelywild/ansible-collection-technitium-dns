#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_enable_dhcp_scope
short_description: Enable a DHCP scope in Technitium DNS server
version_added: "0.6.0"
description:
    - Enable a DHCP scope, allowing the server to start serving DHCP requests.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_disable_dhcp_scope
    description: Disable a DHCP scope in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_set_dhcp_scope
    description: Set DHCP scope configuration in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_list_dhcp_scopes
    description: List all DHCP scopes from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_get_dhcp_scope
    description: Get DHCP scope details from Technitium DNS server
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
    name:
        description:
            - The name of the DHCP scope to enable
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Enable a DHCP scope
  technitium_dns_enable_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Default"
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
            sample: {}
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to enable the DHCP scope
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to enable the DHCP scope
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the result of enabling the DHCP scope
    type: str
    returned: always
    sample: "DHCP scope 'Default' enabled."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class EnableDhcpScopeModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        scope_name = self.params['name']

        # Check if the scope exists and get its current status
        scope_exists, scope_info = self.get_dhcp_scope_status(scope_name)

        if not scope_exists:
            # Scope doesn't exist - cannot enable a non-existent scope
            self.fail_json(msg=f"DHCP scope '{scope_name}' does not exist and cannot be enabled.")

        # The API returns 'enabled' field, so disabled is the opposite
        is_enabled = scope_info.get('enabled', False)
        is_disabled = not is_enabled

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            if is_disabled:
                self.exit_json(changed=True, msg=f"DHCP scope '{scope_name}' would be enabled (check mode)", api_response={})
            else:
                self.exit_json(changed=False, msg=f"DHCP scope '{scope_name}' is already enabled (check mode)", api_response={})

        # Implement idempotent enable behavior
        # If scope is already enabled, return success without changes
        if not is_disabled:
            self.exit_json(
                changed=False,
                msg=f"DHCP scope '{scope_name}' is already enabled.",
                api_response={
                    'status': 'ok',
                    'msg': f"DHCP scope '{scope_name}' is already enabled."
                }
            )

        # Enable the DHCP scope via the Technitium API
        data = self.request('/api/dhcp/scopes/enable', params={'name': scope_name}, method='POST')
        self.validate_api_response(data)

        # Return success - scope was enabled
        self.exit_json(changed=True, msg=f"DHCP scope '{scope_name}' enabled.", api_response=data)


if __name__ == '__main__':
    module = EnableDhcpScopeModule()
    module.run()
