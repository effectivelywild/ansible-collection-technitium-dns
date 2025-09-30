#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_get_dhcp_scope
short_description: Get DHCP scope details from Technitium DNS server
version_added: "0.5.0"
description:
    - Retrieve complete details of a DHCP scope configuration from Technitium DNS server.
    - Returns all scope settings including lease times, DNS settings, exclusions, and reserved leases.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_dhcp_scopes
    description: List all DHCP scopes from Technitium DNS server
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
            - The name of the DHCP scope to get details for
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Get Default DHCP scope details
  technitium_dns_get_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Default"
  register: result

- debug:
    var: result.scope_details

- name: Get details for a custom scope
  technitium_dns_get_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Guest Network"
  register: result

- debug:
    var: result.scope_details
'''

RETURN = r'''
changed:
    description: Whether the module made changes (always false for get operations)
    type: bool
    returned: always
    sample: false
scope_details:
    description: Complete DHCP scope configuration details
    type: dict
    returned: always
    contains:
        name:
            description: Name of the DHCP scope
            type: str
            returned: always
            sample: "Default"
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
        leaseTimeDays:
            description: Lease time in days
            type: int
            returned: always
            sample: 7
        leaseTimeHours:
            description: Lease time in hours
            type: int
            returned: always
            sample: 0
        leaseTimeMinutes:
            description: Lease time in minutes
            type: int
            returned: always
            sample: 0
        offerDelayTime:
            description: Offer delay time in milliseconds
            type: int
            returned: always
            sample: 0
        pingCheckEnabled:
            description: Whether ping check is enabled
            type: bool
            returned: always
            sample: false
        pingCheckTimeout:
            description: Ping check timeout in milliseconds
            type: int
            returned: always
            sample: 1000
        pingCheckRetries:
            description: Number of ping check retries
            type: int
            returned: always
            sample: 2
        domainName:
            description: Domain name for the scope
            type: str
            returned: always
            sample: "local"
        domainSearchList:
            description: List of domain search suffixes
            type: list
            elements: str
            returned: when configured
            sample: ["home.arpa", "lan"]
        dnsUpdates:
            description: Whether DNS updates are enabled
            type: bool
            returned: always
            sample: true
        dnsTtl:
            description: DNS TTL in seconds
            type: int
            returned: always
            sample: 900
        serverAddress:
            description: DHCP server address
            type: str
            returned: when configured
            sample: "192.168.1.1"
        serverHostName:
            description: TFTP server hostname
            type: str
            returned: when configured
            sample: "tftp-server-1"
        bootFileName:
            description: Boot filename
            type: str
            returned: when configured
            sample: "boot.bin"
        routerAddress:
            description: Router/gateway address
            type: str
            returned: always
            sample: "192.168.1.1"
        useThisDnsServer:
            description: Whether to use this DNS server
            type: bool
            returned: always
            sample: false
        dnsServers:
            description: List of DNS server addresses
            type: list
            elements: str
            returned: always
            sample: ["192.168.1.5"]
        winsServers:
            description: List of WINS server addresses
            type: list
            elements: str
            returned: when configured
            sample: ["192.168.1.5"]
        ntpServers:
            description: List of NTP server addresses
            type: list
            elements: str
            returned: when configured
            sample: ["192.168.1.5"]
        staticRoutes:
            description: List of static routes
            type: list
            elements: dict
            returned: when configured
            sample: [{"destination": "172.16.0.0", "subnetMask": "255.255.255.0", "router": "192.168.1.2"}]
        vendorInfo:
            description: List of vendor-specific information
            type: list
            elements: dict
            returned: when configured
        capwapAcIpAddresses:
            description: List of CAPWAP AC IP addresses
            type: list
            elements: str
            returned: when configured
            sample: ["192.168.1.2"]
        tftpServerAddresses:
            description: List of TFTP server addresses
            type: list
            elements: str
            returned: when configured
            sample: ["192.168.1.5", "192.168.1.6"]
        genericOptions:
            description: List of generic DHCP options
            type: list
            elements: dict
            returned: when configured
            sample: [{"code": 150, "value": "C0:A8:01:01"}]
        exclusions:
            description: List of IP address exclusions
            type: list
            elements: dict
            returned: always
            sample: [{"startingAddress": "192.168.1.1", "endingAddress": "192.168.1.10"}]
        reservedLeases:
            description: List of reserved leases
            type: list
            elements: dict
            returned: always
            sample: [{"hostName": null, "hardwareAddress": "00-00-00-00-00-00", "address": "192.168.1.10", "comments": "comments"}]
        allowOnlyReservedLeases:
            description: Whether to allow only reserved leases
            type: bool
            returned: always
            sample: false
        blockLocallyAdministeredMacAddresses:
            description: Whether to block locally administered MAC addresses
            type: bool
            returned: always
            sample: false
        ignoreClientIdentifierOption:
            description: Whether to ignore client identifier option
            type: bool
            returned: always
            sample: true
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class GetDhcpScopeModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        scope_name = self.params['name']

        # Build API parameters for scope details request
        params = {
            'name': scope_name
        }

        # Fetch scope details from the Technitium API
        data = self.request('/api/dhcp/scopes/get', params=params)

        # Check API response status and handle errors
        self.validate_api_response(data)

        # Extract scope details from API response
        scope_details = data.get('response', {})

        # Return the scope details (read-only operation, never changed=True)
        self.exit_json(changed=False, scope_details=scope_details)


if __name__ == '__main__':
    module = GetDhcpScopeModule()
    module.run()
