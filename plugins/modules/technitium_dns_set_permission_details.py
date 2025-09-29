#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_set_permission_details
short_description: Set permission details for a specific section in Technitium DNS server
version_added: "0.5.0"
description:
    - Change permissions for a specific section in Technitium DNS server.
    - Allows setting user permissions and group permissions with view, modify, and delete access.
    - This module is idempotent and will only make changes when the desired permissions differ from current permissions.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_get_permission_details
    description: Get permission details for a specific section from Technitium DNS server
  - module: effectivelywild.technitium_dns.technitium_dns_list_permissions
    description: List all permissions from Technitium DNS server
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
            - The name of the section to set permissions for
            - Should match a section name from the list permissions API call
        required: true
        type: str
    userPermissions:
        description:
            - List of user permissions to set for this section
            - Each item should contain username, canView, canModify, and canDelete
        required: false
        type: list
        elements: dict
        suboptions:
            username:
                description: Username to set permissions for
                required: true
                type: str
            canView:
                description: Whether the user can view this section
                required: true
                type: bool
            canModify:
                description: Whether the user can modify this section
                required: true
                type: bool
            canDelete:
                description: Whether the user can delete from this section
                required: true
                type: bool
    groupPermissions:
        description:
            - List of group permissions to set for this section
            - Each item should contain group name, canView, canModify, and canDelete
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Group name to set permissions for
                required: true
                type: str
            canView:
                description: Whether the group can view this section
                required: true
                type: bool
            canModify:
                description: Whether the group can modify this section
                required: true
                type: bool
            canDelete:
                description: Whether the group can delete from this section
                required: true
                type: bool
'''

EXAMPLES = r'''
- name: Set Dashboard permissions for a user
  technitium_dns_set_permission_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    section: "Dashboard"
    userPermissions:
      - username: "testuser"
        canView: true
        canModify: true
        canDelete: false

- name: Set Cache permissions for a group
  technitium_dns_set_permission_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    section: "Cache"
    groupPermissions:
      - name: "testgroup"
        canView: true
        canModify: true
        canDelete: true

- name: Set both user and group permissions for Zones
  technitium_dns_set_permission_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    section: "Zones"
    userPermissions:
      - username: "user1"
        canView: true
        canModify: false
        canDelete: false
    groupPermissions:
      - name: "Administrators"
        canView: true
        canModify: true
        canDelete: true
      - name: "Everyone"
        canView: true
        canModify: false
        canDelete: false

- name: Check what would change (check mode)
  technitium_dns_set_permission_details:
    api_url: "http://localhost"
    api_token: "myapitoken"
    section: "Dashboard"
    userPermissions:
      - username: "testuser"
        canView: true
        canModify: true
        canDelete: true
  check_mode: true
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: Updated permission details from the API
            type: dict
            contains:
                section:
                    description: The name of the permission section
                    type: str
                    returned: always
                    sample: "Dashboard"
                userPermissions:
                    description: Updated user permissions for this section
                    type: list
                    returned: always
                    elements: dict
                groupPermissions:
                    description: Updated group permissions for this section
                    type: list
                    returned: always
                    elements: dict
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes
    type: bool
    returned: always
    sample: true
diff:
    description: Dictionary showing what changed, with current and desired values
    type: dict
    returned: when changes are made
    sample: {
        "userPermissions": {
            "current": [],
            "desired": [{"username": "testuser", "canView": true, "canModify": true, "canDelete": false}]
        }
    }
failed:
    description: Whether the module failed
    type: bool
    returned: always
    sample: false
