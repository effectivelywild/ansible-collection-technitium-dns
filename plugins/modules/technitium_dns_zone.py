#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_zone
short_description: Manage DNS zones with state-based approach
version_added: "1.0.0"
author: Frank Muise (@effectivelywild)
description:
    - Manage DNS zones in Technitium DNS Server.
    - Supports all zone types with type-specific parameters.
seealso:
    - module: effectivelywild.technitium_dns.technitium_dns_sign_zone
      description: Sign a zone with DNSSEC
    - module: effectivelywild.technitium_dns.technitium_dns_get_zone_info
      description: Get basic zone information
    - module: effectivelywild.technitium_dns.technitium_dns_get_zone_options
      description: Get all configured zone options
    - module: effectivelywild.technitium_dns.technitium_dns_set_zone_options
      description: Set zone options
    - module: effectivelywild.technitium_dns.technitium_dns_enable_zone
      description: Enables a zone
    - module: effectivelywild.technitium_dns.technitium_dns_disable_zone
      description: Disables a zone
options:
    state:
        description:
            - The desired state of the DNS zone
            - C(present) ensures the zone exists with the specified parameters
            - C(absent) ensures the zone does not exist
        choices:
            - present
            - absent
        required: false
        type: str
        default: present
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
    catalog:
        description:
            - The name of the catalog zone to become its member zone
        required: false
        type: str
    node:
        description:
            - The node domain name for which this API call is intended
            - When unspecified, the current node is used
            - This parameter can be used only when Clustering is initialized
        required: false
        type: str
    dnssec:
        description:
            - Enable DNSSEC for the zone
            - When enabled, the zone will be signed with DNSSEC
        required: false
        type: bool
    dnssecValidation:
        description:
            - Enable DNSSEC validation (Forwarder only)
        required: false
        type: bool
    forwarder:
        description:
            - Address of DNS server to use as forwarder (Forwarder only)
        required: false
        type: str
    initializeForwarder:
        description:
            - Initialize Conditional Forwarder zone with FWD record (Forwarder only)
        required: false
        type: bool
    primaryNameServerAddresses:
        description:
            - List of primary name server IP addresses or names (Secondary, SecondaryForwarder, SecondaryCatalog, Stub)
        required: false
        type: list
        elements: str
    protocol:
        description:
            - DNS transport protocol for Conditional Forwarder zone
        required: false
        type: str
        choices: [Udp, Tcp, Tls, Https, Quic]
    proxyAddress:
        description:
            - Proxy server address (Forwarder only)
        required: false
        type: str
    proxyPassword:
        description:
            - Proxy server password (Forwarder only)
        required: false
        type: str
    proxyPort:
        description:
            - Proxy server port (Forwarder only)
        required: false
        type: int
    proxyType:
        description:
            - Proxy type for conditional forwarding (Forwarder only)
        required: false
        type: str
        choices: [NoProxy, DefaultProxy, Http, Socks5]
    proxyUsername:
        description:
            - Proxy server username (Forwarder only)
        required: false
        type: str
    tsigKeyName:
        description:
            - TSIG key name (Secondary, SecondaryForwarder, SecondaryCatalog)
        required: false
        type: str
    type:
        description:
            - The type of zone to be created
            - Required when C(state=present)
        required: false
        type: str
        choices: [Primary, Secondary, Stub, Forwarder, SecondaryForwarder, Catalog, SecondaryCatalog]
    useSoaSerialDateScheme:
        description:
            - Enable using date scheme for SOA serial (Primary, Forwarder, Catalog zones)
        required: false
        type: bool
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests
        required: false
        type: bool
        default: true
    validateZone:
        description:
            - Enable ZONEMD validation (Secondary only)
        required: false
        type: bool
    zone:
        description:
            - The domain name of the zone
        required: true
        type: str
    zoneTransferProtocol:
        description:
            - Zone transfer protocol (Secondary, SecondaryForwarder, SecondaryCatalog)
        required: false
        type: str
        choices: [Tcp, Tls, Quic]
'''

EXAMPLES = r'''
# Basic Primary zone
- name: Ensure Primary zone exists
  effectivelywild.technitium_dns.technitium_dns_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    type: "Primary"
    state: present

# Primary zone with DNSSEC
- name: Create Primary zone with DNSSEC enabled
  effectivelywild.technitium_dns.technitium_dns_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "secure.example.com"
    type: "Primary"
    dnssec: true
    state: present

# Forwarder zone
- name: Create Forwarder zone
  effectivelywild.technitium_dns.technitium_dns_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "forward.example.com"
    type: "Forwarder"
    forwarder: "8.8.8.8"
    initializeForwarder: true
    protocol: "Udp"
    state: present

# Secondary zone
- name: Create Secondary zone
  effectivelywild.technitium_dns.technitium_dns_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "secondary.example.com"
    type: "Secondary"
    primaryNameServerAddresses:
      - "192.0.2.1"
      - "192.0.2.2"
    zoneTransferProtocol: "Tcp"
    state: present

