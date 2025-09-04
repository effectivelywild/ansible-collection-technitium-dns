#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to get DNS records from Technitium DNS using TechnitiumModule base class

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_get_records
short_description: Get DNS record(s)
version_added: "0.0.1"
author: Frank Muise (@effectivelywild)
requirements:
  - requests
description:
    - Get DNS resource records from a Technitium DNS authoritative zone using its API.
seealso:
    - module: effectivelywild.technitium_dns.technitium_dns_add_record
      description: Used to add DNS records
    - module: effectivelywild.technitium_dns.technitium_dns_delete_record
      description: Used to delete DNS record details
options:
    api_url:
        description:
            - Base URL for the Technitium DNS API
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
        required: false
        type: bool
        default: true
    name:
        description:
            - The record or zone name (e.g., test.example.com/example.com).
            - The use of 'domain:' is also supported to align with API.
        required: true
        type: str
        aliases: [domain]
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

RETURN = r'''
records:
    description: 
        - List of DNS records (convenience extraction from api_response.response.records)
        - See api_response.response.records for detailed field documentation
    type: list
    returned: always
    sample: [
        {
            "disabled": false,
            "dnssecStatus": "Unknown",
            "name": "example.com",
            "type": "A",
            "ttl": 3600,
            "rData": {
                "ipAddress": "192.0.2.1"
            }
        }
    ]

api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The core data payload from the API
            type: dict
            contains:
                records:
                    description: Array of DNS record objects with complete details
                    type: list
                    contains:
                        disabled:
                            description: Whether the record is disabled
                            type: bool
                            returned: always
                        dnssecStatus:
                            description: DNSSEC status of the record
                            type: str
                            returned: always
                        expiryTtl:
                            description: Record expiration TTL in seconds
                            type: int
                            returned: always
                        expiryTtlString:
                            description: Record expiration TTL as human-readable string
                            type: str
                            returned: always
                        lastModified:
                            description: When the record was last modified
                            type: str
                            returned: always
                        lastUsedOn:
                            description: When the record was last used
                            type: str
                            returned: always
                        name:
                            description: Full domain name of the record
                            type: str
                            returned: always
                        rData:
                            description: Record-specific data (varies by record type)
                            type: dict
                            returned: always
                            sample: {"ipAddress": "192.0.2.1"}
                        ttl:
                            description: Record TTL in seconds
                            type: int
                            returned: always
                        ttlString:
                            description: Record TTL as human-readable string
                            type: str
                            returned: always
                        type:
                            description: DNS record type
                            type: str
                            returned: always
                zone:
                    description: Information about the zone containing the records
                    type: dict
                    returned: always
                    contains:
                        catalog:
                            description: Zone catalog information
                            type: str
                            returned: always
                        disabled:
                            description: Whether the zone is disabled
                            type: bool
                            returned: always
                        dnssecStatus:
                            description: DNSSEC status of the zone
                            type: str
                            returned: always
                        internal:
                            description: Whether the zone is internal
                            type: bool
                            returned: always
                        lastModified:
                            description: When the zone was last modified
                            type: str
                            returned: always
                        name:
                            description: Zone name
                            type: str
                            returned: always
                        notifyFailed:
                            description: Whether zone notification failed
                            type: bool
                            returned: always
                        notifyFailedFor:
                            description: List of hosts for which notification failed
                            type: list
                            returned: always
                        soaSerial:
                            description: SOA serial number of the zone
                            type: int
                            returned: always
                        type:
                            description: Zone type (e.g., Primary, Secondary)
                            type: str
                            returned: always
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"

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


if __name__ == '__main__':
    module = GetRecordsModule()
    module.run()

