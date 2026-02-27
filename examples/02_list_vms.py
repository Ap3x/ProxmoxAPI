"""List all QEMU VMs and LXC containers across all nodes."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

for node_info in api.nodes.list():
    node_name = node_info["node"]
    node = api.nodes(node_name)
    print(f"\n=== {node_name} ===")

    # QEMU VMs
    vms = node.qemu.list()
    if vms:
        print("\n  QEMU Virtual Machines:")
        for vm in sorted(vms, key=lambda v: v["vmid"]):
            status = vm["status"]
            name = vm.get("name", "unnamed")
            mem_gb = vm.get("maxmem", 0) / (1024**3)
            cpus = vm.get("cpus", "?")
            print(f"    {vm['vmid']:>6}  {name:<30} {status:<10} {cpus} CPU  {mem_gb:.1f} GB RAM")

    # LXC Containers
    cts = node.lxc.list()
    if cts:
        print("\n  LXC Containers:")
        for ct in sorted(cts, key=lambda c: c["vmid"]):
            status = ct["status"]
            name = ct.get("name", "unnamed")
            mem_gb = ct.get("maxmem", 0) / (1024**3)
            cpus = ct.get("cpus", "?")
            print(f"    {ct['vmid']:>6}  {name:<30} {status:<10} {cpus} CPU  {mem_gb:.1f} GB RAM")
