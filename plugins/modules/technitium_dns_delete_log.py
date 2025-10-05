#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: technitium_dns_delete_log
short_description: Delete a log file from Technitium DNS server
version_added: "0.9.0"
description:
    - Permanently delete a log file from disk.
author:
    - Frank Muise (@effectivelywild)
seealso:
  - module: effectivelywild.technitium_dns.technitium_dns_list_logs
    description: List all log files
  - module: effectivelywild.technitium_dns.technitium_dns_delete_all_logs
    description: Delete all log files
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
    log:
        description:
            - The fileName of the log file to delete (as returned by technitium_dns_list_logs)
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Delete a specific log file
  technitium_dns_delete_log:
    api_url: "http://localhost"
    api_token: "myapitoken"
    log: "2020-09-19"
  register: result

- name: Delete multiple old log files
  technitium_dns_delete_log:
    api_url: "http://localhost"
    api_token: "myapitoken"
    log: "{{ item }}"
  loop:
    - "2020-09-10"
    - "2020-09-11"
    - "2020-09-12"
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
    sample: "Log file '2020-09-19' deleted successfully"
'''

from ansible_collections.effectivelywild.technitium_dns.plugins.module_utils.technitium import TechnitiumModule


class DeleteLogModule(TechnitiumModule):
    argument_spec = dict(
        log=dict(type='str', required=True),
        **TechnitiumModule.get_common_argument_spec()
    )

    def run(self):
        log = self.params['log']

        # Check if the log file exists before deleting
        log_exists, log_data = self.check_log_exists(log)

        # Delete the log file
        params = {
            'log': log
        }
        data = self.request('/api/logs/delete', params=params)
        self.validate_api_response(data)

        # Only mark as changed if the log actually existed
        if log_exists:
            self.exit_json(
                changed=True,
                msg=f"Log file '{log}' deleted successfully"
            )
        else:
            self.exit_json(
                changed=False,
                msg=f"Log file '{log}' does not exist, no changes made"
            )


if __name__ == '__main__':
    module = DeleteLogModule()
    module.run()
