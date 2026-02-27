"""Create and manage an LXC container."""

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


def wait_for_task(upid: str) -> None:
    while True:
        task = node.task_status(upid)
        if task["status"] == "stopped":
            if task.get("exitstatus") != "OK":
                raise RuntimeError(f"Task failed: {task.get('exitstatus')}")
            return
        time.sleep(2)


# Create an LXC container
vmid = int(api.cluster.nextid())
print(f"Creating LXC container {vmid}...")

upid = node.lxc.create(
    vmid=vmid,
    ostemplate="local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst",
    hostname="test-ct",
    memory=512,
    swap=512,
    cores=1,
    rootfs="local-lvm:8",
    net0="name=eth0,bridge=vmbr0,ip=dhcp",
    password="changeme",
    unprivileged=1,
    start=0,
)
wait_for_task(upid)

ct = node.lxc(vmid)

# Show container config
config = ct.config()
print(f"Hostname: {config.get('hostname')}")
print(f"Memory:   {config.get('memory')} MB")
print(f"Cores:    {config.get('cores')}")

# Start the container
print(f"\nStarting container {vmid}...")
upid = ct.start()
wait_for_task(upid)

status = ct.status()
print(f"Status: {status['status']}")
print(f"PID:    {status.get('pid')}")
print(f"Uptime: {status.get('uptime')}s")

# Stop and delete
print(f"\nStopping container {vmid}...")
upid = ct.stop()
wait_for_task(upid)

print(f"Deleting container {vmid}...")
upid = ct.delete()
wait_for_task(upid)

print("Done.")
