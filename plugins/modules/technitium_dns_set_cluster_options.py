#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_set_cluster_options
short_description: Set DNS cluster options
version_added: "1.0.0"
description:
    - Configure cluster options to be used by all Secondary nodes.
    - This call can only be made at the Primary node.
    - Options control heartbeat and configuration sync intervals.
author:
    - Frank Muise (@effectivelywild)
requirements:
    - Technitium DNS Server v14.0 or later
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_cluster_state
    description: Get cluster state and current options
  - module: effectivelywild.technitium_dns.technitium_dns_init_cluster
    description: Initialize a new cluster
notes:
    - This operation requires Administration Modify permission.
    - This can only be run on the Primary node.
    - All intervals are in seconds.
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
    heartbeat_refresh_interval_seconds:
        description:
            - The interval in seconds for refreshing the state of all nodes in the cluster.
            - Valid range is 10-300 seconds.
        required: false
        type: int
    heartbeat_retry_interval_seconds:
        description:
            - The interval in seconds for retrying state refresh for all nodes in case of failure.
            - Valid range is 10-300 seconds.
        required: false
        type: int
    config_refresh_interval_seconds:
        description:
            - The interval in seconds for refreshing configuration from the Primary node.
            - Valid range is 30-3600 seconds.
        required: false
        type: int
    config_retry_interval_seconds:
        description:
            - The interval in seconds for retrying configuration refresh in case of failure.
            - Valid range is 30-3600 seconds.
        required: false
        type: int
'''

EXAMPLES = r'''
- name: Set cluster heartbeat intervals
  effectivelywild.technitium_dns.technitium_dns_set_cluster_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    heartbeat_refresh_interval_seconds: 60
    heartbeat_retry_interval_seconds: 15
  register: result

- name: Set cluster config sync intervals
  effectivelywild.technitium_dns.technitium_dns_set_cluster_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    config_refresh_interval_seconds: 1800
    config_retry_interval_seconds: 120

- name: Set all cluster options
  effectivelywild.technitium_dns.technitium_dns_set_cluster_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    heartbeat_refresh_interval_seconds: 45
    heartbeat_retry_interval_seconds: 10
    config_refresh_interval_seconds: 600
    config_retry_interval_seconds: 90
'''

RETURN = r'''
cluster_state:
    description: Complete cluster state after setting options
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
            sample: 45
        heartbeatRetryIntervalSeconds:
            description: Interval in seconds for heartbeat retry
            type: int
            returned: always
            sample: 10
        configRefreshIntervalSeconds:
            description: Interval in seconds for config refresh
            type: int
            returned: always
            sample: 600
        configRetryIntervalSeconds:
            description: Interval in seconds for config retry
            type: int
            returned: always
            sample: 90
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
    sample: "Cluster options updated successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class SetClusterOptionsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False),
        heartbeat_refresh_interval_seconds=dict(type='int', required=False),
        heartbeat_retry_interval_seconds=dict(type='int', required=False),
        config_refresh_interval_seconds=dict(type='int', required=False),
        config_retry_interval_seconds=dict(type='int', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True,
        required_one_of=[
            ['heartbeat_refresh_interval_seconds', 'heartbeat_retry_interval_seconds',
             'config_refresh_interval_seconds', 'config_retry_interval_seconds']
        ]
    )

    def run(self):
        params = self.params
        node = params.get('node')
        heartbeat_refresh = params.get('heartbeat_refresh_interval_seconds')
        heartbeat_retry = params.get('heartbeat_retry_interval_seconds')
        config_refresh = params.get('config_refresh_interval_seconds')
        config_retry = params.get('config_retry_interval_seconds')

        # Validate ranges
        if heartbeat_refresh is not None and not (10 <= heartbeat_refresh <= 300):
            self.fail_json(msg="heartbeat_refresh_interval_seconds must be between 10 and 300")
        if heartbeat_retry is not None and not (10 <= heartbeat_retry <= 300):
            self.fail_json(msg="heartbeat_retry_interval_seconds must be between 10 and 300")
        if config_refresh is not None and not (30 <= config_refresh <= 3600):
            self.fail_json(msg="config_refresh_interval_seconds must be between 30 and 3600")
        if config_retry is not None and not (30 <= config_retry <= 3600):
            self.fail_json(msg="config_retry_interval_seconds must be between 30 and 3600")

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
            self.fail_json(msg="Cluster is not initialized")

        # Check if this is a Primary node
        current_nodes = cluster_state.get('clusterNodes', [])
        self_node = next((n for n in current_nodes if n.get('state') == 'Self'), None)

        if self_node and self_node.get('type') != 'Primary':
            self.fail_json(
                msg="This is not a Primary node. Cluster options can only be set on the Primary node.",
                cluster_state=cluster_state
            )

        # Check if values would actually change
        current_heartbeat_refresh = cluster_state.get('heartbeatRefreshIntervalSeconds')
        current_heartbeat_retry = cluster_state.get('heartbeatRetryIntervalSeconds')
        current_config_refresh = cluster_state.get('configRefreshIntervalSeconds')
        current_config_retry = cluster_state.get('configRetryIntervalSeconds')

        changes_needed = False
        if heartbeat_refresh is not None and heartbeat_refresh != current_heartbeat_refresh:
            changes_needed = True
        if heartbeat_retry is not None and heartbeat_retry != current_heartbeat_retry:
            changes_needed = True
        if config_refresh is not None and config_refresh != current_config_refresh:
            changes_needed = True
        if config_retry is not None and config_retry != current_config_retry:
            changes_needed = True

        if not changes_needed:
            self.exit_json(
                changed=False,
                cluster_state=cluster_state,
                msg="Cluster options already match desired state"
            )

        # If we're in check mode, report that we would make changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="Would update cluster options"
            )

        # Build options parameters
        options_params = {}
        if node:
            options_params['node'] = node
        if heartbeat_refresh is not None:
            options_params['heartbeatRefreshIntervalSeconds'] = heartbeat_refresh
        if heartbeat_retry is not None:
            options_params['heartbeatRetryIntervalSeconds'] = heartbeat_retry
        if config_refresh is not None:
            options_params['configRefreshIntervalSeconds'] = config_refresh
        if config_retry is not None:
            options_params['configRetryIntervalSeconds'] = config_retry

        # Set cluster options
        options_data = self.request('/api/admin/cluster/primary/setOptions', params=options_params, method='POST')
        if options_data.get('status') != 'ok':
            error_msg = options_data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Failed to set cluster options: {error_msg}",
                api_response=options_data
            )

        cluster_state = options_data.get('response', {})
        self.exit_json(
            changed=True,
            cluster_state=cluster_state,
            msg="Cluster options updated successfully"
        )


if __name__ == '__main__':
    module = SetClusterOptionsModule()
    module.run()
