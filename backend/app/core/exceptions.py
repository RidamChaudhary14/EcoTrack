from typing import Optional

class DatabaseError(Exception):
    """Base exception for all database-related errors."""
    pass

class NotFoundError(DatabaseError):
    """Raised when an entity is not found in the database."""
    def __init__(self, entity_name: str, entity_id: Optional[str] = None):
        self.entity_name = entity_name
        self.entity_id = entity_id
        msg = f"{entity_name} not found"
        if entity_id:
            msg += f" (ID: {entity_id})"
        super().__init__(msg)

class IntegrityError(DatabaseError):
    """Raised when a database integrity constraint is violated."""
    pass
