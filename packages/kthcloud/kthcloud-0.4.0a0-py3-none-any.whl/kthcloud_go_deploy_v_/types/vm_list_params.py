# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VmListParams"]


class VmListParams(TypedDict, total=False):
    all: bool
    """List all"""

    page: int
    """Page number"""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """Number of items per page"""

    user_id: Annotated[str, PropertyInfo(alias="userId")]
    """Filter by user ID"""
