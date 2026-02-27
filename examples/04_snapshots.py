"""Manage VM snapshots: create, list, rollback, and delete."""

import time

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

NODE = "pve1"
VMID = 100

vm = api.nodes(NODE).qemu(VMID)
node = api.nodes(NODE)


def wait_for_task(upid: str) -> None:
    while True:
        task = node.task_status(upid)
        if task["status"] == "stopped":
            if task.get("exitstatus") != "OK":
                raise RuntimeError(f"Task failed: {task.get('exitstatus')}")
            return
        time.sleep(2)


# List existing snapshots
print("Current snapshots:")
for snap in vm.snapshot.list():
    name = snap["name"]
    desc = snap.get("description", "")
    if name == "current":
        continue
    print(f"  {name}: {desc}")

# Create a new snapshot
SNAP_NAME = "before-upgrade"
print(f"\nCreating snapshot '{SNAP_NAME}'...")
upid = vm.snapshot.create(SNAP_NAME, description="Snapshot before system upgrade")
wait_for_task(upid)

# Read snapshot config
config = vm.snapshot.get_config(SNAP_NAME)
print(f"Snapshot config: {config}")

# Rollback to snapshot
print(f"\nRolling back to '{SNAP_NAME}'...")
upid = vm.snapshot.rollback(SNAP_NAME)
wait_for_task(upid)

# Delete the snapshot
print(f"\nDeleting snapshot '{SNAP_NAME}'...")
upid = vm.snapshot.delete(SNAP_NAME)
wait_for_task(upid)

print("Done.")
