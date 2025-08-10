from data_classes import CommandRequest
from models import Action, Command, Directions, Statuses
from settings import START_DIRECTION, START_POSITION
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_position(async_session: AsyncSession):
    """
    Retrieves the most recent Action with status RUNNING, FAILED, or COMPLETED,
    ordered by the latest update time, and returns its position and state.

    If no such Action exists, returns the default start position, direction, and status.

    Args:
        async_session: The asynchronous SQLAlchemy session for database access.

    Returns:
        tuple: A tuple containing (x_coord: int, y_coord: int, direction: Directions, status: Statuses).
    """
    x, y, direction, status, command_id = None, None, None, None, None

    query = (
        select(Action)
        .where(
            Action.status.in_([Statuses.RUNNING, Statuses.FAILED, Statuses.COMPLETED])
        )
        .order_by(desc(Action.updated))
        .limit(1)
    )
    result = await async_session.execute(query)
    action = result.scalar_one_or_none()
    if action:
        x = action.x_coord
        y = action.y_coord
        direction = action.direction
        status = action.status
        command_id = action.command_id

    x = x if x is not None else START_POSITION[0]
    y = y if y is not None else START_POSITION[1]
    direction = direction or Directions(START_DIRECTION)
    status = status or Statuses.COMPLETED

    return x, y, direction, status, command_id


async def add_command(async_session: AsyncSession, command: CommandRequest) -> Command:
    """
    Adds a new Command record to the database.

    Args:
        async_session: The SQLAlchemy asynchronous session used for DB operations.
        command: The data object containing command details to be saved.

    Returns:
        Command: The newly created Command instance with updated fields from the database.
    """
    command = Command(command=command.command)
    async_session.add(command)
    await async_session.commit()
    await async_session.refresh(command)
    return command
