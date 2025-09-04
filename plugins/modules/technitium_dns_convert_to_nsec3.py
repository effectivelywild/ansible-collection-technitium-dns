#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_convert_to_nsec3
short_description: Convert a primary DNS zone from NSEC to NSEC3
version_added: "0.0.1"
author: Frank Muise (@effectivelywild)
requirements:
  - requests
description:
  - Converts a primary DNS zone from NSEC to NSEC3 for proof of non-existence using the Technitium DNS API.
  - Only works on zones that are already signed with DNSSEC using NSEC.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_nsec
    description: Convert signed zone from NSEC to NSEC3
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
options:
  api_url:
    description:
      - Base URL for the Technitium DNS API
    type: str
  api_token:
    description:
      - API token for authentication
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
      - The name of the primary zone to convert to NSEC3
    required: true
    type: str
requirements:
  - requests
'''

EXAMPLES = r'''
- name: Convert a primary zone from NSEC to NSEC3
  technitium_dns_convert_to_nsec3:
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
            description: The core data payload from the API (typically empty for conversion operations)
            type: dict
            returned: always
            sample: {}
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"

changed:
    description: Whether the module made changes to convert the zone from NSEC to NSEC3
    type: bool
    returned: always
    sample: true

failed:
    description: Whether the module failed to complete the conversion
    type: bool
    returned: always
    sample: false

msg:
    description: Human-readable message describing the conversion result
    type: str
    returned: always
    sample: "Zone 'dnssec-demo.test.local' converted from NSEC to NSEC3."
'''

class ConvertToNsec3Module(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        zone = self.params['zone']
        
        # Fetch current zone DNSSEC status (this also validates zone exists)
        dnssec_status, zone_info = self.get_dnssec_status(zone)

        # Check if zone is signed with DNSSEC
        if dnssec_status == 'unsigned':
            self.fail_json(msg=f"Zone '{zone}' is not signed with DNSSEC. Cannot convert unsigned zone to NSEC3.", api_response={'status': 'error', 'msg': 'Zone must be signed with DNSSEC'})

        # If zone is already using NSEC3, no changes needed
        if dnssec_status == 'signedwithnsec3':
            self.exit_json(changed=False, msg=f"Zone '{zone}' is already using NSEC3.", api_response={'status': 'ok', 'msg': f"Zone '{zone}' is already using NSEC3."})

        # If zone is not using NSEC, it cannot be converted to NSEC3
        if dnssec_status != 'signedwithnsec':
            self.fail_json(msg=f"Zone '{zone}' is signed but not with NSEC (status: {zone_info.get('dnssecStatus')}). Can only convert NSEC zones to NSEC3.", api_response={'status': 'error', 'msg': 'Zone must be signed with NSEC to convert to NSEC3'})

        if self.check_mode:
            self.exit_json(changed=True, msg="Zone would be converted from NSEC to NSEC3 (check mode)", api_response={})

        # Convert the zone from NSEC to NSEC3
        query = {'zone': zone}
        data = self.request('/api/zones/dnssec/properties/convertToNSEC3', params=query, method='POST')
        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        
        self.exit_json(changed=True, msg=f"Zone '{zone}' converted from NSEC to NSEC3.", api_response=data)

if __name__ == '__main__':
    module = ConvertToNsec3Module()
    module.run()
