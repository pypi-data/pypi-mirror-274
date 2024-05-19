# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["User"]


class User(BaseModel):
    id: int

    email: str

    full_name: Optional[str] = None

    is_active: Optional[bool] = None

    is_superuser: Optional[bool] = None
