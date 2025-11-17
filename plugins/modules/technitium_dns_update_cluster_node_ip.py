#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_update_cluster_node_ip
short_description: Update cluster node IP address
version_added: "1.0.0"
description:
    - Update the current cluster node's IP address.
    - This can be called at both Primary and Secondary nodes.
    - Use this when the node's IP address has changed.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_init_cluster
    description: Initialize a new cluster
  - module: effectivelywild.technitium_dns.technitium_dns_init_join_cluster
    description: Join a cluster
  - module: effectivelywild.technitium_dns.technitium_dns_get_cluster_state
    description: Get cluster state information
notes:
    - This operation requires Administration Modify permission.
    - Can be run on both Primary and Secondary nodes.
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
            - The node domain name for which this API call is intended.
            - When unspecified, the current node is used.
            - This parameter can only be used when clustering is initialized.
        required: false
        type: str
    ip_address:
        description:
            - The new IP address to be updated for the current node.
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Update current node's IP address
  effectivelywild.technitium_dns.technitium_dns_update_cluster_node_ip:
    api_url: "http://localhost"
    api_token: "myapitoken"
    ip_address: "192.168.10.200"
  register: result

- name: Display updated cluster state
  debug:
    var: result.cluster_state

- name: Update specific node's IP address
  effectivelywild.technitium_dns.technitium_dns_update_cluster_node_ip:
    api_url: "http://localhost"
    api_token: "myapitoken"
    node: "server2.example.com"
    ip_address: "192.168.10.201"
'''

RETURN = r'''
cluster_state:
    description: Complete cluster state after updating IP address
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
            description: List of nodes in the cluster (IP should be updated for the specified node)
            type: list
            returned: always
            elements: dict
            contains:
                id:
                    description: Node ID
                    type: int
                    sample: 811905692
                name:
                    description: Node domain name
                    type: str
                    sample: "server2.example.com"
                ipAddress:
                    description: Node IP address (updated)
                    type: str
                    sample: "192.168.10.200"
                type:
                    description: Node type
                    type: str
                    sample: "Primary"
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
    sample: "Node IP address updated successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class UpdateClusterNodeIpModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False),
        ip_address=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        node = params.get('node')
        ip_address = params['ip_address']

        # Get and validate cluster state
        cluster_initialized, cluster_state = self.get_cluster_state(node=node)
        self.require_cluster_initialized(
            cluster_initialized,
            cluster_state,
            fail_message="Not part of any cluster"
        )

        # Check current IP address to determine if change is needed
        self_node = self.get_self_node(cluster_state)

        # v14.1 API uses ipAddresses (array) instead of ipAddress (string)
        current_ip_addresses = self_node.get('ipAddresses', []) if self_node else []
        if self_node and ip_address in current_ip_addresses:
            self.exit_json(
                changed=False,
                cluster_state=cluster_state,
                msg=f"Node IP address is already '{ip_address}'"
            )

        # If we're in check mode, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Would update node IP address to '{ip_address}'"
            )

        # Build update parameters - v14.1 API uses ipAddresses parameter
        update_params = self.build_cluster_params(node=node, ipAddresses=ip_address)

        # Update node IP address
        update_data = self.request('/api/admin/cluster/updateIpAddress', params=update_params, method='POST')
        if update_data.get('status') != 'ok':
            error_msg = update_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to update node IP address: {error_msg}",
                api_response=update_data
            )

        cluster_state = update_data.get('response', {})
        self.exit_json(
            changed=True,
            cluster_state=cluster_state,
            msg="Node IP address updated successfully"
        )


if __name__ == '__main__':
    module = UpdateClusterNodeIpModule()
    module.run()
