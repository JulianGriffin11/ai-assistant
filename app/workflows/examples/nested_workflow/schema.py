from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class NestedWorkflowEventSchema(BaseModel):
    ticket_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    from_email: str
    sender: str
    subject: str
    body: str
