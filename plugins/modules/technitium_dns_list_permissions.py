#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_list_permissions
short_description: List all permissions
version_added: "0.5.0"
description:
    - Retrieve a list of all permissions.
    - This includes both user permissions and group permissions for each section.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_permission_details
    description: Get permission details for a specific section
  - module: effectivelywild.technitium_dns.technitium_dns_set_permission_details
    description: Set permission details for a specific section
  - module: effectivelywild.technitium_dns.technitium_dns_list_users
    description: List all users
  - module: effectivelywild.technitium_dns.technitium_dns_list_groups
    description: List all groups
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
            - Whether to validate SSL certificates when making API requests
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: List all permissions from Technitium DNS
  technitium_dns_list_permissions:
    api_url: "http://localhost"
    api_token: "myapitoken"
  register: result

- debug:
    var: result.permissions
'''

RETURN = r'''
permissions:
    description: List of permissions from the Technitium DNS server
    type: list
    returned: always
    elements: dict
    contains:
        section:
            description: The permission section name
            type: str
            returned: always
            sample: "Dashboard"
        userPermissions:
            description: List of user permissions for this section
            type: list
            returned: always
            elements: dict
            contains:
                username:
                    description: Username of the user
                    type: str
                    returned: always
                    sample: "frank"
                canView:
                    description: Whether the user can view this section
                    type: bool
                    returned: always
                    sample: true
                canModify:
                    description: Whether the user can modify this section
                    type: bool
                    returned: always
                    sample: true
                canDelete:
                    description: Whether the user can delete from this section
                    type: bool
                    returned: always
                    sample: true
        groupPermissions:
            description: List of group permissions for this section
            type: list
            returned: always
            elements: dict
            contains:
                name:
                    description: Name of the group
                    type: str
                    returned: always
                    sample: "Administrators"
                canView:
                    description: Whether the group can view this section
                    type: bool
                    returned: always
                    sample: true
                canModify:
                    description: Whether the group can modify this section
                    type: bool
                    returned: always
                    sample: true
                canDelete:
                    description: Whether the group can delete from this section
                    type: bool
                    returned: always
                    sample: true
changed:
    description: Whether the module made changes (always false for list operations)
    type: bool
    returned: always
    sample: false
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class ListPermissionsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        # Fetch all permissions from the API
        data = self.request('/api/admin/permissions/list')
        self.validate_api_response(data)

        permissions = data.get('response', {}).get('permissions', [])
        self.exit_json(changed=False, permissions=permissions)


if __name__ == '__main__':
    module = ListPermissionsModule()
    module.run()
