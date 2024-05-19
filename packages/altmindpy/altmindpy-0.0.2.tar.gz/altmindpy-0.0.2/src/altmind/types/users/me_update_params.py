# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["MeUpdateParams"]


class MeUpdateParams(TypedDict, total=False):
    email: Optional[str]

    full_name: Optional[str]
