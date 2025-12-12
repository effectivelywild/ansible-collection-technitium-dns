=============================================
effectivelywild.technitium\_dns Release Notes
=============================================

.. contents:: Topics

v1.1.1
======

v1.1.0
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_get_server_settings - Get DNS server settings.
- effectivelywild.technitium_dns.technitium_dns_set_server_settings - Update DNS server settings.

v1.0.1
======

v1.0.0
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_delete_cluster - Delete DNS cluster configuration.
- effectivelywild.technitium_dns.technitium_dns_delete_secondary_node - Immediately delete a Secondary node from the cluster.
- effectivelywild.technitium_dns.technitium_dns_get_cluster_state - Get DNS cluster state.
- effectivelywild.technitium_dns.technitium_dns_init_cluster - Initialize a new DNS cluster.
- effectivelywild.technitium_dns.technitium_dns_init_join_cluster - Join a DNS server to an existing cluster as a Secondary node.
- effectivelywild.technitium_dns.technitium_dns_leave_cluster - Leave a DNS cluster.
- effectivelywild.technitium_dns.technitium_dns_login - Authenticate and get a session token.
- effectivelywild.technitium_dns.technitium_dns_promote_secondary_node - Promote a Secondary node to Primary.
- effectivelywild.technitium_dns.technitium_dns_record - Manage DNS records.
- effectivelywild.technitium_dns.technitium_dns_remove_secondary_node - Remove a Secondary node from the cluster.
- effectivelywild.technitium_dns.technitium_dns_resync_cluster - Manually trigger cluster configuration resync.
- effectivelywild.technitium_dns.technitium_dns_set_cluster_options - Set DNS cluster options.
- effectivelywild.technitium_dns.technitium_dns_update_cluster_node_ip - Update cluster node IP address.
- effectivelywild.technitium_dns.technitium_dns_update_primary_node - Update Primary node details on a Secondary node.
- effectivelywild.technitium_dns.technitium_dns_zone - Manage DNS zones with state-based approach.

v0.9.1
======

v0.9.0
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_delete_log - Delete a log file.
- effectivelywild.technitium_dns.technitium_dns_download_and_install_app - Download and install an app.
- effectivelywild.technitium_dns.technitium_dns_download_and_update_app - Download and update an existing app.
- effectivelywild.technitium_dns.technitium_dns_get_app_config - Get app configuration.
- effectivelywild.technitium_dns.technitium_dns_list_apps - List all installed apps.
- effectivelywild.technitium_dns.technitium_dns_list_logs - List all log files from Technitium DNS server.
- effectivelywild.technitium_dns.technitium_dns_list_store_apps - List all available apps from Technitium DNS App Store.
- effectivelywild.technitium_dns.technitium_dns_query_logs - Query logs from a specified DNS app on Technitium DNS server.
- effectivelywild.technitium_dns.technitium_dns_set_app_config - Set app configuration on Technitium DNS server.
- effectivelywild.technitium_dns.technitium_dns_uninstall_app - Uninstall an app.

v0.8.0
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_delete_all_stats - Delete all statistics from Technitium DNS server.
- effectivelywild.technitium_dns.technitium_dns_delete_cache - Delete a cached DNS.
- effectivelywild.technitium_dns.technitium_dns_flush_cache - Flush the entire DNS cache.
- effectivelywild.technitium_dns.technitium_dns_get_stats - Get DNS statistics from server dashboard.
- effectivelywild.technitium_dns.technitium_dns_get_top_stats - Get top statistics for a specific type.
- effectivelywild.technitium_dns.technitium_dns_list_cache - List cached DNS zones and records.

v0.7.0
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_add_allowed_zone - Add a domain to the allowed zones.
- effectivelywild.technitium_dns.technitium_dns_add_blocked_zone - Add a domain to the blocked zones.
- effectivelywild.technitium_dns.technitium_dns_delete_allowed_zone - Delete a domain from the allowed zones in Technitium DNS server.
- effectivelywild.technitium_dns.technitium_dns_delete_blocked_zone - Delete a domain from the blocked zones in Technitium DNS server.
- effectivelywild.technitium_dns.technitium_dns_flush_allowed_zone - Flush all allowed zones in Technitium DNS server.
- effectivelywild.technitium_dns.technitium_dns_flush_blocked_zone - Flush all blocked zones.
- effectivelywild.technitium_dns.technitium_dns_list_allowed_zones - List allowed zones.
- effectivelywild.technitium_dns.technitium_dns_list_blocked_zones - List blocked zones.

