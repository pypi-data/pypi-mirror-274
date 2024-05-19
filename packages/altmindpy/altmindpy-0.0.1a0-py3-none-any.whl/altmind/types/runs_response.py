# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .run import Run
from .._models import BaseModel

__all__ = ["RunsResponse"]


class RunsResponse(BaseModel):
    count: int

    data: List[Run]

    object: Optional[Literal["list"]] = None
