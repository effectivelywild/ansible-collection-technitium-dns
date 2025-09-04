#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_sign_zone
short_description: Sign a primary DNS zone with DNSSEC using Technitium DNS API
version_added: "1.0.0"
description:
  - Signs a primary DNS zone with DNSSEC using the Technitium DNS API.
  - Will not update DNSSEC properties once intially signed.
  - Idempotency achieved by checking if the zone is already signed, not that all parameters match.
options:
  api_url:
    description:
      - Base URL for the Technitium DNS API (e.g., http://localhost:5380)
    required: true
    type: str
  api_token:
    description:
      - API token for authentication
    required: true
    type: str
  validate_certs:
    description:
      - Whether to validate SSL certificates when making API requests.
      - Set to false to disable SSL certificate validation (not recommended for production).
    required: false
    type: bool
    default: true
  zone:
    description:
      - The name of the primary zone to sign
    required: true
    type: str
  algorithm:
    description:
      - The algorithm to use for signing (RSA, ECDSA, EDDSA)
    required: true
    type: str
    choices: [RSA, ECDSA, EDDSA]
  pemKskPrivateKey:
    description:
      - PEM private key for KSK (optional)
    required: false
    type: str
  pemZskPrivateKey:
    description:
      - PEM private key for ZSK (optional)
    required: false
    type: str
  hashAlgorithm:
    description:
      - Hash algorithm for RSA (optional)
    required: false
    type: str
    choices: [MD5, SHA1, SHA256, SHA512]
  kskKeySize:
    description:
      - KSK key size for RSA (optional)
    required: false
    type: int
  zskKeySize:
    description:
      - ZSK key size for RSA (optional)
    required: false
    type: int
  curve:
    description:
      - Curve for ECDSA/EDDSA (optional)
    required: false
    type: str
    choices: [P256, P384, ED25519, ED448]
  dnsKeyTtl:
    description:
      - TTL for DNSKEY records (optional)
    required: false
    type: int
  zskRolloverDays:
    description:
      - ZSK rollover frequency in days (optional)
    required: false
    type: int
  nxProof:
    description:
      - Proof of non-existence (NSEC, NSEC3)
    required: false
    type: str
    choices: [NSEC, NSEC3]
  iterations:
    description:
      - NSEC3 iterations (optional)
    required: false
    type: int
  saltLength:
    description:
      - NSEC3 salt length (optional)
    required: false
    type: int
requirements:
  - requests
author:
  - Your Name (@yourgithub)
'''

EXAMPLES = r'''
- name: Sign a primary zone with ECDSA
  technitium_dns_sign_zone:
    api_url: "http://localhost:5380"
    api_token: "{{ technitium_api_token }}"
    zone: "example.com"
    algorithm: "ECDSA"
    curve: "P256"
    dnsKeyTtl: 86400
    zskRolloverDays: 30
    nxProof: "NSEC3"
    iterations: 0
    saltLength: 0
'''

RETURN = r'''
status:
  description: API response status
  returned: always
  type: str
  sample: ok
'''

# Refactored to use TechnitiumModule base class
class SignZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        algorithm=dict(type='str', required=True, choices=['RSA', 'ECDSA', 'EDDSA']),
        pemKskPrivateKey=dict(type='str', required=False, default=None, no_log=True),
        pemZskPrivateKey=dict(type='str', required=False, default=None, no_log=True),
        hashAlgorithm=dict(type='str', required=False, choices=['MD5', 'SHA1', 'SHA256', 'SHA512']),
        kskKeySize=dict(type='int', required=False),
        zskKeySize=dict(type='int', required=False),
        curve=dict(type='str', required=False, choices=['P256', 'P384', 'ED25519', 'ED448']),
        dnsKeyTtl=dict(type='int', required=False),
        zskRolloverDays=dict(type='int', required=False),
        nxProof=dict(type='str', required=False, choices=['NSEC', 'NSEC3']),
        iterations=dict(type='int', required=False),
        saltLength=dict(type='int', required=False),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
      zone = self.params['zone']
      algorithm = self.params['algorithm']
      # Build query params for API
      query = {'zone': zone, 'algorithm': algorithm}

      # Build query with optional parameters  
      for key in [
        'pemKskPrivateKey', 'pemZskPrivateKey', 'hashAlgorithm', 'kskKeySize', 'zskKeySize',
        'curve', 'dnsKeyTtl', 'zskRolloverDays', 'nxProof', 'iterations', 'saltLength']:
        value = self.params.get(key)
        if value is not None:
          query[key] = value

      # Fetch current zone DNSSEC status (this also validates zone exists)
      dnssec_status, zone_info = self.get_dnssec_status(zone)

      if dnssec_status != 'unsigned':
        self.exit_json(changed=False, msg=f"Zone '{zone}' is already signed (status: {zone_info.get('dnssecStatus')}).", api_response={'status': 'ok', 'msg': f"Zone '{zone}' is already signed."})

      if self.check_mode:
        self.exit_json(changed=True, msg="Zone would be signed (check mode)", api_response={})

      data = self.request('/api/zones/dnssec/sign', params=query, method='POST')
      status = data.get('status')
      error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"
      already_signed_msg = 'the zone is already signed'

      if status != 'ok':
        if already_signed_msg in str(error_msg).lower():
          self.exit_json(changed=False, msg=f"Zone '{zone}' is already signed.", api_response={'status': 'ok', 'msg': f"Zone '{zone}' is already signed."})
        self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
      self.exit_json(changed=True, msg=f"Zone '{zone}' signed.", api_response=data)

def main():
    module = SignZoneModule()
    module()

if __name__ == '__main__':
    main()
