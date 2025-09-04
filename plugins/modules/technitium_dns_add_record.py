#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to add DNS records to Technitium DNS using TechnitiumModule base class

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_add_record
short_description: Add a DNS record to a Technitium DNS zone
version_added: "0.0.1"
author: Frank Muise (@effectivelywild)
requirements:
  - requests
description:
    - Add a DNS record to a Technitium DNS zone.
    - The module supports all DNS record types.
    - Some parameters are only valid or required for specific record types.
    - For example, C(ipAddress) is required for A and AAAA records, while C(cname) is required for CNAME records.
seealso:
    - module: effectivelywild.technitium_dns.technitium_dns_delete_record
      description: Used to delete DNS records
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
# Basic A record
- name: Add an A record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "www.example.com"
    type: "A"
    ipAddress: "192.0.2.1"
    ttl: 3600
    validate_certs: false

# A record with PTR creation
- name: Add an A record with reverse PTR
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "server.example.com"
    zone: "example.com"
    type: "A"
    ipAddress: "192.0.2.10"
    ptr: true
    createPtrZone: true
    ttl: 3600

# AAAA (IPv6) record
- name: Add an AAAA record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "ipv6.example.com"
    zone: "example.com"
    type: "AAAA"
    ipAddress: "2001:db8::1"
    ttl: 3600

# CNAME record
- name: Add a CNAME record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "alias.example.com"
    zone: "example.com"
    type: "CNAME"
    cname: "www.example.com"
    ttl: 3600

# MX record
- name: Add an MX record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    zone: "example.com"
    type: "MX"
    exchange: "mail.example.com"
    preference: 10
    ttl: 3600

# TXT record
- name: Add a TXT record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    zone: "example.com"
    type: "TXT"
    text: "v=spf1 include:_spf.google.com ~all"
    ttl: 3600

# TXT record with split text
- name: Add a long TXT record with split text
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_dmarc.example.com"
    zone: "example.com"
    type: "TXT"
    text: "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com; ruf=mailto:dmarc@example.com; sp=quarantine"
    splitText: true
    ttl: 3600

# SRV record
- name: Add an SRV record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_sip._tcp.example.com"
    zone: "example.com"
    type: "SRV"
    priority: 10
    weight: 20
    srv_port: 5060
    target: "sip.example.com"
    ttl: 3600

# NS record
- name: Add an NS record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "subdomain.example.com"
    zone: "example.com"
    type: "NS"
    nameServer: "ns1.subdomain.example.com"
    ttl: 86400

# NS record with glue
- name: Add an NS record with glue
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "subdomain.example.com"
    type: "NS"
    nameServer: "ns1.subdomain.example.com"
    glue: "192.0.2.100"
    ttl: 86400

# PTR record
- name: Add a PTR record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "1.2.0.192.in-addr.arpa"
    type: "PTR"
    ptrName: "www.example.com"
    ttl: 3600

# CAA record
- name: Add a CAA record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    type: "CAA"
    flags: 0
    tag: "issue"
    value: "letsencrypt.org"
    ttl: 3600

# ANAME record (alias at apex)
- name: Add an ANAME record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    type: "ANAME"
    aname: "target.example.net"
    ttl: 3600

# SSHFP record
- name: Add an SSHFP record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "server.example.com"
    type: "SSHFP"
    sshfpAlgorithm: RSA
    sshfpFingerprintType: SHA256
    sshfpFingerprint: "123456789abcdef67890123456789abcdef67890"
    ttl: 3600

# HTTPS record
- name: Add an HTTPS record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    zone: "example.com"
    type: "HTTPS"
    svcPriority: 1
    svcTargetName: "svc.example.com"
    svcParams: "alpn|h2,h3"
    ttl: 3600

# SVCB record
- name: Add an SVCB record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_svc.example.com"
    zone: "example.com"
    type: "SVCB"
    svcPriority: 1
    svcTargetName: "svc.example.com"
    svcParams: "port|443"
    ttl: 3600

