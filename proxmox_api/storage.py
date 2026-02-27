"""Storage API resources."""

from __future__ import annotations

from typing import Any

from proxmox_api._base import _ResourceBase


class _StorageAPI(_ResourceBase):

    def list(self, **kwargs: Any) -> Any:
        """GET /storage - Storage index."""
        return self._client.get("/storage", **kwargs)

    def get(self, storage: str) -> Any:
        """GET /storage/{storage}"""
        return self._client.get(f"/storage/{storage}")

    def create(self, storage: str, type: str, **kwargs: Any) -> Any:
        """POST /storage"""
        return self._client.post(
            "/storage", storage=storage, type=type, **kwargs
        )

    def update(self, storage: str, **kwargs: Any) -> Any:
        """PUT /storage/{storage}"""
        return self._client.put(f"/storage/{storage}", **kwargs)

    def delete(self, storage: str) -> Any:
        """DELETE /storage/{storage}"""
        return self._client.delete(f"/storage/{storage}")
