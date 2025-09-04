#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to create zones in Technitium DNS using TechnitiumModule base class

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_create_zone
short_description: Create a DNS zone in Technitium DNS server
version_added: "0.0.1"
author: Frank Muise (@effectivelywild)
description:
    - Create a DNS zone in Technitium DNS server using its API.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_delete_zone
    description: Deletes DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_info
    description: Get basic zone information
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_options
    description: Get all configured zone options
  - module: effectivelywild.technitium_dns.technitium_dns_set_zone_options
    description: Set all zone options
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
    catalog:
        description:
            - The name of the catalog zone to become its member zone.
        required: false
        type: str
    dnssecValidation:
        description:
            - Enable DNSSEC validation (Forwarder only)
        required: false
        type: bool
    forwarder:
        description:
            - Address of DNS server to use as forwarder (Forwarder only)
        required: false
        type: str
    initializeForwarder:
        description:
            - Initialize Conditional Forwarder zone with FWD record (Forwarder only)
        required: false
        type: bool
        default: true
    primaryNameServerAddresses:
        description:
            - Comma separated IPs or names of primary name server (Secondary, SecondaryForwarder, SecondaryCatalog, Stub)
        required: false
        type: str
    protocol:
        description:
            - DNS transport protocol for Conditional Forwarder zone.
        required: false
        type: str
        choices: [Udp, Tcp, Tls, Https, Quic]
    proxyAddress:
        description:
            - Proxy server address (Forwarder only)
        required: false
        type: str
    proxyPassword:
        description:
            - Proxy server password (Forwarder only)
        required: false
        type: str
    proxyPort:
        description:
            - Proxy server port (Forwarder only)
        required: false
        type: int
    proxyType:
        description:
            - Proxy type for conditional forwarding (Forwarder only)
        required: false
        type: str
        choices: [NoProxy, DefaultProxy, Http, Socks5]
    proxyUsername:
        description:
            - Proxy server username (Forwarder only)
        required: false
        type: str
    tsigKeyName:
        description:
            - TSIG key name (Secondary, SecondaryForwarder, SecondaryCatalog)
        required: false
        type: str
    type:
        description:
            - The type of zone to be created.
        required: true
        type: str
        choices: [Primary, Secondary, Stub, Forwarder, SecondaryForwarder, Catalog, SecondaryCatalog]
    useSoaSerialDateScheme:
        description:
            - Enable using date scheme for SOA serial (Primary, Forwarder, Catalog zones)
        required: false
        type: bool
        default: false
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests
        required: false
        type: bool
        default: true
    validateZone:
        description:
            - Enable ZONEMD validation (Secondary only)
        required: false
        type: bool
    zone:
        description:
            - The domain name for creating the new zone
        required: true
        type: str
    zoneTransferProtocol:
        description:
            - Zone transfer protocol (Secondary, SecondaryForwarder, SecondaryCatalog)
        required: false
        type: str
        choices: [Tcp, Tls, Quic]
'''

EXAMPLES = r'''
- name: Create a Primary zone
  technitium_dns_create_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    type: "Primary"

- name: Create a Forwarder zone with forwarder address
  technitium_dns_create_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "forward.example.com"
    type: "Forwarder"
    forwarder: "8.8.8.8"
    initializeForwarder: true
    protocol: "Udp"
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
            contains:
                domain:
                    description: The domain name of the created zone
                    type: str
                    returned: always
                    sample: "demo.test.local"
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to create a new zone
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to complete the zone creation
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the zone creation result
    type: str
    returned: always
    sample: "Zone 'demo.test.local' created."
