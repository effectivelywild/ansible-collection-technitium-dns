#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible_collections.technitium.dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_unsign_zone
short_description: Unsign a primary DNS zone (remove DNSSEC) using Technitium DNS API
version_added: "1.0.0"
description:
  - Unsigns a primary DNS zone by removing DNSSEC using the Technitium DNS API.
  - Idempotency is achieved by checking if the zone is already unsigned.
options:
  api_url:
    description:
      - Base URL for the Technitium DNS API (e.g., http://localhost:5380)
    required: true
    type: str
  api_token:
    description:
      - API token for authentication
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
      - The name of the primary zone to unsign
    required: true
    type: str
requirements:
  - requests
author:
  - Your Name (@yourgithub)
'''

EXAMPLES = r'''
- name: Unsign a primary zone
  technitium_dns_unsign_zone:
    api_url: "http://localhost:5380"
    api_token: "{{ technitium_api_token }}"
    zone: "example.com"
'''

RETURN = r'''
status:
  description: API response status
  returned: always
  type: str
  sample: ok
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

def main():
    module = UnsignZoneModule()
    module()

if __name__ == '__main__':
    main()