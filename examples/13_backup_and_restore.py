"""Schedule backups and restore a VM from a backup."""

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


# --- Scheduled backup jobs (cluster-wide) ---

# List existing backup jobs
for job in api.cluster.backup.list():
    print(f"Backup job: {job['id']}  Schedule: {job.get('schedule', 'N/A')}")

# Create a nightly backup job for specific VMs
api.cluster.backup.create(
    vmid="100,101,102",
    storage="nfs-backup",
    schedule="0 2 * * *",  # daily at 2 AM
    mode="snapshot",
    compress="zstd",
    mailnotification="failure",
    notes_template="{{guestname}} backup",
)
print("Nightly backup job created.")

# Check which guests are NOT covered by any backup job
not_backed = api.cluster.backup_info.not_backed_up()
for guest in not_backed:
    print(f"  Not backed up: VMID {guest['vmid']} ({guest.get('name', '?')})")

# --- On-demand backup of a single VM ---

VMID = 100
print(f"\nBacking up VM {VMID}...")
upid = node.vzdump(
    vmid=VMID,
    storage="local",
    mode="snapshot",
    compress="zstd",
)
wait_for_task(upid)

# --- Restore a VM from backup ---

# Find the most recent backup for a VM
backups = node.storage_content("local", content="backup", vmid=VMID)
if backups:
    latest = sorted(backups, key=lambda b: b.get("ctime", 0))[-1]
    volid = latest["volid"]
    print(f"Latest backup: {volid}")

    # Extract the original config from the backup
    config = node.vzdump_extractconfig(volume=volid)
    print(f"Original VM name: extracted from backup config")

    # Restore to a new VMID
    new_vmid = int(api.cluster.nextid())
    print(f"Restoring to new VM {new_vmid}...")
    upid = node.qemu.create(vmid=new_vmid, archive=volid, storage="local-lvm")
    wait_for_task(upid)
    print(f"VM {new_vmid} restored successfully.")