msg:
    description: Human readable message describing the result
    type: str
    returned: always
    sample: "Permissions updated successfully for section 'Dashboard'."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class SetPermissionsDetailsModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        section=dict(type='str', required=True),
        userPermissions=dict(
            type='list',
            elements='dict',
            required=False,
            options=dict(
                username=dict(type='str', required=True),
                canView=dict(type='bool', required=True),
                canModify=dict(type='bool', required=True),
                canDelete=dict(type='bool', required=True)
            )
        ),
        groupPermissions=dict(
            type='list',
            elements='dict',
            required=False,
            options=dict(
                name=dict(type='str', required=True),
                canView=dict(type='bool', required=True),
                canModify=dict(type='bool', required=True),
                canDelete=dict(type='bool', required=True)
            )
        )
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def check_section_exists(self, section_name):
        """Check if a permission section exists by listing all permissions"""
        permissions_data = self.request('/api/admin/permissions/list')
        if permissions_data.get('status') != 'ok':
            error_msg = permissions_data.get('errorMessage') or "Unknown error"
            self.fail_json(msg=f"Failed to check existing permissions: {error_msg}", api_response=permissions_data)

        permissions = permissions_data.get('response', {}).get('permissions', [])
        existing_section = next((p for p in permissions if p.get('section') == section_name), None)
        return existing_section is not None, existing_section

    def _normalize_permissions_list(self, permissions_list):
        """Normalize and sort permissions list for consistent comparison"""
        if not permissions_list:
            return []

        # Sort by username/name and normalize boolean values
        normalized = []
        for perm in permissions_list:
            normalized_perm = {}
            for key, value in perm.items():
                if key in ['canView', 'canModify', 'canDelete']:
                    normalized_perm[key] = bool(value)
                else:
                    normalized_perm[key] = value
            normalized.append(normalized_perm)

        # Sort by username or name
        sort_key = 'username' if 'username' in normalized[0] else 'name'
        return sorted(normalized, key=lambda x: x[sort_key])

    def _format_permissions_for_api(self, permissions_list, permission_type):
        """Format permissions list into pipe-separated string for API"""
        if not permissions_list:
            return None

        formatted_parts = []
        for perm in permissions_list:
            if permission_type == 'user':
                name = perm['username']
            else:  # group
                name = perm['name']

            can_view = str(perm['canView']).lower()
            can_modify = str(perm['canModify']).lower()
            can_delete = str(perm['canDelete']).lower()

            formatted_parts.append(f"{name}|{can_view}|{can_modify}|{can_delete}")

        return "|".join(formatted_parts)

    def run(self):
        params = self.params
        section = params['section']
        desired_user_permissions = params.get('userPermissions', [])
        desired_group_permissions = params.get('groupPermissions', [])

        # Validate that at least one permission type is provided
        if not desired_user_permissions and not desired_group_permissions:
            self.fail_json(msg="At least one of userPermissions or groupPermissions must be provided")

        # Check if section exists
        section_exists, existing_section = self.check_section_exists(section)
        if not section_exists:
            self.fail_json(msg=f"Permission section '{section}' does not exist")

        # Get current permissions for the section
        current_data = self.request('/api/admin/permissions/get', params={'section': section, 'includeUsersAndGroups': 'false'})
        self.validate_api_response(current_data, f"Failed to get current permissions for section '{section}'")

        current = current_data.get('response', {})
        current_user_permissions = current.get('userPermissions', [])
        current_group_permissions = current.get('groupPermissions', [])

        # Compare current vs desired for idempotency
        diff = {}

        if desired_user_permissions:
            normalized_current_users = self._normalize_permissions_list(current_user_permissions)
            normalized_desired_users = self._normalize_permissions_list(desired_user_permissions)

            if normalized_current_users != normalized_desired_users:
                diff['userPermissions'] = {
                    'current': normalized_current_users,
                    'desired': normalized_desired_users
                }

        if desired_group_permissions:
            normalized_current_groups = self._normalize_permissions_list(current_group_permissions)
            normalized_desired_groups = self._normalize_permissions_list(desired_group_permissions)

            if normalized_current_groups != normalized_desired_groups:
                diff['groupPermissions'] = {
                    'current': normalized_current_groups,
                    'desired': normalized_desired_groups
                }

        # If no changes needed, exit early
        if not diff:
            self.exit_json(changed=False, msg=f"Permissions for section '{section}' already match desired state.")

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            self.exit_json(
                changed=True,
                msg=f"(check mode) Permissions for section '{section}' would be updated.",
                diff=diff,
                api_response={"status": "ok", "check_mode": True, "section": section}
            )

        # Build API parameters
        set_query = {'section': section}

        if desired_user_permissions:
            user_perms_str = self._format_permissions_for_api(desired_user_permissions, 'user')
            if user_perms_str:
                set_query['userPermissions'] = user_perms_str

        if desired_group_permissions:
            group_perms_str = self._format_permissions_for_api(desired_group_permissions, 'group')
            if group_perms_str:
                set_query['groupPermissions'] = group_perms_str

        # Make the API call to set permissions
        data = self.request('/api/admin/permissions/set', params=set_query, method='POST')
        self.validate_api_response(data)

        # Return success with changes made
        self.exit_json(
            changed=True,
            msg=f"Permissions updated successfully for section '{section}'.",
            diff=diff,
            api_response=data
        )


if __name__ == '__main__':
    module = SetPermissionsDetailsModule()
    module.run()
