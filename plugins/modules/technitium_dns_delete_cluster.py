#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_cluster
short_description: Delete DNS cluster configuration
version_added: "1.0.0"
description:
    - Remove all cluster configuration from the Primary node.
    - There will be no data loss except for the cluster configuration.
    - You will need to re-initialize the cluster again to use clustering features.
    - This call can only be made at the Primary node.
    - You can only delete the cluster when there are no Secondary nodes, unless force_delete is used.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_init_cluster
    description: Initialize a new cluster
  - module: effectivelywild.technitium_dns.technitium_dns_get_cluster_state
    description: Get cluster state information
notes:
    - This operation requires Administration Delete permission.
    - Use force_delete with caution as it will orphan Secondary nodes.
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
    force_delete:
        description:
            - Set to true to delete the cluster even when Secondary nodes exist, orphaning them.
            - Use this only when Secondary nodes are unreachable/decommissioned.
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Delete cluster configuration
  effectivelywild.technitium_dns.technitium_dns_delete_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Display result
  debug:
    var: result.cluster_state

- name: Force delete cluster with orphaned secondaries
  effectivelywild.technitium_dns.technitium_dns_delete_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
    force_delete: true
  register: result
'''

RETURN = r'''
cluster_state:
    description: Cluster state after deletion
    type: dict
    returned: always
    contains:
        clusterInitialized:
            description: Whether the cluster is initialized (should be false after deletion)
            type: bool
            returned: always
            sample: false
        dnsServerDomain:
            description: The DNS server domain name
            type: str
            returned: always
            sample: "server1"
        version:
            description: Technitium DNS Server version
            type: str
            returned: always
            sample: "14.0"
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
    sample: "Cluster deleted successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteClusterModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        force_delete=dict(type='bool', required=False, default=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        force_delete = params.get('force_delete', False)

        # First check if cluster is initialized
        state_data = self.request('/api/admin/cluster/state')
        if state_data.get('status') != 'ok':
            error_msg = state_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check cluster state: {error_msg}", api_response=state_data)

        cluster_state = state_data.get('response', {})
        cluster_initialized = cluster_state.get('clusterInitialized', False)

        # If cluster is not initialized, nothing to do
        if not cluster_initialized:
            self.exit_json(
                changed=False,
                cluster_state=cluster_state,
                msg="Cluster is not initialized"
            )

        # If we're in check mode, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="Would delete cluster configuration"
            )

        # Delete the cluster
        delete_params = {}
        if force_delete:
            delete_params['forceDelete'] = 'true'

        delete_data = self.request('/api/admin/cluster/primary/delete', params=delete_params, method='POST')
        if delete_data.get('status') != 'ok':
            error_msg = delete_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to delete cluster: {error_msg}",
                api_response=delete_data
            )

        cluster_state = delete_data.get('response', {})
        self.exit_json(
            changed=True,
            cluster_state=cluster_state,
            msg="Cluster deleted successfully"
        )


if __name__ == '__main__':
    module = DeleteClusterModule()
    module.run()
