# Initializing a cluster
The following example playbook will initialize a cluster and add two secondary nodes.


## Nodes

| Node Type | Hostname | IP           | API Port | HTTPS Port |
| ----------| -------- | ------------ | -------- | ---------- |
| Primary   | ns01     | 192.168.1.10 |   5380   |    53433   |
| Secondary | ns02     | 192.168.1.11 |   5380   |    53433   |
| Secondary | ns03     | 192.168.1.12 |   5380   |    53433   |

## Initilization 
It is important to create delays and pauses during initilization to ensure the cluster is stable before performing additional actions or you could receive API timeouts and other related errors.

In this example there is a 30 second pause after the initial initilization followed by delay loops when a secondary node is joining the cluster. After a secondary node joins the cluster there is another delay loop until the cluster `state` for that node retruns `Connected`.

**NOTE** - You may need to increase these time values if you are having issues. These are the timers used in the integration tests.

## API Tokens
After the secondary nodes have joined the cluster any generated API tokens will no longer be valid. You will need to login to receive a new token using the `technitium_dns.technitium_dns_login` module. You can then use this token for subsequent tasks.

```
- name: "Login to ns02 to create new token (join_init clears tokens)"
    effectivelywild.technitium_dns.technitium_dns_login:
    api_url: "http://localhost"
    api_port: 5380
    username: "admin"
    password: "topsecret"
    register: ns02_login

- name: "Update token fact for ns02"
    ansible.builtin.set_fact:
    token_ns02: "{{ ns02_login.token }}"
```