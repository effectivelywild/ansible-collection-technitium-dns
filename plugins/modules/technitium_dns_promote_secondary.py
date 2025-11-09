#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_promote_secondary
short_description: Promote a Secondary node to Primary
version_added: "1.0.0"
description:
    - Promote this Secondary node to become the Primary node in the cluster.
    - This process will resync complete configuration from the current Primary node.
    - Then it will delete the current Primary from the cluster.
    - Finally it will upgrade this Secondary node to become the new Primary.
    - This call can only be made at a Secondary node.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_init_cluster
    description: Initialize a new cluster
  - module: effectivelywild.technitium_dns.technitium_dns_init_join_cluster
    description: Join a cluster as Secondary
  - module: effectivelywild.technitium_dns.technitium_dns_get_cluster_state
    description: Get cluster state information
notes:
    - This operation requires Administration Delete permission.
    - The process may take a while depending on config size and number of local zones.
    - Use force_delete_primary only when the current Primary is unreachable/decommissioned.
    - This can only be run on a Secondary node.
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
    force_delete_primary:
        description:
            - Set to true to delete the current Primary node without resyncing config and without informing it.
            - Use this only when the Primary node is unreachable/decommissioned.
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Promote this Secondary node to Primary
  effectivelywild.technitium_dns.technitium_dns_promote_secondary:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Display new cluster state
  debug:
    var: result.cluster_state

- name: Force promote when current Primary is unreachable
  effectivelywild.technitium_dns.technitium_dns_promote_secondary:
    api_url: "http://localhost"
    api_token: "myapitoken"
    force_delete_primary: true
  register: result
'''

RETURN = r'''
cluster_state:
    description: Complete cluster state after promotion
    type: dict
    returned: always
    contains:
        clusterInitialized:
            description: Whether the cluster is initialized
            type: bool
            returned: always
            sample: true
        dnsServerDomain:
            description: The DNS server domain name (this node)
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
            description: List of nodes in the cluster (this node should now be type Primary)
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
                type:
                    description: Node type (should be Primary for this node)
                    type: str
                    sample: "Primary"
                state:
                    description: Node state
                    type: str
                    sample: "Self"
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
    sample: "Successfully promoted to Primary node"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class PromoteSecondaryModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False),
        force_delete_primary=dict(type='bool', required=False, default=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        node = params.get('node')
        force_delete_primary = params.get('force_delete_primary', False)

        # Get and validate cluster state
        cluster_initialized, cluster_state = self.get_cluster_state(node=node)
        self.require_cluster_initialized(
            cluster_initialized,
            cluster_state,
            fail_message="Not part of any cluster"
        )

        # Check if this is a Secondary node
        self_node = self.get_self_node(cluster_state)

        if not self_node:
            self.fail_json(msg="Could not identify current node", cluster_state=cluster_state)

        if self_node.get('type') == 'Primary':
            self.exit_json(
                changed=False,
                cluster_state=cluster_state,
                msg="This node is already the Primary node"
            )

        if self_node.get('type') != 'Secondary':
            self.fail_json(
                msg=f"This node type is '{self_node.get('type')}', expected 'Secondary'",
                cluster_state=cluster_state
            )

        # If we're in check mode, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="Would promote this Secondary node to Primary"
            )

        # Build promote parameters
        promote_params = self.build_cluster_params(node=node)
        if force_delete_primary:
            promote_params['forceDeletePrimary'] = 'true'

        # Promote to primary
        promote_data = self.request('/api/admin/cluster/secondary/promote', params=promote_params, method='POST')
        if promote_data.get('status') != 'ok':
            error_msg = promote_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to promote to Primary: {error_msg}",
                api_response=promote_data
            )

        cluster_state = promote_data.get('response', {})
        self.exit_json(
            changed=True,
            cluster_state=cluster_state,
            msg="Successfully promoted to Primary node"
        )


if __name__ == '__main__':
    module = PromoteSecondaryModule()
    module.run()
