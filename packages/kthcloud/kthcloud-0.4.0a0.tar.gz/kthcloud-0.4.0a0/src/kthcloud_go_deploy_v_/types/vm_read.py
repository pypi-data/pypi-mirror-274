# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["VmRead", "GPU", "Port", "PortHTTPProxy", "PortHTTPProxyCustomDomain", "Specs"]


class GPU(BaseModel):
    id: Optional[str] = None

    activated_at: Optional[str] = FieldInfo(alias="activatedAt", default=None)
    """ActivatedAt specifies the time when the lease was activated.

    This is the time the user first attached the GPU or 1 day after the lease was
    created if the user did not attach the GPU.
    """

    assigned_at: Optional[str] = FieldInfo(alias="assignedAt", default=None)
    """AssignedAt specifies the time when the lease was assigned to the user."""

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)

    expired_at: Optional[str] = FieldInfo(alias="expiredAt", default=None)
    """
    ExpiredAt specifies the time when the lease expired. This is only present if the
    lease is expired.
    """

    expires_at: Optional[str] = FieldInfo(alias="expiresAt", default=None)
    """
    ExpiresAt specifies the time when the lease will expire. This is only present if
    the lease is active.
    """

    gpu_group_id: Optional[str] = FieldInfo(alias="gpuGroupId", default=None)

    lease_duration: Optional[float] = FieldInfo(alias="leaseDuration", default=None)


class PortHTTPProxyCustomDomain(BaseModel):
    domain: Optional[str] = None

    secret: Optional[str] = None

    status: Optional[str] = None

    url: Optional[str] = None


class PortHTTPProxy(BaseModel):
    name: str

    custom_domain: Optional[PortHTTPProxyCustomDomain] = FieldInfo(alias="customDomain", default=None)

    url: Optional[str] = None


class Port(BaseModel):
    external_port: Optional[int] = FieldInfo(alias="externalPort", default=None)

    http_proxy: Optional[PortHTTPProxy] = FieldInfo(alias="httpProxy", default=None)

    name: Optional[str] = None

    port: Optional[int] = None

    protocol: Optional[str] = None


class Specs(BaseModel):
    cpu_cores: Optional[int] = FieldInfo(alias="cpuCores", default=None)

    disk_size: Optional[int] = FieldInfo(alias="diskSize", default=None)

    ram: Optional[int] = None


class VmRead(BaseModel):
    id: Optional[str] = None

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)

    gpu: Optional[GPU] = None

    host: Optional[str] = None

    internal_name: Optional[str] = FieldInfo(alias="internalName", default=None)

    name: Optional[str] = None

    owner_id: Optional[str] = FieldInfo(alias="ownerId", default=None)

    ports: Optional[List[Port]] = None

    repaired_at: Optional[str] = FieldInfo(alias="repairedAt", default=None)

    specs: Optional[Specs] = None

    ssh_connection_string: Optional[str] = FieldInfo(alias="sshConnectionString", default=None)

    ssh_public_key: Optional[str] = FieldInfo(alias="sshPublicKey", default=None)

    status: Optional[str] = None

    teams: Optional[List[str]] = None

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)

    zone: Optional[str] = None
