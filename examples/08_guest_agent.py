"""Interact with a running VM via the QEMU guest agent."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

NODE = "pve1"
VMID = 100

agent = api.nodes(NODE).qemu(VMID).agent

# Check if guest agent is responsive
try:
    agent.ping()
    print("Guest agent is running.")
except Exception as e:
    print(f"Guest agent not available: {e}")
    exit(1)

# OS information
osinfo = agent.get_osinfo()
print(f"\nOS: {osinfo.get('pretty-name', osinfo.get('name', '?'))}")
print(f"Kernel: {osinfo.get('kernel-release', '?')}")
print(f"Machine: {osinfo.get('machine', '?')}")

# Hostname
hostname = agent.get_host_name()
print(f"Hostname: {hostname.get('host-name', '?')}")

# Network interfaces
print("\nNetwork interfaces:")
interfaces = agent.network_get_interfaces()
for iface in interfaces:
    name = iface.get("name", "?")
    hwaddr = iface.get("hardware-address", "")
    ips = iface.get("ip-addresses", [])
    print(f"  {name} ({hwaddr})")
    for ip in ips:
        print(f"    {ip['ip-address-type']}: {ip['ip-address']}/{ip['prefix']}")

# Filesystem info
print("\nFilesystems:")
fsinfo = agent.get_fsinfo()
for fs in fsinfo:
    mount = fs.get("mountpoint", "?")
    fstype = fs.get("type", "?")
    total_gb = fs.get("total-bytes", 0) / (1024**3)
    used_gb = fs.get("used-bytes", 0) / (1024**3)
    print(f"  {mount:<20} {fstype:<10} {used_gb:.1f}/{total_gb:.1f} GB")

# Execute a command
print("\nRunning 'uptime':")
result = agent.exec("uptime")
pid = result.get("pid")
if pid is not None:
    import time
    time.sleep(2)
    output = agent.exec_status(pid)
    print(f"  {output.get('out-data', '').strip()}")

# Read a file
print("\nReading /etc/hostname:")
content = agent.file_read("/etc/hostname")
print(f"  {content.get('content', '').strip()}")
