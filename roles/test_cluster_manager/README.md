# Test Cluster Manager Role

This role manages the setup and teardown of a 2-node Technitium DNS cluster for integration testing.

## Purpose

Provides a reusable way to:
- Spin up a test cluster (primary + secondary nodes)
- Initialize clustering
- Clean up cluster resources

## Requirements

- Docker must be installed and running
- `community.docker` collection must be installed
- Ansible 2.9 or higher

## Role Variables

### Action Control
- `cluster_action`: (required) Either `"setup"` or `"teardown"`

### Container Configuration
- `cluster_primary_container_name`: Name for primary container (default: `"technitium_primary"`)
- `cluster_secondary_container_name`: Name for secondary container (default: `"technitium_secondary"`)
- `cluster_container_image`: Docker image to use (default: `"technitium/dns-server:latest"`)
- `cluster_network_name`: Docker network name (default: `"technitium_cluster_net"`)

### Network Configuration
- `cluster_primary_ip`: Primary node IP (default: `"172.30.0.10"`)
- `cluster_secondary_ip`: Secondary node IP (default: `"172.30.0.11"`)
- `cluster_subnet`: Network subnet (default: `"172.30.0.0/24"`)

### DNS Configuration
- `primary_domain`: Primary node domain (default: `"cluster01.local"`)
- `secondary_domain`: Secondary node domain (default: `"cluster02.local"`)
- `cluster_domain`: Cluster domain name (default: `"cluster.local"`)

### API Configuration
- `cluster_primary_http_port`: Primary node HTTP port (default: `"5391"`)
- `cluster_secondary_http_port`: Secondary node HTTP port (default: `"5392"`)
- `cluster_primary_https_port`: Primary node HTTPS port (default: `"53491"`)
- `cluster_secondary_https_port`: Secondary node HTTPS port (default: `"53492"`)
- `cluster_admin_username`: Admin username (default: `"admin"`)
- `cluster_admin_password`: Admin password (default: `"topsecret"`)

### Timeout Settings
- `cluster_startup_wait_seconds`: Initial wait time (default: `10`)
- `cluster_api_retry_count`: API ready check retries (default: `10`)
- `cluster_api_retry_delay`: Delay between retries (default: `3`)

## Exported Variables (after setup)

After running with `cluster_action: "setup"`, these facts are available:
### Primary node
- `cluster_primary_url`: Primary node URL
- `cluster_primary_http_port`: Primary node http port 
- `cluster_primary_https_port`: Primary node https port 
- `cluster_primary_api_token`: Primary node API token
- `cluster_primary_node_domain`: Primary nodes domain name
- `cluster_primary_node_ip`: Primary node docker IP

### Secondary node
- `cluster_secondary_url`: Secondary node URL
- `cluster_secondary_http_port`: Secondary node http port 
- `cluster_secondary_https_port`: Secondary node https port 
- `cluster_secondary_api_token`: Secondary node API token
- `cluster_secondary_node_domain`: Secondary nodes domain name
- `cluster_secondary_node_ip`: Secondary node docker IP

### Cluster info
- `cluster_is_ready`: Boolean indicating cluster is ready
- `cluster_primary_node_url`: Primary node URL
- `cluster_admin_user`: Admin username
- `cluster_admin_pass`: Admin password

## Example Usage

### Basic Setup and Teardown

```yaml
---
# Setup cluster
- name: Setup test cluster
  include_role:
    name: test_cluster_manager
  vars:
    cluster_action: "setup"

# Your tests here
- name: Test module with node parameter
  technitium_dns_get_stats:
    api_url: "{{ cluster_primary_url }}"
    api_token: "{{ cluster_primary_api_token }}"
    api_port: "{{ cluster_primary_http_port }}"
    node: "{{ cluster_secondary_node_domain }}"
  register: result

- name: Test module with cluster parameter
  technitium_dns_get_stats:
    api_url: "{{ cluster_primary_url }}"
    api_token: "{{ cluster_primary_api_token }}"
    api_port: "{{ cluster_primary_http_port }}"
    node: "cluster"
  register: result

# Teardown cluster
- name: Teardown test cluster
  include_role:
    name: test_cluster_manager
  vars:
    cluster_action: "teardown"
```

### In Module Integration Tests

```yaml
---
# tests/integration/targets/technitium_dns_get_stats/tasks/main.yml

- name: Load test configuration
  include_vars: ../../integration_config.yml

# Setup cluster
- name: Setup test cluster for node parameter tests
  include_role:
    name: test_cluster_manager
  vars:
    cluster_action: "setup"

# Test without node parameter (default behavior)
- name: Get stats without node parameter
  technitium_dns_get_stats:
    api_url: "{{ cluster_primary_url }}"
    api_token: "{{ cluster_primary_api_token }}"
    api_port: "{{ cluster_primary_http_port }}"
  register: stats_default

- name: Assert default stats returned
  assert:
    that:
      - not stats_default.failed
      - stats_default.stats is defined

# Test with specific node
- name: Get stats for secondary node
  technitium_dns_get_stats:
    api_url: "{{ cluster_primary_url }}"
    api_token: "{{ cluster_primary_api_token }}"
    api_port: "{{ cluster_primary_http_port }}"
    node: "{{ cluster_secondary_node_domain }}"
  register: stats_secondary

- name: Assert secondary node stats returned
  assert:
    that:
      - not stats_secondary.failed
      - stats_secondary.stats is defined

# Test with cluster parameter
- name: Get cluster-wide stats
  technitium_dns_get_stats:
    api_url: "{{ cluster_primary_url }}"
    api_token: "{{ cluster_primary_api_token }}"
    api_port: "{{ cluster_primary_http_port }}"
    node: "cluster"
  register: stats_cluster

- name: Assert cluster stats returned
  assert:
    that:
      - not stats_cluster.failed
      - stats_cluster.stats is defined

# Cleanup
- name: Teardown test cluster
  include_role:
    name: test_cluster_manager
  vars:
    cluster_action: "teardown"
```

## License

GPL-3.0-or-later

## Author

Frank Muise (@effectivelywild)
