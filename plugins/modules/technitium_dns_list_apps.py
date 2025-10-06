#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_apps
short_description: List all installed apps
version_added: "0.9.0"
description:
    - Retrieve a list of all installed apps.
    - If the DNS server has Internet access and can retrieve data from DNS App Store, the API will also return if a store app has updates available.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_store_apps
    description: List all available apps from the DNS App Store
  - module: effectivelywild.technitium_dns.technitium_dns_download_and_install_app
    description: Download and install an app from a URL
  - module: effectivelywild.technitium_dns.technitium_dns_uninstall_app
    description: Uninstall an app from the DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_get_app_config
    description: Get app configuration
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
- name: List all installed apps from Technitium DNS
  technitium_dns_list_apps:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.apps
'''

RETURN = r'''
apps:
    description: List of installed DNS apps from the Technitium DNS server
    type: list
    returned: always
    elements: dict
    contains:
        name:
            description: Name of the app
            type: str
            returned: always
            sample: "Block Page"
        version:
            description: Version of the installed app
            type: str
            returned: always
            sample: "1.0"
        dnsApps:
            description: List of DNS application components
            type: list
            returned: always
            elements: dict
            contains:
                classPath:
                    description: Class path of the DNS app component
                    type: str
                    returned: always
                    sample: "BlockPageWebServer.App"
                description:
                    description: Description of the DNS app component
                    type: str
                    returned: always
                    sample: "Serves a block page from a built-in web server"
                isAppRecordRequestHandler:
                    description: Whether this is an APP record request handler
                    type: bool
                    returned: always
                    sample: false
                isRequestController:
                    description: Whether this is a request controller
                    type: bool
                    returned: always
                    sample: false
                isAuthoritativeRequestHandler:
                    description: Whether this is an authoritative request handler
                    type: bool
                    returned: always
                    sample: false
                isRequestBlockingHandler:
                    description: Whether this is a request blocking handler
                    type: bool
                    returned: always
                    sample: false
                isQueryLogger:
                    description: Whether this is a query logger
                    type: bool
                    returned: always
                    sample: false
                isPostProcessor:
                    description: Whether this is a post processor
                    type: bool
                    returned: always
                    sample: false
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


class ListAppsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Fetch all apps from the API
        data = self.request('/api/apps/list')
        self.validate_api_response(data)

        apps = data.get('response', {}).get('apps', [])
        self.exit_json(changed=False, apps=apps)


if __name__ == '__main__':
    module = ListAppsModule()
    module.run()
