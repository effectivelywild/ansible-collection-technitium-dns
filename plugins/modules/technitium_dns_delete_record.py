#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_record
short_description: Delete a DNS record
version_added: "0.1.0"
author: Frank Muise (@effectivelywild)
description:
    - Delete a a DNS record.
    - You must include the record parameters when deleting a record.
    - The module supports all DNS record types.
    - Some parameters are only valid or required for specific record types.
    - For example, C(ipAddress) is required for A and AAAA records, while C(cname) is required for CNAME records.
seealso:
    - module: effectivelywild.technitium_dns.technitium_dns_add_record
      description: Used to add DNS records
    - module: effectivelywild.technitium_dns.technitium_dns_get_record
      description: Used to get DNS record details
options:
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
            - The use of domain is also supported to align with API
        aliases:
            - domain
        required: true
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
            - Overwrite existing record set for this type
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
# Basic A record deletion
- name: Delete an A record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "www.example.com"
    type: "A"
    ipAddress: "192.0.2.1"

# AAAA (IPv6) record deletion
- name: Delete an AAAA record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "ipv6.example.com"
    type: "AAAA"
    ipAddress: "2001:db8::1"

# CNAME record deletion
- name: Delete a CNAME record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "alias.example.com"
    type: "CNAME"
    cname: "www.example.com"

# MX record deletion
- name: Delete an MX record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    type: "MX"
    exchange: "mail.example.com"
    preference: 10

# TXT record deletion
- name: Delete a TXT record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    type: "TXT"
    text: "v=spf1 include:_spf.google.com ~all"

# SRV record deletion
- name: Delete an SRV record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_sip._tcp.example.com"
    type: "SRV"
    priority: 10
    weight: 20
    srv_port: 5060
    target: "sip.example.com"

# NS record deletion
- name: Delete an NS record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "subdomain.example.com"
    type: "NS"
    nameServer: "ns1.subdomain.example.com"

# PTR record deletion
- name: Delete a PTR record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "1.2.0.192.in-addr.arpa"
    type: "PTR"
    ptrName: "www.example.com"

# CAA record deletion
- name: Delete a CAA record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    type: "CAA"
    flags: 0
    tag: "issue"
    value: "letsencrypt.org"

# ANAME record deletion
- name: Delete an ANAME record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    type: "ANAME"
    aname: "target.example.net"

# SSHFP record deletion
- name: Delete an SSHFP record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "server.example.com"
    type: "SSHFP"
    sshfpAlgorithm: 1
    sshfpFingerprintType: 1
    sshfpFingerprint: "123456789abcdef67890123456789abcdef67890"

# HTTPS record deletion
- name: Delete an HTTPS record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    type: "HTTPS"
    svcPriority: 1
    svcTargetName: "svc.example.com"
    svcParams: "alpn=h2,h3"

# SVCB record deletion
- name: Delete an SVCB record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_svc.example.com"
    type: "SVCB"
    svcPriority: 1
    svcTargetName: "svc.example.com"
    svcParams: "port=443"

# TLSA record deletion
- name: Delete a TLSA record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_443._tcp.example.com"
    type: "TLSA"
    tlsaCertificateUsage: 3
    tlsaSelector: 1
    tlsaMatchingType: 1
    tlsaCertificateAssociationData: "abcdef1234567890abcdef1234567890abcdef12"

# URI record deletion
- name: Delete a URI record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_http._tcp.example.com"
    type: "URI"
    uriPriority: 10
    uriWeight: 1
    uri: "https://example.com/path"

# DS record deletion
- name: Delete a DS record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "secure.example.com"
    type: "DS"
    keyTag: 12345
    algorithm: 7
    digestType: 1
    digest: "abcdef1234567890abcdef1234567890abcdef1234567890"

# DNAME record deletion
- name: Delete a DNAME record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "old.example.com"
    type: "DNAME"
    dname: "new.example.com"

# FWD record deletion
- name: Delete a FWD record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "forward.example.com"
    type: "FWD"
    protocol: "Udp"
    forwarder: "8.8.8.8"
    forwarderPriority: 1

# APP record deletion
- name: Delete an APP record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "app.example.com"
    type: "APP"
    appName: "MyApp"
    classPath: "com.example.MyApp"
    recordData: "config=production"

# NAPTR record deletion
- name: Delete a NAPTR record
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "enum.example.com"
    type: "NAPTR"
    naptrOrder: 100
    naptrPreference: 10
    naptrFlags: "u"
    naptrServices: "E2U+sip"
    naptrRegexp: "!^.*$!sip:user@example.com!"
    naptrReplacement: "."

# Using custom port and HTTPS
- name: Delete record using custom API port and HTTPS
  technitium_dns_delete_record:
    api_url: "https://dns.example.com"
    api_port: 8443
    api_token: "myapitoken"
    name: "secure.example.com"
    type: "A"
    ipAddress: "192.0.2.50"
    validate_certs: true

