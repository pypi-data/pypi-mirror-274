# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import gpu_lease_list_params, gpu_lease_create_params, gpu_lease_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)
from ..types.gpu_lease_read import GPULeaseRead
from ..types.gpu_lease_created import GPULeaseCreated
from ..types.gpu_lease_deleted import GPULeaseDeleted
from ..types.gpu_lease_updated import GPULeaseUpdated
from ..types.gpu_lease_list_response import GPULeaseListResponse

__all__ = ["GPULeasesResource", "AsyncGPULeasesResource"]


class GPULeasesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GPULeasesResourceWithRawResponse:
        return GPULeasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GPULeasesResourceWithStreamingResponse:
        return GPULeasesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        gpu_group_id: str,
        lease_forever: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseCreated:
        """
        Create GPU lease

        Args:
          gpu_group_id: GpuGroupID is used to specify the GPU to lease. As such, the lease does not
              specify which specific GPU to lease, but rather the type of GPU to lease.

          lease_forever: LeaseForever is used to specify whether the lease should be created forever.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v2/gpuLeases",
            body=maybe_transform(
                {
                    "gpu_group_id": gpu_group_id,
                    "lease_forever": lease_forever,
                },
                gpu_lease_create_params.GPULeaseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GPULeaseCreated,
        )

    def retrieve(
        self,
        gpu_lease_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseRead:
        """
        Get GPU lease

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not gpu_lease_id:
            raise ValueError(f"Expected a non-empty value for `gpu_lease_id` but received {gpu_lease_id!r}")
        return self._get(
            f"/v2/gpuLeases/{gpu_lease_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GPULeaseRead,
        )

    def update(
        self,
        gpu_lease_id: str,
        *,
        vm_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseUpdated:
        """
        Update GPU lease

        Args:
          vm_id: VmID is used to specify the VM to attach the lease to.

              - If specified, the lease will be attached to the VM.

              - If the lease is already attached to a VM, it will be detached from the current
                VM and attached to the new VM.

              - If the lease is not active, specifying a VM will activate the lease.

              - If the lease is not assigned, an error will be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not gpu_lease_id:
            raise ValueError(f"Expected a non-empty value for `gpu_lease_id` but received {gpu_lease_id!r}")
        return self._post(
            f"/v2/gpuLeases/{gpu_lease_id}",
            body=maybe_transform({"vm_id": vm_id}, gpu_lease_update_params.GPULeaseUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GPULeaseUpdated,
        )

    def list(
        self,
        *,
        all: bool | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        vm_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseListResponse:
        """
        List GPU leases

        Args:
          all: List all

          page: Page number

          page_size: Number of items per page

          vm_id: Filter by VM ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v2/gpuLeases",
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
                        "vm_id": vm_id,
                    },
                    gpu_lease_list_params.GPULeaseListParams,
                ),
            ),
            cast_to=GPULeaseListResponse,
        )

    def delete(
        self,
        gpu_lease_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseDeleted:
        """
        Delete GPU lease

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not gpu_lease_id:
            raise ValueError(f"Expected a non-empty value for `gpu_lease_id` but received {gpu_lease_id!r}")
        return self._delete(
            f"/v2/gpuLeases/{gpu_lease_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GPULeaseDeleted,
        )


class AsyncGPULeasesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGPULeasesResourceWithRawResponse:
        return AsyncGPULeasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGPULeasesResourceWithStreamingResponse:
        return AsyncGPULeasesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        gpu_group_id: str,
        lease_forever: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseCreated:
        """
        Create GPU lease

        Args:
          gpu_group_id: GpuGroupID is used to specify the GPU to lease. As such, the lease does not
              specify which specific GPU to lease, but rather the type of GPU to lease.

          lease_forever: LeaseForever is used to specify whether the lease should be created forever.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v2/gpuLeases",
            body=await async_maybe_transform(
                {
                    "gpu_group_id": gpu_group_id,
                    "lease_forever": lease_forever,
                },
                gpu_lease_create_params.GPULeaseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GPULeaseCreated,
        )

    async def retrieve(
        self,
        gpu_lease_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseRead:
        """
        Get GPU lease

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not gpu_lease_id:
            raise ValueError(f"Expected a non-empty value for `gpu_lease_id` but received {gpu_lease_id!r}")
        return await self._get(
            f"/v2/gpuLeases/{gpu_lease_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GPULeaseRead,
        )

    async def update(
        self,
        gpu_lease_id: str,
        *,
        vm_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseUpdated:
        """
        Update GPU lease

        Args:
          vm_id: VmID is used to specify the VM to attach the lease to.

              - If specified, the lease will be attached to the VM.

              - If the lease is already attached to a VM, it will be detached from the current
                VM and attached to the new VM.

              - If the lease is not active, specifying a VM will activate the lease.

              - If the lease is not assigned, an error will be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not gpu_lease_id:
            raise ValueError(f"Expected a non-empty value for `gpu_lease_id` but received {gpu_lease_id!r}")
        return await self._post(
            f"/v2/gpuLeases/{gpu_lease_id}",
            body=await async_maybe_transform({"vm_id": vm_id}, gpu_lease_update_params.GPULeaseUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GPULeaseUpdated,
        )

    async def list(
        self,
        *,
        all: bool | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        vm_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseListResponse:
        """
        List GPU leases

        Args:
          all: List all

          page: Page number

          page_size: Number of items per page

          vm_id: Filter by VM ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v2/gpuLeases",
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
                        "vm_id": vm_id,
                    },
                    gpu_lease_list_params.GPULeaseListParams,
                ),
            ),
            cast_to=GPULeaseListResponse,
        )

    async def delete(
        self,
        gpu_lease_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GPULeaseDeleted:
        """
        Delete GPU lease

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not gpu_lease_id:
            raise ValueError(f"Expected a non-empty value for `gpu_lease_id` but received {gpu_lease_id!r}")
        return await self._delete(
            f"/v2/gpuLeases/{gpu_lease_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GPULeaseDeleted,
        )


class GPULeasesResourceWithRawResponse:
    def __init__(self, gpu_leases: GPULeasesResource) -> None:
        self._gpu_leases = gpu_leases

        self.create = to_raw_response_wrapper(
            gpu_leases.create,
        )
        self.retrieve = to_raw_response_wrapper(
            gpu_leases.retrieve,
        )
        self.update = to_raw_response_wrapper(
            gpu_leases.update,
        )
        self.list = to_raw_response_wrapper(
            gpu_leases.list,
        )
        self.delete = to_raw_response_wrapper(
            gpu_leases.delete,
        )


class AsyncGPULeasesResourceWithRawResponse:
    def __init__(self, gpu_leases: AsyncGPULeasesResource) -> None:
        self._gpu_leases = gpu_leases

        self.create = async_to_raw_response_wrapper(
            gpu_leases.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            gpu_leases.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            gpu_leases.update,
        )
        self.list = async_to_raw_response_wrapper(
            gpu_leases.list,
        )
        self.delete = async_to_raw_response_wrapper(
            gpu_leases.delete,
        )


class GPULeasesResourceWithStreamingResponse:
    def __init__(self, gpu_leases: GPULeasesResource) -> None:
        self._gpu_leases = gpu_leases

        self.create = to_streamed_response_wrapper(
            gpu_leases.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            gpu_leases.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            gpu_leases.update,
        )
        self.list = to_streamed_response_wrapper(
            gpu_leases.list,
        )
        self.delete = to_streamed_response_wrapper(
            gpu_leases.delete,
        )


class AsyncGPULeasesResourceWithStreamingResponse:
    def __init__(self, gpu_leases: AsyncGPULeasesResource) -> None:
        self._gpu_leases = gpu_leases

        self.create = async_to_streamed_response_wrapper(
            gpu_leases.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            gpu_leases.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            gpu_leases.update,
        )
        self.list = async_to_streamed_response_wrapper(
            gpu_leases.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            gpu_leases.delete,
        )
