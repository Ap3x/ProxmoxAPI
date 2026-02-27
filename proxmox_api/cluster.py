"""Cluster-level API resources."""

from __future__ import annotations

from typing import Any

from proxmox_api._base import _ResourceBase


class _ClusterAPI(_ResourceBase):

    def index(self) -> Any:
        """GET /cluster"""
        return self._client.get("/cluster")

    def status(self) -> Any:
        """GET /cluster/status - Get cluster status information."""
        return self._client.get("/cluster/status")

    def resources(self, type: str | None = None) -> Any:
        """GET /cluster/resources - Resources index (cluster wide)."""
        return self._client.get("/cluster/resources", type=type)

    def tasks(self, **kwargs: Any) -> Any:
        """GET /cluster/tasks - List recent tasks (cluster wide)."""
        return self._client.get("/cluster/tasks", **kwargs)

    def options(self) -> Any:
        """GET /cluster/options - Get datacenter options."""
        return self._client.get("/cluster/options")

    def set_options(self, **kwargs: Any) -> Any:
        """PUT /cluster/options - Set datacenter options."""
        return self._client.put("/cluster/options", **kwargs)

    def nextid(self, **kwargs: Any) -> Any:
        """GET /cluster/nextid - Get next free VMID."""
        return self._client.get("/cluster/nextid", **kwargs)

    def log(self, **kwargs: Any) -> Any:
        """GET /cluster/log - Read cluster log."""
        return self._client.get("/cluster/log", **kwargs)

    @property
    def firewall(self) -> _ClusterFirewallAPI:
        return _ClusterFirewallAPI(self._client)

    @property
    def ha(self) -> _ClusterHAAPI:
        return _ClusterHAAPI(self._client)

    @property
    def replication(self) -> _ClusterReplicationAPI:
        return _ClusterReplicationAPI(self._client)

    @property
    def backup(self) -> _ClusterBackupAPI:
        return _ClusterBackupAPI(self._client)

    @property
    def backup_info(self) -> _ClusterBackupInfoAPI:
        return _ClusterBackupInfoAPI(self._client)

    @property
    def config(self) -> _ClusterConfigAPI:
        return _ClusterConfigAPI(self._client)

    @property
    def metrics(self) -> _ClusterMetricsAPI:
        return _ClusterMetricsAPI(self._client)

    @property
    def notifications(self) -> _ClusterNotificationsAPI:
        return _ClusterNotificationsAPI(self._client)

    @property
    def acme(self) -> _ClusterAcmeAPI:
        return _ClusterAcmeAPI(self._client)

    @property
    def ceph(self) -> _ClusterCephAPI:
        return _ClusterCephAPI(self._client)

    @property
    def jobs(self) -> _ClusterJobsAPI:
        return _ClusterJobsAPI(self._client)

    @property
    def mapping(self) -> _ClusterMappingAPI:
        return _ClusterMappingAPI(self._client)

    @property
    def bulk_action(self) -> _ClusterBulkActionAPI:
        return _ClusterBulkActionAPI(self._client)

    @property
    def sdn(self) -> _ClusterSDNAPI:
        return _ClusterSDNAPI(self._client)


# --- Firewall ---

