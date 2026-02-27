"""Tests for the ProxmoxAPI client (mocked HTTP)."""

from unittest.mock import MagicMock, patch

import pytest

from proxmox_api.client import ProxmoxAPI


@pytest.fixture
def api() -> ProxmoxAPI:
    """Create a ProxmoxAPI client using token auth (no network needed)."""
    with patch("proxmox_api.client.requests.Session") as MockSession:
        mock_session = MockSession.return_value
        mock_session.headers = {}
        mock_session.cookies = MagicMock()
        client = ProxmoxAPI(
            host="10.0.0.1",
            user="root@pam",
            token_name="test",
            token_value="00000000-0000-0000-0000-000000000000",
        )
    return client


def test_token_auth_header(api: ProxmoxAPI) -> None:
    assert "Authorization" in api._session.headers
    assert api._session.headers["Authorization"].startswith("PVEAPIToken=")
    assert "root@pam!test=" in api._session.headers["Authorization"]


def test_base_url(api: ProxmoxAPI) -> None:
    assert api.base_url == "https://10.0.0.1:8006/api2/json"


def test_custom_port() -> None:
    with patch("proxmox_api.client.requests.Session") as MockSession:
        mock_session = MockSession.return_value
        mock_session.headers = {}
        mock_session.cookies = MagicMock()
        client = ProxmoxAPI(
            host="10.0.0.1",
            user="root@pam",
            token_name="test",
            token_value="tok",
            port=443,
        )
    assert client.base_url == "https://10.0.0.1:443/api2/json"


def test_missing_auth_raises() -> None:
    with pytest.raises(ValueError, match="Provide either"):
        with patch("proxmox_api.client.requests.Session"):
            ProxmoxAPI(host="10.0.0.1")


def test_token_without_user_raises() -> None:
    with pytest.raises(ValueError, match="user"):
        with patch("proxmox_api.client.requests.Session"):
            ProxmoxAPI(
                host="10.0.0.1",
                token_name="test",
                token_value="tok",
            )


def test_get_calls_session(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"node": "pve1"}]}
    api._session.request.return_value = mock_resp

    result = api.get("/nodes")

    api._session.request.assert_called_once_with(
        "GET",
        "https://10.0.0.1:8006/api2/json/nodes",
        params={},
        data=None,
        timeout=30,
    )
    assert result == [{"node": "pve1"}]


def test_post_calls_session(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:000"}
    api._session.request.return_value = mock_resp

    result = api.post("/nodes/pve1/qemu/100/status/start")

    api._session.request.assert_called_once()
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert result == "UPID:pve1:000"


def test_none_values_stripped(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {}}
    api._session.request.return_value = mock_resp

    api.post("/test", foo="bar", baz=None)

    call_args = api._session.request.call_args
    assert call_args[1]["data"] == {"foo": "bar"}


def test_nodes_accessor(api: ProxmoxAPI) -> None:
    node = api.nodes("pve1")
    assert node.node == "pve1"
    assert node._base == "/nodes/pve1"


def test_qemu_accessor(api: ProxmoxAPI) -> None:
    vm = api.nodes("pve1").qemu(100)
    assert vm.vmid == 100
    assert vm._base == "/nodes/pve1/qemu/100"


def test_lxc_accessor(api: ProxmoxAPI) -> None:
    ct = api.nodes("pve1").lxc(200)
    assert ct.vmid == 200
    assert ct._base == "/nodes/pve1/lxc/200"


def test_vm_start(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:001"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).start()
    assert result == "UPID:pve1:001"

    call_args = api._session.request.call_args
    assert "/nodes/pve1/qemu/100/status/start" in call_args[0][1]


def test_vm_config(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"memory": 2048, "cores": 2}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).config()
    assert result["memory"] == 2048


def test_snapshot_operations(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").qemu(100).snapshot.list()
    call_url = api._session.request.call_args[0][1]
    assert "/nodes/pve1/qemu/100/snapshot" in call_url


def test_cluster_resources(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    api._session.request.return_value = mock_resp

    api.cluster.resources(type="vm")
    call_args = api._session.request.call_args
    assert "cluster/resources" in call_args[0][1]


def test_storage_accessor(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    api._session.request.return_value = mock_resp

    api.storage.list()
    assert "storage" in api._session.request.call_args[0][1]


def test_pools_accessor(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    api._session.request.return_value = mock_resp

    api.pools.list()
    assert "pools" in api._session.request.call_args[0][1]


def test_access_users(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"userid": "root@pam"}]}
    api._session.request.return_value = mock_resp

    result = api.access.list_users()
    assert result == [{"userid": "root@pam"}]


def test_version(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"version": "8.0"}}
    api._session.request.return_value = mock_resp

    result = api.version()
    assert result["version"] == "8.0"


def test_password_auth() -> None:
    with patch("proxmox_api.client.requests.Session") as MockSession:
        mock_session = MockSession.return_value
        mock_session.headers = {}
        mock_session.cookies = MagicMock()

        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "data": {
                "ticket": "PVE:root@pam:XXXX",
                "CSRFPreventionToken": "CSRF:XXXX",
            }
        }
        mock_session.post.return_value = mock_resp

        client = ProxmoxAPI(
            host="10.0.0.1",
            user="root@pam",
            password="secret",
        )

    mock_session.post.assert_called_once()
    mock_session.cookies.set.assert_called_once_with(
        "PVEAuthCookie", "PVE:root@pam:XXXX"
    )
    assert mock_session.headers["CSRFPreventionToken"] == "CSRF:XXXX"


# ============================================================
# Access API
# ============================================================


def test_access_list_user_tokens(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"tokenid": "mytoken"}]}
    api._session.request.return_value = mock_resp

    result = api.access.list_user_tokens("root@pam")
    assert result == [{"tokenid": "mytoken"}]
    assert "/access/users/root@pam/token" in api._session.request.call_args[0][1]


