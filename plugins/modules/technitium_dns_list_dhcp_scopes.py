#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_dhcp_scopes
short_description: List all DHCP scopes from Technitium DNS server
version_added: "0.5.0"
description:
    - Retrieve a list of all DHCP scopes available on the Technitium DNS server.
author:
    - Frank Muise (@effectivelywild)
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
- name: List all DHCP scopes from Technitium DNS
  technitium_dns_list_dhcp_scopes:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.scopes

- name: Check if a specific scope exists
  technitium_dns_list_dhcp_scopes:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: scopes_result

- name: Verify Default scope exists
  assert:
    that:
      - scopes_result.scopes | selectattr('name', 'equalto', 'Default') | list | length > 0
    fail_msg: "Default scope not found"
'''

RETURN = r'''
scopes:
    description: List of DHCP scopes from the Technitium DNS server
    type: list
    returned: always
    elements: dict
    contains:
        name:
            description: Name of the DHCP scope
            type: str
            returned: always
            sample: "Default"
        enabled:
            description: Whether the DHCP scope is enabled
            type: bool
            returned: always
            sample: false
        startingAddress:
            description: Starting IP address of the DHCP scope
            type: str
            returned: always
            sample: "192.168.1.1"
        endingAddress:
            description: Ending IP address of the DHCP scope
            type: str
            returned: always
            sample: "192.168.1.254"
        subnetMask:
            description: Subnet mask for the DHCP scope
            type: str
            returned: always
            sample: "255.255.255.0"
        networkAddress:
            description: Network address of the DHCP scope
            type: str
            returned: always
            sample: "192.168.1.0"
        broadcastAddress:
            description: Broadcast address of the DHCP scope
            type: str
            returned: always
            sample: "192.168.1.255"
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


class ListDhcpScopesModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Fetch all DHCP scopes from the API
        data = self.request('/api/dhcp/scopes/list')
        self.validate_api_response(data)

        scopes = data.get('response', {}).get('scopes', [])
        self.exit_json(changed=False, scopes=scopes)


if __name__ == '__main__':
    module = ListDhcpScopesModule()
    module.run()
