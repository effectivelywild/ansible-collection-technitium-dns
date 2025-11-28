#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_set_server_settings
short_description: Update DNS server settings
version_added: "1.1.0"
description:
    - Update Technitium DNS server settings.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_server_settings
    description: Get DNS server settings
options:
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
    validate_certs:
        description:
            - Whether to validate SSL certificates when making API requests.
        required: false
        type: bool
        default: true
    dnsServerDomain:
        description:
            - Primary domain name used by this DNS Server to identify itself.
        required: false
        type: str
    dnsServerLocalEndPoints:
        description:
            - List of IP:port endpoints to listen for DNS requests.
        required: false
        type: list
        elements: str
    dnsServerIPv4SourceAddresses:
        description:
            - IPv4 source addresses to use for outbound DNS requests.
        required: false
        type: list
        elements: str
    dnsServerIPv6SourceAddresses:
        description:
            - IPv6 source addresses to use for outbound DNS requests.
        required: false
        type: list
        elements: str
    defaultRecordTtl:
        description:
            - Default TTL value for records when not specified.
        required: false
        type: int
    defaultResponsiblePerson:
        description:
            - Default SOA Responsible Person email for new primary zones.
        required: false
        type: str
    useSoaSerialDateScheme:
        description:
            - Use SOA serial date scheme as default for new zones.
        required: false
        type: bool
    minSoaRefresh:
        description:
            - Minimum refresh interval for secondary, stub, and catalog zones.
        required: false
        type: int
    minSoaRetry:
        description:
            - Minimum retry interval for secondary, stub, and catalog zones.
        required: false
        type: int
    zoneTransferAllowedNetworks:
        description:
            - Networks allowed for zone transfers across all zones.
        required: false
        type: list
        elements: str
    notifyAllowedNetworks:
        description:
            - Networks allowed to notify all secondary zones.
        required: false
        type: list
        elements: str
    dnsAppsEnableAutomaticUpdate:
        description:
            - Enable automatic DNS App updates every 24 hours.
        required: false
        type: bool
    preferIPv6:
        description:
            - Prefer IPv6 for querying when possible.
        required: false
        type: bool
    enableUdpSocketPool:
        description:
            - Enable UDP socket pool for outbound DNS-over-UDP requests.
        required: false
        type: bool
    socketPoolExcludedPorts:
        description:
            - Ports to exclude from UDP socket pool.
        required: false
        type: list
        elements: int
    udpPayloadSize:
        description:
            - Maximum EDNS UDP payload size (512-4096).
        required: false
        type: int
    dnssecValidation:
        description:
            - Enable DNSSEC validation for responses.
        required: false
        type: bool
    eDnsClientSubnet:
        description:
            - Enable EDNS Client Subnet.
        required: false
        type: bool
    eDnsClientSubnetIPv4PrefixLength:
        description:
            - EDNS Client Subnet IPv4 prefix length.
        required: false
        type: int
    eDnsClientSubnetIPv6PrefixLength:
        description:
            - EDNS Client Subnet IPv6 prefix length.
        required: false
        type: int
    eDnsClientSubnetIpv4Override:
        description:
            - IPv4 network to use as ECS override.
        required: false
        type: str
    eDnsClientSubnetIpv6Override:
        description:
            - IPv6 network to use as ECS override.
        required: false
        type: str
    qpmPrefixLimitsIPv4:
        description:
            - List of IPv4 prefix limits; set to false to clear. Each item must include prefix, udpLimit, tcpLimit.
        required: false
        type: list
        elements: dict
        suboptions:
            prefix:
                description: IPv4 prefix length to limit (e.g. 32, 24)
                type: int
                required: true
            udpLimit:
                description: Allowed UDP queries per minute for the prefix
                type: int
                required: true
            tcpLimit:
                description: Allowed TCP queries per minute for the prefix
                type: int
                required: true
    qpmPrefixLimitsIPv6:
        description:
            - List of IPv6 prefix limits; set to false to clear. Each item must include prefix, udpLimit, tcpLimit.
        required: false
        type: list
        elements: dict
        suboptions:
            prefix:
                description: IPv6 prefix length to limit (e.g. 128, 64)
                type: int
                required: true
            udpLimit:
                description: Allowed UDP queries per minute for the prefix
                type: int
                required: true
            tcpLimit:
                description: Allowed TCP queries per minute for the prefix
                type: int
                required: true
    qpmLimitSampleMinutes:
        description:
            - Client query stats sample size in minutes.
        required: false
        type: int
    qpmLimitUdpTruncationPercentage:
        description:
            - Percentage of UDP requests truncated when QPM limit exceeds (0-100).
        required: false
        type: int
    qpmLimitBypassList:
        description:
            - Networks allowed to bypass QPM limit.
        required: false
        type: list
        elements: str
    clientTimeout:
        description:
            - Time in ms before responding ServerFailure when no answer (1000-10000).
        required: false
        type: int
    tcpSendTimeout:
        description:
            - Max time in ms to send TCP response (1000-90000).
        required: false
        type: int
    tcpReceiveTimeout:
        description:
            - Max time in ms to receive TCP data (1000-90000).
        required: false
        type: int
    quicIdleTimeout:
        description:
            - Idle timeout in ms for QUIC connections (1000-90000).
        required: false
        type: int
    quicMaxInboundStreams:
        description:
            - Max inbound bidirectional streams per QUIC connection (1-1000).
        required: false
        type: int
    listenBacklog:
        description:
            - Max pending inbound connections.
        required: false
        type: int
    maxConcurrentResolutionsPerCore:
        description:
            - Max concurrent outbound resolutions per CPU core.
        required: false
        type: int
    webServiceLocalAddresses:
        description:
            - Local addresses for web service.
        required: false
        type: list
        elements: str
    webServiceHttpPort:
        description:
            - HTTP port for web console/API.
        required: false
        type: int
    webServiceEnableTls:
        description:
            - Enable HTTPS service.
        required: false
        type: bool
    webServiceEnableHttp3:
        description:
            - Enable HTTP/3 for web service.
        required: false
        type: bool
    webServiceHttpToTlsRedirect:
        description:
            - Redirect HTTP to HTTPS.
        required: false
        type: bool
    webServiceTlsPort:
        description:
            - HTTPS port for web console.
        required: false
        type: int
    webServiceUseSelfSignedTlsCertificate:
        description:
            - Use self-signed certificate when TLS cert path is not set.
        required: false
        type: bool
    webServiceTlsCertificatePath:
        description:
            - Path to PKCS #12 certificate for HTTPS.
        required: false
        type: str
    webServiceTlsCertificatePassword:
        description:
            - Password for TLS certificate file.
        required: false
        type: str
    webServiceRealIpHeader:
        description:
            - Header to read client IP when behind reverse proxy.
        required: false
        type: str
    enableDnsOverUdpProxy:
        description:
            - Accept DNS-over-UDP-PROXY requests.
        required: false
        type: bool
    enableDnsOverTcpProxy:
        description:
            - Accept DNS-over-TCP-PROXY requests.
        required: false
        type: bool
    enableDnsOverHttp:
        description:
            - Accept DNS-over-HTTP requests.
        required: false
        type: bool
    enableDnsOverTls:
        description:
            - Accept DNS-over-TLS requests.
        required: false
        type: bool
    enableDnsOverHttps:
        description:
            - Accept DNS-over-HTTPS requests.
        required: false
        type: bool
    enableDnsOverHttp3:
        description:
            - Accept DNS-over-HTTP/3 requests.
        required: false
        type: bool
    enableDnsOverQuic:
        description:
            - Accept DNS-over-QUIC requests.
        required: false
        type: bool
    dnsOverUdpProxyPort:
        description:
            - UDP port for DNS-over-UDP-PROXY.
        required: false
        type: int
    dnsOverTcpProxyPort:
        description:
            - TCP port for DNS-over-TCP-PROXY.
        required: false
        type: int
    dnsOverHttpPort:
        description:
            - TCP port for DNS-over-HTTP.
        required: false
        type: int
    dnsOverTlsPort:
        description:
            - TCP port for DNS-over-TLS.
        required: false
        type: int
    dnsOverHttpsPort:
        description:
            - TCP port for DNS-over-HTTPS.
        required: false
        type: int
    dnsOverQuicPort:
        description:
            - UDP port for DNS-over-QUIC.
        required: false
        type: int
    reverseProxyNetworkACL:
        description:
            - ACL for reverse proxy sources.
        required: false
        type: list
        elements: str
    dnsTlsCertificatePath:
        description:
            - PKCS #12 certificate path for DNS-over-TLS/HTTPS.
        required: false
        type: str
    dnsTlsCertificatePassword:
        description:
            - Password for DNS TLS certificate.
        required: false
        type: str
    dnsOverHttpRealIpHeader:
        description:
            - Header to read client IP for DNS-over-HTTP when behind reverse proxy.
        required: false
        type: str
    tsigKeys:
        description:
            - List of TSIG keys; set to false to clear. Each item must include keyName, sharedSecret, algorithmName.
        required: false
        type: list
        elements: dict
        suboptions:
            keyName:
                description: TSIG key name
                type: str
                required: true
            sharedSecret:
                description: Base64-encoded shared secret
                type: str
                required: true
            algorithmName:
                description: TSIG algorithm name (e.g. hmac-sha256)
                type: str
                required: true
    recursion:
        description:
            - Recursion policy.
        required: false
        type: str
        choices: [Deny, Allow, AllowOnlyForPrivateNetworks, UseSpecifiedNetworkACL]
    recursionNetworkACL:
        description:
            - ACL for recursion when policy is UseSpecifiedNetworkACL. Set to false to clear.
        required: false
        type: list
        elements: str
    randomizeName:
        description:
            - Enable QNAME randomization.
        required: false
        type: bool
    qnameMinimization:
        description:
            - Enable QNAME minimization for recursive resolution.
        required: false
        type: bool
    resolverRetries:
        description:
            - Number of resolver retries.
        required: false
        type: int
    resolverTimeout:
        description:
            - Resolver timeout in ms.
        required: false
        type: int
    resolverConcurrency:
        description:
            - Number of concurrent resolver requests.
        required: false
        type: int
    resolverMaxStackCount:
        description:
            - Max resolver stack count.
        required: false
        type: int
    saveCache:
        description:
            - Save DNS cache on disk at shutdown.
        required: false
        type: bool
    serveStale:
        description:
            - Serve stale records when upstream unavailable.
        required: false
        type: bool
    serveStaleTtl:
        description:
            - TTL in seconds for stale records (max 604800).
        required: false
        type: int
    serveStaleAnswerTtl:
        description:
            - TTL in seconds for answers in stale response (0-300).
        required: false
        type: int
    serveStaleResetTtl:
        description:
            - TTL reset value in seconds when refresh fails (10-900).
        required: false
        type: int
    serveStaleMaxWaitTime:
        description:
            - Max wait time in ms before serving stale records (0-1800).
        required: false
        type: int
    cacheMaximumEntries:
        description:
            - Maximum cache entries.
        required: false
        type: int
    cacheMinimumRecordTtl:
        description:
            - Minimum TTL allowed in cache.
        required: false
        type: int
    cacheMaximumRecordTtl:
        description:
            - Maximum TTL allowed in cache.
        required: false
        type: int
    cacheNegativeRecordTtl:
        description:
            - Negative TTL value.
        required: false
        type: int
    cacheFailureRecordTtl:
        description:
            - Failure TTL value for caching ServerFailure responses.
        required: false
        type: int
    cachePrefetchEligibility:
        description:
            - Minimum initial TTL to be eligible for prefetching.
        required: false
        type: int
    cachePrefetchTrigger:
        description:
            - TTL trigger to start prefetch; 0 disables.
        required: false
        type: int
    cachePrefetchSampleIntervalInMinutes:
        description:
            - Interval to sample eligible domains for auto prefetch.
        required: false
        type: int
    cachePrefetchSampleEligibilityHitsPerHour:
        description:
            - Minimum hits per hour to be eligible for auto prefetch.
        required: false
        type: int
    enableBlocking:
        description:
            - Enable blocking via blocked zones and lists.
        required: false
        type: bool
    allowTxtBlockingReport:
        description:
            - Include TXT blocking report for TXT queries.
        required: false
        type: bool
    blockingBypassList:
        description:
            - Networks allowed to bypass blocking.
        required: false
        type: list
        elements: str
    blockingType:
        description:
            - Response type for blocked domains.
        required: false
        type: str
        choices: [AnyAddress, NxDomain, CustomAddress]
    blockingAnswerTtl:
        description:
            - TTL in seconds for blocking responses.
        required: false
        type: int
    customBlockingAddresses:
        description:
            - Custom addresses returned when blockingType is CustomAddress.
        required: false
        type: list
        elements: str
    blockListUrls:
        description:
            - Block list URLs; set to false to clear.
        required: false
        type: list
        elements: str
    blockListUpdateIntervalHours:
        description:
            - Interval in hours to update block lists.
        required: false
        type: int
    proxyType:
        description:
            - Proxy protocol for outbound DNS.
        required: false
        type: str
        choices: [None, Http, Socks5]
    proxyAddress:
        description:
            - Proxy server hostname or IP.
        required: false
        type: str
    proxyPort:
        description:
            - Proxy server port.
        required: false
        type: int
    proxyUsername:
        description:
            - Proxy username.
        required: false
        type: str
    proxyPassword:
        description:
            - Proxy password.
        required: false
        type: str
    proxyBypass:
        description:
            - Bypass list for proxy (IP, CIDR, or hostnames).
        required: false
        type: list
        elements: str
    forwarders:
        description:
            - Forwarders list; set to false to remove and use recursion.
        required: false
        type: list
        elements: str
    forwarderProtocol:
        description:
            - Forwarder transport protocol.
        required: false
        type: str
        choices: [Udp, Tcp, Tls, Https, Quic]
    concurrentForwarding:
        description:
            - Query multiple forwarders concurrently.
        required: false
        type: bool
    forwarderRetries:
        description:
            - Number of forwarder retries.
        required: false
        type: int
    forwarderTimeout:
        description:
            - Forwarder timeout in ms.
        required: false
        type: int
    forwarderConcurrency:
        description:
            - Number of concurrent requests per forwarder.
        required: false
        type: int
    loggingType:
        description:
            - How error/audit logs are written.
        required: false
        type: str
        choices: [None, File, Console, FileAndConsole]
    enableLogging:
        description:
            - Legacy flag for enabling logging (use loggingType).
        required: false
        type: bool
    ignoreResolverLogs:
        description:
            - Stop logging resolver errors.
        required: false
        type: bool
    logQueries:
        description:
            - Log every query and response.
        required: false
        type: bool
    useLocalTime:
        description:
            - Use local time for logging.
        required: false
        type: bool
    logFolder:
        description:
            - Folder path for log files.
        required: false
        type: str
    maxLogFileDays:
        description:
            - Max days to keep log files; 0 disables auto delete.
        required: false
        type: int
    enableInMemoryStats:
        description:
            - Store only last hour stats in memory (no disk stats).
        required: false
        type: bool
    maxStatFileDays:
        description:
            - Max days to keep dashboard stats; 0 disables auto delete.
        required: false
        type: int
