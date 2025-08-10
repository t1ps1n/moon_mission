import unittest
from unittest.mock import Mock

from models import Action, ActionTypes, Directions
from robot import Robot


class RobotRotateLeftTests(unittest.TestCase):

    def setUp(self):
        self.action = Mock(spec=Action)
        self.action.type = ActionTypes("L")

    def test_rotate_left_north(self):
        robot = Robot(0, 0, Directions("N"))
        robot.process_action(self.action)
        self.assertEqual(robot.direction, Directions("W"))

    def test_rotate_left_west(self):
        robot = Robot(0, 0, Directions("W"))
        robot.process_action(self.action)
        self.assertEqual(robot.direction, Directions("S"))

    def test_rotate_left_south(self):
        robot = Robot(0, 0, Directions("S"))
        robot.process_action(self.action)
        self.assertEqual(robot.direction, Directions("E"))

    def test_rotate_left_east(self):
        robot = Robot(0, 0, Directions("E"))
        robot.process_action(self.action)
        self.assertEqual(robot.direction, Directions("N"))


class RobotRotateRightTests(unittest.TestCase):

    def setUp(self):
        self.action = Mock(spec=Action)
        self.action.type = ActionTypes("R")

    def test_rotate_right_north(self):
        robot = Robot(0, 0, Directions("N"))
        robot.process_action(self.action)
        self.assertEqual(robot._direction, Directions("E"))

    def test_rotate_right_east(self):
        robot = Robot(0, 0, Directions("E"))
        robot.process_action(self.action)
        self.assertEqual(robot._direction, Directions("S"))

    def test_rotate_right_south(self):
        robot = Robot(0, 0, Directions("S"))
        robot.process_action(self.action)
        self.assertEqual(robot._direction, Directions("W"))

    def test_rotate_right_west(self):
        robot = Robot(0, 0, Directions("W"))
        robot.process_action(self.action)
        self.assertEqual(robot._direction, Directions("N"))


class RobotMoveForwardTests(unittest.TestCase):

    def setUp(self):
        self.action = Mock(spec=Action)
        self.action.type = ActionTypes("F")

    def test_move_forward_north(self):
        robot = Robot(0, 0, Directions("N"))
        robot.process_action(self.action)
        self.assertEqual(robot.direction, Directions("N"))
        self.assertEqual(robot.x, 0)
        self.assertEqual(robot.y, 1)

    def test_move_forward_east(self):
        robot = Robot(0, 0, Directions("E"))
        robot.process_action(self.action)
        self.assertEqual(robot.direction, Directions("E"))
        self.assertEqual(robot.x, 1)
        self.assertEqual(robot.y, 0)

    def test_move_forward_south(self):
        robot = Robot(0, 0, Directions("S"))
        robot.process_action(self.action)
        self.assertEqual(robot.direction, Directions("S"))
        self.assertEqual(robot.x, 0)
        self.assertEqual(robot.y, -1)

    def test_move_forward_west(self):
        robot = Robot(0, 0, Directions("W"))
        robot.process_action(self.action)
        self.assertEqual(robot.direction, Directions("W"))
        self.assertEqual(robot.x, -1)
        self.assertEqual(robot.y, 0)


class RobotMoveBackwardTests(unittest.TestCase):

    def setUp(self):
        self.action = Mock(spec=Action)
        self.action.type = ActionTypes("B")

    def test_move_backward_north(self):
        robot = Robot(0, 0, Directions("N"))
        robot.process_action(self.action)
        self.assertEqual(robot._direction, Directions("N"))
        self.assertEqual(robot._x, 0)
        self.assertEqual(robot._y, -1)

    def test_move_backward_east(self):
        robot = Robot(0, 0, Directions("E"))
        robot.process_action(self.action)
        self.assertEqual(robot._direction, Directions("E"))
        self.assertEqual(robot._x, -1)
        self.assertEqual(robot._y, 0)

    def test_move_backward_south(self):
        robot = Robot(0, 0, Directions("S"))
        robot.process_action(self.action)
        self.assertEqual(robot._direction, Directions("S"))
        self.assertEqual(robot._x, 0)
        self.assertEqual(robot._y, 1)

    def test_move_backward_west(self):
        robot = Robot(0, 0, Directions("W"))
        robot.process_action(self.action)
        self.assertEqual(robot._direction, Directions("W"))
        self.assertEqual(robot._x, 1)
        self.assertEqual(robot._y, 0)
