# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from ..shared.user import User

__all__ = ["Users"]


class Users(BaseModel):
    count: int

    data: List[User]
