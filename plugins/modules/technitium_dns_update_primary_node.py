#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_update_primary_node
short_description: Update Primary node details on a Secondary node
version_added: "1.0.0"
description:
    - Update the Primary node's URL and IP address details on this Secondary node.
    - This is useful when the Primary node's IP address or URL has changed while the Secondary node was offline.
    - This call can only be made at a Secondary node.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_init_join_cluster
    description: Join a cluster as Secondary
  - module: effectivelywild.technitium_dns.technitium_dns_get_cluster_state
    description: Get cluster state information
notes:
    - This operation requires Administration Modify permission.
    - This can only be run on a Secondary node.
    - Use this when the Primary node's connection details have changed.
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
    primary_node_url:
        description:
            - The HTTPS URL of the Primary node.
        required: true
        type: str
    primary_node_ip_address:
        description:
            - The IP address of the Primary node.
            - Optional parameter for updating the Primary node's IP address.
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Update Primary node URL on Secondary
  effectivelywild.technitium_dns.technitium_dns_update_primary_node:
    api_url: "http://localhost"
    api_token: "myapitoken"
    primary_node_url: "https://dns-primary.example.com:5380/"
  register: result

- name: Update Primary node URL and IP address
  effectivelywild.technitium_dns.technitium_dns_update_primary_node:
    api_url: "http://localhost"
    api_token: "myapitoken"
    primary_node_url: "https://dns-primary.example.com:5380/"
    primary_node_ip_address: "192.168.1.100"
  register: result

- name: Display cluster state after update
  debug:
    var: result.cluster_state
'''

RETURN = r'''
cluster_state:
    description: Complete cluster state after updating Primary node details
    type: dict
    returned: always
    contains:
        clusterInitialized:
            description: Whether the cluster is initialized
            type: bool
            returned: always
            sample: true
        dnsServerDomain:
            description: The DNS server domain name (this Secondary node)
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
        clusterNodes:
            description: List of nodes in the cluster
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
    sample: "Primary node details updated successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class UpdatePrimaryNodeModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False),
        primary_node_url=dict(type='str', required=True),
        primary_node_ip_address=dict(type='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        node = params.get('node')
        primary_node_url = params['primary_node_url']
        primary_node_ip_address = params.get('primary_node_ip_address')

        # First check if cluster is initialized
        state_params = {}
        if node:
            state_params['node'] = node

        state_data = self.request('/api/admin/cluster/state', params=state_params)
        if state_data.get('status') != 'ok':
            error_msg = state_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check cluster state: {error_msg}", api_response=state_data)

        cluster_state = state_data.get('response', {})
        cluster_initialized = cluster_state.get('clusterInitialized', False)

        if not cluster_initialized:
            self.fail_json(msg="Not part of any cluster")

        # Check if this is a Secondary node
        current_nodes = cluster_state.get('clusterNodes', [])
        self_node = next((n for n in current_nodes if n.get('state') == 'Self'), None)

        if not self_node:
            self.fail_json(msg="Could not identify current node", cluster_state=cluster_state)

        if self_node.get('type') == 'Primary':
            self.fail_json(
                msg="This is a Primary node. This operation can only be performed on Secondary nodes.",
                cluster_state=cluster_state
            )

        if self_node.get('type') != 'Secondary':
            self.fail_json(
                msg=f"This node type is '{self_node.get('type')}', expected 'Secondary'",
                cluster_state=cluster_state
            )

        # Check if the Primary node details need updating
        primary_node = next((n for n in current_nodes if n.get('type') == 'Primary'), None)

        if primary_node:
            current_url = primary_node.get('url', '')
            current_ip = primary_node.get('ipAddress', '')

            # Normalize URLs for comparison (remove trailing slash)
            current_url_normalized = current_url.rstrip('/')
            new_url_normalized = primary_node_url.rstrip('/')

            url_changed = current_url_normalized != new_url_normalized
            ip_changed = primary_node_ip_address and current_ip != primary_node_ip_address

            if not url_changed and not ip_changed:
                self.exit_json(
                    changed=False,
                    cluster_state=cluster_state,
                    msg="Primary node details already match desired state"
                )

        # If we're in check mode, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="Would update Primary node details"
            )

        # Build update parameters
        update_params = {
            'primaryNodeUrl': primary_node_url
        }
        if node:
            update_params['node'] = node
        if primary_node_ip_address:
            update_params['primaryNodeIpAddress'] = primary_node_ip_address

        # Update Primary node details
        update_data = self.request('/api/admin/cluster/secondary/updatePrimary', params=update_params, method='POST')
        if update_data.get('status') != 'ok':
            error_msg = update_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to update Primary node details: {error_msg}",
                api_response=update_data
            )

        cluster_state = update_data.get('response', {})
        self.exit_json(
            changed=True,
            cluster_state=cluster_state,
            msg="Primary node details updated successfully"
        )


if __name__ == '__main__':
    module = UpdatePrimaryNodeModule()
    module.run()
