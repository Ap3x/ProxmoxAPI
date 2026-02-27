"""QEMU VM API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_api._base import _ResourceBase

if TYPE_CHECKING:
    from proxmox_api.client import ProxmoxAPI


class _QemuCollectionAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self.node = node
        self._base = f"/nodes/{node}/qemu"

    def list(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/qemu - List virtual machines."""
        return self._client.get(self._base, **kwargs)

    def create(self, vmid: int, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu - Create or restore a virtual machine."""
        return self._client.post(self._base, vmid=vmid, **kwargs)

    def __call__(self, vmid: int) -> _QemuVMAPI:
        """Select a specific VM: api.nodes('pve1').qemu(100)."""
        return _QemuVMAPI(self._client, self.node, vmid)


class _QemuVMAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str, vmid: int) -> None:
        super().__init__(client)
        self.node = node
        self.vmid = vmid
        self._base = f"/nodes/{node}/qemu/{vmid}"

    def index(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}"""
        return self._client.get(self._base)

    def status(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/status/current"""
        return self._client.get(f"{self._base}/status/current")

    def status_index(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/status"""
        return self._client.get(f"{self._base}/status")

    def config(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/config"""
        return self._client.get(f"{self._base}/config")

    def set_config(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/config (create pending changes)."""
        return self._client.post(f"{self._base}/config", **kwargs)

    def update_config(self, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/config (apply immediately)."""
        return self._client.put(f"{self._base}/config", **kwargs)

    def pending(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/pending"""
        return self._client.get(f"{self._base}/pending")

    def start(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/status/start"""
        return self._client.post(f"{self._base}/status/start", **kwargs)

    def stop(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/status/stop"""
        return self._client.post(f"{self._base}/status/stop", **kwargs)

    def shutdown(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/status/shutdown"""
        return self._client.post(f"{self._base}/status/shutdown", **kwargs)

    def reboot(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/status/reboot"""
        return self._client.post(f"{self._base}/status/reboot", **kwargs)

    def reset(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/status/reset"""
        return self._client.post(f"{self._base}/status/reset", **kwargs)

    def suspend(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/status/suspend"""
        return self._client.post(f"{self._base}/status/suspend", **kwargs)

    def resume(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/status/resume"""
        return self._client.post(f"{self._base}/status/resume", **kwargs)

    def delete(self, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/qemu/{vmid}"""
        return self._client.delete(self._base, **kwargs)

    def clone(self, newid: int, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/clone"""
        return self._client.post(f"{self._base}/clone", newid=newid, **kwargs)

    def migrate(self, target: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/migrate"""
        return self._client.post(
            f"{self._base}/migrate", target=target, **kwargs
        )

    def migrate_preconditions(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/migrate"""
        return self._client.get(f"{self._base}/migrate")

    def remote_migrate(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/remote_migrate"""
        return self._client.post(f"{self._base}/remote_migrate", **kwargs)

    def move_disk(self, disk: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/move_disk"""
        return self._client.post(
            f"{self._base}/move_disk", disk=disk, **kwargs
        )

    def resize(self, disk: str, size: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/resize"""
        return self._client.put(
            f"{self._base}/resize", disk=disk, size=size, **kwargs
        )

    def unlink(self, idlist: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/unlink"""
        return self._client.put(f"{self._base}/unlink", idlist=idlist, **kwargs)

    def template(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/template - Create a Template."""
        return self._client.post(f"{self._base}/template")

    def rrd(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/rrd"""
        return self._client.get(f"{self._base}/rrd", **kwargs)

    def rrddata(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/rrddata"""
        return self._client.get(f"{self._base}/rrddata", **kwargs)

    def vncproxy(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/vncproxy"""
        return self._client.post(f"{self._base}/vncproxy", **kwargs)

    def vncwebsocket(self, port: int, vncticket: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/vncwebsocket"""
        return self._client.get(
            f"{self._base}/vncwebsocket", port=port, vncticket=vncticket, **kwargs
        )

    def termproxy(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/termproxy"""
        return self._client.post(f"{self._base}/termproxy", **kwargs)

    def spiceproxy(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/spiceproxy"""
        return self._client.post(f"{self._base}/spiceproxy", **kwargs)

    def mtunnel(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/mtunnel"""
        return self._client.post(f"{self._base}/mtunnel", **kwargs)

    def mtunnelwebsocket(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/mtunnelwebsocket"""
        return self._client.get(f"{self._base}/mtunnelwebsocket", **kwargs)

    def sendkey(self, key: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/sendkey"""
        return self._client.put(f"{self._base}/sendkey", key=key, **kwargs)

    def feature(self, feature: str) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/feature"""
        return self._client.get(f"{self._base}/feature", feature=feature)

    def monitor(self, command: str) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/monitor"""
        return self._client.post(f"{self._base}/monitor", command=command)

    def dbus_vmstate(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/dbus-vmstate"""
        return self._client.post(f"{self._base}/dbus-vmstate", **kwargs)

    def cloudinit(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/cloudinit"""
        return self._client.get(f"{self._base}/cloudinit")

    def regenerate_cloudinit(self) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/cloudinit"""
        return self._client.put(f"{self._base}/cloudinit")

    def cloudinit_dump(self, type: str) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/cloudinit/dump"""
        return self._client.get(f"{self._base}/cloudinit/dump", type=type)

    @property
    def snapshot(self) -> _QemuSnapshotAPI:
        return _QemuSnapshotAPI(self._client, self.node, self.vmid)

    @property
    def firewall(self) -> _QemuFirewallAPI:
        return _QemuFirewallAPI(self._client, self.node, self.vmid)

    @property
    def agent(self) -> _QemuAgentAPI:
        return _QemuAgentAPI(self._client, self.node, self.vmid)


class _QemuSnapshotAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str, vmid: int) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/qemu/{vmid}/snapshot"

    def list(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/snapshot"""
        return self._client.get(self._base)

    def create(self, snapname: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/snapshot"""
        return self._client.post(self._base, snapname=snapname, **kwargs)

    def get(self, snapname: str) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/snapshot/{snapname}"""
        return self._client.get(f"{self._base}/{snapname}")

    def get_config(self, snapname: str) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/snapshot/{snapname}/config"""
        return self._client.get(f"{self._base}/{snapname}/config")

    def update_config(self, snapname: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/snapshot/{snapname}/config"""
        return self._client.put(f"{self._base}/{snapname}/config", **kwargs)

    def rollback(self, snapname: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/snapshot/{snapname}/rollback"""
        return self._client.post(f"{self._base}/{snapname}/rollback", **kwargs)

    def delete(self, snapname: str, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/qemu/{vmid}/snapshot/{snapname}"""
        return self._client.delete(f"{self._base}/{snapname}", **kwargs)


class _QemuFirewallAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str, vmid: int) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/qemu/{vmid}/firewall"

    def index(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall"""
        return self._client.get(self._base)

    def list_rules(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/rules"""
        return self._client.get(f"{self._base}/rules")

    def get_rule(self, pos: int) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/rules/{pos}"""
        return self._client.get(f"{self._base}/rules/{pos}")

    def create_rule(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/firewall/rules"""
        return self._client.post(f"{self._base}/rules", **kwargs)

    def update_rule(self, pos: int, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/firewall/rules/{pos}"""
        return self._client.put(f"{self._base}/rules/{pos}", **kwargs)

    def delete_rule(self, pos: int) -> Any:
        """DELETE /nodes/{node}/qemu/{vmid}/firewall/rules/{pos}"""
        return self._client.delete(f"{self._base}/rules/{pos}")

    def list_aliases(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/aliases"""
        return self._client.get(f"{self._base}/aliases")

    def get_alias(self, name: str) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/aliases/{name}"""
        return self._client.get(f"{self._base}/aliases/{name}")

    def create_alias(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/firewall/aliases"""
        return self._client.post(
            f"{self._base}/aliases", name=name, cidr=cidr, **kwargs
        )

    def update_alias(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/firewall/aliases/{name}"""
        return self._client.put(
            f"{self._base}/aliases/{name}", cidr=cidr, **kwargs
        )

    def delete_alias(self, name: str) -> Any:
        """DELETE /nodes/{node}/qemu/{vmid}/firewall/aliases/{name}"""
        return self._client.delete(f"{self._base}/aliases/{name}")

    def list_ipset(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/ipset"""
        return self._client.get(f"{self._base}/ipset")

    def create_ipset(self, name: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/firewall/ipset"""
        return self._client.post(f"{self._base}/ipset", name=name, **kwargs)

    def get_ipset(self, name: str) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}"""
        return self._client.get(f"{self._base}/ipset/{name}")

    def delete_ipset(self, name: str) -> Any:
        """DELETE /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}"""
        return self._client.delete(f"{self._base}/ipset/{name}")

    def add_ipset_entry(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}"""
        return self._client.post(
            f"{self._base}/ipset/{name}", cidr=cidr, **kwargs
        )

    def get_ipset_entry(self, name: str, cidr: str) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}/{cidr}"""
        return self._client.get(f"{self._base}/ipset/{name}/{cidr}")

    def update_ipset_entry(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}/{cidr}"""
        return self._client.put(f"{self._base}/ipset/{name}/{cidr}", **kwargs)

    def delete_ipset_entry(self, name: str, cidr: str) -> Any:
        """DELETE /nodes/{node}/qemu/{vmid}/firewall/ipset/{name}/{cidr}"""
        return self._client.delete(f"{self._base}/ipset/{name}/{cidr}")

    def options(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/options"""
        return self._client.get(f"{self._base}/options")

    def set_options(self, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/qemu/{vmid}/firewall/options"""
        return self._client.put(f"{self._base}/options", **kwargs)

    def log(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/log"""
        return self._client.get(f"{self._base}/log", **kwargs)

    def refs(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/firewall/refs"""
        return self._client.get(f"{self._base}/refs", **kwargs)


class _QemuAgentAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str, vmid: int) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/qemu/{vmid}/agent"

    def index(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent"""
        return self._client.get(self._base)

    def post(self, command: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent"""
        return self._client.post(self._base, command=command, **kwargs)

    def exec(self, command: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/exec"""
        return self._client.post(f"{self._base}/exec", command=command, **kwargs)

    def exec_status(self, pid: int) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/exec-status"""
        return self._client.get(f"{self._base}/exec-status", pid=pid)

    def file_read(self, file: str) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/file-read"""
        return self._client.get(f"{self._base}/file-read", file=file)

    def file_write(self, file: str, content: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/file-write"""
        return self._client.post(
            f"{self._base}/file-write", file=file, content=content, **kwargs
        )

    def ping(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/ping"""
        return self._client.post(f"{self._base}/ping")

    def get_osinfo(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/get-osinfo"""
        return self._client.get(f"{self._base}/get-osinfo")

    def get_host_name(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/get-host-name"""
        return self._client.get(f"{self._base}/get-host-name")

    def get_time(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/get-time"""
        return self._client.get(f"{self._base}/get-time")

    def get_timezone(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/get-timezone"""
        return self._client.get(f"{self._base}/get-timezone")

    def get_users(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/get-users"""
        return self._client.get(f"{self._base}/get-users")

    def get_vcpus(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/get-vcpus"""
        return self._client.get(f"{self._base}/get-vcpus")

    def get_fsinfo(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/get-fsinfo"""
        return self._client.get(f"{self._base}/get-fsinfo")

    def get_memory_blocks(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/get-memory-blocks"""
        return self._client.get(f"{self._base}/get-memory-blocks")

    def get_memory_block_info(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/get-memory-block-info"""
        return self._client.get(f"{self._base}/get-memory-block-info")

    def network_get_interfaces(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/network-get-interfaces"""
        return self._client.get(f"{self._base}/network-get-interfaces")

    def info(self) -> Any:
        """GET /nodes/{node}/qemu/{vmid}/agent/info"""
        return self._client.get(f"{self._base}/info")

    def fsfreeze_freeze(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/fsfreeze-freeze"""
        return self._client.post(f"{self._base}/fsfreeze-freeze")

    def fsfreeze_thaw(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/fsfreeze-thaw"""
        return self._client.post(f"{self._base}/fsfreeze-thaw")

    def fsfreeze_status(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/fsfreeze-status"""
        return self._client.post(f"{self._base}/fsfreeze-status")

    def fstrim(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/fstrim"""
        return self._client.post(f"{self._base}/fstrim")

    def shutdown(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/shutdown"""
        return self._client.post(f"{self._base}/shutdown")

    def suspend_disk(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/suspend-disk"""
        return self._client.post(f"{self._base}/suspend-disk")

    def suspend_hybrid(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/suspend-hybrid"""
        return self._client.post(f"{self._base}/suspend-hybrid")

    def suspend_ram(self) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/suspend-ram"""
        return self._client.post(f"{self._base}/suspend-ram")

    def set_user_password(self, username: str, password: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/qemu/{vmid}/agent/set-user-password"""
        return self._client.post(
            f"{self._base}/set-user-password",
            username=username,
            password=password,
            **kwargs,
        )
