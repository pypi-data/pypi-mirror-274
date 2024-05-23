# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VmUpdateParams", "Port", "PortHTTPProxy"]


class VmUpdateParams(TypedDict, total=False):
    cpu_cores: Annotated[int, PropertyInfo(alias="cpuCores")]

    name: str
    """Name is used to rename a VM. If specified, only name will be updated."""

    owner_id: Annotated[str, PropertyInfo(alias="ownerId")]
    """
    OwnerID is used to initiate transfer a VM to another user. If specified, only
    the transfer will happen. If specified but empty, the transfer will be canceled.
    """

    ports: Iterable[Port]

    ram: int


class PortHTTPProxy(TypedDict, total=False):
    name: Required[str]

    custom_domain: Annotated[str, PropertyInfo(alias="customDomain")]
    """
    CustomDomain is the domain that the deployment will be available on. The max
    length is set to 243 to allow for a sub domain when confirming the domain.
    """


class Port(TypedDict, total=False):
    name: Required[str]

    port: Required[int]

    protocol: Required[Literal["tcp", "udp"]]

    http_proxy: Annotated[PortHTTPProxy, PropertyInfo(alias="httpProxy")]
