"""Pools API resources."""

from __future__ import annotations

from typing import Any

from proxmox_api._base import _ResourceBase


class _PoolsAPI(_ResourceBase):

    def list(self) -> Any:
        """GET /pools"""
        return self._client.get("/pools")

    def get(self, poolid: str) -> Any:
        """GET /pools/{poolid}"""
        return self._client.get(f"/pools/{poolid}")

    def create(self, poolid: str, **kwargs: Any) -> Any:
        """POST /pools"""
        return self._client.post("/pools", poolid=poolid, **kwargs)

    def update(self, poolid: str, **kwargs: Any) -> Any:
        """PUT /pools/{poolid}"""
        return self._client.put(f"/pools/{poolid}", **kwargs)

    def delete(self, poolid: str) -> Any:
        """DELETE /pools/{poolid}"""
        return self._client.delete(f"/pools/{poolid}")

    def bulk_update(self, **kwargs: Any) -> Any:
        """PUT /pools"""
        return self._client.put("/pools", **kwargs)

    def bulk_delete(self, **kwargs: Any) -> Any:
        """DELETE /pools"""
        return self._client.delete("/pools", **kwargs)
