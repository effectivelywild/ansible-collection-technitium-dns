#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to get zone options from Technitium DNS API using TechnitiumModule base class

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_get_zone_options
short_description: Get DNS zone options
version_added: "0.0.1"
description:
    - Retrieve zone-specific options from a Technitium DNS server.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_zone
    description: Creates DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_zone
    description: Deletes DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
  - module: effectivelywild.technitium_dns.technitium_dns_set_zone_options
    description: Set zone options
  - module: effectivelywild.technitium_dns.technitium_dns_enable_zone
    description: Enable a zone
  - module: effectivelywild.technitium_dns.technitium_dns_disable_zone
    description: Disable a zone
options:
    api_url:
        description:
            - Base URL for the Technitium DNS API
        required: true
        type: str
    api_port:
        description:
            - Port for the Technitium DNS API. Defaults to 5380.
        required: false
        type: int
        default: 5380
    api_token:
        description:
            - API token for authenticating with the Technitium DNS API.
        required: true
        type: str
    includeAvailableCatalogZoneNames:
        description:
            - Include list of available Catalog zone names on the DNS server.
        required: false
        type: bool
        default: false
    includeAvailableTsigKeyNames:
        description:
            - Include list of available TSIG key names on the DNS server.
        required: false
        type: bool
        default: false
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests.
        required: false
        type: bool
        default: true
    zone:
        description:
            - The domain name of the zone to get options for.
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Get options for example.com zone
  technitium_dns_get_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    includeAvailableTsigKeyNames: true
  register: result

- debug:
    var: result.options
'''

RETURN = r'''

options:
    description: Zone options returned from API
    type: dict
    returned: always
    contains:
        name:
            description: Zone name
            type: str
            returned: always
        type:
            description: Zone type (e.g., Primary, Secondary)
            type: str
            returned: always
        internal:
            description: Whether the zone is internal
            type: bool
            returned: always
        dnssecStatus:
            description: DNSSEC status of the zone
            type: str
            returned: always
        notifyFailed:
            description: Whether zone notification failed
            type: bool
            returned: always
        notifyFailedFor:
            description: List of hosts for which notification failed
            type: list
            returned: always
        disabled:
            description: Whether the zone is disabled
            type: bool
            returned: always
        catalog:
            description: Zone catalog information
            type: str
            returned: always
        overrideCatalogQueryAccess:
            description: Whether to override catalog query access settings
            type: bool
            returned: always
        overrideCatalogZoneTransfer:
            description: Whether to override catalog zone transfer settings
            type: bool
            returned: always
        overrideCatalogNotify:
            description: Whether to override catalog notify settings
            type: bool
            returned: always
        queryAccess:
            description: Query access policy (e.g., Allow, Deny)
            type: str
            returned: always
        queryAccessNetworkACL:
            description: Network ACL for query access
            type: list
            returned: always
        zoneTransfer:
            description: Zone transfer policy (e.g., AllowOnlyZoneNameServers)
            type: str
            returned: always
        zoneTransferNetworkACL:
            description: Network ACL for zone transfers
            type: list
            returned: always
        zoneTransferTsigKeyNames:
            description: TSIG key names allowed for zone transfers
            type: list
            returned: always
        notify:
            description: Zone notification policy (e.g., ZoneNameServers)
            type: str
            returned: always
        notifyNameServers:
            description: List of name servers to notify
            type: list
            returned: always
        update:
            description: Zone update policy (e.g., UseSpecifiedNetworkACL)
            type: str
            returned: always
        updateNetworkACL:
            description: Network ACL for zone updates
            type: list
            returned: always
        updateSecurityPolicies:
            description: List of update security policies
            type: list
            returned: always
            contains:
                tsigKeyName:
                    description: TSIG key name for the policy
                    type: str
                domain:
                    description: Domain pattern for the policy
                    type: str
                allowedTypes:
                    description: List of allowed DNS record types
                    type: list
        availableCatalogZoneNames:
            description: List of available catalog zone names (when includeAvailableCatalogZoneNames is true)
            type: list
            returned: when requested
        availableTsigKeyNames:
            description: List of available TSIG key names (when includeAvailableTsigKeyNames is true)
            type: list
            returned: when requested
changed:
    description: Whether the module made changes (always false for get operations)
    type: bool
    returned: always
    sample: false
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''

class GetZoneOptionsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        includeAvailableCatalogZoneNames=dict(type='bool', required=False, default=False),
        includeAvailableTsigKeyNames=dict(type='bool', required=False, default=False)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        params = self.params
        zone = params['zone']
        include_catalog = params['includeAvailableCatalogZoneNames']
        include_tsig = params['includeAvailableTsigKeyNames']

        # First validate the zone exists, then get options with additional parameters if needed
        if include_catalog or include_tsig:
            query = {'zone': zone}
            if include_catalog:
                query['includeAvailableCatalogZoneNames'] = 'true'
            if include_tsig:
                query['includeAvailableTsigKeyNames'] = 'true'
            data = self.request('/api/zones/options/get', params=query)
            # Validate zone exists using the response
            error_msg = data.get('errorMessage')
            if error_msg and 'No such zone was found' in error_msg:
                self.fail_json(msg=f"Zone '{zone}' does not exist: {error_msg}")
            if data.get('status') != 'ok':
                error_msg = data.get('errorMessage') or data.get('message') or "Unknown error"
                self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        else:
            # Use base class validation for simple case
            data = self.validate_zone_exists(zone)
            if data.get('status') != 'ok':
                error_msg = data.get('errorMessage') or 'Unknown error'
                self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        options = data.get('response', {})
        self.exit_json(changed=False, options=options)

if __name__ == '__main__':
    module = GetZoneOptionsModule()
    module.run()
