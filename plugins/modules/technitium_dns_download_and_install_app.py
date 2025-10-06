#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_download_and_install_app
short_description: Download and install an app on Technitium DNS server
version_added: "0.9.0"
description:
    - Download an app zip file from a given URL and install it on the DNS server.
    - The URL must start with C(https://).
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_apps
    description: List all installed apps
  - module: effectivelywild.technitium_dns.technitium_dns_list_store_apps
    description: List all available apps from the DNS App Store
  - module: effectivelywild.technitium_dns.technitium_dns_download_and_update_app
    description: Download and update an existing app
  - module: effectivelywild.technitium_dns.technitium_dns_uninstall_app
    description: Uninstall an app from the DNS server
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
            - The name of the app to install
        required: true
        type: str
    url:
        description:
            - The URL of the app zip file
            - URL must start with C(https://)
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Download and install Wild IP app
  technitium_dns_download_and_install_app:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Wild IP"
    url: "https://download.technitium.com/dns/apps/WildIpApp.zip"
  register: result

- debug:
    var: result.installed_app

- name: Install app from DNS App Store
  technitium_dns_download_and_install_app:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "Geo Continent"
    url: "https://download.technitium.com/dns/apps/GeoContinentApp.zip"
'''

RETURN = r'''
installed_app:
    description: Information about the installed app
    type: dict
    returned: success
    contains:
        name:
            description: Name of the installed app
            type: str
            returned: always
            sample: "Wild IP"
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
                    sample: "WildIp.App"
                description:
                    description: Description of the DNS app component
                    type: str
                    returned: always
                    sample: "Returns the IP address that was embedded in the subdomain name"
                isAppRecordRequestHandler:
                    description: Whether this is an APP record request handler
                    type: bool
                    returned: always
                    sample: true
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
    sample: "App 'Wild IP' installed successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DownloadAndInstallAppModule(TechnitiumModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        url=dict(type='str', required=True),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        name = self.params['name']
        url = self.params['url']

        # Validate URL starts with https://
        if not url.startswith('https://'):
            self.fail_json(msg="URL must start with 'https://'")

        # Check if app already exists
        app_exists, existing_app = self.check_app_exists(name)

        if app_exists:
            # App already installed, return success with changed=False
            self.exit_json(
                changed=False,
                installed_app=existing_app,
                msg=f"App '{name}' is already installed"
            )

        # Download and install the app
        params = {
            'name': name,
            'url': url
        }
        data = self.request('/api/apps/downloadAndInstall', params=params)
        self.validate_api_response(data)

        installed_app = data.get('response', {}).get('installedApp', {})
        self.exit_json(
            changed=True,
            installed_app=installed_app,
            msg=f"App '{name}' installed successfully"
        )


if __name__ == '__main__':
    module = DownloadAndInstallAppModule()
    module.run()
