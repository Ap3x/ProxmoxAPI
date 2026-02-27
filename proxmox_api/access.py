"""Access control API resources."""

from __future__ import annotations

from typing import Any

from proxmox_api._base import _ResourceBase


class _AccessAPI(_ResourceBase):

    def list(self) -> Any:
        """GET /access - Directory index."""
        return self._client.get("/access")

    # --- Users ---

    def list_users(self, **kwargs: Any) -> Any:
        """GET /access/users"""
        return self._client.get("/access/users", **kwargs)

    def get_user(self, userid: str) -> Any:
        """GET /access/users/{userid}"""
        return self._client.get(f"/access/users/{userid}")

    def create_user(self, userid: str, **kwargs: Any) -> Any:
        """POST /access/users"""
        return self._client.post("/access/users", userid=userid, **kwargs)

    def update_user(self, userid: str, **kwargs: Any) -> Any:
        """PUT /access/users/{userid}"""
        return self._client.put(f"/access/users/{userid}", **kwargs)

    def delete_user(self, userid: str) -> Any:
        """DELETE /access/users/{userid}"""
        return self._client.delete(f"/access/users/{userid}")

    # --- User TFA ---

    def user_tfa(self, userid: str) -> Any:
        """GET /access/users/{userid}/tfa"""
        return self._client.get(f"/access/users/{userid}/tfa")

    def unlock_user_tfa(self, userid: str) -> Any:
        """PUT /access/users/{userid}/unlock-tfa"""
        return self._client.put(f"/access/users/{userid}/unlock-tfa")

    # --- User API Tokens ---

    def list_user_tokens(self, userid: str) -> Any:
        """GET /access/users/{userid}/token"""
        return self._client.get(f"/access/users/{userid}/token")

    def get_user_token(self, userid: str, tokenid: str) -> Any:
        """GET /access/users/{userid}/token/{tokenid}"""
        return self._client.get(f"/access/users/{userid}/token/{tokenid}")

    def create_user_token(self, userid: str, tokenid: str, **kwargs: Any) -> Any:
        """POST /access/users/{userid}/token/{tokenid}"""
        return self._client.post(
            f"/access/users/{userid}/token/{tokenid}", **kwargs
        )

    def update_user_token(self, userid: str, tokenid: str, **kwargs: Any) -> Any:
        """PUT /access/users/{userid}/token/{tokenid}"""
        return self._client.put(
            f"/access/users/{userid}/token/{tokenid}", **kwargs
        )

    def delete_user_token(self, userid: str, tokenid: str) -> Any:
        """DELETE /access/users/{userid}/token/{tokenid}"""
        return self._client.delete(f"/access/users/{userid}/token/{tokenid}")

    # --- Groups ---

    def list_groups(self) -> Any:
        """GET /access/groups"""
        return self._client.get("/access/groups")

    def get_group(self, groupid: str) -> Any:
        """GET /access/groups/{groupid}"""
        return self._client.get(f"/access/groups/{groupid}")

    def create_group(self, groupid: str, **kwargs: Any) -> Any:
        """POST /access/groups"""
        return self._client.post("/access/groups", groupid=groupid, **kwargs)

    def update_group(self, groupid: str, **kwargs: Any) -> Any:
        """PUT /access/groups/{groupid}"""
        return self._client.put(f"/access/groups/{groupid}", **kwargs)

    def delete_group(self, groupid: str) -> Any:
        """DELETE /access/groups/{groupid}"""
        return self._client.delete(f"/access/groups/{groupid}")

    # --- Roles ---

    def list_roles(self) -> Any:
        """GET /access/roles"""
        return self._client.get("/access/roles")

    def get_role(self, roleid: str) -> Any:
        """GET /access/roles/{roleid}"""
        return self._client.get(f"/access/roles/{roleid}")

    def create_role(self, roleid: str, **kwargs: Any) -> Any:
        """POST /access/roles"""
        return self._client.post("/access/roles", roleid=roleid, **kwargs)

    def update_role(self, roleid: str, **kwargs: Any) -> Any:
        """PUT /access/roles/{roleid}"""
        return self._client.put(f"/access/roles/{roleid}", **kwargs)

    def delete_role(self, roleid: str) -> Any:
        """DELETE /access/roles/{roleid}"""
        return self._client.delete(f"/access/roles/{roleid}")

    # --- Domains / Realms ---

    def list_domains(self) -> Any:
        """GET /access/domains"""
        return self._client.get("/access/domains")

    def get_domain(self, realm: str) -> Any:
        """GET /access/domains/{realm}"""
        return self._client.get(f"/access/domains/{realm}")

    def create_domain(self, realm: str, type: str, **kwargs: Any) -> Any:
        """POST /access/domains"""
        return self._client.post(
            "/access/domains", realm=realm, type=type, **kwargs
        )

    def update_domain(self, realm: str, **kwargs: Any) -> Any:
        """PUT /access/domains/{realm}"""
        return self._client.put(f"/access/domains/{realm}", **kwargs)

    def delete_domain(self, realm: str) -> Any:
        """DELETE /access/domains/{realm}"""
        return self._client.delete(f"/access/domains/{realm}")

    def sync_domain(self, realm: str, **kwargs: Any) -> Any:
        """POST /access/domains/{realm}/sync"""
        return self._client.post(f"/access/domains/{realm}/sync", **kwargs)

    # --- ACL ---

    def acl(self) -> Any:
        """GET /access/acl"""
        return self._client.get("/access/acl")

    def update_acl(self, path: str, roles: str, **kwargs: Any) -> Any:
        """PUT /access/acl"""
        return self._client.put("/access/acl", path=path, roles=roles, **kwargs)

    # --- Tickets & Auth ---

    def create_ticket(self, username: str, password: str, **kwargs: Any) -> Any:
        """POST /access/ticket"""
        return self._client.post(
            "/access/ticket", username=username, password=password, **kwargs
        )

    def get_ticket(self, **kwargs: Any) -> Any:
        """GET /access/ticket"""
        return self._client.get("/access/ticket", **kwargs)

    def create_vncticket(self, **kwargs: Any) -> Any:
        """POST /access/vncticket"""
        return self._client.post("/access/vncticket", **kwargs)

    def password(self, userid: str, password: str, **kwargs: Any) -> Any:
        """PUT /access/password"""
        return self._client.put(
            "/access/password", userid=userid, password=password, **kwargs
        )

    def permissions(self, **kwargs: Any) -> Any:
        """GET /access/permissions"""
        return self._client.get("/access/permissions", **kwargs)

    # --- TFA ---

    def tfa(self) -> Any:
        """GET /access/tfa"""
        return self._client.get("/access/tfa")

    def list_tfa(self, userid: str) -> Any:
        """GET /access/tfa/{userid}"""
        return self._client.get(f"/access/tfa/{userid}")

    def add_tfa(self, userid: str, **kwargs: Any) -> Any:
        """POST /access/tfa/{userid}"""
        return self._client.post(f"/access/tfa/{userid}", **kwargs)

    def get_tfa_entry(self, userid: str, id: str) -> Any:
        """GET /access/tfa/{userid}/{id}"""
        return self._client.get(f"/access/tfa/{userid}/{id}")

    def update_tfa_entry(self, userid: str, id: str, **kwargs: Any) -> Any:
        """PUT /access/tfa/{userid}/{id}"""
        return self._client.put(f"/access/tfa/{userid}/{id}", **kwargs)

    def delete_tfa_entry(self, userid: str, id: str) -> Any:
        """DELETE /access/tfa/{userid}/{id}"""
        return self._client.delete(f"/access/tfa/{userid}/{id}")

    # --- OpenID Connect ---

    def openid(self) -> Any:
        """GET /access/openid"""
        return self._client.get("/access/openid")

    def openid_auth_url(self, realm: str, redirect_url: str, **kwargs: Any) -> Any:
        """POST /access/openid/auth-url"""
        return self._client.post(
            "/access/openid/auth-url",
            realm=realm,
            **{"redirect-url": redirect_url},
            **kwargs,
        )

    def openid_login(self, code: str, state: str, **kwargs: Any) -> Any:
        """POST /access/openid/login"""
        return self._client.post(
            "/access/openid/login", code=code, state=state, **kwargs
        )
