
import uuid
from typing import Optional, Dict, Any, List
from shared.domain_event import DomainEvent
from domain.category_events import CategoryCreated, CategoryUpdated, CategoryActivated, CategoryDeactivated

MAX_NAME = 255

class Category:
    def __init__(
        self,
        name: str,
        description: str = "",
        is_active: bool = True,
        id: Optional[str] = None
    ):
        self.id = id or str(uuid.uuid4())
        self._domain_events: List[DomainEvent] = []

        self.name = self._validate_name(name)
        self.description = description or ""
        self.is_active = bool(is_active)

        if id is None:
            self._add_domain_event(CategoryCreated(
                category_id=self.id,
                name=self.name,
                description=self.description,
                is_active=self.is_active
            ))

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise TypeError("O nome deve ser uma string.")
        n = name.strip()
        if not n:
            raise ValueError("O nome é obrigatório.")
        if len(n) > MAX_NAME:
            raise ValueError(f"O nome deve ter no máximo {MAX_NAME} caracteres.")
        return n

    def update(self, *, name: Optional[str] = None, description: Optional[str] = None) -> None:
        old_name = self.name
        old_description = self.description
        updated = False

        if name is not None and name != self.name:
            self.name = self._validate_name(name)
            updated = True
        if description is not None and description != self.description:
            self.description = description
            updated = True

        if updated:
            self._add_domain_event(CategoryUpdated(
                category_id=self.id,
                old_name=old_name,
                new_name=self.name,
                old_description=old_description,
                new_description=self.description
            ))

    def activate(self) -> None:
        if not self.is_active:
            self.is_active = True
            self._add_domain_event(CategoryActivated(category_id=self.id))

    def deactivate(self) -> None:
        if self.is_active:
            self.is_active = False
            self._add_domain_event(CategoryDeactivated(category_id=self.id))








    def _add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def clear_domain_events(self) -> List[DomainEvent]:
        events = self._domain_events[:]
        self._domain_events.clear()
        return events

    def to_dict(self) -> Dict[str, Any]:
        return {
            "class_name": self.__class__.__name__,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Category":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            is_active=data["is_active"],
        )

    def __str__(self) -> str:
        return f'{self.name} | {self.description} ({"Ativa" if self.is_active else "Inativa"}) | ID: {self.id}'

    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.id})>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Category):
            return False
        return self.id == other.id

