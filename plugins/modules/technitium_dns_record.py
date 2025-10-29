#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_record
short_description: Manage DNS records with state-based approach
version_added: "1.0.0"
author: Frank Muise (@effectivelywild)
description:
    - Manage DNS records using Ansible's standard state pattern (present/absent).
    - This module consolidates the functionality of technitium_dns_add_record and technitium_dns_delete_record.
    - Provides idempotent operations with proper check mode support.
    - The module supports all DNS record types.
    - Some parameters are only valid or required for specific record types.
    - For example, C(ipAddress) is required for A and AAAA records, while C(cname) is required for CNAME records.
    - "B(Important): Some record types (APP, CNAME, DNAME) are singleton records and only allow one record per DNS name.
      If you provide multiple records in the C(records) list for these types, the module will fail with a clear error message."
seealso:
    - module: effectivelywild.technitium_dns.technitium_dns_add_record
      description: Legacy module for adding DNS records
    - module: effectivelywild.technitium_dns.technitium_dns_delete_record
      description: Legacy module for deleting DNS records
    - module: effectivelywild.technitium_dns.technitium_dns_get_record
      description: Used to get DNS record details
options:
    state:
        description:
            - The desired state of the DNS record.
            - C(present) ensures the record exists with the specified parameters.
            - C(absent) ensures the record does not exist.
        choices:
            - present
            - absent
        required: false
        type: str
        default: present
    algorithm:
        description:
            - Algorithm (DS only)
        choices:
            - RSAMD5
            - DSA
            - RSASHA1
            - DSA-NSEC3-SHA1
            - RSASHA1-NSEC3-SHA1
            - RSASHA256
            - RSASHA512
            - ECC-GOST
            - ECDSAP256SHA256
            - ECDSAP384SHA384
            - ED25519
            - ED448
        required: false
        type: str
    aname:
        description:
            - ANAME target (ANAME only)
        required: false
        type: str
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
    appName:
        description:
            - Application name (APP only)
        required: false
        type: str
    autoIpv4Hint:
        description:
            - Automatic IPv4 hint (SVCB and HTTPS only)
        required: false
        type: bool
    autoIpv6Hint:
        description:
            - Automatic IPv6 hint (SVCB and HTTPS only)
        required: false
        type: bool
    classPath:
        description:
            - Class path (APP only)
        required: false
        type: str
    cname:
        description:
            - CNAME target (CNAME only)
        required: false
        type: str
    comments:
        description:
            - Comments for the record
        required: false
        type: str
    createPtrZone:
        description:
            - Create reverse zone for PTR (A/AAAA only)
        required: false
        type: bool
    digest:
        description:
            - Digest (DS and SSHFP only)
        required: false
        type: str
    digestType:
        description:
            - Digest type (DS and SSHFP only)
        choices:
            - SHA1
            - SHA256
            - GOST-R-34-11-94
            - SHA384
        required: false
        type: str
    dname:
        description:
            - DNAME target (DNAME only)
        required: false
        type: str
    dnssecValidation:
        description:
            - DNSSEC validation flag (FWD only)
        required: false
        type: bool
    exchange:
        description:
            - MX exchange domain (MX only)
        required: false
        type: str
    expiryTtl:
        description:
            - Expiry in seconds for auto-deletion
        required: false
        type: int
    flags:
        description:
            - Flags (CAA only)
        required: false
        type: str
    forwarder:
        description:
            - Forwarder address (FWD only)
        required: false
        type: str
    forwarderPriority:
        description:
            - Forwarder priority (FWD only)
        required: false
        type: int
    glue:
        description:
            - Glue address (NS only)
        required: false
        type: str
    ipAddress:
        description:
            - IP address (A/AAAA only)
        required: false
        type: str
    keyTag:
        description:
            - Key tag (DS only)
        required: false
        type: int
    mailbox:
        description:
            - Responsible mailbox (MX only)
        required: false
        type: str
    name:
        description:
            - The record name (e.g., test.example.com)
        required: true
        aliases:
            - domain
        type: str
    nameServer:
        description:
            - Name server domain (NS only)
        required: false
        type: str
    naptrFlags:
        description:
            - Flags (NAPTR only)
        required: false
        type: str
    naptrOrder:
        description:
            - Order (NAPTR only)
        required: false
        type: int
    naptrPreference:
        description:
            - Preference (NAPTR only)
        required: false
        type: int
    naptrRegexp:
        description:
            - Regular expression (NAPTR only)
        required: false
        type: str
    naptrReplacement:
        description:
            - Replacement string (NAPTR only)
        required: false
        type: str
    naptrServices:
        description:
            - Services (NAPTR only)
        required: false
        type: str
    overwrite:
        description:
            - Overwrite existing record set for this type (only applies to state=present)
        required: false
        type: bool
        default: false
    preference:
        description:
            - MX preference (MX only)
        required: false
        type: int
    priority:
        description:
            - Priority (SRV only)
        required: false
        type: int
    protocol:
        description:
            - Protocol (FWD only)
        choices:
            - Udp
            - Tcp
            - Tls
            - Https
            - Quic
        required: false
        type: str
    proxyAddress:
        description:
            - Proxy address (FWD only)
        required: false
        type: str
    proxyPassword:
        description:
            - Proxy password (FWD only)
        required: false
        type: str
    proxyPort:
        description:
            - Proxy port (FWD only)
        required: false
        type: int
    proxyType:
        description:
            - Proxy type (FWD only)
        choices:
            - NoProxy
            - DefaultProxy
            - Http
            - Socks5
        required: false
        type: str
    proxyUsername:
        description:
            - Proxy username (FWD only)
        required: false
        type: str
    ptr:
        description:
            - Add reverse PTR record (A/AAAA only)
        required: false
        type: bool
    ptrName:
        description:
            - PTR domain name (PTR only)
        required: false
        type: str
    rdata:
        description:
            - Used for adding unknown i.e. unsupported record types (UNKNOWN Only)
            - The value must be formatted as a hex string or a colon separated hex string
        required: false
        type: str
    recordData:
        description:
            - Record data (APP only)
        required: false
        type: str
    splitText:
        description:
            - Split TXT into multiple strings (TXT only)
        required: false
        type: bool
    sshfpAlgorithm:
        description:
            - SSHFP algorithm (SSHFP only)
        choices:
            - RSA
            - DSA
            - ECDSA
            - Ed25519
            - Ed448
        required: false
        type: str
    sshfpFingerprint:
        description:
            - SSHFP fingerprint (SSHFP only)
        required: false
        type: str
    sshfpFingerprintType:
        description:
            - SSHFP fingerprint type (SSHFP only)
        choices:
            - SHA1
            - SHA256
        required: false
        type: str
    srv_port:
        description:
            - Port (SRV only)
        required: false
        type: int
    svcParams:
        description:
            - SVCB/HTTPS parameters (SVCB and HTTPS only)
        required: false
        type: str
    svcPriority:
        description:
            - SVCB/HTTPS priority (SVCB and HTTPS only)
        required: false
        type: int
    svcTargetName:
        description:
            - SVCB/HTTPS target name (SVCB and HTTPS only)
        required: false
        type: str
    tag:
        description:
            - Tag (CAA only)
        required: false
        type: str
    target:
        description:
            - Target (SRV only)
        required: false
        type: str
    text:
        description:
            - TXT record text (TXT only)
        required: false
        type: str
    tlsaCertificateAssociationData:
        description:
            - TLSA certificate association data (TLSA only)
        required: false
        type: str
    tlsaCertificateUsage:
        description:
            - TLSA certificate usage (TLSA only)
        choices:
            - PKIX-TA
            - PKIX-EE
            - DANE-TA
            - DANE-EE
        required: false
        type: str
    tlsaMatchingType:
        description:
            - TLSA matching type (TLSA only)
        choices:
            - Full
            - SHA2-256
            - SHA2-512
        required: false
        type: str
    tlsaSelector:
        description:
            - TLSA selector (TLSA only)
        choices:
            - Cert
            - SPKI
        required: false
        type: str
    ttl:
        description:
            - TTL for the record in seconds
        required: false
        type: int
    txtDomain:
        description:
            - Domain for TXT record (if different from the main domain, TXT only)
        required: false
        type: str
    type:
        description:
            - The DNS record type
        choices:
            - A
            - AAAA
            - ANAME
            - APP
            - CNAME
            - CAA
            - DNAME
            - DS
            - FWD
            - HTTPS
            - MX
            - NAPTR
            - NS
            - PTR
            - SSHFP
            - SRV
            - SVCB
            - TLSA
            - TXT
            - UNKNOWN
            - URI
        required: true
        type: str
    updateSvcbHints:
        description:
            - Update SVCB/HTTPS hints (A/AAAA only)
        required: false
        type: bool
    uri:
        description:
            - URI target (URI only)
        required: false
        type: str
    uriPriority:
        description:
            - URI priority (URI only)
        required: false
        type: int
    uriWeight:
        description:
            - URI weight (URI only)
        required: false
        type: int
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests
            - Set to false to disable SSL certificate validation
        required: false
        type: bool
        default: true
    value:
        description:
            - Value (CAA only)
        required: false
        type: str
    weight:
        description:
            - Weight (SRV only)
        required: false
        type: int
    zone:
        description:
            - The authoritative zone name (optional, defaults to closest match)
        required: false
        type: str