'''

EXAMPLES = r'''
- name: Enable HTTPS for web service
  effectivelywild.technitium_dns.technitium_dns_set_server_settings:
    api_url: "http://localhost"
    api_token: "myapitoken"
    webServiceEnableTls: true
    webServiceTlsPort: 53443
    webServiceUseSelfSignedTlsCertificate: true

- name: Configure resolver behavior and logging
  effectivelywild.technitium_dns.technitium_dns_set_server_settings:
    api_url: "http://localhost"
    api_token: "myapitoken"
    resolverTimeout: 2000
    resolverRetries: 3
    loggingType: File
    logQueries: true

- name: Set forwarders with HTTPS transport
  effectivelywild.technitium_dns.technitium_dns_set_server_settings:
    api_url: "http://localhost"
    api_token: "myapitoken"
    forwarders:
      - "1.1.1.1"
      - "1.0.0.1"
    forwarderProtocol: Https
    forwarderTimeout: 1500
'''

RETURN = r'''
settings:
    description: Updated DNS server settings returned by the API
    type: dict
    returned: always
diff:
    description: Dictionary showing which settings changed
    type: dict
    returned: when changes are detected
    sample: {"resolverTimeout": {"current": 1500, "desired": 2000}}
changed:
    description: Whether the module made changes
    type: bool
    returned: always
