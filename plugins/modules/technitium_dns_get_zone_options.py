#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to get zone options from Technitium DNS API using TechnitiumModule base class

from ansible_collections.technitium.dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_get_zone_options
short_description: Get DNS zone options from Technitium DNS server
version_added: "0.0.1"
description:
    - Retrieve zone-specific options from a Technitium DNS server using its API.
options:
    api_url:
        description:
            - Base URL for the Technitium DNS API (e.g., http://localhost)
            - Do not include the port; use the 'api_port' parameter instead.
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
            - The domain name of the zone to get options for.
        required: true
        type: str
    includeAvailableCatalogZoneNames:
        description:
            - Include list of available Catalog zone names on the DNS server.
        required: false
        type: bool
        default: false
    includeAvailableTsigKeyNames:
        description:
            - Include list of available TSIG key names on the DNS server.
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Get options for example.com zone
  technitium_dns_get_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    includeAvailableTsigKeyNames: true
  register: result

- debug:
    var: result.options
'''

class GetZoneOptionsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        includeAvailableCatalogZoneNames=dict(type='bool', required=False, default=False),
        includeAvailableTsigKeyNames=dict(type='bool', required=False, default=False)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        params = self.params
        zone = params['zone']
        include_catalog = params['includeAvailableCatalogZoneNames']
        include_tsig = params['includeAvailableTsigKeyNames']

        # First validate the zone exists, then get options with additional parameters if needed
        if include_catalog or include_tsig:
            query = {'zone': zone}
            if include_catalog:
                query['includeAvailableCatalogZoneNames'] = 'true'
            if include_tsig:
                query['includeAvailableTsigKeyNames'] = 'true'
            data = self.request('/api/zones/options/get', params=query)
            # Validate zone exists using the response
            error_msg = data.get('errorMessage')
            if error_msg and 'No such zone was found' in error_msg:
                self.fail_json(msg=f"Zone '{zone}' does not exist: {error_msg}")
            if data.get('status') != 'ok':
                error_msg = data.get('errorMessage') or data.get('message') or "Unknown error"
                self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        else:
            # Use base class validation for simple case
            data = self.validate_zone_exists(zone)
            if data.get('status') != 'ok':
                error_msg = data.get('errorMessage') or 'Unknown error'
                self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        options = data.get('response', {})
        self.exit_json(changed=False, options=options)

def main():
    module = GetZoneOptionsModule()
    module()

if __name__ == '__main__':
    main()
