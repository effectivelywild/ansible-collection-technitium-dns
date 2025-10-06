#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_dhcp_leases
short_description: List all DHCP leases
version_added: "0.6.0"
description:
    - Retrieve a list of all DHCP leases.
    - Lists both dynamic and reserved leases across all scopes.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_add_reserved_lease
    description: Add a reserved DHCP lease to a scope
  - module: effectivelywild.technitium_dns.technitium_dns_remove_reserved_lease
    description: Remove a reserved DHCP lease from a scope
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_reserved_lease
    description: Convert a dynamic DHCP lease to a reserved lease
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_dynamic_lease
    description: Convert a reserved DHCP lease to a dynamic lease
  - module: effectivelywild.technitium_dns.technitium_dns_remove_dhcp_lease
    description: Remove a DHCP lease
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
'''

EXAMPLES = r'''
- name: List all DHCP leases
  technitium_dns_list_dhcp_leases:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.leases

- name: Find leases for a specific MAC address
  technitium_dns_list_dhcp_leases:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: leases_result

- name: Filter for specific MAC
  set_fact:
    my_lease: "{{ leases_result.leases | selectattr('hardwareAddress', 'equalto', '00-11-22-33-44-55') | list }}"
'''

RETURN = r'''
leases:
    description: List of DHCP leases from the Technitium DNS server
    type: list
    returned: always
    elements: dict
    contains:
        scope:
            description: Name of the DHCP scope this lease belongs to
            type: str
            returned: always
            sample: "Default"
        type:
            description: Type of lease (Dynamic or Reserved)
            type: str
            returned: always
            sample: "Dynamic"
        hardwareAddress:
            description: MAC address of the client
            type: str
            returned: always
            sample: "00-11-22-33-44-55"
        clientIdentifier:
            description: DHCP client identifier
            type: str
            returned: always
            sample: "1-001122334455"
        address:
            description: Leased IP address
            type: str
            returned: always
            sample: "192.168.1.100"
        hostName:
            description: Hostname of the client
            type: str
            returned: when available
            sample: "client.local"
        leaseObtained:
            description: Timestamp when lease was obtained
            type: str
            returned: always
            sample: "08/25/2020 17:52:51"
        leaseExpires:
            description: Timestamp when lease expires
            type: str
            returned: always
            sample: "09/26/2020 14:27:12"
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


class ListDhcpLeasesModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Fetch all DHCP leases from the API
        data = self.request('/api/dhcp/leases/list')
        self.validate_api_response(data)

        leases = data.get('response', {}).get('leases', [])
        self.exit_json(changed=False, leases=leases)


if __name__ == '__main__':
    module = ListDhcpLeasesModule()
    module.run()
