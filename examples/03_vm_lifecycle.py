"""Create, start, stop, and delete a QEMU VM."""

import time

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

NODE = "pve1"
node = api.nodes(NODE)


def wait_for_task(upid: str, poll_interval: float = 2.0) -> None:
    """Poll until a task completes."""
    while True:
        task = node.task_status(upid)
        if task["status"] == "stopped":
            if task.get("exitstatus") != "OK":
                raise RuntimeError(f"Task failed: {task.get('exitstatus')}")
            print(f"  Task complete: {upid}")
            return
        time.sleep(poll_interval)


# Get the next available VMID
vmid = int(api.cluster.nextid())
print(f"Creating VM {vmid}...")

# Create a minimal VM
upid = node.qemu.create(
    vmid=vmid,
    name="test-vm",
    memory=2048,
    cores=2,
    sockets=1,
    net0="virtio,bridge=vmbr0",
    scsihw="virtio-scsi-single",
    scsi0="local-lvm:10",
    ostype="l26",
)
wait_for_task(upid)

# Start the VM
print(f"Starting VM {vmid}...")
upid = node.qemu(vmid).start()
wait_for_task(upid)

# Check status
status = node.qemu(vmid).status()
print(f"VM {vmid} status: {status['status']}")

# Stop the VM
print(f"Stopping VM {vmid}...")
upid = node.qemu(vmid).stop()
wait_for_task(upid)

# Delete the VM
print(f"Deleting VM {vmid}...")
upid = node.qemu(vmid).delete()
wait_for_task(upid)

print("Done.")
