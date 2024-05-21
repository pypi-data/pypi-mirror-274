# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "MessageUpdateParams",
    "Content",
    "ContentTextContent",
    "ContentTextContentText",
    "ContentImageFileContent",
    "ContentImageFileContentImageFile",
    "ContentToolContent",
    "ContentToolContentTool",
]


class MessageUpdateParams(TypedDict, total=False):
    tool_calls: Required[Optional[Iterable[object]]]

    content: Optional[Iterable[Content]]

    message_metadata: object

    role: Optional[Literal["user", "assistant", "system", "tool"]]


class ContentTextContentText(TypedDict, total=False):
    value: Required[str]


class ContentTextContent(TypedDict, total=False):
    text: Required[ContentTextContentText]

    type: Literal["text"]


class ContentImageFileContentImageFile(TypedDict, total=False):
    file_id: Required[str]


class ContentImageFileContent(TypedDict, total=False):
    image_file: Required[ContentImageFileContentImageFile]

    type: Literal["image_file"]


class ContentToolContentTool(TypedDict, total=False):
    content: Optional[object]

    name: Optional[str]

    tool_call_id: Optional[str]


class ContentToolContent(TypedDict, total=False):
    tool: Required[ContentToolContentTool]

    type: Literal["tool_output"]


Content = Union[ContentTextContent, ContentImageFileContent, ContentToolContent]
