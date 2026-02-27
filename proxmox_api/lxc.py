"""LXC container API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_api._base import _ResourceBase

if TYPE_CHECKING:
    from proxmox_api.client import ProxmoxAPI


class _LxcCollectionAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self.node = node
        self._base = f"/nodes/{node}/lxc"

    def list(self) -> Any:
        """GET /nodes/{node}/lxc - List LXC containers."""
        return self._client.get(self._base)

    def create(self, vmid: int, ostemplate: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc - Create or restore a container."""
        return self._client.post(
            self._base, vmid=vmid, ostemplate=ostemplate, **kwargs
        )

    def __call__(self, vmid: int) -> _LxcContainerAPI:
        """Select a specific container: api.nodes('pve1').lxc(100)."""
        return _LxcContainerAPI(self._client, self.node, vmid)


class _LxcContainerAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str, vmid: int) -> None:
        super().__init__(client)
        self.node = node
        self.vmid = vmid
        self._base = f"/nodes/{node}/lxc/{vmid}"

    def index(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}"""
        return self._client.get(self._base)

    def status(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/status/current"""
        return self._client.get(f"{self._base}/status/current")

    def status_index(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/status"""
        return self._client.get(f"{self._base}/status")

    def config(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/config"""
        return self._client.get(f"{self._base}/config")

    def update_config(self, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/lxc/{vmid}/config"""
        return self._client.put(f"{self._base}/config", **kwargs)

    def pending(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/pending"""
        return self._client.get(f"{self._base}/pending")

    def start(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/status/start"""
        return self._client.post(f"{self._base}/status/start", **kwargs)

    def stop(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/status/stop"""
        return self._client.post(f"{self._base}/status/stop", **kwargs)

    def shutdown(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/status/shutdown"""
        return self._client.post(f"{self._base}/status/shutdown", **kwargs)

    def reboot(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/status/reboot"""
        return self._client.post(f"{self._base}/status/reboot", **kwargs)

    def suspend(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/status/suspend"""
        return self._client.post(f"{self._base}/status/suspend", **kwargs)

    def resume(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/status/resume"""
        return self._client.post(f"{self._base}/status/resume", **kwargs)

    def delete(self, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/lxc/{vmid}"""
        return self._client.delete(self._base, **kwargs)

    def clone(self, newid: int, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/clone"""
        return self._client.post(f"{self._base}/clone", newid=newid, **kwargs)

    def migrate(self, target: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/migrate"""
        return self._client.post(
            f"{self._base}/migrate", target=target, **kwargs
        )

    def migrate_preconditions(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/migrate"""
        return self._client.get(f"{self._base}/migrate")

    def remote_migrate(self, target: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/remote_migrate"""
        return self._client.post(
            f"{self._base}/remote_migrate", target=target, **kwargs
        )

    def move_volume(self, volume: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/move_volume"""
        return self._client.post(
            f"{self._base}/move_volume", volume=volume, **kwargs
        )

    def resize(self, disk: str, size: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/lxc/{vmid}/resize"""
        return self._client.put(
            f"{self._base}/resize", disk=disk, size=size, **kwargs
        )

    def feature(self, feature: str) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/feature"""
        return self._client.get(f"{self._base}/feature", feature=feature)

    def template(self) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/template"""
        return self._client.post(f"{self._base}/template")

    def interfaces(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/interfaces"""
        return self._client.get(f"{self._base}/interfaces")

    def vncproxy(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/vncproxy"""
        return self._client.post(f"{self._base}/vncproxy", **kwargs)

    def vncwebsocket(self, port: int, vncticket: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/vncwebsocket"""
        return self._client.get(
            f"{self._base}/vncwebsocket", port=port, vncticket=vncticket, **kwargs
        )

    def termproxy(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/termproxy"""
        return self._client.post(f"{self._base}/termproxy", **kwargs)

    def spiceproxy(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/spiceproxy"""
        return self._client.post(f"{self._base}/spiceproxy", **kwargs)

    def mtunnel(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/mtunnel"""
        return self._client.post(f"{self._base}/mtunnel", **kwargs)

    def mtunnelwebsocket(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/mtunnelwebsocket"""
        return self._client.get(f"{self._base}/mtunnelwebsocket", **kwargs)

    def rrd(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/rrd"""
        return self._client.get(f"{self._base}/rrd", **kwargs)

    def rrddata(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/rrddata"""
        return self._client.get(f"{self._base}/rrddata", **kwargs)

    @property
    def snapshot(self) -> _LxcSnapshotAPI:
        return _LxcSnapshotAPI(self._client, self.node, self.vmid)

    @property
    def firewall(self) -> _LxcFirewallAPI:
        return _LxcFirewallAPI(self._client, self.node, self.vmid)


class _LxcSnapshotAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str, vmid: int) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/lxc/{vmid}/snapshot"

    def list(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/snapshot"""
        return self._client.get(self._base)

    def create(self, snapname: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/snapshot"""
        return self._client.post(self._base, snapname=snapname, **kwargs)

    def get(self, snapname: str) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/snapshot/{snapname}"""
        return self._client.get(f"{self._base}/{snapname}")

    def get_config(self, snapname: str) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/config"""
        return self._client.get(f"{self._base}/{snapname}/config")

    def update_config(self, snapname: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/config"""
        return self._client.put(f"{self._base}/{snapname}/config", **kwargs)

    def rollback(self, snapname: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/snapshot/{snapname}/rollback"""
        return self._client.post(f"{self._base}/{snapname}/rollback", **kwargs)

    def delete(self, snapname: str, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/lxc/{vmid}/snapshot/{snapname}"""
        return self._client.delete(f"{self._base}/{snapname}", **kwargs)


class _LxcFirewallAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str, vmid: int) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/lxc/{vmid}/firewall"

    def index(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall"""
        return self._client.get(self._base)

    def list_rules(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/rules"""
        return self._client.get(f"{self._base}/rules")

    def get_rule(self, pos: int) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/rules/{pos}"""
        return self._client.get(f"{self._base}/rules/{pos}")

    def create_rule(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/firewall/rules"""
        return self._client.post(f"{self._base}/rules", **kwargs)

    def update_rule(self, pos: int, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/lxc/{vmid}/firewall/rules/{pos}"""
        return self._client.put(f"{self._base}/rules/{pos}", **kwargs)

    def delete_rule(self, pos: int) -> Any:
        """DELETE /nodes/{node}/lxc/{vmid}/firewall/rules/{pos}"""
        return self._client.delete(f"{self._base}/rules/{pos}")

    def list_aliases(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/aliases"""
        return self._client.get(f"{self._base}/aliases")

    def get_alias(self, name: str) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/aliases/{name}"""
        return self._client.get(f"{self._base}/aliases/{name}")

    def create_alias(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/firewall/aliases"""
        return self._client.post(
            f"{self._base}/aliases", name=name, cidr=cidr, **kwargs
        )

    def update_alias(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/lxc/{vmid}/firewall/aliases/{name}"""
        return self._client.put(
            f"{self._base}/aliases/{name}", cidr=cidr, **kwargs
        )

    def delete_alias(self, name: str) -> Any:
        """DELETE /nodes/{node}/lxc/{vmid}/firewall/aliases/{name}"""
        return self._client.delete(f"{self._base}/aliases/{name}")

    def list_ipset(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/ipset"""
        return self._client.get(f"{self._base}/ipset")

    def create_ipset(self, name: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/firewall/ipset"""
        return self._client.post(f"{self._base}/ipset", name=name, **kwargs)

    def get_ipset(self, name: str) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}"""
        return self._client.get(f"{self._base}/ipset/{name}")

    def delete_ipset(self, name: str) -> Any:
        """DELETE /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}"""
        return self._client.delete(f"{self._base}/ipset/{name}")

    def add_ipset_entry(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}"""
        return self._client.post(
            f"{self._base}/ipset/{name}", cidr=cidr, **kwargs
        )

    def get_ipset_entry(self, name: str, cidr: str) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}/{cidr}"""
        return self._client.get(f"{self._base}/ipset/{name}/{cidr}")

    def update_ipset_entry(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}/{cidr}"""
        return self._client.put(f"{self._base}/ipset/{name}/{cidr}", **kwargs)

    def delete_ipset_entry(self, name: str, cidr: str) -> Any:
        """DELETE /nodes/{node}/lxc/{vmid}/firewall/ipset/{name}/{cidr}"""
        return self._client.delete(f"{self._base}/ipset/{name}/{cidr}")

    def options(self) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/options"""
        return self._client.get(f"{self._base}/options")

    def set_options(self, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/lxc/{vmid}/firewall/options"""
        return self._client.put(f"{self._base}/options", **kwargs)

    def log(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/log"""
        return self._client.get(f"{self._base}/log", **kwargs)

    def refs(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/lxc/{vmid}/firewall/refs"""
        return self._client.get(f"{self._base}/refs", **kwargs)
