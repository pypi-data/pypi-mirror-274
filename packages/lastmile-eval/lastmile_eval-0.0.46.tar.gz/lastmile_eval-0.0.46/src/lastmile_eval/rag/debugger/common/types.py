"""
Utils file for defining types used in the tracing SDK
"""

from dataclasses import dataclass
from typing import ParamSpec, Optional

from pydantic import BaseModel

T_ParamSpec = ParamSpec("T_ParamSpec")


@dataclass(frozen=True)
class Node(BaseModel):
    """Node used during ingestion"""

    id: str
    title: Optional[str] = None
    text: str


class RetrievedNode(Node):
    """Node used during retrieval that also adds a retrieval score"""

    score: float
