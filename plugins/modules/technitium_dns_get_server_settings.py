#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_get_server_settings
short_description: Get DNS server settings
version_added: "1.1.0"
description:
    - Retrieve all DNS server settings from Technitium DNS.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_set_server_settings
    description: Update DNS server settings
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
- name: Get all DNS server settings
  effectivelywild.technitium_dns.technitium_dns_get_server_settings:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- name: Show resolver configuration
  debug:
    msg: "Resolvers: {{ result.settings.resolverConcurrency }} concurrent, timeout {{ result.settings.resolverTimeout }} ms"
'''

RETURN = r'''
settings:
    description: Complete DNS server settings returned by the API
    type: dict
    returned: always
changed:
    description: Whether the module made changes (always false)
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


class GetServerSettingsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
    )

    def run(self):
        settings = self.get_server_settings()
        self.exit_json(changed=False, settings=settings)


if __name__ == '__main__':
    module = GetServerSettingsModule()
    module.run()
