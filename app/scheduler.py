import asyncio
import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import async_sessionmaker
from exceptions import RobotError
from models import Action, ActionTypes, Command, Statuses
from robot import Robot
from sqlalchemy import asc, select, update
from utils import get_current_position

logger = logging.getLogger("worker_logger")


async def process_actions():
    """
    Processes all queued Actions by executing their commands sequentially.

    The function retrieves the robot's current position, then selects all Actions
    with status QUEUED, ordered by creation time. For each Action:
      - Sets its status to RUNNING and commits.
      - Attempts to process the command using the Robot instance.
      - If processing fails with a RobotError, marks the Action as FAILED, updates
        the robot's position in the Action, and raises the error.
      - If processing succeeds, marks the Action as COMPLETED and updates its position.

    If any RobotError occurs during processing, all remaining QUEUED Actions and Commands
    are marked as WITHDRAWN, and the changes are committed.

    Returns:
        None
    """
    logger.info("Starting processing of queued actions.")

    async with async_sessionmaker() as async_session:
        x, y, direction, _, _ = await get_current_position(async_session)
        robot = Robot(x_coord=x, y_coord=y, direction=direction)

        query = (
            select(Action)
            .where(Action.status == Statuses.QUEUED)
            .order_by(asc(Action.created))
        )
        result = await async_session.execute(query)
        actions = result.scalars()

        try:
            for action in actions:
                action.status = Statuses.RUNNING
                await async_session.commit()

                try:
                    robot.process_action(action)
                except RobotError as e:
                    logger.error(f"{type(e)} while processing action ID {action.id}")
                    action.status = Statuses.FAILED
                    action.x_coord = robot.x
                    action.y_coord = robot.y
                    action.direction = robot.direction
                    raise e
                else:
                    action.status = Statuses.COMPLETED
                    action.x_coord = robot.x
                    action.y_coord = robot.y
                    action.direction = robot.direction
                    await async_session.commit()

                    logger.info(
                        f"Action ID {action.id} completed successfully. Updated robot position."
                    )
        except RobotError:
            logger.warning(
                "RobotError occurred, withdrawing remaining queued actions and commands."
            )
            query = (
                update(Action)
                .where(Action.status == Statuses.QUEUED)
                .values(status=Statuses.WITHDRAWN)
            )
            await async_session.execute(query)

            query = (
                update(Command)
                .where(Command.status == Statuses.QUEUED)
                .values(status=Statuses.WITHDRAWN)
            )
            await async_session.execute(query)

            await async_session.commit()
            logger.info(
                "All remaining queued actions and commands marked as WITHDRAWN."
            )

    logger.info("Completed processing of queued actions.")


async def parse_commands():
    """
    Parses queued Command records into individual Actions and updates their status.

    The function fetches all Commands with status QUEUED, ordered by creation time.
    For each Command:
      - Iterates over its command string, creating an Action for each action character.
      - Associates each Action with the Command by command_id.
      - Marks the Command as COMPLETED after parsing all actions.

    Finally, commits all changes to the database.

    Returns:
        None
    """
    logger.info("Starting parsing of queued commands.")

    async with async_sessionmaker() as async_session:
        query = (
            select(Command)
            .where(Command.status == Statuses.QUEUED)
            .order_by(asc(Command.created))
        )
        result = await async_session.execute(query)
        result = result.scalars()

        for item in result:
            for action in item.command:
                command = Action(type=ActionTypes(action), command_id=item.id)
                async_session.add(command)

            item.status = Statuses.COMPLETED
            await async_session.commit()
            logger.debug(f"Parsed actions for command ID {item.id}.")

    logger.info("Completed parsing of queued commands.")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        process_actions,
        "interval",
        seconds=30,
        max_instances=1,
        coalesce=True,
        next_run_time=datetime.datetime.now(),
    )
    scheduler.add_job(
        parse_commands,
        "interval",
        seconds=30,
        max_instances=1,
        coalesce=True,
        next_run_time=datetime.datetime.now(),
    )
    scheduler.start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
