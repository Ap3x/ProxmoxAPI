"""Base class for all resource API groups."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from proxmox_api.client import ProxmoxAPI


class _ResourceBase:
    """Base class for all resource API groups."""

    def __init__(self, client: ProxmoxAPI) -> None:
        self._client = client
