#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_flush_blocked_zone
short_description: Flush all blocked zones in Technitium DNS server
version_added: "0.7.0"
description:
    - Flush the blocked zone to clear all records.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_blocked_zones
    description: List blocked zones from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_add_blocked_zone
    description: Add a domain to the blocked zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_blocked_zone
    description: Delete a domain from the blocked zones
  - module: effectivelywild.technitium_dns.technitium_dns_flush_allowed_zone
    description: Flush all allowed zones
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
            - Whether to validate SSL certificates when making API requests
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: Flush all blocked zones
  technitium_dns_flush_blocked_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The core data payload from the API
            type: dict
            returned: always
            sample: {}
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module flushed the blocked zones
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the result
    type: str
    returned: always
    sample: "All blocked zones flushed."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class FlushBlockedZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        # Handle check mode
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="All blocked zones would be flushed (check mode).",
                api_response={'status': 'ok', 'response': {}}
            )

        # Flush all blocked zones via the Technitium API
        data = self.request('/api/blocked/flush', method='POST')
        self.validate_api_response(data)

        # Return success
        self.exit_json(
            changed=True,
            msg="All blocked zones flushed.",
            api_response=data
        )


if __name__ == '__main__':
    module = FlushBlockedZoneModule()
    module.run()
