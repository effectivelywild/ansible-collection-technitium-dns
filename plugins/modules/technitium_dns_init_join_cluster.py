#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_init_join_cluster
short_description: Join a DNS server to an existing cluster as a Secondary node
version_added: "1.0.0"
description:
    - Join this DNS server to an existing cluster as a Secondary node.
    - This process will overwrite configuration on this server for Allowed, Blocked, Apps, Settings and Administration sections.
    - The server will automatically synchronize its configuration with the Primary node.
    - If HTTPS is not enabled, it will be enabled automatically with a self-signed certificate.
    - This can only be called on a Secondary node (not yet joined to a cluster).
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_init_cluster
    description: Initialize a new cluster (Primary node)
  - module: effectivelywild.technitium_dns.technitium_dns_leave_cluster
    description: Leave a cluster
  - module: effectivelywild.technitium_dns.technitium_dns_get_cluster_state
    description: Get cluster state information
notes:
    - This operation requires Administration Delete permission.
    - The process may take a while depending on the amount of config data to sync.
    - Configuration will be permanently overwritten for Allowed, Blocked, Apps, Settings and Administration sections.
    - It's recommended to manually configure HTTPS with a valid certificate before joining.
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
    secondary_node_ip_address:
        description:
            - The static IP address of this DNS server that will be accessible by all other nodes in the cluster.
        required: true
        type: str
    primary_node_url:
        description:
            - The web service HTTPS URL of the Primary node in the cluster.
        required: true
        type: str
    primary_node_ip_address:
        description:
            - The IP address of the Primary node in the cluster.
            - When unspecified, the domain name in the Primary node URL will be resolved and used.
        required: false
        type: str
    ignore_certificate_errors:
        description:
            - Set to true only when you know the Primary node uses a self-signed TLS certificate and is on a private network.
        required: false
        type: bool
        default: false
    primary_node_username:
        description:
            - The username of an administrator on the Primary node in the cluster.
        required: true
        type: str
    primary_node_password:
        description:
            - The password of the administrator user.
        required: true
        type: str
    primary_node_totp:
        description:
            - The 6-digit code from your authenticator app for the administrator user.
            - Only required if the user has 2FA enabled.
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Join DNS server to cluster as Secondary node
  effectivelywild.technitium_dns.technitium_dns_init_join_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
    secondary_node_ip_address: "192.168.10.101"
    primary_node_url: "https://server1.example.com:53443/"
    primary_node_username: "admin"
    primary_node_password: "adminpassword"
  register: result

- name: Join cluster with self-signed certificate on primary
  effectivelywild.technitium_dns.technitium_dns_init_join_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
    secondary_node_ip_address: "192.168.10.102"
    primary_node_url: "https://server1.example.com:53443/"
    primary_node_ip_address: "192.168.10.5"
    ignore_certificate_errors: true
    primary_node_username: "admin"
    primary_node_password: "adminpassword"

- name: Join cluster with 2FA enabled
  effectivelywild.technitium_dns.technitium_dns_init_join_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
    secondary_node_ip_address: "192.168.10.103"
    primary_node_url: "https://server1.example.com:53443/"
    primary_node_username: "admin"
    primary_node_password: "adminpassword"
    primary_node_totp: "123456"
'''

RETURN = r'''
cluster_state:
    description: Complete cluster state after joining
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
            sample: "server2.example.com"
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
        configLastSynced:
            description: When the configuration was last synced
            type: str
            returned: always
            sample: "2025-09-27T13:19:55Z"
        clusterNodes:
            description: List of nodes in the cluster
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
                url:
                    description: Node API URL
                    type: str
                    sample: "https://server2.example.com:53443/"
                ipAddress:
                    description: Node IP address
                    type: str
                    sample: "192.168.10.101"
                type:
                    description: Node type (Primary or Secondary)
                    type: str
                    sample: "Secondary"
                state:
                    description: Node state (Self, Connected, Unreachable)
                    type: str
                    sample: "Self"
                upSince:
                    description: Node up since timestamp
                    type: str
                    sample: "2025-09-27T13:19:54.6215569Z"
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
    sample: "Successfully joined cluster"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class InitJoinClusterModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        secondary_node_ip_address=dict(type='str', required=True),
        primary_node_url=dict(type='str', required=True),
        primary_node_ip_address=dict(type='str', required=False),
        ignore_certificate_errors=dict(type='bool', required=False, default=False),
        primary_node_username=dict(type='str', required=True),
        primary_node_password=dict(type='str', required=True, no_log=True),
        primary_node_totp=dict(type='str', required=False, no_log=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        secondary_node_ip_address = params['secondary_node_ip_address']
        primary_node_url = params['primary_node_url']
        primary_node_ip_address = params.get('primary_node_ip_address')
        ignore_certificate_errors = params.get('ignore_certificate_errors', False)
        primary_node_username = params['primary_node_username']
        primary_node_password = params['primary_node_password']
        primary_node_totp = params.get('primary_node_totp')

        # Get cluster state
        already_initialized, cluster_state = self.get_cluster_state()

        # If already initialized, check if it's already joined to the expected cluster
        if already_initialized:
            current_domain = cluster_state.get('clusterDomain')

            # Check if this is a Secondary node (not Primary)
            self_node = self.get_self_node(cluster_state)
            if self_node and self_node.get('type') == 'Primary':
                self.fail_json(
                    msg="This node is a Primary node. Use technitium_dns_delete_cluster to remove cluster configuration first.",
                    cluster_state=cluster_state
                )

            # Already joined - this is idempotent
            self.exit_json(
                changed=False,
                cluster_state=cluster_state,
                msg=f"Already joined to cluster '{current_domain}'"
            )

        # If we're in check mode, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Would join cluster at '{primary_node_url}'"
            )

        # Build join parameters
        join_params = {
            'secondaryNodeIpAddress': secondary_node_ip_address,
            'primaryNodeUrl': primary_node_url,
            'primaryNodeUsername': primary_node_username,
            'primaryNodePassword': primary_node_password
        }

        if primary_node_ip_address:
            join_params['primaryNodeIpAddress'] = primary_node_ip_address

        if ignore_certificate_errors:
            join_params['ignoreCertificateErrors'] = 'true'

        if primary_node_totp:
            join_params['primaryNodeTotp'] = primary_node_totp

        # Join the cluster
        join_data = self.request('/api/admin/cluster/initJoin', params=join_params, method='POST')
        if join_data.get('status') != 'ok':
            error_msg = join_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to join cluster: {error_msg}",
                api_response=join_data
            )

        cluster_state = join_data.get('response', {})
        self.exit_json(
            changed=True,
            cluster_state=cluster_state,
            msg="Successfully joined cluster"
        )


if __name__ == '__main__':
    module = InitJoinClusterModule()
    module.run()
