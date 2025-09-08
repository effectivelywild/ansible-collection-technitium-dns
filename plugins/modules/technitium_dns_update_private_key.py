#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_update_private_key
short_description: Update DNSSEC private key properties
version_added: "0.3.0"
author: Frank Muise (@effectivelywild)
description:
  - Updates the properties of an existing DNSSEC private key in a zone.
  - The zone must already be signed with DNSSEC and the key must exist.
  - Currently supports updating the rollover days property.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_add_private_key
    description: Add DNSSEC private key to a zone
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
      - The name of the primary zone containing the private key
    required: true
    type: str
  key_tag:
    description:
      - The key tag of the private key to be updated
    required: true
    type: int
  rollover_days:
    description:
      - The frequency in days that the DNS server must automatically rollover the private key
      - Valid range is 0-365 days where 0 disables rollover
    required: true
    type: int
'''

EXAMPLES = r'''
- name: Update private key rollover to 90 days
  technitium_dns_update_private_key:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_tag: 1234
    rollover_days: 90

- name: Disable automatic rollover for a key
  technitium_dns_update_private_key:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_tag: 5678
    rollover_days: 0
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
    sample: "Private key 1234 updated successfully in zone 'example.com'"
api_response:
    description: Full API response from Technitium DNS server
    type: dict
    returned: always
    sample: {
        "status": "ok"
    }
key_info:
    description: Information about the updated private key
    type: dict
    returned: success
    sample: {
        "keyTag": 1234,
        "rolloverDays": 90
    }
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class UpdatePrivateKeyModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        key_tag=dict(type='int', required=True, no_log=False),
        rollover_days=dict(type='int', required=True),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def validate_rollover_days(self):
        """Validate rollover days parameter is within valid range"""
        rollover_days = self.params['rollover_days']
        if not (0 <= rollover_days <= 365):
            self.fail_json(msg=f"rollover_days must be between 0-365, got {rollover_days}")

    def find_key_in_zone(self, zone, key_tag):
        """Find and validate that the specified key exists in the zone"""
        dnssec_props = self.get_dnssec_properties(zone)

        # Check if zone has private keys
        private_keys = dnssec_props.get('dnssecPrivateKeys', [])
        if not private_keys:
            return None

        # Find the specific key by key tag
        for key in private_keys:
            if key.get('keyTag') == key_tag:
                return key

        return None

    def run(self):
        zone = self.params['zone']
        key_tag = self.params['key_tag']
        rollover_days = self.params['rollover_days']

        # Validate rollover days parameter
        self.validate_rollover_days()

        # Get DNSSEC properties to validate zone is signed
        dnssec_props = self.get_dnssec_properties(zone)
        dnssec_status = dnssec_props.get('dnssecStatus', '').lower()

        if dnssec_status == 'unsigned':
            self.fail_json(msg=f"Zone '{zone}' is not signed with DNSSEC. Cannot update private keys in unsigned zone.")

        if dnssec_status not in ['signed', 'signedwithnsec', 'signedwithnsec3']:
            self.fail_json(msg=f"Zone '{zone}' has unexpected DNSSEC status: {dnssec_status}")

        # Find the specified key in the zone
        key_info = self.find_key_in_zone(zone, key_tag)
        if not key_info:
            self.fail_json(msg=f"Private key with tag {key_tag} not found in zone '{zone}'")

        # Check if rollover days are already set as requested
        current_rollover_days = key_info.get('rolloverDays', 0)

        if current_rollover_days == rollover_days:
            self.exit_json(
                changed=False,
                msg=f"Private key {key_tag} in zone '{zone}' already has rollover_days={rollover_days}",
                api_response={'status': 'ok', 'msg': 'No changes needed'},
                key_info={
                    'keyTag': key_tag,
                    'rolloverDays': rollover_days
                }
            )

        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Private key {key_tag} in zone '{zone}' would be updated to rollover_days={rollover_days} (check mode)",
                api_response={},
                key_info={
                    'keyTag': key_tag,
                    'rolloverDays': rollover_days
                }
            )

        # Update private key properties via API
        query = {
            'zone': zone,
            'keyTag': key_tag,
            'rolloverDays': rollover_days
        }

        data = self.request('/api/zones/dnssec/properties/updatePrivateKey', params=query, method='POST')
        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        result_msg = f"Private key {key_tag} updated successfully in zone '{zone}' (rollover_days={rollover_days})"

        exit_kwargs = {
            'changed': True,
            'msg': result_msg,
            'api_response': data,
            'key_info': {
                'keyTag': key_tag,
                'rolloverDays': rollover_days
            }
        }

        self.exit_json(**exit_kwargs)


if __name__ == '__main__':
    module = UpdatePrivateKeyModule()
    module.run()
