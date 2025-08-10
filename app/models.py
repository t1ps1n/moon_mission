import enum
import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ActionTypes(enum.Enum):
    MOVE_FORWARD = "F"
    MOVE_BACKWARD = "B"
    ROTATE_LEFT = "L"
    ROTATE_RIGHT = "R"


class Directions(enum.Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


class Statuses(enum.Enum):
    QUEUED = "Q"
    RUNNING = "R"
    COMPLETED = "C"
    FAILED = "F"
    WITHDRAWN = "W"


class Command(Base):
    """
    Represents a command entity consisting of a sequence of actions to be processed.
    """

    __tablename__ = "commands"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command = sa.Column(sa.TEXT, nullable=False)
    status = sa.Column(sa.Enum(Statuses), nullable=False, default=Statuses.QUEUED)

    created = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.now)
    updated = sa.Column(sa.TIMESTAMP, onupdate=datetime.now)

    actions = relationship(
        "Action", back_populates="command", cascade="all, delete-orphan"
    )


class Action(Base):
    """
    Represents a single action derived from a Command,
    tracking its execution status and resulting state.
    """

    __tablename__ = "actions"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_id = sa.Column(
        UUID(as_uuid=True), sa.ForeignKey("commands.id", ondelete="CASCADE")
    )
    type = sa.Column(sa.Enum(ActionTypes), nullable=False)
    status = sa.Column(sa.Enum(Statuses), nullable=False, default=Statuses.QUEUED)

    x_coord = sa.Column(sa.Integer, nullable=True)
    y_coord = sa.Column(sa.Integer, nullable=True)
    direction = sa.Column(sa.Enum(Directions), nullable=True)

    created = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.now)
    updated = sa.Column(sa.TIMESTAMP, onupdate=datetime.now)

    command = relationship("Command", back_populates="actions")
