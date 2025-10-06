#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_uninstall_app
short_description: Uninstall an app
version_added: "0.9.0"
description:
    - Uninstall an app from the DNS server.
    - This does not remove any APP records that were using this DNS application.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_apps
    description: List all installed apps
  - module: effectivelywild.technitium_dns.technitium_dns_download_and_install_app
    description: Download and install an app
  - module: effectivelywild.technitium_dns.technitium_dns_download_and_update_app
    description: Download and update an app
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
            - The name of the app to uninstall
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Uninstall Wild IP app
  technitium_dns_uninstall_app:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Wild IP"
  register: result
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
    sample: "App 'Wild IP' uninstalled successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class UninstallAppModule(TechnitiumModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        name = self.params['name']

        # Uninstall the app
        params = {
            'name': name
        }
        data = self.request('/api/apps/uninstall', params=params)
        self.validate_api_response(data)

        self.exit_json(
            changed=True,
            msg=f"App '{name}' uninstalled successfully"
        )


if __name__ == '__main__':
    module = UninstallAppModule()
    module.run()
