from exceptions import ObstacleDetected, UnknownAction
from models import Action, ActionTypes, Directions
from settings import OBSTACLES


class Robot:

    LEFT_ROTATION = {
        Directions.NORTH: Directions.WEST,
        Directions.SOUTH: Directions.EAST,
        Directions.WEST: Directions.SOUTH,
        Directions.EAST: Directions.NORTH,
    }
    RIGHT_ROTATION = {
        Directions.NORTH: Directions.EAST,
        Directions.SOUTH: Directions.WEST,
        Directions.WEST: Directions.NORTH,
        Directions.EAST: Directions.SOUTH,
    }
    MOVE_FORWARD = {
        Directions.NORTH: {"x": 0, "y": 1},
        Directions.SOUTH: {"x": 0, "y": -1},
        Directions.WEST: {"x": -1, "y": 0},
        Directions.EAST: {"x": 1, "y": 0},
    }
    MOVE_BACKWARD = {
        Directions.NORTH: {"x": 0, "y": -1},
        Directions.SOUTH: {"x": 0, "y": 1},
        Directions.WEST: {"x": 1, "y": 0},
        Directions.EAST: {"x": -1, "y": 0},
    }

    def __init__(self, x_coord: int, y_coord: int, direction: Directions):
        self._x = x_coord
        self._y = y_coord
        self._direction = direction

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def direction(self):
        return self._direction

    def _move_robot(self, changes):
        x = self._x + changes["x"]
        y = self._y + changes["y"]
        if (x, y) in OBSTACLES:
            raise ObstacleDetected(f"Obstacle detected: ({x}, {y})")
        self._x = x
        self._y = y

    def process_action(self, action: Action):
        if action.type == ActionTypes.ROTATE_LEFT:
            self._direction = self.LEFT_ROTATION[self._direction]
        elif action.type == ActionTypes.ROTATE_RIGHT:
            self._direction = self.RIGHT_ROTATION[self._direction]
        elif action.type == ActionTypes.MOVE_FORWARD:
            changes = self.MOVE_FORWARD[self._direction]
            self._move_robot(changes)
        elif action.type == ActionTypes.MOVE_BACKWARD:
            changes = self.MOVE_BACKWARD[self._direction]
            self._move_robot(changes)
        else:
            raise UnknownAction(f"Unknown action: {action.type}.")
