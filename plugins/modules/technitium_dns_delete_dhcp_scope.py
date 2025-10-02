#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_dhcp_scope
short_description: Delete a DHCP scope from Technitium DNS server
version_added: "0.6.0"
description:
    - Delete a DHCP scope from Technitium DNS server using its API.
    - Permanently deletes the DHCP scope from disk.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_dhcp_scopes
    description: List all DHCP scopes from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_get_dhcp_scope
    description: Get DHCP scope details from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_set_dhcp_scope
    description: Set DHCP scope configuration in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_enable_dhcp_scope
    description: Enable a DHCP scope in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_disable_dhcp_scope
    description: Disable a DHCP scope in Technitium DNS server
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
            - The name of the DHCP scope to delete
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Delete a DHCP scope
  technitium_dns_delete_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "TestScope"

- name: Delete DHCP scope in check mode
  technitium_dns_delete_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "TestScope"
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
    description: Whether the module made changes to delete the DHCP scope
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to complete the DHCP scope deletion
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the DHCP scope deletion result
    type: str
    returned: always
    sample: "DHCP scope 'TestScope' deleted."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteDhcpScopeModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        scope_name = self.params['name']

        # Check if the scope exists using the list API to avoid fragile error message parsing
        scope_exists, _ = self.get_dhcp_scope_status(scope_name)

        # If scope doesn't exist, return idempotent success (no action needed in either mode)
        if not scope_exists:
            self.exit_json(
                changed=False,
                msg=f"DHCP scope '{scope_name}' does not exist.",
                api_response={'status': 'ok'}
            )

        # Handle check mode - scope exists and would be deleted
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"DHCP scope '{scope_name}' would be deleted (check mode).",
                api_response={'status': 'ok', 'check_mode': True}
            )

        # Delete the DHCP scope via the Technitium API
        data = self.request('/api/dhcp/scopes/delete', params={'name': scope_name}, method='POST')
        self.validate_api_response(data)

        # Return success - scope was deleted
        self.exit_json(changed=True, msg=f"DHCP scope '{scope_name}' deleted.", api_response=data)


if __name__ == '__main__':
    module = DeleteDhcpScopeModule()
    module.run()
