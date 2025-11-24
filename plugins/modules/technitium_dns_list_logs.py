#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_logs
short_description: List all log files from Technitium DNS server
version_added: "0.9.0"
description:
    - Retrieve a list of all log files.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_delete_log
    description: Delete a specific log file
  - module: effectivelywild.technitium_dns.technitium_dns_delete_all_logs
    description: Delete all log files
  - module: effectivelywild.technitium_dns.technitium_dns_query_logs
    description: Query logs to a specified DNS app
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
            - The node domain name for which this API call is intended
            - When unspecified, the current node is used
            - This parameter can be used only when Clustering is initialized
        required: false
        type: str
'''

EXAMPLES = r'''
- name: List all log files from Technitium DNS
  technitium_dns_list_logs:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.log_files

- name: Find logs from a specific date
  technitium_dns_list_logs:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: logs_result

- name: Display today's log
  debug:
    msg: "Log: {{ item.fileName }} ({{ item.size }})"
  loop: "{{ logs_result.log_files | selectattr('fileName', 'match', '2020-09-19') | list }}"

- name: List log files on a specific cluster node
  technitium_dns_list_logs:
    api_url: "http://localhost"
    api_token: "myapitoken"
    node: "node1.cluster.example.com"
  register: node_logs
'''

RETURN = r'''
log_files:
    description: List of log files from the Technitium DNS server
    type: list
    returned: always
    elements: dict
    contains:
        fileName:
            description: Name of the log file (typically YYYY-MM-DD format)
            type: str
            returned: always
            sample: "2020-09-19"
        size:
            description: Size of the log file with units
            type: str
            returned: always
            sample: "8.14 KB"
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


class ListLogsModule(TechnitiumModule):
    argument_spec = dict(
        node=dict(type='str', required=False),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Fetch all log files from the API
        params = {}
        if self.params.get('node'):
            params['node'] = self.params['node']

        data = self.request('/api/logs/list', params=params)
        self.validate_api_response(data)

        log_files = data.get('response', {}).get('logFiles', [])
        self.exit_json(changed=False, log_files=log_files)


if __name__ == '__main__':
    module = ListLogsModule()
    module.run()
