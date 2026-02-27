"""Node-level operations: services, networking, storage, and tasks."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

NODE = "pve1"
node = api.nodes(NODE)

# --- Node status ---
print("=== Node Status ===")
status = node.status()
cpu_info = status.get("cpuinfo", {})
mem = status.get("memory", {})
print(f"CPU:    {cpu_info.get('model', '?')} ({cpu_info.get('cores', '?')} cores)")
print(f"Memory: {mem.get('used', 0) / (1024**3):.1f} / {mem.get('total', 0) / (1024**3):.1f} GB")
print(f"Uptime: {status.get('uptime', 0) / 3600:.1f} hours")
print(f"Kernel: {status.get('kversion', '?')}")

# --- DNS ---
print("\n=== DNS ===")
dns = node.dns()
print(f"Search domain: {dns.get('search', '?')}")
print(f"DNS1: {dns.get('dns1', '?')}")
print(f"DNS2: {dns.get('dns2', 'not set')}")

# --- Network interfaces ---
print("\n=== Network Interfaces ===")
for iface in node.network():
    name = iface.get("iface", "?")
    itype = iface.get("type", "?")
    addr = iface.get("address", "")
    active = iface.get("active", 0)
    print(f"  {name:<12} type={itype:<10} addr={addr or 'none':<18} active={active}")

# --- Services ---
print("\n=== Services ===")
for svc in node.services():
    name = svc.get("name", svc.get("service", "?"))
    state = svc.get("state", "?")
    desc = svc.get("desc", "")
    print(f"  {name:<25} {state:<10} {desc}")

# --- Storage ---
print("\n=== Node Storage ===")
for store in node.list_storage():
    name = store.get("storage", "?")
    stype = store.get("type", "?")
    total_gb = store.get("total", 0) / (1024**3)
    used_gb = store.get("used", 0) / (1024**3)
    pct = (used_gb / total_gb * 100) if total_gb > 0 else 0
    print(f"  {name:<20} {stype:<10} {used_gb:.1f}/{total_gb:.1f} GB ({pct:.0f}%)")

# --- Recent tasks ---
print("\n=== Recent Tasks (last 10) ===")
tasks = node.tasks()
for task in tasks[:10]:
    status = task.get("status", "?")
    ttype = task.get("type", "?")
    user = task.get("user", "?")
    starttime = task.get("starttime", "?")
    print(f"  {ttype:<20} {status:<10} user={user}  started={starttime}")
