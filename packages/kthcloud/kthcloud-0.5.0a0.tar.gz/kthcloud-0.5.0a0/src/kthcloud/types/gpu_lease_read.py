# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["GPULeaseRead"]


class GPULeaseRead(BaseModel):
    id: Optional[str] = None

    activated_at: Optional[str] = FieldInfo(alias="activatedAt", default=None)
    """ActivatedAt specifies the time when the lease was activated.

    This is the time the user first attached the GPU or 1 day after the lease was
    created if the user did not attach the GPU.
    """

    active: Optional[bool] = None

    assigned_at: Optional[str] = FieldInfo(alias="assignedAt", default=None)
    """AssignedAt specifies the time when the lease was assigned to the user."""

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)

    expired_at: Optional[str] = FieldInfo(alias="expiredAt", default=None)

    expires_at: Optional[str] = FieldInfo(alias="expiresAt", default=None)
    """
    ExpiresAt specifies the time when the lease will expire. This is only present if
    the lease is active.
    """

    gpu_group_id: Optional[str] = FieldInfo(alias="gpuGroupId", default=None)

    lease_duration: Optional[float] = FieldInfo(alias="leaseDuration", default=None)

    queue_position: Optional[int] = FieldInfo(alias="queuePosition", default=None)

    user_id: Optional[str] = FieldInfo(alias="userId", default=None)

    vm_id: Optional[str] = FieldInfo(alias="vmId", default=None)
    """VmID is set when the lease is attached to a VM."""
