"""Bulk operations: start/stop all VMs, find VMs by name, migrate."""

import time

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)


def wait_for_task(node, upid: str) -> None:
    while True:
        task = node.task_status(upid)
        if task["status"] == "stopped":
            if task.get("exitstatus") != "OK":
                raise RuntimeError(f"Task failed: {task.get('exitstatus')}")
            return
        time.sleep(2)


# --- Find VMs by name pattern ---
def find_vms(pattern: str) -> list[dict]:
    """Search all nodes for VMs matching a name pattern."""
    matches = []
    for res in api.cluster.resources(type="vm"):
        name = res.get("name", "")
        if pattern.lower() in name.lower():
            matches.append(res)
    return matches


print("=== Find VMs containing 'web' ===")
for vm in find_vms("web"):
    print(f"  {vm['vmid']} {vm.get('name', '?')} on {vm['node']} ({vm['status']})")


# --- Start all stopped VMs on a node ---
def start_all_vms(node_name: str) -> None:
    node = api.nodes(node_name)
    vms = node.qemu.list()
    stopped = [v for v in vms if v["status"] == "stopped"]

    if not stopped:
        print(f"No stopped VMs on {node_name}")
        return

    print(f"Starting {len(stopped)} VMs on {node_name}...")
    for vm_info in stopped:
        vmid = vm_info["vmid"]
        name = vm_info.get("name", "unnamed")
        upid = node.qemu(vmid).start()
        print(f"  Starting {vmid} ({name})... task={upid}")


# --- Gracefully shutdown all VMs on a node ---
def shutdown_all_vms(node_name: str, timeout: int = 120) -> None:
    node = api.nodes(node_name)
    vms = node.qemu.list()
    running = [v for v in vms if v["status"] == "running"]

    if not running:
        print(f"No running VMs on {node_name}")
        return

    print(f"Shutting down {len(running)} VMs on {node_name}...")
    tasks = []
    for vm_info in running:
        vmid = vm_info["vmid"]
        name = vm_info.get("name", "unnamed")
        upid = node.qemu(vmid).shutdown(timeout=timeout)
        tasks.append((vmid, name, upid))
        print(f"  Shutdown {vmid} ({name})... task={upid}")

    # Wait for all shutdowns to complete
    for vmid, name, upid in tasks:
        wait_for_task(node, upid)
        print(f"  {vmid} ({name}) is now stopped")


# --- Migrate a VM to another node ---
def migrate_vm(source_node: str, vmid: int, target_node: str, online: bool = True) -> None:
    node = api.nodes(source_node)
    vm = node.qemu(vmid)
    name = vm.config().get("name", "unnamed")

    print(f"Migrating {vmid} ({name}) from {source_node} to {target_node}...")
    upid = vm.migrate(target=target_node, online=1 if online else 0)
    wait_for_task(node, upid)
    print(f"  Migration complete.")


# Uncomment to run:
# start_all_vms("pve1")
# shutdown_all_vms("pve1")
# migrate_vm("pve1", 100, "pve2", online=True)
