#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_flush_cache
short_description: Flush the entire DNS cache
version_added: "0.8.0"
description:
    - Clear all cached DNS records.
    - This is a destructive operation that affects all cached entries.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_cache
    description: List cached DNS zones and records
  - module: effectivelywild.technitium_dns.technitium_dns_delete_cache
    description: Delete a specific cached zone
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
'''

EXAMPLES = r'''
- name: Flush entire DNS cache
  technitium_dns_flush_cache:
    api_url: "http://localhost"
    api_token: "myapitoken"
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
    sample: "DNS cache flushed successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class FlushCacheModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Flush the entire cache from the API
        data = self.request('/api/cache/flush')
        self.validate_api_response(data)

        self.exit_json(
            changed=True,
            msg="DNS cache flushed successfully"
        )


if __name__ == '__main__':
    module = FlushCacheModule()
    module.run()
