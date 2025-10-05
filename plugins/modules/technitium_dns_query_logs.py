#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_query_logs
short_description: Query logs from a specified DNS app on Technitium DNS server
version_added: "0.9.0"
description:
    - Query logs from a specified DNS app with optional filtering.
    - Supports pagination and filtering by various criteria.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_logs
    description: List all log files
  - module: effectivelywild.technitium_dns.technitium_dns_delete_log
    description: Delete a specific log file
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
    name:
        description:
            - The name of the installed DNS app
        required: true
        type: str
    class_path:
        description:
            - The class path of the DNS app
        required: true
        type: str
    page_number:
        description:
            - The page number of the data set to retrieve
        required: false
        type: int
    entries_per_page:
        description:
            - The number of entries per page
        required: false
        type: int
    descending_order:
        description:
            - Orders the selected data set in descending order
        required: false
        type: bool
    start:
        description:
            - The start date time in ISO 8601 format to filter the logs
        required: false
        type: str
    end:
        description:
            - The end date time in ISO 8601 format to filter the logs
        required: false
        type: str
    client_ip_address:
        description:
            - The client IP address to filter the logs
        required: false
        type: str
    protocol:
        description:
            - The DNS transport protocol to filter the logs
        required: false
        type: str
        choices: ['Udp', 'Tcp', 'Tls', 'Https', 'Quic']
    response_type:
        description:
            - The DNS server response type to filter the logs
        required: false
        type: str
        choices: ['Authoritative', 'Recursive', 'Cached', 'Blocked', 'UpstreamBlocked', 'CacheBlocked']
    rcode:
        description:
            - The DNS response code to filter the logs
        required: false
        type: str
    qname:
        description:
            - The query name (QNAME) in the request question section to filter the logs
        required: false
        type: str
    qtype:
        description:
            - The DNS resource record type (QTYPE) in the request question section to filter the logs
        required: false
        type: str
    qclass:
        description:
            - The DNS class (QCLASS) in the request question section to filter the logs
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Query logs from a DNS app
  technitium_dns_query_logs:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Query Logger"
    class_path: "QueryLogger.App"
  register: result

- debug:
    var: result.entries

- name: Query logs with filters
  technitium_dns_query_logs:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Query Logger"
    class_path: "QueryLogger.App"
    page_number: 1
    entries_per_page: 50
    descending_order: true
    response_type: "Blocked"
    qname: "example.com"
  register: blocked_queries

- name: Query logs for a specific time range
  technitium_dns_query_logs:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Query Logger"
    class_path: "QueryLogger.App"
    start: "2021-09-10 00:00:00"
    end: "2021-09-11 23:59:59"
    protocol: "Udp"
'''

RETURN = r'''
page_number:
    description: Current page number
    type: int
    returned: always
    sample: 1
total_pages:
    description: Total number of pages
    type: int
    returned: always
    sample: 2
total_entries:
    description: Total number of entries
    type: int
    returned: always
    sample: 13
entries:
    description: List of log entries
    type: list
    returned: always
    elements: dict
    contains:
        rowNumber:
            description: Row number of the entry
            type: int
            returned: always
            sample: 1
        timestamp:
            description: Timestamp of the query
            type: str
            returned: always
            sample: "2021-09-10T12:22:52Z"
        clientIpAddress:
            description: Client IP address
            type: str
            returned: always
            sample: "127.0.0.1"
        protocol:
            description: DNS transport protocol
            type: str
            returned: always
            sample: "Udp"
        responseType:
            description: DNS server response type
            type: str
            returned: always
            sample: "Recursive"
        responseRtt:
            description: Response round-trip time in milliseconds (for recursive queries)
            type: float
            returned: when available
            sample: 33.45
        rcode:
            description: DNS response code
            type: str
            returned: always
            sample: "NoError"
        qname:
            description: Query name
            type: str
            returned: always
            sample: "google.com"
        qtype:
            description: Query type
            type: str
            returned: always
            sample: "A"
        qclass:
            description: Query class
            type: str
            returned: always
            sample: "IN"
        answer:
            description: DNS answer
            type: str
            returned: always
            sample: "172.217.166.46"
changed:
    description: Whether the module made changes (always false for query operations)
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


class QueryLogsModule(TechnitiumModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        class_path=dict(type='str', required=True),
        page_number=dict(type='int', required=False),
        entries_per_page=dict(type='int', required=False),
        descending_order=dict(type='bool', required=False),
        start=dict(type='str', required=False),
        end=dict(type='str', required=False),
        client_ip_address=dict(type='str', required=False),
        protocol=dict(type='str', required=False, choices=['Udp', 'Tcp', 'Tls', 'Https', 'Quic']),
        response_type=dict(type='str', required=False, choices=['Authoritative', 'Recursive', 'Cached', 'Blocked', 'UpstreamBlocked', 'CacheBlocked']),
        rcode=dict(type='str', required=False),
        qname=dict(type='str', required=False),
        qtype=dict(type='str', required=False),
        qclass=dict(type='str', required=False),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Build query parameters
        params = {
            'name': self.params['name'],
            'classPath': self.params['class_path']
        }

        # Add optional parameters if provided
        optional_params = [
            'page_number', 'entries_per_page', 'descending_order',
            'start', 'end', 'client_ip_address', 'protocol',
            'response_type', 'rcode', 'qname', 'qtype', 'qclass'
        ]

        for param in optional_params:
            if self.params.get(param) is not None:
                # Convert snake_case to camelCase for API
                api_param = ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(param.split('_')))
                params[api_param] = self.params[param]

        # Query logs from the API
        data = self.request('/api/logs/query', params=params)
        self.validate_api_response(data)

        response = data.get('response', {})
        self.exit_json(
            changed=False,
            page_number=response.get('pageNumber'),
            total_pages=response.get('totalPages'),
            total_entries=response.get('totalEntries'),
            entries=response.get('entries', [])
        )


if __name__ == '__main__':
    module = QueryLogsModule()
    module.run()
