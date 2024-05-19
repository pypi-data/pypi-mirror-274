# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import (
    make_request_options,
)
from ....types.users.me import password_update_params
from ....types.shared.response_message import ResponseMessage

__all__ = ["PasswordResource", "AsyncPasswordResource"]


class PasswordResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PasswordResourceWithRawResponse:
        return PasswordResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PasswordResourceWithStreamingResponse:
        return PasswordResourceWithStreamingResponse(self)

    def update(
        self,
        *,
        current_password: str,
        new_password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResponseMessage:
        """
        Update own password.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._patch(
            "/api/v1/users/me/password",
            body=maybe_transform(
                {
                    "current_password": current_password,
                    "new_password": new_password,
                },
                password_update_params.PasswordUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseMessage,
        )


class AsyncPasswordResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPasswordResourceWithRawResponse:
        return AsyncPasswordResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPasswordResourceWithStreamingResponse:
        return AsyncPasswordResourceWithStreamingResponse(self)

    async def update(
        self,
        *,
        current_password: str,
        new_password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResponseMessage:
        """
        Update own password.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._patch(
            "/api/v1/users/me/password",
            body=await async_maybe_transform(
                {
                    "current_password": current_password,
                    "new_password": new_password,
                },
                password_update_params.PasswordUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseMessage,
        )


class PasswordResourceWithRawResponse:
    def __init__(self, password: PasswordResource) -> None:
        self._password = password

        self.update = to_raw_response_wrapper(
            password.update,
        )


class AsyncPasswordResourceWithRawResponse:
    def __init__(self, password: AsyncPasswordResource) -> None:
        self._password = password

        self.update = async_to_raw_response_wrapper(
            password.update,
        )


class PasswordResourceWithStreamingResponse:
    def __init__(self, password: PasswordResource) -> None:
        self._password = password

        self.update = to_streamed_response_wrapper(
            password.update,
        )


class AsyncPasswordResourceWithStreamingResponse:
    def __init__(self, password: AsyncPasswordResource) -> None:
        self._password = password

        self.update = async_to_streamed_response_wrapper(
            password.update,
        )