v0.6.0
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_add_reserved_lease - Add a reserved DHCP lease.
- effectivelywild.technitium_dns.technitium_dns_convert_to_dynamic_lease - Convert a reserved DHCP lease to a dynamic lease.
- effectivelywild.technitium_dns.technitium_dns_convert_to_reserved_lease - Convert a dynamic DHCP lease to a reserved lease.
- effectivelywild.technitium_dns.technitium_dns_delete_dhcp_scope - Delete a DHCP scope.
- effectivelywild.technitium_dns.technitium_dns_disable_dhcp_scope - Disable a DHCP scope.
- effectivelywild.technitium_dns.technitium_dns_enable_dhcp_scope - Enable a DHCP scope.
- effectivelywild.technitium_dns.technitium_dns_get_dhcp_scope - Get DHCP scope details.
- effectivelywild.technitium_dns.technitium_dns_list_dhcp_leases - List all DHCP leases.
- effectivelywild.technitium_dns.technitium_dns_list_dhcp_scopes - List all DHCP scopes from Technitium DNS server.
- effectivelywild.technitium_dns.technitium_dns_remove_dhcp_lease - Remove a DHCP lease.
- effectivelywild.technitium_dns.technitium_dns_remove_reserved_lease - Remove a reserved DHCP lease from a scope.
- effectivelywild.technitium_dns.technitium_dns_set_dhcp_scope - Set DHCP scope configuration.

v0.5.0
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_change_password - Change password for the currently logged in user.
- effectivelywild.technitium_dns.technitium_dns_check_for_update - Check for available updates.
- effectivelywild.technitium_dns.technitium_dns_create_token - Create an API token for a user.
- effectivelywild.technitium_dns.technitium_dns_delete_session - Delete a user session.
- effectivelywild.technitium_dns.technitium_dns_get_permission_details - Get permission details for a specific section.
- effectivelywild.technitium_dns.technitium_dns_list_permissions - List all permissions.
- effectivelywild.technitium_dns.technitium_dns_list_sessions - List active user sessions.
- effectivelywild.technitium_dns.technitium_dns_set_permission_details - Set permission details for a specific section.

v0.4.0
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_create_group - Create a group.
- effectivelywild.technitium_dns.technitium_dns_create_user - Create a user account in Technitium DNS server.
- effectivelywild.technitium_dns.technitium_dns_delete_group - Delete a group.
- effectivelywild.technitium_dns.technitium_dns_delete_user - Delete a user account.
- effectivelywild.technitium_dns.technitium_dns_get_group_details - Get group details.
- effectivelywild.technitium_dns.technitium_dns_get_user_details - Get user account profile details.
- effectivelywild.technitium_dns.technitium_dns_list_groups - List all groups.
- effectivelywild.technitium_dns.technitium_dns_list_users - List all users.
- effectivelywild.technitium_dns.technitium_dns_publish_all_keys - Publish all generated DNSSEC private keys in a zone.
- effectivelywild.technitium_dns.technitium_dns_resync_zone - Resync a Secondary or Stub zone.
- effectivelywild.technitium_dns.technitium_dns_rollover_dnskey - Rollover DNSKEY for a DNSSEC-signed zone.
- effectivelywild.technitium_dns.technitium_dns_set_group_details - Set group details.
- effectivelywild.technitium_dns.technitium_dns_set_user_details - Set user account profile details.

v0.3.0
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_add_private_key - Add DNSSEC private key to a zone.
- effectivelywild.technitium_dns.technitium_dns_delete_private_key - Delete DNSSEC private key from a zone.
- effectivelywild.technitium_dns.technitium_dns_update_dnskey_ttl - Update DNSKEY TTL for a DNSSEC-signed zone.
- effectivelywild.technitium_dns.technitium_dns_update_private_key - Update DNSSEC private key properties.

v0.2.1
======

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_update_nsec3_parameters - Update NSEC3 Parameters.

v0.1.0
======

Release Summary
---------------

Test release for new CD workflow

New Modules
-----------

- effectivelywild.technitium_dns.technitium_dns_add_record - Add a DNS record.
- effectivelywild.technitium_dns.technitium_dns_convert_to_nsec - Convert a signed DNS zone from NSEC3 to NSEC.
- effectivelywild.technitium_dns.technitium_dns_convert_to_nsec3 - Convert a signed DNS zone from NSEC to NSEC3.
- effectivelywild.technitium_dns.technitium_dns_create_zone - Create a DNS zone.
- effectivelywild.technitium_dns.technitium_dns_delete_record - Delete a DNS record.
- effectivelywild.technitium_dns.technitium_dns_delete_zone - Delete a DNS zone.
- effectivelywild.technitium_dns.technitium_dns_disable_zone - Disable a DNS zone.
- effectivelywild.technitium_dns.technitium_dns_enable_zone - Enable a DNS zone.
- effectivelywild.technitium_dns.technitium_dns_get_dnssec_properties - Get DNSSEC properties for a primary zone.
- effectivelywild.technitium_dns.technitium_dns_get_record - Get DNS record(s).
- effectivelywild.technitium_dns.technitium_dns_get_zone_info - Get DNS zone(s).
- effectivelywild.technitium_dns.technitium_dns_get_zone_options - Get DNS zone options.
- effectivelywild.technitium_dns.technitium_dns_set_zone_options - Set DNS zone options.
- effectivelywild.technitium_dns.technitium_dns_sign_zone - Sign a DNS zone.
- effectivelywild.technitium_dns.technitium_dns_unsign_zone - Unsign a DNS zone.
