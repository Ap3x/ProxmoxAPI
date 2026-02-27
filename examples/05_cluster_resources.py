"""Query cluster-wide resources and display usage stats."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

# --- Cluster status ---
print("=== Cluster Status ===")
for entry in api.cluster.status():
    if entry["type"] == "cluster":
        print(f"Cluster: {entry['name']}  Nodes: {entry['nodes']}  Quorate: {entry['quorate']}")
    elif entry["type"] == "node":
        status = "online" if entry["online"] else "offline"
        print(f"  Node: {entry['name']}  Status: {status}")

# --- Resource usage by type ---
print("\n=== VM Summary ===")
vms = api.cluster.resources(type="vm")
running = [v for v in vms if v.get("status") == "running"]
stopped = [v for v in vms if v.get("status") == "stopped"]
print(f"Total VMs/CTs: {len(vms)}  Running: {len(running)}  Stopped: {len(stopped)}")

total_mem = sum(v.get("maxmem", 0) for v in vms)
used_mem = sum(v.get("mem", 0) for v in running)
print(f"Allocated memory: {total_mem / (1024**3):.1f} GB")
print(f"Used memory (running): {used_mem / (1024**3):.1f} GB")

# --- Storage usage ---
print("\n=== Storage ===")
storages = api.cluster.resources(type="storage")
for s in storages:
    name = s.get("storage", "?")
    node = s.get("node", "?")
    total_gb = s.get("maxdisk", 0) / (1024**3)
    used_gb = s.get("disk", 0) / (1024**3)
    pct = (used_gb / total_gb * 100) if total_gb > 0 else 0
    print(f"  {node}:{name:<20} {used_gb:.1f}/{total_gb:.1f} GB ({pct:.0f}%)")

# --- Node resource usage ---
print("\n=== Node Resources ===")
for node_info in api.cluster.resources(type="node"):
    name = node_info.get("node", "?")
    cpu = node_info.get("cpu", 0) * 100
    maxcpu = node_info.get("maxcpu", 0)
    mem_gb = node_info.get("mem", 0) / (1024**3)
    maxmem_gb = node_info.get("maxmem", 0) / (1024**3)
    uptime_h = node_info.get("uptime", 0) / 3600
    print(f"  {name}: CPU {cpu:.1f}% ({maxcpu} cores)  "
          f"RAM {mem_gb:.1f}/{maxmem_gb:.1f} GB  "
          f"Uptime {uptime_h:.0f}h")
