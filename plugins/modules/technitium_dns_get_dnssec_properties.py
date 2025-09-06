#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_get_dnssec_properties
short_description: Get DNSSEC properties for a primary zone
version_added: "0.1.0"
author: Frank Muise (@effectivelywild)
description:
    - Retrieve DNSSEC properties for a signed zone.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone (DNSSEC)
  - module: effectivelywild.technitium_dns.technitium_dns_unsign_zone
    description: Unsign a zone (DNSSEC)
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_nsec
    description: Convert signed zone from NSEC to NSEC3
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_nsec3
    description: Convert signed zone from NSEC3 to NSEC
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
            - Whether to validate SSL certificates when making API requests.
        required: false
        type: bool
        default: true
    zone:
        description:
            - The name of the primary zone to get DNSSEC properties for.
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Get DNSSEC properties for example.com
  technitium_dns_get_dnssec_properties:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
  register: result

- debug:
    var: result.dnssec_properties
'''

RETURN = r'''
changed:
    description: Whether the module made changes (always false for get operations)
    type: bool
    returned: always
    sample: false

dnssec_properties:
    description:
        - DNSSEC properties and configuration for the zone
        - Contains comprehensive information about DNSSEC signing status, keys, and settings
    type: dict
    returned: always
    contains:
        disabled:
            description: Whether the zone is disabled
            type: bool
            returned: always
        dnsKeyTtl:
            description: TTL for DNSKEY records in seconds
            type: int
            returned: always
        dnssecPrivateKeys:
            description: List of DNSSEC private keys used for signing
            type: list
            returned: always
            contains:
                algorithm:
                    description: DNSSEC algorithm name
                    type: str
                    returned: always
                    sample: "ECDSAP256SHA256"
                algorithmNumber:
                    description: DNSSEC algorithm number
                    type: int
                    returned: always
                    sample: 13
                isRetiring:
                    description: Whether the key is being retired
                    type: bool
                    returned: always
                keyTag:
                    description: Key tag identifier
                    type: int
                    returned: always
                keyType:
                    description: Type of key (KeySigningKey or ZoneSigningKey)
                    type: str
                    returned: always
                rolloverDays:
                    description: Rollover frequency in days
                    type: int
                    returned: always
                state:
                    description: Current state of the key
                    type: str
                    returned: always
                stateChangedOn:
                    description: When the key state last changed (ISO timestamp)
                    type: str
                    returned: always
                stateReadyBy:
                    description: When the key will be ready for next state (ISO timestamp)
                    type: str
                    returned: when available
        dnssecStatus:
            description: DNSSEC signing status
            type: str
            returned: always
            sample: "SignedWithNSEC3"
        internal:
            description: Whether the zone is internal
            type: bool
            returned: always
        name:
            description: Zone name
            type: str
            returned: always
        nsec3Iterations:
            description: NSEC3 iterations parameter
            type: int
            returned: when zone uses NSEC3
        nsec3SaltLength:
            description: NSEC3 salt length parameter
            type: int
            returned: when zone uses NSEC3
        type:
            description: Zone type
            type: str
            returned: always
            sample: "Primary"

failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''


class GetDnssecPropertiesModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        zone = self.params['zone']

        # Validate that the zone exists before attempting to get DNSSEC properties
        # This will fail with a clear error message if the zone doesn't exist
        self.validate_zone_exists(zone)

        # Build API parameters for DNSSEC properties request
        params = {'zone': zone}

        # Fetch DNSSEC properties from the Technitium API
        # This endpoint returns DNSSEC keys, signing information, and configuration
        data = self.request('/api/zones/dnssec/properties/get', params=params)

        # Check API response status and handle errors
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        # Extract DNSSEC properties from API response
        dnssec_properties = data.get('response', {})

        # Return the DNSSEC properties (read-only operation, never changed=True)
        self.exit_json(changed=False, dnssec_properties=dnssec_properties)


if __name__ == '__main__':
    module = GetDnssecPropertiesModule()
    module.run()
