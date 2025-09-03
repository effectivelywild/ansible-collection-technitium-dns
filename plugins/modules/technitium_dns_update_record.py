#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ansible module to update DNS records in Technitium DNS using TechnitiumModule base class

from ansible_collections.technitium.dns.plugins.module_utils.technitium import TechnitiumModule

DOCUMENTATION = r'''
---
module: technitium_dns_update_record
short_description: Update a DNS record in a Technitium DNS zone
version_added: "0.0.1"
description:
    - Update an existing DNS resource record in a Technitium DNS authoritative zone using its API.
    - This module is idempotent - it will only make changes if the record properties differ from what is specified.
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
        aliases: ['domain']
    zone:
        description:
            - The authoritative zone name (optional, defaults to closest match).
        required: false
        type: str
    type:
        description:
            - The DNS record type to update.
        required: true
        type: str
    # Common record parameters
    newDomain:
        description:
            - The new domain name to be set for the record (to rename subdomain).
        required: false
        type: str
    ttl:
        description:
            - The TTL value of the resource record. Default value of 3600 is used when parameter is missing.
        required: false
        type: int
        default: null
    disable:
        description:
            - Specifies if the record should be disabled. The default value is false when this parameter is missing.
        required: false
        type: bool
        default: false
    overwrite:
        description:
            - Overwrite existing record set for this type.
        required: false
        type: bool
        default: false
    comments:
        description:
            - Sets comments for the updated resource record.
        required: false
        type: str
    expiryTtl:
        description:
            - Set to automatically delete the record when the value in seconds elapses since the record's last modified time.
        required: false
        type: int
    # A/AAAA record parameters
    ipAddress:
        description:
            - The current IP address in the A or AAAA record. This parameter is required when updating A or AAAA record.
        required: false
        type: str
    newIpAddress:
        description:
            - The new IP address in the A or AAAA record. This parameter when missing will use the current value in the record.
        required: false
        type: str
    ptr:
        description:
            - Set this option to true to specify if the PTR record associated with the A or AAAA record must also be updated.
        required: false
        type: bool
    createPtrZone:
        description:
            - Set this option to true to create a reverse zone for PTR record. This option is used only for A and AAAA records.
        required: false
        type: bool
    updateSvcbHints:
        description:
            - Set this option to true to update any SVCB/HTTPS records in the zone that has Automatic Hints option enabled.
        required: false
        type: bool
    # NS record parameters
    nameServer:
        description:
            - The current name server domain name. This option is required for updating NS record.
        required: false
        type: str
    newNameServer:
        description:
            - The new server domain name. This option is used for updating NS record.
        required: false
        type: str
    glue:
        description:
            - The comma separated list of IP addresses set as glue for the NS record.
        required: false
        type: str
    # CNAME record parameters
    cname:
        description:
            - The CNAME domain name to update in the existing CNAME record.
        required: false
        type: str
    # SOA record parameters
    primaryNameServer:
        description:
            - This is the primary name server parameter in the SOA record. This parameter is required when updating the SOA record.
        required: false
        type: str
    responsiblePerson:
        description:
            - This is the responsible person parameter in the SOA record. This parameter is required when updating the SOA record.
        required: false
        type: str
    serial:
        description:
            - This is the serial parameter in the SOA record. This parameter is required when updating the SOA record.
        required: false
        type: int
    refresh:
        description:
            - This is the refresh parameter in the SOA record. This parameter is required when updating the SOA record.
        required: false
        type: int
    retry:
        description:
            - This is the retry parameter in the SOA record. This parameter is required when updating the SOA record.
        required: false
        type: int
    expire:
        description:
            - This is the expire parameter in the SOA record. This parameter is required when updating the SOA record.
        required: false
        type: int
    minimum:
        description:
            - This is the minimum parameter in the SOA record. This parameter is required when updating the SOA record.
        required: false
        type: int
    useSerialDateScheme:
        description:
            - Set value to true to enable using date scheme for SOA serial. This parameter is required when updating the SOA record.
        required: false
        type: bool
    # PTR record parameters
    ptrName:
        description:
            - The current PTR domain name. This option is required for updating PTR record.
        required: false
        type: str
    newPtrName:
        description:
            - The new PTR domain name. This option is required for updating PTR record.
        required: false
        type: str
    # MX record parameters
    preference:
        description:
            - The current preference value in an MX record. This parameter when missing will default to 1 value.
        required: false
        type: int
    newPreference:
        description:
            - The new preference value in an MX record. This parameter when missing will use the old value.
        required: false
        type: int
    exchange:
        description:
            - The current exchange domain name. This option is required for updating MX record.
        required: false
        type: str
    newExchange:
        description:
            - The new exchange domain name. This option is required for updating MX record.
        required: false
        type: str
    # TXT record parameters
    text:
        description:
            - The current text value. This option is required for updating TXT record.
        required: false
        type: str
    newText:
        description:
            - The new text value. This option is required for updating TXT record.
        required: false
        type: str
    splitText:
        description:
            - The current split text value. This option is used for updating TXT record and is set to false when unspecified.
        required: false
        type: bool
    newSplitText:
        description:
            - The new split text value. This option is used for updating TXT record and is set to current split text value when unspecified.
        required: false
        type: bool
    # SRV record parameters
    priority:
        description:
            - This is the current priority in the SRV record. This parameter is required when updating the SRV record.
        required: false
        type: int
    newPriority:
        description:
            - This is the new priority in the SRV record. This parameter when missing will use the old value.
        required: false
        type: int
    weight:
        description:
            - This is the current weight in the SRV record. This parameter is required when updating the SRV record.
        required: false
        type: int
    newWeight:
        description:
            - This is the new weight in the SRV record. This parameter when missing will use the old value.
        required: false
        type: int
    srv_port:
        description:
            - This is the port parameter in the SRV record. This parameter is required when updating the SRV record.
        required: false
        type: int
    newSrvPort:
        description:
            - This is the new value of the port parameter in the SRV record. This parameter when missing will use the old value.
        required: false
        type: int
    target:
        description:
            - The current target value. This parameter is required when updating the SRV record.
        required: false
        type: str
    newTarget:
        description:
            - The new target value. This parameter when missing will use the old value.
        required: false
        type: str
    # CAA record parameters
    flags:
        description:
            - This is the flags parameter in the CAA record. This parameter is required when updating the CAA record.
        required: false
        type: int
    newFlags:
        description:
            - This is the new value of the flags parameter in the CAA record.
        required: false
        type: int
    tag:
        description:
            - This is the tag parameter in the CAA record. This parameter is required when updating the CAA record.
        required: false
        type: str
    newTag:
        description:
            - This is the new value of the tag parameter in the CAA record.
        required: false
        type: str
    value:
        description:
            - The current value in CAA record. This parameter is required when updating the CAA record.
        required: false
        type: str
    newValue:
        description:
            - The new value in CAA record. This parameter is required when updating the CAA record.
        required: false
        type: str
    # ANAME record parameters
    aname:
        description:
            - The current ANAME domain name. This parameter is required when updating the ANAME record.
        required: false
        type: str
    newAName:
        description:
            - The new ANAME domain name. This parameter is required when updating the ANAME record.
        required: false
        type: str
    # FWD record parameters
    protocol:
        description:
            - This is the current protocol value in the FWD record. Valid values are [Udp, Tcp, Tls, Https, Quic].
        required: false
        type: str
        choices: ['Udp', 'Tcp', 'Tls', 'Https', 'Quic']
    newProtocol:
        description:
            - This is the new protocol value in the FWD record. Valid values are [Udp, Tcp, Tls, Https, Quic].
        required: false
        type: str
        choices: ['Udp', 'Tcp', 'Tls', 'Https', 'Quic']
    forwarder:
        description:
            - The current forwarder address. This parameter is required when updating the FWD record.
        required: false
        type: str
    newForwarder:
        description:
            - The new forwarder address. This parameter is required when updating the FWD record.
        required: false
        type: str
    forwarderPriority:
        description:
            - The current forwarder priority value. This optional parameter is to be used with FWD record.
        required: false
        type: int
    dnssecValidation:
        description:
            - Set this boolean value to indicate if DNSSEC validation must be done. This optional parameter is to be used with FWD records.
        required: false
        type: bool
    proxyType:
        description:
            - The type of proxy that must be used for conditional forwarding.
        required: false
        type: str
        choices: ['NoProxy', 'DefaultProxy', 'Http', 'Socks5']
    proxyAddress:
        description:
            - The proxy server address to use when proxyType is configured.
        required: false
        type: str
    proxyPort:
        description:
            - The proxy server port to use when proxyType is configured.
        required: false
        type: int
    proxyUsername:
        description:
            - The proxy server username to use when proxyType is configured.
        required: false
        type: str
    proxyPassword:
        description:
            - The proxy server password to use when proxyType is configured.
        required: false
        type: str
    # RP record parameters
    mailbox:
        description:
            - The current email address value. This option is required for updating RP record.
        required: false
        type: str
    newMailbox:
        description:
            - The new email address value. This option is used for updating RP record and is set to the current value when unspecified.
        required: false
        type: str
    txtDomain:
        description:
            - The current TXT record's domain name value. This option is required for updating RP record.
        required: false
        type: str
    newTxtDomain:
        description:
            - The new TXT record's domain name value. This option is used for updating RP record and is set to the current value when unspecified.
        required: false
        type: str
    # NAPTR record parameters
    naptrOrder:
        description:
            - The current value in the NAPTR record. This parameter is required when updating the NAPTR record.
        required: false
        type: int
    naptrNewOrder:
        description:
            - The new value in the NAPTR record. This parameter when missing will use the old value.
        required: false
        type: int
    naptrPreference:
        description:
            - The current value in the NAPTR record. This parameter is required when updating the NAPTR record.
        required: false
        type: int
    naptrNewPreference:
        description:
            - The new value in the NAPTR record. This parameter when missing will use the old value.
        required: false
        type: int
    naptrFlags:
        description:
            - The current value in the NAPTR record. This parameter is required when updating the NAPTR record.
        required: false
        type: str
    naptrNewFlags:
        description:
            - The new value in the NAPTR record. This parameter when missing will use the old value.
        required: false
        type: str
    naptrServices:
        description:
            - The current value in the NAPTR record. This parameter is required when updating the NAPTR record.
        required: false
        type: str
    naptrNewServices:
        description:
            - The new value in the NAPTR record. This parameter when missing will use the old value.
        required: false
        type: str
    naptrRegexp:
        description:
            - The current value in the NAPTR record. This parameter is required when updating the NAPTR record.
        required: false
        type: str
    naptrNewRegexp:
        description:
            - The new value in the NAPTR record. This parameter when missing will use the old value.
        required: false
        type: str
    naptrReplacement:
        description:
            - The current value in the NAPTR record. This parameter is required when updating the NAPTR record.
        required: false
        type: str
    naptrNewReplacement:
        description:
            - The new value in the NAPTR record. This parameter when missing will use the old value.
        required: false
        type: str
    # DNAME record parameters
    dname:
        description:
            - The DNAME domain name. This parameter is required when updating the DNAME record.
        required: false
        type: str
    # DS record parameters
    keyTag:
        description:
            - This parameter is required when updating DS record.
        required: false
        type: int
    newKeyTag:
        description:
            - This parameter is required when updating DS record.
        required: false
        type: int
    algorithm:
        description:
            - This parameter is required when updating DS record.
        required: false
        type: str
    newAlgorithm:
        description:
            - This parameter is required when updating DS record.
        required: false
        type: str
    digestType:
        description:
            - This parameter is required when updating DS record.
        required: false
        type: str
    newDigestType:
        description:
            - This parameter is required when updating DS record.
        required: false
        type: str
    digest:
        description:
            - This parameter is required when updating DS record.
        required: false
        type: str
    newDigest:
        description:
            - This parameter is required when updating DS record.
        required: false
        type: str
    # SSHFP record parameters
    sshfpAlgorithm:
        description:
            - This parameter is required when updating SSHFP record.
        required: false
        type: str
    newSshfpAlgorithm:
        description:
            - This parameter is required when updating SSHFP record.
        required: false
        type: str
    sshfpFingerprintType:
        description:
            - This parameter is required when updating SSHFP record.
        required: false
        type: str
    newSshfpFingerprintType:
        description:
            - This parameter is required when updating SSHFP record.
        required: false
        type: str
    sshfpFingerprint:
        description:
            - This parameter is required when updating SSHFP record.
        required: false
        type: str
    newSshfpFingerprint:
        description:
            - This parameter is required when updating SSHFP record.
        required: false
        type: str
    # TLSA record parameters
    tlsaCertificateUsage:
        description:
            - This parameter is required when updating TLSA record.
        required: false
        type: str
    newTlsaCertificateUsage:
        description:
            - This parameter is required when updating TLSA record.
        required: false
        type: str
    tlsaSelector:
        description:
            - This parameter is required when updating TLSA record.
        required: false
        type: str
    newTlsaSelector:
        description:
            - This parameter is required when updating TLSA record.
        required: false
        type: str
    tlsaMatchingType:
        description:
            - This parameter is required when updating TLSA record.
        required: false
        type: str
    newTlsaMatchingType:
        description:
            - This parameter is required when updating TLSA record.
        required: false
        type: str
    tlsaCertificateAssociationData:
        description:
            - This parameter is required when updating TLSA record.
        required: false
        type: str
    newTlsaCertificateAssociationData:
        description:
            - This parameter is required when updating TLSA record.
        required: false
        type: str
    # SVCB/HTTPS record parameters
    svcPriority:
        description:
            - The priority value for SVCB or HTTPS record. This parameter is required for updating SCVB or HTTPS record.
        required: false
        type: int
    newSvcPriority:
        description:
            - The new priority value for SVCB or HTTPS record. This parameter when missing will use the old value.
        required: false
        type: int
    svcTargetName:
        description:
            - The target domain name for SVCB or HTTPS record. This parameter is required for updating SCVB or HTTPS record.
        required: false
        type: str
    newSvcTargetName:
        description:
            - The new target domain name for SVCB or HTTPS record. This parameter when missing will use the old value.
        required: false
        type: str
    svcParams:
        description:
            - The service parameters for SVCB or HTTPS record which is a pipe separated list of key and value. This parameter is required for updating SCVB or HTTPS record.
        required: false
        type: str
    newSvcParams:
        description:
            - The new service parameters for SVCB or HTTPS record which is a pipe separated list of key and value. This parameter when missing will use the old value.
        required: false
        type: str
    autoIpv4Hint:
        description:
            - Set this option to true to enable Automatic Hints for the ipv4hint parameter in the newSvcParams. This option is valid only for SVCB and HTTPS records.
        required: false
        type: bool
    autoIpv6Hint:
        description:
            - Set this option to true to enable Automatic Hints for the ipv6hint parameter in the newSvcParams. This option is valid only for SVCB and HTTPS records.
        required: false
        type: bool
    # URI record parameters
    uriPriority:
        description:
            - The priority value for the URI record. This parameter is required for updating the URI record.
        required: false
        type: int
    newUriPriority:
        description:
            - The new priority value for the URI record. This parameter when missing will use the old value.
        required: false
        type: int
    uriWeight:
        description:
            - The weight value for the URI record. This parameter is required for updating the URI record.
        required: false
        type: int
    newUriWeight:
        description:
            - The new weight value for the URI record. This parameter when missing will use the old value.
        required: false
        type: int
    uri:
        description:
            - The URI value for the URI record. This parameter is required for updating the URI record.
        required: false
        type: str
    newUri:
        description:
            - The new URI value for the URI record. This parameter when missing will use the old value.
        required: false
        type: str
    # APP record parameters
    appName:
        description:
            - This parameter is required for updating the APP record.
        required: false
        type: str
    classPath:
        description:
            - This parameter is required for updating the APP record.
        required: false
        type: str
    recordData:
        description:
            - This parameter is used for updating the APP record as per the DNS app requirements.
        required: false
        type: str
    # Unknown record type parameters
    rdata:
        description:
            - This parameter is used for updating unknown i.e. unsupported record types. The value must be formatted as a hex string.
        required: false
        type: str
    newRData:
        description:
            - This parameter is used for updating unknown i.e. unsupported record types. The new value must be formatted as a hex string.
        required: false
        type: str
'''

