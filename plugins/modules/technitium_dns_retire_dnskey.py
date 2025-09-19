#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_retire_dnskey
short_description: Retire a DNSKEY for a DNSSEC-signed zone
version_added: "0.4.0"
author: Frank Muise (@effectivelywild)
description:
  - Retires the specified private key and its associated DNSKEY record and removes it safely.
  - To retire an existing DNSKEY, there must be at least one active key available.
  - The zone must already be signed with DNSSEC.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_dnssec_properties
    description: Get DNSSEC properties for a zone
  - module: effectivelywild.technitium_dns.technitium_dns_update_dnskey_ttl
    description: Update DNSKEY TTL for a zone
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
      - The name of the primary zone to retire DNSKEY from
    required: true
    type: str
  key_tag:
    description:
      - The key tag of the private key to retire
    required: true
    type: int
'''

EXAMPLES = r'''
- name: Retire DNSKEY with key tag 12345
  technitium_dns_retire_dnskey:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_tag: 12345

- name: Retire DNSKEY with check mode
  technitium_dns_retire_dnskey:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_tag: 54321
  check_mode: true
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
    sample: "DNSKEY with tag 12345 retired successfully for zone 'example.com'"
api_response:
    description: Full API response from Technitium DNS server
    type: dict
    returned: always
    sample: {
        "status": "ok"
    }
retired_key_tag:
    description: The key tag of the retired DNSKEY
    type: int
    returned: success
    sample: 12345
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class RetireDnskeyModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        key_tag=dict(type='int', required=True, no_log=False),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def validate_key_tag(self):
        """Validate key_tag parameter is a positive integer"""
        key_tag = self.params['key_tag']
        if key_tag <= 0:
            self.fail_json(msg=f"key_tag must be a positive integer, got {key_tag}")

    def find_key_by_tag(self, dnssec_props, key_tag):
        """Find a key by its tag in the DNSSEC properties"""
        private_keys = dnssec_props.get('dnssecPrivateKeys', [])
        for key in private_keys:
            if key.get('keyTag') == key_tag:
                return key
        return None

    def check_retirement_requirements(self, dnssec_props, key_tag):
        """Check that there is at least one active key available after retirement"""
        private_keys = dnssec_props.get('dnssecPrivateKeys', [])
        if not private_keys:
            self.fail_json(msg="No DNSSEC private keys found in zone")

        target_key = self.find_key_by_tag(dnssec_props, key_tag)
        if not target_key:
            self.fail_json(msg=f"DNSKEY with tag {key_tag} not found in zone")

        # Check if the key is already retired
        key_state = target_key.get('state', '').lower()
        if key_state == 'retired':
            return False  # Key already retired, no change needed

        # Count active keys of the same type after retirement
        key_type = target_key.get('keyType')
        active_keys_same_type = [
            key for key in private_keys
            if key.get('keyType') == key_type
            and key.get('state', '').lower() == 'active'
            and key.get('keyTag') != key_tag
        ]

        if not active_keys_same_type:
            self.fail_json(
                msg=f"Cannot retire DNSKEY with tag {key_tag}: "
                    f"no other active {key_type} keys available. "
                    f"At least one active key of the same type must remain."
            )

        return True

    def run(self):
        zone = self.params['zone']
        key_tag = self.params['key_tag']

        # Validate key_tag parameter
        self.validate_key_tag()

        # Get DNSSEC properties to validate zone is signed
        dnssec_props = self.get_dnssec_properties(zone)
        dnssec_status = dnssec_props.get('dnssecStatus', '').lower()

        if dnssec_status == 'unsigned':
            self.fail_json(msg=f"Zone '{zone}' is not signed with DNSSEC. Cannot retire DNSKEY in unsigned zone.")

        if dnssec_status not in ['signed', 'signedwithnsec', 'signedwithnsec3']:
            self.fail_json(msg=f"Zone '{zone}' has unexpected DNSSEC status: {dnssec_status}")

        # Check retirement requirements and if change is needed
        needs_change = self.check_retirement_requirements(dnssec_props, key_tag)

        if not needs_change:
            self.exit_json(
                changed=False,
                msg=f"DNSKEY with tag {key_tag} for zone '{zone}' is already retired",
                api_response={'status': 'ok', 'msg': 'No changes needed'},
                retired_key_tag=key_tag
            )

        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"DNSKEY with tag {key_tag} for zone '{zone}' would be retired (check mode)",
                api_response={},
                retired_key_tag=key_tag
            )

        # Retire DNSKEY via API
        query = {
            'zone': zone,
            'keyTag': key_tag
        }

        data = self.request('/api/zones/dnssec/properties/retireDnsKey', params=query, method='POST')
        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        result_msg = f"DNSKEY with tag {key_tag} retired successfully for zone '{zone}'"

        exit_kwargs = {
            'changed': True,
            'msg': result_msg,
            'api_response': data,
            'retired_key_tag': key_tag
        }

        self.exit_json(**exit_kwargs)


if __name__ == '__main__':
    module = RetireDnskeyModule()
    module.run()