'''

EXAMPLES = r'''
# Basic A record - ensure present
- name: Ensure A record exists
  effectivelywild.technitium_dns.technitium_dns_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "www.example.com"
    type: "A"
    ipAddress: "192.0.2.1"
    ttl: 3600
    state: present

# Basic A record - ensure absent
- name: Ensure A record is removed
  effectivelywild.technitium_dns.technitium_dns_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "www.example.com"
    type: "A"
    ipAddress: "192.0.2.1"
    state: absent

# Using with loops - much cleaner than before!
- name: Manage multiple DNS records
  effectivelywild.technitium_dns.technitium_dns_record:
    api_url: "https://{{ dnsserver_domain }}"
    api_token: "{{ api_token }}"
    zone: "{{ item.zone }}"
    name: "{{ item.domain }}"
    type: "{{ item.type }}"
    ipAddress: "{{ item.ipAddress }}"
    ttl: "{{ item.ttl }}"
    comments: "{{ item.comments }}"
    state: "{{ item.state | default('present') }}"
  loop: "{{ dnsserver_records }}"
  loop_control:
    label: "{{ item.domain }}"

# CNAME record
- name: Ensure CNAME record exists
  effectivelywild.technitium_dns.technitium_dns_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "alias.example.com"
    zone: "example.com"
    type: "CNAME"
    cname: "www.example.com"
    ttl: 3600
    state: present

# MX record
- name: Ensure MX record exists
  effectivelywild.technitium_dns.technitium_dns_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    zone: "example.com"
    type: "MX"
    exchange: "mail.example.com"
    preference: 10
    ttl: 3600
    state: present

# TXT record with overwrite
- name: Ensure TXT record exists (overwrite if different)
  effectivelywild.technitium_dns.technitium_dns_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    zone: "example.com"
    type: "TXT"
    text: "v=spf1 include:_spf.google.com ~all"
    ttl: 3600
    overwrite: true
    state: present

# A record with PTR
- name: Ensure A record with reverse PTR exists
  effectivelywild.technitium_dns.technitium_dns_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "server.example.com"
    zone: "example.com"
    type: "A"
    ipAddress: "192.0.2.10"
    ptr: true
    createPtrZone: true
    ttl: 3600
    state: present

# Using check mode
- name: Check what would change
  effectivelywild.technitium_dns.technitium_dns_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "test.example.com"
    type: "A"
    ipAddress: "192.0.2.99"
    ttl: 300
    state: present
  check_mode: true
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
            returned: when state=present
            contains:
                addedRecord:
                    description: The details of the record that was added or modified.
                    type: dict
                    returned: when state=present
                    contains:
                        disabled:
                            description: Whether the record is disabled.
                            type: bool
                            returned: always
                        name:
                            description: The full domain name of the record.
                            type: str
                            returned: always
                        rData:
                            description: The data specific to the record type.
                            type: dict
                            returned: always
                        ttl:
                            description: The record's TTL in seconds.
                            type: int
                            returned: always
                        type:
                            description: The type of the DNS record.
                            type: str
                            returned: always
        status:
            description: The status of the API request.
            type: str
            returned: always
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

# Parameter mappings for the update API endpoint
# Each record type defines how parameters map for updates:
# - 'current': Maps user params to rData fields (identifies the record)
# - 'new': Maps user params to API 'new*' parameters (what to update)
# - 'direct': Parameters passed directly to API without 'new' prefix
UPDATE_PARAM_MAPPINGS = {
    'A': {
        'current': {'ipAddress': 'ipAddress'},
        'new': {'ipAddress': 'newIpAddress'},
        'direct': ['ptr', 'createPtrZone', 'updateSvcbHints']
    },
    'AAAA': {
        'current': {'ipAddress': 'ipAddress'},
        'new': {'ipAddress': 'newIpAddress'},
        'direct': ['ptr', 'createPtrZone', 'updateSvcbHints']
    },
    'MX': {
        'current': {'exchange': 'exchange', 'preference': 'preference'},
        'new': {'exchange': 'newExchange', 'preference': 'newPreference'},
        'direct': []
    },
    'TXT': {
        'current': {'text': 'text', 'splitText': 'splitText'},
        'new': {'text': 'newText', 'splitText': 'newSplitText'},
        'direct': []
    },
    'CNAME': {
        'current': {'cname': 'cname'},
        'new': {'cname': 'cname'},  # CNAME doesn't use 'new' prefix
        'direct': []
    },
    'NS': {
        'current': {'nameServer': 'nameServer'},
        'new': {'nameServer': 'newNameServer'},
        'direct': ['glue']
    },
}

