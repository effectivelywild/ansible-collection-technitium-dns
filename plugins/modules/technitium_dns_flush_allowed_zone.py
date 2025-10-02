#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_flush_allowed_zone
short_description: Flush all allowed zones in Technitium DNS server
version_added: "0.6.0"
description:
    - Flush the allowed zone to clear all records.
    - This removes all domains from the allowed zones list.
    - Use with caution as this operation cannot be undone.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_allowed_zones
    description: List allowed zones from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_add_allowed_zone
    description: Add a domain to the allowed zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_allowed_zone
    description: Delete a domain from the allowed zones
  - module: effectivelywild.technitium_dns.technitium_dns_flush_blocked_zone
    description: Flush all blocked zones
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
- name: Flush all allowed zones
  technitium_dns_flush_allowed_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"

- name: Flush allowed zones with confirmation
  block:
    - name: Confirm flush operation
      pause:
        prompt: "Are you sure you want to flush all allowed zones? (yes/no)"
      register: confirm

    - name: Flush if confirmed
      technitium_dns_flush_allowed_zone:
        api_url: "http://localhost"
        api_token: "myapitoken"
      when: confirm.user_input | bool
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
    description: Whether the module flushed the allowed zones
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
    sample: "All allowed zones flushed."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class FlushAllowedZoneModule(TechnitiumModule):
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
                msg="All allowed zones would be flushed (check mode).",
                api_response={'status': 'ok', 'check_mode': True}
            )

        # Flush all allowed zones via the Technitium API
        data = self.request('/api/allowed/flush', method='POST')
        self.validate_api_response(data)

        # Return success
        self.exit_json(
            changed=True,
            msg="All allowed zones flushed.",
            api_response=data
        )


if __name__ == '__main__':
    module = FlushAllowedZoneModule()
    module.run()
