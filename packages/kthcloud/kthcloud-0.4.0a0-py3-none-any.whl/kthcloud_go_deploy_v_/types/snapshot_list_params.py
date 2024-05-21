# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SnapshotListParams"]


class SnapshotListParams(TypedDict, total=False):
    page: int
    """Page number"""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """Number of items per page"""
