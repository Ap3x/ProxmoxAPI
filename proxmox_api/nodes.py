"""Node-level API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_api._base import _ResourceBase
from proxmox_api.lxc import _LxcCollectionAPI
from proxmox_api.node_resources import _DisksAPI, _NodeFirewallAPI
from proxmox_api.qemu import _QemuCollectionAPI

if TYPE_CHECKING:
    from proxmox_api.client import ProxmoxAPI


class _NodesAPI(_ResourceBase):

    def list(self) -> Any:
        """GET /nodes - Cluster node index."""
        return self._client.get("/nodes")

    def __call__(self, node: str) -> _NodeAPI:
        """Select a specific node: api.nodes('pve1')."""
        return _NodeAPI(self._client, node)


class _NodeAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self.node = node
        self._base = f"/nodes/{node}"

    def index(self) -> Any:
        """GET /nodes/{node}"""
        return self._client.get(self._base)

    def status(self) -> Any:
        """GET /nodes/{node}/status"""
        return self._client.get(f"{self._base}/status")

    def post_status(self, command: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/status - Reboot or shutdown a node."""
        return self._client.post(
            f"{self._base}/status", command=command, **kwargs
        )

    def config(self) -> Any:
        """GET /nodes/{node}/config"""
        return self._client.get(f"{self._base}/config")

    def update_config(self, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/config"""
        return self._client.put(f"{self._base}/config", **kwargs)

    def version(self) -> Any:
        """GET /nodes/{node}/version"""
        return self._client.get(f"{self._base}/version")

    def time(self) -> Any:
        """GET /nodes/{node}/time"""
        return self._client.get(f"{self._base}/time")

    def set_time(self, timezone: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/time"""
        return self._client.put(
            f"{self._base}/time", timezone=timezone, **kwargs
        )

    def syslog(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/syslog"""
        return self._client.get(f"{self._base}/syslog", **kwargs)

    def journal(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/journal"""
        return self._client.get(f"{self._base}/journal", **kwargs)

    def dns(self) -> Any:
        """GET /nodes/{node}/dns"""
        return self._client.get(f"{self._base}/dns")

    def set_dns(self, search: str, dns1: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/dns"""
        return self._client.put(
            f"{self._base}/dns", search=search, dns1=dns1, **kwargs
        )

    def hosts(self) -> Any:
        """GET /nodes/{node}/hosts"""
        return self._client.get(f"{self._base}/hosts")

    def set_hosts(self, data: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/hosts"""
        return self._client.post(f"{self._base}/hosts", data=data, **kwargs)

    def report(self) -> Any:
        """GET /nodes/{node}/report"""
        return self._client.get(f"{self._base}/report")

    # --- Tasks ---

    def tasks(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/tasks - Read task list for one node."""
        return self._client.get(f"{self._base}/tasks", **kwargs)

    def task_index(self, upid: str) -> Any:
        """GET /nodes/{node}/tasks/{upid}"""
        return self._client.get(f"{self._base}/tasks/{upid}")

    def task_status(self, upid: str) -> Any:
        """GET /nodes/{node}/tasks/{upid}/status"""
        return self._client.get(f"{self._base}/tasks/{upid}/status")

    def task_log(self, upid: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/tasks/{upid}/log"""
        return self._client.get(f"{self._base}/tasks/{upid}/log", **kwargs)

    def stop_task(self, upid: str) -> Any:
        """DELETE /nodes/{node}/tasks/{upid}"""
        return self._client.delete(f"{self._base}/tasks/{upid}")

    # --- RRD ---

    def rrd(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/rrd"""
        return self._client.get(f"{self._base}/rrd", **kwargs)

    def rrddata(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/rrddata"""
        return self._client.get(f"{self._base}/rrddata", **kwargs)

    # --- Network ---

    def netstat(self) -> Any:
        """GET /nodes/{node}/netstat"""
        return self._client.get(f"{self._base}/netstat")

    def network(self) -> Any:
        """GET /nodes/{node}/network"""
        return self._client.get(f"{self._base}/network")

    def get_network_iface(self, iface: str) -> Any:
        """GET /nodes/{node}/network/{iface}"""
        return self._client.get(f"{self._base}/network/{iface}")

    def create_network(self, iface: str, type: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/network"""
        return self._client.post(
            f"{self._base}/network", iface=iface, type=type, **kwargs
        )

    def update_network(self, iface: str, type: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/network/{iface}"""
        return self._client.put(
            f"{self._base}/network/{iface}", type=type, **kwargs
        )

    def delete_network(self, iface: str) -> Any:
        """DELETE /nodes/{node}/network/{iface}"""
        return self._client.delete(f"{self._base}/network/{iface}")

    def revert_network(self) -> Any:
        """DELETE /nodes/{node}/network - Revert network configuration changes."""
        return self._client.delete(f"{self._base}/network")

    def apply_network(self) -> Any:
        """PUT /nodes/{node}/network - Apply network configuration changes."""
        return self._client.put(f"{self._base}/network")

    # --- Storage ---

    def list_storage(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/storage"""
        return self._client.get(f"{self._base}/storage", **kwargs)

    def get_storage(self, storage: str) -> Any:
        """GET /nodes/{node}/storage/{storage}"""
        return self._client.get(f"{self._base}/storage/{storage}")

    def storage_status(self, storage: str) -> Any:
        """GET /nodes/{node}/storage/{storage}/status"""
        return self._client.get(f"{self._base}/storage/{storage}/status")

    def storage_rrd(self, storage: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/storage/{storage}/rrd"""
        return self._client.get(f"{self._base}/storage/{storage}/rrd", **kwargs)

    def storage_rrddata(self, storage: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/storage/{storage}/rrddata"""
        return self._client.get(
            f"{self._base}/storage/{storage}/rrddata", **kwargs
        )

    def storage_content(self, storage: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/storage/{storage}/content"""
        return self._client.get(
            f"{self._base}/storage/{storage}/content", **kwargs
        )

    def create_storage_content(self, storage: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/storage/{storage}/content - Allocate disk images."""
        return self._client.post(
            f"{self._base}/storage/{storage}/content", **kwargs
        )

    def get_storage_volume(self, storage: str, volume: str) -> Any:
        """GET /nodes/{node}/storage/{storage}/content/{volume}"""
        return self._client.get(
            f"{self._base}/storage/{storage}/content/{volume}"
        )

    def copy_storage_volume(self, storage: str, volume: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/storage/{storage}/content/{volume} - Copy a volume."""
        return self._client.post(
            f"{self._base}/storage/{storage}/content/{volume}", **kwargs
        )

    def update_storage_volume(self, storage: str, volume: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/storage/{storage}/content/{volume}"""
        return self._client.put(
            f"{self._base}/storage/{storage}/content/{volume}", **kwargs
        )

    def delete_storage_volume(self, storage: str, volume: str, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/storage/{storage}/content/{volume}"""
        return self._client.delete(
            f"{self._base}/storage/{storage}/content/{volume}", **kwargs
        )

    def storage_prunebackups(self, storage: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/storage/{storage}/prunebackups"""
        return self._client.get(
            f"{self._base}/storage/{storage}/prunebackups", **kwargs
        )

    def delete_storage_prunebackups(self, storage: str, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/storage/{storage}/prunebackups"""
        return self._client.delete(
            f"{self._base}/storage/{storage}/prunebackups", **kwargs
        )

    def storage_file_restore_list(self, storage: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/storage/{storage}/file-restore/list"""
        return self._client.get(
            f"{self._base}/storage/{storage}/file-restore/list", **kwargs
        )

    def storage_file_restore_download(self, storage: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/storage/{storage}/file-restore/download"""
        return self._client.get(
            f"{self._base}/storage/{storage}/file-restore/download", **kwargs
        )

    def storage_download_url(self, storage: str, url: str, filename: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/storage/{storage}/download-url"""
        return self._client.post(
            f"{self._base}/storage/{storage}/download-url",
            url=url,
            filename=filename,
            **kwargs,
        )

    def storage_import_metadata(self, storage: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/storage/{storage}/import-metadata"""
        return self._client.get(
            f"{self._base}/storage/{storage}/import-metadata", **kwargs
        )

    def upload(self, storage: str, content: str, filename: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/storage/{storage}/upload"""
        return self._client.post(
            f"{self._base}/storage/{storage}/upload",
            content=content,
            filename=filename,
            **kwargs,
        )

    # --- Services ---

    def services(self) -> Any:
        """GET /nodes/{node}/services"""
        return self._client.get(f"{self._base}/services")

    def service_index(self, service: str) -> Any:
        """GET /nodes/{node}/services/{service}"""
        return self._client.get(f"{self._base}/services/{service}")

    def service_state(self, service: str) -> Any:
        """GET /nodes/{node}/services/{service}/state"""
        return self._client.get(f"{self._base}/services/{service}/state")

    def start_service(self, service: str) -> Any:
        """POST /nodes/{node}/services/{service}/start"""
        return self._client.post(f"{self._base}/services/{service}/start")

    def stop_service(self, service: str) -> Any:
        """POST /nodes/{node}/services/{service}/stop"""
        return self._client.post(f"{self._base}/services/{service}/stop")

    def restart_service(self, service: str) -> Any:
        """POST /nodes/{node}/services/{service}/restart"""
        return self._client.post(f"{self._base}/services/{service}/restart")

    def reload_service(self, service: str) -> Any:
        """POST /nodes/{node}/services/{service}/reload"""
        return self._client.post(f"{self._base}/services/{service}/reload")

    # --- APT ---

    def apt_index(self) -> Any:
        """GET /nodes/{node}/apt"""
        return self._client.get(f"{self._base}/apt")

    def apt_update(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/apt/update"""
        return self._client.post(f"{self._base}/apt/update", **kwargs)

    def apt_list_updates(self) -> Any:
        """GET /nodes/{node}/apt/update"""
        return self._client.get(f"{self._base}/apt/update")

    def apt_changelog(self, name: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/apt/changelog"""
        return self._client.get(f"{self._base}/apt/changelog", name=name, **kwargs)

    def apt_repositories(self) -> Any:
        """GET /nodes/{node}/apt/repositories"""
        return self._client.get(f"{self._base}/apt/repositories")

    def apt_add_repository(self, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/apt/repositories"""
        return self._client.put(f"{self._base}/apt/repositories", **kwargs)

    def apt_change_repository(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/apt/repositories"""
        return self._client.post(f"{self._base}/apt/repositories", **kwargs)

    def apt_versions(self) -> Any:
        """GET /nodes/{node}/apt/versions"""
        return self._client.get(f"{self._base}/apt/versions")

    # --- Subscription ---

    def subscription(self) -> Any:
        """GET /nodes/{node}/subscription"""
        return self._client.get(f"{self._base}/subscription")

    def set_subscription(self, key: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/subscription"""
        return self._client.put(f"{self._base}/subscription", key=key, **kwargs)

    def update_subscription(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/subscription"""
        return self._client.post(f"{self._base}/subscription", **kwargs)

    def delete_subscription(self) -> Any:
        """DELETE /nodes/{node}/subscription"""
        return self._client.delete(f"{self._base}/subscription")

    # --- Certificates ---

    def certificates(self) -> Any:
        """GET /nodes/{node}/certificates"""
        return self._client.get(f"{self._base}/certificates")

    def certificates_info(self) -> Any:
        """GET /nodes/{node}/certificates/info"""
        return self._client.get(f"{self._base}/certificates/info")

    def certificates_acme_index(self) -> Any:
        """GET /nodes/{node}/certificates/acme"""
        return self._client.get(f"{self._base}/certificates/acme")

    def certificates_acme_order(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/certificates/acme/certificate"""
        return self._client.post(
            f"{self._base}/certificates/acme/certificate", **kwargs
        )

    def certificates_acme_renew(self, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/certificates/acme/certificate"""
        return self._client.put(
            f"{self._base}/certificates/acme/certificate", **kwargs
        )

    def certificates_acme_revoke(self) -> Any:
        """DELETE /nodes/{node}/certificates/acme/certificate"""
        return self._client.delete(
            f"{self._base}/certificates/acme/certificate"
        )

    def upload_custom_certificate(self, certificates: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/certificates/custom"""
        return self._client.post(
            f"{self._base}/certificates/custom",
            certificates=certificates,
            **kwargs,
        )

    def delete_custom_certificate(self, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/certificates/custom"""
        return self._client.delete(f"{self._base}/certificates/custom", **kwargs)

    # --- VNC / Term / Spice ---

    def vncshell(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/vncshell"""
        return self._client.post(f"{self._base}/vncshell", **kwargs)

    def vncwebsocket(self, port: int, vncticket: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/vncwebsocket"""
        return self._client.get(
            f"{self._base}/vncwebsocket", port=port, vncticket=vncticket, **kwargs
        )

    def termproxy(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/termproxy"""
        return self._client.post(f"{self._base}/termproxy", **kwargs)

    def spiceshell(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/spiceshell"""
        return self._client.post(f"{self._base}/spiceshell", **kwargs)

    # --- Vzdump ---

    def vzdump(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/vzdump - Create backup."""
        return self._client.post(f"{self._base}/vzdump", **kwargs)

    def vzdump_defaults(self) -> Any:
        """GET /nodes/{node}/vzdump/defaults"""
        return self._client.get(f"{self._base}/vzdump/defaults")

    def vzdump_extractconfig(self, volume: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/vzdump/extractconfig"""
        return self._client.get(
            f"{self._base}/vzdump/extractconfig", volume=volume, **kwargs
        )

    # --- Aplinfo (Templates) ---

    def aplinfo(self) -> Any:
        """GET /nodes/{node}/aplinfo - Get list of available templates."""
        return self._client.get(f"{self._base}/aplinfo")

    def download_template(self, storage: str, template: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/aplinfo - Download appliance templates."""
        return self._client.post(
            f"{self._base}/aplinfo", storage=storage, template=template, **kwargs
        )

    # --- Bulk operations ---

    def startall(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/startall"""
        return self._client.post(f"{self._base}/startall", **kwargs)

    def stopall(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/stopall"""
        return self._client.post(f"{self._base}/stopall", **kwargs)

    def suspendall(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/suspendall"""
        return self._client.post(f"{self._base}/suspendall", **kwargs)

    def migrateall(self, target: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/migrateall"""
        return self._client.post(
            f"{self._base}/migrateall", target=target, **kwargs
        )

    # --- Execute / Wake on LAN ---

    def execute(self, command: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/execute"""
        return self._client.post(
            f"{self._base}/execute", command=command, **kwargs
        )

    def wakeonlan(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/wakeonlan"""
        return self._client.post(f"{self._base}/wakeonlan", **kwargs)

    # --- Query ---

    def query_url_metadata(self, url: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/query-url-metadata"""
        return self._client.get(
            f"{self._base}/query-url-metadata", url=url, **kwargs
        )

    def query_oci_repo_tags(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/query-oci-repo-tags"""
        return self._client.get(f"{self._base}/query-oci-repo-tags", **kwargs)

    # --- Nested API properties ---

    @property
    def qemu(self) -> _QemuCollectionAPI:
        return _QemuCollectionAPI(self._client, self.node)

    @property
    def lxc(self) -> _LxcCollectionAPI:
        return _LxcCollectionAPI(self._client, self.node)

    @property
    def disks(self) -> _DisksAPI:
        return _DisksAPI(self._client, self.node)

    @property
    def firewall(self) -> _NodeFirewallAPI:
        return _NodeFirewallAPI(self._client, self.node)

    @property
    def scan(self) -> _NodeScanAPI:
        return _NodeScanAPI(self._client, self.node)

    @property
    def hardware(self) -> _NodeHardwareAPI:
        return _NodeHardwareAPI(self._client, self.node)

    @property
    def capabilities(self) -> _NodeCapabilitiesAPI:
        return _NodeCapabilitiesAPI(self._client, self.node)

    @property
    def ceph(self) -> _NodeCephAPI:
        return _NodeCephAPI(self._client, self.node)

    @property
    def replication(self) -> _NodeReplicationAPI:
        return _NodeReplicationAPI(self._client, self.node)

    @property
    def sdn(self) -> _NodeSDNAPI:
        return _NodeSDNAPI(self._client, self.node)


# --- Scan ---

class _NodeScanAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/scan"

    def index(self) -> Any:
        """GET /nodes/{node}/scan"""
        return self._client.get(self._base)

    def nfs(self, server: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/scan/nfs"""
        return self._client.get(f"{self._base}/nfs", server=server, **kwargs)

    def cifs(self, server: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/scan/cifs"""
        return self._client.get(f"{self._base}/cifs", server=server, **kwargs)

    def pbs(self, server: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/scan/pbs"""
        return self._client.get(f"{self._base}/pbs", server=server, **kwargs)

    def iscsi(self, portal: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/scan/iscsi"""
        return self._client.get(f"{self._base}/iscsi", portal=portal, **kwargs)

    def lvm(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/scan/lvm"""
        return self._client.get(f"{self._base}/lvm", **kwargs)

    def lvmthin(self, vg: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/scan/lvmthin"""
        return self._client.get(f"{self._base}/lvmthin", vg=vg, **kwargs)

    def zfs(self) -> Any:
        """GET /nodes/{node}/scan/zfs"""
        return self._client.get(f"{self._base}/zfs")


# --- Hardware ---

class _NodeHardwareAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/hardware"

    def index(self) -> Any:
        """GET /nodes/{node}/hardware"""
        return self._client.get(self._base)

    def pci(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/hardware/pci"""
        return self._client.get(f"{self._base}/pci", **kwargs)

    def get_pci(self, pciid: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/hardware/pci/{pci-id-or-mapping}"""
        return self._client.get(f"{self._base}/pci/{pciid}", **kwargs)

    def pci_mdev(self, pciid: str) -> Any:
        """GET /nodes/{node}/hardware/pci/{pci-id-or-mapping}/mdev"""
        return self._client.get(f"{self._base}/pci/{pciid}/mdev")

    def usb(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/hardware/usb"""
        return self._client.get(f"{self._base}/usb", **kwargs)


# --- Capabilities ---

class _NodeCapabilitiesAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/capabilities"

    def index(self) -> Any:
        """GET /nodes/{node}/capabilities"""
        return self._client.get(self._base)

    def qemu_index(self) -> Any:
        """GET /nodes/{node}/capabilities/qemu"""
        return self._client.get(f"{self._base}/qemu")

    def qemu_cpu(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/capabilities/qemu/cpu"""
        return self._client.get(f"{self._base}/qemu/cpu", **kwargs)

    def qemu_cpu_flags(self) -> Any:
        """GET /nodes/{node}/capabilities/qemu/cpu-flags"""
        return self._client.get(f"{self._base}/qemu/cpu-flags")

    def qemu_machines(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/capabilities/qemu/machines"""
        return self._client.get(f"{self._base}/qemu/machines", **kwargs)

    def qemu_migration(self) -> Any:
        """GET /nodes/{node}/capabilities/qemu/migration"""
        return self._client.get(f"{self._base}/qemu/migration")


# --- Ceph ---

class _NodeCephAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/ceph"

    def index(self) -> Any:
        """GET /nodes/{node}/ceph"""
        return self._client.get(self._base)

    def status(self) -> Any:
        """GET /nodes/{node}/ceph/status"""
        return self._client.get(f"{self._base}/status")

    def crush(self) -> Any:
        """GET /nodes/{node}/ceph/crush"""
        return self._client.get(f"{self._base}/crush")

    def log(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/ceph/log"""
        return self._client.get(f"{self._base}/log", **kwargs)

    def rules(self) -> Any:
        """GET /nodes/{node}/ceph/rules"""
        return self._client.get(f"{self._base}/rules")

    def cmd_safety(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/ceph/cmd-safety"""
        return self._client.get(f"{self._base}/cmd-safety", **kwargs)

    def init(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/init"""
        return self._client.post(f"{self._base}/init", **kwargs)

    def start(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/start"""
        return self._client.post(f"{self._base}/start", **kwargs)

    def stop(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/stop"""
        return self._client.post(f"{self._base}/stop", **kwargs)

    def restart(self, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/restart"""
        return self._client.post(f"{self._base}/restart", **kwargs)

    # --- Ceph Config ---

    def cfg_index(self) -> Any:
        """GET /nodes/{node}/ceph/cfg"""
        return self._client.get(f"{self._base}/cfg")

    def cfg_raw(self) -> Any:
        """GET /nodes/{node}/ceph/cfg/raw"""
        return self._client.get(f"{self._base}/cfg/raw")

    def cfg_db(self) -> Any:
        """GET /nodes/{node}/ceph/cfg/db"""
        return self._client.get(f"{self._base}/cfg/db")

    def cfg_value(self, **kwargs: Any) -> Any:
        """GET /nodes/{node}/ceph/cfg/value"""
        return self._client.get(f"{self._base}/cfg/value", **kwargs)

    # --- Ceph OSD ---

    def list_osd(self) -> Any:
        """GET /nodes/{node}/ceph/osd"""
        return self._client.get(f"{self._base}/osd")

    def create_osd(self, dev: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/osd"""
        return self._client.post(f"{self._base}/osd", dev=dev, **kwargs)

    def get_osd(self, osdid: int) -> Any:
        """GET /nodes/{node}/ceph/osd/{osdid}"""
        return self._client.get(f"{self._base}/osd/{osdid}")

    def delete_osd(self, osdid: int, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/ceph/osd/{osdid}"""
        return self._client.delete(f"{self._base}/osd/{osdid}", **kwargs)

    def osd_metadata(self, osdid: int) -> Any:
        """GET /nodes/{node}/ceph/osd/{osdid}/metadata"""
        return self._client.get(f"{self._base}/osd/{osdid}/metadata")

    def osd_lv_info(self, osdid: int, **kwargs: Any) -> Any:
        """GET /nodes/{node}/ceph/osd/{osdid}/lv-info"""
        return self._client.get(f"{self._base}/osd/{osdid}/lv-info", **kwargs)

    def osd_in(self, osdid: int) -> Any:
        """POST /nodes/{node}/ceph/osd/{osdid}/in"""
        return self._client.post(f"{self._base}/osd/{osdid}/in")

    def osd_out(self, osdid: int) -> Any:
        """POST /nodes/{node}/ceph/osd/{osdid}/out"""
        return self._client.post(f"{self._base}/osd/{osdid}/out")

    def osd_scrub(self, osdid: int, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/osd/{osdid}/scrub"""
        return self._client.post(f"{self._base}/osd/{osdid}/scrub", **kwargs)

    # --- Ceph MDS ---

    def list_mds(self) -> Any:
        """GET /nodes/{node}/ceph/mds"""
        return self._client.get(f"{self._base}/mds")

    def create_mds(self, name: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/mds/{name}"""
        return self._client.post(f"{self._base}/mds/{name}", **kwargs)

    def delete_mds(self, name: str) -> Any:
        """DELETE /nodes/{node}/ceph/mds/{name}"""
        return self._client.delete(f"{self._base}/mds/{name}")

    # --- Ceph MGR ---

    def list_mgr(self) -> Any:
        """GET /nodes/{node}/ceph/mgr"""
        return self._client.get(f"{self._base}/mgr")

    def create_mgr(self, id: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/mgr/{id}"""
        return self._client.post(f"{self._base}/mgr/{id}", **kwargs)

    def delete_mgr(self, id: str) -> Any:
        """DELETE /nodes/{node}/ceph/mgr/{id}"""
        return self._client.delete(f"{self._base}/mgr/{id}")

    # --- Ceph MON ---

    def list_mon(self) -> Any:
        """GET /nodes/{node}/ceph/mon"""
        return self._client.get(f"{self._base}/mon")

    def create_mon(self, monid: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/mon/{monid}"""
        return self._client.post(f"{self._base}/mon/{monid}", **kwargs)

    def delete_mon(self, monid: str) -> Any:
        """DELETE /nodes/{node}/ceph/mon/{monid}"""
        return self._client.delete(f"{self._base}/mon/{monid}")

    # --- Ceph FS ---

    def list_fs(self) -> Any:
        """GET /nodes/{node}/ceph/fs"""
        return self._client.get(f"{self._base}/fs")

    def create_fs(self, name: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/fs/{name}"""
        return self._client.post(f"{self._base}/fs/{name}", **kwargs)

    # --- Ceph Pool ---

    def list_pool(self) -> Any:
        """GET /nodes/{node}/ceph/pool"""
        return self._client.get(f"{self._base}/pool")

    def create_pool(self, name: str, **kwargs: Any) -> Any:
        """POST /nodes/{node}/ceph/pool"""
        return self._client.post(f"{self._base}/pool", name=name, **kwargs)

    def get_pool(self, name: str) -> Any:
        """GET /nodes/{node}/ceph/pool/{name}"""
        return self._client.get(f"{self._base}/pool/{name}")

    def update_pool(self, name: str, **kwargs: Any) -> Any:
        """PUT /nodes/{node}/ceph/pool/{name}"""
        return self._client.put(f"{self._base}/pool/{name}", **kwargs)

    def delete_pool(self, name: str, **kwargs: Any) -> Any:
        """DELETE /nodes/{node}/ceph/pool/{name}"""
        return self._client.delete(f"{self._base}/pool/{name}", **kwargs)

    def pool_status(self, name: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/ceph/pool/{name}/status"""
        return self._client.get(f"{self._base}/pool/{name}/status", **kwargs)


# --- Replication ---

class _NodeReplicationAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/replication"

    def list(self) -> Any:
        """GET /nodes/{node}/replication"""
        return self._client.get(self._base)

    def get(self, id: str) -> Any:
        """GET /nodes/{node}/replication/{id}"""
        return self._client.get(f"{self._base}/{id}")

    def status(self, id: str) -> Any:
        """GET /nodes/{node}/replication/{id}/status"""
        return self._client.get(f"{self._base}/{id}/status")

    def log(self, id: str, **kwargs: Any) -> Any:
        """GET /nodes/{node}/replication/{id}/log"""
        return self._client.get(f"{self._base}/{id}/log", **kwargs)

    def schedule_now(self, id: str) -> Any:
        """POST /nodes/{node}/replication/{id}/schedule_now"""
        return self._client.post(f"{self._base}/{id}/schedule_now")


# --- SDN ---

class _NodeSDNAPI(_ResourceBase):

    def __init__(self, client: ProxmoxAPI, node: str) -> None:
        super().__init__(client)
        self._base = f"/nodes/{node}/sdn"

    def index(self) -> Any:
        """GET /nodes/{node}/sdn"""
        return self._client.get(self._base)

    def zones(self) -> Any:
        """GET /nodes/{node}/sdn/zones"""
        return self._client.get(f"{self._base}/zones")

    def get_zone(self, zone: str) -> Any:
        """GET /nodes/{node}/sdn/zones/{zone}"""
        return self._client.get(f"{self._base}/zones/{zone}")

    def zone_content(self, zone: str) -> Any:
        """GET /nodes/{node}/sdn/zones/{zone}/content"""
        return self._client.get(f"{self._base}/zones/{zone}/content")

    def zone_bridges(self, zone: str) -> Any:
        """GET /nodes/{node}/sdn/zones/{zone}/bridges"""
        return self._client.get(f"{self._base}/zones/{zone}/bridges")

    def zone_ip_vrf(self, zone: str) -> Any:
        """GET /nodes/{node}/sdn/zones/{zone}/ip-vrf"""
        return self._client.get(f"{self._base}/zones/{zone}/ip-vrf")

    def get_vnet(self, vnet: str) -> Any:
        """GET /nodes/{node}/sdn/vnets/{vnet}"""
        return self._client.get(f"{self._base}/vnets/{vnet}")

    def vnet_mac_vrf(self, vnet: str) -> Any:
        """GET /nodes/{node}/sdn/vnets/{vnet}/mac-vrf"""
        return self._client.get(f"{self._base}/vnets/{vnet}/mac-vrf")

    def fabric_info(self, fabric: str) -> Any:
        """GET /nodes/{node}/sdn/fabrics/{fabric}"""
        return self._client.get(f"{self._base}/fabrics/{fabric}")

    def fabric_routes(self, fabric: str) -> Any:
        """GET /nodes/{node}/sdn/fabrics/{fabric}/routes"""
        return self._client.get(f"{self._base}/fabrics/{fabric}/routes")

    def fabric_neighbors(self, fabric: str) -> Any:
        """GET /nodes/{node}/sdn/fabrics/{fabric}/neighbors"""
        return self._client.get(f"{self._base}/fabrics/{fabric}/neighbors")

    def fabric_interfaces(self, fabric: str) -> Any:
        """GET /nodes/{node}/sdn/fabrics/{fabric}/interfaces"""
        return self._client.get(f"{self._base}/fabrics/{fabric}/interfaces")
