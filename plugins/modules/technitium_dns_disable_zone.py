#!/usr/bin/python
# -*- coding: utf-8 -*-
# New Technitium DNS disable zone module using TechnitiumModule base class

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_disable_zone
short_description: Disable a DNS zone in Technitium DNS server
version_added: "0.0.1"
author: Frank Muise (@effectivelywild)
description:
    - Disable a DNS zone, this will prevent the DNS server from responding to queries for this zone.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_zone
    description: Creates DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_zone
    description: Deletes DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_info
    description: Get basic zone information
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_options
    description: Get all configured zone options
  - module: effectivelywild.technitium_dns.technitium_dns_set_zone_options
    description: Set zone options
  - module: effectivelywild.technitium_dns.technitium_dns_disable_zone
    description: Diables a zone
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
            - Set to false to disable SSL certificate validation (not recommended for production).
        required: false
        type: bool
        default: true
    zone:
        description:
            - The domain name of the zone to be disabled.
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Disable a zone
  technitium_dns_disable_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
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
            sample: "{}"
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to disable the zone
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to disable the zone
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the result of disabling the zone
    type: str
    returned: always
    sample: "Zone 'demo.test.local' disabled."
'''

class DisableZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        zone = self.params['zone']

        # Check if the zone exists and get its current status
        zone_check_query = {'zone': zone}
        zone_check_data = self.request('/api/zones/options/get', params=zone_check_query)
        zone_exists = True
        is_disabled = False
        
        # Parse the API response to determine if zone exists and its status
        if zone_check_data.get('status') != 'ok':
            error_msg = zone_check_data.get('errorMessage', '')
            if 'No such zone was found' in error_msg:
                # Zone doesn't exist - cannot disable a non-existent zone
                self.fail_json(msg=f"Zone '{zone}' does not exist and cannot be disabled.", api_response=zone_check_data)
            else:
                # Unexpected API error occurred during zone existence check
                self.fail_json(msg=f"Technitium API error checking zone: {error_msg}", api_response=zone_check_data)
        else:
            # Zone exists, check if it's already disabled
            zone_info = zone_check_data.get('response', {})
            is_disabled = zone_info.get('disabled', False)

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            if not is_disabled:
                self.exit_json(changed=True, msg="Zone would be disabled (check mode)", api_response={})
            else:
                self.exit_json(changed=False, msg=f"Zone '{zone}' is already disabled (check mode)", api_response={})

        # Implement idempotent disable behavior
        # If zone is already disabled, return success without changes
        if is_disabled:
            self.exit_json(changed=False, msg=f"Zone '{zone}' is already disabled.", api_response={'status': 'ok', 'msg': f"Zone '{zone}' is already disabled."})

        # Disable the zone via the Technitium API
        data = self.request('/api/zones/disable', params={'zone': zone})
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
            
        # Return success - zone was disabled
        self.exit_json(changed=True, msg=f"Zone '{zone}' disabled.", api_response=data)

if __name__ == '__main__':
    module = DisableZoneModule()
    module.run()