# Common parameters updated directly for all record types
# Note: 'comments' is not included here because the GET API doesn't return it,
# so we can't reliably check for changes. Comments will still be updated when
# other fields change, but won't trigger updates on their own.
COMMON_UPDATE_PARAMS = ['ttl', 'expiryTtl']

# Record type schemas define the structure for each DNS record type
# Used for normalization, validation, and identifying records within a set
RECORD_SCHEMAS = {
    'A': {
        'required_fields': ['ipAddress'],
        'optional_fields': ['ptr', 'createPtrZone', 'updateSvcbHints'],
        'identifying_fields': ['ipAddress'],
        'shorthand_primary': 'ipAddress'
    },
    'AAAA': {
        'required_fields': ['ipAddress'],
        'optional_fields': ['ptr', 'createPtrZone', 'updateSvcbHints'],
        'identifying_fields': ['ipAddress'],
        'shorthand_primary': 'ipAddress'
    },
    'NS': {
        'required_fields': ['nameServer'],
        'optional_fields': ['glue'],
        'identifying_fields': ['nameServer'],
        'shorthand_primary': 'nameServer'
    },
    'CNAME': {
        'required_fields': ['cname'],
        'optional_fields': [],
        'identifying_fields': ['cname'],
        'shorthand_primary': 'cname'
    },
    'PTR': {
        'required_fields': ['ptrName'],
        'optional_fields': [],
        'identifying_fields': ['ptrName'],
        'shorthand_primary': 'ptrName'
    },
    'MX': {
        'required_fields': ['exchange', 'preference'],
        'optional_fields': [],
        'identifying_fields': ['exchange', 'preference'],
        'shorthand_required': ['exchange', 'preference']
    },
    'TXT': {
        'required_fields': ['text'],
        'optional_fields': ['splitText'],
        'identifying_fields': ['text'],
        'shorthand_primary': 'text'
    },
    'SRV': {
        'required_fields': ['priority', 'weight', 'srv_port', 'target'],
        'optional_fields': [],
        'identifying_fields': ['priority', 'weight', 'srv_port', 'target'],
        'shorthand_required': ['priority', 'weight', 'srv_port', 'target']
    },
    'NAPTR': {
        'required_fields': ['naptrOrder', 'naptrPreference', 'naptrFlags', 'naptrServices', 'naptrRegexp', 'naptrReplacement'],
        'optional_fields': [],
        'identifying_fields': ['naptrOrder', 'naptrPreference', 'naptrFlags', 'naptrServices', 'naptrRegexp', 'naptrReplacement'],
        'shorthand_required': ['naptrOrder', 'naptrPreference', 'naptrFlags', 'naptrServices', 'naptrRegexp', 'naptrReplacement']
    },
    'DNAME': {
        'required_fields': ['dname'],
        'optional_fields': [],
        'identifying_fields': ['dname'],
        'shorthand_primary': 'dname'
    },
    'DS': {
        'required_fields': ['keyTag', 'algorithm', 'digestType', 'digest'],
        'optional_fields': [],
        'identifying_fields': ['keyTag', 'algorithm', 'digestType', 'digest'],
        'shorthand_required': ['keyTag', 'algorithm', 'digestType', 'digest']
    },
    'SSHFP': {
        'required_fields': ['sshfpAlgorithm', 'sshfpFingerprintType', 'sshfpFingerprint'],
        'optional_fields': [],
        'identifying_fields': ['sshfpAlgorithm', 'sshfpFingerprintType', 'sshfpFingerprint'],
        'shorthand_required': ['sshfpAlgorithm', 'sshfpFingerprintType', 'sshfpFingerprint']
    },
    'TLSA': {
        'required_fields': ['tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData'],
        'optional_fields': [],
        'identifying_fields': ['tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData'],
        'shorthand_required': ['tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData']
    },
    'SVCB': {
        'required_fields': ['svcPriority', 'svcTargetName'],
        'optional_fields': ['svcParams', 'autoIpv4Hint', 'autoIpv6Hint'],
        'identifying_fields': ['svcPriority', 'svcTargetName'],
        'shorthand_required': ['svcPriority', 'svcTargetName']
    },
    'HTTPS': {
        'required_fields': ['svcPriority', 'svcTargetName'],
        'optional_fields': ['svcParams', 'autoIpv4Hint', 'autoIpv6Hint'],
        'identifying_fields': ['svcPriority', 'svcTargetName'],
        'shorthand_required': ['svcPriority', 'svcTargetName']
    },
    'URI': {
        'required_fields': ['uriPriority', 'uriWeight', 'uri'],
        'optional_fields': [],
        'identifying_fields': ['uriPriority', 'uriWeight', 'uri'],
        'shorthand_required': ['uriPriority', 'uriWeight', 'uri']
    },
    'CAA': {
        'required_fields': ['flags', 'tag', 'value'],
        'optional_fields': [],
        'identifying_fields': ['flags', 'tag', 'value'],
        'shorthand_required': ['flags', 'tag', 'value']
    },
    'ANAME': {
        'required_fields': ['aname'],
        'optional_fields': [],
        'identifying_fields': ['aname'],
        'shorthand_primary': 'aname'
    },
    'FWD': {
        'required_fields': ['protocol', 'forwarder'],
        'optional_fields': ['forwarderPriority', 'dnssecValidation', 'proxyType', 'proxyAddress', 'proxyPort', 'proxyUsername', 'proxyPassword'],
        'identifying_fields': ['protocol', 'forwarder'],
        'shorthand_required': ['protocol', 'forwarder']
    },
    'APP': {
        'required_fields': ['appName', 'classPath'],
        'optional_fields': ['recordData'],
        'identifying_fields': ['appName', 'classPath'],
        'shorthand_required': ['appName', 'classPath']
    },
    'UNKNOWN': {
        'required_fields': ['rdata'],
        'optional_fields': [],
        'identifying_fields': ['rdata'],
        'shorthand_primary': 'rdata'
    }
}

# Singleton record types: DNS record types that only allow one record per DNS name
# "Singleton" is DNS terminology used in BIND and other DNS software
# See: RFC 1034 Section 3.6.2 for CNAME restrictions
SINGLETON_RECORD_TYPES = {
    'APP',      # Technitium-specific: Only one APP record per DNS name
    'CNAME',    # DNS standard (RFC 1034): CNAME must be the only record at a name
    'DNAME',    # DNS standard (RFC 6672): Similar to CNAME, delegation name
}


class RecordModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True, aliases=['domain']),
        zone=dict(type='str', required=False),
        type=dict(type='str', required=True, choices=[
            'A', 'AAAA', 'NS', 'CNAME', 'PTR', 'MX', 'TXT', 'SRV', 'NAPTR', 'DNAME', 'DS', 'SSHFP', 'TLSA', 'SVCB',
            'HTTPS', 'URI', 'CAA', 'ANAME', 'FWD', 'APP', 'UNKNOWN'
        ]),
        state=dict(type='str', required=False, default='present', choices=['present', 'absent']),
        ttl=dict(type='int', required=False),
        overwrite=dict(type='bool', required=False, default=True),  # v1.0.0: default=True for declarative behavior
        comments=dict(type='str', required=False),
        expiryTtl=dict(type='int', required=False),
        # New v1.0.0: records list for managing record sets
        records=dict(type='list', elements='dict', required=False),
        # Legacy shorthand parameters (auto-converted to records list)
        ipAddress=dict(type='str', required=False),
        ptr=dict(type='bool', required=False),
        createPtrZone=dict(type='bool', required=False),
        updateSvcbHints=dict(type='bool', required=False),
        nameServer=dict(type='str', required=False),
        glue=dict(type='str', required=False),
        cname=dict(type='str', required=False),
        ptrName=dict(type='str', required=False),
        exchange=dict(type='str', required=False),
        preference=dict(type='int', required=False),
        text=dict(type='str', required=False),
        splitText=dict(type='bool', required=False),
        mailbox=dict(type='str', required=False),
        txtDomain=dict(type='str', required=False),
        priority=dict(type='int', required=False),
        weight=dict(type='int', required=False),
        srv_port=dict(type='int', required=False),
        target=dict(type='str', required=False),
        naptrOrder=dict(type='int', required=False),
        naptrPreference=dict(type='int', required=False),
        naptrFlags=dict(type='str', required=False),
        naptrServices=dict(type='str', required=False),
        naptrRegexp=dict(type='str', required=False),
        naptrReplacement=dict(type='str', required=False),
        dname=dict(type='str', required=False),
        keyTag=dict(type='int', required=False, no_log=True),
        algorithm=dict(type='str', required=False, choices=[
            'RSAMD5', 'DSA', 'RSASHA1', 'DSA-NSEC3-SHA1', 'RSASHA1-NSEC3-SHA1', 'RSASHA256', 'RSASHA512',
            'ECC-GOST', 'ECDSAP256SHA256', 'ECDSAP384SHA384', 'ED25519', 'ED448'
        ]),
        digestType=dict(type='str', required=False, choices=[
            'SHA1', 'SHA256', 'GOST-R-34-11-94', 'SHA384'
        ]),
        digest=dict(type='str', required=False),
        sshfpAlgorithm=dict(type='str', required=False, choices=[
            'RSA', 'DSA', 'ECDSA', 'Ed25519', 'Ed448'
        ]),
        sshfpFingerprintType=dict(type='str', required=False, choices=[
            'SHA1', 'SHA256'
        ]),
        sshfpFingerprint=dict(type='str', required=False),
        tlsaCertificateUsage=dict(type='str', required=False, choices=[
            'PKIX-TA', 'PKIX-EE', 'DANE-TA', 'DANE-EE'
        ]),
        tlsaSelector=dict(type='str', required=False, choices=[
            'Cert', 'SPKI'
        ]),
        tlsaMatchingType=dict(type='str', required=False, choices=[
            'Full', 'SHA2-256', 'SHA2-512'
        ]),
        tlsaCertificateAssociationData=dict(type='str', required=False),
        svcPriority=dict(type='int', required=False),
        svcTargetName=dict(type='str', required=False),
        svcParams=dict(type='str', required=False),
        autoIpv4Hint=dict(type='bool', required=False),
        autoIpv6Hint=dict(type='bool', required=False),
        uriPriority=dict(type='int', required=False),
        uriWeight=dict(type='int', required=False),
        uri=dict(type='str', required=False),
        flags=dict(type='str', required=False),
        tag=dict(type='str', required=False),
        value=dict(type='str', required=False),
        aname=dict(type='str', required=False),
        protocol=dict(type='str', required=False, choices=[
            'Udp', 'Tcp', 'Tls', 'Https', 'Quic'
        ]),
        forwarder=dict(type='str', required=False),
        forwarderPriority=dict(type='int', required=False),
        dnssecValidation=dict(type='bool', required=False),
        proxyType=dict(type='str', required=False, choices=[
            'NoProxy', 'DefaultProxy', 'Http', 'Socks5'
        ]),
        proxyAddress=dict(type='str', required=False),
        proxyPort=dict(type='int', required=False),
        proxyUsername=dict(type='str', required=False),
        proxyPassword=dict(type='str', required=False, no_log=True),
        appName=dict(type='str', required=False),
        classPath=dict(type='str', required=False),
        recordData=dict(type='str', required=False),
        rdata=dict(type='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        state = params['state']
        record_type = params['type'].upper()

        # Normalize records to list format (handles shorthand conversion)
        normalized_records, set_params = self._normalize_records(record_type, params)

        # Store normalized data back in params
        params['_normalized_records'] = normalized_records
        params['_set_params'] = set_params

        # Validate parameters for the record type
        self._validate_parameters(record_type, params)

        # Route to appropriate handler based on state
        if state == 'present':
            self._ensure_present(record_type, params)
        elif state == 'absent':
            self._ensure_absent(record_type, params)

    def _normalize_records(self, record_type, params):
        """
        Convert shorthand single-record parameters to records list format.

        Args:
            record_type: The DNS record type (A, MX, etc.)
            params: Module parameters

        Returns:
            tuple: (records_list, set_level_params)
                - records_list: List of record dictionaries
                - set_level_params: Dict of set-level parameters (ttl, comments, etc.)
        """
        # Extract set-level parameters
        set_params = {
            'ttl': params.get('ttl'),
            'comments': params.get('comments'),
            'expiryTtl': params.get('expiryTtl'),
            'overwrite': params.get('overwrite')
        }
        # Remove None values
        set_params = {k: v for k, v in set_params.items() if v is not None}

        # Check for conflicting parameter usage (records vs shorthand)
        if params.get('records') and record_type in RECORD_SCHEMAS:
            schema = RECORD_SCHEMAS[record_type]
            # Check if any record-specific shorthand parameters are also provided
            conflicting_params = []
            for field in schema['required_fields'] + schema['optional_fields']:
                if params.get(field) is not None:
                    conflicting_params.append(field)

            if conflicting_params:
                self.fail_json(
                    msg=f"Cannot use both 'records' parameter and shorthand parameters. "
                        f"Found both 'records' and: {', '.join(conflicting_params)}. "
                        f"Use either 'records' list OR shorthand parameters, not both."
                )

        # If 'records' provided, use it directly
        if params.get('records'):
            records = params['records']
            # Validate each record has required fields and no invalid fields
            if record_type in RECORD_SCHEMAS:
                schema = RECORD_SCHEMAS[record_type]
                valid_fields = set(schema['required_fields'] + schema['optional_fields'])

                for idx, record in enumerate(records):
                    # Check for required fields
                    for req_field in schema['required_fields']:
                        if req_field not in record or record[req_field] is None:
                            self.fail_json(
                                msg=f"Record {idx} missing required field '{req_field}' for {record_type} record"
                            )

                    # Check for invalid/unsupported fields
                    record_fields = set(record.keys())
                    invalid_fields = record_fields - valid_fields
                    if invalid_fields:
                        self.fail_json(
                            msg=f"Record {idx} contains unsupported field(s) for {record_type} record: {', '.join(sorted(invalid_fields))}"
                        )

            # Check for singleton record type violations
            if record_type in SINGLETON_RECORD_TYPES and len(records) > 1:
                self.fail_json(
                    msg=f"{record_type} records only support one record per DNS name. "
                        f"You provided {len(records)} records in the 'records' list. "
                        f"{record_type} is a singleton record type and cannot have multiple records with the same name."
                )

            return records, set_params

        # Otherwise, build from record-type-specific shorthand parameters
        if record_type not in RECORD_SCHEMAS:
            return [], set_params

        schema = RECORD_SCHEMAS[record_type]
        record_data = {}

        # Collect all required and optional fields from params
        for field in schema['required_fields'] + schema['optional_fields']:
            if field in params and params[field] is not None:
                record_data[field] = params[field]

        # Check if we have required fields for shorthand mode
        has_required = all(
            params.get(field) is not None
            for field in schema['required_fields']
        )

        if has_required:
            # Remove None values
            record_data = {k: v for k, v in record_data.items() if v is not None}
            return [record_data], set_params

        # No records provided via either method
        return [], set_params

    def _extract_set_params(self, params):
        """Extract set-level parameters from params"""
        set_params = {
            'ttl': params.get('ttl'),
            'comments': params.get('comments'),
            'expiryTtl': params.get('expiryTtl')
        }
        return {k: v for k, v in set_params.items() if v is not None}

    def _records_match(self, record1, record2, record_type):
        """
        Check if two records are the same based on identifying fields.

        Args:
            record1: First record dict (from API or user input)
            record2: Second record dict
            record_type: DNS record type

        Returns:
            bool: True if records match on identifying fields
        """
        if record_type not in RECORD_SCHEMAS:
            return False

        schema = RECORD_SCHEMAS[record_type]
        identifying_fields = schema['identifying_fields']

        for field in identifying_fields:
            # Special handling for srv_port vs port
            field1_name = 'port' if field == 'srv_port' else field
            field2_name = field

            val1 = record1.get(field1_name)
            val2 = record2.get(field2_name)

            # Use existing _values_match for robust comparison
            if not self._values_match(val1, val2, field):
                return False

        return True

    def _validate_parameters(self, record_type, params):
        """Validate that parameters are appropriate for the record type"""
        # v1.0.0: All record types now support 'records' parameter
        allowed_params = {
            'A': {'records', 'ipAddress', 'ttl', 'overwrite', 'comments', 'expiryTtl', 'ptr', 'createPtrZone', 'updateSvcbHints'},
            'AAAA': {'records', 'ipAddress', 'ttl', 'overwrite', 'comments', 'expiryTtl', 'ptr', 'createPtrZone', 'updateSvcbHints'},
            'NS': {'records', 'nameServer', 'glue', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'CNAME': {'records', 'cname', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'PTR': {'records', 'ptrName', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'MX': {'records', 'exchange', 'preference', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'TXT': {'records', 'text', 'splitText', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'SRV': {'records', 'priority', 'weight', 'srv_port', 'target', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'NAPTR': {'records', 'naptrOrder', 'naptrPreference', 'naptrFlags', 'naptrServices', 'naptrRegexp', 'naptrReplacement',
                      'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'DNAME': {'records', 'dname', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'DS': {'records', 'keyTag', 'algorithm', 'digestType', 'digest', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'SSHFP': {'records', 'sshfpAlgorithm', 'sshfpFingerprintType', 'sshfpFingerprint', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'TLSA': {'records', 'tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData',
                     'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'SVCB': {'records', 'svcPriority', 'svcTargetName', 'svcParams', 'autoIpv4Hint', 'autoIpv6Hint', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'HTTPS': {'records', 'svcPriority', 'svcTargetName', 'svcParams', 'autoIpv4Hint', 'autoIpv6Hint', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'CAA': {'records', 'flags', 'tag', 'value', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'ANAME': {'records', 'aname', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'FWD': {'records', 'ttl', 'protocol', 'forwarder', 'forwarderPriority', 'dnssecValidation', 'proxyType', 'proxyAddress',
                    'proxyPort', 'proxyUsername', 'proxyPassword', 'overwrite', 'comments', 'expiryTtl'},
            'APP': {'records', 'appName', 'classPath', 'recordData', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'UNKNOWN': {'records', 'rdata', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'URI': {'records', 'uriPriority', 'uriWeight', 'uri', 'ttl', 'overwrite', 'comments', 'expiryTtl'}
        }

        required_params = {
            'A': ['ipAddress'],
            'AAAA': ['ipAddress'],
            'NS': ['nameServer'],
            'CNAME': ['cname'],
            'PTR': ['ptrName'],
            'MX': ['exchange', 'preference'],
            'TXT': ['text'],
            'SRV': ['priority', 'weight', 'srv_port', 'target'],
            'NAPTR': ['naptrOrder', 'naptrPreference'],
            'DNAME': ['dname'],
            'DS': ['keyTag', 'algorithm', 'digestType', 'digest'],
            'SSHFP': ['sshfpAlgorithm', 'sshfpFingerprintType', 'sshfpFingerprint'],
            'TLSA': ['tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData'],
            'SVCB': ['svcPriority', 'svcTargetName', 'svcParams'],
            'HTTPS': ['svcPriority', 'svcTargetName', 'svcParams'],
            'CAA': ['flags', 'tag', 'value'],
            'ANAME': ['aname'],
            'FWD': ['protocol', 'forwarder'],
            'APP': ['appName', 'classPath'],
            'UNKNOWN': ['rdata'],
            'URI': ['uriPriority', 'uriWeight', 'uri'],
        }

        # Check for unsupported parameters (skip internal params and normalized data)
        if record_type in allowed_params:
            for param in params:
                if param in ['api_url', 'api_port', 'api_token', 'domain', 'name', 'zone', 'type',
                           'validate_certs', 'state', '_normalized_records', '_set_params']:
                    continue
                if params[param] is not None and param not in allowed_params[record_type]:
                    self.fail_json(
                        msg=f"Parameter '{param}' is not supported for record type '{record_type}'.")

        # Check for required parameters (v1.0.0: validated in _normalize_records)
        # If using 'records' parameter, validation happens there
        # If using shorthand, we need at least one record in normalized list
        normalized_records = params.get('_normalized_records', [])
        if not normalized_records and params.get('state') == 'present':
            # No records provided via either method for state=present
            if record_type in required_params:
                missing = required_params[record_type]
                self.fail_json(
                    msg=f"No records specified for state=present. Either provide 'records' list or shorthand parameters: {', '.join(missing)}"
                )

        # For state=absent with records specified, validate records have identifying fields
        # (Non-identifying fields are ignored during deletion - only identifying fields matter)
        if params.get('state') == 'absent' and normalized_records and record_type in RECORD_SCHEMAS:
            schema = RECORD_SCHEMAS[record_type]
            identifying_fields = set(schema['identifying_fields'])

            for record in normalized_records:
                # Ensure at least the identifying fields are present
                missing_identifying = identifying_fields - set(record.keys())
                if missing_identifying:
                    self.fail_json(
                        msg=f"Record for deletion missing identifying fields: {', '.join(missing_identifying)}"
                    )

    def _ensure_present(self, record_type, params):
        """
        v1.0.0: Ensure the record set exists with the specified records.

        Behavior:
        - overwrite=true (default): Replace entire record set with specified records
        - overwrite=false: Add specified records to existing set (don't delete others)
        """
        # Get normalized records and set-level params
        desired_records = params.get('_normalized_records', [])
        set_params = params.get('_set_params', {})
        overwrite = set_params.get('overwrite', True)

        # Get existing records of this type/name
        existing_api_records = self._get_existing_records_from_api(record_type, params)

        # Convert existing API records to normalized format for comparison
        existing_records = self._convert_api_records_to_normalized(existing_api_records, record_type)

        # Determine what operations are needed
        changes = self._compute_record_set_changes(
            existing_records,
            desired_records,
            existing_api_records,
            record_type,
            set_params,
            overwrite
        )

        # Check if no changes needed (idempotent)
        if not changes['needs_change']:
            if self.check_mode:
                self.exit_json(changed=False, msg="Record set already matches desired state (check mode).")
            else:
                self.exit_json(changed=False, msg="Record set already matches desired state.")

        # Report what would change in check mode
        if self.check_mode:
            msg_parts = []
            if changes['to_delete']:
                msg_parts.append(f"delete {len(changes['to_delete'])} record(s)")
            if changes['to_update']:
                msg_parts.append(f"update {len(changes['to_update'])} record(s)")
            if changes['to_add']:
                msg_parts.append(f"add {len(changes['to_add'])} record(s)")

            msg = f"Would {', '.join(msg_parts)} (check mode)."
            self.exit_json(changed=True, msg=msg, changes=changes)

        # Execute changes
        results = self._apply_record_set_changes(record_type, params, changes, set_params)

        # Build response message
        msg_parts = []
        if results['deleted']:
            msg_parts.append(f"deleted {results['deleted']} record(s)")
        if results['updated']:
            msg_parts.append(f"updated {results['updated']} record(s)")
        if results['added']:
            msg_parts.append(f"added {results['added']} record(s)")

        msg = f"Record set modified: {', '.join(msg_parts)}." if msg_parts else "Record set updated."
        self.exit_json(changed=True, msg=msg, results=results)

    def _get_existing_records_from_api(self, record_type, params):
        """Fetch existing records from API"""
        get_query = {
            'domain': params['name'],
            'token': self.api_token
        }
        if params.get('zone'):
            get_query['zone'] = params['zone']

        try:
            get_resp = self.request('/api/zones/records/get', params=get_query)
            all_records = get_resp.get('response', {}).get('records', []) if get_resp.get('status') == 'ok' else []
        except Exception:
            return []

        # Filter to records of the correct type
        matching_records = [
            rec for rec in all_records
            if rec.get('type', '').upper() == record_type and
               rec.get('name', '').lower() == params['name'].lower()
        ]

        return matching_records

    def _convert_api_records_to_normalized(self, api_records, record_type):
        """Convert API record format to normalized record dict format"""
        if record_type not in RECORD_SCHEMAS:
            return []

        schema = RECORD_SCHEMAS[record_type]
        normalized = []

        for api_rec in api_records:
            rdata = api_rec.get('rData', {})
            record = {}

            # Extract fields based on schema
            for field in schema['required_fields'] + schema['optional_fields']:
                # Special handling for srv_port
                if field == 'srv_port':
                    if 'port' in rdata:
                        record['srv_port'] = rdata['port']
                # Special handling for APP recordData (API uses 'data')
                elif field == 'recordData':
                    if 'data' in rdata:
                        record['recordData'] = rdata['data']
                elif field in rdata:
                    record[field] = rdata[field]

            # Include TTL and other top-level fields
            record['_ttl'] = api_rec.get('ttl')
            record['_api_record'] = api_rec  # Keep reference to original

            normalized.append(record)

        return normalized

    def _convert_single_api_record_to_normalized(self, api_rec, record_type):
        """Convert a single API record to normalized format"""
        if record_type not in RECORD_SCHEMAS:
            return {}

        schema = RECORD_SCHEMAS[record_type]
        rdata = api_rec.get('rData', {})
        record = {}

        # Extract fields based on schema
        for field in schema['required_fields'] + schema['optional_fields']:
            # Special handling for srv_port
            if field == 'srv_port':
                if 'port' in rdata:
                    record['srv_port'] = rdata['port']
            # Special handling for APP recordData (API uses 'data')
            elif field == 'recordData':
                if 'data' in rdata:
                    record['recordData'] = rdata['data']
            elif field in rdata:
                record[field] = rdata[field]

        # Include TTL and other top-level fields
        record['_ttl'] = api_rec.get('ttl')
        record['_api_record'] = api_rec  # Keep reference to original

        return record

    def _compute_record_set_changes(self, existing_records, desired_records, existing_api_records,
                                     record_type, set_params, overwrite):
        """
        Determine what changes are needed to move from existing to desired state.

        Returns dict with:
            - needs_change: bool
            - to_delete: list of API records to delete
            - to_update: list of (API record, desired record, differences) tuples
            - to_add: list of desired records to create
        """
        changes = {
            'needs_change': False,
            'to_delete': [],
            'to_update': [],
            'to_add': []
        }

        if overwrite:
            # Overwrite mode: Delete all existing, add all desired
            # But check for perfect match first (idempotency)
            if self._record_sets_match(existing_records, desired_records, set_params, record_type):
                return changes  # No changes needed

            changes['needs_change'] = True
            changes['to_delete'] = existing_api_records
            changes['to_add'] = desired_records
        else:
            # Additive mode: Add records that don't exist, update those that do
            for desired_rec in desired_records:
                found_match = False
                for idx, existing_rec in enumerate(existing_records):
                    if self._records_match(desired_rec, existing_rec, record_type):
                        found_match = True
                        # Check if update needed (set-level params)
                        if self._record_needs_set_level_update(existing_rec, set_params):
                            changes['needs_change'] = True
                            api_rec = existing_rec.get('_api_record')
                            changes['to_update'].append((api_rec, desired_rec, set_params))
                        break

                if not found_match:
                    changes['needs_change'] = True
                    changes['to_add'].append(desired_rec)

        return changes

    def _record_sets_match(self, existing_records, desired_records, set_params, record_type):
        """Check if existing and desired record sets are identical"""
        # Must have same number of records
        if len(existing_records) != len(desired_records):
            return False

        # Check set-level parameters
        for existing_rec in existing_records:
            if self._record_needs_set_level_update(existing_rec, set_params):
                return False

        # Check each desired record exists in existing
        for desired_rec in desired_records:
            found = False
            for existing_rec in existing_records:
                if self._records_match(desired_rec, existing_rec, record_type):
                    # Also check all optional fields match
                    if self._all_fields_match(desired_rec, existing_rec, record_type):
                        found = True
                        break
            if not found:
                return False

        return True

    def _record_needs_set_level_update(self, record, set_params):
        """Check if record needs update for set-level params (ttl, etc.)"""
        if 'ttl' in set_params:
            current_ttl = record.get('_ttl')
            if current_ttl != set_params['ttl']:
                return True
        # Note: comments and expiryTtl would go here too
        return False

    def _all_fields_match(self, record1, record2, record_type):
        """Check if all fields (not just identifying) match between records"""
        if record_type not in RECORD_SCHEMAS:
            return False

        schema = RECORD_SCHEMAS[record_type]
        all_fields = schema['required_fields'] + schema['optional_fields']

        for field in all_fields:
            val1 = record1.get(field)
            val2 = record2.get(field)

            if not self._values_match(val1, val2, field):
                return False

        return True

    def _apply_record_set_changes(self, record_type, params, changes, set_params):
        """Execute the computed changes"""
        results = {'deleted': 0, 'updated': 0, 'added': 0}

        # Delete records
        for api_record in changes['to_delete']:
            self._delete_single_record_by_api_record(record_type, params, api_record)
            results['deleted'] += 1

        # Update records
        for api_record, desired_record, update_params in changes['to_update']:
            self._update_single_record(record_type, params, api_record, desired_record, set_params)
            results['updated'] += 1

        # Add new records
        for desired_record in changes['to_add']:
            self._add_single_record(record_type, params, desired_record, set_params)
            results['added'] += 1

        return results

    def _add_single_record(self, record_type, params, record_data, set_params):
        """Add a single record to the set"""
        query = {
            'token': self.api_token,
            'domain': params['name'],
            'type': record_type
        }

        if params.get('zone'):
            query['zone'] = params['zone']

        # Add set-level params
        if 'ttl' in set_params:
            query['ttl'] = set_params['ttl']
        if 'comments' in set_params:
            query['comments'] = set_params['comments']
        if 'expiryTtl' in set_params:
            query['expiryTtl'] = set_params['expiryTtl']

        # Add record-specific data
        for key, value in record_data.items():
            if key.startswith('_'):
                continue  # Skip internal fields
            # Handle srv_port -> port mapping
            if key == 'srv_port':
                query['port'] = value
            # Don't rename recordData - API expects it as-is
            else:
                if isinstance(value, bool):
                    query[key] = str(value).lower()
                else:
                    query[key] = value

        # Make API request
        data = self.request('/api/zones/records/add', params=query, method='POST')

        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to add record: {error_msg}", api_response=data)

        return data

    def _delete_single_record_by_api_record(self, record_type, params, api_record):
        """Delete a single record using its API representation"""
        query = {
            'token': self.api_token,
            'domain': params['name'],
            'type': record_type
        }

        if params.get('zone'):
            query['zone'] = params['zone']

        # Add identifying parameters from the API record
        rdata = api_record.get('rData', {})

        if record_type not in RECORD_SCHEMAS:
            self.fail_json(msg=f"Cannot delete {record_type} record - no schema defined")

        schema = RECORD_SCHEMAS[record_type]

        # Add identifying fields
        for field in schema['identifying_fields']:
            if field == 'srv_port':
                if 'port' in rdata:
                    query['port'] = rdata['port']
            elif field in rdata:
                value = rdata[field]
                if isinstance(value, bool):
                    query[field] = str(value).lower()
                else:
                    query[field] = value

        # Make API request
        data = self.request('/api/zones/records/delete', params=query, method='POST')

        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            # Don't fail on "record not found" - it's already gone
            if 'not found' not in error_msg.lower() and 'does not exist' not in error_msg.lower():
                self.fail_json(msg=f"Failed to delete record: {error_msg}", api_response=data)

        return data

    def _update_single_record(self, record_type, params, api_record, desired_record, set_params):
        """Update a single record (for additive mode with set-level param changes)"""
        # For now, implement as delete + add since most record types don't support
        # partial updates. We can optimize this later for types that do.
        self._delete_single_record_by_api_record(record_type, params, api_record)
        self._add_single_record(record_type, params, desired_record, set_params)

    def _ensure_absent(self, record_type, params):
        """
        v1.0.0: Ensure the record set or specific records are absent.

        Behavior:
        - If no records specified: Delete entire record set (all records of this name/type)
        - If records specified: Delete only those specific records from the set
        """
        # Get normalized records (may be empty for "delete all" operation)
        desired_absent_records = params.get('_normalized_records', [])

        # Get existing records of this type/name
        existing_api_records = self._get_existing_records_from_api(record_type, params)

        # If no existing records, nothing to do
        if not existing_api_records:
            if self.check_mode:
                self.exit_json(changed=False, msg="Record set does not exist (check mode).")
            else:
                self.exit_json(changed=False, msg="Record set does not exist.")

        # Determine what to delete
        if not desired_absent_records:
            # No specific records provided = delete entire record set
            records_to_delete = existing_api_records
            operation_msg = "entire record set"
        else:
            # Specific records provided = delete only matching records
            records_to_delete = []
            for api_rec in existing_api_records:
                normalized_existing = self._convert_single_api_record_to_normalized(api_rec, record_type)
                for desired_rec in desired_absent_records:
                    if self._records_match(normalized_existing, desired_rec, record_type):
                        records_to_delete.append(api_rec)
                        break

            operation_msg = f"{len(records_to_delete)} specific record(s)"

            # If none of the specified records exist, nothing to do
            if not records_to_delete:
                if self.check_mode:
                    self.exit_json(changed=False, msg="Specified records do not exist (check mode).")
                else:
                    self.exit_json(changed=False, msg="Specified records do not exist.")

        # Check mode - just report what would be deleted
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"Would delete {operation_msg} (check mode).",
                records_to_delete=len(records_to_delete)
            )

        # Execute deletions
        deleted_count = 0
        errors = []

        for api_record in records_to_delete:
            try:
                self._delete_single_record_by_api_record(record_type, params, api_record)
                deleted_count += 1
            except Exception as e:
                errors.append(str(e))

        # Report results
        if errors:
            self.fail_json(
                msg=f"Deleted {deleted_count} records but encountered {len(errors)} error(s)",
                deleted_count=deleted_count,
                errors=errors
            )

        self.exit_json(
            changed=True,
            msg=f"Successfully deleted {operation_msg}.",
            deleted_count=deleted_count
        )

    def _build_query(self, params):
        """Build query parameters for API request"""
        query = {}
        for key in self.argument_spec:
            val = params.get(key)
            if val is not None:
                if isinstance(val, bool):
                    val = str(val).lower()
                # Map internal names to API names
                if key == 'srv_port':
                    query['port'] = val
                elif key in ['api_port', 'validate_certs', 'state']:
                    # Skip module-only parameters
                    continue
                else:
                    query[key] = val
        return query

    def _get_required_params(self, record_type):
        """Get list of required parameters for a record type"""
        required_params = {
            'A': ['ipAddress'],
            'AAAA': ['ipAddress'],
            'NS': ['nameServer'],
            'CNAME': ['cname'],
            'PTR': ['ptrName'],
            'MX': ['exchange', 'preference'],
            'TXT': ['text'],
            'SRV': ['priority', 'weight', 'srv_port', 'target'],
            'NAPTR': ['naptrOrder', 'naptrPreference'],
            'DNAME': ['dname'],
            'DS': ['keyTag', 'algorithm', 'digestType', 'digest'],
            'SSHFP': ['sshfpAlgorithm', 'sshfpFingerprintType', 'sshfpFingerprint'],
            'TLSA': ['tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData'],
            'SVCB': ['svcPriority', 'svcTargetName', 'svcParams'],
            'HTTPS': ['svcPriority', 'svcTargetName', 'svcParams'],
            'CAA': ['flags', 'tag', 'value'],
            'ANAME': ['aname'],
            'FWD': ['protocol', 'forwarder'],
            'APP': ['appName', 'classPath'],
            'UNKNOWN': ['rdata'],
            'URI': ['uriPriority', 'uriWeight', 'uri'],
        }
        return required_params.get(record_type, [])

    def _values_match(self, current_value, desired_value, param_name):
        """
        Compare current and desired values, handling type conversions.

        Args:
            current_value: The current value from the record
            desired_value: The desired value from user input
            param_name: The parameter name (for special handling)

        Returns:
            bool: True if values match, False otherwise
        """
        # Both None = match
        if current_value is None and desired_value is None:
            return True

        # Special handling for comments - empty string and None are equivalent,
        # and normalize whitespace
        if param_name == 'comments':
            # Normalize empty values and strip whitespace
            current_normalized = str(current_value).strip() if current_value else ''
            desired_normalized = str(desired_value).strip() if desired_value else ''
            return current_normalized == desired_normalized

        # One is None = no match
        if current_value is None or desired_value is None:
            return False

        # Numeric comparison (handle string vs int)
        if isinstance(current_value, (int, float)) or isinstance(desired_value, (int, float)):
            try:
                return int(current_value) == int(desired_value)
            except (ValueError, TypeError):
                pass

        # String comparison
        if isinstance(current_value, str) and isinstance(desired_value, str):
            # Case-insensitive for certain parameters
            case_insensitive_params = ['sshfpFingerprint', 'tlsaCertificateAssociationData', 'digest']
            if param_name in case_insensitive_params:
                return current_value.lower() == desired_value.lower()
            return current_value == desired_value

        # Boolean comparison
        if isinstance(current_value, bool) or isinstance(desired_value, bool):
            return bool(current_value) == bool(desired_value)

        # Default: direct comparison
        return current_value == desired_value

    def _record_needs_update(self, current_record, desired_params):
        """
        Check if current record differs from desired state.

        Args:
            current_record: The current record from the API
            desired_params: The desired parameters from the user

        Returns:
            tuple: (needs_update: bool, differences: dict)
                differences format: {'param': {'current': value, 'new': value}}
        """
        differences = {}
        record_type = desired_params['type'].upper()

        # Check if this record type supports updates
        if record_type not in UPDATE_PARAM_MAPPINGS:
            # Record type doesn't support native updates yet
            # Return special flag to indicate update needed but not supported
            return None, {'_unsupported': True}

        mappings = UPDATE_PARAM_MAPPINGS[record_type]
        rdata = current_record.get('rData', {})

        # Check record-specific parameters
        for param_name, rdata_field in mappings['current'].items():
            desired_value = desired_params.get(param_name)

            # Skip if user didn't specify this parameter
            if desired_value is None:
                continue

            # Extract current value from rData
            current_value = rdata.get(rdata_field)

            # Special handling for srv_port parameter
            if param_name == 'srv_port':
                current_value = rdata.get('port')

            # Compare values
            if not self._values_match(current_value, desired_value, param_name):
                differences[param_name] = {
                    'current': current_value,
                    'new': desired_value
                }

        # Check common parameters (ttl, comments, expiryTtl)
        for common_param in COMMON_UPDATE_PARAMS:
            if common_param in desired_params and desired_params[common_param] is not None:
                desired_value = desired_params[common_param]
                # Get current value, defaulting to None if not present
                current_value = current_record.get(common_param)

                # Special case for expiryTtl - API returns 0 for "not set"
                if common_param == 'expiryTtl' and current_value == 0:
                    current_value = None

                if not self._values_match(current_value, desired_value, common_param):
                    differences[common_param] = {
                        'current': current_value,
                        'new': desired_value
                    }

        needs_update = len(differences) > 0
        return needs_update, differences

    def _update_record(self, record_type, current_record, desired_params, differences):
        """
        Update an existing record using the /api/zones/records/update endpoint.

        Args:
            record_type: The DNS record type (A, MX, etc.)
            current_record: The current record data from API
            desired_params: The desired parameters from user
            differences: Dict of parameters that need updating

        Returns:
            API response data
        """
        query = {
            'token': self.api_token,
            'domain': desired_params['name'],
            'type': record_type
        }

        if desired_params.get('zone'):
            query['zone'] = desired_params['zone']

        # Add current values (required to identify the record)
        mappings = UPDATE_PARAM_MAPPINGS[record_type]
        rdata = current_record.get('rData', {})

        for param_name, rdata_field in mappings['current'].items():
            # Special handling for srv_port
            if param_name == 'srv_port':
                query['port'] = rdata.get('port')
            else:
                value = rdata.get(rdata_field)
                if value is not None:
                    if isinstance(value, bool):
                        value = str(value).lower()
                    query[param_name] = value

        # Add new values (what we're changing)
        for param_name, new_param_name in mappings['new'].items():
            if param_name in differences:
                new_value = desired_params.get(param_name)
                if new_value is not None:
                    if isinstance(new_value, bool):
                        new_value = str(new_value).lower()
                    # Special handling for srv_port
                    if param_name == 'srv_port':
                        query['newPort'] = new_value
                    else:
                        query[new_param_name] = new_value

        # Add common parameters that changed
        for param in COMMON_UPDATE_PARAMS:
            if param in differences:
                val = desired_params[param]
                if isinstance(val, bool):
                    val = str(val).lower()
                query[param] = val

        # Always include comments if provided (even if not in differences)
        # because the GET API doesn't return comments, so we can't detect changes
        if 'comments' in desired_params and desired_params['comments'] is not None:
            query['comments'] = desired_params['comments']

        # Add direct parameters
        for param in mappings.get('direct', []):
            if param in desired_params and desired_params[param] is not None:
                val = desired_params[param]
                if isinstance(val, bool):
                    val = str(val).lower()
                query[param] = val

        # Make the update API call
        data = self.request('/api/zones/records/update', params=query, method='POST')

        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to update record: {error_msg}", api_response=data)

        return data


def main():
    module = RecordModule()
    module()


if __name__ == '__main__':
    main()
