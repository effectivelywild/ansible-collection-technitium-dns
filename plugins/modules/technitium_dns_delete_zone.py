#!/usr/bin/python
# -*- coding: utf-8 -*-
# New Technitium DNS delete zone module using TechnitiumModule base class

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_delete_zone
short_description: Delete a DNS zone
version_added: "0.0.1"
author: Frank Muise (@effectivelywild)
description:
    - Delete a DNS zone in Technitium DNS server using its API.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_zone
    description: Deletes DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_info
    description: Get basic zone information
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_options
    description: Get all configured zone options
  - module: effectivelywild.technitium_dns.technitium_dns_set_zone_options
    description: Set zone options
  - module: effectivelywild.technitium_dns.technitium_dns_enable_zone
    description: Enables a zone
  - module: effectivelywild.technitium_dns.technitium_dns_disable_zone
    description: Diables a zone

description:
    - Delete an authoritative DNS zone in Technitium DNS server using its API.
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
            - The domain name of the zone to be deleted.
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Delete a zone
  technitium_dns_delete_zone:
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
            contains:
                domain:
                    description: The domain name of the deleted zone
                    type: str
                    returned: always
                    sample: "demo.test.local"
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to delete the zone
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to complete the zone deletion
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the zone deletion result
    type: str
    returned: always
    sample: "Zone 'demo.test.local' deleted."
'''

class DeleteZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        zone = self.params['zone']

        # Check if the zone exists to ensure idempotent behavior
        # Idempotent delete: if zone doesn't exist, report no changes made
        zone_check_query = {'zone': zone}
        zone_check_data = self.request('/api/zones/options/get', params=zone_check_query)
        zone_exists = True
        
        # Parse the API response to determine if zone exists
        if zone_check_data.get('status') != 'ok':
            error_msg = zone_check_data.get('errorMessage', '')
            if 'No such zone was found' in error_msg:
                # Zone doesn't exist - this is expected for idempotent delete
                zone_exists = False
            else:
                # Unexpected API error occurred during zone existence check
                self.fail_json(msg=f"Technitium API error checking zone: {error_msg}", api_response=zone_check_data)

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            if zone_exists:
                self.exit_json(changed=True, msg="Zone would be deleted (check mode)", api_response={})
            else:
                self.exit_json(changed=False, msg=f"Zone '{zone}' does not exist (check mode)", api_response={})

        # Implement idempotent delete behavior
        # If zone doesn't exist, return success without changes (already deleted)
        if not zone_exists:
            self.exit_json(changed=False, msg=f"Zone '{zone}' does not exist.", api_response={'status': 'ok', 'msg': f"Zone '{zone}' does not exist."})

        # Delete the zone via the Technitium API
        data = self.request('/api/zones/delete', params={'zone': zone})
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
            
        # Return success - zone was deleted
        self.exit_json(changed=True, msg=f"Zone '{zone}' deleted.", api_response=data)

if __name__ == '__main__':
    module = DeleteZoneModule()
    module.run()
