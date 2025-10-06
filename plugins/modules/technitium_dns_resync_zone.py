#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_resync_zone
short_description: Resync a Secondary or Stub zone
version_added: "0.4.0"
author: Frank Muise (@effectivelywild)
description:
  - Allows resyncing a Secondary or Stub zone.
  - This process will re-fetch all the records from the primary name server for the zone.
  - The zone will attempt to resync even if currently expired or has sync failures, as these may be resolved by the resync operation.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_zone
    description: Create DNS zones
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_info
    description: Get basic zone information
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_options
    description: Get all configured zone options
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
      - The domain name of the zone to resync
      - Must be a Secondary or Stub zone
      - Zone will attempt to resync even if currently expired or has sync failures
    required: true
    type: str
'''

EXAMPLES = r'''
- name: Resync a secondary zone
  technitium_dns_resync_zone:
    api_url: "http://localhost:5380"
    api_token: "{{ technitium_api_token }}"
    zone: "secondary.example.com"

- name: Resync a stub zone with custom API port
  technitium_dns_resync_zone:
    api_url: "http://dns.example.com"
    api_port: 5381
    api_token: "{{ technitium_api_token }}"
    zone: "stub.example.com"
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The API response payload (empty dict for successful resync operations)
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
    sample: "Zone 'secondary.example.com' resynced successfully."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class ResyncZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True)
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        zone = self.params['zone']

        # Validate that the zone exists and is a Secondary or Stub zone
        self.validate_zone_type(zone)

        if self.check_mode:
            self.exit_json(changed=True, msg=f"Zone '{zone}' would be resynced (check mode)", api_response={})

        # Perform the resync operation
        query = {'zone': zone}
        data = self.request('/api/zones/resync', params=query, method='POST')

        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        self.exit_json(changed=True, msg=f"Zone '{zone}' resynced successfully.", api_response=data)

    def validate_zone_type(self, zone):
        """Validate that the zone exists and is a Secondary or Stub zone"""
        # Get detailed zone information using zones/list API
        data = self.request('/api/zones/list')
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to fetch zone list: {error_msg}", api_response=data)

        zones = data.get('response', {}).get('zones', [])
        zone_info = next((z for z in zones if z.get('name') == zone), None)

        if zone_info is None:
            self.fail_json(msg=f"Zone '{zone}' does not exist")

        zone_type = zone_info.get('type', '')

        # Check if zone type is Secondary or Stub
        if zone_type not in ['Secondary', 'Stub']:
            self.fail_json(
                msg=f"Zone '{zone}' is of type '{zone_type}'. Only Secondary and Stub zones can be resynced."
            )

        # Note: We don't check isExpired or syncFailed status here because
        # the resync operation may actually resolve these issues if the
        # underlying problems (like zone transfer permissions) have been fixed


if __name__ == '__main__':
    module = ResyncZoneModule()
    module.run()