# Delete a zone
- name: Ensure zone is absent
  effectivelywild.technitium_dns.technitium_dns_zone:
    api_url: "http://localhost"
    api_token: "myapitoken"
    zone: "example.com"
    state: absent

# Using with loops
- name: Manage multiple DNS zones
  effectivelywild.technitium_dns.technitium_dns_zone:
    api_url: "https://{{ dnsserver_domain }}"
    api_token: "{{ api_token }}"
    zone: "{{ item.zone }}"
    type: "{{ item.type }}"
    state: "{{ item.state | default('present') }}"
  loop: "{{ dns_zones }}"
  loop_control:
    label: "{{ item.zone }}"
'''

RETURN = r'''
api_response:
    description: The raw response from the Technitium DNS API.
    type: dict
    returned: always
    contains:
        response:
            description: The core data payload from the API.
            type: dict
            returned: always
        status:
            description: API response status.
            type: str
            returned: always
            sample: "ok"
changed:
    description: A boolean indicating if the module made changes to the system.
    returned: always
    type: bool
failed:
    description: A boolean indicating if the module failed.
    returned: always
    type: bool
msg:
    description: A message indicating the result of the operation.
    returned: always
    type: str
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class ZoneModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        state=dict(type='str', required=False, default='present', choices=['present', 'absent']),
        zone=dict(type='str', required=True),
        node=dict(type='str', required=False),
        type=dict(type='str', required=False, choices=[
                  "Primary", "Secondary", "Stub", "Forwarder", "SecondaryForwarder", "Catalog", "SecondaryCatalog"]),
        catalog=dict(type='str', required=False),
        dnssec=dict(type='bool', required=False),
        useSoaSerialDateScheme=dict(type='bool', required=False),
        primaryNameServerAddresses=dict(
            type='list', elements='str', required=False),
        zoneTransferProtocol=dict(type='str', required=False, choices=[
                                  "Tcp", "Tls", "Quic"]),
        tsigKeyName=dict(type='str', required=False, no_log=True),
        validateZone=dict(type='bool', required=False),
        initializeForwarder=dict(type='bool', required=False),
        protocol=dict(type='str', required=False, choices=[
                      "Udp", "Tcp", "Tls", "Https", "Quic"]),
        forwarder=dict(type='str', required=False),
        dnssecValidation=dict(type='bool', required=False),
        proxyType=dict(type='str', required=False, choices=[
                       "NoProxy", "DefaultProxy", "Http", "Socks5"]),
        proxyAddress=dict(type='str', required=False),
        proxyPort=dict(type='int', required=False),
        proxyUsername=dict(type='str', required=False),
        proxyPassword=dict(type='str', required=False, no_log=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        state = params['state']
        zone = params['zone']

        # Validate that type is provided when state=present
        if state == 'present' and not params.get('type'):
            self.fail_json(msg="Parameter 'type' is required when state=present")

        if state == 'present':
            self._ensure_present()
        else:
            self._ensure_absent()

    def _ensure_present(self):
        """Ensure the zone exists with the specified configuration."""
        params = self.params
        zone = params['zone']
        zone_type = params['type']

        # Check if zone already exists
        zone_exists, existing_zone = self._zone_exists(zone)

        if zone_exists:
            # Zone exists - check if it matches desired state
            # For now, we'll consider the zone as already present
            # Future enhancement: update zone options if they differ
            self.exit_json(
                changed=False,
                msg=f"Zone '{zone}' already exists.",
                api_response={'status': 'ok'}
            )
        else:
            # Zone doesn't exist - create it
            if self.check_mode:
                self.exit_json(
                    changed=True,
                    msg=f"Zone '{zone}' would be created (check mode)",
                    api_response={}
                )

            self._create_zone()

    def _ensure_absent(self):
        """Ensure the zone does not exist."""
        zone = self.params['zone']

        # Check if the zone exists
        zone_exists, existing_zone = self._zone_exists(zone)

        if not zone_exists:
            # Zone doesn't exist - already in desired state
            self.exit_json(
                changed=False,
                msg=f"Zone '{zone}' does not exist.",
                api_response={'status': 'ok'}
            )
        else:
            # Zone exists - delete it
            if self.check_mode:
                self.exit_json(
                    changed=True,
                    msg=f"Zone '{zone}' would be deleted (check mode)",
                    api_response={}
                )

            self._delete_zone()

    def _zone_exists(self, zone, node=None):
        """Check if a zone exists.

        Returns:
            tuple: (exists: bool, zone_data: dict or None)
        """
        node = node or self.params.get('node')
        zone_check_query = {'zone': zone}
        if node:
            zone_check_query['node'] = node
        zone_check_data = self.request('/api/zones/options/get', params=zone_check_query)

        if zone_check_data.get('status') == 'ok':
            return True, zone_check_data.get('response', {})
        else:
            error_msg = zone_check_data.get('errorMessage', '')
            if 'No such zone was found' in error_msg:
                return False, None
            if 'No such node exists' in error_msg:
                self.fail_json(
                    msg=f"Invalid node parameter: {error_msg}",
                    api_response=zone_check_data
                )
            else:
                # Unexpected API error
                self.fail_json(
                    msg=f"Technitium API error checking zone: {error_msg}",
                    api_response=zone_check_data
                )

    def _create_zone(self):
        """Create a new zone."""
        params = self.params
        zone = params['zone']
        zone_type = params['type']

        # Validate parameters based on zone type
        self._validate_zone_type_parameters(zone_type)

        # Build query parameters for zone creation
        query_params = self._build_create_query()

        # Create the zone
        data = self.request('/api/zones/create', params=query_params, method='POST')

        if data.get('status') == 'ok':
            # Check if DNSSEC should be enabled
            if params.get('dnssec'):
                self._sign_zone(zone, node=params.get('node'))

            self.exit_json(
                changed=True,
                msg=f"Zone '{zone}' created.",
                api_response=data
            )
        else:
            self.fail_json(
                msg=f"Failed to create zone '{zone}': {data.get('errorMessage', 'Unknown error')}",
                api_response=data
            )

    def _delete_zone(self):
        """Delete a zone."""
        zone = self.params['zone']
        node = self.params.get('node')

        delete_params = {'zone': zone}
        if node:
            delete_params['node'] = node

        data = self.request('/api/zones/delete', params=delete_params, method='POST')

        if data.get('status') == 'ok':
            self.exit_json(
                changed=True,
                msg=f"Zone '{zone}' deleted.",
                api_response=data
            )
        else:
            self.fail_json(
                msg=f"Failed to delete zone '{zone}': {data.get('errorMessage', 'Unknown error')}",
                api_response=data
            )

    def _sign_zone(self, zone, node=None):
        """Sign a zone with DNSSEC using default settings."""
        sign_params = {
            'zone': zone,
            'algorithm': 'RSA',
            'hashAlgorithm': 'SHA256',
            'kskKeySize': 2048,
            'zskKeySize': 1024,
            'dnsKeyTtl': 86400
        }
        if node:
            sign_params['node'] = node
        sign_data = self.request('/api/zones/dnssec/sign', params=sign_params, method='POST')

        if sign_data.get('status') != 'ok':
            self.fail_json(
                msg=f"Zone '{zone}' created but failed to sign with DNSSEC: {sign_data.get('errorMessage', 'Unknown error')}",
                api_response=sign_data
            )

    def _validate_zone_type_parameters(self, zone_type):
        """Validate that only appropriate parameters are provided for the zone type."""
        params = self.params

        # Define allowed parameters for each zone type
        common_params = {
            'api_url', 'api_port', 'api_token', 'validate_certs', 'zone', 'node', 'type', 'state', 'dnssec'
        }

        allowed_params = {
            'Primary': common_params | {'catalog', 'useSoaSerialDateScheme'},
            'Forwarder': common_params | {'catalog', 'useSoaSerialDateScheme', 'initializeForwarder',
                                          'protocol', 'forwarder', 'dnssecValidation', 'proxyType',
                                          'proxyAddress', 'proxyPort', 'proxyUsername', 'proxyPassword'},
            'Secondary': common_params | {'primaryNameServerAddresses', 'zoneTransferProtocol',
                                          'tsigKeyName', 'validateZone'},
            'Stub': common_params | {'primaryNameServerAddresses'},
            'SecondaryForwarder': common_params | {'primaryNameServerAddresses', 'zoneTransferProtocol', 'tsigKeyName'},
            'Catalog': common_params | {'useSoaSerialDateScheme'},
            'SecondaryCatalog': common_params | {'primaryNameServerAddresses', 'zoneTransferProtocol', 'tsigKeyName'}
        }

        if zone_type not in allowed_params:
            self.fail_json(msg=f"Invalid zone type: {zone_type}")

        # Check for unsupported parameters
        provided_params = {k for k, v in params.items() if v is not None}
        unsupported = provided_params - allowed_params[zone_type]

        if unsupported:
            self.fail_json(
                msg=f"Unsupported parameters for {zone_type} zone type: {', '.join(unsupported)}"
            )

    def _build_create_query(self):
        """Build query parameters for zone creation."""
        params = self.params
        query = {
            'zone': params['zone'],
            'type': params['type']
        }

        if params.get('node'):
            query['node'] = params['node']

        # Add optional parameters if provided
        optional_params = [
            'catalog', 'useSoaSerialDateScheme', 'primaryNameServerAddresses',
            'zoneTransferProtocol', 'tsigKeyName', 'validateZone',
            'initializeForwarder', 'protocol', 'forwarder', 'dnssecValidation',
            'proxyType', 'proxyAddress', 'proxyPort', 'proxyUsername', 'proxyPassword'
        ]

        for param in optional_params:
            if params.get(param) is not None:
                value = params[param]
                # Convert list to comma-separated string for primaryNameServerAddresses
                if param == 'primaryNameServerAddresses' and isinstance(value, list):
                    value = ','.join(value)
                query[param] = value

        return query


def main():
    module = ZoneModule()
    module.run()


if __name__ == '__main__':
    main()
