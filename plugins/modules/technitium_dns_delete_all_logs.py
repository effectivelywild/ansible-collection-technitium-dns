#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_all_logs
short_description: Delete all log files
description:
    - Permanently delete all log files from disk.
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
    node:
        description:
            - The node domain name for which this API call is intended
            - When unspecified, the current node is used
            - This parameter can be used only when Clustering is initialized
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Delete all log files from Technitium DNS
  technitium_dns_delete_all_logs:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Delete all logs with confirmation
  technitium_dns_delete_all_logs:
    api_url: "http://localhost"
    api_token: "myapitoken"
  when: cleanup_logs | default(false) | bool

- name: Delete all logs on a specific cluster node
  technitium_dns_delete_all_logs:
    api_url: "http://localhost"
    api_token: "myapitoken"
    node: "node1.cluster.example.com"
'''

RETURN = r'''
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
    description: Human-readable message about the operation
    type: str
    returned: always
    sample: "All log files deleted successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteAllLogsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False)
    )

    def run(self):
        # Delete all log files from the API
        params = {}
        if self.params.get('node'):
            params['node'] = self.params['node']

        data = self.request('/api/logs/deleteAll', params=params)
        self.validate_api_response(data)

        self.exit_json(
            changed=True,
            msg="All log files deleted successfully"
        )


if __name__ == '__main__':
    module = DeleteAllLogsModule()
    module.run()
