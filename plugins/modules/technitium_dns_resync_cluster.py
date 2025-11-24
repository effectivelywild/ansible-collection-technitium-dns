#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_resync_cluster
short_description: Manually trigger cluster configuration resync
version_added: "1.0.0"
description:
    - Manually trigger a complete configuration resync on a Secondary node.
    - When triggered, the Secondary node will sync the complete configuration from the Primary node.
    - This can only be called at a Secondary node.
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
    - The resync is triggered asynchronously and may take time to complete.
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
'''

EXAMPLES = r'''
- name: Manually resync cluster configuration
  effectivelywild.technitium_dns.technitium_dns_resync_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Resync specific node
  effectivelywild.technitium_dns.technitium_dns_resync_cluster:
    api_url: "http://localhost"
    api_token: "myapitoken"
    node: "server2.example.com"
'''

RETURN = r'''
changed:
    description: Whether the module made changes (always true when resync is triggered)
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
    sample: "Cluster resync triggered successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class ResyncClusterModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        node = params.get('node')

        # Get and validate cluster state
        cluster_initialized, cluster_state = self.get_cluster_state(node=node)
        self.require_cluster_initialized(
            cluster_initialized,
            cluster_state,
            fail_message="Not part of any cluster"
        )

        # Validate this is a Secondary node
        self.validate_cluster_node_type(
            cluster_state,
            'Secondary',
            "This is not a Secondary node. Resync can only be triggered on Secondary nodes."
        )

        # If we're in check mode, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="Would trigger cluster resync"
            )

        # Build resync parameters
        resync_params = self.build_cluster_params(node=node)

        # Trigger resync
        resync_data = self.request('/api/admin/cluster/secondary/resync', params=resync_params, method='POST')
        if resync_data.get('status') != 'ok':
            error_msg = resync_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to trigger cluster resync: {error_msg}",
                api_response=resync_data
            )

        self.exit_json(
            changed=True,
            msg="Cluster resync triggered successfully"
        )


if __name__ == '__main__':
    module = ResyncClusterModule()
    module.run()
