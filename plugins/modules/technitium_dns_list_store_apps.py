#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_store_apps
short_description: List all available apps from Technitium DNS App Store
version_added: "0.9.0"
description:
    - Retrieve a list of all available apps from the DNS App Store.
    - Indicates which apps are already installed and if updates are available.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_apps
    description: List all installed apps from the DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_download_and_install_app
    description: Download and install an app from a URL
  - module: effectivelywild.technitium_dns.technitium_dns_download_and_update_app
    description: Download and update an app from a URL
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
'''

EXAMPLES = r'''
- name: List all available apps from DNS App Store
  technitium_dns_list_store_apps:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.store_apps

- name: Find apps that have updates available
  technitium_dns_list_store_apps:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: store_apps_result

- name: Show apps with updates
  debug:
    msg: "App {{ item.name }} has update from {{ item.installedVersion }} to {{ item.version }}"
  loop: "{{ store_apps_result.store_apps | selectattr('updateAvailable', 'equalto', true) | list }}"
  when: store_apps_result.store_apps | selectattr('updateAvailable', 'equalto', true) | list | length > 0
'''

RETURN = r'''
store_apps:
    description: List of available apps from the DNS App Store
    type: list
    returned: always
    elements: dict
    contains:
        name:
            description: Name of the app
            type: str
            returned: always
            sample: "Geo Continent"
        version:
            description: Latest version available in the store
            type: str
            returned: always
            sample: "1.1"
        description:
            description: Description of the app
            type: str
            returned: always
            sample: "Returns A or AAAA records based on client continent"
        url:
            description: Download URL for the app
            type: str
            returned: always
            sample: "https://download.technitium.com/dns/apps/GeoContinentApp.zip"
        size:
            description: Size of the app package
            type: str
            returned: always
            sample: "2.01 MB"
        installed:
            description: Whether the app is currently installed
            type: bool
            returned: always
            sample: false
        installedVersion:
            description: Currently installed version (only if installed=true)
            type: str
            returned: when installed
            sample: "1.0"
        updateAvailable:
            description: Whether an update is available (only if installed=true)
            type: bool
            returned: when installed
            sample: true
changed:
    description: Whether the module made changes (always false for list operations)
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


class ListStoreAppsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Fetch all store apps from the API
        data = self.request('/api/apps/listStoreApps')
        self.validate_api_response(data)

        store_apps = data.get('response', {}).get('storeApps', [])
        self.exit_json(changed=False, store_apps=store_apps)


if __name__ == '__main__':
    module = ListStoreAppsModule()
    module.run()
