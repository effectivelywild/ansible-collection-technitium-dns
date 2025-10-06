#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_check_for_update
short_description: Check for available updates
version_added: "0.5.0"
description:
    - Check if a software update is available.
    - Returns update information including current version, available version, and download links.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_sessions
    description: List active user sessions from Technitium DNS server
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
- name: Check for updates on Technitium DNS server
  technitium_dns_check_for_update:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: update_result

- debug:
    var: update_result.update_info

- name: Display update availability
  debug:
    msg: "Update available: {{ update_result.update_info.updateAvailable }}"
  when: update_result.update_info.updateAvailable is defined

- name: Show current and available versions
  debug:
    msg: "Current: {{ update_result.update_info.currentVersion }}, Available: {{ update_result.update_info.updateVersion }}"
  when: update_result.update_info.updateAvailable
'''

RETURN = r'''
update_info:
    description: Update information from the Technitium DNS server
    type: dict
    returned: always
    contains:
        updateAvailable:
            description: Whether an update is available
            type: bool
            returned: always
            sample: true
        updateVersion:
            description: Version number of the available update
            type: str
            returned: always
            sample: "9.0"
        currentVersion:
            description: Current version of the DNS server
            type: str
            returned: always
            sample: "8.1.4"
        updateTitle:
            description: Title of the update notification
            type: str
            returned: when update is available
            sample: "New Update Available!"
        updateMessage:
            description: Detailed message about the update
            type: str
            returned: when update is available
            sample: "Follow the instructions from the link below to update the DNS server to the latest version."
        downloadLink:
            description: Direct download link for the update
            type: str
            returned: when update is available and link is provided
            sample: "https://download.technitium.com/dns/DnsServerSetup.zip"
        instructionsLink:
            description: Link to update instructions
            type: str
            returned: when update is available
            sample: "https://blog.technitium.com/2017/11/running-dns-server-on-ubuntu-linux.html"
        changeLogLink:
            description: Link to the change log
            type: str
            returned: when update is available
            sample: "https://github.com/TechnitiumSoftware/DnsServer/blob/master/CHANGELOG.md"
changed:
    description: Whether the module made changes (always false for check operations)
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


class CheckForUpdateModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )

    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        # Check for updates using the API
        data = self.request('/api/user/checkForUpdate')
        self.validate_api_response(data)

        update_info = data.get('response', {})
        self.exit_json(changed=False, update_info=update_info)


if __name__ == '__main__':
    module = CheckForUpdateModule()
    module.run()
