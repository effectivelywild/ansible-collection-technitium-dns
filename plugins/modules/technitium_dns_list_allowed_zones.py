#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_allowed_zones
short_description: List allowed zones
version_added: "0.7.0"
description:
    - Retrieve a list of allowed zones.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_add_allowed_zone
    description: Add a domain to the allowed zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_allowed_zone
    description: Delete a domain from the allowed zones
  - module: effectivelywild.technitium_dns.technitium_dns_flush_allowed_zone
    description: Flush all allowed zones
  - module: effectivelywild.technitium_dns.technitium_dns_list_blocked_zones
    description: List blocked zones
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
    node:
        description:
            - The node domain name for which this API call is intended
            - When unspecified, the current node is used
            - This parameter can be used only when Clustering is initialized
        required: false
        type: str
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
- name: List all allowed zones
  technitium_dns_list_allowed_zones:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.zones

- name: List allowed zones for specific domain
  technitium_dns_list_allowed_zones:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "google.com"
  register: result

- name: List allowed zones browsing up
  technitium_dns_list_allowed_zones:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "subdomain.example.com"
    direction: "up"
  register: result

- name: List allowed zones on a specific cluster node
  technitium_dns_list_allowed_zones:
    api_url: "http://localhost"
    api_token: "myapitoken"
    node: "node1.cluster.example.com"
  register: result
'''

RETURN = r'''
domain:
    description: The domain name that was queried
    type: str
    returned: always
    sample: "google.com"
zones:
    description: List of zone names
    type: list
    returned: always
    elements: str
    sample: ["example.com", "test.com"]
records:
    description: List of DNS records in the allowed zone
    type: list
    returned: always
    elements: dict
    contains:
        name:
            description: Record name
            type: str
            returned: always
            sample: "google.com"
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


class ListAllowedZonesModule(TechnitiumModule):
    argument_spec = dict(
        node=dict(type='str', required=False),
        **TechnitiumModule.get_common_argument_spec(),
        domain=dict(type='str', required=False),
        direction=dict(type='str', required=False, choices=['up', 'down'], default='down')
    )

    def run(self):
        # Build query parameters
        params = {}
        if self.params.get('node'):
            params['node'] = self.params['node']
        if self.params.get('domain'):
            params['domain'] = self.params['domain']
        if self.params.get('direction'):
            params['direction'] = self.params['direction']

        # Fetch allowed zones from the API
        data = self.request('/api/allowed/list', params=params)
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
    module = ListAllowedZonesModule()
    module.run()
