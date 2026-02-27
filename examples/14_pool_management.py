"""Manage resource pools to organize VMs, containers, and storage."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

# --- List existing pools ---

for pool in api.pools.list():
    print(f"Pool: {pool['poolid']}  Comment: {pool.get('comment', '')}")

# --- Create a pool ---

api.pools.create(poolid="production", comment="Production workloads")
api.pools.create(poolid="staging", comment="Staging / QA environment")
print("Created production and staging pools.")

# --- Add members to a pool ---

# Add VMs and storage to the production pool
api.pools.update(
    poolid="production",
    vms="100,101,102",
    storage="local-lvm",
)

# --- Inspect pool contents ---

pool = api.pools.get("production")
print(f"\nPool '{pool['poolid']}' members:")
for member in pool.get("members", []):
    print(f"  {member['type']}: {member['id']}  Node: {member.get('node', 'N/A')}")

# --- Remove a member from a pool ---

# Use the delete flag to remove specific members instead of adding
api.pools.update(poolid="production", vms="102", delete=True)
print("Removed VM 102 from production pool.")

# --- Cleanup ---
api.pools.delete("staging")
api.pools.delete("production")
print("Pools deleted.")
