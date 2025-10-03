#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_blocked_zones
short_description: List blocked zones from Technitium DNS server
version_added: "0.7.0"
description:
    - Retrieve a list of blocked zones from the Technitium DNS server.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_add_blocked_zone
    description: Add a domain to the blocked zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_blocked_zone
    description: Delete a domain from the blocked zones
  - module: effectivelywild.technitium_dns.technitium_dns_flush_blocked_zone
    description: Flush all blocked zones
  - module: effectivelywild.technitium_dns.technitium_dns_list_allowed_zones
    description: List allowed zones from Technitium DNS server
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
            - Whether to validate SSL certificates when making API requests
        required: false
        type: bool
        default: true
    domain:
        description:
            - The domain name to list records. If not passed, the domain is set to empty string which corresponds to the zone root.
        required: false
        type: str
    direction:
        description:
            - Allows specifying the direction of browsing the zone.
            - This option allows the server to skip empty labels in the domain name when browsing up or down.
        required: false
        type: str
        choices: ['up', 'down']
        default: 'down'
'''

EXAMPLES = r'''
- name: List all blocked zones
  technitium_dns_list_blocked_zones:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.zones

- name: List blocked zones for specific domain
  technitium_dns_list_blocked_zones:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "ads.example.com"
  register: result

- name: List blocked zones browsing up
  technitium_dns_list_blocked_zones:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "tracker.ads.example.com"
    direction: "up"
  register: result
'''

RETURN = r'''
domain:
    description: The domain name that was queried
    type: str
    returned: always
    sample: "ads.example.com"
zones:
    description: List of zone names
    type: list
    returned: always
    elements: str
    sample: ["ads.com", "tracker.com"]
records:
    description: List of DNS records in the blocked zone
    type: list
    returned: always
    elements: dict
    contains:
        name:
            description: Record name
            type: str
            returned: always
            sample: "ads.example.com"
        type:
            description: Record type
            type: str
            returned: always
            sample: "NS"
        ttl:
            description: Time to live
            type: str
            returned: always
            sample: "14400 (4 hours)"
        rData:
            description: Record data
            type: dict
            returned: always
changed:
    description: Whether the module made changes (always false for list operations)
    type: bool
    returned: always
    sample: false
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class ListBlockedZonesModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        domain=dict(type='str', required=False),
        direction=dict(type='str', required=False, choices=['up', 'down'], default='down')
    )

    def run(self):
        # Build query parameters
        params = {}
        if self.params.get('domain'):
            params['domain'] = self.params['domain']
        if self.params.get('direction'):
            params['direction'] = self.params['direction']

        # Fetch blocked zones from the API
        data = self.request('/api/blocked/list', params=params)
        self.validate_api_response(data)

        response = data.get('response', {})
        domain = response.get('domain', '')
        zones = response.get('zones', [])
        records = response.get('records', [])

        self.exit_json(
            changed=False,
            domain=domain,
            zones=zones,
            records=records
        )


if __name__ == '__main__':
    module = ListBlockedZonesModule()
    module.run()
