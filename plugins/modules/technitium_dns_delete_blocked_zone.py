#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_blocked_zone
short_description: Delete a domain from the blocked zones in Technitium DNS server
version_added: "0.7.0"
description:
    - Delete a domain name from the blocked zones.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_blocked_zones
    description: List blocked zones from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_add_blocked_zone
    description: Add a domain to the blocked zones
  - module: effectivelywild.technitium_dns.technitium_dns_flush_blocked_zone
    description: Flush all blocked zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_allowed_zone
    description: Delete a domain from the allowed zones
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
            - The domain name to delete from the blocked zones
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Delete a domain from blocked zones
  technitium_dns_delete_blocked_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "ads.example.com"

- name: Unblock multiple domains
  technitium_dns_delete_blocked_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "{{ item }}"
  loop:
    - "ads.site1.com"
    - "tracker.site2.com"
    - "analytics.site3.com"
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
    description: Whether the module deleted the domain from blocked zones
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
    sample: "Domain 'ads.example.com' deleted from blocked zones."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteBlockedZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        domain=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        domain = self.params['domain']

        # Check if the domain exists in blocked zones
        domain_exists = self.check_allowed_blocked_zone_exists(domain, zone_type='blocked')

        # If domain doesn't exist, return unchanged (idempotent delete)
        if not domain_exists:
            self.exit_json(
                changed=False,
                msg=f"Domain '{domain}' does not exist in blocked zones.",
                api_response={'status': 'ok'}
            )

        # Handle check mode
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Domain '{domain}' would be deleted from blocked zones (check mode).",
                api_response={'status': 'ok', 'check_mode': True}
            )

        # Delete the domain from blocked zones via the Technitium API
        delete_params = {'domain': domain}
        data = self.request('/api/blocked/delete', params=delete_params, method='POST')
        self.validate_api_response(data)

        # Return success
        self.exit_json(
            changed=True,
            msg=f"Domain '{domain}' deleted from blocked zones.",
            api_response=data
        )


if __name__ == '__main__':
    module = DeleteBlockedZoneModule()
    module.run()
