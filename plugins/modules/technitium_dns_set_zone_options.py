#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_set_zone_options
short_description: Set DNS zone options
version_added: "0.1.0"
description:
    - Set zone-specific options.
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
    node:
        description:
            - The node domain name for which this API call is intended
            - When unspecified, the current node is used
            - This parameter can be used only when Clustering is initialized
        required: false
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
            - List of IPs to notify (Primary, Secondary, Forwarder, Catalog only)
        required: false
        type: list
        elements: str
    notifySecondaryCatalogsNameServers:
        description:
            - List of IPs to notify for catalog updates (Catalog only)
        required: false
        type: list
        elements: str
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
            - List of IPs or names of the primary name server (Secondary, SecondaryForwarder, SecondaryCatalog, Stub only)
        required: false
        type: list
        elements: str
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
            - List of network ACL entries for query access (not SecondaryCatalog, only with certain queryAccess set)
        required: false
        type: list
        elements: str
    update:
        description:
            - Allow dynamic updates
        required: false
        type: str
        choices: [Deny, Allow, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
    updateNetworkACL:
        description:
            - List of network ACL entries for update (Primary, Secondary, Forwarder, with certain update set)
        required: false
        type: list
        elements: str
    updateSecurityPolicies:
        description:
            - List of security policies for zone updates (Primary, Forwarder only)
        required: false
        type: list
        elements: dict
        suboptions:
            tsigKeyName:
                description: TSIG key name for the policy
                type: str
                required: true
            domain:
                description: Domain pattern for the policy
                type: str
                required: true
            allowedTypes:
                description: List of allowed DNS record types
                type: list
                elements: str
                required: true
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
            - List of network ACL entries for zone transfer (Primary, Secondary, Forwarder, Catalog only, with certain zoneTransfer set)
        required: false
        type: list
        elements: str
    zoneTransferTsigKeyNames:
        description:
            - List of TSIG key names for zone transfer (Primary, Secondary, Forwarder, Catalog only)
        required: false
        type: list
        elements: str
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
    queryAccessNetworkACL:
      - "192.168.1.0/24"
      - "10.0.0.0/8"
    zoneTransfer: AllowOnlyZoneNameServers
    zoneTransferTsigKeyNames:
      - "key1.example.com"
      - "key2.example.com"
    update: UseSpecifiedNetworkACL
    updateNetworkACL:
      - "192.168.1.100/32"

- name: Set up secondary zone with custom primary servers
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "secondary.example.com"
    primaryNameServerAddresses:
      - "192.168.1.10"
      - "192.168.1.11"
    primaryZoneTransferProtocol: Tls
    primaryZoneTransferTsigKeyName: "transfer.key"
    validateZone: true
    notify: SpecifiedNameServers
    notifyNameServers:
      - "192.168.1.20"
      - "192.168.1.21"

- name: Configure catalog zone with notification settings
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "catalog.example.com"
    zoneTransfer: UseSpecifiedNetworkACL
    zoneTransferNetworkACL:
      - "192.168.2.0/24"
    notify: SeparateNameServersForCatalogAndMemberZones
    notifySecondaryCatalogsNameServers:
      - "192.168.2.10"
      - "192.168.2.11"

- name: Set update security policies for primary zone
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "dynamic.example.com"
    update: UseSpecifiedNetworkACL
    updateNetworkACL:
      - "192.168.3.0/24"
    updateSecurityPolicies:
      - tsigKeyName: "update.key"
        domain: "dynamic.example.com"
        allowedTypes:
          - "A"
          - "AAAA"
      - tsigKeyName: "update.key"
        domain: "*.dynamic.example.com"
        allowedTypes:
          - "ANY"

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

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class SetZoneOptionsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        node=dict(type='str', required=False),
        zone=dict(type='str', required=True),
        disabled=dict(type='bool', required=False),
        catalog=dict(type='str', required=False),
        overrideCatalogQueryAccess=dict(type='bool', required=False),
        overrideCatalogZoneTransfer=dict(type='bool', required=False),
        overrideCatalogNotify=dict(type='bool', required=False),
        primaryNameServerAddresses=dict(
            type='list', elements='str', required=False),
        primaryZoneTransferProtocol=dict(
            type='str', required=False, choices=['Tcp', 'Tls', 'Quic']),
        primaryZoneTransferTsigKeyName=dict(type='str', required=False, no_log=True),
        validateZone=dict(type='bool', required=False),
        queryAccess=dict(type='str', required=False, choices=['Deny', 'Allow', 'AllowOnlyPrivateNetworks',
                         'AllowOnlyZoneNameServers', 'UseSpecifiedNetworkACL', 'AllowZoneNameServersAndUseSpecifiedNetworkACL']),
        queryAccessNetworkACL=dict(
            type='list', elements='str', required=False),
        zoneTransfer=dict(type='str', required=False, choices=[
                          'Deny', 'Allow', 'AllowOnlyZoneNameServers', 'UseSpecifiedNetworkACL', 'AllowZoneNameServersAndUseSpecifiedNetworkACL']),
        zoneTransferNetworkACL=dict(
            type='list', elements='str', required=False),
        zoneTransferTsigKeyNames=dict(
            type='list', elements='str', required=False, no_log=True),
        notify=dict(type='str', required=False, choices=[
                    'None', 'ZoneNameServers', 'SpecifiedNameServers', 'BothZoneAndSpecifiedNameServers', 'SeparateNameServersForCatalogAndMemberZones']),
        notifyNameServers=dict(type='list', elements='str', required=False),
        notifySecondaryCatalogsNameServers=dict(
            type='list', elements='str', required=False),
        update=dict(type='str', required=False, choices=[
                    'Deny', 'Allow', 'AllowOnlyZoneNameServers', 'UseSpecifiedNetworkACL', 'AllowZoneNameServersAndUseSpecifiedNetworkACL']),
        updateNetworkACL=dict(type='list', elements='str', required=False),
        updateSecurityPolicies=dict(
            type='list',
            elements='dict',
            required=False,
            options=dict(
                tsigKeyName=dict(type='str', required=True, no_log=True),
                domain=dict(type='str', required=True),
                allowedTypes=dict(type='list', elements='str', required=True)
            )
        )
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _normalize_primary_nameserver_addresses(self, value):
        """
        Normalize primaryNameServerAddresses to include default ports.

        In Technitium DNS v14+, the API returns addresses with explicit ports.
        Default ports depend on primaryZoneTransferProtocol:
        - Tcp: port 53
        - Tls: port 853
        - Quic: port 853

        This method ensures addresses are compared consistently by adding
        the default port if not specified.
        """
        # Get the protocol to determine default port
        protocol = self.params.get('primaryZoneTransferProtocol')
        if protocol is None:
            # If we're normalizing current values, get from current state
            protocol = getattr(self, '_current_protocol', None)

        # Determine default port based on protocol
        if protocol == 'Tcp':
            default_port = '53'
        elif protocol in ['Tls', 'Quic']:
            default_port = '853'
        else:
            # If no protocol specified, assume port 53 (standard DNS)
            default_port = '53'

        # Convert value to list
        if isinstance(value, str):
            addresses = [x.strip() for x in value.split(",") if x.strip()]
        elif isinstance(value, list):
            addresses = [str(x) for x in value]
        else:
            addresses = [str(value)]

        # Normalize each address to include port
        normalized = []
        for addr in addresses:
            addr = addr.strip()
            # Check if port is already specified
            if ':' in addr and not addr.startswith('['):
                # IPv4 with port already specified
                normalized.append(addr)
            elif addr.startswith('['):
                # IPv6 address - check for port
                if ']:' in addr:
                    # IPv6 with port already specified
                    normalized.append(addr)
                else:
                    # IPv6 without port - add default
                    normalized.append(f"{addr}:{default_port}")
            else:
                # No port specified - add default
                normalized.append(f"{addr}:{default_port}")

        return sorted(normalized)

    def _normalize_value(self, key, value):
        """Normalize a value for comparison purposes."""
        list_like_fields = [
            'queryAccessNetworkACL', 'primaryNameServerAddresses', 'zoneTransferNetworkACL',
            'zoneTransferTsigKeyNames', 'notifyNameServers', 'notifySecondaryCatalogsNameServers',
            'updateNetworkACL'
        ]

        # Handle None/empty values
        if value in [None, "", []]:
            return [] if key in list_like_fields or key == 'updateSecurityPolicies' else None

        # Normalize booleans to lowercase strings
        if isinstance(value, bool):
            return str(value).lower()

        # Special handling for primaryNameServerAddresses to normalize ports
        if key == 'primaryNameServerAddresses':
            return self._normalize_primary_nameserver_addresses(value)

        # Normalize list-like fields
        if key in list_like_fields:
            if isinstance(value, list):
                return sorted([str(x) for x in value])
            elif isinstance(value, str):
                return sorted([x.strip() for x in value.split(",") if x.strip()])
            else:
                return sorted([str(value)])

        # Normalize updateSecurityPolicies
        if key == 'updateSecurityPolicies':
            if not isinstance(value, list):
                return []
            normalized_policies = []
            for policy in value:
                if isinstance(policy, dict):
                    normalized_policy = dict(policy)
                    if 'allowedTypes' in normalized_policy and isinstance(normalized_policy['allowedTypes'], list):
                        normalized_policy['allowedTypes'] = sorted(
                            normalized_policy['allowedTypes'])
                    normalized_policies.append(normalized_policy)
                else:
                    normalized_policies.append(policy)
            return sorted(normalized_policies, key=lambda x: (x.get('tsigKeyName', ''), x.get('domain', '')))

        return value

    def run(self):
        params = self.params
        zone = params['zone']
        node = params.get('node')

        # 1. Validate zone exists and fetch current zone options
        get_data = self.validate_zone_exists(zone, node=node)
        if get_data.get('status') != 'ok':
            error_msg = get_data.get('errorMessage') or 'Unknown error'
            self.fail_json(
                msg=f"Technitium API error (get options): {error_msg}", api_response=get_data)
        current = get_data.get('response', {})
        zone_type = current.get('type')

        # Store current protocol for normalizing primaryNameServerAddresses
        # Use user-provided protocol if specified, otherwise use current protocol from API
        self._current_protocol = params.get('primaryZoneTransferProtocol') or current.get('primaryZoneTransferProtocol')

        # 1b. Conditional parameter validation based on zone type
        allowed_params = {
            'Primary': set(['disabled', 'catalog', 'overrideCatalogQueryAccess', 'overrideCatalogZoneTransfer',
                            'overrideCatalogNotify', 'queryAccess', 'queryAccessNetworkACL', 'zoneTransfer',
                            'zoneTransferNetworkACL', 'zoneTransferTsigKeyNames', 'notify', 'notifyNameServers',
                            'update', 'updateNetworkACL', 'updateSecurityPolicies']),
            'Stub': set(['disabled', 'catalog', 'overrideCatalogQueryAccess', 'primaryNameServerAddresses',
                         'validateZone', 'queryAccess', 'queryAccessNetworkACL']),
            'Forwarder': set(['disabled', 'catalog', 'overrideCatalogQueryAccess', 'overrideCatalogZoneTransfer',
                              'overrideCatalogNotify', 'notify', 'notifyNameServers', 'update', 'updateNetworkACL',
                              'updateSecurityPolicies']),
            'Secondary': set(['disabled', 'primaryNameServerAddresses', 'primaryZoneTransferProtocol',
                              'primaryZoneTransferTsigKeyName', 'validateZone', 'zoneTransfer', 'zoneTransferNetworkACL',
                              'zoneTransferTsigKeyNames', 'notify', 'notifyNameServers', 'update', 'updateNetworkACL',
                              'queryAccess', 'queryAccessNetworkACL']),
            'SecondaryForwarder': set(['disabled', 'primaryNameServerAddresses', 'primaryZoneTransferProtocol',
                                       'primaryZoneTransferTsigKeyName', 'zoneTransfer', 'zoneTransferNetworkACL',
                                       'zoneTransferTsigKeyNames', 'notify', 'notifyNameServers', 'queryAccess',
                                       'queryAccessNetworkACL']),
            'SecondaryCatalog': set(['disabled', 'primaryNameServerAddresses', 'primaryZoneTransferProtocol',
                                     'primaryZoneTransferTsigKeyName', 'zoneTransfer', 'zoneTransferNetworkACL',
                                     'zoneTransferTsigKeyNames', 'notify', 'notifyNameServers']),
            'Catalog': set(['disabled', 'zoneTransfer', 'zoneTransferNetworkACL', 'zoneTransferTsigKeyNames', 'notify',
                            'notifyNameServers', 'notifySecondaryCatalogsNameServers', 'queryAccess', 'queryAccessNetworkACL']),
            'SecondaryROOT': set(['disabled']),
        }
        if zone_type in allowed_params:
            for param in params:
                if param in ['api_url', 'api_port', 'api_token', 'zone', 'validate_certs', 'node']:
                    continue
                if params[param] is not None and param not in allowed_params[zone_type]:
                    # Show what user attempted to configure for debugging
                    attempted_config = {k: v for k, v in params.items() if v is not None and k not in [
                        'api_url', 'api_port', 'api_token', 'validate_certs', 'zone', 'node']}
                    self.fail_json(
                        msg=f"Parameter '{param}' is not supported for zone type '{zone_type}'.",
                        attempted_changes=attempted_config,
                        zone_type=zone_type,
                        supported_params=sorted(
                            list(allowed_params[zone_type]))
                    )

        # 2. Build desired state dict and validate user inputs
        desired = {}
        list_like_fields = [
            'queryAccessNetworkACL', 'primaryNameServerAddresses', 'zoneTransferNetworkACL',
            'zoneTransferTsigKeyNames', 'notifyNameServers', 'notifySecondaryCatalogsNameServers',
            'updateNetworkACL'
        ]

        for key in [
            'disabled', 'catalog', 'overrideCatalogQueryAccess', 'overrideCatalogZoneTransfer', 'overrideCatalogNotify',
            'primaryNameServerAddresses', 'primaryZoneTransferProtocol', 'primaryZoneTransferTsigKeyName', 'validateZone',
            'queryAccess', 'queryAccessNetworkACL', 'zoneTransfer', 'zoneTransferNetworkACL', 'zoneTransferTsigKeyNames',
            'notify', 'notifyNameServers', 'notifySecondaryCatalogsNameServers', 'update', 'updateNetworkACL', 'updateSecurityPolicies']:
            value = params.get(key)
            if value is not None:
                # Validate input types before storing
                if key in list_like_fields:
                    if not isinstance(value, list):
                        self.fail_json(
                            msg=f"Parameter '{key}' must be a list, got {type(value).__name__}")
                if key == 'updateSecurityPolicies':
                    if not isinstance(value, list):
                        self.fail_json(
                            msg=f"Parameter '{key}' must be a list of dict, got {type(value).__name__}")
                # Store raw value - normalization happens during comparison
                desired[key] = value

        # 3. Compare current vs desired using normalization helper
        diff = {}
        for k, v in desired.items():
            current_val = current.get(k)
            normalized_current = self._normalize_value(k, current_val)
            normalized_desired = self._normalize_value(k, v)

            if normalized_current != normalized_desired:
                diff[k] = {'current': normalized_current,
                           'desired': normalized_desired}

        if not diff:
            self.exit_json(
                changed=False, msg="Zone options already match desired state.")

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
        if node:
            set_query['node'] = node
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
        data = self.request('/api/zones/options/set', params=set_query, method='POST')
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or 'Unknown error'
            self.fail_json(
                msg=f"Technitium API error: {error_msg}",
                api_response=data
            )
        self.exit_json(
            changed=True,
            msg="Zone options set successfully.",
            diff=diff,
            api_response=data
        )


if __name__ == '__main__':
    module = SetZoneOptionsModule()
    module.run()
