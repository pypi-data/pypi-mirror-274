# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ...types.vms.vm_snapshot_deleted import VmSnapshotDeleted

__all__ = ["SnapshotResource", "AsyncSnapshotResource"]


class SnapshotResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SnapshotResourceWithRawResponse:
        return SnapshotResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SnapshotResourceWithStreamingResponse:
        return SnapshotResourceWithStreamingResponse(self)

    def delete(
        self,
        snapshot_id: str,
        *,
        vm_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmSnapshotDeleted:
        """
        Delete snapshot

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vm_id:
            raise ValueError(f"Expected a non-empty value for `vm_id` but received {vm_id!r}")
        if not snapshot_id:
            raise ValueError(f"Expected a non-empty value for `snapshot_id` but received {snapshot_id!r}")
        return self._delete(
            f"/v2/vms/{vm_id}/snapshot/{snapshot_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmSnapshotDeleted,
        )


class AsyncSnapshotResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSnapshotResourceWithRawResponse:
        return AsyncSnapshotResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSnapshotResourceWithStreamingResponse:
        return AsyncSnapshotResourceWithStreamingResponse(self)

    async def delete(
        self,
        snapshot_id: str,
        *,
        vm_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmSnapshotDeleted:
        """
        Delete snapshot

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vm_id:
            raise ValueError(f"Expected a non-empty value for `vm_id` but received {vm_id!r}")
        if not snapshot_id:
            raise ValueError(f"Expected a non-empty value for `snapshot_id` but received {snapshot_id!r}")
        return await self._delete(
            f"/v2/vms/{vm_id}/snapshot/{snapshot_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmSnapshotDeleted,
        )


class SnapshotResourceWithRawResponse:
    def __init__(self, snapshot: SnapshotResource) -> None:
        self._snapshot = snapshot

        self.delete = to_raw_response_wrapper(
            snapshot.delete,
        )


class AsyncSnapshotResourceWithRawResponse:
    def __init__(self, snapshot: AsyncSnapshotResource) -> None:
        self._snapshot = snapshot

        self.delete = async_to_raw_response_wrapper(
            snapshot.delete,
        )


class SnapshotResourceWithStreamingResponse:
    def __init__(self, snapshot: SnapshotResource) -> None:
        self._snapshot = snapshot

        self.delete = to_streamed_response_wrapper(
            snapshot.delete,
        )


class AsyncSnapshotResourceWithStreamingResponse:
    def __init__(self, snapshot: AsyncSnapshotResource) -> None:
        self._snapshot = snapshot

        self.delete = async_to_streamed_response_wrapper(
            snapshot.delete,
        )