# TLSA record
- name: Add a TLSA record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_443._tcp.example.com"
    zone: "example.com"
    type: "TLSA"
    tlsaCertificateUsage: PKIX-TA
    tlsaSelector: Cert
    tlsaMatchingType: SHA2-256
    tlsaCertificateAssociationData: "abcdef1234567890abcdef1234567890abcdef12"
    ttl: 3600

# URI record
- name: Add a URI record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_http._tcp.example.com"
    zone: "example.com"
    type: "URI"
    uriPriority: 10
    uriWeight: 1
    uri: "https://example.com/path"
    ttl: 3600

# DS record
- name: Add a DS record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "secure.example.com"
    zone: "example.com"
    type: "DS"
    keyTag: 12345
    algorithm: RSASHA256
    digestType: SHA256
    digest: "abcdef1234567890abcdef1234567890abcdef1234567890"
    ttl: 86400

# FWD record
- name: Add a FWD record
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "fwdrec.fwd.example.com"
    zone: "fwd.example.com"
    type: "FWD"
    protocol: Udp, 
    forwarder: 192.0.2.10
    forwarderPriority: 10

# Record with overwrite and comments
- name: Add record with overwrite and comments
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "test.example.com"
    zone: "example.com"
    type: "A"
    ipAddress: "192.0.2.99"
    ttl: 300
    overwrite: true
    comments: "Test server - overwrite existing"

# Record with expiry
- name: Add temporary record with expiry
  technitium_dns_add_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "temp.example.com"
    zone: "example.com"
    type: "A"
    ipAddress: "192.0.2.200"
    ttl: 300
    expiryTtl: 3600  # Auto-delete after 1 hour

# Using custom port and HTTPS
- name: Add record using custom API port and HTTPS
  technitium_dns_add_record:
    api_url: "https://dns.example.com"
    api_port: 8443
    api_token: "myapitoken"
    name: "secure.example.com"
    zone: "example.com"
    type: "A"
    ipAddress: "192.0.2.50"
    ttl: 3600
    validate_certs: true
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
            contains:
                addedRecord:
                    description: The details of the record that was added or modified.
                    type: dict
                    returned: always
                    contains:
                        disabled:
                            description: Whether the record is disabled.
                            type: bool
                            returned: always
                        dnssecStatus:
                            description: The DNSSEC status of the record.
                            type: str
                            returned: always
                        expiryTtl:
                            description: The record's expiration TTL in seconds.
                            type: int
                            returned: always
                        expiryTtlString:
                            description: The record's expiration TTL as a human-readable string.
                            type: str
                            returned: always
                        lastModified:
                            description: The date and time the record was last modified.
                            type: str
                            returned: always
                        lastUsedOn:
                            description: The date and time the record was last used.
                            type: str
                            returned: always
                        name:
                            description: The full domain name of the record.
                            type: str
                            returned: always
                        rData:
                            description: The data specific to the record type.
                            type: dict
                            returned: always
                            contains:
                                ipAddress:
                                    description: The IP address for A/AAAA records.
                                    type: str
                                    returned: when record is of type A or AAAA
                                otherOptions:
                                    description: Other options that would have been passed when creating the record
                                    type: str
                                    returned: When option was used adding that record, don't want to add every option here
                        ttl:
                            description: The record's TTL in seconds.
                            type: int
                            returned: always
                        ttlString:
                            description: The record's TTL as a human-readable string.
                            type: str
                            returned: always
                        type:
                            description: The type of the DNS record.
                            type: str
                            returned: always
                zone:
                    description: Information about the zone the record belongs to.
                    type: dict
                    returned: always
                    contains:
                        catalog:
                            description: The zone's catalog.
                            type: str
                            returned: always
                        disabled:
                            description: Whether the zone is disabled.
                            type: bool
                            returned: always
                        dnssecStatus:
                            description: The DNSSEC status of the zone.
                            type: str
                            returned: always
                        internal:
                            description: Whether the zone is internal.
                            type: bool
                            returned: always
                        lastModified:
                            description: The date and time the zone was last modified.
                            type: str
                            returned: always
                        name:
                            description: The name of the zone.
                            type: str
                            returned: always
                        notifyFailed:
                            description: Whether zone notification failed.
                            type: bool
                            returned: always
                        notifyFailedFor:
                            description: A list of hosts for which notification failed.
                            type: list
                            returned: always
                        soaSerial:
                            description: The SOA serial number of the zone.
                            type: int
                            returned: always
                        type:
                            description: The type of the zone.
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

class AddRecordModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True, aliases=['domain']),
        zone=dict(type='str', required=False),
        type=dict(type='str', required=True, choices=[
            'A', 'AAAA', 'NS', 'CNAME', 'PTR', 'MX', 'TXT', 'SRV', 'NAPTR', 'DNAME', 'DS', 'SSHFP', 'TLSA', 'SVCB', 'HTTPS', 'URI', 'CAA', 'ANAME', 'FWD', 'APP', 'UNKNOWN'
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
        keyTag=dict(type='int', required=False),
        algorithm=dict(type='str', required=False, choices=[
            'RSAMD5', 'DSA', 'RSASHA1', 'DSA-NSEC3-SHA1', 'RSASHA1-NSEC3-SHA1', 'RSASHA256', 'RSASHA512', 'ECC-GOST', 'ECDSAP256SHA256', 'ECDSAP384SHA384', 'ED25519', 'ED448'
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
        proxyPassword=dict(type='str', required=False),
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
        
        # Parameter validation maps for different DNS record types
        # Each record type has specific parameters that are allowed/required
        # Using new parameter names to avoid conflicts with Ansible module reserved names
        allowed_params = {
            'A': {'ipAddress','ttl','overwrite','comments','expiryTtl','ptr','createPtrZone','updateSvcbHints'},
            'AAAA': {'ipAddress','ttl','overwrite','comments','expiryTtl','ptr','createPtrZone','updateSvcbHints'},
            'NS': {'nameServer','glue','ttl','overwrite','comments','expiryTtl'},
            'CNAME': {'cname','ttl','overwrite','comments','expiryTtl'},
            'PTR': {'ptrName','ttl','overwrite','comments','expiryTtl'},
            'MX': {'exchange','preference','ttl','overwrite','comments','expiryTtl'},
            'TXT': {'text','splitText','ttl','overwrite','comments','expiryTtl'},
            'SRV': {'priority','weight','srv_port','target','ttl','overwrite','comments','expiryTtl'},
            'NAPTR': {'naptrOrder','naptrPreference','naptrFlags','naptrServices','naptrRegexp','naptrReplacement','ttl','overwrite','comments','expiryTtl'},
            'DNAME': {'dname','ttl','overwrite','comments','expiryTtl'},
            'DS': {'keyTag','algorithm','digestType','digest','ttl','overwrite','comments','expiryTtl'},
            'SSHFP': {'sshfpAlgorithm','sshfpFingerprintType','sshfpFingerprint','ttl','overwrite','comments','expiryTtl'},
            'TLSA': {'tlsaCertificateUsage','tlsaSelector','tlsaMatchingType','tlsaCertificateAssociationData','ttl','overwrite','comments','expiryTtl'},
            'SVCB': {'svcPriority','svcTargetName','svcParams','autoIpv4Hint','autoIpv6Hint','ttl','overwrite','comments','expiryTtl'},
            'HTTPS': {'svcPriority','svcTargetName','svcParams','autoIpv4Hint','autoIpv6Hint','ttl','overwrite','comments','expiryTtl'},
            'CAA': {'flags','tag','value','ttl','overwrite','comments','expiryTtl'},
            'ANAME': {'aname','ttl','overwrite','comments','expiryTtl'},
            'FWD': {'ttl','protocol','forwarder','forwarderPriority','dnssecValidation','proxyType','proxyAddress','proxyPort','proxyUsername','proxyPassword','overwrite','comments','expiryTtl'},
            'APP': {'appName','classPath','recordData','ttl','overwrite','comments','expiryTtl'},
            'UNKNOWN': {'rdata','ttl','overwrite','comments','expiryTtl'},
            'URI': {'uriPriority','uriWeight','uri','ttl','overwrite','comments','expiryTtl'}
        }
        required_params = {
            'A': ['ipAddress'],
            'AAAA': ['ipAddress'],
            'NS': ['nameServer'],
            'CNAME': ['cname'],
            'PTR': ['ptrName'],
            'MX': ['exchange','preference'],
            'TXT': ['text'],
            'SRV': ['priority','weight','srv_port','target'],
            'NAPTR': ['naptrOrder','naptrPreference'],
            'DNAME': ['dname'],
            'DS': ['keyTag','algorithm','digestType','digest'],
            'SSHFP': ['sshfpAlgorithm','sshfpFingerprintType','sshfpFingerprint'],
            'TLSA': ['tlsaCertificateUsage','tlsaSelector','tlsaMatchingType','tlsaCertificateAssociationData'],
            'SVCB': ['svcPriority','svcTargetName','svcParams'],
            'HTTPS': ['svcPriority','svcTargetName','svcParams'],
            'CAA': ['flags','tag','value'],
            'ANAME': ['aname'],
            'FWD': ['protocol','forwarder'],
            'APP': ['appName','classPath','recordData'],
            'UNKNOWN': ['rdata'],
            'URI': ['uriPriority','uriWeight','uri'],
        }
        # Validate allowed/required params
        if record_type in allowed_params:
            for param in params:
                # Skip core connection/control params and the canonical name param (domain) plus its alias (name)
                if param in ['api_url','api_port','api_token','domain','name','zone','type','validate_certs']:
                    continue
                if params[param] is not None and param not in allowed_params[record_type]:
                    self.fail_json(msg=f"Parameter '{param}' is not supported for record type '{record_type}'.")
        if record_type in required_params:
            for req in required_params[record_type]:
                param_value = params.get(req)
                if param_value is None:
                    self.fail_json(msg=f"Parameter '{req}' is required for record type '{record_type}'.")
                # Special handling for parameters that can be 0 or empty string
                if req in ['svcPriority'] and param_value == 0:
                    continue  # 0 is valid for svcPriority (alias mode)

        # Check mode support: determine if record would be created without making changes
        if self.check_mode:
            # Build query to fetch existing records for this domain
            get_query = {
                'domain': params['name'],
                'token': self.api_token
            }
            if params.get('zone'):
                get_query['zone'] = params['zone']
            get_resp = self.request('/api/zones/records/get', params=get_query)
            if get_resp.get('status') != 'ok':
                self.fail_json(msg=f"Technitium API error (check mode fetch): {get_resp.get('errorMessage') or 'Unknown'}", api_response=get_resp)
            existing_records = get_resp.get('response', {}).get('records', [])
            # Technitium API may return record type with capitalization (e.g. 'Unknown') so compare case-insensitively
            type_exists = any((r.get('type') or '').upper() == record_type for r in existing_records)
            overwrite = params.get('overwrite', False)
            # If overwrite requested we report changed even if exists (would replace set)
            would_change = (not type_exists) or overwrite
            msg = "(check mode) DNS record would be added." if would_change else "(check mode) Record already exists."
            self.exit_json(changed=would_change, msg=msg, api_response={'status': 'ok', 'check_mode': True, 'record_type_exists': type_exists})
        
        # Build query, mapping internal names to API names
        query = {}
        for key in self.argument_spec:
            val = params.get(key)
            if val is not None:
                if isinstance(val, bool):
                    val = str(val).lower()
                # Map internal names to API names for conflicting params
                if key == 'srv_port':
                    query['port'] = val
                elif key in ['api_port', 'validate_certs']:
                    # Used only for connection/module config, not sent to API
                    continue
                else:
                    query[key] = val
        query['token'] = self.api_token
        query['domain'] = self.name
        data = self.request('/api/zones/records/add', params=query)
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            if 'record already exists' in error_msg.lower():
                self.exit_json(changed=False, msg=f"Record already exists.", api_response={'status': 'ok', 'msg': f"Record already exists."})
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
        self.exit_json(changed=True, msg="DNS record added.", api_response=data)

def main():
    module = AddRecordModule()
    module()

if __name__ == '__main__':
    main()
