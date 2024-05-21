# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import vm_action_create_params
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
from ..types.vm_action_created import VmActionCreated

__all__ = ["VmActionsResource", "AsyncVmActionsResource"]


class VmActionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VmActionsResourceWithRawResponse:
        return VmActionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VmActionsResourceWithStreamingResponse:
        return VmActionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        action: Literal["start", "stop", "restart", "repair"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmActionCreated:
        """
        Creates a new action

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v2/vmActions",
            body=maybe_transform({"action": action}, vm_action_create_params.VmActionCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmActionCreated,
        )


class AsyncVmActionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVmActionsResourceWithRawResponse:
        return AsyncVmActionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVmActionsResourceWithStreamingResponse:
        return AsyncVmActionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        action: Literal["start", "stop", "restart", "repair"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VmActionCreated:
        """
        Creates a new action

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v2/vmActions",
            body=await async_maybe_transform({"action": action}, vm_action_create_params.VmActionCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VmActionCreated,
        )


class VmActionsResourceWithRawResponse:
    def __init__(self, vm_actions: VmActionsResource) -> None:
        self._vm_actions = vm_actions

        self.create = to_raw_response_wrapper(
            vm_actions.create,
        )


class AsyncVmActionsResourceWithRawResponse:
    def __init__(self, vm_actions: AsyncVmActionsResource) -> None:
        self._vm_actions = vm_actions

        self.create = async_to_raw_response_wrapper(
            vm_actions.create,
        )


class VmActionsResourceWithStreamingResponse:
    def __init__(self, vm_actions: VmActionsResource) -> None:
        self._vm_actions = vm_actions

        self.create = to_streamed_response_wrapper(
            vm_actions.create,
        )


class AsyncVmActionsResourceWithStreamingResponse:
    def __init__(self, vm_actions: AsyncVmActionsResource) -> None:
        self._vm_actions = vm_actions

        self.create = async_to_streamed_response_wrapper(
            vm_actions.create,
        )
