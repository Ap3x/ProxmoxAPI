"""Manage firewall rules at the cluster, node, and VM level."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

NODE = "pve1"
VMID = 100

# --- Cluster-level firewall ---
print("=== Cluster Firewall Options ===")
opts = api.cluster.firewall.options()
print(f"  Enabled: {opts.get('enable', 0)}")
print(f"  Policy IN:  {opts.get('policy_in', '?')}")
print(f"  Policy OUT: {opts.get('policy_out', '?')}")

print("\nCluster firewall rules:")
for rule in api.cluster.firewall.list_rules():
    action = rule.get("action", "?")
    rtype = rule.get("type", "?")
    comment = rule.get("comment", "")
    enable = rule.get("enable", 0)
    print(f"  [{rule.get('pos')}] {rtype} {action}  enabled={enable}  {comment}")

# --- Node-level firewall ---
print(f"\n=== Node {NODE} Firewall Rules ===")
for rule in api.nodes(NODE).firewall.list_rules():
    pos = rule.get("pos", "?")
    action = rule.get("action", "?")
    rtype = rule.get("type", "?")
    source = rule.get("source", "any")
    dest = rule.get("dest", "any")
    dport = rule.get("dport", "any")
    proto = rule.get("proto", "any")
    print(f"  [{pos}] {rtype} {action}  {proto} {source} -> {dest}:{dport}")

# --- VM-level firewall ---
vm_fw = api.nodes(NODE).qemu(VMID).firewall
print(f"\n=== VM {VMID} Firewall ===")
vm_opts = vm_fw.options()
print(f"  Enabled: {vm_opts.get('enable', 0)}")

print(f"\nVM {VMID} firewall rules:")
for rule in vm_fw.list_rules():
    pos = rule.get("pos", "?")
    action = rule.get("action", "?")
    rtype = rule.get("type", "?")
    comment = rule.get("comment", "")
    print(f"  [{pos}] {rtype} {action}  {comment}")

# --- Add a rule to allow SSH on the VM ---
print(f"\nAdding SSH allow rule to VM {VMID}...")
vm_fw.create_rule(
    type="in",
    action="ACCEPT",
    proto="tcp",
    dport="22",
    comment="Allow SSH",
    enable=1,
)

# Verify it was added
rules = vm_fw.list_rules()
print(f"VM {VMID} now has {len(rules)} firewall rule(s)")
