# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["GPULeaseCreateParams"]


class GPULeaseCreateParams(TypedDict, total=False):
    gpu_group_id: Required[Annotated[str, PropertyInfo(alias="gpuGroupId")]]
    """
    GpuGroupID is used to specify the GPU to lease. As such, the lease does not
    specify which specific GPU to lease, but rather the type of GPU to lease.
    """

    lease_forever: Annotated[bool, PropertyInfo(alias="leaseForever")]
    """LeaseForever is used to specify whether the lease should be created forever."""
