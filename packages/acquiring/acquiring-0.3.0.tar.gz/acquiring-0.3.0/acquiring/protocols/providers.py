from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Generic, Optional, Protocol, TypeVar
from uuid import UUID

from acquiring.protocols import storage

Status = TypeVar("Status", bound=StrEnum)


@dataclass(match_args=False)
class AdapterResponse(Generic[Status], Protocol):
    external_id: Optional[str]  # UUID cannot be imposed across all adapters
    timestamp: Optional[datetime]
    raw_data: dict
    status: Status


@dataclass
class Adapter(Protocol):
    base_url: str
    provider_name: str
    transaction_repository: storage.Repository


@dataclass
class Transaction(Protocol):
    external_id: str
    timestamp: datetime
    raw_data: dict
    provider_name: str
    payment_method_id: UUID

    def __repr__(self) -> str: ...
