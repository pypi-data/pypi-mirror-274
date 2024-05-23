# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["GPULeaseUpdateParams"]


class GPULeaseUpdateParams(TypedDict, total=False):
    vm_id: Annotated[str, PropertyInfo(alias="vmId")]
    """VmID is used to specify the VM to attach the lease to.

    - If specified, the lease will be attached to the VM.

    - If the lease is already attached to a VM, it will be detached from the current
      VM and attached to the new VM.

    - If the lease is not active, specifying a VM will activate the lease.

    - If the lease is not assigned, an error will be returned.
    """
