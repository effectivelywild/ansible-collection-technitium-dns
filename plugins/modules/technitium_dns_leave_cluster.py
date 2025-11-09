#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_leave_cluster
short_description: Leave a DNS cluster
version_added: "1.0.0"
description:
    - Remove all cluster configuration from this Secondary node and leave the cluster gracefully.
    - There will be no data loss except for the cluster configuration.
    - This can only be called at a Secondary node.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_init_join_cluster
    description: Join a cluster as a Secondary node
  - module: effectivelywild.technitium_dns.technitium_dns_get_cluster_state
    description: Get cluster state information
notes:
    - This operation requires Administration Delete permission.
    - Use force_leave only when the Primary node is unreachable/decommissioned.
    - This can only be run on a Secondary node, not on the Primary node.
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
    force_leave:
        description:
            - Set to true to make this Secondary node leave the cluster without informing the Primary node.
            - Use this only when the Primary node is unreachable/decommissioned.
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Leave DNS cluster gracefully
  effectivelywild.technitium_dns.technitium_dns_leave_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Display result
  debug:
    var: result.cluster_state

- name: Force leave cluster when Primary is unreachable
  effectivelywild.technitium_dns.technitium_dns_leave_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
    force_leave: true
  register: result
'''

RETURN = r'''
cluster_state:
    description: Cluster state after leaving
    type: dict
    returned: always
    contains:
        clusterInitialized:
            description: Whether the cluster is initialized (should be false after leaving)
            type: bool
            returned: always
            sample: false
        dnsServerDomain:
            description: The DNS server domain name
            type: str
            returned: always
            sample: "server2"
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
    sample: "Successfully left cluster"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class LeaveClusterModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False),
        force_leave=dict(type='bool', required=False, default=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        node = params.get('node')
        force_leave = params.get('force_leave', False)

        # Get cluster state
        cluster_initialized, cluster_state = self.get_cluster_state(node=node)

        # If cluster is not initialized, nothing to do (idempotent)
        self.require_cluster_not_initialized(
            cluster_initialized,
            cluster_state,
            exit_message="Not part of any cluster"
        )

        # Validate this is a Secondary node
        self.validate_cluster_node_type(
            cluster_state,
            'Secondary',
            "This is a Primary node. Use technitium_dns_delete_cluster to delete the cluster instead."
        )

        # If we're in check mode, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="Would leave cluster"
            )

        # Build leave parameters
        leave_params = self.build_cluster_params(node=node)
        if force_leave:
            leave_params['forceLeave'] = 'true'

        # Leave the cluster
        leave_data = self.request('/api/admin/cluster/secondary/leave', params=leave_params, method='POST')
        if leave_data.get('status') != 'ok':
            error_msg = leave_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to leave cluster: {error_msg}",
                api_response=leave_data
            )

        cluster_state = leave_data.get('response', {})
        self.exit_json(
            changed=True,
            cluster_state=cluster_state,
            msg="Successfully left cluster"
        )


if __name__ == '__main__':
    module = LeaveClusterModule()
    module.run()
