#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_get_cluster_state
short_description: Get DNS cluster state
version_added: "1.0.0"
description:
    - Returns data on the current state of the DNS cluster.
    - Can be used to check if clustering is initialized and view cluster node information.
    - Optionally includes server IP addresses configured on the server.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_init_cluster
    description: Initialize a new cluster
  - module: effectivelywild.technitium_dns.technitium_dns_delete_cluster
    description: Delete cluster configuration
notes:
    - This operation requires Administration View permission.
    - The I(node) parameter can only be used when clustering is initialized.
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
            - This parameter can be used only when clustering is initialized.
        required: false
        type: str
    include_server_ip_addresses:
        description:
            - Set to true to return a list of static IP addresses configured on the server.
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Get cluster state
  effectivelywild.technitium_dns.technitium_dns_get_cluster_state:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Display cluster state
  debug:
    var: result.cluster_state

- name: Check if cluster is initialized
  effectivelywild.technitium_dns.technitium_dns_get_cluster_state:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Fail if cluster is not initialized
  fail:
    msg: "Cluster is not initialized"
  when: not result.cluster_state.clusterInitialized

- name: Get cluster state with server IP addresses
  effectivelywild.technitium_dns.technitium_dns_get_cluster_state:
    api_url: "http://localhost"
    api_token: "myapitoken"
    include_server_ip_addresses: true
  register: result

- name: Display server IP addresses
  debug:
    var: result.cluster_state.serverIpAddresses

- name: Get cluster state for specific node
  effectivelywild.technitium_dns.technitium_dns_get_cluster_state:
    api_url: "http://localhost"
    api_token: "myapitoken"
    node: "server2.example.com"
  register: result
'''

RETURN = r'''
cluster_state:
    description: Complete cluster state information
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
            description: The cluster domain name (only when initialized)
            type: str
            returned: when cluster is initialized
            sample: "example.com"
        heartbeatRefreshIntervalSeconds:
            description: Interval in seconds for heartbeat refresh (only when initialized)
            type: int
            returned: when cluster is initialized
            sample: 30
        heartbeatRetryIntervalSeconds:
            description: Interval in seconds for heartbeat retry (only when initialized)
            type: int
            returned: when cluster is initialized
            sample: 10
        configRefreshIntervalSeconds:
            description: Interval in seconds for config refresh (only when initialized)
            type: int
            returned: when cluster is initialized
            sample: 900
        configRetryIntervalSeconds:
            description: Interval in seconds for config retry (only when initialized)
            type: int
            returned: when cluster is initialized
            sample: 60
        configLastSynced:
            description: When the configuration was last synced (ISO 8601 format, only when initialized)
            type: str
            returned: when cluster is initialized
            sample: "2025-09-26T12:30:16Z"
        clusterNodes:
            description: List of nodes in the cluster (only when initialized)
            type: list
            returned: when cluster is initialized
            elements: dict
            contains:
                id:
                    description: Node ID
                    type: int
                    sample: 1342079372
                name:
                    description: Node domain name
                    type: str
                    sample: "server1.example.com"
                url:
                    description: Node API URL
                    type: str
                    sample: "https://server1.example.com:53443/"
                ipAddress:
                    description: Node IP address
                    type: str
                    sample: "192.168.10.5"
                type:
                    description: Node type (Primary or Secondary)
                    type: str
                    sample: "Primary"
                state:
                    description: Node state (Self, Connected, Unreachable)
                    type: str
                    sample: "Self"
                upSince:
                    description: Last seen timestamp
                    type: str
                    sample: "2025-09-26T12:30:16Z"
        serverIpAddresses:
            description: List of static IP addresses configured on the server (only when include_server_ip_addresses is true)
            type: list
            returned: when include_server_ip_addresses is true
            elements: str
            sample: ["192.168.10.5", "192.168.120.1"]
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
msg:
    description: Status message
    type: str
    returned: on error
    sample: "Failed to get cluster state"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class GetClusterStateModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False),
        include_server_ip_addresses=dict(type='bool', required=False, default=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        node = params.get('node')
        include_server_ip_addresses = params.get('include_server_ip_addresses', False)

        # Build request parameters
        request_params = {}
        if node:
            request_params['node'] = node
        if include_server_ip_addresses:
            request_params['includeServerIpAddresses'] = 'true'

        # Get cluster state
        data = self.request('/api/admin/cluster/state', params=request_params)
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to get cluster state: {error_msg}", api_response=data)

        cluster_state = data.get('response', {})
        self.exit_json(changed=False, cluster_state=cluster_state)


if __name__ == '__main__':
    module = GetClusterStateModule()
    module.run()
