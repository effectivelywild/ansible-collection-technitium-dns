#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_set_dhcp_scope
short_description: Set DHCP scope configuration in Technitium DNS server
version_added: "0.6.0"
description:
    - Set or create DHCP scope configuration on Technitium DNS server.
    - If the scope does not exist, it will be created.
author:
    - Frank Muise (@effectivelywild)
seealso:
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
            - The name of the DHCP scope
        required: true
        type: str
    newName:
        description:
            - The new name of the DHCP scope to rename an existing scope
        required: false
        type: str
    startingAddress:
        description:
            - The starting IP address of the DHCP scope
            - Required when creating a new scope
        required: false
        type: str
    endingAddress:
        description:
            - The ending IP address of the DHCP scope
            - Required when creating a new scope
        required: false
        type: str
    subnetMask:
        description:
            - The subnet mask of the network
            - Required when creating a new scope
        required: false
        type: str
    leaseTimeDays:
        description:
            - The lease time in number of days
        required: false
        type: int
    leaseTimeHours:
        description:
            - The lease time in number of hours
        required: false
        type: int
    leaseTimeMinutes:
        description:
            - The lease time in number of minutes
        required: false
        type: int
    offerDelayTime:
        description:
            - The time duration in milliseconds that the DHCP server delays sending an DHCPOFFER message
        required: false
        type: int
    pingCheckEnabled:
        description:
            - Allow the DHCP server to check if an IP address is already in use to prevent IP address conflicts
        required: false
        type: bool
    pingCheckTimeout:
        description:
            - The timeout interval in milliseconds to wait for a ping reply
        required: false
        type: int
    pingCheckRetries:
        description:
            - The maximum number of ping requests to try
        required: false
        type: int
    domainName:
        description:
            - The domain name to be used by this network
            - The DHCP server automatically adds forward and reverse DNS entries when configured
        required: false
        type: str
    domainSearchList:
        description:
            - List of domain names that clients can use as a suffix when searching a domain name
        required: false
        type: list
        elements: str
    dnsUpdates:
        description:
            - Allow the DHCP server to automatically update forward and reverse DNS entries for clients
        required: false
        type: bool
    dnsTtl:
        description:
            - The TTL value in seconds used for forward and reverse DNS records
        required: false
        type: int
    serverAddress:
        description:
            - The IP address of next server (TFTP) to use in bootstrap by the clients
            - If not specified, the DHCP server's IP address is used
        required: false
        type: str
    serverHostName:
        description:
            - The optional bootstrap server host name to be used by clients to identify the TFTP server
        required: false
        type: str
    bootFileName:
        description:
            - The boot file name stored on the bootstrap TFTP server to be used by clients
        required: false
        type: str
    routerAddress:
        description:
            - The default gateway IP address to be used by the clients
        required: false
        type: str
    useThisDnsServer:
        description:
            - Use this DNS server's IP address to configure the DNS Servers DHCP option for clients
        required: false
        type: bool
    dnsServers:
        description:
            - List of DNS server IP addresses to be used by the clients
            - Ignored when useThisDnsServer is set to true
        required: false
        type: list
        elements: str
    winsServers:
        description:
            - List of NBNS/WINS server IP addresses to be used by the clients
        required: false
        type: list
        elements: str
    ntpServers:
        description:
            - List of Network Time Protocol (NTP) server IP addresses to be used by the clients
        required: false
        type: list
        elements: str
    ntpServerDomainNames:
        description:
            - List of NTP server domain names that the DHCP server should automatically resolve
        required: false
        type: list
        elements: str
    staticRoutes:
        description:
            - List of static routes for clients
        required: false
        type: list
        elements: dict
        suboptions:
            destination:
                description: Destination network address
                type: str
                required: true
            subnetMask:
                description: Subnet mask for the destination
                type: str
                required: true
            router:
                description: Router/gateway address for this route
                type: str
                required: true
    vendorInfo:
        description:
            - List of vendor information entries
        required: false
        type: list
        elements: dict
        suboptions:
            identifier:
                description: Vendor class identifier
                type: str
                required: true
            information:
                description: Vendor specific information as colon-separated or normal hex string
                type: str
                required: true
    capwapAcIpAddresses:
        description:
            - List of CAPWAP Access Controller IP addresses for Wireless Termination Points
        required: false
        type: list
        elements: str
    tftpServerAddresses:
        description:
            - List of TFTP Server addresses or VoIP Configuration Server addresses
        required: false
        type: list
        elements: str
    genericOptions:
        description:
            - List of generic DHCP options not directly supported
        required: false
        type: list
        elements: dict
        suboptions:
            code:
                description: DHCP option code
                type: int
                required: true
            value:
                description: Option value as colon-separated or normal hex string
                type: str
                required: true
    exclusions:
        description:
            - List of IP address ranges to exclude from dynamic allocation
        required: false
        type: list
        elements: dict
        suboptions:
            startingAddress:
                description: Starting IP address of exclusion range
                type: str
                required: true
            endingAddress:
                description: Ending IP address of exclusion range
                type: str
                required: true
    reservedLeases:
        description:
            - List of reserved IP addresses to assign to specific clients
        required: false
        type: list
        elements: dict
        suboptions:
            hostName:
                description: Host name for the reserved lease
                type: str
                required: false
            hardwareAddress:
                description: MAC address of the client
                type: str
                required: true
            address:
                description: Reserved IP address
                type: str
                required: true
            comments:
                description: Comments for this reservation
                type: str
                required: false
    allowOnlyReservedLeases:
        description:
            - Stop dynamic IP address allocation and allocate only reserved IP addresses
        required: false
        type: bool
    blockLocallyAdministeredMacAddresses:
        description:
            - Stop dynamic IP address allocation for clients with locally administered MAC addresses
        required: false
        type: bool
    ignoreClientIdentifierOption:
        description:
            - Always use the client's MAC address as the identifier instead of Client Identifier option
        required: false
        type: bool
