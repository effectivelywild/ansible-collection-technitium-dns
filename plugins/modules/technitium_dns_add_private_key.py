#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_add_private_key
short_description: Add DNSSEC private key to a zone
version_added: "0.3.0"
author: Frank Muise (@effectivelywild)
description:
  - Adds a private key to be used for signing a zone with DNSSEC.
  - The zone must already be signed with DNSSEC.
  - Supports RSA, ECDSA, and EDDSA algorithms with appropriate parameters.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
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
  node:
    description:
      - The node domain name for which this API call is intended
      - When unspecified, the current node is used
      - This parameter can be used only when Clustering is initialized
    required: false
    type: str
  zone:
    description:
      - The name of the primary zone to add the private key to
    required: true
    type: str
  key_type:
    description:
      - The type of key for which the private key is to be generated
    required: true
    type: str
    choices: ['KeySigningKey', 'ZoneSigningKey']
  rollover_days:
    description:
      - The frequency in days that the DNS server must automatically rollover the private key
      - Valid range is 0-365 days where 0 disables rollover
      - Default value is 90 days for Zone Signing Key (ZSK) and 0 days for Key Signing Key (KSK)
    required: false
    type: int
  algorithm:
    description:
      - The algorithm to be used for signing
    required: true
    type: str
    choices: ['RSA', 'ECDSA', 'EDDSA']
  pem_private_key:
    description:
      - Specifies a user generated private key in PEM format to add
      - When not specified a private key will be automatically generated
      - Must match the specified algorithm and curve/key_size parameters
    required: false
    type: str
  hash_algorithm:
    description:
      - The hash algorithm to be used when using RSA algorithm
      - This parameter is required when using RSA algorithm
    required: false
    type: str
    choices: ['MD5', 'SHA1', 'SHA256', 'SHA512']
  key_size:
    description:
      - The size of the generated private key in bits to be used when using RSA algorithm
      - This parameter is required when using RSA algorithm
      - Common values are 2048, 3072, 4096
    required: false
    type: int
  curve:
    description:
      - The name of the curve to be used when using ECDSA or EDDSA algorithm
      - For ECDSA algorithm valid values are P256, P384
      - For EDDSA algorithm valid values are ED25519, ED448
      - This parameter is required when using ECDSA or EDDSA algorithm
    required: false
    type: str
    choices: ['P256', 'P384', 'ED25519', 'ED448']
'''

EXAMPLES = r'''
- name: Add RSA Key Signing Key with SHA256
  technitium_dns_add_private_key:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_type: "KeySigningKey"
    algorithm: "RSA"
    hash_algorithm: "SHA256"
    key_size: 2048

- name: Add ECDSA Zone Signing Key with P256 curve
  technitium_dns_add_private_key:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_type: "ZoneSigningKey"
    algorithm: "ECDSA"
    curve: "P256"
    rollover_days: 30

- name: Add EDDSA Key Signing Key with ED25519 curve
  technitium_dns_add_private_key:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_type: "KeySigningKey"
    algorithm: "EDDSA"
    curve: "ED25519"

- name: Add user-provided RSA private key
  technitium_dns_add_private_key:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_type: "KeySigningKey"
    algorithm: "RSA"
    hash_algorithm: "SHA256"
    key_size: 2048
    pem_private_key: |
      -----BEGIN RSA PRIVATE KEY-----
      MIIEpAIBAAKCAQEA...
      -----END RSA PRIVATE KEY-----

- name: Add Zone Signing Key with automatic rollover
  technitium_dns_add_private_key:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_type: "ZoneSigningKey"
    algorithm: "ECDSA"
    curve: "P384"
    rollover_days: 90

- name: Add EDDSA private key on a specific cluster node
  technitium_dns_add_private_key:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    key_type: "ZoneSigningKey"
    algorithm: "EDDSA"
    curve: "ED25519"
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
    sample: "Private key added successfully to zone 'example.com'"
