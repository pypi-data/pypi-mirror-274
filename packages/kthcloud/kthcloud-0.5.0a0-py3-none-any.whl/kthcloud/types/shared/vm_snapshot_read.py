# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["VmSnapshotRead"]


class VmSnapshotRead(BaseModel):
    id: Optional[str] = None

    created: Optional[str] = None

    name: Optional[str] = None

    status: Optional[str] = None
