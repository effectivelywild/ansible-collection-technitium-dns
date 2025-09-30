#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_get_permission_details
short_description: Get permission details for a specific section from Technitium DNS server
version_added: "0.5.0"
description:
    - Retrieve detailed permission information for a specific section from Technitium DNS server.
    - Returns user permissions, group permissions, and optionally lists of users and groups.
    - The includeUsersAndGroups option controls whether to include user and group lists.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_permissions
    description: List all permissions from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_list_users
    description: List all users from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_list_groups
    description: List all groups from Technitium DNS server
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
    section:
        description:
            - The name of the section to get permission details for
            - Should match a section name from the list permissions API call
        required: true
        type: str
    includeUsersAndGroups:
        description:
            - Whether to include lists of users and groups in the response
        required: false
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: Get Dashboard permission details
  technitium_dns_get_permission_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    section: "Dashboard"
  register: result

- debug:
    var: result.permission_details

- name: Get Zones permission details without user/group lists
  technitium_dns_get_permission_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    section: "Zones"
    includeUsersAndGroups: false
  register: result

- debug:
    var: result.permission_details
'''

RETURN = r'''
changed:
    description: Whether the module made changes (always false for get operations)
    type: bool
    returned: always
    sample: false
permission_details:
    description: Complete permission details for the specified section
    type: dict
    returned: always
    contains:
        section:
            description: The name of the permission section
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
                    sample: "shreyas"
                canView:
                    description: Whether the user can view this section
                    type: bool
                    returned: always
                    sample: true
                canModify:
                    description: Whether the user can modify this section
                    type: bool
                    returned: always
                    sample: false
                canDelete:
                    description: Whether the user can delete from this section
                    type: bool
                    returned: always
                    sample: false
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
        users:
            description: List of all available users (when includeUsersAndGroups is true)
            type: list
            returned: when includeUsersAndGroups is true
            elements: str
            sample: ["admin", "shreyas"]
        groups:
            description: List of all available groups (when includeUsersAndGroups is true)
            type: list
            returned: when includeUsersAndGroups is true
            elements: str
            sample: ["Administrators", "DHCP Administrators", "DNS Administrators", "Everyone"]
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class GetPermissionsDetailsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        section=dict(type='str', required=True),
        includeUsersAndGroups=dict(type='bool', required=False, default=True)
    )
    module_kwargs = dict(
        supports_check_mode=False
    )

    def run(self):
        section = self.params['section']
        include_users_and_groups = self.params['includeUsersAndGroups']

        # Check if section exists by listing all permissions (avoids stack trace on non-existent section)
        section_exists, existing_section = self.check_section_exists(section)
        if not section_exists:
            self.fail_json(msg=f"Permission section '{section}' does not exist")

        # Build API parameters for permission details request
        params = {
            'section': section,
            'includeUsersAndGroups': 'true' if include_users_and_groups else 'false'
        }

        # Fetch permission details from the Technitium API
        data = self.request('/api/admin/permissions/get', params=params)

        # Check API response status and handle errors
        self.validate_api_response(data)

        # Extract permission details from API response
        permission_details = data.get('response', {})

        # Return the permission details (read-only operation, never changed=True)
        self.exit_json(changed=False, permission_details=permission_details)


if __name__ == '__main__':
    module = GetPermissionsDetailsModule()
    module.run()