def test_access_get_user_token(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"tokenid": "tok1", "privsep": 1}}
    api._session.request.return_value = mock_resp

    result = api.access.get_user_token("root@pam", "tok1")
    assert result["tokenid"] == "tok1"
    assert "/access/users/root@pam/token/tok1" in api._session.request.call_args[0][1]


def test_access_create_user_token(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"full-tokenid": "root@pam!tok1", "value": "secret"}}
    api._session.request.return_value = mock_resp

    result = api.access.create_user_token("root@pam", "tok1")
    assert result["value"] == "secret"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/access/users/root@pam/token/tok1" in call_args[0][1]


def test_access_delete_user_token(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.access.delete_user_token("root@pam", "tok1")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/access/users/root@pam/token/tok1" in call_args[0][1]


def test_access_user_tfa(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"type": "totp"}]}
    api._session.request.return_value = mock_resp

    result = api.access.user_tfa("root@pam")
    assert result == [{"type": "totp"}]
    assert "/access/users/root@pam/tfa" in api._session.request.call_args[0][1]


def test_access_unlock_user_tfa(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": True}
    api._session.request.return_value = mock_resp

    result = api.access.unlock_user_tfa("root@pam")
    assert result is True
    call_args = api._session.request.call_args
    assert call_args[0][0] == "PUT"
    assert "/access/users/root@pam/unlock-tfa" in call_args[0][1]


def test_access_tfa_crud(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": "tfa1"}]}
    api._session.request.return_value = mock_resp

    result = api.access.list_tfa("root@pam")
    assert result == [{"id": "tfa1"}]
    assert "/access/tfa/root@pam" in api._session.request.call_args[0][1]


def test_access_tfa_entry(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"id": "tfa1", "type": "totp"}}
    api._session.request.return_value = mock_resp

    result = api.access.get_tfa_entry("root@pam", "tfa1")
    assert result["type"] == "totp"
    assert "/access/tfa/root@pam/tfa1" in api._session.request.call_args[0][1]


def test_access_add_tfa(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"id": "tfa2"}}
    api._session.request.return_value = mock_resp

    result = api.access.add_tfa("root@pam", type="totp")
    assert result["id"] == "tfa2"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"


