"""Data models for the task manager."""

from datetime import datetime
from enum import Enum
from typing import Dict, Any
from dataclasses import dataclass, asdict
import uuid


class TaskStatus(Enum):
    """Task status enumeration."""

    PENDING = "pending"
    COMPLETED = "completed"


class Priority(Enum):
    """Task priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """Task data model."""

    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    created_at: datetime = None
    completed_at: datetime = None

    def __post_init__(self):
        """Initialize computed fields."""
        if self.created_at is None:
            self.created_at = datetime.now()

    @classmethod
    def create(
        cls, title: str, description: str = "", priority: Priority = Priority.MEDIUM
    ) -> "Task":
        """Create a new task with generated ID."""
        return cls(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority,
        )

    def complete(self) -> None:
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        data = asdict(self)
        # Convert enums to strings
        data["status"] = self.status.value
        data["priority"] = self.priority.value
        # Convert datetime to ISO format
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        data["completed_at"] = (
            self.completed_at.isoformat() if self.completed_at else None
        )
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task from dictionary."""
        # Convert strings back to enums
        data["status"] = TaskStatus(data["status"])
        data["priority"] = Priority(data["priority"])
        # Convert ISO strings back to datetime
        if data["created_at"]:
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data["completed_at"]:
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])
        return cls(**data)