class _ClusterFirewallAPI(_ResourceBase):

    _base = "/cluster/firewall"

    def index(self) -> Any:
        """GET /cluster/firewall"""
        return self._client.get(self._base)

    def list_rules(self) -> Any:
        """GET /cluster/firewall/rules"""
        return self._client.get(f"{self._base}/rules")

    def get_rule(self, pos: int) -> Any:
        """GET /cluster/firewall/rules/{pos}"""
        return self._client.get(f"{self._base}/rules/{pos}")

    def create_rule(self, **kwargs: Any) -> Any:
        """POST /cluster/firewall/rules"""
        return self._client.post(f"{self._base}/rules", **kwargs)

    def update_rule(self, pos: int, **kwargs: Any) -> Any:
        """PUT /cluster/firewall/rules/{pos}"""
        return self._client.put(f"{self._base}/rules/{pos}", **kwargs)

    def delete_rule(self, pos: int) -> Any:
        """DELETE /cluster/firewall/rules/{pos}"""
        return self._client.delete(f"{self._base}/rules/{pos}")

    def options(self) -> Any:
        """GET /cluster/firewall/options"""
        return self._client.get(f"{self._base}/options")

    def set_options(self, **kwargs: Any) -> Any:
        """PUT /cluster/firewall/options"""
        return self._client.put(f"{self._base}/options", **kwargs)

    def macros(self) -> Any:
        """GET /cluster/firewall/macros"""
        return self._client.get(f"{self._base}/macros")

    def refs(self, **kwargs: Any) -> Any:
        """GET /cluster/firewall/refs"""
        return self._client.get(f"{self._base}/refs", **kwargs)

    # --- Groups ---

    def list_groups(self) -> Any:
        """GET /cluster/firewall/groups"""
        return self._client.get(f"{self._base}/groups")

    def create_group(self, **kwargs: Any) -> Any:
        """POST /cluster/firewall/groups"""
        return self._client.post(f"{self._base}/groups", **kwargs)

    def get_group(self, group: str) -> Any:
        """GET /cluster/firewall/groups/{group}"""
        return self._client.get(f"{self._base}/groups/{group}")

    def delete_group(self, group: str) -> Any:
        """DELETE /cluster/firewall/groups/{group}"""
        return self._client.delete(f"{self._base}/groups/{group}")

    def create_group_rule(self, group: str, **kwargs: Any) -> Any:
        """POST /cluster/firewall/groups/{group}"""
        return self._client.post(f"{self._base}/groups/{group}", **kwargs)

    def get_group_rule(self, group: str, pos: int) -> Any:
        """GET /cluster/firewall/groups/{group}/{pos}"""
        return self._client.get(f"{self._base}/groups/{group}/{pos}")

    def update_group_rule(self, group: str, pos: int, **kwargs: Any) -> Any:
        """PUT /cluster/firewall/groups/{group}/{pos}"""
        return self._client.put(f"{self._base}/groups/{group}/{pos}", **kwargs)

    def delete_group_rule(self, group: str, pos: int) -> Any:
        """DELETE /cluster/firewall/groups/{group}/{pos}"""
        return self._client.delete(f"{self._base}/groups/{group}/{pos}")

    # --- Aliases ---

    def list_aliases(self) -> Any:
        """GET /cluster/firewall/aliases"""
        return self._client.get(f"{self._base}/aliases")

    def get_alias(self, name: str) -> Any:
        """GET /cluster/firewall/aliases/{name}"""
        return self._client.get(f"{self._base}/aliases/{name}")

    def create_alias(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """POST /cluster/firewall/aliases"""
        return self._client.post(
            f"{self._base}/aliases", name=name, cidr=cidr, **kwargs
        )

    def update_alias(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """PUT /cluster/firewall/aliases/{name}"""
        return self._client.put(
            f"{self._base}/aliases/{name}", cidr=cidr, **kwargs
        )

    def delete_alias(self, name: str) -> Any:
        """DELETE /cluster/firewall/aliases/{name}"""
        return self._client.delete(f"{self._base}/aliases/{name}")

    # --- IPSet ---

    def list_ipset(self) -> Any:
        """GET /cluster/firewall/ipset"""
        return self._client.get(f"{self._base}/ipset")

    def create_ipset(self, name: str, **kwargs: Any) -> Any:
        """POST /cluster/firewall/ipset"""
        return self._client.post(f"{self._base}/ipset", name=name, **kwargs)

    def get_ipset(self, name: str) -> Any:
        """GET /cluster/firewall/ipset/{name}"""
        return self._client.get(f"{self._base}/ipset/{name}")

    def delete_ipset(self, name: str) -> Any:
        """DELETE /cluster/firewall/ipset/{name}"""
        return self._client.delete(f"{self._base}/ipset/{name}")

    def add_ipset_entry(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """POST /cluster/firewall/ipset/{name}"""
        return self._client.post(
            f"{self._base}/ipset/{name}", cidr=cidr, **kwargs
        )

    def get_ipset_entry(self, name: str, cidr: str) -> Any:
        """GET /cluster/firewall/ipset/{name}/{cidr}"""
        return self._client.get(f"{self._base}/ipset/{name}/{cidr}")

    def update_ipset_entry(self, name: str, cidr: str, **kwargs: Any) -> Any:
        """PUT /cluster/firewall/ipset/{name}/{cidr}"""
        return self._client.put(f"{self._base}/ipset/{name}/{cidr}", **kwargs)

    def delete_ipset_entry(self, name: str, cidr: str) -> Any:
        """DELETE /cluster/firewall/ipset/{name}/{cidr}"""
        return self._client.delete(f"{self._base}/ipset/{name}/{cidr}")


# --- HA ---

class _ClusterHAAPI(_ResourceBase):

    _base = "/cluster/ha"

    def index(self) -> Any:
        """GET /cluster/ha"""
        return self._client.get(self._base)

    def status_index(self) -> Any:
        """GET /cluster/ha/status"""
        return self._client.get(f"{self._base}/status")

    def status(self) -> Any:
        """GET /cluster/ha/status/current"""
        return self._client.get(f"{self._base}/status/current")

    def manager_status(self) -> Any:
        """GET /cluster/ha/status/manager_status"""
        return self._client.get(f"{self._base}/status/manager_status")

    # --- Resources ---

    def list_resources(self) -> Any:
        """GET /cluster/ha/resources"""
        return self._client.get(f"{self._base}/resources")

    def get_resource(self, sid: str) -> Any:
        """GET /cluster/ha/resources/{sid}"""
        return self._client.get(f"{self._base}/resources/{sid}")

    def create_resource(self, sid: str, **kwargs: Any) -> Any:
        """POST /cluster/ha/resources"""
        return self._client.post(f"{self._base}/resources", sid=sid, **kwargs)

    def update_resource(self, sid: str, **kwargs: Any) -> Any:
        """PUT /cluster/ha/resources/{sid}"""
        return self._client.put(f"{self._base}/resources/{sid}", **kwargs)

    def delete_resource(self, sid: str) -> Any:
        """DELETE /cluster/ha/resources/{sid}"""
        return self._client.delete(f"{self._base}/resources/{sid}")

    def migrate_resource(self, sid: str, node: str, **kwargs: Any) -> Any:
        """POST /cluster/ha/resources/{sid}/migrate"""
        return self._client.post(
            f"{self._base}/resources/{sid}/migrate", node=node, **kwargs
        )

    def relocate_resource(self, sid: str, node: str, **kwargs: Any) -> Any:
        """POST /cluster/ha/resources/{sid}/relocate"""
        return self._client.post(
            f"{self._base}/resources/{sid}/relocate", node=node, **kwargs
        )

    # --- Groups ---

    def list_groups(self) -> Any:
        """GET /cluster/ha/groups"""
        return self._client.get(f"{self._base}/groups")

    def get_group(self, group: str) -> Any:
        """GET /cluster/ha/groups/{group}"""
        return self._client.get(f"{self._base}/groups/{group}")

    def create_group(self, group: str, nodes: str, **kwargs: Any) -> Any:
        """POST /cluster/ha/groups"""
        return self._client.post(
            f"{self._base}/groups", group=group, nodes=nodes, **kwargs
        )

    def update_group(self, group: str, **kwargs: Any) -> Any:
        """PUT /cluster/ha/groups/{group}"""
        return self._client.put(f"{self._base}/groups/{group}", **kwargs)

    def delete_group(self, group: str) -> Any:
        """DELETE /cluster/ha/groups/{group}"""
        return self._client.delete(f"{self._base}/groups/{group}")

    # --- Rules ---

    def list_rules(self) -> Any:
        """GET /cluster/ha/rules"""
        return self._client.get(f"{self._base}/rules")

    def get_rule(self, rule: str) -> Any:
        """GET /cluster/ha/rules/{rule}"""
        return self._client.get(f"{self._base}/rules/{rule}")

    def create_rule(self, **kwargs: Any) -> Any:
        """POST /cluster/ha/rules"""
        return self._client.post(f"{self._base}/rules", **kwargs)

    def update_rule(self, rule: str, **kwargs: Any) -> Any:
        """PUT /cluster/ha/rules/{rule}"""
        return self._client.put(f"{self._base}/rules/{rule}", **kwargs)

    def delete_rule(self, rule: str) -> Any:
        """DELETE /cluster/ha/rules/{rule}"""
        return self._client.delete(f"{self._base}/rules/{rule}")


# --- Replication ---

class _ClusterReplicationAPI(_ResourceBase):

    def list(self) -> Any:
        """GET /cluster/replication"""
        return self._client.get("/cluster/replication")

    def get(self, id: str) -> Any:
        """GET /cluster/replication/{id}"""
        return self._client.get(f"/cluster/replication/{id}")

    def create(self, id: str, target: str, type: str, **kwargs: Any) -> Any:
        """POST /cluster/replication"""
        return self._client.post(
            "/cluster/replication", id=id, target=target, type=type, **kwargs
        )

    def update(self, id: str, **kwargs: Any) -> Any:
        """PUT /cluster/replication/{id}"""
        return self._client.put(f"/cluster/replication/{id}", **kwargs)

    def delete(self, id: str, **kwargs: Any) -> Any:
        """DELETE /cluster/replication/{id}"""
        return self._client.delete(f"/cluster/replication/{id}", **kwargs)


# --- Backup ---

class _ClusterBackupAPI(_ResourceBase):

    def list(self) -> Any:
        """GET /cluster/backup"""
        return self._client.get("/cluster/backup")

    def get(self, id: str) -> Any:
        """GET /cluster/backup/{id}"""
        return self._client.get(f"/cluster/backup/{id}")

    def create(self, **kwargs: Any) -> Any:
        """POST /cluster/backup"""
        return self._client.post("/cluster/backup", **kwargs)

    def update(self, id: str, **kwargs: Any) -> Any:
        """PUT /cluster/backup/{id}"""
        return self._client.put(f"/cluster/backup/{id}", **kwargs)

    def delete(self, id: str) -> Any:
        """DELETE /cluster/backup/{id}"""
        return self._client.delete(f"/cluster/backup/{id}")

    def included_volumes(self, id: str) -> Any:
        """GET /cluster/backup/{id}/included_volumes"""
        return self._client.get(f"/cluster/backup/{id}/included_volumes")


class _ClusterBackupInfoAPI(_ResourceBase):

    _base = "/cluster/backup-info"

    def index(self) -> Any:
        """GET /cluster/backup-info"""
        return self._client.get(self._base)

    def not_backed_up(self) -> Any:
        """GET /cluster/backup-info/not-backed-up"""
        return self._client.get(f"{self._base}/not-backed-up")


# --- Config ---

class _ClusterConfigAPI(_ResourceBase):

    _base = "/cluster/config"

    def index(self) -> Any:
        """GET /cluster/config"""
        return self._client.get(self._base)

    def create(self, clustername: str, **kwargs: Any) -> Any:
        """POST /cluster/config"""
        return self._client.post(self._base, clustername=clustername, **kwargs)

    def apiversion(self) -> Any:
        """GET /cluster/config/apiversion"""
        return self._client.get(f"{self._base}/apiversion")

    def totem(self) -> Any:
        """GET /cluster/config/totem"""
        return self._client.get(f"{self._base}/totem")

    def qdevice(self) -> Any:
        """GET /cluster/config/qdevice"""
        return self._client.get(f"{self._base}/qdevice")

    def list_nodes(self) -> Any:
        """GET /cluster/config/nodes"""
        return self._client.get(f"{self._base}/nodes")

    def add_node(self, node: str, **kwargs: Any) -> Any:
        """POST /cluster/config/nodes/{node}"""
        return self._client.post(f"{self._base}/nodes/{node}", **kwargs)

    def delete_node(self, node: str) -> Any:
        """DELETE /cluster/config/nodes/{node}"""
        return self._client.delete(f"{self._base}/nodes/{node}")

    def join_info(self, **kwargs: Any) -> Any:
        """GET /cluster/config/join"""
        return self._client.get(f"{self._base}/join", **kwargs)

    def join(self, **kwargs: Any) -> Any:
        """POST /cluster/config/join"""
        return self._client.post(f"{self._base}/join", **kwargs)


# --- Metrics ---

class _ClusterMetricsAPI(_ResourceBase):

    _base = "/cluster/metrics"

    def index(self) -> Any:
        """GET /cluster/metrics"""
        return self._client.get(self._base)

    def export(self) -> Any:
        """GET /cluster/metrics/export"""
        return self._client.get(f"{self._base}/export")

    def list_servers(self) -> Any:
        """GET /cluster/metrics/server"""
        return self._client.get(f"{self._base}/server")

    def get_server(self, id: str) -> Any:
        """GET /cluster/metrics/server/{id}"""
        return self._client.get(f"{self._base}/server/{id}")

    def create_server(self, id: str, type: str, port: int, **kwargs: Any) -> Any:
        """POST /cluster/metrics/server/{id}"""
        return self._client.post(
            f"{self._base}/server/{id}", type=type, port=port, **kwargs
        )

    def update_server(self, id: str, port: int, **kwargs: Any) -> Any:
        """PUT /cluster/metrics/server/{id}"""
        return self._client.put(
            f"{self._base}/server/{id}", port=port, **kwargs
        )

    def delete_server(self, id: str) -> Any:
        """DELETE /cluster/metrics/server/{id}"""
        return self._client.delete(f"{self._base}/server/{id}")


# --- Notifications ---

class _ClusterNotificationsAPI(_ResourceBase):

    _base = "/cluster/notifications"

    def index(self) -> Any:
        """GET /cluster/notifications"""
        return self._client.get(self._base)

    def matcher_fields(self) -> Any:
        """GET /cluster/notifications/matcher-fields"""
        return self._client.get(f"{self._base}/matcher-fields")

    def matcher_field_values(self) -> Any:
        """GET /cluster/notifications/matcher-field-values"""
        return self._client.get(f"{self._base}/matcher-field-values")

    def list_targets(self) -> Any:
        """GET /cluster/notifications/targets"""
        return self._client.get(f"{self._base}/targets")

    def test_target(self, name: str) -> Any:
        """POST /cluster/notifications/targets/{name}/test"""
        return self._client.post(f"{self._base}/targets/{name}/test")

    # --- Endpoints ---

    def endpoints_index(self) -> Any:
        """GET /cluster/notifications/endpoints"""
        return self._client.get(f"{self._base}/endpoints")

    # Sendmail
    def list_sendmail(self) -> Any:
        """GET /cluster/notifications/endpoints/sendmail"""
        return self._client.get(f"{self._base}/endpoints/sendmail")

    def get_sendmail(self, name: str) -> Any:
        """GET /cluster/notifications/endpoints/sendmail/{name}"""
        return self._client.get(f"{self._base}/endpoints/sendmail/{name}")

    def create_sendmail(self, name: str, **kwargs: Any) -> Any:
        """POST /cluster/notifications/endpoints/sendmail"""
        return self._client.post(
            f"{self._base}/endpoints/sendmail", name=name, **kwargs
        )

    def update_sendmail(self, name: str, **kwargs: Any) -> Any:
        """PUT /cluster/notifications/endpoints/sendmail/{name}"""
        return self._client.put(
            f"{self._base}/endpoints/sendmail/{name}", **kwargs
        )

    def delete_sendmail(self, name: str) -> Any:
        """DELETE /cluster/notifications/endpoints/sendmail/{name}"""
        return self._client.delete(f"{self._base}/endpoints/sendmail/{name}")

    # Gotify
    def list_gotify(self) -> Any:
        """GET /cluster/notifications/endpoints/gotify"""
        return self._client.get(f"{self._base}/endpoints/gotify")

    def get_gotify(self, name: str) -> Any:
        """GET /cluster/notifications/endpoints/gotify/{name}"""
        return self._client.get(f"{self._base}/endpoints/gotify/{name}")

    def create_gotify(self, name: str, server: str, **kwargs: Any) -> Any:
        """POST /cluster/notifications/endpoints/gotify"""
        return self._client.post(
            f"{self._base}/endpoints/gotify", name=name, server=server, **kwargs
        )

    def update_gotify(self, name: str, **kwargs: Any) -> Any:
        """PUT /cluster/notifications/endpoints/gotify/{name}"""
        return self._client.put(
            f"{self._base}/endpoints/gotify/{name}", **kwargs
        )

    def delete_gotify(self, name: str) -> Any:
        """DELETE /cluster/notifications/endpoints/gotify/{name}"""
        return self._client.delete(f"{self._base}/endpoints/gotify/{name}")

    # SMTP
    def list_smtp(self) -> Any:
        """GET /cluster/notifications/endpoints/smtp"""
        return self._client.get(f"{self._base}/endpoints/smtp")

    def get_smtp(self, name: str) -> Any:
        """GET /cluster/notifications/endpoints/smtp/{name}"""
        return self._client.get(f"{self._base}/endpoints/smtp/{name}")

    def create_smtp(self, name: str, **kwargs: Any) -> Any:
        """POST /cluster/notifications/endpoints/smtp"""
        return self._client.post(
            f"{self._base}/endpoints/smtp", name=name, **kwargs
        )

    def update_smtp(self, name: str, **kwargs: Any) -> Any:
        """PUT /cluster/notifications/endpoints/smtp/{name}"""
        return self._client.put(
            f"{self._base}/endpoints/smtp/{name}", **kwargs
        )

    def delete_smtp(self, name: str) -> Any:
        """DELETE /cluster/notifications/endpoints/smtp/{name}"""
        return self._client.delete(f"{self._base}/endpoints/smtp/{name}")

    # Webhook
    def list_webhook(self) -> Any:
        """GET /cluster/notifications/endpoints/webhook"""
        return self._client.get(f"{self._base}/endpoints/webhook")

    def get_webhook(self, name: str) -> Any:
        """GET /cluster/notifications/endpoints/webhook/{name}"""
        return self._client.get(f"{self._base}/endpoints/webhook/{name}")

    def create_webhook(self, name: str, **kwargs: Any) -> Any:
        """POST /cluster/notifications/endpoints/webhook"""
        return self._client.post(
            f"{self._base}/endpoints/webhook", name=name, **kwargs
        )

    def update_webhook(self, name: str, **kwargs: Any) -> Any:
        """PUT /cluster/notifications/endpoints/webhook/{name}"""
        return self._client.put(
            f"{self._base}/endpoints/webhook/{name}", **kwargs
        )

    def delete_webhook(self, name: str) -> Any:
        """DELETE /cluster/notifications/endpoints/webhook/{name}"""
        return self._client.delete(f"{self._base}/endpoints/webhook/{name}")

    # --- Matchers ---

    def list_matchers(self) -> Any:
        """GET /cluster/notifications/matchers"""
        return self._client.get(f"{self._base}/matchers")

    def get_matcher(self, name: str) -> Any:
        """GET /cluster/notifications/matchers/{name}"""
        return self._client.get(f"{self._base}/matchers/{name}")

    def create_matcher(self, name: str, **kwargs: Any) -> Any:
        """POST /cluster/notifications/matchers"""
        return self._client.post(
            f"{self._base}/matchers", name=name, **kwargs
        )

    def update_matcher(self, name: str, **kwargs: Any) -> Any:
        """PUT /cluster/notifications/matchers/{name}"""
        return self._client.put(f"{self._base}/matchers/{name}", **kwargs)

    def delete_matcher(self, name: str) -> Any:
        """DELETE /cluster/notifications/matchers/{name}"""
        return self._client.delete(f"{self._base}/matchers/{name}")


# --- ACME ---

class _ClusterAcmeAPI(_ResourceBase):

    _base = "/cluster/acme"

    def index(self) -> Any:
        """GET /cluster/acme"""
        return self._client.get(self._base)

    def tos(self, **kwargs: Any) -> Any:
        """GET /cluster/acme/tos"""
        return self._client.get(f"{self._base}/tos", **kwargs)

    def meta(self, **kwargs: Any) -> Any:
        """GET /cluster/acme/meta"""
        return self._client.get(f"{self._base}/meta", **kwargs)

    def directories(self) -> Any:
        """GET /cluster/acme/directories"""
        return self._client.get(f"{self._base}/directories")

    def challenge_schema(self) -> Any:
        """GET /cluster/acme/challenge-schema"""
        return self._client.get(f"{self._base}/challenge-schema")

    # Plugins
    def list_plugins(self) -> Any:
        """GET /cluster/acme/plugins"""
        return self._client.get(f"{self._base}/plugins")

    def get_plugin(self, id: str) -> Any:
        """GET /cluster/acme/plugins/{id}"""
        return self._client.get(f"{self._base}/plugins/{id}")

    def create_plugin(self, id: str, type: str, **kwargs: Any) -> Any:
        """POST /cluster/acme/plugins"""
        return self._client.post(
            f"{self._base}/plugins", id=id, type=type, **kwargs
        )

    def update_plugin(self, id: str, **kwargs: Any) -> Any:
        """PUT /cluster/acme/plugins/{id}"""
        return self._client.put(f"{self._base}/plugins/{id}", **kwargs)

    def delete_plugin(self, id: str) -> Any:
        """DELETE /cluster/acme/plugins/{id}"""
        return self._client.delete(f"{self._base}/plugins/{id}")

    # Accounts
    def list_accounts(self) -> Any:
        """GET /cluster/acme/account"""
        return self._client.get(f"{self._base}/account")

    def get_account(self, name: str) -> Any:
        """GET /cluster/acme/account/{name}"""
        return self._client.get(f"{self._base}/account/{name}")

    def create_account(self, contact: str, **kwargs: Any) -> Any:
        """POST /cluster/acme/account"""
        return self._client.post(
            f"{self._base}/account", contact=contact, **kwargs
        )

    def update_account(self, name: str, **kwargs: Any) -> Any:
        """PUT /cluster/acme/account/{name}"""
        return self._client.put(f"{self._base}/account/{name}", **kwargs)

    def delete_account(self, name: str) -> Any:
        """DELETE /cluster/acme/account/{name}"""
        return self._client.delete(f"{self._base}/account/{name}")


# --- Ceph ---

class _ClusterCephAPI(_ResourceBase):

    _base = "/cluster/ceph"

    def index(self) -> Any:
        """GET /cluster/ceph"""
        return self._client.get(self._base)

    def metadata(self, **kwargs: Any) -> Any:
        """GET /cluster/ceph/metadata"""
        return self._client.get(f"{self._base}/metadata", **kwargs)

    def status(self) -> Any:
        """GET /cluster/ceph/status"""
        return self._client.get(f"{self._base}/status")

    def flags(self) -> Any:
        """GET /cluster/ceph/flags"""
        return self._client.get(f"{self._base}/flags")

    def set_flags(self, **kwargs: Any) -> Any:
        """PUT /cluster/ceph/flags"""
        return self._client.put(f"{self._base}/flags", **kwargs)

    def get_flag(self, flag: str) -> Any:
        """GET /cluster/ceph/flags/{flag}"""
        return self._client.get(f"{self._base}/flags/{flag}")

    def set_flag(self, flag: str, **kwargs: Any) -> Any:
        """PUT /cluster/ceph/flags/{flag}"""
        return self._client.put(f"{self._base}/flags/{flag}", **kwargs)


# --- Jobs ---

class _ClusterJobsAPI(_ResourceBase):

    _base = "/cluster/jobs"

    def index(self) -> Any:
        """GET /cluster/jobs"""
        return self._client.get(self._base)

    def schedule_analyze(self, **kwargs: Any) -> Any:
        """GET /cluster/jobs/schedule-analyze"""
        return self._client.get(f"{self._base}/schedule-analyze", **kwargs)

    # Realm sync
    def list_realm_sync(self) -> Any:
        """GET /cluster/jobs/realm-sync"""
        return self._client.get(f"{self._base}/realm-sync")

    def get_realm_sync(self, id: str) -> Any:
        """GET /cluster/jobs/realm-sync/{id}"""
        return self._client.get(f"{self._base}/realm-sync/{id}")

    def create_realm_sync(self, id: str, schedule: str, **kwargs: Any) -> Any:
        """POST /cluster/jobs/realm-sync/{id}"""
        return self._client.post(
            f"{self._base}/realm-sync/{id}", schedule=schedule, **kwargs
        )

    def update_realm_sync(self, id: str, schedule: str, **kwargs: Any) -> Any:
        """PUT /cluster/jobs/realm-sync/{id}"""
        return self._client.put(
            f"{self._base}/realm-sync/{id}", schedule=schedule, **kwargs
        )

    def delete_realm_sync(self, id: str) -> Any:
        """DELETE /cluster/jobs/realm-sync/{id}"""
        return self._client.delete(f"{self._base}/realm-sync/{id}")


# --- Mapping ---

class _ClusterMappingAPI(_ResourceBase):

    _base = "/cluster/mapping"

    def index(self) -> Any:
        """GET /cluster/mapping"""
        return self._client.get(self._base)

    # Directory
    def list_dir(self) -> Any:
        """GET /cluster/mapping/dir"""
        return self._client.get(f"{self._base}/dir")

    def get_dir(self, id: str) -> Any:
        """GET /cluster/mapping/dir/{id}"""
        return self._client.get(f"{self._base}/dir/{id}")

    def create_dir(self, id: str, map: str, **kwargs: Any) -> Any:
        """POST /cluster/mapping/dir"""
        return self._client.post(f"{self._base}/dir", id=id, map=map, **kwargs)

    def update_dir(self, id: str, **kwargs: Any) -> Any:
        """PUT /cluster/mapping/dir/{id}"""
        return self._client.put(f"{self._base}/dir/{id}", **kwargs)

    def delete_dir(self, id: str) -> Any:
        """DELETE /cluster/mapping/dir/{id}"""
        return self._client.delete(f"{self._base}/dir/{id}")

    # PCI
    def list_pci(self) -> Any:
        """GET /cluster/mapping/pci"""
        return self._client.get(f"{self._base}/pci")

    def get_pci(self, id: str) -> Any:
        """GET /cluster/mapping/pci/{id}"""
        return self._client.get(f"{self._base}/pci/{id}")

    def create_pci(self, id: str, map: str, **kwargs: Any) -> Any:
        """POST /cluster/mapping/pci"""
        return self._client.post(f"{self._base}/pci", id=id, map=map, **kwargs)

    def update_pci(self, id: str, **kwargs: Any) -> Any:
        """PUT /cluster/mapping/pci/{id}"""
        return self._client.put(f"{self._base}/pci/{id}", **kwargs)

    def delete_pci(self, id: str) -> Any:
        """DELETE /cluster/mapping/pci/{id}"""
        return self._client.delete(f"{self._base}/pci/{id}")

    # USB
    def list_usb(self) -> Any:
        """GET /cluster/mapping/usb"""
        return self._client.get(f"{self._base}/usb")

    def get_usb(self, id: str) -> Any:
        """GET /cluster/mapping/usb/{id}"""
        return self._client.get(f"{self._base}/usb/{id}")

    def create_usb(self, id: str, map: str, **kwargs: Any) -> Any:
        """POST /cluster/mapping/usb"""
        return self._client.post(f"{self._base}/usb", id=id, map=map, **kwargs)

    def update_usb(self, id: str, **kwargs: Any) -> Any:
        """PUT /cluster/mapping/usb/{id}"""
        return self._client.put(f"{self._base}/usb/{id}", **kwargs)

    def delete_usb(self, id: str) -> Any:
        """DELETE /cluster/mapping/usb/{id}"""
        return self._client.delete(f"{self._base}/usb/{id}")


# --- Bulk Action ---

class _ClusterBulkActionAPI(_ResourceBase):

    _base = "/cluster/bulk-action"

    def index(self) -> Any:
        """GET /cluster/bulk-action"""
        return self._client.get(self._base)

    def guest_index(self) -> Any:
        """GET /cluster/bulk-action/guest"""
        return self._client.get(f"{self._base}/guest")

    def guest_start(self, **kwargs: Any) -> Any:
        """POST /cluster/bulk-action/guest/start"""
        return self._client.post(f"{self._base}/guest/start", **kwargs)

    def guest_shutdown(self, **kwargs: Any) -> Any:
        """POST /cluster/bulk-action/guest/shutdown"""
        return self._client.post(f"{self._base}/guest/shutdown", **kwargs)

    def guest_suspend(self, **kwargs: Any) -> Any:
        """POST /cluster/bulk-action/guest/suspend"""
        return self._client.post(f"{self._base}/guest/suspend", **kwargs)

    def guest_migrate(self, **kwargs: Any) -> Any:
        """POST /cluster/bulk-action/guest/migrate"""
        return self._client.post(f"{self._base}/guest/migrate", **kwargs)


# --- SDN ---

class _ClusterSDNAPI(_ResourceBase):

    _base = "/cluster/sdn"

    def index(self) -> Any:
        """GET /cluster/sdn"""
        return self._client.get(self._base)

    def apply(self) -> Any:
        """PUT /cluster/sdn"""
        return self._client.put(self._base)

    def lock(self) -> Any:
        """POST /cluster/sdn/lock"""
        return self._client.post(f"{self._base}/lock")

    def unlock(self) -> Any:
        """DELETE /cluster/sdn/lock"""
        return self._client.delete(f"{self._base}/lock")

    def rollback(self) -> Any:
        """POST /cluster/sdn/rollback"""
        return self._client.post(f"{self._base}/rollback")

    # --- VNets ---

    def list_vnets(self) -> Any:
        """GET /cluster/sdn/vnets"""
        return self._client.get(f"{self._base}/vnets")

    def get_vnet(self, vnet: str) -> Any:
        """GET /cluster/sdn/vnets/{vnet}"""
        return self._client.get(f"{self._base}/vnets/{vnet}")

    def create_vnet(self, vnet: str, zone: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/vnets"""
        return self._client.post(
            f"{self._base}/vnets", vnet=vnet, zone=zone, **kwargs
        )

    def update_vnet(self, vnet: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/vnets/{vnet}"""
        return self._client.put(f"{self._base}/vnets/{vnet}", **kwargs)

    def delete_vnet(self, vnet: str) -> Any:
        """DELETE /cluster/sdn/vnets/{vnet}"""
        return self._client.delete(f"{self._base}/vnets/{vnet}")

    # VNet subnets
    def list_subnets(self, vnet: str) -> Any:
        """GET /cluster/sdn/vnets/{vnet}/subnets"""
        return self._client.get(f"{self._base}/vnets/{vnet}/subnets")

    def get_subnet(self, vnet: str, subnet: str) -> Any:
        """GET /cluster/sdn/vnets/{vnet}/subnets/{subnet}"""
        return self._client.get(
            f"{self._base}/vnets/{vnet}/subnets/{subnet}"
        )

    def create_subnet(self, vnet: str, subnet: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/vnets/{vnet}/subnets"""
        return self._client.post(
            f"{self._base}/vnets/{vnet}/subnets", subnet=subnet, **kwargs
        )

    def update_subnet(self, vnet: str, subnet: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/vnets/{vnet}/subnets/{subnet}"""
        return self._client.put(
            f"{self._base}/vnets/{vnet}/subnets/{subnet}", **kwargs
        )

    def delete_subnet(self, vnet: str, subnet: str) -> Any:
        """DELETE /cluster/sdn/vnets/{vnet}/subnets/{subnet}"""
        return self._client.delete(
            f"{self._base}/vnets/{vnet}/subnets/{subnet}"
        )

    # VNet IPs
    def create_vnet_ip(self, vnet: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/vnets/{vnet}/ips"""
        return self._client.post(f"{self._base}/vnets/{vnet}/ips", **kwargs)

    def update_vnet_ip(self, vnet: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/vnets/{vnet}/ips"""
        return self._client.put(f"{self._base}/vnets/{vnet}/ips", **kwargs)

    def delete_vnet_ip(self, vnet: str, **kwargs: Any) -> Any:
        """DELETE /cluster/sdn/vnets/{vnet}/ips"""
        return self._client.delete(f"{self._base}/vnets/{vnet}/ips", **kwargs)

    # VNet firewall
    def vnet_firewall_index(self, vnet: str) -> Any:
        """GET /cluster/sdn/vnets/{vnet}/firewall"""
        return self._client.get(f"{self._base}/vnets/{vnet}/firewall")

    def vnet_firewall_rules(self, vnet: str) -> Any:
        """GET /cluster/sdn/vnets/{vnet}/firewall/rules"""
        return self._client.get(f"{self._base}/vnets/{vnet}/firewall/rules")

    def vnet_firewall_create_rule(self, vnet: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/vnets/{vnet}/firewall/rules"""
        return self._client.post(
            f"{self._base}/vnets/{vnet}/firewall/rules", **kwargs
        )

    def vnet_firewall_get_rule(self, vnet: str, pos: int) -> Any:
        """GET /cluster/sdn/vnets/{vnet}/firewall/rules/{pos}"""
        return self._client.get(
            f"{self._base}/vnets/{vnet}/firewall/rules/{pos}"
        )

    def vnet_firewall_update_rule(self, vnet: str, pos: int, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/vnets/{vnet}/firewall/rules/{pos}"""
        return self._client.put(
            f"{self._base}/vnets/{vnet}/firewall/rules/{pos}", **kwargs
        )

    def vnet_firewall_delete_rule(self, vnet: str, pos: int) -> Any:
        """DELETE /cluster/sdn/vnets/{vnet}/firewall/rules/{pos}"""
        return self._client.delete(
            f"{self._base}/vnets/{vnet}/firewall/rules/{pos}"
        )

    def vnet_firewall_options(self, vnet: str) -> Any:
        """GET /cluster/sdn/vnets/{vnet}/firewall/options"""
        return self._client.get(
            f"{self._base}/vnets/{vnet}/firewall/options"
        )

    def vnet_firewall_set_options(self, vnet: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/vnets/{vnet}/firewall/options"""
        return self._client.put(
            f"{self._base}/vnets/{vnet}/firewall/options", **kwargs
        )

    # --- Zones ---

    def list_zones(self) -> Any:
        """GET /cluster/sdn/zones"""
        return self._client.get(f"{self._base}/zones")

    def get_zone(self, zone: str) -> Any:
        """GET /cluster/sdn/zones/{zone}"""
        return self._client.get(f"{self._base}/zones/{zone}")

    def create_zone(self, zone: str, type: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/zones"""
        return self._client.post(
            f"{self._base}/zones", zone=zone, type=type, **kwargs
        )

    def update_zone(self, zone: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/zones/{zone}"""
        return self._client.put(f"{self._base}/zones/{zone}", **kwargs)

    def delete_zone(self, zone: str) -> Any:
        """DELETE /cluster/sdn/zones/{zone}"""
        return self._client.delete(f"{self._base}/zones/{zone}")

    # --- Controllers ---

    def list_controllers(self) -> Any:
        """GET /cluster/sdn/controllers"""
        return self._client.get(f"{self._base}/controllers")

    def get_controller(self, controller: str) -> Any:
        """GET /cluster/sdn/controllers/{controller}"""
        return self._client.get(f"{self._base}/controllers/{controller}")

    def create_controller(self, controller: str, type: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/controllers"""
        return self._client.post(
            f"{self._base}/controllers",
            controller=controller,
            type=type,
            **kwargs,
        )

    def update_controller(self, controller: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/controllers/{controller}"""
        return self._client.put(
            f"{self._base}/controllers/{controller}", **kwargs
        )

    def delete_controller(self, controller: str) -> Any:
        """DELETE /cluster/sdn/controllers/{controller}"""
        return self._client.delete(f"{self._base}/controllers/{controller}")

    # --- IPAMs ---

    def list_ipams(self) -> Any:
        """GET /cluster/sdn/ipams"""
        return self._client.get(f"{self._base}/ipams")

    def get_ipam(self, ipam: str) -> Any:
        """GET /cluster/sdn/ipams/{ipam}"""
        return self._client.get(f"{self._base}/ipams/{ipam}")

    def create_ipam(self, ipam: str, type: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/ipams"""
        return self._client.post(
            f"{self._base}/ipams", ipam=ipam, type=type, **kwargs
        )

    def update_ipam(self, ipam: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/ipams/{ipam}"""
        return self._client.put(f"{self._base}/ipams/{ipam}", **kwargs)

    def delete_ipam(self, ipam: str) -> Any:
        """DELETE /cluster/sdn/ipams/{ipam}"""
        return self._client.delete(f"{self._base}/ipams/{ipam}")

    def ipam_status(self, ipam: str) -> Any:
        """GET /cluster/sdn/ipams/{ipam}/status"""
        return self._client.get(f"{self._base}/ipams/{ipam}/status")

    # --- DNS ---

    def list_dns(self) -> Any:
        """GET /cluster/sdn/dns"""
        return self._client.get(f"{self._base}/dns")

    def get_dns(self, dns: str) -> Any:
        """GET /cluster/sdn/dns/{dns}"""
        return self._client.get(f"{self._base}/dns/{dns}")

    def create_dns(self, dns: str, type: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/dns"""
        return self._client.post(
            f"{self._base}/dns", dns=dns, type=type, **kwargs
        )

    def update_dns(self, dns: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/dns/{dns}"""
        return self._client.put(f"{self._base}/dns/{dns}", **kwargs)

    def delete_dns(self, dns: str) -> Any:
        """DELETE /cluster/sdn/dns/{dns}"""
        return self._client.delete(f"{self._base}/dns/{dns}")

    # --- Fabrics ---

    def list_fabrics(self) -> Any:
        """GET /cluster/sdn/fabrics"""
        return self._client.get(f"{self._base}/fabrics")

    def list_fabric(self) -> Any:
        """GET /cluster/sdn/fabrics/fabric"""
        return self._client.get(f"{self._base}/fabrics/fabric")

    def get_fabric(self, id: str) -> Any:
        """GET /cluster/sdn/fabrics/fabric/{id}"""
        return self._client.get(f"{self._base}/fabrics/fabric/{id}")

    def create_fabric(self, id: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/fabrics/fabric"""
        return self._client.post(
            f"{self._base}/fabrics/fabric", id=id, **kwargs
        )

    def update_fabric(self, id: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/fabrics/fabric/{id}"""
        return self._client.put(f"{self._base}/fabrics/fabric/{id}", **kwargs)

    def delete_fabric(self, id: str) -> Any:
        """DELETE /cluster/sdn/fabrics/fabric/{id}"""
        return self._client.delete(f"{self._base}/fabrics/fabric/{id}")

    # Fabric nodes
    def list_fabric_nodes(self) -> Any:
        """GET /cluster/sdn/fabrics/node"""
        return self._client.get(f"{self._base}/fabrics/node")

    def list_fabric_node(self, fabric_id: str) -> Any:
        """GET /cluster/sdn/fabrics/node/{fabric_id}"""
        return self._client.get(f"{self._base}/fabrics/node/{fabric_id}")

    def create_fabric_node(self, fabric_id: str, **kwargs: Any) -> Any:
        """POST /cluster/sdn/fabrics/node/{fabric_id}"""
        return self._client.post(
            f"{self._base}/fabrics/node/{fabric_id}", **kwargs
        )

    def get_fabric_node(self, fabric_id: str, node_id: str) -> Any:
        """GET /cluster/sdn/fabrics/node/{fabric_id}/{node_id}"""
        return self._client.get(
            f"{self._base}/fabrics/node/{fabric_id}/{node_id}"
        )

    def update_fabric_node(self, fabric_id: str, node_id: str, **kwargs: Any) -> Any:
        """PUT /cluster/sdn/fabrics/node/{fabric_id}/{node_id}"""
        return self._client.put(
            f"{self._base}/fabrics/node/{fabric_id}/{node_id}", **kwargs
        )

    def delete_fabric_node(self, fabric_id: str, node_id: str) -> Any:
        """DELETE /cluster/sdn/fabrics/node/{fabric_id}/{node_id}"""
        return self._client.delete(
            f"{self._base}/fabrics/node/{fabric_id}/{node_id}"
        )

    def list_fabrics_all(self) -> Any:
        """GET /cluster/sdn/fabrics/all"""
        return self._client.get(f"{self._base}/fabrics/all")