'''

EXAMPLES = r'''
- name: Create a new DHCP scope
  technitium_dns_set_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Office Network"
    startingAddress: "10.0.1.1"
    endingAddress: "10.0.1.254"
    subnetMask: "255.255.255.0"
    routerAddress: "10.0.1.1"
    leaseTimeDays: 7

- name: Update existing scope with DNS settings
  technitium_dns_set_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Office Network"
    domainName: "office.local"
    useThisDnsServer: true
    dnsUpdates: true
    dnsTtl: 900

- name: Configure scope with exclusions and reserved leases
  technitium_dns_set_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Office Network"
    exclusions:
      - startingAddress: "10.0.1.1"
        endingAddress: "10.0.1.10"
    reservedLeases:
      - hostName: "printer"
        hardwareAddress: "00-11-22-33-44-55"
        address: "10.0.1.100"
        comments: "Office printer"

- name: Rename a scope
  technitium_dns_set_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Office Network"
    newName: "Main Office Network"

- name: Check what would change (check mode)
  technitium_dns_set_dhcp_scope:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Office Network"
    leaseTimeDays: 14
  check_mode: true
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: Response data from the API
            type: dict
            returned: always
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes
    type: bool
    returned: always
    sample: true
diff:
    description: Dictionary showing what changed, with current and desired values
    type: dict
    returned: when changes are made
    sample: {
        "leaseTimeDays": {
            "current": 7,
            "desired": 14
        }
    }
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
msg:
    description: Human readable message describing the result
    type: str
    returned: always
    sample: "DHCP scope configuration updated successfully."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class SetDhcpScopeModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True),
        newName=dict(type='str', required=False),
        startingAddress=dict(type='str', required=False),
        endingAddress=dict(type='str', required=False),
        subnetMask=dict(type='str', required=False),
        leaseTimeDays=dict(type='int', required=False),
        leaseTimeHours=dict(type='int', required=False),
        leaseTimeMinutes=dict(type='int', required=False),
        offerDelayTime=dict(type='int', required=False),
        pingCheckEnabled=dict(type='bool', required=False),
        pingCheckTimeout=dict(type='int', required=False),
        pingCheckRetries=dict(type='int', required=False),
        domainName=dict(type='str', required=False),
        domainSearchList=dict(type='list', elements='str', required=False),
        dnsUpdates=dict(type='bool', required=False),
        dnsTtl=dict(type='int', required=False),
        serverAddress=dict(type='str', required=False),
        serverHostName=dict(type='str', required=False),
        bootFileName=dict(type='str', required=False),
        routerAddress=dict(type='str', required=False),
        useThisDnsServer=dict(type='bool', required=False),
        dnsServers=dict(type='list', elements='str', required=False),
        winsServers=dict(type='list', elements='str', required=False),
        ntpServers=dict(type='list', elements='str', required=False),
        ntpServerDomainNames=dict(type='list', elements='str', required=False),
        staticRoutes=dict(
            type='list',
            elements='dict',
            required=False,
            options=dict(
                destination=dict(type='str', required=True),
                subnetMask=dict(type='str', required=True),
                router=dict(type='str', required=True)
            )
        ),
        vendorInfo=dict(
            type='list',
            elements='dict',
            required=False,
            options=dict(
                identifier=dict(type='str', required=True),
                information=dict(type='str', required=True)
            )
        ),
        capwapAcIpAddresses=dict(type='list', elements='str', required=False),
        tftpServerAddresses=dict(type='list', elements='str', required=False),
        genericOptions=dict(
            type='list',
            elements='dict',
            required=False,
            options=dict(
                code=dict(type='int', required=True),
                value=dict(type='str', required=True)
            )
        ),
        exclusions=dict(
            type='list',
            elements='dict',
            required=False,
            options=dict(
                startingAddress=dict(type='str', required=True),
                endingAddress=dict(type='str', required=True)
            )
        ),
        reservedLeases=dict(
            type='list',
            elements='dict',
            required=False,
            options=dict(
                hostName=dict(type='str', required=False),
                hardwareAddress=dict(type='str', required=True),
                address=dict(type='str', required=True),
                comments=dict(type='str', required=False)
            )
        ),
        allowOnlyReservedLeases=dict(type='bool', required=False),
        blockLocallyAdministeredMacAddresses=dict(type='bool', required=False),
        ignoreClientIdentifierOption=dict(type='bool', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _normalize_value(self, key, value):
        """Normalize a value for comparison purposes."""
        list_like_fields = [
            'domainSearchList', 'dnsServers', 'winsServers', 'ntpServers',
            'ntpServerDomainNames', 'capwapAcIpAddresses', 'tftpServerAddresses'
        ]
        list_of_dict_fields = ['staticRoutes', 'vendorInfo', 'genericOptions', 'exclusions', 'reservedLeases']

        # Handle None/empty values
        if value in [None, "", []]:
            return [] if key in list_like_fields or key in list_of_dict_fields else None

        # Normalize booleans
        if isinstance(value, bool):
            return value

        # Normalize list-like fields (simple lists)
        if key in list_like_fields:
            if isinstance(value, list):
                return sorted([str(x) for x in value])
            elif isinstance(value, str):
                return sorted([x.strip() for x in value.split(",") if x.strip()])
            else:
                return sorted([str(value)])

        # Normalize list of dict fields
        if key in list_of_dict_fields:
            if not isinstance(value, list):
                return []
            normalized_list = []
            for item in value:
                if isinstance(item, dict):
                    normalized_list.append(dict(item))
            # Sort for consistent comparison
            if key == 'staticRoutes':
                return sorted(normalized_list, key=lambda x: (x.get('destination', ''), x.get('subnetMask', '')))
            elif key == 'vendorInfo':
                return sorted(normalized_list, key=lambda x: x.get('identifier', ''))
            elif key == 'genericOptions':
                return sorted(normalized_list, key=lambda x: x.get('code', 0))
            elif key == 'exclusions':
                return sorted(normalized_list, key=lambda x: x.get('startingAddress', ''))
            elif key == 'reservedLeases':
                return sorted(normalized_list, key=lambda x: x.get('hardwareAddress', ''))
            return sorted(normalized_list, key=str)

        return value

    def run(self):
        params = self.params
        scope_name = params['name']

        # Check if scope exists
        scope_exists = False
        current = {}
        try:
            get_data = self.request('/api/dhcp/scopes/get', params={'name': scope_name})
            if get_data.get('status') == 'ok':
                scope_exists = True
                current = get_data.get('response', {})
        except Exception:
            # Scope doesn't exist, will be created
            scope_exists = False

        # If creating a new scope, require startingAddress, endingAddress, and subnetMask
        if not scope_exists:
            required_for_create = ['startingAddress', 'endingAddress', 'subnetMask']
            missing = [p for p in required_for_create if params.get(p) is None]
            if missing:
                self.fail_json(
                    msg=f"When creating a new DHCP scope, the following parameters are required: {', '.join(missing)}"
                )

        # Build desired state dict
        desired = {}
        for key in [
            'newName', 'startingAddress', 'endingAddress', 'subnetMask', 'leaseTimeDays',
            'leaseTimeHours', 'leaseTimeMinutes', 'offerDelayTime', 'pingCheckEnabled',
            'pingCheckTimeout', 'pingCheckRetries', 'domainName', 'domainSearchList',
            'dnsUpdates', 'dnsTtl', 'serverAddress', 'serverHostName', 'bootFileName',
            'routerAddress', 'useThisDnsServer', 'dnsServers', 'winsServers', 'ntpServers',
            'ntpServerDomainNames', 'staticRoutes', 'vendorInfo', 'capwapAcIpAddresses',
            'tftpServerAddresses', 'genericOptions', 'exclusions', 'reservedLeases',
            'allowOnlyReservedLeases', 'blockLocallyAdministeredMacAddresses', 'ignoreClientIdentifierOption'
        ]:
            value = params.get(key)
            if value is not None:
                desired[key] = value

        # Compare current vs desired for idempotency
        diff = {}
        if scope_exists:
            for k, v in desired.items():
                # Skip newName in comparison (it's for renaming)
                if k == 'newName':
                    if v != scope_name:  # Only add to diff if actually renaming
                        diff[k] = {'current': scope_name, 'desired': v}
                    continue

                current_val = current.get(k)
                normalized_current = self._normalize_value(k, current_val)
                normalized_desired = self._normalize_value(k, v)

                if normalized_current != normalized_desired:
                    diff[k] = {'current': normalized_current, 'desired': normalized_desired}
        else:
            # Creating new scope - all provided values are changes
            diff = {k: {'current': None, 'desired': v} for k, v in desired.items()}

        # If no changes needed, exit early
        if not diff:
            self.exit_json(changed=False, msg="DHCP scope configuration already matches desired state.")

        # Handle check mode
        if self.check_mode:
            msg = "(check mode) DHCP scope would be created." if not scope_exists else "(check mode) DHCP scope configuration would be updated."
            self.exit_json(
                changed=True,
                msg=msg,
                diff=diff,
                api_response={"status": "ok", "check_mode": True, "scope": scope_name}
            )

        # Build API parameters
        set_query = {'name': scope_name}

        # Helper function to convert list of dicts to pipe-separated format
        def list_of_dicts_to_str(items, keys):
            """Convert list of dicts to pipe-separated string"""
            parts = []
            for item in items:
                values = [str(item.get(k, '')) for k in keys]
                parts.append("|".join(values))
            return "|".join(parts)

        # Convert desired values to API format
        list_like_fields = [
            'domainSearchList', 'dnsServers', 'winsServers', 'ntpServers',
            'ntpServerDomainNames', 'capwapAcIpAddresses', 'tftpServerAddresses'
        ]

        for k, v in desired.items():
            if k in list_like_fields and isinstance(v, list):
                set_query[k] = ",".join(str(x) for x in v)
            elif k == 'staticRoutes' and isinstance(v, list):
                set_query[k] = list_of_dicts_to_str(v, ['destination', 'subnetMask', 'router'])
            elif k == 'vendorInfo' and isinstance(v, list):
                set_query[k] = list_of_dicts_to_str(v, ['identifier', 'information'])
            elif k == 'genericOptions' and isinstance(v, list):
                set_query[k] = list_of_dicts_to_str(v, ['code', 'value'])
            elif k == 'exclusions' and isinstance(v, list):
                set_query[k] = list_of_dicts_to_str(v, ['startingAddress', 'endingAddress'])
            elif k == 'reservedLeases' and isinstance(v, list):
                set_query[k] = list_of_dicts_to_str(v, ['hostName', 'hardwareAddress', 'address', 'comments'])
            elif isinstance(v, bool):
                set_query[k] = str(v).lower()
            else:
                set_query[k] = v

        # Make the API call
        data = self.request('/api/dhcp/scopes/set', params=set_query, method='POST')
        self.validate_api_response(data)

        # Return success
        msg = "DHCP scope created successfully." if not scope_exists else "DHCP scope configuration updated successfully."
        self.exit_json(
            changed=True,
            msg=msg,
            diff=diff,
            api_response=data
        )


if __name__ == '__main__':
    module = SetDhcpScopeModule()
    module.run()
