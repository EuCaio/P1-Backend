
import uuid
from datetime import datetime
from dataclasses import dataclass, field

@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_on: datetime = field(default_factory=datetime.now)

