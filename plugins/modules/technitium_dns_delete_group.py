#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_group
short_description: Delete a group
version_added: "0.4.0"
description:
    - Delete a group.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_create_group
    description: Create a group
  - module: effectivelywild.technitium_dns.technitium_dns_list_groups
    description: List all groups
  - module: effectivelywild.technitium_dns.technitium_dns_get_group_details
    description: Get group details
  - module: effectivelywild.technitium_dns.technitium_dns_set_group_details
    description: Set group details
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
    group:
        description:
            - The name of the group to delete
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Delete a group
  technitium_dns_delete_group:
    api_url: "http://localhost"
    api_token: "myapitoken"
    group: "testgroup"
'''

RETURN = r'''
api_response:
    description: Complete raw API response from Technitium DNS
    type: dict
    returned: always
    contains:
        response:
            description: The core data payload from the API (empty for delete operations)
            type: dict
            returned: always
            sample: {}
        status:
            description: API response status
            type: str
            returned: always
            sample: "ok"
changed:
    description: Whether the module made changes to delete the group
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed to complete the group deletion
    type: bool
    returned: always
    sample: false
msg:
    description: Human-readable message describing the group deletion result
    type: str
    returned: always
    sample: "Group 'testgroup' deleted."
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteGroupModule(TechnitiumModule):
    argument_spec = dict(
        **TechnitiumModule.get_common_argument_spec(),
        group=dict(type='str', required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        group_name = self.params['group']

        # Check if this is a built-in group that cannot be deleted
        if self.check_builtin_group(group_name):
            self.fail_json(msg=f"Cannot delete built-in group '{group_name}'")

        # Check if the group exists to ensure idempotent behavior
        # Idempotent delete: if group doesn't exist, report no changes made
        group_exists, existing_group = self.check_group_exists(group_name)

        # Handle check mode - report what would be done without making changes
        if self.check_mode:
            if group_exists:
                self.exit_json(changed=True, msg=f"Group '{group_name}' would be deleted (check mode)", api_response={})
            else:
                self.exit_json(changed=False, msg=f"Group '{group_name}' does not exist (check mode)", api_response={})

        # Implement idempotent delete behavior
        # If group doesn't exist, return success without changes (already deleted)
        if not group_exists:
            self.exit_json(
                changed=False,
                msg=f"Group '{group_name}' does not exist.",
                api_response={'status': 'ok', 'msg': f"Group '{group_name}' does not exist."}
            )

        # Delete the group via the Technitium API
        data = self.request('/api/admin/groups/delete', params={'group': group_name}, method='POST')
        self.validate_api_response(data)

        # Return success - group was deleted
        self.exit_json(changed=True, msg=f"Group '{group_name}' deleted.", api_response=data)


if __name__ == '__main__':
    module = DeleteGroupModule()
    module.run()
