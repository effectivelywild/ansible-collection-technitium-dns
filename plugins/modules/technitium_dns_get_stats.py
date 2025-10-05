#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_get_stats
short_description: Get DNS statistics from server dashboard
version_added: "0.8.0"
description:
    - Retrieve DNS statistics displayed on the server dashboard.
    - Returns aggregate stats, chart data, and top lists for clients, domains, and blocked domains.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_top_stats
    description: Get top statistics for specific stats type
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
    type:
        description:
            - The duration type for statistics.
        required: false
        type: str
        choices: ['LastHour', 'LastDay', 'LastWeek', 'LastMonth', 'LastYear', 'Custom']
        default: 'LastHour'
    utc:
        description:
            - Set to true to return chart data with labels in UTC format.
        required: false
        type: bool
        default: false
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
'''

EXAMPLES = r'''
- name: Get last hour statistics
  technitium_dns_get_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Get last day statistics in UTC
  technitium_dns_get_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
    type: "LastDay"
    utc: true
  register: result

- name: Get custom date range statistics
  technitium_dns_get_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
    type: "Custom"
    start: "2024-01-01T00:00:00Z"
    end: "2024-01-31T23:59:59Z"
  register: result

- debug:
    var: result.stats
'''

RETURN = r'''
stats:
    description: Aggregate DNS statistics
    type: dict
    returned: always
    contains:
        totalQueries:
            description: Total number of queries
            type: int
            returned: always
            sample: 925
        totalNoError:
            description: Total successful queries
            type: int
            returned: always
            sample: 834
        totalServerFailure:
            description: Total server failure responses
            type: int
            returned: always
            sample: 1
        totalNxDomain:
            description: Total non-existent domain responses
            type: int
            returned: always
            sample: 90
        totalRefused:
            description: Total refused queries
            type: int
            returned: always
            sample: 0
        totalAuthoritative:
            description: Total authoritative responses
            type: int
            returned: always
            sample: 47
        totalRecursive:
            description: Total recursive queries
            type: int
            returned: always
            sample: 348
        totalCached:
            description: Total cached responses
            type: int
            returned: always
            sample: 481
        totalBlocked:
            description: Total blocked queries
            type: int
            returned: always
            sample: 49
        totalDropped:
            description: Total dropped queries
            type: int
            returned: always
            sample: 0
        totalClients:
            description: Total unique clients
            type: int
            returned: always
            sample: 6
        zones:
            description: Total number of zones
            type: int
            returned: always
            sample: 19
        cachedEntries:
            description: Total cached entries
            type: int
            returned: always
            sample: 6330
        allowedZones:
            description: Total allowed zones
            type: int
            returned: always
            sample: 10
        blockedZones:
            description: Total blocked zones
            type: int
            returned: always
            sample: 1
        allowListZones:
            description: Total allow list zones
            type: int
            returned: always
            sample: 0
        blockListZones:
            description: Total block list zones
            type: int
            returned: always
            sample: 307447
mainChartData:
    description: Main chart data with time series
    type: dict
    returned: always
    contains:
        labelFormat:
            description: Format for time labels
            type: str
            returned: always
            sample: "HH:mm"
        labels:
            description: Array of timestamp labels
            type: list
            elements: str
            returned: always
        datasets:
            description: Chart datasets for different metrics
            type: list
            elements: dict
            returned: always
queryResponseChartData:
    description: Query response type distribution chart data
    type: dict
    returned: always
    contains:
        labels:
            description: Response type labels
            type: list
            elements: str
            returned: always
        datasets:
            description: Response count datasets
            type: list
            elements: dict
            returned: always
queryTypeChartData:
    description: Query type distribution chart data
    type: dict
    returned: always
    contains:
        labels:
            description: Query type labels (A, AAAA, HTTPS, etc.)
            type: list
            elements: str
            returned: always
        datasets:
            description: Query count datasets
            type: list
            elements: dict
            returned: always
protocolTypeChartData:
    description: Protocol type distribution chart data
    type: dict
    returned: always
    contains:
        labels:
            description: Protocol labels (UDP, TCP, etc.)
            type: list
            elements: str
            returned: always
        datasets:
            description: Protocol count datasets
            type: list
            elements: dict
            returned: always
topClients:
    description: List of top DNS clients
    type: list
    returned: always
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
            sample: "server1.home"
        hits:
            description: Number of queries from this client
            type: int
            returned: always
            sample: 463
        rateLimited:
            description: Whether client is rate limited
            type: bool
            returned: always
            sample: false
topDomains:
    description: List of most queried domains
    type: list
    returned: always
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
    description: List of most blocked domains
    type: list
    returned: always
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


class GetStatsModule(TechnitiumModule):
    argument_spec = dict(
        type=dict(type='str', required=False, default='LastHour',
                  choices=['LastHour', 'LastDay', 'LastWeek', 'LastMonth', 'LastYear', 'Custom']),
        utc=dict(type='bool', required=False, default=False),
        start=dict(type='str', required=False),
        end=dict(type='str', required=False),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        params = {
            'type': self.params['type'],
            'utc': str(self.params['utc']).lower()
        }

        # Add custom date range parameters if type is Custom
        if self.params['type'] == 'Custom':
            if self.params.get('start'):
                params['start'] = self.params['start']
            if self.params.get('end'):
                params['end'] = self.params['end']

        # Fetch stats from the API
        data = self.request('/api/dashboard/stats/get', params=params)
        self.validate_api_response(data)

        response = data.get('response', {})

        self.exit_json(
            changed=False,
            stats=response.get('stats', {}),
            mainChartData=response.get('mainChartData', {}),
            queryResponseChartData=response.get('queryResponseChartData', {}),
            queryTypeChartData=response.get('queryTypeChartData', {}),
            protocolTypeChartData=response.get('protocolTypeChartData', {}),
            topClients=response.get('topClients', []),
            topDomains=response.get('topDomains', []),
            topBlockedDomains=response.get('topBlockedDomains', [])
        )


if __name__ == '__main__':
    module = GetStatsModule()
    module.run()
