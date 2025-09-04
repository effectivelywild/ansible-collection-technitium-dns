#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_sign_zone
short_description: Sign a DNS zone
version_added: "0.0.1"
author: Frank Muise (@effectivelywild)
requirements:
  - requests
description:
  - Signs a primary DNS zone using the Technitium DNS API.
  - Will not update DNSSEC properties once intially signed.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_unsign_zone
    description: Unsign a zone with DNSSEC
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_nsec
    description: Convert signed zone from NSEC to NSEC3
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_nsec3
    description: Convert signed zone from NSEC3 to NSEC
  - module: effectivelywild.technitium_dns.technitium_dns_get_dnssec_properties
    description: Get dnssec properties for a zone
options:
  algorithm:
    description:
      - The algorithm to use for signing
    required: true
    type: str
    choices: [RSA, ECDSA, EDDSA]
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
  curve:
    description:
      - The name of the curve to be used when using V(ECDSA) or V(EDDSA) O(algorithm)
      - Use V(P256) or  V(P384) for V(ECDSA) O(algorithm)
      - Use V(ED25519) or V(ED448) for V(EDDSA) O(algorithm)
    required: false
    type: str
    choices: [P256, P384, ED25519, ED448]
  dnsKeyTtl:
    description:
      - TTL for DNSKEY records
    default: 86400
    required: false
    type: int
  hashAlgorithm:
    description:
      - The hash algorithm to be used when using V(RSA) O(algorithm)
    required: false
    type: str
    choices: [MD5, SHA1, SHA256, SHA512]
  iterations:
    description:
      - NSEC3 iterations
    default: 0
    required: false
    type: int
  kskKeySize:
    description:
      - The size of the Key Signing Key (KSK) in bits to be used when using V(RSA) O(algorithm)
    required: false
    type: int
  nxProof:
    description:
      - Proof of non-existence
    required: false
    default: NSEC
    type: str
    choices: [NSEC, NSEC3]
  pemKskPrivateKey:
    description:
      - PEM private key for KSK
      - When this parameter is specified, the private key specified is used instead of automatically generating it.
    required: false
    type: str
  pemZskPrivateKey:
    description:
      - PEM private key for ZSK
      - When this parameter is specified, the private key specified is used instead of automatically generating it.
    required: false
    type: str
  saltLength:
    description:
      - NSEC3 salt length
    default: 0
    required: false
    type: int
  validate_certs:
    description:
      - Whether to validate SSL certificates when making API requests.
    required: false
    type: bool
    default: true
  zone:
    description:
      - The name of the primary zone to sign
    required: true
    type: str
  zskKeySize:
    description:
      - The size of the Zone Signing Key (ZSK) in bits to be used when using V(RSA) O(algorithm)
    required: false
    type: int
  zskRolloverDays:
    description:
      - ZSK rollover frequency in days
    default: 30
    required: false
    type: int
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

- name: Sign a zone with RSA algorithm and custom key sizes
  technitium_dns_sign_zone:
    api_url: "http://localhost:5380"
    api_token: "{{ technitium_api_token }}"
    zone: "secure.example.com"
    algorithm: "RSA"
    hashAlgorithm: "SHA256"
    kskKeySize: 2048
    zskKeySize: 1024
    dnsKeyTtl: 3600
    zskRolloverDays: 90
    nxProof: "NSEC"

- name: Sign a zone with EDDSA and custom NSEC3 parameters
  technitium_dns_sign_zone:
    api_url: "http://localhost:5380"
    api_token: "{{ technitium_api_token }}"
    zone: "modern.example.com"
    algorithm: "EDDSA"
    curve: "ED25519"
    dnsKeyTtl: 172800
    zskRolloverDays: 60
    nxProof: "NSEC3"
    iterations: 10
    saltLength: 8
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The API response payload (empty dict for successful sign operations)
            type: dict
            returned: always
            sample: "{}"
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
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
    sample: "Zone 'demo.test.local' signed."
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
