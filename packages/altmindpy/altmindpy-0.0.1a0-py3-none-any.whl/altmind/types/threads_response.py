# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .thread import Thread
from .._models import BaseModel

__all__ = ["ThreadsResponse"]


class ThreadsResponse(BaseModel):
    count: int

    data: List[Thread]

    object: Optional[Literal["list"]] = None
