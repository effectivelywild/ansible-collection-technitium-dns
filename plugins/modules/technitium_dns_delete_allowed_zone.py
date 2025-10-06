#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_allowed_zone
short_description: Delete a domain from the allowed zones in Technitium DNS server
version_added: "0.7.0"
description:
    - Delete a domain name from the allowed zones.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_allowed_zones
    description: List allowed zones
  - module: effectivelywild.technitium_dns.technitium_dns_add_allowed_zone
    description: Add a domain to the allowed zones
  - module: effectivelywild.technitium_dns.technitium_dns_flush_allowed_zone
    description: Flush all allowed zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_blocked_zone
    description: Delete a domain from the blocked zones
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
    domain:
        description:
            - The domain name to delete from the allowed zones
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Delete a domain from allowed zones
  technitium_dns_delete_allowed_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "example.com"

- name: Remove multiple domains from allowed zones
  technitium_dns_delete_allowed_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "{{ item }}"
  loop:
    - "old1.com"
    - "old2.com"
    - "old3.com"
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
    description: Whether the module deleted the domain from allowed zones
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
    sample: "Domain 'example.com' deleted from allowed zones."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteAllowedZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        domain=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        domain = self.params['domain']

        # Check if the domain exists in allowed zones
        domain_exists, list_response = self.check_allowed_blocked_zone_exists(domain, zone_type='allowed')

        # If domain doesn't exist, return unchanged (idempotent delete)
        if not domain_exists:
            self.exit_json(
                changed=False,
                msg=f"Domain '{domain}' does not exist in allowed zones.",
                api_response=list_response
            )

        # Handle check mode
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Domain '{domain}' would be deleted from allowed zones (check mode).",
                api_response={'status': 'ok', 'response': {}}
            )

        # Delete the domain from allowed zones via the Technitium API
        delete_params = {'domain': domain}
        data = self.request('/api/allowed/delete', params=delete_params, method='POST')
        self.validate_api_response(data)

        # Return success
        self.exit_json(
            changed=True,
            msg=f"Domain '{domain}' deleted from allowed zones.",
            api_response=data
        )


if __name__ == '__main__':
    module = DeleteAllowedZoneModule()
    module.run()
