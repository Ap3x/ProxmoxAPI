"""Inspect and manage disks on a Proxmox node."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

NODE = "pve1"
node = api.nodes(NODE)

# --- List physical disks ---

print("Physical disks:")
for disk in node.disks.list():
    size_gb = disk.get("size", 0) / (1024**3)
    print(
        f"  {disk['devpath']}  "
        f"Size: {size_gb:.0f} GB  "
        f"Type: {disk.get('type', '?')}  "
        f"Used: {disk.get('used', 'unused')}"
    )

# --- Check SMART health ---

print("\nSMART status for /dev/sda:")
smart = node.disks.smart("/dev/sda")
print(f"  Health: {smart.get('health', 'unknown')}")
for attr in smart.get("attributes", []):
    print(f"  {attr['name']}: {attr['raw']}")

# --- LVM management ---

print("\nLVM volume groups:")
for vg in node.disks.lvm():
    print(f"  VG: {vg['name']}  Size: {vg.get('size', 'N/A')}")

print("\nLVM thin pools:")
for tp in node.disks.lvmthin():
    print(f"  Pool: {tp['lv']}  VG: {tp['vg']}  Usage: {tp.get('usage', 'N/A')}")

# --- ZFS pools ---

print("\nZFS pools:")
for pool in node.disks.zfs():
    print(f"  Pool: {pool['name']}  Health: {pool.get('health', '?')}")

# --- Scan for available storage backends ---

print("\nScanning for NFS exports on 10.0.0.5:")
for export in node.scan.nfs("10.0.0.5"):
    print(f"  {export['path']}  Options: {export.get('options', '')}")

print("\nScanning for iSCSI targets on 10.0.0.10:")
for target in node.scan.iscsi("10.0.0.10"):
    print(f"  {target['target']}")
