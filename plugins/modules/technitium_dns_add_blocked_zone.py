#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_add_blocked_zone
short_description: Add a domain to the blocked zones in Technitium DNS server
version_added: "0.7.0"
description:
    - Add a domain name to the blocked zones.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_blocked_zones
    description: List blocked zones from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_delete_blocked_zone
    description: Delete a domain from the blocked zones
  - module: effectivelywild.technitium_dns.technitium_dns_flush_blocked_zone
    description: Flush all blocked zones
  - module: effectivelywild.technitium_dns.technitium_dns_add_allowed_zone
    description: Add a domain to the allowed zones
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
            - The domain name to add to the blocked zones
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Add a domain to blocked zones
  technitium_dns_add_blocked_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "ads.example.com"

- name: Block multiple ad domains
  technitium_dns_add_blocked_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "{{ item }}"
  loop:
    - "ads.tracker.com"
    - "analytics.example.com"
    - "telemetry.badsite.com"
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
    description: Whether the module added the domain to blocked zones
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
    sample: "Domain 'ads.example.com' added to blocked zones."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class AddBlockedZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        domain=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        domain = self.params['domain']

        # Check if the domain already exists in blocked zones
        list_params = {'domain': domain}
        list_data = self.request('/api/blocked/list', params=list_params)
        self.validate_api_response(list_data)

        response = list_data.get('response', {})
        zones = response.get('zones', [])
        records = response.get('records', [])

        # Check if domain exists in zones list or records
        domain_exists = False

        # Check in zones list
        if domain in zones:
            domain_exists = True

        # Check in records list (domain might be in records as a zone)
        for record in records:
            if record.get('name') == domain:
                domain_exists = True
                break

        # If domain already exists, return unchanged
        if domain_exists:
            self.exit_json(
                changed=False,
                msg=f"Domain '{domain}' already exists in blocked zones.",
                api_response={'status': 'ok'}
            )

        # Handle check mode
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Domain '{domain}' would be added to blocked zones (check mode).",
                api_response={'status': 'ok', 'check_mode': True}
            )

        # Add the domain to blocked zones via the Technitium API
        add_params = {'domain': domain}
        data = self.request('/api/blocked/add', params=add_params, method='POST')
        self.validate_api_response(data)

        # Return success
        self.exit_json(
            changed=True,
            msg=f"Domain '{domain}' added to blocked zones.",
            api_response=data
        )


if __name__ == '__main__':
    module = AddBlockedZoneModule()
    module.run()