EXAMPLES = r'''
- name: Update A record IP address
  technitium_dns_update_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "test.example.com"
    type: "A"
    ipAddress: "192.168.1.100"
    newIpAddress: "192.168.1.101"

- name: Update MX record preference and exchange
  technitium_dns_update_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    type: "MX"
    preference: 10
    exchange: "old-mail.example.com"
    newPreference: 20
    newExchange: "new-mail.example.com"

- name: Update TXT record
  technitium_dns_update_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_dmarc.example.com"
    type: "TXT"
    text: "v=DMARC1; p=none"
    newText: "v=DMARC1; p=quarantine"

- name: Update SRV record
  technitium_dns_update_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "_sip._tcp.example.com"
    type: "SRV"
    priority: 10
    weight: 20
    srv_port: 5060
    target: "sip1.example.com"
    newPriority: 15
    newWeight: 25
    newSrvPort: 5061
    newTarget: "sip2.example.com"

- name: Update SOA record
  technitium_dns_update_record:
    api_url: "http://localhost"
    api_token: "myapitoken"
    name: "example.com"
    type: "SOA"
    primaryNameServer: "ns1.example.com"
    responsiblePerson: "admin.example.com"
    serial: 2024010101
    refresh: 3600
    retry: 1800
    expire: 604800
    minimum: 86400
'''

class UpdateRecordModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        name=dict(type='str', required=True, aliases=['domain']),
        zone=dict(type='str', required=False),
        type=dict(type='str', required=True, choices=[
            'A', 'AAAA', 'NS', 'CNAME', 'PTR', 'MX', 'TXT', 'RP', 'SRV', 'NAPTR', 'DNAME', 'DS', 'SSHFP', 'TLSA', 'SVCB', 'HTTPS', 'URI', 'CAA', 'ANAME', 'FWD', 'APP', 'UNKNOWN'
        ]),
        # Common parameters
        newDomain=dict(type='str', required=False),
        ttl=dict(type='int', required=False),
        disable=dict(type='bool', required=False, default=False),
        overwrite=dict(type='bool', required=False, default=False),
        comments=dict(type='str', required=False),
        expiryTtl=dict(type='int', required=False),
        # A/AAAA record parameters
        ipAddress=dict(type='str', required=False),
        newIpAddress=dict(type='str', required=False),
        ptr=dict(type='bool', required=False),
        createPtrZone=dict(type='bool', required=False),
        updateSvcbHints=dict(type='bool', required=False),
        # NS record parameters
        nameServer=dict(type='str', required=False),
        newNameServer=dict(type='str', required=False),
        glue=dict(type='str', required=False),
        # CNAME record parameters
        cname=dict(type='str', required=False),
        # SOA record parameters
        primaryNameServer=dict(type='str', required=False),
        responsiblePerson=dict(type='str', required=False),
        serial=dict(type='int', required=False),
        refresh=dict(type='int', required=False),
        retry=dict(type='int', required=False),
        expire=dict(type='int', required=False),
        minimum=dict(type='int', required=False),
        useSerialDateScheme=dict(type='bool', required=False),
        # PTR record parameters
        ptrName=dict(type='str', required=False),
        newPtrName=dict(type='str', required=False),
        # MX record parameters
        preference=dict(type='int', required=False),
        newPreference=dict(type='int', required=False),
        exchange=dict(type='str', required=False),
        newExchange=dict(type='str', required=False),
        # TXT record parameters
        text=dict(type='str', required=False),
        newText=dict(type='str', required=False),
        splitText=dict(type='bool', required=False),
        newSplitText=dict(type='bool', required=False),
        # RP record parameters
        mailbox=dict(type='str', required=False),
        newMailbox=dict(type='str', required=False),
        txtDomain=dict(type='str', required=False),
        newTxtDomain=dict(type='str', required=False),
        # SRV record parameters
        priority=dict(type='int', required=False),
        newPriority=dict(type='int', required=False),
        weight=dict(type='int', required=False),
        newWeight=dict(type='int', required=False),
        srv_port=dict(type='int', required=False),
        newSrvPort=dict(type='int', required=False),
        target=dict(type='str', required=False),
        newTarget=dict(type='str', required=False),
        # CAA record parameters
        flags=dict(type='int', required=False),
        newFlags=dict(type='int', required=False),
        tag=dict(type='str', required=False),
        newTag=dict(type='str', required=False),
        value=dict(type='str', required=False),
        newValue=dict(type='str', required=False),
        # ANAME record parameters
        aname=dict(type='str', required=False),
        newAName=dict(type='str', required=False),
        # FWD record parameters
        protocol=dict(type='str', required=False, choices=['Udp', 'Tcp', 'Tls', 'Https', 'Quic']),
        newProtocol=dict(type='str', required=False, choices=['Udp', 'Tcp', 'Tls', 'Https', 'Quic']),
        forwarder=dict(type='str', required=False),
        newForwarder=dict(type='str', required=False),
        forwarderPriority=dict(type='int', required=False),
        dnssecValidation=dict(type='bool', required=False),
        proxyType=dict(type='str', required=False, choices=['NoProxy', 'DefaultProxy', 'Http', 'Socks5']),
        proxyAddress=dict(type='str', required=False),
        proxyPort=dict(type='int', required=False),
        proxyUsername=dict(type='str', required=False),
        proxyPassword=dict(type='str', required=False),
        # NAPTR record parameters
        naptrOrder=dict(type='int', required=False),
        naptrNewOrder=dict(type='int', required=False),
        naptrPreference=dict(type='int', required=False),
        naptrNewPreference=dict(type='int', required=False),
        naptrFlags=dict(type='str', required=False),
        naptrNewFlags=dict(type='str', required=False),
        naptrServices=dict(type='str', required=False),
        naptrNewServices=dict(type='str', required=False),
        naptrRegexp=dict(type='str', required=False),
        naptrNewRegexp=dict(type='str', required=False),
        naptrReplacement=dict(type='str', required=False),
        naptrNewReplacement=dict(type='str', required=False),
        # DNAME record parameters
        dname=dict(type='str', required=False),
        # DS record parameters
        keyTag=dict(type='int', required=False),
        newKeyTag=dict(type='int', required=False),
        algorithm=dict(type='str', required=False, choices=[
            'RSAMD5', 'DSA', 'RSASHA1', 'DSA-NSEC3-SHA1', 'RSASHA1-NSEC3-SHA1', 'RSASHA256', 'RSASHA512', 'ECC-GOST', 'ECDSAP256SHA256', 'ECDSAP384SHA384', 'ED25519', 'ED448'
        ]),
        newAlgorithm=dict(type='str', required=False, choices=[
            'RSAMD5', 'DSA', 'RSASHA1', 'DSA-NSEC3-SHA1', 'RSASHA1-NSEC3-SHA1', 'RSASHA256', 'RSASHA512', 'ECC-GOST', 'ECDSAP256SHA256', 'ECDSAP384SHA384', 'ED25519', 'ED448'
        ]),
        digestType=dict(type='str', required=False, choices=[
            'SHA1', 'SHA256', 'GOST-R-34-11-94', 'SHA384'
        ]),
        newDigestType=dict(type='str', required=False, choices=[
            'SHA1', 'SHA256', 'GOST-R-34-11-94', 'SHA384'
        ]),
        digest=dict(type='str', required=False),
        newDigest=dict(type='str', required=False),
        # SSHFP record parameters
        sshfpAlgorithm=dict(type='str', required=False, choices=[
            'RSA', 'DSA', 'ECDSA', 'Ed25519', 'Ed448'
        ]),
        newSshfpAlgorithm=dict(type='str', required=False, choices=[
            'RSA', 'DSA', 'ECDSA', 'Ed25519', 'Ed448'
        ]),
        sshfpFingerprintType=dict(type='str', required=False, choices=[
            'SHA1', 'SHA256'
        ]),
        newSshfpFingerprintType=dict(type='str', required=False, choices=[
            'SHA1', 'SHA256'
        ]),
        sshfpFingerprint=dict(type='str', required=False),
        newSshfpFingerprint=dict(type='str', required=False),
        # TLSA record parameters
        tlsaCertificateUsage=dict(type='str', required=False, choices=[
            'PKIX-TA', 'PKIX-EE', 'DANE-TA', 'DANE-EE'
        ]),
        newTlsaCertificateUsage=dict(type='str', required=False, choices=[
            'PKIX-TA', 'PKIX-EE', 'DANE-TA', 'DANE-EE'
        ]),
        tlsaSelector=dict(type='str', required=False, choices=[
            'Cert', 'SPKI'
        ]),
        newTlsaSelector=dict(type='str', required=False, choices=[
            'Cert', 'SPKI'
        ]),
        tlsaMatchingType=dict(type='str', required=False, choices=[
            'Full', 'SHA2-256', 'SHA2-512'
        ]),
        newTlsaMatchingType=dict(type='str', required=False, choices=[
            'Full', 'SHA2-256', 'SHA2-512'
        ]),
        tlsaCertificateAssociationData=dict(type='str', required=False),
        newTlsaCertificateAssociationData=dict(type='str', required=False),
        # SVCB/HTTPS record parameters
        svcPriority=dict(type='int', required=False),
        newSvcPriority=dict(type='int', required=False),
        svcTargetName=dict(type='str', required=False),
        newSvcTargetName=dict(type='str', required=False),
        svcParams=dict(type='str', required=False),
        newSvcParams=dict(type='str', required=False),
        autoIpv4Hint=dict(type='bool', required=False),
        autoIpv6Hint=dict(type='bool', required=False),
        # URI record parameters
        uriPriority=dict(type='int', required=False),
        newUriPriority=dict(type='int', required=False),
        uriWeight=dict(type='int', required=False),
        newUriWeight=dict(type='int', required=False),
        uri=dict(type='str', required=False),
        newUri=dict(type='str', required=False),
        # APP record parameters
        appName=dict(type='str', required=False),
        classPath=dict(type='str', required=False),
        recordData=dict(type='str', required=False),
        # Unknown record type parameters
        rdata=dict(type='str', required=False),
        newRData=dict(type='str', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        params = self.params
        domain = params['name']  # Using 'name' parameter (with 'domain' alias support)
        zone = params.get('zone')
        record_type = params['type'].upper()

        # Validate record type specific parameters
        self._validate_allowed_parameters(record_type)
        self._validate_record_type_parameters(record_type)

        # Get current record to check if update is needed
        current_record = self._get_current_record(domain, zone, record_type)
        
        if not current_record:
            self.fail_json(msg=f"Record {domain} of type {record_type} not found. Cannot update non-existent record.")

        # Check if update is needed by comparing current and desired values
        update_needed = self._is_update_needed(current_record, record_type)

        if self.check_mode:
            if update_needed:
                self.exit_json(changed=True, msg="Record would be updated (check mode)", api_response={})
            else:
                self.exit_json(changed=False, msg="Record already matches desired state (check mode)", api_response={})

        # Implement idempotent update behavior
        if not update_needed:
            self.exit_json(
                changed=False, 
                msg=f"Record {domain} of type {record_type} already matches desired state",
                api_response={'status': 'ok', 'record': current_record}
            )

        # Build API query parameters for update
        query = self._build_update_query(domain, zone, record_type)

        # Update the record via the Technitium API
        data = self.request('/api/zones/records/update', params=query)
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Technitium API error: {error_msg}", api_response=data)
            
        # Return success - record was updated
        self.exit_json(
            changed=True, 
            msg=f"Record {domain} of type {record_type} updated successfully",
            api_response=data
        )

    def _validate_allowed_parameters(self, record_type):
        """Validate that only allowed parameters are provided for the specific record type."""
        params = self.params
        
        # Parameter validation maps for different DNS record types
        # Each record type has specific parameters that are allowed
        allowed_params = {
            'A': {'ipAddress', 'newIpAddress', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl', 'ptr', 'createPtrZone', 'updateSvcbHints'},
            'AAAA': {'ipAddress', 'newIpAddress', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl', 'ptr', 'createPtrZone', 'updateSvcbHints'},
            'NS': {'nameServer', 'newNameServer', 'glue', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'CNAME': {'cname', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'SOA': {'primaryNameServer', 'responsiblePerson', 'serial', 'refresh', 'retry', 'expire', 'minimum', 'useSerialDateScheme', 'ttl', 'disable', 'comments', 'expiryTtl'},
            'PTR': {'ptrName', 'newPtrName', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'MX': {'preference', 'newPreference', 'exchange', 'newExchange', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'TXT': {'text', 'newText', 'splitText', 'newSplitText', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'RP': {'mailbox', 'newMailbox', 'txtDomain', 'newTxtDomain', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'SRV': {'priority', 'newPriority', 'weight', 'newWeight', 'srv_port', 'newSrvPort', 'target', 'newTarget', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'NAPTR': {'naptrOrder', 'naptrNewOrder', 'naptrPreference', 'naptrNewPreference', 'naptrFlags', 'naptrNewFlags', 'naptrServices', 'naptrNewServices', 'naptrRegexp', 'naptrNewRegexp', 'naptrReplacement', 'naptrNewReplacement', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'DNAME': {'dname', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'DS': {'keyTag', 'newKeyTag', 'algorithm', 'newAlgorithm', 'digestType', 'newDigestType', 'digest', 'newDigest', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'SSHFP': {'sshfpAlgorithm', 'newSshfpAlgorithm', 'sshfpFingerprintType', 'newSshfpFingerprintType', 'sshfpFingerprint', 'newSshfpFingerprint', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'TLSA': {'tlsaCertificateUsage', 'newTlsaCertificateUsage', 'tlsaSelector', 'newTlsaSelector', 'tlsaMatchingType', 'newTlsaMatchingType', 'tlsaCertificateAssociationData', 'newTlsaCertificateAssociationData', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'SVCB': {'svcPriority', 'newSvcPriority', 'svcTargetName', 'newSvcTargetName', 'svcParams', 'newSvcParams', 'autoIpv4Hint', 'autoIpv6Hint', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'HTTPS': {'svcPriority', 'newSvcPriority', 'svcTargetName', 'newSvcTargetName', 'svcParams', 'newSvcParams', 'autoIpv4Hint', 'autoIpv6Hint', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'URI': {'uriPriority', 'newUriPriority', 'uriWeight', 'newUriWeight', 'uri', 'newUri', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'CAA': {'flags', 'newFlags', 'tag', 'newTag', 'value', 'newValue', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'ANAME': {'aname', 'newAName', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'FWD': {'ttl','protocol', 'newProtocol', 'forwarder', 'newForwarder', 'forwarderPriority', 'dnssecValidation', 'proxyType', 'proxyAddress', 'proxyPort', 'proxyUsername', 'proxyPassword', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'APP': {'appName', 'classPath', 'recordData', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'},
            'UNKNOWN': {'rdata', 'newRData', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'}
        }
        
        # For unknown/unsupported record types, allow rdata parameters
        if record_type not in allowed_params:
            allowed_params[record_type] = {'rdata', 'newRData', 'ttl', 'disable', 'overwrite', 'comments', 'expiryTtl'}
        
        # Validate allowed params
        if record_type in allowed_params:
            for param in params:
                # Skip core connection/control params and the canonical name param plus its aliases
                if param in ['api_url', 'api_port', 'api_token', 'name', 'domain', 'zone', 'type', 'validate_certs', 'newDomain']:
                    continue
                if params[param] is not None and param not in allowed_params[record_type]:
                    self.fail_json(msg=f"Parameter '{param}' is not supported for record type '{record_type}'.")

    def _validate_record_type_parameters(self, record_type):
        """Validate that required parameters are provided for the specific record type."""
        params = self.params
        
        # Define required parameters for each record type
        required_params = {
            'A': ['ipAddress'],
            'AAAA': ['ipAddress'],
            'NS': ['nameServer'],
            'CNAME': ['cname'],
            'SOA': ['primaryNameServer', 'responsiblePerson', 'serial', 'refresh', 'retry', 'expire', 'minimum'],
            'PTR': ['ptrName'],
            'MX': ['preference', 'exchange'],
            'TXT': ['text'],
            'RP': ['mailbox', 'txtDomain'],
            'SRV': ['priority', 'weight', 'srv_port', 'target'],
            'NAPTR': ['naptrOrder', 'naptrPreference', 'naptrFlags', 'naptrServices', 'naptrRegexp', 'naptrReplacement'],
            'DNAME': ['dname'],
            'DS': ['keyTag', 'algorithm', 'digestType', 'digest'],
            'SSHFP': ['sshfpAlgorithm', 'sshfpFingerprintType', 'sshfpFingerprint'],
            'TLSA': ['tlsaCertificateUsage', 'tlsaSelector', 'tlsaMatchingType', 'tlsaCertificateAssociationData'],
            'SVCB': ['svcPriority', 'svcTargetName', 'svcParams'],
            'HTTPS': ['svcPriority', 'svcTargetName', 'svcParams'],
            'URI': ['uriPriority', 'uriWeight', 'uri'],
            'CAA': ['flags', 'tag', 'value'],
            'ANAME': ['aname'],
            'FWD': ['forwarder'],
            'APP': ['appName', 'classPath'],
            'UNKNOWN': ['rdata']
        }

        if record_type in required_params:
            for param in required_params[record_type]:
                # For CAA records, allow "new" parameters to satisfy requirements
                if record_type == 'CAA' and param in ['flags', 'tag', 'value']:
                    new_param_map = {'flags': 'newFlags', 'tag': 'newTag', 'value': 'newValue'}
                    if params.get(param) is None and params.get(new_param_map[param]) is None:
                        self.fail_json(msg=f"Parameter '{param}' or '{new_param_map[param]}' is required for updating {record_type} record")
                # For UNKNOWN records, allow either rdata or newRData to satisfy requirements
                elif record_type == 'UNKNOWN' and param == 'rdata':
                    if params.get('rdata') is None and params.get('newRData') is None:
                        self.fail_json(msg=f"Parameter 'rdata' or 'newRData' is required for updating {record_type} record")
                else:
                    if params.get(param) is None:
                        self.fail_json(msg=f"Parameter '{param}' is required for updating {record_type} record")

    def _get_current_record(self, domain, zone, record_type):
        """Get the current record from the DNS server."""
        query = {'domain': domain, 'type': record_type}
        if zone:
            query['zone'] = zone

        data = self.request('/api/zones/records/get', params=query)
        if data.get('status') != 'ok':
            return None

        # Find the specific record matching our criteria
        records = data.get('response', {}).get('records', [])
        matching_records = []
        
        for record in records:
            # Handle case sensitivity for UNKNOWN records (API returns "Unknown", we use "UNKNOWN")
            api_record_type = record.get('type')
            if record_type == 'UNKNOWN' and api_record_type == 'Unknown':
                api_record_type = 'UNKNOWN'
            
            if api_record_type == record_type and record.get('name') == domain:
                matching_records.append(record)
        
        if not matching_records:
            return None
            
        # For records where we might have multiple records of the same type for the same domain,
        # we need to find the specific one that matches our parameters
        if len(matching_records) > 1:
            params = self.params
            
            # Handle CAA records
            if record_type == 'CAA':
                for record in matching_records:
                    rdata = record.get('rData', {})
                    
                    # First try to match based on current parameters if provided
                    if (params.get('flags') is not None and rdata.get('flags') == params.get('flags') and
                        params.get('tag') and rdata.get('tag') == params.get('tag') and
                        params.get('value') and rdata.get('value') == params.get('value')):
                        return record
                    
                    # If current params not provided, try to match with "new" parameters (idempotency case)
                    if (params.get('flags') is None and params.get('tag') is None and params.get('value') is None):
                        if (params.get('newFlags') is not None and rdata.get('flags') == params.get('newFlags') and
                            params.get('newTag') and rdata.get('tag') == params.get('newTag') and
                            params.get('newValue') and rdata.get('value') == params.get('newValue')):
                            return record
            
            # Handle MX records
            elif record_type == 'MX':
                for record in matching_records:
                    rdata = record.get('rData', {})
                    
                    # First try to match based on current parameters if provided
                    if (params.get('preference') is not None and rdata.get('preference') == params.get('preference') and
                        params.get('exchange') and rdata.get('exchange') == params.get('exchange')):
                        return record
                    
                    # If current params not provided, try to match with "new" parameters (idempotency case)
                    if (params.get('preference') is None and params.get('exchange') is None):
                        if (params.get('newPreference') is not None and rdata.get('preference') == params.get('newPreference') and
                            params.get('newExchange') and rdata.get('exchange') == params.get('newExchange')):
                            return record
            
            # Handle FWD records
            elif record_type == 'FWD':
                for record in matching_records:
                    rdata = record.get('rData', {})
                    
                    # First try to match based on current parameters if provided
                    if (params.get('protocol') and rdata.get('protocol') == params.get('protocol') and
                        params.get('forwarder') and rdata.get('forwarder') == params.get('forwarder')):
                        return record
                    
                    # If current params not provided, try to match with "new" parameters (idempotency case)
                    if (params.get('protocol') is None and params.get('forwarder') is None):
                        if (params.get('newProtocol') and rdata.get('protocol') == params.get('newProtocol') and
                            params.get('newForwarder') and rdata.get('forwarder') == params.get('newForwarder')):
                            return record
            
            # Handle UNKNOWN records
            elif record_type == 'UNKNOWN':
                for record in matching_records:
                    rdata = record.get('rData', {})
                    
                    # First try to match based on current rdata parameter if provided
                    if params.get('rdata'):
                        # Normalize hex strings for comparison - remove colons and convert to uppercase
                        current_value = rdata.get('value', '').replace(':', '').upper()
                        param_value = params['rdata'].replace(':', '').upper()
                        if current_value == param_value:
                            return record
                    
                    # If rdata param not provided, try to match with newRData parameter (idempotency case)
                    if params.get('rdata') is None and params.get('newRData'):
                        current_value = rdata.get('value', '').replace(':', '').upper()
                        new_value = params['newRData'].replace(':', '').upper()
                        if current_value == new_value:
                            return record
            
            # If no specific match found, return the first matching record
            return matching_records[0]
        
        return matching_records[0] if matching_records else None

    def _normalize_ipv6(self, ip_address):
        """Normalize IPv6 address for comparison."""
        try:
            import ipaddress
            return str(ipaddress.IPv6Address(ip_address))
        except Exception:
            return ip_address

    def _parse_svc_params(self, params_string):
        """Parse svcParams string into a dictionary for comparison."""
        if not params_string:
            return {}
        
        result = {}
        parts = params_string.split('|')
        i = 0
        while i < len(parts):
            if i + 1 < len(parts):
                key = parts[i]
                value = parts[i + 1]
                result[key] = value
                i += 2
            else:
                i += 1
        return result

    def _is_update_needed(self, current_record, record_type):
        """Compare current record with desired values to determine if update is needed."""
        params = self.params
        
        # Check common properties first
        if params.get('newDomain') and params['newDomain'] != current_record.get('name'):
            return True
        if params.get('ttl') and params['ttl'] != current_record.get('ttl'):
            return True
        if params.get('disable', False) != current_record.get('disabled', False):
            return True
        if params.get('comments') and params['comments'] != current_record.get('comments', ''):
            return True

        # Check record type specific properties
        rdata = current_record.get('rData', {})
        
        if record_type in ['A', 'AAAA']:
            if params.get('newIpAddress'):
                current_ip = rdata.get('ipAddress')
                new_ip = params['newIpAddress']
                # Normalize IPv6 addresses for comparison
                if record_type == 'AAAA':
                    current_ip = self._normalize_ipv6(current_ip) if current_ip else current_ip
                    new_ip = self._normalize_ipv6(new_ip)
                if new_ip != current_ip:
                    return True
        
        elif record_type == 'NS':
            if params.get('newNameServer') and params['newNameServer'] != rdata.get('nameServer'):
                return True
        
        elif record_type == 'CNAME':
            if params.get('cname') and params['cname'] != rdata.get('cname'):
                return True
        
        elif record_type == 'SOA':
            soa_fields = ['primaryNameServer', 'responsiblePerson', 'serial', 'refresh', 'retry', 'expire', 'minimum']
            for field in soa_fields:
                if params.get(field) is not None and params[field] != rdata.get(field):
                    return True
        
        elif record_type == 'PTR':
            if params.get('newPtrName') and params['newPtrName'] != rdata.get('ptrName'):
                return True
        
        elif record_type == 'MX':
            if params.get('newPreference') is not None and params['newPreference'] != rdata.get('preference'):
                return True
            if params.get('newExchange') and params['newExchange'] != rdata.get('exchange'):
                return True
        
        elif record_type == 'TXT':
            if params.get('newText') and params['newText'] != rdata.get('text'):
                return True
        
        elif record_type == 'SRV':
            srv_fields = [('newPriority', 'priority'), ('newWeight', 'weight'), ('newSrvPort', 'port'), ('newTarget', 'target')]
            for new_field, current_field in srv_fields:
                if params.get(new_field) is not None and params[new_field] != rdata.get(current_field):
                    return True
        
        elif record_type == 'CAA':
            # Check new parameters if provided, otherwise check current parameters
            flags_to_check = params.get('newFlags') if params.get('newFlags') is not None else params.get('flags')
            if flags_to_check is not None and flags_to_check != rdata.get('flags'):
                return True
            
            tag_to_check = params.get('newTag') or params.get('tag')
            if tag_to_check and tag_to_check != rdata.get('tag'):
                return True
            
            value_to_check = params.get('newValue') or params.get('value')
            if value_to_check and value_to_check != rdata.get('value'):
                return True
        
        elif record_type == 'ANAME':
            if params.get('newAName') and params['newAName'] != rdata.get('aname'):
                return True
        
        elif record_type == 'FWD':
            # For FWD records, compare new values if provided
            if params.get('newProtocol') and params['newProtocol'] != rdata.get('protocol'):
                return True
            if params.get('newForwarder') and params['newForwarder'] != rdata.get('forwarder'):
                return True
        
        elif record_type == 'RP':
            if params.get('newMailbox') and params['newMailbox'] != rdata.get('mailbox'):
                return True
            if params.get('newTxtDomain') and params['newTxtDomain'] != rdata.get('txtDomain'):
                return True
        
        elif record_type == 'NAPTR':
            naptr_fields = [
                ('naptrNewOrder', 'order'), ('naptrNewPreference', 'preference'),
                ('naptrNewFlags', 'flags'), ('naptrNewServices', 'services'),
                ('naptrNewRegexp', 'regexp'), ('naptrNewReplacement', 'replacement')
            ]
            for new_field, current_field in naptr_fields:
                if params.get(new_field) is not None and params[new_field] != rdata.get(current_field):
                    return True
        
        elif record_type == 'DNAME':
            if params.get('dname') and params['dname'] != rdata.get('dname'):
                return True
        
        elif record_type == 'DS':
            ds_fields = [
                ('newKeyTag', 'keyTag'), ('newAlgorithm', 'algorithm'),
                ('newDigestType', 'digestType'), ('newDigest', 'digest')
            ]
            for new_field, current_field in ds_fields:
                if params.get(new_field) is not None and params[new_field] != rdata.get(current_field):
                    return True
        
        elif record_type == 'SSHFP':
            if params.get('newSshfpAlgorithm') and params['newSshfpAlgorithm'] != rdata.get('algorithm'):
                return True
            if params.get('newSshfpFingerprintType') and params['newSshfpFingerprintType'] != rdata.get('fingerprintType'):
                return True
            if params.get('newSshfpFingerprint'):
                # Case-insensitive comparison for fingerprint
                current_fp = rdata.get('fingerprint', '').upper()
                new_fp = params['newSshfpFingerprint'].upper()
                if new_fp != current_fp:
                    return True
        
        elif record_type == 'TLSA':
            if params.get('newTlsaCertificateUsage') and params['newTlsaCertificateUsage'] != rdata.get('certificateUsage'):
                return True
            if params.get('newTlsaSelector') and params['newTlsaSelector'] != rdata.get('selector'):
                return True
            if params.get('newTlsaMatchingType') and params['newTlsaMatchingType'] != rdata.get('matchingType'):
                return True
            if params.get('newTlsaCertificateAssociationData'):
                # Case-insensitive comparison for certificate data
                current_cert = rdata.get('certificateAssociationData', '').upper()
                new_cert = params['newTlsaCertificateAssociationData'].upper()
                if new_cert != current_cert:
                    return True
        
        elif record_type in ['SVCB', 'HTTPS']:
            if params.get('newSvcPriority') is not None and params['newSvcPriority'] != rdata.get('svcPriority'):
                return True
            if params.get('newSvcTargetName') is not None:
                # Normalize target names: "." and "" both represent the current domain
                current_target = rdata.get('svcTargetName', '')
                new_target = params['newSvcTargetName']
                # Convert "." to "" for comparison since API returns ""
                if new_target == '.':
                    new_target = ''
                if new_target != current_target:
                    return True
            # svcParams comparison - parse string and compare with object
            if params.get('newSvcParams'):
                desired_params = self._parse_svc_params(params['newSvcParams'])
                current_params = rdata.get('svcParams', {})
                if desired_params != current_params:
                    return True
        
        elif record_type == 'URI':
            uri_fields = [
                ('newUriPriority', 'priority'), ('newUriWeight', 'weight'),
                ('newUri', 'uri')
            ]
            for new_field, current_field in uri_fields:
                if params.get(new_field) is not None and params[new_field] != rdata.get(current_field):
                    return True

        elif record_type == 'APP':
            # APP records don't use 'new' prefix - compare parameters directly
            if params.get('appName') and params['appName'] != rdata.get('appName'):
                return True
            if params.get('classPath') and params['classPath'] != rdata.get('classPath'):
                return True
            if params.get('recordData') and params['recordData'] != rdata.get('data'):
                return True

        elif record_type == 'UNKNOWN':
            # UNKNOWN records use newRData parameter
            if params.get('newRData'):
                # Normalize hex strings for comparison - remove colons and convert to uppercase
                current_value = rdata.get('value', '').replace(':', '').upper()
                new_value = params['newRData'].replace(':', '').upper()
                if new_value != current_value:
                    return True

        # No changes needed
        return False

    def _build_update_query(self, domain, zone, record_type):
        """Build the API query parameters for the update request."""
        params = self.params
        query = {
            'domain': domain,
            'type': record_type
        }
        
        if zone:
            query['zone'] = zone

        # Define which parameters use 'new<Parameter>' prefix according to API documentation
        # Only these specific parameters require the 'new' prefix
        new_prefix_params = {
            'newDomain', 'newIpAddress', 'newNameServer', 'newPtrName', 'newPreference', 'newExchange',
            'newText', 'newSplitText', 'newMailbox', 'newTxtDomain', 'newPriority', 'newWeight', 
            'newPort', 'newTarget', 'newKeyTag', 'newAlgorithm', 'newDigestType', 'newDigest',
            'newSshfpAlgorithm', 'newSshfpFingerprintType', 'newSshfpFingerprint',
            'newTlsaCertificateUsage', 'newTlsaSelector', 'newTlsaMatchingType', 'newTlsaCertificateAssociationData',
            'newSvcPriority', 'newSvcTargetName', 'newSvcParams', 'newUriPriority', 'newUriWeight', 'newUri',
            'newFlags', 'newTag', 'newValue', 'newAName', 'newProtocol', 'newForwarder', 'newRData'
        }

        # Add all parameters that have values, handling data type conversions
        for key in self.argument_spec:
            val = params.get(key)
            if val is not None and key not in ['name', 'zone', 'type']:
                # Skip connection/module configuration parameters
                if key in ['api_url', 'port', 'api_token', 'validate_certs']:
                    continue
                
                # Convert boolean values to lowercase strings for API compatibility
                if isinstance(val, bool):
                    val = str(val).lower()
                
                # Handle special parameter name mappings
                if key == 'srv_port':
                    query['port'] = val
                elif key == 'newSrvPort':
                    query['newPort'] = val
                else:
                    # For parameters that use the 'new' prefix, pass them directly
                    # For all other parameters, pass them as-is (no 'new' prefix needed)
                    query[key] = val

        return query

def main():
    module = UpdateRecordModule()
    module()

if __name__ == '__main__':
    main()