#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to get zone data from Technitium DNS API using TechnitiumModule base class

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_get_zone_info
short_description: Get DNS zone(s) from Technitium DNS server
version_added: "0.0.1"
description:
    - Retrieve all DNS zones, or filter by zone type and/or name, from a Technitium DNS server.
    - Returns a subset of zone information compared to `technitium_dns_get_zone_options`
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_zone
    description: Creates DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_zone
    description: Deletes DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_options
    description: Get all configured zone options
  - module: effectivelywild.technitium_dns.technitium_dns_set_zone_options
    description: Set zone options
  - module: effectivelywild.technitium_dns.technitium_dns_enable_zone
    description: Enable a zone
  - module: effectivelywild.technitium_dns.technitium_dns_disable_zone
    description: Disable a zone
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
    zone:
        description:
            - The DNS zone to retrieve information for. If not specified, all zones are returned.
        required: false
        type: str
    zone_type:
        description:
            - Filter zones by type.
        required: false
        type: str
        choices: [Primary, Forwarder, SecondaryForwarder, Stub, Secondary, Catalog, SecondaryCatalog, SecondaryROOT]
'''

EXAMPLES = r'''
- name: Get all zones from Technitium DNS
  technitium_dns_get_zone_info:
    api_url: "http://localhost"
    api_token: "myapitoken"
    port: 5203
  register: result

- debug:
    var: result.zones

- name: Get all Primary zones from Technitium DNS
  technitium_dns_get_zone_info:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone_type: Primary
  register: result

- debug:
    var: result.zones

- name: Get a specific zone from Technitium DNS
  technitium_dns_get_zone_info:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
  register: result

- debug:
    var: result.zone
'''

RETURN = r'''
zone:
    description: Zone information when requesting a specific zone
    type: dict
    returned: when zone parameter is provided
    contains:
        catalog:
            description: Catalog zone association (null if not part of catalog)
            type: str
            returned: always
            sample: null
        disabled:
            description: Whether the zone is disabled
            type: bool
            returned: always
            sample: false
        dnssecStatus:
            description: DNSSEC status of the zone
            type: str
            returned: always
            sample: "Unsigned"
        internal:
            description: Whether the zone is internal
            type: bool
            returned: always
            sample: false
        lastModified:
            description: When the zone was last modified (ISO 8601 format)
            type: str
            returned: always
            sample: "2025-09-04T17:26:31.5111735Z"
        name:
            description: Zone name/domain
            type: str
            returned: always
            sample: "demo.test.local"
        notifyFailed:
            description: Whether zone notification failed
            type: bool
            returned: always
            sample: false
        notifyFailedFor:
            description: List of hosts for which notification failed
            type: list
            returned: always
            sample: []
        soaSerial:
            description: SOA serial number of the zone
            type: int
            returned: always
            sample: 2025090400
        type:
            description: Zone type
            type: str
            returned: always
            sample: "Primary"

zones:
    description: List of zones when requesting all zones or filtering by type, returns same values as zone, see above for details.
    type: list
    returned: when zone parameter is not provided
changed:
    description: Whether the module made changes (always false for get operations)
    type: bool
    returned: always
    sample: false
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''


class GetZoneInfoModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=False),
        zone_type=dict(type='str', required=False, choices=['Primary', 'Forwarder', 'SecondaryForwarder', 'Stub', 'Secondary', 'Catalog', 'SecondaryCatalog'])
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        zone_name = params.get('zone')
        zone_type = params.get('zone_type')

        # Fetch all zones from the API
        data = self.request('/api/zones/list')
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        
        zones = data.get('response', {}).get('zones', [])
        
        # Apply zone type filter if specified
        if zone_type:
            zones = [z for z in zones if z.get('type') == zone_type]
        
        # Handle specific zone request vs. all zones request
        if zone_name:
            # Find the specific zone in the filtered list
            zone = next((z for z in zones if z.get('name') == zone_name), None)
            if zone is None:
                self.fail_json(msg=f"Zone '{zone_name}' not found", api_response={'status': 'error', 'msg': f"Zone '{zone_name}' not found"})
            self.exit_json(changed=False, zone=zone)
        else:
            # Return all zones (optionally filtered by type)
            self.exit_json(changed=False, zones=zones)

def main():
    module = GetZoneInfoModule()
    module()

if __name__ == '__main__':
    main()