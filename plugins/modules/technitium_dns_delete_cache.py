#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_cache
short_description: Delete a cached DNS
version_added: "0.8.0"
description:
    - Delete cached DNS records for a specific domain.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_cache
    description: List cached DNS zones and records
  - module: effectivelywild.technitium_dns.technitium_dns_flush_cache
    description: Flush the entire DNS cache
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
    domain:
        description:
            - The domain name to delete cached records for.
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Delete cached records for google.com
  technitium_dns_delete_cache:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "google.com"
  register: result

- name: Delete cached records for subdomain
  technitium_dns_delete_cache:
    api_url: "http://localhost"
    api_token: "myapitoken"
    domain: "www.example.com"
  register: result
'''

RETURN = r'''
changed:
    description: Whether the module made changes
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message about the operation
    type: str
    returned: always
    sample: "Cached zone 'google.com' deleted successfully"
domain:
    description: The domain that was deleted from cache
    type: str
    returned: always
    sample: "google.com"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteCacheModule(TechnitiumModule):
    argument_spec = dict(
        domain=dict(type='str', required=True),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        domain = self.params['domain']

        params = {
            'domain': domain
        }

        # Delete the cached zone from the API
        data = self.request('/api/cache/delete', params=params)
        self.validate_api_response(data)

        self.exit_json(
            changed=True,
            msg=f"Cached zone '{domain}' deleted successfully",
            domain=domain
        )


if __name__ == '__main__':
    module = DeleteCacheModule()
    module.run()
