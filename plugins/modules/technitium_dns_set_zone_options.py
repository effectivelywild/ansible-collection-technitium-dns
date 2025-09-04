#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to set zone options on Technitium DNS API using TechnitiumModule base class

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_set_zone_options
short_description: Set DNS zone options
version_added: "0.0.1"
description:
    - Set zone-specific options on a Technitium DNS server.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_zone
    description: Creates DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_delete_zone
    description: Deletes DNS Zones
  - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
    description: Sign a zone with DNSSEC
  - module: effectivelywild.technitium_dns.technitium_dns_get_zone_options
    description: Get zone options
  - module: effectivelywild.technitium_dns.technitium_dns_enable_zone
    description: Enable a zone
  - module: effectivelywild.technitium_dns.technitium_dns_disable_zone
    description: Disable a zone
options:
    api_port:
        description:
            - Port for the Technitium DNS API. Defaults to 5380.
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
    catalog:
        description:
            - Catalog zone name to register as its member zone (Primary, Stub, Forwarder only)
        required: false
        type: str
    disabled:
        description:
            - Sets if the zone is enabled or disabled
        required: false
        type: bool
    notify:
        description:
            - Notify policy
        required: false
        type: str
        choices: [None, ZoneNameServers, SpecifiedNameServers, BothZoneAndSpecifiedNameServers, SeparateNameServersForCatalogAndMemberZones]
    notifyNameServers:
        description:
            - Comma separated IPs to notify (Primary, Secondary, Forwarder, Catalog only)
        required: false
        type: str
    notifySecondaryCatalogsNameServers:
        description:
            - Comma separated IPs to notify for catalog updates (Catalog only)
        required: false
        type: str
    overrideCatalogNotify:
        description:
            - Override Notify option in the Catalog zone (Primary, Forwarder only)
        required: false
        type: bool
    overrideCatalogQueryAccess:
        description:
            - Override Query Access option in the Catalog zone (Primary, Stub, Forwarder only)
        required: false
        type: bool
    overrideCatalogZoneTransfer:
        description:
            - Override Zone Transfer option in the Catalog zone (Primary, Forwarder only)
        required: false
        type: bool
    primaryNameServerAddresses:
        description:
            - Comma separated IPs or names of the primary name server (Secondary, SecondaryForwarder, SecondaryCatalog, Stub only)
        required: false
        type: str
    primaryZoneTransferProtocol:
        description:
            - Zone transfer protocol (Secondary, SecondaryForwarder, SecondaryCatalog only)
        required: false
        type: str
        choices: [Tcp, Tls, Quic]
    primaryZoneTransferTsigKeyName:
        description:
            - TSIG key name for zone transfer (Secondary, SecondaryForwarder, SecondaryCatalog only)
        required: false
        type: str
    queryAccess:
        description:
            - Query access policy
        required: false
        type: str
        choices: [Deny, Allow, AllowOnlyPrivateNetworks, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
    queryAccessNetworkACL:
        description:
            - Comma separated ACL for query access (not SecondaryCatalog, only with certain queryAccess set)
        required: false
        type: str
    update:
        description:
            - Allow dynamic updates
        required: false
        type: str
        choices: [Deny, Allow, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
    updateNetworkACL:
        description:
            - Comma separated ACL for update (Primary, Secondary, Forwarder, with certain update set)
        required: false
        type: str
    updateSecurityPolicies:
        description:
            - Pipe separated table of security policies (Primary, Forwarder only)
        required: false
        type: str
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests.
        required: false
        type: bool
        default: true
    validateZone:
        description:
            - Enable ZONEMD validation (Secondary only).
        required: false
        type: bool
    zone:
        description:
            - The domain name of the zone to set options for.
        required: true
        type: str
    zoneTransfer:
        description:
            - Zone transfer policy (Primary, Secondary only)
        required: false
        type: str
        choices: [Deny, Allow, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
    zoneTransferNetworkACL:
        description:
            - Comma separated ACL for zone transfer (Primary, Secondary, Forwarder, Catalog only, with certain zoneTransfer set).
        required: false
        type: str
    zoneTransferTsigKeyNames:
        description:
            - Comma separated TSIG key names for zone transfer (Primary, Secondary, Forwarder, Catalog only)
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Set basic options for primary zone
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    disabled: false
    zoneTransfer: Allow
    notify: ZoneNameServers

- name: Configure primary zone with restricted access and TSIG keys
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "secure.example.com"
    queryAccess: UseSpecifiedNetworkACL
    queryAccessNetworkACL: "192.168.1.0/24,10.0.0.0/8"
    zoneTransfer: AllowOnlyZoneNameServers
    zoneTransferTsigKeyNames: "key1.example.com,key2.example.com"
    update: UseSpecifiedNetworkACL
    updateNetworkACL: "192.168.1.100/32"

- name: Set up secondary zone with custom primary servers
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "secondary.example.com"
    primaryNameServerAddresses: "192.168.1.10,192.168.1.11"
    primaryZoneTransferProtocol: Tls
    primaryZoneTransferTsigKeyName: "transfer.key"
    validateZone: true
    notify: SpecifiedNameServers
    notifyNameServers: "192.168.1.20,192.168.1.21"

- name: Configure catalog zone with notification settings
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "catalog.example.com"
    zoneTransfer: UseSpecifiedNetworkACL
    zoneTransferNetworkACL: "192.168.2.0/24"
    notify: SeparateNameServersForCatalogAndMemberZones
    notifySecondaryCatalogsNameServers: "192.168.2.10,192.168.2.11"

- name: Set update security policies for primary zone
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "dynamic.example.com"
    update: UseSpecifiedNetworkACL
    updateNetworkACL: "192.168.3.0/24"
    updateSecurityPolicies: "update.key|dynamic.example.com|A,AAAA|update.key|*.dynamic.example.com|ANY"

- name: Configure zone as catalog member with overrides
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "member.example.com"
    catalog: "catalog.example.com"
    overrideCatalogQueryAccess: true
    overrideCatalogZoneTransfer: true
    queryAccess: AllowOnlyPrivateNetworks
    zoneTransfer: Deny
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The API response payload (empty dict for successful set operations)
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
diff:
    description: Dictionary showing what changed, with current and desired values
    type: dict
    returned: when changes are made
    sample: {
        "zoneTransfer": {
            "current": "AllowOnlyZoneNameServers",
            "desired": "Allow"
        },
        "zoneTransferNetworkACL": {
            "current": [],
            "desired": [
                "192.168.2.0/24"
            ]
        }
    }
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
msg:
    description: Human readable message describing the result
    type: str
    returned: always
    sample: "Zone options set successfully."
'''

class SetZoneOptionsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        zone=dict(type='str', required=True),
        disabled=dict(type='bool', required=False),
        catalog=dict(type='str', required=False),
        overrideCatalogQueryAccess=dict(type='bool', required=False),
        overrideCatalogZoneTransfer=dict(type='bool', required=False),
        overrideCatalogNotify=dict(type='bool', required=False),
        primaryNameServerAddresses=dict(type='list', elements='str', required=False),
        primaryZoneTransferProtocol=dict(type='str', required=False, choices=['Tcp', 'Tls', 'Quic']),
        primaryZoneTransferTsigKeyName=dict(type='str', required=False),
        validateZone=dict(type='bool', required=False),
        queryAccess=dict(type='str', required=False, choices=['Deny', 'Allow', 'AllowOnlyPrivateNetworks', 'AllowOnlyZoneNameServers', 'UseSpecifiedNetworkACL', 'AllowZoneNameServersAndUseSpecifiedNetworkACL']),
        queryAccessNetworkACL=dict(type='list', elements='str', required=False),
        zoneTransfer=dict(type='str', required=False, choices=['Deny', 'Allow', 'AllowOnlyZoneNameServers', 'UseSpecifiedNetworkACL', 'AllowZoneNameServersAndUseSpecifiedNetworkACL']),
        zoneTransferNetworkACL=dict(type='list', elements='str', required=False),
        zoneTransferTsigKeyNames=dict(type='list', elements='str', required=False),
        notify=dict(type='str', required=False, choices=['None', 'ZoneNameServers', 'SpecifiedNameServers', 'BothZoneAndSpecifiedNameServers', 'SeparateNameServersForCatalogAndMemberZones']),
        notifyNameServers=dict(type='list', elements='str', required=False),
        notifySecondaryCatalogsNameServers=dict(type='list', elements='str', required=False),
        update=dict(type='str', required=False, choices=['Deny', 'Allow', 'AllowOnlyZoneNameServers', 'UseSpecifiedNetworkACL', 'AllowZoneNameServersAndUseSpecifiedNetworkACL']),
        updateNetworkACL=dict(type='str', required=False),
        updateSecurityPolicies=dict(type='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        zone = params['zone']

        # 1. Validate zone exists and fetch current zone options
        get_data = self.validate_zone_exists(zone)
        if get_data.get('status') != 'ok':
            error_msg = get_data.get('errorMessage') or 'Unknown error'
            self.fail_json(msg=f"Technitium API error (get options): {error_msg}", api_response=get_data)
        current = get_data.get('response', {})
        zone_type = current.get('type')

        # 1b. Conditional parameter validation based on zone type
        allowed_params = {
            'Primary': set(['disabled','catalog','overrideCatalogQueryAccess','overrideCatalogZoneTransfer','overrideCatalogNotify','queryAccess','queryAccessNetworkACL','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers','update','updateNetworkACL','updateSecurityPolicies']),
            'Stub': set(['disabled','catalog','overrideCatalogQueryAccess','primaryNameServerAddresses','validateZone','queryAccess','queryAccessNetworkACL']),
            'Forwarder': set(['disabled','catalog','overrideCatalogQueryAccess','overrideCatalogZoneTransfer','overrideCatalogNotify','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers','update','updateNetworkACL','updateSecurityPolicies']),
            'Secondary': set(['disabled','primaryNameServerAddresses','primaryZoneTransferProtocol','primaryZoneTransferTsigKeyName','validateZone','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers','update','updateNetworkACL','queryAccess','queryAccessNetworkACL']),
            'SecondaryForwarder': set(['disabled','primaryNameServerAddresses','primaryZoneTransferProtocol','primaryZoneTransferTsigKeyName','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers','queryAccess','queryAccessNetworkACL']),
            'SecondaryCatalog': set(['disabled','primaryNameServerAddresses','primaryZoneTransferProtocol','primaryZoneTransferTsigKeyName','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers']),
            'Catalog': set(['disabled','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers','notifySecondaryCatalogsNameServers','queryAccess','queryAccessNetworkACL']),
            'SecondaryROOT': set(['disabled']),
        }
        if zone_type in allowed_params:
            for param in params:
                if param in ['api_url','api_port','api_token','zone','validate_certs']:
                    continue
                if params[param] is not None and param not in allowed_params[zone_type]:
                    self.fail_json(msg=f"Parameter '{param}' is not supported for zone type '{zone_type}'.")

        # 2. Build desired state dict (for comparison, keep lists as lists)
        desired = {}
        list_like_fields = [
            'queryAccessNetworkACL', 'primaryNameServerAddresses', 'zoneTransferNetworkACL',
            'zoneTransferTsigKeyNames', 'notifyNameServers', 'notifySecondaryCatalogsNameServers',
            'updateNetworkACL'
        ]

        def parse_update_security_policies(val):
            # Accepts a list of pipe-separated strings or a single string, returns list of dicts
            if val is None or val == "":
                return []
            if isinstance(val, str):
                val = [val]
            result = []
            for item in val:
                if isinstance(item, dict):
                    result.append(item)
                elif isinstance(item, str):
                    parts = item.split("|")
                    if len(parts) == 3:
                        allowed_types = [t.strip() for t in parts[2].split(",") if t.strip()] if parts[2] else []
                        result.append({
                            'tsigKeyName': parts[0],
                            'domain': parts[1],
                            'allowedTypes': allowed_types
                        })
            return result
        for key in [
            'disabled', 'catalog', 'overrideCatalogQueryAccess', 'overrideCatalogZoneTransfer', 'overrideCatalogNotify',
            'primaryNameServerAddresses', 'primaryZoneTransferProtocol', 'primaryZoneTransferTsigKeyName', 'validateZone',
            'queryAccess', 'queryAccessNetworkACL', 'zoneTransfer', 'zoneTransferNetworkACL', 'zoneTransferTsigKeyNames',
            'notify', 'notifyNameServers', 'notifySecondaryCatalogsNameServers', 'update', 'updateNetworkACL', 'updateSecurityPolicies']:
            value = params.get(key)
            if value is not None:
                if isinstance(value, bool):
                    value = str(value).lower()
                # For list-like fields, always store as list for comparison
                if key in list_like_fields:
                    if isinstance(value, str):
                        value = [x.strip() for x in value.split(",") if x.strip()]
                    elif not isinstance(value, list):
                        value = [str(value)]
                # For updateSecurityPolicies, always store as list of dicts for comparison
                if key == 'updateSecurityPolicies':
                    value = parse_update_security_policies(value)
                desired[key] = value

        # 3. Compare current vs desired (normalize, build diff for idempotency)
        diff = {}
        for k, v in desired.items():
            current_val = current.get(k)
            # Normalize booleans to string for comparison
            if isinstance(current_val, bool):
                current_val = str(current_val).lower()
            if isinstance(v, bool):
                v = str(v).lower()
            # Compare list-like fields as sorted lists
            if k in list_like_fields:
                def to_list(val):
                    if val is None or val == "":
                        return []
                    if isinstance(val, list):
                        return [str(x) for x in val]
                    if isinstance(val, str):
                        return [x.strip() for x in val.split(",") if x.strip()]
                    return [str(val)]
                current_list = sorted(to_list(current_val))
                desired_list = sorted(to_list(v))
                if current_list != desired_list:
                    diff[k] = {'current': current_list, 'desired': desired_list}
                continue
            # Special handling for updateSecurityPolicies: compare as list of dicts
            if k == 'updateSecurityPolicies':
                def canonicalize_policy(policy):
                    # Sort allowedTypes for comparison
                    if isinstance(policy, dict):
                        c = dict(policy)
                        if 'allowedTypes' in c and isinstance(c['allowedTypes'], list):
                            c['allowedTypes'] = sorted(c['allowedTypes'])
                        return c
                    return policy
                current_policies = [canonicalize_policy(x) for x in (current_val or [])]
                desired_policies = [canonicalize_policy(x) for x in (v or [])]
                if sorted(current_policies, key=lambda x: (x.get('tsigKeyName'), x.get('domain'))) != \
                   sorted(desired_policies, key=lambda x: (x.get('tsigKeyName'), x.get('domain'))):
                    diff[k] = {'current': current_policies, 'desired': desired_policies}
                continue
            # Treat None, empty string, and empty list as equivalent for unset fields
            if current_val in [None, "", []] and v in [None, "", []]:
                continue
            if current_val != v:
                diff[k] = {'current': current_val, 'desired': v}

        if not diff:
            self.exit_json(changed=False, msg="Zone options already match desired state.")

        # Debug: show diff, current, and desired if a change is detected
        debug_info = {
            'diff': diff,
            'current': current,
            'desired': desired
        }

        # Check mode: if changes would be made, exit early and show diff
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg="(check mode) Zone options would be updated.",
                diff=diff,
                api_response={"status": "ok", "check_mode": True, "zone": zone}
            )

        # 4. Set options if needed
        set_query = {'zone': zone}
        # For API call, convert list-like fields to comma-separated strings as needed
        for k, v in desired.items():
            if k in list_like_fields and isinstance(v, list):
                set_query[k] = ",".join(str(x) for x in v)
            elif k == 'updateSecurityPolicies' and isinstance(v, list):
                # Convert list of dicts to pipe-separated strings for API
                def policy_to_str(policy):
                    if isinstance(policy, dict):
                        return "|".join([
                            str(policy.get('tsigKeyName', '')),
                            str(policy.get('domain', '')),
                            ",".join(sorted(policy.get('allowedTypes', [])))
                        ])
                    return str(policy)
                set_query[k] = "|".join(policy_to_str(x) for x in v)
            else:
                set_query[k] = v
        data = self.request('/api/zones/options/set', params=set_query)
        error_msg = data.get('errorMessage')
        if error_msg and 'No such zone was found' in error_msg:
            # Remove stackTrace if present
            clean_response = dict(data)
            clean_response.pop('stackTrace', None)
            self.fail_json(msg=f"Zone '{zone}' does not exist: {error_msg}", api_response=clean_response)
        if data.get('status') != 'ok':
            self.fail_json(msg=f"Technitium API error: {error_msg or 'Unknown error'}", api_response=data)
        self.exit_json(
            changed=True,
            msg="Zone options set successfully.",
            diff=diff,
            api_response=data
        )

if __name__ == '__main__':
    module = SetZoneOptionsModule()
    module.run()
