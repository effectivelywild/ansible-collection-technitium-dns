#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_remove_reserved_lease
short_description: Remove a reserved DHCP lease from a scope in Technitium DNS server
version_added: "0.6.0"
description:
    - Remove a reserved lease entry from a specified DHCP scope.
    - This module is idempotent - if the reserved lease doesn't exist, no changes are made.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_add_reserved_lease
    description: Add a reserved DHCP lease to a scope in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_list_dhcp_leases
    description: List all DHCP leases from Technitium DNS server
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
            - The name of the DHCP scope to remove the reserved lease from
        required: true
        type: str
    hardwareAddress:
        description:
            - The MAC address of the client (format can be colon or hyphen separated)
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Remove a reserved DHCP lease
  technitium_dns_remove_reserved_lease:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Default"
    hardwareAddress: "00:11:22:33:44:55"

- name: Remove reserved lease with hyphen-separated MAC
  technitium_dns_remove_reserved_lease:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Office"
    hardwareAddress: "00-AA-BB-CC-DD-EE"

- name: Remove reserved lease in check mode
  technitium_dns_remove_reserved_lease:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Default"
    hardwareAddress: "00:11:22:33:44:55"
  check_mode: true
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The core data payload from the API (empty for remove operations)
            type: dict
            returned: always
            sample: {}
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to remove the reserved lease
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to remove the reserved lease
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the result
    type: str
    returned: always
    sample: "Reserved lease for MAC '00:11:22:33:44:55' removed from scope 'Default'."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class RemoveReservedLeaseModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True),
        hardwareAddress=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        scope_name = self.params['name']
        hardware_address = self.params['hardwareAddress']

        # Normalize MAC address for consistent comparison
        normalized_mac = self.normalize_mac_address(hardware_address)

        # Check if the scope exists
        scope_exists, scope_info = self.get_dhcp_scope_status(scope_name)
        if not scope_exists:
            self.fail_json(msg=f"DHCP scope '{scope_name}' does not exist.")

        # Get scope details to check if the reserved lease exists
        scope_data = self.request('/api/dhcp/scopes/get', params={'name': scope_name})
        self.validate_api_response(scope_data)

        scope_details = scope_data.get('response', {})
        reserved_leases = scope_details.get('reservedLeases', [])

        # Check if the reserved lease exists
        lease_exists = False
        for reserved in reserved_leases:
            reserved_mac = reserved.get('hardwareAddress', '')

            # Normalize the reserved MAC for comparison
            if reserved_mac:
                normalized_reserved_mac = self.normalize_mac_address(reserved_mac)
            else:
                normalized_reserved_mac = ''

            if normalized_reserved_mac == normalized_mac:
                lease_exists = True
                break

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            if lease_exists:
                self.exit_json(
                    changed=True,
                    msg=f"Reserved lease for MAC '{hardware_address}' would be removed from scope '{scope_name}' (check mode).",
                    api_response={"status": "ok", "check_mode": True}
                )
            else:
                self.exit_json(
                    changed=False,
                    msg=f"Reserved lease for MAC '{hardware_address}' does not exist in scope '{scope_name}' (check mode).",
                    api_response={"status": "ok", "check_mode": True}
                )

        # Implement idempotent remove behavior
        # If lease doesn't exist, return success without changes (already removed)
        if not lease_exists:
            self.exit_json(
                changed=False,
                msg=f"Reserved lease for MAC '{hardware_address}' does not exist in scope '{scope_name}'.",
                api_response={"status": "ok"}
            )

        # Build API query parameters
        query = {
            'name': scope_name,
            'hardwareAddress': hardware_address
        }

        # Remove the reserved lease via the Technitium API
        data = self.request('/api/dhcp/scopes/removeReservedLease', params=query, method='POST')
        self.validate_api_response(data)

        # Return success - reserved lease was removed
        self.exit_json(
            changed=True,
            msg=f"Reserved lease for MAC '{hardware_address}' removed from scope '{scope_name}'.",
            api_response=data
        )


if __name__ == '__main__':
    module = RemoveReservedLeaseModule()
    module.run()
