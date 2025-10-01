#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_disable_dhcp_scope
short_description: Disable a DHCP scope in Technitium DNS server
version_added: "0.5.0"
description:
    - Disable a DHCP scope, stopping any further lease allocations.
    - This will prevent the DHCP server from allocating leases from this scope.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_enable_dhcp_scope
    description: Enable a DHCP scope in Technitium DNS server
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
            - The name of the DHCP scope to disable
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Disable a DHCP scope
  technitium_dns_disable_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Default"

- name: Disable DHCP scope in check mode
  technitium_dns_disable_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Office Network"
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
            sample: {}
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to disable the DHCP scope
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to disable the DHCP scope
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the result of disabling the DHCP scope
    type: str
    returned: always
    sample: "DHCP scope 'Default' disabled."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DisableDhcpScopeModule(TechnitiumModule):
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
            # Scope doesn't exist - cannot disable a non-existent scope
            self.fail_json(msg=f"DHCP scope '{scope_name}' does not exist and cannot be disabled.")

        # The API returns 'enabled' field, so disabled is the opposite
        is_enabled = scope_info.get('enabled', False)
        is_disabled = not is_enabled

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            if not is_disabled:
                self.exit_json(changed=True, msg=f"DHCP scope '{scope_name}' would be disabled (check mode)", api_response={})
            else:
                self.exit_json(changed=False, msg=f"DHCP scope '{scope_name}' is already disabled (check mode)", api_response={})

        # Implement idempotent disable behavior
        # If scope is already disabled, return success without changes
        if is_disabled:
            self.exit_json(
                changed=False, msg=f"DHCP scope '{scope_name}' is already disabled.",
                api_response={'status': 'ok', 'msg': f"DHCP scope '{scope_name}' is already disabled."})

        # Disable the DHCP scope via the Technitium API
        data = self.request('/api/dhcp/scopes/disable', params={'name': scope_name}, method='POST')
        self.validate_api_response(data)

        # Return success - scope was disabled
        self.exit_json(changed=True, msg=f"DHCP scope '{scope_name}' disabled.", api_response=data)


if __name__ == '__main__':
    module = DisableDhcpScopeModule()
    module.run()