def test_access_delete_tfa_entry(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.access.delete_tfa_entry("root@pam", "tfa1")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/access/tfa/root@pam/tfa1" in call_args[0][1]


def test_access_openid_index(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    api._session.request.return_value = mock_resp

    result = api.access.openid()
    assert result == []
    assert "/access/openid" in api._session.request.call_args[0][1]


def test_access_openid_auth_url(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "https://idp.example.com/auth"}
    api._session.request.return_value = mock_resp

    result = api.access.openid_auth_url("myrealm", "https://pve.local/callback")
    assert result == "https://idp.example.com/auth"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/access/openid/auth-url" in call_args[0][1]


def test_access_openid_login(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"ticket": "PVE:user@realm:XXX"}}
    api._session.request.return_value = mock_resp

    result = api.access.openid_login("authcode", "stateXYZ")
    assert result["ticket"] == "PVE:user@realm:XXX"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/access/openid/login" in call_args[0][1]


def test_access_sync_domain(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:sync"}
    api._session.request.return_value = mock_resp

    result = api.access.sync_domain("ldap1")
    assert result == "UPID:pve1:sync"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/access/domains/ldap1/sync" in call_args[0][1]


def test_access_create_vncticket(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"ticket": "PVEVNC:XXX"}}
    api._session.request.return_value = mock_resp

    result = api.access.create_vncticket()
    assert result["ticket"] == "PVEVNC:XXX"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/access/vncticket" in call_args[0][1]


# ============================================================
# Pools API
# ============================================================


def test_pools_bulk_update(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.pools.bulk_update(poolid="pool1", members="100,101")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "PUT"
    url = call_args[0][1]
    assert url.endswith("/pools")


def test_pools_bulk_delete(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.pools.bulk_delete(poolid="pool1")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    url = call_args[0][1]
    assert url.endswith("/pools")


# ============================================================
# Node Resources - Disks
# ============================================================


def test_node_disk_wipedisk(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:wipe"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").disks.wipedisk("/dev/sdb")
    assert result == "UPID:pve1:wipe"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "PUT"
    assert "/nodes/pve1/disks/wipedisk" in call_args[0][1]


def test_node_disk_delete_lvm(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:del"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").disks.delete_lvm("data")
    assert result == "UPID:pve1:del"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/nodes/pve1/disks/lvm/data" in call_args[0][1]


def test_node_disk_delete_lvmthin(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:del"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").disks.delete_lvmthin("thinpool")
    assert result == "UPID:pve1:del"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/nodes/pve1/disks/lvmthin/thinpool" in call_args[0][1]


def test_node_disk_directory(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"path": "/mnt/data"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").disks.directory()
    assert result == [{"path": "/mnt/data"}]
    assert "/nodes/pve1/disks/directory" in api._session.request.call_args[0][1]


def test_node_disk_delete_zfs(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:del"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").disks.delete_zfs("rpool")
    assert result == "UPID:pve1:del"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/nodes/pve1/disks/zfs/rpool" in call_args[0][1]


def test_node_disk_create_zfs(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:create"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").disks.create_zfs("/dev/sdb", "mypool", "mirror")
    assert result == "UPID:pve1:create"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/disks/zfs" in call_args[0][1]


def test_node_disk_get_zfs(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"name": "rpool", "state": "ONLINE"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").disks.get_zfs("rpool")
    assert result["state"] == "ONLINE"
    assert "/nodes/pve1/disks/zfs/rpool" in api._session.request.call_args[0][1]


# ============================================================
# LXC API
# ============================================================


def test_lxc_index(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"subdir": "config"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).index()
    assert result == [{"subdir": "config"}]
    url = api._session.request.call_args[0][1]
    assert url.endswith("/nodes/pve1/lxc/200")


def test_lxc_status_index(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"subdir": "current"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).status_index()
    assert result == [{"subdir": "current"}]
    assert "/nodes/pve1/lxc/200/status" in api._session.request.call_args[0][1]


def test_lxc_pending(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"key": "memory", "pending": 4096}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).pending()
    assert result[0]["key"] == "memory"
    assert "/nodes/pve1/lxc/200/pending" in api._session.request.call_args[0][1]


def test_lxc_migrate_preconditions(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"running": 1}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).migrate_preconditions()
    assert result["running"] == 1
    call_args = api._session.request.call_args
    assert call_args[0][0] == "GET"
    assert "/nodes/pve1/lxc/200/migrate" in call_args[0][1]


def test_lxc_remote_migrate(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:rmig"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).remote_migrate("pve2")
    assert result == "UPID:pve1:rmig"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/lxc/200/remote_migrate" in call_args[0][1]


def test_lxc_move_volume(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:move"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).move_volume("rootfs")
    assert result == "UPID:pve1:move"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/lxc/200/move_volume" in call_args[0][1]


def test_lxc_feature(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"hasFeature": True}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).feature("snapshot")
    assert result["hasFeature"] is True
    assert "/nodes/pve1/lxc/200/feature" in api._session.request.call_args[0][1]


def test_lxc_interfaces(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "eth0"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).interfaces()
    assert result == [{"name": "eth0"}]
    assert "/nodes/pve1/lxc/200/interfaces" in api._session.request.call_args[0][1]


def test_lxc_vncwebsocket(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"port": "5900"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).vncwebsocket(5900, "PVEVNC:ticket")
    assert result["port"] == "5900"
    assert "/nodes/pve1/lxc/200/vncwebsocket" in api._session.request.call_args[0][1]


def test_lxc_mtunnel(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"socket": "/run/mtunnel"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).mtunnel()
    assert "socket" in result
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/lxc/200/mtunnel" in call_args[0][1]


def test_lxc_firewall_aliases(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "myalias", "cidr": "10.0.0.0/24"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).firewall.list_aliases()
    assert result[0]["name"] == "myalias"
    assert "/nodes/pve1/lxc/200/firewall/aliases" in api._session.request.call_args[0][1]


def test_lxc_firewall_create_alias(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").lxc(200).firewall.create_alias("web", "10.0.0.0/24")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/lxc/200/firewall/aliases" in call_args[0][1]


def test_lxc_firewall_ipset(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "myset"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").lxc(200).firewall.list_ipset()
    assert result[0]["name"] == "myset"
    assert "/nodes/pve1/lxc/200/firewall/ipset" in api._session.request.call_args[0][1]


def test_lxc_firewall_create_ipset(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").lxc(200).firewall.create_ipset("myset")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/lxc/200/firewall/ipset" in call_args[0][1]


def test_lxc_firewall_add_ipset_entry(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").lxc(200).firewall.add_ipset_entry("myset", "10.0.0.1")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/lxc/200/firewall/ipset/myset" in call_args[0][1]


# ============================================================
# QEMU API
# ============================================================


def test_qemu_index(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"subdir": "config"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).index()
    assert result == [{"subdir": "config"}]
    url = api._session.request.call_args[0][1]
    assert url.endswith("/nodes/pve1/qemu/100")


def test_qemu_status_index(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"subdir": "current"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).status_index()
    assert result == [{"subdir": "current"}]
    assert "/nodes/pve1/qemu/100/status" in api._session.request.call_args[0][1]


def test_qemu_migrate_preconditions(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"running": 0, "local_disks": []}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).migrate_preconditions()
    assert result["running"] == 0
    call_args = api._session.request.call_args
    assert call_args[0][0] == "GET"
    assert "/nodes/pve1/qemu/100/migrate" in call_args[0][1]


def test_qemu_remote_migrate(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:rmig"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).remote_migrate()
    assert result == "UPID:pve1:rmig"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/qemu/100/remote_migrate" in call_args[0][1]


def test_qemu_unlink(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").qemu(100).unlink("unused0")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "PUT"
    assert "/nodes/pve1/qemu/100/unlink" in call_args[0][1]


def test_qemu_vncwebsocket(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"port": "5900"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).vncwebsocket(5900, "PVEVNC:ticket")
    assert result["port"] == "5900"
    assert "/nodes/pve1/qemu/100/vncwebsocket" in api._session.request.call_args[0][1]


def test_qemu_mtunnel(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"socket": "/run/mtunnel"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).mtunnel()
    assert "socket" in result
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/qemu/100/mtunnel" in call_args[0][1]


def test_qemu_dbus_vmstate(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").qemu(100).dbus_vmstate()
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/qemu/100/dbus-vmstate" in call_args[0][1]


def test_qemu_firewall_aliases(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "alias1"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).firewall.list_aliases()
    assert result[0]["name"] == "alias1"
    assert "/nodes/pve1/qemu/100/firewall/aliases" in api._session.request.call_args[0][1]


def test_qemu_firewall_create_alias(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").qemu(100).firewall.create_alias("web", "10.0.0.0/24")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/qemu/100/firewall/aliases" in call_args[0][1]


def test_qemu_firewall_ipset(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "blocklist"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).firewall.list_ipset()
    assert result[0]["name"] == "blocklist"
    assert "/nodes/pve1/qemu/100/firewall/ipset" in api._session.request.call_args[0][1]


def test_qemu_firewall_create_ipset(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").qemu(100).firewall.create_ipset("blocklist")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"


def test_qemu_firewall_add_ipset_entry(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").qemu(100).firewall.add_ipset_entry("blocklist", "192.168.1.0/24")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/qemu/100/firewall/ipset/blocklist" in call_args[0][1]


def test_qemu_agent_index(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "ping"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).agent.index()
    assert result == [{"name": "ping"}]
    call_args = api._session.request.call_args
    assert call_args[0][0] == "GET"
    url = call_args[0][1]
    assert url.endswith("/nodes/pve1/qemu/100/agent")


def test_qemu_agent_post(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"result": "ok"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").qemu(100).agent.post("ping")
    assert result["result"] == "ok"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    url = call_args[0][1]
    assert url.endswith("/nodes/pve1/qemu/100/agent")


# ============================================================
# Nodes API - Core methods
# ============================================================


def test_node_post_status(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:reboot"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").post_status("reboot")
    assert result == "UPID:pve1:reboot"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/status" in call_args[0][1]


def test_node_config(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"description": "primary node"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").config()
    assert result["description"] == "primary node"
    assert "/nodes/pve1/config" in api._session.request.call_args[0][1]


def test_node_update_config(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").update_config(description="updated")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "PUT"
    assert "/nodes/pve1/config" in call_args[0][1]


def test_node_version(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"version": "8.0.3"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").version()
    assert result["version"] == "8.0.3"
    assert "/nodes/pve1/version" in api._session.request.call_args[0][1]


def test_node_journal(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": ["line1", "line2"]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").journal()
    assert len(result) == 2
    assert "/nodes/pve1/journal" in api._session.request.call_args[0][1]


def test_node_hosts(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"data": "127.0.0.1 localhost"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").hosts()
    assert "data" in result
    assert "/nodes/pve1/hosts" in api._session.request.call_args[0][1]


def test_node_report(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "report text"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").report()
    assert result == "report text"
    assert "/nodes/pve1/report" in api._session.request.call_args[0][1]


def test_node_aplinfo(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"template": "debian-11"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").aplinfo()
    assert result[0]["template"] == "debian-11"
    assert "/nodes/pve1/aplinfo" in api._session.request.call_args[0][1]


def test_node_download_template(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:download"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").download_template("local", "debian-11-standard")
    assert result == "UPID:pve1:download"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/aplinfo" in call_args[0][1]


def test_node_startall(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:startall"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").startall()
    assert result == "UPID:pve1:startall"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/startall" in call_args[0][1]


def test_node_stopall(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:stopall"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").stopall()
    assert result == "UPID:pve1:stopall"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/stopall" in call_args[0][1]


def test_node_execute(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").execute("ls /tmp")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/execute" in call_args[0][1]


def test_node_wakeonlan(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:wol"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").wakeonlan()
    assert result == "UPID:pve1:wol"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/wakeonlan" in call_args[0][1]


def test_node_vzdump(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:vzdump"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").vzdump(vmid=100)
    assert result == "UPID:pve1:vzdump"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/vzdump" in call_args[0][1]


def test_node_vncshell(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"port": "5901", "ticket": "VNC:XX"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").vncshell()
    assert result["port"] == "5901"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/vncshell" in call_args[0][1]


def test_node_termproxy(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"port": "5901"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").termproxy()
    assert result["port"] == "5901"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/termproxy" in call_args[0][1]


def test_node_spiceshell(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"proxy": "pve1:3128"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").spiceshell()
    assert "proxy" in result
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/spiceshell" in call_args[0][1]


def test_node_subscription(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"status": "Active"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").subscription()
    assert result["status"] == "Active"
    assert "/nodes/pve1/subscription" in api._session.request.call_args[0][1]


def test_node_certificates(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").certificates()
    assert result == []
    assert "/nodes/pve1/certificates" in api._session.request.call_args[0][1]


def test_node_certificates_acme_order(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:acme"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").certificates_acme_order()
    assert result == "UPID:pve1:acme"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/certificates/acme/certificate" in call_args[0][1]


def test_node_upload_custom_certificate(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"filename": "/etc/pve/local/pve-ssl.pem"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").upload_custom_certificate("-----BEGIN CERT-----")
    assert "filename" in result
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/certificates/custom" in call_args[0][1]


# ============================================================
# Nodes API - Scan
# ============================================================


def test_node_scan_nfs(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"path": "/export", "options": "rw"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").scan.nfs("nas.local")
    assert result[0]["path"] == "/export"
    assert "/nodes/pve1/scan/nfs" in api._session.request.call_args[0][1]


def test_node_scan_cifs(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"share": "backup"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").scan.cifs("nas.local")
    assert result[0]["share"] == "backup"
    assert "/nodes/pve1/scan/cifs" in api._session.request.call_args[0][1]


def test_node_scan_zfs(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"pool": "rpool"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").scan.zfs()
    assert result[0]["pool"] == "rpool"
    assert "/nodes/pve1/scan/zfs" in api._session.request.call_args[0][1]


def test_node_scan_lvm(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"vg": "pve"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").scan.lvm()
    assert result[0]["vg"] == "pve"
    assert "/nodes/pve1/scan/lvm" in api._session.request.call_args[0][1]


def test_node_scan_iscsi(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"target": "iqn.2023-01.com.example:storage"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").scan.iscsi("192.168.1.100")
    assert "iqn" in result[0]["target"]
    assert "/nodes/pve1/scan/iscsi" in api._session.request.call_args[0][1]


# ============================================================
# Nodes API - Hardware
# ============================================================


def test_node_hardware_pci(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": "0000:00:02.0"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").hardware.pci()
    assert result[0]["id"] == "0000:00:02.0"
    assert "/nodes/pve1/hardware/pci" in api._session.request.call_args[0][1]


def test_node_hardware_usb(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"vendid": "1234"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").hardware.usb()
    assert result[0]["vendid"] == "1234"
    assert "/nodes/pve1/hardware/usb" in api._session.request.call_args[0][1]


# ============================================================
# Nodes API - Capabilities
# ============================================================


def test_node_capabilities_qemu_cpu(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "host"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").capabilities.qemu_cpu()
    assert result[0]["name"] == "host"
    assert "/nodes/pve1/capabilities/qemu/cpu" in api._session.request.call_args[0][1]


def test_node_capabilities_qemu_machines(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": "pc-i440fx-8.0"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").capabilities.qemu_machines()
    assert result[0]["id"] == "pc-i440fx-8.0"
    assert "/nodes/pve1/capabilities/qemu/machines" in api._session.request.call_args[0][1]


# ============================================================
# Nodes API - Ceph
# ============================================================


def test_node_ceph_status(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"health": {"status": "HEALTH_OK"}}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").ceph.status()
    assert result["health"]["status"] == "HEALTH_OK"
    assert "/nodes/pve1/ceph/status" in api._session.request.call_args[0][1]


def test_node_ceph_list_osd(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": 0, "status": "up"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").ceph.list_osd()
    assert result[0]["id"] == 0
    assert "/nodes/pve1/ceph/osd" in api._session.request.call_args[0][1]


def test_node_ceph_list_mon(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "pve1"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").ceph.list_mon()
    assert result[0]["name"] == "pve1"
    assert "/nodes/pve1/ceph/mon" in api._session.request.call_args[0][1]


def test_node_ceph_list_pool(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"pool_name": "rbd"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").ceph.list_pool()
    assert result[0]["pool_name"] == "rbd"
    assert "/nodes/pve1/ceph/pool" in api._session.request.call_args[0][1]


def test_node_ceph_create_pool(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:cephpool"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").ceph.create_pool("mypool")
    assert result == "UPID:pve1:cephpool"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/ceph/pool" in call_args[0][1]


# ============================================================
# Nodes API - Replication
# ============================================================


def test_node_replication_list(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": "100-0"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").replication.list()
    assert result[0]["id"] == "100-0"
    assert "/nodes/pve1/replication" in api._session.request.call_args[0][1]


def test_node_replication_schedule_now(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:rep"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").replication.schedule_now("100-0")
    assert result == "UPID:pve1:rep"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/replication/100-0/schedule_now" in call_args[0][1]


# ============================================================
# Nodes API - SDN
# ============================================================


def test_node_sdn_zones(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"zone": "localzone"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").sdn.zones()
    assert result[0]["zone"] == "localzone"
    assert "/nodes/pve1/sdn/zones" in api._session.request.call_args[0][1]


# ============================================================
# Nodes API - Storage expanded
# ============================================================


def test_node_get_storage(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"storage": "local", "type": "dir"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").get_storage("local")
    assert result["type"] == "dir"
    assert "/nodes/pve1/storage/local" in api._session.request.call_args[0][1]


def test_node_storage_status(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"total": 1000, "used": 500}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").storage_status("local")
    assert result["total"] == 1000
    assert "/nodes/pve1/storage/local/status" in api._session.request.call_args[0][1]


def test_node_storage_rrd(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"filename": "rrd.png"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").storage_rrd("local", timeframe="hour")
    assert "filename" in result
    assert "/nodes/pve1/storage/local/rrd" in api._session.request.call_args[0][1]


def test_node_create_storage_content(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:alloc"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").create_storage_content("local-lvm", filename="vm-100-disk-0", size="10G")
    assert result == "UPID:pve1:alloc"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/storage/local-lvm/content" in call_args[0][1]


def test_node_storage_download_url(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve1:dl"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").storage_download_url(
        "local", "https://example.com/image.qcow2", "image.qcow2"
    )
    assert result == "UPID:pve1:dl"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/nodes/pve1/storage/local/download-url" in call_args[0][1]


# ============================================================
# Nodes API - APT expanded
# ============================================================


def test_node_apt_changelog(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "changelog text"}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").apt_changelog("pve-manager")
    assert result == "changelog text"
    assert "/nodes/pve1/apt/changelog" in api._session.request.call_args[0][1]


def test_node_apt_repositories(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"files": []}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").apt_repositories()
    assert "files" in result
    assert "/nodes/pve1/apt/repositories" in api._session.request.call_args[0][1]


def test_node_apt_versions(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"Package": "pve-manager"}]}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").apt_versions()
    assert result[0]["Package"] == "pve-manager"
    assert "/nodes/pve1/apt/versions" in api._session.request.call_args[0][1]


# ============================================================
# Nodes API - Network expanded
# ============================================================


def test_node_get_network_iface(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"iface": "vmbr0", "type": "bridge"}}
    api._session.request.return_value = mock_resp

    result = api.nodes("pve1").get_network_iface("vmbr0")
    assert result["type"] == "bridge"
    assert "/nodes/pve1/network/vmbr0" in api._session.request.call_args[0][1]


def test_node_revert_network(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").revert_network()
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/nodes/pve1/network" in call_args[0][1]


def test_node_apply_network(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.nodes("pve1").apply_network()
    call_args = api._session.request.call_args
    assert call_args[0][0] == "PUT"
    assert "/nodes/pve1/network" in call_args[0][1]


# ============================================================
# Cluster API - Config
# ============================================================


def test_cluster_config_index(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    api._session.request.return_value = mock_resp

    result = api.cluster.config.index()
    assert result == []
    assert "/cluster/config" in api._session.request.call_args[0][1]


def test_cluster_config_apiversion(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": 1}
    api._session.request.return_value = mock_resp

    result = api.cluster.config.apiversion()
    assert result == 1
    assert "/cluster/config/apiversion" in api._session.request.call_args[0][1]


def test_cluster_config_list_nodes(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"node": "pve1"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.config.list_nodes()
    assert result[0]["node"] == "pve1"
    assert "/cluster/config/nodes" in api._session.request.call_args[0][1]


def test_cluster_config_add_node(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"corosync_conf": "..."}}
    api._session.request.return_value = mock_resp

    result = api.cluster.config.add_node("pve2")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/config/nodes/pve2" in call_args[0][1]


def test_cluster_config_join(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": "UPID:pve2:join"}
    api._session.request.return_value = mock_resp

    result = api.cluster.config.join(hostname="pve2", fingerprint="AA:BB")
    assert result == "UPID:pve2:join"
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/config/join" in call_args[0][1]


# ============================================================
# Cluster API - Metrics
# ============================================================


def test_cluster_metrics_list_servers(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": "influx1"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.metrics.list_servers()
    assert result[0]["id"] == "influx1"
    assert "/cluster/metrics/server" in api._session.request.call_args[0][1]


def test_cluster_metrics_create_server(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.metrics.create_server("influx1", "influxdb", 8086)
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/metrics/server/influx1" in call_args[0][1]


# ============================================================
# Cluster API - Notifications
# ============================================================


def test_cluster_notifications_list_sendmail(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "default"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.notifications.list_sendmail()
    assert result[0]["name"] == "default"
    assert "/cluster/notifications/endpoints/sendmail" in api._session.request.call_args[0][1]


def test_cluster_notifications_create_sendmail(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.notifications.create_sendmail("alert1", mailto="admin@example.com")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/notifications/endpoints/sendmail" in call_args[0][1]


def test_cluster_notifications_list_matchers(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "matcher1"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.notifications.list_matchers()
    assert result[0]["name"] == "matcher1"
    assert "/cluster/notifications/matchers" in api._session.request.call_args[0][1]


def test_cluster_notifications_create_matcher(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.notifications.create_matcher("matcher1")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/notifications/matchers" in call_args[0][1]


# ============================================================
# Cluster API - ACME
# ============================================================


def test_cluster_acme_list_plugins(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"plugin": "standalone"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.acme.list_plugins()
    assert result[0]["plugin"] == "standalone"
    assert "/cluster/acme/plugins" in api._session.request.call_args[0][1]


def test_cluster_acme_create_plugin(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.acme.create_plugin("myplugin", "standalone")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/acme/plugins" in call_args[0][1]


def test_cluster_acme_list_accounts(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "default"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.acme.list_accounts()
    assert result[0]["name"] == "default"
    assert "/cluster/acme/account" in api._session.request.call_args[0][1]


# ============================================================
# Cluster API - Ceph
# ============================================================


def test_cluster_ceph_status(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"health": {"status": "HEALTH_OK"}}}
    api._session.request.return_value = mock_resp

    result = api.cluster.ceph.status()
    assert result["health"]["status"] == "HEALTH_OK"
    assert "/cluster/ceph/status" in api._session.request.call_args[0][1]


def test_cluster_ceph_flags(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "noout"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.ceph.flags()
    assert result[0]["name"] == "noout"
    assert "/cluster/ceph/flags" in api._session.request.call_args[0][1]


def test_cluster_ceph_set_flag(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.ceph.set_flag("noout")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "PUT"
    assert "/cluster/ceph/flags/noout" in call_args[0][1]


# ============================================================
# Cluster API - Jobs
# ============================================================


def test_cluster_jobs_list_realm_sync(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": "rsync1"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.jobs.list_realm_sync()
    assert result[0]["id"] == "rsync1"
    assert "/cluster/jobs/realm-sync" in api._session.request.call_args[0][1]


def test_cluster_jobs_schedule_analyze(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"timestamp": 1700000000}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.jobs.schedule_analyze(schedule="*/5")
    assert "timestamp" in result[0]
    assert "/cluster/jobs/schedule-analyze" in api._session.request.call_args[0][1]


# ============================================================
# Cluster API - Mapping
# ============================================================


def test_cluster_mapping_list_dir(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": "dir1"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.mapping.list_dir()
    assert result[0]["id"] == "dir1"
    assert "/cluster/mapping/dir" in api._session.request.call_args[0][1]


def test_cluster_mapping_list_pci(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": "gpu0"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.mapping.list_pci()
    assert result[0]["id"] == "gpu0"
    assert "/cluster/mapping/pci" in api._session.request.call_args[0][1]


def test_cluster_mapping_list_usb(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"id": "usb0"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.mapping.list_usb()
    assert result[0]["id"] == "usb0"
    assert "/cluster/mapping/usb" in api._session.request.call_args[0][1]


def test_cluster_mapping_create_pci(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.mapping.create_pci("gpu0", map="node=pve1,path=0000:00:02.0")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/mapping/pci" in call_args[0][1]


# ============================================================
# Cluster API - Bulk Action
# ============================================================


def test_cluster_bulk_action_guest_start(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    api._session.request.return_value = mock_resp

    api.cluster.bulk_action.guest_start()
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/bulk-action/guest/start" in call_args[0][1]


def test_cluster_bulk_action_guest_shutdown(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    api._session.request.return_value = mock_resp

    api.cluster.bulk_action.guest_shutdown()
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/bulk-action/guest/shutdown" in call_args[0][1]


# ============================================================
# Cluster API - SDN
# ============================================================


def test_cluster_sdn_list_vnets(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"vnet": "vnet0"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.sdn.list_vnets()
    assert result[0]["vnet"] == "vnet0"
    assert "/cluster/sdn/vnets" in api._session.request.call_args[0][1]


def test_cluster_sdn_create_vnet(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.sdn.create_vnet("vnet0", "zone1")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/sdn/vnets" in call_args[0][1]


def test_cluster_sdn_list_zones(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"zone": "zone1"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.sdn.list_zones()
    assert result[0]["zone"] == "zone1"
    assert "/cluster/sdn/zones" in api._session.request.call_args[0][1]


def test_cluster_sdn_list_controllers(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"controller": "evpn1"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.sdn.list_controllers()
    assert result[0]["controller"] == "evpn1"
    assert "/cluster/sdn/controllers" in api._session.request.call_args[0][1]


def test_cluster_sdn_list_ipams(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"ipam": "pve"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.sdn.list_ipams()
    assert result[0]["ipam"] == "pve"
    assert "/cluster/sdn/ipams" in api._session.request.call_args[0][1]


def test_cluster_sdn_create_zone(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.sdn.create_zone("zone1", "vlan")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/sdn/zones" in call_args[0][1]


def test_cluster_sdn_create_controller(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.sdn.create_controller("evpn1", "evpn")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/sdn/controllers" in call_args[0][1]


def test_cluster_sdn_create_ipam(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.sdn.create_ipam("pve", "pve")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/sdn/ipams" in call_args[0][1]


# ============================================================
# Cluster API - Firewall expanded
# ============================================================


def test_cluster_firewall_list_groups(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"group": "webservers"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.firewall.list_groups()
    assert result[0]["group"] == "webservers"
    assert "/cluster/firewall/groups" in api._session.request.call_args[0][1]


def test_cluster_firewall_create_group(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.firewall.create_group(group="webservers")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/firewall/groups" in call_args[0][1]


def test_cluster_firewall_get_group(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"pos": 0}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.firewall.get_group("webservers")
    assert result == [{"pos": 0}]
    assert "/cluster/firewall/groups/webservers" in api._session.request.call_args[0][1]


def test_cluster_firewall_delete_group(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.firewall.delete_group("webservers")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/cluster/firewall/groups/webservers" in call_args[0][1]


def test_cluster_firewall_list_aliases(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "mynet"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.firewall.list_aliases()
    assert result[0]["name"] == "mynet"
    assert "/cluster/firewall/aliases" in api._session.request.call_args[0][1]


def test_cluster_firewall_create_alias(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.firewall.create_alias("mynet", "10.0.0.0/8")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/firewall/aliases" in call_args[0][1]


def test_cluster_firewall_delete_alias(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.firewall.delete_alias("mynet")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/cluster/firewall/aliases/mynet" in call_args[0][1]


def test_cluster_firewall_list_ipset(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"name": "blocklist"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.firewall.list_ipset()
    assert result[0]["name"] == "blocklist"
    assert "/cluster/firewall/ipset" in api._session.request.call_args[0][1]


def test_cluster_firewall_create_ipset(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.firewall.create_ipset("blocklist")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/firewall/ipset" in call_args[0][1]


def test_cluster_firewall_add_ipset_entry(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.firewall.add_ipset_entry("blocklist", "192.168.1.0/24")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/firewall/ipset/blocklist" in call_args[0][1]


def test_cluster_firewall_macros(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"macro": "SSH"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.firewall.macros()
    assert result[0]["macro"] == "SSH"
    assert "/cluster/firewall/macros" in api._session.request.call_args[0][1]


# ============================================================
# Cluster API - HA expanded
# ============================================================


def test_cluster_ha_manager_status(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"manager_status": "active"}}
    api._session.request.return_value = mock_resp

    result = api.cluster.ha.manager_status()
    assert "manager_status" in result
    assert "/cluster/ha/status/manager_status" in api._session.request.call_args[0][1]


def test_cluster_ha_migrate_resource(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.ha.migrate_resource("vm:100", "pve2")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/ha/resources/vm:100/migrate" in call_args[0][1]


def test_cluster_ha_list_groups(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"group": "grp1"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.ha.list_groups()
    assert result[0]["group"] == "grp1"
    assert "/cluster/ha/groups" in api._session.request.call_args[0][1]


def test_cluster_ha_create_group(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.ha.create_group("grp1", "pve1,pve2")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/ha/groups" in call_args[0][1]


def test_cluster_ha_delete_group(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.ha.delete_group("grp1")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/cluster/ha/groups/grp1" in call_args[0][1]


def test_cluster_ha_list_rules(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"rule": "rule1"}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.ha.list_rules()
    assert result[0]["rule"] == "rule1"
    assert "/cluster/ha/rules" in api._session.request.call_args[0][1]


def test_cluster_ha_create_rule(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.ha.create_rule(type="location")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "POST"
    assert "/cluster/ha/rules" in call_args[0][1]


def test_cluster_ha_delete_rule(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": None}
    api._session.request.return_value = mock_resp

    api.cluster.ha.delete_rule("rule1")
    call_args = api._session.request.call_args
    assert call_args[0][0] == "DELETE"
    assert "/cluster/ha/rules/rule1" in call_args[0][1]


# ============================================================
# Cluster API - Backup expanded
# ============================================================


def test_cluster_backup_included_volumes(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": {"children": []}}
    api._session.request.return_value = mock_resp

    result = api.cluster.backup.included_volumes("backup-job1")
    assert "children" in result
    assert "/cluster/backup/backup-job1/included_volumes" in api._session.request.call_args[0][1]


# ============================================================
# Cluster API - Backup Info
# ============================================================


def test_cluster_backup_info_not_backed_up(api: ProxmoxAPI) -> None:
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [{"vmid": 100}]}
    api._session.request.return_value = mock_resp

    result = api.cluster.backup_info.not_backed_up()
    assert result[0]["vmid"] == 100
    assert "/cluster/backup-info/not-backed-up" in api._session.request.call_args[0][1]