'''

class CreateZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        type=dict(type='str', required=True, choices=["Primary", "Secondary", "Stub", "Forwarder", "SecondaryForwarder", "Catalog", "SecondaryCatalog"]),
        catalog=dict(type='str', required=False),
        useSoaSerialDateScheme=dict(type='bool', required=False),
        primaryNameServerAddresses=dict(type='list', elements='str', required=False),
        zoneTransferProtocol=dict(type='str', required=False, choices=["Tcp", "Tls", "Quic"]),
        tsigKeyName=dict(type='str', required=False),
        validateZone=dict(type='bool', required=False),
        initializeForwarder=dict(type='bool', required=False),
        protocol=dict(type='str', required=False, choices=["Udp", "Tcp", "Tls", "Https", "Quic"]),
        forwarder=dict(type='str', required=False),
        dnssecValidation=dict(type='bool', required=False),
        proxyType=dict(type='str', required=False, choices=["NoProxy", "DefaultProxy", "Http", "Socks5"]),
        proxyAddress=dict(type='str', required=False),
        proxyPort=dict(type='int', required=False),
        proxyUsername=dict(type='str', required=False),
        proxyPassword=dict(type='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        zone = params['zone']
        zone_type = params['type']

        # Define a set of parameters that are always allowed, regardless of zone type.
        # These are the common parameters for the Technitium API module.
        common_params = {
            'api_url', 'api_port', 'api_token', 'validate_certs', 'zone', 'type'
        }

        # Validate parameters based on zone type
        # Each zone type has specific allowed and required parameters
        allowed_params = {
            'Primary': set(['catalog','useSoaSerialDateScheme']),
            'Forwarder': set(['catalog','useSoaSerialDateScheme','initializeForwarder','protocol','forwarder','dnssecValidation','proxyType','proxyAddress','proxyPort','proxyUsername','proxyPassword']),
            'Catalog': set(['catalog','useSoaSerialDateScheme']),
            'Secondary': set(['primaryNameServerAddresses','zoneTransferProtocol','tsigKeyName','validateZone']),
            'SecondaryForwarder': set(['primaryNameServerAddresses','zoneTransferProtocol','tsigKeyName']),
            'SecondaryCatalog': set(['primaryNameServerAddresses','zoneTransferProtocol','tsigKeyName']),
            'Stub': set(['primaryNameServerAddresses']),
        }
        
        # Check for invalid parameters for the specified zone type
        for param, value in params.items():
            if param in common_params:
                continue
            # We'll only check if the parameter was explicitly provided by the user.
            is_user_provided = True
            if value is None:
                is_user_provided = False
            elif isinstance(value, list) and not value:
                # This handles the specific case of an empty list
                is_user_provided = False
            if is_user_provided and zone_type in allowed_params and param not in allowed_params[zone_type]:
                self.fail_json(msg=f"Parameter '{param}' is not supported for zone type '{zone_type}'.")

        # Check for missing required parameters for the specified zone type
        required_params = {
            'Forwarder': ['forwarder'],
            'SecondaryForwarder': ['primaryNameServerAddresses'],
            'SecondaryCatalog': ['primaryNameServerAddresses'],
            'Secondary': ['primaryNameServerAddresses'],
            'Stub': ['primaryNameServerAddresses'],
        }
        if zone_type in required_params:
            for req in required_params[zone_type]:
                if not params.get(req):
                    self.fail_json(msg=f"Parameter '{req}' is required for zone type '{zone_type}'.")

        # Check for existing zone to ensure idempotent behavior
        # If zone already exists with same type, return success without changes
        info_data = self.request('/api/zones/list')
        zones = info_data.get('response', {}).get('zones', [])
        existing_zone = next((z for z in zones if z.get('name') == zone), None)
        if existing_zone:
            if existing_zone.get('type') == zone_type:
                self.exit_json(changed=False, msg=f"Zone '{zone}' of type '{zone_type}' already exists.", zone=existing_zone, api_response=info_data)

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Zone '{zone}' of type '{zone_type}' would be created (check mode).",
                api_response={"status": "ok", "check_mode": True, "zone": zone, "type": zone_type}
            )

        # Build API query parameters from module arguments
        query = {
            'zone': zone,
            'type': zone_type
        }
        
        # Add optional parameters to the query, handling data type conversions
        for key in [
            'catalog', 'useSoaSerialDateScheme', 'primaryNameServerAddresses', 'zoneTransferProtocol',
            'tsigKeyName', 'validateZone', 'initializeForwarder', 'protocol', 'forwarder', 'dnssecValidation',
            'proxyType', 'proxyAddress', 'proxyPort', 'proxyUsername', 'proxyPassword']:
            val = params.get(key)
            if val is not None:
                # Convert boolean values to lowercase strings for API compatibility
                if isinstance(val, bool):
                    val = str(val).lower()
                # Convert list of nameservers to comma-separated string
                if key == 'primaryNameServerAddresses' and isinstance(val, list):
                    val = ",".join(str(x) for x in val)
                query[key] = val

        # Create the zone via the Technitium API
        data = self.request('/api/zones/create', params=query)
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
            
        # Return success - zone was created
        self.exit_json(changed=True, msg=f"Zone '{zone}' created.", api_response=data)

if __name__ == '__main__':
    module = CreateZoneModule()
    module.run()
