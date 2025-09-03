#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to set zone options on Technitium DNS API using TechnitiumModule base class

from ansible_collections.technitium.dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_set_zone_options
short_description: Set DNS zone options on Technitium DNS server
version_added: "0.0.1"
description:
    - Set zone-specific options on a Technitium DNS server using its API.
options:
    api_url:
        description:
            - Base URL for the Technitium DNS API (e.g., http://localhost)
            - Do not include the port; use the 'port' parameter instead.
        required: true
        type: str
    port:
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
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests.
            - Set to false to disable SSL certificate validation (not recommended for production).
        required: false
        type: bool
        default: true
    zone:
        description:
            - The domain name of the zone to set options for.
        required: true
        type: str
    disabled:
        description:
            - Sets if the zone is enabled or disabled.
        required: false
        type: bool
    catalog:
        description:
            - Catalog zone name to register as its member zone (Primary, Stub, Forwarder only).
        required: false
        type: str
    overrideCatalogQueryAccess:
        description:
            - Override Query Access option in the Catalog zone (Primary, Stub, Forwarder only).
        required: false
        type: bool
    overrideCatalogZoneTransfer:
        description:
            - Override Zone Transfer option in the Catalog zone (Primary, Forwarder only).
        required: false
        type: bool
    overrideCatalogNotify:
        description:
            - Override Notify option in the Catalog zone (Primary, Forwarder only).
        required: false
        type: bool
    primaryNameServerAddresses:
        description:
            - Comma separated IPs or names of the primary name server (Secondary, SecondaryForwarder, SecondaryCatalog, Stub).
        required: false
        type: str
    primaryZoneTransferProtocol:
        description:
            - Zone transfer protocol (Secondary, SecondaryForwarder, SecondaryCatalog). [Tcp, Tls, Quic]
        required: false
        type: str
        choices: [Tcp, Tls, Quic]
    primaryZoneTransferTsigKeyName:
        description:
            - TSIG key name for zone transfer (Secondary, SecondaryForwarder, SecondaryCatalog).
        required: false
        type: str
    validateZone:
        description:
            - Enable ZONEMD validation (Secondary only).
        required: false
        type: bool
    queryAccess:
        description:
            - Query access policy. [Deny, Allow, AllowOnlyPrivateNetworks, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
        required: false
        type: str
        choices: [Deny, Allow, AllowOnlyPrivateNetworks, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
    queryAccessNetworkACL:
        description:
            - Comma separated ACL for query access (not SecondaryCatalog, only with certain queryAccess).
        required: false
        type: str
    zoneTransfer:
        description:
            - Zone transfer policy (Primary, Secondary only). [Deny, Allow, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
        required: false
        type: str
        choices: [Deny, Allow, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
    zoneTransferNetworkACL:
        description:
            - Comma separated ACL for zone transfer (Primary, Secondary, Forwarder, Catalog only, with certain zoneTransfer).
        required: false
        type: str
    zoneTransferTsigKeyNames:
        description:
            - Comma separated TSIG key names for zone transfer (Primary, Secondary, Forwarder, Catalog).
        required: false
        type: str
    notify:
        description:
            - Notify policy. [None, ZoneNameServers, SpecifiedNameServers, BothZoneAndSpecifiedNameServers, SeparateNameServersForCatalogAndMemberZones]
        required: false
        type: str
        choices: [None, ZoneNameServers, SpecifiedNameServers, BothZoneAndSpecifiedNameServers, SeparateNameServersForCatalogAndMemberZones]
    notifyNameServers:
        description:
            - Comma separated IPs to notify (Primary, Secondary, Forwarder, Catalog).
        required: false
        type: str
    notifySecondaryCatalogsNameServers:
        description:
            - Comma separated IPs to notify for catalog updates (Catalog only).
        required: false
        type: str
    update:
        description:
            - Allow dynamic updates (Primary, Secondary, Forwarder). [Deny, Allow, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
        required: false
        type: str
        choices: [Deny, Allow, AllowOnlyZoneNameServers, UseSpecifiedNetworkACL, AllowZoneNameServersAndUseSpecifiedNetworkACL]
    updateNetworkACL:
        description:
            - Comma separated ACL for update (Primary, Secondary, Forwarder, with certain update).
        required: false
        type: str
    updateSecurityPolicies:
        description:
            - Pipe separated table of security policies (Primary, Forwarder only).
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Set options for example.com zone
  technitium_dns_set_zone_options:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    disabled: false
    zoneTransfer: Allow
    notify: ZoneNameServers
  register: result

- debug:
    var: result
'''

class SetZoneOptionsModule(TechnitiumModule):
    argument_spec = dict(
        api_url=dict(type='str', required=True),
        port=dict(type='int', required=False, default=5380),
        api_token=dict(type='str', required=True, no_log=True),
        validate_certs=dict(type='bool', required=False, default=True),
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
        zoneTransferTsigKeyNames=dict(type='str', required=False),
        notify=dict(type='str', required=False, choices=['None', 'ZoneNameServers', 'SpecifiedNameServers', 'BothZoneAndSpecifiedNameServers', 'SeparateNameServersForCatalogAndMemberZones']),
        notifyNameServers=dict(type='str', required=False),
        notifySecondaryCatalogsNameServers=dict(type='str', required=False),
        update=dict(type='str', required=False, choices=['Deny', 'Allow', 'AllowOnlyZoneNameServers', 'UseSpecifiedNetworkACL', 'AllowZoneNameServersAndUseSpecifiedNetworkACL']),
        updateNetworkACL=dict(type='str', required=False),
        updateSecurityPolicies=dict(type='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        params = self.params
        api_url = self.api_url
        port = self.port
        api_token = self.api_token
        zone = params['zone']

        # 1. Fetch current zone options
        get_query = {'zone': zone}
        get_data = self.request('/api/zones/options/get', params=get_query)
        if get_data.get('status') != 'ok':
            error_msg = get_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error (get options): {error_msg}", api_response=get_data)
        current = get_data.get('response', {})
        zone_type = current.get('type')

        # 1b. Conditional parameter validation based on zone type
        allowed_params = {
            'Primary': set(['disabled','catalog','overrideCatalogQueryAccess','overrideCatalogZoneTransfer','overrideCatalogNotify','queryAccess','queryAccessNetworkACL','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers','update','updateNetworkACL','updateSecurityPolicies']),
            'Stub': set(['disabled','catalog','overrideCatalogQueryAccess','primaryNameServerAddresses','validateZone','queryAccess','queryAccessNetworkACL']),
            'Forwarder': set(['disabled','catalog','overrideCatalogQueryAccess','overrideCatalogZoneTransfer','overrideCatalogNotify','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers','update','updateNetworkACL','updateSecurityPolicies']),
            'Secondary': set(['disabled','primaryNameServerAddresses','primaryZoneTransferProtocol','primaryZoneTransferTsigKeyName','validateZone','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers','update','updateNetworkACL']),
            'SecondaryForwarder': set(['disabled','primaryNameServerAddresses','primaryZoneTransferProtocol','primaryZoneTransferTsigKeyName','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers']),
            'SecondaryCatalog': set(['disabled','primaryNameServerAddresses','primaryZoneTransferProtocol','primaryZoneTransferTsigKeyName','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers']),
            'Catalog': set(['disabled','zoneTransfer','zoneTransferNetworkACL','zoneTransferTsigKeyNames','notify','notifyNameServers','notifySecondaryCatalogsNameServers']),
            'SecondaryROOT': set(['disabled']),
        }
        if zone_type in allowed_params:
            for param in params:
                if param in ['api_url','port','api_token','zone']:
                    continue
                if params[param] is not None and param not in allowed_params[zone_type]:
                    self.fail_json(msg=f"Parameter '{param}' is not supported for zone type '{zone_type}'.")

        # 2. Build desired state dict (API param names)
        desired = {}
        for key in [
            'disabled', 'catalog', 'overrideCatalogQueryAccess', 'overrideCatalogZoneTransfer', 'overrideCatalogNotify',
            'primaryNameServerAddresses', 'primaryZoneTransferProtocol', 'primaryZoneTransferTsigKeyName', 'validateZone',
            'queryAccess', 'queryAccessNetworkACL', 'zoneTransfer', 'zoneTransferNetworkACL', 'zoneTransferTsigKeyNames',
            'notify', 'notifyNameServers', 'notifySecondaryCatalogsNameServers', 'update', 'updateNetworkACL', 'updateSecurityPolicies']:
            value = params.get(key)
            if value is not None:
                if isinstance(value, bool):
                    value = str(value).lower()
                if key in ['queryAccessNetworkACL', 'primaryNameServerAddresses', 'zoneTransferNetworkACL'] and isinstance(value, list):
                    value = ",".join(str(x) for x in value)
                desired[key] = value

        # 3. Compare current vs desired (simple string/boolean comparison)
        changed = False
        for k, v in desired.items():
            current_val = current.get(k)
            if isinstance(current_val, bool):
                current_val = str(current_val).lower()
            if isinstance(current_val, list):
                current_val = ",".join(str(x) for x in current_val)
            if isinstance(v, list):
                v = ",".join(str(x) for x in v)
            if current_val != v:
                changed = True
                break

        if not changed:
            self.exit_json(changed=False, msg="Zone options already match desired state.")

        # 4. Set options if needed
        set_query = {'zone': zone}
        set_query.update(desired)
        data = self.request('/api/zones/options/set', params=set_query)
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        self.exit_json(changed=True, msg="Zone options set successfully.", api_response=data)

def main():
    module = SetZoneOptionsModule()
    module()

if __name__ == '__main__':
    main()
