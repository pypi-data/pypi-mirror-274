# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.users import open_create_params
from ..._base_client import (
    make_request_options,
)
from ...types.shared.user_out import UserOut

__all__ = ["OpenResource", "AsyncOpenResource"]


class OpenResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OpenResourceWithRawResponse:
        return OpenResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OpenResourceWithStreamingResponse:
        return OpenResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        email: str,
        password: str,
        full_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserOut:
        """
        Create new user without the need to be logged in.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/users/open",
            body=maybe_transform(
                {
                    "email": email,
                    "password": password,
                    "full_name": full_name,
                },
                open_create_params.OpenCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserOut,
        )


class AsyncOpenResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOpenResourceWithRawResponse:
        return AsyncOpenResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOpenResourceWithStreamingResponse:
        return AsyncOpenResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        email: str,
        password: str,
        full_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserOut:
        """
        Create new user without the need to be logged in.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/users/open",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "password": password,
                    "full_name": full_name,
                },
                open_create_params.OpenCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserOut,
        )


class OpenResourceWithRawResponse:
    def __init__(self, open: OpenResource) -> None:
        self._open = open

        self.create = to_raw_response_wrapper(
            open.create,
        )


class AsyncOpenResourceWithRawResponse:
    def __init__(self, open: AsyncOpenResource) -> None:
        self._open = open

        self.create = async_to_raw_response_wrapper(
            open.create,
        )


class OpenResourceWithStreamingResponse:
    def __init__(self, open: OpenResource) -> None:
        self._open = open

        self.create = to_streamed_response_wrapper(
            open.create,
        )


class AsyncOpenResourceWithStreamingResponse:
    def __init__(self, open: AsyncOpenResource) -> None:
        self._open = open

        self.create = async_to_streamed_response_wrapper(
            open.create,
        )
