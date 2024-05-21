# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VmCreateParams", "Port", "PortHTTPProxy"]


class VmCreateParams(TypedDict, total=False):
    cpu_cores: Required[Annotated[int, PropertyInfo(alias="cpuCores")]]

    disk_size: Required[Annotated[int, PropertyInfo(alias="diskSize")]]

    name: Required[str]

    ram: Required[int]

    ssh_public_key: Required[Annotated[str, PropertyInfo(alias="sshPublicKey")]]

    ports: Iterable[Port]

    zone: str


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
