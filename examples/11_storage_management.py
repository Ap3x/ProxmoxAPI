"""Manage datacenter-level and node-level storage."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

NODE = "pve1"
node = api.nodes(NODE)

# --- Datacenter-level storage definitions ---

# List all configured storage
for store in api.storage.list():
    print(f"Storage: {store['storage']}  Type: {store['type']}")

# Add an NFS storage
api.storage.create(
    storage="nfs-backup",
    type="nfs",
    server="10.0.0.5",
    export="/mnt/backups",
    content="backup,iso",
)

# Update storage to restrict to specific nodes
api.storage.update("nfs-backup", nodes="pve1,pve2")

# --- Node-level storage usage ---

# Check space on all storage available to a node
for store in node.list_storage():
    total = store.get("total", 0)
    used = store.get("used", 0)
    if total > 0:
        pct = used / total * 100
        print(f"  {store['storage']}: {pct:.1f}% used")

# List contents (ISOs, disk images, etc.) of a specific storage
for vol in node.storage_content("local", content="iso"):
    print(f"  ISO: {vol['volid']}  Size: {vol.get('size', 'N/A')}")

# Download an ISO from a URL to node storage
upid = node.storage_download_url(
    storage="local",
    url="https://releases.ubuntu.com/24.04/ubuntu-24.04-live-server-amd64.iso",
    filename="ubuntu-24.04-server.iso",
    content="iso",
)
print(f"Download started: {upid}")

# --- Cleanup ---
api.storage.delete("nfs-backup")
print("Removed nfs-backup storage definition.")
