from dataclasses import dataclass

from app.models.enums import Role


@dataclass(frozen=True)
class Principal:
    """Who is calling. Never carries the key itself, only its database id."""

    role: Role
    key_id: int | None = None


PUBLIC = Principal(Role.PUBLIC)
