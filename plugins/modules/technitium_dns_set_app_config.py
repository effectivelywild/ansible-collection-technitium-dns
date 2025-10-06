#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_set_app_config
short_description: Set app configuration on Technitium DNS server
version_added: "0.9.0"
description:
    - Saves the provided DNS application config into the C(dnsApp.config) file in the application folder.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_app_config
    description: Get app configuration
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
    name:
        description:
            - The name of the app to set the config for
        required: true
        type: str
    config:
        description:
            - The configuration data to save
            - Can be a string, dict, or list that will be converted to the appropriate format
        required: true
        type: raw
'''

EXAMPLES = r'''
- name: Set configuration for Split Horizon app
  technitium_dns_set_app_config:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Split Horizon"
    config: '{"networks": ["192.168.1.0/24"], "servers": ["10.0.0.1"]}'
  register: result

- name: Set configuration using a dict
  technitium_dns_set_app_config:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Geo Continent"
    config:
      maxmind_db_path: "/opt/maxmind/GeoLite2-Country.mmdb"
      default_continent: "NA"

- name: Set Query Logs configuration
  technitium_dns_set_app_config:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Query Logs (Sqlite)"
    config:
      enableLogging: true
      maxLogDays: 30
      maxLogRecords: 10000
'''

RETURN = r'''
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
    description: Human-readable message about the operation
    type: str
    returned: always
    sample: "Configuration for app 'Split Horizon' set successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule
import json


class SetAppConfigModule(TechnitiumModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        config=dict(type='raw', required=True),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        name = self.params['name']
        config = self.params['config']

        # Convert config to string if it's not already
        if isinstance(config, (dict, list)):
            config_str = json.dumps(config)
        else:
            config_str = str(config)

        # Set the app config via the API
        params = {
            'name': name,
            'config': config_str
        }
        data = self.request('/api/apps/config/set', params=params, method='POST')
        self.validate_api_response(data)

        self.exit_json(
            changed=True,
            msg=f"Configuration for app '{name}' set successfully"
        )


if __name__ == '__main__':
    module = SetAppConfigModule()
    module.run()
