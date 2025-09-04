#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to get DNSSEC properties from Technitium DNS API using TechnitiumModule base class

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_get_dnssec_properties
short_description: Get DNSSEC properties for a primary zone from Technitium DNS server
version_added: "0.0.1"
description:
    - Retrieve DNSSEC properties for a primary zone from a Technitium DNS server using its API.
    - This module requires Zones: Modify or Zone: View permissions.
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
            - The name of the primary zone to get DNSSEC properties for.
        required: true
        type: str
notes:
    - This module only works with primary zones.
    - Requires Zones: Modify or Zone: View permissions.
'''


EXAMPLES = r'''
- name: Get DNSSEC properties for example.com
  technitium_dns_get_dnssec_properties:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
  register: result

- debug:
    var: result.dnssec_properties
'''


class GetDnssecPropertiesModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        zone = self.params['zone']
        
        # Validate that the zone exists before attempting to get DNSSEC properties
        # This will fail with a clear error message if the zone doesn't exist
        self.validate_zone_exists(zone)
        
        # Build API parameters for DNSSEC properties request
        params = {'zone': zone}
        
        # Fetch DNSSEC properties from the Technitium API
        # This endpoint returns DNSSEC keys, signing information, and configuration
        data = self.request('/api/zones/dnssec/properties/get', params=params)
        
        # Check API response status and handle errors
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        
        # Extract DNSSEC properties from API response
        dnssec_properties = data.get('response', {})
        
        # Return the DNSSEC properties (read-only operation, never changed=True)
        self.exit_json(changed=False, dnssec_properties=dnssec_properties)


if __name__ == '__main__':
    module = GetDnssecPropertiesModule()
    module.run()
