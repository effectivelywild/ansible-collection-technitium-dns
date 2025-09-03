#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to get DNS records from Technitium DNS using TechnitiumModule base class

from ansible_collections.technitium.dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_get_records
short_description: Get DNS records from a Technitium DNS zone
version_added: "0.0.1"
description:
    - Get DNS resource records from a Technitium DNS authoritative zone using its API.
options:
    api_url:
        description:
            - Base URL for the Technitium DNS API (e.g., http://localhost)
            - Do not include the port; use the 'port' parameter instead.
        required: true
        type: str
    port:
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
    name:
        description:
            - The record or zone name (e.g., test.example.com/example.com).
            - The use of 'domain:' is also supported to align with API.
        required: true
        type: str
    zone:
        description:
            - The authoritative zone name (optional, defaults to closest match).
        required: false
        type: str
    listZone:
        description:
            - If true, list all records in the zone. If false, only records for the given domain.
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Get specific record by name
  technitium_dns_get_records:
    api_url: "http://localhost"
    api_token: "myapitoken"
    port: 5380
    name: "record.example.com"

- name: Get all records for a zone
  technitium_dns_get_records:
    api_url: "http://localhost"
    api_token: "myapitoken"
    port: 5380
    name: "example.com"
    listZone: true
    validate_certs: false

- name: Get SOA and NS records for zone
  technitium_dns_get_records:
    api_url: "http://localhost"
    api_token: "myapitoken"
    port: 5380
    name: "example.com"
'''

class GetRecordsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True, aliases=['domain']),
        zone=dict(type='str', required=False),
        listZone=dict(type='bool', required=False, default=False)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        params = self.params
        
        # Build API query parameters from module arguments
        query = {}
        for key in self.argument_spec:
            val = params.get(key)
            if val is not None:
                # Convert boolean values to lowercase strings for API compatibility
                if isinstance(val, bool):
                    val = str(val).lower()
                query[key] = val
        
        # Add authentication token and set domain parameter for API
        query['token'] = self.api_token
        query['domain'] = self.name
        
        # Fetch DNS records from the API
        data = self.request('/api/zones/records/get', params=query)
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        
        records = data.get('response', {}).get('records', [])
        
        # Validate results based on operation mode
        # For specific record queries (not zone listing), ensure records were found
        if self.params.get('name') and not self.params.get('listZone', False):
            if not records:
                self.fail_json(msg=f"No records found for name '{self.params['name']}' in zone '{self.params.get('zone', '')}'", api_response=data)
        
        self.exit_json(changed=False, records=records, api_response=data)

def main():
    module = GetRecordsModule()
    module()

if __name__ == '__main__':
    main()
