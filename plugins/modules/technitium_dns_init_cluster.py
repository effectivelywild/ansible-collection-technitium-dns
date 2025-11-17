#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_init_cluster
short_description: Initialize a new DNS cluster
version_added: "1.0.0"
description:
    - Initialize a new Technitium DNS cluster making this server the Primary node.
    - You can add other DNS servers to this cluster later which will be added as Secondary nodes.
    - No data will be lost on this DNS server in this process.
    - If HTTPS is not enabled, it will be enabled automatically with a self-signed certificate.
    - Creates two zones if they don't exist - the Cluster Primary zone and the Cluster Catalog zone.
    - The Cluster domain name cannot be changed later.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_cluster_state
    description: Get cluster state information
  - module: effectivelywild.technitium_dns.technitium_dns_delete_cluster
    description: Delete cluster configuration
notes:
    - The initialization process will enable HTTPS with a self-signed certificate if not already enabled.
    - It's recommended to manually configure HTTPS with a valid certificate before initializing the cluster.
    - The Cluster Primary zone is named as the cluster domain name.
    - The Cluster Catalog zone uses 'cluster-catalog' as a subdomain of the cluster domain.
    - This operation requires Administration Delete permission.
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
    cluster_domain:
        description:
            - The fully qualified domain name to be used to identify the new cluster.
            - This cannot be changed later.
        required: true
        type: str
    primary_node_ip_addresses:
        description:
            - The static IP address(es) of this DNS server.
            - Must be accessible by all other DNS servers to be added later as Secondary nodes.
            - Accepts a list of IP addresses for nodes with multiple network interfaces.
            - When multiple IPs are provided, they will be used for cluster communication.
        required: true
        type: list
        elements: str
'''

EXAMPLES = r'''
- name: Initialize a new DNS cluster with single IP
  effectivelywild.technitium_dns.technitium_dns_init_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
    cluster_domain: "example.com"
    primary_node_ip_addresses:
      - "192.168.10.5"
  register: result

- name: Initialize cluster with multiple IP addresses
  effectivelywild.technitium_dns.technitium_dns_init_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
    cluster_domain: "example.com"
    primary_node_ip_addresses:
      - "192.168.10.5"
      - "10.0.1.5"
  register: result

- name: Display cluster state after initialization
  debug:
    var: result.cluster_state

- name: Initialize cluster with custom API port
  effectivelywild.technitium_dns.technitium_dns_init_cluster:
    api_url: "http://server1.example.com"
    api_token: "myapitoken"
    api_port: 5381
    cluster_domain: "dns-cluster.example.com"
    primary_node_ip_addresses:
      - "10.0.1.5"
'''

RETURN = r'''
cluster_state:
    description: Complete cluster state after initialization
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
            description: List of nodes in the cluster
            type: list
            returned: always
            elements: dict
            contains:
                id:
                    description: Node ID
                    type: int
                    sample: 1081800048
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
                    description: Node up since timestamp
                    type: str
                    sample: "2025-11-08T19:11:05.591447Z"
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
    returned: on error
    sample: "Failed to initialize cluster"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class InitClusterModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        cluster_domain=dict(type='str', required=True),
        primary_node_ip_addresses=dict(type='list', elements='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        cluster_domain = params['cluster_domain']
        ip_list = params['primary_node_ip_addresses']
        primary_node_ip_addresses_str = ','.join(ip_list)
        # For idempotency check, use first IP
        primary_node_ip_address = ip_list[0]

        # Get cluster state
        already_initialized, cluster_state = self.get_cluster_state()

        # If already initialized, check if it matches our desired state
        if already_initialized:
            current_domain = cluster_state.get('clusterDomain')

            # Find the primary node
            primary_node = self.get_primary_node(cluster_state)

            if current_domain == cluster_domain:
                # Already initialized with the same domain
                # Note: For idempotency we check if the first IP address is in the node's IP list
                current_ip_addresses = primary_node.get('ipAddresses', []) if primary_node else []
                if primary_node and primary_node_ip_address in current_ip_addresses:
                    # Perfect match - no changes needed
                    self.exit_json(
                        changed=False,
                        cluster_state=cluster_state,
                        msg="Cluster already initialized with matching configuration"
                    )
                else:
                    # Domain matches but IP address differs
                    self.fail_json(
                        msg=f"Cluster already initialized with domain '{cluster_domain}' but different IP address. "
                            f"Current: {', '.join(current_ip_addresses) if current_ip_addresses else 'unknown'}, "
                            f"Desired: {primary_node_ip_address}",
                        cluster_state=cluster_state
                    )
            else:
                # Already initialized with a different domain
                self.fail_json(
                    msg=f"Cluster already initialized with different domain '{current_domain}'. "
                        f"The cluster domain cannot be changed. Delete the cluster first.",
                    cluster_state=cluster_state
                )

        # If we're in check mode and cluster is not initialized, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Would initialize cluster with domain '{cluster_domain}'"
            )

        # Initialize the cluster - use new API parameter name
        init_params = {
            'clusterDomain': cluster_domain,
            'primaryNodeIpAddresses': primary_node_ip_addresses_str
        }

        init_data = self.request('/api/admin/cluster/init', params=init_params, method='POST')
        if init_data.get('status') != 'ok':
            error_msg = init_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to initialize cluster: {error_msg}",
                api_response=init_data
            )

        cluster_state = init_data.get('response', {})
        self.exit_json(
            changed=True,
            cluster_state=cluster_state,
            msg=f"Successfully initialized cluster with domain '{cluster_domain}'"
        )


if __name__ == '__main__':
    module = InitClusterModule()
    module.run()
