# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .assistant import Assistant

__all__ = ["AssistantsResponse"]


class AssistantsResponse(BaseModel):
    count: int

    data: List[Assistant]

    object: Optional[Literal["list"]] = None