# Using zone parameter
- name: Delete record with explicit zone
  technitium_dns_delete_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "sub.domain.example.com"
    zone: "example.com"
    type: "A"
    ipAddress: "192.0.2.75"

'''

RETURN = r'''
api_response:
    description: The raw response from the Technitium DNS API.
    type: dict
    returned: always
    contains:
        response:
            description: The core data payload from the API, will be empty "[]".
            type: dict
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


class DeleteRecordModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True, aliases=['domain']),
        zone=dict(type='str', required=False),
        type=dict(type='str', required=True, choices=[
            'A', 'AAAA', 'NS', 'CNAME', 'PTR', 'MX', 'TXT', 'SRV', 'NAPTR', 'DNAME', 'DS', 'SSHFP', 'TLSA', 'SVCB',
            'HTTPS', 'URI', 'CAA', 'ANAME', 'FWD', 'APP', 'UNKNOWN'
        ]),
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
        record_type = params['type'].upper()
        # Map of record type to allowed/required params (using new names for conflicting params)
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
            'TLSA': {'tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'SVCB': {'svcPriority', 'svcTargetName', 'svcParams', 'autoIpv4Hint', 'autoIpv6Hint', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'HTTPS': {'svcPriority', 'svcTargetName', 'svcParams', 'autoIpv4Hint', 'autoIpv6Hint', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'CAA': {'flags', 'tag', 'value', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'ANAME': {'aname', 'ttl', 'overwrite', 'comments', 'expiryTtl'},
            'FWD': {'protocol', 'forwarder', 'forwarderPriority', 'dnssecValidation', 'proxyType', 'proxyAddress',
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

        # Validate required parameters for the specific record type
        if record_type in allowed_params:
            for param in params:
                if param in ['api_url', 'api_port', 'api_token', 'domain', 'name', 'zone', 'type', 'validate_certs']:
                    continue
                if params[param] is not None and param not in allowed_params[record_type]:
                    self.fail_json(
                        msg=f"Parameter '{param}' is not supported for record type '{record_type}'.")

        # Validate that no unsupported parameters are provided
        if record_type in required_params:
            for req in required_params[record_type]:
                if params.get(req) is None:
                    self.fail_json(
                        msg=f"Parameter '{req}' is required for record type '{record_type}'.")

        # Build the query for the GET request to check for existence.
        # This must include all parameters needed for a unique match.
        get_query = {
            'domain': params['name'],
            'token': self.api_token,
            'type': record_type
        }
        for key, val in params.items():
            if key in required_params.get(record_type, []):
                if key == 'srv_port':
                    get_query['port'] = val
                else:
                    get_query[key] = val
            if key == 'zone' and val:
                get_query['zone'] = val

        # --- Check Phase: Determine if the record exists ---
        try:
            get_resp = self.request('/api/zones/records/get', params=get_query)
        except Exception as e:
            self.fail_json(msg=f"Failed to check for existing record: {e}")

        if get_resp.get('status') != 'ok':
            # The API failed to get a response. This is a critical error.
            self.fail_json(
                msg=f"Technitium API error during existence check: {get_resp.get('errorMessage') or 'Unknown'}", api_response=get_resp)

        # Filter for an exact match among the returned records.
        found_records = get_resp.get('response', {}).get('records', [])
        matching_type_records = []
        exact_match_found = False

        # First, find all records that match type and domain
        for rec in found_records:
            if rec.get('type', '').upper() == record_type and rec.get('name', '').lower() == params['name'].lower():
                matching_type_records.append(rec)

        if not matching_type_records:
            # No records of this type/domain exist at all
            self.exit_json(
                changed=False, msg=f"DNS record of type '{record_type}' for '{params['name']}' does not exist.")

        # Now check for exact parameter matches
        parameter_mismatches = []
        for rec in matching_type_records:
            mismatch_details = self._check_record_parameters(
                record_type, params, rec, required_params)

            if not mismatch_details:
                exact_match_found = True
                break
            else:
                parameter_mismatches.extend(mismatch_details)

        # --- Act Phase: Decide whether to delete or exit ---
        if not exact_match_found:
            if parameter_mismatches:
                # Records exist but with different parameter values
                mismatch_msg = "; ".join(parameter_mismatches)
                debug_info = f"Found {len(matching_type_records)} {record_type} record(s) for '{params['name']}'"
                self.fail_json(
                    msg=f"DNS record of type '{record_type}' for '{params['name']}' exists but with different parameter values: {mismatch_msg}. {debug_info}")
            else:
                # This shouldn't happen but handle gracefully
                self.exit_json(
                    changed=False, msg=f"DNS record of type '{record_type}' for '{params['name']}' does not match the specified parameters.")

        # If we get here, the record exists and parameters are valid
        # Check mode: report what would happen without actually doing it
        if self.check_mode:
            self.exit_json(
                changed=True, msg=f"DNS record of type '{record_type}' for '{params['name']}' would be deleted (check mode).")

        # If not in check mode, perform the actual deletion
        delete_query = {
            'token': self.api_token,
            'domain': self.name,
            'type': record_type
        }
        # Add all the required parameters for deletion to the query
        for req in required_params.get(record_type, []):
            if req == 'srv_port':
                delete_query['port'] = params['srv_port']
            else:
                delete_query[req] = params[req]
        if params.get('zone'):
            delete_query['zone'] = params['zone']

        # Send the DELETE request
        data = self.request('/api/zones/records/delete', params=delete_query, method='POST')

        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(
                msg=f"Technitium API error during deletion: {error_msg}", api_response=data)

        self.exit_json(
            changed=True, msg=f"DNS record of type '{record_type}' for '{params['name']}' deleted.", api_response=data)

    def _check_record_parameters(self, record_type, params, rec, required_params):
        """
        Check if a record matches the provided parameters.
        Returns a list of mismatch details, or empty list if all parameters match.
        """
        mismatch_details = []

        # Define parameter mapping exceptions (most map to themselves)
        param_mapping_exceptions = {
            'SRV': {
                'srv_port': 'port',
                'srv_target': 'target',
                'srv_priority': 'priority'
            },
            'APP': {
                'recordData': 'data'
            },
            'SSHFP': {
                'sshfpAlgorithm': 'algorithm',
                'sshfpFingerprintType': 'fingerprintType',
                'sshfpFingerprint': 'fingerprint'
            },
            'TLSA': {
                'tlsaCertificateUsage': 'certificateUsage',
                'tlsaSelector': 'selector',
                'tlsaMatchingType': 'matchingType',
                'tlsaCertificateAssociationData': 'certificateAssociationData'
            },
            'URI': {
                'uriPriority': 'priority',
                'uriWeight': 'weight'
            }
        }

        # Special case for UNKNOWN records
        if record_type == 'UNKNOWN':
            expected_rdata = params.get('rdata')
            actual_rdata = rec.get('rData', {}).get('value')
            if expected_rdata and actual_rdata:
                # Normalize both formats to continuous hex for comparison
                # API always returns: "01:02:03:04:DE:AD:BE:EF"
                # Input can be: "01020304deadbeef" OR "01:02:03:04:de:ad:be:ef"
                actual_continuous = actual_rdata.replace(':', '').lower()
                expected_continuous = expected_rdata.replace(':', '').lower()
                if actual_continuous != expected_continuous:
                    mismatch_details.append(
                        f"rdata: found '{actual_rdata}', expected '{expected_rdata}'")
            return mismatch_details

        # Check parameters for this record type
        required_params_for_type = required_params.get(record_type, [])
        exceptions = param_mapping_exceptions.get(record_type, {})

        for param_name in required_params_for_type:
            expected_value = params.get(param_name)
            # Use exception mapping if available, otherwise param maps to itself
            record_field = exceptions.get(param_name, param_name)

            # Most record data is nested in rData object
            rdata = rec.get('rData', {})
            actual_value = rdata.get(record_field)

            # If not found in rData, check top level (for fields like ttl, name, etc.)
            if actual_value is None:
                actual_value = rec.get(record_field)

            # Special handling for svcParams in HTTPS/SVCB records
            if param_name == 'svcParams' and record_type in ['HTTPS', 'SVCB']:
                if isinstance(actual_value, dict) and isinstance(expected_value, str):
                    # Convert API dict format to pipe-delimited string for comparison
                    actual_params_str = '|'.join(
                        f'{k}|{v}' for k, v in actual_value.items())
                    converted_match = (actual_params_str == expected_value)
                    if converted_match:
                        continue  # Skip the normal comparison

            # Special handling for SSHFP fingerprints (case-insensitive comparison)
            if param_name == 'sshfpFingerprint' and record_type == 'SSHFP':
                if isinstance(actual_value, str) and isinstance(expected_value, str):
                    if actual_value.upper() == expected_value.upper():
                        continue  # Skip the normal comparison

            # Special handling for TLSA records (numeric to text conversion and case-insensitive)
            if record_type == 'TLSA':
                # TLSA certificate data case-insensitive comparison
                if param_name == 'tlsaCertificateAssociationData':
                    if isinstance(actual_value, str) and isinstance(expected_value, str):
                        if actual_value.upper() == expected_value.upper():
                            continue  # Skip the normal comparison

            if expected_value is not None and actual_value != expected_value:
                # Try type conversion for numeric comparisons (e.g., CAA flags "0" vs 0)
                converted_match = False
                if isinstance(actual_value, int) and isinstance(expected_value, str):
                    try:
                        converted_match = (actual_value == int(expected_value))
                    except ValueError:
                        pass
                elif isinstance(actual_value, str) and isinstance(expected_value, int):
                    try:
                        converted_match = (int(actual_value) == expected_value)
                    except ValueError:
                        pass

                if not converted_match:
                    mismatch_details.append(
                        f"{param_name}: found '{actual_value}', expected '{expected_value}'")

        return mismatch_details


if __name__ == '__main__':
    module = DeleteRecordModule()
    module.run()
