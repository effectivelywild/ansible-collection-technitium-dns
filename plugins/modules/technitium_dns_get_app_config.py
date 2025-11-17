#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_get_app_config
short_description: Get app configuration
version_added: "0.9.0"
description:
    - Retrieve the DNS application config from the C(dnsApp.config) file in the application folder.
    - Returns the configuration data or null if no configuration exists.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_set_app_config
    description: Set app configuration
  - module: effectivelywild.technitium_dns.technitium_dns_list_apps
    description: List all installed apps
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
            - The node domain name for which this API call is intended
            - When unspecified, the current node is used
            - This parameter can be used only when Clustering is initialized
        required: false
        type: str
    name:
        description:
            - The name of the app to retrieve the config from
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Get configuration for Split Horizon app
  technitium_dns_get_app_config:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Split Horizon"
  register: result

- debug:
    var: result.config

- name: Check if app has configuration
  technitium_dns_get_app_config:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Geo Continent"
  register: app_config

- name: Display config if it exists
  debug:
    msg: "App configuration: {{ app_config.config }}"

- name: Get app config on a specific cluster node
  technitium_dns_get_app_config:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Split Horizon"
    node: "node1.cluster.example.com"
  register: result
'''

RETURN = r'''
config:
    description: Configuration data from the dnsApp.config file, or null if no configuration exists
    type: str
    returned: always
    sample: '{"networks": ["192.168.1.0/24"], "servers": ["10.0.0.1"]}'
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
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class GetAppConfigModule(TechnitiumModule):
    argument_spec = dict(
        node=dict(type='str', required=False),
        name=dict(type='str', required=True),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        name = self.params['name']

        # Get the app config from the API
        params = {
            'name': name
        }
        if self.params.get('node'):
            params['node'] = self.params['node']

        data = self.request('/api/apps/config/get', params=params)
        self.validate_api_response(data)

        config = data.get('response', {}).get('config')
        self.exit_json(changed=False, config=config)


if __name__ == '__main__':
    module = GetAppConfigModule()
    module.run()
