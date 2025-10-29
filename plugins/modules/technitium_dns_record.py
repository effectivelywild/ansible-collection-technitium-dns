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
        overwrite=dict(type='bool', required=False, default=False),
        comments=dict(type='str', required=False),
        expiryTtl=dict(type='int', required=False),
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

        # Validate parameters for the record type
        self._validate_parameters(record_type, params)

        # Route to appropriate handler based on state
        if state == 'present':
            self._ensure_present(record_type, params)
        elif state == 'absent':
            self._ensure_absent(record_type, params)

    def _validate_parameters(self, record_type, params):
        """Validate that parameters are appropriate for the record type"""
        allowed_params = {
            'A': {'ipAddress', 'ttl', 'overwrite', 'comments', 'expiryTtl', 'ptr', 'createPtrZone', 'updateSvcbHints'},
            'AAAA': {'ipAddress', 'ttl', 'overwrite', 'comments', 'expiryTtl', 'ptr', 'createPtrZone', 'updateSvcbHints'},
            'NS': {'nameServer', 'glue', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'CNAME': {'cname', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'PTR': {'ptrName', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'MX': {'exchange', 'preference', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'TXT': {'text', 'splitText', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'SRV': {'priority', 'weight', 'srv_port', 'target', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'NAPTR': {'naptrOrder', 'naptrPreference', 'naptrFlags', 'naptrServices', 'naptrRegexp', 'naptrReplacement',
                      'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'DNAME': {'dname', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'DS': {'keyTag', 'algorithm', 'digestType', 'digest', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'SSHFP': {'sshfpAlgorithm', 'sshfpFingerprintType', 'sshfpFingerprint', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'TLSA': {'tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData',
                     'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'SVCB': {'svcPriority', 'svcTargetName', 'svcParams', 'autoIpv4Hint', 'autoIpv6Hint', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'HTTPS': {'svcPriority', 'svcTargetName', 'svcParams', 'autoIpv4Hint', 'autoIpv6Hint', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'CAA': {'flags', 'tag', 'value', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'ANAME': {'aname', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'FWD': {'ttl', 'protocol', 'forwarder', 'forwarderPriority', 'dnssecValidation', 'proxyType', 'proxyAddress',
                    'proxyPort', 'proxyUsername', 'proxyPassword', 'overwrite', 'comments', 'expiryTtl'},
            'APP': {'appName', 'classPath', 'recordData', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'UNKNOWN': {'rdata', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'URI': {'uriPriority', 'uriWeight', 'uri', 'ttl', 'overwrite', 'comments', 'expiryTtl'}
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
            'APP': ['appName', 'classPath', 'recordData'],
            'UNKNOWN': ['rdata'],
            'URI': ['uriPriority', 'uriWeight', 'uri'],
        }

        # Check for unsupported parameters
        if record_type in allowed_params:
            for param in params:
                if param in ['api_url', 'api_port', 'api_token', 'domain', 'name', 'zone', 'type', 'validate_certs', 'state']:
                    continue
                if params[param] is not None and param not in allowed_params[record_type]:
                    self.fail_json(
                        msg=f"Parameter '{param}' is not supported for record type '{record_type}'.")

        # Check for required parameters
        if record_type in required_params:
            for req in required_params[record_type]:
                param_value = params.get(req)
                if param_value is None:
                    self.fail_json(
                        msg=f"Parameter '{req}' is required for record type '{record_type}'.")
                # Special handling for parameters that can be 0 or empty string
                if req in ['svcPriority'] and param_value == 0:
                    continue  # 0 is valid for svcPriority (alias mode)

    def _ensure_present(self, record_type, params):
        """Ensure the record exists with the specified parameters"""
        # First, try to find any existing records of this type/name that we could update
        get_query = {
            'domain': params['name'],
            'token': self.api_token
        }
        if params.get('zone'):
            get_query['zone'] = params['zone']

        try:
            get_resp = self.request('/api/zones/records/get', params=get_query)
            existing_records = get_resp.get('response', {}).get('records', []) if get_resp.get('status') == 'ok' else []
        except Exception:
            existing_records = []

        # Filter to records of the correct type
        matching_type_records = [rec for rec in existing_records
                                  if rec.get('type', '').upper() == record_type and
                                  rec.get('name', '').lower() == params['name'].lower()]

        # Check if we have a record that exactly matches desired state (idempotency check)
        for rec in matching_type_records:
            if self._record_matches(record_type, params, rec):
                # Found exact match - check if it needs updating anyway (e.g., TTL change)
                needs_update, differences = self._record_needs_update(rec, params)

                if needs_update is None and differences.get('_unsupported'):
                    msg = (f"Record type '{record_type}' exists but update checking is not yet implemented. "
                           f"Supported types for updates: {', '.join(UPDATE_PARAM_MAPPINGS.keys())}. "
                           f"To update this record, delete it first with state=absent, then recreate it.")
                    if self.check_mode:
                        self.exit_json(changed=False, msg=f"{msg} (check mode - cannot verify if changes needed)")
                    else:
                        self.exit_json(changed=False, msg=msg)

                if not needs_update:
                    # Perfect match - idempotent
                    if self.check_mode:
                        self.exit_json(changed=False, msg="Record already matches desired state (check mode).")
                    else:
                        self.exit_json(changed=False, msg="Record already matches desired state.")

                # Record matches required params but needs update (e.g., TTL changed)
                if self.check_mode:
                    diff_msg = ", ".join([f"{k}: {v['current']} → {v['new']}" for k, v in differences.items()])
                    self.exit_json(changed=True, msg=f"Record would be updated: {diff_msg} (check mode).")

                data = self._update_record(record_type, rec, params, differences)
                self.exit_json(changed=True, msg="DNS record updated.", api_response=data)

        # No exact match found - check if we should update an existing record
        # For record types that support updates, if there's exactly ONE record of this type/name,
        # we should update it rather than create a duplicate
        if len(matching_type_records) == 1 and record_type in UPDATE_PARAM_MAPPINGS:
            # Check if this single record needs updating
            current_record = matching_type_records[0]
            needs_update, differences = self._record_needs_update(current_record, params)

            if needs_update is None and differences.get('_unsupported'):
                # Shouldn't happen since we checked UPDATE_PARAM_MAPPINGS, but be safe
                pass
            elif needs_update:
                # Update the existing record
                if self.check_mode:
                    diff_msg = ", ".join([f"{k}: {v['current']} → {v['new']}" for k, v in differences.items()])
                    self.exit_json(changed=True, msg=f"Record would be updated: {diff_msg} (check mode).")

                data = self._update_record(record_type, current_record, params, differences)
                self.exit_json(changed=True, msg="DNS record updated.", api_response=data)

        # No matching record to update - create new record
        if self.check_mode:
            self.exit_json(changed=True, msg="Record would be created (check mode).")

        # Build query for API request
        query = self._build_query(params)
        query['token'] = self.api_token
        query['domain'] = self.name

        # Make API request to create
        data = self.request('/api/zones/records/add', params=query, method='POST')

        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to create record: {error_msg}", api_response=data)

        self.exit_json(changed=True, msg="DNS record created.", api_response=data)

    def _ensure_absent(self, record_type, params):
        """Ensure the record does not exist"""
        # Check if record exists
        exists, matching_record = self._check_record_exists(record_type, params)

        if not exists:
            # Record doesn't exist, nothing to do
            if self.check_mode:
                self.exit_json(changed=False, msg="Record does not exist (check mode).")
            else:
                self.exit_json(changed=False, msg="Record does not exist.")

        # Need to delete the record
        if self.check_mode:
            self.exit_json(changed=True, msg="Record would be deleted (check mode).")

        # Build query for delete request
        query = {
            'token': self.api_token,
            'domain': self.name,
            'type': record_type
        }

        # Add required parameters for deletion
        required_params = self._get_required_params(record_type)
        for req in required_params:
            if req == 'srv_port':
                query['port'] = params['srv_port']
            else:
                query[req] = params[req]

        if params.get('zone'):
            query['zone'] = params['zone']

        # Make API request
        data = self.request('/api/zones/records/delete', params=query, method='POST')

        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error during deletion: {error_msg}", api_response=data)

        self.exit_json(changed=True, msg="DNS record is absent.", api_response=data)

    def _check_record_exists(self, record_type, params):
        """Check if a record exists with the exact specified parameters"""
        get_query = {
            'domain': params['name'],
            'token': self.api_token
        }
        if params.get('zone'):
            get_query['zone'] = params['zone']

        try:
            get_resp = self.request('/api/zones/records/get', params=get_query)
        except Exception:
            # If we can't fetch records, assume it doesn't exist
            return False, None

        if get_resp.get('status') != 'ok':
            # If API call fails, assume record doesn't exist
            return False, None

        existing_records = get_resp.get('response', {}).get('records', [])

        # Look for exact match
        for rec in existing_records:
            if rec.get('type', '').upper() != record_type:
                continue
            if rec.get('name', '').lower() != params['name'].lower():
                continue

            # Check if all required parameters match
            if self._record_matches(record_type, params, rec):
                return True, rec

        return False, None

    def _record_matches(self, record_type, params, rec):
        """Check if a record matches the specified parameters"""
        required_params = self._get_required_params(record_type)

        # Parameter mapping for special cases
        param_mapping = {
            'srv_port': 'port',
        }

        rdata = rec.get('rData', {})

        for param_name in required_params:
            expected_value = params.get(param_name)
            record_field = param_mapping.get(param_name, param_name)
            actual_value = rdata.get(record_field)

            if actual_value is None:
                actual_value = rec.get(record_field)

            # Handle type conversions and case sensitivity
            if expected_value is not None:
                # String comparisons (handle case insensitivity for certain fields)
                if isinstance(expected_value, str) and isinstance(actual_value, str):
                    if expected_value.lower() != actual_value.lower():
                        return False
                # Numeric comparisons (handle type mismatches)
                elif isinstance(expected_value, int) or isinstance(actual_value, int):
                    try:
                        if int(expected_value) != int(actual_value):
                            return False
                    except (ValueError, TypeError):
                        return False
                # Exact match for other types
                elif expected_value != actual_value:
                    return False

        return True

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
            'APP': ['appName', 'classPath', 'recordData'],
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
