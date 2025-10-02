#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_convert_to_dynamic_lease
short_description: Convert a reserved DHCP lease to a dynamic lease in Technitium DNS server
version_added: "0.6.0"
description:
    - Convert a reserved lease to a dynamic lease.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_dhcp_leases
    description: List all DHCP leases from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_add_reserved_lease
    description: Add a reserved DHCP lease to a scope in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_remove_reserved_lease
    description: Remove a reserved DHCP lease from a scope in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_reserved_lease
    description: Convert a dynamic DHCP lease to a reserved lease in Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_remove_dhcp_lease
    description: Remove a DHCP lease from Technitium DNS server
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
            - The name of the DHCP scope containing the lease
        required: true
        type: str
    hardwareAddress:
        description:
            - The MAC address of the device bearing the reserved lease
            - Either hardwareAddress or clientIdentifier must be specified
        required: false
        type: str
    clientIdentifier:
        description:
            - The client identifier for the lease
            - Either hardwareAddress or clientIdentifier must be specified
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Convert reserved lease to dynamic by MAC address
  technitium_dns_convert_to_dynamic_lease:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Default"
    hardwareAddress: "00:11:22:33:44:55"

- name: Convert reserved lease to dynamic by client identifier
  technitium_dns_convert_to_dynamic_lease:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Default"
    clientIdentifier: "1-001122334455"
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The core data payload from the API (empty for convert operations)
            type: dict
            returned: always
            sample: {}
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to convert the lease
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to convert the lease
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the result
    type: str
    returned: always
    sample: "Reserved lease for MAC '00:11:22:33:44:55' converted to dynamic in scope 'Default'."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class ConvertToDynamicLeaseModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True),
        hardwareAddress=dict(type='str', required=False),
        clientIdentifier=dict(type='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True,
        required_one_of=[['hardwareAddress', 'clientIdentifier']]
    )

    def run(self):
        scope_name = self.params['name']
        hardware_address = self.params.get('hardwareAddress')
        client_identifier = self.params.get('clientIdentifier')

        # Normalize MAC address if provided for consistent comparison
        if hardware_address:
            normalized_mac = self.normalize_mac_address(hardware_address)
        else:
            normalized_mac = None

        # Check if the scope exists
        scope_exists, scope_info = self.get_dhcp_scope_status(scope_name)
        if not scope_exists:
            self.fail_json(msg=f"DHCP scope '{scope_name}' does not exist.")

        # List all leases to check current lease status
        leases_data = self.request('/api/dhcp/leases/list')
        self.validate_api_response(leases_data)

        leases = leases_data.get('response', {}).get('leases', [])

        # Find the lease in the specified scope
        found_lease = None
        for lease in leases:
            lease_scope = lease.get('scope', '')

            # Only check leases in the specified scope
            if lease_scope != scope_name:
                continue

            # Check by hardware address if provided
            if hardware_address:
                lease_mac = lease.get('hardwareAddress', '')
                if lease_mac:
                    normalized_lease_mac = self.normalize_mac_address(lease_mac)
                    if normalized_lease_mac == normalized_mac:
                        found_lease = lease
                        break

            # Check by client identifier if provided
            if client_identifier:
                lease_client_id = lease.get('clientIdentifier', '')
                if lease_client_id == client_identifier:
                    found_lease = lease
                    break

        # Build identifier string for messages
        if hardware_address:
            identifier = f"MAC '{hardware_address}'"
        else:
            identifier = f"client identifier '{client_identifier}'"

        # If lease doesn't exist, fail
        if not found_lease:
            self.fail_json(msg=f"DHCP lease for {identifier} does not exist in scope '{scope_name}'.")

        # Check lease type and validate it can be converted
        lease_type = found_lease.get('type', '')

        # If already dynamic, return idempotent success (no action needed in either mode)
        if lease_type == 'Dynamic':
            self.exit_json(
                changed=False,
                msg=f"Lease for {identifier} is already dynamic in scope '{scope_name}'.",
                api_response={"status": "ok"}
            )

        # If not Reserved, fail with clear error
        if lease_type != 'Reserved':
            self.fail_json(
                msg=f"Lease for {identifier} in scope '{scope_name}' has type '{lease_type}', not 'Reserved'. Only reserved leases can be converted to dynamic."
            )

        # Handle check mode - lease is Reserved and will be converted
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Reserved lease for {identifier} would be converted to dynamic in scope '{scope_name}' (check mode).",
                api_response={"status": "ok", "check_mode": True}
            )

        # Build API query parameters
        query = {
            'name': scope_name
        }

        if hardware_address:
            query['hardwareAddress'] = normalized_mac
        if client_identifier:
            query['clientIdentifier'] = client_identifier

        # Convert the lease to dynamic via the Technitium API
        data = self.request('/api/dhcp/leases/convertToDynamic', params=query, method='POST')
        self.validate_api_response(data)

        # Return success - lease was converted
        self.exit_json(
            changed=True,
            msg=f"Reserved lease for {identifier} converted to dynamic in scope '{scope_name}'.",
            api_response=data
        )


if __name__ == '__main__':
    module = ConvertToDynamicLeaseModule()
    module.run()
