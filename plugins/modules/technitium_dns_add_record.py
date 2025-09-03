#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to add DNS records to Technitium DNS using TechnitiumModule base class

from ansible_collections.technitium.dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_add_record
short_description: Add a DNS record to a Technitium DNS zone
version_added: "0.0.1"
description:
    - Add a DNS resource record to a Technitium DNS authoritative zone using its API.
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
    name:
        description:
            - The record name (e.g., test.example.com).
            - The use of domain is also supported to align with API.
        required: true
        type: str
    zone:
        description:
            - The authoritative zone name (optional, defaults to closest match).
        required: false
        type: str
    type:
        description:
            - The DNS record type (A, AAAA, CNAME, MX, etc).
        required: true
        type: str
    ttl:
        description:
            - TTL for the record in seconds.
        required: false
        type: int
    overwrite:
        description:
            - Overwrite existing record set for this type.
        required: false
        type: bool
        default: false
    comments:
        description:
            - Comments for the record.
        required: false
        type: str
    expiryTtl:
        description:
            - Expiry in seconds for auto-deletion.
        required: false
        type: int
    ipAddress:
        description:
            - IP address for A/AAAA record.
        required: false
        type: str
    ptr:
        description:
            - Add reverse PTR record (A/AAAA only).
        required: false
        type: bool
    createPtrZone:
        description:
            - Create reverse zone for PTR (A/AAAA only).
        required: false
        type: bool
    updateSvcbHints:
        description:
            - Update SVCB/HTTPS hints (A/AAAA only).
        required: false
        type: bool
    nameServer:
        description:
            - Name server domain (NS only).
        required: false
        type: str
    glue:
        description:
            - Glue address for NS record.
        required: false
        type: str
    cname:
        description:
            - CNAME target (CNAME only).
        required: false
        type: str
    ptrName:
        description:
            - PTR domain name (PTR only).
        required: false
        type: str
    exchange:
        description:
            - MX exchange domain (MX only).
        required: false
        type: str
    preference:
        description:
            - MX preference (MX only).
        required: false
        type: int
    text:
        description:
            - TXT record text (TXT only).
        required: false
        type: str
    splitText:
        description:
            - Split TXT into multiple strings (TXT only).
        required: false
        type: bool
    mailbox:
        description:
            - Responsible mailbox for MX record.
        required: false
        type: str
    txtDomain:
        description:
            - Domain for TXT record (if different from the main domain).
        required: false
        type: str
    priority:
        description:
            - Priority for SRV record.
        required: false
        type: int
    weight:
        description:
            - Weight for SRV record.
        required: false
        type: int
    port:
        description:
            - Port for SRV record.
        required: false
        type: int
    target:
        description:
            - Target for SRV record.
        required: false
        type: str
    naptrOrder:
        description:
            - Order for NAPTR record.
        required: false
        type: int
    naptrPreference:
        description:
            - Preference for NAPTR record.
        required: false
        type: int
    naptrFlags:
        description:
            - Flags for NAPTR record.
        required: false
        type: str
    naptrServices:
        description:
            - Services for NAPTR record.
        required: false
        type: str
    naptrRegexp:
        description:
            - Regular expression for NAPTR record.
        required: false
        type: str
    naptrReplacement:
        description:
            - Replacement string for NAPTR record.
        required: false
        type: str
    dname:
        description:
            - DNAME target.
        required: false
        type: str
    keyTag:
        description:
            - Key tag for DNSKEY record.
        required: false
        type: int
    algorithm:
        description:
            - Algorithm for DNSKEY record.
        required: false
        type: str
    digestType:
        description:
            - Digest type for DS and SSHFP records.
        required: false
        type: str
    digest:
        description:
            - Digest for DS and SSHFP records.
        required: false
        type: str
    sshfpAlgorithm:
        description:
            - SSHFP algorithm.
        required: false
        type: str
    sshfpFingerprintType:
        description:
            - SSHFP fingerprint type.
        required: false
        type: str
    sshfpFingerprint:
        description:
            - SSHFP fingerprint.
        required: false
        type: str
    tlsaCertificateUsage:
        description:
            - TLSA certificate usage.
        required: false
        type: str
    tlsaSelector:
        description:
            - TLSA selector.
        required: false
        type: str
    tlsaMatchingType:
        description:
            - TLSA matching type.
        required: false
        type: str
    tlsaCertificateAssociationData:
        description:
            - TLSA certificate association data.
        required: false
        type: str
    svcPriority:
        description:
            - SVCB/HTTPS priority.
        required: false
        type: int
    svcTargetName:
        description:
            - SVCB/HTTPS target name.
        required: false
        type: str
    svcParams:
        description:
            - SVCB/HTTPS parameters.
        required: false
        type: str
    autoIpv4Hint:
        description:
            - Automatic IPv4 hint.
        required: false
        type: bool
    autoIpv6Hint:
        description:
            - Automatic IPv6 hint.
        required: false
        type: bool
    uriPriority:
        description:
            - URI priority.
        required: false
        type: int
    uriWeight:
        description:
            - URI weight.
        required: false
        type: int
    uri:
        description:
            - URI target.
        required: false
        type: str
    flags:
        description:
            - Flags for CAA record.
        required: false
        type: str
    tag:
        description:
            - Tag for CAA record.
        required: false
        type: str
    value:
        description:
            - Value for CAA record.
        required: false
        type: str
    aname:
        description:
            - ANAME target.
        required: false
        type: str
    protocol:
        description:
            - Protocol for FWD record.
        required: false
        type: str
    forwarder:
        description:
            - Forwarder address for FWD record.
        required: false
        type: str
    forwarderPriority:
        description:
            - Forwarder priority for FWD record.
        required: false
        type: int
    dnssecValidation:
        description:
            - DNSSEC validation flag.
        required: false
        type: bool
    proxyType:
        description:
            - Proxy type for FWD record.
        required: false
        type: str
    proxyAddress:
        description:
            - Proxy address for FWD record.
        required: false
        type: str
    proxyPort:
        description:
            - Proxy port for FWD record.
        required: false
        type: int
    proxyUsername:
        description:
            - Proxy username for FWD record.
        required: false
        type: str
    proxyPassword:
        description:
            - Proxy password for FWD record.
        required: false
        type: str
    appName:
        description:
            - Application name for APP record.
        required: false
        type: str
    classPath:
        description:
            - Class path for APP record.
        required: false
        type: str
    recordData:
        description:
            - Record data for APP record.
        required: false
        type: str
    rdata:
        description:
            - Used for adding unknown i.e. unsupported record types. The value must be formatted as a hex string or a colon separated hex string
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
    zone: "example.com"
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
    sshfpAlgorithm: 1
    sshfpFingerprintType: 1
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
    tlsaCertificateUsage: 3
    tlsaSelector: 1
    tlsaMatchingType: 1
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
    algorithm: 7
    digestType: 1
    digest: "abcdef1234567890abcdef1234567890abcdef1234567890"
    ttl: 86400

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