failed:
    description: Whether the module failed
    type: bool
    returned: always
msg:
    description: Human readable message describing the result
    type: str
    returned: always
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class SetServerSettingsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        dnsServerDomain=dict(type='str', required=False),
        dnsServerLocalEndPoints=dict(type='list', elements='str', required=False),
        dnsServerIPv4SourceAddresses=dict(type='list', elements='str', required=False),
        dnsServerIPv6SourceAddresses=dict(type='list', elements='str', required=False),
        defaultRecordTtl=dict(type='int', required=False),
        defaultResponsiblePerson=dict(type='str', required=False),
        useSoaSerialDateScheme=dict(type='bool', required=False),
        minSoaRefresh=dict(type='int', required=False),
        minSoaRetry=dict(type='int', required=False),
        zoneTransferAllowedNetworks=dict(type='list', elements='str', required=False),
        notifyAllowedNetworks=dict(type='list', elements='str', required=False),
        dnsAppsEnableAutomaticUpdate=dict(type='bool', required=False),
        preferIPv6=dict(type='bool', required=False),
        enableUdpSocketPool=dict(type='bool', required=False),
        socketPoolExcludedPorts=dict(type='list', elements='int', required=False),
        udpPayloadSize=dict(type='int', required=False),
        dnssecValidation=dict(type='bool', required=False),
        eDnsClientSubnet=dict(type='bool', required=False),
        eDnsClientSubnetIPv4PrefixLength=dict(type='int', required=False),
        eDnsClientSubnetIPv6PrefixLength=dict(type='int', required=False),
        eDnsClientSubnetIpv4Override=dict(type='str', required=False),
        eDnsClientSubnetIpv6Override=dict(type='str', required=False),
        qpmPrefixLimitsIPv4=dict(type='raw', required=False),
        qpmPrefixLimitsIPv6=dict(type='raw', required=False),
        qpmLimitSampleMinutes=dict(type='int', required=False),
        qpmLimitUdpTruncationPercentage=dict(type='int', required=False),
        qpmLimitBypassList=dict(type='list', elements='str', required=False, no_log=True),
        clientTimeout=dict(type='int', required=False),
        tcpSendTimeout=dict(type='int', required=False),
        tcpReceiveTimeout=dict(type='int', required=False),
        quicIdleTimeout=dict(type='int', required=False),
        quicMaxInboundStreams=dict(type='int', required=False),
        listenBacklog=dict(type='int', required=False),
        maxConcurrentResolutionsPerCore=dict(type='int', required=False),
        webServiceLocalAddresses=dict(type='list', elements='str', required=False),
        webServiceHttpPort=dict(type='int', required=False),
        webServiceEnableTls=dict(type='bool', required=False),
        webServiceEnableHttp3=dict(type='bool', required=False),
        webServiceHttpToTlsRedirect=dict(type='bool', required=False),
        webServiceTlsPort=dict(type='int', required=False),
        webServiceUseSelfSignedTlsCertificate=dict(type='bool', required=False),
        webServiceTlsCertificatePath=dict(type='str', required=False),
        webServiceTlsCertificatePassword=dict(type='str', required=False, no_log=True),
        webServiceRealIpHeader=dict(type='str', required=False),
        enableDnsOverUdpProxy=dict(type='bool', required=False),
        enableDnsOverTcpProxy=dict(type='bool', required=False),
        enableDnsOverHttp=dict(type='bool', required=False),
        enableDnsOverTls=dict(type='bool', required=False),
        enableDnsOverHttps=dict(type='bool', required=False),
        enableDnsOverHttp3=dict(type='bool', required=False),
        enableDnsOverQuic=dict(type='bool', required=False),
        dnsOverUdpProxyPort=dict(type='int', required=False),
        dnsOverTcpProxyPort=dict(type='int', required=False),
        dnsOverHttpPort=dict(type='int', required=False),
        dnsOverTlsPort=dict(type='int', required=False),
        dnsOverHttpsPort=dict(type='int', required=False),
        dnsOverQuicPort=dict(type='int', required=False),
        reverseProxyNetworkACL=dict(type='list', elements='str', required=False),
        dnsTlsCertificatePath=dict(type='str', required=False),
        dnsTlsCertificatePassword=dict(type='str', required=False, no_log=True),
        dnsOverHttpRealIpHeader=dict(type='str', required=False),
        tsigKeys=dict(type='raw', required=False, no_log=True),
        recursion=dict(type='str', required=False, choices=['Deny', 'Allow', 'AllowOnlyForPrivateNetworks', 'UseSpecifiedNetworkACL']),
        recursionNetworkACL=dict(type='raw', required=False),
        randomizeName=dict(type='bool', required=False),
        qnameMinimization=dict(type='bool', required=False),
        resolverRetries=dict(type='int', required=False),
        resolverTimeout=dict(type='int', required=False),
        resolverConcurrency=dict(type='int', required=False),
        resolverMaxStackCount=dict(type='int', required=False),
        saveCache=dict(type='bool', required=False),
        serveStale=dict(type='bool', required=False),
        serveStaleTtl=dict(type='int', required=False),
        serveStaleAnswerTtl=dict(type='int', required=False),
        serveStaleResetTtl=dict(type='int', required=False),
        serveStaleMaxWaitTime=dict(type='int', required=False),
        cacheMaximumEntries=dict(type='int', required=False),
        cacheMinimumRecordTtl=dict(type='int', required=False),
        cacheMaximumRecordTtl=dict(type='int', required=False),
        cacheNegativeRecordTtl=dict(type='int', required=False),
        cacheFailureRecordTtl=dict(type='int', required=False),
        cachePrefetchEligibility=dict(type='int', required=False),
        cachePrefetchTrigger=dict(type='int', required=False),
        cachePrefetchSampleIntervalInMinutes=dict(type='int', required=False),
        cachePrefetchSampleEligibilityHitsPerHour=dict(type='int', required=False),
        enableBlocking=dict(type='bool', required=False),
        allowTxtBlockingReport=dict(type='bool', required=False),
        blockingBypassList=dict(type='list', elements='str', required=False, no_log=True),
        blockingType=dict(type='str', required=False, choices=['AnyAddress', 'NxDomain', 'CustomAddress']),
        blockingAnswerTtl=dict(type='int', required=False),
        customBlockingAddresses=dict(type='list', elements='str', required=False),
        blockListUrls=dict(type='list', elements='str', required=False),
        blockListUpdateIntervalHours=dict(type='int', required=False),
        proxyType=dict(type='str', required=False, choices=['None', 'Http', 'Socks5']),
        proxyAddress=dict(type='str', required=False),
        proxyPort=dict(type='int', required=False),
        proxyUsername=dict(type='str', required=False),
        proxyPassword=dict(type='str', required=False, no_log=True),
        proxyBypass=dict(type='list', elements='str', required=False, no_log=True),
        forwarders=dict(type='raw', required=False),
        forwarderProtocol=dict(type='str', required=False, choices=['Udp', 'Tcp', 'Tls', 'Https', 'Quic']),
        concurrentForwarding=dict(type='bool', required=False),
        forwarderRetries=dict(type='int', required=False),
        forwarderTimeout=dict(type='int', required=False),
        forwarderConcurrency=dict(type='int', required=False),
        loggingType=dict(type='str', required=False, choices=['None', 'File', 'Console', 'FileAndConsole']),
        enableLogging=dict(type='bool', required=False),
        ignoreResolverLogs=dict(type='bool', required=False),
        logQueries=dict(type='bool', required=False),
        useLocalTime=dict(type='bool', required=False),
        logFolder=dict(type='str', required=False),
        maxLogFileDays=dict(type='int', required=False),
        enableInMemoryStats=dict(type='bool', required=False),
        maxStatFileDays=dict(type='int', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    settings_keys = [
        'dnsServerDomain', 'dnsServerLocalEndPoints', 'dnsServerIPv4SourceAddresses', 'dnsServerIPv6SourceAddresses',
        'defaultRecordTtl', 'defaultResponsiblePerson', 'useSoaSerialDateScheme', 'minSoaRefresh', 'minSoaRetry',
        'zoneTransferAllowedNetworks', 'notifyAllowedNetworks', 'dnsAppsEnableAutomaticUpdate', 'preferIPv6',
        'enableUdpSocketPool', 'socketPoolExcludedPorts', 'udpPayloadSize', 'dnssecValidation', 'eDnsClientSubnet',
        'eDnsClientSubnetIPv4PrefixLength', 'eDnsClientSubnetIPv6PrefixLength', 'eDnsClientSubnetIpv4Override',
        'eDnsClientSubnetIpv6Override', 'qpmPrefixLimitsIPv4', 'qpmPrefixLimitsIPv6', 'qpmLimitSampleMinutes',
        'qpmLimitUdpTruncationPercentage', 'qpmLimitBypassList', 'clientTimeout', 'tcpSendTimeout', 'tcpReceiveTimeout',
        'quicIdleTimeout', 'quicMaxInboundStreams', 'listenBacklog', 'maxConcurrentResolutionsPerCore',
        'webServiceLocalAddresses', 'webServiceHttpPort', 'webServiceEnableTls', 'webServiceEnableHttp3',
        'webServiceHttpToTlsRedirect', 'webServiceTlsPort', 'webServiceUseSelfSignedTlsCertificate',
        'webServiceTlsCertificatePath', 'webServiceTlsCertificatePassword', 'webServiceRealIpHeader',
        'enableDnsOverUdpProxy', 'enableDnsOverTcpProxy', 'enableDnsOverHttp', 'enableDnsOverTls',
        'enableDnsOverHttps', 'enableDnsOverHttp3', 'enableDnsOverQuic', 'dnsOverUdpProxyPort', 'dnsOverTcpProxyPort',
        'dnsOverHttpPort', 'dnsOverTlsPort', 'dnsOverHttpsPort', 'dnsOverQuicPort', 'reverseProxyNetworkACL',
        'dnsTlsCertificatePath', 'dnsTlsCertificatePassword', 'dnsOverHttpRealIpHeader', 'tsigKeys', 'recursion',
        'recursionNetworkACL', 'randomizeName', 'qnameMinimization', 'resolverRetries', 'resolverTimeout',
        'resolverConcurrency', 'resolverMaxStackCount', 'saveCache', 'serveStale', 'serveStaleTtl', 'serveStaleAnswerTtl',
        'serveStaleResetTtl', 'serveStaleMaxWaitTime', 'cacheMaximumEntries', 'cacheMinimumRecordTtl',
        'cacheMaximumRecordTtl', 'cacheNegativeRecordTtl', 'cacheFailureRecordTtl', 'cachePrefetchEligibility',
        'cachePrefetchTrigger', 'cachePrefetchSampleIntervalInMinutes', 'cachePrefetchSampleEligibilityHitsPerHour',
        'enableBlocking', 'allowTxtBlockingReport', 'blockingBypassList', 'blockingType', 'blockingAnswerTtl',
        'customBlockingAddresses', 'blockListUrls', 'blockListUpdateIntervalHours', 'proxyType', 'proxyAddress',
        'proxyPort', 'proxyUsername', 'proxyPassword', 'proxyBypass', 'forwarders', 'forwarderProtocol',
        'concurrentForwarding', 'forwarderRetries', 'forwarderTimeout', 'forwarderConcurrency', 'loggingType',
        'enableLogging', 'ignoreResolverLogs', 'logQueries', 'useLocalTime', 'logFolder', 'maxLogFileDays',
        'enableInMemoryStats', 'maxStatFileDays'
    ]

    simple_list_fields = {
        'dnsServerLocalEndPoints', 'dnsServerIPv4SourceAddresses', 'dnsServerIPv6SourceAddresses',
        'zoneTransferAllowedNetworks', 'notifyAllowedNetworks', 'qpmLimitBypassList', 'webServiceLocalAddresses',
        'reverseProxyNetworkACL', 'recursionNetworkACL', 'blockingBypassList', 'customBlockingAddresses',
        'blockListUrls', 'proxyBypass', 'forwarders'
    }

    int_list_fields = {'socketPoolExcludedPorts'}
    false_clear_simple_list_fields = {'blockListUrls', 'recursionNetworkACL', 'forwarders'}
    false_clear_limit_fields = {'qpmPrefixLimitsIPv4', 'qpmPrefixLimitsIPv6'}
    false_clear_key_fields = {'tsigKeys'}

    @staticmethod
    def _is_false_clear(value):
        """Helper to detect explicit clear intent (boolean False or literal 'false')."""
        if isinstance(value, list) and len(value) == 1:
            inner = value[0]
            if inner is False:
                return True
            if isinstance(inner, str) and inner.strip().lower() == 'false':
                return True
        if value is False:
            return True
        if isinstance(value, str) and value.strip().lower() == 'false':
            return True
        return False

    def _normalize_limits(self, value):
        if self._is_false_clear(value):
            return []
        if not isinstance(value, list):
            return []
        normalized = []
        for item in value:
            if not isinstance(item, dict):
                continue
            normalized.append({
                'prefix': int(item.get('prefix', 0)),
                'udpLimit': int(item.get('udpLimit', 0)),
                'tcpLimit': int(item.get('tcpLimit', 0))
            })
        return sorted(normalized, key=lambda x: x.get('prefix', 0))

    def _normalize_tsig_keys(self, value):
        if self._is_false_clear(value):
            return []
        if not isinstance(value, list):
            return []
        normalized = []
        for item in value:
            if not isinstance(item, dict):
                continue
            normalized.append({
                'keyName': item.get('keyName'),
                'sharedSecret': item.get('sharedSecret'),
                'algorithmName': item.get('algorithmName')
            })
        return sorted(normalized, key=lambda x: x.get('keyName') or '')

    def _normalize_value(self, key, value):
        if key in self.simple_list_fields:
            if value is None:
                return []
            if key in self.false_clear_simple_list_fields and self._is_false_clear(value):
                return []
            if isinstance(value, bool):
                return [str(value)]
            if isinstance(value, list):
                return sorted([str(v) for v in value])
            if isinstance(value, str):
                return sorted([v.strip() for v in value.split(",") if v.strip()])
            return [str(value)]
        if key in self.int_list_fields:
            if value is None:
                return []
            if isinstance(value, bool):
                return [] if value is False else [int(value)]
            if isinstance(value, list):
                return sorted([int(v) for v in value])
            if isinstance(value, str):
                parts = [p.strip() for p in value.split(",") if p.strip()]
            return sorted([int(p) for p in parts])
            return [int(value)]
        if key in ['qpmPrefixLimitsIPv4', 'qpmPrefixLimitsIPv6']:
            return self._normalize_limits(value)
        if key == 'tsigKeys':
            return self._normalize_tsig_keys(value)
        return value

    def _validate_list_or_false(self, name, value, allow_string=False):
        """Ensure raw-typed list fields accept only list/false/optional string for backward compatibility."""
        if value is None:
            return
        if self._is_false_clear(value):
            return
        if isinstance(value, list):
            return
        if allow_string and isinstance(value, str):
            return
        self.fail_json(msg=f"{name} must be a list or false to clear")

    def _serialize_list(self, value):
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, list):
            return ",".join(str(v) for v in value)
        return str(value)

    def _serialize_int_list(self, value):
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, list):
            return ",".join(str(int(v)) for v in value)
        return str(value)

    def _serialize_limits(self, value):
        if isinstance(value, bool):
            return str(value).lower()
        if not isinstance(value, list):
            return str(value)
        rows = []
        for item in value:
            rows.append("|".join([
                str(item.get('prefix', '')),
                str(item.get('udpLimit', '')),
                str(item.get('tcpLimit', ''))
            ]))
        return "|".join(rows)

    def _serialize_tsig_keys(self, value):
        if isinstance(value, bool):
            return str(value).lower()
        if not isinstance(value, list):
            return str(value)
        rows = []
        for item in value:
            rows.append("|".join([
                str(item.get('keyName', '')),
                str(item.get('sharedSecret', '')),
                str(item.get('algorithmName', ''))
            ]))
        return "|".join(rows)

    def _build_query(self, desired):
        query = {}
        for key, value in desired.items():
            if key in self.simple_list_fields:
                if key in self.false_clear_simple_list_fields and self._is_false_clear(value):
                    query[key] = 'false'
                else:
                    query[key] = self._serialize_list(value)
            elif key in self.int_list_fields:
                query[key] = self._serialize_int_list(value)
            elif key in ['qpmPrefixLimitsIPv4', 'qpmPrefixLimitsIPv6']:
                query[key] = self._serialize_limits(value)
            elif key == 'tsigKeys':
                query[key] = self._serialize_tsig_keys(value)
            elif isinstance(value, bool):
                query[key] = str(value).lower()
            else:
                query[key] = value
        return query

    def _compute_diff(self, current, desired):
        # Flatten proxy fields from nested structure (API response) for comparison
        proxy = current.get('proxy') or {}
        if proxy:
            current = dict(current)
            current['proxyType'] = proxy.get('type')
            current['proxyAddress'] = proxy.get('address')
            current['proxyPort'] = proxy.get('port')
            current['proxyUsername'] = proxy.get('username')
            current['proxyPassword'] = proxy.get('password')
            current['proxyBypass'] = proxy.get('bypass')

        diff = {}
        for key, desired_value in desired.items():
            current_value = current.get(key)

            # Treat blockListUrls cleared via "false" as equivalent to null/empty
            if key == 'blockListUrls' and self._is_false_clear(desired_value):
                if self._is_false_clear(current_value) or current_value in [None, []]:
                    continue

            norm_current = self._normalize_value(key, current_value)
            norm_desired = self._normalize_value(key, desired_value)

            if norm_current != norm_desired:
                diff[key] = {'current': current_value, 'desired': desired_value}
        return diff

    def run(self):
        params = self.params
        desired_settings = {}
        for key in self.settings_keys:
            value = params.get(key)
            if value is not None:
                desired_settings[key] = value

        if not desired_settings:
            self.fail_json(msg="At least one setting must be provided.")

        # Validate raw list-or-false fields before further processing
        for name in self.false_clear_limit_fields | self.false_clear_key_fields:
            if name in desired_settings:
                self._validate_list_or_false(name, desired_settings[name])
        for name in {'recursionNetworkACL', 'forwarders'}:
            if name in desired_settings:
                self._validate_list_or_false(name, desired_settings[name], allow_string=True)

        # Only allow clearing blockListUrls via explicit boolean false
        if 'blockListUrls' in desired_settings:
            val = desired_settings['blockListUrls']
            if isinstance(val, list) and len(val) == 0:
                self.fail_json(msg="blockListUrls can only be cleared with boolean false, not an empty list")

        current_settings = self.get_server_settings()

        # Special-case: clearing blockListUrls with False should be idempotent when already empty/null
        if 'blockListUrls' in desired_settings and self._is_false_clear(desired_settings.get('blockListUrls')):
            current_blocklists = self._normalize_value('blockListUrls', current_settings.get('blockListUrls'))
            desired_blocklists = self._normalize_value('blockListUrls', desired_settings.get('blockListUrls'))
            if current_blocklists == desired_blocklists:
                self.exit_json(
                    changed=False,
                    settings=current_settings,
                    msg="Server settings already match desired values"
                )

        diff = self._compute_diff(current_settings, desired_settings)

        if not diff:
            self.exit_json(
                changed=False,
                settings=current_settings,
                msg="Server settings already match desired values"
            )

        if self.check_mode:
            self.exit_json(
                changed=True,
                diff=diff,
                msg="(check mode) Server settings would be updated"
            )

        set_query = self._build_query(desired_settings)
        data = self.request('/api/settings/set', params=set_query, method='POST')
        self.validate_api_response(data, context="Failed to set server settings")
        updated_settings = data.get('response', {})

        self.exit_json(
            changed=True,
            diff=diff,
            settings=updated_settings,
            msg="Server settings updated successfully"
        )


if __name__ == '__main__':
    module = SetServerSettingsModule()
    module.run()
