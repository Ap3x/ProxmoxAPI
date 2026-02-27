# Proxmox API

[![Tests](https://github.com/Ap3x/ProxmoxAPI/actions/workflows/tests.yml/badge.svg)](https://github.com/Ap3x/ProxmoxAPI/actions/workflows/tests.yml)
[![Docs](https://github.com/Ap3x/ProxmoxAPI/actions/workflows/docs.yml/badge.svg)](https://github.com/Ap3x/ProxmoxAPI/actions/workflows/docs.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/Ap3x/ProxmoxAPI)](https://github.com/Ap3x/ProxmoxAPI/blob/main/LICENSE)

A Python wrapper around the Proxmox VE REST API, auto-generated from the official `apidoc.json` documentation.

## Features

- **Full API coverage** — 646 endpoints across cluster, nodes, storage, access, pools, and version
- **Fluent interface** — chainable accessors like `api.nodes("pve1").qemu(100).start()`
- **Two auth methods** — API token or username/password
- **apidoc parser** — CLI tool to inspect and analyze the Proxmox API schema

## Installation

```bash
pip install proxmox_api
```

Or install from source for development:

```bash
git clone https://github.com/your-username/ProxmoxAPI.git
cd ProxmoxAPI
pip install -e ".[dev]"
```

## Quick Start

### API Token Authentication

```python
from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)
```

### Password Authentication

```python
api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    password="secret",
)
```

### Common Operations

```python
# Cluster
api.version()
api.cluster.status()
api.cluster.resources(type="vm")
api.cluster.nextid()

# Nodes
api.nodes.list()
node = api.nodes("pve1")
node.status()
node.tasks()
node.services()

# QEMU VMs
node.qemu.list()
vm = node.qemu(100)
vm.config()
vm.start()
vm.stop()
vm.shutdown()
vm.reboot()
vm.clone(newid=101, name="my-clone")
vm.resize(disk="scsi0", size="+10G")
vm.snapshot.create("before-update")
vm.snapshot.rollback("before-update")
vm.agent.get_osinfo()
vm.agent.exec("ls /tmp")

# LXC Containers
node.lxc.list()
ct = node.lxc(200)
ct.config()
ct.start()
ct.stop()
ct.clone(newid=201)

# Storage
api.storage.list()
api.storage.get("local-lvm")
node.list_storage()
node.storage_content("local")

# Access Control
api.access.list_users()
api.access.list_roles()
api.access.acl()

# Pools
api.pools.list()
api.pools.create("dev-pool", comment="Development VMs")

# Firewall (cluster, node, or VM level)
api.cluster.firewall.list_rules()
node.firewall.list_rules()
vm.firewall.list_rules()

# Disks
node.disks.list()
node.disks.smart("/dev/sda")
```

### Raw Requests

For endpoints not covered by the wrapper, use the HTTP helpers directly:

```python
api.get("/nodes/pve1/ceph/status")
api.post("/nodes/pve1/qemu", vmid=999, memory=4096, cores=2)
api.put("/cluster/options", keyboard="en-us")
api.delete("/pools/old-pool")
```

## Examples

The [examples/](examples/) directory contains runnable scripts covering common use cases:

| # | Script | Description |
|---|--------|-------------|
| 01 | `01_connect.py` | Connect and print cluster info |
| 02 | `02_list_vms.py` | List VMs and containers across nodes |
| 03 | `03_vm_lifecycle.py` | Create, start, stop, and delete a VM |
| 04 | `04_snapshots.py` | Snapshot management (create, rollback, delete) |
| 05 | `05_cluster_resources.py` | Cluster status and resource usage |
| 06 | `06_lxc_container.py` | LXC container lifecycle |
| 07 | `07_node_management.py` | Node status, DNS, network, services, tasks |
| 08 | `08_guest_agent.py` | Guest agent interaction (exec, file ops, OS info) |
| 09 | `09_bulk_operations.py` | Find VMs by name, bulk start/stop, migration |
| 10 | `10_firewall.py` | Firewall rules at cluster, node, and VM levels |
| 11 | `11_storage_management.py` | Storage definitions, usage, ISOs, downloads |
| 12 | `12_user_management.py` | Users, groups, roles, ACLs, API tokens |
| 13 | `13_backup_and_restore.py` | Scheduled backups, on-demand backup, restore |
| 14 | `14_pool_management.py` | Resource pools for organizing VMs and storage |
| 15 | `15_cloud_init.py` | Cloud-init VM from template with SSH keys and networking |
| 16 | `16_disk_management.py` | Physical disks, SMART, LVM/ZFS, storage scanning |
| 17 | `17_ha_management.py` | High Availability groups, failover, migration |

## Proxmox API Doc Parser

Inspect the Proxmox API schema from the command line:

```bash
parse-apidoc apidoc.json
```

Or use it programmatically:

```python
from proxmox_api.parse_apidoc import parse_apidoc, group_by_section

endpoints = parse_apidoc("apidoc.json")
groups = group_by_section(endpoints)

for ep in groups["nodes"]:
    print(f"{ep.method:6s} {ep.path}")
    for p in ep.required_params:
        print(f"  {p.name} ({p.python_type}) - {p.description}")
```

## Configuration Options

| Parameter      | Default | Description                          |
|----------------|---------|--------------------------------------|
| `host`         | —       | Proxmox host IP or hostname          |
| `user`         | —       | User (e.g. `root@pam`)              |
| `password`     | `None`  | Password (for ticket auth)           |
| `token_name`   | `None`  | API token name                       |
| `token_value`  | `None`  | API token value                      |
| `port`         | `8006`  | API port                             |
| `verify_ssl`   | `False` | Verify SSL certificates              |
| `timeout`      | `30`    | Request timeout in seconds           |

## Running Tests

```bash
pytest tests/ -v
```

## License

See [LICENSE](LICENSE) for details.
