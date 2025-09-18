#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_rollover_dnskey
short_description: Rollover DNSKEY for a DNSSEC-signed zone
version_added: "0.4.0"
author: Frank Muise (@effectivelywild)
description:
  - Generates and publishes a new private key for the given key that has to be rolled over.
  - The old private key and its associated DNSKEY record will be automatically retired and removed safely once the new key is active.
  - The zone must already be signed with DNSSEC.
  - This module is not idempotent as each rollover generates a new key.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_dnssec_properties
    description: Get DNSSEC properties for a zone
  - module: effectivelywild.technitium_dns.technitium_dns_update_private_key
    description: Update DNSSEC private key properties
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
      - The name of the primary zone to rollover DNSKEY for
    required: true
    type: str
  key_tag:
    description:
      - The key tag of the private key to rollover
    required: true
    type: int
'''

EXAMPLES = r'''
- name: Rollover DNSKEY with tag 12345
  technitium_dns_rollover_dnskey:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_tag: 12345

- name: Rollover DNSKEY with custom API port
  technitium_dns_rollover_dnskey:
    api_url: "http://localhost"
    api_port: 5380
    api_token: "myapitoken"
    zone: "example.com"
    key_tag: 67890
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
    sample: "DNSKEY rollover initiated for key tag 12345 in zone 'example.com'"
api_response:
    description: Full API response from Technitium DNS server
    type: dict
    returned: always
    sample: {
        "status": "ok"
    }
key_tag:
    description: The key tag that was rolled over
    type: int
    returned: success
    sample: 12345
zone:
    description: The zone where the rollover was performed
    type: str
    returned: success
    sample: "example.com"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class RolloverDnskeyModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        key_tag=dict(type='int', required=True, no_log=False),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def find_key_in_zone(self, zone, key_tag):
        """Find and validate that the specified key exists in the zone"""
        dnssec_props = self.get_dnssec_properties(zone)

        # Check if zone has private keys
        private_keys = dnssec_props.get('dnssecPrivateKeys', [])
        if not private_keys:
            return None, None

        # Find the specific key by key tag
        for key in private_keys:
            if key.get('keyTag') == key_tag:
                return key, dnssec_props

        return None, dnssec_props

    def run(self):
        zone = self.params['zone']
        key_tag = self.params['key_tag']

        # Get DNSSEC properties to validate zone is signed
        dnssec_props = self.get_dnssec_properties(zone)
        dnssec_status = dnssec_props.get('dnssecStatus', '').lower()

        if dnssec_status == 'unsigned':
            self.fail_json(msg=f"Zone '{zone}' is not signed with DNSSEC. Cannot rollover DNSKEY in unsigned zone.")

        if dnssec_status not in ['signed', 'signedwithnsec', 'signedwithnsec3']:
            self.fail_json(msg=f"Zone '{zone}' has unexpected DNSSEC status: {dnssec_status}")

        # Find the specified key in the zone
        key_info, _ = self.find_key_in_zone(zone, key_tag)
        if not key_info:
            self.fail_json(msg=f"DNSKEY with tag {key_tag} not found in zone '{zone}'")

        # Check key state - we don't need to be as restrictive as the TTL update
        key_state = key_info.get('state', '').lower()
        is_retiring = key_info.get('isRetiring', False)

        if key_state in ['retired', 'revoked']:
            self.fail_json(msg=f"DNSKEY with tag {key_tag} is in '{key_state}' state and cannot be rolled over")
        elif key_state == 'retiring' or is_retiring:
            self.fail_json(msg=f"DNSKEY with tag {key_tag} is already set to retire and cannot be rolled over again")

        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"DNSKEY rollover would be initiated for key tag {key_tag} in zone '{zone}' (check mode)",
                api_response={},
                key_tag=key_tag,
                zone=zone
            )

        # Rollover DNSKEY via API
        query = {
            'zone': zone,
            'keyTag': key_tag
        }

        data = self.request('/api/zones/dnssec/properties/rolloverDnsKey', params=query, method='POST')
        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        result_msg = f"DNSKEY rollover initiated for key tag {key_tag} in zone '{zone}'"

        exit_kwargs = {
            'changed': True,
            'msg': result_msg,
            'api_response': data,
            'key_tag': key_tag,
            'zone': zone
        }

        self.exit_json(**exit_kwargs)


if __name__ == '__main__':
    module = RolloverDnskeyModule()
    module.run()