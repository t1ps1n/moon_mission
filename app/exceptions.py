class RobotError(Exception):
    pass


class UnknownAction(RobotError):
    pass


class ObstacleDetected(RobotError):
    pass
