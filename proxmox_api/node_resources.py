"""Node-level resource APIs: disks and firewall."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_api._base import _ResourceBase

if TYPE_CHECKING:
    from proxmox_api.client import ProxmoxAPI


class _DisksAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/disks"

    def list(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/disks/list"""
        return self._client.get(f"{self._base}/list", **kwargs)

    def smart(self, disk: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/disks/smart"""
        return self._client.get(f"{self._base}/smart", disk=disk, **kwargs)

    def initgpt(self, disk: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/disks/initgpt"""
        return self._client.post(f"{self._base}/initgpt", disk=disk, **kwargs)

    def wipedisk(self, disk: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/disks/wipedisk"""
        return self._client.put(f"{self._base}/wipedisk", disk=disk, **kwargs)

    def lvm(self) -> Any:
        """GET /nodes/{node}/disks/lvm"""
        return self._client.get(f"{self._base}/lvm")

    def create_lvm(self, device: str, name: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/disks/lvm"""
        return self._client.post(
            f"{self._base}/lvm", device=device, name=name, **kwargs
        )

    def delete_lvm(self, name: str, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/disks/lvm/{name}"""
        return self._client.delete(f"{self._base}/lvm/{name}", **kwargs)

    def lvmthin(self) -> Any:
        """GET /nodes/{node}/disks/lvmthin"""
        return self._client.get(f"{self._base}/lvmthin")

    def create_lvmthin(self, device: str, name: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/disks/lvmthin"""
        return self._client.post(
            f"{self._base}/lvmthin", device=device, name=name, **kwargs
        )

    def delete_lvmthin(self, name: str, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/disks/lvmthin/{name}"""
        return self._client.delete(f"{self._base}/lvmthin/{name}", **kwargs)

    def directory(self) -> Any:
        """GET /nodes/{node}/disks/directory"""
        return self._client.get(f"{self._base}/directory")

    def create_directory(self, device: str, name: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/disks/directory"""
        return self._client.post(
            f"{self._base}/directory", device=device, name=name, **kwargs
        )

    def delete_directory(self, name: str, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/disks/directory/{name}"""
        return self._client.delete(f"{self._base}/directory/{name}", **kwargs)

    def zfs(self) -> Any:
        """GET /nodes/{node}/disks/zfs"""
        return self._client.get(f"{self._base}/zfs")

    def create_zfs(self, devices: str, name: str, raidlevel: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/disks/zfs"""
        return self._client.post(
            f"{self._base}/zfs",
            devices=devices,
            name=name,
            raidlevel=raidlevel,
            **kwargs,
        )

    def get_zfs(self, name: str) -> Any:
        """GET /nodes/{node}/disks/zfs/{name}"""
        return self._client.get(f"{self._base}/zfs/{name}")

    def delete_zfs(self, name: str, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/disks/zfs/{name}"""
        return self._client.delete(f"{self._base}/zfs/{name}", **kwargs)


class _NodeFirewallAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/firewall"

    def list_rules(self) -> Any:
        """GET /nodes/{node}/firewall/rules"""
        return self._client.get(f"{self._base}/rules")

    def get_rule(self, pos: int) -> Any:
        """GET /nodes/{node}/firewall/rules/{pos}"""
        return self._client.get(f"{self._base}/rules/{pos}")

    def create_rule(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/firewall/rules"""
        return self._client.post(f"{self._base}/rules", **kwargs)

    def update_rule(self, pos: int, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/firewall/rules/{pos}"""
        return self._client.put(f"{self._base}/rules/{pos}", **kwargs)

    def delete_rule(self, pos: int) -> Any:
        """DELETE /nodes/{node}/firewall/rules/{pos}"""
        return self._client.delete(f"{self._base}/rules/{pos}")

    def options(self) -> Any:
        """GET /nodes/{node}/firewall/options"""
        return self._client.get(f"{self._base}/options")

    def set_options(self, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/firewall/options"""
        return self._client.put(f"{self._base}/options", **kwargs)

    def log(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/firewall/log"""
        return self._client.get(f"{self._base}/log", **kwargs)
