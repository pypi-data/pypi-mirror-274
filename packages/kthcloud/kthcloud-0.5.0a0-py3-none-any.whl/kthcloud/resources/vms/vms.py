# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ...types import vm_list_params, vm_create_params, vm_update_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .snapshot import (
    SnapshotResource,
    AsyncSnapshotResource,
    SnapshotResourceWithRawResponse,
    AsyncSnapshotResourceWithRawResponse,
    SnapshotResourceWithStreamingResponse,
    AsyncSnapshotResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import (
    make_request_options,
)
from ...types.vm_read import VmRead
from ...types.vm_created import VmCreated
from ...types.vm_deleted import VmDeleted
from ...types.vm_updated import VmUpdated
from ...types.vm_list_response import VmListResponse

__all__ = ["VmsResource", "AsyncVmsResource"]


class VmsResource(SyncAPIResource):
    @cached_property
    def snapshot(self) -> SnapshotResource:
        return SnapshotResource(self._client)

    @cached_property
    def with_raw_response(self) -> VmsResourceWithRawResponse:
        return VmsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VmsResourceWithStreamingResponse:
        return VmsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        cpu_cores: int,
        disk_size: int,
        name: str,
        ram: int,
        ssh_public_key: str,
        ports: Iterable[vm_create_params.Port] | NotGiven = NOT_GIVEN,
        zone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmCreated:
        """
        Create VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v2/vms",
            body=maybe_transform(
                {
                    "cpu_cores": cpu_cores,
                    "disk_size": disk_size,
                    "name": name,
                    "ram": ram,
                    "ssh_public_key": ssh_public_key,
                    "ports": ports,
                    "zone": zone,
                },
                vm_create_params.VmCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmCreated,
        )

    def retrieve(
        self,
        vm_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmRead:
        """
        Get VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vm_id:
            raise ValueError(f"Expected a non-empty value for `vm_id` but received {vm_id!r}")
        return self._get(
            f"/v2/vms/{vm_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmRead,
        )

    def update(
        self,
        vm_id: str,
        *,
        cpu_cores: int | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        owner_id: str | NotGiven = NOT_GIVEN,
        ports: Iterable[vm_update_params.Port] | NotGiven = NOT_GIVEN,
        ram: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmUpdated:
        """Update VM

        Args:
          name: Name is used to rename a VM.

        If specified, only name will be updated.

          owner_id: OwnerID is used to initiate transfer a VM to another user. If specified, only
              the transfer will happen. If specified but empty, the transfer will be canceled.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vm_id:
            raise ValueError(f"Expected a non-empty value for `vm_id` but received {vm_id!r}")
        return self._post(
            f"/v2/vms/{vm_id}",
            body=maybe_transform(
                {
                    "cpu_cores": cpu_cores,
                    "name": name,
                    "owner_id": owner_id,
                    "ports": ports,
                    "ram": ram,
                },
                vm_update_params.VmUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmUpdated,
        )

    def list(
        self,
        *,
        all: bool | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmListResponse:
        """
        List VMs

        Args:
          all: List all

          page: Page number

          page_size: Number of items per page

          user_id: Filter by user ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v2/vms",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "all": all,
                        "page": page,
                        "page_size": page_size,
                        "user_id": user_id,
                    },
                    vm_list_params.VmListParams,
                ),
            ),
            cast_to=VmListResponse,
        )

    def delete(
        self,
        vm_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmDeleted:
        """
        Delete VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vm_id:
            raise ValueError(f"Expected a non-empty value for `vm_id` but received {vm_id!r}")
        return self._delete(
            f"/v2/vms/{vm_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmDeleted,
        )


class AsyncVmsResource(AsyncAPIResource):
    @cached_property
    def snapshot(self) -> AsyncSnapshotResource:
        return AsyncSnapshotResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVmsResourceWithRawResponse:
        return AsyncVmsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVmsResourceWithStreamingResponse:
        return AsyncVmsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        cpu_cores: int,
        disk_size: int,
        name: str,
        ram: int,
        ssh_public_key: str,
        ports: Iterable[vm_create_params.Port] | NotGiven = NOT_GIVEN,
        zone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmCreated:
        """
        Create VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v2/vms",
            body=await async_maybe_transform(
                {
                    "cpu_cores": cpu_cores,
                    "disk_size": disk_size,
                    "name": name,
                    "ram": ram,
                    "ssh_public_key": ssh_public_key,
                    "ports": ports,
                    "zone": zone,
                },
                vm_create_params.VmCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmCreated,
        )

    async def retrieve(
        self,
        vm_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmRead:
        """
        Get VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vm_id:
            raise ValueError(f"Expected a non-empty value for `vm_id` but received {vm_id!r}")
        return await self._get(
            f"/v2/vms/{vm_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmRead,
        )

    async def update(
        self,
        vm_id: str,
        *,
        cpu_cores: int | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        owner_id: str | NotGiven = NOT_GIVEN,
        ports: Iterable[vm_update_params.Port] | NotGiven = NOT_GIVEN,
        ram: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmUpdated:
        """Update VM

        Args:
          name: Name is used to rename a VM.

        If specified, only name will be updated.

          owner_id: OwnerID is used to initiate transfer a VM to another user. If specified, only
              the transfer will happen. If specified but empty, the transfer will be canceled.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vm_id:
            raise ValueError(f"Expected a non-empty value for `vm_id` but received {vm_id!r}")
        return await self._post(
            f"/v2/vms/{vm_id}",
            body=await async_maybe_transform(
                {
                    "cpu_cores": cpu_cores,
                    "name": name,
                    "owner_id": owner_id,
                    "ports": ports,
                    "ram": ram,
                },
                vm_update_params.VmUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmUpdated,
        )

    async def list(
        self,
        *,
        all: bool | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmListResponse:
        """
        List VMs

        Args:
          all: List all

          page: Page number

          page_size: Number of items per page

          user_id: Filter by user ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v2/vms",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "all": all,
                        "page": page,
                        "page_size": page_size,
                        "user_id": user_id,
                    },
                    vm_list_params.VmListParams,
                ),
            ),
            cast_to=VmListResponse,
        )

    async def delete(
        self,
        vm_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmDeleted:
        """
        Delete VM

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vm_id:
            raise ValueError(f"Expected a non-empty value for `vm_id` but received {vm_id!r}")
        return await self._delete(
            f"/v2/vms/{vm_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmDeleted,
        )


class VmsResourceWithRawResponse:
    def __init__(self, vms: VmsResource) -> None:
        self._vms = vms

        self.create = to_raw_response_wrapper(
            vms.create,
        )
        self.retrieve = to_raw_response_wrapper(
            vms.retrieve,
        )
        self.update = to_raw_response_wrapper(
            vms.update,
        )
        self.list = to_raw_response_wrapper(
            vms.list,
        )
        self.delete = to_raw_response_wrapper(
            vms.delete,
        )

    @cached_property
    def snapshot(self) -> SnapshotResourceWithRawResponse:
        return SnapshotResourceWithRawResponse(self._vms.snapshot)


class AsyncVmsResourceWithRawResponse:
    def __init__(self, vms: AsyncVmsResource) -> None:
        self._vms = vms

        self.create = async_to_raw_response_wrapper(
            vms.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            vms.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            vms.update,
        )
        self.list = async_to_raw_response_wrapper(
            vms.list,
        )
        self.delete = async_to_raw_response_wrapper(
            vms.delete,
        )

    @cached_property
    def snapshot(self) -> AsyncSnapshotResourceWithRawResponse:
        return AsyncSnapshotResourceWithRawResponse(self._vms.snapshot)


class VmsResourceWithStreamingResponse:
    def __init__(self, vms: VmsResource) -> None:
        self._vms = vms

        self.create = to_streamed_response_wrapper(
            vms.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            vms.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            vms.update,
        )
        self.list = to_streamed_response_wrapper(
            vms.list,
        )
        self.delete = to_streamed_response_wrapper(
            vms.delete,
        )

    @cached_property
    def snapshot(self) -> SnapshotResourceWithStreamingResponse:
        return SnapshotResourceWithStreamingResponse(self._vms.snapshot)


class AsyncVmsResourceWithStreamingResponse:
    def __init__(self, vms: AsyncVmsResource) -> None:
        self._vms = vms

        self.create = async_to_streamed_response_wrapper(
            vms.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            vms.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            vms.update,
        )
        self.list = async_to_streamed_response_wrapper(
            vms.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            vms.delete,
        )

    @cached_property
    def snapshot(self) -> AsyncSnapshotResourceWithStreamingResponse:
        return AsyncSnapshotResourceWithStreamingResponse(self._vms.snapshot)
