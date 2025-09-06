from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
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
        from urllib.parse import urlencode, quote
        
        url = f"{self.api_url}:{self.api_port}{path}"
        params = params or {}
        params['token'] = self.api_token

        if method == 'GET':
            url_with_params = url + '?' + urlencode(params)
            data = None
        else:
            url_with_params = url
            data = urlencode(params)

        try:
            # Note: validate_certs parameter is accepted but may not be fully supported
            # by all Ansible versions. For HTTPS connections with self-signed certificates,
            # you may need to use environment variables like SSL_VERIFY=false
            resp, info = fetch_url(
                self,
                url_with_params,
                data=data,
                method=method,
                headers={'Accept': 'application/json'},
                timeout=10
            )
            
            # Check if the request failed
            if info['status'] >= 400:
                error_msg = f"API request failed with status {info['status']}"
                if 'msg' in info:
                    error_msg += f": {info['msg']}"
                self.fail_json(msg=error_msg)
            
            # Check if response is None (connection failed)
            if resp is None:
                error_msg = "API request failed - no response received"
                if 'msg' in info:
                    error_msg += f": {info['msg']}"
                self.fail_json(msg=error_msg)

            import json
            return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            self.fail_json(msg=f"Technitium API request failed: {e}")

    def run(self):
        raise NotImplementedError("Subclasses must implement run()")

    def validate_zone_exists(self, zone):
        """Validate that a zone exists, fail gracefully if not"""
        get_query = {'zone': zone}
        get_data = self.request('/api/zones/options/get', params=get_query)
        error_msg = get_data.get('errorMessage')
        if error_msg and 'No such zone was found' in error_msg:
            self.fail_json(msg=f"Zone '{zone}' does not exist: {error_msg}")
        return get_data

    def get_dnssec_status(self, zone):
        """Get the DNSSEC status of a zone, with standardized error handling"""
        zone_options_resp = self.request('/api/zones/options/get', params={'zone': zone})
        if zone_options_resp.get('status') != 'ok':
            error_msg = zone_options_resp.get('errorMessage') or zone_options_resp.get('error') or zone_options_resp.get('message') or "Unknown error"
            # Remove stackTrace if present for cleaner error responses
            clean_response = dict(zone_options_resp)
            clean_response.pop('stackTrace', None)
            self.fail_json(msg=f"Failed to fetch zone options: {error_msg}", api_response=clean_response)
        zone_info = zone_options_resp.get('response', {})
        dnssec_status = zone_info.get('dnssecStatus', '').lower()
        return dnssec_status, zone_info

    def __call__(self):
        self.run()
