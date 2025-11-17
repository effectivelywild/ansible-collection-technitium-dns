from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import json
from urllib.parse import urlencode
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


class TechnitiumModule(AnsibleModule):
    argument_spec = {}
    module_kwargs = {}

    @classmethod
    def get_common_argument_spec(cls):
        """Return the common argument specification used by all Technitium modules."""
        return {
            'api_url': dict(type='str', required=True),
            'api_port': dict(type='int', required=False, default=5380),
            'api_token': dict(type='str', required=True, no_log=True),
            'validate_certs': dict(type='bool', required=False, default=True)
        }

    def __init__(self):
        super().__init__(
            argument_spec=self.argument_spec,
            **self.module_kwargs
        )
        self.api_url = self.params['api_url'].rstrip('/')
        self.api_port = self.params.get('api_port', 5380)
        self.api_token = self.params['api_token']
        self.validate_certs = self.params.get('validate_certs', True)
        self.name = self.params.get('name')

    def request(self, path, params=None, method='GET'):
        url = f"{self.api_url}:{self.api_port}{path}"
        params = params or {}
        params['token'] = self.api_token

        headers = {'Accept': 'application/json'}

        if method == 'GET':
            url_with_params = url + '?' + urlencode(params)
            data = None
        else:
            url_with_params = url
            data = urlencode(params)
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        try:
            resp, info = fetch_url(
                self,
                url_with_params,
                data=data,
                method=method,
                headers=headers,
                timeout=10
            )

            # Check if response is None (connection/transport failed)
            if resp is None:
                error_msg = "API request failed - no response received"
                if 'msg' in info:
                    error_msg += f": {info['msg']}"
                self.fail_json(msg=error_msg)

            # Check if the request failed with HTTP error status
            if info['status'] >= 400:
                error_msg = f"API request failed with status {info['status']}"
                if 'msg' in info:
                    error_msg += f": {info['msg']}"
                self.fail_json(msg=error_msg)

            return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            self.fail_json(msg=f"Technitium API request failed: {e}")

    def run(self):
        raise NotImplementedError("Subclasses must implement run()")

    def validate_zone_exists(self, zone, node=None):
        """Validate that a zone exists, fail gracefully if not"""
        get_query = {'zone': zone}
        if node:
            get_query['node'] = node
        get_data = self.request('/api/zones/options/get', params=get_query)
        error_msg = get_data.get('errorMessage')
        if error_msg and 'No such zone was found' in error_msg:
            self.fail_json(msg=f"Zone '{zone}' does not exist: {error_msg}")
        return get_data

    def get_dnssec_status(self, zone, node=None):
        """Get the DNSSEC status of a zone, with standardized error handling"""
        query = {'zone': zone}
        if node:
            query['node'] = node
        zone_options_resp = self.request('/api/zones/options/get', params=query)
        if zone_options_resp.get('status') != 'ok':
            error_msg = zone_options_resp.get('errorMessage') or zone_options_resp.get('error') or zone_options_resp.get('message') or "Unknown error"
            # Remove stackTrace if present for cleaner error responses
            clean_response = dict(zone_options_resp)
            clean_response.pop('stackTrace', None)
            self.fail_json(msg=f"Failed to fetch zone options: {error_msg}", api_response=clean_response)
        zone_info = zone_options_resp.get('response', {})
        dnssec_status = zone_info.get('dnssecStatus', '').lower()
        return dnssec_status, zone_info

    def get_dnssec_properties(self, zone, node=None):
        """Get DNSSEC properties for a zone, with standardized error handling

        Args:
            zone (str): Zone name
            node (str): Optional node parameter for cluster operations
        """
        params = {'zone': zone}
        if node:
            params['node'] = node
        data = self.request('/api/zones/dnssec/properties/get', params=params)

        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or data.get('error') or data.get('message') or "Unknown error"
            # Remove stackTrace if present for cleaner error responses
            clean_response = dict(data)
            clean_response.pop('stackTrace', None)
            self.fail_json(msg=f"Failed to fetch DNSSEC properties: {error_msg}", api_response=clean_response)

        return data.get('response', {})

    def check_user_exists(self, username):
        """Check if a user exists and return user data if found"""
        users_data = self.request('/api/admin/users/list')
        if users_data.get('status') != 'ok':
            error_msg = users_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check existing users: {error_msg}", api_response=users_data)

        users = users_data.get('response', {}).get('users', [])
        existing_user = next((u for u in users if u.get('username') == username), None)
        return existing_user is not None, existing_user

    def check_group_exists(self, group_name):
        """Check if a group exists and return group data if found"""
        groups_data = self.request('/api/admin/groups/list')
        if groups_data.get('status') != 'ok':
            error_msg = groups_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check existing groups: {error_msg}", api_response=groups_data)

        groups = groups_data.get('response', {}).get('groups', [])
        existing_group = next((g for g in groups if g.get('name') == group_name), None)
        return existing_group is not None, existing_group

    def check_builtin_group(self, group_name):
        """Check if a group is a built-in/protected group that cannot be deleted"""
        builtin_groups = ['Administrators', 'DHCP Administrators', 'DNS Administrators']
        return group_name in builtin_groups

    def get_dhcp_scope_status(self, scope_name):
        """Get DHCP scope status including enabled/disabled state

        Returns:
            tuple: (exists: bool, scope_data: dict or None)
            scope_data contains the full scope information including 'enabled' field
        """
        list_data = self.request('/api/dhcp/scopes/list')
        self.validate_api_response(list_data)

        scopes = list_data.get('response', {}).get('scopes', [])
        matching_scope = next((s for s in scopes if s.get('name') == scope_name), None)

        return matching_scope is not None, matching_scope

    def normalize_mac_address(self, mac):
        """Normalize MAC address to uppercase with hyphens for consistent comparison

        Handles both colon-separated (00:11:22:33:44:55) and hyphen-separated
        (00-11-22-33-44-55) formats, converting them to a standard format
        (00-11-22-33-44-55 uppercase) for comparison.

        Args:
            mac (str): MAC address in any common format

        Returns:
            str: Normalized MAC address in format XX-XX-XX-XX-XX-XX
        """
        # Remove common separators and convert to uppercase
        mac_clean = mac.replace(':', '').replace('-', '').upper()
        # Format as XX-XX-XX-XX-XX-XX
        return '-'.join([mac_clean[i:i + 2] for i in range(0, len(mac_clean), 2)])

    def validate_api_response(self, data, context=""):
        """Validate API response status and fail with standardized error message"""
        if data.get('status') != 'ok':
            error_msg = data.get('errorMessage') or "Unknown error"
            context_msg = f"{context}: " if context else ""
            self.fail_json(msg=f"{context_msg}Technitium API error: {error_msg}", api_response=data)

    def get_sessions_list(self):
        """Get list of all active sessions with standardized error handling"""
        sessions_data = self.request('/api/admin/sessions/list')
        if sessions_data.get('status') != 'ok':
            error_msg = sessions_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check existing sessions: {error_msg}", api_response=sessions_data)
        return sessions_data.get('response', {}).get('sessions', [])

    def check_session_exists_by_partial_token(self, partial_token):
        """Check if a session with the given partial token exists"""
        sessions = self.get_sessions_list()
        existing_session = next((s for s in sessions if s.get('partialToken') == partial_token), None)
        return existing_session is not None, existing_session

    def check_token_session_exists(self, username, token_name):
        """Check if a token session with the given name exists for the user"""
        sessions = self.get_sessions_list()
        existing_token = next((s for s in sessions
                              if s.get('username') == username
                              and s.get('tokenName') == token_name
                              and s.get('type') == 'ApiToken'), None)
        return existing_token is not None, existing_token

    def check_section_exists(self, section_name):
        """Check if a permission section exists by listing all permissions"""
        permissions_data = self.request('/api/admin/permissions/list')
        if permissions_data.get('status') != 'ok':
            error_msg = permissions_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check existing permissions: {error_msg}", api_response=permissions_data)

        permissions = permissions_data.get('response', {}).get('permissions', [])
        existing_section = next((p for p in permissions if p.get('section') == section_name), None)
        return existing_section is not None, existing_section

    def check_allowed_blocked_zone_exists(self, domain, zone_type='allowed'):
        """Check if a domain exists in allowed/blocked zone lists (ACL)

        Note: This is different from validate_zone_exists() which checks DNS zones.
        This method checks the allowed/blocked zone access control lists.

        Args:
            domain (str): Domain name to check
            zone_type (str): Either 'allowed' or 'blocked'

        Returns:
            tuple: (exists: bool, api_response: dict)
                - exists: True if domain exists in the zone, False otherwise
                - api_response: The full API response from the list endpoint
        """
        list_params = {'domain': domain}
        list_data = self.request(f'/api/{zone_type}/list', params=list_params)
        self.validate_api_response(list_data)

        response = list_data.get('response', {})
        zones = response.get('zones', [])
        records = response.get('records', [])

        # Check if domain exists in zones list or records
        if domain in zones:
            return True, list_data

        # Check in records list (domain might be in records as a zone)
        for record in records:
            if record.get('name') == domain:
                return True, list_data

        return False, list_data

    def check_log_exists(self, log_name):
        """Check if a log file exists and return log data if found

        Args:
            log_name (str): Name of the log file (e.g., "2025-10-05")

        Returns:
            tuple: (exists: bool, log_data: dict or None)
                - exists: True if log file exists, False otherwise
                - log_data: dict containing fileName and size if found, None otherwise
        """
        list_data = self.request('/api/logs/list')
        self.validate_api_response(list_data)

        log_files = list_data.get('response', {}).get('logFiles', [])
        existing_log = next((log for log in log_files if log.get('fileName') == log_name), None)
        return existing_log is not None, existing_log

    def check_app_exists(self, app_name, node=None):
        """Check if an app is installed and return app data if found

        Args:
            app_name (str): Name of the app (e.g., "Query Logs (Sqlite)")
            node (str): Optional node parameter for cluster environments

        Returns:
            tuple: (exists: bool, app_data: dict or None)
                - exists: True if app is installed, False otherwise
                - app_data: dict containing app details if found, None otherwise
        """
        params = {}
        if node:
            params['node'] = node

        list_data = self.request('/api/apps/list', params=params)
        self.validate_api_response(list_data)

        apps = list_data.get('response', {}).get('apps', [])
        existing_app = next((app for app in apps if app.get('name') == app_name), None)
        return existing_app is not None, existing_app

    # Clustering helper methods

    def get_cluster_state(self, node=None, fail_on_error=True):
        """Get cluster state with standardized error handling

        Args:
            node (str): Optional node domain name for the API call
            fail_on_error (bool): Whether to fail on API errors (default True)

        Returns:
            tuple: (cluster_initialized: bool, cluster_state: dict)
                - cluster_initialized: Whether the cluster is initialized
                - cluster_state: The complete cluster state response
        """
        state_params = {}
        if node:
            state_params['node'] = node

        state_data = self.request('/api/admin/cluster/state', params=state_params)
        if fail_on_error and state_data.get('status') != 'ok':
            error_msg = state_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check cluster state: {error_msg}", api_response=state_data)

        cluster_state = state_data.get('response', {})
        cluster_initialized = cluster_state.get('clusterInitialized', False)

        return cluster_initialized, cluster_state

    def get_self_node(self, cluster_state):
        """Get the current node from cluster state

        Args:
            cluster_state (dict): The cluster state response containing clusterNodes

        Returns:
            dict or None: The self node data, or None if not found
        """
        current_nodes = cluster_state.get('clusterNodes', [])
        return next((n for n in current_nodes if n.get('state') == 'Self'), None)

    def get_primary_node(self, cluster_state):
        """Get the Primary node from cluster state

        Args:
            cluster_state (dict): The cluster state response containing clusterNodes

        Returns:
            dict or None: The Primary node data, or None if not found
        """
        current_nodes = cluster_state.get('clusterNodes', [])
        return next((n for n in current_nodes if n.get('type') == 'Primary'), None)

    def get_node_by_id(self, cluster_state, node_id, expected_type=None, fail_if_not_found=True):
        """Get a specific node from cluster state by ID

        Args:
            cluster_state (dict): The cluster state response containing clusterNodes
            node_id (int): The node ID to find
            expected_type (str): Optional expected node type ('Primary' or 'Secondary')
            fail_if_not_found (bool): Whether to fail if node is not found (default True)

        Returns:
            dict or None: The node data if found, None if not found and fail_if_not_found=False

        Raises:
            AnsibleFailJson if node is not found and fail_if_not_found=True
            AnsibleFailJson if expected_type is set and doesn't match
        """
        current_nodes = cluster_state.get('clusterNodes', [])
        node = next((n for n in current_nodes if n.get('id') == node_id), None)

        if not node:
            if fail_if_not_found:
                self.fail_json(
                    changed=False,
                    cluster_state=cluster_state,
                    msg=f"Node with ID {node_id} not found in cluster"
                )
            return None

        if expected_type:
            actual_type = node.get('type')
            if actual_type != expected_type:
                self.fail_json(
                    msg=f"Node {node_id} is type '{actual_type}', not '{expected_type}'",
                    cluster_state=cluster_state
                )

        return node

    def validate_cluster_node_type(self, cluster_state, expected_type, custom_error_msg=None):
        """Validate that the current node is of the expected type

        Args:
            cluster_state (dict): The cluster state response containing clusterNodes
            expected_type (str): Expected node type ('Primary' or 'Secondary')
            custom_error_msg (str): Optional custom error message

        Returns:
            dict: The self node data if validation passes

        Raises:
            AnsibleFailJson if node type doesn't match expected_type
        """
        self_node = self.get_self_node(cluster_state)

        if not self_node:
            self.fail_json(
                msg="Could not identify current node in cluster",
                cluster_state=cluster_state
            )

        actual_type = self_node.get('type')
        if actual_type != expected_type:
            if custom_error_msg:
                error_msg = custom_error_msg
            else:
                error_msg = f"This is not a {expected_type} node. Current node type is '{actual_type}'."

            self.fail_json(msg=error_msg, cluster_state=cluster_state)

        return self_node

    def require_cluster_initialized(self, cluster_initialized, cluster_state, fail_message=None):
        """Ensure cluster is initialized, fail if not

        Args:
            cluster_initialized (bool): Whether cluster is initialized
            cluster_state (dict): The cluster state response
            fail_message (str): Optional custom failure message

        Raises:
            AnsibleFailJson if cluster is not initialized
        """
        if not cluster_initialized:
            msg = fail_message or "Cluster is not initialized"
            self.fail_json(msg=msg, cluster_state=cluster_state)

    def require_cluster_not_initialized(self, cluster_initialized, cluster_state, exit_message=None):
        """Ensure cluster is not initialized (for idempotent cleanup operations)

        Args:
            cluster_initialized (bool): Whether cluster is initialized
            cluster_state (dict): The cluster state response
            exit_message (str): Optional custom success message

        Returns:
            None if cluster is not initialized (allows continuing execution)

        Side Effects:
            Calls exit_json if cluster is not initialized
        """
        if not cluster_initialized:
            msg = exit_message or "Cluster is not initialized"
            self.exit_json(changed=False, cluster_state=cluster_state, msg=msg)

    def build_cluster_params(self, node=None, **additional_params):
        """Build request parameters with optional node parameter

        Args:
            node (str): Optional node domain name
            **additional_params: Additional parameters to include

        Returns:
            dict: Parameters dictionary with node added if provided
        """
        params = {}
        if node:
            params['node'] = node
        params.update(additional_params)
        return params

    def __call__(self):
        self.run()
