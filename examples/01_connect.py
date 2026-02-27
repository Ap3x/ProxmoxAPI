"""Connect to a Proxmox instance and print basic info."""

from proxmox_api import ProxmoxAPI

# --- Token authentication (recommended) ---
api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

# --- OR password authentication ---
# api = ProxmoxAPI(
#     "192.168.1.100",
#     user="root@pam",
#     password="your-password",
# )

# Print Proxmox version
version = api.version()
print(f"Proxmox VE {version['version']} (release {version['release']})")

# List all nodes in the cluster
nodes = api.nodes.list()
for node in nodes:
    print(f"  Node: {node['node']}  Status: {node['status']}")
