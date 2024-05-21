# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["RunResponse"]


class RunResponse(BaseModel):
    id: int

    additional_instructions: Optional[str] = None

    assistant_id: Optional[int] = None

    created_at: int

    instructions: Optional[str] = None

    required_action: Optional[object] = None

    status: Literal["queued", "in_progress", "completed", "requires_action", "expired", "cancelled", "failed"]

    thread_id: Optional[int] = None

    timeline: Optional[Dict[str, int]] = None

    type: Literal["default", "analysis", "execution"]

    usage: Optional[Dict[str, int]] = None

    model: Optional[str] = None

    object: Optional[Literal["run"]] = None

    run_metadata: Optional[builtins.object] = None
