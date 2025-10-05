#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_cache
short_description: List cached DNS zones and records from Technitium DNS server
version_added: "0.8.0"
description:
    - Retrieve cached DNS zones and records from server cache.
    - Can list cache for a specific domain or browse the cache hierarchy.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_delete_cache
    description: Delete a specific cached zone
  - module: effectivelywild.technitium_dns.technitium_dns_flush_cache
    description: Flush the entire DNS cache
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
    domain:
        description:
            - The domain name to list cached records for.
            - If not specified, lists the cache root (empty string).
        required: false
        type: str
        default: ""
    direction:
        description:
            - Direction for browsing the zone hierarchy.
            - Allows the server to skip empty labels when browsing.
        required: false
        type: str
        choices: ['up', 'down']
        default: 'down'
'''

EXAMPLES = r'''
- name: List all cached zones at root
  technitium_dns_list_cache:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: List cached records for google.com
  technitium_dns_list_cache:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "google.com"
  register: result

- name: Browse cache hierarchy upward from subdomain
  technitium_dns_list_cache:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "www.example.com"
    direction: "up"
  register: result
'''

RETURN = r'''
domain:
    description: The domain name that was queried
    type: str
    returned: always
    sample: "google.com"
zones:
    description: List of sub-zones under the queried domain
    type: list
    returned: always
    elements: str
    sample: ["www.google.com", "mail.google.com"]
records:
    description: List of cached DNS records for the domain
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
            description: DNS record type
            type: str
            returned: always
            sample: "A"
        ttl:
            description: Time to live for the cached record
            type: str
            returned: always
            sample: "283 (4 mins 43 sec)"
        rData:
            description: Record data
            type: dict
            returned: always
            sample: {"value": "216.58.199.174"}
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


class ListCacheModule(TechnitiumModule):
    argument_spec = dict(
        domain=dict(type='str', required=False, default=''),
        direction=dict(type='str', required=False, default='down', choices=['up', 'down']),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        params = {}

        # Add domain parameter if provided
        if self.params['domain']:
            params['domain'] = self.params['domain']

        # Add direction parameter
        params['direction'] = self.params['direction']

        # Fetch cached zones from the API
        data = self.request('/api/cache/list', params=params)
        self.validate_api_response(data)

        response = data.get('response', {})

        self.exit_json(
            changed=False,
            domain=response.get('domain', ''),
            zones=response.get('zones', []),
            records=response.get('records', [])
        )


if __name__ == '__main__':
    module = ListCacheModule()
    module.run()
