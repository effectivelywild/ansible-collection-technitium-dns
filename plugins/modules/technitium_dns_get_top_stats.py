#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_get_top_stats
short_description: Get top statistics for a specific type
version_added: "0.8.0"
description:
    - Retrieve top statistics data for a specified stats type
    - Can retrieve top clients, top domains, or top blocked domains.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_stats
    description: Get general DNS statistics from the dashboard
  - module: effectivelywild.technitium_dns.technitium_dns_delete_all_stats
    description: Delete all statistics from the server
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
    node:
        description:
            - The node domain name for which the stats data is needed
            - When unspecified, the current node is used
            - Set node name as 'cluster' to get aggregate stats for the entire cluster
            - This parameter can be used only when Clustering is initialized
        required: false
        type: str
    type:
        description:
            - The duration type for statistics.
        required: false
        type: str
        choices: ['LastHour', 'LastDay', 'LastWeek', 'LastMonth', 'LastYear', 'Custom']
        default: 'LastHour'
    start:
        description:
            - Start date in ISO 8601 format. Only applies to 'Custom' type.
        required: false
        type: str
    end:
        description:
            - End date in ISO 8601 format. Only applies to 'Custom' type.
        required: false
        type: str
    stats_type:
        description:
            - The type of statistics to retrieve.
        required: true
        type: str
        choices: ['TopClients', 'TopDomains', 'TopBlockedDomains']
    limit:
        description:
            - Maximum number of records to return.
        required: false
        type: int
        default: 1000
    no_reverse_lookup:
        description:
            - Disable reverse DNS lookup for Top Clients. Only applicable with TopClients stats type.
        required: false
        type: bool
        default: false
    only_rate_limited_clients:
        description:
            - List only clients that are being rate limited. Only applicable with TopClients stats type.
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Get top 10 clients for last hour
  technitium_dns_get_top_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
    stats_type: "TopClients"
    limit: 10
  register: result

- name: Get top domains for last day
  technitium_dns_get_top_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
    type: "LastDay"
    stats_type: "TopDomains"
    limit: 100
  register: result

- name: Get top blocked domains without reverse lookup
  technitium_dns_get_top_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
    stats_type: "TopBlockedDomains"
    limit: 50
  register: result

- name: Get only rate limited clients
  technitium_dns_get_top_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
    stats_type: "TopClients"
    only_rate_limited_clients: true
  register: result

- name: Get cluster-wide top domains
  technitium_dns_get_top_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
    stats_type: "TopDomains"
    node: "cluster"
  register: result

- debug:
    var: result.data
'''

RETURN = r'''
data:
    description: Top statistics data (format depends on stats_type)
    type: list
    returned: always
    elements: dict
    sample:
        - name: "192.168.10.5"
          domain: "server1.local"
          hits: 236
          rateLimited: false
topClients:
    description: List of top clients (only when stats_type is TopClients)
    type: list
    returned: when stats_type is TopClients
    elements: dict
    contains:
        name:
            description: Client IP address
            type: str
            returned: always
            sample: "192.168.10.5"
        domain:
            description: Client hostname (if resolved)
            type: str
            returned: always
            sample: "server1.local"
        hits:
            description: Number of queries from this client
            type: int
            returned: always
            sample: 236
        rateLimited:
            description: Whether client is rate limited
            type: bool
            returned: always
            sample: false
topDomains:
    description: List of top domains (only when stats_type is TopDomains)
    type: list
    returned: when stats_type is TopDomains
    elements: dict
    contains:
        name:
            description: Domain name
            type: str
            returned: always
            sample: "www.google.com"
        hits:
            description: Number of queries for this domain
            type: int
            returned: always
            sample: 34
topBlockedDomains:
    description: List of top blocked domains (only when stats_type is TopBlockedDomains)
    type: list
    returned: when stats_type is TopBlockedDomains
    elements: dict
    contains:
        name:
            description: Blocked domain name
            type: str
            returned: always
            sample: "mobile.pipe.aria.microsoft.com"
        hits:
            description: Number of blocked queries for this domain
            type: int
            returned: always
            sample: 10
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

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class GetTopStatsModule(TechnitiumModule):
    argument_spec = dict(
        node=dict(type='str', required=False),
        type=dict(type='str', required=False, default='LastHour',
                  choices=['LastHour', 'LastDay', 'LastWeek', 'LastMonth', 'LastYear', 'Custom']),
        start=dict(type='str', required=False),
        end=dict(type='str', required=False),
        stats_type=dict(type='str', required=True, choices=['TopClients', 'TopDomains', 'TopBlockedDomains']),
        limit=dict(type='int', required=False, default=1000),
        no_reverse_lookup=dict(type='bool', required=False, default=False),
        only_rate_limited_clients=dict(type='bool', required=False, default=False),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        params = {
            'type': self.params['type'],
            'statsType': self.params['stats_type'],
            'limit': self.params['limit']
        }

        # Add node parameter if specified
        if self.params.get('node'):
            params['node'] = self.params['node']

        # Add custom date range parameters if type is Custom
        if self.params['type'] == 'Custom':
            if self.params.get('start'):
                params['start'] = self.params['start']
            if self.params.get('end'):
                params['end'] = self.params['end']

        # Add TopClients-specific parameters
        if self.params['stats_type'] == 'TopClients':
            if self.params['no_reverse_lookup']:
                params['noReverseLookup'] = 'true'
            if self.params['only_rate_limited_clients']:
                params['onlyRateLimitedClients'] = 'true'

        # Fetch top stats from the API
        data = self.request('/api/dashboard/stats/getTop', params=params)
        self.validate_api_response(data)

        response = data.get('response', {})

        # Build result based on stats_type
        result = {
            'changed': False,
            'data': response.get(self.params['stats_type'][0].lower() + self.params['stats_type'][1:], [])
        }

        # Also include the specific key for backwards compatibility
        stats_key = self.params['stats_type'][0].lower() + self.params['stats_type'][1:]
        result[stats_key] = result['data']

        self.exit_json(**result)


if __name__ == '__main__':
    module = GetTopStatsModule()
    module.run()
