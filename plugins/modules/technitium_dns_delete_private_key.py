#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_private_key
short_description: Delete DNSSEC private key from a zone
version_added: "0.3.0"
author: Frank Muise (@effectivelywild)
description:
  - Deletes a private key that has state set as Generated from a DNSSEC signed zone.
  - Private keys with any other state cannot be deleted.
  - The zone must already be signed with DNSSEC.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_add_private_key
    description: Add DNSSEC private key to a zone
  - module: effectivelywild.technitium_dns.technitium_dns_update_private_key
    description: Update DNSSEC private key in a zone
  - module: effectivelywild.technitium_dns.technitium_dns_get_dnssec_properties
    description: Get DNSSEC properties for a zone
options:
  api_port:
    description:
      - Port for the Technitium DNS API. Defaults to 5380
    required: false
    type: int
    default: 5380
  api_token:
    description:
      - API token for authentication
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
  zone:
    description:
      - The name of the primary zone to delete the private key from
    required: true
    type: str
  key_tag:
    description:
      - The key tag of the private key to be deleted
    required: true
    type: int
'''

EXAMPLES = r'''
- name: Delete private key with key tag 12345
  technitium_dns_delete_private_key:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_tag: 12345

- name: Delete private key from HTTPS API
  technitium_dns_delete_private_key:
    api_url: "https://dns.example.com"
    api_token: "myapitoken"
    zone: "example.com"
    key_tag: 54321
    validate_certs: true
'''

RETURN = r'''
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
    description: Human readable message describing the result
    type: str
    returned: always
    sample: "Private key with tag 12345 deleted successfully from zone 'example.com'"
api_response:
    description: Full API response from Technitium DNS server
    type: dict
    returned: always
    sample: {
        "status": "ok"
    }
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeletePrivateKeyModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        key_tag=dict(type='int', required=True, no_log=False),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        zone = self.params['zone']
        key_tag = self.params['key_tag']

        # Get DNSSEC properties to validate zone is signed
        dnssec_props = self.get_dnssec_properties(zone)
        dnssec_status = dnssec_props.get('dnssecStatus', '').lower()

        if dnssec_status == 'unsigned':
            self.fail_json(msg=f"Zone '{zone}' is not signed with DNSSEC. Cannot delete private key from unsigned zone.")

        if dnssec_status not in ['signed', 'signedwithnsec', 'signedwithnsec3']:
            self.fail_json(msg=f"Zone '{zone}' has unexpected DNSSEC status: {dnssec_status}")

        # Verify the key exists and is in Generated state before attempting deletion
        private_keys = dnssec_props.get('dnssecPrivateKeys', [])
        key_found = False
        key_state = None

        for key in private_keys:
            if key.get('keyTag') == key_tag:
                key_found = True
                key_state = key.get('state', '').lower()
                break

        if not key_found:
            self.fail_json(msg=f"Private key with tag '{key_tag}' not found in zone '{zone}'")

        if key_state != 'generated':
            self.fail_json(msg=f"Private key with tag '{key_tag}' has state '{key_state}'. Only keys with state 'Generated' can be deleted.")

        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Private key with tag {key_tag} would be deleted from zone '{zone}' (check mode)",
                api_response={}
            )

        # Build API parameters
        query = {
            'zone': zone,
            'keyTag': key_tag
        }

        # Delete private key via API
        data = self.request('/api/zones/dnssec/properties/deletePrivateKey', params=query, method='POST')
        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        result_msg = f"Private key with tag {key_tag} deleted successfully from zone '{zone}'"

        self.exit_json(
            changed=True,
            msg=result_msg,
            api_response=data
        )


if __name__ == '__main__':
    module = DeletePrivateKeyModule()
    module.run()