api_response:
    description: Full API response from Technitium DNS server
    type: dict
    returned: always
    sample: {
        "status": "ok"
    }
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class AddPrivateKeyModule(TechnitiumModule):
    argument_spec = dict(
        node=dict(type='str', required=False),
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        key_type=dict(type='str', required=True, choices=['KeySigningKey', 'ZoneSigningKey']),
        rollover_days=dict(type='int', required=False),
        algorithm=dict(type='str', required=True, choices=['RSA', 'ECDSA', 'EDDSA']),
        pem_private_key=dict(type='str', required=False, no_log=True),
        hash_algorithm=dict(type='str', required=False, choices=['MD5', 'SHA1', 'SHA256', 'SHA512']),
        key_size=dict(type='int', required=False),
        curve=dict(type='str', required=False, choices=['P256', 'P384', 'ED25519', 'ED448']),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def validate_algorithm_parameters(self):
        """Validate that required parameters are provided for each algorithm"""
        algorithm = self.params['algorithm']
        hash_algorithm = self.params.get('hash_algorithm')
        key_size = self.params.get('key_size')
        curve = self.params.get('curve')

        if algorithm == 'RSA':
            if not hash_algorithm:
                self.fail_json(msg="hash_algorithm is required when using RSA algorithm")
            if not key_size:
                self.fail_json(msg="key_size is required when using RSA algorithm")
            if curve:
                self.fail_json(msg="curve parameter is not valid for RSA algorithm")

        elif algorithm == 'ECDSA':
            if not curve:
                self.fail_json(msg="curve is required when using ECDSA algorithm")
            if curve not in ['P256', 'P384']:
                self.fail_json(msg=f"Invalid curve '{curve}' for ECDSA. Valid values are: P256, P384")
            if hash_algorithm:
                self.fail_json(msg="hash_algorithm parameter is not valid for ECDSA algorithm")
            if key_size:
                self.fail_json(msg="key_size parameter is not valid for ECDSA algorithm")

        elif algorithm == 'EDDSA':
            if not curve:
                self.fail_json(msg="curve is required when using EDDSA algorithm")
            if curve not in ['ED25519', 'ED448']:
                self.fail_json(msg=f"Invalid curve '{curve}' for EDDSA. Valid values are: ED25519, ED448")
            if hash_algorithm:
                self.fail_json(msg="hash_algorithm parameter is not valid for EDDSA algorithm")
            if key_size:
                self.fail_json(msg="key_size parameter is not valid for EDDSA algorithm")

    def run(self):
        zone = self.params['zone']
        key_type = self.params['key_type']
        algorithm = self.params['algorithm']
        node = self.params.get('node')

        # Validate algorithm-specific parameters
        self.validate_algorithm_parameters()

        # Get DNSSEC properties to validate zone is signed
        dnssec_props = self.get_dnssec_properties(zone, node=node)
        dnssec_status = dnssec_props.get('dnssecStatus', '').lower()

        if dnssec_status == 'unsigned':
            self.fail_json(msg=f"Zone '{zone}' is not signed with DNSSEC. Cannot add private key to unsigned zone.")

        if dnssec_status not in ['signed', 'signedwithnsec', 'signedwithnsec3']:
            self.fail_json(msg=f"Zone '{zone}' has unexpected DNSSEC status: {dnssec_status}")

        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Private key would be added to zone '{zone}' with {algorithm} algorithm (check mode)",
                api_response={}
            )

        # Build API parameters
        query = {
            'zone': zone,
            'keyType': key_type,
            'algorithm': algorithm
        }

        # Add optional parameters
        if node:
            query['node'] = node
        if self.params.get('rollover_days') is not None:
            query['rolloverDays'] = self.params['rollover_days']
        if self.params.get('pem_private_key'):
            query['pemPrivateKey'] = self.params['pem_private_key']
        if self.params.get('hash_algorithm'):
            query['hashAlgorithm'] = self.params['hash_algorithm']
        if self.params.get('key_size'):
            query['keySize'] = self.params['key_size']
        if self.params.get('curve'):
            query['curve'] = self.params['curve']

        # Add private key via API
        data = self.request('/api/zones/dnssec/properties/addPrivateKey', params=query, method='POST')
        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        # Extract key information if available
        key_info = {}
        response_data = data.get('response', {})
        if response_data:
            key_info = response_data

        result_msg = f"Private key added successfully to zone '{zone}' (algorithm: {algorithm}, type: {key_type})"

        exit_kwargs = {
            'changed': True,
            'msg': result_msg,
            'api_response': data
        }

        if key_info:
            exit_kwargs['key_info'] = key_info

        self.exit_json(**exit_kwargs)


if __name__ == '__main__':
    module = AddPrivateKeyModule()
    module.run()
