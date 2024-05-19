# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "Message",
    "Content",
    "ContentTextContent",
    "ContentTextContentText",
    "ContentImageFileContent",
    "ContentImageFileContentImageFile",
]


class ContentTextContentText(BaseModel):
    value: str


class ContentTextContent(BaseModel):
    text: ContentTextContentText

    type: Optional[Literal["text"]] = None


class ContentImageFileContentImageFile(BaseModel):
    file_id: str


class ContentImageFileContent(BaseModel):
    image_file: ContentImageFileContentImageFile

    type: Optional[Literal["image_file"]] = None


Content = Union[ContentTextContent, ContentImageFileContent]


class Message(BaseModel):
    id: int

    content: List[Content]

    created_at: int

    original_role: Optional[Literal["user", "assistant", "system", "tool"]] = None

    message_metadata: Optional[object] = None

    object: Optional[Literal["message"]] = None

    role: Optional[Literal["user", "assistant", "system", "tool"]] = None

    thread_id: Optional[int] = None
