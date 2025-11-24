#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_update_dnskey_ttl
short_description: Update DNSKEY TTL for a DNSSEC-signed zone
version_added: "0.3.0"
author: Frank Muise (@effectivelywild)
description:
  - Updates the TTL value for DNSKEY resource record set in a DNSSEC-signed zone.
  - The value can be updated only when all the DNSKEYs are in ready or active state.
  - The zone must already be signed with DNSSEC.
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
  node:
    description:
      - The node domain name for which this API call is intended
      - When unspecified, the current node is used
      - This parameter can be used only when Clustering is initialized
    required: false
    type: str
  zone:
    description:
      - The name of the primary zone to update DNSKEY TTL for
    required: true
    type: str
  ttl:
    description:
      - The TTL value for the DNSKEY resource record set in seconds
    required: true
    type: int
'''

EXAMPLES = r'''
- name: Update DNSKEY TTL to 86400 seconds (24 hours)
  technitium_dns_update_dnskey_ttl:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    ttl: 86400

- name: Update DNSKEY TTL to 3600 seconds (1 hour)
  technitium_dns_update_dnskey_ttl:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    ttl: 3600

- name: Update DNSKEY TTL on a specific cluster node
  technitium_dns_update_dnskey_ttl:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    ttl: 86400
    node: "node1.cluster.example.com"
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
    sample: "DNSKEY TTL updated successfully for zone 'example.com' to 86400 seconds"
api_response:
    description: Full API response from Technitium DNS server
    type: dict
    returned: always
    sample: {
        "status": "ok"
    }
dnskey_ttl:
    description: The updated DNSKEY TTL value
    type: int
    returned: success
    sample: 86400
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class UpdateDnskeyTtlModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False),
        zone=dict(type='str', required=True),
        ttl=dict(type='int', required=True),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def validate_ttl(self):
        """Validate TTL parameter is a positive integer"""
        ttl = self.params['ttl']
        if ttl <= 0:
            self.fail_json(msg=f"ttl must be a positive integer, got {ttl}")

    def check_dnskey_states(self, dnssec_props):
        """Check that all DNSKEYs are in ready or active state"""
        private_keys = dnssec_props.get('dnssecPrivateKeys', [])
        if not private_keys:
            self.fail_json(msg="No DNSSEC private keys found in zone")

        for key in private_keys:
            state = key.get('state', '').lower()
            if state not in ['ready', 'active']:
                key_tag = key.get('keyTag', 'unknown')
                self.fail_json(
                    msg=f"DNSKEY with tag {key_tag} is in state '{state}'. "
                        f"All DNSKEYs must be in 'ready' or 'active' state to update TTL."
                )

    def run(self):
        zone = self.params['zone']
        ttl = self.params['ttl']

        # Validate TTL parameter
        self.validate_ttl()

        # Get DNSSEC properties to validate zone is signed
        dnssec_props = self.get_dnssec_properties(zone)
        dnssec_status = dnssec_props.get('dnssecStatus', '').lower()

        if dnssec_status == 'unsigned':
            self.fail_json(msg=f"Zone '{zone}' is not signed with DNSSEC. Cannot update DNSKEY TTL in unsigned zone.")

        if dnssec_status not in ['signed', 'signedwithnsec', 'signedwithnsec3']:
            self.fail_json(msg=f"Zone '{zone}' has unexpected DNSSEC status: {dnssec_status}")

        # Check that all DNSKEYs are in ready or active state
        self.check_dnskey_states(dnssec_props)

        # Check if TTL is already set as requested
        current_ttl = dnssec_props.get('dnsKeyTtl', 0)

        if current_ttl == ttl:
            self.exit_json(
                changed=False,
                msg=f"DNSKEY TTL for zone '{zone}' is already set to {ttl} seconds",
                api_response={'status': 'ok', 'msg': 'No changes needed'},
                dnskey_ttl=ttl
            )

        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"DNSKEY TTL for zone '{zone}' would be updated to {ttl} seconds (check mode)",
                api_response={},
                dnskey_ttl=ttl
            )

        # Update DNSKEY TTL via API
        query = {
            'zone': zone,
            'ttl': ttl
        }
        if self.params.get('node'):
            query['node'] = self.params['node']

        data = self.request('/api/zones/dnssec/properties/updateDnsKeyTtl', params=query, method='POST')
        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        result_msg = f"DNSKEY TTL updated successfully for zone '{zone}' to {ttl} seconds"

        exit_kwargs = {
            'changed': True,
            'msg': result_msg,
            'api_response': data,
            'dnskey_ttl': ttl
        }

        self.exit_json(**exit_kwargs)


if __name__ == '__main__':
    module = UpdateDnskeyTtlModule()
    module.run()
