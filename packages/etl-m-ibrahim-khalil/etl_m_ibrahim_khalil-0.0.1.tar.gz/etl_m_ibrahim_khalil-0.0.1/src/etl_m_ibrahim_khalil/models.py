"""Module to store data sources models."""

import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Quote(BaseModel):
    """Model representing a row in the Quotes table"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    author: str
    quote: str
    tags: List[str]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
