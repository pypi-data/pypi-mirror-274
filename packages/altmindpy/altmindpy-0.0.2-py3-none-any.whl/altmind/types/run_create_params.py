# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["RunCreateParams"]


class RunCreateParams(TypedDict, total=False):
    assistant_id: Required[Optional[int]]

    thread_id: Required[Optional[int]]

    stream: bool

    additional_instructions: Optional[str]
    """Additional instructions for this run, appended to the assistant instructions"""

    instructions: Optional[str]
    """Override the assistant instructions for this run"""

    model: Optional[str]
    """Override the assistant model for this run"""

    run_metadata: object

    type: Literal["default", "analysis", "execution"]
