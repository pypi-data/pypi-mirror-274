# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .stream import (
    StreamResource,
    AsyncStreamResource,
    StreamResourceWithRawResponse,
    AsyncStreamResourceWithRawResponse,
    StreamResourceWithStreamingResponse,
    AsyncStreamResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["ExperimentalResource", "AsyncExperimentalResource"]


class ExperimentalResource(SyncAPIResource):
    @cached_property
    def stream(self) -> StreamResource:
        return StreamResource(self._client)

    @cached_property
    def with_raw_response(self) -> ExperimentalResourceWithRawResponse:
        return ExperimentalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExperimentalResourceWithStreamingResponse:
        return ExperimentalResourceWithStreamingResponse(self)


class AsyncExperimentalResource(AsyncAPIResource):
    @cached_property
    def stream(self) -> AsyncStreamResource:
        return AsyncStreamResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncExperimentalResourceWithRawResponse:
        return AsyncExperimentalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExperimentalResourceWithStreamingResponse:
        return AsyncExperimentalResourceWithStreamingResponse(self)


class ExperimentalResourceWithRawResponse:
    def __init__(self, experimental: ExperimentalResource) -> None:
        self._experimental = experimental

    @cached_property
    def stream(self) -> StreamResourceWithRawResponse:
        return StreamResourceWithRawResponse(self._experimental.stream)


class AsyncExperimentalResourceWithRawResponse:
    def __init__(self, experimental: AsyncExperimentalResource) -> None:
        self._experimental = experimental

    @cached_property
    def stream(self) -> AsyncStreamResourceWithRawResponse:
        return AsyncStreamResourceWithRawResponse(self._experimental.stream)


class ExperimentalResourceWithStreamingResponse:
    def __init__(self, experimental: ExperimentalResource) -> None:
        self._experimental = experimental

    @cached_property
    def stream(self) -> StreamResourceWithStreamingResponse:
        return StreamResourceWithStreamingResponse(self._experimental.stream)


class AsyncExperimentalResourceWithStreamingResponse:
    def __init__(self, experimental: AsyncExperimentalResource) -> None:
        self._experimental = experimental

    @cached_property
    def stream(self) -> AsyncStreamResourceWithStreamingResponse:
        return AsyncStreamResourceWithStreamingResponse(self._experimental.stream)
