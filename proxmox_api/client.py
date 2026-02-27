"""Core HTTP client for the Proxmox VE REST API."""

from __future__ import annotations

import urllib3
from typing import Any

import requests

from proxmox_api.access import _AccessAPI
from proxmox_api.cluster import _ClusterAPI
from proxmox_api.nodes import _NodesAPI
from proxmox_api.pools import _PoolsAPI
from proxmox_api.storage import _StorageAPI


# Suppress InsecureRequestWarning when verify_ssl=False (common for Proxmox).
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ProxmoxAPI:
    """Low-level client that handles authentication and HTTP requests.

    Supports both API token and ticket (user/password) authentication.

    Usage with API token::

        api = ProxmoxAPI(
            host="192.168.1.100",
            token_name="mytoken",
            token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            user="root@pam",
        )
        nodes = api.nodes.list()

    Usage with password::

        api = ProxmoxAPI(
            host="192.168.1.100",
            user="root@pam",
            password="secret",
        )
        nodes = api.nodes.list()
    """

    def __init__(
        self,
        host: str,
        *,
        user: str | None = None,
        password: str | None = None,
        token_name: str | None = None,
        token_value: str | None = None,
        port: int = 8006,
        verify_ssl: bool = False,
        timeout: int = 30,
    ) -> None:
        self.host = host
        self.port = port
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.base_url = f"https://{host}:{port}/api2/json"

        self._session = requests.Session()
        self._session.verify = verify_ssl

        if token_name and token_value:
            if not user:
                raise ValueError("'user' is required when using API token auth")
            self._session.headers["Authorization"] = (
                f"PVEAPIToken={user}!{token_name}={token_value}"
            )
        elif user and password:
            self._authenticate(user, password)
        else:
            raise ValueError(
                "Provide either (user + token_name + token_value) "
                "or (user + password)"
            )

        # Lazily initialised resource accessors
        self._cluster: _ClusterAPI | None = None
        self._nodes: _NodesAPI | None = None
        self._storage: _StorageAPI | None = None
        self._access: _AccessAPI | None = None
        self._pools: _PoolsAPI | None = None

    def _authenticate(self, user: str, password: str) -> None:
        """Authenticate via user/password and store the ticket + CSRF token."""
        resp = self._session.post(
            f"{self.base_url}/access/ticket",
            data={"username": user, "password": password},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        ticket = data["ticket"]
        csrf = data["CSRFPreventionToken"]
        self._session.cookies.set("PVEAuthCookie", ticket)
        self._session.headers["CSRFPreventionToken"] = csrf

    # -- HTTP helpers --------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Send a request and return the 'data' field from the JSON response."""
        url = f"{self.base_url}{path}"
        # Strip None values so the API doesn't receive empty params.
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        if data:
            data = {k: v for k, v in data.items() if v is not None}

        resp = self._session.request(
            method,
            url,
            params=params if method == "GET" else None,
            data=data if method != "GET" else (params or None),
            timeout=self.timeout,
        )
        resp.raise_for_status()
        json_body = resp.json()
        return json_body.get("data", json_body)

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, params=kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.request("POST", path, data=kwargs)

    def put(self, path: str, **kwargs: Any) -> Any:
        return self.request("PUT", path, data=kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self.request("DELETE", path, params=kwargs)

    # -- Resource accessors --------------------------------------------------

    @property
    def cluster(self) -> _ClusterAPI:
        if self._cluster is None:
            self._cluster = _ClusterAPI(self)
        return self._cluster

    @property
    def nodes(self) -> _NodesAPI:
        if self._nodes is None:
            self._nodes = _NodesAPI(self)
        return self._nodes

    @property
    def storage(self) -> _StorageAPI:
        if self._storage is None:
            self._storage = _StorageAPI(self)
        return self._storage

    @property
    def access(self) -> _AccessAPI:
        if self._access is None:
            self._access = _AccessAPI(self)
        return self._access

    @property
    def pools(self) -> _PoolsAPI:
        if self._pools is None:
            self._pools = _PoolsAPI(self)
        return self._pools

    def version(self) -> Any:
        """GET /version"""
        return self.get("/version")
