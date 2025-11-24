#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_update_nsec3_parameters
short_description: Update NSEC3 Parameters
version_added: "0.2.1"
author: Frank Muise (@effectivelywild)
description:
  - Updates the iteration and salt length parameters for NSEC3 on a signed DNS zone.
  - The zone must already be signed with DNSSEC and using NSEC3.
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
  - module: effectivelywild.technitium_dns.technitium_dns_convert_to_nsec3
    description: Convert signed zone from NSEC to NSEC3
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
      - The name of the primary zone to update NSEC3 parameters for
    required: true
    type: str
  iterations:
    description:
      - The number of iterations to use for hashing
      - Default value is 0 when not specified
    required: false
    type: int
    default: 0
  salt_length:
    description:
      - The length of salt in bytes to use for hashing
      - Default value is 0 when not specified
    required: false
    type: int
    default: 0
'''

EXAMPLES = r'''
- name: Update NSEC3 parameters with custom iterations and salt length
  technitium_dns_update_nsec3_parameters:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    iterations: 10
    salt_length: 8

- name: Reset NSEC3 parameters to defaults
  technitium_dns_update_nsec3_parameters:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    iterations: 0
    salt_length: 0

- name: Update only iterations parameter
  technitium_dns_update_nsec3_parameters:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    iterations: 5

- name: Update NSEC3 parameters on a specific cluster node
  technitium_dns_update_nsec3_parameters:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    iterations: 10
    salt_length: 8
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
    sample: "NSEC3 parameters updated for zone 'example.com'"
api_response:
    description: Full API response from Technitium DNS server
    type: dict
    returned: always
    sample: {
        "status": "ok"
    }
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class UpdateNSEC3ParametersModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False),
        zone=dict(type='str', required=True),
        iterations=dict(type='int', required=False, default=0),
        salt_length=dict(type='int', required=False, default=0),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        zone = self.params['zone']
        iterations = self.params['iterations']
        salt_length = self.params['salt_length']

        # Get DNSSEC properties - this includes status and current NSEC3 parameters
        dnssec_props = self.get_dnssec_properties(zone)
        dnssec_status = dnssec_props.get('dnssecStatus', '').lower()

        if dnssec_status == 'unsigned':
            self.fail_json(msg=f"Zone '{zone}' is not signed. NSEC3 parameters can only be updated on signed zones.")

        # Check if zone is using NSEC3 by looking for NSEC3 parameters
        if 'nsec3Iterations' not in dnssec_props:
            self.fail_json(msg=f"Zone '{zone}' is not using NSEC3. Convert to NSEC3 first.")

        # Check if parameters are already set as requested
        current_iterations = dnssec_props.get('nsec3Iterations', 0)
        current_salt_length = dnssec_props.get('nsec3SaltLength', 0)

        params_changed = not (current_iterations == iterations and current_salt_length == salt_length)

        if not params_changed:
            self.exit_json(
                changed=False,
                msg=f"NSEC3 parameters for zone '{zone}' are already set to iterations={iterations}, salt_length={salt_length}",
                api_response={'status': 'ok', 'msg': 'No changes needed'}
            )

        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"NSEC3 parameters for zone '{zone}' would be updated to iterations={iterations}, salt_length={salt_length} (check mode)",
                api_response={}
            )

        # Update NSEC3 parameters
        query = {
            'zone': zone,
            'iterations': iterations,
            'saltLength': salt_length
        }
        if self.params.get('node'):
            query['node'] = self.params['node']

        data = self.request('/api/zones/dnssec/properties/updateNSEC3Params', params=query, method='POST')
        status = data.get('status')
        error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"

        if status != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)

        self.exit_json(
            changed=True,
            msg=f"NSEC3 parameters updated for zone '{zone}' (iterations={iterations}, salt_length={salt_length})",
            api_response=data
        )


if __name__ == '__main__':
    module = UpdateNSEC3ParametersModule()
    module.run()
