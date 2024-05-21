# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .password import (
    PasswordResource,
    AsyncPasswordResource,
    PasswordResourceWithRawResponse,
    AsyncPasswordResourceWithRawResponse,
    PasswordResourceWithStreamingResponse,
    AsyncPasswordResourceWithStreamingResponse,
)
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
from ....types.users import me_update_params
from ...._base_client import (
    make_request_options,
)
from ....types.shared.user_out import UserOut

__all__ = ["MeResource", "AsyncMeResource"]


class MeResource(SyncAPIResource):
    @cached_property
    def password(self) -> PasswordResource:
        return PasswordResource(self._client)

    @cached_property
    def with_raw_response(self) -> MeResourceWithRawResponse:
        return MeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MeResourceWithStreamingResponse:
        return MeResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserOut:
        """Get current user."""
        return self._get(
            "/api/v1/users/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserOut,
        )

    def update(
        self,
        *,
        email: Optional[str] | NotGiven = NOT_GIVEN,
        full_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserOut:
        """
        Update own user.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._patch(
            "/api/v1/users/me",
            body=maybe_transform(
                {
                    "email": email,
                    "full_name": full_name,
                },
                me_update_params.MeUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserOut,
        )


class AsyncMeResource(AsyncAPIResource):
    @cached_property
    def password(self) -> AsyncPasswordResource:
        return AsyncPasswordResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMeResourceWithRawResponse:
        return AsyncMeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMeResourceWithStreamingResponse:
        return AsyncMeResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserOut:
        """Get current user."""
        return await self._get(
            "/api/v1/users/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserOut,
        )

    async def update(
        self,
        *,
        email: Optional[str] | NotGiven = NOT_GIVEN,
        full_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserOut:
        """
        Update own user.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._patch(
            "/api/v1/users/me",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "full_name": full_name,
                },
                me_update_params.MeUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserOut,
        )


class MeResourceWithRawResponse:
    def __init__(self, me: MeResource) -> None:
        self._me = me

        self.retrieve = to_raw_response_wrapper(
            me.retrieve,
        )
        self.update = to_raw_response_wrapper(
            me.update,
        )

    @cached_property
    def password(self) -> PasswordResourceWithRawResponse:
        return PasswordResourceWithRawResponse(self._me.password)


class AsyncMeResourceWithRawResponse:
    def __init__(self, me: AsyncMeResource) -> None:
        self._me = me

        self.retrieve = async_to_raw_response_wrapper(
            me.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            me.update,
        )

    @cached_property
    def password(self) -> AsyncPasswordResourceWithRawResponse:
        return AsyncPasswordResourceWithRawResponse(self._me.password)


class MeResourceWithStreamingResponse:
    def __init__(self, me: MeResource) -> None:
        self._me = me

        self.retrieve = to_streamed_response_wrapper(
            me.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            me.update,
        )

    @cached_property
    def password(self) -> PasswordResourceWithStreamingResponse:
        return PasswordResourceWithStreamingResponse(self._me.password)


class AsyncMeResourceWithStreamingResponse:
    def __init__(self, me: AsyncMeResource) -> None:
        self._me = me

        self.retrieve = async_to_streamed_response_wrapper(
            me.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            me.update,
        )

    @cached_property
    def password(self) -> AsyncPasswordResourceWithStreamingResponse:
        return AsyncPasswordResourceWithStreamingResponse(self._me.password)
