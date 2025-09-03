#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to get zone data from Technitium DNS API using TechnitiumModule base class

from ansible_collections.technitium.dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_get_zone_info
short_description: Get DNS zone(s) from Technitium DNS server
version_added: "0.0.1"
description:
    - Retrieve all DNS zones, or filter by zone type and/or name, from a Technitium DNS server using its API.
    - Returns a subset of zone information compared to `technitium_dns_get_zone_options`
author:
    - Frank Muise (@effectivelywild)
options:
    api_url:
        description:
            - Base URL for the Technitium DNS API (e.g., http://localhost)
            - Do not include the port; use the 'port' parameter instead.
        required: true
        type: str
    api_port:
        description:
            - Port for the Technitium DNS API. Defaults to 5380.
        required: false
        type: int
        default: 5380
    api_token:
        description:
            - API token for authenticating with the Technitium DNS API.
        required: true
        type: str
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests.
            - Set to false to disable SSL certificate validation (not recommended for production).
        required: false
        type: bool
        default: true
    zone:
        description:
            - (Optional) The DNS zone to retrieve information for. If not specified, all zones are returned.
        required: false
        type: str
    zone_type:
        description:
            - (Optional) Filter zones by type (e.g., Primary, Forwarder, Secondary, Catalog, etc). If not specified, all zones are returned.
        required: false
        type: str
        choices: [Primary, Forwarder, SecondaryForwarder, Stub, Secondary, Catalog, SecondaryCatalog, SecondaryROOT]
notes:
    - Example of data returned from a unsigned Primary zone:

        `"primary_zone_result": {
            "changed": false,
            "failed": false,
            "zone": {
                "catalog": null,
                "disabled": false,
                "dnssecStatus": "Unsigned",
                "internal": false,
                "lastModified": "2025-08-23T16:44:21.1647605Z",
                "name": "primary.example.com",
                "notifyFailed": false,
                "notifyFailedFor": [],
                "soaSerial": 1,
                "type": "Primary"
            }
        }`

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

- name: Get a specific Forwarder zone from Technitium DNS
  technitium_dns_get_zone_info:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    zone_type: Forwarder
  register: result

- debug:
    var: result.zone
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