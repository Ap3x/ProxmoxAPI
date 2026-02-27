"""Configure High Availability for VMs and containers."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

# --- Check HA status ---

status = api.cluster.ha.status()
print("HA Manager status:")
for entry in status:
    print(f"  {entry.get('type', '?')}: {entry.get('status', 'N/A')}")

manager = api.cluster.ha.manager_status()
print(f"Manager state: {manager.get('manager_status', 'unknown')}")

# --- HA Groups (define preferred/failover nodes) ---

# Create an HA group that prefers pve1 and pve2
api.cluster.ha.create_group(
    group="web-group",
    nodes="pve1:2,pve2:1",  # pve1 has priority 2 (higher = preferred)
    nofailback=False,
    comment="Web server failover group",
)
print("Created HA group 'web-group'.")

# List HA groups
for group in api.cluster.ha.list_groups():
    print(f"  Group: {group['group']}  Nodes: {group.get('nodes', '')}")

# --- Add VMs to HA ---

# Add VM 100 as an HA-managed resource
api.cluster.ha.create_resource(
    sid="vm:100",
    group="web-group",
    max_restart=3,
    max_relocate=2,
    state="started",
    comment="Primary web server",
)
print("VM 100 added to HA.")

# Add a container
api.cluster.ha.create_resource(
    sid="ct:200",
    group="web-group",
    state="started",
    comment="Load balancer",
)
print("CT 200 added to HA.")

# --- List HA resources ---

print("\nHA resources:")
for res in api.cluster.ha.list_resources():
    print(
        f"  {res['sid']}  "
        f"State: {res.get('state', '?')}  "
        f"Group: {res.get('group', 'none')}  "
        f"Status: {res.get('status', 'N/A')}"
    )

# --- Migrate an HA resource to a specific node ---

api.cluster.ha.migrate_resource("vm:100", node="pve2")
print("Requested HA migration of VM 100 to pve2.")

# --- Cleanup ---
api.cluster.ha.delete_resource("ct:200")
api.cluster.ha.delete_resource("vm:100")
api.cluster.ha.delete_group("web-group")
print("HA resources and group removed.")
