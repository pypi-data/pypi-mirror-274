# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["GPUGroup"]


class GPUGroup(BaseModel):
    id: Optional[str] = None

    available: Optional[int] = None

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)

    name: Optional[str] = None

    total: Optional[int] = None

    vendor: Optional[str] = None

    zone: Optional[str] = None
