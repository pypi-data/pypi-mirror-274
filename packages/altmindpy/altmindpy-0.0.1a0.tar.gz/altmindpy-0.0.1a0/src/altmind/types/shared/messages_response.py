# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..message import Message
from ..._models import BaseModel

__all__ = ["MessagesResponse"]


class MessagesResponse(BaseModel):
    count: int

    data: List[Message]

    object: Optional[Literal["list"]] = None
