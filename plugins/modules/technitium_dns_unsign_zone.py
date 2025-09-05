#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_unsign_zone
short_description: Unsign a DNS zone
version_added: "0.0.1"
author: Frank Muise (@effectivelywild)
requirements:
  - requests
description:
  - Unsigns a DNS zone using the Technitium DNS API.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_nsec
    description: Convert signed zone from NSEC to NSEC3
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_nsec3
    description: Convert signed zone from NSEC3 to NSEC
  - module: effectivelywild.technitium_dns.technitium_dns_get_dnssec_properties
    description: Get dnssec properties for a zone
options:
  api_port:
      description:
          - Port for the Technitium DNS API. Defaults to 5380
      required: false
      type: int
      default: 5380
  api_token:
    description:
      - API token for authentication
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
      - The name of the primary zone to unsign
    required: true
    type: str
'''

EXAMPLES = r'''
- name: Unsign a primary zone
  technitium_dns_unsign_zone:
    api_url: "http://localhost:5380"
    api_token: "{{ technitium_api_token }}"
    zone: "example.com"
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The API response payload (empty dict for successful unsign operations)
            type: dict
            returned: always
            sample: "{}"
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
msg:
    description: Human readable message describing the result
    type: str
    returned: always
    sample: "Zone 'demo.test.local' unsigned."
'''

class UnsignZoneModule(TechnitiumModule):
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

        # If zone is already unsigned, no changes needed
        if dnssec_status == 'unsigned':
            self.exit_json(changed=False, msg=f"Zone '{zone}' is already unsigned.", api_response={'status': 'ok', 'msg': f"Zone '{zone}' is already unsigned."})

        if self.check_mode:
            self.exit_json(changed=True, msg="Zone would be unsigned (check mode)", api_response={})

        # Unsign the zone
        query = {'zone': zone}
        data = self.request('/api/zones/dnssec/unsign', params=query, method='POST')
        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        
        self.exit_json(changed=True, msg=f"Zone '{zone}' unsigned.", api_response=data)

if __name__ == '__main__':
    module = UnsignZoneModule()
    module.run()
