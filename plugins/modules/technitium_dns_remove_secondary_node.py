#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_remove_secondary_node
short_description: Remove a Secondary node from the cluster
version_added: "1.0.0"
description:
    - Ask a Secondary node to leave the cluster gracefully.
    - The Secondary node will initiate the Leave Cluster process.
    - This is equivalent to running leave_cluster on the Secondary node itself.
    - This call can only be made at the Primary node.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_delete_secondary_node
    description: Immediately delete a Secondary node without asking it to leave
  - module: effectivelywild.technitium_dns.technitium_dns_leave_cluster
    description: Leave cluster (run on Secondary node)
  - module: effectivelywild.technitium_dns.technitium_dns_get_cluster_state
    description: Get cluster state information
notes:
    - This operation requires Administration Delete permission.
    - This can only be run on the Primary node.
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
    secondary_node_id:
        description:
            - The Secondary node ID which needs to be asked to leave the cluster.
            - This is the numeric ID visible in cluster state.
        required: true
        type: int
'''

EXAMPLES = r'''
- name: Get cluster state to find Secondary node ID
  effectivelywild.technitium_dns.technitium_dns_get_cluster_state:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: cluster_state

- name: Remove Secondary node gracefully
  effectivelywild.technitium_dns.technitium_dns_remove_secondary_node:
    api_url: "http://localhost"
    api_token: "myapitoken"
    secondary_node_id: 811905692
  register: result

- name: Display updated cluster state
  debug:
    var: result.cluster_state
'''

RETURN = r'''
cluster_state:
    description: Complete cluster state after removing Secondary node
    type: dict
    returned: always
    contains:
        clusterInitialized:
            description: Whether the cluster is initialized
            type: bool
            returned: always
            sample: true
        dnsServerDomain:
            description: The DNS server domain name
            type: str
            returned: always
            sample: "server1.example.com"
        version:
            description: Technitium DNS Server version
            type: str
            returned: always
            sample: "14.0"
        clusterDomain:
            description: The cluster domain name
            type: str
            returned: always
            sample: "example.com"
        heartbeatRefreshIntervalSeconds:
            description: Interval in seconds for heartbeat refresh
            type: int
            returned: always
            sample: 30
        heartbeatRetryIntervalSeconds:
            description: Interval in seconds for heartbeat retry
            type: int
            returned: always
            sample: 10
        configRefreshIntervalSeconds:
            description: Interval in seconds for config refresh
            type: int
            returned: always
            sample: 900
        configRetryIntervalSeconds:
            description: Interval in seconds for config retry
            type: int
            returned: always
            sample: 60
        clusterNodes:
            description: List of nodes in the cluster (Secondary node should be removed)
            type: list
            returned: always
            elements: dict
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
    description: Status message
    type: str
    returned: always
    sample: "Secondary node removed successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class RemoveSecondaryModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        secondary_node_id=dict(type='int', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        secondary_node_id = params['secondary_node_id']

        # Get and validate cluster state
        cluster_initialized, cluster_state = self.get_cluster_state()
        self.require_cluster_initialized(cluster_initialized, cluster_state)

        # Validate this is a Primary node
        self.validate_cluster_node_type(
            cluster_state,
            'Primary',
            "This is not a Primary node. Secondary nodes can only be removed from the Primary node."
        )

        # Find and validate the Secondary node
        secondary_node = self.get_node_by_id(
            cluster_state,
            secondary_node_id,
            expected_type='Secondary',
            fail_if_not_found=False
        )

        # Idempotent check - if not found, nothing to remove
        if not secondary_node:
            self.exit_json(
                changed=False,
                cluster_state=cluster_state,
                msg=f"Secondary node with ID {secondary_node_id} not found in cluster"
            )

        # If we're in check mode, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Would remove Secondary node {secondary_node_id} ({secondary_node.get('name')})"
            )

        # Remove the Secondary node
        remove_params = {
            'secondaryNodeId': secondary_node_id
        }

        remove_data = self.request('/api/admin/cluster/primary/removeSecondary', params=remove_params, method='POST')
        if remove_data.get('status') != 'ok':
            error_msg = remove_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to remove Secondary node: {error_msg}",
                api_response=remove_data
            )

        cluster_state = remove_data.get('response', {})
        self.exit_json(
            changed=True,
            cluster_state=cluster_state,
            msg=f"Secondary node {secondary_node_id} removed successfully"
        )


if __name__ == '__main__':
    module = RemoveSecondaryModule()
    module.run()
