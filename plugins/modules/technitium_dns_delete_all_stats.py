#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_all_stats
short_description: Delete all statistics from Technitium DNS server
version_added: "0.8.0"
description:
    - Permanently delete all hourly and daily stats files from disk.
    - Clears all statistics stored in memory.
    - This will clear all stats from the Dashboard.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_stats
    description: Get DNS statistics from the dashboard
  - module: effectivelywild.technitium_dns.technitium_dns_get_top_stats
    description: Get top statistics for specific stats type
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
            - The node domain name for which the stats data needs to be deleted
            - When unspecified, the current node is used
            - This parameter can be used only when Clustering is initialized
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Delete all statistics from Technitium DNS
  technitium_dns_delete_all_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Delete all statistics from specific cluster node
  technitium_dns_delete_all_stats:
    api_url: "http://localhost"
    api_token: "myapitoken"
    node: "node1.example.com"
  register: result
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
    sample: "All statistics deleted successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteAllStatsModule(TechnitiumModule):
    argument_spec = dict(
        node=dict(type='str', required=False),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        params = {}

        # Add node parameter if specified
        if self.params.get('node'):
            params['node'] = self.params['node']

        # Delete all stats from the API
        data = self.request('/api/dashboard/stats/deleteAll', params=params)
        self.validate_api_response(data)

        self.exit_json(
            changed=True,
            msg="All statistics deleted successfully"
        )


if __name__ == '__main__':
    module = DeleteAllStatsModule()
    module.run()
