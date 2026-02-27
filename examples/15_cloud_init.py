"""Create a cloud-init enabled VM from a cloud image template."""

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


# Assume VM 9000 is a cloud image template (e.g. Ubuntu cloud image)
TEMPLATE_VMID = 9000
vmid = int(api.cluster.nextid())

# Clone the template
print(f"Cloning template {TEMPLATE_VMID} → VM {vmid}...")
upid = node.qemu(TEMPLATE_VMID).clone(
    newid=vmid,
    name="web-server-01",
    full=True,
    storage="local-lvm",
)
wait_for_task(upid)

vm = node.qemu(vmid)

# Configure cloud-init settings
vm.set_config(
    ciuser="deploy",
    cipassword="changeme",
    sshkeys="ssh-ed25519 AAAA... deploy@workstation",
    ipconfig0="ip=10.0.0.50/24,gw=10.0.0.1",
    nameserver="1.1.1.1 8.8.8.8",
    searchdomain="example.com",
)

# Resize the disk to give the VM more space
vm.resize(disk="scsi0", size="+18G")
print(f"VM {vmid} disk resized to template + 18 GB")

# Regenerate the cloud-init drive with the new settings
vm.regenerate_cloudinit()

# Verify cloud-init config
ci_config = vm.cloudinit()
print(f"Cloud-init user: {ci_config.get('ciuser', 'N/A')}")

# Start the VM
print(f"Starting VM {vmid}...")
upid = vm.start()
wait_for_task(upid)

print(f"VM {vmid} is running. Cloud-init will configure on first boot.")
