from typing import Optional

from models import Directions, Statuses
from pydantic import UUID4, BaseModel


class CommandRequest(BaseModel):
    command: str


class CommandResponse(BaseModel):
    id: UUID4


class RobotStatus(BaseModel):
    x: int
    y: int
    direction: Directions
    status: Statuses
    command_id: Optional[UUID4] = None
